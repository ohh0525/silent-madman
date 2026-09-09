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

## See Also
- [[Skill]] — primary use case
- [[LLMContext]] — solves the bounded-context problem
- [[Agent]] — typical consumer of progressive disclosure