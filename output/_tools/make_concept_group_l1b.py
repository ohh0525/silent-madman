# -*- coding: utf-8 -*-
"""concept-group-guide / Phase 2 生成器（第二组）

为概念组「Python 第 1 课 · 下半场四概念」生成：
  4 份 7 段式 HTML 学习材料 -> Python基础语法课程/learning-materials/

复用 learning-materials/agent.html 的 CSS 结构（与第一组同一套），只改 --accent / --accent-soft。
"""
import io
import os

ROOT = r"D:\桌面\silent-madman"
OUT_DIR = os.path.join(ROOT, "Python基础语法课程", "learning-materials")
GROUP_DIR = os.path.join(ROOT, "concept-group", "python-lesson1-second-half")

GROUP_NAME = "Python 第 1 课 · 下半场四概念"
DATE = "2026-09-17"
SKILL_SIGN = "concept-group-guide"
TOTAL = 4

# --------------------------------------------------------------------------
# CSS：与第一组逐字同源（learning-materials/agent.html），仅主题色变量参数化
# --------------------------------------------------------------------------
STYLE = """<style>
  :root {
    --bg: #fafaf7;
    --panel: #ffffff;
    --ink: #1f2328;
    --ink-soft: #57606a;
    --accent: __ACCENT__;
    --accent-soft: __ACCENT_SOFT__;
    --line: #e5e2dc;
    --code-bg: #f6f4ee;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    font-family: -apple-system, "PingFang SC", "Microsoft YaHei", "Helvetica Neue", Arial, sans-serif;
    background: var(--bg);
    color: var(--ink);
    line-height: 1.75;
    -webkit-font-smoothing: antialiased;
  }
  .wrap { max-width: 880px; margin: 0 auto; padding: 48px 32px 96px; }
  header.cover {
    border-bottom: 1px solid var(--line);
    padding-bottom: 24px;
    margin-bottom: 32px;
  }
  .tag {
    display: inline-block;
    background: var(--accent-soft);
    color: var(--accent);
    font-size: 12px;
    padding: 4px 10px;
    border-radius: 999px;
    letter-spacing: 0.04em;
  }
  h1 {
    font-size: 32px;
    margin: 16px 0 6px;
    line-height: 1.3;
  }
  .subtitle { color: var(--ink-soft); font-size: 14px; margin: 0; }
  section {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 24px 28px;
    margin-bottom: 20px;
  }
  h2 {
    font-size: 18px;
    margin: 0 0 14px;
    color: var(--accent);
    letter-spacing: 0.02em;
    border-left: 3px solid var(--accent);
    padding-left: 12px;
  }
  h3 { font-size: 15px; margin: 18px 0 8px; }
  p { margin: 0 0 12px; }
  ul, ol { margin: 8px 0 12px; padding-left: 22px; }
  li { margin-bottom: 6px; }
  .def {
    background: var(--accent-soft);
    border-radius: 8px;
    padding: 14px 18px;
    font-size: 17px;
    margin: 0;
  }
  .scenario {
    background: var(--code-bg);
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 12px;
  }
  .scenario h3 { margin: 0 0 6px; font-size: 15px; color: var(--ink); }
  .scenario p { margin: 0 0 4px; font-size: 14px; }
  .scenario .label { font-weight: 600; color: var(--accent); }
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
    margin: 8px 0;
  }
  th, td {
    text-align: left;
    padding: 10px 12px;
    border-bottom: 1px solid var(--line);
    vertical-align: top;
  }
  th { background: var(--code-bg); font-weight: 600; }
  .sources li { font-size: 14px; word-break: break-all; }
  .sources a { color: var(--accent); text-decoration: none; }
  .sources a:hover { text-decoration: underline; }
  .takeaway {
    background: var(--accent-soft);
    border-radius: 8px;
    padding: 16px 20px;
    font-size: 17px;
    font-weight: 500;
  }
  .callout {
    background: var(--accent-soft);
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 14px;
    margin: 12px 0;
  }
  footer {
    margin-top: 32px;
    text-align: center;
    color: var(--ink-soft);
    font-size: 13px;
  }
  .mermaid-placeholder {
    background: var(--code-bg);
    border-radius: 8px;
    padding: 18px;
    font-family: ui-monospace, "SFMono-Regular", Consolas, monospace;
    font-size: 13px;
    white-space: pre;
    overflow-x: auto;
    color: var(--ink-soft);
  }
</style>"""


def page(title, tag, h1, subtitle, body, accent, accent_soft):
    style = STYLE.replace("__ACCENT__", accent).replace("__ACCENT_SOFT__", accent_soft)
    return (
        "<!DOCTYPE html>\n<html lang=\"zh-CN\">\n<head>\n"
        "<meta charset=\"UTF-8\" />\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />\n"
        "<title>" + title + "</title>\n"
        + style + "\n</head>\n<body>\n<div class=\"wrap\">\n\n"
        + "<header class=\"cover\">\n"
        + "  <span class=\"tag\">" + tag + "</span>\n"
        + "  <h1>" + h1 + "</h1>\n"
        + "  <p class=\"subtitle\">" + subtitle + "</p>\n"
        + "</header>\n\n"
        + body
        + "\n<footer>由 " + SKILL_SIGN + " Skill 生成 · " + DATE
        + " · 概念组：" + GROUP_NAME + "</footer>\n\n</div>\n</body>\n</html>\n"
    )


def footer_note(n):
    return "生成时间 " + DATE + " · 组内第 " + str(n) + " / " + str(TOTAL)


TAG = "概念组 · " + GROUP_NAME


