---
title: "Memory Governance"
type: concept
tags: [agent-memory, memory-governance, memory-lifecycle, forgetting, learned-policy]
sources: [memory-lifecycle, agent-memory-provenance]
last_updated: 2026-10-09
---

# Memory Governance

The discipline of treating an agent's durable memory **not as a store but as four actions that each fail differently** — Capture → Update → Recall → QA — and of answering, explicitly, the question every design otherwise answers by accident: **who holds the decision rights over what is written, when it is retrieved, and when it is deleted.**

Distinguish it from the two neighbours it is most often confused with: [[LongTermMemory]] asks *where does durable state live and how is it read credibly*; Memory Governance asks *how does it change over time, and under whose authority.* The framing question is not “can we store it?” but **“when should we let it be forgotten — and who is allowed to decide?”**

## The four actions (per [[memory-lifecycle]])
| Action | What it does | Characteristic failure |
|---|---|---|
| **Capture** | Write new memories out of this session | Systematically **low recall** — the thing you changed last week never got written |
| **Update** | Reconcile with the existing bank | **Coexistence instead of supersession** — two publication dates side by side, and the agent argues with itself |
| **Recall** | Select entries that are still valid | **Incomplete recall** — one of three relevant memories comes back |
| **QA** | Answer from the evidence | Answer looks right while the bank underneath is broken |

The reason to split them is diagnostic: an **end-to-end QA score stirs four different qualities together**. A correct answer can come out of a broken bank (lucky); a wrong answer tells you nothing about *which* stage to repair. [[DyadMem]] is the benchmark that makes the four stages separately measurable — and its headline result is a **measurement artefact, not a model ranking**: frontier models are strong **given gold memory**, and collapse once they must run the **full pipeline** themselves.

## Forgetting is a capability, not a failure
- **“Failed to forget” is now a deductible score.** Memora's **FAMA** = recall score − **stale-dependency penalty** (it explicitly penalises reliance on deleted or superseded memories). This turns *“the agent is quoting a superseded runbook as current”* from rhetoric into a number.
- **The opposite failure must also be measured.** **Unsafe deletion** — removing a fact that is still under reference — is the other end, and DyadMem quantifies both.
- **Retention is per-type, never one global TTL.** The three stores [[LongTermMemory]] defines do not expire alike: episodic (high volume, timestamp-bound, expires first) → semantic (durable; the main **merge** target) → procedural (lowest volume, highest value, retained longest, hardest to prune).
- The sharpest seam: **deletion vs [[Provenance]]**. Provenance wants every fact to keep origin + time + evidence so it stays auditable; the right to erasure wants the same fact removed at the root. Deleting it **breaks the citation chain** — so the deletion itself must leave a trace (a receipt, a failure list, a rollback-capable snapshot).

## The load-bearing variable: who decides
There are exactly three classes of decider, and picking one is the design decision that matters.

