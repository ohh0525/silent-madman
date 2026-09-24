# Agent / 上下文窗口 / Skill 的关系图谱

> 一份用 Mermaid 流程图 + 文字解析，把「Agent」「上下文窗口」「Skill」三者联系起来的工作笔记；文末「扩展」一节再接入「上下文工程」与「带溯源的长期记忆」两个概念。
> 配套学习资料：[agent.html](./learning-materials/agent.html)、[llm-context.html](./learning-materials/llm-context.html)、[skill.html](./learning-materials/skill.html)、[context-engineering.html](./learning-materials/context-engineering.html)、[agent-memory-provenance.html](./learning-materials/agent-memory-provenance.html)
>
> **行动侧三份（2026-09-22 · 待人工核查）**：[agent-identity.html](./learning-materials/agent-identity.html)、[human-in-the-loop.html](./learning-materials/human-in-the-loop.html)、[tool-hallucination.html](./learning-materials/tool-hallucination.html) —— 对应文末「扩展二 · 行动侧」一节。
>
> **相关图谱（另一领域）**：Python 教学概念组 —— [Python 第 1 课 · 上手四概念的关系图](./concept-group/python-lesson1-starter/关系图.md)、[Python 第 1 课 · 下半场四概念的关系图](./concept-group/python-lesson1-second-half/关系图.md)。两组与本图谱（AI Agent 领域）分属不同知识网，故独立成篇、仅互为索引，不合并进同一张图。

---

## 一句话定位

> **Agent** 用 **Skill** 把专业知识按需装进 **上下文窗口**，三者共同构成一个「懂业务又能跑」的执行系统。

三者既不是平行概念，也不是上下级——它们是**同一个智能体工作流的三个侧面**：

| 概念 | 解决什么问题 | 在系统中扮演的角色 |
|---|---|---|
| **上下文窗口** | 模型这一轮「能看见什么」 | 物理资源：一张有限的桌子 |
| **Agent** | 谁来「决定下一步干什么」 | 组织形态：观察 → 推理 → 行动 的循环 |
| **Skill** | 模型如何「按规矩办事」 | 知识介质：渐进披露加载的经验目录 |

---

## 关系总览

下图展示了「用户提问」从进入到返回结果的全过程，三个概念在何处登场、各自负责什么：

```mermaid
flowchart TB
    subgraph User[用户层]
        U[用户提问]
    end

    subgraph ContextBudget[上下文窗口 - 物理资源]
        SP[系统提示<br/>始终在场]
        SKL[所有 Skill 的 YAML 元数据<br/>始终在场 · 约 100 tokens/个]
        HIST[历史对话 + 工具返回<br/>不断累积]
        RES[预留输出空间]
    end

    subgraph AgentLoop[Agent - 组织形态]
        G[接收目标]
        R{推理下一步}
        TC[决定调用哪个工具]
        EX[执行工具]
        OB[观察结果]
        DONE{目标完成?}
        RET[生成回答 / 交还控制权]
    end

    subgraph Skills[Skill - 知识介质]
        SD[SKILL.md 正文<br/>二级披露]
        SC[scripts/ 可执行脚本<br/>三级披露]
        SA[assets/ 参考资料<br/>三级披露]
    end

    U --> SP
    U --> HIST
    SKL -.被扫描.-> R
    R -->|加载正文| SD
    R -->|调用脚本| SC
    R -->|读取资料| SA
    SD --> TC
    SC --> TC
    SA --> TC
    TC --> EX
    EX --> OB
    OB --> HIST
    OB --> DONE
    DONE -->|否| R
    DONE -->|是| RET
    RET --> RES

    classDef ctx fill:#e7f1fa,stroke:#1a6fb4,color:#1f2328
    classDef agent fill:#fff4e0,stroke:#b35900,color:#1f2328
    classDef skill fill:#efeaf6,stroke:#5b3a8a,color:#1f2328
    class SP,SKL,HIST,RES ctx
    class G,R,TC,EX,OB,DONE,RET agent
    class SD,SC,SA skill
```

---

## 关键循环：Agent × 上下文

把上图压缩成最有用的最小循环，看清楚两者的关系：

