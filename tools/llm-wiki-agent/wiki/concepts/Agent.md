---
title: "Agent"
type: concept
tags: [ai-agent, llm, autonomous-system]
sources: [agent, skill]
last_updated: 2026-09-09
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

## See Also
- [[Skill]] — the packaging unit that turns general models into domain experts
- [[LLMContext]] — Agent operations constrained by context window
- [[ProgressiveDisclosure]] — load-on-demand that lets Agents use Skills within bounded context
- [[ReAct]] — reasoning pattern used in Agent's step 2
- [[Anthropic]] / [[OpenAI]] — primary vendors shaping Agent design vocabulary