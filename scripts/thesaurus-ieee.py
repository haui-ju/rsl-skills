#!/usr/bin/env python3
"""
IEEE Thesaurus (PDF, 2 columnas) → JSON estructurado → graph.json Graphify.

  python scripts/thesaurus-ieee.py                # parse + build
  python scripts/thesaurus-ieee.py --parse-only
  python scripts/thesaurus-ieee.py --lookup "Assistive technology"

Salidas (regenerables, gitignored — licencia CC BY-NC-ND):
  global/thesaurus/ieee-thesaurus.json
  global/thesaurus/graphify-out/graph.json + GRAPH_REPORT.md
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THES_DIR = ROOT / "global" / "thesaurus"
PDF = THES_DIR / "IEEE.pdf"
JSON_OUT = THES_DIR / "ieee-thesaurus.json"
GRAPH_DIR = THES_DIR / "graphify-out"

FIRST_PAGE = 3
HEADER_MAX_TOP = 100
FOOTER_MIN_TOP = 1060

REL_RE = re.compile(r"^\s*(BT|NT|RT|UF|USE):\s*(.*)$")
TEXT_RE = re.compile(r'<text top="(\d+)" left="(\d+)" width="\d+" height="\d+" font="\d+">(.*?)</text>')
PAGE_RE = re.compile(r'<page number="(\d+)"[^>]*width="(\d+)"')
RELS = ("BT", "NT", "RT", "UF", "USE")
EDGE_NAME = {"BT": "broader", "NT": "narrower", "RT": "related", "USE": "use", "UF": "used_for"}


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    return re.sub(r"\s+", " ", s).strip()


def key(s: str) -> str:
    return norm(s).casefold()


def join_wrap(a: str, b: str) -> str:
    return a + b if a.endswith("-") else f"{a} {b}"


def split_known(value: str, known: set[str]) -> list[str] | None:
    words = value.split(" ")
    best: list[list[str] | None] = [None] * (len(words) + 1)
    best[0] = []
    for i in range(len(words)):
        if best[i] is None:
            continue
        for j in range(i + 1, len(words) + 1):
            cand = " ".join(words[i:j])
            if key(cand) in known and (best[j] is None or len(best[i]) + 1 < len(best[j])):
                best[j] = best[i] + [cand]
    return best[-1]


def repair_values(values: list[str], known: set[str]) -> list[str]:
    vals = [re.sub(r"\s+AND$", "", v) for v in values]
    out: list[str] = []
    i = 0
    while i < len(vals):
        v = vals[i]
        if key(v) not in known and i + 1 < len(vals) and key(join_wrap(v, vals[i + 1])) in known:
            v = join_wrap(v, vals[i + 1])
            i += 1
        if key(v) not in known:
            parts = split_known(v, known)
            if parts:
                out.extend(parts)
                i += 1
                continue
        out.append(v)
        i += 1
    return list(dict.fromkeys(out))


def pdf_lines():
    """Yield (page, lines) in reading order; each line = list of (left, raw_text), columns split."""
    xml = subprocess.run(
        ["pdftohtml", "-xml", "-i", "-stdout", "-f", str(FIRST_PAGE), str(PDF)],
        capture_output=True, text=True, check=True,
    ).stdout
    for chunk in xml.split("<page ")[1:]:
        pm = PAGE_RE.match("<page " + chunk)
        page, width = int(pm.group(1)), int(pm.group(2))
        cols: dict[int, dict[int, list]] = {0: {}, 1: {}}
        for top, left, raw in TEXT_RE.findall(chunk):
            top, left = int(top), int(left)
            if top < HEADER_MAX_TOP or top > FOOTER_MIN_TOP:
                continue
            if not re.sub(r"<[^>]+>", "", raw).strip():
                continue
            col = 0 if left < width / 2 else 1
            row = next((t for t in cols[col] if abs(t - top) <= 3), top)
            cols[col].setdefault(row, []).append((left, raw))
        for col in (0, 1):
            yield page, [sorted(items) for _, items in sorted(cols[col].items())]


def parse() -> dict:
    entries: list[dict] = []
    cur: dict | None = None
    cur_rel: str | None = None
    value_x = 0
    last_was_heading = False

    for page, lines in pdf_lines():
        for items in lines:
            first_raw = items[0][1]
            if "<b>" in first_raw or "<i>" in first_raw:
                text = norm(re.sub(r"<[^>]+>", "", " ".join(r for _, r in items)))
                if last_was_heading and cur is not None:
                    cur["term"] = join_wrap(cur["term"], text)
                else:
                    cur = {"term": text, "page": page, "bold": "<b>" in first_raw, **{r: [] for r in RELS}}
                    entries.append(cur)
                    cur_rel = None
                last_was_heading = True
                continue
            last_was_heading = False
            if cur is None:
                continue
            line = " ".join(re.sub(r"<[^>]+>", "", r) for _, r in items)
            m = REL_RE.match(line)
            if m:
                cur_rel = m.group(1)
                vals = [(l, r) for l, r in items if not REL_RE.match(r)]
                value_x = vals[0][0] if vals else items[-1][0] + 40
                if m.group(2).strip():
                    cur[cur_rel].append(norm(m.group(2)))
                continue
            if cur_rel is None:
                continue
            text = norm(line)
            starts_value = items[0][0] >= value_x - 20 or first_raw[:1].isspace()
            if starts_value or not cur[cur_rel]:
                cur[cur_rel].append(text)
            else:
                cur[cur_rel][-1] = join_wrap(cur[cur_rel][-1], text)

    for e in entries:
        for r in RELS:
            e[r] = [v for v in e[r] if v != "AND"]

    merged: dict[str, dict] = {}
    for e in entries:
        k = key(e["term"])
        if k in merged:
            for r in RELS:
                merged[k][r].extend(v for v in e[r] if v not in merged[k][r])
        else:
            merged[k] = {"term": norm(e["term"]), "page": e["page"], **{r: list(dict.fromkeys(e[r])) for r in RELS}}
    known = set(merged)
    for e in merged.values():
        for r in ("BT", "NT", "RT", "USE"):
            e[r] = repair_values(e[r], known)
        e["preferred"] = not e["USE"]

    targets = [(e["term"], r, t) for e in merged.values() for r in ("BT", "NT", "RT", "USE") for t in e[r]]
    unresolved = [t for t in targets if key(t[2]) not in merged]
    stats = {
        "terms": len(merged),
        "preferred": sum(e["preferred"] for e in merged.values()),
        "non_preferred": sum(not e["preferred"] for e in merged.values()),
        "relations": len(targets),
        "unresolved": len(unresolved),
        "unresolved_pct": round(100 * len(unresolved) / max(1, len(targets)), 2),
    }
    return {
        "source": "IEEE Thesaurus 2019 v1.0 (CC BY-NC-ND 4.0)",
        "pdf": str(PDF.relative_to(ROOT)),
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "stats": stats,
        "unresolved_sample": unresolved[:40],
        "terms": dict(sorted(merged.items())),
    }


def node_ids(terms: dict) -> dict[str, str]:
    ids: dict[str, str] = {}
    used: set[str] = set()
    for k in terms:
        base = "ieee_" + re.sub(r"[^a-z0-9]+", "_", k).strip("_")
        nid, n = base, 2
        while nid in used:
            nid, n = f"{base}_{n}", n + 1
        used.add(nid)
        ids[k] = nid
    return ids


def build_graph(data: dict) -> dict:
    from graphify.build import build
    from graphify.cluster import cluster
    from graphify.export import to_json

    terms = data["terms"]
    src = data["pdf"]
    ids = node_ids(terms)
    nodes = [
        {
            "id": ids[key(e["term"])],
            "label": e["term"],
            "file_type": "document",
            "node_kind": "preferred_term" if e["preferred"] else "non_preferred_term",
            "source_file": src,
            "source_location": f"p.{e['page']}",
        }
        for e in terms.values()
    ]
    edges = []
    for e in terms.values():
        for r in ("BT", "NT", "RT", "USE"):
            for t in e[r]:
                if key(t) not in terms:
                    continue
                edges.append({
                    "source": ids[key(e["term"])],
                    "target": ids[key(t)],
                    "relation": EDGE_NAME[r],
                    "confidence": "EXTRACTED",
                    "source_file": src,
                    "source_location": f"p.{e['page']}",
                    "weight": 1.0,
                })
    G = build([{"nodes": nodes, "edges": edges}], directed=True, dedup=False, root=str(ROOT))
    communities = cluster(G)
    labels = {i: f"Community {i}" for i in communities}
    GRAPH_DIR.mkdir(parents=True, exist_ok=True)
    graph_path = GRAPH_DIR / "graph.json"
    if not to_json(G, communities, str(graph_path), force=True, community_labels=labels):
        sys.exit("error: to_json refused")
    s = data["stats"]
    (GRAPH_DIR / "GRAPH_REPORT.md").write_text(
        "\n".join([
            "# IEEE Thesaurus graph",
            "",
            f"- Fuente: `{src}` ({data['source']})",
            f"- Términos: {s['terms']} (preferidos {s['preferred']}, no preferidos {s['non_preferred']})",
            f"- Nodos: {G.number_of_nodes()} · Aristas: {G.number_of_edges()} · Comunidades: {len(communities)}",
            f"- Relaciones no resueltas: {s['unresolved']} ({s['unresolved_pct']} %)",
            "- Aristas: `broader` (BT) · `narrower` (NT) · `related` (RT) · `use` (no preferido → preferido)",
            "",
        ]),
        encoding="utf-8",
    )
    return {"nodes": G.number_of_nodes(), "edges": G.number_of_edges(), "communities": len(communities), "graph": str(graph_path.relative_to(ROOT))}


def lookup(q: str) -> None:
    data = json.loads(JSON_OUT.read_text(encoding="utf-8"))
    terms = data["terms"]
    hits = [terms[key(q)]] if key(q) in terms else [e for k, e in terms.items() if key(q) in k][:15]
    if not hits:
        print(f"no IEEE term for: {q}")
        return
    for e in hits:
        print(f"\n{e['term']}  [{'preferred' if e['preferred'] else 'non-preferred'} · p.{e['page']}]")
        for r in RELS:
            if e[r]:
                print(f"  {r}: {' | '.join(e[r])}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--parse-only", action="store_true")
    ap.add_argument("--lookup")
    a = ap.parse_args()
    if a.lookup:
        lookup(a.lookup)
        return
    if not PDF.exists():
        sys.exit(f"missing {PDF}")
    data = parse()
    JSON_OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"parse": data["stats"], "json": str(JSON_OUT.relative_to(ROOT))}, ensure_ascii=False))
    if not a.parse_only:
        print(json.dumps({"build": build_graph(data)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
