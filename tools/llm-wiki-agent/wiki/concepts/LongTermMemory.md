---
title: "Long-Term Memory"
type: concept
tags: [agent-memory, long-term-memory, memory-lifecycle, latent-memory, scoped-revision, aggregate-metric-blindness]
sources: [agent-memory-provenance, memory-lifecycle]
last_updated: 2026-10-21
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
- ⚠️ **Read that 95.60% carefully** *(added 2026-10-09)*: it is a **given-the-right-memory / end-to-end** result. [[DyadMem]] shows frontier models are strong on Gold-Memory and **collapse on Full-Pipeline** (running capture/update/recall themselves), and Memora finds memory modules delivering only **marginal** gains with 94%/85% of pre-existing benchmark questions spanning ≤2 sessions. Not a contradiction — a **change of measurement target**. Stop quoting a single benchmark number as evidence that long-term memory works.

## The other half of a memory's life (now sourced — *2026-09-24, banner cleared 2026-10-09*)

This page describes only the **first half** of a memory's life — how to store it, split it by purpose, and read it credibly. A memory also has a **second half**: decay scoring, merge, TTL expiry and compliant deletion. The framing question is not *"can we store it?"* but **"when should we let it be forgotten?"** — and, as of 2026-10-09, **who is entitled to decide**. That half now has its own pages: **[[MemoryGovernance]]** (the four actions · the three deciders · the four governance bottom lines) and **[[MemoryPoisoning]]** (the write-side attack surface).

- **Retention is per-type, never one global TTL.** The three stores this page defines do not expire alike: *episodic* (high volume, timestamp-bound, expires first) → *semantic* (durable facts; the main **merge** target) → *procedural* (lowest volume, highest value, retained longest, hardest to prune).
- **Deletion vs [[Provenance]] is the sharpest seam in this cluster.** Provenance requires every stored fact to carry origin / timestamp / evidence so it stays auditable; the right to erasure requires the *same* fact to be removed at the root. Deleting the fact **breaks the citation chain** — so the deletion itself must leave a trace (a receipt, a failure list, and a rollback-capable snapshot).
- **The opposite failure mode also exists.** Unmanaged memory fails twice over: stale entries get re-injected as if current (a resolved dispute re-raised months later; a superseded runbook re-quoted), while [[Provenance]] without deletion fails on compliance. Memora's **FAMA** metric turns the first of these into a deductible score.
- **Not [[Compaction]].** Compaction operates *inside* the window, per turn, and is lossy; lifecycle governance operates *outside* it, across sessions, on a day/week cadence, offline — it does not participate in the current inference turn.

## The third carrier — Latent & Soft-Token Memory *(added 2026-10-17)*

> **Draft annotation, pending ingest.** This section is **not yet backed by a source page in this wiki** — its claims were verified against live sources on 2026-10-17 (recorded in `.workbuddy/memory/concept-radar/2026-10-17.md`, candidate 1; ledger row **10-17A**). Remove this banner when the material is ingested and human-reviewed, and move the source slug into the frontmatter `sources` field.

**The assumption this page never stated.** Everything above — split by purpose, intent gate, source router, [[Provenance]] on every item, [[Abstention]] without evidence — presupposes that memory is **addressable text**: something you can enumerate, point at, open, and cite. The 2026-10 family below does not improve on that assumption; it **removes** it.

| Carrier | Form | Addressable? | Where the wiki treats it |
|---|---|---|---|
| **历史文本** | episodic / semantic / procedural stores | ✅ | this page |
| **任务对象** | the artifacts the task operates on | ✅ | ledger row 10-13 (two carriers × four paths) |
| **连续载体** | learned vectors · soft tokens · weight updates | ❌ | **this section** |

