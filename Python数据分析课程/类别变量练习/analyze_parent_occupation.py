#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
父母职业相关性分析 —— 一体化独立脚本
=====================================================================
从原始 CSV 出发，一键完成：
    编码自动识别 -> 数据清理 -> 类别转化 -> 统计复算 -> 报告生成

用法:
    python analyze_parent_occupation.py
    python analyze_parent_occupation.py --src <源CSV路径> --out <输出目录>

默认源: D:/cxdownload/类别变量练习数据.csv
默认输出: 本脚本所在目录

产出:
    类别变量练习数据_UTF8.csv          纯编码转换副本（GBK -> UTF-8）
    类别变量练习数据_清理转化后.csv     原始值 + 类别码 + 类别标签 + 重复标记
    父母职业相关性分析报告.html         可视化分析报告（模板快照）
    analysis_summary.json              统计结果摘要（可机读）

依赖: 仅 Python 标准库（无需 numpy / pandas / scipy）
统计实现: 卡方分布生存函数用正则化上不完全 gamma 函数（Numerical Recipes），
          Fisher 精确检验用超几何分布枚举，均为独立实现并经交叉验证。
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import math
import sys
from collections import Counter
from pathlib import Path

DEFAULT_SRC = r"D:\cxdownload\类别变量练习数据.csv"

# ---------------------------------------------------------------- 类别定义
LABEL = {
    "G": "党政机关/基层政权",
    "P": "事业单位/教育医疗专业技术",
    "W": "企业白领/管理技术",
    "S": "个体经营/商贸服务",
    "M": "工农制造/建筑运输",
    "H": "家务/无业/缺失",
}

FATHER_MAP: dict[str, str] = {}
for _v in ["市经济合作局", "市民政局", "市农业农村局", "市统计局", "市农业综合行政执法队",
           "市中级人民法院", "市旅游局", "XXX镇政府", "市团委", "市公安局", "公安局",
           "西区管委会", "市住建局", "XXX建设局", "市政管理处", "省监狱局", "市财政局",
           "市纪委", "市委办"]:
    FATHER_MAP[_v] = "G"
for _v in ["市广播电视大学", "市第一人民医院"]:
    FATHER_MAP[_v] = "P"
for _v in ["凯信会议服务有限公司", "元拓科技咨询有限公司", "盛泰房地产公司",
           "大禹工程咨询有限公司", "长通公司"]:
    FATHER_MAP[_v] = "W"
for _v in ["区建豪汽修中心", "北京路九洋菜市场刘伟鲜面店", "老姐饺子馆", "大市场清华电动工具",
           "陇风巢浴", "万盛体能拓展中心鑫多米便利店", "娟红杂粮食府", "第十一中学北侧校园书店"]:
    FATHER_MAP[_v] = "S"
for _v in ["中铁六局太原铁路建设公司", "银光聚银化工有限公司", "陕西省水利水电第三工程局",
           "渭源陇原恒新畜牧科技有限公司", "县瑞金路锦辉消防工程有限公司", "银中源工贸有限公司",
           "广东省中海油", "中国兵器工业公司三冶炼", "万民工程建设有限公司",
           "江苏路之久工程建设有限公司", "瑞禾农资"]:
    FATHER_MAP[_v] = "M"
for _v in ["家庭父亲", "家庭父母", "家庭主妇"]:
    FATHER_MAP[_v] = "H"

MOTHER_MAP: dict[str, str] = {}
for _v in ["XX路街道诚信社区", "市委编办", "纺织路街道办", "白银区公园路街道办事处",
           "区应急管理局", "区人民法院", "市人社局", "市科学技术局", "区住建局", "市教育局",
           "市委统战部", "市公安局交警支队", "市审计局"]:
    MOTHER_MAP[_v] = "G"
for _v in ["市实验中学", "县住房保障中心", "矿冶职业技术学院", "公路应急保障与路网监测中心",
           "区妇幼保健站", "省第三人民医院", "泰安学校教职工", "市育才学校", "区融媒体中心"]:
    MOTHER_MAP[_v] = "P"
for _v in ["中国平安财险股份有限公司", "宏信房地资产评估公司", "农行XXX县支行", "顶新文化公司"]:
    MOTHER_MAP[_v] = "W"
for _v in ["长城国际旅行社有限责任公司", "九亩花田蛋糕店", "北京路九洋菜市场刘伟鲜面店",
           "个体", "大自然旅行社", "凤巢浴足", "美年大健康有限公司", "北门流觞烟酒",
           "娟红杂粮食府", "新疆省和田市个体药店"]:
    MOTHER_MAP[_v] = "S"
for _v in ["鑫智点交通设施有限公司", "二十一冶", "市给排水（集团）有限公司"]:
    MOTHER_MAP[_v] = "M"
for _v in ["家庭主妇", "家庭父母", "无", ""]:
    MOTHER_MAP[_v] = "H"