# ==========================================================================
# 1. 运算符
# ==========================================================================
BODY_OP = """<section>
  <h2>1 · 一句话定义</h2>
  <p class="def">运算符就是让 Python 对值做运算的符号：算术运算符负责算数，比较运算符负责比大小，逻辑运算符负责把条件组合起来。</p>
</section>

<section>
  <h2>2 · 个人解释</h2>
  <p>把一段代码想成一句话。在 <em>3 + 5</em> 里，<em>3</em> 和 <em>5</em> 是名词，<em>+</em> 是动词 —— 运算符就是这门语言里的动词。变量和类型告诉你"有什么"，运算符决定"拿它做什么"。上半场你已经会写 <em>name = "小明"</em> 这种"给数据起名"的句子；从这一篇起，句子开始真的动起来。</p>
  <p>这里有一条最容易被忽略、却几乎解释了所有相关报错的规则：<strong>同一个符号，遇到不同类型的值，做的事不一样</strong>。<em>+</em> 碰上两个数字就相加，碰上两个文本就拼接。所以 <em>"2" + "3"</em> 得到的是 <em>'23'</em>，不是 5 —— 这不是 Python 有毛病，而是 <em>+</em> 在文本世界里的职责本来就是"接起来"。同理 <em>*</em> 碰上"文本 × 整数"就变成重复：<em>"ab" * 2</em> 得到 <em>'abab'</em>。想通这一层，你以后看到 <em>TypeError</em> 就不会慌，因为你知道那多半是"两种不同类型的值被拿去做同一件要求类型一致的事"。</p>
  <p>还有一个必须当场分清的对子：<em>=</em> 和 <em>==</em>。<em>=</em> 是<strong>赋值</strong>——把右边的值装进左边的名字；<em>==</em> 是<strong>比较</strong>——问"这两边相等吗"，回答是 <em>True</em> 或 <em>False</em>。把它们写混是新手最高频的一类糊涂：写成 <em>x = 5</em> 是"把 5 给 x"，写成 <em>x == 5</em> 才是"问 x 是不是 5"。</p>
  <p>最后一个直觉，关于顺序。你写 <em>2 + 3 * 4</em>，Python 给的是 <strong>14</strong> 而不是 20 —— 因为 <em>*</em> 的优先级高于 <em>+</em>，先算 3 * 4 再加 2。<em>7 / 2</em> 也不是 3，而是 <strong>3.5</strong>：Python 的 <em>/</em> 是"真除法"，永远给你小数；想要"整数除以整数得整数"，得用 <em>//</em>。这两条各对应一个很常见的困惑，记住它们比背优先级表划算得多。</p>
</section>

<section>
  <h2>3 · 核心机制</h2>
  <p>入门阶段真正要掌握的是三组运算符。它们的共同点是：输入是值，输出也是一个值 —— 也就是"表达式"。</p>
  <ol>
    <li><strong>算术运算符</strong>：<em>+</em> 加、<em>-</em> 减、<em>*</em> 乘、<em>/</em> 除、<em>//</em> 整除、<em>%</em> 取余、<em>**</em> 幂。<br />为什么重要：<em>/</em> 与 <em>//</em> 的区别（3.5 还是 3）是新手第一个"和直觉不符"的点，而 <em>%</em> 是判断奇偶、按编号分组的唯一工具。</li>
    <li><strong>比较运算符</strong>：<em>==</em> 等于、<em>!=</em> 不等于、<em>&gt;</em> 大于、<em>&lt;</em> 小于、<em>&gt;=</em> 大于等于、<em>&lt;=</em> 小于等于。<br />为什么重要：它们的<strong>结果永远是 <em>bool</em>（True / False）</strong>，不是数字 —— 认清这一点，才知道比较的结果该交给谁（后续课程的条件分支）去用。</li>
    <li><strong>逻辑运算符</strong>：<em>and</em> 两个都成立、<em>or</em> 任一成立、<em>not</em> 取反。<br />为什么重要：现实里的条件很少只有一个；把"A 且 B"合成一个真假值，靠的就是它们。</li>
    <li><strong>优先级与括号</strong>：从高到低大致是 括号 → <em>**</em> → <em>* / // %</em> → <em>+ -</em> → 比较 → <em>not</em> → <em>and</em> → <em>or</em>。<br />为什么重要：不必背全表，记住一句"<strong>不确定就加括号</strong>"即可 —— 括号既消除歧义，也让代码更像人话。</li>
  </ol>
  <div class="mermaid-placeholder"># 算术：注意 / 与 // 的区别
7 / 2      # 3.5   ← 真除法：结果永远是小数
7 // 2     # 3     ← 整除：向下取整
7 % 2      # 1     ← 取余
2 ** 3     # 8     ← 幂

# 比较：结果永远是 True / False
3 == 3     # True
3 != 3     # False
2 &lt;= 2     # True

# 逻辑：把多个条件合成一个
1 &lt; 2 and 2 &lt; 3     # True   两个都成立才为 True
1 &lt; 2 or 3 &lt; 2      # True   任一个成立就为 True
not True           # False

# 同一个 +，两种含义 —— 取决于两边是什么类型
2 + 3         # 5        数字相加
"2" + "3"     # '23'     文本拼接（不是 5！）
"ab" * 2      # 'abab'   文本重复
# 2 + "3"     # TypeError：类型不匹配，读法见「报错怎么读」

# 优先级：不确定就加括号
2 + 3 * 4      # 14      不是 20
(2 + 3) * 4    # 20      括号最优先</div>
</section>

<section>
  <h2>4 · 应用场景</h2>
  <div class="scenario">
    <h3>场景 1 · 用取余判断奇偶</h3>
    <p><span class="label">背景：</span>要给一批编号分流：偶数的排左边、奇数的排右边。</p>
    <p><span class="label">如何应用：</span>用 <em>n % 2</em> —— 结果是 0 就是偶数，是 1 就是奇数；写成 <em>n % 2 == 0</em> 就得到一个 True / False 的结果。</p>
    <p><span class="label">结果：</span>把"奇数还是偶数"这个需要肉眼判断的问题，变成一个可以被程序直接使用的真假值。</p>
  </div>
  <div class="scenario">
    <h3>场景 2 · 用真除法算平均分</h3>
    <p><span class="label">背景：</span>总分 253、人数 3，想算平均分，却发现结果是 84 而不是 84.33。</p>
    <p><span class="label">如何应用：</span>把 <em>total // count</em> 改成 <em>total / count</em> —— 前者整除会把小数位直接切掉，后者才是真除法。</p>
    <p><span class="label">结果：</span>拿到 84.33…，小数不再被无声吞掉；也顺手记住了 <em>/</em> 与 <em>//</em> 的分工。</p>
  </div>
  <div class="scenario">
    <h3>场景 3 · 把多个条件合成一个</h3>
    <p><span class="label">背景：</span>要表达"成年且有票"这样一个完整条件。</p>
    <p><span class="label">如何应用：</span>用 <em>and</em> 把两个比较连起来：<em>age &gt;= 18 and has_ticket == True</em>；只要有一个不成立，整个表达式就是 False。</p>
    <p><span class="label">结果：</span>复杂条件被压成<strong>一个</strong>真假值，可以直接交给后续的判断语句使用，而不必层层嵌套。</p>
  </div>
</section>

<section>
  <h2>5 · 边界辨析</h2>
  <h3>5.1 不是什么</h3>
  <ul>
    <li><strong>不是"符号就是运算"</strong>：<em>=</em> 是赋值、<em>==</em> 是比较，两者职责完全不同。把 <em>=</em> 当成"等于"来读，是新手最典型的误读。</li>
    <li><strong>不含成员运算 <em>in</em></strong>：<em>"x" in "xyz"</em>、<em>3 in [1,2,3]</em>、<em>"name" in {...}</em> 确实都是"某个值在不在里面"，但它们的语义要看容器本身 —— 本篇不展开，"在不在列表里"归 <a href="列表.html">列表</a> 篇，"这个键在不在字典里"归 <a href="字典.html">字典</a> 篇。</li>
    <li><strong>不含位运算与身份运算</strong>：<em>&amp; | ^ &lt;&lt; &gt;&gt;</em> 是给整数按二进制位做运算的，<em>is</em> 是判断"是不是同一个对象"，入门阶段几乎用不到，本篇不展开。</li>
    <li><strong>不负责分支</strong>："算出一个 True / False"是本篇的终点；"拿它去决定走哪条路"属于后续的控制流课程。</li>
  </ul>
  <h3>5.2 常见误解</h3>
  <ul>
    <li>「<em>7 / 2</em> 得 3」—— 不是，得 <em>3.5</em>。<em>/</em> 是真除法，永远返回小数；要整除必须用 <em>//</em>。</li>
    <li>「<em>"2" + "3"</em> 得 5」—— 不是，得 <em>'23'</em>。加号在文本上做的是拼接，类型不同则含义不同。</li>
    <li>「<em>2 + 3 * 4</em> 从左往右算」—— 不是，先乘后加，得 <em>14</em>。真拿不准就加括号。</li>
    <li>「<em>0.1 + 0.2 == 0.3</em> 是 True」—— 不是。浮点数是二进制近似表示，这个比较会得到 False —— 原理见上半场 <a href="变量与基本类型.html">变量与基本类型</a> 篇。</li>
  </ul>
  <h3>5.3 与组内邻居的分工</h3>
  <table>
    <thead><tr><th>相邻概念</th><th>本概念负责</th><th>交给邻居</th></tr></thead>
    <tbody>
      <tr><td><a href="列表.html">列表</a></td><td>讲 <em>+</em> 在数字与文本上的两种含义</td><td>列表的创建、索引、切片与增删改（本概念只提一句"两个列表也能用 <em>+</em> 合并"）</td></tr>
      <tr><td><a href="字典.html">字典</a></td><td>只讲算术 / 比较 / 逻辑三组运算符，<strong>不含 <em>in</em></strong></td><td>"这个键在不在字典里"、按键取值与改值</td></tr>
      <tr><td><a href="列表套字典.html">列表套字典 = 一张表</a></td><td>只给"对单个值做运算"的规则</td><td>把多行记录按字段取出来的整套结构</td></tr>
      <tr><td>变量与基本类型（上半场）</td><td>直接沿用不变与类型的概念，不重复讲</td><td>变量是名字指向值、int / float / str / bool 与类型转换</td></tr>
    </tbody>
  </table>
  <h3>5.4 适用与不适用</h3>
  <table>
    <thead><tr><th>本概念能解决</th><th>要找别处</th></tr></thead>
    <tbody>
      <tr><td>算数、比大小、组合条件</td><td>根据条件走不同分支（后续控制流课程）</td></tr>
      <tr><td>理解同一符号在不同类型上的不同行为</td><td>类型不匹配报错的逐行读法（找 <a href="报错怎么读.html">报错怎么读</a>）</td></tr>
      <tr><td>知道 <em>/</em> 与 <em>//</em>、<em>=</em> 与 <em>==</em> 的区别</td><td>在容器里找东西（找 <a href="列表.html">列表</a> / <a href="字典.html">字典</a>）</td></tr>
    </tbody>
  </table>
</section>

<section class="sources">
  <h2>6 · 来源链接</h2>
  <ol>
    <li><a href="https://docs.python.org/zh-cn/3/tutorial/introduction.html">3. 一个非正式介绍 · Python 官方教程（中文）</a> — 官方用"把 Python 当作计算器"的方式介绍算术运算符，并明确 <em>/</em> 返回浮点数、<em>//</em> 用于整除、<em>%</em> 用于取余。</li>
    <li><a href="https://docs.python.org/zh-cn/3/reference/expressions.html">6. 表达式 · Python 官方语言参考（中文）</a> — 官方对算术转换、比较运算（含 <em>==</em> / <em>!=</em> / <em>&gt;=</em> 等）、布尔运算 <em>and / or / not</em> 的定义，以及完整的<strong>运算符优先级表</strong>。</li>
    <li><a href="https://docs.python.org/zh-cn/3/library/stdtypes.html">内置类型 · Python 官方文档（中文）</a> — 官方对数字类型的运算规则与比较运算的说明，是"比较结果永远是布尔值"的直接依据。</li>
    <li><a href="https://docs.python.org/zh-cn/3/library/operator.html">operator —— 标准运算符替代函数 · Python 官方文档（中文）</a> — 官方把每个运算符对应到同名函数的一览表，可作为"运算符有哪几类"的权威索引。</li>
    <li><a href="https://realpython.com/python-operators/">Python Operators · Real Python</a> — 权威二手教程：按算术 / 比较 / 逻辑 / 位运算等分类讲解，并给出优先级与"括号消除歧义"的实践建议。</li>
  </ol>
  <p class="callout">说明：「浮点数是二进制近似表示，因此 <em>0.1 + 0.2 == 0.3</em> 会得到 False」这一条属于工程共识，来源于通用知识整理，未逐条绑定上列来源 <strong>[unverified]</strong>；详细原理见上半场 <a href="变量与基本类型.html">变量与基本类型</a> 篇。</p>
</section>

<section>
  <h2>7 · 一句话回顾</h2>
  <p class="takeaway">运算符的规则只有两条要刻进肌肉记忆：<em>7 / 2</em> 是 3.5 不是 3，<em>"2" + "3"</em> 是 '23' 不是 5 —— 前者是除法有两种，后者是同一个符号遇上不同类型。</p>
</section>"""


