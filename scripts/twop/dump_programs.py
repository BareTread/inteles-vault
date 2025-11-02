import os
from pathlib import Path
try:
    from dotenv import load_dotenv  # optional
except Exception:
    load_dotenv = lambda *a, **k: None
import sys
from pathlib import Path as _P
sys.path.append(str(_P(__file__).resolve().parents[2]))
from scripts.twop.two_performant_client import TwoPerformantClient


def main():
    load_dotenv()
    email = os.getenv("TWO_P_EMAIL")
    password = os.getenv("TWO_P_PASSWORD")
    base = os.getenv("TWO_P_BASE", "https://api.2performant.com")
    if not (email and password):
        raise SystemExit("Missing TWO_P_EMAIL / TWO_P_PASSWORD. See .env.example")
    client = TwoPerformantClient(base_url=base, email=email, password=password)
    client.login()
    data = client.list_all_affiliate_programs(relation="accepted")
    out = Path("04-Monetization/Programs-Dump.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    # Minimal JSON writing without extra dependencies
    import json
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {out} with {len(data)} programs")


if __name__ == "__main__":
    main()
