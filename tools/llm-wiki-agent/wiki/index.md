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
- [MCP 2026-07-28 Specification(MCP 无状态化修订)](sources/mcp-2026-07-28.md) — spec digest: MCP becomes stateless (official blog + docs + AWS + GitHub, 2026-09-16)
- [智能体身份与委派授权(Agent Identity & Delegated Authority)](sources/agent-identity.md) — concept-learning HTML on workload identity, RFC 8693 delegation and per-hop attenuation (silent-madman, 2026-09-22)
- [人在环审批闸门(Human-in-the-Loop / Escalation Gate)](sources/human-in-the-loop.md) — concept-learning HTML on grading actions and gating irreversible writes (silent-madman, 2026-09-22)
- [工具幻觉与封闭世界消解(Tool Hallucination & Closed-World Resolution)](sources/tool-hallucination.md) — concept-learning HTML on the pre-gate resolution rung (silent-madman, 2026-09-22; primary source arXiv:2609.19425v1)
- [Agent Harness(智能体外壳)](sources/agent-harness.md) — concept-learning HTML on the engineering shell that hosts the loop (silent-madman, 2026-09-26; "Harness Wars" evidence)
- [Agent 沙箱与执行隔离(Agent Sandbox / Execution Isolation)](sources/agent-sandbox.md) — concept-learning HTML on kernel-level containment as the `execute` leg (silent-madman, 2026-09-26; K8s SIG Apps upstream)

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
- [MCP](concepts/MCP.md) — Model Context Protocol; stateless as of the 2026-07-28 spec
- [Transformer](concepts/Transformer.md) — n²-cost architecture underlying LLMs
- [Context Engineering](concepts/ContextEngineering.md) — discipline of curating the minimal high-signal token set
- [Context Rot](concepts/ContextRot.md) — accuracy decline as context tokens grow
- [Compaction](concepts/Compaction.md) — summarize-and-restart technique for long tasks
- [Long-Term Memory](concepts/LongTermMemory.md) — out-of-window durable state across sessions
- [Provenance](concepts/Provenance.md) — every stored fact carries origin / time / evidence
- [Citation Lock](concepts/CitationLock.md) — answer may cite only evidence actually opened
- [Abstention](concepts/Abstention.md) — refuse to answer when no sourced evidence exists
- [Agent Identity](concepts/AgentIdentity.md) — who acts, on whose behalf, and authority that only narrows per hop
- [Human-in-the-Loop](concepts/HumanInTheLoop.md) — grade actions by impact × reversibility; read freely, keep writes human
- [Tool Hallucination](concepts/ToolHallucination.md) — calls to non-existent tools; needs a closed-world rung before any gate
- [Agent Harness](concepts/AgentHarness.md) — the engineering shell that runs the Agent loop; `Agent = Model + Harness`
- [Agent Sandbox](concepts/AgentSandbox.md) — kernel-level containment; the `execute` leg — authority is not isolation

## Syntheses
- [Overview](overview.md) — living synthesis across all sources
