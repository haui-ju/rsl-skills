"""Versiones del marco de búsqueda: docs/<slug>/picoc/<AAAA-MM-DD>[-n]-<MARCO>/picoc.md.

El marco activo sale de docs/<slug>/paper/paper.yml (formato.marco); si no está, PICOCT.
El marco es libre: cualquier combinación de letras del diccionario (PIO, PICO, PICOS, PICOCT…);
la primera C es Comparación y la segunda, Contexto (Co). También se acepta una lista [P, I, O].
"""
from __future__ import annotations

import datetime as dt
import re
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

NAMES = {
    "P": "población",
    "I": "intervención",
    "C": "comparación",
    "O": "resultado",
    "Co": "contexto",
    "T": "tiempo",
    "S": "diseño de estudio",
}
DEFAULT_MARCO = "PICOCT"
PICOC_DIR_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:-([2-9]|[1-9]\d+))?-([A-Za-z]+)$")
PICOC_FILE = "picoc.md"


class MarcoError(ValueError):
    fix = "corrige formato.marco en paper/paper.yml (letras P I C O T S; la segunda C es contexto)"


class ConfigError(MarcoError):
    fix = "corrige la sintaxis de paper/paper.yml"


class VersionError(MarcoError):
    fix = "renombra o borra la carpeta indicada; las versiones las crea rsl-picoc"


def version_date(s: str) -> dt.date | None:
    """Fecha de una carpeta de versión, o None si no es una fecha real."""
    try:
        return dt.date.fromisoformat(s)
    except ValueError:
        return None


def parse_marco(value) -> list[str]:
    """'PICOC' -> [P, I, C, O, Co]; [P, I, O] -> [P, I, O]. MarcoError si hay letras desconocidas o repetidas."""
    if isinstance(value, (list, tuple)):
        comps = [str(v).strip() for v in value]
        comps = [c if c in NAMES else c.upper() for c in comps]
    else:
        s = str(value or "").strip()
        if not re.fullmatch(r"[A-Za-z]+", s):
            raise MarcoError(f"marco '{value}' vacío o con caracteres no válidos")
        comps = []
        for ch in s.upper():
            comps.append("Co" if ch == "C" and "C" in comps else ch)
    if not comps:
        raise MarcoError(f"marco '{value}' vacío")
    bad = [c for c in comps if c not in NAMES]
    if bad:
        raise MarcoError(f"letra(s) desconocida(s) {', '.join(bad)} en el marco '{value}' (válidas: {', '.join(k for k in NAMES if k != 'Co')}; la segunda C es Contexto)")
    if len(set(comps)) != len(comps):
        raise MarcoError(f"componente repetido en el marco '{value}'")
    if comps == ["T"]:
        raise MarcoError(f"el marco '{value}' solo tiene T; necesita al menos un componente de búsqueda (P, I, C, O o S)")
    return comps


def marco_label(value) -> str:
    """Nombre canónico del marco (letras): [P, I, C, O, Co] -> PICOC."""
    return "".join("C" if c == "Co" else c for c in parse_marco(value))


def component_words(value) -> str:
    """'población, intervención y resultado'."""
    words = [NAMES[c] for c in parse_marco(value)]
    return words[0] if len(words) == 1 else ", ".join(words[:-1]) + " y " + words[-1]


def configured_marco(theme: Path) -> str:
    """Marco de paper.yml como etiqueta canónica; lanza MarcoError si no es válido."""
    yml = theme / "paper" / "paper.yml"
    if yaml is None or not yml.exists():
        return DEFAULT_MARCO
    try:
        data = yaml.safe_load(yml.read_text(encoding="utf-8-sig"))
    except yaml.YAMLError as e:
        mark = getattr(e, "problem_mark", None)
        raise ConfigError("paper/paper.yml no es YAML válido" + (f" (línea {mark.line + 1})" if mark else ""))
    except UnicodeDecodeError:
        raise ConfigError("paper/paper.yml no está en UTF-8")
    data = data or {}
    if not isinstance(data, dict):
        raise ConfigError("paper/paper.yml debe ser un mapa clave: valor")
    formato = data.get("formato") or {}
    if not isinstance(formato, dict):
        raise ConfigError("formato de paper/paper.yml debe ser un bloque clave: valor")
    if "marco" not in formato:
        return DEFAULT_MARCO
    try:
        return marco_label(formato["marco"])
    except MarcoError as e:
        raise MarcoError(f"formato.marco: {e}")


def versions(theme: Path) -> list[Path]:
    d = theme / "picoc"
    if not d.is_dir():
        return []
    today = dt.date.today()
    vs, seen = [], {}
    for p in d.iterdir():
        m = PICOC_DIR_RE.match(p.name)
        if not (p.is_dir() and m and (day := version_date(m.group(1)))):
            continue
        if day > today:
            raise VersionError(f"picoc/{p.name} tiene fecha futura")
        k = (m.group(1), int(m.group(2) or 1))
        if k in seen:
            raise VersionError(f"picoc/{seen[k]} y picoc/{p.name} tienen la misma fecha y número; no se sabe cuál es la última")
        seen[k] = p.name
        vs.append((k, p))
    return [p for _, p in sorted(vs, key=lambda x: x[0])]


def next_dir(theme: Path, marco: str, today: str | None = None) -> Path:
    today = today or dt.date.today().isoformat()
    used = [int(m.group(2) or 1) for p in versions(theme) if (m := PICOC_DIR_RE.match(p.name)) and m.group(1) == today]
    n = max(used, default=0) + 1
    return theme / "picoc" / (f"{today}-{marco_label(marco)}" if n == 1 else f"{today}-{n}-{marco_label(marco)}")


def latest_file(theme: Path) -> Path | None:
    for v in reversed(versions(theme)):
        if (v / PICOC_FILE).is_file():
            return v / PICOC_FILE
    return None


def dir_marco(path: Path) -> str | None:
    m = PICOC_DIR_RE.match(path.name if path.is_dir() else path.parent.name)
    return m.group(3).upper() if m else None


def status(theme: Path) -> tuple[str, Path | None, str]:
    """(marco configurado, último picoc.md, OK | DESFASADO | FALTA). Lanza MarcoError si el marco no es válido."""
    marco = configured_marco(theme)
    f = latest_file(theme)
    if f is None:
        return marco, None, "FALTA"
    return marco, f, "OK" if dir_marco(f) == marco else "DESFASADO"


def theme_of(path: Path) -> Path:
    """docs/<slug> a partir de docs/<slug>/picoc/<versión>/picoc.md."""
    return path.parent.parent.parent if path.parent.parent.name == "picoc" else path.parent
