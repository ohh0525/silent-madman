# -*- coding: utf-8 -*-
"""concept-group-guide / Phase 2 + Phase 3 生成器

为概念组「Python 第 1 课 · 上手四概念」生成：
  4 份 7 段式 HTML 学习材料 -> Python基础语法课程/learning-materials/
  1 份组索引页             -> concept-group/python-lesson1-starter/index.html

复用 learning-materials/agent.html 的 CSS 结构，只改 --accent / --accent-soft。
"""
import io
import os

ROOT = r"D:\桌面\silent-madman"
OUT_DIR = os.path.join(ROOT, "Python基础语法课程", "learning-materials")
GROUP_DIR = os.path.join(ROOT, "concept-group", "python-lesson1-starter")

GROUP_NAME = "Python 第 1 课 · 上手四概念"
DATE = "2026-09-17"
SKILL_SIGN = "concept-group-guide"

# --------------------------------------------------------------------------
# CSS：逐字复制 learning-materials/agent.html 的 <style>，仅主题色变量参数化
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
    return "生成时间 " + DATE + " · 组内第 " + str(n) + " / 4"


TAG = "概念组 · " + GROUP_NAME


# ==========================================================================
# 1. 环境搭建
# ==========================================================================
BODY_ENV = """<section>
  <h2>1 · 一句话定义</h2>
  <p class="def">环境搭建就是在本机装好「解释器」和「写代码的工具」，并让一个最简单的程序真的跑起来、看到它的输出。</p>
</section>

<section>
  <h2>2 · 个人解释</h2>
  <p>把写 Python 想成做菜。解释器（interpreter）是厨房里的灶台 —— 真正把菜做熟的东西；编辑器（editor）是你切菜备料的案板 —— 你在这里写下代码。光有案板没有灶，菜做不熟；光有灶没有案板，你连菜都没地方切。Python 官网提供的是灶台，VS Code 这类工具提供的是案板。两者必须都装，而且要能接上。</p>
  <p>为什么新手会在这里卡很久？因为「装好了」和「能用」是两件事。你双击安装包一路下一步，进度条走到 100%，看起来完成了；但真正决定成败的是安装时那个小小的复选框 —— <strong>Add Python to PATH</strong>。它决定系统能不能在任意目录下找到灶台。没勾，你在命令行敲 <em>python</em> 就会得到「不是内部或外部命令」，而绝大多数人此刻会误以为「没装成功」，于是反复重装。</p>
  <p>一个虚拟场景：你在 Windows 上从 python.org 下载并安装，然后打开终端敲 <em>python --version</em>。如果屏幕上出现版本号，环境就通了；如果提示命令找不到，别急着重装 —— <strong>先去把 PATH 补上</strong>。重新运行安装程序选择「Modify」勾上那个选项，或者手动把 Python 安装目录追加进环境变量，问题通常立刻消失。这个「装完了但命令找不到」是新手第一道坎，也是本概念唯一要求你牢牢记住的排障动作。</p>
  <p>最后一个心法：搭建环境的验收标准不是「安装向导走完了」，而是「我敲一行代码，屏幕上出现了我预期的结果」。把判据放在<strong>输出</strong>上，而不是放在安装过程上，你就不会在第一步反复打转。</p>
</section>

<section>
  <h2>3 · 核心机制</h2>
  <ol>
    <li><strong>装解释器</strong>：从 python.org 获取 CPython 安装包并安装（Windows 上可用图形安装程序，也可用 Microsoft Store）。<br />为什么重要：解释器是唯一能真正执行你代码的程序，没有它后面三件事全部无从谈起。</li>
    <li><strong>选并装一个编辑器 / IDE</strong>：例如 VS Code 加装官方 Python 扩展。<br />为什么重要：记事本能写代码，但不报错、不补全、不提示类型；对初学者来说，一个会实时提示的工具能省下大量「明明写错了却看不出来」的时间。</li>
    <li><strong>让系统能找到解释器</strong>：勾选 Add Python to PATH，或使用 Windows 的 <em>py</em> 启动器；安装完成后需要<strong>重开终端</strong>才会生效。<br />为什么重要：这是「命令找不到」的唯一根因，也是这一步唯一真正容易出错的地方。</li>
    <li><strong>验证并跑通第一个程序</strong>：先用 <em>python --version</em> 确认版本号，再写一行 <em>print("Hello")</em> 并运行。<br />为什么重要：看到输出才算环境真的通了 —— 这才是本概念的完成信号，而不是安装进度条。</li>
  </ol>
  <div class="mermaid-placeholder"># 第 1 步：在「终端 / 命令行」里执行（不是写在 .py 文件里）
python --version
# 如果提示命令找不到，换这个试试：
py -3 --version

# 第 2 步：把下面这行写进 hello.py，然后运行
print("Hello, Python!")

# 第 3 步：在终端里运行这个文件
python hello.py</div>
</section>

<section>
  <h2>4 · 应用场景</h2>
  <div class="scenario">
    <h3>场景 1 · 一台全新电脑从零开始</h3>
    <p><span class="label">背景：</span>刚拿到一台没装过任何开发工具的电脑，要开始学 Python。</p>
    <p><span class="label">如何应用：</span>先装解释器（勾上 Add Python to PATH），再装 VS Code 与 Python 扩展，用 <em>python --version</em> 确认版本，最后跑通一个 <em>print</em> 文件。</p>
    <p><span class="label">结果：</span>得到一台「敲得动代码、看得见输出」的可用机器，后续所有练习都建立在它之上。</p>
  </div>
  <div class="scenario">
    <h3>场景 2 · 排掉「命令找不到」</h3>
    <p><span class="label">背景：</span>明明装完了，终端却提示 python 不是内部或外部命令。</p>
    <p><span class="label">如何应用：</span>先重开一个终端（PATH 只在终端启动时读取一次）；仍不行则重跑安装程序选 Modify 勾上 Add Python to PATH，或手动把安装目录加入环境变量。</p>
    <p><span class="label">结果：</span>把「以为装失败了」变成一次两分钟就能定位的配置问题，避免反复重装。</p>
  </div>
  <div class="scenario">
    <h3>场景 3 · 分清「编辑器」和「解释器」</h3>
    <p><span class="label">背景：</span>装了编辑器却跑不起来，或者装了 Python 却发现编辑器里没有提示。</p>
    <p><span class="label">如何应用：</span>把三者关系记住 —— 编辑器负责写，扩展负责把编辑器接到解释器上，解释器负责跑；VS Code 的 Python 扩展本身不包含解释器。</p>
    <p><span class="label">结果：</span>出问题时能立刻判断是哪一层没接上，而不是笼统地觉得「环境有问题」。</p>
  </div>
</section>

<section>
  <h2>5 · 边界辨析</h2>
  <h3>5.1 不是什么</h3>
  <ul>
    <li><strong>不是「装一个软件」那么简单</strong>：它是三件事一起配好 —— 解释器、编辑器、以及让系统找得到解释器的 PATH。少一件都会表现为「装好了但用不了」。</li>
    <li><strong>不是以「安装完成」为终点</strong>：终点是「跑通一行代码并看到输出」。以安装过程为判据，是新手在第一步反复打转的根本原因。</li>
    <li><strong>不含包管理与虚拟环境</strong>：pip、venv、多版本共存属于后续内容。本概念只要求你在遇到相关报错时<strong>能照着关键字搜</strong>，不要求讲透原理。</li>
  </ul>
  <h3>5.2 常见误解</h3>
  <ul>
    <li>「装了 Anaconda 还要再装 Python 吗」—— 不需要。Anaconda 自带解释器，重复安装反而容易造成多版本混乱。</li>
    <li>「有编辑器就够了」—— 不够。编辑器不含解释器，两者是分开安装的独立部件。</li>
    <li>「版本越新越好」—— 关键指标是<em>能跑、命令能找到</em>。版本取舍与兼容性问题属于后面的内容。</li>
  </ul>
  <h3>5.3 与组内邻居的分工</h3>
  <table>
    <thead><tr><th>相邻概念</th><th>本概念负责</th><th>交给邻居</th></tr></thead>
    <tbody>
      <tr><td><a href="notebook.html">Notebook</a></td><td>把解释器与编辑器装好、让命令可用</td><td>打开 Notebook、单元格与内核怎么用</td></tr>
      <tr><td><a href="变量与基本类型.html">变量与基本类型</a></td><td>第一个程序只写 <em>print("...")</em>，不引入变量</td><td>引入变量、赋值与四种基本类型</td></tr>
      <tr><td><a href="报错怎么读.html">报错怎么读</a></td><td>只要求「能照着关键字搜」</td><td>Traceback 四段结构与逐行读法</td></tr>
    </tbody>
  </table>
  <h3>5.4 适用与不适用</h3>
  <table>
    <thead><tr><th>适合本概念的场合</th><th>不适合、应去找别处</th></tr></thead>
    <tbody>
      <tr><td>第一次在某台机器上跑 Python</td><td>已有可用环境，只想写代码</td></tr>
      <tr><td>出现「命令找不到」「版本不对」的配置问题</td><td>运行时代码报错（找 <a href="报错怎么读.html">报错怎么读</a>）</td></tr>
      <tr><td>分不清编辑器 / 扩展 / 解释器的关系</td><td>装包、建虚拟环境（属后续课程）</td></tr>
    </tbody>
  </table>
</section>

<section class="sources">
  <h2>6 · 来源链接</h2>
  <ol>
    <li><a href="https://docs.python.org/zh-cn/3/using/windows.html">4. 在 Windows 上使用 Python · Python 官方文档（中文）</a> — 安装路径、Add Python to PATH、<em>py</em> 启动器，以及「命令找不到」的故障排查章节。</li>
    <li><a href="https://www.python.org/downloads/">Python 官方下载页 · python.org</a> — 各平台 CPython 安装包的官方入口。</li>
    <li><a href="https://docs.python.org/3/using/index.html">Python Setup and Usage · Python 官方文档</a> — 官方对「安装与使用」的总体指引，含各操作系统分支。</li>
    <li><a href="https://wiki.python.org/moin/BeginnersGuide/Download">Downloading Python · Python 官方 Wiki 初学者指南</a> — 如何用 <em>python --version</em> 判断解释器是否已安装及其版本。</li>
    <li><a href="https://code.visualstudio.com/docs/python/python-quick-start">Quick Start Guide for Python in VS Code · 微软官方文档</a> — 明确区分「编辑器 / Python 扩展 / 解释器」三者，并给出验证安装与运行第一个文件的步骤。</li>
  </ol>
</section>

<section>
  <h2>7 · 一句话回顾</h2>
  <p class="takeaway">环境搭建的完成标志不是「装完了」，而是「敲一行 print 能看到输出」；装完却提示命令找不到，八成是 PATH 没配上，重开终端再修 PATH 即可。</p>
</section>"""


