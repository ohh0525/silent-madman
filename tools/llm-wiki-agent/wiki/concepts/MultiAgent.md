---
title: "Multi-Agent Orchestration"
type: concept
tags: [multi-agent, test-time-communication, orchestration, verifier, cross-contamination]
sources: [multi-agent]
last_updated: 2026-09-26
---

# Multi-Agent Orchestration (多智能体协作)

Multiple agents with **independent context windows** working on one goal: exchanging **verified** partial results, failure paths and intermediate scores through a shared workspace, so that **less total compute beats best-of-k independent sampling** — **provided a verifier exists**. Without a verifier, or under tight compute, communication overhead exceeds its gains and independent agents do better.

## Mechanism (per [[multi-agent]])
- **The exchange object is verified progress, not messages** — k agents, same goal, same compute budget, no preset roles, no central orchestrator; a shared workspace holds partial results, failure paths and code. *The gain comes entirely from building on confirmed breakthroughs and not re-walking confirmed dead ends — not from workflow design.*
- **The verifier is the precondition of the gain.** Only when "who actually progressed" can be judged cheaply does "build on others' progress" work. On LP85, 64 independent attempts all failed while team@5 solved 65% — progress was verifiable. *This turns "should we go multi-agent" from taste into a predicate: first ask whether the task has a verifier.*
- **The counter-result ships with the result.** ARC-AGI-3: team@3 = best@13, team@5 = best@33 (≈4.3× / 6.6× equivalent compute); polyomino packing team@3 SOTA 0.945; MNIST 4-agent classifier 1,957 bytes @ 99.4%. But the paper's own abstract: the method "**fails without verifier or low compute**". *Cite the gain together with its boundary condition, or you are quoting a conditional result as a panacea.*
- **New failure surface: cross-contamination (互相污染).** One agent's unverified conclusion gets inherited by peers as a premise — a failure mode absent from the single-agent world, landing on [[Provenance]]'s extension line: team trust must cover the **verification status of peers' conclusions**, not just fact origin.

## Boundary
- **Not subagents** — subagents are threads *inside* one agent (returning a summary to the main context); multi-agent is a **peer team**, members each holding the full goal and an independent window. Claude Code Projects nests both: threads are the team, and each thread can spawn its own subagents.
- **Not shared memory** — [[LongTermMemory]] is one agent's persistence **across sessions** (time dimension); multi-agent is shared state **across agents at one moment** (space dimension). Complementary; the governance of team-shared memory is their open intersection.
- **Not a replacement for [[ContextEngineering]]** — context engineering places content *within* one window; multi-agent decides what to exchange *between* windows. The latter is the former's cross-window extension ([[Compaction]]'s "clean-window subagent returning 1–2k tokens" is the seed).
- **Not "more agents is always better"** — the paper carries its own counter-example (no verifier / tight compute → independent wins); the product carries its own cost (threads each burn quota). A bounded tool, not a free lunch.

## Why It Matters
- **It is the wiki's first "between agents" page.** All 39 prior pages and both connection diagrams describe a single agent; this page opens the space dimension the wiki had never covered.
- **September 2026 assembled three grades of evidence at once:** a reproducible experiment (team@k vs best@k, Microsoft Research + UC Berkeley), a product entry point (Anthropic's Claude Code Projects: coordinator → parallel cloud threads → shared memory → ordinary merge conflicts, with honest self-declared limits — quota per thread, cloud-only launch, CI/tests/human review as the integration boundary), and decentralised scale (Agensh: 1,024 agents, no central orchestrator, pandoc 33.89% → 55.06%). The question moved from *can multi-agent work* to *when is it worth it and who pays the coordination cost*.
- **The verifier predicate is portable.** "First find a cheap way to judge correctness, then form the team" is the single most reusable sentence in the material.
- **Evidence-grade honesty:** the team@k numbers are secondhand (AlphaSignal's report of the paper; arXiv not opened), Agensh is secondhand, Claude Projects' shared memory has "no detailed performance evaluation" — direction-and-magnitude grade throughout; verbatim citation requires the primary sources.

## See Also
- [[multi-agent]] — source
- [[Compaction]] — whose clean-window-subagent note this page promotes from footnote to mainline
- [[Provenance]] — extended by cross-contamination: peer conclusions need verification status
- [[AgentHarness]] — multi-agent as a productised harness capability (subagent scheduling, duty ④)
- [[ContextEngineering]] — intra-window placement vs inter-window exchange
- [[Agent]] — the single-agent world this page extends
- [[Anthropic]] · [[OpenAI]] — the two productisation paths (Projects coordinator; Agents API subagent flag)
