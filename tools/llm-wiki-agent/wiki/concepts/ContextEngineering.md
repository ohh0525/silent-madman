---
title: "Context Engineering"
type: concept
tags: [context-engineering, anthropic, prompt-engineering, cache-engineering, kv-cache, reachability, resident-budget, capacitated-assortment, re-sent-context]
sources: [context-engineering]
last_updated: 2026-10-26
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

## The resident budget — the tokens this page never prices *(ledger row 10-09; applied 2026-10-26)*

> **Draft annotation, pending ingest.** Not yet backed by a source page in this wiki — verified against live sources on 2026-10-09 and re-verified 2026-10-26 (`.workbuddy/memory/concept-radar/2026-10-09.md`, candidate 1; ledger row **10-09** — the 🎯 oldest un-landed row). Remove this banner on ingest; move the slug into frontmatter `sources`.

**What this page has always assumed.** Layer by lifespan, just-in-time retrieval, trim + re-inject — every mechanism here is about the **window's working set**. The file that loads at session start and **never leaves** (`AGENTS.md` / `CLAUDE.md` / the system prompt) is priced **nowhere on this page** — yet **each of its tokens is charged again in every later round of the session**, and it is the one thing [[Compaction]] (this page's own long-horizon technique) is designed **not** to touch.

**Curating always-loaded context** (`arXiv:2610.11007`, 2026-10-07, UIUC / Georgia Tech / Saint Louis — **re-verified 2026-10-26**) formalizes it as a **capacitated assortment problem**:

- **An upper bound on the optimal file size exists**, regardless of how many candidate instructions are available.
- **Adding an instruction never raises the compliance of the others** (non-monotone) ⇒ **appending every instruction with positive standalone value can be *arbitrarily worse* in net value than selecting an optimal subset.**
- **Feedback is censored** — a *missing* instruction generates feedback only when its absence causes harm ⇒ **"delete what the agent ignores" inevitably deletes helpful instructions.** The paper instead characterizes **how much evidence to collect before adding one**, and bounds regret when human reviewers can inspect only a limited number of edits per period.
- Empirically **irrelevant rules drawn from real context files reduce compliance**; across **1,867** repositories such files **more than double over their lifetime** while **deletions become rarer with age** — curation pressure is one-directional in practice.

**The cost column is measured, not assumed** — **Evaluating AGENTS.md** (`arXiv:2602.11988`, ETH Zürich + LogicStar.ai, MemAgents @ ICLR 2026 Oral; **re-verified 2026-10-26**): over **60,000** repositories ship such files; on AGENTbench (138 instances / 12 niche Python repos / 5,694 real PRs) context files overall **do not raise success while pushing inference cost above 20%** — LLM-generated **−2~−3%**, human-written **+4%** with **+2.45–3.92 extra steps**; the recommended **"repository overview" section is specifically called out as ineffective**; removing repo docs flipped LLM-generated context to **+2.7%** ⇒ **redundancy, not presence, is the disease.**

**Cost cross-check（ledger row 09-25, merged here 2026-10-26）— the re-sent context is the biggest single line of the invoice.** Stanford Digital Economy Lab（*Agentic AI Cost Attribution*）attributes **~62% of agent inference bills to re-sent context** — the system prompt, tool definitions and state transmitted with every call; agentic tasks consume **5–30×** the tokens of a chat query（Gartner, 2026-03）; prompt caching can cut the re-sent share by **up to 90%**, but only while the prefix stays byte-stable. *（Re-verified 2026-10-26 via multiple independent secondary sources; the original report was not opened — 62% keeps its second-hand marking at one remove.）* ⇒ **The resident file is not merely re-read — it is the single biggest line of the bill, and this page's verbs are the only levers on it.** The observation/judgement side of the same invoice（judge pricing, evaluation tax）is filed as Chapter E of [[AgentObservability]]; the provable lower bounds on the whole bill live on [[AgentHarness]]'s LAM section — three columns of one invoice, split by page.

⇒ **Consequence for this page.** The resident file is **not** part of the window's working set — it is a **capacity-planned, upper-bounded, non-monotone budget** that this page's verbs (layer / fetch / trim) never touch. ⇒ **A new verb is missing: *curate* — select under capacity, with an evidence bar for additions and a censored-feedback-aware policy for deletions.** The allocation rule (what earns the resident slot vs the on-demand slot) is filed as a section on [[ProgressiveDisclosure]].

**Boundaries.** **vs the「layer beneath」section above** — that layer is **below** the text record (KV cache); this one is **above** the window's churn (the never-trimmed file). Both are layers this page's verbs missed; different directions. **vs [[Compaction]]** — compaction manages the window; the resident budget is what compaction must **preserve**. **vs [[ProgressiveDisclosure]]** — that page owns the **allocation rule**; this one owns the **budget and its price**.

⚠️ **Evidence grade.** The assortment results are **theoretical bounds plus compliance experiments**, not a deployed-curation trial; AGENTbench is **Python-only, 4 agents**, does **not separate** rule types, and found **no length–effect relationship** in tested ranges ⇒ **"keep it under N lines" is vendor advice, not an empirical result.** IFScale / vendor-eval figures recorded 2026-10-09 are **not re-verified this session**.

## See Also
- [[context-engineering]] — primary source
- [[Compaction]] — its long-horizon technique (see its scope note for the cache cost of the same verbs)
- [[ContextRot]] — the phenomenon it fights
- [[LLMContext]] — the resource it manages
- [[ProgressiveDisclosure]] & [[Skill]] — knowledge-loading instance of the same principle (see its 10-09 section for the resident-vs-on-demand allocation rule)
- [[Provenance]] — retrieved memory is only as useful as it is trustworthy
