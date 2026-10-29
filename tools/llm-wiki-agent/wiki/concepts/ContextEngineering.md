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

## The half-life of the always-loaded file — the budget answers「留多少」, not「还对不对」*(ledger row 10-29B; applied 2026-10-29)*

> **Draft annotation, pending ingest.** Not yet backed by a source page in this wiki — verified against live sources on 2026-10-29 (`.workbuddy/memory/concept-radar/2026-10-29.md`, candidate 2; ledger row **10-29B**). Remove this banner on ingest; move the slug into frontmatter `sources`.

**What the section above leaves out.** The resident budget answers a **capacity** question — *how many tokens may the always-loaded file have, and which rules earn them*. It is silent about a second, orthogonal question: **do the rules that are already in there still describe the repository they point at?** The file is priced, capacity-planned, and non-monotone — and none of those properties say anything about **truth over time**.

**OSTEON**（`arXiv:2610.31306`, submitted **2026-10-22 14:04:13 UTC**; Mohammad Mehdi Gholinejad, single author; cs.SE + cs.AI）puts a number on it, and the number is the reason this section exists:

- **452** of the most-starred public GitHub repositories were scanned: **48.67%**（95% CI **44.1–53.3**）carry a root-level or `.github/` agent context file ⇒ the artifact this page's resident-budget section prices is now **half of the ecosystem**, not a niche pattern.
- **In the median file that names repository paths, 9.5%–22% of those paths no longer resolve**（the spread is the two readings of "a reference"）. ⚠️ This is **paths that do not resolve**, *not* "22% of the file is wrong" — the file can be internally coherent and still point at a deleted module.
- The argument's spine: **correctness rests on decisions and contracts that the code does not carry** · **knowledge decays** · once an agent outpaces its reviewers, **reading catches a shrinking share of changes built on stale knowledge**. A simple model: past a fixed review capacity, **escaping changes grow linearly with throughput while the fraction reading catches falls toward zero** ⇒ *governance can lower the slope, capability alone cannot.*
- **OSTEON**'s four moves: a **governed knowledge repository of decisions and contracts** · every change **mechanically checked** against it · **the knowledge itself checked for decay at every session start** · planning gated, and sessions **record what they learn without writing rules**.

⇒ **The verb this page is still missing is neither *curate* nor *trim* — it is *expire*.** The resident budget can be perfectly curated and still be **stale**; conversely a stale file is invisible to every capacity metric, because a dead path costs exactly as many tokens as a live one.

**The other direction — the same file, failing by *contradiction* rather than by *decay*.** Drew Breunig's AGNTCon talk *Context Fails & Fixes*（write-up **2026-10-24**）adds the failure mode this page did not have: **context inertia** — *"models hyper-focus on a hypothesis, subtask, or goal in their context, and keep pursuing it after they should stop."* Three independent instances converge on the same fix: Anthropic's **Memento** harness clears the agent's context **every hour and a half**, keeping the environment and artifacts intact; Microsoft Research's **Fork-and-Flush** and UC Berkeley's *Scaling Discovery Requires Forgetting*（Shangyin Tan）do the same thing — **periodically wipe the context, keep what was produced in the environment**. Breunig's operational threshold is deliberately crude and deliberately quoted as a heuristic: *"Delete your context. I'm not joking. **Around 200,000 tokens is my warning point.**"* And his forward-looking claim, which is exactly this section's topic: *"As we focus more on memory, we also need to think about **strategic forgetting**. Over time, overly precise memories become conflicted and messy, and nobody has yet figured out how to handle this."*

⇒ **OSTEON = the resident file goes stale; Breunig = the resident file goes contradictory.** Decay and conflict are **two different directions of the same half-life**, and neither is measurable on this page's capacity budget.

**Boundaries (do not merge).**

- **vs [[ContextRot]]** — rot is the **attention** axis (it fits, but attention degrades); this is the **truth** axis (it fits, it is attended to, and it is no longer true). ⚠️ **Different axes; a short stale file has no rot at all.**
- **vs the resident-budget section above** — that section owns **how much and which**; this one owns **whether it still holds**. Same object, two questions.
- **vs [[Compaction]] / 10-26B** — compaction **drops** things from the window (no attacker, class-biased loss); this section has **no compaction event at all** — the file simply accumulated references to a world that moved.
- **vs [[Provenance]] / 10-26A（Tether）** — that pair handles **memory** whose supporting premise expired; this handles **instruction files** whose *pointers* expired. Same shape (*invalidation is not an action on the object*), different object ⇒ **cross-name, do not merge.**

⚠️ **Evidence grade — and the honest part is unusual.** The author of OSTEON **states outright that no measured effect of OSTEON is reported**, marks the mechanism claims as **opinion**, the practice heuristics as **design rationale**, and lists **the questions that would falsify the thesis** ⇒ **this is a thesis / discipline paper, not an effect paper.** The 48.67% and 9.5%–22% figures are an **exploratory snapshot** by a **single author**; the 452 repos are the *most-starred*, i.e. **not a random sample**. The Breunig items are a **talk transcript** and a **practitioner heuristic**（200k tokens is his warning point, not a measured cliff）, and the three "forgetting" fixes are three self-reported engineering practices ⇒ **direction-grade only.**

## See Also
- [[context-engineering]] — primary source
- [[Compaction]] — its long-horizon technique (see its scope note for the cache cost of the same verbs)
- [[ContextRot]] — the phenomenon it fights
- [[LLMContext]] — the resource it manages
- [[ProgressiveDisclosure]] & [[Skill]] — knowledge-loading instance of the same principle (see its 10-09 section for the resident-vs-on-demand allocation rule; and its 10-29B note on what the resident file must survive)
- [[Provenance]] — retrieved memory is only as useful as it is trustworthy
- [[RAG]] — the "do nothing to the raw history" baseline this page's verbs are measured against (added 2026-10-29)
