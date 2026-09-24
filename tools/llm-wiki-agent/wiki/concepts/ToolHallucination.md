---
title: "Tool Hallucination"
type: concept
tags: [tool-hallucination, closed-world, mcp, reliability]
sources: [tool-hallucination]
last_updated: 2026-09-24
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
