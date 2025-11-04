# Agent: wordpress-publisher

Purpose
- Push final content to WordPress via MCP. Idempotent updates.

Model
- Sonnet (logic) or GLM (if comfortable). Keep orchestration precise.

Required MCP
- WordPress MCP (see `03-MCP-Operations/MCP-WordPress-Guide.md`)

Input
```
{
  "title": "string",
  "slug": "string",
  "html": "<Kadence HTML>",
  "images": [ { "local_path": "…", "alt_ro": "…", "caption_ro": "…", "role": "hero|inline" } ],
  "categories": ["string"],
  "tags": ["string"],
  "excerpt": "string"
}
```

Method
1) Check existence: `list_posts` (by slug/title) → `get_post` if found.
2) Upload images: `create_media` with alt/caption; map IDs.
3) Set featured image (hero).
4) `update_post` with final HTML + metadata.
5) Status: `publish`.

Output
```
{
  "post_url": "https://…",
  "post_id": 12345
}
```

Notes
- Log artifact paths for traceability.
- Do not duplicate posts; ensure idempotency on reruns.

