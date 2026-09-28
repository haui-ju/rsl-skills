"""Versiones del marco de búsqueda: docs/<slug>/picoc/<AAAA-MM-DD>[-n]-<MARCO>/picoc.md.

El marco activo sale de docs/<slug>/paper/paper.yml (formato.marco); si no está, PICOCT.
"""
from __future__ import annotations

import re
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

COMPONENTS = {
    "PICO": ["P", "I", "C", "O"],
    "PICOC": ["P", "I", "C", "O", "Co"],
    "PICOCT": ["P", "I", "C", "O", "Co", "T"],
}
DEFAULT_MARCO = "PICOCT"
PICOC_DIR_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:-(\d+))?-(PICO|PICOC|PICOCT)$")
PICOC_FILE = "picoc.md"


def configured_marco(theme: Path) -> str:
    yml = theme / "paper" / "paper.yml"
    if yaml is None or not yml.exists():
        return DEFAULT_MARCO
    data = yaml.safe_load(yml.read_text(encoding="utf-8")) or {}
    return str((data.get("formato") or {}).get("marco") or DEFAULT_MARCO).upper()


def versions(theme: Path) -> list[Path]:
    d = theme / "picoc"
    if not d.is_dir():
        return []
    vs = [p for p in d.iterdir() if p.is_dir() and PICOC_DIR_RE.match(p.name)]
    key = lambda p: (PICOC_DIR_RE.match(p.name).group(1), int(PICOC_DIR_RE.match(p.name).group(2) or 1))
    return sorted(vs, key=key)


def latest_file(theme: Path) -> Path | None:
    for v in reversed(versions(theme)):
        if (v / PICOC_FILE).is_file():
            return v / PICOC_FILE
    return None


def dir_marco(path: Path) -> str | None:
    m = PICOC_DIR_RE.match(path.name if path.is_dir() else path.parent.name)
    return m.group(3) if m else None


def status(theme: Path) -> tuple[str, Path | None, str]:
    """(marco configurado, último picoc.md, OK | DESFASADO | FALTA)."""
    marco = configured_marco(theme)
    f = latest_file(theme)
    if f is None:
        return marco, None, "FALTA"
    return marco, f, "OK" if dir_marco(f) == marco else "DESFASADO"


def theme_of(path: Path) -> Path:
    """docs/<slug> a partir de docs/<slug>/picoc/<versión>/picoc.md."""
    return path.parent.parent.parent if path.parent.parent.name == "picoc" else path.parent
