#!/usr/bin/env python3
"""qa:destroy — intenta romper el flujo RSL en un sandbox y reporta lo que falla.

Uso:
  pnpm -s qa:destroy                 # todos los grupos + reporte en qa/<fecha>[-n]/
  pnpm -s qa:destroy --only destruir # un grupo: positivo | orden | destruir | marco | skills
  pnpm -s qa:destroy --only D21,M16 --verbose  # casos sueltos, con todos los pasos
  pnpm -s qa:destroy --no-report     # sin escribir qa/ (depuración)
  pnpm -s qa:destroy --keep          # conserva el sandbox /tmp/rsl-qa-*

Cada paso verifica: sin traceback, última línea `OK:` o `ERROR:`, código de salida coherente
(OK -> 0, ERROR -> distinto de 0) y, si el caso lo pide, una palabra clave. Nunca toca docs/.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIX = ROOT / "qa" / "fixtures"
TODAY = dt.date.today().isoformat()
GROUPS = ("positivo", "orden", "destruir", "marco", "skills")
SCRIPT_OF = {
    "paper": "scripts/paper-manifest.py",
    "lint": "scripts/picoc-lint.py",
    "latest": "scripts/picoc-lint.py",
    "red": "scripts/redaccion-lint.py",
    "thes": "scripts/thesaurus-ieee.py",
    "src": "scripts/rsl-source.py",
    "bib": "scripts/graphify-bibliography.py",
    "crib": "scripts/cribado.py",
}


@dataclass
class Step:
    cmd: str
    expect: str
    code: int
    last: str
    problems: list[str]
    output: str


@dataclass
class Case:
    id: str
    group: str
    desc: str
    fn: object
    steps: list[Step] = field(default_factory=list)
    crash: str | None = None

    @property
    def failed(self) -> bool:
        return bool(self.crash) or any(s.problems for s in self.steps)


CASES: list[Case] = []


def case(cid: str, group: str, desc: str):
    def deco(fn):
        CASES.append(Case(cid, group, desc, fn))
        return fn
    return deco


class Sandbox:
    def __init__(self, base: Path):
        self.base = base
        self.case: Case | None = None
        self.n = 0

    # --- fixtures -------------------------------------------------------
    def theme(self, *, informe=True, paper=True, picoc: str | None = "PICOCT", borrador=False, md=True) -> Path:
        self.n += 1
        t = self.base / "docs" / f"t{self.n:03d}"
        t.mkdir(parents=True)
        if informe:
            shutil.copy(FIX / "informe.md", t / "informe.md")
        if md:
            (t / "RSL" / "MD").mkdir(parents=True)
            (t / "RSL" / "MD" / "fuente.md").write_text("# Fuente\n\nTexto.\n", encoding="utf-8")
        if paper:
            self.run(["paper", t, "--init"], "OK", quiet=True)
        if picoc:
            self.add_picoc(t, picoc)
        if borrador:
            self.run(["paper", t, "--new-version"], "OK", quiet=True)
            v = self.versions(t)[-1]
            shutil.copy(FIX / "paper-borrador.md", t / "paper" / v / "paper-borrador.md")
        return t

    def add_picoc(self, t: Path, marco: str, name: str | None = None) -> Path:
        d = t / "picoc" / (name or f"{TODAY}-{marco}")
        d.mkdir(parents=True, exist_ok=True)
        shutil.copy(FIX / f"picoc-{marco}.md", d / "picoc.md")
        (d / "picoc-debate.md").write_text("# Debate\n", encoding="utf-8")
        return d / "picoc.md"

    def versions(self, t: Path) -> list[str]:
        return sorted((p.name for p in (t / "paper").iterdir() if re.match(r"\d{4}-\d{2}-\d{2}(-\d+)?$", p.name)),
                      key=lambda v: (v[:10], int(v[11:] or 1)))

    def set_yml(self, t: Path, pattern: str, repl: str) -> None:
        f = t / "config.yml"
        txt = f.read_text(encoding="utf-8")
        new = re.sub(pattern, repl, txt, flags=re.M)
        assert new != txt, f"set_yml no cambió nada: {pattern}"
        f.write_text(new, encoding="utf-8")

    def states(self, t: Path, value: str) -> None:
        f = t / "config.yml"
        txt = re.sub(r"^(  [a-z-]+:\s+)(on|off|rewrite|frozen)\b", rf"\g<1>{value}", f.read_text(encoding="utf-8"), flags=re.M)
        f.write_text(txt, encoding="utf-8")

    # --- ejecución ------------------------------------------------------
    def run(self, argv: list, expect: str, has: str | None = None, lacks: str | None = None, code: int | None = None, quiet=False) -> Step:
        kind, *rest = argv
        if kind == "pnpm":
            cmd = ["pnpm", "-s", *map(str, rest)]
        else:
            cmd = [sys.executable, SCRIPT_OF[kind], *(["--latest"] if kind == "latest" else []), *map(str, rest)]
        cmd = [str(c).replace(str(self.base) + "/", "") if not str(c).startswith("/abs:") else str(c)[5:] for c in cmd]
        try:
            r = subprocess.run(cmd, cwd=self.base, capture_output=True, text=True, timeout=120, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
            out, rc = (r.stdout + r.stderr), r.returncode
        except subprocess.TimeoutExpired:
            out, rc = "TIMEOUT", 124
        lines = [l for l in out.strip().splitlines() if l.strip()]
        last = lines[-1] if lines else ""
        probs = []
        if "Traceback (most recent call last)" in out:
            probs.append("traceback de Python")
        if not re.match(r"^(OK|ERROR): ", last):
            probs.append("la última línea no empieza por OK: ni ERROR:")
        got = "OK" if last.startswith("OK:") else "ERROR" if last.startswith("ERROR:") else "?"
        if got != expect:
            probs.append(f"se esperaba {expect} y salió {got}")
        if got == "OK" and rc != 0 or got == "ERROR" and rc == 0:
            probs.append(f"código de salida {rc} incoherente con {got}")
        if code is not None and rc != code:
            probs.append(f"código de salida {rc}, se esperaba {code}")
        if has and has.casefold() not in out.casefold():
            probs.append(f"falta en la salida: «{has}»")
        if lacks and lacks.casefold() in out.casefold():
            probs.append(f"no debería aparecer: «{lacks}»")
        shown = " ".join(["python3" if c == sys.executable else (f"'{c}'" if " " in c else c) for c in cmd])
        st = Step(shown, expect, rc, last, probs, out[-2500:])
        if self.case is not None and not (quiet and not probs):
            self.case.steps.append(st)
        return st

    def check(self, cond: bool, what: str) -> None:
        if not cond and self.case is not None:
            self.case.steps.append(Step("(verificación)", "OK", 0, what, [what], ""))


def next_dir(out: str) -> str:
    m = re.search(r"^siguiente versión: (\S+?)/?$", out, re.M)
    return m.group(1) if m else ""


# ============================ positivo ================================

@case("P01", "positivo", "flujo completo desde cero: init, picoc, versión, borrador, polish y segunda versión")
def _(sb: Sandbox):
    t = sb.theme(paper=False, picoc=None)
    sb.run(["latest", t], "ERROR", has="FALTA")
    sb.run(["paper", t], "ERROR", has="--init")
    sb.run(["paper", t, "--init"], "OK", has="creados")
    sb.run(["paper", t, "--init"], "OK", has="ya existían")
    st = sb.run(["latest", t], "ERROR", has="siguiente versión")
    nd = next_dir(st.output)
    sb.check(nd.endswith(f"{TODAY}-PICOCT"), f"siguiente versión inesperada: {nd}")
    (sb.base / nd).mkdir(parents=True, exist_ok=True)
    shutil.copy(FIX / "picoc-PICOCT.md", sb.base / nd / "picoc.md")
    sb.run(["lint", t], "OK", has="5 bloques")
    sb.run(["latest", t], "OK")
    sb.run(["paper", t], "OK", has="rsl-make-paper")
    sb.run(["paper", t, "--new-version"], "OK", has="creada")
    v = sb.versions(t)[-1]
    shutil.copy(FIX / "paper-borrador.md", t / "paper" / v / "paper-borrador.md")
    sb.run(["paper", t, "--cites", f"paper/{v}/paper-borrador.md"], "OK")
    sb.run(["red", t / "paper" / v / "paper-borrador.md"], "OK")
    sb.run(["paper", t, "--update", "borrador"], "OK", has="rsl-polish-paper")
    shutil.copy(t / "paper" / v / "paper-borrador.md", t / "paper" / v / "paper-polish.md")
    sb.run(["paper", t, "--cites"], "OK")
    sb.run(["paper", t, "--update", "polish"], "OK", has="congela")
    sb.run(["paper", t, "--new-version"], "OK", has=f"{TODAY}-2")
    sb.run(["paper", t], "OK", has="etapas cerradas: ninguna")


@case("P02", "positivo", "cambio de marco a PIO con un picoc PIO válido")
def _(sb):
    t = sb.theme()
    sb.set_yml(t, r"^(  marco:\s*)PICOCT", r"\g<1>PIO")
    st = sb.run(["latest", t], "ERROR", has="DESFASADO")
    sb.run(["paper", t], "OK", has="rsl-picoc")
    nd = next_dir(st.output)
    sb.check(nd.endswith(f"{TODAY}-2-PIO"), f"con otra versión del mismo día la siguiente debería ser -2-PIO: {nd}")
    (sb.base / nd).mkdir(parents=True, exist_ok=True)
    shutil.copy(FIX / "picoc-PIO.md", sb.base / nd / "picoc.md")
    sb.run(["lint", t], "OK", has="3 bloques")
    sb.run(["latest", t], "OK", has="PIO")


@case("P03", "positivo", "modo ligero: la § 1.2 cambia y una versión nueva con la pregunta nueva vuelve a pasar")
def _(sb):
    t = sb.theme()
    inf = t / "informe.md"
    inf.write_text(inf.read_text(encoding="utf-8").replace("¿Cómo se ha integrado", "¿De qué manera se ha integrado"), encoding="utf-8")
    sb.run(["lint", t], "ERROR", has="PG")
    f = sb.add_picoc(t, "PICOCT", f"{TODAY}-2-PICOCT")
    f.write_text(f.read_text(encoding="utf-8").replace("¿Cómo se ha integrado", "¿De qué manera se ha integrado"), encoding="utf-8")
    sb.run(["lint", t], "OK")


@case("P04", "positivo", "thesaurus:check por pnpm (cableado de package.json)")
def _(sb):
    sb.run(["pnpm", "thesaurus:check", "Autism", "neurodiversity"], "OK", has="1 libre")
    sb.run(["pnpm", "thesaurus:lookup", "Autism"], "OK")


@case("P05", "positivo", "lints de la ficha limpia y citas APA e IEEE correctas")
def _(sb):
    t = sb.theme()
    sb.run(["red", t / "informe.md"], "OK")
    sb.run(["paper", t, "--cites", t / "informe.md"], "OK")
    sb.set_yml(t, r"^(  citas:\s*)apa7", r"\g<1>ieee")
    f = t / "ieee.md"
    f.write_text("Texto [1] y luego [2]-[3].\n\n## Referencias\n\n[1] A. B, \"X,\" 2020.\n\n[2] C. D, \"Y,\" 2021.\n\n[3] E. F, \"Z,\" 2022.\n", encoding="utf-8")
    sb.run(["paper", t, "--cites", f], "OK")


@case("P06", "positivo", "pnpm con los scripts del paquete: paper:status, picoc:latest, picoc:lint")
def _(sb):
    t = sb.theme()
    sb.run(["pnpm", "paper:status", t], "OK")
    sb.run(["pnpm", "picoc:latest", t], "OK")
    sb.run(["pnpm", "picoc:lint", t], "OK")
    sb.run(["pnpm", "redaccion:lint", t / "informe.md"], "OK")


# ============================== orden =================================

@case("M01", "orden", "--update borrador sin versiones")
def _(sb):
    t = sb.theme()
    sb.run(["paper", t, "--update", "borrador"], "ERROR", has="no hay versiones")


@case("M02", "orden", "--update polish cuando la versión no tiene paper-polish.md")
def _(sb):
    t = sb.theme(borrador=True)
    sb.run(["paper", t, "--update", "polish"], "ERROR", has="no existe")


@case("M03", "orden", "--cites sin versiones del paper")
def _(sb):
    t = sb.theme()
    sb.run(["paper", t, "--cites"], "ERROR", has="no hay archivo")


@case("M04", "orden", "picoc:lint antes de rsl-picoc")
def _(sb):
    t = sb.theme(picoc=None)
    sb.run(["lint", t], "ERROR", has="rsl-picoc")


@case("M05", "orden", "picoc:latest en un tema vacío (sin informe ni paper)")
def _(sb):
    t = sb.theme(informe=False, paper=False, picoc=None, md=False)
    sb.run(["latest", t], "ERROR", has="FALTA")


@case("M06", "orden", "paper:status sin picoc: OK con BLOCKED y próximo paso rsl-picoc")
def _(sb):
    t = sb.theme(picoc=None)
    sb.run(["paper", t], "OK", has="BLOCKED")
    sb.run(["paper", t], "OK", has="rsl-picoc")


@case("M07", "orden", "paper:status sin informe: próximo paso rsl-make-report")
def _(sb):
    t = sb.theme(informe=False)
    sb.run(["paper", t], "OK", has="rsl-make-report")


@case("M08", "orden", "dos --new-version el mismo día")
def _(sb):
    t = sb.theme()
    sb.run(["paper", t, "--new-version"], "OK")
    sb.run(["paper", t, "--new-version"], "OK", has=f"{TODAY}-2")


@case("M09", "orden", "--new-version con todo frozen/off no crea carpeta")
def _(sb):
    t = sb.theme()
    sb.states(t, "off")
    before = sb.versions(t)
    sb.run(["paper", t, "--new-version"], "ERROR", has="nada que generar")
    sb.check(sb.versions(t) == before, "se creó una versión aunque no había nada que generar")


@case("M10", "orden", "editar una sección frozen: status, --update y --new-version fallan")
def _(sb):
    t = sb.theme(borrador=True)
    sb.run(["paper", t, "--update", "borrador"], "OK", quiet=True)
    sb.set_yml(t, r"^(  encabezado:\s*)on", r"\g<1>frozen")
    v = sb.versions(t)[-1]
    f = t / "paper" / v / "paper-borrador.md"
    f.write_text(f.read_text(encoding="utf-8").replace("# Inteligencia artificial para", "# IA para"), encoding="utf-8")
    sb.run(["paper", t], "ERROR", has="frozen")
    sb.run(["paper", t, "--update", "borrador"], "ERROR", has="frozen")
    sb.run(["paper", t, "--new-version"], "ERROR", has="frozen")


@case("M11", "orden", "--migrate sobre el formato nuevo no cambia nada")
def _(sb):
    t = sb.theme()
    before = (t / "config.yml").read_text(encoding="utf-8")
    sb.run(["paper", t, "--migrate"], "OK", has="ya estaba")
    sb.check((t / "config.yml").read_text(encoding="utf-8") == before, "--migrate modificó un config.yml ya migrado")


@case("M12", "orden", "cambio de marco a mitad del flujo: secciones del marco BLOCKED")
def _(sb):
    t = sb.theme(borrador=True)
    sb.run(["paper", t, "--update", "borrador"], "OK", quiet=True)
    sb.set_yml(t, r"^(  marco:\s*)PICOCT", r"\g<1>PIO")
    sb.run(["paper", t], "OK", has="falta picoc")


@case("M13", "orden", "--update borrador cuando solo existe paper-polish.md")
def _(sb):
    t = sb.theme(borrador=True)
    v = sb.versions(t)[-1]
    (t / "paper" / v / "paper-borrador.md").rename(t / "paper" / v / "paper-polish.md")
    sb.run(["paper", t, "--update", "borrador"], "ERROR", has="no existe")
    sb.run(["paper", t, "--update", "polish"], "OK")


@case("M14", "orden", "un picoc nuevo el mismo día con otro marco pasa a ser el último")
def _(sb):
    t = sb.theme()
    sb.set_yml(t, r"^(  marco:\s*)PICOCT", r"\g<1>PIO")
    sb.add_picoc(t, "PIO", f"{TODAY}-2-PIO")
    sb.run(["latest", t], "OK", has=f"{TODAY}-2-PIO")


@case("M15", "orden", "--init con un config.yml existente no lo pisa")
def _(sb):
    t = sb.theme()
    sb.set_yml(t, r"^(  citas:\s*)apa7", r"\g<1>ieee")
    sb.run(["paper", t, "--init"], "OK", has="ya existían")
    sb.check("citas: ieee" in (t / "config.yml").read_text(encoding="utf-8"), "--init sobrescribió config.yml")


@case("M17", "orden", "tema viejo con paper/paper.yml: ERROR hasta correr --migrate, que lo mueve a config.yml")
def _(sb):
    t = sb.theme(borrador=True)
    sb.run(["paper", t, "--update", "borrador"], "OK", quiet=True)
    (t / "config.yml").rename(t / "paper" / "paper.yml")
    sb.run(["paper", t], "ERROR", has="--migrate")
    sb.run(["latest", t], "ERROR", has="--migrate")
    sb.run(["lint", t], "ERROR", has="--migrate")
    sb.run(["paper", t, "--init"], "ERROR", has="--migrate")
    sb.check(not (t / "config.yml").exists(), "--init creó config.yml encima de la configuración vieja")
    sb.run(["paper", t, "--migrate"], "OK", has="movido a config.yml")
    sb.check((t / "config.yml").exists() and not (t / "paper" / "paper.yml").exists(), "--migrate no movió paper/paper.yml")
    sb.run(["paper", t], "OK", has="mejorar")
    shutil.copy(t / "config.yml", t / "paper" / "paper.yml")
    sb.run(["paper", t, "--migrate"], "ERROR", has="dos configuraciones")


@case("M18", "orden", "--migrate de paper/paper.yml con el formato antiguo (enabled/frozen): lo mueve y lo convierte")
def _(sb):
    t = sb.theme()
    (t / "config.yml").unlink()
    (t / "paper" / "paper.yml").write_text(
        "format: {}\nsections:\n  - {id: contexto, enabled: true}\n  - {id: problema, frozen: true}\n  - {id: abstract, enabled: false}\n",
        encoding="utf-8")
    sb.run(["paper", t, "--migrate"], "OK", has="convertido")
    txt = (t / "config.yml").read_text(encoding="utf-8") if (t / "config.yml").exists() else ""
    sb.check(re.search(r"^  contexto:\s+on", txt, re.M) and re.search(r"^  problema:\s+frozen", txt, re.M), "el formato antiguo no se convirtió bien")
    sb.run(["paper", t], "OK")


# ============================= destruir ===============================

def yml(sb, t, text):
    (t / "config.yml").write_text(text, encoding="utf-8")


@case("D01", "destruir", "config.yml con YAML roto")
def _(sb):
    t = sb.theme()
    yml(sb, t, "formato:\n  idioma: es\n   citas: [apa7\n")
    sb.run(["paper", t], "ERROR", has="YAML")
    sb.run(["latest", t], "ERROR", has="YAML")
    sb.run(["lint", t], "ERROR", has="YAML")


@case("D02", "destruir", "config.yml vacío: todo off, sin romperse")
def _(sb):
    t = sb.theme()
    yml(sb, t, "")
    sb.run(["paper", t], "OK", has="on o rewrite")


@case("D03", "destruir", "config.yml que es una lista")
def _(sb):
    t = sb.theme()
    yml(sb, t, "- a\n- b\n")
    sb.run(["paper", t], "ERROR", has="mapa")
    sb.run(["latest", t], "ERROR")


@case("D04", "destruir", "estado de sección desconocido (maybe)")
def _(sb):
    t = sb.theme()
    sb.set_yml(t, r"^(  contexto:\s*)on", r"\g<1>maybe")
    sb.run(["paper", t], "ERROR", has="maybe")


@case("D05", "destruir", "estado de sección como lista [on]")
def _(sb):
    t = sb.theme()
    sb.set_yml(t, r"^(  contexto:\s*)on", r"\g<1>[on]")
    sb.run(["paper", t], "ERROR", has="contexto")


@case("D06", "destruir", "sección inexistente en config.yml")
def _(sb):
    t = sb.theme()
    p = t / "config.yml"
    p.write_text(p.read_text(encoding="utf-8").replace("  contexto:", "  inventada: on\n  contexto:"), encoding="utf-8")
    sb.run(["paper", t], "ERROR", has="inventada")


@case("D07", "destruir", "formato inválido: idioma, citas, numeracion, resumen, clave desconocida")
def _(sb):
    for pat, rep, key in ((r"^(  idioma:\s*)es", r"\g<1>español", "idioma"),
                          (r"^(  citas:\s*)apa7", r"\g<1>vancouver", "citas"),
                          (r"^(  numeracion:\s*)romana", r"\g<1>3", "numeracion"),
                          (r"^(  resumen:\s*).*$", r"\g<1>english", "resumen"),
                          (r"^(formato:)$", r"\g<1>\n  color: azul", "color")):
        t = sb.theme()
        sb.set_yml(t, pat, rep)
        sb.run(["paper", t], "ERROR", has=key)


@case("D08", "destruir", "formato como texto en vez de bloque")
def _(sb):
    t = sb.theme()
    yml(sb, t, "formato: hola\nIntroducción:\n  contexto: on\n")
    sb.run(["paper", t], "ERROR", has="formato")


@case("D09", "destruir", "paper.state.jsonc corrupto, vacío y con tipos erróneos")
def _(sb):
    t = sb.theme(borrador=True)
    s = t / "paper" / "paper.state.jsonc"
    s.write_text("{ esto no es json", encoding="utf-8")
    sb.run(["paper", t], "ERROR", has="corrupto")
    s.write_text('{"sections": [], "versions": {}}', encoding="utf-8")
    sb.run(["paper", t], "ERROR", has="corrupto")
    s.write_text("", encoding="utf-8")
    sb.run(["paper", t], "OK")


@case("D10", "destruir", "paper.shadow.yml ausente, roto y con ids repetidos")
def _(sb):
    t = sb.theme()
    sh = t / "paper" / "paper.shadow.yml"
    good = sh.read_text(encoding="utf-8")
    sh.unlink()
    sb.run(["paper", t], "ERROR", has="--init")
    sh.write_text("sections: hola\n", encoding="utf-8")
    sb.run(["paper", t], "ERROR", has="sections")
    sh.write_text(good.replace("  - { id: resumen,", "  - { id: contexto,"), encoding="utf-8")
    sb.run(["paper", t], "ERROR", has="repite")


def borrador_with(sb, t, fn):
    v = sb.versions(t)[-1]
    f = t / "paper" / v / "paper-borrador.md"
    f.write_text(fn(f.read_text(encoding="utf-8")), encoding="utf-8")
    return f


@case("D11", "destruir", "marcadores rotos: sin cerrar, repetidos, anidados, cierre huérfano")
def _(sb):
    muts = {
        "no se cierra": lambda s: s.rstrip("\n").removesuffix("<!-- /paper:section -->") + "\n",
        "repetida": lambda s: s + "\n<!-- paper:section id=contexto -->\nOtra vez.\n<!-- /paper:section -->\n",
        "se abre antes": lambda s: s.replace("### Justificación\n", "### Justificación\n<!-- paper:section id=calidad -->\n", 1),
        "sin apertura": lambda s: s + "\n<!-- /paper:section -->\n",
    }
    for key, fn in muts.items():
        t = sb.theme(borrador=True)
        borrador_with(sb, t, fn)
        sb.run(["paper", t], "ERROR", has=key)
        sb.run(["paper", t, "--update", "borrador"], "ERROR", has="marcadores")


@case("D12", "destruir", "borrador sin marcadores, vacío, no UTF-8 y con id desconocido")
def _(sb):
    t = sb.theme(borrador=True)
    borrador_with(sb, t, lambda s: "Texto sin marcadores.\n")
    sb.run(["paper", t, "--update", "borrador"], "ERROR", has="no tiene marcadores")
    borrador_with(sb, t, lambda s: "")
    sb.run(["paper", t, "--update", "borrador"], "ERROR", has="no tiene marcadores")
    borrador_with(sb, t, lambda s: "<!-- paper:section id=fantasma -->\nx\n<!-- /paper:section -->\n")
    sb.run(["paper", t, "--update", "borrador"], "ERROR", has="fantasma")
    v = sb.versions(t)[-1]
    (t / "paper" / v / "paper-borrador.md").write_bytes("<!-- paper:section id=contexto -->\ncaf\xe9\n<!-- /paper:section -->\n".encode("latin-1"))
    sb.run(["paper", t], "ERROR", has="UTF-8")


@case("D13", "destruir", "ficha sin pregunta en la § 1.2 y con dos preguntas")
def _(sb):
    t = sb.theme()
    inf = t / "informe.md"
    txt = inf.read_text(encoding="utf-8")
    q = re.search(r"### 1\.2 Problemática\n(.*?)\n", txt).group(1)
    inf.write_text(txt.replace(q, "Hay un problema sin pregunta."), encoding="utf-8")
    sb.run(["lint", t], "ERROR", has="1.2")
    inf.write_text(txt.replace(q, q + " ¿Y otra pregunta más?"), encoding="utf-8")
    sb.run(["lint", t], "ERROR", has="1.2")


@case("D14", "destruir", "picoc vacío, sin **Marco:**, sin queries, con tipo de documento distinto de CR y con T invertido")
def _(sb):
    def mut(fn, has):
        t = sb.theme()
        f = next((t / "picoc").glob("*/picoc.md"))
        f.write_text(fn(f.read_text(encoding="utf-8")), encoding="utf-8")
        sb.run(["lint", t], "ERROR", has=has)
    mut(lambda s: "", "vacío")
    mut(lambda s: s.replace("**Marco:** PICOCT", "Marco PICOCT"), "Marco")
    mut(lambda s: re.sub(r"## Query Web of Science.*?(?=## Query IEEE)", "", s, flags=re.S), "Web of Science")
    mut(lambda s: s.replace(' OR LIMIT-TO ( DOCTYPE , "cp" )', "", 1), "tipo de documento")
    mut(lambda s: s.replace("`2020–2026`", "`2026–2020`"), "años")


@case("D15", "destruir", "carpetas basura en picoc/ y paper/ se ignoran")
def _(sb):
    t = sb.theme(borrador=True)
    for n in ("notas", "2026-13-45-PICOCT", "2099-01-01-PICOCT-viejo", "PICOCT"):
        (t / "picoc" / n).mkdir()
        (t / "picoc" / n / "picoc.md").write_text("basura", encoding="utf-8")
    for n in ("borrador-viejo", "2026-99-99", "copia"):
        (t / "paper" / n).mkdir()
    sb.run(["latest", t], "OK", has=f"{TODAY}-PICOCT")
    sb.run(["lint", t], "OK")
    sb.run(["paper", t], "OK", lacks="2026-99-99")


@case("D16", "destruir", "rutas: / final, absoluta, archivo en vez de tema, tema inexistente")
def _(sb):
    t = sb.theme()
    rel = str(t.relative_to(sb.base))
    sb.run(["paper", rel + "/"], "OK")
    sb.run(["latest", rel + "/"], "OK")
    sb.run(["paper", f"/abs:{t}"], "OK")
    sb.run(["lint", f"/abs:{t}"], "OK")
    sb.run(["paper", t / "informe.md"], "ERROR", has="archivo")
    sb.run(["latest", t / "informe.md"], "ERROR")
    sb.run(["paper", "docs/no-existe"], "ERROR", has="no existe")
    sb.run(["lint", "docs/no-existe"], "ERROR", has="no existe")


@case("D17", "destruir", "argumentos inválidos en todos los scripts")
def _(sb):
    t = sb.theme(borrador=True)
    sb.run(["paper", t, "--update"], "ERROR", code=2)
    sb.run(["paper", t, "--update", "final"], "ERROR", code=2)
    sb.run(["paper", t, "--init", "extra"], "ERROR", code=2)
    sb.run(["paper", t, "--volar"], "ERROR", has="desconocida")
    sb.run(["paper", t, "--cites", t / "paper"], "ERROR", has="carpeta")
    sb.run(["paper", t, "--cites", "no-existe.md"], "ERROR")
    sb.run(["paper"], "ERROR", code=2)
    sb.run(["lint"], "ERROR", code=2)
    sb.run(["lint", t, t], "ERROR", code=2)
    sb.run(["red"], "ERROR", code=2)
    sb.run(["red", t], "ERROR", has="carpeta")
    sb.run(["red", "no-existe.md"], "ERROR", has="no existe")
    sb.run(["red", t / "informe.md", "--max-palabras", "x"], "ERROR", code=2)
    sb.run(["pnpm", "thesaurus:check", ""], "ERROR")
    sb.run(["pnpm", "thesaurus:check"], "ERROR")


@case("D18", "destruir", "citas rotas: APA huérfana, IEEE fuera de orden y sin referencia; APA con página sí cuenta como citada")
def _(sb):
    t = sb.theme()
    f = t / "apa.md"
    f.write_text("Texto (Gómez, 2023) y (Pérez, 2024).\n\n## Referencias\n\nPérez, J. (2024). *A*.\n\nRuiz, A. (2020). *B*.\n", encoding="utf-8")
    sb.run(["paper", t, "--cites", f], "ERROR", has="Gómez")
    f.write_text("Según Ruiz y Soto (2020, p. 4), algo (Pérez et al., 2024, pp. 10–11).\n\n## Referencias\n\nPérez, J. (2024). *A*.\n\nRuiz, A., & Soto, B. (2020). *B*.\n", encoding="utf-8")
    sb.run(["paper", t, "--cites", f], "OK")
    sb.set_yml(t, r"^(  citas:\s*)apa7", r"\g<1>ieee")
    f.write_text("Texto [2] y [1], luego [3]-[4].\n\n## Referencias\n\n[1] A.\n\n[2] B.\n\n[3] C.\n", encoding="utf-8")
    sb.run(["paper", t, "--cites", f], "ERROR", has="[4]")


@case("D19", "destruir", "finales de línea CRLF y BOM UTF-8")
def _(sb):
    t = sb.theme(borrador=True)
    for f in (t / "informe.md", t / "config.yml", next((t / "picoc").glob("*/picoc.md"))):
        f.write_bytes(f.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
    y = t / "config.yml"
    y.write_bytes(b"\xef\xbb\xbf" + y.read_bytes())
    sb.run(["paper", t], "OK")
    sb.run(["lint", t], "OK")
    sb.run(["latest", t], "OK")


@case("D20", "destruir", "no se pierde nada si una versión del paper desaparece")
def _(sb):
    t = sb.theme(borrador=True)
    sb.run(["paper", t, "--update", "borrador"], "OK", quiet=True)
    shutil.rmtree(t / "paper" / sb.versions(t)[-1])
    sb.run(["paper", t], "OK")
    sb.run(["paper", t, "--new-version"], "OK")


@case("D21", "destruir", "sin permisos de escritura: paper.state.jsonc de solo lectura y paper/ sin escritura (ataques A3, A9)")
def _(sb):
    if os.geteuid() == 0:
        return
    t = sb.theme(borrador=True)
    s = t / "paper" / "paper.state.jsonc"
    s.chmod(0o444)
    try:
        sb.run(["paper", t, "--update", "borrador"], "ERROR", has="permiso", lacks="fallo interno")
    finally:
        s.chmod(0o644)
    (t / "paper").chmod(0o555)
    try:
        sb.run(["paper", t, "--new-version"], "ERROR", has="permiso", lacks="fallo interno")
    finally:
        (t / "paper").chmod(0o755)


@case("D22", "destruir", "versiones con fecha futura en picoc/ y paper/ (ataque A4)")
def _(sb):
    t = sb.theme(borrador=True)
    sb.add_picoc(t, "PICOCT", "2099-01-01-PICOCT")
    sb.run(["latest", t], "ERROR", has="fecha futura")
    sb.run(["lint", t], "ERROR", has="fecha futura")
    shutil.rmtree(t / "picoc" / "2099-01-01-PICOCT")
    (t / "paper" / "2099-01-01").mkdir()
    sb.run(["paper", t], "ERROR", has="fecha futura")


@case("D23", "destruir", "estados con mayúsculas o espacios se aceptan (ataque A5)")
def _(sb):
    t = sb.theme()
    sb.set_yml(t, r"^(  contexto:\s*)on", r"\g<1>Frozen")
    sb.set_yml(t, r"^(  problema:\s*)on", r"\g<1>'  REWRITE '")
    sb.run(["paper", t], "OK", has="| contexto | frozen")


@case("D24", "destruir", "carpetas de versión -0, -1 y -01 se ignoran y la versión nueva es la última (ataque A8)")
def _(sb):
    t = sb.theme()
    for n in (f"{TODAY}-0", f"{TODAY}-1", f"{TODAY}-01"):
        (t / "paper" / n).mkdir()
    sb.add_picoc(t, "PICOCT", f"{TODAY}-01-PICOCT")
    sb.run(["paper", t, "--new-version"], "OK", has=f"paper/{TODAY}/")
    sb.run(["paper", t], "OK", has=f"última versión: {TODAY} ")
    sb.run(["latest", t], "OK", has=f"{TODAY}-PICOCT")


@case("D25", "destruir", "dos picoc con la misma fecha y número (ataque A11)")
def _(sb):
    t = sb.theme()
    sb.add_picoc(t, "PIO", f"{TODAY}-PIO")
    sb.run(["latest", t], "ERROR", has="misma fecha")
    sb.run(["paper", t], "ERROR", has="misma fecha")


@case("D26", "destruir", "rutas con espacios y acentos, y tema enlazado con symlink (ataques A1, A6)")
def _(sb):
    t = sb.theme(borrador=True)
    raro = sb.base / "docs" / "tema con ñ y espacios"
    shutil.copytree(t, raro)
    sb.run(["paper", raro], "OK")
    sb.run(["lint", raro], "OK")
    sb.run(["red", raro / "informe.md"], "OK")
    link = sb.base / "docs" / "enlace"
    link.symlink_to(t)
    sb.run(["paper", link], "OK")
    sb.run(["latest", link], "OK")


@case("D27", "destruir", "celda con \\| escapado y ? interna en una RQ (ataque A10)")
def _(sb):
    t = sb.theme()
    f = next((t / "picoc").glob("*/picoc.md"))
    f.write_text(f.read_text(encoding="utf-8").replace("| RQ1 | P | ¿Qué perfiles", "| RQ1 | P | ¿Qué perfiles (versión 2.0 \\| beta?) y", 1), encoding="utf-8")
    sb.run(["lint", t], "OK")


@case("D28", "destruir", "picoc.md convertido en carpeta (ataque A2)")
def _(sb):
    t = sb.theme()
    f = next((t / "picoc").glob("*/picoc.md"))
    f.unlink()
    f.mkdir()
    sb.run(["latest", t], "ERROR", has="FALTA")
    sb.run(["lint", t], "ERROR", has="rsl-picoc")


@case("M16", "orden", "borrar picoc/ con el paper ya generado: BLOCKED y próximo paso rsl-picoc (ataque A7)")
def _(sb):
    t = sb.theme(borrador=True)
    sb.run(["paper", t, "--update", "borrador"], "OK", quiet=True)
    shutil.rmtree(t / "picoc")
    sb.run(["paper", t], "OK", has="rsl-picoc")
    sb.run(["paper", t, "--update", "borrador"], "OK")


# =============================== marco ================================

@case("K01", "marco", "variantes válidas del marco: pio, ' PICOCT ', [p, i, o], PICOCTS, PICOS")
def _(sb):
    for raw, label in (("pio", "PIO"), ("' PICOCT '", "PICOCT"), ("[p, i, o]", "PIO"), ("PICOCTS", "PICOCTS"), ("PICOS", "PICOS")):
        t = sb.theme()
        sb.set_yml(t, r"^(  marco:\s*)PICOCT", rf"\g<1>{raw}")
        sb.run(["paper", t], "OK", has=f"marco: {label}")


@case("K02", "marco", "variantes inválidas: PIX, PICCC, 123, vacío, P-I-O, PICoO, solo T")
def _(sb):
    for raw, has in (("PIX", "X"), ("PICCC", "repetido"), ("'123'", "123"), ("''", "vacío"), ("P-I-O", "P-I-O"), ("PICoO", "repetido"), ("T", "T")):
        t = sb.theme()
        sb.set_yml(t, r"^(  marco:\s*)PICOCT", rf"\g<1>{raw}")
        sb.run(["paper", t], "ERROR", has=has)
        sb.run(["latest", t], "ERROR", has=has)


@case("K03", "marco", "picoc con **Marco:** inválido o distinto de su carpeta")
def _(sb):
    t = sb.theme()
    f = next((t / "picoc").glob("*/picoc.md"))
    f.write_text(f.read_text(encoding="utf-8").replace("**Marco:** PICOCT", "**Marco:** PIX", 1), encoding="utf-8")
    sb.run(["lint", t], "ERROR", has="X")
    f.write_text(f.read_text(encoding="utf-8").replace("**Marco:** PIX", "**Marco:** PICO", 1), encoding="utf-8")
    sb.run(["lint", t], "ERROR", has="carpeta")


@case("K04", "marco", "picoc PIO con filtro de año distinto del periodo de CR o con una fila de más")
def _(sb):
    t = sb.theme()
    sb.set_yml(t, r"^(  marco:\s*)PICOCT", r"\g<1>PIO")
    f = sb.add_picoc(t, "PIO", f"{TODAY}-2-PIO")
    good = f.read_text(encoding="utf-8")
    f.write_text(good.replace("AND PUBYEAR > 2020 AND PUBYEAR < 2027", "AND PUBYEAR > 2018 AND PUBYEAR < 2027", 1), encoding="utf-8")
    sb.run(["lint", t], "ERROR", has="2021–2026 de los criterios de inclusión")
    f.write_text(good.replace("| O | Métricas", "| C | Comparación | RQ3 | `x` | — | Procede de “sesgo” |\n| O | Métricas", 1), encoding="utf-8")
    sb.run(["lint", t], "ERROR", has="exactamente las filas")


@case("K05", "marco", "criterios de inclusión y exclusión: ausentes, fuera de lugar, largos, incompletos o con otros años que T")
def _(sb):
    t = sb.theme()
    f = next((t / "picoc").glob("*/picoc.md"))
    good = f.read_text(encoding="utf-8")
    head, crit = good.split("\n## Criterios de inclusión y exclusión", 1)
    crit = "\n## Criterios de inclusión y exclusión" + crit

    def lint(text, has):
        f.write_text(text, encoding="utf-8")
        sb.run(["lint", t], "ERROR", has=has)

    lint(head, "falta la sección final")
    lint(head.replace("\n## Descriptores revisados", crit + "\n\n## Descriptores revisados"), "debe ser la última sección")
    lint(good.replace("### Exclusión", "### Descarte"), "falta '### Exclusión'")
    lint(good.replace("- Revisiones sistemáticas y otros estudios secundarios.\n", ""), "al menos 2 criterios")
    lint(good.replace("- Revisiones sistemáticas y otros estudios secundarios.", "- " + " ".join(["palabra"] * 30) + "."), "demasiado largo")
    lint(good.replace(", en inglés o español", ""), "fijar el idioma")
    lint(good.replace("Artículos de revista o de congreso revisados por pares", "Trabajos"), "tipo de documento")
    lint(good.replace("entre 2020 y 2026", "entre 2018 y 2026"), "mismo periodo que T")
    f.write_text(good, encoding="utf-8")
    sb.run(["lint", t], "OK", has="3 criterios de inclusión y 2 de exclusión")
    sb.set_yml(t, r"^(  marco:\s*)PICOCT", r"\g<1>PIO")
    sb.add_picoc(t, "PIO", f"{TODAY}-2-PIO")
    sb.run(["lint", t], "OK", has="2 criterios de inclusión")


@case("K08", "marco", "filtros de inclusión en las queries: sin acceso abierto en CR o en Scopus, WoS sin tipo, idioma o nota de acceso abierto")
def _(sb):
    t = sb.theme()
    f = next((t / "picoc").glob("*/picoc.md"))
    good = f.read_text(encoding="utf-8")

    def lint(text, has):
        f.write_text(text, encoding="utf-8")
        sb.run(["lint", t], "ERROR", has=has)

    lint(good.replace(", de acceso abierto,", ","), "fijar el acceso abierto")
    lint(good.replace('\nAND ( LIMIT-TO ( OA , "all" ) )', "", 1), "[Scopus]: falta el filtro de acceso abierto")
    lint(good.replace(' AND DT=(Article OR "Proceedings Paper")', ""), "[Web of Science]: falta el filtro de tipo de documento")
    lint(good.replace("LA=(English OR Spanish)", "LA=(English)"), "idiomas de la query")
    lint(good.replace("Filtro de la interfaz: Open Access.", ""), "anotado bajo la query")
    f.write_text(good, encoding="utf-8")
    sb.run(["lint", t], "OK")


@case("K06", "marco", "keywords del paper: ausentes, fuera de lugar, más de 6, menos de 5, inventadas, de otro componente o sin cubrir un componente")
def _(sb):
    t = sb.theme()
    f = next((t / "picoc").glob("*/picoc.md"))
    good = f.read_text(encoding="utf-8")
    start = good.index("\n## Keywords")
    end = good.index("\n## Query Scopus")
    ky, rest = good[start:end], good[:start] + good[end:]

    def lint(text, has):
        f.write_text(text, encoding="utf-8")
        sb.run(["lint", t], "ERROR", has=has)

    lint(rest, "falta '## Keywords'")
    lint(rest.replace("\n## Criterios de inclusión", ky + "\n\n## Criterios de inclusión"), "justo después de '## Palabras clave'")
    lint(good.replace("| accessibility evaluation | evaluación de accesibilidad | Co |", "| accessibility evaluation | evaluación de accesibilidad | Co |\n| Usability | usabilidad | O |"), "deben ser 5 o 6")
    lint(good.replace("| neurodiversity | neurodiversidad | P |\n", "").replace("| WCAG | pautas WCAG | C |\n", ""), "deben ser 5 o 6")
    lint(good.replace("| WCAG | pautas WCAG | C |", "| digital inclusion | inclusión digital | C |"), "no está en la tabla 'Palabras clave'")
    lint(good.replace("| WCAG | pautas WCAG | C |", "| WCAG | pautas WCAG | O |"), "es del componente C")
    lint(good.replace("| WCAG | pautas WCAG | C |", "| Usability | usabilidad | O |"), "falta al menos una keyword de C")
    lint(good.replace("| WCAG | pautas WCAG | C |", "| neurodiversity | neurodiversidad | P |"), "repetida")
    f.write_text(good, encoding="utf-8")
    sb.run(["lint", t], "OK", has="6 keywords")


# ============================== skills ================================

SKILLS = ROOT / ".cursor" / "skills"
AGENTS = ROOT / ".cursor" / "agents"


def rsl_skills() -> list[Path]:
    return sorted(SKILLS.glob("rsl-*/SKILL.md"))


def static(sb: Sandbox, ok_: bool, what: str) -> None:
    sb.check(ok_, what)


@case("S01", "skills", "cada `pnpm -s X` citado en skills, agentes, playbooks y README existe en package.json")
def _(sb):
    scripts = set(json.loads((ROOT / "package.json").read_text(encoding="utf-8"))["scripts"])
    files = rsl_skills() + sorted(AGENTS.glob("*.md")) + sorted((ROOT / "playbooks").glob("*.md")) + [ROOT / "README.md"]
    for f in files:
        for m in re.finditer(r"pnpm (?:-s )?(?:run )?([a-z][\w:-]*)", f.read_text(encoding="utf-8")):
            name = m.group(1)
            if name in ("install", "add", "exec", "dlx") or name.endswith(":"):
                continue
            static(sb, name in scripts, f"{f.relative_to(ROOT)}: `pnpm {name}` no existe en package.json")


@case("S02", "skills", "rutas global/, playbooks/ y scripts/ citadas existen")
def _(sb):
    for f in rsl_skills() + sorted(AGENTS.glob("*-rsl.md")) + sorted((ROOT / "playbooks").glob("*.md")):
        for m in re.finditer(r"(?<![\w/.<])((?:global|playbooks|scripts)/[\w./-]+\.(?:md|py|json|ya?ml))", f.read_text(encoding="utf-8")):
            p = m.group(1)
            if "<" in p or "*" in p:
                continue
            static(sb, (ROOT / p).exists(), f"{f.relative_to(ROOT)}: la ruta {p} no existe")


@case("S03", "skills", "agentes *-rsl y skills rsl-* citados existen; nombre del frontmatter = carpeta")
def _(sb):
    agents = {p.stem for p in AGENTS.glob("*.md")}
    section_ids = set(re.findall(r"id: ([\w-]+)", (ROOT / "scripts" / "paper-manifest.py").read_text(encoding="utf-8")))
    skills = {p.parent.name for p in SKILLS.glob("*/SKILL.md")}
    for f in rsl_skills() + sorted(AGENTS.glob("*-rsl.md")) + [ROOT / "README.md"]:
        txt = f.read_text(encoding="utf-8")
        for a in sorted(set(re.findall(r"`([a-z]+(?:-[a-z]+)*-rsl)`", txt)) - section_ids):
            static(sb, a in agents, f"{f.relative_to(ROOT)}: el agente {a} no existe en .cursor/agents/")
        for s in sorted(set(re.findall(r"\b(rsl-[a-z]+(?:-[a-z0-9]+)*)\b(?!-?\*)", txt)) - {"rsl-skills"}):
            static(sb, s in skills, f"{f.relative_to(ROOT)}: la skill {s} no existe en .cursor/skills/")
    for f in rsl_skills():
        m = re.search(r"^name:\s*(\S+)", f.read_text(encoding="utf-8"), re.M)
        static(sb, bool(m) and m.group(1) == f.parent.name, f"{f.relative_to(ROOT)}: name del frontmatter distinto de la carpeta")
        static(sb, "description:" in f.read_text(encoding="utf-8"), f"{f.relative_to(ROOT)}: falta description")


@case("S04", "skills", "cada skill rsl-* tiene la sección Cierre con el contrato OK/ERROR")
def _(sb):
    for f in rsl_skills():
        txt = f.read_text(encoding="utf-8")
        m = re.search(r"^## Cierre\n(.*?)(?=^## |\Z)", txt, re.M | re.S)
        static(sb, bool(m), f"{f.relative_to(ROOT)}: falta '## Cierre'")
        if m:
            static(sb, "`OK:" in m.group(1) and "`ERROR:" in m.group(1) and "Próximo paso" in m.group(1),
                   f"{f.relative_to(ROOT)}: el Cierre no define `OK: … Próximo paso: …` y `ERROR: …`")


@case("S05", "skills", "sin restos de reglas viejas (PICO | PICOC | PICOCT, picoc-polish, mínimos en agentes)")
def _(sb):
    files = rsl_skills() + sorted(AGENTS.glob("*-rsl.md")) + sorted((ROOT / "playbooks").glob("*.md")) + [ROOT / "README.md", ROOT / ".cursor" / "rules" / "graphify.mdc"]
    for f in files:
        txt = f.read_text(encoding="utf-8")
        for bad in ("PICO | PICOC | PICOCT", "PICO / PICOC / PICOCT", "picoc-polish"):
            static(sb, bad not in txt, f"{f.relative_to(ROOT)}: resto «{bad}»")
    for f in AGENTS.glob("*-rsl.md"):
        static(sb, not re.search(r"[Mm]ínimo \d", f.read_text(encoding="utf-8")), f"{f.relative_to(ROOT)}: mínimo obligatorio de hallazgos")


@case("S06", "skills", "README lista todas las skills rsl-*")
def _(sb):
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for f in rsl_skills():
        static(sb, f"`{f.parent.name}`" in readme, f"README.md no menciona `{f.parent.name}`")


# ============================== motor =================================

def build_sandbox() -> Path:
    base = Path(tempfile.mkdtemp(prefix="rsl-qa-"))
    shutil.copytree(ROOT / "scripts", base / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(ROOT / "playbooks", base / "playbooks")
    shutil.copy(ROOT / "package.json", base / "package.json")
    (base / "global" / "thesaurus").mkdir(parents=True)
    shutil.copytree(ROOT / "global" / "citation-style", base / "global" / "citation-style")
    thes = ROOT / "global" / "thesaurus" / "ieee-thesaurus.json"
    if thes.exists():
        shutil.copy(thes, base / "global" / "thesaurus" / thes.name)
    (base / "docs").mkdir()
    return base


@case("S07", "skills", "rsl-picoc solo escribe picoc/: no edita informe, paper ni config.yml")
def _(sb):
    txt = (SKILLS / "rsl-picoc" / "SKILL.md").read_text(encoding="utf-8")
    body = txt.split("## Forbidden")[0]
    for bad in ("--init", "--new-version", "--update", "Section 2 of"):
        sb.check(bad not in body, f"rsl-picoc/SKILL.md pide '{bad}' fuera de Forbidden (la skill no puede escribir el informe ni el paper)")
    sb.check("Read-only outside `picoc/`" in txt, "rsl-picoc/SKILL.md no declara que solo lee fuera de picoc/")
    for other in ("rsl-make-report", "rsl-polish-report"):
        sb.check("rsl-picoc` never edits the informe" in (SKILLS / other / "SKILL.md").read_text(encoding="utf-8"),
                 f"{other}/SKILL.md no asume el enlace de la sección 2 del informe")


# ======================= bibliografía y Metodología =======================

@case("P07", "positivo", "rsl:source convierte un PDF real en MD junto al PDF y no lo rehace si está al día")
def _(sb):
    src = ROOT / "global" / "bibliography" / "prisma" / "page-2021-prisma-2020.pdf"
    if not src.exists():
        sb.check(False, f"falta {src.relative_to(ROOT)} (PDF CC BY de la bibliografía compartida)")
        return
    d = sb.base / "global" / "bibliography" / "prisma"
    d.mkdir(parents=True, exist_ok=True)
    shutil.copy(src, d / src.name)
    rel = f"global/bibliography/prisma/{src.name}"
    sb.run(["src", rel], "OK", has="generado")
    md = d / f"{src.stem}.md"
    sb.check(md.exists(), "rsl:source no escribió el MD junto al PDF")
    sb.check(md.exists() and "Theme relevance" not in md.read_text(encoding="utf-8"), "el MD global arrastra los ganchos de relevancia de un tema")
    sb.check((d / "_raw" / f"{src.stem}.txt").exists(), "rsl:source no dejó el texto por página en _raw/")
    sb.run(["src", rel], "OK", has="ya estaba al día")
    sb.run(["pnpm", "rsl:source", rel, "--force"], "OK", has="generado")


@case("D29", "destruir", "rsl:source sin PDF, con ruta inexistente, con un .md o con un HTML disfrazado de .pdf")
def _(sb):
    sb.run(["src"], "ERROR", has="falta el PDF", code=2)
    sb.run(["src", "global/bibliography/nada.pdf"], "ERROR", has="no existe")
    f = sb.base / "global" / "bibliography" / "x"
    f.mkdir(parents=True, exist_ok=True)
    (f / "nota.md").write_text("# Nota\n", encoding="utf-8")
    sb.run(["src", "global/bibliography/x/nota.md"], "ERROR", has="no es un archivo .pdf")
    (f / "falso.pdf").write_text("<!DOCTYPE html><html>Just a moment...</html>", encoding="utf-8")
    sb.run(["src", "global/bibliography/x/falso.pdf"], "ERROR", has="no es un PDF real")
    sb.check(not (f / "falso.md").exists(), "rsl:source escribió un MD a partir de un PDF falso")


@case("M19", "orden", "graphify:bibliography:status sin grafo: ERROR con el refresh como arreglo")
def _(sb):
    (sb.base / "global" / "bibliography").mkdir(parents=True, exist_ok=True)
    sb.run(["bib", "--status"], "ERROR", has="graphify:bibliography:refresh")
    sb.run(["bib", "--estado"], "ERROR", has="no reconocido", code=2)


@case("M20", "orden", "seleccion-prisma sin RSL/seleccion no queda BLOCKED (los conteos van como X)")
def _(sb):
    t = sb.theme()
    sb.run(["paper", t], "OK", lacks="seleccion-prisma (falta")


IEEE_NOTE = "_Nota._ En cursiva, descriptores del IEEE Thesaurus (IEEE, 2019); el resto son términos libres."


def metodologia(picoc: Path, extra_term: str | None = None, note: str = IEEE_NOTE) -> str:
    """palabras-clave + ecuacion-busqueda copiadas del picoc (espejo), con prosa fija."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import paper_picoc_sync as s
    m = s.mirror(picoc)
    rows = []
    for c, ts in m["keywords"].items():
        en = ts + ([extra_term] if extra_term and c == "P" else [])
        rows.append(f"| {c} | {', '.join(f'término {i + 1}' for i in range(len(en)))} | {', '.join(en)} |")
    return ("<!-- paper:section id=palabras-clave -->\n### B. Palabras clave pertinentes\n\nProsa fija de las palabras clave.\n\n"
            "| Componente | Palabras clave (ES) | Keywords (EN) |\n|---|---|---|\n" + "\n".join(rows) + f"\n\n{note}\n<!-- /paper:section -->\n\n"
            "<!-- paper:section id=ecuacion-busqueda -->\n### C. Ecuación de búsqueda\n\nProsa fija de la ecuación.\n\n"
            f"**Scopus**\n\n```text\n{m['queries']['Scopus']}```\n\n**Web of Science**\n\n```text\n{m['queries']['Web of Science']}```\n"
            "<!-- /paper:section -->\n\n")