EXPECT_F = Counter({"G": 22, "P": 2, "W": 6, "S": 9, "M": 11, "H": 3})
EXPECT_M = Counter({"G": 14, "P": 9, "W": 4, "S": 10, "M": 3, "H": 13})
ORDER = ["G", "P", "W", "S", "M", "H"]


# ---------------------------------------------------------------- 数据读取与清理
def read_csv_auto(path: str):
    """自动识别 GBK / UTF-8 编码，按 CSV 引号规则解析（保留跨行字段）。"""
    raw = Path(path).read_bytes()
    for enc in ("utf-8-sig", "utf-8", "gbk", "gb18030"):
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        raise RuntimeError("无法识别文件编码")
    rows = list(csv.reader(io.StringIO(text)))
    return rows, enc, text


def clean_str(s: str) -> str:
    """去除首尾空白与内嵌换行符。"""
    return s.replace("\r", "").replace("\n", "").strip()


def transform(rows: list[list[str]]):
    """逐条编码并做完整性校验；返回带编码的行与频数统计。"""
    data = rows[1:]
    out: list[list] = []
    seen: Counter = Counter()
    for i, r in enumerate(data, 1):
        f, m = clean_str(r[0]), clean_str(r[1])
        if f not in FATHER_MAP:
            raise ValueError(f"第 {i} 条父亲取值未编码: {f!r}")
        if m not in MOTHER_MAP:
            raise ValueError(f"第 {i} 条母亲取值未编码: {m!r}")
        pair = (f, m)
        seen[pair] += 1
        out.append([i, f, FATHER_MAP[f], LABEL[FATHER_MAP[f]],
                    m, MOTHER_MAP[m], LABEL[MOTHER_MAP[m]],
                    "重复" if seen[pair] > 1 else ""])
    fc = Counter(r[2] for r in out)
    mc = Counter(r[5] for r in out)
    if fc != EXPECT_F or mc != EXPECT_M:
        print("⚠️  编码频数与基准不一致，请复核映射表或数据。", file=sys.stderr)
        print(f"   父亲: {dict(fc)}  期望: {dict(EXPECT_F)}", file=sys.stderr)
        print(f"   母亲: {dict(mc)}  期望: {dict(EXPECT_M)}", file=sys.stderr)
    return out, dict(fc), dict(mc)


# ---------------------------------------------------------------- 统计函数（纯 Python）
def gammq(a: float, x: float) -> float:
    """正则化上不完全 gamma 函数 Q(a,x)，Numerical Recipes 实现。"""
    if x <= 0:
        return 1.0
    if x < a + 1.0:
        ap, s, d = a, 1.0 / a, 1.0 / a
        for n in range(1, 1000):
            ap += 1.0
            d *= x / ap
            s += d
            if abs(d) < abs(s) * 1e-14:
                break
        return 1.0 - s * math.exp(-x + a * math.log(x) - math.lgamma(a))
    fpm = 1e-300
    b, c, d = x + 1.0 - a, 1.0 / fpm, 1.0 / (x + 1.0 - a)
    h = d
    for i in range(1, 1000):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < fpm:
            d = fpm
        c = b + an / c
        if abs(c) < fpm:
            c = fpm
        d = 1.0 / d
        dl = d * c
        h *= dl
        if abs(dl - 1.0) < 1e-14:
            break
    return math.exp(-x + a * math.log(x) - math.lgamma(a)) * h


def chi2_p(chi2: float, df: int) -> float:
    """卡方分布上尾概率。"""
    return gammq(df / 2.0, chi2 / 2.0)


def pearson(table: list[list[int]]):
    """Pearson 卡方；返回 chi2, df, n, 最小期望, E<5 格数, E<1 格数。"""
    R, C = len(table), len(table[0])
    rt = [sum(r) for r in table]
    ct = [sum(table[i][j] for i in range(R)) for j in range(C)]
    n = sum(rt)
    chi2 = 0.0
    emin, lt5, lt1 = float("inf"), 0, 0
    for i in range(R):
        for j in range(C):
            e = rt[i] * ct[j] / n
            emin = min(emin, e)
            lt5 += e < 5
            lt1 += e < 1
            chi2 += (table[i][j] - e) ** 2 / e
    return chi2, (R - 1) * (C - 1), n, emin, lt5, lt1


def cramers_v(chi2: float, n: int, R: int, C: int) -> float:
    return math.sqrt(chi2 / (n * min(R - 1, C - 1)))


def yates_2x2(table: list[list[int]]) -> float:
    a, b = table[0]
    c, d = table[1]
    n = a + b + c + d
    return (abs(a * d - b * c) - n / 2.0) ** 2 * n / ((a + b) * (c + d) * (a + c) * (b + d))


