# 每日维护者 · 自动化执行记忆

> 只留高层摘要，不放正文。完整产出在 `.workbuddy/memory/concept-radar/YYYY-MM-DD.md`。

## 固定流程（已验证可跑通）

1. `cd tools/llm-wiki-agent && python tools/health.py` + `python tools/daily_lint.py`
   —— **七个维度 A–G 全绿即本期无维护项**；两个脚本都是零 LLM 调用，可放心每次跑。
2. 改完后**再跑一次同样的两个脚本**复核（log.md 追加后尤其要复核维度 G）。
3. `git add -A` + `git commit -F -`（heredoc）→ `python output/_tools/api_push.py`。
4. 推送后看 `git status -sb` 是否干净。

## 各次运行

| 日期 | 维护结果 | 雷达候选 | 推送 |
|---|---|---|---|
| 2026-10-30 | **零新增**：13 源 / 49 页 / 51 `.md`，与 10-29 持平；七维全绿；无 ingest ⇒ synthesis 未修订 | 3 条（10-30A/B/C），**只登记未落地** | 2 次推送，最终 `git status -sb` 干净 |

### 2026-10-30 详情

- **首次无人值守运行**。⇒ 关键裁定：**自动化运行默认「只登记、不落地」**；落地需要用户显式指令（对照 2026-10-29 的「按你的建议来」）。报告里必须写明本次档位。
- 雷达三条均为「本库已点名、缺仪器」型：内在/外在记忆评测（arXiv:2610.22209 FEB-30）· 上下文质量七项构造（arXiv:2607.14275）· 记忆依赖推理 Cascade/Absence/Deletion（arXiv:2605.12477 MEME）。
- 未执行项：`BACKLOG.md` 未登记 3 行 ⏸（主表 92 行 / 550 KB，属结构性改动，留待拍板）。

## 两个已踩的坑（下期直接沿用结论）

1. **`api_push.py` 自报的「内容完全一致」不可直接采信。**
   首次推送后它报 `False`，但独立查 `api.github.com` 显示远端 tree == 本地 tree，推送其实成功。
   根因：本地对齐步骤未生效时，它拿 `origin/main` ref 仍指向的**旧提交**当基准。
   ⇒ **判据 = 远端 tree == 本地 tree，且要比对新创建的那个远端 commit**；脚本那行只作参考。
   复核方式（不走 git 传输）：`urllib` 取 `https://api.github.com/repos/ohh0525/silent-madman/commits/main`，看 `sha` / `commit.tree.sha` / `files`。
2. **对齐降级是自愈的，不要手动干预。**
   第一次推送后 `git status -sb` 显示 `ahead 1`（本地 `origin/main` ref 停在旧提交）。**第二次推送时脚本自动抹平**，并打印「已把本地 main 对齐到远端」。
   ⇒ 遇到 `ahead N` **不要** fetch / rebase / reset / `git push`，再跑一次 `api_push.py` 即可。

## 环境事实

- `curl -o /tmp/...` 在本沙盒**写不出文件**（无报错但文件不存在）→ 查 GitHub 一律用 **python `urllib`**，不要用 curl。
- 无 token 也能读公开仓库的 `api.github.com`，无需鉴权。
