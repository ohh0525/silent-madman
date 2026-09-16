#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Stage 2 版式生成：Markdown -> 美化 HTML（doc-typeset 模板套用）。

用法:
  python3 build_html.py --md <final_draft.md> --out <formatted.html> \
      --tokens <compiled.json> --title "标题" --subtitle "副标题" \
      --eyebrow "分类" --meta "键=值;键=值"
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import markdown

ROOT_VARS = """
  :root {
    --layout-contentWidth: @contentWidth@;
    --typography-fontSize-h1: @fsH1@;
    --typography-fontSize-h2: @fsH2@;
    --typography-fontSize-h3: @fsH3@;
    --typography-fontSize-body: @fsBody@;
    --typography-fontSize-small: @fsSmall@;
    --typography-fontSize-title: @fsTitle@;
    --typography-fontFamily-heading: @ffHeading@;
    --typography-fontFamily-body: @ffBody@;
    --typography-fontFamily-mono: @ffMono@;
    --typography-lineHeight-body: @lhBody@;
    --typography-lineHeight-heading: @lhHeading@;
    --color-primary: @cPrimary@;
    --color-text: @cText@;
    --color-muted: @cMuted@;
    --color-border: @cBorder@;
    --color-bg: @cBg@;
    --color-highlight: @cHighlight@;
    --color-codeBg: @cCodeBg@;

    --page-content-width: var(--layout-contentWidth, 15.6cm);
    --fs-title: var(--typography-fontSize-title, 24pt);
    --fs-h1: var(--typography-fontSize-h1, 18pt);
    --fs-h2: var(--typography-fontSize-h2, 15pt);
    --fs-h3: var(--typography-fontSize-h3, 13pt);
    --fs-body: var(--typography-fontSize-body, 11pt);
    --fs-small: var(--typography-fontSize-small, 9pt);
    --ff-heading: var(--typography-fontFamily-heading, "PingFang SC", sans-serif);
    --ff-body: var(--typography-fontFamily-body, "PingFang SC", sans-serif);
    --ff-mono: var(--typography-fontFamily-mono, monospace);
    --ff-mono-alt: var(--typography-fontFamily-code, monospace);
    --lh-body: var(--typography-lineHeight-body, 1.6);
    --lh-heading: var(--typography-lineHeight-heading, 1.3);
    --fw-bold: var(--typography-fontWeight-heading, 600);
    --fw-normal: var(--typography-fontWeight-body, 400);
    --spacing-paragraph: var(--spacing-paragraphValue, 0.6em);
    --spacing-section: var(--spacing-sectionGap, 2em);
    --spacing-block: var(--spacing-blockValue, 1em);
    --margin-page: var(--layout-marginTop, 2.5cm);
  }
"""