@case("M21", "orden", "picoc nuevo con keywords frozen en el paper: RESYNC, --picoc-sync y --update fallan hasta copiar el picoc; la prosa frozen sigue protegida")
def _(sb):
    t = sb.theme(borrador=True)
    v = sb.versions(t)[-1]
    f = t / "paper" / v / "paper-borrador.md"
    first = next((t / "picoc").iterdir()) / "picoc.md"
    ref = "<!-- paper:section id=referencias -->"
    base = f.read_text(encoding="utf-8")
    f.write_text(base.replace(ref, metodologia(first) + ref), encoding="utf-8")
    sb.set_yml(t, r"^(  palabras-clave:\s*)off", r"\g<1>on")
    sb.set_yml(t, r"^(  ecuacion-busqueda:\s*)off", r"\g<1>on")
    sb.run(["paper", t, "--picoc-sync", f"paper/{v}/paper-borrador.md"], "OK", has="palabras-clave, ecuacion-busqueda")
    sb.run(["paper", t, "--update", "borrador"], "OK", quiet=True)
    sb.set_yml(t, r"^(  palabras-clave:\s*)on", r"\g<1>frozen")
    sb.set_yml(t, r"^(  ecuacion-busqueda:\s*)on", r"\g<1>frozen")
    new = sb.add_picoc(t, "PICOCT", f"{TODAY}-2-PICOCT")
    txt = new.read_text(encoding="utf-8")
    txt = txt.replace('`"cognitive accessibility"` |', '`"cognitive accessibility"` · `Asperger` |')
    txt = txt.replace('dyslexi* OR "cognitive accessibility" )', 'dyslexi* OR "cognitive accessibility" OR Asperger )')
    txt = txt.replace('dyslexi* OR "cognitive accessibility")', 'dyslexi* OR "cognitive accessibility" OR Asperger)')
    new.write_text(txt, encoding="utf-8")
    f.write_text(base.replace(ref, metodologia(first, '"autism disorder"') + ref), encoding="utf-8")
    sb.run(["paper", t], "OK", has="RESYNC")
    sb.run(["paper", t], "OK", has="WARN picoc-sync", lacks="fue editado")
    st = sb.run(["paper", t, "--picoc-sync", f"paper/{v}/paper-borrador.md"], "ERROR", has="-asperger")
    sb.check("+autism disorder" in st.output and "[Scopus]" in st.output, "--picoc-sync no reporta el término sobrante ni la query de Scopus desfasada")
    sb.run(["paper", t, "--update", "borrador"], "ERROR", has="no copia")
    f.write_text(base.replace(ref, metodologia(new) + ref), encoding="utf-8")
    sb.run(["paper", t, "--picoc-sync", f"paper/{v}/paper-borrador.md"], "OK")
    sb.run(["paper", t, "--update", "borrador"], "OK", quiet=True)
    sb.run(["paper", t], "OK", lacks="RESYNC")
    f.write_text(f.read_text(encoding="utf-8").replace("Prosa fija de las palabras clave.", "Prosa cambiada."), encoding="utf-8")
    sb.run(["paper", t], "ERROR", has="fuera de sus tablas")


