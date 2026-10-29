---
title: "RAG (Retrieval-Augmented Generation)"
type: concept
tags: [rag, retrieval, baseline, memory-tax, net-value, chunking, assistant]
sources: []
last_updated: 2026-10-29
---

# RAG (Retrieval-Augmented Generation) — 以及它作为「基线」的身份

**朴素 RAG 不是一种记忆方案，而是所有记忆方案必须打赢的那个对手。** 它把原始历史切块、检索、拼进上下文，**不做任何记忆处理**（不抽取原子事实、不整合、不蒸馏偏好、不维护摘要）——正因为什么都不做，它才是唯一能用来「记账」的零点。

> **Draft annotation, pending ingest.** 本页 2026-10-29 建立，源材料为雷达候选 **10-29A**（`arXiv:2610.34073`）；**尚无可摄取的 source 页**，因此 `sources:` 保持为空。摄取时把 slug 移入 frontmatter 并删除本横幅。该页同时承担一个长期悬空项的部分结清，见下「开放项」。

## 为什么现在才建这一页

本库 wiki 存在 20 天，`concepts/` 下**一直没有 RAG 页**：`RAG` 一词在全库仅出现 5 次，分散在 [[AgentObservability]] / [[LLMContext]] / [[LongTermMemory]] / [[Provenance]] / [[Zep]] 各一次，全是顺带提及。而 `overview.md` 的**最老开放项**（*"A concrete RAG system case study (vector DB choice, chunking strategy, retrieval quality)"*，记于 **2026-09-09**）与台账**最老未落地 `⏸` 行**（**09-17 RAG**，至 2026-10-29 重算 **42 天**）**两条独立计数长期指向同一件事**。

⇒ 这条缺口的真实形态不是「没人有空写」，而是**没有可引用的仪器**：在 `arXiv:2610.34073` 之前，本库没有任何证据能回答「做记忆到底值不值」。所以本页的写法不是「RAG 综述」，而是**把 RAG 钉成基线**。

## 三条判据句

- **基线不是选项，是零点。** 判断一个记忆系统，先问「朴素 RAG 在这题上得几分、建库要几小时」。
- **任何对原始历史的偏离都是双刃的。** 抽取原子事实、链接会话、锚定时间、改写内容 —— 命中问题时是收益（**memory benefit**），丢掉或埋掉证据时是税（**memory tax**）。净值 = benefit − tax。
- **天花板低的时候，税才显形。** 一批长期记忆基准上，**无向量的 IDF 关键词匹配也能过 50%**、混合检索约 **70%** ⇒ 任务本身对检索友好，于是「记忆到底加了什么」被掩盖。

## 记忆税 / Memory Tax 的记账框架（候选 10-29A）

`arXiv:2610.34073`（v1 **2026-10-25 05:29:05 UTC**；Xuan He 等 **11 人**，UIUC 为主 + 清华 / 人大 / Waterloo / Verdent.ai；cs.CL；项目页 `hexuan21.github.io/MemoryTax`）。

**实验设计（这几点是本页敢把它当仪器的原因）**

| 维度 | 设置 |
|---|---|
| 被测 | **11 个记忆系统**，按存储方式分四族：扁平（A-Mem / SimpleMem / MemOS）· 层级-生命周期（MemoryOS / LightMem / OpenViking）· 图（HippoRAG2 / PlugMem / MAGMA）· 训练策略（Mem-T / Memory-R2） |
| 基准 | LongMemEval-s（全 500 问）· PersonaMem-v2（20%，934 问）· MINT-Eval（10%，1,557 问） |
| 骨干 | Qwen3.5-4B · Qwen3.6-27B · GPT-5.6-luna |
| 参照 | **朴素 RAG**（原始历史分块检索，无记忆处理），**one-round 与 two-round 两版** |
| 控制 | 统一 embedding、**对齐 retrieval scope**（把 top-k 上调，先堵住「记忆系统只是拿到的更少」这一反驳）、LLM judge 评分 |

**结果**

- LongMemEval-s / 27B 骨干：**two-round RAG 81.4**，最接近的 **A-Mem 79.4**，MemOS **76.6**；LightMem 在 4B 上落后 **14.6 分**，OpenViking 落后 **40.4 分**。**11 个系统在三骨干上全部低于 two-round RAG。**
- **不是全歼**（必须同屏）：Memory-R2 在 PersonaMem-v2 上**赢 RAG 2.0**、PlugMem 在 MINT-Eval 上**赢 3.3** ⇒ 记忆确实在「需要抽象与偏好蒸馏」的题上挣钱。
- **成本侧更刺眼**：A-Mem 离线建库 **117 小时** vs RAG **0.11 小时**（**三个数量级**），**98.4K** 次 LLM 调用 vs **200** 次。⇒ *pay a thousand times the build cost, get a lower score*。
- **廉价修法（转引自二手页，一手未核）**：把原始历史与记忆库一起检索并联合重排（`src-aug`）——即**不要用记忆取代原始历史**。

