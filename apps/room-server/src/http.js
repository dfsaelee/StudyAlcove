import { createStore } from './store.js';
import { fail } from './http-helpers.js';
import { createGuest } from './guest-handlers.js';
import { createRoom, findRoom } from './room-handlers.js';

export { normalizeRoomCode } from './room-handlers.js';

const defaultStore = createStore();

export function createHandler(store = createStore()) {
  return function handleRequest(request, response) {
    const path = request.url?.split('?')[0];
    if (path === '/healthz' || path === '/readyz') {
      if (request.method !== 'GET') {
        response.writeHead(405, { Allow: 'GET' });
        response.end();
      } else {
        response.writeHead(200, { 'Content-Type': 'text/plain; charset=utf-8' });
        response.end(path === '/healthz' ? 'ok\n' : 'ready\n');
      }
      return;
    }

    const collection = path === '/api/guests' ? 'guest' : path === '/api/rooms' ? 'room' : null;
    const roomMatch = /^\/api\/rooms\/([^/]+)$/.exec(path || '');
    if (!collection && !roomMatch) {
      fail(response, 404, 'not_found', 'Resource not found');
      return;
    }
    const allowed = collection ? 'POST' : 'GET';
    if (request.method !== allowed) {
      fail(response, 405, 'method_not_allowed', 'Method not allowed', { Allow: allowed });
      return;
    }
    if (roomMatch) {
      return findRoom(response, store, roomMatch[1]);
    }
    return collection === 'guest'
      ? createGuest(request, response, store)
      : createRoom(request, response, store);
  };
}

// Keep the existing entry point for the running service and health test.
export const handleRequest = createHandler(defaultStore);
