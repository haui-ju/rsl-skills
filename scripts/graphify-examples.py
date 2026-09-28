#!/usr/bin/env python3
"""Grafo Graphify de los papers de ejemplo: global/examples/*.md → global/examples/graphify-out/graph.json.

Extracción offline de markdown (0 tokens LLM). Si ningún ejemplo cambió (mismo sha) y el grafo existe, no reconstruye.

Uso:
  pnpm graphify:examples:refresh            # incremental
  pnpm graphify:examples:refresh --force
  pnpm graphify:examples:status
  pnpm graphify:examples:query "estructura de Resultados"
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ROOT / "global" / "examples"
OUT = EXAMPLES / "graphify-out"
MANIFEST = OUT / "examples-manifest.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def status(files: list[Path], shas: dict[str, str], prev: dict) -> int:
    if not (OUT / "graph.json").exists():
        print("FAIL  examples: falta global/examples/graphify-out/graph.json (pnpm graphify:examples:refresh)")
        return 1
    old = prev.get("files", {})
    new = [f for f in shas if f not in old]
    changed = [f for f in shas if f in old and old[f] != shas[f]]
    removed = [f for f in old if f not in shas]
    if new or changed or removed:
        print(f"STALE examples: nuevos {new or '—'} · modificados {changed or '—'} · eliminados {removed or '—'}")
        return 1
    print(f"PASS  examples: {len(files)} ejemplos · {prev.get('nodes')} nodos · {prev.get('edges')} aristas · al día")
    return 0


def main(force: bool, only_status: bool = False) -> int:
    files = sorted(p for p in EXAMPLES.glob("*.md") if not p.name.startswith("_"))
    shas = {p.name: sha(p) for p in files}
    prev = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {}
    if only_status:
        return status(files, shas, prev)
    if not files:
        print("WARN: global/examples/ no tiene .md; nada que indexar")
        return 0
    if not force and prev.get("files") == shas and (OUT / "graph.json").exists():
        print(f"sin cambios: {len(files)} ejemplos ya indexados → {OUT.relative_to(ROOT)}/graph.json")
        return 0

    from graphify.build import build
    from graphify.cluster import cluster
    from graphify.export import to_json
    from graphify.extractors.markdown import extract_markdown

    extractions, per_file = [], {}
    for f in files:
        result = extract_markdown(f)
        n = len((result or {}).get("nodes") or [])
        per_file[f.name] = n
        if n:
            extractions.append(result)
        print(f"extracted: global/examples/{f.name} → {n} nodes")
    if not extractions:
        print("error: no se extrajeron nodos", file=sys.stderr)
        return 1

    OUT.mkdir(parents=True, exist_ok=True)
    G = build(extractions, directed=False, root=str(EXAMPLES))
    communities = cluster(G)
    labels = {i: f"Community {i}" for i in communities}
    if not to_json(G, communities, str(OUT / "graph.json"), force=True, community_labels=labels):
        print("error: to_json refused", file=sys.stderr)
        return 1
    try:
        from graphify.exporters.html import to_html

        to_html(G, communities, str(OUT / "graph.html"), community_labels=labels)
    except Exception as e:
        print(f"warn: graph.html skipped: {e}", file=sys.stderr)

    MANIFEST.write_text(
        json.dumps(
            {
                "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "files": shas,
                "nodes_per_file": per_file,
                "nodes": G.number_of_nodes(),
                "edges": G.number_of_edges(),
                "communities": len(communities),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"PASS ejemplos: {len(files)} archivos · {G.number_of_nodes()} nodos · {G.number_of_edges()} aristas → {OUT.relative_to(ROOT)}/graph.json")
    return 0


if __name__ == "__main__":
    unknown = [a for a in sys.argv[1:] if a not in ("--force", "--status")]
    if unknown:
        sys.exit(f"argumento no reconocido: {' '.join(unknown)} (para consultar: pnpm graphify:examples:query \"…\")")
    sys.exit(main("--force" in sys.argv[1:], "--status" in sys.argv[1:]))
