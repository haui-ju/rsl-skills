#!/usr/bin/env python3
"""Integridad PDF/MD ↔ documentos.json (cribado 2)."""
from __future__ import annotations

import json
import re
from pathlib import Path

DOI_RE = re.compile(r"-\s*DOI:\s*`([^`]+)`", re.I)
PAGE1_IN_CHUNKS_RE = re.compile(
    r"## Page chunks.*?(### \[PDF p\.1\].*?\n\n(.{40,2500}))",
    re.S | re.I,
)
MOTIVO_SIN_ACCESO = (
    "No se pudo obtener el texto completo; el documento es de pago o no se dispone de acceso al mismo."
)
MOTIVO_OA_SIN_PDF = (
    "No se pudo obtener el texto completo. Figura como acceso abierto, "
    "pero el documento es de pago o no se dispone de acceso al mismo."
)
MOTIVO_NO_OA = (
    "No se pudo obtener el texto completo. No consta acceso abierto; "
    "el documento es de pago o no se dispone de acceso al mismo."
)
MOTIVO_SIN_DOI = "No hay DOI en el registro; localizar el documento por título."

_PORQUE_TECNICO = (
    "http",
    "bot",
    "script",
    "descarga automática",
    "descargas automáticas",
    "bloquea",
    "bloquean",
    "protección contra",
    "ábrela en el navegador",
    "el script",
)

STOP = frozenset(
    "with and the for from that this using based into their through about among other".split()
)


def normalize_doi(doi: str | None) -> str:
    if not doi:
        return ""
    d = doi.strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if d.startswith(prefix):
            d = d[len(prefix) :]
    return d.strip("/")


def no_texto_completo(reg: dict) -> bool:
    return bool(reg.get("sin_acceso")) or reg.get("descargado") != "si"


def _porque_es_tecnico(why: str) -> bool:
    w = why.lower()
    return any(t in w for t in _PORQUE_TECNICO)


def _infer_oa_registrada(reg: dict) -> bool | None:
    oa = reg.get("oa_registrada")
    if oa is not None:
        return bool(oa)
    why = (reg.get("porque") or "").lower()
    if "no tiene versión de acceso abierto" in why or "no consta versión de acceso abierto" in why:
        return False
    if "versión abierta" in why or "acceso abierto" in why or "figura como acceso abierto" in why:
        return True
    return None


def table_cell(s: str) -> str:
    """Celda de tabla markdown: sin truncar (solo escapa pipes y espacios)."""
    return " ".join((s or "").split()).replace("|", "/")


def _fin_oracion(text: str) -> str:
    t = text.strip()
    if not t:
        return MOTIVO_SIN_ACCESO
    return t if t.endswith(".") else t + "."


def motivo_sin_acceso(reg: dict) -> str:
    if not (reg.get("doi") or "").strip():
        return _fin_oracion(MOTIVO_SIN_DOI)
    oa = _infer_oa_registrada(reg)
    if oa is True:
        return MOTIVO_OA_SIN_PDF
    if oa is False:
        return MOTIVO_NO_OA
    why = (reg.get("porque") or "").strip()
    if why and not _porque_es_tecnico(why):
        if why.startswith("Sin DOI"):
            return _fin_oracion(MOTIVO_SIN_DOI)
        return _fin_oracion(why)
    return MOTIVO_SIN_ACCESO


def aplicar_porque_publico(reg: dict) -> None:
    if reg.get("descargado") == "si":
        reg["porque"] = ""
        return
    reg["porque"] = motivo_sin_acceso(reg)


def sanitize_catalog_porque(cat: dict) -> int:
    changed = 0
    for reg in cat.get("registros") or []:
        if reg.get("descargado") == "si":
            continue
        before = reg.get("porque")
        aplicar_porque_publico(reg)
        if reg.get("porque") != before:
            changed += 1
    return changed


def decision_no_recuperado(reg: dict) -> dict:
    return {
        "orden": reg["orden"],
        "id": reg["id"],
        "titulo": reg["titulo"],
        "merito": "NO",
        "decision": "NO",
        "criterios": ["retrieval"],
        "motivo": motivo_sin_acceso(reg),
        "fuente": "documentos.json",
    }


def md_path_for_reg(corpus: Path, reg: dict) -> Path | None:
    pdf_rel = reg.get("pdf") or ""
    if not pdf_rel:
        return None
    stem = Path(pdf_rel).stem
    md = corpus / "docs" / "md" / f"{stem}.md"
    return md if md.is_file() else None


def dois_align(expected: str, found: str) -> bool:
    if not expected or not found:
        return False
    if expected == found:
        return True
    if expected.startswith(found) or found.startswith(expected):
        return min(len(expected), len(found)) >= 10
    return False


def doi_in_text(expected: str, text: str) -> bool:
    if not expected:
        return False
    norm = text.lower().replace("https://doi.org/", "").replace("http://doi.org/", "")
    return expected in normalize_doi(norm) or expected in norm


def title_keywords(titulo: str) -> list[str]:
    words = [w.lower() for w in re.findall(r"[a-zA-Z]{6,}", titulo or "")]
    return [w for w in words if w not in STOP][:10]