@case("M22", "orden", "vocabularios citados (VOC): picoc que usa ACM CCS sin citarla falla; el paper debe citar en la nota los mismos vocabularios que el picoc")
def _(sb):
    t = sb.theme(borrador=True)
    v = sb.versions(t)[-1]
    new = sb.add_picoc(t, "PICOCT", f"{TODAY}-2-PICOCT")
    txt = new.read_text(encoding="utf-8").replace("IEEE 2019 no tiene *Accessibility*; las WCAG", "IEEE 2019 no tiene *Accessibility* (ACM CCS: *Accessibility*); las WCAG")
    new.write_text(txt, encoding="utf-8")
    sb.run(["lint", new], "ERROR", has="VOC")
    new.write_text(txt.replace("IEEE Thesaurus (IEEE, 2019) y términos libres", "IEEE Thesaurus (IEEE, 2019) y términos libres; los de informática se contrastan con la ACM Computing Classification System (ACM, 2012)"), encoding="utf-8")
    sb.run(["lint", new], "OK")
    sb.set_yml(t, r"^(  palabras-clave:\s*)off", r"\g<1>on")
    f = t / "paper" / v / "paper-borrador.md"
    ref = "<!-- paper:section id=referencias -->"
    base = f.read_text(encoding="utf-8")
    f.write_text(base.replace(ref, metodologia(new) + ref), encoding="utf-8")
    sb.run(["paper", t, "--picoc-sync", f"paper/{v}/paper-borrador.md"], "ERROR", has="ACM Computing Classification System")
    sb.run(["paper", t, "--update", "borrador"], "ERROR", has="no copia")
    acm = IEEE_NOTE.replace("; el resto son términos libres.", ". Los demás son términos libres; los de informática se contrastaron con la ACM Computing Classification System (Association for Computing Machinery [ACM], 2012).")
    f.write_text(base.replace(ref, metodologia(new, note=acm) + ref), encoding="utf-8")
    sb.run(["paper", t, "--picoc-sync", f"paper/{v}/paper-borrador.md"], "OK")
    mesh = acm.replace("(Association for Computing Machinery [ACM], 2012).", "(Association for Computing Machinery [ACM], 2012) y los Medical Subject Headings (NLM, 2026).")
    f.write_text(base.replace(ref, metodologia(new, note=mesh) + ref), encoding="utf-8")
    sb.run(["paper", t, "--picoc-sync", f"paper/{v}/paper-borrador.md"], "ERROR", has="que el picoc no usa")


