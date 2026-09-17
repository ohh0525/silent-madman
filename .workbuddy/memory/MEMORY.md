# MEMORY.md — silent-madman 长期约定

> 跨会话复用的项目级事实与约定。日常流水记在 `YYYY-MM-DD.md`,这里只沉淀**长期有效**的条目。

## 仓库约定

- **只 commit,不 push**。除非本人明确要求,任何会话都不得 `git push`、不得处理 token/PAT。
- **人工核查承诺**:`learning-materials/` 下的资料必须逐条对照原始来源后才能入库,未经核查不得由模型直接写入。
- `.gitignore` 排除 `*_draft.md` / `*.draft.md` / `*.scratch.md` → 流水线中间稿(stage1 的 `final_draft.md`)**不入库**,属正常现象,不要强行 `-f` 添加。
- 产出目录约定:`learning-materials/<concept>.html`(单概念)、`concept-relationship.md`(图谱);教学资料放 `Python基础语法课程/`。
- 本仓库有两份同名 Skill:项目级 `.workbuddy/skills/concept-learning-skill/`(优先)与 user 级 `~/.workbuddy/skills/concept-explainer/`,内容同步。

## 文档流水线(tencent-docx v5.5.3)

- 链路:`tdoc-orchestrator` → Stage1 `doc-writer`(落到 `output/<request_id>/stage1/final_draft.md`)→ Stage2 `doc-typeset`(`stage2/formatted-*.html` + `design_tokens.json`)→ `html-review` 质量门禁(≥80 且全维度通过)→ Stage3 `doc-converter` / `html-to-docx`(产 `.docx`)。
- Stage2 渲染脚本放在 `output/_tools/`,**复用主讲义的 `<head>`/`<style>`** 以保证全套讲义视觉一致。
- html-review 硬约束(踩过的坑):封面 `<table>` 必须有 `<thead>`;`<h2>` 后不能直接跟 `<h3>`,必须有导语 `<p>`;blockquote 首行加 `&nbsp;&nbsp;`;顶层用 `<section role="cover">` + `<section role="body">`;**改同一文件的多处编辑要串行执行**(并行 Edit 可能相互覆盖)。
- 质量门禁允许**一次**定向修正,修正后直接输出(不复检、不循环)。

## html-to-docx 环境(Windows + Git Bash 专属坑)

官方 `setup-html-to-docx.sh` 在本机 **跑不通**,需手工建环境。两个根因:
1. Windows venv 解释器在 `Scripts/python.exe`,脚本却检查 `bin/python` → 判定永不通过;
2. 依赖校验写成 `import htmldocx`,而包 `html-for-docx` 的真实 import 名是 **`html4docx`**。

**Git Bash 路径坑(关键)**:传给 uv 的路径必须用 `C:/Users/...` 正斜杠 Windows 形式;写成 `/c/Users/...` 会被解析成 `D:\c\Users\...`(按当前盘符),包会装到错误位置。

可复用手工流程:
```bash
uv venv --clear --python 3.12 C:/Users/Lenovo/.venv-html-to-docx
uv pip install --python C:/Users/Lenovo/.venv-html-to-docx/Scripts/python.exe \
  --only-binary=:all: -r <plugin>/skills/html-to-docx/scripts/requirements.txt
# cwd 设为 <plugin>/skills/html-to-docx/scripts
C:/Users/Lenovo/.venv-html-to-docx/Scripts/python.exe -m html_to_docx convert in.html -o out.docx
```

## 教学资料约定

- `Python基础语法课程/` 已有:主讲义、练习题、教学方案三份 docx + 补充章节《报错怎么读》。
- 配套可运行 Notebook 在 `Python基础语法课程/notebooks/`,生成器 `output/_tools/make_lesson_notebooks.py`(**本机未装 `nbformat`**,直接构造 nbformat 4.5 JSON)。代码格必须**实跑核对输出**再交付。
- 已知讲义笔误:`"张三".replace("张","李")` 输出是 **"李三"**(讲义旧版误写"李四"),Notebook 已更正。
