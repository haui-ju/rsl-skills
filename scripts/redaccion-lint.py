#!/usr/bin/env python3
"""Lint de redacción académica (playbooks/redaccion-academica.md) sobre un entregable .md.

Uso:
  python3 scripts/redaccion-lint.py <archivo.md> [--max-palabras 40]

FAIL (bloquea la entrega):
  - marcas editoriales pendientes ([citar], (citar), TODO: citar, TODO, PENDIENTE, TBD, FIXME, ???)
  - huellas del flujo interno en la prosa (topic.md, panel, GO_*, rsl-*, rutas, `código`, "Nota de artefacto") y apelaciones a quien lee ("el lector")
  - siglas usadas antes de definirse ("forma completa (SIGLA)" o "SIGLA (forma completa)");
    en el paper, el encabezado (Título/Tema/Problemática/Objetivo) no cuenta: las siglas se definen en el cuerpo
WARN (revisar; corregir o justificar):
  - oraciones de más de N palabras
  - notación de trabajo en la prosa (×, →, A+B, sufijos -duro/-dura)
  - párrafos con más de 3 siglas distintas
Marcadores del usuario (no fallan; se cuentan en la línea OK): [[ … ]] (p. ej. [[ AGREGAR DIAGRAMA ]]) y X como dato pendiente (n = X).

Solo se analiza prosa: se omiten bloques de código, tablas, comentarios HTML, encabezados, enlaces y la sección Referencias.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rsl_out import Fail, error, ok, run  # noqa: E402

MARKERS = re.compile(
    r"\b(?:TODO|FIXME|TBD|XXX|PENDIENTE)\b|\?\?\?"
    r"|(?i:[\[(«\"]\s*citar?\b[^\])»\"]*[\])»\"]|\bcitar\s*$|:\s*citar\b|\[cita[^\]]*\])",
    re.M,
)
INTERNAL = re.compile(
    r"topic\.md|informe(?:-polish)?\.md|picoc(?:-polish|-debate)?\.md|\bpicoc/\d|\bpanel\b|\bGO_\w+|\brsl-[a-z-]+|RSL/(?:PDF|MD)|graphify|"
    r"Nota de artefacto|\bveredicto\b|\b(?:el|al|del|los|las|la|como|nuestros?|nuestras?) lector(?:es|as?)?\b(?! de pantalla)",
    re.I,
)
CODE_SPAN = re.compile(r"`[^`]+`")
ACRONYM = re.compile(r"(?<![\w/.-])([A-Z][A-Za-z]*[A-Z][A-Za-z0-9]*|[A-Z]&[A-Z])(?![\w-])")
NOTATION = [
    (re.compile(r"\s×\s"), "símbolo × en la prosa (dilo en palabras: «por condición, técnica, fase y métrica»)"),
    (re.compile(r"→"), "flecha → en la prosa"),
    (re.compile(r"\b\w+\+\w+\b"), "unión con + (p. ej. «GenAI+web»): usa «y» o reformula"),
    (re.compile(r"\b\w+-dur[oa]s?\b", re.I), "sufijo híbrido «-duro/-dura»: explica qué significa"),
]
# Siglas que no requieren definición (unidades, romanos, operadores booleanos, nombres propios de norma ya expandidos por convención).
ALLOW = {"TODO", "FIXME", "TBD", "XXX", "PENDIENTE", "AND", "OR", "NOT", "II", "III", "IV", "VI", "VII", "VIII", "IX", "XI", "XII", "ISO", "IEEE", "ACM", "DOI", "URL", "PDF", "HTML", "AA", "AAA"}
ROMAN = re.compile(r"^[IVXLC]+$")
CODE_ID = re.compile(r"^(?:RQ|CI|CE)\d+$")
USER_BLOCK = re.compile(r"\[\[[^\[\]\n]+\]\]")
USER_X = re.compile(r"(?<![\w-])X(?![\w-])")


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


def clean(par: str) -> str:
    par = re.sub(r"\[[^\]]*\]\((?!https?:)[^)]*\.md\)", "", par)
    par = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", par)
    return re.sub(r"https?://\S+", "", par)


def is_defined(par: str, m: re.Match) -> bool:
    before, after = par[: m.start()], par[m.end():]
    if re.search(r"[(\[]\s*$", before) and re.match(r"\s*[)\]]", after):
        return True  # «forma completa (SIGLA)» o «[SIGLA]»
    return bool(re.match(r"\s*\((?![^)]*\d{4})[^)]{4,}\)", after))  # «SIGLA (forma completa)», sin confundir con (Autor, 2024)


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return error("uso: redaccion:lint <archivo.md> [--max-palabras N]", code=2) if not argv else ok("ayuda mostrada")
    path = Path(argv[0])
    try:
        max_words = int(argv[argv.index("--max-palabras") + 1]) if "--max-palabras" in argv else 40
    except (IndexError, ValueError):
        raise Fail("--max-palabras necesita un número entero", code=2)
    if not path.exists():
        raise Fail(f"no existe {path}", "indica un archivo .md existente")
    if path.is_dir():
        raise Fail(f"{path} es una carpeta", "indica un archivo .md")
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise Fail(f"{path} no está en UTF-8", "guárdalo como UTF-8")
    fails: list[str] = []
    warns: list[str] = []
    seen: dict[str, int] = {}
    header = re.search(r"<!-- paper:section id=encabezado -->(.*?)<!-- /paper:section -->", text, flags=re.S)
    header_lines = range(text.count("\n", 0, header.start()) + 1, text.count("\n", 0, header.end()) + 2) if header else range(0)

    for m in re.finditer(r"^.*$", text, flags=re.M):
        line = m.group(0)
        n = text.count("\n", 0, m.start()) + 1
        if line.lstrip().startswith("<!--"):
            continue
        for mk in MARKERS.finditer(line):
            fails.append(f"L{n}: marca editorial «{mk.group(0)}»")

    for n, par in prose_blocks(text):
        p = clean(par)
        for mi in INTERNAL.finditer(CODE_SPAN.sub("", p)):
            fails.append(f"L{n}: huella del flujo interno «{mi.group(0)}»")
        for cs in CODE_SPAN.finditer(p):
            fails.append(f"L{n}: código/ruta en la prosa {cs.group(0)}")
        p = USER_BLOCK.sub("", CODE_SPAN.sub("", p))
        acr_here = set()
        for m in ACRONYM.finditer(p):
            a = m.group(1)
            if a in ALLOW or ROMAN.match(a) or CODE_ID.match(a) or len(a) > 12 or re.match(r"\s\d", p[m.end():]):
                continue
            acr_here.add(a)
            if n in header_lines:
                continue
            if a not in seen:
                seen[a] = n
                if not is_defined(p, m):
                    fails.append(f"L{n}: sigla «{a}» sin definir en su primera aparición")
        if len(acr_here) > 3:
            warns.append(f"L{n}: {len(acr_here)} siglas en un párrafo ({', '.join(sorted(acr_here))}); dosifica")
        for rx, msg in NOTATION:
            for mm in rx.finditer(p):
                warns.append(f"L{n}: {msg} → «{mm.group(0).strip()}»")
        for sent in re.split(r"(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÑ¿¡])", p):
            words = len(re.findall(r"\w+", sent))
            if words > max_words:
                warns.append(f"L{n}: oración de {words} palabras (máx. {max_words}): «{sent[:70]}…»")

    body = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    body = re.sub(r"^```.*?^```", "", body, flags=re.S | re.M)
    n_user = len(USER_BLOCK.findall(body)) + len(USER_X.findall(USER_BLOCK.sub("", body)))
    pending = f"; {n_user} marcador(es) del usuario por completar (X, [[ … ]])" if n_user else ""
    for f in fails:
        print(f"  - {f}")
    for w in warns:
        print(f"  ~ {w}")
    if fails:
        return error(f"redacción de {path}: {len(fails)} error(es) y {len(warns)} aviso(s) (ver detalle arriba)", "corrígelos con redaccion-rsl según playbooks/redaccion-academica.md")
    return ok(f"redacción de {path} sin errores ({len(warns)} aviso(s) a corregir o justificar{pending})")


if __name__ == "__main__":
    run(main)
