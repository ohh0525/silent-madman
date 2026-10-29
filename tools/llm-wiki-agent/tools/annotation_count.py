#!/usr/bin/env python3
"""固定范围的「草稿批注」计数器 —— 该计数的唯一口径真源。

为什么需要这个文件（2026-10-29 建立）
------------------------------------
「草稿批注有几处」这个量在 2026-10-26 → 10-27 → 10-29 之间被人工转述了**三次**，
三次数字互不相同（25 处/10 文件 → 44/15 → 「85/19」→ 86/19 vs 50/16）。

根因不是数错，而是**扫描范围从未被定义**：
    - 把 `wiki/log.md` 等**叙述文件里对批注的「转述」**也计入，
      数字会随「昨天写了多少条报告」而变 —— 这不是库的状态，是我自己的话。
    - 把 `overview.md` 顶部的说明段计入，数字会随「更正说明写了几行」而变。

所以本文件把两件事写死在代码里，**不得口头修改**：

    1. 范围 = `wiki/sources/` + `wiki/concepts/` + `wiki/entities/`
       （只算内容页；`index.md` / `log.md` / `overview.md` 一律排除）
    2. 口径 = 行首严格横幅 `> **Draft annotation, pending ingest.`

用法
----
    python tools/annotation_count.py                # 打印当前计数
    python tools/annotation_count.py --json         # 机器可读
    python tools/annotation_count.py --check        # 与基线比对，不一致则 exit 1
    python tools/annotation_count.py --update-baseline   # 有意改动内容后更新基线

基线文件：`tools/annotation_baseline.json`。`tools/daily_lint.py` 的维度 G 会调用
`--check`，使跨日复核自动化，不再依赖人工 grep。
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
BASELINE = Path(__file__).resolve().parent / "annotation_baseline.json"

# ---- 口径定义：改这两行等于改口径，必须在 wiki/log.md 留痕 ----
SCOPE_DIRS = ("sources", "concepts", "entities")
BANNER = "> **Draft annotation, pending ingest."


def scan():
    """按固定范围与固定口径扫描，返回 {count, files, per_file}。"""
    per_file = {}
    for d in SCOPE_DIRS:
        for f in sorted((WIKI / d).glob("*.md")):
            hits = 0
            for line in f.read_text(encoding="utf-8").splitlines():
                if line.lstrip().startswith(BANNER):
                    hits += 1
            if hits:
                per_file[f"{d}/{f.name}"] = hits
    return {
        "count": sum(per_file.values()),
        "files": len(per_file),
        "per_file": per_file,
        "scope": "wiki/{" + ",".join(SCOPE_DIRS) + "}",
        "rule": BANNER,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--check", action="store_true", help="与基线比对，不一致则 exit 1")
    ap.add_argument("--update-baseline", action="store_true")
    ap.add_argument("--verbose", action="store_true", help="打印逐文件明细")
    a = ap.parse_args()

    r = scan()

    if a.update_baseline:
        import datetime

        data = {
            "count": r["count"],
            "files": r["files"],
            "scope": r["scope"],
            "rule": r["rule"],
            "updated": datetime.date.today().isoformat(),
        }
        BASELINE.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"基线已更新：{r['count']} 处 / {r['files']} 个文件 -> {BASELINE.name}")
        return 0

    if a.check:
        if not BASELINE.exists():
            print("✗ 基线文件不存在，请先运行 --update-baseline")
            return 1
        base = json.loads(BASELINE.read_text(encoding="utf-8"))
        ok = base["count"] == r["count"] and base["files"] == r["files"]
        mark = "✅" if ok else "✗"
        print(
            f"{mark} 草稿批注：实测 {r['count']} 处 / {r['files']} 文件 "
            f"｜ 基线 {base['count']} 处 / {base['files']} 文件 "
            f"（基线更新于 {base.get('updated', '?')}）"
        )
        if not ok:
            print(f"   范围：{r['scope']}    口径：{r['rule']}")
            print("   若本次为**有意**新增批注，请运行：python tools/annotation_count.py --update-baseline")
        return 0 if ok else 1

    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0

    print(f"范围: {r['scope']}")
    print(f"口径: 行首 {r['rule']!r}")
    print(f"结果: {r['count']} 处 / {r['files']} 个文件")
    if a.verbose:
        for k, v in sorted(r["per_file"].items(), key=lambda kv: (-kv[1], kv[0])):
            print(f"  {v:>3}  {k}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
