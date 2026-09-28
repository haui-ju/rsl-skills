#!/usr/bin/env node
/**
 * Run prepare→build→verify for one theme (default: ia-inclusion-cognitiva-software)
 * or all docs/* that contain RSL/.
 *
 *   node scripts/graphify-theme-test.mjs ia-inclusion-cognitiva-software
 *   pnpm graphify:theme:refresh --all      (usa este script; también bootstrap)
 */
import { spawnSync } from 'node:child_process';
import { existsSync, readdirSync, statSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const args = process.argv.slice(2);
const all = args.includes('--all');
const force = args.includes('--force');
const positional = args.filter((a) => !a.startsWith('--'));

function themes() {
  if (!all && positional[0]) {
    const t = positional[0].replace(/\/+$/, '').replace(/^docs\//, '');
    return [t];
  }
  if (all) {
    const docs = path.join(root, 'docs');
    return readdirSync(docs).filter((name) => {
      const p = path.join(docs, name);
      return statSync(p).isDirectory() && existsSync(path.join(p, 'RSL'));
    });
  }
  return ['ia-inclusion-cognitiva-software'];
}

let failed = 0;
for (const slug of themes()) {
  console.log(`\n======== TEST theme: ${slug} ========`);
  const r = spawnSync(
    'node',
    [path.join(root, 'scripts', 'graphify-theme.mjs'), slug, ...(force ? ['--force'] : [])],
    { encoding: 'utf8', cwd: root, env: process.env }
  );
  if (r.stdout) process.stdout.write(r.stdout);
  if (r.stderr) process.stderr.write(r.stderr);
  if ((r.status ?? 1) !== 0) {
    console.error(`FAIL: ${slug} exit=${r.status}`);
    failed += 1;
  } else {
    console.log(`PASS: ${slug}`);
  }
}

console.log(failed ? `\n${failed} theme(s) FAILED` : '\nAll theme Graphify tests PASSED');
process.exit(failed ? 1 : 0);
