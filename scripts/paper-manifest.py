#!/usr/bin/env python3
"""Manifiesto del paper RSL por secciones: docs/<slug>/paper/paper.yml (+ paper.state.json).

Uso:
  python3 scripts/paper-manifest.py docs/<slug>                    # estado + qué regenerar (FAIL si un frozen fue editado)
  python3 scripts/paper-manifest.py docs/<slug> --init             # crea paper/paper.yml por defecto
  python3 scripts/paper-manifest.py docs/<slug> --new-version      # crea paper/<fecha>/ copiando la versión anterior
  python3 scripts/paper-manifest.py docs/<slug> --update borrador  # registra hashes tras escribir paper-borrador.md
  python3 scripts/paper-manifest.py docs/<slug> --update polish    # registra hashes tras escribir paper-polish.md
  python3 scripts/paper-manifest.py docs/<slug> --cites [archivo]  # citas en texto vs referencias (format.citation)

paper.yml lo edita el usuario (enabled / frozen / format). paper.state.json lo gestiona este script.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("error: falta PyYAML (pip install --user pyyaml | sudo pacman -S python-yaml | sudo apt install python3-yaml)")

ROOT = Path(__file__).resolve().parent.parent
FILES = {"borrador": "paper-borrador.md", "polish": "paper-polish.md"}
VERSION_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:-(\d+))?$")
SECTION_RE = re.compile(r"<!-- paper:section id=([\w-]+) -->\n(.*?)<!-- /paper:section -->", re.S)

DEFAULT_YML = """\
# Manifiesto del paper RSL. Lo editas tú; las skills rsl-make-paper / rsl-polish-paper lo respetan.
#   enabled: false -> la sección no se genera
#   enabled: true + frozen: false -> se regenera en la próxima corrida
#   frozen: true -> se copia tal cual (si cambia una fuente de depends_on queda 'stale' y se avisa)
# Estado interno (hashes, versiones): paper.state.json (no editar).
version: 1
format:
  numbering: roman           # roman (I. II.) | arabic (1. 2.) | none
  subsection_letters: true   # A. B. C. dentro de Metodología / Resultados
  citation: apa7             # apa7 | ieee  -> global/citation-style/APA7.md | IEEE.md
  language: es
  abstract: [en, es]         # Abstract + Resumen al inicio
  keywords_from: picoc       # palabras clave del abstract salen de picoc(-polish).md
  results_by: rq             # rq (una subsección por RQ de picoc) | tema (categorías emergentes)
  examples: global/examples  # papers de referencia (solo estructura / presentación)
sections:
  - { id: encabezado,   title: "Título · Tema · Problemática · Objetivo", group: portada, enabled: true,  frozen: false, depends_on: [topic.md, informe-polish.md, picoc.md] }
  - { id: abstract,     title: "Abstract / Resumen + palabras clave",     group: portada, enabled: false, frozen: false, depends_on: [all] }
  # I. Introducción
  - { id: contexto,      title: Contexto,              group: introduccion, enabled: true, frozen: false, depends_on: [RSL/MD] }
  - { id: problema,      title: El problema,           group: introduccion, enabled: true, frozen: false, depends_on: [picoc.md] }
  - { id: justificacion, title: Justificación,         group: introduccion, enabled: true, frozen: false, depends_on: [informe-polish.md] }
  - { id: objetivo-rsl,  title: Objetivo de la RSL,    group: introduccion, enabled: true, frozen: false, depends_on: [picoc.md] }
  - { id: organizacion,  title: Organización del contenido de la revisión, group: introduccion, enabled: true, frozen: false, depends_on: [paper/paper.yml] }
  # II. Metodología
  - { id: marco-pico,          title: "Pregunta PICO y sus componentes",       group: metodologia, enabled: false, frozen: false, depends_on: [picoc.md] }
  - { id: palabras-clave,      title: Palabras clave pertinentes,              group: metodologia, enabled: false, frozen: false, depends_on: [picoc.md] }
  - { id: ecuacion-busqueda,   title: Ecuación de búsqueda,                    group: metodologia, enabled: false, frozen: false, depends_on: [picoc.md] }
  - { id: criterios-seleccion, title: Criterios de inclusión y exclusión,      group: metodologia, enabled: false, frozen: false, depends_on: [topic.md, picoc.md] }
  - { id: seleccion-prisma,    title: "Proceso de selección — Diagrama PRISMA", group: metodologia, enabled: false, frozen: false, depends_on: [RSL/seleccion] }
  - { id: calidad,             title: Evaluación de calidad,                   group: metodologia, enabled: false, frozen: false, depends_on: [RSL/seleccion] }
  # III. Resultados (requieren RSL/seleccion y RSL/extraccion, preparados por el usuario)
  - { id: distribucion,        title: Distribución anual de publicaciones, group: resultados, enabled: false, frozen: false, depends_on: [RSL/extraccion] }
  - { id: hallazgos-generales, title: Hallazgos generales,                 group: resultados, enabled: false, frozen: false, depends_on: [RSL/extraccion] }
  - { id: resultados-rq,       title: Resultados por pregunta,             group: resultados, enabled: false, frozen: false, depends_on: [picoc.md, RSL/extraccion] }
  # IV. Discusión
  - { id: discusion-temas, title: Discusión por tema,                      group: discusion, enabled: false, frozen: false, depends_on: [resultados-rq] }
  - { id: discusion-rq,    title: Discusión por pregunta de investigación, group: discusion, enabled: false, frozen: false, depends_on: [resultados-rq] }
  - { id: amenazas,        title: Amenazas a la validez,                   group: discusion, enabled: false, frozen: false, depends_on: [ecuacion-busqueda, seleccion-prisma] }
  # V. Conclusión · VI. Referencias
  - { id: conclusion,  title: Conclusión,  group: conclusion,  enabled: false, frozen: false, depends_on: [resultados-rq, discusion-rq] }
  - { id: referencias, title: Referencias, group: referencias, enabled: true, derived: true }