```mermaid
sequenceDiagram
    participant User as 用户
    participant Ctx as 上下文窗口
    participant LLM as 大模型
    participant Tool as 工具 / Skill

    User->>Ctx: 1. 写入提问
    activate Ctx
    loop while not done
        LLM->>Ctx: 2. 读取历史 + 元数据
        LLM->>LLM: 3. 推理下一步 (ReAct)
        alt 调用 Skill
            LLM->>Tool: 4a. 加载 SKILL.md 正文/脚本
            Tool-->>Ctx: 5a. 写入结果到上下文
        else 调用外部工具
            LLM->>Tool: 4b. 执行搜索/API/代码
            Tool-->>Ctx: 5b. 写入结果到上下文
        end
        LLM->>Ctx: 6. 判断是否完成
    end
    LLM->>User: 7. 输出回答 (消耗预留空间)
    deactivate Ctx
    Note over Ctx: 容量耗尽时<br/>最早内容被静默截断
```

**这段循环里有一个隐藏张力：**
- 模型每一步都需要在上下文里「思考」——历史越丰富、决策质量越高。
- 但窗口是有限的，每一步的累积都在为下一步挤压空间。
- Agent 不能既「记得多」又「跑得久」，必须在二者之间走钢丝。

---

## Skill 如何帮 Agent 节约上下文

这是 Anthropic 工程博客里强调的「渐进式披露 (Progressive Disclosure)」：

```mermaid
flowchart LR
    L1["一级披露<br/>YAML 元数据 (~100 tokens)<br/>始终在场"]
    L2["二级披露<br/>SKILL.md 正文<br/>按需整篇加载"]
    L3["三级披露<br/>scripts / references / assets<br/>按需逐项读取"]

    L1 -->|匹配任务| L2
    L2 -->|正文指引| L3

    L1 -.始终在.-> Ctx[上下文窗口]
    L2 -.相关时入.-> Ctx
    L3 -.用到时入.-> Ctx

    style L1 fill:#efeaf6,stroke:#5b3a8a
    style L2 fill:#efeaf6,stroke:#5b3a8a
    style L3 fill:#efeaf6,stroke:#5b3a8a
    style Ctx fill:#e7f1fa,stroke:#1a6fb4
```

**对比错误做法**：

| 做法 | 上下文代价 | 实际效果 |
|---|---|---|
| 把所有 Skill 正文常驻 | 假设 10 个 Skill × 2K tokens = 20K，永远占用 | 「全知道」幻觉，token 烧光 |
| 只放元数据 + 用时加载 | 每个常驻 100 tokens，需要时按需加载 | 「用到才加载」，动态控制成本 |

Skill 让 Agent 的「知识库」**理论上无限**、**实际上下文开销接近常数**。

---

## 三者为何不可替代

最容易混淆的边界：

| 想做的事 | 用 | 不该用 |
|---|---|---|
| 想要大模型这次能「看到」100 万字 | 扩大上下文窗口 | 写 Skill；Skill 不会改变窗口物理上限 |
| 想让模型按公司流程做事 | 写 Skill | 在系统提示里堆几千字；会被新会话忘掉 |
| 想要模型自己挑下一步该做啥 | 写 Agent 循环 | 用 Skill；Skill 不解决「下一步是什么」 |
| 想让模型直接操作浏览器 / 数据库 | 写 Agent + 调工具 | 只加大窗口；窗口只是「桌面」，不是「手」 |

**三者各管一摊：**
- **上下文窗口**管**「看得见什么」**（物理）
- **Skill** 管**「按什么规矩办事」**（知识）
- **Agent** 管**「下一步干什么」**（策略）

---

## 一个完整的最小例子

把三者合到一个具体场景里看：

