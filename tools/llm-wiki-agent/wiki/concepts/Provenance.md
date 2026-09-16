---
title: "Provenance"
type: concept
tags: [agent-memory, provenance, reliability]
sources: [agent-memory-provenance]
last_updated: 2026-09-16
---

# Provenance

The design constraint that every stored fact must carry its origin, timestamp, and an evidence pointer — so the system can always answer "why is this believed?" and can grade trust by *source*, not by *relevance alone*.

## Mechanism (per [[agent-memory-provenance]])
- A memory is not a string; it is a record answering: what claim is stored, which source produced it, is it fact/preference/inference, when observed or last verified, and what condition should replace or expire it.
- Write-time gate: reject unknown or untrusted sources; grade trust by origin (`human` / `verified_tool` / `self_inferred`), and the agent does not get to fully trust its own guesses.
- Read-time filter: drop expired / low-trust entries *before* they reach the context window; a retrieved memory without source and time metadata is "just a persuasive sentence occupying expensive context".

## Why It Matters
- Kills two compounding failure modes: **stale facts** (no TTL ⇒ presents a 3-week-old value with the same confidence as a 30-second-old one) and **unbounded growth** (append-only memory buries the right answer under near-duplicates).
- Makes trust *meaningful*: when every record carries its source, retrieval filters can act on it; without it, trust becomes uniform and therefore meaningless.
- Directly matches the silent-madman repo's own "人工核查承诺" instinct — nothing enters as fact without a traceable source.

## See Also
- [[agent-memory-provenance]] — primary source
- [[LongTermMemory]] — the store that carries provenance
- [[CitationLock]] — the read-side companion
- [[Abstention]] — what happens when provenance is absent
