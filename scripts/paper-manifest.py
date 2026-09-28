#!/usr/bin/env python3
"""Manifiesto del paper RSL por secciones: docs/<slug>/paper/paper.yml (+ paper.shadow.yml, paper.state.jsonc).

Uso:
  python3 scripts/paper-manifest.py docs/<slug>                    # estado + qué mejorar / reescribir (FAIL si una sección frozen fue editada)
  python3 scripts/paper-manifest.py docs/<slug> --init             # crea paper.yml + paper.shadow.yml por defecto
  python3 scripts/paper-manifest.py docs/<slug> --migrate          # convierte el paper.yml antiguo (enabled/frozen) y paper.state.json
  python3 scripts/paper-manifest.py docs/<slug> --new-version      # crea paper/<fecha>/ copiando la versión anterior
  python3 scripts/paper-manifest.py docs/<slug> --update borrador  # registra hashes tras escribir paper-borrador.md
  python3 scripts/paper-manifest.py docs/<slug> --update polish    # registra hashes tras escribir paper-polish.md
  python3 scripts/paper-manifest.py docs/<slug> --cites [archivo]  # citas en texto vs referencias (format.citation)

paper.yml lo edita el usuario (frozen / on / rewrite / off + formato).
paper.shadow.yml: títulos, grupos, depends_on y formato avanzado.
paper.state.jsonc: hashes y versiones; lo gestiona este script.
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

GROUPS = [
    ("portada", "Portada"),
    ("introduccion", "Introducción"),
    ("metodologia", "Metodología"),
    ("resultados", "Resultados"),
    ("discusion", "Discusión"),
    ("conclusion", "Conclusión"),
]
STATES = {"on": (True, False), "rewrite": (True, False), "frozen": (True, True), "off": (False, False)}
STATE_ALIASES = {True: "on", False: "off"}  # PyYAML lee on/off como booleanos
FORMATO = {  # clave humana -> (clave interna, {valor humano: valor interno})
    "idioma": ("language", None),
    "numeracion": ("numbering", {"romana": "roman", "arabiga": "arabic", "ninguna": "none"}),
    "citas": ("citation", {"apa7": "apa7", "ieee": "ieee"}),
    "resumen": ("abstract", None),
    "resultados_por": ("results_by", {"rq": "rq", "tema": "tema"}),
}
DEFAULT_ON = {"encabezado", "contexto", "problema", "justificacion", "objetivo-rsl", "organizacion"}

DEFAULT_SHADOW = """\
# Configuración técnica del paper; normalmente no se edita.
# Para activar, congelar o apagar secciones edita paper.yml.
#   title: encabezado que usa la skill · group: capítulo · depends_on: fuentes que, si cambian, marcan la sección como 'stale'
#   depends_on especiales: all (todo el paper) · grupos (qué capítulos están on/frozen)
#   derived: se reconstruye sola (Referencias sale de las citas del texto)
version: 1
format:
  subsection_letters: true   # A. B. C. dentro de Metodología / Resultados
  keywords_from: picoc       # palabras clave del abstract salen de picoc(-polish).md
  examples: global/examples  # papers de referencia (solo estructura / presentación)