# ==========================================================================
# 2. Notebook
# ==========================================================================
BODY_NB = """<section>
  <h2>1 · 一句话定义</h2>
  <p class="def">Notebook 是一个把代码、运行输出和文字笔记装进同一个文件的交互式编程环境：代码写在「单元格」里，由后台的「内核」真正执行。</p>
</section>

<section>
  <h2>2 · 个人解释</h2>
  <p>把 Notebook 想成一本会自动批改的作业本。普通的脚本文件像一整篇作文 —— 你写完全篇才交上去批；Notebook 则像一栏一栏的作业格，你写一个单元格、马上看到它的结果对不对，再写下第二个。这种「写一个、跑一个、看一个」的节奏，正是它对新手的最大价值：不必等整段代码写完，才知道自己哪里想错了。</p>
  <p>但这里有一个反直觉之处，也是新手最容易困惑的地方：<strong>代码显示在单元格里，而变量实际住在内核里</strong>。第一个单元格里你写 <em>name = "小明"</em> 并运行；第二个只写 <em>print(name)</em> 也能打印出「小明」—— 因为名字存在内核的内存中，而不是存在某个单元格的文本里。于是就有了那个经典困惑：「我上面那个单元格都删了，怎么下面还能跑？」答案是你删掉的是<em>屏幕上的代码</em>，内核里那份记忆还在。</p>
  <p>一个虚拟场景：你把第一个单元格从 <em>x = 10</em> 改成 <em>x = 20</em>，但只运行了改动后的那一个，然后回头去跑下面那个 —— 结果和上次不一样了。这不是 Notebook 出了 bug，而是你<strong>改变了执行顺序</strong>。每个单元格左侧那个 <em>In [n]</em> 里的编号，记录的就是真实的运行次序。想验证「我的代码是否真的自洽」，唯一可靠的做法是<strong>重启内核并全部运行</strong>，让整本作业从第一个单元格按顺序重做一遍。</p>
</section>

<section>
  <h2>3 · 核心机制</h2>
  <ol>
    <li><strong>单元格（cell）是执行的最小单位</strong>：按 <em>Shift+Enter</em> 运行当前单元格并跳到下一个，<em>Ctrl+Enter</em> 则原地运行不跳。<br />为什么重要：把一段大程序切成一个个单元格，出错范围就被限定在单个单元格内，「哪里错了」一眼可见。</li>
    <li><strong>每个单元格执行时被送进内核</strong>：内核（kernel）是后台真正执行代码的进程，算出的结果回送到该单元格下方显示。<br />为什么重要：理解「代码送到哪儿、结果从哪儿来」，才理解输出为什么出现在单元格下面，而不是弹出一个新窗口。</li>
    <li><strong>内核持有全部状态，且与执行顺序绑定</strong>：变量、导入的模块都活在核心里，跨单元格共享。<br />为什么重要：这正是「改了上面的单元格、下面没重跑」导致结果对不上的根因；编号 <em>In [n]</em> 就是你的运行日志。</li>
    <li><strong>重启内核 / 全部运行</strong>：重启会清空内存状态；Run All 则从第一个单元格按顺序重跑一遍。<br />为什么重要：这是检验代码是否自洽的可靠手段 —— 交付前跑一次 Run All 而不报错，才算真的能用。</li>
  </ol>
  <div class="mermaid-placeholder">In [1]: x = 10          # 运行第 1 个单元格
In [2]: print(x)        # 运行第 2 个单元格  ->  10

# 现在把第 1 个单元格改成 x = 20，只重跑它：
In [3]: x = 20

# 此时在下面任意一个单元格 print(x) 都会得到 20
# —— 你没改第 2 个单元格的代码，但结果变了，因为执行顺序变了

# 想回到干净状态：Kernel -> Restart &amp; Run All
# 保存文件（.ipynb）保存的是代码与输出，不保存内核内存</div>
</section>

<section>
  <h2>4 · 应用场景</h2>
  <div class="scenario">
    <h3>场景 1 · 跟着课程逐个单元格练</h3>
    <p><span class="label">背景：</span>零基础学第一课，每讲一个知识点就想立刻验证一下。</p>
    <p><span class="label">如何应用：</span>把每个知识点放一个单元格：一个写代码、下一个用 Markdown 写笔记，跑完立刻看到输出。</p>
    <p><span class="label">结果：</span>形成一份「代码 + 讲解 + 运行结果」三合一的课堂笔记，复习时不用重新回忆当时发生了什么。</p>
  </div>
  <div class="scenario">
    <h3>场景 2 · 改一个参数看一个结果</h3>
    <p><span class="label">背景：</span>想试着调一个数值，看看输出怎么变。</p>
    <p><span class="label">如何应用：</span>只改这个单元格里的数字，按 <em>Ctrl+Enter</em> 原地重跑，不污染其他单元格的内容。</p>
    <p><span class="label">结果：</span>「试错」的成本降到一次按键，探索过程不会被反复保存、重新运行的仪式感打断。</p>
  </div>
  <div class="scenario">
    <h3>场景 3 · 把过程和结果一起交出去</h3>
    <p><span class="label">背景：</span>要把一份分析或作业发给同学或老师看。</p>
    <p><span class="label">如何应用：</span>保存为单个 <em>.ipynb</em> 文件；对方打开后既能看到代码，也能看到每一个单元格的输出与说明。</p>
    <p><span class="label">结果：</span>一份自解释的文件，不必再附截图或另写说明；对方若要复现，<em>Run All</em> 即可。</p>
  </div>
</section>

<section>
  <h2>5 · 边界辨析</h2>
  <h3>5.1 不是什么</h3>
  <ul>
    <li><strong>不是通用编辑器 / IDE 的替代品</strong>：它擅长交互式试验与讲解，不适合写大型工程（文件组织能力弱、调试器能力有限）。写项目该用 VS Code 这类编辑器。</li>
    <li><strong>不是「跑一次就存进文件」</strong>：<em>.ipynb</em> 保存的是代码和输出，<strong>内核里的内存状态不会被保存</strong>。重开文件后要重新运行才能恢复变量。</li>
    <li><strong>不是 Python 自带的</strong>：需要单独安装（例如通过 <em>pip install jupyter</em>），这一步属于环境准备，不是 Notebook 本身的用法。</li>
  </ul>
  <h3>5.2 常见误解</h3>
  <ul>
    <li>「单元格一定从上到下按顺序执行」—— 不一定。你可以跳着跑，<em>In [n]</em> 里的编号才是真实顺序。</li>
    <li>「删掉单元格，变量就没了」—— 不对。变量活在内核里，删单元格只删屏幕上的文本，不清内存。</li>
    <li>「关掉浏览器页面就等于关掉内核」—— 不一定。内核可能还在后台运行，这也是「明明关了怎么还占着资源」的来源。</li>
  </ul>
  <h3>5.3 与组内邻居的分工</h3>
  <table>
    <thead><tr><th>相邻概念</th><th>本概念负责</th><th>交给邻居</th></tr></thead>
    <tbody>
      <tr><td><a href="环境搭建.html">环境搭建</a></td><td>不装任何东西，只讲怎么用</td><td>解释器 / 编辑器怎么装、PATH 怎么修</td></tr>
      <tr><td><a href="变量与基本类型.html">变量与基本类型</a></td><td>只讲「代码写在哪、怎么跑」</td><td>代码内容本身：变量、赋值与四种基本类型</td></tr>
      <tr><td><a href="报错怎么读.html">报错怎么读</a></td><td>只讲「输出显示在单元格下方」</td><td>输出内容什么意思、报错文字怎么逐行读</td></tr>
    </tbody>
  </table>
  <h3>5.4 适用与不适用</h3>
  <table>
    <thead><tr><th>适合用 Notebook</th><th>不适合、应换工具</th></tr></thead>
    <tbody>
      <tr><td>学习、试验、逐步验证想法</td><td>需要多文件组织的正式项目</td></tr>
      <tr><td>「代码 + 讲解 + 结果」一体的笔记</td><td>需要长时间运行的生产任务</td></tr>
      <tr><td>把过程与输出一起分享给别人</td><td>对执行顺序要求严格的批处理脚本</td></tr>
    </tbody>
  </table>
</section>

<section class="sources">
  <h2>6 · 来源链接</h2>
  <ol>
    <li><a href="https://jupyter-notebook.readthedocs.io/">Jupyter Notebook Documentation · 官方文档首页</a> — 官方对「计算型笔记本」的定义：把代码、文字说明、数据与可视化放进同一份可分享文档。</li>
    <li><a href="https://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Running%20Code.html">Running Code · Jupyter Notebook 官方文档</a> — 官方对单元格运行快捷键、内核（kernel）是独立进程、可中断与重启、输出按 <em>stdout/stderr</em> 显示的说明。</li>
    <li><a href="https://realpython.com/jupyter-notebook-introduction/">Jupyter Notebook: An Introduction · Real Python</a> — 权威二手教程：单元格默认是代码、变量可在单元格之间共享、<em>In [ ]</em> 中的数字表示单元格被运行的顺序。</li>
    <li><a href="https://testnb.readthedocs.io/_/downloads/en/stable/pdf/">Jupyter Notebook Documentation（PDF 版）· 官方文档镜像</a> — 官方文档的 PDF 呈现，含四种单元格类型（code / markdown / raw / heading）与基本工作流。</li>
  </ol>
</section>

<section>
  <h2>7 · 一句话回顾</h2>
  <p class="takeaway">Notebook 的关键只有一句：代码在单元格里，状态在内核里，两者不是一回事 —— 所以「删了单元格变量还在」很正常，交付前用「重启内核 + 全部运行」才是干净起点。</p>
</section>"""


