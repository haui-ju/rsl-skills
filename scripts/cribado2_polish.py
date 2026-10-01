#!/usr/bin/env python3
"""Cribado 2 polish: merge lotes, cuota min_rsl, reporte y apply CSV."""
from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

import picoc_versions as pv
from cribado2_config import read_cribado2_min_rsl
from rsl_out import Fail, error, ok

WORK = ".cribado-2"
EVAL_DIR = "evaluaciones"
DECISIONES = "decisiones.jsonl"
CUOTA_JSON = "cuota.json"
EVAL_MD = "cribado-2-evaluacion.md"
CRITERIA = "Criterios de inclusión y exclusión"
HASH_RE = re.compile(r"<!-- cribado2:hash=([0-9a-f]+) -->")
COL_OK = "¿Se acepta?"
COL_WHY1 = "Justificación cribado 1"
COL_WHY2 = "Justificación cribado 2"
SHADOW_JSONL = "cribado-2.shadow.jsonl"

MERIT = frozenset({"SI", "PODRIA", "NO"})
RELLENO_LEVE = "RELLENO-LEVE"
RELLENO_ALTO = "RELLENO-ALTO"
ALL_DECISIONS = MERIT | {RELLENO_LEVE, RELLENO_ALTO}
ACCEPT_TIERS = frozenset({"SI", "PODRIA", RELLENO_LEVE, RELLENO_ALTO})
STAGE = "cribado-2"


def rel(p: Path, root: Path) -> str:
    try:
        return str(p.resolve().relative_to(root))
    except ValueError:
        return str(p)


def work_dir(corpus: Path) -> Path:
    d = corpus / WORK
    d.mkdir(parents=True, exist_ok=True)
    return d


