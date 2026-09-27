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
| ✅ 已入 raw 并摄取 | 9 |
| 🟡 材料已出待核查 | 0 |
| ⏸ 已建议未动 | 22 |
| **合计** | **31** |

> ✅ **2026-09-24 更新:入库通道已打通。** 09-22 那 3 条「行动侧」候选(身份 / 人在环 / 工具幻觉)经用户明确授权后已进入 `raw/learning-materials/` 并完成摄取,`🟡` 这一态**归零**。此前 9 天累积的积压全部结清。
>
> ⚠️ 仍需留意的结构事实:雷达已运行 **9 天**、提出 **27 条**候选,其中 **21 条(78%)仍是 `⏸ 已建议未动`** —— 也就是说瓶颈已从「核查」转移到「**决定要不要把它做成材料**」。
>
> ⚠️ **2026-09-27 更新上述结构事实**:雷达已运行 **12 天**、提出 **31 条**候选,其中 **22 条(71%)仍是 `⏸`**。09-24 之后「核查」瓶颈已被打通(09-24 与 09-26 两天共 6 条候选经用户授权当日全链路落地),但**未动比例仍高达七成**——瓶颈依旧在「**决定要不要把它做成材料**」,且 09-25/09-27 两条新候选被明确标注「**建议等基准结果再成文**」(记忆时效性)与「**不建议单独成文**」(评测经济学),说明「该等/该并」本身也是一种处置。

---

## 候选清单(按提出日期)

