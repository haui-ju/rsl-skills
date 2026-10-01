#!/usr/bin/env python3
"""cribado_2.use en docs/<slug>/config.yml — qué SI entran al retrieval de cribado 2."""
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

_MIN_CONFIG = """# Retrieval cribado 2 (rsl-cribado-2). Valores: all | solo_si | solo_dudas
# Paper completo: pnpm -s paper:status docs/<slug> --init
cribado_2:
  use: all
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


def _load_yaml(path: Path) -> dict:
    if yaml is None:
        raise Fail("falta PyYAML", "instálalo: pip install --user pyyaml | sudo pacman -S python-yaml")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
    except yaml.YAMLError as e:
        mark = getattr(e, "problem_mark", None)
        where = f" (línea {mark.line + 1})" if mark else ""
        raise Fail(f"{path.name} no es YAML válido{where}", "corrige la sintaxis de config.yml")
    except UnicodeDecodeError:
        raise Fail(f"{path.name} no está en UTF-8", "guarda config.yml en UTF-8")
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise Fail(f"{path.name} debe ser un mapa clave: valor", "corrige config.yml")
    return data


def _dump_yaml(data: dict) -> str:
    if yaml is None:
        raise Fail("falta PyYAML", "instálalo: pip install --user pyyaml | sudo pacman -S python-yaml")
    return yaml.safe_dump(data, allow_unicode=True, sort_keys=False, default_flow_style=False)


def read_cribado2_use(theme: Path) -> str:
    path = theme / CONFIG
    if not path.is_file():
        return USE_ALL
    data = _load_yaml(path)
    block = data.get("cribado_2")
    if not isinstance(block, dict):
        return USE_ALL
    return normalize_use(block.get("use"))


def write_cribado2_config_on_apply(theme: Path) -> str:
    """Asegura cribado_2.use en config.yml; no pisa use si ya existe. Devuelve el valor actual."""
    path = theme / CONFIG
    if not path.is_file():
        path.write_text(_MIN_CONFIG, encoding="utf-8")
        return USE_ALL
    data = _load_yaml(path)
    block = data.get("cribado_2")
    if not isinstance(block, dict):
        block = {}
        data["cribado_2"] = block
    if "use" not in block or block.get("use") is None or str(block.get("use")).strip() == "":
        block["use"] = USE_ALL
    else:
        block["use"] = normalize_use(block.get("use"))
    path.write_text(_dump_yaml(data), encoding="utf-8")
    return str(block["use"])


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
