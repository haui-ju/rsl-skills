#!/usr/bin/env node
/**
 * Deja listos todos los grafos Graphify tras clonar (o cuando quieras un refresh total).
 *
 *   pnpm run bootstrap
 *
 * Orden: prerrequisitos → root → thesaurus IEEE → ejemplos global/examples → bibliografía global/bibliography → temas docs/* con RSL/ → resumen.
 * Los temas no re-extraen PDFs ya indexados (mismo sha en RSL/index-manifest.json).
 */
import { spawnSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { homedir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
process.chdir(root);

const home = process.env.USERPROFILE || process.env.HOME || homedir();
const localBin = path.join(home, '.local', 'bin');
const env = { ...process.env, PATH: [localBin, process.env.PATH || ''].join(path.delimiter) };
const graphifyPy = path.join(home, '.local', 'share', 'pipx', 'venvs', 'graphifyy', 'bin', 'python');
const thesaurusPdf = path.join(root, 'global', 'thesaurus', 'IEEE.pdf');

function has(cmd) {
  return spawnSync('sh', ['-c', `command -v ${cmd}`], { env }).status === 0;
}

function run(label, cmd, args) {
  console.log(`\n======== ${label} ========`);
  const r = spawnSync(cmd, args, { cwd: root, env, stdio: 'inherit' });
  return (r.status ?? 1) === 0;
}

const missing = [];
if (!has('graphify') || !existsSync(graphifyPy)) {
  missing.push('graphify (pipx):  pipx install graphifyy && pipx ensurepath && graphify install --platform cursor');
}
} else if (spawnSync(graphifyPy, ['-c', 'import xlrd'], { env }).status !== 0) {
  missing.push('xlrd (WoS .xls en cribado:prepare):  pipx inject graphifyy xlrd');
}
for (const bin of ['pdftotext', 'pdftohtml', 'pdfinfo']) {
  if (!has(bin)) missing.push(`${bin} (poppler):  sudo pacman -S poppler  |  sudo apt install poppler-utils  |  brew install poppler`);
}
if (spawnSync('python3', ['-c', 'import yaml'], { env }).status !== 0) {
  missing.push('PyYAML (paper:status):  sudo pacman -S python-yaml  |  sudo apt install python3-yaml  |  pip install --user pyyaml');
}
if (missing.length) {
  console.error(['Faltan prerrequisitos:', ...[...new Set(missing)].map((m) => `  - ${m}`)].join('\n'));
  process.exit(1);
}

const results = [];
results.push(['root', run('Graphify root', 'node', ['scripts/graphify-refresh.mjs'])]);

if (existsSync(thesaurusPdf)) {
  results.push(['thesaurus IEEE', run('Thesaurus IEEE', graphifyPy, ['scripts/thesaurus-ieee.py'])]);
} else {
  console.warn('\nWARN: global/thesaurus/IEEE.pdf no existe; se salta el thesaurus.');
  results.push(['thesaurus IEEE', null]);
}

results.push(['ejemplos global/examples', run('Papers de ejemplo', graphifyPy, ['scripts/graphify-examples.py'])]);
results.push(['bibliografía global/bibliography', run('Bibliografía compartida', graphifyPy, ['scripts/graphify-bibliography.py'])]);

results.push(['temas docs/*', run('Temas (docs/* con RSL/)', 'node', ['scripts/graphify-theme-test.mjs', '--all'])]);

console.log('\n======== Resumen ========');
for (const [name, ok] of results) console.log(`${ok === null ? 'SKIP' : ok ? 'PASS' : 'FAIL'}  ${name}`);
process.exit(results.some(([, ok]) => ok === false) ? 1 : 0);
