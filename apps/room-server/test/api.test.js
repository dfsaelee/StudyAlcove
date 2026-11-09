import assert from 'node:assert/strict';
import { Readable } from 'node:stream';
import { test } from 'node:test';
import { createHandler } from '../src/http.js';
import { createStore } from '../src/store.js';

function call(handler, method, url, body, contentType = 'application/json') {
  return new Promise((resolve) => {
    const request = Readable.from(body === undefined ? [] : [Buffer.from(body)]);
    request.method = method;
    request.url = url;
    request.headers = { 'content-type': contentType };
    const response = {
      writeHead(status, headers = {}) { this.status = status; this.headers = headers; },
      end(data = '') { resolve({ status: this.status, headers: this.headers, body: data }); },
    };
    handler(request, response);
  });
}
const parse = (result) => JSON.parse(result.body);

test('creates guest and room, then retrieves public metadata', async () => {
  const handler = createHandler();
  const guest = await call(handler, 'POST', '/api/guests', JSON.stringify({ displayName: ' Robin ' }));
  assert.equal(guest.status, 201);
  assert.equal(parse(guest).displayName, 'Robin');
  assert.match(parse(guest).credential, /^[A-Za-z0-9_-]{43}$/);
  assert.equal(guest.headers['Cache-Control'], 'no-store');
  const created = await call(handler, 'POST', '/api/rooms', JSON.stringify({ name: 'Library' }));
  assert.equal(created.status, 201);
  const room = parse(created);
  assert.match(room.code, /^[0-9A-F]{20}$/);
  const read = await call(handler, 'GET', `/api/rooms/${room.code.toLowerCase()}`);
  assert.equal(read.status, 200);
  assert.deepEqual(parse(read), room);
  assert.equal(read.body.includes(parse(guest).credential), false);
  assert.equal((await call(handler, 'GET', '/api/rooms/00000000000000000000')).status, 404);
});

test('rejects invalid requests, bodies and names', async () => {
  const handler = createHandler();
  assert.equal((await call(handler, 'GET', '/api/rooms')).status, 405);
  assert.equal((await call(handler, 'GET', '/api/unknown')).status, 404);
  assert.equal((await call(handler, 'POST', '/api/rooms', '{')).status, 400);
  assert.equal((await call(handler, 'POST', '/api/rooms', '[]')).status, 400);
  assert.equal((await call(handler, 'POST', '/api/rooms', '{}', 'text/plain')).status, 415);
  assert.equal((await call(handler, 'POST', '/api/rooms', 'x'.repeat(16385))).status, 413);
  for (const name of ['', '   ', 'a'.repeat(33), 'bad\nname', 42]) {
    assert.equal((await call(handler, 'POST', '/api/rooms', JSON.stringify({ name }))).status, 400);
  }
  assert.equal((await call(handler, 'POST', '/api/guests', JSON.stringify({ displayName: '' }))).status, 400);
});

test('enforces capacity and bounded collision retries', async () => {
  const fixed = 'AAAAAAAAAAAAAAAAAAAA';
  const store = createStore({ maxGuests: 1, maxRooms: 2, makeId: () => 'same', makeCode: () => fixed });
  const handler = createHandler(store);
  assert.equal((await call(handler, 'POST', '/api/guests', '{"displayName":"Robin"}')).status, 201);
  assert.equal((await call(handler, 'POST', '/api/guests', '{"displayName":"Robin"}')).status, 503);
  assert.equal((await call(handler, 'POST', '/api/rooms', '{"name":"Library"}')).status, 201);
  assert.equal((await call(handler, 'POST', '/api/rooms', '{"name":"Library"}')).status, 503);
  const full = createHandler(createStore({ maxRooms: 0 }));
  assert.equal((await call(full, 'POST', '/api/rooms', '{"name":"Library"}')).status, 503);
});

test('concurrent room requests produce distinct codes', async () => {
  const handler = createHandler();
  const results = await Promise.all(Array.from({ length: 50 }, () =>
    call(handler, 'POST', '/api/rooms', '{"name":"Library"}')));
  assert.ok(results.every((result) => result.status === 201));
  assert.equal(new Set(results.map((result) => parse(result).code)).size, 50);
});

test('retries generated identifier collisions without overwriting existing records', () => {
  const ids = ['id-1', 'id-1', 'id-2'];
  const codes = ['AAAAAAAAAAAAAAAAAAAA', 'AAAAAAAAAAAAAAAAAAAA', 'BBBBBBBBBBBBBBBBBBBB'];
  const store = createStore({ makeId: () => ids.shift(), makeCode: () => codes.shift() });
  assert.equal(store.createGuest('First').guestId, 'id-1');
  assert.equal(store.createGuest('Second').guestId, 'id-2');
  const first = store.createRoom('First');
  const second = store.createRoom('Second');
  assert.equal(second.code, 'BBBBBBBBBBBBBBBBBBBB');
  assert.equal(store.findRoom(first.code).name, 'First');
});

test('preserves API error codes and method headers', async () => {
  const handler = createHandler();
  const wrongMethod = await call(handler, 'GET', '/api/guests');
  assert.equal(wrongMethod.status, 405);
  assert.equal(wrongMethod.headers.Allow, 'POST');
  assert.equal(parse(wrongMethod).error.code, 'method_not_allowed');
  const invalidCode = await call(handler, 'GET', '/api/rooms/not-a-code');
  assert.equal(invalidCode.status, 400);
  assert.equal(parse(invalidCode).error.code, 'invalid_room_code');
  const wrongType = await call(handler, 'POST', '/api/guests', '{}', 'text/plain');
  assert.equal(wrongType.status, 415);
  assert.equal(parse(wrongType).error.code, 'unsupported_media_type');
});
