#!/usr/bin/env python3
"""cribado_2 en docs/<slug>/config.yml — retrieval (use) y meta min_rsl para cribado 2 polish."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore[assignment]

from rsl_out import Fail

CONFIG = "config.yml"
USE_ALL = "all"
USE_SOLO_SI = "solo_si"
USE_SOLO_DUDAS = "solo_dudas"
USE_VALUES = (USE_ALL, USE_SOLO_SI, USE_SOLO_DUDAS)
MIN_RSL_DEFAULT = 40

_ALIAS = {
    "all": USE_ALL,
    "todo": USE_ALL,
    "todos": USE_ALL,
    "solo_si": USE_SOLO_SI,
    "solosi": USE_SOLO_SI,
    "solo si": USE_SOLO_SI,
    "sisi": USE_SOLO_SI,
    "solo_dudas": USE_SOLO_DUDAS,
    "solodudas": USE_SOLO_DUDAS,
    "solo dudas": USE_SOLO_DUDAS,
    "dudas": USE_SOLO_DUDAS,
    "solo duda": USE_SOLO_DUDAS,
}

_MIN_BLOCK = """# Retrieval cribado 2 (rsl-cribado-2). use: all | solo_si | solo_dudas
# min_rsl: meta mínima de estudios aceptados tras cribado 2 (SI+PODRIA+relleno en CSV)
cribado_2:
  use: all
  min_rsl: 40
"""


def _norm_key(raw: str) -> str:
    return re.sub(r"[\s_\-]+", " ", (raw or "").strip().lower())


def normalize_use(raw: str | None, *, strict: bool = True) -> str:
    if raw is None or not str(raw).strip():
        return USE_ALL
    key = _norm_key(str(raw))
    if key in _ALIAS:
        return _ALIAS[key]
    if strict:
        opts = ", ".join(USE_VALUES)
        raise Fail(
            f"cribado_2.use «{raw}» no es válido",
            f"usa uno de: {opts} (en config.yml)",
        )
    return USE_ALL


def normalize_min_rsl(raw: object | None, *, strict: bool = True) -> int:
    if raw is None or (isinstance(raw, str) and not raw.strip()):
        return MIN_RSL_DEFAULT
    try:
        n = int(raw)
    except (TypeError, ValueError):
        if strict:
            raise Fail(f"cribado_2.min_rsl «{raw}» no es un entero ≥ 0", "usa p. ej. min_rsl: 40 en config.yml")
        return MIN_RSL_DEFAULT
    if n < 0:
        if strict:
            raise Fail(f"cribado_2.min_rsl no puede ser negativo ({n})", "usa min_rsl: 40 o el valor que necesites")
        return MIN_RSL_DEFAULT
    return n


def _parse_cribado2_block(text: str) -> dict[str, object]:
    """Lee use y min_rsl del bloque cribado_2 sin reescribir el YAML entero."""
    use = USE_ALL
    min_rsl = MIN_RSL_DEFAULT
    m = re.search(r"^cribado_2:\s*$([\s\S]*?)(?=^\S|\Z)", text, re.M)
    block = m.group(1) if m else ""
    um = re.search(r"^\s*use:\s*(\S+)\s*$", block, re.M)
    if um:
        use = normalize_use(um.group(1))
    mm = re.search(r"^\s*min[_-]rsl:\s*(\d+)\s*$", block, re.M)
    if mm:
        min_rsl = normalize_min_rsl(int(mm.group(1)))
    return {"use": use, "min_rsl": min_rsl}


def _patch_cribado2_in_text(text: str, use: str, min_rsl: int, *, force_use: bool, force_min: bool) -> str:
    if "cribado_2:" not in text:
        return text.rstrip() + "\n\n" + _MIN_BLOCK + "\n"
    if not re.search(r"^\s*min[_-]rsl:", text, re.M):
        text = re.sub(
            r"(^cribado_2:\s*\n)(\s*use:\s*\S+\s*\n)",
            rf"\1\2  min_rsl: {min_rsl}\n",
            text,
            count=1,
            flags=re.M,
        )
    if force_use:
        text = re.sub(r"(^cribado_2:\s*\n\s*)use:\s*\S+", rf"\1use: {use}", text, count=1, flags=re.M)
    if force_min and re.search(r"^\s*min[_-]rsl:", text, re.M):
        text = re.sub(r"^\s*min[_-]rsl:\s*\d+", f"  min_rsl: {min_rsl}", text, count=1, flags=re.M)
    return text


def read_cribado2_use(theme: Path) -> str:
    path = theme / CONFIG
    if not path.is_file():
        return USE_ALL
    return str(_parse_cribado2_block(path.read_text(encoding="utf-8-sig"))["use"])


def read_cribado2_min_rsl(theme: Path) -> int:
    path = theme / CONFIG
    if not path.is_file():
        return MIN_RSL_DEFAULT
    return int(_parse_cribado2_block(path.read_text(encoding="utf-8-sig"))["min_rsl"])


def ensure_cribado2_config(theme: Path) -> dict[str, object]:
    """Añade cribado_2 o min_rsl sin re-serializar todo config.yml."""
    path = theme / CONFIG
    if not path.is_file():
        path.write_text(_MIN_BLOCK + "\n", encoding="utf-8")
        return {"use": USE_ALL, "min_rsl": MIN_RSL_DEFAULT}
    text = path.read_text(encoding="utf-8-sig")
    parsed = _parse_cribado2_block(text)
    had_block = "cribado_2:" in text
    had_min = bool(re.search(r"^\s*min[_-]rsl:", text, re.M))
    had_use = bool(re.search(r"^cribado_2:[\s\S]*?^\s*use:", text, re.M))
    use = parsed["use"] if had_use else USE_ALL
    min_rsl = parsed["min_rsl"] if had_min else MIN_RSL_DEFAULT
    new_text = _patch_cribado2_in_text(
        text,
        str(use),
        int(min_rsl),
        force_use=False,
        force_min=False,
    )
    if new_text != text or not had_block:
        path.write_text(new_text, encoding="utf-8")
    return {"use": use, "min_rsl": min_rsl}


def write_cribado2_config_on_apply(theme: Path) -> str:
    return str(ensure_cribado2_config(theme)["use"])


def filter_si_for_retrieval(si: list[dict], dmap: dict[str, bool], use: str) -> list[dict]:
    use = normalize_use(use)
    if use == USE_ALL:
        return list(si)
    out: list[dict] = []
    for row in si:
        rid = row.get("Id") or ""
        duda = dmap.get(rid, False)
        if use == USE_SOLO_SI and not duda:
            out.append(row)
        elif use == USE_SOLO_DUDAS and duda:
            out.append(row)
    return out


def empty_retrieval_message(use: str, si_total: int) -> str:
    use = normalize_use(use)
    if use == USE_SOLO_DUDAS:
        return f"ningún SI con duda en el shadow (hay {si_total} SI en el CSV)"
    if use == USE_SOLO_SI:
        return f"todos los SI del CSV tienen duda ({si_total} registros)"
    return "no hay registros SI en el CSV"
