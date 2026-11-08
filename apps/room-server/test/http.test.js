import assert from 'node:assert/strict';
import { test } from 'node:test';
import { handleRequest } from '../src/http.js';

test('GET /healthz reports liveness', () => {
  const response = {
    writeHead(status, headers) { this.status = status; this.headers = headers; },
    end(body) { this.body = body; },
  };
  handleRequest({ method: 'GET', url: '/healthz' }, response);
  assert.equal(response.status, 200);
  assert.equal(response.body, 'ok\n');
});
