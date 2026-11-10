---
title: "Skill"
type: concept
tags: [anthropic, skill, progressive-disclosure, design-pattern, self-evolving-skills]
sources: [skill]
last_updated: 2026-11-10
---

# Skill

An organized folder of instructions, scripts, and resources that Claude loads on demand when a task is relevant — turning a general model into a domain expert.

## Definition
Per [[skill]] source: Same Skill folder usable across Claude app / Claude Code / API / Agent SDK. Released as an open standard after 2025-12.

## Core Mechanism
- **Progressive disclosure (3 layers)**:
  - Layer 1 — YAML metadata (name + description) always in system prompt
  - Layer 2 — SKILL.md body loaded when task relevant
  - Layer 3 — scripts and referenced assets loaded on demand
- **Auto relevance check** — Claude scans metadata descriptions each turn; user doesn't "pick"
- **Code as first-class** — scripts allow deterministic operations (sort, render PDF, generate chart)
- **Cross-product portability** — same Skill works in multiple products

## Boundary
- **Not = prompt template** — template is per-conversation; Skill is cross-conversation, version-controlled, multi-product-shared
- **Not = fine-tuning** — Skill changes context, not model parameters
- **Not = MCP** — MCP = "connect the tool" (interface standard); Skill = "teach the model how to use the tool"

## Practical Use
| Use Skill | Use Prompt / Project |
|---|---|
| Cross-team / multi-product domain workflow | One-off, temporary input requirement |
| Complex tasks needing executable scripts | Static reference knowledge (glossaries) |
| Dynamic relevance activation | Always-on rules for every session |

## Skills stop being hand-curated — the source changes, the structure doesn't *(ledger row 11-10A; applied 2026-11-10)*

> **Draft annotation, pending ingest.** Not yet backed by a source page in this wiki — verified against live sources on 2026-11-10 (recorded in `.workbuddy/memory/concept-radar/2026-11-10.md`, candidate 1; ledger row **11-10A**). Remove this banner when the material is ingested and human-reviewed, and move the source slug into the frontmatter `sources` field.

This page defines a Skill as an **organised folder a developer writes and curates**. Within one week (2026-11-02 → 11-05) three teams that do not cite each other each shipped a version in which the library **writes and revises itself from execution experience**:

| System | What it compiles into a Skill | Measured (author-reported) |
|---|---|---|
| **ScienceCUA** (`arXiv:2611.03238`, Daiqiang Li + 9, cs.AI, v1 2026-11-02) | Software documentation → inferred operational trajectories → reusable Skills; command catalogs kept separately as References | Initial Skills + References **+7.23 pp** task success; execution-guided self-evolution raises total gain to **+17.12 pp**. ScienceBoard-VE keeps evolution and test tasks **disjoint** so the library cannot memorise the exam. |
| **Evolver** (`arXiv:2611.07595`, Haoyang Zhang + 5, cs.SE + cs.AI, v1 2026-11-05) | Agent exploration traces → structured **Gene** assets, retrieved and revised by feedback, on top of existing harnesses | 320 paired executions: **83.13% → 87.50% (+4.38 pp)** success, tokens **−24.24%**; among 265 both-success pairs **−17.57%** tokens. Tested on Claude Code and Codex. |
| **EvoML** (`arXiv:2611.04180`, Zixiao Zhao + 9, cs.AI, v1 2026-11-03, ICSE 49th) | A post-run **Curator** consolidates recovered scripts and guidance into the skill library, behind a validation-gated harness | Full automation and best final model quality on eight datasets / six task types (qualitative in the abstract). |

**The shared design answer is the admission gate.** ScienceCUA updates the library *only after repeated validation in real environments*; Evolver is feedback-guided; EvoML is validation-gated. That is precisely the governance response to the 11-07A finding that **a benign procedural asset has no anomaly to detect** (accuracy and unsafe-operation rate rose by the same +10.3 pp): detection-style defences cannot help, only a position-type check **before the asset is admitted** can.

- **What does not change:** the loaded artefact is still imperative procedural guidance activated on demand. So the 11-07A capability–risk co-origin conclusion **transfers directly**, even though all three papers measure only the capability side.
- **What does change:** authorship. Curated assets have a accountable owner; self-evolving ones are written by a run, and none of the three answers **who deletes** — libraries only grow, the same read-range > write-range problem recorded for EvoGroup (11-07B).
- **Boundaries:** vs 11-09C (forge_dc) — that compiles **user corrections** into behavioural RULEs ("never make this mistake again"); these compile **execution traces** into task capability ("do this better"). Both are experience → imperative asset, with different input signals. vs [[LongTermMemory]] — a memory entry stores a fact; a Skill stores a procedure. vs Anchor (`arXiv:2611.10382`) — memory admission vs skill admission, the same question ("what entitles this experience to be stored?") on two asset types.

⚠️ **Limits:** all three are **abstract-level** citations (HTML tables not opened); each uses its **own self-built benchmark** and the gains are not on comparable scales (+17.12 total over baseline vs +4.38 on a paired diagnostic set vs a qualitative eight-dataset claim) — **do not compare them horizontally**. None tests the safety side; the risk-transfer statement is an inference from 11-07A, not an experiment in these papers.

## See Also
- [[Agent]] — Skill is the unit that empowers Agents
- [[ProgressiveDisclosure]] — load-on-demand mechanism
- [[LLMContext]] — Skills operate within bounded context
- [[MCP]] — complementary tool-connection standard
- [[Anthropic]] — Skill is an Anthropic product feature