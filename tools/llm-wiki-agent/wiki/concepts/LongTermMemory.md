---
title: "Long-Term Memory"
type: concept
tags: [agent-memory, long-term-memory]
sources: [agent-memory-provenance]
last_updated: 2026-09-16
---

# Long-Term Memory

The out-of-window storage layer that lets an agent carry state and knowledge across sessions and tool calls — the durable counterpart to the ephemeral [[LLMContext]] working set.

## Mechanism (per [[agent-memory-provenance]])
- Split by purpose rather than one general store; a proven design runs **three parallel memories**:
  - **Episodic** — an event timeline making *when* and *what changed* first-class.
  - **Associative** — an entity–event knowledge graph linking people/projects across sessions.
  - **Semantic** — a curated, [[CitationLock|citation-locked]] Hierarchical Documentary Memory (HDM) of durable facts.
- Retrieval: **intent gate** → **source router** → **three concurrent agentic searches** → one integrated answer.
- Governed by [[Provenance]] (every item carries origin/timestamp/evidence) and [[Abstention]] (no sourced evidence ⇒ refuse).

## Why It Matters
- Resolves the tension [[ContextEngineering]] leaves open: the window cannot hold cross-session state, so state must live elsewhere and be re-injected.
- Failure is *compounding*: a mistake written to durable memory recurs in every future plan; injection poisoning persists forever.
- Benchmarks: [[AgentZeroMemory]] 95.60% on [[LongMemEval]]; naive long-context reading drops 30–60%.

## See Also
- [[agent-memory-provenance]] — primary source
- [[Provenance]] · [[CitationLock]] · [[Abstention]] — the reading discipline
- [[MemGPT]] · [[AgentZeroMemory]] · [[Zep]] — systems
- [[ContextEngineering]] — writes/reads are context-engineering decisions
- [[LLMContext]] — the bounded working set it complements
