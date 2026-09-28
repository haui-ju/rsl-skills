#!/usr/bin/env python3
"""Convierte un PDF de la bibliografía compartida en MD consultable (mismo pipeline que el grafo del tema).

  pnpm -s rsl:source global/bibliography/<carpeta>/<archivo>.pdf [--force]

Escribe <archivo>.md junto al PDF (índice con [PDF p.N] por sección) y _raw/<archivo>.txt con marcas de página.
No refresca Graphify: después, `pnpm graphify:bibliography:refresh`.
"""
from __future__ import annotations

import importlib.util
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rsl_out import Fail, ok, run  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
USAGE = "uso: rsl:source global/bibliography/<carpeta>/<archivo>.pdf [--force]"


def pipeline():
    spec = importlib.util.spec_from_file_location("graphify_theme_offline", Path(__file__).with_name("graphify-theme-offline.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def rel(p: Path) -> Path:
    return p.relative_to(ROOT) if ROOT in p.parents else p


def main(argv: list[str]) -> int:
    args = [a for a in argv if a != "--force"]
    force = "--force" in argv
    if len(args) != 1 or args[0] in ("-h", "--help"):
        raise Fail("falta el PDF" if not args else f"argumentos de más: {' '.join(args)}" if len(args) > 1 else "ayuda", USAGE, 2)
    pdf = Path(args[0])
    pdf = pdf if pdf.is_absolute() else ROOT / pdf
    if not pdf.exists():
        raise Fail(f"no existe {args[0]}", "descarga primero el PDF en global/bibliography/<carpeta>/")
    if not pdf.is_file() or pdf.suffix.lower() != ".pdf":
        raise Fail(f"{args[0]} no es un archivo .pdf", USAGE)
    with pdf.open("rb") as fh:
        if fh.read(5) != b"%PDF-":
            raise Fail(f"{args[0]} no es un PDF real (la descarga trajo otra cosa, p. ej. una página HTML)", "bórralo y descarga el PDF desde el enlace directo")
    if shutil.which("pdftotext") is None:
        raise Fail("falta pdftotext (poppler)", "instálalo con rsl-bootstrap")
    md = pdf.with_suffix(".md")
    if md.exists() and md.stat().st_mtime >= pdf.stat().st_mtime and not force:
        return ok(f"{rel(md)} ya estaba al día; no se regeneró (usa --force para rehacerlo)",
                  "cita desde el catálogo global/bibliography/bibliography.md")
    g = pipeline()
    good, raw, err = g.pdftotext_raw(pdf)
    if not good or len(raw.split()) < 200:
        raise Fail(f"no se pudo extraer texto de {args[0]} ({err or 'casi sin texto; ¿PDF escaneado?'})", "busca otra versión del PDF con texto seleccionable")
    raw_dir = pdf.parent / "_raw"
    raw_dir.mkdir(exist_ok=True)
    g.write_raw_with_pages(raw_dir, pdf.stem, raw)
    text = g.structure_rag_md(stem=pdf.stem, pdf_name=pdf.name, raw_text=raw)
    text = re.sub(r"## Relevance hooks\n(### Theme relevance:.*\n)*\n?", "", text)
    text = text.replace("ver RSL/MD/_raw", f"ver _raw/{pdf.stem}.txt")
    md.write_text(text, encoding="utf-8")
    pages = len(g.split_pdf_pages(raw))
    return ok(f"{rel(md)} generado desde {pdf.name} ({pages} páginas; texto por página en {rel(raw_dir)}/{pdf.stem}.txt)",
              "agrega la obra al catálogo global/bibliography/bibliography.md y corre pnpm graphify:bibliography:refresh")


if __name__ == "__main__":
    run(main)
