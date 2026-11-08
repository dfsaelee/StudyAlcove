import http from 'node:http';
import { loadConfig } from './config.js';
import { handleRequest } from './http.js';

function log(level, message, details = {}) {
  console.log(JSON.stringify({ time: new Date().toISOString(), level, message, ...details }));
}

let config;
try {
  config = loadConfig();
} catch (error) {
  log('error', 'invalid configuration', { error: error.message });
  process.exitCode = 1;
}

if (config) {
  const server = http.createServer(handleRequest);
  server.headersTimeout = 5000;
  let shuttingDown = false;

  server.on('error', (error) => {
    log('error', 'server error', { error: error.message });
    process.exitCode = 1;
  });

  server.listen(config.port, config.host, () => {
    log('info', 'server listening', { host: config.host, port: config.port });
  });

  function shutdown(signal) {
    if (shuttingDown) return;
    shuttingDown = true;
    log('info', 'shutting down', { signal });

    // The deadline bounds shutdown even if an active request never finishes.
    const deadline = setTimeout(() => {
      log('error', 'shutdown timed out');
      process.exitCode = 1;
      server.closeAllConnections();
    }, 5000);
    deadline.unref();

    server.close((error) => {
      clearTimeout(deadline);
      if (error) {
        log('error', 'shutdown failed', { error: error.message });
        process.exitCode = 1;
      } else {
        log('info', 'shutdown complete');
      }
    });
  }

  process.once('SIGINT', () => shutdown('SIGINT'));
  process.once('SIGTERM', () => shutdown('SIGTERM'));
}