# ==========================================================================
# 2. 列表
# ==========================================================================
BODY_LIST = """<section>
  <h2>1 · 一句话定义</h2>
  <p class="def">列表是把一串值按顺序装在一起、并且随时可以增删改的容器，用方括号 <em>[]</em> 表示。</p>
</section>

<section>
  <h2>2 · 个人解释</h2>
  <p>把列表想成一排按顺序编号的储物柜：左起第一个编号是 <strong>0</strong>，第二个是 1，以此类推。<em>fruits = ["苹果", "香蕉", "梨"]</em> 就是按顺序摆了三样东西。想拿第一个，写 <em>fruits[0]</em>。为什么从 0 开始而不是 1？因为方括号里的数字其实是"<strong>从开头往后偏移几位</strong>"—— 偏移 0 位就是第一个。接受这个解释，你就不会再把 0 当成"第零个"这种别扭的说法。</p>
  <p>编号还可以是负的。<em>fruits[-1]</em> 是"<strong>从末尾往前数第一位</strong>"，也就是梨；<em>fruits[-2]</em> 是香蕉。当你只关心"最后一个"而不确定列表有多长时，负号索引比先算长度方便得多。</p>
  <p>最反直觉、也最值得当场讲透的一点是<strong>可变</strong>（mutable）。上半场你已经学过"变量是名字指向值"；现在把这个原理放到列表上，就会出现一个让人吃惊的现象：<em>a = [1, 2, 3]</em> 之后写 <em>b = a</em>，再执行 <em>a.append(4)</em>，你去打印 <em>b</em>，结果也是 <em>[1, 2, 3, 4]</em>。<strong>这不是 bug</strong> —— <em>b = a</em> 并没有复制出一个新列表，它只是让 <em>b</em> 也成了同一个列表的第二个名字。想真正拿到一份独立副本，得写 <em>a.copy()</em> 或 <em>a[:]</em>。这个坑几乎每个人都会踩一次，早踩早免疫。</p>
  <p>再补一个高频易错点：<strong>切片不含结尾位置</strong>。<em>fruits[0:2]</em> 取的是编号 0 和 1 两个元素，<strong>不包含</strong>编号 2。你可以把它读成"从 0 开始，到 2 之前为止"。想取到最后一个，要么用 <em>fruits[0:3]</em>，要么干脆省略结尾写 <em>fruits[0:]</em>。</p>
</section>

<section>
  <h2>3 · 核心机制</h2>
  <ol>
    <li><strong>创建</strong>：用方括号直接写 <em>[]</em>，或把别的序列转过来 <em>list(...)</em>。<br />为什么重要：列表可以装任何类型的值，也可以混装 —— 它不挑食，所以几乎什么东西都能先装进去再说。</li>
    <li><strong>索引与切片</strong>：<em>a[0]</em> 取第一个，<em>a[-1]</em> 取最后一个；<em>a[1:3]</em> 取"从 1 到 3 之前"的一段。<br />为什么重要：这是"取出我要的那一份"的唯一手段；而"切片不含结尾"是新手第一个反复踩的坑。</li>
    <li><strong>长度与成员运算</strong>：<em>len(a)</em> 得到元素个数；<em>x in a</em> 判断某个值在不在里面。<br />为什么重要：<em>len()</em> 是防止索引越界的依据，<em>in</em> 让"在不在"变成一个可以直接用的真假值。</li>
    <li><strong>增删改</strong>：<em>append</em> 末尾加一项、<em>insert</em> 指定位置插入、<em>remove</em> 按值删、<em>pop</em> 按位置删并返回被删的那一项、<em>del a[i]</em> 按索引删。<br />为什么重要：列表是"活的"，随用随改；而这些方法<strong>改的是列表本身</strong>，不返回新列表。</li>
    <li><strong>排序</strong>：<em>a.sort()</em> 原地排序（不返回值）、<em>sorted(a)</em> 返回排好序的新列表。<br />为什么重要：这两者一个改原件、一个出副本，混用会让"我的原数据怎么悄悄变了"变成悬案。</li>
    <li><strong>可变带来的引用共享</strong>：<em>b = a</em> 是<strong>第二个名字</strong>，不是复制；要独立副本用 <em>a.copy()</em>。<br />为什么重要：这是上半场"名字指向值"在可变对象上的直接后果，也是"我明明没动 b 啊"这类问题的唯一根因。</li>
  </ol>
  <div class="mermaid-placeholder">fruits = ["苹果", "香蕉", "梨"]
fruits[0]      # '苹果'   ← 索引从 0 开始
fruits[-1]     # '梨'     ← 负数从末尾数
fruits[0:2]    # ['苹果', '香蕉']  ← 切片不含结尾位置
len(fruits)    # 3
"香蕉" in fruits   # True  ← 成员运算（in 的语义见本篇，不属运算符篇）

fruits.append("葡萄")      # 末尾加一项
fruits.insert(0, "草莓")   # 插到最前面
fruits.remove("香蕉")      # 按值删（没有这个值会抛 ValueError）
last = fruits.pop()       # 按位置删并返回被删项；不写位置默认删最后一个
del fruits[0]             # 按索引删

# 越界：第 4 格不存在，会抛 IndexError（读法见「报错怎么读」）
# fruits[99]

# 可变带来的坑 —— 上半场「名字指向值」在列表上的后果
a = [1, 2, 3]
b = a            # 不是复制！b 是同一个列表的第二个名字
a.append(4)
print(b)         # [1, 2, 3, 4]  ← b 也变了，因为它俩是同一个列表

c = a.copy()     # 想要独立副本用 copy() 或 a[:]
a.append(5)
print(c)         # [1, 2, 3, 4]  ← c 不受影响

# 原地排序 vs 返回新列表
nums = [3, 1, 2]
nums.sort()            # 原地改，返回 None
print(nums)            # [1, 2, 3]
print(sorted([3, 1, 2]))   # [1, 2, 3]，原列表不变</div>
</section>

<section>
  <h2>4 · 应用场景</h2>
  <div class="scenario">
    <h3>场景 1 · 一份会变的待办列表</h3>
    <p><span class="label">背景：</span>要按顺序记录今天要做的事，并且随时会加一条、划掉一条。</p>
    <p><span class="label">如何应用：</span>用列表存事项，新任务 <em>append</em> 到末尾；做完的用 <em>remove</em> 按内容划掉，或 <em>pop</em> 按位置取出。</p>
    <p><span class="label">结果：</span>一支随时能增删的列表；顺序天然保持，因为列表记住的正是你放进来的先后。</p>
  </div>
  <div class="scenario">
    <h3>场景 2 · 只看最近三条记录</h3>
    <p><span class="label">背景：</span>日志攒了很多条，只想快速看最后三条。</p>
    <p><span class="label">如何应用：</span>用负号切片 <em>logs[-3:]</em>，意思是"从倒数第三个开始，一直取到末尾"。</p>
    <p><span class="label">结果：</span>不必先知道总条数，也不用算编号；负号与省略结尾的写法把"取最后几条"变成一句话。</p>
  </div>
  <div class="scenario">
    <h3>场景 3 · 把成绩排名次</h3>
    <p><span class="label">背景：</span>手上有一串分数，要按从高到低排列。</p>
    <p><span class="label">如何应用：</span>用 <em>scores.sort(reverse=True)</em> 原地降序排；如果原来的顺序还要留着，就先 <em>copy()</em> 一份再排，或用 <em>sorted(scores, reverse=True)</em>。</p>
    <p><span class="label">结果：</span>得到排好序的结果，同时清楚"原件有没有被动过"——这正是 <em>sort()</em> 与 <em>sorted()</em> 的分工所在。</p>
  </div>
</section>

<section>
  <h2>5 · 边界辨析</h2>
  <h3>5.1 不是什么</h3>
  <ul>
    <li><strong>不是数组</strong>：很多语言里的数组长度固定、类型统一；Python 的列表长度可变、可以混装任何类型 —— 它更像一条能伸缩的队伍。</li>
    <li><strong>不是字典</strong>：列表按"位置编号"取，字典按"名字"取。要按"第几个"就找列表，要按"叫什么"就找 <a href="字典.html">字典</a>。</li>
    <li><strong>不负责"记录"这件事</strong>：如果每一项其实有好几个属性（姓名、分数、班级），那它应该是个 <a href="字典.html">字典</a>；多行这样的记录就交给 <a href="列表套字典.html">列表套字典 = 一张表</a>，而不是硬塞进一个列表里靠位置去记。</li>
    <li><strong>不展开遍历与推导式</strong>：<em>for</em> 循环与列表推导式属于后续课程；本篇只在代码块里给一行写法预览，不展开讲。</li>
  </ul>
  <h3>5.2 常见误解</h3>
  <ul>
    <li>「<em>a[1:3]</em> 取三个元素」—— 不是，取两个（编号 1 和 2）。切片<strong>不含结尾位置</strong>。</li>
    <li>「<em>b = a</em> 是复制了一份」—— 不是。它只是给同一个列表起了第二个名字，改一个两边都变；要复制得用 <em>copy()</em>。</li>
    <li>「<em>sort()</em> 会返回排好序的列表」—— 不会，它返回 <em>None</em>，排序是<strong>原地</strong>发生的。写 <em>a = a.sort()</em> 会让 <em>a</em> 变成 <em>None</em>。</li>
    <li>「列表可以从 1 开始编号」—— 不能。索引从 0 开始；要"从末尾数"才用负数。</li>
  </ul>
  <h3>5.3 与组内邻居的分工</h3>
  <table>
    <thead><tr><th>相邻概念</th><th>本概念负责</th><th>交给邻居</th></tr></thead>
    <tbody>
      <tr><td><a href="字典.html">字典</a></td><td>按位置编号存取、切片、增删改</td><td>按键取值、<em>get()</em> 与 <em>KeyError</em>、"这个键在不在"</td></tr>
      <tr><td><a href="列表套字典.html">列表套字典 = 一张表</a></td><td>讲"列表是行的外壳"这一半</td><td>把字典一行行装进列表、按字段取值的那套结构</td></tr>
      <tr><td><a href="运算符.html">运算符</a></td><td>用 <em>in</em> 判断值在不在列表里（成员运算归本篇）</td><td><em>+</em> 在数字与文本上的两种含义（本概念只提一句"两个列表也能用 <em>+</em> 合并"）</td></tr>
      <tr><td><a href="变量与基本类型.html">变量与基本类型</a>（上半场）</td><td>把"名字指向值"落到<strong>可变对象</strong>上（<em>b = a</em> 的坑）</td><td>变量是什么、int / float / str / bool 与类型转换</td></tr>
    </tbody>
  </table>
  <h3>5.4 适用与不适用</h3>
  <table>
    <thead><tr><th>适合用列表</th><th>应换别的结构</th></tr></thead>
    <tbody>
      <tr><td>一串同类的值，顺序重要</td><td>要按名字取（找 <a href="字典.html">字典</a>）</td></tr>
      <tr><td>顺序会变、长度会增删</td><td>每一项都有多个属性（找 <a href="列表套字典.html">列表套字典</a>）</td></tr>
      <tr><td>想取"第几个"或"一小段"</td><td>需要做分组、筛选、统计（后续课程 / pandas）</td></tr>
    </tbody>
  </table>
</section>

<section class="sources">
  <h2>6 · 来源链接</h2>
  <ol>
    <li><a href="https://docs.python.org/zh-cn/3/tutorial/datastructures.html">5. 数据结构 · Python 官方教程（中文）</a> — 官方对列表全部方法（<em>append</em> / <em>insert</em> / <em>remove</em> / <em>pop</em> / <em>sort</em> / <em>copy</em> 等）的定义与示例，并明确指出"只修改列表的方法返回 <em>None</em>，这是所有可变数据结构的设计原则"。</li>
    <li><a href="https://docs.python.org/zh-cn/3/library/stdtypes.html#sequence-types-list-tuple-range">序列类型 list / tuple / range · Python 官方文档（中文）</a> — 官方对通用序列操作的定义：索引、负索引、切片（含"切片不含结尾"的语义）、<em>len()</em> 与成员检测 <em>in</em>。</li>
    <li><a href="https://docs.python.org/zh-cn/3/library/functions.html#len">内置函数 len() · Python 官方文档（中文）</a> — 官方对 <em>len()</em> 的定义：返回容器中的项数。</li>
    <li><a href="https://realpython.com/python-list/">Python's list Data Type: A Deep Dive With Examples · Real Python</a> — 权威二手教程：系统列举列表的关键特性（有序、索引从 0 开始、可变、可混装、可嵌套），并强调"可变意味着列表不可哈希，不能当字典的键"。</li>
  </ol>
</section>

<section>
  <h2>7 · 一句话回顾</h2>
  <p class="takeaway">列表是按编号排队的一串值：编号从 0 开始，切片不含结尾，而 <em>b = a</em> 只是同一个列表多了个名字 —— 想复制就 <em>copy()</em>。</p>
</section>"""


