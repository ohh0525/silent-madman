---
title: "Overview"
type: synthesis
tags: []
sources: [agent, llm-context, skill, context-engineering, agent-memory-provenance]
last_updated: 2026-09-16
---

# Overview

*This page is maintained by the LLM. It is updated on every ingest to reflect the current synthesis across all sources.*

## Current Synthesis (2026-09-16)

Five silent-madman concept-learning documents have been ingested. The first three form a cluster around "how LLMs reason with bounded resources"; the two added on 2026-09-16 supply the **methodology layer** and the **time dimension** that organize them.

### Cluster A — Bounded resources (2026-09-05)
- **[[Agent]]** is the autonomous execution layer — a system that picks tools and loops around a goal.
- **[[LLMContext]]** is the hard constraint Agent operates under — a token-budgeted "desktop" bounded by [[Transformer]]'s n² cost.
- **[[Skill]]** is the unit that lets a general model act like a domain expert without bloating context — via **[[ProgressiveDisclosure]]**.

### Cluster B — Methodology + time (2026-09-16)
- **[[ContextEngineering]]** answers *who decides what goes on the desk*: it manages the window by layering information by lifespan, retrieving just-in-time, and trimming/re-injecting each turn. It battles **[[ContextRot]]** and uses **[[Compaction]]** for long tasks. Crucially, it reframes Cluster A: [[ProgressiveDisclosure]] is *an instance* of context engineering, not a separate mechanism.
- **[[LongTermMemory]]** answers *what happens across sessions*: the window cannot hold durable state, so it lives outside and is re-injected. The 2026 design bet is **three parallel memories** (episodic / associative / semantic-HDM) governed by a reading discipline — **[[Provenance]]** (every fact carries origin + time + evidence), **[[CitationLock]]** (cite only what you opened), and **[[Abstention]]** (no sourced evidence ⇒ refuse). Systems: [[MemGPT]], [[AgentZeroMemory]], [[Zep]]; evidence: [[LongMemEval]].

### How they connect

```
Context Engineering  ──manages/crops──▶  LLM Context Window
        │                                   ▲
        │ Progressive Disclosure is          │ supplies trusted
        │ one instance of it                 │ long-term facts
        ▼                                   │
      Skill                              Long-Term Memory
        │                                   ▲
        └──────loads into────────────────────┘
                     Agent reads/writes ─────┘
```

The five-page story: **an Agent, bounded by a Context Window, uses Skills to load knowledge on demand (Progressive Disclosure); Context Engineering decides what belongs in that window each step; and provenance-aware Long-Term Memory lets the Agent remember across sessions — honestly.**

## Cross-Cutting Themes
- **Bounded context is the central constraint** — every concept traces back to a token / window / cost limit. [[ContextRot]] sharpens it: capacity ≠ effective capacity.
- **"On-demand loading" is the dominant solution shape** — Skills (progressive disclosure), RAG, and memory retrieval all share it. [[ContextEngineering]] names it as a principle.
- **Trust is the new frontier** — Cluster A assumed more/cleaner context; Cluster B adds that retrieved context must be *sourced and current* ([[Provenance]], [[CitationLock]], [[Abstention]]).
- **Memory errors compound** — a mistake written to durable memory recurs; this reframes memory as a *reliability subsystem*, not a recall feature.
- **[[Anthropic]] is the primary vendor** contributing this design vocabulary; [[OpenAI]] complements; memory systems now contribute [[AgentZeroMemory]], [[MemGPT]], [[Zep]].

## Open Questions (suggested next sources)
- A concrete RAG system case study (vector DB choice, chunking strategy, retrieval quality) — still open from 2026-09-09.
- The MCP stateless revision (2026-07-28 spec) — [[MCP]] page may be outdated (flagged by the 2026-09-16 concept radar).
- How [[ContextEngineering]] techniques are measured end-to-end (beyond single-provider claims) — needs an independent evaluation.
- Multi-agent memory sharing and role-based access control on shared persistent memory.

## Next Ingest Suggestions
- `raw/papers/rag-survey.md` — RAG foundations
- `raw/specs/mcp-2026-07-28.md` — MCP stateless revision
- `raw/papers/context-engineering-eval.md` — independent context-engineering evaluation
