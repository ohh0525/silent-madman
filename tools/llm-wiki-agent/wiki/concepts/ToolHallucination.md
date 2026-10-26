---
title: "Tool Hallucination"
type: concept
tags: [tool-hallucination, closed-world, mcp, reliability, cross-turn-feasibility, affordance-set]
sources: [tool-hallucination]
last_updated: 2026-10-26
---

# Tool Hallucination (Closed-World Resolution)

An agent invoking a tool that **does not exist in the registry**, or passing arguments **no schema ever declared**. Because such a call is, *by construction, not a decision any gate ever made*, it must be caught **before** every permission check.

## Mechanism (per [[tool-hallucination]])
- **Where it comes from** — fluent language completion, not a configuration error. Having seen many `delete_file`-shaped traces, the model generates a `wipe_disk`-shaped name; knowing a transfer tool needs an amount, it attaches an `override` switch no schema declares. Documentation and prompt edits cannot fix this.
- **Why gates miss it — structurally** — a gate's judgement domain is *the set of tools it exposed*. A hallucinated tool is outside that set, so the call never becomes a gate decision and the gate never gets to refuse. A **structural blind spot, not insufficient rigour**.
- **The fix: a Resolution Rung** — two training-free checks before dispatching anything: ① is the tool name a member of a **closed registry**; ② does its contract signature match the trusted source. Only then do permission gates, least privilege and audit run. Its value is **in its position, not its algorithm** — it must sit upstream of every causal gate.
- **Merging [[MCP]] servers adds a new hallucination surface** — one shared namespace creates failures no single registry can express: name **collision** and **shadowing**. This is structural in the *act of merging*, not linear in tool count, and it affects models that were clean on the single-registry surface.
- **Irreducible residual** — "borrowed parameters" are schema-indistinguishable from legitimate calls. Constraining the invocation surface lowers probability; it never reaches zero.

## Boundary
- **Not tool selection** — selection asks *which real tool* (ranking within the real set); hallucination asks *whether the named tool exists*. Selection methods all presuppose the real-tool premise, so they cannot address this.
- **Not permission gating, and not replaceable by it** — an upstream/downstream pair, not alternatives: `resolve()` **then** `policy.allows()`. Same ordering with respect to [[AgentIdentity]]: identity answers *may you*, the rung answers *does it exist*.
- **Not a parse error** — malformed JSON is caught by a parser for the price of a retry; a **syntactically valid** call to a non-existent tool passes every format check. For an agent that can act, that is an **unbounded action**, not a formatting mistake.
- **Not "a bigger model will fix it"** — measurement puts a **675B** model on par with a **7–8B** model here. Reading it as a capability problem leads to the wrong roadmap (keep buying scale) instead of the right one (add a fact-check layer).

> **Scope note — what closed-world resolution does *not* buy you *(ledger row 10-19A; applied 2026-10-20)*.** This page's criterion is **does the tool exist**. TRACER (`arXiv:2610.19133`) holds the malicious payload fixed and varies only the vessel it arrives in: follow-up message **70%** → agent message **92%** → **tool output 95%** → retrieved context **96%**. A **real** tool returning the payload is a **95%** channel ⇒ **existence is not the variable.** Closed-world resolution still earns its place — it removes the non-existent fraction, which is exactly what this page was built to do — but it is **not sufficient** as an injection defence. **Record this as a boundary, not a counterexample:** the resolution rung never claimed to inspect payload *content*, only tool *existence*. (Same convention as the 2026-10-17 scope note on [[MemoryGovernance]]'s four bottom lines — the rule was not refuted; it stops being the whole answer.) ⚠️ The gradient figures are second-hand pending a check against arXiv figures 3 / 4 — see [[Provenance]]「Evidence's outer garment」for the full evidence grade.

## 跨轮次的可行性核验 —— 注册表答「存在吗」，能力集答「轮次之后还有谁能执行」/ Cross-turn feasibility — the registry answers *does it exist*, the affordance set answers *can anyone run it after this turn* *(ledger row 10-09E; applied 2026-10-26)*

> **Draft annotation, pending ingest.** Not yet backed by a source page in this wiki — verified against live sources on 2026-10-09 and re-verified 2026-10-26 (`.workbuddy/memory/concept-radar/2026-10-09.md` §3.3; ledger row **10-09E**). Remove this banner on ingest; move the slug into frontmatter `sources`.

