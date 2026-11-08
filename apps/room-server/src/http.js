// Readiness has no dependencies yet; PostgreSQL is not checked.
export function handleRequest(request, response) {
  if (request.method !== 'GET') {
    response.writeHead(405, { Allow: 'GET' });
    response.end();
    return;
  }

  const paths = { '/healthz': 'ok\n', '/readyz': 'ready\n' };
  const path = request.url?.split('?')[0];
  if (!Object.hasOwn(paths, path)) {
    response.writeHead(404);
    response.end();
    return;
  }

  response.writeHead(200, { 'Content-Type': 'text/plain; charset=utf-8' });
  response.end(paths[path]);
}
