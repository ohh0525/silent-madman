---
name: concept-group-guide
description: Generate a coherent SET of learning materials for a group of RELATED concepts, building on the single-concept guide format. Use when the user supplies two or more related concepts and wants one coherent set of materials rather than one-off pages — e.g. "把这几个概念做成一套材料", "生成一组相关概念的学习材料", "这几个概念一起做", "概念组", "concept group", "concept set", "batch learning materials". The key value is the RELATIONSHIPS between concepts: this skill first produces a concept-group skeleton (concept list, scope boundaries, prerequisite order, shared glossary) for the user to confirm, then generates each 7-section guide, then builds group-level artifacts and refreshes the knowledge graph. Do NOT use for a single concept (use concept-learning-skill) or for dictionary-style one-line definitions.
agent_created: true
---

# Concept Group Guide

## Overview

在单概念 guide 格式（见 `concept-learning-skill` 的 7 段结构）之上，生成**一组相关概念**的学习材料。

与"逐个生成"的本质区别只有一句话：**难点不在生成 N 份，而在 N 份之间的关系**。逐个独立生成几乎必然出现四种病：边界互相重叠、术语各写各的、没有先修顺序、彼此不引用。本 Skill 的增量全部用来治这四种病。

工作方式：**骨架先行 + 人工检查点**。先把关系（清单 / 边界 / 顺序 / 术语）定下来并经用户确认，再逐份生成，最后整合出组级产物并回流更新仓库图谱与知识库。

## When to Use

- 用户一次给出 **≥2 个相关概念**，要求做成一套材料
- 触发语：「把这几个概念做成一套材料」「生成一组学习材料」「这几个概念一起做」「概念组」「一组相关概念」
- 用户要求批量生成学习材料，且这些概念**同属一个知识网 / 一门课 / 一个主题**

**Do NOT use：**

- 单个概念 → 用 `concept-learning-skill`
- 词典式一句话定义、任务执行类（代码 / 文档 / 表格）
- 概念数 ≥ 8 时：先提醒用户可考虑并行编排方案（本项目暂未实现），并建议拆成多个组

## Inputs

| 字段 | 必填 | 默认 | 说明 |
|---|---|---|---|
| `concepts` | ✅ | — | 用户显式给出的概念清单（**本 Skill 只接受显式清单**，不自动扩展） |
| `group_name` |  | 由骨架阶段提议 | 组名，用于输出目录与索引页标题 |
| `output_root` |  | `learning-materials/` | 单份 HTML 的输出根目录；课程类概念可改为如 `Python基础语法课程/learning-materials/` |
| `audience_level` |  | `intermediate` | beginner / intermediate / expert |
| `context` |  | — | 为什么学（考试 / 工作 / 技术选型 / 好奇） |
| `depth` |  | `balanced` | 偏机制 / 偏应用 / 平衡 |
| `language` |  | 跟随提问语言 | 输出语言 |

## Workflow

### Phase 1 — 概念组骨架（**产出后必须停下等确认**）

产出 `concept-group/<group-slug>/00-骨架.md`，必须包含以下 6 项，一项都不能少：

1. **组定位** —— 这一组在解决什么问题（一句话）+ 目标读者 + 一组学完之后的收益
2. **概念清单表** —— 每行：概念名 | 一句话定义 | 在本组中的角色 | 先修（依赖本组哪些概念，可为空）
3. **边界声明（最关键）** —— 每个概念分别列出：
   - `in-scope`：本概念负责讲透什么
   - `out-of-scope`：本概念**不讲**什么，且**必须点名"归到哪个概念"**
   - 例：「变量与基本类型」out-of-scope：`TypeError` 的排查方法 → 归「报错怎么读」
4. **先修顺序** —— 对概念清单做拓扑排序，给出一条学习路径（序号 + 理由一句话）
5. **共享术语表** —— 本组内术语的统一措辞（中英文对照），防止各份材料自造词
6. **冲突检查** —— 显式列出"两两之间可能重叠的点"及归属裁决结论

骨架产出后**停下**，把骨架呈给用户审阅。**用户确认（或改完再确认）之后才进 Phase 2。**
若用户表示跳过确认直接生成 → 允许，但必须在骨架文件顶部标注 `> ⚠️ 未确认骨架，以下为模型假设`，并在最终回复里提醒。

### Phase 2 — 逐份生成

对 `concepts` 里每个概念，按 `concept-learning-skill` 的 7 段结构生成（一句话定义 / 个人解释 / 核心机制 / 应用场景 / 边界辨析 / 来源链接 / 一句话回顾），并追加以下**组内强制项**：

- **第 5 段边界辨析必须点名组内相邻概念**，格式如：「与 X 的分工：本概念负责 …，X 负责 …，详见 X 篇」。每份至少点名 1 个，无邻居的孤立概念要显式说明"本组内无直接相邻概念"。
- **严格服从骨架**：边界声明与术语表以 Phase 1 为准。生成中发现骨架有误（如边界冲突、顺序反了）→ **停下来回报**，不擅自扩写或改边界。
- **来源要求**沿用单概念 Skill 的领域最低来源数（通用 / 技术 / 法律医学三档），不得编造 URL，未核实断言标 `[unverified]`。
- 产出到 `<output_root>/<concept>.html`。