**The adjacent failure this page does not cover.** The resolution rung checks a call **at dispatch time**: is the tool in the registry, does the signature match. That is a **one-shot, per-call** fact about the tool set. An agent can also **promise** an action that **spans turns** — *"I'll remind you tomorrow"* — where **no tool was named and no call was made**, yet the promise is still factually empty. **The tool existed or not was never the issue; feasibility is.**

**Empty Commitments** (`arXiv:2610.01045`; Jiaqi Tang / Lan Wei / Bingyu Shen / Boyang Li; cs.AI + cs.CL; v1 4 pages / 3 tables, **v2 adds the controlled benchmark**):

> **Definition:** *a promise of action after the current turn that nothing in the agent's tools or runtime can carry out.* Verbatim: *"its emptiness is decided by the agent's configuration at the moment of speaking, so it can be detected from a single turn, before deployment or at run time."*

- **Affordance set** = tools **+ four persistence properties** (act after the turn / schedule future actions / keep memory across sessions / delegate to third parties). A commitment is **felicitous** iff some execution path under that set performs it.
- **Three failure types** — **capability** (no affordance performs it) · **temporal** (falls at a time the agent is not running and cannot schedule) · **agentive** (a third party must act and the agent cannot delegate).
- **Anchoring** — where an enabling tool exists, the commitment counts only if the agent **calls it in the same turn**; otherwise **unanchored** ⇒ *adding a scheduler trades one defect for a quieter one.*
- **Numbers** — **293** requests × **5** setups (all tools **mocked**): four open-weight **8–14B** models fail **45.9%** of responses when no tool exists and nothing is stated; a frontier model **4.4%**, but by **deferring and asking**, not by using its tools ⇒ **unanchored promises remain in every model**. Stating the runtime (**cheapest fix**) roughly **halves** open-weight failures where nothing is doable and **changes nothing** where a scheduler exists; a **capability card** removes most failures at the largest **over-refusal** cost.

⇒ **Consequence for this page.** The closed-world rung and the feasibility rung are **the same shape at two timescales**: both are **structural, training-free checks upstream of every gate**, and both are decided by **configuration, not by behaviour** — a hallucinated tool by the registry, an empty promise by the **affordance set**. ⇒ **The registry answers *does it exist*; the affordance set answers *can anyone run it after this turn*.**

**Boundaries.**
- **vs this page's own scope note (10-19A)** — that note is about **payload content travelling through real tools**; this one is about the **feasibility of a promised action**. Different objects; both stay.
- **vs [[Abstention]]** — 该不该拒答 vs 答应得对不对; and a fix that refuses everything is not a fix (over-refusal is the cost side).
- **vs [[HumanInTheLoop]]** — the gate adjudicates **dispatched calls**; a promise is a **future-directed utterance** — the gate-side landing is a section on that page (filed 2026-10-26).

⚠️ **Evidence grade, must sit beside the numbers.** **45.9% / 4.4% come from one controlled benchmark with mocked tools — a decidability finding, not a prevalence finding; no online incidence rate exists.** **v1 reported no rates at all** — the numbers appear only in v2's controlled benchmark; the authors state the protocol still awaits human validation and a multi-model evaluation. **This is the wiki's first pre-deployment-decidable defect class: configuration + one turn, no trajectory needed.**

## Why It Matters
- It is the *factual premise* the rest of the actor-side stack silently assumes. Every downstream control — [[AgentIdentity]]'s authority check, [[HumanInTheLoop]]'s gate, least privilege, audit — is defined relative to a set of real tools. This page is what makes that set **closed and checkable**.
- It is measurable: the source reports **322** real hallucinations across 10 hosted models and two invocation surfaces, and **154** on a real [[MCP]] surface after merging — so the failure is a *statistic to monitor*, not an anecdote.
- It relocates the fix from "harden the gate" to "add a level of fact-checking *before* the gate" — an **architectural position** question rather than a policy-strength question.

## See Also
- [[tool-hallucination]] — source
- [[MCP]] — namespace merging is what creates collision / shadowing
- [[AgentIdentity]] · [[HumanInTheLoop]] — the downstream checks this must run before
- [[Agent]] — sharpens its "not a fixed automation script" boundary with a factual premise
- [[Skill]] — documents *when to call which tool*; cannot make the registry closed
- [[ContextEngineering]] — explains the origin (fluent completion) and why prompt-side fixes fail
