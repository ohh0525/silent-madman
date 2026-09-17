#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Stage 2 (doc-typeset) 渲染器：把 Stage1 的 Markdown 转成符合 HTML→docx 硬约束的版式 HTML。

- 复用《Python 基础语法讲义》stage2 的 <head>/<style>（同一 design-token 产物 modern-minimal），
  保证两份文档视觉完全一致。
- 遵守 doc-typeset 规范：无裸值、表格含 thead/tbody、blockquote 带 border-left 故加 &nbsp;&nbsp;、
  不用 <dl>/<div grid>、不用装饰性短横线、封面每个块显式 text-align。
"""
import io
import os
import re
import html as H

ROOT = "D:/桌面/silent-madman"
RID = "7eb7eb3c-d82e-4dd9-b317-61813bdb8c45"
SRC = ROOT + "/output/" + RID + "/stage1/final_draft.md"
TPL = ROOT + "/output/96a168d7-c868-48f0-840a-6f60ab8eb26a/stage2/formatted-Python基础语法讲义.html"
OUT = ROOT + "/output/" + RID + "/stage2/formatted-报错怎么读（讲义补充章节）.html"

DOC_TITLE = "Python 基础语法讲义 · 补充章节：报错怎么读"


def inline(t):
    t = H.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    return t


def is_table_sep(cells):
    return all(re.fullmatch(r":?-{2,}:?", c.strip()) for c in cells) and cells


def split_row(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def render_body(md_lines):
    out = []
    toc = []
    sec = {"n": 0}
    i = 0
    n = len(md_lines)

    def next_id():
        sec["n"] += 1
        return "section-%d" % sec["n"]

    while i < n:
        raw = md_lines[i]
        s = raw.strip()

        if not s:
            i += 1
            continue

        # 分隔线：跳过（不用装饰性横线，避免 docx 里变成突兀满版线）
        if re.fullmatch(r"-{3,}", s):
            i += 1
            continue

        # 代码块
        if s.startswith("```"):
            lang = s[3:].strip()
            i += 1
            buf = []
            while i < n and not md_lines[i].strip().startswith("```"):
                buf.append(md_lines[i])
                i += 1
            i += 1
            cls = (' class="language-%s"' % lang) if lang else ""
            body = H.escape("\n".join(buf), quote=True)
            out.append("<pre><code%s>%s\n</code></pre>" % (cls, body))
            continue

        # 标题
        m = re.match(r"^(#{1,4})\s+(.*)$", s)
        if m:
            lvl = len(m.group(1))
            txt = m.group(2).strip()
            if lvl == 1:
                i += 1
                continue  # 文档主标题由封面承载
            sid = next_id()
            if lvl == 2:
                out.append('<h2 id="%s">%s</h2>' % (sid, inline(txt)))
                toc.append(("l1", sid, txt))
            elif lvl == 3:
                out.append('<h3 id="%s">%s</h3>' % (sid, inline(txt)))
                toc.append(("l2", sid, txt))
            else:
                out.append('<h4 id="%s">%s</h4>' % (sid, inline(txt)))
            i += 1
            continue

        # 引用块（border-left → 文字前必须加不折叠空格）
        if s.startswith(">"):
            buf = []
            while i < n and md_lines[i].strip().startswith(">"):
                buf.append(md_lines[i].strip()[1:].strip())
                i += 1
            paras, cur = [], []
            for b in buf:
                if b == "":
                    if cur:
                        paras.append("".join(cur))
                        cur = []
                else:
                    cur.append(b)
            if cur:
                paras.append("".join(cur))
            inner = "".join(
                "<p>&nbsp;&nbsp;%s</p>" % inline(p) for p in paras if p
            )
            out.append("<blockquote>%s</blockquote>" % inner)
            continue

        # 表格
        if s.startswith("|"):
            rows = []
            while i < n and md_lines[i].strip().startswith("|"):
                rows.append(split_row(md_lines[i]))
                i += 1
            head = rows[0]
            body_rows = rows[1:]
            if body_rows and is_table_sep(body_rows[0]):
                body_rows = body_rows[1:]
            th = "".join("<th>%s</th>" % inline(c) for c in head)
            tb = "".join(
                "<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c) for c in r)
                for r in body_rows
            )
            out.append(
                "<table><thead><tr>%s</tr></thead><tbody>%s</tbody></table>" % (th, tb)
            )
            continue

        # 有序列表
        if re.match(r"^\d+\.\s+", s):
            items = []
            while i < n and re.match(r"^\d+\.\s+", md_lines[i].strip()):
                items.append(re.sub(r"^\d+\.\s+", "", md_lines[i].strip()))
                i += 1
            out.append(
                "<ol>%s</ol>" % "".join("<li>%s</li>" % inline(x) for x in items)
            )
            continue

        # 无序列表
        if re.match(r"^-\s+", s):
            items = []
            while i < n and re.match(r"^-\s+", md_lines[i].strip()):
                items.append(re.sub(r"^-\s+", "", md_lines[i].strip()))
                i += 1
            out.append(
                "<ul>%s</ul>" % "".join("<li>%s</li>" % inline(x) for x in items)
            )
            continue

        # 段落
        buf = []
        while i < n:
            cur = md_lines[i].strip()
            if not cur:
                break
            if cur.startswith(("#", ">", "|", "```")) or re.match(r"^(\d+\.|[-*])\s+", cur):
                break
            if re.fullmatch(r"-{3,}", cur):
                break
            buf.append(cur)
            i += 1
        if buf:
            out.append("<p>%s</p>" % inline("".join(buf)))

    return out, toc


def main():
    tpl = io.open(TPL, encoding="utf-8").read().split("\n")
    head = "\n".join(tpl[:205])  # 到 </head> 为止（含 </head>）
    head = head.replace(
        "<title>Python 基础语法讲义（第 1–4 课）</title>",
        "<title>%s</title>" % DOC_TITLE,
    )
    assert DOC_TITLE in head, "title 替换失败"

    src = io.open(SRC, encoding="utf-8").read()
    body, toc = render_body(src.split("\n"))

    toc_html = "".join(
        '<li class="toc-%s"><a href="#%s">%s</a></li>' % (lvl, sid, inline(txt))
        for lvl, sid, txt in toc
    )

    cover = """<section role="cover">
  <p class="cover-eyebrow">课堂讲义 · 补充章节</p>
  <h1 class="cover-title">%s</h1>
  <p class="cover-subtitle">Traceback 逐行拆解 · 五类高频错误 · 五步排查法</p>
  <table class="cover-info"><thead><tr><th>项目</th><th>内容</th></tr></thead><tbody><tr><td>所属讲义</td><td>Python 基础语法讲义（第 1–4 课）</td></tr><tr><td>对应章节</td><td>§1.1 环境搭建与第一个程序 · §1.2 变量与数据类型 · 衔接 §3.6 异常处理</td></tr><tr><td>建议课时</td><td>1 个半场（45 分钟）</td></tr><tr><td>目标产出</td><td>看到报错能在 10 秒内定位出错行</td></tr></tbody></table>
</section>
<section role="body" data-page-restart="1">
<nav class="doc-toc" aria-label="文档目录"><p class="toc-title">目录</p><ol class="toc-list">%s</ol></nav>
%s
</section>
</body>
</html>
""" % (DOC_TITLE, toc_html, "\n".join(body))

    io.open(OUT, "w", encoding="utf-8").write(head + "\n<body>\n" + cover)
    print("written:", OUT)
    print("  body blocks: %d   toc entries: %d" % (len(body), len(toc)))


if __name__ == "__main__":
    main()