**HTML 复用规则**：直接复用 `learning-materials/` 现有 HTML 的 `<style>` 结构（同一套 CSS 变量与版式），**只替换 `--accent` 与 `--accent-soft` 两个主题色变量**。不要另起一套设计 —— 一组材料的价值之一就是视觉一致。

细节见 `references/html-conventions.md`。

### Phase 3 — 组级产物

1. **组索引页** `concept-group/<group-slug>/index.html`
   - 组定位 + 学习路径图（Mermaid，展示先修关系）+ 每份材料的卡片入口（标题 + 一句话定义 + 相对链接）
   - 视觉沿用同一套 CSS 变量
2. **交叉链接补全** —— 逐份检查 HTML 里对邻居的引用，确保相对路径真实可达（生成后必须实测，不能只写不验）
3. **关系段落** —— 按「领域边界」二选一（这是最容易犯错的一步）：
   - **同领域**：在既有关系图谱（如 `concept-relationship.md`）追加本组的关系段落（Mermaid 流程图 + 一句话定位），格式对齐该文件既有约定。
   - **跨领域**：**不要混入**既有图谱。改为在组目录下新建 `concept-group/<group-slug>/关系图.md`（结构对齐既有图谱：一句话定位 / 关系总览 Mermaid / 边界矩阵 / 学习路径 / 一句话总结），并在既有图谱顶部加**一行**「相关图谱（另一领域）」指引。判断依据：既有图谱的标题与前言已经声明了它的领域，本组若不属于该领域即为跨领域。

### Phase 4 — 回流图谱与知识库

1. **关系图**：仅当本组**属于该图谱声明的领域**时才重建 —— `python tools/build_graph.py --no-infer`（`networkx` 在场时 Louvain 社区检测自动启用；重建后确认节点数 ≥ 生成前）。**跨领域时跳过重建**：输入没有变化，重建只会产生无意义 diff 与 commit churn。
2. **登记进 LLM Wiki**：**先判断领域是否匹配**。Wiki 的收录范围由 `wiki/index.md` 的现有条目体现。若本组不属于该范围的领域（例：把 Python 教学概念放进一个 sources 全是 AI / LLM 的 Wiki）→ **不登记**，只在当天 daily log 写明「因领域不匹配未登记」。匹配时才追加索引条目；需要新建 concept 页则按 `tools/llm-wiki-agent/CLAUDE.md` 的 Ingest Workflow 执行。
3. **不修改 `raw/` 任何文件**
4. **提交并推送**：
   ```
   git add <本组产物> <图谱与 wiki 变更>
   git commit -m "feat(concept-group): <组名> —— N 份学习材料 + 图谱回流"
   python output/_tools/api_push.py
   ```

## Self-Check

交付前逐项过一遍，任何一项不过就修完再交：

1. 骨架文件存在，且 6 项内容齐全（组定位 / 清单表 / 边界声明 / 先修顺序 / 术语表 / 冲突检查）
2. 每个概念都有 in-scope 与 out-of-scope，且每条 out-of-scope 都点名了归属概念
3. 两两重叠点已裁决；**同一内容没有在两份材料里被完整讲两遍**
4. 每份 HTML 的第 5 段至少点名 1 个组内相邻概念（或显式说明无邻居）
5. 术语表里的词在各份材料中措辞一致（抽查 3 个词）
6. 组索引页里所有链接真实可达（相对路径已实测）
7. 每份材料的来源数达标，无编造 URL，未核实断言已标 `[unverified]`
8. 图谱：**同领域**则重建成功且节点数 ≥ 生成前；**跨领域**则既未污染既有图谱（已独立成篇 + 在既有图谱留一行指引），也未误登记进领域不匹配的 Wiki
9. 组内每份材料都能回答："它和我隔壁那份的边界在哪？"

## 硬约束（本仓库约定）

- **人工核查承诺**：README 有「所有入库资料经本人逐条核查」的承诺。模型可以生成产物，但**不得声称"已验证"**；核查由用户本人完成。
- **不修改 `raw/` 任何文件**（LLM Wiki 的不可变源材料）。
- **推送全自动**：commit 后用 `python output/_tools/api_push.py`。不要用 `git push`（本机 git 协议被封）。不要读取 / 打印 token 明文。
- 不在骨架未经确认时假装已确认。
- 中文、结构化输出（编号、表格、清单、分步）。

## Resources

- `references/html-conventions.md` —— HTML 结构复用规范与主题色分配
- `references/skeleton-template.md` —— 骨架文件模板（直接套用）

本 Skill 不含脚本；图谱重建与推送复用仓库既有脚本。

上游依赖：单概念 7 段结构定义在 `.workbuddy/skills/concept-learning-skill/SKILL.md`，执行 Phase 2 前应先读它。
