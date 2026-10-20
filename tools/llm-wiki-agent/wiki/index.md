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
- [多智能体协作的工程化(Multi-Agent Orchestration)](sources/multi-agent.md) — concept-learning HTML on team@k vs best@k and the verifier precondition (silent-madman, 2026-09-26; secondhand evidence, flagged)
- [记忆的治理:从档案库到策略(Agent Memory: From Archive to Policy)](sources/memory-lifecycle.md) — concept-learning HTML merging memory lifecycle · recall timing · integrity/poisoning · learned policy into one governance spine (silent-madman, 2026-10-06; ingested 2026-10-09, clears five backlog rows)

## Entities
- [Anthropic](entities/Anthropic.md) — creator of Claude; primary source for Agent / Skill / MCP design
- [OpenAI](entities/OpenAI.md) — creator of GPT / ChatGPT; complementary AI vendor
- [SourceScore](entities/SourceScore.md) — third-party agent-rating site referenced for Agent engineering
- [Baidu Baike](entities/BaiduBaike.md) — Chinese encyclopedia referenced for context window basics
- [MemGPT](entities/MemGPT.md) — OS-inspired virtual context management system (Packer et al., 2023)
- [AgentZeroMemory](entities/AgentZeroMemory.md) — provenance-aware long-term memory system (Wu & Zhu, 2026)
- [LongMemEval](entities/LongMemEval.md) — benchmark for long-term interactive memory (Wu et al., ICLR 2025)
- [Zep](entities/Zep.md) — vendored agent memory on temporal context graphs
- [DyadMem](entities/DyadMem.md) — staged long-term-memory benchmark: Capture/Update/Recall/QA with gold annotations at every stage (Tao et al., arXiv:2610.03020, 2026-10-02)

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
- [Long-Term Memory](concepts/LongTermMemory.md) — out-of-window durable state across sessions; a third carrier (latent / soft-token memory) that is not addressable (draft section added 2026-10-17)
- [Provenance](concepts/Provenance.md) — every stored fact carries origin / time / evidence; the garment in which evidence is delivered is its own variable (draft section + cross-row open experiment added 2026-10-20)
- [Citation Lock](concepts/CitationLock.md) — answer may cite only evidence actually opened
- [Abstention](concepts/Abstention.md) — refuse to answer when no sourced evidence exists
- [Agent Identity](concepts/AgentIdentity.md) — who acts, on whose behalf, and authority that only narrows per hop
- [Human-in-the-Loop](concepts/HumanInTheLoop.md) — grade actions by impact × reversibility; read freely, keep writes human
- [Tool Hallucination](concepts/ToolHallucination.md) — calls to non-existent tools; needs a closed-world rung before any gate; scope note: existence is not the injection variable (added 2026-10-20)
- [Agent Harness](concepts/AgentHarness.md) — the engineering shell that runs the Agent loop; `Agent = Model + Harness`
- [Agent Sandbox](concepts/AgentSandbox.md) — kernel-level containment; the `execute` leg — authority is not isolation
- [Multi-Agent Orchestration](concepts/MultiAgent.md) — peer agents exchanging verified progress; the verifier is the precondition; cross-protocol authorization inheritance / protocol pivoting (draft section added 2026-10-16) + substrate-centric coordination, the missing shape for that failure (draft subsection added 2026-10-17) + its own scope note, the three operations presuppose a text wire (draft note added 2026-10-20) + Finding ≠ Fixing, the page is entirely discovery-side (draft section added 2026-10-20)
- [Memory Governance](concepts/MemoryGovernance.md) — memory as four actions that each fail differently + who holds the decision rights; scope note on where the four bottom lines stop applying + intrinsic vs extrinsic evaluation and the open experiment it defines (draft sections added 2026-10-17)
- [Memory Poisoning](concepts/MemoryPoisoning.md) — write-side attack surface: an attacker inherits the decision rights you never claimed

## Syntheses
- [Overview](overview.md) — living synthesis across all sources
