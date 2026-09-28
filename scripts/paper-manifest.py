#!/usr/bin/env python3
"""Manifiesto del paper RSL por secciones: docs/<slug>/config.yml (+ paper/paper.shadow.yml, paper/paper.state.jsonc).

Uso:
  python3 scripts/paper-manifest.py docs/<slug>                    # estado + qué mejorar / reescribir (FAIL si una sección frozen fue editada)
  python3 scripts/paper-manifest.py docs/<slug> --init             # crea config.yml + paper/paper.shadow.yml por defecto
  python3 scripts/paper-manifest.py docs/<slug> --migrate          # mueve paper/paper.yml a config.yml y convierte el formato antiguo (enabled/frozen)
  python3 scripts/paper-manifest.py docs/<slug> --new-version      # crea paper/<fecha>/ copiando la versión anterior
  python3 scripts/paper-manifest.py docs/<slug> --update borrador  # registra hashes tras escribir paper-borrador.md
  python3 scripts/paper-manifest.py docs/<slug> --update polish    # registra hashes tras escribir paper-polish.md
  python3 scripts/paper-manifest.py docs/<slug> --cites [archivo]  # citas en texto vs referencias (format.citation)
  python3 scripts/paper-manifest.py docs/<slug> --picoc            # marco configurado + último picoc/<fecha>-<MARCO>/picoc.md

config.yml lo edita el usuario (frozen / on / rewrite / off + formato).
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

sys.path.insert(0, str(Path(__file__).resolve().parent))
import picoc_versions  # noqa: E402
from rsl_out import Fail, error, ok, run  # noqa: E402

try:
    import yaml
except ImportError:
    print("ERROR: falta PyYAML. Instálalo: pip install --user pyyaml | sudo pacman -S python-yaml | sudo apt install python3-yaml.")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
FILES = {"borrador": "paper-borrador.md", "polish": "paper-polish.md"}
OPTIONAL_DEPS = {"topic.md"}
VERSION_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:-([2-9]|[1-9]\d+))?$")
SECTION_RE = re.compile(r"<!-- paper:section id=([\w-]+) -->\n?(.*?)<!-- /paper:section -->", re.S)
MARK_RE = re.compile(r"<!--\s*(/)?\s*paper:section(?:\s+id=([\w-]+))?\s*-->")

GROUPS = [
    ("portada", "Portada"),
    ("introduccion", "Introducción"),
    ("metodologia", "Metodología"),
    ("resultados", "Resultados"),
    ("discusion", "Discusión"),
    ("conclusion", "Conclusión"),
    ("declaraciones", "Declaraciones"),
]
STATES = {"on": (True, False), "rewrite": (True, False), "frozen": (True, True), "off": (False, False)}
STATE_ALIASES = {True: "on", False: "off"}  # PyYAML lee on/off como booleanos
FORMATO = {  # clave humana -> (clave interna, {valor humano: valor interno})
    "idioma": ("language", None),
    "numeracion": ("numbering", {"romana": "roman", "arabiga": "arabic", "ninguna": "none"}),
    "citas": ("citation", {"apa7": "apa7", "ieee": "ieee"}),
    "resumen": ("abstract", None),
    "resultados_por": ("results_by", {"rq": "rq", "tema": "tema"}),
    "marco": ("framework", None),
}
DEFAULT_FMT = {"language": "es", "numbering": "roman", "citation": "apa7", "abstract": ["en", "es"], "results_by": "rq", "framework": picoc_versions.DEFAULT_MARCO}
DEFAULT_ON = {"encabezado", "contexto", "problema", "justificacion", "objetivo-rsl", "organizacion"}

DEFAULT_SHADOW = """\
# Configuración técnica del paper; normalmente no se edita.
# Para activar, congelar o apagar secciones edita config.yml (en la carpeta del tema).
#   title: encabezado que usa la skill · group: capítulo · depends_on: fuentes que, si cambian, marcan la sección como 'stale'
#   depends_on especiales: all (todo el paper) · grupos (qué capítulos están on/frozen) · picoc (último picoc/<fecha>-<MARCO>/picoc.md)
#   derived: se reconstruye sola (Referencias sale de las citas del texto)
version: 1
format:
  subsection_letters: true   # A. B. C. dentro de Metodología / Resultados
  keywords_from: picoc       # keywords del abstract = sección ## Keywords del último picoc/<fecha>-<MARCO>/picoc.md
  examples: global/examples  # papers de referencia (solo estructura / presentación)