- **① Memorilla** — `arXiv:2610.21375` (**2026-10-15**; Fallahpour / Idehpour / Kothapalli / Mounier / Wu / Pardis / **Jure Leskovec** — Stanford · Toronto · UPenn · MIT · Vector · Arc). A frozen encoder turns each document into a reusable embedding; learned memory slots read **the whole collection *plus* the question** and emit a fixed budget of **16 memory tokens** placed directly into the **frozen LLM's input embedding space**. Highest average across eight benchmarks **49.68**, leading Mem0 / MemoRAG on five; document tokens down **394×** on average (**>4,000×** on NarrativeQA); **FactKG 84.33% vs full-context 80.43% at 108× fewer tokens** — i.e. it *beats* putting everything in; 512 documents **0.74 s vs 19.9 s** (single H100-80GB, batch 1, `Qwen3-8B`); TextWorld success **18.6% → 24.2%**.
- **② REMORY** — `arXiv:2610.11287` (**2026-10-08**). Learned **soft tokens appended *after* the summary**, described as "an analogue of a residual connection along the sequence dimension". On SummHay it approaches the full-context joint score at **5.2%** of input positions; provenance score rises while insight coverage is nearly unchanged; repeated tool outputs and tool errors drop on BrowseComp / Terminal-Bench 2.1.
- **③ Cortex** — `arXiv:2610.20399`. Distils the context gain into **mergeable low-rank / FFN updates**: a 14B model retains **88.9%** of the context gain and **99.8%** of off-target performance after **50** consecutive edits.

⇒ The three members jointly cash out a sentence already in circulation: context has **three exits — delete it ([[Compaction]]) / index it (this page) / compile it into the weights (this section)**. The third exit had **no page in this wiki**.

- **All three members above are scored on aggregate accuracy — and that ruler has now been shown to be blind per-decision** *(added 2026-10-21, ledger row 10-20A; draft annotation, pending ingest — same banner as this section)*. In latent / soft-token memory the learned prefix earns its gain mainly by **revising the model's default action**, and when that revision is **unscoped** it repairs errors while damaging **8–13%** of decisions that were already correct; the authors state it plainly: **“Overall accuracy metrics hide these losses.”** ⇒ Memorilla's **49.68**, REMORY's **5.2%** of input positions and Cortex's **88.9%** are all of the aggregate kind. **Not a refutation of the three members — a statement about what their ruler cannot see.** Full variable and its counterfactual (scoped revision ⇒ **5.6%**, with *more* errors repaired) sit in the open experiment in [[MemoryGovernance]].

> **The load-bearing sentence: you cannot cite a vector.** Continuous memory has **no address**, so four wiki rules lose their *conditions of statement* at once — [[Provenance]] (must hang on **a record**) · [[CitationLock]] ("cite only what you actually opened" — there is no *opened*) · [[Abstention]] ("abstain when you didn't open it" — no object to abstain about) · [[MemoryGovernance]]'s four bottom lines (presuppose memory is enumerable — three of the four become unstatable). **The rules are not refuted; they stop being applicable** — which is harder to notice than being refuted.

**Boundaries.**
- **vs [[Compaction]]** — REMORY positions itself explicitly as **residual compensation for the summary**: a second leg, not a replacement. Compaction asks *what to drop*; this asks *what was lost in the dropping*.
- **vs [[ContextRot]]** — ContextRot says *"it fits but doesn't get used"*; this family answers *"don't put it in at all"*. Two exits on the same failure axis, not rival claims.
- **vs [[ContextEngineering]]** — that page's "minimum high-signal **token** set" is rewritten literally here: **the signal handed to the model need not be tokens at all**.
- **vs [[MemoryGovernance]]** — that page governs a bank you can list; this section is the case where you cannot. See the scope note and the open experiment there.

⚠️ **Counter-evidence, must sit beside the numbers:** every figure is **author-reported**; Memorilla's mainline runs on a **single frozen `Qwen3-8B`** (cross-backbone generalisation unproven); and **none of these benchmarks track fact evolution** — which is precisely what the FEB-30 instrument measures, and where compressed continuous storage is most likely to fail. ⇒ **open experiment**, see [[MemoryGovernance]].

## See Also
- [[agent-memory-provenance]] — primary source (the reading discipline)
- [[memory-lifecycle]] — second source (lifecycle, forgetting, decision-rights)
- [[MemoryGovernance]] · [[MemoryPoisoning]] — the second half of a memory's life
- [[Provenance]] · [[CitationLock]] · [[Abstention]] — the reading discipline
- [[DyadMem]] · [[LongMemEval]] — staged vs end-to-end memory benchmarks
- [[MemGPT]] · [[AgentZeroMemory]] · [[Zep]] — systems
- [[ContextEngineering]] — writes/reads are context-engineering decisions
- [[LLMContext]] — the bounded working set it complements
