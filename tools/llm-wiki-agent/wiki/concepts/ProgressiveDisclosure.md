---
title: "Progressive Disclosure"
type: concept
tags: [anthropic, context-engineering, design-pattern]
sources: [skill]
last_updated: 2026-09-09
---

# Progressive Disclosure

A load-on-demand design pattern that fits arbitrarily many resources into a bounded context window by exposing only metadata initially.

## Mechanism (per [[skill]])
1. **Layer 1** — YAML metadata (name + description) always in system prompt
2. **Layer 2** — SKILL.md body loaded when task relevant
3. **Layer 3** — scripts/assets loaded on demand

## Why It Matters
- Lets a single Skill carry arbitrary resources without bloating context
- User doesn't need to "pick" — model selects based on description matching
- Reasoning chain shows the activation, making it observable / debuggable

## 「按需加载」的前提是它会加载 —— 常驻与按需的分配规则 / The premise of load-on-demand is that it loads *(ledger row 10-09; applied 2026-10-26)*

> **Draft annotation, pending ingest.** Not yet backed by a source page in this wiki — verified against live sources on 2026-10-09 and re-verified 2026-10-26 (`.workbuddy/memory/concept-radar/2026-10-09.md`, candidate 1; ledger row **10-09** — the 🎯 oldest un-landed row, 17 days). Remove this banner on ingest; move the slug into frontmatter `sources`.

**The premise this page has never tested.** Layers 1–3 assume the description-matching step **fires** — that the model, mid-task, connects an available resource to the task at hand. The 2026 measurements say that step is the weak one, not the storage question this page was built to solve.

- **Vercel agent evals (2026-01-27)** — the same 8 KB documentation, two delivery modes: **always-loaded AGENTS.md docs index 100%** pass · **on-demand skill retrieval 53%** — **equal to the no-documentation baseline** — with **56% of cases never loading the skill at all**; an explicit instruction raises it to **79%**. *(re-verified 2026-10-26)*
- **A 34,000-skill evaluation** — the dominant failure mode is **retrieval miss**, not skill failure: the agent never associates "available skills" with the current task and **works empty-handed** — corroborating the 56%. *(recorded 2026-10-09)*
- **The counterweight that keeps "always-loaded" honest** — **curating always-loaded context** (`arXiv:2610.11007`, 2026-10-07, UIUC / Georgia Tech / Saint Louis): the always-loaded file is a **capacitated assortment problem** — **an upper bound on the optimal file size exists**; **appending every instruction with positive standalone value can be *arbitrarily worse* than the optimal subset**; **adding an instruction never raises the others' compliance**; and feedback is **censored** (a missing instruction produces feedback only when its absence causes harm) ⇒ **deleting instructions the agent ignores inevitably removes helpful ones**. Empirically, **irrelevant rules drawn from real context files reduce compliance**; and across **1,867** repositories such files **more than double over their life** while **deletions become rarer as the file ages**. *(re-verified 2026-10-26)*
- **The cost column** — **Evaluating AGENTS.md** (`arXiv:2602.11988`, ETH Zürich + LogicStar.ai, MemAgents @ ICLR 2026 Oral; **AGENTbench**: 138 instances / 12 niche Python repos from 5,694 real PRs + SWE-bench Lite 300 / 4 agents): context files overall **do not raise success while pushing inference cost above 20%** (LLM-generated **−2~−3%**; human-written **+4%** with more steps and cost; **+2.45–3.92 extra steps**); the officially recommended **"repository overview" section is called out as ineffective**; and with repo docs removed, LLM-generated context **improved +2.7%** ⇒ the main disease is **redundancy**. Over **60,000** repositories ship such files. *(re-verified 2026-10-26)*

⇒ **The allocation rule this page was missing.** "Always-loaded" and "on-demand" are not a lazy/eager implementation choice of the same thing; they are **two different positions with different compliance and different prices**:

| Position | Compliance | Price |
|---|---|---|
| **Always-loaded** | **highest measured** (100% vs 53%) — and the **only position immune to [[Compaction]]** (see [[HumanInTheLoop]] 10-26B: executable rules get eaten by compaction while task scores stay flat) | every token **re-charged every round**; upper-bounded optimal size; non-monotone in additions |
| **On-demand (this page)** | ≈ **baseline when the trigger misses** (53% = no-docs; 56% never load) | paid only when loaded — **if** loaded |

**Content type decides which position earns its price**: concrete, non-standard, project-specific constraints work in the resident slot; "overview"-style content does not work anywhere. *(recorded 2026-10-09)*

**Boundaries.**
- **vs [[ContextEngineering]]** — that page owns the **in-window** tradeoff; this section owns **capacity planning of the always-loaded file** (the second landing of this row is a section there).
- **vs [[Skill]]** — Skill is the **loading unit**; this section is about the **loading probability**. The unit can be perfect and the probability still ≈ baseline.
- **vs [[ContextRot]]** — rot is a *phenomenon* (fits but unused); the resident budget is a *configurable* response to it.
- **vs [[HumanInTheLoop]] 10-26B** — compaction eats resident-seeming rules; the **truly always-loaded file is exempt**, which is exactly why it is both the only stable position and the most expensive one.

⚠️ **Evidence grade.** Vercel figures are **vendor self-reported**; IFScale / Scott Spence / Lulla / UFMG figures recorded 2026-10-09 are **not re-verified this session**; AGENTbench is **Python-only, 4 agents**, and does **not separate** style rules / tool preferences / architecture docs; **"keep it under 200 lines" is vendor advice, not an empirical result** — no study found a length–effect relationship in the ranges tested. **The only three citable conclusions are the ones in the table and the content-type rule.**

## See Also
- [[Skill]] — primary use case
- [[LLMContext]] — solves the bounded-context problem
- [[Agent]] — typical consumer of progressive disclosure
- [[ContextEngineering]] — progressive disclosure is an instance of this broader curation principle (see「The resident budget」there, 10-09)
- [[HumanInTheLoop]] — why the always-loaded file is the only compaction-immune position (10-26B × 10-09)