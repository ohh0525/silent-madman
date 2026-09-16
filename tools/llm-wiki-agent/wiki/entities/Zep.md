---
title: "Zep"
type: entity
tags: [vendor, memory, temporal-graph]
sources: [agent-memory-provenance]
last_updated: 2026-09-16
---

# Zep

Vendor of an agent-memory platform built on **temporal context graphs** (a "Context Lake" of governed context graphs). Framed in its hallucination-reduction writing as pairing *agent memory (provenance + temporality)* with RAG and abstention as the first-line controls against hallucinated / stale answers.

Illustrates [[CitationLock]] and [[Provenance]] in practice: inputs are ingested, entities and facts extracted with validity windows and provenance, and retrieval returns only the relevant, currently-valid slice — so a changed fact (e.g. "Adidas" → "Nike") is answered with what is true now, not both.