@case("M23", "orden", "un formateador de Markdown (líneas vacías, *cursiva* → _cursiva_, relleno de tablas, [[ … ]]) no cuenta como editar una sección frozen, ni en la versión siguiente; un cambio de texto sí")
def _(sb):
    t = sb.theme(borrador=True)
    sb.run(["paper", t, "--update", "borrador"], "OK", quiet=True)
    sb.states(t, "frozen")
    v = sb.versions(t)[-1]
    f = t / "paper" / v / "paper-borrador.md"
    txt = f.read_text(encoding="utf-8")
    fmt = re.sub(r"(?<![\\*\w])\*(?![\s*])([^*\n]+?)(?<![\s\\])\*(?![*\w])", r"_\1_", txt)
    fmt = re.sub(r"^\|(-+\|)+$", lambda m: "| " + " | ".join("---" for _ in m.group(0).strip("|").split("|")) + " |", fmt, flags=re.M)
    fmt = fmt.replace("\n\n", "\n\n\n").replace("[[ ", "[[").replace(" ]]", "]]")
    sb.check(fmt != txt, "el formateo simulado no cambió el borrador")
    f.write_text(fmt, encoding="utf-8")
    sb.run(["paper", t], "OK", lacks="fue editado")
    sb.set_yml(t, r"^(  contexto:\s*)frozen", r"\g<1>on")
    sb.run(["paper", t, "--new-version"], "OK", quiet=True)
    v2 = sb.versions(t)[-1]
    sb.run(["paper", t, "--update", "borrador"], "OK", quiet=True)
    f2 = t / "paper" / v2 / "paper-borrador.md"
    f2.write_text(f2.read_text(encoding="utf-8").replace("\n\n\n", "\n\n"), encoding="utf-8")
    sb.run(["paper", t], "OK", lacks="fue editado")
    f2.write_text(f2.read_text(encoding="utf-8").replace("# Inteligencia artificial para", "# IA para"), encoding="utf-8")
    sb.run(["paper", t], "ERROR", has="frozen")