# ==========================================================================
# 3. 变量与基本类型
# ==========================================================================
BODY_VAR = """<section>
  <h2>1 · 一句话定义</h2>
  <p class="def">变量就是一个指向某个值的名字；基本类型则是把值分成整数 int、小数 float、文本 str、真假 bool 这四类。</p>
</section>

<section>
  <h2>2 · 个人解释</h2>
  <p>把变量想成一张贴纸标签。你有一个装着 18 的盒子，在盒子上贴一张写着 <em>age</em> 的标签 —— 这就是 <em>age = 18</em>。之后你一提 <em>age</em>，Python 就顺着标签去取那个值。这里最要紧的一点是：<strong>标签不是盒子本身</strong>。同一张标签可以撕下来贴到另一个盒子上（<em>age = 19</em>），原来那个 18 并没有被修改，只是暂时没有名字指着它了。</p>
  <p>为什么强调这一点？因为它解释了初学者最困惑的现象之一：<em>a = 1</em> 之后写 <em>b = a</em>，再写 <em>a = 2</em>，为什么 <em>b</em> 还是 1？因为第二句只是让 <em>b</em> 也指向了那个 1，第三句是把 <em>a</em> 这张标签挪开了，跟 <em>b</em> 没关系。把变量理解成「名字指向值」而不是「盒子装值」，这类问题从此不再需要死记。</p>
  <p>一个虚拟场景：你写下 <em>price = 19.9</em> 和 <em>count = 3</em>，然后算 <em>price * count</em>，屏幕却给出 <em>59.699999999999996</em>。这不是 Python 算错，而是<strong>小数在计算机里只能用二进制近似表示</strong> —— 19.9 存进去的那一刻就已经不是精确的 19.9。理解这一点，你既不会被浮点数的「尾巴」吓到，也会知道涉及金额的计算需要专门的处理方式，而不是直接比较是否相等。</p>
</section>

<section>
  <h2>3 · 核心机制</h2>
  <ol>
    <li><strong>赋值 = 让一个名字指向一个值</strong>：<em>name = "小明"</em>。等号左边是名字，右边是值。<br />为什么重要：这是「给数据起名」的唯一动作，后面所有复用、计算、传递都建立在它之上。</li>
    <li><strong>值自带类型，类型跟着值走</strong>：写 <em>18</em> 是 int，写 <em>18.0</em> 是 float，写 <em>"18"</em> 是 str，写 <em>True</em> 是 bool。<br />为什么重要：类型决定这个值能参与什么运算 —— <em>"2" + 2</em> 会报错，正是因为它俩类型不同。</li>
    <li><strong>用 <em>type()</em> 查看类型</strong>：不确定就查，不要猜。<br />为什么重要：初学者相当一部分报错，根源都是「我以为它是数字，其实它是文本」。</li>
    <li><strong>类型转换：<em>int()</em> / <em>float()</em> / <em>str()</em></strong>：把值从一类变成另一类。<br />为什么重要：<em>input()</em> 拿回来的<strong>永远是文本</strong>，想拿它做算术，必须先显式转成数字。</li>
  </ol>
  <div class="mermaid-placeholder">age = 18          # int   整数
price = 19.9      # float 小数
name = "小明"      # str   文本（引号包起来的都是文本）
is_ok = True      # bool  真假，只有 True / False 两个值

print(type(age))    # &lt;class 'int'&gt;
print(type(name))   # &lt;class 'str'&gt;

# 类型不匹配时会报错：下面是初学者最经典的一种
# print("年龄：" + 18)          # TypeError
print("年龄：" + str(18))       # 先用 str() 转成文本，才能拼

n = int("42") + 1  # 文本 "42" -> 整数 42，才能做加法
print(n)           # 43</div>
</section>

<section>
  <h2>4 · 应用场景</h2>
  <div class="scenario">
    <h3>场景 1 · 记住用户的输入并计算</h3>
    <p><span class="label">背景：</span>要做一个小程序：问用户年龄，然后算出他明年几岁。</p>
    <p><span class="label">如何应用：</span>用 <em>input()</em> 取回输入（是文本），先 <em>int()</em> 转成整数存进变量，再 <em>+ 1</em> 输出。</p>
    <p><span class="label">结果：</span>一个真正能和人交互的小程序；同时把「输入永远是文本」这个坑一次性踩明白。</p>
  </div>
  <div class="scenario">
    <h3>场景 2 · 用真假值描述状态</h3>
    <p><span class="label">背景：</span>需要记录「是否已完成」「是否登录」这类只有两种状态的信息。</p>
    <p><span class="label">如何应用：</span>用 bool 变量存 <em>True</em> / <em>False</em>，注意区分<em>赋值用的 =</em> 与 <em>比较用的 ==</em>，别把状态和判断写混。</p>
    <p><span class="label">结果：</span>程序能表达「条件」而不只是「数值」，为后面的判断与循环打好底子。</p>
  </div>
  <div class="scenario">
    <h3>场景 3 · 看清小数的误差</h3>
    <p><span class="label">背景：</span>用 float 做金额或科学计算，发现结果多出一串意料之外的小数位。</p>
    <p><span class="label">如何应用：</span>理解 float 是二进制近似表示；需要精确比较时用容差判断，或改用专门的十进制处理方式，不做 <em>==</em> 直接比。</p>
    <p><span class="label">结果：</span>不再把浮点误差误判成「Python 算错了」，也避免写出「永远不相等」的比较条件。</p>
  </div>
</section>

<section>
  <h2>5 · 边界辨析</h2>
  <h3>5.1 不是什么</h3>
  <ul>
    <li><strong>变量不是盒子、不是容器</strong>：它是<em>名字指向值</em>。这一点直接决定了 <em>b = a</em> 的语义 —— 两个名字指向同一个值，而不是复制出一个盒子。</li>
    <li><strong>不是「先声明类型再使用」</strong>：Python 不需要提前声明变量类型，类型跟着值走，同一个名字可以先后指向不同类型的值。</li>
    <li><strong>不是只有这四种类型</strong>：int / float / str / bool 是本课要求认识的四种基本类型；列表、字典等容器类型属于后续课程，本篇不展开。</li>
  </ul>
  <h3>5.2 常见误解</h3>
  <ul>
    <li>「<em>1</em> 和 <em>"1"</em> 是一回事」—— 不是。前者是数字可以参与运算，后者是文本，只能拼接，混用就会触发类型错误。</li>
    <li>「变量名随便起」—— 有规则：由字母、数字、下划线组成，不能以数字开头，不能使用关键字，且区分大小写。</li>
    <li>「浮点数可以放心用 == 比较」—— 不建议。<em>0.1 + 0.2 == 0.3</em> 在 Python 里结果是 False。</li>
  </ul>
  <h3>5.3 与组内邻居的分工</h3>
  <table>
    <thead><tr><th>相邻概念</th><th>本概念负责</th><th>交给邻居</th></tr></thead>
    <tbody>
      <tr><td><a href="报错怎么读.html">报错怎么读</a></td><td>只留一句「类型不匹配会抛出 TypeError」</td><td>TypeError 的完整排查步骤与逐行读法</td></tr>
      <tr><td><a href="环境搭建.html">环境搭建</a></td><td>开始引入赋值与变量</td><td>第一个程序只用 <em>print("...")</em>，不引入变量</td></tr>
      <tr><td><a href="notebook.html">Notebook</a></td><td>讲代码内容本身</td><td>代码写在哪、怎么运行、内核状态怎么管理</td></tr>
    </tbody>
  </table>
  <h3>5.4 适用与不适用</h3>
  <table>
    <thead><tr><th>本概念能解决</th><th>要找别处</th></tr></thead>
    <tbody>
      <tr><td>给数据起名、做简单计算</td><td>字符串的完整方法清单（后续「字符串专题」）</td></tr>
      <tr><td>判断一个值是什么类型、如何转换</td><td>类型错误的具体排查（找 <a href="报错怎么读.html">报错怎么读</a>）</td></tr>
      <tr><td>理解「名字指向值」带来的现象</td><td>列表 / 字典 / 元组等容器类型（后续课程）</td></tr>
    </tbody>
  </table>
</section>

<section class="sources">
  <h2>6 · 来源链接</h2>
  <ol>
    <li><a href="https://docs.python.org/zh-cn/3/library/stdtypes.html">内置类型 · Python 官方文档（中文）</a> — 官方对数字类型（int / float / complex）、布尔类型是整数子类型、以及真值检测与比较运算的说明。</li>
    <li><a href="https://docs.python.org/3/library/functions.html">Built-in Functions · Python 官方文档</a> — <em>type()</em>、<em>int()</em>、<em>float()</em>、<em>str()</em> 等内置函数的官方定义，对应本篇的类型查看与转换。</li>
    <li><a href="https://docs.python.org/3/reference/lexical_analysis.html#identifiers">Lexical analysis — Identifiers · Python 官方文档</a> — 变量命名规则的官方依据：字母 / 数字 / 下划线，不能以数字开头，区分大小写。</li>
    <li><a href="https://www.cs.toronto.edu/~david/course-notes/csc110-111/A-python-builtins/02-types.html">A.2 Python Built-In Data Types Reference · 多伦多大学 CSC110/111 课程笔记</a> — 权威教学材料：int / float / bool 的行为与 <em>int()</em> 截断、<em>float(x)</em> 转换等示例。</li>
  </ol>
  <p class="callout">说明：关于浮点数为二进制近似表示、以及「不建议用 == 直接比较浮点数」的表述，属于工程共识，来源于通用知识整理，未逐条绑定上列来源 <strong>[unverified]</strong>。</p>
</section>

<section>
  <h2>7 · 一句话回顾</h2>
  <p class="takeaway">变量是贴在值上的名字，不是装值的盒子；不确定类型就 <em>type()</em> 一下 —— 把文本当数字用，是初学者最常见的一类错误。</p>
</section>"""


