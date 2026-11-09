const MAX_BODY_BYTES = 16 * 1024;

export function json(response, status, body, headers = {}) {
  response.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8', ...headers });
  response.end(JSON.stringify(body));
}

export function fail(response, status, code, message, headers) {
  json(response, status, { error: { code, message } }, headers);
}

export function readBody(request) {
  return new Promise((resolve, reject) => {
    let size = 0;
    let tooLarge = false;
    const chunks = [];
    request.on('data', (chunk) => {
      if (tooLarge) return;
      size += chunk.length;
      if (size > MAX_BODY_BYTES) {
        tooLarge = true;
        chunks.length = 0;
        reject(new Error('too_large'));
        return;
      }
      chunks.push(chunk);
    });
    request.on('end', () => {
      if (tooLarge) return;
      try {
        const value = JSON.parse(Buffer.concat(chunks).toString('utf8'));
        if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error();
        resolve(value);
      } catch {
        reject(new Error('invalid_json'));
      }
    });
    request.on('error', () => reject(new Error('read_error')));
    request.on('aborted', () => reject(new Error('read_error')));
  });
}

export function normalizedName(value) {
  if (typeof value !== 'string') return null;
  const name = value.trim();
  if ([...name].length < 1 || [...name].length > 32 || /[\u0000-\u001f\u007f]/.test(name)) return null;
  return name;
}

export function handleCreate(request, response, field, create) {
  if (!/^application\/json(?:\s*;|\s*$)/i.test(request.headers['content-type'] || '')) {
    fail(response, 415, 'unsupported_media_type', 'Content-Type must be application/json');
    return;
  }

  readBody(request).then((body) => {
    const name = normalizedName(body[field]);
    if (!name) return fail(response, 400, 'invalid_name', 'Name must be 1–32 characters and contain no control characters');
    const result = create(name);
    if (result.error) return fail(response, 503, 'service_unavailable', 'Unable to create resource');
    return json(response, 201, result, { 'Cache-Control': 'no-store' });
  }).catch((error) => {
    if (request.aborted || response.destroyed) return;
    if (error.message === 'too_large') return fail(response, 413, 'body_too_large', 'Request body exceeds 16 KiB');
    if (error.message === 'invalid_json') return fail(response, 400, 'invalid_json', 'Request body must be a JSON object');
    if (error.message === 'read_error') return fail(response, 400, 'invalid_request', 'Could not read request');
    return fail(response, 500, 'internal_error', 'Unexpected server error');
  });
}