CSS = """
  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: var(--ff-body);
    font-size: var(--fs-body);
    line-height: var(--lh-body);
    color: var(--color-text);
    background: var(--color-bg);
    max-width: var(--page-content-width);
    margin-left: auto;
    margin-right: auto;
    padding-top: var(--margin-page);
    padding-bottom: var(--margin-page);
  }

  h1, h2, h3, h4 {
    font-family: var(--ff-heading);
    line-height: var(--lh-heading);
    font-weight: var(--fw-bold);
    color: var(--color-text);
    margin-top: var(--spacing-section);
    margin-bottom: var(--spacing-paragraph);
  }
  h1 { font-size: var(--fs-h1); }
  h2 { font-size: var(--fs-h2); }
  h3 { font-size: var(--fs-h3); }
  h4 { font-size: var(--fs-body); }

  p { margin-bottom: var(--spacing-paragraph); }

  ul, ol { padding-left: var(--spacing-section); margin-bottom: var(--spacing-paragraph); }
  li { margin-bottom: var(--spacing-paragraph); line-height: var(--lh-body); }

  table {
    border-collapse: collapse;
    width: 100%;
    margin-bottom: var(--spacing-block);
    font-size: var(--fs-body);
  }
  th, td {
    padding: var(--spacing-paragraph);
    border: 1px solid var(--color-border);
    text-align: left;
    vertical-align: top;
    line-height: var(--lh-body);
  }
  th {
    font-family: var(--ff-heading);
    font-weight: var(--fw-bold);
    background: var(--color-codeBg);
  }

  pre {
    font-family: var(--ff-mono);
    font-size: var(--fs-small);
    line-height: var(--lh-heading);
    background: var(--color-codeBg);
    border: 1px solid var(--color-border);
    padding: var(--spacing-block);
    margin-bottom: var(--spacing-block);
    white-space: pre-wrap;
    word-wrap: break-word;
  }
  pre code { font-family: var(--ff-mono); background: transparent; padding: 0; border: none; }

  code {
    font-family: var(--ff-mono-alt);
    font-size: var(--fs-small);
    background: var(--color-codeBg);
  }

  blockquote {
    border-left: 3px solid var(--color-primary);
    background: var(--color-codeBg);
    padding: var(--spacing-block);
    margin-bottom: var(--spacing-block);
    color: var(--color-text);
    line-height: var(--lh-body);
  }
  blockquote p { margin-bottom: 0; }

  strong { font-weight: var(--fw-bold); color: var(--color-text); }
  em { color: var(--color-muted); }

  .doc-toc {
    margin-bottom: var(--spacing-section);
    padding: var(--spacing-block);
    background: var(--color-codeBg);
    border: 1px solid var(--color-border);
  }
  .toc-title {
    font-family: var(--ff-heading);
    font-size: var(--fs-h3);
    font-weight: var(--fw-bold);
    margin-bottom: var(--spacing-paragraph);
  }
  .toc-list, .toc-list ol, .toc-list ul {
    list-style: none;
    list-style-type: none;
    padding-left: var(--spacing-block);
  }
  .toc-list li { margin-bottom: var(--spacing-paragraph); line-height: var(--lh-heading); }
  .toc-list a { color: var(--color-text); text-decoration: none; }

  section[role="cover"] { text-align: center; }
  .cover-eyebrow {
    text-align: center;
    font-family: var(--ff-heading);
    font-size: var(--fs-small);
    color: var(--color-muted);
    margin-bottom: var(--spacing-section);
  }
  .cover-title {
    text-align: center;
    font-family: var(--ff-heading);
    font-size: var(--fs-title);
    font-weight: var(--fw-bold);
    color: var(--color-text);
    line-height: var(--lh-heading);
    margin-bottom: var(--spacing-block);
  }
  .cover-subtitle {
    text-align: center;
    font-size: var(--fs-h3);
    color: var(--color-muted);
    margin-bottom: var(--spacing-section);
  }
  .cover-info {
    margin-top: var(--spacing-section);
    text-align: left;
    font-size: var(--fs-body);
  }
  .cover-info td { border: none; padding: var(--spacing-paragraph); }
  .cover-info td:first-child {
    font-family: var(--ff-heading);
    font-weight: var(--fw-bold);
    width: 30%;
    color: var(--color-muted);
  }

  .doc-footer {
    margin-top: var(--spacing-section);
    color: var(--color-muted);
    font-size: var(--fs-small);
  }
"""

PAGE_CSS = """
  @page {
    @bottom-center { content: counter(page); }
  }
  @page cover {
    @bottom-center { content: none; }
  }
  section[role="cover"] { page: cover; }
"""


def slugify_headings(html: str) -> tuple[str, list[tuple[int, str, str]]]:
    """给正文标题加 id，并收集 (level, id, text) 用于目录。"""
    toc: list[tuple[int, str, str]] = []
    counter = {"n": 0}

    def repl(m: re.Match) -> str:
        level = int(m.group(1))
        text = m.group(2)
        plain = re.sub(r"<[^>]+>", "", text).strip()
        counter["n"] += 1
        hid = f"section-{counter['n']}"
        toc.append((level, hid, plain))
        return f'<h{level} id="{hid}">{text}</h{level}>'

    html = re.sub(r"<h([1-4])>(.*?)</h\1>", repl, html, flags=re.S)
    return html, toc


