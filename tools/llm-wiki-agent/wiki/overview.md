---
title: "Overview"
type: synthesis
tags: []
sources: [agent, llm-context, skill]
last_updated: 2026-09-09
---

# Overview

*This page is maintained by the LLM. It is updated on every ingest to reflect the current synthesis across all sources.*

## Current Synthesis (2026-09-09)

Three silent-madman concept-learning documents have been ingested, forming a tightly interconnected cluster around "how LLMs reason with bounded resources":

- **[[Agent]]** is the autonomous execution layer — a system that picks tools and loops around a goal.
- **[[LLMContext]]** is the hard constraint Agent operates under — a token-budgeted "desktop" bounded by Transformer's n² cost.
- **[[Skill]]** is the unit that lets a general model act like a domain expert without bloating context — via **[[ProgressiveDisclosure]]**, which exposes only YAML metadata initially and loads deeper resources on demand.

The three form a closed feedback loop:

```
            ┌──────────────────────────────────────┐
            │  Agent picks tools + loops          │
            └────────────────┬─────────────────────┘
                             │ bounded by
            ┌────────────────▼─────────────────────┐
            │  LLM Context Window (token budget)   │
            └────────────────┬─────────────────────┘
                             │ preserved by
            ┌────────────────▼─────────────────────┐
            │  Skill + Progressive Disclosure      │
            └────────────────┬─────────────────────┘
                             │ activated by
            └──────────────────────────────────────┘
                            (back to Agent)
```

## Cross-Cutting Themes
- **Bounded context is the central engineering constraint** — every concept traces back to a token / window / cost limit.
- **"On-demand loading" is the dominant solution shape** — Skills (progressive disclosure), RAG (vector retrieval), file_search (OpenAI), memory tool (Anthropic) all share this pattern.
- **[[Anthropic]] is the primary vendor contributing this design vocabulary**; [[OpenAI]] provides complementary framing.
- **Memory ≠ context window ≠ training knowledge** — the three are easy to confuse but operate on different axes.

## Open Questions (suggested next sources)
- A concrete RAG system case study (vector DB choice, chunking strategy, retrieval quality)
- MemGPT or Anthropic memory tool reference (for OS-style tiered memory)
- LangChain's memory module deep-dive (for practical patterns across 6 memory types)
- How Agent memory system (vector / summary / KV trade-offs) interacts with Skill loading

## Next Ingest Suggestions
- `raw/papers/rag-survey.md` — RAG foundations
- `raw/tools/memgpt-paper.md` — OS-style tiered memory
- `raw/tools/langchain-memory.md` — practical memory patterns