sections:
  - { id: encabezado,   title: "Título · Tema · Problemática · Objetivo", group: portada, depends_on: [topic.md, informe-polish.md, picoc] }
  - { id: resumen,      title: "Abstract / Resumen + palabras clave",     group: portada, depends_on: [all] }
  # Introducción
  - { id: contexto,      title: Contexto,           group: introduccion, depends_on: [RSL/MD] }
  - { id: problema,      title: El problema,        group: introduccion, depends_on: [picoc] }
  - { id: justificacion, title: Justificación,      group: introduccion, depends_on: [informe-polish.md] }
  - { id: objetivo-rsl,  title: Objetivo de la RSL, group: introduccion, depends_on: [picoc] }
  - { id: organizacion,  title: Organización del contenido de la revisión, group: introduccion, depends_on: [grupos] }
  # Metodología
  - { id: marco-pico,          title: "Pregunta {marco} y sus componentes",        group: metodologia, depends_on: [picoc] }
  - { id: palabras-clave,      title: Palabras clave pertinentes,               group: metodologia, depends_on: [picoc] }
  - { id: ecuacion-busqueda,   title: Ecuación de búsqueda,                     group: metodologia, depends_on: [picoc] }
  - { id: criterios-seleccion, title: Criterios de inclusión y exclusión,       group: metodologia, depends_on: [topic.md, picoc] }
  - { id: seleccion-prisma,    title: "Proceso de selección — Diagrama PRISMA", group: metodologia, depends_on: [picoc] }
  - { id: calidad,             title: Evaluación de calidad,                    group: metodologia, depends_on: [RSL/seleccion] }
  - { id: extraccion-datos,    title: Extracción de datos,                      group: metodologia, depends_on: [picoc] }
  - { id: sintesis,            title: Síntesis de datos,                        group: metodologia, depends_on: [picoc] }
  # Resultados (requieren RSL/seleccion y RSL/extraccion, preparados por el usuario)
  - { id: distribucion,        title: Distribución anual de publicaciones, group: resultados, depends_on: [RSL/extraccion] }
  - { id: hallazgos-generales, title: Hallazgos generales,                 group: resultados, depends_on: [RSL/extraccion] }
  - { id: resultados-rq,       title: Resultados por pregunta,             group: resultados, depends_on: [picoc, RSL/extraccion] }
  # Discusión
  - { id: discusion-temas, title: Discusión por tema,                      group: discusion, depends_on: [resultados-rq] }
  - { id: discusion-rq,    title: Discusión por pregunta de investigación, group: discusion, depends_on: [resultados-rq] }
  - { id: amenazas,        title: Amenazas a la validez,                   group: discusion, depends_on: [ecuacion-busqueda, seleccion-prisma] }
  # Conclusión · Referencias
  - { id: conclusion,  title: Conclusión,  group: conclusion,  depends_on: [resultados-rq, discusion-rq] }
  # Declaraciones (PRISMA 2020, ítems 24–27): registro y protocolo, financiamiento, conflictos, datos
  - { id: declaraciones, title: Declaraciones, group: declaraciones, depends_on: [picoc] }
  - { id: referencias, title: Referencias, group: referencias, derived: true }
"""

HUMAN_HEADER = """\
# Qué hacer con cada sección en la próxima corrida de rsl-make-paper / rsl-polish-paper:
#   frozen   -> está bien: no se toca, se copia tal cual (si cambia su fuente, se avisa como 'stale')
#   on       -> revisar y mejorar: se conserva la base y se corrige / pule
#   rewrite  -> reescribir: se replantea desde cero a partir de las fuentes
#   off      -> inactivo: no se genera ni aparece
# Detalle técnico (títulos, dependencias): paper/paper.shadow.yml · Estado interno: paper/paper.state.jsonc (no editar)

formato:
  idioma: {idioma}              # idioma del paper: es | en | pt | fr | de (cualquier código ISO 639-1)
  numeracion: {numeracion}      # romana | arabiga | ninguna
  citas: {citas}             # apa7 | ieee
  resumen: [{resumen}]       # idiomas del Abstract/Resumen
  resultados_por: {resultados_por}      # rq | tema
  marco: {marco}           # marco de búsqueda libre: PICO, PIO, PICOC, PICOCT, PICOS… (por defecto PICOCT); al cambiarlo, correr rsl-picoc