# ==========================================================================
# 3. 字典
# ==========================================================================
BODY_DICT = """<section>
  <h2>1 · 一句话定义</h2>
  <p class="def">字典是一张「名字 → 内容」的对应表，用花括号 <em>{}</em> 写，靠键（key）直接取出对应的值（value）。</p>
</section>

<section>
  <h2>2 · 个人解释</h2>
  <p>列表像一排按编号找的储物柜，字典像一本按姓名找的通讯录。想找列表里的东西你得说"第 5 个"，想找字典里的东西你说"'小明'的电话" —— <strong>取东西的依据从"位置"换成了"名字"</strong>。这就是字典存在的全部理由：当你要按某个有意义的名字去取数据时，用位置去记既容易错、也读不懂。</p>
  <p>字典的样子是 <em>{键: 值}</em>，一个键配一个值，中间用冒号，多个键值对之间用逗号：<em>tel = {"小明": 138, "小红": 139}</em>。取值写 <em>tel["小明"]</em>，得到 138。这里有个必须知道的规矩：<strong>取一个不存在的键会直接报错</strong>（抛 <em>KeyError</em>），而不是像列表那样给你一个空值。想让"键不存在"这件事变得安全，就用 <em>tel.get("小刚")</em> —— 它取不到时给回一个默认值（不写就是 <em>None</em>），不报错。这是 <em>d[键]</em> 与 <em>d.get(键)</em> 最重要的区别。</p>
  <p>还有一个反直觉的点，几乎每个人都误解过一次：<em>'小明' in tel</em> 判断的是"<strong>字典里有没有'小明'这个<em>键</em></strong>"，<strong>不是</strong>有没有"小明"这个值。键是"找东西的名字"，值才是"内容"——<em>in</em> 只查名字那一栏。</p>
  <p>最后一条关于"键本身"的规矩：<strong>键必须是不可变的类型</strong>。字符串、数字、元组都可以当键；列表不行，因为列表能被原地修改。原因很直白：字典是靠"键的名字"来定位的，如果这个名字本身还会变，那这本通讯录就废了。至于为什么按键查找很快 —— 那涉及哈希表的实现原理，超出本篇范围，你只要先建立"按键直取、不靠从头逐个找"这一层直觉就够了。</p>
</section>

<section>
  <h2>3 · 核心机制</h2>
  <ol>
    <li><strong>创建</strong>：用花括号写键值对 <em>{键: 值, ...}</em>；空字典写 <em>{}</em>。<br />为什么重要：键值成对出现是字典的本质 —— 你永远同时拿到"名字"和"内容"两样东西。</li>
    <li><strong>按键取值</strong>：<em>d[键]</em> 取不到就抛 <em>KeyError</em>；<em>d.get(键, 默认值)</em> 取不到就给默认值。<br />为什么重要：这是"安全取值"与"直接取值"的分岔口；不确定键在不在时用 <em>get()</em>，能省掉一整类报错。</li>
    <li><strong>增 / 改 / 删</strong>：赋一个新键就是新增（<em>d["新键"] = 值</em>）；赋一个已有的键就是修改；<em>del d[键]</em> 删除整个键值对。<br />为什么重要：注意<strong>新增和修改的写法完全一样</strong> —— 字典不在乎那个键本来有没有，它只管"现在这个键对应什么值"。</li>
    <li><strong>键的规矩</strong>：键唯一、且必须是不可变类型（字符串 / 数字 / 元组可以，列表不行）。<br />为什么重要：键重复时后写的会覆盖前一个；键不可变才能被可靠地定位 —— 用列表当键会直接抛 <em>TypeError</em>。</li>
    <li><strong>成员运算与三个视图</strong>：<em>键 in d</em> 查的是<strong>键</strong>；<em>keys()</em> 看所有键、<em>values()</em> 看所有值、<em>items()</em> 看所有键值对。<br />为什么重要：把"查键"和"查值"分清，能避免"明明值在里面，为什么 <em>in</em> 说是 False"的困惑。</li>
    <li><strong>保持插入顺序</strong>：较新的 Python 里字典记住你放入键值对的先后。<br />为什么重要：打印出来是人读得懂的顺序，而不是随机乱跳 —— 调试时省心。</li>
  </ol>
  <div class="mermaid-placeholder">tel = {"小明": 138, "小红": 139}
tel["小明"]        # 138      ← 按键直接取
tel.get("小刚")     # None     ← 取不到时给默认值，不报错
tel.get("小刚", 0)  # 0        ← 也可以自己指定默认值
# tel["小刚"]      # KeyError ← 取不存在的键会抛错（读法见「报错怎么读」）

tel["小刚"] = 137   # 新增：键本来不存在
tel["小明"] = 140   # 修改：键已存在，写法完全一样
del tel["小红"]     # 删除一个键值对

"小明" in tel        # True   ← 查的是「键」，不是值
138 in tel          # False  ← 值在字典里，但 in 不查值

list(tel.keys())    # ['小明', '小刚']
list(tel.values())  # [140, 137]
list(tel.items())   # [('小明', 140), ('小刚', 137)]

# 键必须是不可变类型：
ok = {"name": "小明"}          # 字符串当键 —— 可以
# bad = {["name"]: "小明"}     # TypeError：列表不能当键

# 字典同样可变（原理见「列表」篇：名字指向值）
d2 = tel
tel["新键"] = 1
print(d2)           # d2 也变了 —— 它俩是同一个字典</div>
</section>

<section>
  <h2>4 · 应用场景</h2>
  <div class="scenario">
    <h3>场景 1 · 一本通讯录</h3>
    <p><span class="label">背景：</span>要存一批"姓名 → 电话"，并且经常按姓名直接查。</p>
    <p><span class="label">如何应用：</span>用姓名当键、电话当值：<em>tel = {"小明": 138, "小红": 139}</em>，查询写 <em>tel["小明"]</em>。</p>
    <p><span class="label">结果：</span>代码读起来就是一句人话 —— "查小明的电话"，而不是"查第 0 项的第二个字段"。</p>
  </div>
  <div class="scenario">
    <h3>场景 2 · 一组带名字的配置项</h3>
    <p><span class="label">背景：</span>程序要保存一堆设置：字体大小、主题色、是否开启提示。</p>
    <p><span class="label">如何应用：</span>用字典把它们收在一起，每个设置一个键；要用时按名字取，想改就 <em>config["font_size"] = 16</em>。</p>
    <p><span class="label">结果：</span>配置项自带名字、不用记顺序；新增一项只是多写一个键，不影响已有代码。</p>
  </div>
  <div class="scenario">
    <h3>场景 3 · 给"查不到"留一个默认值</h3>
    <p><span class="label">背景：</span>统计里想给某个尚未出现过的项加 1，直接写 <em>counts[项]</em> 会因键不存在而报错。</p>
    <p><span class="label">如何应用：</span>用 <em>counts[项] = counts.get(项, 0) + 1</em> —— <em>get()</em> 在键不存在时给出 0，再往上加 1 就完成了"首次出现即初始化为 1"。</p>
    <p><span class="label">结果：</span>把"键可能不存在"这一整类 <em>KeyError</em> 从根上消掉，统计逻辑变得短且稳。</p>
  </div>
</section>

<section>
  <h2>5 · 边界辨析</h2>
  <h3>5.1 不是什么</h3>
  <ul>
    <li><strong>不是列表</strong>：列表按位置编号取、字典按名字取。要"第几个"用 <a href="列表.html">列表</a>，要"叫什么"用字典。</li>
    <li><strong>不是"什么都能当键"</strong>：键必须是不可变类型。列表不能当键（会抛 <em>TypeError</em>）；字符串、数字、元组可以。</li>
    <li><strong>不等于"查所有值"</strong>：<em>in</em> 只查键。判断某个<strong>值</strong>在不在，得看 <em>values()</em>，这与"键在不在"是两件事。</li>
    <li><strong>不负责多行记录</strong>：字典天然表达"一条记录"（姓名 / 分数 / 班级各是一个键）；多行记录交给 <a href="列表套字典.html">列表套字典 = 一张表</a> 篇。</li>
  </ul>
  <h3>5.2 常见误解</h3>
  <ul>
    <li>「<em>d["不存在的键"]</em> 会返回空或 None」—— 不会，会抛 <em>KeyError</em>。想要"取不到给默认值"必须用 <em>get()</em>。</li>
    <li>「<em>'小明' in d</em> 是判断有没有这个值」—— 不是，判断的是有没有这个<strong>键</strong>。</li>
    <li>「键写重复了会报错」—— 不会报错，后写的会<strong>覆盖</strong>先写的。键必须唯一是"约束"，不是"报错"。</li>
    <li>「字典是乱序的」—— 较新的 Python 里字典<strong>保持插入顺序</strong>；不要再把它当作无序容器来理解。</li>
  </ul>
  <h3>5.3 与组内邻居的分工</h3>
  <table>
    <thead><tr><th>相邻概念</th><th>本概念负责</th><th>交给邻居</th></tr></thead>
    <tbody>
      <tr><td><a href="列表.html">列表</a></td><td>按键取值、<em>get()</em>、键的规矩与三个视图</td><td>索引、切片、增删方法与"<em>b = a</em> 是同一个列表"（本概念只提一句"字典同样可变"）</td></tr>
      <tr><td><a href="列表套字典.html">列表套字典 = 一张表</a></td><td>讲"一个字典 = 一条记录"这一半</td><td>把多条记录装进列表、按 <em>行 / 字段</em> 取值的那套结构</td></tr>
      <tr><td><a href="运算符.html">运算符</a></td><td>用 <em>in</em> 判断键在不在字典里（成员运算归本篇，且<strong>只查键</strong>）</td><td>算术 / 比较 / 逻辑运算符与优先级</td></tr>
      <tr><td><a href="报错怎么读.html">报错怎么读</a>（上半场）</td><td>只说明"取不存在的键会抛 <em>KeyError</em>、用 <em>get()</em> 可避免"</td><td><em>KeyError</em> 的逐行读法与五步排查动作</td></tr>
    </tbody>
  </table>
  <h3>5.4 适用与不适用</h3>
  <table>
    <thead><tr><th>适合用字典</th><th>应换别的结构</th></tr></thead>
    <tbody>
      <tr><td>按有意义的名字取数据（姓名 / 配置项 / 字段名）</td><td>只按先后顺序存取（找 <a href="列表.html">列表</a>）</td></tr>
      <tr><td>描述"一个东西的多个属性"</td><td>描述"很多个东西"（找 <a href="列表套字典.html">列表套字典</a>）</td></tr>
      <tr><td>需要"取不到就给默认值"的安全查询</td><td>要做排序、分组、聚合（后续课程 / pandas）</td></tr>
    </tbody>
  </table>
</section>

<section class="sources">
  <h2>6 · 来源链接</h2>
  <ol>
    <li><a href="https://docs.python.org/zh-cn/3/tutorial/datastructures.html#dictionaries">5.5 字典 · Python 官方教程（中文）</a> — 官方定义："字典可以看作一组键值对，键必须唯一"，并给出按键取值、<em>del</em> 删除、<em>list(d)</em> 取所有键、<em>in</em> 判断键是否存在的示例。</li>
    <li><a href="https://docs.python.org/zh-cn/3/library/stdtypes.html#mapping-types-dict">映射类型 dict · Python 官方文档（中文）</a> — 官方对 <em>dict</em> 的完整定义：键必须是可哈希（因而不可变）的对象、<em>get()</em> 的默认值行为、<em>keys()</em> / <em>values()</em> / <em>items()</em> 视图，以及"字典保持插入顺序"的说明。</li>
    <li><a href="https://docs.python.org/zh-cn/3/library/stdtypes.html">内置类型 · Python 官方文档（中文）</a> — 官方对"可哈希"这一条件的定义，是"为什么列表不能当键"的直接依据。</li>
    <li><a href="https://realpython.com/python-dicts/">Dictionaries in Python · Real Python</a> — 权威二手教程：系统讲解字典的创建、取值（含 <em>get()</em> 与 <em>KeyError</em> 的区别）、增删改与常见陷阱。</li>
  </ol>
</section>

<section>
  <h2>7 · 一句话回顾</h2>
  <p class="takeaway">字典是按键取值的对应表：取不存在的键会报错，要么先确认键存在、要么用 <em>get()</em> 给个默认值 —— 而 <em>in</em> 查的一直是键，不是值。</p>
</section>"""


