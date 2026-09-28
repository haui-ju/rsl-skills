---
name: graphify-root
description: >-
  Create or refresh the FIS root Graphify memory at graphify-out/. Use when
  the user says graphify-root, refresh root graphify, or asks to update project
  memory. Does not refresh theme graphs. Agents must not run this unless the
  user explicitly invokes this skill.
---

# graphify-root

Build / refresh the **repo-root** knowledge graph (skills, `global/`, README, candidatos). Theme SLR corpora under `docs/` are **out of scope** here — use **graphify-theme**.

## Control

- You run refresh **only** when the user explicitly invokes this skill (or clearly asks to refresh root Graphify).
- `rsl-*` agents and casual coding must **never** call refresh on their own.
- Lookup (`query` / `path` / `explain`) against an existing root graph is always OK.

## Procedure

1. Confirm workspace is FIS repo root (`package.json` with `graphify:root:refresh`).
2. Run from root:

```bash
pnpm graphify:root:refresh
```

Equivalent: `graphify update .`

3. Verify with `pnpm graphify:root:status` (PASS = al día). Optionally note `GRAPH_REPORT.md` / `graph.html`.
4. Chat: path of graph, brief status (ok / error). Remind that themes need **graphify-theme**.

## Lookup (after graph exists)

```bash
graphify query "<question>"
graphify path "A" "B"
graphify explain "<concept>"
```

## Invoke examples

```text
Usa graphify-root
```

```text
Actualiza la memoria graphify del root
```

## Forbidden

- Running `pnpm graphify:theme:refresh` from this skill.
- Refreshing because “the graph might be stale” without user request.
- Inventing graph contents if update fails — report the error and install hint (`pipx install graphifyy`).