SCOPUS_HEAD = ["Authors", "Title", "Year", "Source title", "DOI", "Abstract", "Author Keywords", "Index Keywords", "Document Type", "EID"]
SCOPUS_ROWS = [
    ["A", "LLM assistant for autistic users", "2025", "J1", "10.1/a", "We evaluate an LLM assistant with 20 autistic users. © 2025 Elsevier", "autism; LLM; user trust", "Autism", "Article", "2-s2.0-1"],
    ["B", "EEG deep learning to classify ADHD", "2024", "J2", "10.1/b", "A CNN classifies ADHD from EEG.", "ADHD", "", "Article", "2-s2.0-2"],
    ["C", "LLM Assistant for Autistic Users.", "2025", "J1", "", "Same study, other export.", "", "", "Article", "2-s2.0-3"],
    ["D", "Screen reader testing with AI", "2023", "J3", "10.1/d", "Blind users, sensory only.", "blindness", "", "Article", "2-s2.0-4"],
    ["E", "Dyslexia-friendly text simplification", "2026", "J4", "10.1/e", "GPT simplifies texts; readability measured with users with dyslexia.", "dyslexia; LLM", "", "Article", "2-s2.0-5"],
]
WOS_HEAD = ["PT", "AU", "TI", "SO", "LA", "DT", "DE", "ID", "AB", "PY", "DI", "UT", "DL"]
WOS_ROWS = [
    ["J", "B", "EEG deep learning to classify ADHD", "J2", "English", "Article", "ADHD", "", "A CNN classifies ADHD.", "2024", "https://doi.org/10.1/B", "WOS:1", ""],
    ["J", "E", "Dyslexia friendly text simplification", "J4", "English", "Article", "", "", "Same study in WoS.", "2026", "", "WOS:2", ""],
    ["J", "W", "Voice agent requirements for ADHD developers", "J5", "English", "Article", "ADHD; LLM; user trust", "", "An LLM elicits requirements with 12 developers with ADHD.", "2025", "10.1/w", "WOS:3", ""],
]


