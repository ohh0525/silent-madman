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
- [Progressive Disclosure](concepts/ProgressiveDisclosure.md) — 3-layer load-on-demand pattern; + the premise of load-on-demand is that it loads — the always-loaded vs on-demand allocation rule (100% vs 53%, 10-09, 2026-10-26)
- [Token](concepts/Token.md) — sub-word unit for context accounting
- [ReAct](concepts/ReAct.md) — Reason+Act prompting pattern used by Agents
- [MCP](concepts/MCP.md) — Model Context Protocol; stateless as of the 2026-07-28 spec
- [RAG (Retrieval-Augmented Generation)](concepts/RAG.md) — 朴素 RAG 作为「所有记忆方案必须打赢的基线」；memory benefit / memory tax / 净值三元组；两处失败轴（注意力 vs 真值）之外的第三方——取用值不值（2026-10-29 新建，pending ingest）
- [Transformer](concepts/Transformer.md) — n²-cost architecture underlying LLMs
- [Context Engineering](concepts/ContextEngineering.md) — discipline of curating the minimal high-signal token set; + the resident budget — the tokens this page never prices (capacitated assortment, 10-09, 2026-10-26); + the re-sent context is ~62% of the inference bill (09-25 cross-check, 2026-10-26)
- [Context Rot](concepts/ContextRot.md) — accuracy decline as context tokens grow
- [Compaction](concepts/Compaction.md) — summarize-and-restart technique for long tasks; + compaction is not neutral — it drops the constraint class ~6× faster than the spec class, and the task score does not move (draft section added 2026-10-26); + the lower bound for recompute-vs-store: Θ(n²/(C+S)+n) model calls (10-09-2, 2026-10-26)
- [Long-Term Memory](concepts/LongTermMemory.md) — out-of-window durable state across sessions; a third carrier (latent / soft-token memory) that is not addressable (draft section added 2026-10-17; + the third carrier is scored only on aggregate accuracy, which hides 8–13% per-decision revision loss, 2026-10-21); + retrieved ≠ operative — the projection is a second object (10-24B, 2026-10-26)
- [Provenance](concepts/Provenance.md) — every stored fact carries origin / time / evidence; the garment in which evidence is delivered is its own variable (draft section + cross-row open experiment added 2026-10-20); + provenance as model-side discipline vs the harness-side enforcement point (2026-10-21); + provenance must be reversible — the backward pointer is only half of it (2026-10-25); + invalidation is non-local while dependency is local — a record's truth expires where its metadata cannot see (2026-10-26)
- [Citation Lock](concepts/CitationLock.md) — answer may cite only evidence actually opened
- [Abstention](concepts/Abstention.md) — refuse to answer when no sourced evidence exists; + a refusal is an output channel, not a terminal state (draft section added 2026-10-25); + abstention is not binary — it is a budget decision priced by what happens next: proceed → verify → direct abstention (10-24A, 2026-10-26)
- [Agent Identity](concepts/AgentIdentity.md) — who acts, on whose behalf, and authority that only narrows per hop; + per-hop narrowing is not narrowing over the batch (draft section added 2026-10-25)
- [Human-in-the-Loop](concepts/HumanInTheLoop.md) — grade actions by impact × reversibility; read freely, keep writes human; + persistence of directives / authority erosion (10-20C) + the gate does not know where its arguments came from / per-argument authorization (10-21A, design-only — not implemented); draft sections added 2026-10-21; + a rule in code is not enough, it must also survive compaction (2026-10-26); + the grading scale is mounted one layer too high — premises are priced by consequence (10-24A) + reversibility is a supposition until someone supplies it (10-24C) + a promise is a gate object, decidable without a trajectory (10-09E), 2026-10-26
- [Tool Hallucination](concepts/ToolHallucination.md) — calls to non-existent tools; needs a closed-world rung before any gate; scope note: existence is not the injection variable (added 2026-10-20); + cross-turn feasibility — the registry answers *does it exist*, the affordance set answers *can anyone run it after this turn* (10-09E, 2026-10-26)
- [Agent Harness](concepts/AgentHarness.md) — the engineering shell that runs the Agent loop; `Agent = Model + Harness`; + the duty the four omit — make the action reversible before it happens ($0.014/task backup layer, 10-24C, 2026-10-26); + the harness has a bill — four metered resources, LAM's provable lower bounds (10-09-2, 2026-10-26)
- [Agent Sandbox](concepts/AgentSandbox.md) — kernel-level containment; the `execute` leg — authority is not isolation; + containment ≠ restorability — bounding what can be touched is half the job (10-24C, 2026-10-26)
- [Agent Observability & Evaluation](concepts/AgentObservability.md) — trace answers「发生了什么」, eval answers「做得好不好」, the trust layer answers「这条 pass 该不该被相信」— record / semantic / judge / meta / cost layers, structural merge of four ledger rows (10-08 + 09-17 + 10-09-3 + 09-25; draft page created 2026-10-26, pending ingest)
- [Multi-Agent Orchestration](concepts/MultiAgent.md) — peer agents exchanging verified progress; the verifier is the precondition; cross-protocol authorization inheritance / protocol pivoting (draft section added 2026-10-16) + substrate-centric coordination, the missing shape for that failure (draft subsection added 2026-10-17) + its own scope note, the three operations presuppose a text wire (draft note added 2026-10-20) + Finding ≠ Fixing, the page is entirely discovery-side (draft section added 2026-10-20) + what a flag must earn before it costs a retry, i.e. repair pricing for the verifier predicate (draft subsection added 2026-10-25) + autonomous vs user-serving, the second precondition (2026-10-22)
- [Memory Governance](concepts/MemoryGovernance.md) — memory as four actions that each fail differently + who holds the decision rights; scope note on where the four bottom lines stop applying + intrinsic vs extrinsic evaluation and the open experiment it defines (draft sections added 2026-10-17; + scoped vs unscoped revision as the experiment's first half-leg, a Permissioned scope refinement and the protection-descriptor mechanism for Permissioned itself, 2026-10-21) + deletion is not closed at the record layer, DELETE needs closure semantics (2026-10-25); + UPDATE can be triggered upstream, with nothing in the bank changing (10-26A) + Recall rewrites the input to Capture, the pipeline has no return edge (10-26C), 2026-10-26; + Recall has no cost model — verification effort is priced by the action, not by the record (10-24A) + the fourth column of memory failure — the selection layer / control plane (10-24B), 2026-10-26
- [Memory Poisoning](concepts/MemoryPoisoning.md) — write-side attack surface: an attacker inherits the decision rights you never claimed; + exposure ≠ behaviour ≠ state — correct content belonging to the wrong principal (draft section added 2026-10-21)

## Syntheses
- [Overview](overview.md) — living synthesis across all sources
