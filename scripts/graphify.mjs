#!/usr/bin/env node
/**
 * Despachador único de los grafos Graphify del repo.
 *
 *   node scripts/graphify.mjs <alcance> <acción> [args]
 *
 * Alcances: root · theme · thesaurus · examples
 * Acciones: refresh (actualizar) · status (validar) · query (consultar) · open (abrir graph.html)
 *
 *   pnpm graphify:root:query "skills rsl"
 *   pnpm graphify:theme:refresh ia-inclusion-cognitiva-software [--force|--all]
 *   pnpm graphify:theme:query ia-inclusion-cognitiva-software "cognitive accessibility"
 *   pnpm graphify:thesaurus:query "machine learning"
 *   pnpm graphify:examples:status
 *
 * theme: si se omite el slug y solo hay un tema con RSL/, se usa ese.
 * status sale con código 1 si el grafo falta o está desactualizado.
 */
import { spawnSync } from 'node:child_process';
import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { homedir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
process.chdir(root);

const home = process.env.USERPROFILE || process.env.HOME || homedir();
const env = { ...process.env, PATH: [path.join(home, '.local', 'bin'), process.env.PATH || ''].join(path.delimiter) };
const graphifyPy = path.join(home, '.local', 'share', 'pipx', 'venvs', 'graphifyy', 'bin', 'python');

const [scope, action, ...rest] = process.argv.slice(2);
const flags = rest.filter((a) => a.startsWith('--'));
const positional = rest.filter((a) => !a.startsWith('--'));

const SCOPES = ['root', 'theme', 'thesaurus', 'examples'];
const ACTIONS = ['refresh', 'status', 'query', 'open'];

function usage(msg) {
  if (msg) console.error(`error: ${msg}\n`);
  console.error(
    [
      'Uso: pnpm graphify:<alcance>:<acción> [args]',
      `  alcances: ${SCOPES.join(' · ')}`,
      `  acciones: ${ACTIONS.join(' · ')}`,
      '  theme necesita <slug> (o se autodetecta si solo hay uno); refresh/status aceptan --all',
    ].join('\n')
  );
  process.exit(2);
}

function run(cmd, args) {
  const r = spawnSync(cmd, args, { cwd: root, env, stdio: 'inherit' });
  return r.status ?? 1;
}

function themes() {
  const docs = path.join(root, 'docs');
  if (!existsSync(docs)) return [];
  return readdirSync(docs).filter((n) => {
    const p = path.join(docs, n);
    return !n.startsWith('_') && statSync(p).isDirectory() && existsSync(path.join(p, 'RSL'));
  });
}

function resolveSlug(args) {
  const raw = args[0]?.replace(/\/+$/, '').replace(/^docs\//, '');
  if (raw && existsSync(path.join(root, 'docs', raw))) return { slug: raw, rest: args.slice(1) };
  const all = themes();
  if (raw && args.length > 1) usage(`el tema '${raw}' no existe: ${all.join(' | ') || '(no hay docs/*/RSL)'}`);
  if (all.length === 1) return { slug: all[0], rest: args };
  usage(`indica el tema: ${all.join(' | ') || '(no hay docs/*/RSL)'}`);
}

function graphPath(s, slug) {
  return {
    root: 'graphify-out/graph.json',
    theme: `docs/${slug}/graphify-out/graph.json`,
    thesaurus: 'global/thesaurus/graphify-out/graph.json',
    examples: 'global/examples/graphify-out/graph.json',
  }[s];
}

function walk(dir, out = []) {
  if (!existsSync(dir)) return out;
  for (const n of readdirSync(dir)) {
    if (['graphify-out', 'node_modules', '.git', '_raw', '__pycache__', 'thesaurus', 'examples', '.output', 'dist'].includes(n)) continue;
    const p = path.join(dir, n);
    const st = statSync(p);
    if (st.isDirectory()) walk(p, out);
    else out.push(p);
  }
  return out;
}

function graphInfo(rel) {
  const p = path.join(root, rel);
  if (!existsSync(p)) return null;
  const g = JSON.parse(readFileSync(p, 'utf8'));
  return { mtime: statSync(p).mtimeMs, nodes: (g.nodes || []).length, edges: (g.links || g.edges || []).length };
}

function report(label, rel, sources) {
  const info = graphInfo(rel);
  if (!info) {
    console.log(`FAIL  ${label}: falta ${rel}`);
    return 1;
  }
  const stale = sources.filter((f) => statSync(f).mtimeMs > info.mtime).map((f) => path.relative(root, f));
  const when = new Date(info.mtime).toISOString().slice(0, 16).replace('T', ' ');
  if (stale.length) {
    console.log(`STALE ${label}: ${info.nodes} nodos · ${info.edges} aristas · ${when} · ${stale.length} archivo(s) más nuevos que el grafo:`);
    for (const f of stale.slice(0, 15)) console.log(`        - ${f}`);
    if (stale.length > 15) console.log(`        … y ${stale.length - 15} más`);
    return 1;
  }
  console.log(`PASS  ${label}: ${info.nodes} nodos · ${info.edges} aristas · ${when} · al día`);
  return 0;
}

function rootSources() {
  const dirs = ['.cursor/skills', '.cursor/agents', '.cursor/rules', 'scripts', 'global', 'playbooks'];
  const files = ['README.md', 'package.json'].map((f) => path.join(root, f)).filter(existsSync);
  return [...files, ...dirs.flatMap((d) => walk(path.join(root, d)))].filter((f) => /\.(md|mdc|mjs|js|py|json|ya?ml)$/.test(f));
}

function themeSources(slug) {
  const t = path.join(root, 'docs', slug);
  const top = readdirSync(t).filter((n) => n.endsWith('.md')).map((n) => path.join(t, n));
  return [...top, ...walk(path.join(t, 'RSL', 'MD')), ...walk(path.join(t, 'RSL', 'PDF')), ...walk(path.join(t, 'paper'))].filter((f) => /\.(md|pdf)$/.test(f));
}

function openHtml(rel) {
  const html = path.join(root, path.dirname(rel), 'graph.html');
  if (!existsSync(html)) {
    console.error(`error: falta ${path.relative(root, html)} (corre el refresh de ese alcance)`);
    return 1;
  }
  for (const cmd of ['xdg-open', 'open']) {
    if (spawnSync('sh', ['-c', `command -v ${cmd}`], { env }).status === 0) {
      spawnSync(cmd, [html], { env, stdio: 'ignore', detached: true });
      console.log(`abierto ${path.relative(root, html)}`);
      return 0;
    }
  }
  console.log(html);
  return 0;
}

function query(rel, words) {
  if (!words.length) usage('falta la pregunta entre comillas');
  const args = ['query', words.join(' '), ...flags];
  if (rel !== 'graphify-out/graph.json') args.push('--graph', rel);
  return run('graphify', args);
}

if (!SCOPES.includes(scope) || !ACTIONS.includes(action)) usage();

let code = 0;
switch (scope) {
  case 'root': {
    const rel = graphPath('root');
    if (action === 'refresh') code = run('node', ['scripts/graphify-refresh.mjs']);
    if (action === 'status') code = report('root', rel, rootSources());
    if (action === 'query') code = query(rel, positional);
    if (action === 'open') code = openHtml(rel);
    break;
  }
  case 'theme': {
    if (flags.includes('--all') && ['refresh', 'status'].includes(action)) {
      if (action === 'refresh') code = run('node', ['scripts/graphify-theme-test.mjs', '--all', ...flags.filter((f) => f !== '--all')]);
      else for (const t of themes()) code = report(`theme ${t}`, graphPath('theme', t), themeSources(t)) || code;
      break;
    }
    const { slug, rest: words } = resolveSlug(positional);
    const rel = graphPath('theme', slug);
    if (action === 'refresh') code = run('node', ['scripts/graphify-theme.mjs', slug, ...flags]);
    if (action === 'status') {
      code = report(`theme ${slug}`, rel, themeSources(slug));
      if (existsSync(path.join(root, rel))) code = run('node', ['scripts/graphify-theme.mjs', slug, '--verify-only']) || code;
    }
    if (action === 'query') code = query(rel, words);
    if (action === 'open') code = openHtml(rel);
    break;
  }
  case 'thesaurus': {
    const rel = graphPath('thesaurus');
    const pdf = path.join(root, 'global', 'thesaurus', 'IEEE.pdf');
    if (action === 'refresh') code = run(graphifyPy, ['scripts/thesaurus-ieee.py', ...flags]);
    if (action === 'status') {
      const src = [pdf, path.join(root, 'scripts', 'thesaurus-ieee.py')].filter(existsSync);
      code = report('thesaurus IEEE', rel, src);
      if (!existsSync(path.join(root, 'global', 'thesaurus', 'ieee-thesaurus.json'))) {
        console.log('FAIL  thesaurus IEEE: falta global/thesaurus/ieee-thesaurus.json');
        code = 1;
      }
    }
    if (action === 'query') code = query(rel, positional);
    if (action === 'open') code = openHtml(rel);
    break;
  }
  case 'examples': {
    const rel = graphPath('examples');
    if (action === 'refresh') code = run(graphifyPy, ['scripts/graphify-examples.py', ...flags]);
    if (action === 'status') code = run(graphifyPy, ['scripts/graphify-examples.py', '--status']);
    if (action === 'query') code = query(rel, positional);
    if (action === 'open') code = openHtml(rel);
    break;
  }
}
process.exit(code);