def scopus_csv(path: Path) -> None:
    import csv as _csv
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        w = _csv.writer(fh, quoting=_csv.QUOTE_ALL)
        w.writerow(SCOPUS_HEAD)
        w.writerows(SCOPUS_ROWS)


def wos_txt(path: Path) -> None:
    path.write_text("\n".join("\t".join(r) for r in [WOS_HEAD, *WOS_ROWS]) + "\n", encoding="utf-8-sig")


def crib_decisions(d: Path, ids: dict[str, tuple], sintesis: bool = True) -> None:
    (d / "decisiones.jsonl").write_text("".join(json.dumps({"id": i, "decision": v[0], "criterios": v[1], "motivo": v[2], "duda": v[3], "acuerdo": not v[3]}, ensure_ascii=False) + "\n"
                                                for i, v in ids.items()), encoding="utf-8")
    if sintesis:
        (d / "sintesis.json").write_text(json.dumps({"aceptados": "Evalúan asistentes con usuarios.", "rechazados": "Solo diagnóstico o solo sensorial.",
                                                     "dudas": "Falta confirmar la fase del ciclo de vida."}, ensure_ascii=False), encoding="utf-8")


CRIB_OK = {"R001": ("SI", ["CI3"], "Evalúa un asistente LLM con usuarios autistas", False),
           "R002": ("NO", ["CE2"], "Solo clasifica TDAH con EEG", False),
           "R004": ("NO", ["CI3"], "Accesibilidad solo sensorial, sin población neurodivergente", False),
           "R005": ("SI", ["CI3"], "Simplificación con GPT evaluada con usuarios con dislexia", True),
           "R008": ("SI", ["CI3"], "LLM para requisitos con desarrolladores con TDAH", False)}


def crib_theme(sb) -> tuple[Path, Path]:
    t = sb.theme(paper=False)
    pdir = next((t / "picoc").iterdir())
    scopus_csv(pdir / "scopus-result.csv")
    wos_txt(pdir / "wos-resultados.txt")
    return t, pdir