sections:
  - { id: encabezado,   title: "Título · Tema · Problemática · Objetivo", group: portada, depends_on: [topic.md, informe-polish.md, picoc.md] }
  - { id: resumen,      title: "Abstract / Resumen + palabras clave",     group: portada, depends_on: [all] }
  # Introducción
  - { id: contexto,      title: Contexto,           group: introduccion, depends_on: [RSL/MD] }
  - { id: problema,      title: El problema,        group: introduccion, depends_on: [picoc.md] }
  - { id: justificacion, title: Justificación,      group: introduccion, depends_on: [informe-polish.md] }
  - { id: objetivo-rsl,  title: Objetivo de la RSL, group: introduccion, depends_on: [picoc.md] }
  - { id: organizacion,  title: Organización del contenido de la revisión, group: introduccion, depends_on: [grupos] }
  # Metodología
  - { id: marco-pico,          title: "Pregunta PICO y sus componentes",        group: metodologia, depends_on: [picoc.md] }
  - { id: palabras-clave,      title: Palabras clave pertinentes,               group: metodologia, depends_on: [picoc.md] }
  - { id: ecuacion-busqueda,   title: Ecuación de búsqueda,                     group: metodologia, depends_on: [picoc.md] }
  - { id: criterios-seleccion, title: Criterios de inclusión y exclusión,       group: metodologia, depends_on: [topic.md, picoc.md] }
  - { id: seleccion-prisma,    title: "Proceso de selección — Diagrama PRISMA", group: metodologia, depends_on: [RSL/seleccion] }
  - { id: calidad,             title: Evaluación de calidad,                    group: metodologia, depends_on: [RSL/seleccion] }
  # Resultados (requieren RSL/seleccion y RSL/extraccion, preparados por el usuario)
  - { id: distribucion,        title: Distribución anual de publicaciones, group: resultados, depends_on: [RSL/extraccion] }
  - { id: hallazgos-generales, title: Hallazgos generales,                 group: resultados, depends_on: [RSL/extraccion] }
  - { id: resultados-rq,       title: Resultados por pregunta,             group: resultados, depends_on: [picoc.md, RSL/extraccion] }
  # Discusión
  - { id: discusion-temas, title: Discusión por tema,                      group: discusion, depends_on: [resultados-rq] }
  - { id: discusion-rq,    title: Discusión por pregunta de investigación, group: discusion, depends_on: [resultados-rq] }
  - { id: amenazas,        title: Amenazas a la validez,                   group: discusion, depends_on: [ecuacion-busqueda, seleccion-prisma] }
  # Conclusión · Referencias
  - { id: conclusion,  title: Conclusión,  group: conclusion,  depends_on: [resultados-rq, discusion-rq] }
  - { id: referencias, title: Referencias, group: referencias, derived: true }
"""

HUMAN_HEADER = """\
# Qué hacer con cada sección en la próxima corrida de rsl-make-paper / rsl-polish-paper:
#   frozen   -> está bien: no se toca, se copia tal cual (si cambia su fuente, se avisa como 'stale')
#   on       -> revisar y mejorar: se conserva la base y se corrige / pule
#   rewrite  -> reescribir: se replantea desde cero a partir de las fuentes
#   off      -> inactivo: no se genera ni aparece
# Detalle técnico (títulos, dependencias): paper.shadow.yml · Estado interno: paper.state.jsonc (no editar)

formato:
  idioma: {idioma}              # idioma del paper: es | en | pt | fr | de (cualquier código ISO 639-1)
  numeracion: {numeracion}      # romana | arabiga | ninguna
  citas: {citas}             # apa7 | ieee
  resumen: [{resumen}]       # idiomas del Abstract/Resumen
  resultados_por: {resultados_por}      # rq | tema
