---
title: "Compaction"
type: concept
tags: [context-engineering, long-horizon, anthropic]
sources: [context-engineering]
last_updated: 2026-09-16
---

# Compaction

One of the three long-horizon context techniques: summarize the conversation history and restart from the summary, preserving only architectural decisions, open questions, and the most recently accessed files.

## Mechanism (per [[context-engineering]])
- **Compaction** — summarize history → restart with a compacted context.
- **Structured notes** — the agent writes progress to a file *outside* context (Claude Code's todo list is this pattern).
- **Sub-agents** — a dedicated agent digs into a clean window and returns only ~1,000–2,000 high-density tokens to the main agent.

## Why It Matters
- Tasks spanning tens of minutes to hours cannot fit in any window; state must live outside the dialogue.
- Improves *recall* first (don't drop the load-bearing decision), then iterate on *precision* (remove redundancy).
- Over-compression can lose nuance, but doing nothing is worse — the agent simply fails at the limit.

## See Also
- [[context-engineering]] — primary source
- [[ContextEngineering]] — parent discipline
- [[Agent]] — the long-task consumer
- [[LLMContext]] — the bounded resource being compacted
