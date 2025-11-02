import csv
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from urllib.parse import urlparse, parse_qs, unquote

try:
    from dotenv import load_dotenv  # optional
except Exception:
    def load_dotenv(*a, **k):
        return False


MASTER_PATH = Path("04-Monetization/MASTER-PRODUCTS-LIST.md")
CSV_PATH = Path("affiliate_merchants_2performant.csv")
REPORT_PATH = Path("04-Monetization/Affiliate-Audit-Report.md")
HOMEPAGES_PATH = Path("04-Monetization/Approved-Merchant-Homepages.md")
PROGRAMS_DUMP = Path("04-Monetization/Programs-Dump.json")
VAULT_AUDIT_PATH = Path("04-Monetization/Vault-Wide-Affiliate-Audit.md")


@dataclass
class Quicklink:
    raw: str
    aff_code: Optional[str]
    redirect_to: Optional[str]
    dest_domain: Optional[str]
    unique: Optional[str]
    valid_format: bool


def _norm_domain(host: str) -> str:
    host = host.strip().lower()
    # Extract the first domain-like token
    import re as _re
    m = _re.search(r"([a-z0-9.-]+\.[a-z]{2,})(?![a-zA-Z0-9])", host)
    if m:
        host = m.group(1)
    if host.startswith("http://") or host.startswith("https://"):
        try:
            host = urlparse(host).netloc
        except Exception:
            pass
    if host.startswith("www."):
        host = host[4:]
    return host


def load_accepted_domains(csv_path: Path) -> List[str]:
    if not csv_path.exists():
        return []
    domains: List[str] = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            merchant = (row.get("Merchant") or "").strip().lower()
            status = (row.get("Status") or "").strip().lower()
            if not merchant:
                continue
            host = _norm_domain(merchant)
            domains.append(host)
    # De-duplicate, keep order
    seen = set()
    out: List[str] = []
    for d in domains:
        if d and d not in seen:
            seen.add(d)
            out.append(d)
    return out


def extract_quicklinks(md_text: str) -> List[str]:
    # Capture 2Performant click URLs inside code blocks or plain lines
    pattern = re.compile(r"https://event\.2performant\.com/events/click\?[^\s`]+")
    return pattern.findall(md_text)


def parse_quicklink(url: str) -> Quicklink:
    ok = urlparse(url)
    valid = ok.scheme == "https" and ok.netloc == "event.2performant.com" and ok.path.startswith("/events/click")
    qs = parse_qs(ok.query)
    aff_code = (qs.get("aff_code") or [None])[0]
    unique = (qs.get("unique") or [None])[0]
    redir_raw = (qs.get("redirect_to") or [None])[0]
    redirect_to = unquote(redir_raw) if redir_raw else None
    domain = None
    if redirect_to:
        try:
            domain = urlparse(redirect_to).netloc.lower()
            if domain.startswith("www."):
                domain = domain[4:]
        except Exception:
            domain = None
    return Quicklink(raw=url, aff_code=aff_code, redirect_to=redirect_to, dest_domain=domain, unique=unique, valid_format=valid)


