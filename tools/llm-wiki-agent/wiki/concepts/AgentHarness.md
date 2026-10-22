---
title: "Agent Harness"
type: concept
tags: [agent-harness, runtime, orchestration, durability, subagents, harness-plurality, inheritance, routing]
sources: [agent-harness]
last_updated: 2026-10-22
---

# Agent Harness (智能体外壳)

The engineering shell that turns **one model call** into **an agent that gets work done**: it assembles the prompt, retrieves and injects tool definitions, executes tools, decides what to drop when the window fills, resumes after crashes, and schedules subagents. It is neither the model nor the business logic — it is **the loop code between the model and the real world**. Canonical split: **`Agent = Model + Harness`**.

## Mechanism (per [[agent-harness]])
Four duties per loop; miss any one and the agent degrades from "works" to "demo":
- **① Assemble context** — system prompt + tool definitions into this turn's request; modern harnesses use **tool search** (retrieve tool schemas on demand) instead of injecting every schema every turn. *What goes in the window decides both the agent's sight and its cost.*
- **② Run the loop and judge stopping** — request → parse tool call → execute → write observation back → decide done / continue / give up. *Autonomy is this loop; a loop without a stop condition is an infinitely expensive loop.*
- **③ Govern the window** — near the context limit, automatically summarise earlier context (**automatic compaction**) so the task spans multiple windows instead of breaking at the boundary. *Long-task bottleneck is window size, not model intelligence: whoever decides "what gets dropped when full" holds long-task quality.*
- **④ Resilience & scale** — session keep-alive and crash recovery (real tasks run for days; a single process loop cannot survive that), plus subagent scheduling (the harness itself provides create / message / wait / interrupt; enabled by a flag + `max_concurrent_subagents`).

## Boundary
- **Not [[Agent]]** — semantics vs implementation. [[Agent]] describes the loop's *semantics* (reason → choose tool → execute → observe); the harness is that loop's concrete *implementation* — who assembles prompts, who manages the tool table, who runs compaction, who handles recovery.
- **Not any single mechanism page — it is their container.** [[Compaction]], [[ToolHallucination]]'s resolution rung, [[Skill]] loading, [[ContextEngineering]]'s per-turn policy are all **parts inside the shell**; the harness decides *when each part fires and with what threshold*. Corroboration: OpenAI's three headline features (automatic compaction / tool search / multi-agent) are exactly pre-existing wiki concepts.
- **Not [[ContextEngineering]]** — principles vs program. Context engineering is the *policy* of what belongs in the window each step; the harness is *the program that executes that policy*.
- **Not the sandbox** — the harness decides **who orchestrates**; the sandbox decides **where it runs and what it can touch**. OpenAI makes the split explicit as separate `Agent` and `Environment` objects (environment optional: `openai_hosted` / `self_hosted` / `none`); the two should be chosen separately. See [[AgentSandbox]].

## Why It Matters
- **It names the wiki's implicit host.** Every mechanism page was already describing a part of this shell; the wiki had the parts and lacked the container. Naming it turns a pile of techniques into a runtime architecture.
- **As of September 2026 the shell itself became infrastructure.** OpenAI's Agents API public beta (2026-09-10) rents out the Codex harness — durable sessions, automatic compaction, tool search, subagents, pluggable environments; Anthropic plays the same layer with Opus 5.5 "managed orchestration". Agent Brief names it "Harness Wars" and frames it as *orchestration as managed infrastructure* — the layer LangChain/CrewAI used to sell, now offered by the model vendors themselves.
- **Managed ≠ safe.** The defaults are the security boundary and they are permissive: egress defaults to `enabled`; `restricted` mode accepts only 1–100 exact hostnames (no wildcards/paths/ports); injected secrets remain exposed to agent-generated code. Same-week Codex sandbox escapes (Heapjack / Overpatch) show managed harnesses *centralise* patch responsibility, they do not remove sandbox risk.
- **Honest numbers discipline:** vendor performance claims (latency ~¼, cost −60%, failures −86%) are self-reported and must be discounted; documented defaults are citable facts, self-reported performance is not.

## Should the harness be singular? *(ledger row 10-21C; applied 2026-10-22)*

> **Draft annotation, pending ingest.** Verified against live sources on 2026-10-21/22, recorded in `.workbuddy/memory/concept-radar/2026-10-21.md` (candidate 3). Remove this banner on ingest; move the slug into frontmatter `sources`.
>
> 🔴 **Two attribution corrections were made at ingest-decision time and are binding.** (1) The headline figure is **"up to 15.79%"** — and it is measured **against the unevolved base harness**, *not* against Meta-Harness (against Meta-Harness: **+13.49 / +9.92 / +4.00** on the three main settings). (2) The EvoHarnessBench result below is **NOT the authors' self-citation** — it is an **independent benchmark (Ke et al., 2026, `arXiv:2609.04280`)** that the authors cite. Earlier drafts of this row mislabelled it "作者自引"; the correction makes the counter-evidence **stronger, not weaker**.

