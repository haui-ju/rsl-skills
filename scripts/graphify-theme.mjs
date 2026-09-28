#!/usr/bin/env node
/**
 * Theme Graphify orchestrator
 *
 * Stages:
 *   A prepare  → pnpm graphify:theme:refresh <slug> --prepare-only
 *   C build+D  → pnpm graphify:theme:refresh <slug>
 *   D verify   → pnpm graphify:theme:status <slug>
 *
 * Full:
 *   pnpm graphify:theme:refresh <slug>
 *   pnpm graphify:theme:refresh <slug> --force
 */
import { spawnSync } from 'node:child_process';
import { existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { homedir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
process.chdir(root);

const args = process.argv.slice(2);
const flags = new Set(args.filter((a) => a.startsWith('--')));
const positional = args.filter((a) => !a.startsWith('--'));
const raw = positional[0];

if (!raw) {
  console.error(
    [
      'Usage:',
      '  pnpm graphify:theme:refresh <titulo-breve>',
      '  pnpm graphify:theme:refresh <titulo-breve> --prepare-only',
      '  pnpm graphify:theme:refresh <titulo-breve> --build-only',
      '  pnpm graphify:theme:refresh <titulo-breve> --verify-only',
      '  pnpm graphify:theme:refresh <titulo-breve> --force',
    ].join('\n')
  );
  process.exit(1);
}

let themeRel = raw.replace(/\/+$/, '');
if (!themeRel.startsWith('docs/')) themeRel = path.join('docs', themeRel);
const themeAbs = path.resolve(root, themeRel);

if (!existsSync(themeAbs)) {
  console.error(`Theme folder not found: ${themeRel}`);
  process.exit(1);
}

mkdirSync(path.join(themeAbs, 'RSL', 'PDF'), { recursive: true });
mkdirSync(path.join(themeAbs, 'RSL', 'MD'), { recursive: true });

const themeIgnore = path.join(themeAbs, '.graphifyignore');
if (!existsSync(themeIgnore)) {
  writeFileSync(
    themeIgnore,
    ['# Re-include this theme (root ignores docs/**).', '!**', '!*', ''].join('\n'),
    'utf8'
  );
}

const home = process.env.USERPROFILE || process.env.HOME || homedir();
const graphifyPy = path.join(home, '.local', 'share', 'pipx', 'venvs', 'graphifyy', 'bin', 'python');
const py = existsSync(graphifyPy) ? graphifyPy : 'python3';
const offline = path.join(root, 'scripts', 'graphify-theme-offline.py');
const pathEnv = [path.join(home, '.local', 'bin'), process.env.PATH || ''].join(path.delimiter);

const pyArgs = [offline, themeAbs];
if (flags.has('--force')) pyArgs.push('--force');
if (flags.has('--prepare-only')) pyArgs.push('--prepare-only');
if (flags.has('--build-only')) pyArgs.push('--build-only');
if (flags.has('--verify-only')) pyArgs.push('--verify-only');

console.log(`[graphify-theme] theme=${themeRel}`);
console.log(`[graphify-theme] python=${py}`);
console.log(`[graphify-theme] flags=${[...flags].join(' ') || '(full: prepare→build→verify)'}`);

const result = spawnSync(py, pyArgs, {
  encoding: 'utf8',
  shell: false,
  cwd: root,
  env: { ...process.env, PATH: pathEnv },
});
if (result.stdout) process.stdout.write(result.stdout);
if (result.stderr) process.stderr.write(result.stderr);

const code = result.status ?? 1;
if (code === 0) {
  const graphJson = path.join(themeAbs, 'graphify-out', 'graph.json');
  const manifest = path.join(themeAbs, 'RSL', 'index-manifest.json');
  if (existsSync(graphJson)) console.log('[graphify-theme] PASS graph →', path.relative(root, graphJson));
  if (existsSync(manifest)) console.log('[graphify-theme] PASS manifest →', path.relative(root, manifest));
}
process.exit(code);