def build_report(aff_code_env: Optional[str], accepted_domains: List[str], qls: List[Quicklink]) -> str:
    total = len(qls)
    invalid_fmt = [q for q in qls if not q.valid_format]
    wrong_aff = [q for q in qls if aff_code_env and q.aff_code and q.aff_code != aff_code_env]
    missing_aff = [q for q in qls if not q.aff_code]
    missing_redir = [q for q in qls if not q.redirect_to]
    not_in_csv = [q for q in qls if q.dest_domain and accepted_domains and q.dest_domain not in accepted_domains]

    lines: List[str] = []
    lines.append("# Affiliate Audit Report — 2Performant\n")
    lines.append(f"Env affiliate code detected: {aff_code_env or '(none)'}\n")
    lines.append(f"CSV accepted merchants: {len(accepted_domains)}\n")
    lines.append(f"Scanned links: {total}\n")
    lines.append("\n---\n")

    def add_section(title: str, items: List[Quicklink], annotate: bool = False):
        if not items:
            return
        lines.append(f"## {title} ({len(items)})")
        for q in items[:200]:
            desc = q.raw
            if annotate and q.dest_domain:
                desc += f"\n   → {q.dest_domain}"
            lines.append(f"- {desc}")
        lines.append("")

    add_section("Invalid 2Performant link format", invalid_fmt)
    add_section("Missing aff_code param", missing_aff)
    add_section("Wrong aff_code vs .env", wrong_aff)
    add_section("Missing redirect_to param", missing_redir)
    add_section("Destination domain NOT in CSV", not_in_csv, annotate=True)

    ok_links = [q for q in qls if q.valid_format and q.aff_code and (not aff_code_env or q.aff_code == aff_code_env)]
    lines.append("## Summary")
    lines.append(f"- Valid links: {len(ok_links)}/{total}")
    lines.append(f"- Invalid format: {len(invalid_fmt)}")
    lines.append(f"- Wrong `aff_code`: {len(wrong_aff)}")
    lines.append(f"- Dest not in CSV: {len(not_in_csv)}")
    lines.append("")

    if not_in_csv:
        lines.append("### Note")
        lines.append("Some destinations are not present in `affiliate_merchants_2performant.csv`.\n"
                     "If these programs are no longer approved, replace with merchants from the CSV or update the CSV.")
        lines.append("")

    return "\n".join(lines)


def chunk_by_products(md_text: str) -> List[Tuple[str, str]]:
    """Split the master list into chunks keyed by their product heading.
    Returns list of (key, chunk_text). key is the heading for product chunks, or "__OTHER__" for non-product regions.
    """
    lines = md_text.splitlines(keepends=True)
    chunks: List[Tuple[str, List[str]]] = []
    current_key = "__OTHER__"
    current: List[str] = []
    for ln in lines:
        if ln.startswith("### "):
            # flush previous
            if current:
                chunks.append((current_key, current))
            current_key = ln.strip()
            current = [ln]
        else:
            current.append(ln)
    if current:
        chunks.append((current_key, current))
    # join back
    return [(k, "".join(v)) for k, v in chunks]


def quicklinks_in_text(text: str) -> List[Quicklink]:
    urls = extract_quicklinks(text)
    return [parse_quicklink(u) for u in urls]


def write_filtered_master(md_text: str, accepted_domains: List[str], out_path: Path) -> int:
    chunks = chunk_by_products(md_text)
    out_parts: List[str] = []
    removed = 0
    for key, chunk in chunks:
        if key == "__OTHER__":
            out_parts.append(chunk)
            continue
        qls = quicklinks_in_text(chunk)
        # Keep if no quicklinks OR all destinations are in accepted list
        if not qls:
            out_parts.append(chunk)
            continue
        dests = [q.dest_domain for q in qls if q.dest_domain]
        all_ok = all((d in accepted_domains) for d in dests) if dests else True
        if all_ok:
            out_parts.append(chunk)
        else:
            removed += 1
    out = "".join(out_parts)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(out, encoding="utf-8")
    return removed


def build_homepages_md(aff_code: Optional[str], domains: List[str]) -> str:
    lines: List[str] = []
    lines.append("# Approved Merchant Homepages — 2Performant\n")
    if not aff_code:
        lines.append("> Warning: TWO_P_AFF_CODE not set. Quicklinks below will not track without an affiliate code.\n")
    lines.append("\nUse these quicklinks when a specific product link is not yet curated.\n")
    lines.append("\n---\n")
    base = "https://event.2performant.com/events/click?ad_type=quicklink"
    for d in domains:
        dest = f"https://{d}"
        from urllib.parse import quote
        redir = quote(dest, safe="")
        if aff_code:
            url = f"{base}&aff_code={aff_code}&redirect_to={redir}"
        else:
            url = f"{base}&redirect_to={redir}"
        lines.append(f"- {d}\n  {url}")
    lines.append("")
    return "\n".join(lines)


