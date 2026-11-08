import assert from 'node:assert/strict';
import { test } from 'node:test';
import { loadConfig } from '../src/config.js';

test('listen address defaults to local port 8080', () => {
  assert.deepEqual(loadConfig({}), { host: '127.0.0.1', port: 8080 });
});

test('listen address accepts an IPv6 host and validates its port', () => {
  assert.deepEqual(loadConfig({ LISTEN_ADDR: '[::1]:3000' }), { host: '::1', port: 3000 });
  for (const value of ['localhost', 'localhost:0', 'localhost:65536', 'localhost:not-a-port']) {
    assert.throws(() => loadConfig({ LISTEN_ADDR: value }), /LISTEN_ADDR/);
  }
});