@case("C01", "orden", "cribado 1: prepare pasa WoS a CSV, une Scopus y WoS en resultados-<MARCO>.csv y deduplica (DOI y título, dentro y entre bases) antes de los lotes; report escribe cribado-1.md y el shadow; apply escribe el unificado con las dos columnas sin tocar las exportaciones")
def _(sb):
    t = sb.theme(paper=False)
    pdir = next((t / "picoc").iterdir())
    sb.run(["crib", "prepare", t], "ERROR", has="no hay exportaciones")
    scopus_csv(pdir / "scopus-result.csv")
    wos_txt(pdir / "wos-resultados.txt")
    before = {p.name: p.read_bytes() for p in pdir.iterdir() if p.is_file()}
    st = sb.run(["crib", "prepare", t], "OK", has="3 duplicado(s)")
    sb.check(all(r in st.output for r in ("R003→R001", "R006→R002", "R007→R005")), f"prepare no lista los duplicados R003 (título, Scopus), R006 (DOI, WoS) y R007 (título, WoS): {st.output[:400]}")
    sb.check("líneas 1–5" in st.output, "prepare no da el rango de líneas del lote")
    uni = pdir / "resultados-PICOCT.csv"
    wcsv = pdir / "wos-resultados.csv"
    sb.check(uni.exists() and wcsv.exists(), "prepare no escribió el unificado o el CSV de WoS")
    import csv as _csv
    rows = list(_csv.reader(uni.open(encoding="utf-8-sig", newline="")))
    sb.check(rows[0][:3] == ["Id", "Fuente", "Título"] and len(rows) == 9, f"unificado con cabecera o filas inesperadas: {rows[0][:3]}, {len(rows)}")
    sb.check(rows[2][1] == "Scopus; WoS" and rows[6][1] == "WoS", f"Fuente mal: el conservado debe decir Scopus; WoS ({rows[2][1]}) y el duplicado WoS ({rows[6][1]})")
    w = pdir / ".cribado-1"
    regs = (w / "registros.jsonl").read_text(encoding="utf-8")
    sb.check(len(regs.splitlines()) == 5 and "Elsevier" not in regs and '"R003"' not in regs, "registros.jsonl con duplicados, copyright o conteo equivocado")
    sb.check("| CE1 | Registros duplicados" in (w / "criterios.md").read_text(encoding="utf-8"), "criterios.md sin los códigos del picoc")
    sb.run(["crib", "prepare", t], "OK", has="3 duplicado(s)")
    sb.run(["crib", "report", t], "ERROR", has="decisiones.jsonl")
    crib_decisions(w, {k: v for k, v in CRIB_OK.items() if k != "R005"})
    sb.run(["crib", "report", t], "ERROR", has="faltan 1")
    crib_decisions(w, {**CRIB_OK, "R005": ("TAL VEZ", [], "x", False)})
    sb.run(["crib", "report", t], "ERROR", has="no es SI ni NO")
    crib_decisions(w, {**CRIB_OK, "R006": ("SI", [], "x", False)})
    sb.run(["crib", "report", t], "ERROR", has="es un duplicado")
    crib_decisions(w, {**CRIB_OK, "R002": ("NO", ["CE99"], "x", False)})
    sb.run(["crib", "report", t], "ERROR", has="CE99")
    crib_decisions(w, CRIB_OK, sintesis=False)
    (w / "sintesis.json").unlink(missing_ok=True)
    sb.run(["crib", "report", t], "ERROR", has="sintesis.json")
    crib_decisions(w, CRIB_OK)
    sb.run(["crib", "apply", t], "ERROR", has="no están al día")
    sb.run(["crib", "report", t], "OK", has="3 duplicado(s), SI 3 (dudas 1), NO 2")
    rep = (pdir / "cribado-1.md").read_text(encoding="utf-8")
    for bit in ("## Duplicados: 3", "mismo DOI", "mismo título", "## Se aceptaron: 2", "## Se rechazaron: 2", "### Por criterio de inclusión no cumplido",
                "### Por criterio de exclusión", "## Dudas: 1", "## PRISMA", "Web of Science (n = 3)", "**Por qué:** Solo diagnóstico"):
        sb.check(bit in rep, f"cribado-1.md sin «{bit}»")
    sh = (pdir / "cribado-1.shadow.jsonl").read_text(encoding="utf-8").splitlines()
    sb.check(len(sh) == 9 and '"_meta"' in sh[0] and "Duplicado de R002 (Scopus; mismo DOI)" in sh[6], f"shadow inesperado: {len(sh)} líneas; {sh[6][:160] if len(sh) > 6 else ''}")
    sb.run(["crib", "apply", t], "OK", has="SI 3, NO 5")
    out = list(_csv.reader((pdir / "resultados-PICOCT-cribado-1.csv").open(encoding="utf-8-sig", newline="")))
    sb.check(out[0][-2:] == ["¿Se acepta?", "Justificación cribado 1"] and len(out) == 9, f"columnas o filas inesperadas: {out[0][-2:]}, {len(out)}")
    sb.check(out[3][-2] == "NO" and "Duplicado de R001" in out[3][-1], f"el duplicado por título no quedó como NO con su registro: {out[3][-2:]}")
    sb.check(out[5][-1].startswith("Duda:"), "la duda no se marca en la justificación")
    sb.check(all((pdir / n).read_bytes() == b for n, b in before.items()), "apply modificó una exportación")


@case("C02", "destruir", "cribado 1: set corrige y regenera reporte y shadow; set inválido no cambia nada; exportación cambiada, dos por base, cabeceras ajenas o sin criterios dan ERROR")
def _(sb):
    t, pdir = crib_theme(sb)
    sb.run(["crib", "prepare", t], "OK", quiet=True)
    w = pdir / ".cribado-1"
    crib_decisions(w, CRIB_OK)
    sb.run(["crib", "report", t], "OK", quiet=True)
    sb.run(["crib", "set", t, "R004", "SI", "Revisar a texto completo"], "OK", has="SI 4")
    sb.check('"id": "R004", "fuente": "Scopus", "uid": "10.1/d", "titulo": "Screen reader testing with AI", "decision": "SI"' in (pdir / "cribado-1.shadow.jsonl").read_text(encoding="utf-8"), "set no regeneró el shadow")
    sb.run(["crib", "set", t, "R002", "NO", "sin criterios", ""], "ERROR", has="al menos un criterio")
    sb.run(["crib", "set", t, "R006", "SI", "x"], "ERROR", has="duplicado")
    sb.run(["crib", "set", t, "R999", "SI", "x"], "ERROR", has="no tiene decisión")
    sb.run(["crib", "apply", t], "OK", has="SI 4")
    sb.run(["crib", "prepare", t], "OK", has="se conserva")
    sb.run(["crib", "apply", t], "OK", has="SI 4")
    wos = pdir / "wos-resultados.txt"
    wos.write_text(wos.read_text(encoding="utf-8-sig") + "J\tX\tNuevo estudio\tJ6\tEnglish\tArticle\t\t\tabc\t2026\t\tWOS:4\t\n", encoding="utf-8-sig")
    sb.run(["crib", "report", t], "ERROR", has="cambió")
    sb.run(["crib", "prepare", t], "OK", has="las exportaciones cambiaron")
    sb.check(not (w / "decisiones.jsonl").exists(), "con otras exportaciones las decisiones viejas siguieron vigentes")
    sb.run(["crib", "report", t], "ERROR", has="decisiones.jsonl")
    scopus_csv(pdir / "otro.csv")
    sb.run(["crib", "prepare", t], "ERROR", has="hay 2 exportaciones de Scopus")
    (pdir / "otro.csv").write_text("Titulo,Resumen\nx,y\n", encoding="utf-8")
    sb.run(["crib", "prepare", t], "OK", quiet=True)
    (pdir / "otro.csv").unlink()
    wos.write_text("PT\tTI\tUT\nJ\tSin resumen\tWOS:9\n", encoding="utf-8")
    sb.run(["crib", "prepare", t], "ERROR", has="AB (Resumen)")
    wos_txt(wos)
    p = pdir / "picoc.md"
    p.write_text(p.read_text(encoding="utf-8").split("## Criterios de inclusión y exclusión")[0], encoding="utf-8")
    sb.run(["crib", "prepare", t], "ERROR", has="Criterios de inclusión y exclusión")


@case("C03", "orden", "cribado 1: keywords mide los términos de la query y propone palabras clave de los aceptados; picoc:latest avisa la sugerencia pendiente y deja de avisar con la versión nueva")
def _(sb):
    t, pdir = crib_theme(sb)
    sb.run(["crib", "prepare", t], "OK", quiet=True)
    crib_decisions(pdir / ".cribado-1", CRIB_OK)
    sb.run(["crib", "keywords", t], "OK", has="términos analizados")
    kw = (pdir / ".cribado-1" / "keywords.md").read_text(encoding="utf-8")
    sb.check("| I | `llm` | 3 | 3 | 0 |" in kw and "Solo este término (SI / NO)" in kw and "| user trust | 2 | 0 |" in kw, f"keywords.md sin el conteo del término LLM o sin la candidata «user trust»: {kw[-300:]}")
    sb.run(["latest", t], "OK", lacks="sugerencia")
    (pdir / "cribado-1-sugerencia.md").write_text("# Sugerencia de búsqueda — cribado 1\n", encoding="utf-8")
    sb.run(["latest", t], "OK", has="modo sugerencia")
    nxt = t / "picoc" / f"{pdir.name.split('-PICOCT')[0]}-2-PICOCT"
    nxt.mkdir()
    (nxt / "picoc.md").write_text((pdir / "picoc.md").read_text(encoding="utf-8"), encoding="utf-8")
    sb.run(["latest", t], "OK", lacks="sugerencia")


@case("C04", "orden", "cribado 1: merge toma los acuerdos de los agentes, frena con los desacuerdos sin resolver, aplica resoluciones.md, escribe debate.md y conserva las correcciones del usuario")
def _(sb):
    t, pdir = crib_theme(sb)
    sb.run(["crib", "prepare", t], "OK", quiet=True)
    w = pdir / ".cribado-1"
    sb.run(["crib", "merge", t], "ERROR", has="lote-01.md")
    head = "## Defensor\n\n| Id | Decisión | Criterios | Duda | Motivo |\n|---|---|---|---|---|\n"
    rows = {"R001": "| R001 | SI | CI3 | no | Asistente LLM evaluado con usuarios autistas |",
            "R002": "| R002 | NO | CE2 | no | Solo clasifica TDAH con EEG |",
            "R004": "| R004 | NO | CE2 | no | Accesibilidad solo sensorial |",
            "R005": "| R005 | SI | CI3 | sí | Simplificación con GPT para dislexia |",
            "R008": "| R008 | SI | CI3 | no | LLM para requisitos con desarrolladores con TDAH |"}
    lote = w / "propuestas" / "lote-01.md"
    lote.write_text(head + "\n".join(v for k, v in rows.items() if k != "R008") + "\n\n## Crítico\n\n", encoding="utf-8")
    sb.run(["crib", "merge", t], "ERROR", has="no decidió R008")
    lote.write_text(head + "\n".join(rows.values()) + "\n\n## Crítico\n\n| Id | Propuesta | Tu decisión | Criterios | Motivo |\n|---|---|---|---|---|\n"
                    "| R008 | SI | NO | CE2 | Trabajo de congreso |\n| R002 | NO | NO | CI3 | Mismo NO, otro criterio |\n", encoding="utf-8")
    st = sb.run(["crib", "merge", t], "ERROR", has="1 desacuerdo(s) sin resolver")
    sb.check("R008 · defensor SI" in st.output and "Voice agent requirements" in st.output and "R002 ·" not in st.output, f"merge no muestra solo el desacuerdo real con su resumen: {st.output[:300]}")
    sb.check(not (w / "decisiones.jsonl").exists(), "merge escribió decisiones con desacuerdos pendientes")
    (w / "resoluciones.md").write_text("## Resoluciones\n\n| Id | Decisión | Criterios | Duda | Motivo |\n|---|---|---|---|---|\n| R008 | SI | CI3 | sí | Confirmar tipo de publicación a texto completo |\n", encoding="utf-8")
    sb.run(["crib", "merge", t], "OK", has="SI 3 (dudas 2), NO 2, 1 desacuerdo(s) resuelto(s)")
    decs = {json.loads(l)["id"]: json.loads(l) for l in (w / "decisiones.jsonl").read_text(encoding="utf-8").splitlines()}
    sb.check(decs["R008"]["acuerdo"] is False and decs["R008"]["duda"] and decs["R001"]["acuerdo"] and decs["R001"]["criterios"] == ["CI3"], f"decisiones mal consolidadas: {decs['R008']}, {decs['R001']}")
    sb.check("R008: defensor SI, crítico NO → SI con duda" in (w / "debate.md").read_text(encoding="utf-8"), "debate.md sin la resolución")
    crib_decisions(w, {}, sintesis=True)
    sb.run(["crib", "merge", t], "OK", quiet=True)
    sb.run(["crib", "report", t], "OK", quiet=True)
    sb.run(["crib", "set", t, "R004", "SI", "Revisar a texto completo"], "OK", quiet=True)
    sb.run(["crib", "merge", t], "OK", has="1 corrección(es) del usuario conservada(s)")