"""

STATE_HEADER = """\
// NO EDITAR A MANO. Lo gestiona scripts/paper-manifest.py (--update / --new-version).
// Para activar, congelar o apagar secciones, edita config.yml (en la carpeta del tema).
"""


def render_human(fmt: dict, shadow_sections: list[dict], states: dict[str, str]) -> str:
    inv = {k: {iv: hv for hv, iv in (m or {}).items()} for k, (_, m) in FORMATO.items()}
    fmt = {**DEFAULT_FMT, **{k: v for k, v in (fmt if isinstance(fmt, dict) else {}).items() if v}}
    human_fmt = {}
    for hk, (ik, m) in FORMATO.items():
        v = fmt[ik]
        v = [v] if hk == "resumen" and isinstance(v, str) else v
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
    return render_human(DEFAULT_FMT, shadow["sections"], {i: "on" for i in DEFAULT_ON})


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:12]


def text_hash(s: str) -> str:
    return sha(s.strip().encode("utf-8"))


class Paper:
    def __init__(self, theme: Path):
        self.theme = theme
        self.dir = theme / "paper"
        self.yml_path = theme / picoc_versions.CONFIG
        self.legacy_yml_path = theme / picoc_versions.LEGACY_CONFIG
        self.shadow_path = self.dir / "paper.shadow.yml"
        self.state_path = self.dir / "paper.state.jsonc"
        self.legacy_state_path = self.dir / "paper.state.json"

    def rel(self, f: Path) -> Path:
        return f.relative_to(ROOT) if ROOT in f.parents else f

    def read_yaml(self, path: Path) -> dict:
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
        except yaml.YAMLError as e:
            where = getattr(e, "problem_mark", None)
            raise Fail(f"{self.rel(path)} no es YAML válido" + (f" (línea {where.line + 1})" if where else ""), "corrige la sintaxis (sangría, dos puntos, comillas)")
        except UnicodeDecodeError:
            raise Fail(f"{self.rel(path)} no está en UTF-8", "guárdalo como UTF-8")
        if data is None:
            data = {}
        if not isinstance(data, dict):
            raise Fail(f"{self.rel(path)} debe ser un mapa clave: valor", "restáuralo desde git o con --init")
        return data

    def load(self) -> None:
        if not self.yml_path.exists() and self.legacy_yml_path.exists():
            raise Fail(f"la configuración sigue en {self.rel(self.legacy_yml_path)}; ahora va en {self.rel(self.yml_path)}", "muévela con: pnpm -s paper:status <tema> --migrate")
        if not self.yml_path.exists():
            raise Fail(f"no existe {self.rel(self.yml_path)}", "crea el paper con: pnpm -s paper:status <tema> --init")
        human = self.read_yaml(self.yml_path)
        if isinstance(human.get("sections"), list):
            raise Fail(f"{self.rel(self.yml_path)} tiene el formato antiguo (enabled/frozen)", "conviértelo con: pnpm -s paper:status <tema> --migrate")
        if not self.shadow_path.exists():
            raise Fail(f"no existe {self.rel(self.shadow_path)}", "recréalo con: pnpm -s paper:status <tema> --init")
        shadow = self.read_yaml(self.shadow_path)
        secs = shadow.get("sections")
        if not isinstance(secs, list) or not secs or not all(isinstance(s, dict) and isinstance(s.get("id"), str) for s in secs):
            raise Fail(f"{self.rel(self.shadow_path)} no tiene una lista 'sections' válida (cada una con id)", "restáuralo desde git o bórralo y corre --init")
        ids = [s["id"] for s in secs]
        dup = sorted({i for i in ids if ids.count(i) > 1})
        if dup:
            raise Fail(f"{self.rel(self.shadow_path)} repite secciones: {', '.join(dup)}", "deja un solo id por sección")
        added: set[str] = set()
        defaults = yaml.safe_load(DEFAULT_SHADOW)["sections"]
        for i, d in enumerate(defaults):
            if d["id"] in ids:
                continue
            prev = next((defaults[j]["id"] for j in range(i - 1, -1, -1) if defaults[j]["id"] in ids), None)
            pos = ids.index(prev) + 1 if prev else 0
            secs.insert(pos, dict(d))
            ids.insert(pos, d["id"])
            added.add(d["id"])
        self.cfg = {"format": dict(shadow.get("format") or {}) if isinstance(shadow.get("format"), dict) else {}}
        errors: list[str] = []
        formato = human.get("formato") or {}
        if not isinstance(formato, dict):
            errors.append("formato debe ser un bloque clave: valor")
            formato = {}
        for hk, v in formato.items():
            if hk in ("idioma",) and not (isinstance(v, str) and re.fullmatch(r"[a-z]{2}", v)):
                errors.append(f"formato.idioma: '{v}' no válido (código ISO 639-1 de dos letras, p. ej. es, en)")
                continue
            if hk == "resumen":
                v = [v] if isinstance(v, str) else v
                if not (isinstance(v, list) and v and all(isinstance(x, str) and re.fullmatch(r"[a-z]{2}", x) for x in v)):
                    errors.append(f"formato.resumen: '{v}' no válido (lista de códigos de idioma, p. ej. [en, es])")
                    continue
            if hk not in FORMATO:
                errors.append(f"formato.{hk} desconocido (válidos: {', '.join(FORMATO)})")
                continue
            ik, m = FORMATO[hk]
            if hk == "marco":
                try:
                    v = picoc_versions.marco_label(v)
                except picoc_versions.MarcoError as e:
                    errors.append(f"formato.marco: {e}")
                    continue
            if m is not None and (not isinstance(v, str) or v not in m):
                errors.append(f"formato.{hk}: '{v}' no válido (usa {' | '.join(m)})")
                continue
            self.cfg["format"][ik] = m[v] if m else v
        states: dict[str, str] = {}
        for key, block in human.items():
            if key == "formato" or not isinstance(block, dict):
                continue
            for sid, raw in block.items():
                val = STATE_ALIASES.get(raw, raw.strip().lower() if isinstance(raw, str) else raw) if isinstance(raw, (str, bool)) else raw
                if not isinstance(val, str) or val not in STATES:
                    errors.append(f"{sid}: estado '{raw}' no válido (usa frozen | on | rewrite | off)")
                states[sid] = val
        self.cfg["format"].setdefault("framework", picoc_versions.DEFAULT_MARCO)
        self.sections = secs
        for sec in self.sections:
            sec["title"] = str(sec.get("title", "")).replace("{marco}", self.cfg["format"]["framework"])
        self.ids = [s["id"] for s in self.sections]
        for sid in states:
            if sid not in self.ids:
                errors.append(f"sección '{sid}' no existe en paper.shadow.yml (válidas: {', '.join(i for i in self.ids if i != 'referencias')})")
        if errors:
            for e in errors:
                print(f"  - {e}")
            raise Fail(f"{self.rel(self.yml_path)} tiene {len(errors)} valor(es) inválido(s) (ver detalle arriba)", "corrígelos en config.yml")
        for sec in self.sections:
            if sec.get("derived"):
                sec["enabled"], sec["frozen"] = True, False
                continue
            if sec["id"] not in states and sec["id"] not in added:
                print(f"WARN: '{sec['id']}' no está en config.yml; se trata como off")
            sec["estado"] = states.get(sec["id"], "off")
            sec["enabled"], sec["frozen"] = STATES.get(sec["estado"], (False, False))
        self.state = self.read_state()
        for st in self.state.get("sections", {}).values():
            src = st.get("sources_hash") or {}
            if "picoc.md" in src:
                src.setdefault("picoc", src.pop("picoc.md"))

    def read_state(self) -> dict:
        path = self.state_path if self.state_path.exists() else (self.legacy_state_path if self.legacy_state_path.exists() else None)
        if path is None:
            return {"sections": {}, "versions": {}}
        try:
            text = "\n".join(l for l in path.read_text(encoding="utf-8").splitlines() if not l.lstrip().startswith("//"))
            data = json.loads(text) if text.strip() else {}
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            raise Fail(f"{self.rel(path)} está corrupto ({e.__class__.__name__})", "restáuralo con git checkout, o bórralo para reconstruir el estado (se pierden los hashes de frozen)")
        if not isinstance(data, dict):
            raise Fail(f"{self.rel(path)} está corrupto (no es un objeto)", "restáuralo con git checkout o bórralo")
        data.setdefault("sections", {})
        data.setdefault("versions", {})
        if not isinstance(data["sections"], dict) or not isinstance(data["versions"], dict):
            raise Fail(f"{self.rel(path)} está corrupto (sections/versions)", "restáuralo con git checkout o bórralo")
        return data

    def save_state(self) -> None:
        self.state_path.write_text(STATE_HEADER + json.dumps(self.state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if self.legacy_state_path.exists():
            self.legacy_state_path.unlink()

    def versions(self) -> list[str]:
        vs = []
        for p in (self.dir.iterdir() if self.dir.exists() else []):
            m = VERSION_RE.match(p.name)
            if not (p.is_dir() and m and (day := picoc_versions.version_date(m.group(1)))):
                continue
            if day > dt.date.today():
                raise Fail(f"paper/{p.name} tiene fecha futura", "renómbrala o bórrala; las versiones las crea --new-version")
            vs.append(p.name)
        return sorted(vs, key=lambda v: (v[:10], int(VERSION_RE.match(v).group(2) or 1)))

    def latest(self) -> str | None:
        vs = self.versions()
        return vs[-1] if vs else None

    def read_sections(self, version: str, stage: str) -> dict[str, str]:
        f = self.dir / version / FILES[stage]
        if not f.exists():
            return {}
        try:
            text = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            raise Fail(f"{self.rel(f)} no está en UTF-8", "guárdalo como UTF-8")
        problems, ids, open_id = [], [], None
        for m in MARK_RE.finditer(text):
            line = text.count("\n", 0, m.start()) + 1
            if not m.group(1):
                sid = m.group(2)
                if open_id:
                    problems.append(f"L{line}: '{sid}' se abre antes de cerrar '{open_id}'")
                if not sid:
                    problems.append(f"L{line}: marcador de apertura sin id")
                elif sid in ids:
                    problems.append(f"L{line}: la sección '{sid}' está repetida")
                ids.append(sid)
                open_id = sid or "?"
            else:
                if not open_id:
                    problems.append(f"L{line}: cierre <!-- /paper:section --> sin apertura")
                open_id = None
        if open_id:
            problems.append(f"la sección '{open_id}' no se cierra")
        if problems:
            for pr in problems:
                print(f"  - {pr}")
            raise Fail(f"{self.rel(f)} tiene marcadores de sección rotos", "cada sección va entre <!-- paper:section id=X --> y <!-- /paper:section -->, sin anidar ni repetir")
        return {m.group(1): m.group(2) for m in SECTION_RE.finditer(text)}

    def dep_hash(self, dep: str) -> str | None:
        if dep == "grupos":
            return sha(",".join(sorted({s.get("group", "") for s in self.sections if s.get("enabled")})).encode())
        if dep == "all":
            return sha(json.dumps({k: v.get("content_hash") for k, v in sorted(self.state["sections"].items())}).encode())
        if dep == "picoc":
            _, f, state = picoc_versions.status(self.theme)
            return sha(f.read_bytes()) if state == "OK" else None
        if dep in self.ids:
            return (self.state["sections"].get(dep, {}).get("content_hash") or {}).get("polish") or "-"
        p = self.theme / dep
        if dep == "informe-polish.md" and not p.is_file():
            p = self.theme / "informe.md"
        if dep in OPTIONAL_DEPS and not p.exists():
            return "-"
        if p.is_file():
            return sha(p.read_bytes())
        if p.is_dir():
            files = sorted(f for f in p.rglob("*") if f.is_file() and "_raw" not in f.parts)
            return sha("".join(f"{f.relative_to(p)}:{sha(f.read_bytes())}" for f in files).encode()) if files else None
        return None

    def sources(self, sec: dict) -> dict[str, str | None]:
        return {d: self.dep_hash(d) for d in sec.get("depends_on", [])}


def next_step(p: Paper, c: dict | None = None) -> str:
    if not any((p.theme / f).is_file() for f in ("informe-polish.md", "informe.md")):
        return "rsl-make-report"
    if picoc_versions.status(p.theme)[2] != "OK":
        return f"Usa rsl-picoc sobre {p.rel(p.theme)}/"
    if c is None:
        return "rsl-make-paper"
    if not c["improve"] and not c["rewrite"]:
        return "pon en on o rewrite las secciones a trabajar en config.yml"
    vstate = p.state["versions"].get(c["version"], {}) if c["version"] else {}
    if vstate.get("borrador") and not vstate.get("polish"):
        return "rsl-polish-paper"
    if vstate.get("polish"):
        return "congela en config.yml las secciones validadas, o rsl-make-paper para una versión nueva"
    return "rsl-make-paper"


def cmd_init(p: Paper) -> int:
    if not p.yml_path.exists() and p.legacy_yml_path.exists():
        raise Fail(f"la configuración sigue en {p.rel(p.legacy_yml_path)}; ahora va en {p.rel(p.yml_path)}", "muévela con: pnpm -s paper:status <tema> --migrate (no --init)")
    p.dir.mkdir(parents=True, exist_ok=True)
    made, kept = [], []
    for path, content in ((p.shadow_path, DEFAULT_SHADOW), (p.yml_path, default_human())):
        if path.exists():
            kept.append(path.name)
        else:
            path.write_text(content, encoding="utf-8")
            made.append(path.name)
    p.load()
    return ok(f"paper/ listo (creados: {', '.join(made) or 'ninguno'}; ya existían: {', '.join(kept) or 'ninguno'})", next_step(p))


def cmd_migrate(p: Paper) -> int:
    moved = False
    if p.legacy_yml_path.exists():
        if p.yml_path.exists():
            raise Fail(f"hay dos configuraciones: {p.rel(p.yml_path)} y {p.rel(p.legacy_yml_path)}", f"quédate con {p.rel(p.yml_path)} y borra {p.rel(p.legacy_yml_path)}")
        p.legacy_yml_path.replace(p.yml_path)
        print(f"movido {p.rel(p.legacy_yml_path)} -> {p.rel(p.yml_path)}")
        moved = True
    if not p.yml_path.exists():
        raise Fail(f"no existe {p.rel(p.yml_path)}", "crea el paper con --init")
    old = p.read_yaml(p.yml_path)
    if isinstance(old.get("sections"), list):
        rename = {"abstract": "resumen"}
        states = {}
        for s in old["sections"]:
            if not isinstance(s, dict) or "id" not in s:
                raise Fail("config.yml antiguo con una sección sin id", "corrígelo a mano antes de migrar")
            if s.get("derived"):
                continue
            sid = rename.get(s["id"], s["id"])
            states[sid] = "frozen" if s.get("frozen") else ("on" if s.get("enabled") else "off")
        shadow = yaml.safe_load(DEFAULT_SHADOW)
        p.shadow_path.write_text(DEFAULT_SHADOW, encoding="utf-8")
        p.yml_path.write_text(render_human(old.get("format") or {}, shadow["sections"], states), encoding="utf-8")
        print(f"migrado {p.rel(p.yml_path)} + creado {p.rel(p.shadow_path)}")
        if p.legacy_state_path.exists():
            p.state = p.read_state()
            for a, b in rename.items():
                if a in p.state["sections"]:
                    p.state["sections"][b] = p.state["sections"].pop(a)
            p.save_state()
            print(f"migrado estado -> {p.rel(p.state_path)}")
        migrated = True
    else:
        migrated = False
    p.load()
    c = report(p)
    if c["errors"]:
        return frozen_error(c)
    done = [x for x, y in ((f"{picoc_versions.LEGACY_CONFIG} movido a {p.yml_path.name}", moved), (f"{p.yml_path.name} convertido al formato nuevo", migrated)) if y]
    return ok(" y ".join(done) if done else f"{p.yml_path.name} ya estaba al día; no se cambió nada", next_step(p, c))


def cmd_new_version(p: Paper) -> int:
    p.load()
    c = classify(p)
    if c["errors"]:
        report(p)
        return frozen_error(c)
    if not c["improve"] and not c["rewrite"]:
        report(p)
        return error("nada que generar: ninguna sección está en on o rewrite (no se creó versión)", "pon en on o rewrite las secciones a trabajar en config.yml")
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
    c = report(p)
    return ok(f"versión paper/{name}/ creada (copia de {prev or 'nada'}); a mejorar: {', '.join(c['improve']) or '—'}; a reescribir: {', '.join(c['rewrite']) or '—'}",
              "escribir esas secciones en paper-borrador.md (rsl-make-paper) o pulirlas (rsl-polish-paper)")


def cmd_update(p: Paper, stage: str) -> int:
    p.load()
    v = p.latest()
    if not v:
        raise Fail("no hay versiones del paper", "crea una con --new-version (rsl-make-paper)")
    if not (p.dir / v / FILES[stage]).exists():
        raise Fail(f"no existe paper/{v}/{FILES[stage]}", "escribe el archivo antes de registrarlo")
    found = p.read_sections(v, stage)
    if not found:
        raise Fail(f"paper/{v}/{FILES[stage]} no tiene marcadores <!-- paper:section id=… -->", "envuelve cada sección con sus marcadores")
    pre = classify(p)
    if pre["errors"]:
        report(p)
        return frozen_error(pre)
    by_id = {s["id"]: s for s in p.sections}
    unknown = []
    for sid, content in found.items():
        sec = by_id.get(sid)
        if sec is None:
            unknown.append(sid)
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
    if unknown:
        raise Fail(f"paper/{v}/{FILES[stage]} tiene secciones que no existen en paper.shadow.yml: {', '.join(unknown)}", "usa los ids de paper.shadow.yml (no se registró nada)")
    p.state["versions"].setdefault(v, {})[stage] = True
    p.save_state()
    c = report(p)
    return ok(f"registradas {len(found)} secciones de paper/{v}/{FILES[stage]}", next_step(p, c))


def frozen_error(c: dict) -> int:
    for e in c["errors"]:
        print(f"  - {e}")
    return error(f"{len(c['errors'])} sección(es) frozen fueron editadas", "restaura su texto (git checkout) o cambia su estado a on en config.yml")


def classify(p: Paper) -> dict:
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
    return {"version": v, "current": current, "rows": rows, "improve": improve, "rewrite": rewrite,
            "blocked": blocked, "stale": stale, "errors": errors}


def report(p: Paper) -> dict:
    c = classify(p)
    v, current, rows, improve, rewrite = c["version"], c["current"], c["rows"], c["improve"], c["rewrite"]
    fmt = p.cfg.get("format", {})
    vstate = p.state["versions"].get(v, {}) if v else {}
    stages = "/".join(s for s in FILES if vstate.get(s)) or "ninguna"
    print(f"paper/ · última versión: {v or '—'} (etapas cerradas: {stages}) · idioma: {fmt.get('language', 'es')} · citation: {fmt.get('citation', 'apa7')} · numbering: {fmt.get('numbering', 'roman')} · marco: {fmt['framework']}")
    print("| Sección | estado | status | fuente cambiada | versión |")
    print("|---|---|---|---|---|")
    for r in rows:
        print("| " + " | ".join(r) + " |")
    print(f"\nA mejorar (on): {', '.join(improve) or '—'}")
    print(f"A reescribir (rewrite): {', '.join(rewrite) or '—'}")
    if c["stale"]:
        print(f"STALE (frozen, no se tocan; decide si descongelar): {'; '.join(c['stale'])}")
    if c["blocked"]:
        print(f"BLOCKED (datos faltantes, no se generan): {'; '.join(c['blocked'])}")
    marco, pf, pstate = picoc_versions.status(p.theme)
    if pstate != "OK":
        print(f"WARN picoc {pstate}: marco configurado {marco} · último {p.rel(pf) if pf else '—'} → correr rsl-picoc (las secciones que dependen de picoc quedan BLOCKED)")
    marco_sec = next((secs["marco-pico"] for secs in (current["polish"], current["borrador"]) if "marco-pico" in secs), None)
    if marco_sec is not None and not re.search(rf"\b{marco}\b", marco_sec):
        print(f"WARN marco-pico no nombra el marco configurado ({marco})")
    return c


def cmd_status(p: Paper) -> int:
    p.load()
    c = report(p)
    if c["errors"]:
        return frozen_error(c)
    parts = [f"{len(c['improve'])} a mejorar", f"{len(c['rewrite'])} a reescribir"]
    if c["stale"]:
        parts.append(f"{len(c['stale'])} stale")
    if c["blocked"]:
        parts.append(f"{len(c['blocked'])} blocked")
    return ok(f"paper/{c['version'] or '—'}: " + ", ".join(parts), next_step(p, c))


APA_LOC = r"(?:,\s*(?:pp?\.|cap\.|párr\.)\s*[\w–\-, ]+?)?"
APA_PAREN = re.compile(r"\(([^()]*?\b(?:19|20)\d{2}[a-z]?" + APA_LOC + r")\)")
APA_NARR = re.compile(r"([A-ZÁÉÍÓÚÑ][\wÁÉÍÓÚÑáéíóúñ'\-]+)(?: et al\.| (?:y|&) [A-ZÁÉÍÓÚÑ][\w'\-]+)? \(((?:19|20)\d{2}[a-z]?)" + APA_LOC + r"\)")


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
        if not f.exists() and (p.theme / target).exists():
            f = p.theme / target
    else:
        v = p.latest()
        f = p.dir / v / FILES["polish"] if v and (p.dir / v / FILES["polish"]).exists() else (p.dir / v / FILES["borrador"] if v else None)
    if not f or not f.exists():
        raise Fail(f"no hay archivo que revisar ({target or 'el paper no tiene versiones'})", "indica un archivo existente o crea el borrador con rsl-make-paper")
    if f.is_dir():
        raise Fail(f"{target} es una carpeta, no un archivo", "indica el .md a revisar")
    try:
        text = f.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise Fail(f"{f} no está en UTF-8", "guárdalo como UTF-8")
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
        for i in issues:
            print(f"  - {i}")
        return error(f"citas ({style}) de {rel}: {len(issues)} problema(s) (ver detalle arriba)", "corrígelos con citas-rsl y vuelve a correr --cites")
    return ok(f"citas ({style}) de {rel} coherentes con {len(refs)} referencias")


def cmd_picoc(p: Paper) -> int:
    marco, f, state = picoc_versions.status(p.theme)
    print(f"marco: {marco} ({p.yml_path.name if p.yml_path.exists() else f'por defecto, sin {p.yml_path.name}'})")
    print(f"último: {p.rel(f) if f else '—'}")
    if state != "OK":
        return error(f"picoc {state}: el marco configurado es {marco} y el último es {p.rel(f) if f else 'ninguno'}", f"corre rsl-picoc (siguiente versión: {p.rel(picoc_versions.next_dir(p.theme, marco))}/)")
    return ok(f"marco {marco} al día ({p.rel(f)})")


USAGE = "uso: paper:status docs/<slug> [--init | --migrate | --new-version | --update borrador|polish | --cites [archivo] | --picoc]"


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return error(USAGE, code=2) if not argv else ok("ayuda mostrada")
    theme = Path(argv[0].rstrip("/") or "/")
    theme = theme if theme.is_absolute() else ROOT / theme
    if not theme.exists():
        raise Fail(f"no existe el tema {argv[0]}", "usa la carpeta docs/<slug> del tema")
    if not theme.is_dir():
        raise Fail(f"{argv[0]} es un archivo, no la carpeta de un tema", "usa la carpeta docs/<slug>")
    p = Paper(theme)
    flag = argv[1] if len(argv) > 1 else None
    extra = argv[2:]
    try:
        if flag is None:
            return cmd_status(p)
        if flag in ("--init", "--migrate", "--new-version", "--picoc") and extra:
            raise Fail(f"{flag} no acepta argumentos ({' '.join(extra)})", USAGE, 2)
        if flag == "--init":
            return cmd_init(p)
        if flag == "--migrate":
            return cmd_migrate(p)
        if flag == "--new-version":
            return cmd_new_version(p)
        if flag == "--update":
            if len(extra) != 1 or extra[0] not in FILES:
                raise Fail("--update necesita exactamente una etapa: borrador | polish", USAGE, 2)
            return cmd_update(p, extra[0])
        if flag == "--cites":
            if len(extra) > 1:
                raise Fail("--cites acepta un solo archivo", USAGE, 2)
            return cmd_cites(p, extra[0] if extra else None)
        if flag == "--picoc":
            return cmd_picoc(p)
    except picoc_versions.MarcoError as e:
        raise Fail(str(e), e.fix)
    raise Fail(f"opción desconocida {flag}", USAGE, 2)


if __name__ == "__main__":
    run(main)