def build_csv_api_delta_md(csv_domains: List[str], programs_dump: Path) -> Optional[str]:
    if not programs_dump.exists():
        return None
    import json
    try:
        data = json.loads(programs_dump.read_text(encoding="utf-8"))
    except Exception:
        return None
    api_domains: List[str] = []
    for p in data if isinstance(data, list) else []:
        base = (p.get("base_url") or p.get("main_url") or "").strip().lower()
        if base:
            api_domains.append(_norm_domain(base))
    api_set = set(d for d in api_domains if d)
    csv_set = set(d for d in csv_domains if d)
    only_csv = sorted(csv_set - api_set)
    only_api = sorted(api_set - csv_set)

    lines: List[str] = []
    lines.append("# CSV vs API Programs — Diff\n")
    lines.append(f"CSV merchants: {len(csv_set)} | API accepted: {len(api_set)}\n")
    if only_csv:
        lines.append("\n## In CSV but not in API")
        for d in only_csv:
            lines.append(f"- {d}")
    if only_api:
        lines.append("\n## In API but not in CSV (you may be accepted here)")
        for d in only_api[:100]:
            lines.append(f"- {d}")
    lines.append("")
    return "\n".join(lines)


def vault_wide_audit(accepted_domains: List[str]) -> str:
    root = Path('.')
    # Find files with quicklinks (simple grep equivalent)
    files: List[Path] = []
    for p in root.rglob('*'):
        if not p.is_file():
            continue
        if any(seg in p.parts for seg in ['.git', '.venv', '__pycache__']):
            continue
        try:
            txt = p.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        if 'https://event.2performant.com/events/click?' in txt:
            files.append(p)

    rows: List[Tuple[str, int, int, int]] = []  # file, total, ok, not_in_csv
    for p in sorted(files):
        try:
            txt = p.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        urls = extract_quicklinks(txt)
        qls = [parse_quicklink(u) for u in urls]
        total = len(qls)
        not_in = 0
        ok = 0
        for q in qls:
            if q.dest_domain and q.dest_domain in accepted_domains:
                ok += 1
            else:
                not_in += 1
        rows.append((str(p), total, ok, not_in))

    lines: List[str] = []
    lines.append("# Vault-wide Affiliate Audit\n")
    lines.append(f"Files with 2Performant links: {len(rows)}\n")
    lines.append("\nFormat: file — total | ok | not-in-CSV\n")
    lines.append("\n---\n")
    for f, total, ok, bad in rows:
        lines.append(f"- {f} — {total} | {ok} | {bad}")
    lines.append("")
    return "\n".join(lines)


def main():
    # Load .env if present
    load_dotenv()
    aff_env = os.getenv("TWO_P_AFF_CODE")
    if not MASTER_PATH.exists():
        print(f"Missing master list: {MASTER_PATH}")
        sys.exit(1)

    md = MASTER_PATH.read_text(encoding="utf-8", errors="ignore")
    urls = extract_quicklinks(md)
    qls = [parse_quicklink(u) for u in urls]
    accepted = load_accepted_domains(CSV_PATH)
    report = build_report(aff_env, accepted, qls)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"Wrote {REPORT_PATH} — scanned {len(qls)} links, CSV merchants: {len(accepted)}")

    # Also write a filtered master list based on accepted CSV merchants
    filtered_path = MASTER_PATH.with_suffix(".ACCEPTED.md")
    removed = write_filtered_master(md, accepted, filtered_path)
    print(f"Wrote {filtered_path} — removed {removed} product blocks not in CSV")

    # Write a helper with homepage quicklinks for all CSV merchants
    home_md = build_homepages_md(aff_env, accepted)
    HOMEPAGES_PATH.write_text(home_md, encoding="utf-8")
    print(f"Wrote {HOMEPAGES_PATH} — {len(accepted)} merchants")

    # CSV vs API delta report (if Programs-Dump.json exists)
    delta = build_csv_api_delta_md(accepted, PROGRAMS_DUMP)
    if delta:
        delta_path = Path("04-Monetization/CSV-API-Programs-Delta.md")
        delta_path.write_text(delta, encoding="utf-8")
        print(f"Wrote {delta_path}")

    # Vault-wide audit summary
    VAULT_AUDIT_PATH.write_text(vault_wide_audit(accepted), encoding='utf-8')
    print(f"Wrote {VAULT_AUDIT_PATH}")


if __name__ == "__main__":
    main()
