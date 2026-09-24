---
title: "Long-Term Memory"
type: concept
tags: [agent-memory, long-term-memory, memory-lifecycle]
sources: [agent-memory-provenance]
last_updated: 2026-09-24
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

## Boundary Note — the other half of a memory's life *(added 2026-09-24)*

> **Draft annotation, pending ingest.** This section is **not yet backed by a source page in this wiki** — its claims were verified against live primary sources on 2026-09-24 (recorded in `.workbuddy/memory/concept-radar/2026-09-24.md`, candidate 1). Remove this banner when the material is ingested and human-reviewed, and move the source slug into the frontmatter `sources` field.

This page describes only the **first half** of a memory's life — how to store it, split it by purpose, and read it credibly. A memory also has a **second half**: decay scoring, merge, TTL expiry and compliant deletion. The framing question is not *"can we store it?"* but **"when should we let it be forgotten?"**

- **Retention is per-type, never one global TTL.** The three stores this page defines do not expire alike: *episodic* (high volume, timestamp-bound, expires first) → *semantic* (durable facts; the main **merge** target) → *procedural* (lowest volume, highest value, retained longest, hardest to prune).
- **Deletion vs [[Provenance]] is the sharpest seam in this cluster.** Provenance requires every stored fact to carry origin / timestamp / evidence so it stays auditable; the right to erasure requires the *same* fact to be removed at the root. Deleting the fact **breaks the citation chain** — so the deletion itself must leave a trace (a receipt, a failure list, and a rollback-capable snapshot).
- **The opposite failure mode also exists.** Unmanaged memory fails twice over: stale entries get re-injected as if current (a resolved dispute re-raised months later; a superseded runbook re-quoted), while [[Provenance]] without deletion fails on compliance.
- **Not [[Compaction]].** Compaction operates *inside* the window, per turn, and is lossy; lifecycle governance operates *outside* it, across sessions, on a day/week cadence, offline — it does not participate in the current inference turn.

## See Also
- [[agent-memory-provenance]] — primary source
- [[Provenance]] · [[CitationLock]] · [[Abstention]] — the reading discipline
- [[MemGPT]] · [[AgentZeroMemory]] · [[Zep]] — systems
- [[ContextEngineering]] — writes/reads are context-engineering decisions
- [[LLMContext]] — the bounded working set it complements
