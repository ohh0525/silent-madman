#!/usr/bin/env python3
# 每日 wiki lint —— 五维度 + raw/ 未摄取扫描
# 约定(沿用既有口径):
#  - index.md / log.md 无 frontmatter 属设计如此(CLAUDE.md 的 Index/Log 格式未定义),不计入维度 C
#  - overview.md 的 tags: [] 为「键在、值为空」,非缺字段
#  - [[Target|display]] 管道别名必须解析 Target,不能整串匹配
import re, os, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
RAW = ROOT / "raw"

md = sorted(WIKI.rglob("*.md"))
pages = [f for f in md]

def rel(f): return str(f.relative_to(WIKI)).replace("\\", "/")

# ---------- frontmatter ----------
def split_fm(text):
    if not text.startswith("---"):
        return None, text
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return None, text
    return m.group(1), m.group(2)

pages_fm = {}
for f in pages:
    raw_t = f.read_text(encoding="utf-8")
    fm, body = split_fm(raw_t)
    pages_fm[rel(f)] = (fm, body)

# ---------- 节点名 -> 存在性 ----------
# wikilink 目标按 CLAUDE.md 约定为 PageName(不含目录、不含扩展名)
names = {}
for r in pages_fm:
    stem = Path(r).stem
    names[stem] = r

LINK = re.compile(r"\[\[([^\]]+)\]\]")

def link_targets(body):
    """返回 [(raw, target, exists)] —— 处理管道别名"""
    out = []
    for raw in LINK.findall(body):
        tgt = raw.split("|")[0].strip()
        out.append((raw, tgt, tgt in names))
    return out

# ---------- 维度 A:悬空 wikilink ----------
print("=== A. 悬空 [[wikilink]] ===")
dangling = []
link_edges = {}  # target -> set(source page)
for r, (fm, body) in pages_fm.items():
    if r in ("index.md", "log.md"):
        continue
    for raw, tgt, ok in link_targets(body):
        if not ok:
            dangling.append((r, raw, tgt))
print(f"悬空链接: {len(dangling)}")
for r, raw, tgt in dangling[:40]:
    print(f"  ✗ {r} -> [[{raw}]]")
if not dangling:
    print("  ✅ 0 —— 全部解析")

# ---------- 维度 B:孤立页(0 入链)----------
print("\n=== B. 孤立页(0 inbound)===")
for r, (fm, body) in pages_fm.items():
    if r in ("index.md", "log.md"):
        continue
    for raw, tgt, ok in link_targets(body):
        if ok:
            src_u = r
            dst = names[tgt]
            if src_u != dst:  # 自链排除
                link_edges.setdefault(dst, set()).add(src_u)

structural = {"index.md", "log.md"}
orphans = []
for r in pages_fm:
    if r in structural or r == "overview.md":
        continue
    inbound = link_edges.get(r, set())
    inbound = {s for s in inbound if s not in structural and s != "overview.md"}
    if len(inbound) == 0:
        orphans.append(r)
print(f"孤立页: {len(orphans)}")
for o in orphans:
    print(f"  ⚠ {o}")
if not orphans:
    print("  ✅ 0")

# 最小入链
mind = sorted(((len({s for s in v if s not in structural and s != 'overview.md'}), k)
               for k, v in link_edges.items() if k not in structural and k != "overview.md"))
print("最小入链 Top5:", [(n, k) for n, k in mind[:5]] if mind else "n/a")

# ---------- 维度 C:frontmatter 完整性 ----------
print("\n=== C. frontmatter 完整性 ===")
REQUIRED = ["title", "type", "tags", "sources", "last_updated"]
c_issues = []
for r, (fm, body) in pages_fm.items():
    if r in structural:
        continue
    if fm is None:
        c_issues.append((r, "缺失整个 frontmatter"))
        continue
    keys = re.findall(r"^([a-zA-Z_][a-zA-Z0-9_]*):", fm, re.M)
    missing = [k for k in REQUIRED if k not in keys]
    if missing:
        c_issues.append((r, f"缺字段 {missing}"))
print(f"frontmatter 问题: {len(c_issues)}")
for r, msg in c_issues:
    print(f"  ✗ {r} — {msg}")
if not c_issues:
    print("  ✅ 0")
print("  注: index.md / log.md 按设计无 frontmatter,已排除; overview.md 的 tags: [] 计为通过")

# ---------- 维度 D:sources slug 存在性 ----------
print("\n=== D. frontmatter sources slug 有效性 ===")
source_slugs = {Path(r).stem for r in pages_fm if r.startswith("sources/")}
all_slugs = {Path(r).stem for r in pages_fm}
total_refs = 0
bad_refs = []
for r, (fm, body) in pages_fm.items():
    if fm is None or r in structural:
        continue
    m = re.search(r"^sources:\s*\[(.*?)\]", fm, re.S | re.M)
    if not m:
        continue
    inner = m.group(1).strip()
    if not inner:
        continue
    slugs = [s.strip().strip("'\"") for s in inner.split(",") if s.strip()]
    for s in slugs:
        total_refs += 1
        # sources 字段通常引用 source 页;也允许引用任意页名
        if s not in source_slugs and s not in all_slugs:
            bad_refs.append((r, s))
print(f"sources 引用总数: {total_refs}")
print(f"无效 slug: {len(bad_refs)}")
for r, s in bad_refs:
    print(f"  ✗ {r} -> {s}")
if not bad_refs:
    print(f"  ✅ 全部 {total_refs} 条解析")
print(f"  sources/ 页: {len(source_slugs)} 个")

# ---------- 维度 E:index.md <-> 磁盘 ----------
print("\n=== E. index.md <-> 磁盘 ===")
idx_text = (WIKI / "index.md").read_text(encoding="utf-8")
listed = set(re.findall(r"\]\(((?:sources|concepts|entities|syntheses)/[^)]+\.md)\)", idx_text))
listed.add("overview.md")
on_disk = {r for r in pages_fm if r != "index.md" and r != "log.md"}
only_disk = sorted(on_disk - listed)
only_index = sorted(listed - on_disk)
print(f"磁盘未收录进 index: {len(only_disk)}")
for x in only_disk:
    print(f"  ✗ {x}")
print(f"index 中指向不存在文件: {len(only_index)}")
for x in only_index:
    print(f"  ✗ {x}")
if not only_disk and not only_index:
    print("  ✅ 双向一致")

# ---------- raw/ 未摄取扫描 ----------
print("\n=== F. raw/ 未摄取 ===")
raw_files = sorted([p for p in RAW.rglob("*") if p.is_file() and p.name != ".gitkeep"])
declared = set()
for r, (fm, body) in pages_fm.items():
    if fm is None:
        continue
    for m in re.finditer(r"^source_file:\s*(.+)$", fm, re.M):
        declared.add(m.group(1).strip())
un_ingested = []
for p in raw_files:
    rp = str(p.relative_to(ROOT)).replace("\\", "/")
    hit = any(rp == d or rp.endswith(d) or d.endswith(rp) for d in declared)
    if not hit:
        un_ingested.append(rp)
print(f"raw/ 文件总数: {len(raw_files)}")
print(f"未摄取: {len(un_ingested)}")
for x in un_ingested:
    print(f"  ⚠ {x}")
if not un_ingested:
    print("  ✅ 0 —— raw/ 只读扫描,未做任何修改")

print("\n=== 汇总 ===")
print(f"内容页(含 overview): {len([r for r in pages_fm if r not in structural])}")
print(f"总 .md 文件: {len(pages)}")
