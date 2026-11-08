// Lightweight, dependency-free whitespace checks; this is not a code formatter.
import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

const roots = ['apps/room-server', 'scripts'];
let failed = false;

function check(path) {
  for (const entry of readdirSync(path, { withFileTypes: true })) {
    const file = join(path, entry.name);
    if (entry.isDirectory()) {
      check(file);
    } else if (entry.name.endsWith('.js')) {
      const text = readFileSync(file, 'utf8');
      if (!text.endsWith('\n') || text.split(/\r?\n/).some((line) => /[ \t]+$/.test(line))) {
        console.error(`${file}: use a final newline and no trailing whitespace`);
        failed = true;
      }
    }
  }
}
for (const root of roots) check(root);
if (failed) process.exitCode = 1;