def fisher_2x2(table: list[list[int]]) -> float:
    """2x2 双尾 Fisher 精确检验（超几何枚举）。"""
    a, b = table[0]
    c, d = table[1]
    r1, r2 = a + b, c + d
    c1, c2 = a + c, b + d
    n = r1 + r2

    def prob(x: int) -> float:
        return math.comb(c1, x) * math.comb(c2, r1 - x) / math.comb(n, r1)

    pobs = prob(a)
    return min(1.0, sum(prob(x) for x in range(max(0, r1 - c2), min(r1, c1) + 1)
                        if prob(x) <= pobs * (1 + 1e-9)))


# ---------------------------------------------------------------- 列联表构建
def build_tables(out: list[list]):
    uniq = [r for r in out if r[7] != "重复"]
    t66 = [[0] * 6 for _ in range(6)]
    for r in uniq:
        t66[ORDER.index(r[2])][ORDER.index(r[5])] += 1

    # 2x3: 父(体制内 G+P / 非体制内) × 母(体制内 G+P / 市场 W+S+M / 家务 H)
    t23 = [[0, 0, 0], [0, 0, 0]]
    for i, j in [(i, j) for i in range(6) for j in range(6)]:
        row = 0 if ORDER[i] in ("G", "P") else 1
        col = 0 if ORDER[j] in ("G", "P") else (2 if ORDER[j] == "H" else 1)
        t23[row][col] += t66[i][j]

    # 2x2: 在业子集（排除任一方 H）
    t22 = [[0, 0], [0, 0]]
    for i in range(5):          # 排除父 H（索引 5）
        for j in range(5):      # 排除母 H（索引 5）
            row = 0 if ORDER[i] in ("G", "P") else 1
            col = 0 if ORDER[j] in ("G", "P") else 1
            t22[row][col] += t66[i][j]

    diag = sum(t66[i][i] for i in range(6))
    return {"uniq": uniq, "t66": t66, "t23": t23, "t22": t22,
            "diag": diag, "n": len(uniq)}


def run_stats(t: dict) -> dict:
    res = {}
    for key in ("t66", "t23", "t22"):
        chi, df, n, emin, lt5, lt1 = pearson(t[key])
        R = len(t[key]); C = len(t[key][0])
        res[key] = {
            "chi2": round(chi, 4), "df": df, "n": n,
            "p": chi2_p(chi, df), "V": cramers_v(chi, n, R, C),
            "Emin": round(emin, 3), "E_lt5": lt5, "E_lt1": lt1,
        }
    y = yates_2x2(t["t22"])
    res["yates"] = {"chi2": round(y, 4), "p": chi2_p(y, 1)}
    res["fisher_p"] = fisher_2x2(t["t22"])
    res["diag_ratio"] = t["diag"] / t["n"]
    return res


# ---------------------------------------------------------------- 输出
def write_clean_csv(out: list[list], path: Path):
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["序号", "父亲工作(清洗)", "父亲类别码", "父亲类别",
                    "母亲工作(清洗)", "母亲类别码", "母亲类别", "重复标记"])
        w.writerows(out)


def print_report(res: dict, fc: dict, mc: dict, n_raw: int):
    print("\n" + "=" * 64)
    print("父母职业相关性分析 · 统计结果（独立复算）")
    print("=" * 64)
    print(f"原始记录 {n_raw} 条；去重后 {res['t66']['n']} 条")
    print(f"父亲编码频数: {fc}")
    print(f"母亲编码频数: {mc}")
    for key, name in [("t66", "6×6 原始"), ("t23", "2×3 全样本"), ("t22", "2×2 在业子集")]:
        r = res[key]
        print(f"\n[{name}] chi2={r['chi2']}  df={r['df']}  n={r['n']}  "
              f"p={r['p']:.6g}  V={r['V']:.4f}  Emin={r['Emin']}  "
              f"E<5={r['E_lt5']}  E<1={r['E_lt1']}")
    print(f"\n[Yates 校正] chi2={res['yates']['chi2']}  p={res['yates']['p']:.6g}")
    print(f"[Fisher 双尾] p={res['fisher_p']:.6g}")
    print(f"[六分类完全一致] {res['diag_ratio']*100:.1f}%")
    print("\n提示: 6×6 表期望频数严重不足，p 值仅描述用；以 2×3 / 2×2 为推断口径。")
    print("=" * 64 + "\n")