| 期次 | 候选(中 / 英) | wiki 预期落点 | 状态 | 备注 |
|---|---|---|---|---|
| 09-16 | 上下文工程 / Context Engineering | `concepts/ContextEngineering.md` | ✅ 已入 raw 并摄取 | 已产出 `learning-materials/context-engineering.html` |
| 09-16 | 带溯源的智能体长期记忆 / Provenance-Aware Agent Memory | `concepts/Provenance.md` · `LongTermMemory.md` · `CitationLock.md` · `Abstention.md` | ✅ 已入 raw 并摄取 | 已产出 `learning-materials/agent-memory-provenance.html` |
| 09-16 | MCP 无状态化 / Stateless MCP(2026-07-28 规范) | `concepts/MCP.md` · `sources/mcp-2026-07-28.md` | ✅ 已入 raw 并摄取 | 已产出 `learning-materials/agent.html` |
| 09-17 | RAG / 检索增强生成 | 无 `concepts/RAG.md` | ⏸ 已建议未动 | **09-27 承接强化(证据性质变化,非重复推荐)**:已从「你缺一页 RAG 基础」变为「**RAG 的默认起点本身被推翻**」——Amazon Science 在 AAAI 2026 的《Keyword Search Is All You Need》(Subramanian 等,同 LLM/同 6 数据集/同评测框架,唯一变量是检索器)实证:无向量库的 agentic 关键词检索达成 RAG 的 **Faithfulness 94.5%**、Context Recall 88.0%、Answer Correctness 91.5%,且在长表格密集的 FinanceBench 上**反转胜出**(30.40% > 24.24%);Search-R1(arXiv 2503.09516)用 RL 训检索策略,多跳 QA 相对 **+24%**;Windsurf / Cline / Devin / Sourcegraph Amp 已在编码场景放弃 embedding。仍是 overview **最老**的开放项。**建议下一步**:生成 `learning-materials/agentic-rag.html`(青碧) |
| 09-17 | 智能体评测 / Agent Evals | 无 `concepts/AgentEvals.md` | ⏸ 已建议未动 | 与 09-24 候选 3(模型路由)构成上下游:evals 是路由的决策信号供给 |
| 09-17 | 多智能体共享记忆 / 记忆互操作 | 无 `concepts/AgentMemoryInterop.md` | ⏸ 已建议未动 | 与 09-24 备查「企业上下文层」有交叠,需先厘清边界 |
| 09-18 | Agent Harness / 智能体外壳 | `concepts/AgentHarness.md` **已建** | ✅ 已入 raw 并摄取 | 09-24 候选 2(上下文卸载)是它内部的一个机制。**09-26 承接强化**:当时只有一句话,2026-09 被三方同时产品化——**OpenAI 2026-09-10 把 Codex harness 做成 Agents API 公测**(automatic compaction / tool search / programmatic tool calling / `max_concurrent_subagents`,环境可选 openai_hosted / self_hosted / none,9 家沙箱合作方)、**Anthropic 以 Opus 5.5 打「托管编排」**、Agent Brief 09-25 命名为「**Harness Wars**」并定性「orchestration as managed infrastructure」。被列为 09-26 ⭐ 首选,理由:一次成文激活最多既有节点,且是 concept-relationship.md 缺的**底座层**。**09-26(同日)全链路落地**:用户指令「1」选定 → concept-explainer 产出 HTML → 用户指令「你帮我做完」授权完成 raw 投递 + 摄取(wiki 源 9→10、页 37→39,新增 [[AgentHarness]] 概念页与 [[Agent]] 运行时轴,overview 新增 Cluster E)+ `concept-relationship.md`「扩展三 · 运行时底座」。入库方式为用户指令授权自动化,非逐条人工核查,已在 wiki log 与 README 如实标注 |
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
| 09-21 | Agent 沙箱 / 执行隔离 / Agent Sandbox | `concepts/AgentSandbox.md` **已建** | ✅ 已入 raw 并摄取 | **09-25 承接强化**:当时仅是 overview Open Question 一句话,本周被 Docker Cloud Sandboxes(2026-09-24,microVM + OCI Kits→CNCF)与 Nvidia OpenShell(2026-09-21,策略在推理环之外)各自产品化,证据强度完全不同,当周被列为 ⭐ 首选。与 09-23 持久化执行可合并成文(Docker 已把两者捆在同一产品里)。**09-26 承接强化(连续第二次,变的是证据"性质"而非热度)**:从「厂商发产品」升级为「**被标准化为基础设施原语**」——`kubernetes-sigs/agent-sandbox` 作为 **SIG Apps 子项目**提供声明式 `Sandbox` CRD(gVisor 默认 / Kata 可插拔 / warm pool 300 沙箱每秒 / suspend-resume),GKE 版 2026-05-20 GA、5 个月增长 16×、LangChain 与 Lovable 部署数百万 agent;**Google 开源 AX**(Apache 2.0,Task/Workspace/Gateway/Model);**阿里云智能体沙箱 2026-09-22 正式商业化**(10 万沙箱/分钟、百万级并发、独立 VM、兼容 E2B 与 K8s API)。与 09-26 候选 1(harness)可合成一篇「Agent 运行时」(上半编排 / 下半执行)。**09-26(同日)全链路落地**:用户指令「继续做」授权——`agent-sandbox.html` 产出并入 raw、摄取(源 10→11、页 39→41,新增 [[AgentSandbox]],overview Cluster E 补执行层、行动侧链 execute 格关闭),`concept-relationship.md` 增「扩展四 · 执行隔离」。入库方式为用户指令授权,非逐条人工核查,已在 wiki log 与 README 如实标注 |
| 09-22 | 智能体身份与委派授权 / Agent Identity & Delegated Authority | `concepts/AgentIdentity.md` | ✅ 已入 raw 并摄取 | **2026-09-24 摄取**(源文件 `raw/learning-materials/agent-identity.html`,源页 `sources/agent-identity.md`);README 标签已从「待核查」改为「已入库」 |
| 09-22 | 人在环审批闸门 / Human-in-the-Loop | `concepts/HumanInTheLoop.md` | ✅ 已入 raw 并摄取 | **2026-09-24 摄取**(源页 `sources/human-in-the-loop.md`);该材料自带来源强度提示,已在源页如实保留 |
| 09-22 | 工具幻觉与封闭世界消解 / Tool Hallucination | `concepts/ToolHallucination.md` | ✅ 已入 raw 并摄取 | **2026-09-24 摄取**(源页 `sources/tool-hallucination.md`,主来源 arXiv:2609.19425v1 **预印本**);材料自身的 `3434 vs 34/3` 口径冲突已如实记录并**未被采用** |
| 09-23 | 持久化执行 / 智能体运行时 / Durable Execution | 无 `concepts/DurableExecution.md` | ⏸ 已建议未动 | **09-27 承接强化(连续关注,证据性质升级)**:当时只是「与 09-24 候选 2 共用窗口外存储、目的相反」的一句判断;现已成为 **harness(09-26 新建)的下一层**——LangChain 原话「*To build a good agent, you need a good harness. To deploy that agent, you need a good runtime. The runtime is everything underneath*」。变了的是**证据类别**,不是热度:①**2026-09-19 首次出现中立的多运行时恢复语义对比**(Seed Hypermedia:证据截止 09-17),直接补上 overview 自认「尚未写」的那句;②确立 **checkpoint ≠ durable execution**(检查点保留控制状态,不是下游副作用的 exactly-once);③「resume」在四家**不是同一个操作**(Temporal 事件历史重放 / DBOS 按持久化位点采纳已完成操作 / MS Agent Framework superstep 检查点 / LangGraph 线程快照 + pending writes);④Nirvana Labs 给出可引用的判据句「问厂商的不是它**是否**持久化,而是**一次没人安排的 kill 之后还剩什么**」。**建议下一步**:生成 `learning-materials/durable-execution.html`(深灰蓝);**只改本行备注,不新增行** |
| 09-23 | 间接提示注入 / 对抗性输入 / Prompt Injection | 无 `concepts/PromptInjection.md` | ⏸ 已建议未动 | — |
| 09-23 | 从自身轨迹中学习 / 自进化智能体 / Self-Improving Agents | 无 `concepts/SelfImprovingAgents.md` | ⏸ 已建议未动 | — |
| 09-24 | **智能体记忆的生命周期治理 / 遗忘 · Memory Lifecycle Governance / Agent Forgetting** ⭐ | 无 `concepts/MemoryLifecycle.md` | ⏸ 已建议未动 | **首选**。已按建议给 `concepts/LongTermMemory.md` 补边界注记(2026-09-24,待摄取后转为正式来源) |
| 09-24 | 上下文卸载 / 文件系统即上下文层 · Context Offloading / Filesystem as Context Layer | 无 `concepts/ContextOffloading.md` | ⏸ 已建议未动 | 承接自 `Compaction.md` 的注记建议(尚未执行) |
| 09-24 | 模型路由 / 成本-质量路由 · Model Routing / Cost-Quality Routing | 无 `concepts/ModelRouting.md` | ⏸ 已建议未动 | 承接 09-23 备查表承诺(「若再现则单列」);与 09-20 提示缓存构成概念对;评测经济学(09-25 候选 3)是其成本侧背景 |
| 09-25 | 记忆时效性 / 「旧记忆比没记忆更糟」 · Memory Freshness / Stale-Memory Evaluation | 无 `concepts/MemoryFreshness.md` | ⏸ 已建议未动 | Agent Memory Challenge Cycle 2(2026-09-20 开赛,11-04 截止,11 月中出结果)**建议等结果再成文**;与 [[Provenance]]/[[CitationLock]]/[[Abstention]] 构成真实性三闸门;与 09-24 候选 1(生命周期)为上下游 |
| 09-25 | Agent 评测经济学 / 评测税 · Agent Evaluation Economics | 无 `concepts/EvaluationEconomics.md` | ⏸ 已建议未动 | 三条中最不急:建议作为 09-17 候选 2(Agent Evals)材料的成本章,不单独成文;「~62% 推理账单来自重发上下文」(Stanford,二手转述)值得记进 [[ContextEngineering]] 开篇 |
| 09-26 | 多智能体协作的工程化 · Multi-Agent Orchestration | `concepts/MultiAgent.md` **已建** | ✅ 已入 raw 并摄取 | **本期唯一新增候选**。全库 37 页零覆盖(所有图都是单 agent)。2026-09 三线证据:微软研究院 + UC Berkeley「team@k vs best@k」(ARC-AGI-3 team@5=best@33;LP85 独立 64 次全败 vs team@5 65%;且**无验证器或算力紧张时独立 agent 反而更好**)、Anthropic Claude Code Projects(2026-09-17 beta,协调者+并行云端线程+共享记忆,重叠按 merge conflict)、微软 Agensh(无中央编排者扩到 1,024 agent)。与 09-17(多智能体共享记忆,记忆侧)、09-18(子智能体上下文隔离,单 agent 内部)相邻但不同;与 09-26 候选 1(harness)是「harness 的一个已产品化能力」但作为概念有独立取舍逻辑。新失效面:**多 agent 间未验证结论被当作前提继承(互相污染)**。**09-26(同日)全链路落地**:用户指令「继续做」授权——`multi-agent.html` 产出并入 raw、摄取(源 11→12、页 41→43,新增 [[MultiAgent]],overview Cluster E 补协作层、新增横断主题「验证器是协作的前提」),`concept-relationship.md` 增「扩展五 · 多智能体协作」。证据等级二手(AlphaSignal/AGI Hunt 报道,arXiv 摘要未开)已在材料、源页与 overview 三处标注,arXiv 一手已列入 Next Ingest Suggestions |
| 09-27 | **智能体记忆治理 / 记忆的权限·冲突·审计 · Agent Memory Governance** | 无 `concepts/MemoryGovernance.md` | ⏸ 已建议未动 | **本期唯一新增候选**。直接回应 overview 自认开放的治理侧:「the governance side — **RBAC on shared memory, who may write what** — remains open」(编排侧已被 09-26 的 [[MultiAgent]] 覆盖)。现有记忆簇四页(Provenance / CitationLock / Abstention / LongTermMemory)**只治理单 agent 跨会话的事实来源**,对「谁能往共享记忆里写、冲突谁裁决、写错了怎么撤」零覆盖。2026-09 产业证据齐备:①**三种共享记忆架构**(分层知识图谱 / 事件驱动 append-only 日志 = HydraDB Hive Memory / 监督者+私有记忆,各换一致性 vs 吞吐);②**冲突四策略**(last-write-wins / supervisor decides / versioning 保留多个真相 / temporal ordering);③企业记忆 **「Git-like 五原则」**(Scoped / Versioned / Reviewable / Auditable / **Portable**);④**治理四层**(身份与授权 / 编排控制 / **数据与记忆治理** / 运行时观测);⑤中文源的组织级记忆三层内容架构(宪法 / 典籍 / 战报)。与 09-24 候选 1(生命周期/遗忘)**上下游但不同**:治理管「**谁能写**」,生命周期管「**何时删**」。与 [[AgentIdentity]] 那句「事实可信 ≠ 行动者可问责」**同构**。**建议下一步**:生成 `learning-materials/agent-memory-governance.html`(砖橙);**不建议**与 09-23 持久化执行合并成文(制度层 vs 执行层,取舍逻辑不同) |

