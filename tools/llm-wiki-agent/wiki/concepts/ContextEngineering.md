---
title: "Context Engineering"
type: concept
tags: [context-engineering, anthropic, prompt-engineering]
sources: [context-engineering]
last_updated: 2026-09-16
---

# Context Engineering

The discipline of deciding, at every inference step, which tokens to place into the bounded context window — targeting the *minimal set of high-signal tokens* that produces the target result, rather than maximal volume.

## Mechanism (per [[context-engineering]])
1. **Layer by information lifespan** — stable boundaries once at start; current state reread right before key steps; large raw payloads kept as identifiers/addresses only.
2. **Just-in-time retrieval** — replace pre-loading with on-demand fetch; the window holds references, not originals.
3. **Each turn: trim + re-inject** — tool results return summaries + evidence pointers by default; old processed results are cleared near the limit.
4. **Long-horizon techniques** — [[Compaction]], structured notes, sub-agents.

## Why It Matters
- The constraint is architectural: [[Transformer]] attention is an n² budget, so longer context spreads attention thinner.
- Directly opposes "bigger window = better": [[ContextRot]] means effective capacity runs below the nominal ceiling.
- Evidence: Anthropic cut Claude Code's system prompt by 80%+ with no measurable coding-eval loss; tool definitions dropped 77K → 8.7K tokens (−85%) while accuracy *rose* 79.5% → 88.1%.

## See Also
- [[context-engineering]] — primary source
- [[ContextRot]] — the phenomenon it fights
- [[LLMContext]] — the resource it manages
- [[Compaction]] — its long-horizon technique
- [[ProgressiveDisclosure]] & [[Skill]] — knowledge-loading instance of the same principle
- [[Provenance]] — retrieved memory is only as useful as it is trustworthy
