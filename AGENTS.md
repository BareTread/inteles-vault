# Repository Guidelines

## Project Structure & Module Organization
- Content vault: `00-AGENT-CONTEXT`, `01-Project-Overview`, …, `12-Recent-Work-Sessions` (Obsidian‑ready Markdown).
- Automation: Python utilities in `scripts/twop/` and a helper shell script in `scripts/monetization-refresh.sh`.
- Generated outputs and reports live in `04-Monetization/` (e.g., `Auto-Generated-Affiliate-Links.md`, `Affiliate-Audit-Report.md`).
- Configuration: `.env` (local only) with `TWO_P_EMAIL`, `TWO_P_PASSWORD`, `TWO_P_AFF_CODE`. See `.env.example`.

## Build, Test, and Development Commands
- Create venv and install deps:
  ```bash
  python3 -m venv .venv
  .venv/bin/pip install -r scripts/twop/requirements.txt
  ```
- Refresh monetization bundle (end‑to‑end):
  ```bash
  bash scripts/monetization-refresh.sh
  ```
- Run individual steps:
  ```bash
  .venv/bin/python scripts/twop/dump_programs.py
  .venv/bin/python scripts/twop/fetch_and_build.py --out 04-Monetization/Auto-Generated-Affiliate-Links.md
  .venv/bin/python scripts/twop/audit_and_fix_affiliates.py
  ```

## Coding Style & Naming Conventions
- Python: PEP 8, 4‑space indent, type hints where practical; prefer `pathlib`, minimal deps (`requests`, `python-dotenv`).
- Filenames: snake_case for Python (`filter_md_by_csv.py`), kebab/Title Case for Markdown as used in the vault.
- Keep scripts idempotent and safe to re‑run; write outputs under `04-Monetization/`.

## Testing Guidelines
- No formal test suite. Validate by running the refresh script and reviewing generated files:
  - `04-Monetization/Auto-Generated-Affiliate-Links.md`
  - `04-Monetization/Affiliate-Audit-Report.md`
  - `04-Monetization/Best-Opportunities.ACCEPTED.md` (if present)
- Use `.env.example` to verify required vars. Avoid network calls in docs‑only changes.

## Commit & Pull Request Guidelines
- Commit style mirrors history: concise imperative prefix in CAPS (e.g., `FIX:`, `ADD:`, `REFACTOR:`, `DOCS:`), then a short scope.
- PRs should include:
  - Purpose, linked issue (if any), and impact on `04-Monetization/` outputs.
  - Before/after snippets or paths of changed/generated files.
  - Notes on config/env requirements and any external calls.

## Security & Configuration Tips
- Never commit `.env` or secrets. Use `.env.example` for placeholders.
- When sharing outputs, redact affiliate codes unless explicitly intended for publication.

## Agent‑Specific Instructions
- Honor this guide across the entire vault. Avoid large‑scale reformatting of Markdown.
- Prefer small, reviewable changes; keep generated files out of diff unless purposefully updated.
