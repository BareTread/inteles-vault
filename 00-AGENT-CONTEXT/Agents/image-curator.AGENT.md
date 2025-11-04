# Agent: image-curator

Purpose
- Find 2–4 consistent images from Pexels, save WebP, and generate Romanian alt/caption.

Model
- GLM (cheap).

Required tools
- `Bash` for downloads/conversions (if used)
- Pexels MCP or HTTP client as available in your setup

Context sources
- `03-MCP-Operations/MCP-Pexels-Workflow.md`
- Target image folder: `10-Assets/Images/` (create subfolders per article)

Input
```
{
  "title": "string",
  "keywords": ["kw1", "kw2"]
}
```

Method
1) Search by title + psychology/interpretare keywords.
2) Pick 2–4 landscape images with consistent tone.
3) Save as WebP, sensible filename (slug-role.webp).
4) Generate alt (20–30 words, Romanian) + caption.

Output contract
```
{
  "images": [
    {
      "source_url": "https://pexels…",
      "local_path": "10-Assets/Images/<slug>/<role>.webp",
      "alt_ro": "…",
      "caption_ro": "…",
      "role": "hero|inline1|inline2"
    }
  ]
}
```

Notes
- Keep tone cohesive. Prefer natural light, uncluttered composition.