def criteria_from_picoc(picoc: Path) -> dict[str, str]:
    text = picoc.read_text(encoding="utf-8")
    m = re.search(rf"^## {re.escape(CRITERIA)}\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not m:
        raise Fail(f"{rel(picoc, picoc.parent.parent.parent)} no tiene '## {CRITERIA}'", "regenera el picoc con rsl-picoc")
    out: dict[str, str] = {}
    for head, code in (("Inclusión", "CI"), ("Exclusión", "CE")):
        sm = re.search(rf"^### {head}\s*$(.*?)(?=^### |\Z)", m.group(1), re.M | re.S)
        items = re.findall(r"^\s*[-*]\s+(.+)$", sm.group(1), re.M) if sm else []
        for i, it in enumerate(items, 1):
            ex = re.match(r"^\**\s*(" + code + r"\d+)\.?\s*\**\s*(.*)$", it.strip(), re.I)
            if ex:
                out[ex.group(1).upper()] = ex.group(2).strip()
            else:
                out[f"{code}{i}"] = it.strip()
    return out


def indexed_ids(corpus: Path) -> set[str]:
    traza = corpus / "memoria-traza.json"
    if not traza.is_file():
        return set()
    data = json.loads(traza.read_text(encoding="utf-8"))
    ids = data.get("ids") or {}
    return {rid for rid, meta in ids.items() if (meta or {}).get("status") == "graphify_indexed"}


def cmd_polish_prepare(theme: Path, corpus: Path, folder: Path, root: Path) -> int:
    picoc = folder / "picoc.md"
    crit = criteria_from_picoc(picoc)
    w = work_dir(corpus)
    lines = [f"# Criterios — cribado 2\n", f"Fuente: `{rel(picoc, root)}`\n"]
    for code in sorted(crit):
        lines.append(f"- **{code}** {crit[code]}\n")
    (w / "criterios.md").write_text("".join(lines), encoding="utf-8")
    cat = json.loads((corpus / "documentos.json").read_text(encoding="utf-8"))
    idx = indexed_ids(corpus)
    reg_lines = []
    for r in sorted(cat["registros"], key=lambda x: x["orden"]):
        reg_lines.append(
            json.dumps(
                {
                    "orden": r["orden"],
                    "id": r["id"],
                    "titulo": r["titulo"],
                    "indexado": r["id"] in idx,
                    "sin_acceso": bool(r.get("sin_acceso")),
                },
                ensure_ascii=False,
            )
        )
    (w / "registros.jsonl").write_text("\n".join(reg_lines) + "\n", encoding="utf-8")
    n_idx = sum(1 for ln in reg_lines if json.loads(ln)["indexado"])
    return ok(
        f".cribado-2 preparado ({len(reg_lines)} registros, {n_idx} indexados)",
        f"corre lotes defensor/crítico y pnpm -s cribado2:polish-merge {rel(theme, root)}",
    )


def load_lotes(corpus: Path) -> dict[str, dict]:
    ev = corpus / WORK / EVAL_DIR
    if not ev.is_dir():
        return {}
    by_id: dict[str, dict] = {}
    for p in sorted(ev.glob("lote-*.jsonl")):
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            rid = row.get("id")
            if rid:
                by_id[rid] = row
    return by_id


def merit_decision(row: dict) -> str:
    d = (row.get("merito") or row.get("decision") or "NO").upper()
    if d not in MERIT:
        if d in {RELLENO_LEVE, RELLENO_ALTO}:
            return "NO"
        return "NO"
    return d


def cmd_polish_merge(theme: Path, corpus: Path, folder: Path, root: Path) -> int:
    cat = json.loads((corpus / "documentos.json").read_text(encoding="utf-8"))
    lotes = load_lotes(corpus)
    if not lotes:
        return error("no hay .cribado-2/evaluaciones/lote-*.jsonl", "completa los lotes de rsl-cribado-2-polish")
    w = work_dir(corpus)
    out = []
    missing = []
    for r in sorted(cat["registros"], key=lambda x: x["orden"]):
        rid = r["id"]
        if rid not in lotes:
            if r.get("sin_acceso") or r.get("descargado") != "si":
                rec = {
                    "orden": r["orden"],
                    "id": rid,
                    "titulo": r["titulo"],
                    "merito": "NO",
                    "decision": "NO",
                    "criterios": ["retrieval"],
                    "motivo": (r.get("porque") or "Sin texto completo.").strip()[:200],
                    "fuente": "documentos.json",
                }
                out.append(rec)
                continue
            missing.append(rid)
            continue
        raw = lotes[rid]
        mer = merit_decision(raw)
        rec = {
            "orden": raw.get("orden", r["orden"]),
            "id": rid,
            "titulo": raw.get("titulo") or r["titulo"],
            "merito": mer,
            "decision": mer,
            "criterios": raw.get("criterios") or [],
            "motivo": (raw.get("motivo") or "").strip(),
            "fuente": raw.get("fuente") or "grafo",
        }
        if mer == "NO" and raw.get("relleno"):
            rec["relleno"] = raw["relleno"]
        out.append(rec)
    if missing:
        return error(f"faltan decisiones para {', '.join(missing)}", "completa los lotes o añade filas en evaluaciones/")
    path = w / DECISIONES
    path.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in out), encoding="utf-8")
    return ok(f"{len(out)} decisiones de mérito en {rel(path, root)}", f"pnpm -s cribado2:cuota {rel(theme, root)}")


def relleno_rank(rec: dict) -> tuple[int, int]:
    """Menor = mejor candidato (leve antes que alto)."""
    rel = rec.get("relleno") or {}
    if not rel.get("elegible"):
        return (9, 999)
    nivel = (rel.get("nivel") or "alto").lower()
    tier = 0 if nivel == "leve" else 1
    orden = int(rel.get("orden") or 99)
    return (tier, orden)