**税的三个来源（本页最可复用的部分）**

| 来源 | 失效形态 | 证据 |
|---|---|---|
| **Faithfulness** | 原始语料里的事实，进了记忆单元就被丢 | OpenViking 对 **38%** 的事实**根本没有**记忆单元、另 **13%** 重大损失；对照 MAGMA **93.6%** 无损 ⇒ *loss is a design choice, not fate* |
| **Accessibility** | 证据活下来了，但**取不回**（碎片化 / 稀释 / 改写） | 第一轮取回的 query 数少于 RAG，证据被埋得更深 |
| **Robustness** | 记忆固定、只换 QA 骨干，记忆系统比原始 RAG **更抖** | 中间操作对模型依赖，把脆弱性焊进了存储 |

## 边界（不可合并）

- **vs [[LongTermMemory]]** — 那页问「跨会话的持久状态放在哪、怎么诚实读取」；本页是**它的对照组**。记忆系统是「对原始历史做处理」的那一支，RAG 是「不处理」的那一支。**没有本页，那页的收益无法定价。**
- **vs [[ContextEngineering]]** — 上下文工程管**这个窗口里放什么**（分层、及时检索、裁剪重注）；RAG 是它下面**一种具体的取用方式**。本页只负责把「不处理的取用」钉成基线。
- **vs [[Compaction]]** — 压缩作用于**窗口内已有内容**；RAG 作用于**窗口外取什么**。两者都会丢东西，但丢的位置不同 ⇒ **分栏**。
- **vs [[MemoryGovernance]]** — 治理问「谁有权改、改了怎么审计」；本页提供**评估它们收益的零点**。
- **vs [[Provenance]] / [[CitationLock]] / [[Abstention]]** — 那三页管「取回的东西可不可信」；本页管「取回这件事本身值不值」。⇒ **信任纪律与净值纪律是两个问题**。
- **vs [[AgentHarness]]** — 外壳决定**谁来编排检索**；本页是**被编排的那个动作的基线得分**。

## 开放项状态（精确到哪一半被结清）

`overview.md` 那条最老开放项写的是三件事：**向量库选型 · 分块策略 · 检索质量**。

- ✅ **检索质量**——有了基线分数（上表），且附带一个反向结论：**基准本身对检索友好，绝对分数不可横比**。
- ❌ **向量库选型 / 分块策略**——本页**没有**这两项的证据；`arXiv:2610.34073` 不测它们。
- ⇒ 因此本条开放项记为**「部分结清」**，不记为已关闭。诚实表述：**「值不值」有了答案，「怎么搭」仍然没有。**

## 证据分级（引用本页时必须一起走）

- `arXiv:2610.34073` 是**预印本，未见同行评议**；作者自陈将开源代码与结果（`github.com/hexuan21/MemoryTax`，MIT）。
- **上表全部数字转引自二手详解页**（`explainx.ai` / `aimodeling.com`），**一手 PDF 的 Table 1 未逐格核对** ⇒ 引用具体分数时应标注「二手」。
- 「基准天花板低」这一条是**作者自己的批评**，不是外部发现，但它同时削弱了**该论文自身的绝对分**——引用时不可只取一半。
- **不可读作「记忆无用」**：作者的落点是**换记账方式**（从单看分数换到看净值），不是删掉记忆层。

## See Also

- [[LongTermMemory]] — 对照组：跨会话持久状态本身
- [[MemoryGovernance]] — 治理对象；本页是其收益的零点
- [[ContextEngineering]] — 取用方式的上一层策略（并见其「常驻内容的半衰期」一节）
- [[Compaction]] — 窗口内的丢失 vs 窗口外的取用：两个不同的丢失位置
- [[Provenance]] · [[CitationLock]] · [[Abstention]] — 取回内容的可信度纪律（与本页的净值纪律分栏）
- [[AgentObservability]] — 判分那一侧；本页是其判分对象的基线
- [[Zep]] · [[MemGPT]] · [[AgentZeroMemory]] — 本库已收录的记忆系统，其收益应以本页为分母