# ==========================================================================
# 4. 列表套字典 = 一张表
# ==========================================================================
BODY_TABLE = """<section>
  <h2>1 · 一句话定义</h2>
  <p class="def">把"每行一条记录"的字典装进一个列表，就得到一张表：<strong>列表是行，字典是"列名 → 值"。</strong></p>
</section>

<section>
  <h2>2 · 个人解释</h2>
  <p>先看一张再普通不过的表格：一张学生成绩表，有三列（姓名、班级、分数），有两行数据。现在问一个问题 —— 在 Python 里怎么把它装起来？</p>
  <p>你可能会想到"列表套列表"：<em>[["小明", "一班", 90], ["小红", "二班", 85]]</em>。它能跑，但有个致命缺陷：<strong>列名丢了</strong>。看到 <em>row[0]</em>，你怎么知道这是"姓名"还是"班级"？全靠脑记。表格一旦长到十几列，代码就没法看了。</p>
  <p>换一个思路：<strong>一行数据，其实是一组"字段名 → 值"的对应</strong> —— 姓名字段是小明、班级字段是一班、分数字段是 90。这不正好就是<a href="字典.html">字典</a>吗？于是一行写成 <em>{"name": "小明", "class": "一班", "score": 90}</em>。再把多行按顺序放进一个<a href="列表.html">列表</a>里，整张表就是 <em>[{...}, {...}]</em> —— <strong>列表保管"有哪几行"，字典保管"每一行里每个字段叫什么"</strong>。</p>
  <p>这个结构的取值方式也很顺口：<em>rows[0]</em> 是"第 1 行"（一个字典），<em>rows[0]["name"]</em> 是"第 1 行的 name 那一格"。读起来就是"第 1 行的姓名"，和你说人话的顺序完全一致 —— 这正是它比"列表套列表"强的地方。</p>
  <p>最后一点，也是这一篇最想让你记住的：<strong>它不是某种冷门技巧，而是真实数据最常见的形状</strong>。CSV 文件读进来是这个样子，网页接口返回的 JSON 常常是这个样子，数据库查出来的结果也常被整理成这个样子。你在入门阶段学到的这个结构，后面会一直用下去。</p>
</section>

<section>
  <h2>3 · 核心机制</h2>
  <ol>
    <li><strong>为什么用字典装一行</strong>：因为字典能把"字段名"和"值"绑在一起。<br />为什么重要：换成列表，<em>row[0]</em> 是第几列全靠记忆；换成字典，<em>row["name"]</em> 自带说明 —— 这是"看得懂"和"看得懂但不敢改"的分界。</li>
    <li><strong>为什么用列表装多行</strong>：因为列表有序、可增删，天然对应"表里有很多行、行的先后有意义"。<br />为什么重要：列表负责"有哪几行、什么顺序"，字典负责"每行长什么样"，两者各管一半，互不越界。</li>
    <li><strong>取一行与取一格</strong>：<em>rows[i]</em> 取第 i 行（得到字典）；<em>rows[i]["字段"]</em> 取第 i 行某个字段的值。<br />为什么重要：这是本结构最常用的动作；先按位置找行、再按名字找字段，两层恰好把列表和字典的强项都用上了。</li>
    <li><strong>增一行 / 改一格 / 删一行</strong>：<em>rows.append({...})</em> 加一行、<em>rows[i]["字段"] = 新值</em> 改一格、<em>del rows[i]</em> 删一行。<br />为什么重要：增删行用列表的写法、改字段用字典的写法 —— 认清"哪一层用哪种写法"，就不会写错括号。</li>
    <li><strong>同一张表里键要一致</strong>：每行字典应使用同一组字段名。<br />为什么重要：这是"表"成立的前提。第一行有 <em>"score"</em>、第二行写成 <em>"points"</em>，程序读第 2 行时就会因找不到 <em>"score"</em> 而出问题。</li>
  </ol>
  <div class="mermaid-placeholder"># 一行 = 一个字典：字段名随身带着，不用记第几列
row1 = {"name": "小明", "class": "一班", "score": 90}
row2 = {"name": "小红", "class": "二班", "score": 85}

# 整张表 = 一个列表装多行
students = [row1, row2]
# 也可以直接写在一起：
students = [
    {"name": "小明", "class": "一班", "score": 90},
    {"name": "小红", "class": "二班", "score": 85},
]

students[0]              # {'name': '小明', 'class': '一班', 'score': 90}  ← 取第 1 行
students[0]["name"]      # '小明'   ← 取第 1 行的 name 格
students[1]["score"]     # 85       ← 取第 2 行的 score 格

# 增一行（用列表的写法）
students.append({"name": "小刚", "class": "一班", "score": 78})

# 改一格（用字典的写法）
students[0]["score"] = 95     # 小明这次考了 95

# 删一行
del students[1]               # 删掉第 2 行
# students.pop(1)             # 同上，且返回被删的那一行

# 取整列需要遍历（for / 列表推导式属后续课程，这里只预览一眼写法）
# names = [s["name"] for s in students]   # ['小明', '小刚']

# 每行的键必须一致，否则按字段取值时会出问题
# 第 1 行用 "score"、第 2 行写 "points"，读第 2 行就会 KeyError</div>
</section>

<section>
  <h2>4 · 应用场景</h2>
  <div class="scenario">
    <h3>场景 1 · 一张成绩表</h3>
    <p><span class="label">背景：</span>要存一个班的学生成绩，每人有姓名、班级、分数三项。</p>
    <p><span class="label">如何应用：</span>每人写成一个字典，全部放进一个列表：<em>students = [{"name": ..., "class": ..., "score": ...}, ...]</em>。</p>
    <p><span class="label">结果：</span>结构一眼看懂、字段名不会丢；要查谁的分，写 <em>students[0]["score"]</em> 就像在说"第 1 行的分数"。</p>
  </div>
  <div class="scenario">
    <h3>场景 2 · 从 CSV 文件读进来的就是它</h3>
    <p><span class="label">背景：</span>手上有一个表格文件（CSV），想读到程序里处理。</p>
    <p><span class="label">如何应用：</span>Python 标准库的 <em>csv.DictReader</em> 会把每一行都读成一个字典：<strong>表头的那一行自动变成每行的字段名</strong>，你不需要再靠"第几列"去记。</p>
    <p><span class="label">结果：</span>文件内容直接变成"列表套字典"，与你手写的成绩表结构完全一致 —— 这正是它被称为"真实数据最常见形状"的原因。</p>
  </div>
  <div class="scenario">
    <h3>场景 3 · 网页接口返回的数据</h3>
    <p><span class="label">背景：</span>调用一个网络接口，拿回一段 JSON 文本。</p>
    <p><span class="label">如何应用：</span>用标准库 <em>json</em> 解析后，得到的就是 Python 的字典与列表；一段"多条记录"的返回结果，通常正好是列表套字典。</p>
    <p><span class="label">结果：</span>你不需要另学一套语法去读接口数据 —— 本组学的两个容器，已经足够描述绝大多数返回结果。</p>
  </div>
</section>

<section>
  <h2>5 · 边界辨析</h2>
  <h3>5.1 不是什么</h3>
  <ul>
    <li><strong>不是"列表套列表"</strong>：那种写法丢掉字段名，<em>row[0]</em> 得靠记忆理解。只要每行有"多个属性"，就该用字典装行。</li>
    <li><strong>不是字典套字典</strong>：字典擅长"一个东西的多个属性"，不擅长表达"很多行、且有先后"。多行的职责属于<a href="列表.html">列表</a>。</li>
    <li><strong>不是一个数据库或 DataFrame</strong>：它只是"形状像表"。真正的筛选、分组、连接、统计能力属于后续课程（pandas / SQL）——本篇只建立结构直觉。</li>
    <li><strong>不含遍历与筛选的写法</strong>：取整列、按条件筛行都需要 <em>for</em> 或列表推导式，属后续课程；本篇只在代码块里留一行写法预览。</li>
  </ul>
  <h3>5.2 常见误解</h3>
  <ul>
    <li>「<em>rows["name"]</em> 就能取到姓名」—— 不能。得先按位置取行：<em>rows[0]["name"]</em>。括号要写两层。</li>
    <li>「每行字典的键可以随便不一样」—— 技术上能跑，但作为"一张表"必须一致，否则某一行的字段会取不到。</li>
    <li>「它就是 Excel，可以直接做透视和公式」—— 不是。它只是数据<strong>形状</strong>像表；真正的表格计算能力在 pandas / 电子表格软件里。</li>
    <li>「改了字典等于复制出了新数据」—— 不是。字典和列表都是可变的，<em>same = students</em> 只是同一个列表的第二个名字，改一处两边都变（原理见<a href="列表.html">列表</a>篇）。</li>
  </ul>
  <h3>5.3 与组内邻居的分工</h3>
  <table>
    <thead><tr><th>相邻概念</th><th>本概念负责</th><th>交给邻居</th></tr></thead>
    <tbody>
      <tr><td><a href="列表.html">列表</a></td><td>讲"列表是装行的外壳"这一半职责</td><td>索引、切片、<em>append</em> / <em>pop</em> / <em>del</em> 的完整规则与可变性陷阱</td></tr>
      <tr><td><a href="字典.html">字典</a></td><td>讲"字典是一条记录"这一半职责</td><td><em>get()</em> 与 <em>KeyError</em>、键不可变、三个视图的完整规则</td></tr>
      <tr><td><a href="运算符.html">运算符</a></td><td>只做"按行、按字段取值"这一件事</td><td>对取出来的值做算术、比较与条件组合</td></tr>
    </tbody>
  </table>
  <h3>5.4 适用与不适用</h3>
  <table>
    <thead><tr><th>适合用列表套字典</th><th>应换别的方案</th></tr></thead>
    <tbody>
      <tr><td>一批同结构的记录，每行字段有明确名字</td><td>只有一两条数据、字段很少（直接写两个变量更省事）</td></tr>
      <tr><td>要逐行读取、增删行、按字段取值</td><td>要做分组 / 排序 / 统计（后续课程 / pandas）</td></tr>
      <tr><td>承接 CSV、JSON、接口返回的数据</td><td>要做真正的表格计算与导出（电子表格 / pandas）</td></tr>
    </tbody>
  </table>
</section>

<section class="sources">
  <h2>6 · 来源链接</h2>
  <ol>
    <li><a href="https://docs.python.org/zh-cn/3/tutorial/datastructures.html">5. 数据结构 · Python 官方教程（中文）</a> — 官方对"嵌套的数据结构"的示例：列表里可以放字典等各类对象，展示"用容器装容器"表示复杂数据的标准写法。</li>
    <li><a href="https://docs.python.org/zh-cn/3/library/csv.html#csv.DictReader">csv.DictReader · Python 官方文档（中文）</a> — 官方说明：<em>DictReader</em> 把 CSV 的每一行读成一个字典，字段名默认取自第一行表头 —— 这是"列表套字典"就是表格数据常见形状的官方依据。</li>
    <li><a href="https://docs.python.org/zh-cn/3/library/json.html">json —— JSON 编码器与解码器 · Python 官方文档（中文）</a> — 官方对 JSON 与 Python 对象对应关系的说明：JSON 对象 ↔ <em>dict</em>、JSON 数组 ↔ <em>list</em>，因此一组记录解析后正是"列表套字典"。</li>
    <li><a href="https://realpython.com/python-list/">Python's list Data Type: A Deep Dive With Examples · Real Python</a> — 权威二手教程：明确指出列表可以"代表数据库中的一张表"，此时<strong>列表本身叫 table、每个元素是一行（row）</strong>，并给出由字典组成的列表实例。</li>
  </ol>
</section>

<section>
  <h2>7 · 一句话回顾</h2>
  <p class="takeaway">一张表 = 列表装行 + 字典装字段名：<em>rows[0]["name"]</em> 就是"第 1 行的姓名"—— 别用列表套列表，那样列名会丢。</p>
</section>"""


