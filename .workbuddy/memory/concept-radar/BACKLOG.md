# 概念雷达 · 候选持久化台账(BACKLOG)

> **用途**:跨天追踪与去重。回答两个问题 ——「这条以前推荐过吗?」「它落地到哪一步了?」
>
> **维护规则**
> 1. **只追加,不删除**;候选提出时新增一行。
> 2. 状态变化时**只改对应行的「状态」与「备注」两列**,不改候选名。
> 3. 每日维护任务(concept-radar)在生成当天报告后,同步追加当天新候选。
>
> **状态三态**(沿用 2026-09-23 起的口径)
>
> | 标记 | 含义 |
> |---|---|
> | ⏸ 已建议未动 | 已在雷达中提出,wiki 中尚无对应页,也未产出材料 |
> | 🟡 材料已出待核查 | `learning-materials/` 下已有 HTML 并已提交,但未入 `raw/`、未摄取(受 README「人工核查承诺」约束) |
> | ✅ 已入 raw 并摄取 | 已放入 `raw/` 并按 CLAUDE.md 的 Ingest Workflow 摄取,`wiki/` 中有 source + concept 页 |
>
> **边界**:本台账**不收录**「备查」类信号(热度高但不适合单列的概念),那些只保留在当日报告里。
>
> 建立于 2026-09-24(回填 09-16 起全部候选)。

## 当前状态汇总

| 状态 | 条数 |
|---|---|
| ✅ 已入 raw 并摄取 | 6 |
| 🟡 材料已出待核查 | 0 |
| ⏸ 已建议未动 | 21 |
| **合计** | **27** |

> ✅ **2026-09-24 更新:入库通道已打通。** 09-22 那 3 条「行动侧」候选(身份 / 人在环 / 工具幻觉)经用户明确授权后已进入 `raw/learning-materials/` 并完成摄取,`🟡` 这一态**归零**。此前 9 天累积的积压全部结清。
>
> ⚠️ 仍需留意的结构事实:雷达已运行 **9 天**、提出 **27 条**候选,其中 **21 条(78%)仍是 `⏸ 已建议未动`** —— 也就是说瓶颈已从「核查」转移到「**决定要不要把它做成材料**」。

---

## 候选清单(按提出日期)

