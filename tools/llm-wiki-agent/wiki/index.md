# Wiki Index

This file is maintained by the LLM. Updated on every ingest.

## Overview
- [Overview](overview.md) — living synthesis across all sources

## Sources
- [AI Agent(智能体)](sources/agent.md) — concept-learning HTML on AI Agent (silent-madman, 2026-09-05)
- [LLM Context Window(上下文窗口)](sources/llm-context.md) — concept-learning HTML on LLM context window (silent-madman, 2026-09-05)
- [Skill(技能)](sources/skill.md) — concept-learning HTML on Skill + progressive disclosure (silent-madman, 2026-09-05)
- [上下文工程(Context Engineering)](sources/context-engineering.md) — concept-learning HTML on context engineering + context rot (silent-madman, 2026-09-16)
- [带溯源的智能体长期记忆(Provenance-Aware Memory)](sources/agent-memory-provenance.md) — concept-learning HTML on provenance-aware long-term memory (silent-madman, 2026-09-16)

## Entities
- [Anthropic](entities/Anthropic.md) — creator of Claude; primary source for Agent / Skill / MCP design
- [OpenAI](entities/OpenAI.md) — creator of GPT / ChatGPT; complementary AI vendor
- [SourceScore](entities/SourceScore.md) — third-party agent-rating site referenced for Agent engineering
- [Baidu Baike](entities/BaiduBaike.md) — Chinese encyclopedia referenced for context window basics
- [MemGPT](entities/MemGPT.md) — OS-inspired virtual context management system (Packer et al., 2023)
- [AgentZeroMemory](entities/AgentZeroMemory.md) — provenance-aware long-term memory system (Wu & Zhu, 2026)
- [LongMemEval](entities/LongMemEval.md) — benchmark for long-term interactive memory (Wu et al., ICLR 2025)
- [Zep](entities/Zep.md) — vendored agent memory on temporal context graphs

## Concepts
- [Agent](concepts/Agent.md) — autonomous LLM-driven system with tool use + loop
- [LLM Context](concepts/LLMContext.md) — token-budget that bounds a single inference
- [Context Window](concepts/ContextWindow.md) — English-name redirect to [[LLMContext]]
- [Skill](concepts/Skill.md) — folder of instructions + scripts loaded on demand
- [Progressive Disclosure](concepts/ProgressiveDisclosure.md) — 3-layer load-on-demand pattern
- [Token](concepts/Token.md) — sub-word unit for context accounting
- [ReAct](concepts/ReAct.md) — Reason+Act prompting pattern used by Agents
- [MCP](concepts/MCP.md) — Model Context Protocol for connecting tools
- [Transformer](concepts/Transformer.md) — n²-cost architecture underlying LLMs
- [Context Engineering](concepts/ContextEngineering.md) — discipline of curating the minimal high-signal token set
- [Context Rot](concepts/ContextRot.md) — accuracy decline as context tokens grow
- [Compaction](concepts/Compaction.md) — summarize-and-restart technique for long tasks
- [Long-Term Memory](concepts/LongTermMemory.md) — out-of-window durable state across sessions
- [Provenance](concepts/Provenance.md) — every stored fact carries origin / time / evidence
- [Citation Lock](concepts/CitationLock.md) — answer may cite only evidence actually opened
- [Abstention](concepts/Abstention.md) — refuse to answer when no sourced evidence exists

## Syntheses
- [Overview](overview.md) — living synthesis across all sources
