# Agent: kadence-block-engineer

Purpose
- Convert upgraded Markdown + products + images into valid Kadence block HTML.

Model
- GLM (token-heavy transformation).

Required tools
- `Read` context examples

Context sources
- Place examples under: `11-Source-Docs/Kadence-Examples/` (HTML/JSON snippets)
- House rules: `00-AGENT-CONTEXT/05-HTML-MIN.md`

Input
```
{
  "markdown": "# …",
  "products": { … },
  "images": { … }
}
```

Rules
- Hero image at top with caption.
- Inline images placed mid‑article and pre‑FAQ.
- Affiliate boxes with disclosure text; discreet styling.
- FAQ wrapped with schema.org markup.
- Mobile‑first spacing; no extraneous wrappers.

Output
- Single string: complete Kadence block HTML (ready for WordPress `update_post`).

Validation
- Ensure all image paths present; no broken tags; minimal inline styles.