@case("K07", "marco", "redaccion:lint acepta n = X y [[ AGREGAR DIAGRAMA ]] como marcadores del usuario, pero sigue fallando con TODO y con apelaciones a «el lector» (no con «lector de pantalla»)")
def _(sb):
    f = sb.base / "metodo.md"
    f.write_text("# Método\n\nSe identificaron registros en Scopus (n = X) y en Web of Science (n = X). Se aplicaron los criterios CI1 y CE2.\n\n"
                 "[[ AGREGAR DIAGRAMA ]]\n\n*Fig. 1. Diagrama de flujo PRISMA 2020.*\n", encoding="utf-8")
    sb.run(["red", f], "OK", has="3 marcador(es) del usuario")
    f.write_text(f.read_text(encoding="utf-8") + "\nTODO: revisar.\n", encoding="utf-8")
    sb.run(["red", f], "ERROR", has="TODO")
    f.write_text("# Método\n\nSe probó con un lector de pantalla y con varios lectores de pantalla.\n", encoding="utf-8")
    sb.run(["red", f], "OK")
    f.write_text("# Método\n\nEsas decisiones son las que el lector debe poder revisar.\n", encoding="utf-8")
    sb.run(["red", f], "ERROR", has="el lector")


@case("K09", "marco", "redaccion:lint avisa (sin fallar) el ritmo monótono y el contraste troceado «No es X. Es Y.»; la prosa variada y el «no… sino» pasan limpios")
def _(sb):
    f = sb.base / "intro.md"
    f.write_text("# Contexto\n\nEl objeto de la revisión no es la tecnología asistiva clínica. Es el modo en que se construye el software.\n\n"
                 "La revisión reúne estudios de varias bases y los ordena por fase del ciclo de vida. "
                 "La selección aplica criterios de inclusión y de exclusión fijados antes de la búsqueda. "
                 "La extracción registra la técnica, la fase y la métrica de cada estudio incluido. "
                 "La síntesis cruza esas dimensiones para localizar las combinaciones sin evidencia.\n", encoding="utf-8")
    sb.run(["red", f], "OK", has="contraste troceado")
    sb.run(["red", f], "OK", has="ritmo monótono")
    f.write_text("# Contexto\n\nEl objeto de la revisión no es la tecnología asistiva clínica, sino el modo en que se construye el software. "
                 "Por eso importa la fase. Cada estudio incluido se ubica en ella, junto con la técnica y la métrica que reporta, "
                 "para que la síntesis pueda cruzar esas dimensiones.\n", encoding="utf-8")
    sb.run(["red", f], "OK", lacks="troceado")
    sb.run(["red", f], "OK", lacks="monótono")


@case("S08", "skills", "Metodología: make y polish del paper usan la bibliografía compartida, solo Scopus y WoS y los marcadores del usuario")
def _(sb):
    make = (SKILLS / "rsl-make-paper" / "SKILL.md").read_text(encoding="utf-8")
    polish = (SKILLS / "rsl-polish-paper" / "SKILL.md").read_text(encoding="utf-8")
    for need in ("global/bibliography/bibliography.md", "rsl:source", "[[ AGREGAR DIAGRAMA ]]", "Web of Science", "n = X", "excluidos por los filtros de la base de datos", "Búsqueda por base de datos", "IEEE, 2019", "estandares-rsl.md", "número de revisores", "CI1"):
        sb.check(need in make, f"rsl-make-paper/SKILL.md no contiene «{need}»")
    for need in ("global/bibliography/bibliography.md", "[[ AGREGAR DIAGRAMA ]]", "estandares-rsl.md", "IEEE, 2019", "Hilo", "R7", "R8", "Sustento", "Minimal diff", "Write, do not bolt on", "No redundancy"):
        sb.check(need in polish, f"rsl-polish-paper/SKILL.md no contiene «{need}»")
    sb.check("R7" in make, "rsl-make-paper/SKILL.md no pide el hilo entre párrafos (R7)")
    sb.check("R8" in make, "rsl-make-paper/SKILL.md no pide citar las afirmaciones importantes (R8)")
    critic = (ROOT / ".cursor" / "agents" / "critico-rsl.md").read_text(encoding="utf-8")
    sb.check("### Sustento" in critic, "critico-rsl no devuelve la tabla Sustento (afirmaciones importantes sin cita)")
    playbook = (ROOT / "playbooks" / "redaccion-academica.md").read_text(encoding="utf-8")
    sb.check("### R7" in playbook, "playbooks/redaccion-academica.md no tiene la regla R7 de coherencia y progresión")
    sb.check("Sin redundancia" in playbook, "el playbook no prohíbe repetir argumentos (R7, Sin redundancia)")
    sb.check("Los objetivos anteriores" in make, "rsl-make-paper no prohíbe abrir la Metodología resumiendo la Introducción")
    sb.check("### R8" in playbook, "playbooks/redaccion-academica.md no tiene la regla R8 de sustento con citas")
    agent = (ROOT / ".cursor" / "agents" / "redaccion-rsl.md").read_text(encoding="utf-8")
    sb.check("### Hilo" in agent, "redaccion-rsl no devuelve la tabla Hilo (intención y enlace de cada párrafo)")
    sb.check("### Calidad de prosa" in agent, "redaccion-rsl no juzga la calidad de la prosa de cada párrafo (tabla Calidad de prosa, R9)")
    sb.check("Calidad de prosa" in polish and "R9" in polish, "rsl-polish-paper no exige la Calidad de prosa (R9) de redaccion-rsl")
    for name, txt in (("rsl-make-paper", make), ("rsl-polish-paper", polish)):
        sb.check("quality reference" in txt, f"{name}/SKILL.md no usa las secciones frozen como referencia de calidad")
        sb.check("why it failed" in txt and "AskQuestion" in txt, f"{name}/SKILL.md no pregunta por qué falló una sección rewrite antes de reescribirla")
        sb.check("Base = this section" in txt, f"{name}/SKILL.md no toma la versión anterior como base de las secciones on")
    sb.check("### R9" in playbook, "playbooks/redaccion-academica.md no tiene la regla R9 de prosa con sentido y elegancia")
    cat = ROOT / "global" / "bibliography" / "bibliography.md"
    sb.check(cat.exists(), "falta el catálogo global/bibliography/bibliography.md")
    if cat.exists():
        txt = cat.read_text(encoding="utf-8")
        for key, folder in (("kitchenham-charters-2007", "picoc"), ("page-2021-prisma-2020", "prisma")):
            sb.check(key in txt, f"el catálogo no lista {key}")
            sb.check((ROOT / "global" / "bibliography" / folder / f"{key}.md").exists(), f"falta el MD de {key} en global/bibliography/{folder}/")



def report_dir() -> Path:
    qa = ROOT / "qa"
    name, n = TODAY, 1
    while (qa / name).exists():
        n += 1
        name = f"{TODAY}-{n}"
    d = qa / name
    d.mkdir(parents=True)
    return d


def suspect(step: Step) -> str:
    for k, path in SCRIPT_OF.items():
        if path in step.cmd:
            return path
    if "pnpm" in step.cmd:
        return "package.json / scripts"
    return ".cursor/skills · .cursor/agents · README"


def write_report(cases: list[Case], d: Path) -> None:
    failed = [c for c in cases if c.failed]
    data = {"date": TODAY, "total": len(cases), "failed": len(failed), "proposed": [], "cases": []}
    md = [f"# Reporte qa:destroy — {d.name}", "",
          f"Casos: {len(cases)} · fallidos: {len(failed)} · grupos: {', '.join(sorted({c.group for c in cases}))}", ""]
    if failed:
        md += ["## Fallos", "", "| Caso | Grupo | Qué se probó | Comando | Esperado | Obtenido | Problema | Sospechoso |", "|---|---|---|---|---|---|---|---|"]
    for c in cases:
        entry = {"id": c.id, "group": c.group, "desc": c.desc, "failed": c.failed, "crash": c.crash, "steps": []}
        for s in c.steps:
            if not s.problems:
                continue
            entry["steps"].append({"cmd": s.cmd, "expect": s.expect, "code": s.code, "last": s.last, "problems": s.problems, "suspect": suspect(s), "output": s.output})
            cell = lambda x: str(x).replace("|", "\\|").replace("\n", " ")[:160]
            md.append(f"| {c.id} | {c.group} | {cell(c.desc)} | `{cell(s.cmd)}` | {s.expect} | {cell(s.last)} | {cell('; '.join(s.problems))} | {suspect(s)} |")
        if c.crash:
            md.append(f"| {c.id} | {c.group} | {c.desc} | — | — | — | el caso se rompió: {c.crash} | scripts/qa-destroy.py |")
        data["cases"].append(entry)
    md += ["", "## Ataques propuestos", "", "_(los agrega rsl-qa-destroy tras la corrida; rsl-qa-fix los convierte en casos)_", ""]
    (d / "qa-report.md").write_text("\n".join(md), encoding="utf-8")
    (d / "qa-report.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main(argv: list[str]) -> int:
    keep, no_report, verbose = "--keep" in argv, "--no-report" in argv, "--verbose" in argv
    only = argv[argv.index("--only") + 1] if "--only" in argv and argv.index("--only") + 1 < len(argv) else None
    ids = {c.id for c in CASES}
    wanted = set(only.split(",")) if only and only not in GROUPS else set()
    if wanted - ids:
        print(f"ERROR: grupo o caso desconocido '{','.join(sorted(wanted - ids))}' (usa {' | '.join(GROUPS)} o ids como D01,M02).")
        return 2
    if not FIX.is_dir():
        print("ERROR: faltan los fixtures en qa/fixtures/. Restáuralos desde git.")
        return 1
    base = build_sandbox()
    sb = Sandbox(base)
    cases = [c for c in CASES if not only or c.group == only or c.id in wanted]
    try:
        for c in cases:
            sb.case = c
            try:
                c.fn(sb)
            except Exception as e:  # noqa: BLE001
                c.crash = f"{type(e).__name__}: {e}"
            mark = "FALLA" if c.failed else "ok"
            print(f"[{mark:5}] {c.id} {c.group:9} {c.desc}")
            for s in c.steps:
                if s.problems or verbose:
                    print(f"          $ {s.cmd}\n            → {s.last or '(sin salida)'}\n            {'✗ ' + '; '.join(s.problems) if s.problems else '✓'}")
            if c.crash:
                print(f"            ✗ el caso se rompió: {c.crash}")
    finally:
        if keep:
            print(f"sandbox conservado: {base}")
        else:
            shutil.rmtree(base, ignore_errors=True)
    failed = [c for c in cases if c.failed]
    where = ""
    if not no_report:
        d = report_dir()
        write_report(cases, d)
        where = f"; reporte en {d.relative_to(ROOT)}/qa-report.md"
    if failed:
        print(f"ERROR: {len(failed)} de {len(cases)} casos fallaron ({', '.join(c.id for c in failed)}){where}. Próximo paso: rsl-qa-fix.")
        return 1
    print(f"OK: {len(cases)} casos sin fallos{where}. Próximo paso: rsl-qa-destroy con ataques nuevos, o seguir con el flujo RSL.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
