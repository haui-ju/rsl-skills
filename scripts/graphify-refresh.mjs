#!/usr/bin/env node
/**
 * Refresh Graphify at FIS repo root (AST/docs extract, no LLM required for update).
 * Usage: pnpm graphify:root:refresh
 */
import { spawnSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { homedir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
process.chdir(root);

const home = process.env.USERPROFILE || process.env.HOME || homedir();
const extraBins = [
  path.join(home, '.local', 'bin'),
  path.join(home, 'AppData', 'Roaming', 'Python', 'Python314', 'Scripts'),
  path.join(home, 'AppData', 'Roaming', 'Python', 'Python313', 'Scripts'),
  path.join(home, 'AppData', 'Roaming', 'Python', 'Python312', 'Scripts'),
].filter((p) => existsSync(p));

const pathEnv = [...extraBins, process.env.PATH || ''].filter(Boolean).join(path.delimiter);

function run(cmd, args) {
  return spawnSync(cmd, args, {
    encoding: 'utf8',
    shell: true,
    cwd: root,
    env: { ...process.env, PATH: pathEnv },
  });
}

let result = run('graphify', ['update', '.']);
if ((result.status ?? 1) !== 0) {
  result = run('python3', ['-m', 'graphify', 'update', '.']);
}
if ((result.status ?? 1) !== 0) {
  result = run('python', ['-m', 'graphify', 'update', '.']);
}

if ((result.status ?? 1) !== 0) {
  console.error(result.stdout || '');
  console.error(result.stderr || '');
  console.error(
    [
      'graphify CLI not found or update failed.',
      '',
      'Arch / Linux:',
      '  pipx install graphifyy && pipx ensurepath && hash -r',
      '  graphify install --platform cursor',
    ].join('\n')
  );
  process.exit(result.status ?? 1);
}

if (result.stdout) process.stdout.write(result.stdout);
if (result.stderr) process.stderr.write(result.stderr);

const graphJson = path.join(root, 'graphify-out', 'graph.json');
if (!existsSync(graphJson)) {
  console.error('Update finished but graphify-out/graph.json is still missing.');
  process.exit(1);
}

console.log('PASS: graphify root →', path.relative(root, graphJson));
process.exit(0);
