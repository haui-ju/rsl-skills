#!/usr/bin/env python3
"""Extrae texto calificado (prosa larga) para simulación Turnitin RSL.

Uso:
  python3 scripts/turnitin-qualified-text.py <archivo.md>

Salida: JSON en stdout (indent 2) + última línea OK:/ERROR: vía rsl_out.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rsl_out import Fail, error, ok, run  # noqa: E402

MIN_QUALIFIED_WORDS = 300
MAX_QUALIFIED_WORDS = 30_000

ES_HINT = re.compile(
    r"\b(?:el|la|los|las|de|que|en|un|una|por|con|para|como|esta|este|del|al|se|su|sus)\b",
    re.I,
)
EN_HINT = re.compile(r"\b(?:the|and|of|to|in|that|for|with|as|on|is|are|this|was)\b", re.I)


def strip_frontmatter(text: str) -> tuple[str, list[dict]]:
    excluded = []
    if text.startswith("---"):
        m = re.match(r"^---\n.*?\n---\n", text, re.S)
        if m:
            excluded.append({"type": "yaml", "lineStart": 1, "lineEnd": m.group(0).count("\n")})
            text = text[m.end() :]
    return text, excluded


def prose_blocks(text: str) -> list[tuple[int, str]]:
    text = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    lines = text.splitlines()
    out, buf, start, in_code = [], [], 0, False
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if s.startswith("```"):
            in_code = not in_code
            continue
        if re.match(r"^#{1,6}\s+(?:[IVXLC]+\.\s+|\d+\.\s+)?(Referencias|References)\b", s, re.I):
            break
        if in_code or s.startswith("|") or s.startswith("#") or not s:
            if buf:
                out.append((start, " ".join(buf)))
                buf = []
            continue
        if buf and re.match(r"^(?:[-*+]|\d+\.)\s", s):
            out.append((start, " ".join(buf)))
            buf = []
        if not buf:
            start = i
        buf.append(s)
    if buf:
        out.append((start, " ".join(buf)))
    return out


def split_sentences(paragraph: str) -> list[str]:
    parts = re.split(r"(?<=[.!?…])\s+", paragraph.strip())
    return [p.strip() for p in parts if p.strip()]


def word_count(s: str) -> int:
    return len(re.findall(r"\w+(?:['']\w+)?", s, re.UNICODE))


def language_hint(text: str) -> str:
    es = len(ES_HINT.findall(text))
    en = len(EN_HINT.findall(text))
    if es > en * 1.2:
        return "es"
    if en > es * 1.2:
        return "en"
    return "mixed"


def main(argv: list[str]) -> int:
    if len(argv) != 1 or argv[0] in ("-h", "--help"):
        raise Fail("uso: turnitin-qualified-text.py <archivo.md>", "pnpm -s turnitin:qualified docs/.../paper-polish.md", 2)
    path = Path(argv[0])
    if not path.is_file():
        raise Fail(f"no existe {path}", "indica la ruta del paper-polish.md o informe-polish.md")
    if path.suffix.lower() != ".md":
        raise Fail("solo archivos .md", "usa paper-polish.md o informe-polish.md")

    raw = path.read_text(encoding="utf-8")
    body, excluded = strip_frontmatter(raw)
    blocks = prose_blocks(body)

    sentences: list[dict] = []
    sid = 0
    for para_idx, (line_start, par) in enumerate(blocks, 1):
        for sent in split_sentences(par):
            sid += 1
            sentences.append(
                {
                    "id": f"S{sid}",
                    "text": sent,
                    "paragraphId": f"P{para_idx}",
                    "lineStart": line_start,
                }
            )

    qualified_text = " ".join(s["text"] for s in sentences)
    qw = word_count(qualified_text)
    processable = MIN_QUALIFIED_WORDS <= qw <= MAX_QUALIFIED_WORDS

    payload = {
        "sourcePath": str(path.resolve()),
        "sourceBasename": path.name,
        "qualifiedWords": qw,
        "sentenceCount": len(sentences),
        "sentences": sentences,
        "excluded": excluded,
        "processable": processable,
        "languageHint": language_hint(qualified_text),
        "minWords": MIN_QUALIFIED_WORDS,
        "maxWords": MAX_QUALIFIED_WORDS,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if not processable:
        if qw < MIN_QUALIFIED_WORDS:
            return error(
                f"texto calificado {qw} palabras (< {MIN_QUALIFIED_WORDS})",
                "añade prosa en párrafos o usa un polish más largo",
            )
        return error(
            f"texto calificado {qw} palabras (> {MAX_QUALIFIED_WORDS})",
            "divide el documento o excluye anexos del archivo analizado",
        )
    return ok(f"{qw} palabras calificadas, {len(sentences)} oraciones", "rsl-turnitin-informe sobre el mismo archivo")


if __name__ == "__main__":
    run(main, sys.argv[1:])
