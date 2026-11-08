// LISTEN_ADDR uses host:port, with brackets around IPv6 addresses.
export function loadConfig(env = process.env) {
  const address = env.LISTEN_ADDR || '127.0.0.1:8080';
  const match = /^(?:\[([^\]]+)\]|([^:]+)):(\d+)$/.exec(address);
  if (!match) {
    throw new Error('LISTEN_ADDR must be host:port (use [host]:port for IPv6)');
  }

  const port = Number(match[3]);
  if (!Number.isInteger(port) || port < 1 || port > 65535) {
    throw new Error('LISTEN_ADDR port must be between 1 and 65535');
  }
  return { host: match[1] || match[2], port };
}
