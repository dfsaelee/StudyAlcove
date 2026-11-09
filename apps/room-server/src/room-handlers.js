import { fail, handleCreate, json } from './http-helpers.js';

// Room codes are 80 random bits, represented by 20 hexadecimal characters.
export function normalizeRoomCode(code) {
  return /^[0-9a-fA-F]{20}$/.test(code) ? code.toUpperCase() : null;
}

export function findRoom(response, store, rawCode) {
  const code = normalizeRoomCode(rawCode);
  if (!code) return fail(response, 400, 'invalid_room_code', 'Room code must be 20 hexadecimal characters');
  const room = store.findRoom(code);
  if (!room) return fail(response, 404, 'room_not_found', 'Room not found');
  return json(response, 200, room);
}

export function createRoom(request, response, store) {
  return handleCreate(request, response, 'name', (name) => store.createRoom(name));
}