# ==========================================================================
# 4. 报错怎么读
# ==========================================================================
BODY_ERR = """<section>
  <h2>1 · 一句话定义</h2>
  <p class="def">读报错，就是看懂 Python 抛出的 Traceback 的结构 —— 先看最后一行知道「错在哪一类」，再顺着文件与行号回到出事的那一行。</p>
</section>

<section>
  <h2>2 · 个人解释</h2>
  <p>报错信息不是判决书，而是一张体检报告。它从下往上写：<strong>最后一行是「病名」，再往上两行是「病灶在哪儿」</strong>。新手常被一大段英文吓住，习惯从第一行开始逐字读，读到一半就放弃了；正确的姿势恰恰相反 —— <em>倒着读</em>。先看最后一行，你立刻就知道是 TypeError 还是 NameError，十秒之内定位到大类。</p>
  <p>为什么它长得这么啰嗦？因为 Python 想把话说全：它要告诉你「是哪个文件、第几行、哪个函数里出的问题」，还要把出事那行代码原样抄一遍，并用一个小箭头指出真正出问题的位置。这些信息对新手像是噪音，对熟练的人却是坐标系 —— 有了它，你不必猜，也不必把整段代码从头到尾重看一遍。</p>
  <p>一个虚拟场景：你写下 <em>print("我的年龄是" + 18)</em>，屏幕弹出一段红字。看最后一行：<em>TypeError: can only concatenate str (not "int") to str</em> —— 意思是「加号只能用文本来拼接文本，你却塞了个整数进来」。再看倒数第二行，它直接把你写的那句抄了出来，并用箭头指向那个加号。修法因此非常清楚：<em>print("我的年龄是" + str(18))</em>。整个过程不需要搜索，也不需要猜。</p>
  <p>最后一点心法：<strong>报错是信息，不是失败</strong>。它出现的那一刻，正是程序在替你指出「这里你以为的和实际的不一致」。能读懂它的人，调试速度是别人的数倍。</p>
</section>

<section>
  <h2>3 · 核心机制</h2>
  <p>Python 的报错信息称为 Traceback（堆栈回溯）。它由四段构成，认识这四段，就等于拿到了阅读顺序。</p>
  <div class="mermaid-placeholder">Traceback (most recent call last):                    &lt;- ① 头部：固定开场
  File "demo.py", line 2, in &lt;module&gt;                  &lt;- ② 位置：哪个文件 / 第几行 / 在哪个函数里
    print("我的年龄是" + 18)                            &lt;- ③ 代码行：把出事的这行抄给你看
          ~~~~~~~~~~~~~^~~~                            &lt;- ③ 箭头：指向真正出问题的位置
TypeError: can only concatenate str (not "int") to str &lt;- ④ 类型 + 原因：整份报告的病名</div>
  <p>有了结构，再看排查动作。下面五步是固定套路，熟练之后大约十秒走完：</p>
  <ol>
    <li><strong>看最后一行</strong> —— 确定错误类型，以及它自带的原因说明。</li>
    <li><strong>看倒数第二、三行</strong> —— 确认是哪个文件的第几行出了问题。</li>
    <li><strong>回到代码里那一行</strong> —— 只看这一行，尤其只看操作符（<em>+</em>、<em>[]</em>、<em>(</em>）的左右两边。</li>
    <li><strong>问三个问题</strong> —— 这个名字我定义过吗？这两个东西的类型对吗？它的值真的是我以为的那个吗？</li>
    <li><strong>只改一处，再跑一次</strong> —— 一次改五处，你永远不会知道是哪一处修好的。</li>
  </ol>
  <p>下表列出入门阶段最常见的五类错误。它们覆盖了绝大多数「新手撞墙」的场景：</p>
  <table>
    <thead><tr><th>错误类型</th><th>你看到的关键词</th><th>真实含义</th><th>修法方向</th></tr></thead>
    <tbody>
      <tr><td>NameError</td><td>name 'x' is not defined</td><td>这个名字当前不存在</td><td>检查拼写 / 是否漏了赋值 / 是否在内核重启后忘了重跑定义那格</td></tr>
      <tr><td>TypeError</td><td>can only concatenate str (not "int") to str</td><td>参与运算的两个东西类型不匹配</td><td>用 <em>str()</em> / <em>int()</em> 显式转换后再运算</td></tr>
      <tr><td>ValueError</td><td>invalid literal for int() with base 10: 'abc'</td><td>类型对，但那个值根本转不过去</td><td>先校验输入，再转换</td></tr>
      <tr><td>KeyError</td><td>'age'</td><td>字典里没有这个键</td><td>先判断键是否存在，再取值</td></tr>
      <tr><td>FileNotFoundError</td><td>[Errno 2] No such file or directory: 'data.txt'</td><td>按这个路径找不到文件</td><td>检查路径、当前工作目录与文件名拼写</td></tr>
    </tbody>
  </table>
  <p>最后，记住几句高频英文，读报错的速度会立刻上一个台阶：</p>
  <table>
    <thead><tr><th>报错里的英文</th><th>中文意思</th></tr></thead>
    <tbody>
      <tr><td>... is not defined</td><td>这个名字没有定义（写错或没赋值）</td></tr>
      <tr><td>can only concatenate str ... to str</td><td>只能用文本来拼接文本</td></tr>
      <tr><td>invalid literal for int()</td><td>这个字符串没法转成整数</td></tr>
      <tr><td>No such file or directory</td><td>没有这个文件或目录</td></tr>
      <tr><td>expected an indented block</td><td>这里应该有缩进，但没有</td></tr>
      <tr><td>takes N positional arguments but M were given</td><td>参数个数不对</td></tr>
    </tbody>
  </table>
</section>

<section>
  <h2>4 · 应用场景</h2>
  <div class="scenario">
    <h3>场景 1 · 名字写错或没赋值</h3>
    <p><span class="label">背景：</span>想打印一个变量，屏幕上却出现 <em>NameError: name 'scoer' is not defined</em>。</p>
    <p><span class="label">如何应用：</span>看最后一行拿到「名字不存在」，再看倒数第二行确认行号，回去核对拼写 —— 通常是 <em>score</em> 拼成了 <em>scoer</em>，或者赋值那格在重启内核后忘了重跑。</p>
    <p><span class="label">结果：</span>把一个看起来吓人的红字，降解成一次拼写检查。</p>
  </div>
  <div class="scenario">
    <h3>场景 2 · 把输入直接当数字算</h3>
    <p><span class="label">背景：</span>用 <em>input()</em> 取回年龄后直接加 1，结果报错。</p>
    <p><span class="label">如何应用：</span>看最后一行，若关键词是 <em>invalid literal for int()</em>（ValueError），说明输进来的文本根本不像数字；若是 <em>can only concatenate str</em>（TypeError），说明你压根没转换。</p>
    <p><span class="label">结果：</span>能一眼分辨「值不合法」和「类型不对」这两种截然不同的毛病，修法不会用错。</p>
  </div>
  <div class="scenario">
    <h3>场景 3 · 读文件时路径不对</h3>
    <p><span class="label">背景：</span>程序要打开一个数据文件，直接抛 <em>FileNotFoundError: [Errno 2] No such file or directory: 'data.txt'</em>。</p>
    <p><span class="label">如何应用：</span>最后一行已经给出了它实际在找的完整文件名与路径 —— 对照实际文件位置，多半是路径不对、或运行目录不是你以为的那个。</p>
    <p><span class="label">结果：</span>不再怀疑「文件明明在啊」，而是直接拿报错给出的路径与实际路径做比对。</p>
  </div>
</section>

<section>
  <h2>5 · 边界辨析</h2>
  <h3>5.1 不是什么</h3>
  <ul>
    <li><strong>不是「程序坏了」</strong>：报错是程序在告诉你「这里你以为的和实际的不一致」。它是信息，不是失败，也不是判你代码死刑。</li>
    <li><strong>不是「要从第一行开始读」</strong>：要从<em>最后一行</em>开始读。从上往下读，等于把结论放在最后才看到。</li>
    <li><strong>不是一份错误类型大全</strong>：本篇教的是<em>读的方法</em>（四段结构 + 五步动作），不是穷举所有异常。遇到清单之外的类型，方法依然适用。</li>
  </ul>
  <h3>5.2 常见误解</h3>
  <ul>
    <li>「报错了就是白写了」—— 恰恰相反。能读懂报错的人，定位问题的速度是别人的数倍，这是投入产出比最高的一项基本功。</li>
    <li>「搜报错要把整段粘进去」—— 不必。粘<em>最后一行</em>并去掉你自己起的变量名，更容易搜到同款问题。</li>
    <li>「编辑器有红波浪线，就不用管运行时报错了」—— 红波浪线是静态检查，只能发现一部分问题；运行时错误只有真的跑起来才会暴露。</li>
  </ul>
  <h3>5.3 与组内邻居的分工</h3>
  <table>
    <thead><tr><th>相邻概念</th><th>本概念负责</th><th>交给邻居</th></tr></thead>
    <tbody>
      <tr><td><a href="变量与基本类型.html">变量与基本类型</a></td><td>完整讲 TypeError 等运行时报错的排查步骤</td><td>只留一句「类型不匹配会抛出 TypeError」</td></tr>
      <tr><td><a href="环境搭建.html">环境搭建</a></td><td>只讲代码运行时抛出的报错</td><td>安装失败、「命令找不到」这类环境问题</td></tr>
      <tr><td><a href="notebook.html">Notebook</a></td><td>讲报错内容怎么读</td><td>只讲「输出显示在单元格下方」这一现象</td></tr>
    </tbody>
  </table>
  <p class="callout"><strong>与既有讲义的边界</strong>：本篇定位为<strong>自学速查卡</strong>（结构 + 速查表），不复刻课堂练习。课堂用讲义（含教学法、练习与错误记录表）见 <em>Python基础语法课程/Python基础语法讲义（补充·报错怎么读）.docx</em>。</p>
  <h3>5.4 适用与不适用</h3>
  <table>
    <thead><tr><th>本概念能解决</th><th>要找别处</th></tr></thead>
    <tbody>
      <tr><td>运行时抛出的报错，如何定位到行</td><td>每种错误背后的类型系统原理（找 <a href="变量与基本类型.html">变量与基本类型</a>）</td></tr>
      <tr><td>看懂 Traceback 四段结构与高频英文</td><td>断点调试器、pdb 等「调」的工具（本篇只讲「读」，不讲「调」）</td></tr>
      <tr><td>快速判断错误大类与修法方向</td><td>安装失败类问题（找 <a href="环境搭建.html">环境搭建</a>）</td></tr>
    </tbody>
  </table>
</section>

<section class="sources">
  <h2>6 · 来源链接</h2>
  <ol>
    <li><a href="https://docs.python.org/zh-cn/3/tutorial/errors.html">8. 错误和异常 · Python 官方教程（中文）</a> — 官方对语法错误与异常的区分、Traceback 的「最后一行说明发生了什么、前段展示堆栈回溯」的权威表述，并给出 TypeError / NameError / ZeroDivisionError 的原始报错样例。</li>
    <li><a href="https://docs.python.org/zh-cn/3/library/exceptions.html">内置异常 · Python 官方文档（中文）</a> — 官方对异常层级与本篇五类错误（TypeError / NameError / ValueError / KeyError / FileNotFoundError）的定义，是速查表的直接依据。</li>
    <li><a href="https://docs.python.org/zh-cn/3.9/library/traceback.html">traceback —— 打印或读取栈回溯信息 · Python 官方文档（中文）</a> — 官方对 Traceback 的构造与打印方式的说明，佐证「四段结构」并非民间说法。</li>
    <li><a href="https://wiki.python.org/moin/HandlingExceptions.html">Handling Exceptions · Python 官方 Wiki</a> — 官方 Wiki 对异常处理与 <em>sys.exc_info()</em> 的说明，并指向内置异常清单页。</li>
  </ol>
</section>

<section>
  <h2>7 · 一句话回顾</h2>
  <p class="takeaway">报错要倒着读：最后一行告诉你「错在哪一类」，往上两行告诉你「错在哪一行」，然后只盯那一行 —— 一次只改一个地方，再跑一次。</p>
</section>"""