"""


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:12]


def text_hash(s: str) -> str:
    return sha(s.strip().encode("utf-8"))


class Paper:
    def __init__(self, theme: Path):
        self.theme = theme
        self.dir = theme / "paper"
        self.yml_path = self.dir / "paper.yml"
        self.state_path = self.dir / "paper.state.json"

    def load(self) -> None:
        if not self.yml_path.exists():
            sys.exit(f"error: no existe {self.yml_path.relative_to(ROOT)} (usa --init)")
        self.cfg = yaml.safe_load(self.yml_path.read_text(encoding="utf-8"))
        self.sections = self.cfg["sections"]
        self.ids = [s["id"] for s in self.sections]
        self.state = json.loads(self.state_path.read_text(encoding="utf-8")) if self.state_path.exists() else {"sections": {}, "versions": {}}

    def save_state(self) -> None:
        self.state_path.write_text(json.dumps(self.state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def versions(self) -> list[str]:
        vs = [p.name for p in self.dir.iterdir() if p.is_dir() and VERSION_RE.match(p.name)] if self.dir.exists() else []
        key = lambda v: (VERSION_RE.match(v).group(1), int(VERSION_RE.match(v).group(2) or 1))
        return sorted(vs, key=key)

    def latest(self) -> str | None:
        vs = self.versions()
        return vs[-1] if vs else None

    def read_sections(self, version: str, stage: str) -> dict[str, str]:
        f = self.dir / version / FILES[stage]
        return {m.group(1): m.group(2) for m in SECTION_RE.finditer(f.read_text(encoding="utf-8"))} if f.exists() else {}

    def dep_hash(self, dep: str) -> str | None:
        if dep == "all":
            return sha(json.dumps({k: v.get("content_hash") for k, v in sorted(self.state["sections"].items())}).encode())
        if dep in self.ids:
            return (self.state["sections"].get(dep, {}).get("content_hash") or {}).get("polish") or "-"
        p = self.theme / dep
        if p.is_file():
            return sha(p.read_bytes())
        if p.is_dir():
            files = sorted(f for f in p.rglob("*") if f.is_file() and "_raw" not in f.parts)
            return sha("".join(f"{f.relative_to(p)}:{sha(f.read_bytes())}" for f in files).encode()) if files else None
        return None

    def sources(self, sec: dict) -> dict[str, str | None]:
        return {d: self.dep_hash(d) for d in sec.get("depends_on", [])}


def cmd_init(p: Paper) -> int:
    if p.yml_path.exists():
        print(f"ya existe {p.yml_path.relative_to(ROOT)}")
        return 0
    p.dir.mkdir(parents=True, exist_ok=True)
    p.yml_path.write_text(DEFAULT_YML, encoding="utf-8")
    print(f"creado {p.yml_path.relative_to(ROOT)} (Introducción enabled; resto off)")
    return 0


def cmd_new_version(p: Paper) -> int:
    p.load()
    prev = p.latest()
    today = dt.date.today().isoformat()
    name, n = today, 1
    while (p.dir / name).exists():
        n += 1
        name = f"{today}-{n}"
    (p.dir / name).mkdir(parents=True)
    if prev:
        for f in FILES.values():
            if (p.dir / prev / f).exists():
                shutil.copy2(p.dir / prev / f, p.dir / name / f)
    p.state["versions"][name] = {"from": prev, "borrador": False, "polish": False}
    p.save_state()
    print(f"nueva versión: paper/{name}/ (copiada de {prev or '—'})")
    return cmd_status(p, header=False)


def cmd_update(p: Paper, stage: str) -> int:
    p.load()
    v = p.latest()
    if not v:
        sys.exit("error: no hay versiones (usa --new-version)")
    found = p.read_sections(v, stage)
    if not found:
        sys.exit(f"error: paper/{v}/{FILES[stage]} no tiene marcadores <!-- paper:section id=… -->")
    by_id = {s["id"]: s for s in p.sections}
    for sid, content in found.items():
        sec = by_id.get(sid)
        if sec is None:
            print(f"WARN: sección '{sid}' no está en paper.yml")
            continue
        st = p.state["sections"].setdefault(sid, {})
        st.setdefault("content_hash", {})[stage] = text_hash(content)
        st["version"] = v
        if not sec.get("frozen"):
            st["sources_hash"] = p.sources(sec)
            st["status"] = "polished" if stage == "polish" else "borrador"
    p.state["versions"].setdefault(v, {})[stage] = True
    p.save_state()
    print(f"actualizado paper.state.json · paper/{v}/{FILES[stage]} · {len(found)} secciones")
    return cmd_status(p, header=False)


def cmd_status(p: Paper, header: bool = True) -> int:
    if header:
        p.load()
    v = p.latest()
    current = {st: (p.read_sections(v, st) if v else {}) for st in FILES}
    rows, regen, blocked, stale, errors = [], [], [], [], []
    for sec in p.sections:
        sid = sec["id"]
        st = p.state["sections"].get(sid, {})
        srcs = p.sources(sec)
        missing = [d for d, h in srcs.items() if h is None]
        changed = [d for d, h in srcs.items() if h is not None and st.get("sources_hash", {}).get(d) not in (None, h)]
        if sec.get("derived"):
            status = "derived"
        elif not sec.get("enabled"):
            status = "off"
        elif missing:
            status = "blocked"
            blocked.append(f"{sid} (falta {', '.join(missing)})")
        elif sec.get("frozen"):
            status = "stale" if changed else st.get("status", "pending")
            if changed:
                stale.append(f"{sid} ({', '.join(changed)})")
            for stage, secs in current.items():
                h = st.get("content_hash", {}).get(stage)
                if h and sid in secs and text_hash(secs[sid]) != h:
                    errors.append(f"frozen '{sid}' fue editado en paper/{v}/{FILES[stage]}")
        else:
            status = "regenerar"
            regen.append(sid)
        rows.append((sid, "on" if sec.get("enabled") else "off", "sí" if sec.get("frozen") else "no", status, ", ".join(changed) or "—", st.get("version", "—")))
    print(f"paper/ · última versión: {v or '—'} · citation: {p.cfg.get('format', {}).get('citation', 'apa7')} · numbering: {p.cfg.get('format', {}).get('numbering', 'roman')}")
    print("| Sección | enabled | frozen | status | fuente cambiada | versión |")
    print("|---|---|---|---|---|---|")
    for r in rows:
        print("| " + " | ".join(r) + " |")
    print(f"\nA regenerar: {', '.join(regen) or '—'}")
    if stale:
        print(f"STALE (frozen, no se tocan; decide si descongelar): {'; '.join(stale)}")
    if blocked:
        print(f"BLOCKED (datos faltantes, no se generan): {'; '.join(blocked)}")
    if errors:
        print("FAIL:\n  - " + "\n  - ".join(errors))
        return 1
    return 0


APA_PAREN = re.compile(r"\(([^()]*?\b(?:19|20)\d{2}[a-z]?)\)")
APA_NARR = re.compile(r"([A-ZÁÉÍÓÚÑ][\wÁÉÍÓÚÑáéíóúñ'\-]+)(?: et al\.| (?:y|&) [A-ZÁÉÍÓÚÑ][\w'\-]+)? \(((?:19|20)\d{2}[a-z]?)\)")


def split_refs(text: str) -> tuple[str, list[str]]:
    m = re.search(r"^##\s+(?:[IVXLC]+\.\s+|\d+\.\s+)?Referencias.*$", text, flags=re.M | re.I)
    if not m:
        return text, []
    body, tail = text[: m.start()], text[m.end():]
    refs = [l.strip() for l in tail.splitlines() if l.strip() and not l.startswith("<!--") and not l.startswith("#")]
    return body, refs


def cmd_cites(p: Paper, target: str | None) -> int:
    p.load()
    style = p.cfg.get("format", {}).get("citation", "apa7").lower()
    if target:
        f = Path(target)
    else:
        v = p.latest()
        f = p.dir / v / FILES["polish"] if v and (p.dir / v / FILES["polish"]).exists() else (p.dir / v / FILES["borrador"] if v else None)
    if not f or not f.exists():
        sys.exit("error: no hay archivo del paper que revisar")
    text = f.read_text(encoding="utf-8")
    body, refs = split_refs(text)
    issues: list[str] = []
    if style == "ieee":
        order: list[int] = []
        for m in re.finditer(r"\[(\d+)\](?:\s*[-–]\s*\[(\d+)\])?", body):
            a, b = int(m.group(1)), int(m.group(2) or m.group(1))
            for n in range(a, b + 1):
                if n not in order:
                    order.append(n)
        ref_nums = [int(m.group(1)) for r in refs if (m := re.match(r"\[(\d+)\]", r))]
        if order != list(range(1, len(order) + 1)):
            issues.append(f"numeración no sigue el orden de primera aparición: {order}")
        issues += [f"[{n}] citado sin referencia" for n in order if n not in ref_nums]
        issues += [f"[{n}] en Referencias pero no citado" for n in ref_nums if n not in order]
    else:
        cited: set[tuple[str, str]] = set()
        for m in APA_PAREN.finditer(body):
            for part in m.group(1).split(";"):
                mm = re.match(r"\s*(?:p\.\s*ej\.,?\s*|e\.\s*g\.,?\s*|véase\s+)?([A-ZÁÉÍÓÚÑ][\wÁÉÍÓÚÑáéíóúñ'\-]+).*?,\s*((?:19|20)\d{2}[a-z]?)", part)
                if mm:
                    cited.add((mm.group(1), mm.group(2)))
        for m in APA_NARR.finditer(body):
            cited.add((m.group(1), m.group(2)))
        ref_keys = []
        for r in refs:
            mm = re.match(r"(?:[-*]\s*)?([A-ZÁÉÍÓÚÑ][\wÁÉÍÓÚÑáéíóúñ'\-]+),.*?\(((?:19|20)\d{2}[a-z]?)\)", r)
            if mm:
                ref_keys.append((mm.group(1), mm.group(2)))
        issues += [f"({a}, {y}) citado sin referencia" for a, y in sorted(cited) if (a, y) not in ref_keys]
        issues += [f"{a} ({y}) en Referencias pero no citado" for a, y in ref_keys if (a, y) not in cited]
        surnames = [a for a, _ in ref_keys]
        if surnames != sorted(surnames, key=str.casefold):
            issues.append(f"Referencias no están en orden alfabético: {surnames}")
    rel = f.relative_to(ROOT) if f.is_absolute() and ROOT in f.parents else f
    if issues:
        print(f"FAIL citas ({style}) · {rel}")
        for i in issues:
            print(f"  - {i}")
        return 1
    print(f"PASS citas ({style}) · {rel} · {len(refs)} referencias")
    return 0


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 2
    theme = Path(argv[0])
    theme = theme if theme.is_absolute() else ROOT / theme
    if not theme.is_dir():
        sys.exit(f"error: no existe el tema {argv[0]}")
    p = Paper(theme)
    flag = argv[1] if len(argv) > 1 else None
    if flag == "--init":
        return cmd_init(p)
    if flag == "--new-version":
        return cmd_new_version(p)
    if flag == "--update":
        if len(argv) < 3 or argv[2] not in FILES:
            sys.exit("uso: --update borrador|polish")
        return cmd_update(p, argv[2])
    if flag == "--cites":
        return cmd_cites(p, argv[2] if len(argv) > 2 else None)
    return cmd_status(p)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
