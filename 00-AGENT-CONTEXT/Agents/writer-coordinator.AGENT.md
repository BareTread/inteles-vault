# Agent: writer-coordinator

Purpose
- Assemble perfect prompt + context and call Claude Pro MCP to generate premium Romanian content.

Model
- Runs under GLM instance. Delegates writing to Claude Pro MCP.

Required MCP servers / tools
- `@claude-code-writer` (community MCP that spawns Claude CLI / Pro)
- Read from vault context files

Context sources
- `00-AGENT-CONTEXT/07-STYLE-GUARDRAILS.md`
- `00-AGENT-CONTEXT/02-WRITING-RUBRIC.md`
- `00-AGENT-CONTEXT/06-ARTICLE-BRIEF-TEMPLATE.md`
- Optional: research notes saved alongside the article brief

Input (from orchestrator)
```
{
  "topic": "string",
  "outline": ["H1/H2..."],
  "insights": ["bulleted SEO + research takeaways"],
  "keywords": ["kw1", "kw2", "kw3"]
}
```

Tool call
- Use `@claude-code-writer` (tool: `claude_code` with `prompt` + optional `workFolder`)
- Hard rules in the prompt:
  - Romanian only with diacritics (ă, î, ș, ț, â)
  - Preserve structure; no CJK characters
  - Short paragraphs (2–3 sentences)
  - Quick answer in first 2–3 paragraphs
  - 900–1200 words (or as requested)

Output contract
```
{
  "content": "<Markdown>…</Markdown>",
  "excerpt": "25–35 words",
  "keywords": ["kw1", "kw2", "kw3"]
}
```

Notes
- Keep returned text compact. Do not include analysis or traces.
- If the MCP tool is generic (e.g., `complete`), enforce output contract in the prompt.
