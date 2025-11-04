# Agents — Hybrid Workflow (Claude Pro + GLM)

This folder defines the sub‑agents used by the GLM Claude Code instance. Each agent has:
- Purpose and responsibilities
- Context sources within the vault
- Required MCP servers / tools
- Strict I/O contract to keep tokens lean

Run order (typical):
1) Research (Perplexity or manual) → produce brief + key insights
2) Writer Coordinator → calls Claude Pro MCP to write premium Romanian
3) In parallel → Monetization Specialist & Image Curator
4) Kadence Block Engineer → assemble HTML
5) Publisher → WordPress MCP publish (idempotent)

Keep each agent’s context minimal and focused to avoid polluting session memory.