**The question this page has never asked.** Since 2026-09-26 this wiki has used "harness" in the **singular**: the four duties above (assemble context / run the loop and decide stopping / govern the window / keep-alive, resume and scheduling) describe **one global shell**, and so does 10-15C's measurement of the harness's contribution. **OO-Harness** (`arXiv:2610.28380`, submitted 2026-10-20 15:32 UTC; 12 authors) poses the number dimension: *a single global harness strains to handle heterogeneous tasks requiring different execution strategies.*

| Element | Design |
|---|---|
| **Representation** | an **inheritable class hierarchy** of executable harness classes; a subclass inherits the base or an existing specialist and overrides/adds methods |
| **Training** | cluster discovery tasks by **shared execution needs** identified in base-class traces; an evolution agent picks a cluster + a parent harness → builds a subclass → evaluates on that cluster; feedback accumulates as **design lessons** and **routing lessons** |
| **Test** | a **harness router** selects a specialist (or keeps the base result) from task + observable base-class trace + routing lessons; polymorphism runs them through one interface |
| **Deployment discipline** | **the hierarchy and lessons are frozen before deployment; executor weights are fixed in both stages** |

**The second organizing principle: inheritance, not replacement.** A specialist **inherits** the base or an existing specialist and overrides only what must change ⇒ **an improvement for one task cluster does not contaminate the base class or the other specialists** (the authors state this as the generalization advantage). ⇒ This is this page's answer to the 10-18B / 10-16B family — *"changing one place degrades another"*: the fix is not a better single harness but **a structure in which the change is local**.

**Deployment discipline belongs on this page too.** Evolution happens **during training**; at run time the system is deterministic ⇒ **the same shape as "managed ≠ safe" above**: what is *learned* is frozen, what is *executed* is fixed.

**Results.** Best main score among compared methods on three long-horizon benchmarks (AutomationBench / Workspace-Bench / Toolathlon-GYM), **up to 15.79% absolute over the base harness**; vs Meta-Harness **+13.49** (AutomationBench mean), **+9.92** (Workspace-Bench mean), **+4.00** (Toolathlon-GYM PASS). Meta-Harness is compared throughout (§4.2, §5.3, Table 1) — **the "beats Meta-Harness" claim is confirmed against the primary text, contrary to what the abstract alone would suggest** (the abstract mentions only "base harness").

### ⚠️ The counter-evidence, listed separately — it is [[Skill]]'s boundary, not a footnote

**EvoHarnessBench** (Ke et al., 2026 — **independent**, cited by the authors): **adding tools, skills, and specialist agents can degrade previously effective behavior.** Related work adds **Agentic Harness Engineering**: evolved memory **improves hard tasks and harms easy ones**; and **Meta-Harness**'s global selection is **not guaranteed to remain beneficial under distribution shift**.

⇒ [[Skill]] and [[ProgressiveDisclosure]] rest on *"load on demand ⇒ stronger without bloat."* **"Adding more can be worse" is a direct instance against that narrative** — but it is a **boundary, not a refutation**: those pages never claimed infinitely additive gains. Filed here because [[Skill]]'s own page should be able to point at it.

**Why it is not the same row as 10-15C.** That row asks **"how much does the harness contribute"** (backbone frozen, harness swapped; Max moves 7–17 points). This one asks **"should the harness be plural."** ⇒ **Separate columns; must not be merged.** Same for **[[MultiAgent]]**: that is **multiple runtime instances cooperating**; this is **one executor with several selectable harness classes** — *parallelism vs polymorphism*.

🔴 **Boundaries:** 15.79% is a self-reported **"up to"** (an upper bound); all three benchmarks are **long-horizon agentic** tasks — short tasks and multi-turn dialogue are uncovered; **the cost of training the hierarchy and the routing lessons is not counted**; no independent reproduction.

## See Also
- [[agent-harness]] — source
- [[Agent]] — the loop semantics this shell implements (runtime axis added there)
- [[Compaction]] — harness duty ③ in detail
- [[ToolHallucination]] — the resolution rung lives in the harness's dispatch path
- [[Skill]] — the packaging format the harness loads on demand; becoming the ecosystem standard (372 / 216 / 193 skills, 2026-09)
- [[ContextEngineering]] — the policy the harness executes
- [[HumanInTheLoop]] — its pause/resume requirements are harness durability requirements
- [[MCP]] — remote MCP tools are called by the harness even with no environment selected
- [[AgentSandbox]] — the execution environment the harness plugs into (added 2026-09-26)
- [[MultiAgent]] — subagent scheduling (duty ④) productised; the team-vs-single trade-off has its own page (added 2026-09-26)
- [[OpenAI]] · [[Anthropic]] — the two vendors simultaneously productising this layer
