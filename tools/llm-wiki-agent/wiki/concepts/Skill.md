---
title: "Skill"
type: concept
tags: [anthropic, skill, progressive-disclosure, design-pattern]
sources: [skill]
last_updated: 2026-09-09
---

# Skill

An organized folder of instructions, scripts, and resources that Claude loads on demand when a task is relevant — turning a general model into a domain expert.

## Definition
Per [[skill]] source: Same Skill folder usable across Claude app / Claude Code / API / Agent SDK. Released as an open standard after 2025-12.

## Core Mechanism
- **Progressive disclosure (3 layers)**:
  - Layer 1 — YAML metadata (name + description) always in system prompt
  - Layer 2 — SKILL.md body loaded when task relevant
  - Layer 3 — scripts and referenced assets loaded on demand
- **Auto relevance check** — Claude scans metadata descriptions each turn; user doesn't "pick"
- **Code as first-class** — scripts allow deterministic operations (sort, render PDF, generate chart)
- **Cross-product portability** — same Skill works in multiple products

## Boundary
- **Not = prompt template** — template is per-conversation; Skill is cross-conversation, version-controlled, multi-product-shared
- **Not = fine-tuning** — Skill changes context, not model parameters
- **Not = MCP** — MCP = "connect the tool" (interface standard); Skill = "teach the model how to use the tool"

## Practical Use
| Use Skill | Use Prompt / Project |
|---|---|
| Cross-team / multi-product domain workflow | One-off, temporary input requirement |
| Complex tasks needing executable scripts | Static reference knowledge (glossaries) |
| Dynamic relevance activation | Always-on rules for every session |

## See Also
- [[Agent]] — Skill is the unit that empowers Agents
- [[ProgressiveDisclosure]] — load-on-demand mechanism
- [[LLMContext]] — Skills operate within bounded context
- [[MCP]] — complementary tool-connection standard
- [[Anthropic]] — Skill is an Anthropic product feature