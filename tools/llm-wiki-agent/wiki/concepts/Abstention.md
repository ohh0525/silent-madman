---
title: "Abstention"
type: concept
tags: [agent-memory, abstention, reliability]
sources: [agent-memory-provenance]
last_updated: 2026-09-16
---

# Abstention

The ability of a memory system to refuse to answer when it lacks sourced evidence — treating "I don't know" / "unknown" as a correct state transition rather than a failure.

## Mechanism (per [[agent-memory-provenance]])
- Built into the reading discipline: if no sourced evidence was opened, the system returns an abstention instead of a plausible guess.
- One of LongMemEval's five core long-term-memory abilities (information extraction, multi-session reasoning, temporal reasoning, knowledge updates, **abstention**).
- Depends on [[Provenance]] and [[CitationLock]]: without them the system cannot tell an established sourced fact from something merely asserted once.

## Why It Matters
- The dangerous failure is not a wrong answer per se, but confidently stating something that cannot be traced to a source — poisoning future plans.
- Benchmark evidence ([[LongMemEval]]): abstention is one of the abilities where commercial assistants and long-context LLMs degrade most.
- "Abstention is not the system being dumb" — hard-answering with a reasonable-sounding guess is what writes hallucination into the future.

## See Also
- [[agent-memory-provenance]] — primary source
- [[CitationLock]] · [[Provenance]] — the enabling constraints
- [[LongMemEval]] — benchmark that scores abstention
- [[LongTermMemory]] — the system exercising it
