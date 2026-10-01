#!/usr/bin/env python3
"""
Theme Graphify pipeline (optimized).

Stages:
  A prepare  — diff manifest, pdftotext, structure RAG MD with real ## headings
  B stamp    — mark agent-rag MD as md_ready
  C build    — AST graph from theme + RSL/MD
  D verify   — quality gates (nodes per paper, queries, manifest)

Manifest: docs/<tema>/RSL/index-manifest.json

Corpus mode (--corpus <dir>): PDFs in <dir>/*.pdf, MD in <dir>/MD, manifest in
<dir>/index-manifest.json, graph in <dir>/graphify-out (used by cribado 2).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import NamedTuple

MANIFEST_NAME = "index-manifest.json"
MIN_WORDS_OK = 400
MIN_ALPHA_RATIO = 0.55
MIN_HEADINGS_FOR_PAPER = 8
MIN_NODES_PER_PAPER_SOURCE = 8


class Layout(NamedTuple):
    root: Path
    pdf_dir: Path
    pdf_prefix: str
    md_dir: Path
    md_prefix: str
    manifest_dir: Path
    out: Path
    theme_md: bool


def layout(
    theme: Path,
    corpus: Path | None = None,
    *,
    pdf_subdir: str | None = None,
    md_subdir: str | None = None,
) -> Layout:
    if corpus is None:
        return Layout(
            root=theme,
            pdf_dir=theme / "RSL" / "PDF",
            pdf_prefix="RSL/PDF/",
            md_dir=theme / "RSL" / "MD",
            md_prefix="RSL/MD/",
            manifest_dir=theme / "RSL",
            out=theme / "graphify-out",
            theme_md=True,
        )
    pdf_rel = pdf_subdir or "docs/pdf"
    md_rel = md_subdir or "docs/md"
    return Layout(
        root=corpus,
        pdf_dir=corpus / pdf_rel,
        pdf_prefix=f"{pdf_rel}/",
        md_dir=corpus / md_rel,
        md_prefix=f"{md_rel}/",
        manifest_dir=corpus,
        out=corpus / "graphify-out",
        theme_md=False,
    )


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def entry_key(rel: str) -> str:
    return rel.replace("\\", "/")


PAPER_VERSION_RE = re.compile(r"^\d{4}-\d{2}-\d{2}(?:-(\d+))?$")


def theme_md_files(theme: Path) -> list[Path]:
    """theme/*.md + paper/<última versión>/*.md (solo la última, para no duplicar nodos)."""
    files = sorted(theme.glob("*.md"))
    paper = theme / "paper"
    if paper.is_dir():
        versions = [p for p in paper.iterdir() if p.is_dir() and PAPER_VERSION_RE.match(p.name)]
        if versions:
            latest = max(versions, key=lambda p: (p.name[:10], int(PAPER_VERSION_RE.match(p.name).group(1) or 1)))
            files += sorted(latest.glob("*.md"))
    return files


def word_stats(text: str) -> tuple[int, float]:
    words = re.findall(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9]{2,}", text)
    if not words:
        return 0, 0.0
    alpha = sum(1 for w in words if re.search(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]", w))
    return len(words), alpha / len(words)


def quality_ok(text: str) -> tuple[bool, str]:
    words, ratio = word_stats(text)
    if words < MIN_WORDS_OK:
        return False, f"too_few_words:{words}"
    if ratio < MIN_ALPHA_RATIO:
        return False, f"low_alpha_ratio:{ratio:.2f}"
    return True, f"words:{words},alpha:{ratio:.2f}"


def load_manifest(rsl: Path) -> dict:
    path = rsl / MANIFEST_NAME
    if not path.exists():
        return {"version": 1, "updated_at": None, "entries": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def save_manifest(rsl: Path, manifest: dict) -> None:
    manifest["updated_at"] = utc_now()
    (rsl / MANIFEST_NAME).write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def count_md_headings(text: str) -> int:
    return len(re.findall(r"(?m)^#{1,3}\s+\S+", text))


def extract_doi(text: str) -> str | None:
    m = re.search(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+", text)
    return m.group(0).rstrip(".)]") if m else None


def extract_keywords_block(text: str) -> list[str]:
    m = re.search(
        r"(?is)KEYWORDS?\s*(?:\n|\r|:)\s*(.+?)(?:\n\s*\n|\n\s*1\s+Introduction|\n\s*#)",
        text,
    )
    if not m:
        # single-line after KEYWORDS
        m = re.search(r"(?im)^KEYWORDS?\s*[:\n]\s*(.+)$", text)
    if not m:
        return []
    raw = re.sub(r"\s+", " ", m.group(1)).strip()
    parts = re.split(r"[,;]", raw)
    out = []
    for p in parts:
        p = p.strip(" .-")
        if 2 < len(p) < 80:
            out.append(p)
    return out[:20]


def extract_abstractish(text: str) -> str:
    # Frontiers-style Introduction:/Methods:/Results:/Discussion: blurb
    m = re.search(
        r"(?is)Introduction:\s*(.+?)(?:\n\s*KEYWORDS|\n\s*1\s+Introduction)",
        text,
    )
    if m:
        return re.sub(r"\s+", " ", m.group(1)).strip()[:2500]
    m = re.search(r"(?is)\bAbstract\b[:\s]+(.+?)(?:\n\s*\n|\n\s*Keywords)", text)
    if m:
        return re.sub(r"\s+", " ", m.group(1)).strip()[:2500]
    # first long paragraph
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if len(p.strip()) > 200]
    return re.sub(r"\s+", " ", paras[0])[:2500] if paras else ""


def slugify_anchor(text: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9áéíóúüñÁÉÍÓÚÜÑ]+", "-", text.lower()).strip("-")
    return s[:80] or "chunk"


def split_pdf_pages(raw_text: str) -> list[str]:
    """pdftotext emits \\x0c between pages."""
    pages = raw_text.split("\f")
    # drop trailing empty from final formfeed
    while pages and not pages[-1].strip():
        pages.pop()
    if not pages:
        return [raw_text]
    return pages


def first_substantive_line(page_text: str) -> str:
    for line in page_text.splitlines():
        s = re.sub(r"\s+", " ", line).strip()
        if 12 < len(s) < 140 and re.search(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]{4}", s):
            if not re.match(r"^(DOI|http|OPEN ACCESS|EDITED BY|REVIEWED BY)", s, re.I):
                return s
    return "(sin título de página)"


def find_page_for_snippet(pages: list[str], snippet: str) -> int | None:
    if not snippet or len(snippet) < 12:
        return None
    needle = re.sub(r"\s+", " ", snippet[:80]).lower()
    for i, page in enumerate(pages, start=1):
        hay = re.sub(r"\s+", " ", page).lower()
        if needle[:40] in hay:
            return i
    return None


def detect_sections_with_pages(pages: list[str]) -> list[dict]:
    """Numbered section headers → {num, title, page, anchor}."""
    section_re = re.compile(
        r"^\s*(\d+(?:\.\d+){0,3})\s+([A-ZÁÉÍÓÚÜÑ][\wÁÉÍÓÚÜÑáéíóúüñ ,;:/\-]{2,100})\s*$"
    )
    found: list[dict] = []
    seen: set[str] = set()
    for page_no, page in enumerate(pages, start=1):
        for line in page.splitlines():
            m = section_re.match(line.strip())
            if not m:
                continue
            num, title = m.group(1), m.group(2).strip(" .-")
            if len(title) < 4:
                continue
            key = f"{num}:{title.lower()}"
            if key in seen:
                continue
            seen.add(key)
            label = f"{num} {title}"
            found.append(
                {
                    "num": num,
                    "title": title,
                    "label": label,
                    "page": page_no,
                    "anchor": slugify_anchor(f"p{page_no}-{label}"),
                }
            )
    return found


def structure_rag_md(*, stem: str, pdf_name: str, raw_text: str) -> str:
    """
    Técnica: índice con locators (página PDF + ancla) + chunks ### [PDF p.N].

    Graphify solo indexa headings → cada locator/chunk es un nodo consultable.
    El cuerpo bajo el heading guarda el texto; el label dice en qué página del PDF está.
    """
    pages = split_pdf_pages(raw_text)
    doi = extract_doi(raw_text)
    keywords = extract_keywords_block(raw_text)
    abstract = extract_abstractish(raw_text)
    sections = detect_sections_with_pages(pages)

    title = stem.replace("-", " ")
    for line in pages[0].splitlines() if pages else []:
        s = re.sub(r"\s+", " ", line).strip()
        if 20 < len(s) < 180 and "DOI" not in s and "http" not in s.lower():
            if re.search(r"[A-Za-z]{4}", s) and not s.isupper():
                title = s
                break

    # --- locator rows for index table ---
    locators: list[dict] = []

    abs_page = find_page_for_snippet(pages, abstract[:60]) if abstract else 1
    locators.append(
        {
            "kind": "abstract",
            "label": "Abstract / blurb",
            "page": abs_page or 1,
            "anchor": "abstract",
        }
    )
    for sec in sections:
        locators.append(
            {
                "kind": "section",
                "label": sec["label"],
                "page": sec["page"],
                "anchor": sec["anchor"],
            }
        )

    seed_concepts = list(keywords)
    for extra in re.split(r"[-_]+", stem):
        if len(extra) > 3:
            seed_concepts.append(extra)
    seen_c: set[str] = set()
    concept_hooks: list[tuple[str, int | None]] = []
    for c in seed_concepts:
        key = c.lower()
        if key in seen_c:
            continue
        seen_c.add(key)
        page = find_page_for_snippet(pages, c)
        concept_hooks.append((c, page))
        locators.append(
            {
                "kind": "concept",
                "label": c,
                "page": page or "?",
                "anchor": slugify_anchor(f"concept-{c}"),
            }
        )

    finding_hooks: list[tuple[str, int | None]] = []
    for sent in re.split(r"(?<=[.!?])\s+", abstract):
        sent = sent.strip()
        if 40 < len(sent) < 220:
            page = find_page_for_snippet(pages, sent[:50])
            finding_hooks.append((sent, page))
            locators.append(
                {
                    "kind": "finding",
                    "label": sent[:90] + ("…" if len(sent) > 90 else ""),
                    "page": page or abs_page or 1,
                    "anchor": slugify_anchor(f"finding-{sent[:40]}"),
                }
            )
        if len(finding_hooks) >= 6:
            break

    # page map locators
    for i, page in enumerate(pages, start=1):
        preview = first_substantive_line(page)
        locators.append(
            {
                "kind": "page",
                "label": preview[:90],
                "page": i,
                "anchor": f"pdf-p{i}",
            }
        )

    parts: list[str] = [
        f"# {title}",
        "",
        f"> Fuente PDF: `{pdf_name}` · técnica **locator index** (página + ancla) + chunks Graphify",
        "",
        "## Metadata",
        f"- Stem: `{stem}`",
        f"- PDF: `{pdf_name}`",
        f"- DOI: `{doi or 'unknown'}`",
        f"- Pages: `{len(pages)}`",
        f"- Structured_at: `{utc_now()}`",
        f"- Technique: `pdf-page-locators + heading-chunks`",
        "",
        "## Locator index (qué hay y en qué página del PDF)",
        "",
        "| Kind | Label | PDF page | MD anchor |",
        "|------|-------|----------|-----------|",
    ]
    # Cap table size but keep sections/concepts/findings/pages (pages summarized if huge)
    table_rows = []
    page_rows = [L for L in locators if L["kind"] == "page"]
    other_rows = [L for L in locators if L["kind"] != "page"]
    for L in other_rows:
        table_rows.append(
            f"| {L['kind']} | {L['label'].replace('|', '/')} | {L['page']} | `#{L['anchor']}` |"
        )
    # include all page rows if <= 40 else first/last sample + note
    if len(page_rows) <= 40:
        for L in page_rows:
            table_rows.append(
                f"| page | p.{L['page']}: {L['label'].replace('|', '/')} | {L['page']} | `#{L['anchor']}` |"
            )
    else:
        for L in page_rows[:15] + page_rows[-5:]:
            table_rows.append(
                f"| page | p.{L['page']}: {L['label'].replace('|', '/')} | {L['page']} | `#{L['anchor']}` |"
            )
        table_rows.append(f"| page | … {len(page_rows)-20} páginas más en chunks abajo … | — | — |")
    parts.extend(table_rows)

    parts.extend(["", "## Abstract", f'<a id="abstract"></a>', ""])
    parts.append(abstract or "_(no abstract auto-detected)_")

    parts.extend(["", "## Keywords", ""])
    if keywords:
        parts.extend(f"- {k}" for k in keywords)
    else:
        parts.append("- _(none auto-detected)_")

    parts.extend(["", "## Concept index (graph hooks + página)", ""])
    for c, page in concept_hooks or [("systematic review", None)]:
        pinfo = f"p.{page}" if page else "p.?"
        parts.append(f'<a id="{slugify_anchor(f"concept-{c}")}"></a>')
        parts.append(f"### [PDF {pinfo}] Concept: {c}")
        parts.append(f"- Locator: `{pdf_name}` · página **{page or '?'}**")
        parts.append("")

    parts.extend(["", "## Findings index (graph hooks + página)", ""])
    for sent, page in finding_hooks or [("see full text", abs_page)]:
        pinfo = f"p.{page}" if page else "p.?"
        parts.append(f'<a id="{slugify_anchor(f"finding-{sent[:40]}")}"></a>')
        parts.append(f"### [PDF {pinfo}] Finding: {sent}")
        parts.append(f"- Locator: `{pdf_name}` · página **{page or '?'}**")
        parts.append("")

    parts.extend(
        [
            "",
            "## Relevance hooks",
            "### Theme relevance: software engineering and accessibility",
            "### Theme relevance: cognitive accessibility and neurodiversity",
            "### Theme relevance: evaluation metrics and WCAG",
            "",
            "## Sections (detected in PDF)",
            "",
        ]
    )
    if sections:
        for sec in sections:
            parts.append(f'<a id="{sec["anchor"]}"></a>')
            parts.append(f"### [PDF p.{sec['page']}] Section: {sec['label']}")
            parts.append(f"- Locator: `{pdf_name}` · página **{sec['page']}** · ancla `#{sec['anchor']}`")
            parts.append("")
    else:
        parts.append("_(no numbered sections auto-detected)_")
        parts.append("")

    parts.extend(["", "## Page chunks (texto por página del PDF)", ""])
    parts.append(
        "_Cada heading es un nodo Graphify. El label incluye la página para volver al PDF sin releer todo._"
    )
    parts.append("")
    for i, page in enumerate(pages, start=1):
        preview = first_substantive_line(page)
        body = page.strip()
        # keep chunk readable but bounded for token-ish sanity in future agent reads
        if len(body) > 12000:
            body = body[:12000] + "\n\n…[truncado en MD; ver RSL/MD/_raw]…"
        parts.append(f'<a id="pdf-p{i}"></a>')
        parts.append(f"### [PDF p.{i}] {preview}")
        parts.append(f"- Locator: `{pdf_name}` · página **{i}** / {len(pages)}")
        parts.append("")
        parts.append(body)
        parts.append("")

    return "\n".join(parts)


def write_raw_with_pages(raw_dir: Path, stem: str, raw_text: str) -> Path:
    """Persist raw text with explicit page markers for agent/debug."""
    pages = split_pdf_pages(raw_text)
    chunks = []
    for i, page in enumerate(pages, start=1):
        chunks.append(f"===== PDF PAGE {i} / {len(pages)} =====\n{page.rstrip()}\n")
    path = raw_dir / f"{stem}.txt"
    path.write_text("\n".join(chunks), encoding="utf-8")
    return path


def pdftotext_raw(pdf: Path) -> tuple[bool, str, str]:
    r = subprocess.run(
        ["pdftotext", "-layout", str(pdf), "-"],
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        return False, "", (r.stderr or "pdftotext failed").strip()
    return True, r.stdout or "", ""


def prepare(theme: Path, force: bool = False, lay: Layout | None = None) -> dict:
    lay = lay or layout(theme)
    root = lay.root
    rsl = lay.manifest_dir
    pdf_dir = lay.pdf_dir
    md_dir = lay.md_dir
    raw_dir = md_dir / "_raw"
    pdf_dir.mkdir(parents=True, exist_ok=True)
    md_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)

    manifest = load_manifest(rsl)
    entries: dict = manifest.setdefault("entries", {})
    needs_agent: list[str] = []
    skipped: list[str] = []
    converted: list[str] = []

    current_md = theme_md_files(theme) if lay.theme_md else []
    current_keys = {entry_key(str(md.relative_to(theme))) for md in current_md}
    for k in [k for k, v in entries.items() if v.get("method") == "theme-md" and k not in current_keys]:
        del entries[k]

    for md in current_md:
        rel = entry_key(str(md.relative_to(theme)))
        digest = sha256_file(md)
        prev = entries.get(rel)
        if (
            prev
            and prev.get("source_sha256") == digest
            and prev.get("status") in {"md_ready", "graphify_indexed"}
            and not force
        ):
            skipped.append(rel)
            continue
        entries[rel] = {
            "source": rel,
            "source_sha256": digest,
            "source_bytes": md.stat().st_size,
            "md": rel,
            "md_sha256": digest,
            "method": "theme-md",
            "status": "md_ready",
            "md_created_at": utc_now(),
            "graphify_indexed_at": prev.get("graphify_indexed_at") if prev else None,
            "notes": "theme markdown",
            "heading_count": count_md_headings(md.read_text(encoding="utf-8", errors="replace")),
        }
        converted.append(rel)

    for pdf in sorted(pdf_dir.glob("*.pdf")):
        rel = entry_key(f"{lay.pdf_prefix}{pdf.name}")
        digest = sha256_file(pdf)
        out_md = md_dir / f"{pdf.stem}.md"
        md_rel = entry_key(f"{lay.md_prefix}{out_md.name}")
        prev = entries.get(rel)

        unchanged = (
            prev
            and prev.get("source_sha256") == digest
            and prev.get("status") in {"md_ready", "graphify_indexed", "needs_agent"}
            and (root / prev.get("md", md_rel)).exists()
            and not force
        )
        if unchanged and prev.get("status") == "needs_agent":
            needs_agent.append(rel)
            skipped.append(rel)
            continue
        if unchanged and prev.get("status") in {"md_ready", "graphify_indexed"}:
            # Re-check heading density; poor structure must be rebuilt
            existing = (root / prev["md"]).read_text(encoding="utf-8", errors="replace")
            if count_md_headings(existing) >= MIN_HEADINGS_FOR_PAPER:
                skipped.append(rel)
                continue
            print(f"restructure: {rel} (too few headings)")

        ok, raw, err = pdftotext_raw(pdf)
        if not ok or not raw.strip():
            entries[rel] = {
                "source": rel,
                "source_sha256": digest,
                "source_bytes": pdf.stat().st_size,
                "md": md_rel,
                "md_sha256": None,
                "method": "pdftotext",
                "status": "needs_agent",
                "md_created_at": None,
                "graphify_indexed_at": None,
                "notes": f"pdftotext_failed: {err or 'empty'}",
                "heading_count": 0,
            }
            needs_agent.append(rel)
            converted.append(rel)
            print(f"needs_agent: {rel}")
            continue

        write_raw_with_pages(raw_dir, pdf.stem, raw)
        q_ok, q_note = quality_ok(raw)
        structured = structure_rag_md(stem=pdf.stem, pdf_name=pdf.name, raw_text=raw)
        out_md.write_text(structured, encoding="utf-8")
        headings = count_md_headings(structured)

        status = "md_ready" if q_ok and headings >= MIN_HEADINGS_FOR_PAPER else "needs_agent"
        notes = f"{q_note};headings:{headings}"
        if status == "needs_agent" and q_ok:
            notes += ";insufficient_structure"

        entries[rel] = {
            "source": rel,
            "source_sha256": digest,
            "source_bytes": pdf.stat().st_size,
            "md": md_rel,
            "md_sha256": sha256_file(out_md),
            "method": "pdftotext+structure",
            "status": status,
            "md_created_at": utc_now(),
            "graphify_indexed_at": None,
            "notes": notes,
            "heading_count": headings,
        }
        converted.append(rel)
        if status == "needs_agent":
            needs_agent.append(rel)
            print(f"needs_agent: {rel} [{notes}]")
        else:
            print(f"prepared: {rel} → {md_rel} [{notes}]")

    save_manifest(rsl, manifest)
    report = {
        "stage": "A_prepare",
        "theme": str(root),
        "converted": converted,
        "skipped": skipped,
        "needs_agent": needs_agent,
        "manifest": str(rsl / MANIFEST_NAME),
    }
    print(json.dumps({"prepare": report}, ensure_ascii=False, indent=2))
    return report


def stamp_agent_md(
    theme: Path, pdf_rel: str, method: str = "agent-rag", notes: str = "", lay: Layout | None = None
) -> None:
    lay = lay or layout(theme)
    rsl = lay.manifest_dir
    manifest = load_manifest(rsl)
    key = entry_key(pdf_rel)
    ent = manifest.setdefault("entries", {}).get(key)
    if not ent:
        print(f"error: no manifest entry for {key}", file=sys.stderr)
        sys.exit(1)
    md_path = lay.root / ent["md"]
    if not md_path.exists():
        print(f"error: MD missing: {md_path}", file=sys.stderr)
        sys.exit(1)
    text = md_path.read_text(encoding="utf-8", errors="replace")
    headings = count_md_headings(text)
    if headings < MIN_HEADINGS_FOR_PAPER:
        print(
            f"error: agent MD needs >= {MIN_HEADINGS_FOR_PAPER} markdown headings "
            f"(#{'/##'}), found {headings}",
            file=sys.stderr,
        )
        sys.exit(1)
    ent["md_sha256"] = sha256_file(md_path)
    ent["method"] = method
    ent["status"] = "md_ready"
    ent["md_created_at"] = utc_now()
    ent["graphify_indexed_at"] = None
    ent["heading_count"] = headings
    ent["notes"] = notes or "agent-rag enriched"
    save_manifest(rsl, manifest)
    print(f"stamped md_ready: {key} → {ent['md']} (headings={headings})")


def stamp_graphify(theme: Path, indexed_rels: list[str], lay: Layout | None = None) -> None:
    rsl = (lay or layout(theme)).manifest_dir
    manifest = load_manifest(rsl)
    entries = manifest.setdefault("entries", {})
    now = utc_now()
    for rel in indexed_rels:
        key = entry_key(rel)
        for k, v in list(entries.items()):
            if k == key or v.get("md") == key:
                if v.get("status") == "needs_agent":
                    continue
                v["status"] = "graphify_indexed"
                v["graphify_indexed_at"] = now
    save_manifest(rsl, manifest)


def build_graph(theme: Path, lay: Layout | None = None) -> dict:
    from graphify.analyze import god_nodes as find_gods, surprising_connections
    from graphify.build import build
    from graphify.cluster import cluster, score_all
    from graphify.export import to_json
    from graphify.extractors.markdown import extract_markdown
    from graphify.report import generate

    lay = lay or layout(theme)
    root = lay.root
    out = lay.out
    out.mkdir(parents=True, exist_ok=True)
    md_dir = lay.md_dir
    rsl = lay.manifest_dir
    manifest = load_manifest(rsl)
    entries = manifest.get("entries", {})

    md_files: list[Path] = []
    indexed_keys: list[str] = []

    for md in theme_md_files(theme) if lay.theme_md else []:
        rel = entry_key(str(md.relative_to(theme)))
        ent = entries.get(rel)
        if ent and ent.get("status") == "needs_agent":
            continue
        md_files.append(md)
        indexed_keys.append(rel)

    for md in sorted(md_dir.glob("*.md")):
        if md.name.startswith("_"):
            continue
        md_rel = entry_key(f"{lay.md_prefix}{md.name}")
        pdf_key = None
        pdf_ent = None
        for k, v in entries.items():
            if v.get("md") == md_rel:
                pdf_key, pdf_ent = k, v
                break
        if pdf_ent and pdf_ent.get("status") == "needs_agent":
            print(f"skip (needs_agent): {md_rel}")
            continue
        md_files.append(md)
        indexed_keys.append(pdf_key or md_rel)

    extractions = []
    per_file_nodes: dict[str, int] = {}
    for f in md_files:
        result = extract_markdown(f)
        if not result:
            continue
        n = len(result.get("nodes") or [])
        per_file_nodes[str(f.relative_to(root))] = n
        extractions.append(result)
        print(f"extracted: {f.relative_to(root)} → {n} nodes")

    if not extractions or not any(e.get("nodes") for e in extractions):
        print("error: no markdown nodes extracted", file=sys.stderr)
        sys.exit(1)

    G = build(extractions, directed=False, root=str(root))
    communities = cluster(G)
    cohesion = score_all(G, communities)
    labels = {i: f"Community {i}" for i in communities}
    gods = find_gods(G)
    surprises = surprising_connections(G)

    graph_path = out / "graph.json"
    if not to_json(G, communities, str(graph_path), force=True, community_labels=labels):
        print("error: to_json refused", file=sys.stderr)
        sys.exit(1)

    detection = {
        "files_by_type": {"document": [str(p) for p in md_files]},
        "total_files": len(md_files),
        "total_words": 0,
        "languages": {},
    }
    token_cost = {"input": 0, "output": 0, "total": 0, "model": "offline-ast"}
    try:
        report = generate(
            G, communities, cohesion, labels, gods, surprises, detection, token_cost, str(root)
        )
    except Exception as e:
        report = (
            f"# Graphify theme report\n\n"
            f"- Nodes: {G.number_of_nodes()}\n- Edges: {G.number_of_edges()}\n"
            f"- Fallback: {e}\n"
        )
    (out / "GRAPH_REPORT.md").write_text(report, encoding="utf-8")
    try:
        from graphify.exporters.html import to_html

        to_html(G, communities, str(out / "graph.html"), community_labels=labels)
    except Exception as e:
        print(f"warn: graph.html skipped: {e}", file=sys.stderr)

    stamp_graphify(theme, indexed_keys, lay)
    meta = {
        "stage": "C_build",
        "mode": "offline-markdown",
        "theme": str(root),
        "files": [str(p.relative_to(root)) for p in md_files],
        "nodes_per_file": per_file_nodes,
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "communities": len(communities),
        "manifest": str(rsl / MANIFEST_NAME),
        "graph": str(graph_path),
    }
    (out / "theme-build.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps({"build": meta}, ensure_ascii=False, indent=2))
    return meta


def _latest_picoc_md(theme: Path) -> Path | None:
    picoc_root = theme / "picoc"
    if not picoc_root.is_dir():
        return None
    candidates = sorted(
        (d for d in picoc_root.iterdir() if d.is_dir() and (d / "picoc.md").is_file()),
        key=lambda p: p.name,
        reverse=True,
    )
    return (candidates[0] / "picoc.md") if candidates else None


def _theme_query_checks_from_picoc(theme: Path) -> list[tuple[str, str]]:
    """Smoke-test queries from the latest picoc ## Keywords (theme-specific)."""
    picoc_md = _latest_picoc_md(theme)
    if not picoc_md:
        return []
    text = picoc_md.read_text(encoding="utf-8")
    block = re.search(
        r"## Keywords\s*\n+\|[^\n]+\n\|[-| :]+\n((?:\|[^\n]+\n)+)",
        text,
    )
    if not block:
        return []
    checks: list[tuple[str, str]] = []
    for line in block.group(1).strip().splitlines()[:3]:
        cells = [c.strip() for c in line.split("|") if c.strip()]
        if not cells:
            continue
        keyword = cells[0]
        hint = keyword.split()[0][:5].lower() if keyword.split() else keyword[:5].lower()
        checks.append((keyword, hint))
    return checks


def verify(theme: Path, lay: Layout | None = None) -> dict:
    """Quality gates — must pass before trusting theme memory."""
    lay = lay or layout(theme)
    rsl = lay.manifest_dir
    graph_path = lay.out / "graph.json"
    manifest = load_manifest(rsl)
    errors: list[str] = []
    warnings: list[str] = []

    if not graph_path.exists():
        errors.append("missing graphify-out/graph.json")
        result = {"ok": False, "errors": errors, "warnings": warnings}
        print(json.dumps({"verify": result}, indent=2))
        return result

    data = json.loads(graph_path.read_text(encoding="utf-8"))
    nodes = data.get("nodes") or []
    by_source: dict[str, list[dict]] = {}
    for n in nodes:
        sf = (n.get("source_file") or "").replace("\\", "/")
        # normalize to theme-relative if absolute-ish path fragment present
        if "RSL/MD/" in sf:
            sf = "RSL/MD/" + sf.split("RSL/MD/")[-1]
        elif sf.endswith("informe.md"):
            sf = "informe.md"
        elif sf.endswith("topic.md"):
            sf = "topic.md"
        by_source.setdefault(sf, []).append(n)

    entries = manifest.get("entries") or {}
    pdf_entries = {
        k: v for k, v in entries.items() if k.startswith(lay.pdf_prefix) and k.lower().endswith(".pdf")
    }

    if not lay.theme_md:
        pass
    elif "informe.md" not in by_source and not any(Path(theme, "informe.md").exists() for _ in [0]):
        warnings.append("informe.md not in theme folder")
    elif Path(theme, "informe.md").exists():
        # find any node from informe
        informe_nodes = [n for n in nodes if str(n.get("source_file", "")).endswith("informe.md")]
        if len(informe_nodes) < 3:
            errors.append(f"informe.md under-indexed ({len(informe_nodes)} nodes, want >= 3)")

    topic_nodes = [n for n in nodes if str(n.get("source_file", "")).endswith("topic.md")]
    if lay.theme_md and Path(theme, "topic.md").exists() and len(topic_nodes) < 3:
        errors.append(f"topic.md under-indexed ({len(topic_nodes)} nodes, want >= 3)")

    for key, ent in pdf_entries.items():
        status = ent.get("status")
        if status == "needs_agent":
            warnings.append(f"pending needs_agent: {key}")
            continue
        if status != "graphify_indexed":
            errors.append(f"{key} status={status}, expected graphify_indexed")
            continue
        md_rel = ent.get("md") or ""
        paper_nodes = [
            n
            for n in nodes
            if md_rel.endswith(Path(str(n.get("source_file", ""))).name)
            or str(n.get("source_file", "")).replace("\\", "/").endswith(md_rel)
            or f"{lay.md_prefix}{Path(md_rel).name}" in str(n.get("source_file", "")).replace("\\", "/")
        ]
        if len(paper_nodes) < MIN_NODES_PER_PAPER_SOURCE:
            errors.append(
                f"{key} only {len(paper_nodes)} graph nodes (want >= {MIN_NODES_PER_PAPER_SOURCE}). "
                "MD needs more ## headings / concept hooks."
            )

    # CLI query smoke tests
    query_checks = []
    stems = [Path(k).stem for k in pdf_entries if pdf_entries[k].get("status") == "graphify_indexed"]
    for stem in stems[:3]:
        parts = stem.split("-")
        token = parts[0]
        if len(parts) > 1 and re.fullmatch(r"R\d+", parts[0]):
            words = [p for p in parts[1:] if not p.isdigit()]
            token = max(words, key=len) if words else parts[0]
        query_checks.append((token, stem))
    if lay.theme_md:
        query_checks.extend(_theme_query_checks_from_picoc(theme))

    for q, expect_substr in query_checks:
        r = subprocess.run(
            [
                "graphify",
                "query",
                q,
                "--graph",
                str(graph_path),
                "--budget",
                "600",
            ],
            capture_output=True,
            text=True,
        )
        out = (r.stdout or "") + (r.stderr or "")
        hit = expect_substr.lower() in out.lower() or "nodes found" in out.lower()
        # stronger: must find >0 nodes
        m = re.search(r"(\d+) nodes found", out)
        count = int(m.group(1)) if m else 0
        if count < 1:
            errors.append(f"query failed / empty: {q!r} (expect hint {expect_substr!r})")
        else:
            print(f"query_ok: {q!r} → {count} nodes")

    if len(nodes) < 20:
        errors.append(f"graph too small: {len(nodes)} nodes")

    locator_nodes = [n for n in nodes if "[PDF p." in str(n.get("label", ""))]
    if pdf_entries and len(locator_nodes) < 5:
        errors.append(
            f"missing page locators in graph ({len(locator_nodes)} nodes with '[PDF p.'] — "
            "MD structure step may have failed"
        )
    else:
        print(f"locator_ok: {len(locator_nodes)} nodes with [PDF p.N] labels")

    # smoke: query a page locator style label
    r = subprocess.run(
        ["graphify", "query", "PDF p.1", "--graph", str(graph_path), "--budget", "400"],
        capture_output=True,
        text=True,
    )
    out = (r.stdout or "") + (r.stderr or "")
    m = re.search(r"(\d+) nodes found", out)
    if not m or int(m.group(1)) < 1:
        errors.append("query 'PDF p.1' returned no locator nodes")
    else:
        print(f"query_ok: 'PDF p.1' → {m.group(1)} nodes")

    result = {
        "stage": "D_verify",
        "ok": not errors,
        "nodes": len(nodes),
        "errors": errors,
        "warnings": warnings,
        "graph": str(graph_path),
        "manifest": str(rsl / MANIFEST_NAME),
    }
    print(json.dumps({"verify": result}, ensure_ascii=False, indent=2))
    return result


def main() -> None:
    ap = argparse.ArgumentParser(description="Theme Graphify pipeline")
    ap.add_argument("theme")
    ap.add_argument("--prepare-only", action="store_true")
    ap.add_argument("--build-only", action="store_true")
    ap.add_argument("--verify-only", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--stamp-agent", metavar="PDF_REL")
    ap.add_argument("--stamp-notes", default="")
    ap.add_argument("--corpus", metavar="DIR", help="PDF corpus folder (MD, manifest and graph live inside)")
    args = ap.parse_args()
    theme = Path(args.theme).resolve()
    if not theme.is_dir():
        print(f"error: not a directory: {theme}", file=sys.stderr)
        sys.exit(1)
    corpus = Path(args.corpus).resolve() if args.corpus else None
    if corpus is not None and not corpus.is_dir():
        print(f"error: not a directory: {corpus}", file=sys.stderr)
        sys.exit(1)
    lay = layout(theme, corpus)

    if args.stamp_agent:
        stamp_agent_md(theme, args.stamp_agent, notes=args.stamp_notes, lay=lay)
        return

    if args.verify_only:
        ok = verify(theme, lay)["ok"]
        sys.exit(0 if ok else 1)

    if args.build_only:
        build_graph(theme, lay)
        ok = verify(theme, lay)["ok"]
        sys.exit(0 if ok else 1)

    prep = prepare(theme, force=args.force, lay=lay)
    if args.prepare_only:
        sys.exit(2 if prep.get("needs_agent") else 0)

    if prep.get("needs_agent"):
        print(
            "error: unresolved needs_agent — run graphify-theme skill RAG step first:\n"
            + "\n".join(f"  - {x}" for x in prep["needs_agent"]),
            file=sys.stderr,
        )
        sys.exit(2)

    build_graph(theme, lay)
    ok = verify(theme, lay)["ok"]
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
