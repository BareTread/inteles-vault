import argparse
import csv
import re
from pathlib import Path
from urllib.parse import urlparse, parse_qs, unquote


def _norm_domain(host: str) -> str:
    host = host.strip().lower()
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


def load_csv_domains(csv_path: Path):
    domains = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            merchant = (row.get("Merchant") or "").strip()
            if not merchant:
                continue
            domains.append(_norm_domain(merchant))
    return set(d for d in domains if d)


def extract_quicklinks(text: str):
    pattern = re.compile(r"https://event\.2performant\.com/events/click\?[^\s`]+")
    return pattern.findall(text)


def link_domain(u: str):
    ok = urlparse(u)
    qs = parse_qs(ok.query)
    redir_raw = (qs.get("redirect_to") or [None])[0]
    if not redir_raw:
        return None
    dest = unquote(redir_raw)
    try:
        host = urlparse(dest).netloc.lower()
    except Exception:
        return None
    if host.startswith("www."):
        host = host[4:]
    return host


def filter_sections(md_text: str, accepted: set[str], level: int = 2):
    lines = md_text.splitlines(keepends=True)
    out = []
    current = []
    current_ok = True
    header_prefix = "#" * level + " "

    def flush():
        if current:
            if current_ok:
                out.extend(current)
            current.clear()

    for ln in lines:
        if ln.startswith(header_prefix):
            flush()
            current_ok = True  # assume ok until we see a disallowed link
            current.append(ln)
            continue
        if "https://event.2performant.com/events/click?" in ln:
            urls = extract_quicklinks(ln)
            for u in urls:
                d = link_domain(u)
                if d and d not in accepted:
                    current_ok = False
        current.append(ln)
    flush()
    return "".join(out)


def main():
    ap = argparse.ArgumentParser(description="Filter a Markdown file to keep only sections whose 2Performant links redirect to CSV merchants")
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--csv", default="affiliate_merchants_2performant.csv")
    ap.add_argument("--level", type=int, default=2, help="Markdown header level to treat as a section (default ##)")
    args = ap.parse_args()

    accepted = load_csv_domains(Path(args.csv))
    md = Path(args.input).read_text(encoding="utf-8", errors="ignore")
    filtered = filter_sections(md, accepted, level=args.level)
    Path(args.output).write_text(filtered, encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()