| Decider | Write / retrieve / delete | Representative evidence | Core weakness |
|---|---|---|---|
| **Human-written rules** (today's default) | Thresholds, TTL, extraction counts, top-k hard-coded by an engineer | Layered memory (resident core + external retrieval + explicit forgetting policy) is the 2026 production form | Rules have **no judgement about what counts as stale**; every new domain needs re-tuning |
| **Trained policy** (2026's new answer) | **ADD / UPDATE / DELETE / NOOP placed in the action space**, trained by RL on task-success reward | Memory-R1 (152 QA pairs ⇒ LoCoMo F1 **+68.9%** vs Mem0); ATMem (cost-aware reward + STR-GRPO; **76.6%** on AndroidWorld at ≈**1/29** the parameters) — six independent teams | **None deployed in production**; benchmarks exclude distribution shift and adversarial input; no single system owns write + retrieval + transformation |
| **Attacker** (the decider nobody wants) | Write timing and content chosen by the injector | **PMPA** and **Darktrace** — see [[MemoryPoisoning]] | **The fix is vendor-side**, so the defending operator cannot deploy it |

> **The rule that makes this page worth having: if memory has no owner, the owner slot does not stay vacant — it flows to whoever wants to exploit it.**

The middle row is why this is a *2026* page: the whole point of putting `DELETE` **into the action space** is that *“when is this stale?”* stops being a hand-tuned constant and becomes a learned decision that the task-success reward can correct.

## The four governance bottom lines
1. **Auditable** — every write / supersede / delete traceable like a git commit (who, when, on which source). This is [[Provenance]]'s instinct, applied to *change* rather than to *storage*.
2. **Rollbackable** — deletion is a real, recorded, provable operation with a version history, not an invisible manual sweep of an undocumented store.
3. **Permissioned** — **who may write to shared memory** managed as explicitly as database permissions (this is the *governance* half of the wiki's long-open “multi-agent shared memory” question).
4. **Signature-verified** — against forged-history attacks the only root fix is **cryptographically signed model replies validated server-side every turn**. Until that ships, the local session-history store must be treated as a **security-sensitive file**.

Bottom lines 1–3 govern *your own mistakes*; bottom line 4 governs *someone else's malice*. **The reliability discipline and the security discipline merge at the memory layer** — which is why [[MemoryPoisoning]] is a decider in the table above rather than a separate topic.

## Boundaries
- **vs [[LongTermMemory]]** — that page is the **first half** of a memory's life (store it, split it by purpose, read it credibly); this page is the **second half** (update, forget, decide). Neither subsumes the other: you can have a perfectly sourced bank that is also a governance disaster.
- **vs [[Compaction]]** — compaction is **inside** the window, per turn, lossy; governance is **outside** it, across sessions, offline, and does not participate in the current inference turn. Adjacent in one direction only: anything compaction drops that still matters should *land in long-term memory rather than evaporate*.
- **vs [[Provenance]] / [[CitationLock]] / [[Abstention]]** — those are **entry and exit discipline** (writes carry origin; cite only what you opened; abstain without sourced evidence); this is the **whole lifecycle in between**. Not redundant: **a clean entry does not imply a clean lifecycle** — PMPA's payload arrives inside a benign document wearing legitimate provenance. (`ABSTAIN` on incomplete recall is this page *reusing* [[Abstention]], the way [[ContextEngineering]] reuses [[ProgressiveDisclosure]].)
- **vs a bigger context window** — window is capacity; governance is structure and discipline. The counter-evidence is directional and specific: **Gold-Memory strong ⇒ Full-Pipeline collapse** means the bottleneck is the four actions, not the fit.
- **vs [[ContextEngineering]]** — context engineering decides what goes on the desk **this step**; governance decides what survives **between** sessions.
- **vs [[MemoryPoisoning]]** — poisoning is not *one more failure mode of a broken action*; it is **the third decider**, i.e. a claim of authority over the same three decisions. That is why it is treated as an owner, not as a bug.

## Why It Matters
- It reframes memory from a **personalisation feature** to a **reliability subsystem**: write one wrong entry and every future plan runs on bad input; poison one entry and the attack recurs in every later session.
- It supplies the missing pass over [[LongTermMemory]]: the wiki could already say *where* memory lives and *how* to read it honestly; it could not yet say **how it expires, and who is entitled to expire it.**
- It closes the “governance side” of the shared-memory question [[MultiAgent]] left open (verified ✅ vs speculation inside a team's shared memory; who may write what), and it makes the security and reliability disciplines meet on one object.

## See Also
- [[memory-lifecycle]] — primary source (2026-10-06 material, ingested 2026-10-09)
- [[agent-memory-provenance]] — the entry/exit discipline it extends
- [[LongTermMemory]] — the store whose second half this page governs
- [[MemoryPoisoning]] — the third decider
- [[Provenance]] · [[CitationLock]] · [[Abstention]] — adjacent reading discipline
- [[Compaction]] · [[ContextEngineering]] · [[LLMContext]] — the in-window neighbours
- [[DyadMem]] — the staged benchmark · [[LongMemEval]] — the end-to-end generation it corrects
- [[MemGPT]] · [[AgentZeroMemory]] · [[Zep]] — the systems whose next question is governance
- [[AgentSandbox]] — containment bounds what the agent can touch; governance bounds what it will remember
