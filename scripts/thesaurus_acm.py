#!/usr/bin/env python3
"""
ACM Computing Classification System 2012 (SKOS/XML) → JSON → graph.json Graphify.

  python scripts/thesaurus_acm.py                 # parse + build
  python scripts/thesaurus_acm.py --parse-only
  python scripts/thesaurus_acm.py --lookup "Accessibility"

Entrada:  global/thesaurus/acm-ccs/acm-ccs-2012.xml
          (https://dl.acm.org/pb-assets/dl_ccs/acm_ccs2012-1626988337597.xml)
Salidas (regenerables, gitignored):
  global/thesaurus/acm-ccs/acm-ccs.json
  global/thesaurus/acm-ccs/graphify-out/graph.json + GRAPH_REPORT.md

`thesaurus-ieee.py --check` importa `load_acm` y `acm_match` para la columna ACM CCS.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rsl_out import Fail, ok, run  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ACM_DIR = ROOT / "global" / "thesaurus" / "acm-ccs"
XML = ACM_DIR / "acm-ccs-2012.xml"
JSON_OUT = ACM_DIR / "acm-ccs.json"
GRAPH_DIR = ACM_DIR / "graphify-out"
SOURCE_URL = "https://dl.acm.org/pb-assets/dl_ccs/acm_ccs2012-1626988337597.xml"

NS = {
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "skos": "http://www.w3.org/2004/02/skos/core#",
}
RDF_ABOUT = f"{{{NS['rdf']}}}about"
RDF_RES = f"{{{NS['rdf']}}}resource"


def key(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", s.lower())).strip()


def parse() -> dict:
    root = ET.parse(XML).getroot()
    concepts: dict[str, dict] = {}
    for c in root.findall("skos:Concept", NS):
        cid = c.get(RDF_ABOUT)
        label = (c.findtext("skos:prefLabel", default="", namespaces=NS) or "").strip()
        concepts[cid] = {
            "label": label,
            "broader": [b.get(RDF_RES) for b in c.findall("skos:broader", NS)],
            "narrower": [n.get(RDF_RES) for n in c.findall("skos:narrower", NS)],
        }

    def path(cid: str) -> str:
        chain, cur = [], cid
        while cur in concepts:
            chain.append(concepts[cur]["label"])
            parents = concepts[cur]["broader"]
            cur = parents[0] if parents else None
        return " → ".join(reversed(chain))

    terms: dict[str, dict] = {}
    for cid, c in concepts.items():
        k = key(c["label"])
        e = terms.setdefault(k, {"term": c["label"], "ids": [], "paths": [], "BT": [], "NT": []})
        e["ids"].append(cid)
        e["paths"].append(path(cid))
        for rel, src in (("BT", "broader"), ("NT", "narrower")):
            for r in c[src]:
                lab = concepts.get(r, {}).get("label")
                if lab and lab not in e[rel]:
                    e[rel].append(lab)
    return {
        "source": SOURCE_URL,
        "xml": str(XML.relative_to(ROOT)),
        "stats": {"concepts": len(concepts), "terms": len(terms)},
        "terms": terms,
    }


def build_graph(data: dict) -> dict:
    from graphify.build import build
    from graphify.cluster import cluster
    from graphify.export import to_json

    terms = data["terms"]
    src = data["xml"]
    nid = {k: "acm_" + re.sub(r"[^a-z0-9]+", "_", k).strip("_") for k in terms}
    nodes = [
        {
            "id": nid[k],
            "label": e["term"],
            "file_type": "document",
            "node_kind": "acm_ccs_concept",
            "source_file": src,
            "source_location": e["ids"][0],
        }
        for k, e in terms.items()
    ]
    edges = [
        {
            "source": nid[k],
            "target": nid[key(t)],
            "relation": "broader" if rel == "BT" else "narrower",
            "confidence": "EXTRACTED",
            "source_file": src,
            "source_location": e["ids"][0],
            "weight": 1.0,
        }
        for k, e in terms.items()
        for rel in ("BT", "NT")
        for t in e[rel]
        if key(t) in terms
    ]
    G = build([{"nodes": nodes, "edges": edges}], directed=True, dedup=False, root=str(ROOT))
    communities = cluster(G)
    labels = {i: f"Community {i}" for i in communities}
    GRAPH_DIR.mkdir(parents=True, exist_ok=True)
    graph_path = GRAPH_DIR / "graph.json"
    if not to_json(G, communities, str(graph_path), force=True, community_labels=labels):
        raise Fail("to_json rechazó el grafo ACM CCS")
    try:
        from graphify.exporters.html import to_html

        to_html(G, communities, str(GRAPH_DIR / "graph.html"), community_labels=labels)
    except Exception as e:  # noqa: BLE001
        print(f"warn: graph.html skipped: {e}", file=sys.stderr)
    s = data["stats"]
    (GRAPH_DIR / "GRAPH_REPORT.md").write_text(
        "\n".join([
            "# ACM CCS 2012 graph",
            "",
            f"- Fuente: `{src}` ({data['source']})",
            f"- Conceptos: {s['concepts']} · Etiquetas únicas: {s['terms']}",
            f"- Nodos: {G.number_of_nodes()} · Aristas: {G.number_of_edges()} · Comunidades: {len(communities)}",
            "- Aristas: `broader` · `narrower` (el SKOS de ACM no trae sinónimos ni relacionados)",
            "",
        ]),
        encoding="utf-8",
    )
    return {"nodes": G.number_of_nodes(), "edges": G.number_of_edges(), "graph": str(graph_path.relative_to(ROOT))}


def load_acm() -> dict | None:
    if not JSON_OUT.exists():
        return None
    try:
        return json.loads(JSON_OUT.read_text(encoding="utf-8"))["terms"]
    except (json.JSONDecodeError, KeyError, UnicodeDecodeError):
        raise Fail(f"{JSON_OUT.relative_to(ROOT)} está corrupto", "regenéralo con: pnpm graphify:thesaurus:refresh")


def acm_match(q: str, terms: dict) -> tuple[dict | None, list[str]]:
    """Concepto ACM exacto (singular/plural) o conceptos que contienen todas las palabras del término."""
    k = key(q)
    for cand in (k, k[:-1] if k.endswith("s") else k + "s"):
        if cand in terms:
            return terms[cand], []
    words = [w.rstrip("s") for w in k.split() if len(w) > 3]
    near = [
        e["term"] for t, e in terms.items()
        if words and all(any(x.startswith(w) for x in t.split()) for w in words)
    ]
    return None, sorted(near, key=len)[:3]


def lookup(q: str) -> int:
    terms = load_acm()
    if terms is None:
        raise Fail(f"falta {JSON_OUT.relative_to(ROOT)}", "genéralo con: pnpm graphify:thesaurus:refresh")
    e, near = acm_match(q, terms)
    if e is None:
        return ok(f"'{q}' no es concepto ACM CCS" + (f"; cercanos: {' · '.join(near)}" if near else ""))
    print(f"\n{e['term']}  [{', '.join(e['ids'])}]")
    for p in e["paths"]:
        print(f"  ruta: {p}")
    for rel in ("BT", "NT"):
        if e[rel]:
            print(f"  {rel}: {' | '.join(e[rel])}")
    return ok(f"concepto ACM CCS para '{q}'")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--parse-only", action="store_true")
    ap.add_argument("--lookup")
    a = ap.parse_args(argv)
    if a.lookup is not None:
        return lookup(a.lookup)
    if not XML.exists():
        raise Fail(f"falta {XML.relative_to(ROOT)}", f"descárgalo de {SOURCE_URL}")
    data = parse()
    JSON_OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"parse": data["stats"], "json": str(JSON_OUT.relative_to(ROOT))}, ensure_ascii=False))
    if not a.parse_only:
        print(json.dumps({"build": build_graph(data)}, ensure_ascii=False))
    return ok(f"ACM CCS 2012 parseado ({data['stats']['terms']} etiquetas)")


if __name__ == "__main__":
    run(main)