# ==========================================================================
# 生成四份材料
# ==========================================================================
MATERIALS = [
    {
        "file": "环境搭建.html",
        "title": "概念学习：环境搭建（Environment Setup）",
        "h1": "环境搭建（Environment Setup）",
        "subtitle": "装好解释器与编辑器，让第一个程序真的跑起来 · " + footer_note(1),
        "accent": "#2e7d4f",
        "soft": "#e6f4ea",
        "body": BODY_ENV,
    },
    {
        "file": "notebook.html",
        "title": "概念学习：Notebook（Jupyter Notebook）",
        "h1": "Notebook（Jupyter Notebook）",
        "subtitle": "代码写在单元格里，状态活在内核里 · " + footer_note(2),
        "accent": "#3a4fa8",
        "soft": "#e9ecfa",
        "body": BODY_NB,
    },
    {
        "file": "变量与基本类型.html",
        "title": "概念学习：变量与基本类型（Variables & Basic Types）",
        "h1": "变量与基本类型（Variables &amp; Basic Types）",
        "subtitle": "给数据起名，并认识整数 / 小数 / 文本 / 真假四类值 · " + footer_note(3),
        "accent": "#8a6a00",
        "soft": "#f7f1de",
        "body": BODY_VAR,
    },
    {
        "file": "报错怎么读.html",
        "title": "概念学习：报错怎么读（Reading Tracebacks）",
        "h1": "报错怎么读（Reading Tracebacks）",
        "subtitle": "看懂 Traceback 的四段结构，从最后一行定位错误 · " + footer_note(4),
        "accent": "#b02a2a",
        "soft": "#fbeaea",
        "body": BODY_ERR,
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
