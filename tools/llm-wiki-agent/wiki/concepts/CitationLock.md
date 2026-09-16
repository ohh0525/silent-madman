---
title: "Citation Lock"
type: concept
tags: [agent-memory, provenance, hallucination]
sources: [agent-memory-provenance]
last_updated: 2026-09-16
---

# Citation Lock

The reading discipline in which an answer may cite only evidence its reader *actually opened* during this reasoning turn — making fabrication structurally impossible rather than merely discouraged.

## Mechanism (per [[agent-memory-provenance]])
- Every answer is read under a citation lock: the set of citable evidence is exactly the set the agent opened, not everything retrievable.
- Combined with [[Provenance]] (every learned item carries origin/timestamp/evidence), fabrication is excluded by construction.
- Knowledge updates are explicit: newer facts *supersede* older ones (an explicit `superseded_by` link), rather than silent overwrite or unbounded contradiction accretion.

## Why It Matters
- Turns "don't hallucinate" from a prompt-level plea into an architectural invariant.
- Fixes the "temporal contradiction" failure: a flat vector store recalls both "Adidas" and "Nike" with no notion of which is current; a citation-locked, time-aware store returns only what is true now, with its source.
- Pairs with [[Abstention]]: when the opened evidence set is empty, the correct output is "I don't know".

## See Also
- [[agent-memory-provenance]] — primary source
- [[Provenance]] — the write-side constraint this complements
- [[Abstention]] — the fallback behavior
- [[LongTermMemory]] — the system enforcing it
- [[Zep]] — vendor implementation on temporal context graphs