def cmd_cuota(theme: Path, corpus: Path, folder: Path, root: Path) -> int:
    w = work_dir(corpus)
    dec_path = w / DECISIONES
    if not dec_path.is_file():
        return error(f"falta {rel(dec_path, root)}", f"pnpm -s cribado2:polish-merge {rel(theme, root)}")
    decisions = [json.loads(l) for l in dec_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    idx = indexed_ids(corpus)
    evaluables = [d for d in decisions if d["id"] in idx]
    min_rsl = read_cribado2_min_rsl(theme)
    nucleo = sum(1 for d in evaluables if d.get("merito") in ("SI", "PODRIA"))
    disponibles = len(evaluables)
    objetivo = min(min_rsl, disponibles)
    relleno_leve = relleno_alto = 0
    min_alcanzado = nucleo >= objetivo
    warn = ""

    if nucleo < objetivo:
        hueco = objetivo - nucleo
        pool = sorted(
            [d for d in evaluables if d.get("merito") == "NO"],
            key=relleno_rank,
        )
        elegibles = [d for d in pool if relleno_rank(d)[0] < 9]
        for d in elegibles:
            if hueco <= 0:
                break
            tier, _ = relleno_rank(d)
            if tier == 0:
                d["decision"] = RELLENO_LEVE
                relleno_leve += 1
            else:
                d["decision"] = RELLENO_ALTO
                relleno_alto += 1
            hueco -= 1
        aceptados = sum(1 for d in evaluables if d.get("decision") in ACCEPT_TIERS)
        min_alcanzado = aceptados >= objetivo
        if aceptados < objetivo:
            warn = (
                f"WARN min_rsl={min_rsl}: solo {aceptados} aceptables (núcleo {nucleo}, "
                f"disponibles indexados {disponibles}); no se alcanza el mínimo."
            )
    else:
        aceptados = nucleo

    dec_path.write_text("".join(json.dumps(d, ensure_ascii=False) + "\n" for d in decisions), encoding="utf-8")
    cuota = {
        "min_rsl": min_rsl,
        "disponibles_indexados": disponibles,
        "nucleo_si_podria": nucleo,
        "objetivo": objetivo,
        "relleno_leve": relleno_leve,
        "relleno_alto": relleno_alto,
        "aceptados_traza": sum(1 for d in decisions if d.get("decision") in ACCEPT_TIERS),
        "min_alcanzado": min_alcanzado,
    }
    (w / CUOTA_JSON).write_text(json.dumps(cuota, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if warn:
        print(warn)
    return ok(
        f"cuota: núcleo {nucleo}, relleno {relleno_leve}+{relleno_alto}, "
        f"aceptados traza {cuota['aceptados_traza']}/{objetivo} (min_rsl={min_rsl})",
        f"pnpm -s cribado2:polish-report {rel(theme, root)}",
    )


def decisions_hash(decisions: list[dict]) -> str:
    payload = json.dumps(
        [{k: d[k] for k in ("id", "decision", "motivo", "criterios") if k in d} for d in decisions],
        ensure_ascii=False,
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode()).hexdigest()[:12]


def cmd_polish_report(theme: Path, corpus: Path, folder: Path, root: Path) -> int:
    w = work_dir(corpus)
    dec_path = w / DECISIONES
    if not dec_path.is_file():
        return error(f"falta {rel(dec_path, root)}", f"pnpm -s cribado2:cuota {rel(theme, root)}")
    decisions = [json.loads(l) for l in dec_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    h = decisions_hash(decisions)
    cat = json.loads((corpus / "documentos.json").read_text(encoding="utf-8"))
    by_id = {d["id"]: d for d in decisions}
    counts = Counter(d.get("decision", "?") for d in decisions)

    def cell(s: str, n: int = 55) -> str:
        s = " ".join((s or "").split()).replace("|", "/")
        return s if len(s) <= n else s[: n - 1] + "…"

    lines = [
        f"# Cribado 2 — evaluación a texto completo",
        f"",
        f"<!-- cribado2:hash={h} -->",
        f"",
        f"Picoc: `{cat['picoc']}` · Corpus: `{rel(corpus, root)}/`",
        f"",
        f"Decisiones: SI {counts.get('SI', 0)} · PODRIA {counts.get('PODRIA', 0)} · "
        f"RELLENO-LEVE {counts.get(RELLENO_LEVE, 0)} · RELLENO-ALTO {counts.get(RELLENO_ALTO, 0)} · NO {counts.get('NO', 0)}",
        f"",
    ]
    cuota_p = w / CUOTA_JSON
    if cuota_p.is_file():
        cq = json.loads(cuota_p.read_text(encoding="utf-8"))
        lines.append(
            f"Cuota: min_rsl **{cq['min_rsl']}** · núcleo **{cq['nucleo_si_podria']}** · "
            f"objetivo **{cq['objetivo']}** · aceptados traza **{cq['aceptados_traza']}** · "
            f"min_alcanzado **{'sí' if cq['min_alcanzado'] else 'no'}**"
        )
        lines.append("")
    lines += [
        "| # | id | titulo | decision | motivo |",
        "|---:|---|---|---|---|",
    ]
    for r in sorted(cat["registros"], key=lambda x: x["orden"]):
        d = by_id.get(r["id"])
        if not d:
            lines.append(f"| {r['orden']} | {r['id']} | {cell(r['titulo'])} | — | sin decisión |")
            continue
        lines.append(
            f"| {r['orden']} | {r['id']} | {cell(r['titulo'])} | {d['decision']} | {cell(d.get('motivo', ''), 90)} |"
        )
    lines.append("")
    dest = corpus / EVAL_MD
    dest.write_text("\n".join(lines), encoding="utf-8")
    shadow_path = folder / SHADOW_JSONL
    shadow_path.write_text(shadow_lines(decisions, h, rel(corpus, root)), encoding="utf-8")
    return ok(
        f"{rel(dest, root)} + {rel(shadow_path, root)} ({len(decisions)} decisiones, hash {h})",
        f"revisa el informe; luego Usa rsl-cribado-2-aplicar sobre {rel(theme, root)}/",
    )


def csv_accept(decision: str) -> str:
    return "SI" if decision in ACCEPT_TIERS else "NO"


def shadow_lines(decisions: list[dict], h: str, corpus_rel: str) -> str:
    lines = [
        json.dumps(
            {"_meta": {"hash": h, "corpus": corpus_rel, "stage": "cribado-2"}},
            ensure_ascii=False,
        )
    ]
    for d in sorted(decisions, key=lambda x: x.get("orden", 0)):
        lines.append(
            json.dumps(
                {
                    "id": d["id"],
                    "orden": d.get("orden"),
                    "decision": d.get("decision"),
                    "acepta": csv_accept(d.get("decision", "NO")),
                    "criterios": d.get("criterios") or [],
                    "motivo": (d.get("motivo") or "").strip(),
                },
                ensure_ascii=False,
            )
        )
    return "\n".join(lines) + "\n"


def load_shadow(folder: Path) -> tuple[dict[str, dict], str | None]:
    p = folder / SHADOW_JSONL
    if not p.is_file():
        return {}, None
    raw = [ln for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()]
    if not raw:
        return {}, None
    meta = json.loads(raw[0]).get("_meta") or {}
    by_id: dict[str, dict] = {}
    for ln in raw[1:]:
        row = json.loads(ln)
        if row.get("id"):
            by_id[row["id"]] = row
    return by_id, meta.get("hash")


def cribado1_justification(row: list[str], header: list[str]) -> tuple[str, str]:
    """Devuelve (¿Se acepta? cribado 1, justificación cribado 1) de la fila del CSV unificado."""
    if len(header) >= 2 and header[-2] == COL_OK and header[-1] == COL_WHY1 and len(row) >= len(header):
        return (row[-2] or "NO").strip(), (row[-1] or "").strip()
    return "NO", ""


def motivo_csv(text: str, fallback: str) -> str:
    why = (text or fallback).strip()
    if not why:
        why = fallback
    return why if why.endswith(".") else why + "."


def update_prisma_eligibility(folder: Path, assessed: int, included: int, excluded: dict[str, int]) -> None:
    p = folder / "prisma.json"
    if not p.is_file():
        return
    data = json.loads(p.read_text(encoding="utf-8"))
    el = data.setdefault("eligibility", {})
    el["assessed"] = assessed
    el["excluded_reasons"] = excluded
    inc = data.setdefault("included", {})
    inc["studies"] = included
    inc["reports"] = included
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def cmd_apply(theme: Path, corpus: Path, folder: Path, root: Path) -> int:
    w = work_dir(corpus)
    dec_path = w / DECISIONES
    eval_md = corpus / EVAL_MD
    if not dec_path.is_file():
        return error(f"falta {rel(dec_path, root)}", f"pnpm -s cribado2:polish-report {rel(theme, root)}")
    decisions = [json.loads(l) for l in dec_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    h = decisions_hash(decisions)
    shadow_by, sh_hash = load_shadow(folder)
    if shadow_by and sh_hash and sh_hash != h:
        return error(
            f"{SHADOW_JSONL} desactualizado (hash {sh_hash} ≠ {h})",
            f"pnpm -s cribado2:polish-report {rel(theme, root)}",
        )
    if eval_md.is_file():
        m = HASH_RE.search(eval_md.read_text(encoding="utf-8"))
        if not m or m.group(1) != h:
            return error(
                f"{EVAL_MD} no coincide con decisiones.jsonl (hash {h})",
                f"pnpm -s cribado2:polish-report {rel(theme, root)}",
            )
    by_id = shadow_by if shadow_by else {d["id"]: d for d in decisions}
    marco = pv.dir_marco(folder / "picoc.md") or "MARCO"
    src = folder / f"resultados-{marco}-cribado-1.csv"
    if not src.is_file():
        raise Fail(f"falta {rel(src, root)}", "corre rsl-cribado-1-aplicar primero")
    with src.open(encoding="utf-8-sig", newline="") as fh:
        table = list(csv.reader(fh))
    header, body = table[0], table[1:]
    if len(header) >= 2 and header[-1] == COL_WHY1 and header[-2] == COL_OK:
        base_header = header[:-2]
    elif len(header) >= 2:
        base_header = header[:-2]
    else:
        base_header = header
    out_rows = []
    assessed_ids = set(by_id)
    excluded_criteria: Counter[str] = Counter()
    included = 0
    for row in body:
        rid = row[0] if row else ""
        d = by_id.get(rid)
        c1_ok, c1_why = cribado1_justification(row, header)
        if d:
            acc = d.get("acepta") or csv_accept(d.get("decision", "NO"))
            why = motivo_csv(d.get("motivo") or "", "Sin justificación en cribado 2.")
            crits = d.get("criterios") or []
            if acc == "NO" and crits:
                for c in crits:
                    excluded_criteria[str(c)] += 1
        else:
            acc = "NO"
            why = motivo_csv(c1_why, "Excluido en cribado 1.")
        if acc == "SI":
            included += 1
        out_rows.append(row[: len(base_header)] + [acc, why])
    dest = folder / f"resultados-{marco}-cribado-2.csv"
    with dest.open("w", encoding="utf-8-sig", newline="") as fh:
        wcsv = csv.writer(fh, quoting=csv.QUOTE_ALL)
        wcsv.writerow(base_header + [COL_OK, COL_WHY2])
        wcsv.writerows(out_rows)
    update_prisma_eligibility(folder, len(assessed_ids), included, dict(excluded_criteria))
    si = sum(1 for r in out_rows if r[-2] == "SI")
    return ok(
        f"{rel(dest, root)} con {len(out_rows)} registros (¿Se acepta? SI {si}, NO {len(out_rows) - si}); prisma eligibility actualizado",
        "revisión humana del CSV; usa el corpus aceptado en síntesis del paper",
    )
