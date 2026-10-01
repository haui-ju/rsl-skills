#!/usr/bin/env python3
"""Cribado 2 de PRISMA 2020 (texto completo): descarga de los SI y memoria Graphify del corpus.

Entrada: resultados-<MARCO>-cribado-1.csv de la última versión del picoc (lo escribe rsl-cribado-1-aplicar).
Corpus: docs/<slug>/RSL/picoc/<fecha>-cribado-2-<MARCO>/  (documentos.json/md, docs/pdf, docs/pdf-draft, docs/md, memoria-traza.json, graphify-out/).

Uso:
  cribado2.py init     docs/<slug>             # carpetas + documentos.json/md (orden del CSV de SI)
  cribado2.py download docs/<slug>             # descarga OA → docs/pdf/<Id>-<titulo-slug>.pdf
  cribado2.py align    docs/<slug>             # mueve docs/pdf-draft/ → docs/pdf/ por título
  cribado2.py documentos docs/<slug>           # regenera documentos.md desde documentos.json
  cribado2.py prepare  docs/<slug>             # PDF → MD con localizadores de página (exit 2 si queda needs_agent)
  cribado2.py stamp    docs/<slug> <pdf>       # marca como listo el MD que escribió el agente para ese PDF
  cribado2.py build    docs/<slug>             # grafo Graphify del corpus + controles de calidad
  cribado2.py status   docs/<slug>             # valida sin reconstruir (manifest al día + controles)
  cribado2.py query    docs/<slug> "<pregunta>"

Solo fuentes de acceso abierto: Unpaywall, OpenAlex, Semantic Scholar (arXiv, PMC) y la meta
citation_pdf_url de la página del DOI. Lo que no se consigue queda en descargas.md para descarga manual:
los PDF manuales van a `docs/pdf-draft/` con un nombre parecido al título; `align` los mueve al nombre canónico.
"""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import html
import importlib.util
import json
import os
import re
import subprocess
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import picoc_versions as pv  # noqa: E402
from cribado2_config import (  # noqa: E402
    empty_retrieval_message,
    filter_si_for_retrieval,
    normalize_use,
    read_cribado2_use,
)
from rsl_out import Fail, error, ok, run  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
COL_OK = "¿Se acepta?"
COL_WHY = "Justificación cribado 1"
CRIBADO1_SHADOW = "cribado-1.shadow.jsonl"
DOCUMENTOS_JSON = "documentos.json"
DOCUMENTOS_MD = "documentos.md"
MEMORIA_TRAZA = "memoria-traza.json"
PORQUE_MAX = 120
TITLE_SLUG_MAX = 80
MIN_PDF_BYTES = 10_000
MAX_PDF_BYTES = 80_000_000
TIMEOUT = 30
WORKERS = 6
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
DOI_PREFIX = re.compile(r"^(https?://(dx\.)?doi\.org/|doi:\s*)", re.I)
META_PDF = re.compile(
    r"<meta[^>]+(?:name|property)=[\"']citation_pdf_url[\"'][^>]*content=[\"']([^\"']+)[\"']"
    r"|<meta[^>]+content=[\"']([^\"']+)[\"'][^>]*(?:name|property)=[\"']citation_pdf_url[\"']",
    re.I,
)
USAGE = (
    "uso: cribado2.py init|download|align|prepare|build|status docs/<slug> "
    "· stamp docs/<slug> <pdf> · query docs/<slug> \"<pregunta>\""
)


def rel(p: Path) -> str:
    try:
        return str(p.resolve().relative_to(ROOT))
    except ValueError:
        return str(p)


def theme_dir(arg: str) -> Path:
    t = Path(arg)
    t = t if t.is_absolute() else Path.cwd() / t
    if not t.is_dir():
        raise Fail(f"{arg} no es la carpeta de un tema", "usa docs/<slug>")
    return t.resolve()


def picoc_folder(theme: Path) -> Path:
    f = pv.latest_file(theme)
    if f is None:
        raise Fail(f"{rel(theme)} no tiene picoc/<fecha>-<MARCO>/picoc.md", f"créalo con: Usa rsl-picoc sobre {rel(theme)}/")
    return f.parent


def cribado2_dir_name(picoc_folder_name: str) -> str:
    m = pv.PICOC_DIR_RE.match(picoc_folder_name)
    if not m:
        return f"{picoc_folder_name}-cribado-2"
    date, rev, marco = m.group(1), m.group(2), m.group(3)
    prefix = f"{date}-{rev}" if rev else date
    return f"{prefix}-cribado-2-{marco}"


def cribado2_dir(theme: Path) -> Path:
    folder = picoc_folder(theme)
    return theme / "RSL" / "picoc" / cribado2_dir_name(folder.name)