# ==========================================================================
# 生成四份材料
# ==========================================================================
MATERIALS = [
    {
        "file": "运算符.html",
        "title": "概念学习：运算符（Operators）",
        "h1": "运算符（Operators）",
        "subtitle": "算术 / 比较 / 逻辑三组运算符，以及「同一符号两种含义」 · " + footer_note(1),
        "accent": "#5f7a1f",
        "soft": "#eef3dd",
        "body": BODY_OP,
    },
    {
        "file": "列表.html",
        "title": "概念学习：列表（Lists）",
        "h1": "列表（Lists）",
        "subtitle": "按编号排队的一串值：索引从 0 开始，切片不含结尾 · " + footer_note(2),
        "accent": "#9c2a7a",
        "soft": "#f9e7f4",
        "body": BODY_LIST,
    },
    {
        "file": "字典.html",
        "title": "概念学习：字典（Dictionaries）",
        "h1": "字典（Dictionaries）",
        "subtitle": "按键取值的对应表：get() 与 KeyError 的分岔口 · " + footer_note(3),
        "accent": "#4f5f6d",
        "soft": "#e8edf1",
        "body": BODY_DICT,
    },
    {
        "file": "列表套字典.html",
        "title": "概念学习：列表套字典 = 一张表（List of Dicts）",
        "h1": "列表套字典 = 一张表（List of Dicts）",
        "subtitle": "列表装行、字典装字段 —— 真实数据最常见的形状 · " + footer_note(4),
        "accent": "#2f6f2f",
        "soft": "#e6f3e6",
        "body": BODY_TABLE,
    },
]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(GROUP_DIR, exist_ok=True)
    for m in MATERIALS:
        html = page(m["title"], TAG, m["h1"], m["subtitle"], m["body"], m["accent"], m["soft"])
        p = os.path.join(OUT_DIR, m["file"])
        io.open(p, "w", encoding="utf-8").write(html)
        print("written:", p, len(html), "chars")


if __name__ == "__main__":
    main()