def shift_headings(html: str) -> str:
    """md 的 h2/h3/h4 下移为正文 h1/h2/h3（md 首个 h1 已移至封面）。"""
    html = re.sub(r"<h4>", "<h3>", html)
    html = re.sub(r"</h4>", "</h3>", html)
    html = re.sub(r"<h3>", "<h2>", html)
    html = re.sub(r"</h3>", "</h2>", html)
    html = re.sub(r"<h2>", "<h1>", html)
    html = re.sub(r"</h2>", "</h1>", html)
    return html


def build_toc(toc: list[tuple[int, str, str]]) -> str:
    if len([t for t in toc if t[0] == 2]) < 3:
        return ""
    items = []
    for level, hid, text in toc:
        if level > 3:
            continue
        cls = "toc-l1" if level == 2 else "toc-l2"
        items.append(f'<li class="{cls}"><a href="#{hid}">{text}</a></li>')
    return (
        '<nav class="doc-toc" aria-label="文档目录">'
        '<p class="toc-title">目录</p>'
        '<ol class="toc-list">' + "".join(items) + "</ol></nav>"
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--tokens", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--eyebrow", default="")
    ap.add_argument("--meta", default="")
    ap.add_argument("--footer", default="")
    args = ap.parse_args()

    md_text = Path(args.md).read_text(encoding="utf-8")

    # 首个 H1 提到封面
    m = re.search(r"^#\s+(.+)$", md_text, flags=re.M)
    if m:
        md_text = md_text[: m.start()] + md_text[m.end():]

    body_html = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "sane_lists", "attr_list"],
    )
    body_html, toc = slugify_headings(body_html)

    tok = json.loads(Path(args.tokens).read_text(encoding="utf-8"))
    cv = tok["css_variables"]
    def g(k: str, d: str) -> str:
        return cv.get(k, d)

    _vals = dict(
        contentWidth=g("--layout-maxContentWidth", "15.6cm"),
        fsTitle=g("--typography-fontSize-title", "24pt"),
        fsH1=g("--typography-fontSize-h1", "18pt"),
        fsH2=g("--typography-fontSize-h2", "15pt"),
        fsH3=g("--typography-fontSize-h3", "13pt"),
        fsBody=g("--typography-fontSize-body", "11pt"),
        fsSmall=g("--typography-fontSize-small", "9pt"),
        ffHeading=g("--typography-fontFamily-heading", '"PingFang SC", sans-serif'),
        ffBody=g("--typography-fontFamily-body", '"PingFang SC", sans-serif'),
        ffMono=g("--typography-fontFamily-code", "monospace"),
        lhBody=str(g("--typography-lineHeight-body", "1.6")),
        lhHeading=str(g("--typography-lineHeight-heading", "1.3")),
        cPrimary=g("--color-primary", "#2563EB"),
        cText=g("--color-text", "#111827"),
        cMuted=g("--color-textSecondary", "#6B7280"),
        cBorder=g("--color-border", "#E5E7EB"),
        cBg=g("--color-background", "#FFFFFF"),
        cHighlight=g("--color-highlight", "#FEF3C7"),
        cCodeBg=g("--color-codeBg", "#F9FAFB"),
    )
    root = ROOT_VARS
    for _k, _v in _vals.items():
        root = root.replace("@" + _k + "@", str(_v))

    meta_rows = ""
    if args.meta:
        for pair in args.meta.split(";"):
            if "=" in pair:
                k, v = pair.split("=", 1)
                meta_rows += f"<tr><td>{k.strip()}</td><td>{v.strip()}</td></tr>"
    meta_html = f'<table class="cover-info"><tbody>{meta_rows}</tbody></table>' if meta_rows else ""

    footer_html = (
        f'<p class="doc-footer">{args.footer}</p>' if args.footer else ""
    )

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="docx-page-size" content="A4">
<title>{args.title}</title>
<style>{root}{CSS}{PAGE_CSS}</style>
</head>
<body>
<section role="cover">
  <p class="cover-eyebrow">{args.eyebrow}</p>
  <h1 class="cover-title">{args.title}</h1>
  <p class="cover-subtitle">{args.subtitle}</p>
  {meta_html}
</section>
<section role="body" data-page-restart="1">
{build_toc(toc)}
{body_html}
{footer_html}
</section>
</body>
</html>
"""
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"OK -> {out}  ({len(html)} bytes, toc={len(toc)} headings)")


if __name__ == "__main__":
    main()