def cribado_paths(corpus: Path) -> tuple[Path, Path, Path]:
    pdf = corpus / "docs" / "pdf"
    md = corpus / "docs" / "md"
    draft = corpus / "docs" / "pdf-draft"
    return pdf, md, draft


def ensure_cribado_dirs(corpus: Path) -> tuple[Path, Path, Path]:
    pdf, md, draft = cribado_paths(corpus)
    pdf.mkdir(parents=True, exist_ok=True)
    md.mkdir(parents=True, exist_ok=True)
    (md / "_raw").mkdir(parents=True, exist_ok=True)
    draft.mkdir(parents=True, exist_ok=True)
    return pdf, md, draft


def screening_csv(folder: Path) -> Path:
    name = f"resultados-{pv.dir_marco(folder) or 'MARCO'}-cribado-1.csv"
    p = folder / name
    if not p.is_file():
        raise Fail(f"falta picoc/{folder.name}/{name}", f"corre primero: Usa rsl-cribado-1-aplicar sobre {rel(folder.parent.parent)}/")
    return p


def norm_doi(s: str) -> str:
    return DOI_PREFIX.sub("", (s or "").strip()).strip().rstrip(".").lower()


def slug(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def first_author(authors: str) -> str:
    first = re.split(r"[;|]", authors or "")[0].strip()
    last = re.split(r"[,\s]", first)[0] if first else ""
    return slug(last)[:30] or "anon"


def title_slug(titulo: str) -> str:
    return slug(titulo or "sin-titulo")[:TITLE_SLUG_MAX] or "sin-titulo"


def pdf_basename(rec: dict) -> str:
    return f"{rec['Id']}-{title_slug(rec.get('Título') or '')}.pdf"


def pdf_rel(rec: dict) -> str:
    return f"docs/pdf/{pdf_basename(rec)}"


def load_si(csv_path: Path) -> list[dict]:
    with csv_path.open(encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    if not rows or COL_OK not in rows[0]:
        raise Fail(f"{csv_path.name} no tiene la columna «{COL_OK}»", "vuelve a correr rsl-cribado-1-aplicar")
    return [r for r in rows if (r.get(COL_OK) or "").strip().upper() == "SI"]


def load_si_for_retrieval(theme: Path, folder: Path, csv_path: Path) -> tuple[list[dict], list[dict], str]:
    si_all = load_si(csv_path)
    if not si_all:
        raise Fail(f"{csv_path.name} no tiene registros SI", "aplica el cribado 1 antes del cribado 2")
    use = read_cribado2_use(theme)
    dmap = duda_from_shadow(folder)
    si = filter_si_for_retrieval(si_all, dmap, use)
    if not si:
        raise Fail(
            f"cribado_2.use={use} no deja registros para retrieval",
            f"{empty_retrieval_message(use, len(si_all))}; cambia cribado_2.use en config.yml",
        )
    return si, si_all, use


def set_retrieval_meta(cat: dict, use: str, si_total: int, si_retrieval: int) -> None:
    cat["cribado_2_use"] = use
    cat["si_total"] = si_total
    cat["si_retrieval"] = si_retrieval


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def is_pdf(path: Path) -> bool:
    if not path.is_file() or path.stat().st_size < MIN_PDF_BYTES:
        return False
    with path.open("rb") as f:
        return f.read(1024).lstrip().startswith(b"%PDF")


# --- HTTP --------------------------------------------------------------------

def mail() -> str:
    m = os.environ.get("UNPAYWALL_EMAIL", "").strip()
    if not m:
        r = subprocess.run(["git", "config", "user.email"], capture_output=True, text=True, cwd=ROOT)
        m = r.stdout.strip()
    return m or "rsl-skills@example.org"


def fetch(url: str, accept: str = "*/*") -> tuple[bytes, str, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        data = r.read(MAX_PDF_BYTES + 1)
        return data, r.headers.get("Content-Type", ""), r.geturl()


def get_json(url: str) -> dict | None:
    try:
        data, _, _ = fetch(url, "application/json")
        return json.loads(data.decode("utf-8", "replace"))
    except (urllib.error.URLError, TimeoutError, ValueError, OSError):
        return None


def candidates(doi: str, email: str) -> tuple[list[tuple[str, str]], dict]:
    """(URLs candidatas en orden, metadatos: is_oa y editor según Unpaywall/OpenAlex)."""
    q = urllib.parse.quote(doi, safe="/")
    out: list[tuple[str, str]] = []
    meta = {"is_oa": None, "editor": None}
    u = get_json(f"https://api.unpaywall.org/v2/{q}?email={urllib.parse.quote(email)}")
    if u:
        meta["is_oa"], meta["editor"] = u.get("is_oa"), u.get("publisher")
        locs = ([u.get("best_oa_location")] if u.get("best_oa_location") else []) + (u.get("oa_locations") or [])
        out += [("unpaywall", l["url_for_pdf"]) for l in locs if l and l.get("url_for_pdf")]
        out += [("unpaywall-landing", l["url"]) for l in locs if l and l.get("url")]
    o = get_json(f"https://api.openalex.org/works/https://doi.org/{q}?mailto={urllib.parse.quote(email)}")
    if o:
        if meta["is_oa"] is None:
            meta["is_oa"] = (o.get("open_access") or {}).get("is_oa")
        locs = ([o.get("best_oa_location")] if o.get("best_oa_location") else []) + (o.get("locations") or [])
        out += [("openalex", l["pdf_url"]) for l in locs if l and l.get("pdf_url") and l.get("is_oa", True)]
        if (o.get("open_access") or {}).get("oa_url"):
            out.append(("openalex-landing", o["open_access"]["oa_url"]))
    s = get_json(f"https://api.semanticscholar.org/graph/v1/paper/DOI:{q}?fields=openAccessPdf,externalIds")
    if s:
        if (s.get("openAccessPdf") or {}).get("url"):
            out.append(("semanticscholar", s["openAccessPdf"]["url"]))
        ext = s.get("externalIds") or {}
        if ext.get("ArXiv"):
            out.append(("arxiv", f"https://arxiv.org/pdf/{ext['ArXiv']}"))
        if ext.get("PubMedCentral"):
            out.append(("pmc", f"https://europepmc.org/articles/PMC{ext['PubMedCentral']}?pdf=render"))
    out.append(("doi-landing", f"https://doi.org/{q}"))
    seen, uniq = set(), []
    for src, url in out:
        if url and url not in seen:
            seen.add(url)
            uniq.append((src, url))
    return uniq, meta


PDF_SOURCES = {"unpaywall", "openalex", "semanticscholar", "arxiv", "pmc"}
PUBLISHERS = {"10.1145": "ACM", "10.1109": "IEEE", "10.3390": "MDPI", "10.1007": "Springer", "10.1016": "Elsevier",
              "10.1111": "Wiley", "10.1002": "Wiley", "10.4018": "IGI Global", "10.1080": "Taylor & Francis",
              "10.1177": "SAGE", "10.3389": "Frontiers", "10.1371": "PLOS", "10.2196": "JMIR"}


def editor_of(doi: str, meta: dict) -> str:
    return PUBLISHERS.get(doi.split("/")[0]) or meta.get("editor") or "desconocido"


def host(url: str) -> str:
    return urllib.parse.urlparse(url).netloc.removeprefix("www.") or url


def site(url: str, editor: str) -> str:
    h = host(url)
    return f"la página del editor ({editor})" if h in {"doi.org", "dx.doi.org"} else h


def sites(ts: list[dict], editor: str) -> str:
    return ", ".join(sorted({site(t["url"], editor) for t in ts}))


def why_missing(doi: str, tries: list[dict], meta: dict) -> tuple[str, str]:
    """(motivo en español para el usuario, enlace donde bajarlo a mano)."""
    editor = editor_of(doi, meta)
    oa = [t for t in tries if t["fuente"] != "doi-landing"]
    blocked = [t for t in oa if t["resultado"] in {"HTTP 401", "HTTP 403", "HTTP 429"}]
    slow = [t for t in oa if "Timeout" in t["resultado"] or "URLError" in t["resultado"]]
    html_only = [t for t in oa if t["resultado"].startswith("no es PDF")]
    non_doi = [t for t in oa if "doi.org" not in t["url"]]
    pool = non_doi or oa
    pdfs = [t for t in pool if t["fuente"] in PDF_SOURCES]
    link = (pdfs or pool or [{"url": f"https://doi.org/{doi}"}])[0]["url"]
    if not oa:
        if meta.get("is_oa"):
            return ("Figura como acceso abierto, pero ninguna base (Unpaywall, OpenAlex, Semantic Scholar) da un enlace "
                    "al PDF: bájalo desde la página del editor.", link)
        return ("No tiene versión de acceso abierto registrada en Unpaywall, OpenAlex ni Semantic Scholar: es de pago; "
                "necesitas acceso institucional o pedírselo al autor.", link)
    def verb(ts: list[dict], one: str, many: str) -> str:
        return many if len({site(t["url"], editor) for t in ts}) > 1 else one

    parts = []
    if blocked:
        parts.append(f"{sites(blocked, editor)} {verb(blocked, 'bloquea', 'bloquean')} las descargas automáticas "
                     "(HTTP 403, protección contra bots)")
    if html_only:
        parts.append(f"{sites(html_only, editor)} {verb(html_only, 'muestra', 'muestran')} una página web sin enlace "
                     "directo al PDF que el script pueda leer")
    if slow:
        parts.append(f"{sites(slow, editor)} no {verb(slow, 'respondió', 'respondieron')} a tiempo")
    if not parts:
        parts.append("los enlaces abiertos no devolvieron un PDF válido (" + "; ".join(sorted({t["resultado"] for t in oa})) + ")")
    return "Hay versión abierta, pero " + "; y ".join(parts) + ": ábrela en el navegador y guarda el PDF.", link


def try_download(url: str, dest: Path, follow_meta: bool = True) -> tuple[bool, str]:
    try:
        data, ctype, final = fetch(url, "application/pdf,text/html;q=0.9,*/*;q=0.8")
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as e:
        return False, f"{type(e).__name__}"
    if data.lstrip()[:5].startswith(b"%PDF"):
        if len(data) < MIN_PDF_BYTES or len(data) > MAX_PDF_BYTES:
            return False, f"tamaño {len(data)}"
        tmp = dest.with_suffix(".part")
        tmp.write_bytes(data)
        tmp.replace(dest)
        return True, final
    if follow_meta and "html" in ctype.lower():
        m = META_PDF.search(data.decode("utf-8", "replace"))
        if m:
            pdf_url = urllib.parse.urljoin(final, html.unescape(m.group(1) or m.group(2)))
            return try_download(pdf_url, dest, follow_meta=False)
    return False, f"no es PDF ({ctype.split(';')[0] or 'sin tipo'})"


def existing_pdf(pdf_dir: Path, rid: str) -> Path | None:
    for p in sorted(pdf_dir.glob(f"{rid}-*.pdf")) + sorted(pdf_dir.glob(f"{rid}.pdf")):
        if is_pdf(p):
            return p
    return None


def duda_from_shadow(picoc_dir: Path) -> dict[str, bool]:
    sh = picoc_dir / CRIBADO1_SHADOW
    if not sh.is_file():
        return {}
    out: dict[str, bool] = {}
    for line in sh.read_text(encoding="utf-8").splitlines()[1:]:
        if not line.strip():
            continue
        try:
            r = json.loads(line)
            out[r["id"]] = bool(r.get("duda"))
        except (json.JSONDecodeError, KeyError):
            continue
    return out


def row_duda(row: dict, dmap: dict[str, bool]) -> bool:
    rid = row.get("Id") or ""
    if rid in dmap:
        return dmap[rid]
    return (row.get(COL_WHY) or "").startswith("Duda:")


def registro_base(orden: int, row: dict, dmap: dict[str, bool]) -> dict:
    return {
        "orden": orden,
        "id": row["Id"],
        "titulo": (row.get("Título") or "").strip(),
        "doi": norm_doi(row.get("DOI", "")),
        "descargado": "no",
        "porque": "",
        "pdf": None,
        "fuente": None,
        "url": None,
        "enlace_manual": None,
        "sha256": None,
        "bytes": None,
        "intentos": [],
        "duda": row_duda(row, dmap),
    }


def sync_registro_pdf(reg: dict, pdf_dir: Path) -> bool:
    """Si ya hay PDF en docs/pdf, marca descargado."""
    found = existing_pdf(pdf_dir, reg["id"])
    if not found:
        return False
    rel = f"docs/pdf/{found.name}"
    reg["descargado"] = "si"
    reg["porque"] = ""
    reg["pdf"] = rel
    if not reg.get("fuente"):
        reg["fuente"] = "existente"
    reg["sha256"] = sha256(found)
    reg["bytes"] = found.stat().st_size
    return True


def download_one(reg: dict, pdf_dir: Path, email: str) -> None:
    row = {"Id": reg["id"], "Título": reg["titulo"], "DOI": reg["doi"]}
    dest = pdf_dir / pdf_basename(row)
    doi = reg["doi"]
    if not doi:
        reg["porque"] = "Sin DOI: búscalo por título."
        return
    tries: list[dict] = []
    urls, meta = candidates(doi, email)
    for src, url in urls:
        good, info = try_download(url, dest)
        if good:
            reg["pdf"] = f"docs/pdf/{dest.name}"
            reg["descargado"] = "si"
            reg["porque"] = ""
            reg["fuente"] = src
            reg["url"] = info
            reg["sha256"] = sha256(dest)
            reg["bytes"] = dest.stat().st_size
            reg["intentos"] = tries
            return
        tries.append({"fuente": src, "url": url, "resultado": info})
    motivo, link = why_missing(doi, tries, meta)
    reg["descargado"] = "no"
    reg["porque"] = md_cell(motivo, PORQUE_MAX)
    reg["pdf"] = None
    reg["fuente"] = None
    reg["url"] = None
    reg["enlace_manual"] = link
    reg["intentos"] = tries


def best_download_url(reg: dict) -> str | None:
    """Mejor URL para abrir o descargar el PDF a mano (o la del PDF ya bajado)."""
    url = reg.get("url")
    if url:
        return url
    link = reg.get("enlace_manual")
    if link:
        return link
    doi = reg.get("doi") or ""
    tries = reg.get("intentos") or []
    oa = [t for t in tries if t.get("fuente") != "doi-landing"]
    if not oa and not doi:
        return None
    non_doi = [t for t in oa if "doi.org" not in (t.get("url") or "")]
    pool = non_doi or oa
    pdfs = [t for t in pool if t.get("fuente") in PDF_SOURCES]
    return (pdfs or pool or [{"url": f"https://doi.org/{doi}"}])[0]["url"]


def enlaces_markdown(reg: dict) -> str:
    parts: list[str] = []
    doi = reg.get("doi")
    if doi:
        parts.append(f"[DOI](https://doi.org/{doi})")
    dl = best_download_url(reg)
    if dl:
        doi_url = f"https://doi.org/{doi}" if doi else ""
        label = "PDF" if reg.get("descargado") == "si" else "descargar"
        if dl != doi_url or reg.get("descargado") == "si":
            parts.append(f"[{label}]({dl})")
    return " · ".join(parts) if parts else "—"


def md_cell(s: str, n: int = 90) -> str:
    s = " ".join((s or "").split()).replace("|", "/")
    return s if len(s) <= n else s[: n - 1] + "…"


def load_catalog(corpus: Path) -> dict:
    p = corpus / DOCUMENTOS_JSON
    if not p.is_file():
        theme = corpus.parent.parent.parent
        raise Fail(f"falta {rel(p)}", f"corre pnpm -s cribado2:init {rel(theme)}/")
    return json.loads(p.read_text(encoding="utf-8"))


def save_catalog(corpus: Path, cat: dict) -> None:
    (corpus / DOCUMENTOS_JSON).write_text(json.dumps(cat, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_documentos_md(corpus: Path, cat: dict) -> Path:
    lines = [
        "# Documentos — cribado 2",
        "",
        f"<!-- cribado2:documentos picoc={Path(cat['picoc']).parent.name} -->",
        "",
        f"Picoc: `{cat['picoc']}` · CSV: `{cat['csv_cribado_1']}` · Marco: **{cat.get('marco', '—')}**",
        "",
        "| # | id | titulo | enlaces | descargado | porque |",
        "|---:|---|---|---|---|---|",
    ]
    for r in sorted(cat["registros"], key=lambda x: x["orden"]):
        lines.append(
            f"| {r['orden']} | {r['id']} | {md_cell(r['titulo'], 60)} | {enlaces_markdown(r)} | {r['descargado']} | {md_cell(r.get('porque') or '', PORQUE_MAX)} |"
        )
    lines.append("")
    dest = corpus / DOCUMENTOS_MD
    dest.write_text("\n".join(lines), encoding="utf-8")
    return dest


def build_catalog(
    theme: Path,
    folder: Path,
    csv_path: Path,
    si: list[dict],
    use: str,
    si_total: int,
) -> dict:
    dmap = duda_from_shadow(folder)
    cat = {
        "picoc": rel(folder / "picoc.md"),
        "csv_cribado_1": rel(csv_path),
        "marco": pv.dir_marco(folder) or "MARCO",
        "carpeta": rel(cribado2_dir(theme)),
        "generado": dt.datetime.now().isoformat(timespec="seconds"),
        "registros": [registro_base(i, r, dmap) for i, r in enumerate(si, 1)],
    }
    set_retrieval_meta(cat, use, si_total, len(si))
    return cat


def prisma_counts(cat: dict) -> tuple[int, int]:
    regs = cat["registros"]
    got = sum(1 for r in regs if r.get("descargado") == "si")
    return len(regs), len(regs) - got


def update_prisma(folder: Path, sought: int, missing: int) -> bool:
    p = folder / "prisma.json"
    if not p.is_file():
        return False
    data = json.loads(p.read_text(encoding="utf-8"))
    ret = data.setdefault("retrieval", {})
    ret["sought"], ret["not_retrieved"] = sought, missing
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return True


def merge_catalog_si(
    theme: Path,
    folder: Path,
    csv_path: Path,
    si: list[dict],
    cat: dict | None,
    use: str,
    si_total: int,
) -> dict:
    dmap = duda_from_shadow(folder)
    if cat is None:
        return build_catalog(theme, folder, csv_path, si, use, si_total)
    by_id = {r["id"]: r for r in cat.get("registros", [])}
    regs: list[dict] = []
    for i, row in enumerate(si, 1):
        rid = row["Id"]
        if rid in by_id:
            r = by_id[rid]
            r["orden"] = i
            r["titulo"] = (row.get("Título") or "").strip()
            r["doi"] = norm_doi(row.get("DOI", ""))
            r["duda"] = row_duda(row, dmap)
        else:
            r = registro_base(i, row, dmap)
        regs.append(r)
    cat["registros"] = regs
    cat["csv_cribado_1"] = rel(csv_path)
    cat["picoc"] = rel(folder / "picoc.md")
    cat["marco"] = pv.dir_marco(folder) or "MARCO"
    cat["carpeta"] = rel(cribado2_dir(theme))
    set_retrieval_meta(cat, use, si_total, len(si))
    return cat


def cmd_init(theme: Path) -> int:
    folder = picoc_folder(theme)
    csv_path = screening_csv(folder)
    si, si_all, use = load_si_for_retrieval(theme, folder, csv_path)
    corpus = cribado2_dir(theme)
    ensure_cribado_dirs(corpus)
    jpath = corpus / DOCUMENTOS_JSON
    prev = json.loads(jpath.read_text(encoding="utf-8")) if jpath.is_file() else None
    cat = merge_catalog_si(theme, folder, csv_path, si, prev, use, len(si_all))
    cat["generado"] = dt.datetime.now().isoformat(timespec="seconds")
    save_catalog(corpus, cat)
    report = write_documentos_md(corpus, cat)
    return ok(
        f"carpeta {rel(corpus)}/ con {len(si)} SI para retrieval (cribado_2.use={use}; {len(si_all)} SI en CSV) en {rel(report)}",
        f"pnpm -s cribado2:download {rel(theme)}",
    )


def process_download_reg(reg: dict, pdf_dir: Path, email: str) -> dict:
    if reg.get("descargado") == "si":
        sync_registro_pdf(reg, pdf_dir)
        return reg
    if sync_registro_pdf(reg, pdf_dir):
        return reg
    download_one(reg, pdf_dir, email)
    return reg


def cmd_download(theme: Path) -> int:
    folder = picoc_folder(theme)
    corpus = cribado2_dir(theme)
    if not (corpus / DOCUMENTOS_JSON).is_file():
        cmd_init(theme)
    cat = load_catalog(corpus)
    use = read_cribado2_use(theme)
    prev_use = cat.get("cribado_2_use")
    if prev_use and normalize_use(str(prev_use)) != use:
        print(
            f"WARN cribado_2.use cambió ({prev_use} → {use}); "
            f"corre pnpm -s cribado2:init {rel(theme)}/ antes de confiar en el catálogo"
        )
    pdf_dir, _, _ = ensure_cribado_dirs(corpus)
    email = mail()
    with ThreadPoolExecutor(WORKERS) as ex:
        regs = list(ex.map(lambda r: process_download_reg(r, pdf_dir, email), cat["registros"]))
    cat["registros"] = regs
    for r in regs:
        mark = "OK" if r["descargado"] == "si" else "FALTA"
        why = f" ({r['fuente']})" if r.get("fuente") else (f" — {r['porque']}" if r.get("porque") else "")
        print(f"  - {r['id']} {mark}: {r.get('pdf') or pdf_rel({'Id': r['id'], 'Título': r['titulo']})}{why}")
    si_ids = {r["id"] for r in regs}
    for p in sorted(pdf_dir.glob("*.pdf")):
        rid = p.name.split("-")[0]
        if rid not in si_ids:
            print(f"WARN {p.name} no corresponde a un SI del cribado 1")
    save_catalog(corpus, cat)
    report = write_documentos_md(corpus, cat)
    sought, miss = prisma_counts(cat)
    if not update_prisma(folder, sought, miss):
        print(f"WARN picoc/{folder.name}/prisma.json no existe; no se actualizó retrieval.not_retrieved")
    got = sought - miss
    man = sum(1 for r in regs if r.get("descargado") == "si" and r.get("fuente") in {"manual", "alineamiento", "existente"})
    nxt = ""
    if miss:
        nxt = (
            f"deja PDF en {rel(corpus)}/docs/pdf-draft/ con nombre parecido al título y corre "
            f"pnpm -s cribado2:align {rel(theme)}, o revisa {rel(report)}; "
        )
    nxt += f"Usa rsl-cribado-2-memoria sobre {rel(theme)}/"
    return ok(
        f"{got} de {sought} PDF en {rel(corpus)}/docs/pdf/ ({man} manuales/alineados, {miss} no recuperados); tabla en {rel(report)}",
        nxt,
    )


def draft_matches_reg(draft_stem: str, reg: dict) -> bool:
    stem = draft_stem.strip()
    rid = (reg.get("id") or "").strip()
    if rid and stem.upper() == rid.upper():
        return True
    key = slug(draft_stem)
    tkey = title_slug(reg["titulo"])
    if key == tkey:
        return True
    doi_in_name = norm_doi(draft_stem)
    if doi_in_name and reg.get("doi") and doi_in_name == reg["doi"]:
        return True
    if len(key) >= 12 and (key in tkey or tkey in key):
        return True
    return False


def cmd_documentos(theme: Path) -> int:
    corpus = cribado2_dir(theme)
    cat = load_catalog(corpus)
    report = write_documentos_md(corpus, cat)
    return ok(f"tabla actualizada en {rel(report)}")


def cmd_align(theme: Path) -> int:
    corpus = cribado2_dir(theme)
    cat = load_catalog(corpus)
    pdf_dir, _, draft_dir = ensure_cribado_dirs(corpus)
    aligned, ambiguous, nomatch = 0, [], []
    for draft in sorted(draft_dir.glob("*.pdf")):
        if not is_pdf(draft):
            print(f"WARN {draft.name} no es un PDF válido (se deja en pdf-draft)")
            continue
        candidates = [r for r in cat["registros"] if r.get("descargado") != "si" and draft_matches_reg(draft.stem, r)]
        if len(candidates) != 1:
            if len(candidates) > 1:
                ambiguous.append((draft.name, [c["id"] for c in candidates]))
            else:
                nomatch.append(draft.name)
            continue
        reg = candidates[0]
        dest = pdf_dir / pdf_basename({"Id": reg["id"], "Título": reg["titulo"]})
        draft_name = draft.name
        if dest.exists() and sha256(dest) != sha256(draft):
            print(f"WARN {draft_name}: ya existe {dest.name} con otro contenido")
            continue
        draft.rename(dest)
        reg["descargado"] = "si"
        reg["porque"] = ""
        reg["pdf"] = f"docs/pdf/{dest.name}"
        reg["fuente"] = "alineamiento"
        reg["url"] = None
        reg["sha256"] = sha256(dest)
        reg["bytes"] = dest.stat().st_size
        aligned += 1
        print(f"  - {reg['id']} ← {draft_name} → {dest.name}")
    save_catalog(corpus, cat)
    write_documentos_md(corpus, cat)
    folder = picoc_folder(theme)
    sought, miss = prisma_counts(cat)
    update_prisma(folder, sought, miss)
    for name, ids in ambiguous:
        print(f"WARN {name}: varios candidatos ({', '.join(ids)})")
    for name in nomatch:
        print(f"WARN {name}: sin registro pendiente que coincida por título")
    return ok(
        f"{aligned} PDF alineados desde pdf-draft ({miss} siguen sin PDF)",
        f"pnpm -s cribado2:align {rel(theme)} tras cada tanda, o pnpm -s cribado2:download {rel(theme)}",
    )


# --- memoria (Graphify del corpus) -------------------------------------------

def offline():
    spec = importlib.util.spec_from_file_location("graphify_theme_offline", ROOT / "scripts" / "graphify-theme-offline.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def corpus_or_fail(theme: Path) -> Path:
    corpus = cribado2_dir(theme)
    pdf_dir, _, _ = cribado_paths(corpus)
    if not pdf_dir.is_dir() or not any(pdf_dir.glob("*.pdf")):
        raise Fail(f"{rel(pdf_dir)}/ no tiene PDF", f"corre primero: Usa rsl-cribado-2 sobre {rel(theme)}/")
    return corpus


def pdf_manifest_key(lay, pdf_name: str) -> str:
    return f"{lay.pdf_prefix}{pdf_name}".replace("\\", "/")


def pending(corpus: Path, lay) -> tuple[list[str], list[str]]:
    """(needs_agent, PDF sin manifest o con sha distinto)."""
    mpath = lay.manifest_dir / "index-manifest.json"
    entries = json.loads(mpath.read_text(encoding="utf-8")).get("entries", {}) if mpath.is_file() else {}
    agent = sorted(k for k, v in entries.items() if v.get("status") == "needs_agent")
    stale = []
    for pdf in sorted(lay.pdf_dir.glob("*.pdf")):
        key = pdf_manifest_key(lay, pdf.name)
        ent = entries.get(key)
        if not ent or ent.get("source_sha256") != sha256(pdf):
            stale.append(pdf.name)
    return agent, stale


def write_memoria_traza(corpus: Path, lay, meta: dict) -> None:
    cat = load_catalog(corpus) if (corpus / DOCUMENTOS_JSON).is_file() else {"registros": []}
    mpath = lay.manifest_dir / "index-manifest.json"
    entries = json.loads(mpath.read_text(encoding="utf-8")).get("entries", {}) if mpath.is_file() else {}
    ids: dict = {}
    for reg in cat.get("registros", []):
        pdf_name = Path(reg.get("pdf") or "").name
        key = pdf_manifest_key(lay, pdf_name) if pdf_name else None
        ent = entries.get(key) if key else None
        ids[reg["id"]] = {
            "pdf": reg.get("pdf"),
            "md": ent.get("md") if ent else None,
            "status": ent.get("status") if ent else ("pendiente" if reg.get("descargado") != "si" else "sin_md"),
            "updated_at": dt.datetime.now().isoformat(timespec="seconds"),
        }
    traza = {
        "carpeta": rel(corpus),
        "graph": rel(lay.out / "graph.json"),
        "nodes": meta.get("nodes"),
        "updated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "ids": ids,
    }
    (corpus / MEMORIA_TRAZA).write_text(json.dumps(traza, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def cmd_prepare(theme: Path) -> int:
    corpus = corpus_or_fail(theme)
    off = offline()
    rep = off.prepare(theme, lay=off.layout(theme, corpus))
    if rep.get("needs_agent"):
        for k in rep["needs_agent"]:
            print(f"  - needs_agent: {k}")
        return error(f"{len(rep['needs_agent'])} PDF necesitan un MD escrito por el agente",
                     f"escribe {rel(corpus)}/docs/md/<stem>.md (8 o más headings, localizadores [PDF p.N]) y corre pnpm -s cribado2:stamp {rel(theme)} <pdf>",
                     code=2)
    lay = off.layout(theme, corpus)
    return ok(
        f"{len(rep['converted'])} PDF convertidos y {len(rep['skipped'])} sin cambios en {rel(lay.md_dir)}/",
        f"pnpm -s cribado2:build {rel(theme)}",
    )


def cmd_stamp(theme: Path, pdf: str) -> int:
    corpus = corpus_or_fail(theme)
    off = offline()
    lay = off.layout(theme, corpus)
    name = Path(pdf).name
    off.stamp_agent_md(theme, pdf_manifest_key(lay, name), notes="agent-rag", lay=lay)
    return ok(f"{name} marcado como listo", f"pnpm -s cribado2:prepare {rel(theme)} y luego cribado2:build")


def cmd_build(theme: Path) -> int:
    corpus = corpus_or_fail(theme)
    off = offline()
    lay = off.layout(theme, corpus)
    agent, stale = pending(corpus, lay)
    if agent or stale:
        raise Fail(f"{len(agent)} PDF en needs_agent y {len(stale)} sin preparar",
                   f"corre pnpm -s cribado2:prepare {rel(theme)} y resuelve los needs_agent")
    meta = off.build_graph(theme, lay)
    res = off.verify(theme, lay)
    if not res["ok"]:
        return error(f"verify falló: {'; '.join(res['errors'][:3])}", "mejora los MD con más headings y vuelve a correr cribado2:build")
    write_memoria_traza(corpus, lay, meta)
    return ok(f"memoria de {len(meta['files'])} MD en {rel(lay.out / 'graph.json')} ({meta['nodes']} nodos, {meta['edges']} aristas)",
              "Usa rsl-cribado-2-polish sobre el tema cuando el grafo esté listo")


def cmd_status(theme: Path) -> int:
    corpus = corpus_or_fail(theme)
    off = offline()
    lay = off.layout(theme, corpus)
    agent, stale = pending(corpus, lay)
    if agent or stale:
        return error(f"{len(agent)} PDF en needs_agent y {len(stale)} sin preparar", f"Usa rsl-cribado-2-memoria sobre {rel(theme)}/")
    graph = lay.out / "graph.json"
    if not graph.is_file():
        return error(f"falta {rel(graph)}", f"pnpm -s cribado2:build {rel(theme)}")
    newest = max(p.stat().st_mtime for p in lay.md_dir.glob("*.md"))
    if newest > graph.stat().st_mtime:
        return error("hay MD más nuevos que el grafo", f"pnpm -s cribado2:build {rel(theme)}")
    res = off.verify(theme, lay)
    if not res["ok"]:
        return error(f"verify falló: {'; '.join(res['errors'][:3])}", f"pnpm -s cribado2:build {rel(theme)}")
    return ok(f"memoria al día en {rel(graph)} ({res['nodes']} nodos)")


def cmd_query(theme: Path, question: str) -> int:
    graph = cribado2_dir(theme) / "graphify-out" / "graph.json"
    if not graph.is_file():
        raise Fail(f"falta {rel(graph)}", f"Usa rsl-cribado-2-memoria sobre {rel(theme)}/")
    r = subprocess.run(["graphify", "query", question, "--graph", str(graph)], text=True)
    return r.returncode


def main(args: list[str]) -> int:
    if len(args) < 2:
        print(__doc__)
        return error(USAGE, code=2)
    cmd, theme, rest = args[0], theme_dir(args[1]), args[2:]
    simple = {
        "init": cmd_init,
        "download": cmd_download,
        "documentos": cmd_documentos,
        "align": cmd_align,
        "prepare": cmd_prepare,
        "build": cmd_build,
        "status": cmd_status,
    }
    if cmd in simple and not rest:
        return simple[cmd](theme)
    if cmd == "stamp" and len(rest) == 1:
        return cmd_stamp(theme, rest[0])
    if cmd == "query" and len(rest) == 1:
        return cmd_query(theme, rest[0])
    print(__doc__)
    return error(USAGE, code=2)


if __name__ == "__main__":
    run(main)