"""

STATE_HEADER = """\
// NO EDITAR A MANO. Lo gestiona scripts/paper-manifest.py (--update / --new-version).
// Para activar, congelar o apagar secciones, edita paper.yml.
"""


def render_human(fmt: dict, shadow_sections: list[dict], states: dict[str, str]) -> str:
    inv = {k: {iv: hv for hv, iv in (m or {}).items()} for k, (_, m) in FORMATO.items()}
    human_fmt = {}
    for hk, (ik, m) in FORMATO.items():
        v = fmt.get(ik)
        human_fmt[hk] = ", ".join(v) if hk == "resumen" else inv[hk].get(v, v)
    out = [HUMAN_HEADER.format(**human_fmt).rstrip("\n")]
    for gid, label in GROUPS:
        ids = [s["id"] for s in shadow_sections if s.get("group") == gid and not s.get("derived")]
        if not ids:
            continue
        out.append(f"\n{label}:")
        w = max(len(i) for i in ids) + 1
        out += [f"  {(i + ':').ljust(w)} {states.get(i, 'off')}" for i in ids]
    out.append("\n# Referencias: automáticas (siempre se derivan de las citas del texto)\n")
    return "\n".join(out)


def default_human() -> str:
    shadow = yaml.safe_load(DEFAULT_SHADOW)
    fmt = {"language": "es", "numbering": "roman", "citation": "apa7", "abstract": ["en", "es"], "results_by": "rq"}
    return render_human(fmt, shadow["sections"], {i: "on" for i in DEFAULT_ON})


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:12]


def text_hash(s: str) -> str:
    return sha(s.strip().encode("utf-8"))


class Paper:
    def __init__(self, theme: Path):
        self.theme = theme
        self.dir = theme / "paper"
        self.yml_path = self.dir / "paper.yml"
        self.shadow_path = self.dir / "paper.shadow.yml"
        self.state_path = self.dir / "paper.state.jsonc"
        self.legacy_state_path = self.dir / "paper.state.json"

    def rel(self, f: Path) -> Path:
        return f.relative_to(ROOT) if ROOT in f.parents else f

    def load(self) -> None:
        if not self.yml_path.exists():
            sys.exit(f"error: no existe {self.rel(self.yml_path)} (usa --init)")
        human = yaml.safe_load(self.yml_path.read_text(encoding="utf-8")) or {}
        if isinstance(human.get("sections"), list):
            sys.exit(f"error: {self.rel(self.yml_path)} tiene el formato antiguo (enabled/frozen); usa --migrate")
        if not self.shadow_path.exists():
            sys.exit(f"error: no existe {self.rel(self.shadow_path)} (usa --init para crearlo)")
        shadow = yaml.safe_load(self.shadow_path.read_text(encoding="utf-8"))
        self.cfg = {"format": dict(shadow.get("format") or {})}
        errors: list[str] = []
        for hk, v in (human.get("formato") or {}).items():
            if hk not in FORMATO:
                errors.append(f"formato.{hk} desconocido (válidos: {', '.join(FORMATO)})")
                continue
            ik, m = FORMATO[hk]
            if m is not None and v not in m:
                errors.append(f"formato.{hk}: '{v}' no válido (usa {' | '.join(m)})")
                continue
            self.cfg["format"][ik] = m[v] if m else v
        states: dict[str, str] = {}
        for key, block in human.items():
            if key == "formato" or not isinstance(block, dict):
                continue
            for sid, raw in block.items():
                val = STATE_ALIASES.get(raw, raw)
                if val not in STATES:
                    errors.append(f"{sid}: estado '{raw}' no válido (usa frozen | on | rewrite | off)")
                states[sid] = val
        self.sections = shadow["sections"]
        self.ids = [s["id"] for s in self.sections]
        for sid in states:
            if sid not in self.ids:
                errors.append(f"sección '{sid}' no existe en paper.shadow.yml (válidas: {', '.join(i for i in self.ids if i != 'referencias')})")
        if errors:
            sys.exit("error en paper.yml:\n  - " + "\n  - ".join(errors))
        for sec in self.sections:
            if sec.get("derived"):
                sec["enabled"], sec["frozen"] = True, False
                continue
            if sec["id"] not in states:
                print(f"WARN: '{sec['id']}' no está en paper.yml; se trata como off")
            sec["estado"] = states.get(sec["id"], "off")
            sec["enabled"], sec["frozen"] = STATES.get(sec["estado"], (False, False))
        self.state = self.read_state()

    def read_state(self) -> dict:
        if self.state_path.exists():
            text = "\n".join(l for l in self.state_path.read_text(encoding="utf-8").splitlines() if not l.lstrip().startswith("//"))
            return json.loads(text)
        if self.legacy_state_path.exists():
            return json.loads(self.legacy_state_path.read_text(encoding="utf-8"))
        return {"sections": {}, "versions": {}}

    def save_state(self) -> None:
        self.state_path.write_text(STATE_HEADER + json.dumps(self.state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if self.legacy_state_path.exists():
            self.legacy_state_path.unlink()

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
        if dep == "grupos":
            return sha(",".join(sorted({s.get("group", "") for s in self.sections if s.get("enabled")})).encode())
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
    p.dir.mkdir(parents=True, exist_ok=True)
    for path, content in ((p.shadow_path, DEFAULT_SHADOW), (p.yml_path, default_human())):
        if path.exists():
            print(f"ya existe {p.rel(path)}")
        else:
            path.write_text(content, encoding="utf-8")
            print(f"creado {p.rel(path)}")
    return 0


def cmd_migrate(p: Paper) -> int:
    if not p.yml_path.exists():
        sys.exit(f"error: no existe {p.rel(p.yml_path)}")
    old = yaml.safe_load(p.yml_path.read_text(encoding="utf-8"))
    if not isinstance(old.get("sections"), list):
        print("paper.yml ya está en el formato nuevo")
    else:
        rename = {"abstract": "resumen"}
        states = {}
        for s in old["sections"]:
            if s.get("derived"):
                continue
            sid = rename.get(s["id"], s["id"])
            states[sid] = "frozen" if s.get("frozen") else ("on" if s.get("enabled") else "off")
        shadow = yaml.safe_load(DEFAULT_SHADOW)
        p.shadow_path.write_text(DEFAULT_SHADOW, encoding="utf-8")
        p.yml_path.write_text(render_human(old.get("format") or {}, shadow["sections"], states), encoding="utf-8")
        print(f"migrado {p.rel(p.yml_path)} + creado {p.rel(p.shadow_path)}")
        if p.legacy_state_path.exists():
            st = json.loads(p.legacy_state_path.read_text(encoding="utf-8"))
            for a, b in rename.items():
                if a in st.get("sections", {}):
                    st["sections"][b] = st["sections"].pop(a)
            p.state = st
            p.save_state()
            print(f"migrado estado -> {p.rel(p.state_path)}")
    return cmd_status(p)


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
            print(f"WARN: sección '{sid}' no está en paper.shadow.yml")
            continue
        st = p.state["sections"].setdefault(sid, {})
        st.setdefault("content_hash", {})[stage] = text_hash(content)
        st["version"] = v
        if not sec.get("frozen"):
            st["sources_hash"] = p.sources(sec)
            st["status"] = "polished" if stage == "polish" else "borrador"
        else:
            old = st.get("sources_hash", {})
            st["sources_hash"] = {d: old.get(d, h) for d, h in p.sources(sec).items()}
    p.state["versions"].setdefault(v, {})[stage] = True
    p.save_state()
    print(f"actualizado paper.state.jsonc · paper/{v}/{FILES[stage]} · {len(found)} secciones")
    return cmd_status(p, header=False)


def cmd_status(p: Paper, header: bool = True) -> int:
    if header:
        p.load()
    v = p.latest()
    current = {st: (p.read_sections(v, st) if v else {}) for st in FILES}
    rows, improve, rewrite, blocked, stale, errors = [], [], [], [], [], []
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
        elif sec["estado"] == "rewrite" or not any(sid in secs for secs in current.values()):
            status = "reescribir" if sec["estado"] == "rewrite" else "reescribir (nueva)"
            rewrite.append(sid)
        else:
            status = "mejorar"
            improve.append(sid)
        rows.append((sid, sec.get("estado", "auto"), status, ", ".join(changed) or "—", st.get("version", "—")))
    print(f"paper/ · última versión: {v or '—'} · idioma: {p.cfg.get('format', {}).get('language', 'es')} · citation: {p.cfg.get('format', {}).get('citation', 'apa7')} · numbering: {p.cfg.get('format', {}).get('numbering', 'roman')}")
    print("| Sección | estado | status | fuente cambiada | versión |")
    print("|---|---|---|---|---|")
    for r in rows:
        print("| " + " | ".join(r) + " |")
    print(f"\nA mejorar (on): {', '.join(improve) or '—'}")
    print(f"A reescribir (rewrite): {', '.join(rewrite) or '—'}")
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


def split_refs(text: str) -> tuple[str, list[str], bool]:
    m = re.search(r"^##\s+(?:[IVXLC]+\.\s+|\d+\.\s+)?Referencias.*$", text, flags=re.M | re.I)
    if not m:
        rows = [l for l in text.splitlines() if l.lstrip().startswith("|")]
        cells = [r.strip().strip("|").split("|")[0].strip() for r in rows]
        refs = [c for c in cells if re.search(r"\((?:19|20)\d{2}[a-z]?\)", c)]
        body = "\n".join(l for l in text.splitlines() if not l.lstrip().startswith("|"))
        return body, refs, True
    body, tail = text[: m.start()], text[m.end():]
    refs = [l.strip() for l in tail.splitlines() if l.strip() and not l.startswith("<!--") and not l.startswith("#")]
    return body, refs, False


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
    body, refs, from_table = split_refs(text)
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
        aliases = {m.group(2): m.group(1).split()[0] for m in re.finditer(r"([A-ZÁÉÍÓÚÑ][\w ]+?) \[([A-Z][\w]+)\]", body)}
        cited = {(aliases.get(a, a), y) for a, y in cited}
        ref_keys = []
        for r in refs:
            mm = re.match(r"(?:[-*]\s*)?([A-ZÁÉÍÓÚÑ][\wÁÉÍÓÚÑáéíóúñ'\-]+)[^()]*?\(((?:19|20)\d{2}[a-z]?)\)", r)
            if mm:
                ref_keys.append((mm.group(1), mm.group(2)))
        issues += [f"({a}, {y}) citado sin referencia" for a, y in sorted(cited) if (a, y) not in ref_keys]
        issues += [f"{a} ({y}) en Referencias pero no citado" for a, y in ref_keys if (a, y) not in cited]
        surnames = [a for a, _ in ref_keys]
        if not from_table and surnames != sorted(surnames, key=str.casefold):
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
    if flag == "--migrate":
        return cmd_migrate(p)
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