def page1_title_text(md_text: str) -> str:
    m = PAGE1_IN_CHUNKS_RE.search(md_text)
    if not m:
        return ""
    lines = [ln.strip() for ln in m.group(2).splitlines() if len(ln.strip()) > 12]
    return " ".join(lines[:5])


def title_overlap(a: str, b: str) -> float:
    wa = {w.lower() for w in re.findall(r"[a-z]{5,}", a or "")}
    wb = {w.lower() for w in re.findall(r"[a-z]{5,}", b or "")}
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / len(wa | wb)


def title_matches_pdf(titulo: str, md_text: str) -> bool:
    page1 = page1_title_text(md_text)
    if page1 and title_overlap(titulo, page1) >= 0.22:
        return True
    keys = title_keywords(titulo)
    if not keys:
        return True
    sample = (page1 or md_text[800:3500]).lower()
    hits = sum(1 for w in keys if w in sample)
    need = min(3, max(2, len(keys) // 3))
    return hits >= need


def doi_from_md(md_path: Path) -> str | None:
    text = md_path.read_text(encoding="utf-8", errors="replace")[:8000]
    m = DOI_RE.search(text)
    if not m:
        return None
    raw = m.group(1).strip()
    if raw.lower() in ("unknown", "n/a", ""):
        return None
    return normalize_doi(raw)


def check_record(reg: dict, corpus: Path) -> list[str]:
    rid = reg.get("id") or "?"
    errs: list[str] = []
    if no_texto_completo(reg):
        return errs
    expected = normalize_doi(reg.get("doi"))
    if not expected:
        return errs
    md = md_path_for_reg(corpus, reg)
    if not md:
        errs.append(f"{rid}: falta MD para PDF descargado")
        return errs
    md_text = md.read_text(encoding="utf-8", errors="replace")
    if doi_in_text(expected, md_text):
        return errs
    found = doi_from_md(md)
    if found and dois_align(expected, found):
        return errs
    if title_matches_pdf(reg.get("titulo") or "", md_text):
        return errs
    if found and found != expected:
        errs.append(f"{rid}: DOI MD ({found}) ≠ documentos ({expected}); título no coincide con p.1")
    elif not found:
        errs.append(f"{rid}: MD sin DOI y título no coincide con el PDF indexado")
    else:
        errs.append(f"{rid}: contenido del PDF no coincide con título/DOI de documentos.json")
    pdf_rel = reg.get("pdf") or ""
    if pdf_rel and rid not in Path(pdf_rel).name:
        errs.append(f"{rid}: nombre PDF no contiene el id")
    return errs


def check_corpus(corpus: Path) -> dict:
    cat_path = corpus / "documentos.json"
    if not cat_path.is_file():
        return {"ok": False, "errors": ["falta documentos.json"], "by_id": {}}
    cat = json.loads(cat_path.read_text(encoding="utf-8"))
    by_id: dict[str, list[str]] = {}
    all_errs: list[str] = []
    seen_hash: dict[str, str] = {}
    for reg in sorted(cat.get("registros") or [], key=lambda x: x.get("orden", 0)):
        rid = reg.get("id")
        if not rid:
            continue
        errs = list(check_record(reg, corpus))
        h = reg.get("sha256")
        if not no_texto_completo(reg) and h:
            other = seen_hash.get(h)
            if other:
                errs.append(f"{rid}: PDF duplicado del registro {other} (mismo sha256)")
            else:
                seen_hash[h] = rid
        if errs:
            by_id[rid] = errs
            all_errs.extend(errs)
    return {"ok": not all_errs, "errors": all_errs, "by_id": by_id}


def integrity_ok_ids(corpus: Path) -> set[str]:
    rep = check_corpus(corpus)
    cat = json.loads((corpus / "documentos.json").read_text(encoding="utf-8"))
    ok: set[str] = set()
    bad = set(rep.get("by_id") or {})
    for reg in cat.get("registros") or []:
        rid = reg.get("id")
        if not rid or no_texto_completo(reg):
            continue
        if rid not in bad:
            ok.add(rid)
    return ok


def patch_memoria_traza(corpus: Path) -> None:
    traza_p = corpus / "memoria-traza.json"
    if not traza_p.is_file():
        return
    rep = check_corpus(corpus)
    cat = json.loads((corpus / "documentos.json").read_text(encoding="utf-8"))
    reg_by_id = {r["id"]: r for r in cat.get("registros") or []}
    traza = json.loads(traza_p.read_text(encoding="utf-8"))
    ids = traza.get("ids") or {}
    for rid, meta in ids.items():
        if not isinstance(meta, dict):
            continue
        reg = reg_by_id.get(rid) or {}
        errs = (rep.get("by_id") or {}).get(rid) or []
        if no_texto_completo(reg):
            meta["integrity_ok"] = False
            meta["integrity_errors"] = []
        else:
            meta["integrity_ok"] = not errs
            meta["integrity_errors"] = errs
    traza_p.write_text(json.dumps(traza, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
