---
title: "AgentZeroMemory"
type: entity
tags: [system, memory, provenance, state-of-the-art]
sources: [agent-memory-provenance]
last_updated: 2026-09-16
---

# Agent Zero Memory

A provenance-aware long-term memory system (Ming Wu, Pengyuan Zhu, Zero Labs; arXiv:2608.29606, 2026-08-30). Distills a user's conversations, files, and connected sources into **three parallel memories** — an episodic Memory Events timeline, an associative entity–event knowledge graph, and a semantic, curation-locked Hierarchical Documentary Memory (HDM).

Sets state of the art on [[LongMemEval]] (95.60%) and LoCoMo (93.60%), improving on the strongest prior systems by +0.73 / +1.10 points. Across 8 backbones, accuracy varies only 3.4 points while per-query cost varies ~30× — the "memory-driven, not model-driven, quality" signature. Implements [[Provenance]], [[CitationLock]], and [[Abstention]] as first-class design postulates.
