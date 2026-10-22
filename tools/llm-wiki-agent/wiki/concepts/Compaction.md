---
title: "Compaction"
type: concept
tags: [context-engineering, long-horizon, anthropic, trust-boundary, serialization, cache-invalidation]
sources: [context-engineering]
last_updated: 2026-10-22
---

# Compaction

One of the three long-horizon context techniques: summarize the conversation history and restart from the summary, preserving only architectural decisions, open questions, and the most recently accessed files.

## Mechanism (per [[context-engineering]])
- **Compaction** — summarize history → restart with a compacted context.
- **Structured notes** — the agent writes progress to a file *outside* context (Claude Code's todo list is this pattern).
- **Sub-agents** — a dedicated agent digs into a clean window and returns only ~1,000–2,000 high-density tokens to the main agent.

## Why It Matters
- Tasks spanning tens of minutes to hours cannot fit in any window; state must live outside the dialogue.
- Improves *recall* first (don't drop the load-bearing decision), then iterate on *precision* (remove redundancy).
- Over-compression can lose nuance, but doing nothing is worse — the agent simply fails at the limit.

## Compaction is a trust boundary *(ledger row 10-22A; applied 2026-10-22)*

> **Draft annotation, pending ingest.** Not yet backed by a source page in this wiki — verified against live sources on 2026-10-22, recorded in `.workbuddy/memory/concept-radar/2026-10-22.md` (candidate 1). Remove this banner when the material is ingested and human-reviewed, and move the source slug into the frontmatter `sources` field.
>
> 🔴 **Must travel with every citation of this section: preprint, not peer-reviewed; single institution (Pixee, a code-security vendor); the attack surface exists ONLY in flattening harnesses — the four role-typed harnesses measured 0%. Do not generalize to "all harnesses are affected."**

This page has described compaction as a **window-internal, per-turn** technique — `overview.md` states the split in so many words: *governance runs outside the window ... where Compaction runs inside and per-turn*. **Compaction Laundering** (`arXiv:2610.29869`, submitted **2026-10-21 15:24:23 UTC**; 29 pages / 5 figures; source, raw data and a recorded end-to-end demo released) argues **that cut is in the wrong place: compaction is itself a governance boundary.**

**Mechanism — the origin is destroyed before the model sees the text.** To feed a summarizer, the harness **flattens a typed conversation into one plain string**, marking origin with inline text labels such as `[User]:` / `[Tool result]:`, and **does not escape** identical labels occurring inside untrusted content. The original is then discarded and the summary *becomes* the memory ⇒ a forged one-line `[User]:` approval **launders into a genuine user instruction**.

| Harness class | Forged approval laundered into memory |
|---|---|
| **Flattening** — pi / opencode / Cline / Aider / OpenHands (5) | **87–100%**, sustained out to a ~908,000-token window |
| **Role-typed** — Codex / Gemini CLI / Qwen Code / Continue (4) | **0%** |

**End-to-end.** The laundered standing approval drove a real tool-executing agent to run an attacker-controlled `curl | sh` — **~50%** on the live pi TUI versus **0%** in the matched clean control. The same channel reliably steers the agent's plan away from a named file ⇒ **it can blind code review to an implanted backdoor**.

**The correction this row makes to the prior literature — and to this page.** Prior work frames this failure as a **limitation of the model** (the model cannot reliably tell where content came from). In flattening harnesses the origin is destroyed *before the model sees the text* ⇒ **"Susceptibility is therefore a property of the serialization strategy, not of the model."** This refines [[Provenance]]'s 2026-10-21 boundary (a **discipline** vs an **enforcement point**): the missing column is that the failure had been **attributed to the wrong agent** — on this evidence it is not a reading failure at all.

**Both ends of the fix.** Because the origin is destroyed **deterministically in code**, **no prompt-level defence can recover it**. The authors' **code-level origin check** caught **77%** of laundering while degrading only **2%** of legitimate summary content (self-measured); the serializer-side fix is to **escape role labels before flattening**.

**Why it lands here, not on [[MemoryPoisoning]].** That page is the **write-side** surface. This row supplies the step `overview.md` names as an open item — **how transient injection becomes durable memory**: laundering *is* that step. It is also heritable: **"Derivative agents inherit it"** — everything built atop someone else's compaction inherits its serialization.

**Applicability limit worth stating.** The whole chain presupposes that **the original is discarded after summarization**. Retain the original and there is nothing left to launder — which is the other end of the argument recorded under [[MemoryGovernance]] (ledger row 10-22B).

### Scope note — compaction's second cost: it invalidates the cache beneath it *(ledger row 10-21B; applied 2026-10-22)*

> **Draft annotation, pending ingest.** Verified against live sources on 2026-10-20/21, recorded in `.workbuddy/memory/concept-radar/2026-10-21.md` (candidate 2). Remove this banner on ingest; move the slug into frontmatter `sources`.

**This note and the section above are placed adjacently by design and must NOT be merged** — they are two distinct costs of the *same* action:

| | **10-22A** (above) | **10-21B** (this note) |
|---|---|---|
| What compaction destroys | **origin** — the typed role of each message | **cache validity** — already-cached state downstream of the rewritten prefix |
| Layer | the **governance** boundary | the **KV-cache** layer, *beneath* the text |
| Consequence | forged content launders into instruction | **expensive re-prefill** |

**Cache engineering** (`arXiv:2610.28577`, submitted 2026-10-20; code at `github.com/thu-nics/AKV`) names the contrast precisely: **compaction = rewriting the historical text; `drop` = leaving the record byte-identical and changing only what can still be attended to.** Compaction rewrites the trajectory prefix ⇒ downstream cached state is invalidated ⇒ re-prefill; and keeping less context in order to suppress re-prefill costs accuracy ⇒ **each of the two goals manufactures part of the other**.

Its two verbs act on **reachability, not content**: **`drop`** (exclude a selected cache from future attention) and **`repos`** (reposition the retained keys' positional encodings) — **not one word of the record changes**.

**The new problem this creates — content identical, state not.** The same token sequence under different sequences of cache operations yields **different cache states** ⇒ **prefix matching is no longer sufficient to decide reuse**. This is this wiki's first reuse criterion of the form "same content, different state" — a clean parallel to [[Provenance]]'s "same content, different origin".

🔴 **Boundaries that must travel with these numbers:** the abstract does **not** name the benchmarks, so the comparability of **+1.7 points** cannot be confirmed from it; **−27.7%** cost is measured against **threshold-triggered summarization**, not against doing nothing — it is an improvement *between comparable schemes*, not "adopt it and save 27.7%"; **1.2× throughput / 1.5× P95** are AKV's own **system-level** gains and are **not additive** with the +1.7 **policy** gain. Submitted 2026-10-20; no independent reproduction; the authors are the implementing team.

## See Also
- [[context-engineering]] — primary source
- [[ContextEngineering]] — parent discipline
- [[Agent]] — the long-task consumer
- [[LLMContext]] — the bounded resource being compacted
- [[Provenance]] — the boundary compaction turns out to sit on (10-22A)
- [[MemoryPoisoning]] — the write-side surface this row connects to
- [[MemoryGovernance]] — the opposite conclusion about retaining the original (10-22B)
