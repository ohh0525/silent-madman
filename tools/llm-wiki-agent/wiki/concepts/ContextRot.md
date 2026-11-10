---
title: "Context Rot"
type: concept
tags: [context-engineering, degradation, anthropic, validity-vs-quantity]
sources: [context-engineering]
last_updated: 2026-11-10
---

# Context Rot

The phenomenon in which a model's ability to accurately retrieve information from its context *continuously declines* as the number of tokens in the window rises. Named by Anthropic.

## Mechanism (per [[context-engineering]])
- Informally called "context rot" in Anthropic's engineering writing.
- It is a *slope*, not a cliff: the model does not "crash" — it grows progressively more likely to misread long inputs.
- Root cause is the same architectural fact as [[LLMContext]]: attention is a finite budget spread across n² token-pair relationships.

## Why It Matters
- Explains why "open the window to 1M tokens and it fits everything" is a false solution — fitting ≠ using.
- Justifies [[ContextEngineering]] as active *curation* rather than passive accumulation.
- Corroborated downstream by [[LongMemEval]]: long-context models lose 30–60% accuracy when forced to read full 115K-token histories.

## Validity vs quantity — rot has a twin the token count cannot see *(ledger row 10-10; applied 2026-11-10)*

> **Draft annotation, pending ingest.** Not yet backed by a source page in this wiki — verified against live sources on 2026-10-10 (recorded in `.workbuddy/memory/concept-radar/2026-10-10.md`, candidate 19; ledger row **10-10**); abstracts re-checked alive on 2026-11-10. Remove this banner when the material is ingested and human-reviewed, and move the source slug into the frontmatter `sources` field.

**The twin failure this page's variable cannot express.** Everything above prices degradation in **tokens**: attention is a finite budget, the slope declines with length, fitting ≠ using. That is the **quantity** axis. There is a failure with the *same symptom* — the agent asserts, with full confidence, things that are not true of the current state — whose cause is not quantity at all: the observation **went stale**. A forty-token stale observation is exactly as wrong as a four-hundred-token one; no amount of window management fixes it, because **the token count was never the variable**.

- **Concord** (`arXiv:2610.05281`, **AgenticOS Workshop @ SOSP 2026**, v2) names the object — **incoherence in volatile agent context**: the sources behind tool observations change (users, other agents, external tools) while the model retains only the stale content, and "existing agent runtimes provide little support for notifying the model" — the reuse proceeds as if the observation were current. The fix lives on the **validity** axis (link observation → source, detect change, update/annotate/suppress before reuse), and it *pays for itself* (**46.4% fewer tokens** than the strongest non-oracle baseline) — the two axes are not rivals; fixing validity shrinks quantity too.
- **Second-hand signal (must be labelled as such):** the **STALE** benchmark reports models retrieve updated facts **77%** of the time but mark only **~3%** as worth acting on; asked directly, **92%** identify staleness — with an implicit dependency, **30%**. The rot-looking symptom and the validity failure are separable, and the model cannot tell them apart from the inside.

**Boundaries.** vs this page's own mechanism — length/position vs **content validity**; shortening the window (the standard rot response) does not touch staleness, and can *hide* it (less history ⇒ fewer anchors to notice a contradiction against). vs [[Provenance]]「Source ≠ present validity」(same row, landed the same day) — that page holds the **observation→source link and the instrument**; this page holds the **differential diagnosis**: before treating "the agent is wrong about current state" as rot, check whether the content was ever going to stay true. vs [[LongTermMemory]]「Re-validate before reuse」— that is the memory-side duty; this is the window-side symptom book. Not a fourth mechanism of rot — a **sibling variable** with a shared symptom.

⚠️ **Limits:** first-party material is workshop-preprint, abstract-level, benchmark constructed by its authors; the STALE numbers are **second-hand** (not independently reproduced) and cited only to name the knowing/noticing gap.

## See Also
- [[context-engineering]] — primary source
- [[ContextEngineering]] — the response to it
- [[LLMContext]] — capacity ceiling vs. effective capacity
- [[Transformer]] — n² attention cost as the root
