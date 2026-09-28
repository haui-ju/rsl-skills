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
sys.path.insert(0, str(ROOT / "scripts"))
from rsl_out import Fail, ok, run  # noqa: E402

SKIP_DIRS = {"graphify-out", "_raw"}


class Scope:
    def __init__(self, name: str, folder: Path, label: str, recursive: bool = False):
        self.name, self.folder, self.label, self.recursive = name, folder, label, recursive
        self.out = folder / "graphify-out"
        self.manifest = self.out / f"{name}-manifest.json"

    def rel(self, p: Path) -> str:
        return str(p.relative_to(ROOT))

    def files(self) -> list[Path]:
        found = self.folder.rglob("*.md") if self.recursive else self.folder.glob("*.md")
        return sorted(p for p in found if not p.name.startswith("_") and not SKIP_DIRS & set(p.relative_to(self.folder).parts))


EXAMPLES = Scope("examples", ROOT / "global" / "examples", "ejemplos")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def status(sc: Scope, files: list[Path], shas: dict[str, str], prev: dict) -> int:
    if not (sc.out / "graph.json").exists():
        print(f"FAIL  {sc.name}: falta {sc.rel(sc.out)}/graph.json (pnpm graphify:{sc.name}:refresh)")
        return 1
    old = prev.get("files", {})
    new = [f for f in shas if f not in old]
    changed = [f for f in shas if f in old and old[f] != shas[f]]
    removed = [f for f in old if f not in shas]
    if new or changed or removed:
        print(f"STALE {sc.name}: nuevos {new or '—'} · modificados {changed or '—'} · eliminados {removed or '—'}")
        return 1
    print(f"PASS  {sc.name}: {len(files)} {sc.label} · {prev.get('nodes')} nodos · {prev.get('edges')} aristas · al día")
    return 0


def main(sc: Scope, force: bool, only_status: bool = False) -> int:
    files = sc.files()
    shas = {str(p.relative_to(sc.folder)): sha(p) for p in files}
    prev = json.loads(sc.manifest.read_text(encoding="utf-8")) if sc.manifest.exists() else {}
    if only_status:
        return status(sc, files, shas, prev)
    if not files:
        print(f"WARN: {sc.rel(sc.folder)}/ no tiene .md; nada que indexar")
        return 0
    if not force and prev.get("files") == shas and (sc.out / "graph.json").exists():
        print(f"sin cambios: {len(files)} {sc.label} ya indexados → {sc.rel(sc.out)}/graph.json")
        return 0

    from graphify.build import build
    from graphify.cluster import cluster
    from graphify.export import to_json
    from graphify.extractors.markdown import extract_markdown

    extractions, per_file = [], {}
    for f in files:
        result = extract_markdown(f)
        n = len((result or {}).get("nodes") or [])
        per_file[str(f.relative_to(sc.folder))] = n
        if n:
            extractions.append(result)
        print(f"extracted: {sc.rel(f)} → {n} nodes")
    if not extractions:
        print("error: no se extrajeron nodos", file=sys.stderr)
        return 1

    sc.out.mkdir(parents=True, exist_ok=True)
    G = build(extractions, directed=False, root=str(sc.folder))
    communities = cluster(G)
    labels = {i: f"Community {i}" for i in communities}
    if not to_json(G, communities, str(sc.out / "graph.json"), force=True, community_labels=labels):
        print("error: to_json refused", file=sys.stderr)
        return 1
    try:
        from graphify.exporters.html import to_html

        to_html(G, communities, str(sc.out / "graph.html"), community_labels=labels)
    except Exception as e:
        print(f"warn: graph.html skipped: {e}", file=sys.stderr)

    sc.manifest.write_text(
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
    print(f"PASS {sc.label}: {len(files)} archivos · {G.number_of_nodes()} nodos · {G.number_of_edges()} aristas → {sc.rel(sc.out)}/graph.json")
    return 0


def cli(sc: Scope) -> None:
    def entry(argv: list[str]) -> int:
        unknown = [a for a in argv if a not in ("--force", "--status")]
        if unknown:
            raise Fail(f"argumento no reconocido: {' '.join(unknown)}", f"para consultar: pnpm graphify:{sc.name}:query \"…\"", 2)
        if main(sc, "--force" in argv, "--status" in argv):
            raise Fail(f"el grafo {sc.name} no está al día (ver detalle arriba)", f"pnpm graphify:{sc.name}:refresh")
        return ok(f"grafo {sc.name} al día en {sc.rel(sc.out)}/graph.json", f"consulta con pnpm graphify:{sc.name}:query \"…\"")

    run(entry)


if __name__ == "__main__":
    cli(EXAMPLES)