| 期次 | 候选(中 / 英) | wiki 预期落点 | 状态 | 备注 |
|---|---|---|---|---|
| 09-16 | 上下文工程 / Context Engineering | `concepts/ContextEngineering.md` | ✅ 已入 raw 并摄取 | 已产出 `learning-materials/context-engineering.html` |
| 09-16 | 带溯源的智能体长期记忆 / Provenance-Aware Agent Memory | `concepts/Provenance.md` · `LongTermMemory.md` · `CitationLock.md` · `Abstention.md` | ✅ 已入 raw 并摄取 | 已产出 `learning-materials/agent-memory-provenance.html` |
| 09-16 | MCP 无状态化 / Stateless MCP(2026-07-28 规范) | `concepts/MCP.md` · `sources/mcp-2026-07-28.md` | ✅ 已入 raw 并摄取 | 已产出 `learning-materials/agent.html` |
| 09-17 | RAG / 检索增强生成 | 无 `concepts/RAG.md` | ⏸ 已建议未动 | — |
| 09-17 | 智能体评测 / Agent Evals | 无 `concepts/AgentEvals.md` | ⏸ 已建议未动 | 与 09-24 候选 3(模型路由)构成上下游:evals 是路由的决策信号供给 |
| 09-17 | 多智能体共享记忆 / 记忆互操作 | 无 `concepts/AgentMemoryInterop.md` | ⏸ 已建议未动 | 与 09-24 备查「企业上下文层」有交叠,需先厘清边界 |
| 09-18 | Agent Harness / 智能体外壳 | 无 `concepts/AgentHarness.md` | ⏸ 已建议未动 | 09-24 候选 2(上下文卸载)是它内部的一个机制 |
| 09-18 | 子智能体上下文隔离 | 无对应页 | ⏸ 已建议未动 | — |
| 09-18 | 智能体记忆投毒 / Memory Poisoning(ASI06) | 无 `concepts/MemoryPoisoning.md` | ⏸ 已建议未动 | 与 09-24 候选 1(遗忘)是记忆卫生的两端:投毒=写进来的东西是恶意的;遗忘=写进来的东西是陈旧的 |
| 09-19 | A2A 协议 / Agent2Agent | 无 `concepts/A2A.md` | ⏸ 已建议未动 | — |
| 09-19 | 线索锚定的工作记忆 / Cue-Anchored Working Memory | 无 `concepts/CueAnchoredMemory.md` | ⏸ 已建议未动 | — |
| 09-19 | 测试时计算 / 推理预算 / Test-Time Compute | 无 `concepts/TestTimeCompute.md` | ⏸ 已建议未动 | — |
| 09-20 | 提示缓存 / KV 缓存 / Prompt Caching | 无 `concepts/PromptCaching.md` | ⏸ 已建议未动 | 与 09-24 候选 3(模型路由)构成对照:缓存=复用,路由=切换;二者在 compaction 时刻交汇 |
| 09-20 | 工具调用 / 结构化输出 / Tool Use | 无 `concepts/ToolUse.md` | ⏸ 已建议未动 | — |
| 09-20 | 提示词自动优化 / GEPA | 无 `concepts/PromptOptimization.md` | ⏸ 已建议未动 | — |
| 09-21 | 压缩的保真度与安全 / Compaction Fidelity | 无 `concepts/CompactionFidelity.md` | ⏸ 已建议未动 | 09-24 候选 2(卸载)是**绕开**压缩的那条路,两者互补 |
| 09-21 | 记忆调用时机是可学习的策略 / Memory Timing Policy | 无 `concepts/MemoryTimingPolicy.md` | ⏸ 已建议未动 | 与 09-24 候选 1(记忆生命周期)相邻:一个是「何时取」,一个是「何时删」 |
| 09-21 | Agent 沙箱 / 执行隔离 / Agent Sandbox | 无 `concepts/AgentSandbox.md` | ⏸ 已建议未动 | — |
| 09-22 | 智能体身份与委派授权 / Agent Identity & Delegated Authority | `concepts/AgentIdentity.md` | ✅ 已入 raw 并摄取 | **2026-09-24 摄取**(源文件 `raw/learning-materials/agent-identity.html`,源页 `sources/agent-identity.md`);README 标签已从「待核查」改为「已入库」 |
| 09-22 | 人在环审批闸门 / Human-in-the-Loop | `concepts/HumanInTheLoop.md` | ✅ 已入 raw 并摄取 | **2026-09-24 摄取**(源页 `sources/human-in-the-loop.md`);该材料自带来源强度提示,已在源页如实保留 |
| 09-22 | 工具幻觉与封闭世界消解 / Tool Hallucination | `concepts/ToolHallucination.md` | ✅ 已入 raw 并摄取 | **2026-09-24 摄取**(源页 `sources/tool-hallucination.md`,主来源 arXiv:2609.19425v1 **预印本**);材料自身的 `3434 vs 34/3` 口径冲突已如实记录并**未被采用** |
| 09-23 | 持久化执行 / 智能体运行时 / Durable Execution | 无 `concepts/DurableExecution.md` | ⏸ 已建议未动 | 与 09-24 候选 2 共用「窗口外存储」,但目的相反:卸载是让模型少看,持久化执行是让进程不死 |
| 09-23 | 间接提示注入 / 对抗性输入 / Prompt Injection | 无 `concepts/PromptInjection.md` | ⏸ 已建议未动 | — |
| 09-23 | 从自身轨迹中学习 / 自进化智能体 / Self-Improving Agents | 无 `concepts/SelfImprovingAgents.md` | ⏸ 已建议未动 | — |
| 09-24 | **智能体记忆的生命周期治理 / 遗忘 · Memory Lifecycle Governance / Agent Forgetting** ⭐ | 无 `concepts/MemoryLifecycle.md` | ⏸ 已建议未动 | **首选**。已按建议给 `concepts/LongTermMemory.md` 补边界注记(2026-09-24,待摄取后转为正式来源) |
| 09-24 | 上下文卸载 / 文件系统即上下文层 · Context Offloading / Filesystem as Context Layer | 无 `concepts/ContextOffloading.md` | ⏸ 已建议未动 | 承接自 `Compaction.md` 的注记建议(尚未执行) |
| 09-24 | 模型路由 / 成本-质量路由 · Model Routing / Cost-Quality Routing | 无 `concepts/ModelRouting.md` | ⏸ 已建议未动 | 承接 09-23 备查表承诺(「若再现则单列」);与 09-20 提示缓存构成概念对 |

---

## 变更记录

- **2026-09-24** 建台账,回填 09-16 起全部 **27** 条候选(3 ✅ / 3 🟡 / 21 ⏸)。同日为 09-24 候选 1 执行了「给 `LongTermMemory.md` 补边界注记」这一低成本动作。
- **2026-09-24(同日稍后)** 用户授权摄取,09-22 的 3 条「行动侧」候选由 🟡 转为 **✅**;`wiki/` 源页 6 → **9**,wiki 页数 31 → **34**,新增 concept 页 `AgentIdentity` / `HumanInTheLoop` / `ToolHallucination`,并追加更新 `MCP`(授权 profile + 命名空间合并风险)与 `Agent`(权限轴);`overview.md` 完成一次**真正的 synthesis 修订**(新增行动侧 Cluster D)。汇总态变为 **6 ✅ / 0 🟡 / 21 ⏸**。
