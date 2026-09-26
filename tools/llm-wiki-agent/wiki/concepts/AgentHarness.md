---
title: "Agent Harness"
type: concept
tags: [agent-harness, runtime, orchestration, durability, subagents]
sources: [agent-harness]
last_updated: 2026-09-26
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
- [[OpenAI]] · [[Anthropic]] — the two vendors simultaneously productising this layer