---

## 变更记录

- **2026-09-24** 建台账,回填 09-16 起全部 **27** 条候选(3 ✅ / 3 🟡 / 21 ⏸)。同日为 09-24 候选 1 执行了「给 `LongTermMemory.md` 补边界注记」这一低成本动作。
- **2026-09-24(同日稍后)** 用户授权摄取,09-22 的 3 条「行动侧」候选由 🟡 转为 **✅**;`wiki/` 源页 6 → **9**,wiki 页数 31 → **34**,新增 concept 页 `AgentIdentity` / `HumanInTheLoop` / `ToolHallucination`,并追加更新 `MCP`(授权 profile + 命名空间合并风险)与 `Agent`(权限轴);`overview.md` 完成一次**真正的 synthesis 修订**(新增行动侧 Cluster D)。汇总态变为 **6 ✅ / 0 🟡 / 21 ⏸**。
- **2026-09-25** 新增 2 条候选(记忆时效性 / 评测经济学);另将 09-21「Agent 沙箱」行标注**承接强化**(本周 Docker Cloud Sandboxes + Nvidia OpenShell 各自产品化,09-25 报告将其列为 ⭐ 首选,属同义候选的证据升级而非重复推荐)。汇总态变为 **6 ✅ / 0 🟡 / 23 ⏸**。
- **2026-09-26** 新增 **1** 条候选(多智能体协作的工程化);另将 **09-18「Agent Harness」** 与 **09-21「Agent 沙箱」** 两行标注**承接强化**,当日报告将其并列为 ⭐ 首选与次选。两条均**只改备注、不新增行**——其中沙箱是连续第二天承接强化,本次强调「变的是证据的性质(产品→基础设施原语)而非热度」,该判据已写进当日报告的经验节。汇总态变为 **6 ✅ / 0 🟡 / 24 ⏸**(合计 30)。
- **2026-09-26(同日稍后)** 用户以指令「1」选定 09-26 候选 1(Agent Harness)为落地对象;`learning-materials/agent-harness.html` 由 concept-explainer Skill 产出并提交,README 已生成清单同步登记。09-18 行状态 ⏸ → **🟡**。汇总态变为 **6 ✅ / 1 🟡 / 23 ⏸**(合计 30)。
- **2026-09-26(再稍后)** 用户指令「你帮我做完」,授权自动化完成全链路:HTML 复制入 `raw/learning-materials/`(md5 一致)→ 按 Ingest Workflow 摄取(源 9→**10**、wiki 页 37→**39**:新增 `sources/agent-harness.md` 与 `concepts/AgentHarness.md`,`[[Agent]]` 增运行时轴,`overview.md` 新增 **Cluster E** 与两条新横断主题)→ `concept-relationship.md` 新增「扩展三 · 运行时底座」并修正两条 09-24 已过时的「待核查」标注。09-18 行 🟡 → **✅**。汇总态变为 **7 ✅ / 0 🟡 / 23 ⏸**(合计 30)。**注意:本次入库为用户指令授权,非逐条人工核查,已在 wiki log.md、README 与来源页如实标注**。
- **2026-09-26(晚间)** 用户指令「继续做」,候选 2(Agent 沙箱)全链路落地:`agent-sandbox.html` 产出并入 `raw/`(md5 一致)→ 摄取(源 10→**11**、wiki 页 39→**41**:`sources/agent-sandbox.md` + `concepts/AgentSandbox.md`,overview Cluster E 补执行层、行动侧链 `execute` 格关闭、open question「执行隔离 missing third leg」标记 resolved)→ `concept-relationship.md`「扩展四 · 执行隔离」+ 扩展三沙箱节点更新。09-21 行 ⏸ → **✅**。汇总态 **8 ✅ / 0 🟡 / 22 ⏸**。同轮修复:发现并补回上轮丢失的 overview 两处编辑(open questions sharpened + OpenAI docs 摄取建议),已在 wiki log 记录。
- **2026-09-26(更晚)** 候选 3(多智能体协作)全链路落地:`multi-agent.html`(靛青)产出并入 raw(md5 一致)→ 摄取(源 11→**12**、页 41→**43**:`sources/multi-agent.md` + `concepts/MultiAgent.md`;overview Cluster E 补协作层并改题「host / where it runs / who it works with」、十二页故事、新横断主题「验证器是协作的前提」;open question「多智能体共享记忆」标注编排侧已覆盖、治理侧仍开放)→ `concept-relationship.md`「扩展五 · 多智能体协作」。09-26 行 ⏸ → **✅**。**至此 2026-09-26 雷达三条候选全部当日落地**。汇总态 **9 ✅ / 0 🟡 / 21 ⏸**(合计 30)。证据等级二手已三处标注。
- **2026-09-27** 新增 **1** 条候选(**智能体记忆治理 / Agent Memory Governance** —— 补上 overview 自认开放的「治理侧」);另将 **09-17「RAG」** 与 **09-23「持久化执行」** 两行标注**承接强化**。两条均**只改备注、不新增行**,且本次强化强调的是「**变化的是证据的性质,不是热度**」:RAG 从「缺一页基础」变为「**默认起点被 AAAI 2026 论文推翻**」;持久化执行从「Temporal 已存在」变为「**四个运行时恢复语义首次被中立并列 + checkpoint ≠ durable execution**」。汇总态变为 **9 ✅ / 0 🟡 / 22 ⏸**(合计 31)。
