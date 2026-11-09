import { createHash, randomBytes, randomUUID } from 'node:crypto';

// This store belongs to one server process; all records disappear on restart.
export function createStore({ maxGuests = 10000, maxRooms = 10000, makeId = randomUUID,
  makeCredential = () => randomBytes(32).toString('base64url'),
  makeCode = () => randomBytes(10).toString('hex').toUpperCase() } = {}) {
  const guests = new Map();
  const rooms = new Map();
  const maxAttempts = 10;

  function createGuest(displayName) {
    if (guests.size >= maxGuests) return { error: 'capacity' };
    for (let attempt = 0; attempt < maxAttempts; attempt++) {
      const id = makeId();
      if (guests.has(id)) continue;
      const credential = makeCredential();
      const credentialHash = createHash('sha256').update(credential).digest('hex');
      guests.set(id, { id, displayName, credentialHash });
      return { guestId: id, displayName, credential };
    }
    return { error: 'collision' };
  }

  function createRoom(name) {
    if (rooms.size >= maxRooms) return { error: 'capacity' };
    for (let attempt = 0; attempt < maxAttempts; attempt++) {
      const code = makeCode();
      if (rooms.has(code)) continue;
      const room = { code, name, createdAt: new Date().toISOString() };
      rooms.set(code, room);
      return room;
    }
    return { error: 'collision' };
  }

  return { createGuest, createRoom, findRoom: (code) => rooms.get(code) };
}
