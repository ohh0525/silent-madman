# silent-madman

> 个人概念学习仓库：用一个通用 Skill 把任意概念生成结构化学习资料，用 Mermaid 图谱打通概念之间的关联。

---

## 仓库用途

本仓库沉淀了我用 WorkBuddy 学习陌生概念的全套产出，目的是：

- **可复用**：用一个 Skill 接住「任何新概念」，不必每次从零设计。
- **可关联**：用图谱把零散概念串成知识网。
- **可核查**：所有产出都附原始来源，并经过我**人工核查**后入库。

## ⏸ 人工核查承诺

> 本仓库内**所有资料都经过我个人的人工核查**：
>
> - 来源链接真实可达、引用准确；
> - 个人解释去掉了废话，没有未定义的术语；
> - 边界辨析区分了「容易混淆的邻居概念」；
> - 自检清单（结构、来源、长度、URL 真实性等 10 项）全部通过；
> - 不在未标 `[unverified]` 的情况下使用通用知识替代引用。
>
> 任何模型自动生成的内容，都会被我**逐条对照**原始资料后再标记为「通过」。

---

## 目录结构

```
silent-madman/
├── README.md                       # 你正在读的入口
├── concept-relationship.md         # 概念关联图谱 (Mermaid)
├── learning-materials/             # 单概念学习资料
│   ├── agent.html                  # Agent 智能体
│   ├── llm-context.html            # 大模型上下文窗口
│   └── skill.html                  # Skill 技能
└── .workbuddy/
    └── skills/
        └── concept-learning-skill/ # 本仓库专用的 Skill (project 级)
            └── SKILL.md
```

此外，WorkBuddy 在 user 级还存了一份同样的 Skill：

```
C:\Users\Lenovo\.workbuddy\skills\concept-explainer\SKILL.md
```

两份内容同步，**优先使用本仓库内的版本**（项目级）；user 级那份用来跨项目兜底。

---

## Skill 存放路径

| 级别 | 路径 | 作用域 |
|---|---|---|
| **Project 级**（推荐） | `D:\桌面\silent-madman\.workbuddy\skills\concept-learning-skill\SKILL.md` | 仅本仓库 |
| **User 级** | `C:\Users\Lenovo\.workbuddy\skills\concept-explainer\SKILL.md` | 所有项目 |

> 命名差异说明：项目级用 kebab-case (`concept-learning-skill`)，user 级用合法目录名 (`concept-explainer`)。两者内容已通过官方校验脚本 `quick_validate.py`，前端按 description 触发。

---

## 调用方法

### 方式 1：在本仓库对话中直接说

只要 WorkBuddy 在本工作目录被调用，下面这些说法都会自动触发 Skill：

- 「用 concept-learning-skill 帮我深入理解 [概念]」
- 「讲解 [概念]，给我生成学习资料」
- 「学习 [概念]，输出 HTML」
- 「用通俗的话讲讲 [概念]」

### 方式 2：手动传入参数

把 Skill 当作输入处理器，向我提供：

| 字段 | 必填 | 默认值 | 说明 |
|---|---|---|---|
| `concept` | ✅ | — | 要学的概念名（中英文都行） |
| `audience_level` |  | intermediate | beginner / intermediate / expert |
| `context` |  | — | 为什么学（考试/工作/技术选型/好奇） |
| `depth` |  | balanced | 偏机制 / 偏应用 / 平衡 |
| `language` |  | 跟随提问语言 | 输出语言 |

### 方式 3：跨项目调用

在任意目录调用 WorkBuddy，它会自动使用 user 级的 `concept-explainer`。如果需要强调用项目级版本，可以说：「用项目内的 Skill 处理 [概念]」。

---

## 输出位置约定

- **单概念学习资料** → `<repo>/learning-materials/<concept-name>.html`
- **概念关联图谱** → `<repo>/concept-relationship.md`
- **单概念 Markdown 版本** → 默认内联在对话中；若要落盘，正文可在 HTML `<details>` 块内复制，或告诉我「也存一份 md」。

---

## 已生成清单

| 文件 | 主题 | 类型 | 主题色 |
|---|---|---|---|
| `learning-materials/agent.html` | AI Agent | 单概念 | 橙 |
| `learning-materials/llm-context.html` | 大模型上下文窗口 | 单概念 | 蓝 |
| `learning-materials/skill.html` | Skill 技能 | 单概念 | 紫 |
| `concept-relationship.md` | 三者关联 | 图谱 | — |

> 想新增一个主题，直接告诉我概念名即可，本 Skill 会沿用同一份样式与结构，确保后续 HTML 之间排版一致。

---

## 维护规范（自我约束）

每生成一份新资料，对照以下清单逐项过一遍：

1. Skill 自检 10 条全部通过（结构、可读性、来源、长度、URL）
2. 来源已通过 WebSearch 真实返回，不抄训练数据当引用
3. Mermaid 图谱节点/连线与文字说明一一对应
4. 个人解释去除营销话术，留下「能复述给朋友的版本」
5. 在 README 已生成清单末尾追加一行

---

**最后更新**：2026-09-05 · 由本人逐条人工核查后入库。