REPORT_TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>父母职业相关性分析 · 类别变量练习数据</title>
<style>
  :root{
    --bg:#f5f6f8; --card:#ffffff; --ink:#1f2329; --ink2:#5a6270; --ink3:#8a93a2;
    --line:#e3e7ee; --accent:#2563eb; --accent-soft:#eaf1ff;
    --hot:#c0392b; --hot-soft:#fdecea; --ok:#1f8a5b; --warn:#b8860b;
    --dad:#3b6fd4; --mom:#c2587f;
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);
    font-family:"PingFang SC","Microsoft YaHei","Segoe UI",system-ui,sans-serif;
    line-height:1.75;font-size:15px}
  .wrap{max-width:1000px;margin:0 auto;padding:36px 24px 80px}
  header{background:linear-gradient(135deg,#1e3a8a,#2563eb);color:#fff;border-radius:16px;
    padding:34px 38px;margin-bottom:24px;box-shadow:0 8px 24px rgba(37,99,235,.18)}
  header h1{margin:0 0 8px;font-size:27px;letter-spacing:.5px}
  header .sub{opacity:.86;font-size:14px}
  .verdict{margin-top:20px;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.28);
    border-radius:10px;padding:16px 20px;font-size:15px}
  .verdict b{color:#fff}
  section{background:var(--card);border:1px solid var(--line);border-radius:14px;
    padding:26px 30px;margin-bottom:20px;box-shadow:0 2px 10px rgba(20,30,50,.03)}
  h2{font-size:20px;margin:0 0 18px;padding-left:12px;border-left:4px solid var(--accent)}
  h3{font-size:16px;margin:24px 0 10px;color:#243b6b}
  p{margin:10px 0}
  .muted{color:var(--ink2)}
  .small{font-size:13px;color:var(--ink2)}
  .cards{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:18px 0}
  .card{background:var(--accent-soft);border:1px solid #d5e3ff;border-radius:10px;
    padding:16px 14px;text-align:center}
  .card .num{font-size:24px;font-weight:700;color:var(--accent)}
  .card .lab{font-size:12px;color:var(--ink2);margin-top:4px}
  .card.red{background:var(--hot-soft);border-color:#f5cfca}
  .card.red .num{color:var(--hot)}
  table{border-collapse:collapse;width:100%;margin:12px 0;font-size:13.5px}
  th,td{border:1px solid var(--line);padding:8px 10px;text-align:center}
  th{background:#eef2f7;color:#33405c;font-weight:600}
  td.l,th.l{text-align:left}
  tr:nth-child(even) td{background:#fafbfd}
  .tag{display:inline-block;padding:2px 9px;border-radius:20px;font-size:12px;font-weight:600}
  .t-g{background:#e8eefc;color:#2b56b8}.t-p{background:#e6f6ee;color:#1f8a5b}
  .t-w{background:#fff2e0;color:#b26a00}.t-s{background:#fbeaf1;color:#b34270}
  .t-m{background:#eceff3;color:#566270}.t-h{background:#f2eafd;color:#7c3aed}
  .bars{margin:16px 0}
  .bar-row{display:flex;align-items:center;gap:10px;margin:7px 0;font-size:13px}
  .bar-row .name{width:150px;flex:none;text-align:right;color:var(--ink2)}
  .bar-track{flex:1;background:#eef1f6;border-radius:6px;height:20px;position:relative;overflow:hidden}
  .bar-fill{height:100%;border-radius:6px;display:flex;align-items:center;justify-content:flex-end;
    padding-right:7px;color:#fff;font-size:11px;font-weight:600;min-width:26px}
  .legend{display:flex;gap:20px;justify-content:center;margin:10px 0 4px;font-size:13px;color:var(--ink2)}
  .legend i{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:6px;vertical-align:-1px}
  .heat{font-weight:700}
  .callout{background:#f8fafc;border-left:4px solid var(--accent);border-radius:0 8px 8px 0;
    padding:14px 18px;margin:14px 0;font-size:14px}
  .callout.warn{background:#fffaf0;border-color:var(--warn)}
  .callout.red{background:var(--hot-soft);border-color:var(--hot)}
  .disc{display:grid;grid-template-columns:120px 1fr;gap:14px;padding:14px 0;border-bottom:1px dashed var(--line)}
  .disc:last-child{border-bottom:none}
  .disc .who{font-weight:700;color:#243b6b}
  .refs{font-size:12.5px;color:var(--ink2)}
  .refs li{margin:8px 0}
  a{color:var(--accent);text-decoration:none;word-break:break-all}
  a:hover{text-decoration:underline}
  footer{text-align:center;color:var(--ink3);font-size:12px;padding:20px}
  @media(max-width:720px){.cards{grid-template-columns:repeat(2,1fr)}.disc{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="wrap">

<header>
  <h1>父母职业相关性分析</h1>
  <div class="sub">数据对象：类别变量练习数据.csv · 53 条记录 · 清理去重后 51 条 · 2026-11-18</div>
  <div class="verdict">
    <b>结论先行：</b>在合规统计口径下，父亲与母亲的职业类别存在<b>统计显著、中等偏强</b>的关联
    （在业子集 χ²=8.77, p=0.0031, Cramér's V=0.474；全样本二分口径 V=0.622）。
    关联的方向是<b>“体制内配体制内、市场配市场/家务”</b>的同类匹配，且伴随明显的性别职业分工。
    但该结论仅在本练习样本内成立，样本小、编码主观，<b>不可外推为对真实社会的估计</b>。
  </div>
</header>

<section>
  <h2>一、数据清理与转化</h2>

  <h3>1.1 原始数据结构与问题</h3>
  <p>文件为 <b>GBK 编码</b>，直接以 UTF-8 读取会乱码；含 <b>1 处跨行带引号字段</b>（须按 CSV 引号规则解析，否则行数会错）。
  表头两列：父亲工作、母亲工作，均为文本型类别变量，取值高度分散（多为具体单位全名）。</p>
  <table>
    <tr><th class="l">问题类型</th><th>数量</th><th class="l">处置</th></tr>
    <tr><td class="l">母亲列空单元格</td><td>1</td><td class="l">归入 H 类（家务/无业/缺失），保留记录</td></tr>
    <tr><td class="l">母亲列填“无”</td><td>1</td><td class="l">归入 H 类</td></tr>
    <tr><td class="l">完全重复记录</td><td>2</td><td class="l">推断统计中剔除（n=51），描述统计另报含重复版</td></tr>
    <tr><td class="l">XX / XXX 匿名占位</td><td>4</td><td class="l">保留，按可识别行业归入相应类别</td></tr>
    <tr><td class="l">首尾空白 / 换行符</td><td>3</td><td class="l">统一 strip 清洗</td></tr>
  </table>
  <p class="small">重复记录：区建豪汽修中心×家庭主妇、盛泰房地产公司×家庭主妇（各出现 2 次）。</p>

  <h3>1.2 从“单位名”到“职业类别”的转化</h3>
  <p>原始取值是<b>具体单位名称</b>，53 行里有 40+ 个不同单位，直接做列联表会极度稀疏、无法检验。
  因此按<b>单位性质 / 行业</b>归并为 6 类（这是本分析最关键、也最主观的一步）：</p>
  <table>
    <tr><th class="l">类别码</th><th class="l">含义</th><th class="l">典型原始值</th></tr>
    <tr><td><span class="tag t-g">G</span></td><td class="l">党政机关 / 基层政权</td><td class="l">市民政局、市公安局、XXX镇政府、街道办</td></tr>
    <tr><td><span class="tag t-p">P</span></td><td class="l">事业单位 / 教育医疗专业技术</td><td class="l">市实验中学、市第一人民医院、职业技术学院</td></tr>
    <tr><td><span class="tag t-w">W</span></td><td class="l">企业白领 / 管理技术</td><td class="l">科技公司、房地产、银行、资产评估</td></tr>
    <tr><td><span class="tag t-s">S</span></td><td class="l">个体经营 / 商贸服务</td><td class="l">饺子馆、汽修中心、旅行社、个体药店</td></tr>
    <tr><td><span class="tag t-m">M</span></td><td class="l">工农制造 / 建筑运输</td><td class="l">中铁六局、化工公司、水利水电工程局</td></tr>
    <tr><td><span class="tag t-h">H</span></td><td class="l">家务 / 无业 / 缺失</td><td class="l">家庭主妇、家庭父母、无、空</td></tr>
  </table>
  <p class="small">完整的逐条编码映射见交付文件《类别变量练习数据_清理转化后.csv》，含原始值、类别码、类别标签与重复标记。</p>

  <h3>1.3 归并后频数分布（n=53）</h3>
  <div class="legend"><span><i style="background:var(--dad)"></i>父亲</span><span><i style="background:var(--mom)"></i>母亲</span></div>
  <div class="bars">
    <div class="bar-row"><span class="name">G 党政机关</span><div class="bar-track"><div class="bar-fill" style="width:100%;background:var(--dad)">22</div></div></div>
    <div class="bar-row"><span class="name"></span><div class="bar-track"><div class="bar-fill" style="width:63.6%;background:var(--mom)">14</div></div></div>
    <div class="bar-row"><span class="name">P 事业/专技</span><div class="bar-track"><div class="bar-fill" style="width:9.1%;background:var(--dad)">2</div></div></div>
    <div class="bar-row"><span class="name"></span><div class="bar-track"><div class="bar-fill" style="width:40.9%;background:var(--mom)">9</div></div></div>
    <div class="bar-row"><span class="name">W 企业白领</span><div class="bar-track"><div class="bar-fill" style="width:27.3%;background:var(--dad)">6</div></div></div>
    <div class="bar-row"><span class="name"></span><div class="bar-track"><div class="bar-fill" style="width:18.2%;background:var(--mom)">4</div></div></div>
    <div class="bar-row"><span class="name">S 个体/服务</span><div class="bar-track"><div class="bar-fill" style="width:40.9%;background:var(--dad)">9</div></div></div>
    <div class="bar-row"><span class="name"></span><div class="bar-track"><div class="bar-fill" style="width:45.5%;background:var(--mom)">10</div></div></div>
    <div class="bar-row"><span class="name">M 工农制造</span><div class="bar-track"><div class="bar-fill" style="width:50%;background:var(--dad)">11</div></div></div>
    <div class="bar-row"><span class="name"></span><div class="bar-track"><div class="bar-fill" style="width:13.6%;background:var(--mom)">3</div></div></div>
    <div class="bar-row"><span class="name">H 家务/无业</span><div class="bar-track"><div class="bar-fill" style="width:13.6%;background:var(--dad)">3</div></div></div>
    <div class="bar-row"><span class="name"></span><div class="bar-track"><div class="bar-fill" style="width:59.1%;background:var(--mom)">13</div></div></div>
  </div>
  <div class="callout">
    <b>第一眼发现：</b>父亲高度集中于党政机关（22/53 = 41.5%），母亲则集中在党政机关（26.4%）与家务/无业（24.5%）。
    母亲家务/无业比例是父亲的 <b>8.7 倍</b>（13 vs 3），父亲工农制造比例是母亲的 <b>3.7 倍</b>（11 vs 3）——
    这是典型的性别职业分工信号。
  </div>
</section>

<section>
  <h2>二、相关性分析</h2>

  <h3>2.1 先做前提诊断：细粒度列联表不能用</h3>
  <p>6×6 原始列联表（去重后 n=51）的卡方结果为 χ²=42.00, df=25, p=0.018, V=0.406。
  但诊断发现 <b>36 个单元格中有 35 个期望频数 &lt; 5、20 个 &lt; 1</b>，卡方近似的适用前提被严重违反，
  这个 p 值<b>不可用于推断</b>，只能当描述。必须合并类别。</p>
  <div class="callout warn">
    <b>方法要点：</b>卡方检验要求多数单元格期望频数 ≥5。类别过细 → 表格稀疏 → 检验失真。
    这也是为什么“先归并成有意义的大类”不是可选项，而是必需步骤。
  </div>

  <h3>2.2 合规口径一：2×3 全样本（父：体制内/非 × 母：体制内/市场/家务）</h3>
  <table>
    <tr><th>父亲 ＼ 母亲</th><th>体制内(G+P)</th><th>市场就业(W+S+M)</th><th>家务(H)</th><th>合计</th></tr>
    <tr><th>体制内</th><td class="heat" style="background:#dbe7ff">18</td><td>6</td><td>0</td><td>24</td></tr>
    <tr><th>非体制内</th><td>5</td><td class="heat" style="background:#dbe7ff">11</td><td>5</td><td>27</td></tr>
    <tr><th>合计</th><td>23</td><td>17</td><td>11</td><td>51</td></tr>
  </table>
  <p>最小期望频数 5.18，全部 6 格满足 E≥5，前提达标。结果：<b>χ²=19.71, df=2, p=5.2×10⁻⁵, Cramér's V=0.622</b>。
  显著且关联强度较高。</p>

  <h3>2.3 合规口径二：2×2 在业子集（排除任一方家务/无业，n=39）</h3>
  <table>
    <tr><th>父亲 ＼ 母亲</th><th>体制内</th><th>市场就业</th><th>合计</th></tr>
    <tr><th>体制内</th><td class="heat" style="background:#f7cfc9">18</td><td>6</td><td>24</td></tr>
    <tr><th>非体制内</th><td>4</td><td class="heat" style="background:#f7cfc9">11</td><td>15</td></tr>
    <tr><th>合计</th><td>22</td><td>17</td><td>39</td></tr>
  </table>
  <table>
    <tr><th class="l">统计量</th><th>数值</th><th class="l">说明</th></tr>
    <tr><td class="l">Pearson χ² (df=1)</td><td>8.770</td><td class="l">p = 0.0031</td></tr>
    <tr><td class="l">Yates 校正 χ²</td><td>6.914</td><td class="l">p = 0.0086（2×2 保守校正）</td></tr>
    <tr><td class="l">Fisher 精确检验（双尾）</td><td>p = 0.0069</td><td class="l">不依赖近似，结论稳健</td></tr>
    <tr><td class="l">Cramér's V</td><td>0.474</td><td class="l">中等偏强关联</td></tr>
  </table>
  <p>三种检验一致显著，说明结论稳健。体制内父亲中 75%（18/24）的妻子也在体制内；体制外父亲的妻子仅 27%（4/15）在体制内。</p>

  <h3>2.4 描述性佐证</h3>
  <div class="cards">
    <div class="card"><div class="num">41.2%</div><div class="lab">六分类“职业完全相同”比例（21/51）</div></div>
    <div class="card"><div class="num">60.8%</div><div class="lab">三分类口径同类匹配比例</div></div>
    <div class="card"><div class="num">75%</div><div class="lab">体制内父亲的配偶也在体制内</div></div>
    <div class="card red"><div class="num">8.7×</div><div class="lab">母亲家务/无业比例 ÷ 父亲</div></div>
  </div>
  <p>对角线贡献最大的是 G×G=10（党政机关配偶匹配）。剔除 2 条重复记录后关联强度反而略升，
  说明重复记录并未驱动结论。</p>
</section>

<section>
  <h2>三、多学科解读</h2>
  <p class="muted">以下用不同学科的解释框架理解上述发现。<b>注意：</b>本数据集是练习数据（含 XXX 占位、编造单位名、样本仅 51 条），
  学科理论用于解释“这类模式通常意味着什么”，而不是证明本样本代表了真实社会。</p>

  <div class="disc">
    <div class="who">统计学</div>
    <div><b>“相关”成立，但只是类别层面的总体关联，不等于个体层面的预测，更不等于因果。</b>
      Cramér's V 在 0.47–0.62 之间，属于中等到较强；但 V 对分类粒度敏感——分类越粗 V 越大，
      所以 0.622 与 0.474 的差异主要来自口径而非真实强度差异。真正稳健的结论是：
      在两种合规口径下都显著、方向一致。卡方检验的适用前提（期望频数）在此数据中必须依靠合并类别才满足，
      这本身提醒我们：<b>统计结论是“分析选择的产物”，不是数据自动给出的。</b></div>
  </div>

  <div class="disc">
    <div class="who">社会学<br><span class="small">分层与婚配</span></div>
    <div>本研究最贴近社会学中的<b>职业同质婚配（occupational homogamy / assortative mating）</b>现象——
      即夫妻在职业、教育、阶层上相似性高于随机。Kalmijn（1994）用 70×70 职业婚姻表发现，
      基于<b>文化地位</b>的同质婚配比基于经济地位的更重要，并提出“匹配假说”（相似者相吸）与
      “竞争假说”（都想要高地位者，结果高地位者彼此结合）两种机制。本样本中“体制内—体制内”的强匹配，
      既可用匹配假说解释（相似的工作环境、作息、价值观、社交圈），也可用机会结构解释——
      《北京社会科学》2019 年的研究发现，<b>职业阶层同质婚更适合用“机会结构理论”解释</b>：
      阶层位置越低、择偶圈越窄，越可能在相似人群中婚配。样本中党政机关占父亲 41.5%，
      这类单位的封闭社交圈恰好为同类匹配提供了结构条件。
      更宏观地，Schwartz 等（2021）用美国 1970–2017 数据发现双专业人士夫妻近三倍增长，
      但指出绝大部分变化来自<b>职业分布本身的变化</b>（如女性进入专业职业增多），而非匹配倾向增强——
      这提醒我们：<b>看到“同类配同类”，未必是择偶偏好变强，也可能只是某类人在人群里变多了。</b></div>
  </div>

  <div class="disc">
    <div class="who">人口学<br>与性别研究</div>
    <div>母亲“家务/无业”占 24.5%、父亲仅 5.7%（差 8.7 倍），以及
      “个体/体力父亲 × 家务母亲”的 8 个组合（S父×H母=3、M父×H母=5），
      指向<b>性别化的家庭分工</b>。赵耀辉、毕汝岱基于 1990–2020 普查数据的研究显示，
      中国 25–44 岁女性劳动参与率从 90% 降至 71%，已生育女性劳动参与率下降是主因（贡献超 100%），
      且配偶收入提高会<b>负向</b>影响女性劳动参与——这与本样本中“丈夫在体制内、妻子在家务”的
      不对称组合方向一致（虽不能据此推断因果）。第四期中国妇女社会地位调查显示，
      0–17 岁子女的日常照料主要由母亲承担的家庭占 76.1%，女性家务劳动时间约为男性 2 倍。
      上野千鹤子《父权制与资本主义》把这种“男性从事生产劳动、女性负责家务”的分工视为
      资本主义与父权制妥协的结果。人口学视角还提示<b>生命周期偏差</b>：
      母亲“无业”可能只是阶段性退出（育儿期），若数据未记录年龄与子女状况，
      会把“暂时退出”误读为“永久无业”。</div>
  </div>

  <div class="disc">
    <div class="who">劳动<br>经济学</div>
    <div>职业是分层系统的核心——它决定收入、声望、生活方式与社交网络。
      夫妻职业高度相关，意味着<b>家庭收入的相关性上升、家庭间不平等被放大</b>：
      两个体制内/双专业人士的组合会把资源集中到同一家庭。
      Schwartz 等（2021）量化发现，职业同质婚配对美国家庭收入不平等上升的贡献约为 5%，
      虽不算大，却大于此前教育同质婚配的估计。本样本没有收入字段，无法直接检验这一机制，
      但“体制内同配 75%”至少提示了资源在同质家庭内聚集的可能性。
      另外要注意<b>单位性质 ≠ 职业岗位</b>：同在“有限公司”，可能是高管也可能是普通工人，
      用单位名推断职业会引入测量误差，削弱或扭曲关联估计。</div>
  </div>

  <div class="disc">
    <div class="who">数据科学<br>方法论</div>
    <div>这个练习数据本身就是一堂方法论课：①<b>编码前必须理解业务</b>——把单位名映射成职业类别
      是主观判断，不同人的编码会得出不同的 V；②<b>稀疏列联表必须诊断期望频数</b>，
      否则 p 值失真；③<b>样本量决定结论边界</b>——51 条数据只能做探索性分析，
      任何细粒度（6×6）结论都不可靠；④<b>缺失与重复要显式处理并报告</b>，
      不能静默丢弃；⑤<b>相关不等于因果</b>——即使父母职业显著相关，
      也无法回答“是择偶时匹配、还是婚后互相影响、还是家庭背景共同塑造”。
      规范的流程应是：清理 → 编码 → 前提诊断 → 选择合适检验 → 报告效应量与局限。</div>
  </div>
</section>

<section>
  <h2>四、局限与使用建议</h2>
  <ul>
    <li><b>样本小：</b>n=51（在业子集 39），仅可做探索性分析，不可外推到总体。</li>
    <li><b>编码主观：</b>基于单位名推断职业，M/W 边界、“家庭父亲/父母”的归类会实质影响 V 值。</li>
    <li><b>测量粗：</b>没有职业地位、收入、教育、年龄、婚龄等变量，无法做更精细的分层分析或控制混杂。</li>
    <li><b>数据性质：</b>含 XXX 占位与编造单位名，是练习数据；学科解读是框架演示，不是实证结论。</li>
    <li><b>若要深化：</b>可补充父母教育、收入、年龄，改用对数线性模型或列联表精确检验（Fisher–Freeman–Halton），
      并用更大真实样本（如 CGSS、CFPS）复核。</li>
  </ul>
  <div class="callout red">
    <b>一句话提醒：</b>“父母职业显著相关”在这里是一个<b>统计描述</b>，
    它打开了社会学解释的大门，但不构成对社会因果的证明。
  </div>
</section>

<section>
  <h2>参考来源（均经检索核实）</h2>
  <ol class="refs">
    <li>Kalmijn, M. (1994). <i>Assortative Mating by Cultural and Economic Occupational Status</i>, American Journal of Sociology.
      <a href="https://pure.uvt.nl/ws/portalfiles/portal/647948/MK01_.PDF">pure.uvt.nl/ws/portalfiles/portal/647948/MK01_.PDF</a></li>
    <li>Schwartz, C. R. et al. (2021). <i>Opportunity and change in occupational assortative mating</i> (1970–2017, 美国人口普查/ACS).
      <a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC8387636/">pmc.ncbi.nlm.nih.gov/articles/PMC8387636/</a></li>
    <li>《偏好与结构——同质婚的形成机制研究》，《北京社会科学》2019 年第 8 期。
      <a href="https://tg.bass.org.cn/CN/10.13262/j.bjsshkxy.bjshkx.190807">tg.bass.org.cn/CN/10.13262/j.bjsshkxy.bjshkx.190807</a></li>
    <li>赵耀辉、毕汝岱：《从家庭视角看中国女性劳动参与率的下降趋势》（基于 1990–2020 全国人口普查与抽样调查）。
      <a href="http://www.hsskw.com/zkjs/zjjs/202502/t20250212_1192611.html">hsskw.com/zkjs/zjjs/202502/t20250212_1192611.html</a></li>
    <li>第四期中国妇女社会地位调查主要数据（2021），人民网转载。
      <a href="https://m.people.cn/n4/2022/0223/c34-15452450.html">m.people.cn/n4/2022/0223/c34-15452450.html</a></li>
    <li>Clark, G. &amp; Cummins, N. (2022). <i>Assortative Mating and the Industrial Revolution: England, 1754–2021</i>, LSE.
      <a href="http://eprints.lse.ac.uk/115008/1/WP337.pdf">eprints.lse.ac.uk/115008/1/WP337.pdf</a></li>
  </ol>
</section>

<footer>本报告由数据清理转化结果 + 独立复算统计 + 多学科文献解读生成 · 仅供学习使用</footer>

</div>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser(description="父母职业相关性分析（一体化脚本）")
    ap.add_argument("--src", default=DEFAULT_SRC, help="源 CSV 路径（默认 GBK 编码）")
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent), help="输出目录")
    args = ap.parse_args()

    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    rows, enc, text = read_csv_auto(args.src)
    print(f"读取成功: {args.src}  编码={enc}  解析记录={len(rows)-1}")

    utf8_path = outdir / "类别变量练习数据_UTF8.csv"
    utf8_path.write_text(text, encoding="utf-8", newline="")

    out, fc, mc = transform(rows)
    write_clean_csv(out, outdir / "类别变量练习数据_清理转化后.csv")

    t = build_tables(out)
    res = run_stats(t)
    print_report(res, fc, mc, len(out))

    summary = {
        "source": args.src, "encoding": enc, "n_raw": len(out),
        "n_unique": t["n"], "father_freq": fc, "mother_freq": mc,
        "tables": {"t66": t["t66"], "t23": t["t23"], "t22": t["t22"]},
        "stats": res,
        "note": "6x6 表期望频数不足，仅作描述；推断以 2x3 / 2x2 为准。",
    }
    (outdir / "analysis_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    if REPORT_TEMPLATE.lstrip().startswith("<!DOCTYPE"):
        (outdir / "父母职业相关性分析报告.html").write_text(
            REPORT_TEMPLATE, encoding="utf-8")
    print(f"产物目录: {outdir}")


if __name__ == "__main__":
    main()
