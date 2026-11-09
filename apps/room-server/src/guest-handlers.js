import { handleCreate } from './http-helpers.js';

export function createGuest(request, response, store) {
  return handleCreate(request, response, 'displayName', (name) => store.createGuest(name));
}