```mermaid
flowchart TB
    A[用户: 把这份 PDF 转成 Excel]
    --> B[上下文窗口]
    B --> C{Agent 推理:<br/>是否加载 PDF Skill?}

    C -->|元数据说: PDF 相关任务| D[读取 Skill B SKILL.md 正文]
    D --> E[按正文指引加载 scripts/convert_pdf.py]
    E --> F[Agent 调用脚本执行转换]
    F --> G[工具返回新 Excel 文件路径]
    G --> H[写入上下文历史]
    H --> I{Agent 判断:<br/>目标完成?}
    I -->|是| J[输出: 已生成 report.xlsx]
    I -->|否| C

    style B fill:#e7f1fa,stroke:#1a6fb4
    style C fill:#fff4e0,stroke:#b35900
    style D,E fill:#efeaf6,stroke:#5b3a8a
    style I fill:#fff4e0,stroke:#b35900
```

**这个流程同时展示了：**
1. **上下文窗口**始终承担当前所有信息（用户问题、Skill 正文、工具结果、历史）的物理存储；
2. **Skill**贡献「怎么转换」的程序化知识和可执行代码；
3. **Agent**决定「什么时候加载 Skill」「什么时候调工具」「什么时候停」。

少任何一样，这个任务都会失败：
- 没有上下文窗口 → 模型失忆
- 没有 Skill → 模型不知道有 convert_pdf.py 可用
- 没有 Agent → 没人决定第一步是读 Skill 还是直接猜答案

---

## 一句话总结

> **上下文是桌面，Skill 是文件夹，Agent 是坐在桌前、按文件夹做事的人。**
> 三者各司其职，组合起来才是一个真正能干活、不会失忆、又守规矩的智能体。

---

## 延伸案例：GitHub Agentic Workflow

