---
title: "Context Engineering"
type: concept
tags: [context-engineering, anthropic, prompt-engineering, cache-engineering, kv-cache, reachability]
sources: [context-engineering]
last_updated: 2026-10-22
---

# Context Engineering

The discipline of deciding, at every inference step, which tokens to place into the bounded context window — targeting the *minimal set of high-signal tokens* that produces the target result, rather than maximal volume.

## Mechanism (per [[context-engineering]])
1. **Layer by information lifespan** — stable boundaries once at start; current state reread right before key steps; large raw payloads kept as identifiers/addresses only.
2. **Just-in-time retrieval** — replace pre-loading with on-demand fetch; the window holds references, not originals.
3. **Each turn: trim + re-inject** — tool results return summaries + evidence pointers by default; old processed results are cleared near the limit.
4. **Long-horizon techniques** — [[Compaction]], structured notes, sub-agents.

## Why It Matters
- The constraint is architectural: [[Transformer]] attention is an n² budget, so longer context spreads attention thinner.
- Directly opposes "bigger window = better": [[ContextRot]] means effective capacity runs below the nominal ceiling.
- Evidence: Anthropic cut Claude Code's system prompt by 80%+ with no measurable coding-eval loss; tool definitions dropped 77K → 8.7K tokens (−85%) while accuracy *rose* 79.5% → 88.1%.

## The layer beneath *(ledger row 10-21B; applied 2026-10-22)*

> **Draft annotation, pending ingest.** Verified against live sources on 2026-10-20/21, recorded in `.workbuddy/memory/concept-radar/2026-10-21.md` (candidate 2). Remove this banner on ingest; move the slug into frontmatter `sources`.

**Every verb on this page acts on the text record.** Layering, just-in-time retrieval, trim + re-inject, [[Compaction]] — all of them **change the text**. That is the layer this page has always described. **Cache engineering** (`arXiv:2610.28577`, submitted 2026-10-20; code at `github.com/thu-nics/AKV`) works **one layer below**, on the **KV cache**, and its first finding is about *this* page's verbs:

> **Rewriting the trajectory prefix invalidates already-cached state downstream ⇒ an expensive re-prefill.** And keeping less context in order to suppress re-prefill costs accuracy ⇒ **each of the two goals manufactures part of the other.**

⇒ **Context management reflexively manufactures part of the cost it exists to control.** The shape — *a mechanism produces part of the problem it solves* — previously appeared in this wiki only at the **behaviour** layer (10-18C); this is the **system** layer.

**Two new verbs, both acting on reachability rather than content.** **`drop`** — exclude a selected cache from future attention. **`repos`** — reposition the retained keys' positional encodings. **Not one word of the record changes; what changes is whether it can still be attended to.** ⇒ This is scan line 16 again: same goal (shrink the active context), two non-substitutable routes — **change the content** (this page) versus **change the reachability** (that layer). See [[Compaction]]'s scope note, where the two are filed adjacently by design.

**The new problem: content identical, state not.** The same token sequence under different sequences of cache operations yields **different cache states** ⇒ **prefix matching is no longer sufficient to decide reuse.** This wiki's first reuse criterion of the form *"same content, different state"* — a clean parallel to [[Provenance]]'s *"same content, different origin"*.

**Where it sits against the neighbouring rows:**
- **vs 10-19C (text wire vs KV wire)** — that row is the **communication** view (what agents pass to each other); this one is the **serving** view (what one machine reuses). Complementary, mutually named.
- **vs [[ContextRot]]** — rot asks *"it fits but it doesn't work"* (**attention**); this asks *"touch it and you recompute"* (**cache coherence**). Two different failure axes.
- **vs 10-14A** — that row treats the prefix cache as a **leakage channel** (CVE-2026-105752); this row treats it as a **resource and coherence object**. **The same object's two faces; this wiki had only recorded the dangerous one.**
- **vs the `09-20` ledger row (prompt caching / KV cache, ⏸ 30+ days)** — that row was an empty "missing page" judgement; this supplies **concrete verbs, a concrete cost, and a concrete engine** ⇒ **merged into that row as its successor, not opened as a new row.**

🔴 **Boundaries for the numbers:** the abstract does **not** name the benchmarks, so **+1.7 points**' comparability cannot be confirmed from it; **−27.7%** is against **threshold-triggered summarization**, not against no management at all; **1.2× throughput / 1.5× P95** are AKV's **system** gains and are **not additive** with the +1.7 **policy** gain. No independent reproduction; the authors are the implementing team.

## See Also
- [[context-engineering]] — primary source
- [[Compaction]] — its long-horizon technique (see its scope note for the cache cost of the same verbs)
- [[ContextRot]] — the phenomenon it fights
- [[LLMContext]] — the resource it manages
- [[ProgressiveDisclosure]] & [[Skill]] — knowledge-loading instance of the same principle
- [[Provenance]] — retrieved memory is only as useful as it is trustworthy
