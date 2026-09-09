---
title: "ReAct"
type: concept
tags: [agent, prompting, reasoning]
sources: [agent]
last_updated: 2026-09-09
---

# ReAct

A prompting pattern that interleaves Reasoning and Action steps in an Agent loop: **Thought → Action → Observation → Thought → …**.

## Role in Agent
Per [[agent]] core mechanism step 2, ReAct (along with Chain-of-Thought) is the canonical reasoning pattern for Agent's "decide next action" step.

## Strengths
- Forces explicit reasoning before each tool call → reduces hallucination
- Traceable — every Thought is inspectable in the log
- Composable with any tool set

## See Also
- [[Agent]] — primary use case
- [[Skill]] — Skill metadata + ReAct reasoning together drive tool selection