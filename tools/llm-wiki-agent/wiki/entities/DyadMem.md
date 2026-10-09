---
title: "DyadMem"
type: entity
tags: [benchmark, memory, evaluation, staged-annotation]
sources: [memory-lifecycle]
last_updated: 2026-10-09
---

# DyadMem

A **staged** long-term-memory benchmark (Tao et al., arXiv:2610.03020, 2026-10-02; NTU / NUS / HKU / StepFun) that splits an agent's durable memory into four explicitly measured stages — **Capture → Update → Recall → QA** — and places **gold annotations at every stage** rather than only at the final answer. Scale: **3,065 episodes / 50,961 sessions / 61,210 QA**, spanning **16 open-weight + 4 closed** models.

Its contribution to the wiki is **diagnostic, not ranking**. Because end-to-end QA scores stir four different qualities together, DyadMem's design makes it possible to say *which stage is broken* rather than *the agent scored X*.

## Key findings cited by [[memory-lifecycle]]
- **Gold-Memory is strong; Full-Pipeline collapses.** Frontier models perform well when handed the correct memory (Gold-Memory) and drop sharply once they must capture, update and recall for themselves (Full-Pipeline). This is the wiki's clearest evidence that the bottleneck is the **quality of the four actions**, not whether the window can hold the state — and it is why “a bigger context window” is not an answer to memory problems.
- **Systematic, per-stage defects in frontier models:** low **Capture** recall (things that should have been written never were), **incomplete Recall** (one of three relevant memories returns), and **unsafe deletion** (facts still under reference get removed). Note that the last two are *opposite ends* — DyadMem quantifies both, so “forgetting is a capability” and “deletion is dangerous” are measured rather than asserted.
- **URAM — “same user, different agents should remember different things.”** Bounds the naive assumption that one memory bank is correct for every agent serving the same principal.

## Connections
- [[MemoryGovernance]] — DyadMem is the measurement instrument for the four actions that page governs
- [[memory-lifecycle]] — the source page that cites it
- [[LongMemEval]] — the **end-to-end QA generation** DyadMem was built to correct: LongMemEval measures five abilities from the outside, DyadMem opens the pipeline and annotates each stage
- [[LongTermMemory]] — the store whose benchmark evidence this entity sharpens
- [[Abstention]] — appears here as *recall-incompleteness → prefer abstention*, the pipeline boundary case
