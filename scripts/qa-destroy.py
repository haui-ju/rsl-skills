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


@case("D14", "destruir", "picoc vacío, sin **Marco:**, sin queries, con DOCTYPE y con T invertido")
def _(sb):
    def mut(fn, has):
        t = sb.theme()
        f = next((t / "picoc").glob("*/picoc.md"))
        f.write_text(fn(f.read_text(encoding="utf-8")), encoding="utf-8")
        sb.run(["lint", t], "ERROR", has=has)
    mut(lambda s: "", "vacío")
    mut(lambda s: s.replace("**Marco:** PICOCT", "Marco PICOCT"), "Marco")
    mut(lambda s: re.sub(r"## Query Web of Science.*?(?=## Query IEEE)", "", s, flags=re.S), "Web of Science")
    mut(lambda s: s.replace("AND PUBYEAR > 2019 AND PUBYEAR < 2027", "AND PUBYEAR > 2019 AND PUBYEAR < 2027 AND DOCTYPE(ar)", 1), "tipo de documento")
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


@case("D18", "destruir", "citas rotas: APA huérfana, IEEE fuera de orden y sin referencia")
def _(sb):
    t = sb.theme()
    f = t / "apa.md"
    f.write_text("Texto (Gómez, 2023) y (Pérez, 2024).\n\n## Referencias\n\nPérez, J. (2024). *A*.\n\nRuiz, A. (2020). *B*.\n", encoding="utf-8")
    sb.run(["paper", t, "--cites", f], "ERROR", has="Gómez")
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


@case("K04", "marco", "picoc PIO con filtro de año o con una fila de más")
def _(sb):
    t = sb.theme()
    sb.set_yml(t, r"^(  marco:\s*)PICOCT", r"\g<1>PIO")
    f = sb.add_picoc(t, "PIO", f"{TODAY}-2-PIO")
    good = f.read_text(encoding="utf-8")
    f.write_text(re.sub(r"(TITLE-ABS-KEY \(.*?\n\))\n", r"\1\nAND PUBYEAR > 2019 AND PUBYEAR < 2027\n", good, count=1, flags=re.S), encoding="utf-8")
    sb.run(["lint", t], "ERROR", has="sin componente T")
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
        for s in sorted(set(re.findall(r"\b(rsl-[a-z]+(?:-[a-z]+)*)\b(?!-?\*)", txt)) - {"rsl-skills"}):
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