[GitHub Agentic Workflows（gh-aw）](https://github.com/github/gh-aw) 是 2026 年 GitHub 官方推出的「在仓库里以 Markdown 写 AI agent 自动化」机制。它把上述「Agent / 上下文窗口 / Skill」的三者关系**实例化到 GitHub Actions 的工作流里**：

| 三者 | 在 gh-aw 里的对应物 |
|---|---|
| **Agent** | YAML frontmatter 中的 `engine`（copilot / codex / claude）+ Markdown body 中的自然语言 prompt |
| **上下文窗口** | 编译产物 `.lock.yml` 里 `GH_AW_PROMPT`、`GH_AW_PROMPT_CONTENT_*`、`GH_AW_GITHUB_*` 等 env vars 把 trigger 上下文（issue 标题、PR diff、评论原文）一次性塞给 agent |
| **Skill** | frontmatter 中 `safe-outputs`（限定 agent 能写的副作用）、`skip-bots`/`skip-roles`（限定谁能触发）、`imports:`（复用其他 .md workflow） |

本仓库的 [.github/workflows/agent-triage-issue.md](./.github/workflows/agent-triage-issue.md) 是这一范式的最小可运行示例：
- **触发**：新 issue 一旦被打开
- **决定下一步**：由 Copilot agent 读 issue 标题 + 描述
- **副作用边界**：通过 `safe-outputs.add-labels` 限定只能打 5 个内置标签之一，且每条 issue 最多改 1 次

它是上面那张「Mermaid 流程图」的最简落地——**没有 Skill 加载层、没有工具调用循环**，只是一个观察→分类→打标签的一次性 agent。这就是「概念」与「实例」的对应关系：

> 概念图谱回答「*为什么需要这三者*」，gh-aw 回答「*这三者在 GitHub Actions 里怎么落地*」。

---

## 扩展：两个新概念如何接进这张网

随着学习深入，又落了两份资料——[context-engineering.html](./learning-materials/context-engineering.html)（上下文工程）与 [agent-memory-provenance.html](./learning-materials/agent-memory-provenance.html)（带溯源的智能体长期记忆）。它们不是三个平行概念之外的"第四、第五个并列项"，而是**分别站在「方法论层」和「时间维度」上，把原来的三者组织起来**：

```mermaid
flowchart TB
    subgraph New[新增 · 方法论与时间维度]
        CE["上下文工程<br/>每一步往窗口里放什么<br/>（取舍与裁剪的方法论）"]
        PM["带溯源的长期记忆<br/>跨会话外存 + 引用锁定<br/>（时间维度上的记忆）"]
    end

    subgraph Old[原有 · 三者]
        CW["上下文窗口<br/>物理资源：有限的桌子"]
        SK["Skill<br/>知识介质：渐进披露目录"]
        AG["Agent<br/>组织形态：观察→推理→行动"]
    end

    CE -->|"管理 / 裁剪 / 再注入"| CW
    CE -->|"渐进披露只是它的一个实例"| SK
    CE -->|"即时检索 / 压缩 / 笔记"| PM
    AG -->|"读写（决定何时记、记什么）"| PM
    PM -->|"提供可信的长期事实"| CW
    SK -->|"按需加载进"| CW

    classDef newe fill:#fbe9f0,stroke:#b3426b,color:#1f2328
    classDef ctx fill:#e7f1fa,stroke:#1a6fb4,color:#1f2328
    classDef agent fill:#fff4e0,stroke:#b35900,color:#1f2328
    classDef skill fill:#efeaf6,stroke:#5b3a8a,color:#1f2328
    class CE,PM newe
    class CW ctx
    class AG agent
    class SK skill
```

**三条新增连线，解释了为什么这两个概念是"接缝"而非"并列"：**

| 关系 | 含义 |
|---|---|
| **上下文工程 → 上下文窗口** | 原来的图谱说"窗口是有限的桌子"，但没说"谁来决定桌上摆什么"。上下文工程补上的正是这层方法论：它是**对窗口的主动管理**，而不是被动接受窗口上限。 |
| **上下文工程 → Skill** | 之前讲的"渐进披露"（一级元数据常驻、正文按需加载）**本身就是上下文工程的一个实例**。Skill 不是孤立的机制，它是"高信号 token 最小集"这条原则在知识加载上的落地。 |
| **Agent ↔ 长期记忆 ← 上下文工程** | 窗口装不下跨会话的状态，于是需要窗口之外的持久存储；**带溯源的长期记忆就是那个外存**，而它"何时写入、写入什么、如何检索再注入"由上下文工程支配，读写动作由 Agent 发起。 |

**与原有"一句话总结"的关系：**

> 原来：**上下文是桌面，Skill 是文件夹，Agent 是坐在桌前、按文件夹做事的人。**
>
> 现在补两句：**上下文工程是这个人"决定桌上摆哪几份材料"的手艺；带溯源的长期记忆则是他身后那排"每份材料都贴着来源与日期标签"的档案柜——取用前必须核对标签，标签对不上就宁可说"我查不到"。**

**边界要点（避免把这五个概念混成一层）：**

- **上下文窗口 vs 上下文工程** = 资源 vs 方法。前者是物理上限，后者是主动取舍。
- **Skill vs 上下文工程** = 实例 vs 原则。Skill 是"渐进披露"的具体载体，不是原则本身。
- **RAG vs 带溯源的长期记忆** = 检索手段 vs 完整记忆系统。前者检索到就用完即弃，后者持久化、会更新、且规定"未打开的证据不得引用"。
- **Agent vs 长期记忆** = 谁去读写 vs 存在哪。Agent 是动作发起方，记忆是状态承载方。

---

## 扩展二：行动侧三份如何接进这张网

> ⚠️ 本节对应的三份材料（`agent-identity.html` / `human-in-the-loop.html` / `tool-hallucination.html`）生成于 2026-09-22，**尚未经本人逐条人工核查**，页脚标为「待人工核查后入库」。

上面五份回答的是「**agent 知道什么、记得什么、凭什么相信**」。可是 agent 一旦从"回答"变成"动手"，还欠三个更靠前的问题——它们共同构成**「信任的行动侧」**：

| 问题 | 概念 | 一句话 |
|---|---|---|
| **谁在动手？** | 智能体身份与委派授权<br/>Agent Identity & Delegated Authority | 可验证的身份 + **只能收窄不能放大**的委派链 |
| **这件事该不该由它自己决定？** | 人在环审批闸门<br/>Human-in-the-Loop / Escalation Gate | 按「影响 × 可逆性」分级，在**不可逆写动作**前插一个可审计、可超时的检查点 |
| **它说它要调用的那个工具，真的存在吗？** | 工具幻觉与封闭世界消解<br/>Tool Hallucination & Closed-World Resolution | **先**做「注册表成员资格 + 签名」的事实核对，**再**谈权限门控 |

```mermaid
flowchart TB
    subgraph Fact["事实侧（已有 · 五份）"]
        PM["带溯源的长期记忆<br/>Provenance / CitationLock / Abstention"]
        CE["上下文工程<br/>每一步放什么"]
    end

    subgraph Action["行动侧（2026-09-22 · 已入库 2026-09-24）"]
        ID["智能体身份<br/>谁在动手 · 代表谁"]
        HITL["人在环审批闸门<br/>该不该由它自己决定"]
        RES["封闭世界消解<br/>这个工具真的存在吗"]
    end

    CW["上下文窗口<br/>物理资源"]

    CE -->|"管理 / 裁剪"| CW
    PM -->|"提供可信的长期事实"| CW
    PM -.->|"事实可信 ≠ 行动者可问责"| ID
    ID -->|"授权范围进入执行路径"| HITL
    HITL -->|"放行的调用才轮到核对"| RES
    RES -->|"核对通过后落到"| AG["Agent<br/>执行动作"]
    HITL -.->|"暂停需持久化<br/>恢复进程未必是原进程"| AG

    classDef fact fill:#fbe9f0,stroke:#b3426b,color:#1f2328
    classDef act fill:#e8eef9,stroke:#2f4f8f,color:#1f2328
    classDef ctx fill:#e7f1fa,stroke:#1a6fb4,color:#1f2328
    classDef agent fill:#fff4e0,stroke:#b35900,color:#1f2328
    class PM,CE fact
    class ID,HITL,RES act
    class CW ctx
    class AG agent
```

**四条新增连线，解释了为什么这三份是"行动侧的接缝"而非"第六、七、八个并列项"：**

| 关系 | 含义 |
|---|---|
| **事实侧 → 身份（虚线）** | 「带溯源的长期记忆」规定每条**事实**带来源、时间、证据；但它对**行动者**没有任何规定。事实可信 **≠** 行动者可问责——这两件事在 provenance 的经典三分（entity / activity / **agent**）里分属不同格，目前的五份只填了 entity 那一格。 |
| **身份 → 闸门** | 身份给出「你是谁、代表谁、被允许做什么」；闸门回答「这件事要不要先问人」。前者是**授权的范围**，后者是**执行的节流**——有身份不等于自动放行，也不等于必须人批。 |
| **闸门 → 消解（顺序不可换）** | 闸门只能对它**放出来的**工具做判定；而幻觉调用指向的工具从未被放出来，因此**不是任何门做过的决策**。所以核对工具是否存在必须**早于**门控，顺序反了就漏掉整整一类失败。 |
| **闸门 ↔ 执行（虚线）** | 一次人工复核可能持续数秒到数天，而恢复流程的进程未必是最初暂停它的那个进程——所以闸门天然要求「运行态持久化」，这也是 `Agent = Model + Harness` 之下还有一层 runtime 的原因。 |

**与「扩展」一节那段话的关系：**

> 原来：**上下文是桌面，Skill 是文件夹，Agent 是坐在桌前、按文件夹做事的人。上下文工程是他决定桌上摆哪几份材料的手艺；带溯源的长期记忆是他身后那排贴着来源与日期标签的档案柜——取用前必须核对标签，标签对不上就宁可说"我查不到"。**
>
> 现在补三句：**这个人在公司里有工牌（身份），工牌上写着"我是谁、我替谁办事、我能动什么"；有的事他得先拿签字（闸门）；而他伸手去拿工具之前，得先确认那个工具真的挂在墙上（消解）——因为墙上没挂的东西，任何签字制度都管不着。**

**行动侧三条之间的边界要点：**

- **身份 vs 闸门** = 逻辑授权 vs 流程控制。前者回答"可不可以"，后者回答"要不要现在做"。
- **闸门 vs 消解** = 上下游，不可互换顺序。消解在最上游，门控在其后。
- **身份 vs 沙箱** = 逻辑授权 vs 物理隔离，不可互替（一个身份完全合法的 agent 仍可能跑在能写穿宿主内核的环境里）。
- **闸门 vs agent 自律（Abstention / CitationLock）** = 主语不同：自律的主语是**模型**、只管"说"；闸门的主语是**系统与人**、管"写 / 付 / 删"。

