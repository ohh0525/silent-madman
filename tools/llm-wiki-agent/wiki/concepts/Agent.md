---
title: "Agent"
type: concept
tags: [ai-agent, llm, autonomous-system, authority, runtime]
sources: [agent, skill, agent-identity, human-in-the-loop, tool-hallucination, agent-harness]
last_updated: 2026-09-26
---

# Agent

A software system driven by a large language model that autonomously decides which tools to call around a target, observes results, and loops until the task completes or control is yielded.

## Definition
Per [[agent]] source: Agent 是组织好的 LLM + 工具 + 记忆 + 循环。

## Core Mechanism (from [[agent]])
1. **Receive goal + context** — translate fuzzy intent into executable target
2. **Reason next action** — ReAct / Chain-of-Thought pick tool + params
3. **Execute tool + collect observation** — external executor does the work
4. **Update state + judge stop** — merge observation, decide done or loop back

A canonical pseudo-code:

```
while not done:
    thought    = model.reason(goal, history)
    if thought.is_final_answer: return thought.answer
    tool_call  = model.choose_tool()
    observation = execute(tool_call)
    history.append((thought, tool_call, observation))
```

## Boundary
- **Not a chatbot** — must dynamically control flow, not just answer questions
- **Not a fixed automation script** — steps are auto-determined, not pre-encoded
- **Not AGI** — bounded by permissions, token budget, stopping condition

## Practical Use
| Use Agent | Use Script |
|---|---|
| Steps cannot be enumerated in advance | Steps are fixed, repeated |
| Need to adapt based on results | Millisecond-SLA hot paths |
| Single failures acceptable via retry | Any failure is irreversible |

## Authority axis (added 2026-09-24, per [[agent-identity]] · [[human-in-the-loop]] · [[tool-hallucination]])
The Boundary section above says an Agent is "bounded by permissions, token budget, stopping condition". That sentence named a ceiling but never said **who grants it, how far it travels, or who checks whether the action was physically possible**. Three pages now supply that axis:

| Question | Page |
|---|---|
| **Who is acting, on whose behalf, and how far may that authority travel?** | [[AgentIdentity]] — workload identity + RFC 8693 token exchange + strictly narrowing per-hop attenuation + dual-subject audit |
| **May it do this, or must a person approve first?** | [[HumanInTheLoop]] — grade by impact × reversibility; read freely, keep writes human; the rule lives in code, not the prompt |
| **Does the thing it just called even exist?** | [[ToolHallucination]] — a closed-world resolution rung *before* any gate, because a hallucinated call is not a decision any gate ever made |

The ordering between them is not decoration: **resolve the call → verify authority → gate the irreversible step**. Read in that order, the agent's loop above (reason → choose tool → execute) acquires the three failure checks it was missing. This also fixes a boundary previously left implicit: an Agent's loop can be *correct* and still *unauthorized*, *unapproved*, or *aimed at a tool that does not exist* — three independent ways to fail that "did it complete the task?" cannot detect.

## Runtime axis (added 2026-09-26, per [[agent-harness]])
Everything above describes the loop's **semantics**. Something must actually *run* that loop — assemble the prompt, inject tool definitions, execute calls, compact the window near its limit, resume after crashes, schedule subagents. That engineering shell is the **harness**, giving the canonical split **`Agent = Model + Harness`**. The wiki's mechanism pages ([[Compaction]], [[ToolHallucination]]'s rung, [[Skill]] loading, [[ContextEngineering]]'s per-turn policy) are **parts inside that shell**; as of 2026-09 the shell itself is being productised as managed infrastructure by both [[OpenAI]] (Agents API on the Codex harness) and [[Anthropic]] (Opus 5.5 managed orchestration). See [[AgentHarness]].

## See Also
- [[Skill]] — the packaging unit that turns general models into domain experts
- [[LLMContext]] — Agent operations constrained by context window
- [[ProgressiveDisclosure]] — load-on-demand that lets Agents use Skills within bounded context
- [[ReAct]] — reasoning pattern used in Agent's step 2
- [[Anthropic]] / [[OpenAI]] — primary vendors shaping Agent design vocabulary
- [[AgentIdentity]] · [[HumanInTheLoop]] · [[ToolHallucination]] — the authority / control / factualness axis (see above)
- [[AgentHarness]] — the runtime axis: the shell that hosts and executes this page's loop (see above)