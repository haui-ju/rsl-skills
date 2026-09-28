#!/usr/bin/env python3
"""Grafo Graphify de la bibliografía compartida: global/bibliography/**/*.md → global/bibliography/graphify-out/graph.json.

Fuentes metodológicas que cualquier tema puede citar (p. ej. picoc/, prisma/) y su catálogo bibliography.md.
Extracción offline de markdown (0 tokens LLM), incremental por sha.

Uso:
  pnpm graphify:bibliography:refresh [--force]
  pnpm graphify:bibliography:status
  pnpm graphify:bibliography:query "PICOC"
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("graphify_examples", Path(__file__).with_name("graphify-examples.py"))
gx = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gx)

BIBLIOGRAPHY = gx.Scope("bibliography", gx.ROOT / "global" / "bibliography", "fuentes", recursive=True)

if __name__ == "__main__":
    gx.cli(BIBLIOGRAPHY)
