# -*- coding: utf-8 -*-
"""
生成 learning-materials 候选：清洁工也会被污染（Contagious Pollution）

来源：arXiv:2611.00518v1（cs.AI / cs.CL，v1 2026-10-31 01:13:55 UTC）
产出：output/pending-review/contagious-pollution.html（草稿，不入库）
主题色：#0f4c5c（深石油蓝）—— 与既有 28 个 --accent 均不撞色
"""
import os

ACCENT = "#0f4c5c"
ACCENT_SOFT = "#e9f2f4"

HEAD = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>概念学习：清洁工也会被污染——清洗上下文的那只手，自己也逃不过被读到的东西改变（Contagious Pollution）</title>
<style>
  :root {
    --bg: #fafaf7;
    --panel: #ffffff;
    --ink: #1f2328;
    --ink-soft: #57606a;
    --accent: ACCENT;
    --accent-soft: ACCENTSOFT;
    --line: #e5e2dc;
    --code-bg: #eef2f4;
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
    padding-left: 10px;
  }
  h3 { font-size: 15px; margin: 18px 0 8px; color: var(--ink); }
  p, li { font-size: 15px; }
  code {
    background: var(--code-bg);
    padding: 1px 5px;
    border-radius: 4px;
    font-size: 13px;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
    margin: 10px 0;
  }
  th, td {
    border: 1px solid var(--line);
    padding: 8px 10px;
    text-align: left;
    vertical-align: top;
  }
  th { background: var(--accent-soft); color: var(--accent); }
  .def {
    background: var(--accent-soft);
    border-radius: 8px;
    padding: 16px 20px;
    font-size: 17px;
    font-weight: 500;
  }
  .warn {
    background: #fdf6ec;
    border: 1px solid #ecd9b5;
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 14px;
    margin: 10px 0;
  }
  .takeaway {
    background: var(--code-bg);
    border-radius: 8px;
    padding: 14px 18px;
    font-size: 14px;
  }
  pre {
    background: var(--code-bg);
    border-radius: 8px;
    padding: 14px 18px;
    overflow-x: auto;
    font-size: 13px;
    line-height: 1.6;
  }
  blockquote {
    margin: 10px 0;
    padding: 8px 16px;
    border-left: 3px solid var(--accent);
    color: var(--ink-soft);
    font-size: 14px;
  }
  ol li { margin-bottom: 10px; }
  footer {
    margin-top: 32px;
    text-align: center;
    color: var(--ink-soft);
    font-size: 13px;
  }
</style>
</head>
<body>
<div class="wrap">
'''

COVER = '''
<header class="cover">
  <span class="tag">概念学习 · 清洁工也会被污染（Contagious Pollution · 一只被它读的东西改变的读手 · 一条结构隔离铁律）</span>
  <h1>清洁工也会被污染：清洗上下文的那只手，自己也逃不过被读到的东西改变</h1>
  <p class="subtitle">Contagious Pollution —— 让清洗器一边看着旧输出一边归纳任务规格，<strong>80 / 53 / 32 掉到 40 / 11 / 8</strong>，多格<strong>低于完全不干预</strong> · 草稿 2026-11-09 · 落 <code>output/pending-review/</code> · 核查通过后目标名 <code>learning-materials/contagious-pollution.html</code></p>
</header>
'''

WARN = '''
<p class="warn"><strong>必须与结论一起读的证据等级（第一屏）：</strong>① 承重来源是<strong>预印本 arXiv:2611.00518v1，未经同行评审</strong>，单团队单篇；一手全文已抓取（<code>arxiv.org/html/2611.00518v1</code>），但<strong>无独立复现</strong>。② Lost in Conversation 回放的是<strong>难度筛选后的实例</strong> —— 测的是「从固定污染历史中恢复」，不是生产对话的在线表现。③ WildChat 的偏好数字<strong>依赖单一 GPT-5-mini judge</strong>：论文自己报告<strong>另外三个 judge 在同一批响应上偏好 AO</strong>、GPT-5 自评时 AC3 未胜出 ⇒ 偏好侧结论只当信号。④ 在<strong>完全模拟的指涉性基准</strong>（tau2-bench / CollabLLM）上，<strong>没有任何 AC3 算子胜过 full context</strong>（tau2 上差 7–12 pp，不显著）⇒ AC3 在那里证明的是「不崩塌」，不是「更好」。⑤ <strong>math 任务上的增益不可信</strong>：47% 的分析器输出含答案（泄漏），去泄漏后配对增益 <strong>−2.6 pp</strong>（p=0.815）；code / database 泄漏率 0–1%，增益在这两格成立（<strong>+30.2 / +26.0 pp</strong>）。⑥ 多数单元格<strong>单次试验</strong>，复现仅变动采样温度。⑦ 成本：每个被分析轮次<strong>多 2–3 次 LLM 调用</strong>。⑧ 本页是<strong>草稿</strong>，落在 <code>output/pending-review/</code>，<strong>未写入 <code>learning-materials/</code></strong>（受 README 人工核查承诺约束）。</p>
'''

S1 = '''
<section>
  <h2>1 · 一句话定义</h2>
  <p class="def">要洗掉模型自己先前的输出时，<strong>执行「判断哪些该洗」的那个读手，会被它读到的东西污染</strong> —— 让它一边看着旧输出一边归纳任务，判断会跟着一起歪；而<strong>命令它「忽略这些内容」不能修复</strong>，唯一可靠的做法是<strong>结构上不给它看</strong>。</p>
  <p>最短的写法：<strong>「污染会传染 —— 读过污染的人，自己也会被改变。」</strong>清洗不是安全动作；清洗是一道新的推理，而它的输入正是污染源。</p>
</section>
'''

S2 = '''
<section>
  <h2>2 · 个人解释：化验员该穿防护服，还是该被叮嘱「小心点」</h2>
  <p>想象一间化验室要处理一批<strong>已知被污染的样本</strong>。有三种安排：</p>
  <p><strong>安排 A —— 原样处理</strong>（什么都不洗）：化验员直接上手。样本里的东西会影响他对整份病例的判断 —— 这就是「上下文污染」：模型自己早先的回答留在窗口里，把后面的轮次往它先前错读的方向带。用户明明已经纠正了，模型还在沿着旧理解走。</p>
  <p><strong>安排 B —— 把样本全扔了</strong>（最粗暴的洗法）：干净是真干净，但化验单、病人主诉之外的<strong>所有中间结果</strong> —— 上一轮已经做出来的诊断、已经查到的指标 —— 也一起进了垃圾桶。下一个化验员只能从头再查一遍。这在多轮对话里就是「丢弃全部助手消息」：它确实消除了污染，但在<strong>后续轮次会引用前面结果</strong>的对话里，agent 会反复重查直到把步数预算烧光 —— 有状态工具调用的基准上，<strong>全线跌到 0%</strong>。</p>
  <p><strong>安排 C —— 派一位化验员去读样本、写一份报告</strong>（本文的方法 AC3）：由一个<strong>单独的分析器</strong>来判断「任务到底是什么、之前做得对不对」。现在关键的分岔来了 —— <strong>这位化验员怎么防自己被样本污染？</strong></p>
  <ul>
    <li><strong>做法一：叮嘱他「小心，别被样本影响」。</strong>这相当于提示词层隔离 —— 在 prompt 里写「只依据用户陈述的需求判断」。论文实测：<strong>没用，差距没有闭合。</strong></li>
    <li><strong>做法二：给他穿防护服 —— 把样本从他的输入里拿掉。</strong>任务规格只从<strong>用户侧消息</strong>归纳，助手轮次<strong>结构性地不进入他的视野</strong>；等规格立住了，再带着这个规格去审助手的工作。</li>
  </ul>
  <p>三种做法放在一起量，差距大得吓人。同样是「读一遍、判一遍」，<strong>看不见污染的版本（穿了防护服）80 / 53 / 32，看得见的版本只有 40 / 11 / 8</strong> —— 多数任务上，让读手看见污染，比<strong>完全不洗</strong>还差。叮嘱「小心点」的那一版，就是 40 / 11 / 8。</p>
  <p>它为什么是<strong>当下</strong>值得单独成篇的一格：上下文工程这条线 —— 组装、压缩、过滤、清洗 —— 全部默认<strong>「动手清理的那一方是干净的」</strong>。本文是第一篇把这个前提拿出来<strong>单独做消融</strong>的：同一个方法、同一套数字，只换「读手能不能看见助手轮次」这一个变量，增益整个消失甚至反转为负。</p>
</section>
'''

S3 = '''
<section>
  <h2>3 · 核心机制：污染、洗法、传染、与唯一可靠的隔离</h2>
  <pre>  多轮对话 ──▶ 模型早期输出留在窗口里（At-1）
                    │
                    ▼
            锚定后续轮次（context pollution）
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
   AO：全扔掉              AC3：分析器判一遍
   （干净但把诊断           （读手自己会不会被污染？）
     结果也扔了 → 0%）           │
                    ┌───────────┴───────────┐
                    ▼                       ▼
            看得见 assistant        结构上不给看
            40 / 11 / 8 ⛔          80 / 53 / 32 ✓
              （「叮嘱忽略」也在这一侧）</pre>

  <h3>3.1 第一步：污染是什么 —— 模型信自己说过的话</h3>
  <p>论文给的形式化一句话：<strong>p(correct | 当前用户消息, 早先助手输出) &lt; p(correct | 当前用户消息)</strong> —— 助手自己先前的输出<strong>降低</strong>了本轮答对的概率。被锚定的往往是最早的误读：<strong>用户已经纠正，模型还在沿旧方向走</strong>。引用的量级（Laban et al. 2025）：15 个模型、6 个任务领域平均退化 <strong>39%</strong>，对话平均只有<strong>约 8 轮</strong>。</p>
  <p><strong>为什么这一点重要</strong>：污染源不是攻击者、不是脏网页、不是被掉包的工具 —— 是<strong>模型自己上一轮的输出</strong>。内容上没有任何异常可检测，因为它就是模型自己写的。<code>[[ContextRot]]</code> 把退化归给长度与位置，这一条补上第三个来源：<strong>内容的所有权</strong> —— 是模型自己说的话，而它倾向相信自己。</p>

  <h3>3.2 第二步：最粗暴的洗法，以及它在哪里崩塌</h3>
  <p>消除污染最直接的办法是<strong>助手遗漏（AO）</strong>：把每一条助手消息整个丢掉。论文按后续轮次对先前内容的依赖方式分了三类：</p>
  <table>
    <tr><th>轮次类型</th><th>含义</th><th>AO 的后果</th></tr>
    <tr><td><strong>自含（self-contained）</strong></td><td>用户消息合起来足以完成任务</td><td>AO 近似「设计上的最优」</td></tr>
    <tr><td><strong>指涉（referential）</strong></td><td>后续轮次引用只存在于助手轮次的草稿 / 决定 / 结论</td><td>AO 开始失败</td></tr>
    <tr><td><strong>有状态（stateful）</strong></td><td>指涉对象是环境状态（工具调用的结果）</td><td><strong>AO 彻底崩塌</strong></td></tr>
  </table>
  <p>有状态工具调用（tau2-bench，9 个单元格、171 个 rollout、N=3）：<strong>AO 在所有被测模型上全部跌到 0%</strong>，没有一个非零奖励 —— 因为剥离助手消息把 agent 已经查到的诊断结果也剥掉了，agent 只能反复重新查询，直到步数预算耗尽。与 full context 的差距 <strong>−68.4 / −69.6 / −78.9 pp</strong>（p&lt;0.0001）。</p>
  <p><strong>为什么这一点重要</strong>：「把脏东西全扔了」永远不是一个可用方案，因为<strong>干净和可用是两回事</strong>。这也预先堵死了「那我把旧输出全删了不就行了」这条捷径 —— 你会连着把工作成果一起删掉。</p>

  <h3>3.3 第三步：AC3 —— 让一个干净的读手来做判断</h3>
  <p>AC3（Agentic Conversation Context Curation）是 training-free 的推理时方法，在 harness 里、助手生成<strong>之前</strong>运行。一个<strong>单独的分析器</strong>做两件事，顺序是关键：</p>
  <ol>
    <li><strong>规格提取</strong>：只从<strong>用户侧消息</strong>（含系统消息）归纳任务规格 —— 助手轮次<strong>结构性排除</strong>，在数据流上就不可见；</li>
    <li><strong>对照审核</strong>：拿着这个规格当基准，<strong>这时候才</strong>去读完整上下文，审助手先前的工作，标出 aligned（做对了）与 issues（偏离）。</li>
  </ol>
  <p>然后按审核结果执行<strong>编辑算子</strong>，一条纪律贯穿：<strong>只添加信息的算子每轮触发；删除内容的算子只在发现问题时触发。</strong></p>
  <ul>
    <li><strong>Augment（追加）</strong>：把分析结果附加在对话后面，污染内容仍可见 —— 温和版，每轮都跑；</li>
    <li><strong>Reset（丢弃重建）</strong>：用模板「（任务规格, 已确认做对的部分）+ 最新用户消息」替换整个对话，只在标记了问题时触发；默认的 <strong>Gated Reset</strong> 加了护栏 —— 跳过前两个用户轮、每对话最多重置 3 次；</li>
    <li><strong>Rewrite（重写）</strong>：再多一次 LLM 调用重构上下文。</li>
  </ul>

  <h3>3.4 第四步：传染 —— 量出来的那一刀</h3>
  <p>本文最值钱的消融只有一个变量：<strong>规格提取器能不能看见助手消息</strong>（Augment 算子、无记忆、单次试验）：</p>
  <table>
    <tr><th>配置</th><th>Math</th><th>Code</th><th>Database</th></tr>
    <tr><td><strong>AC3 完整版</strong>（结构性排除）</td><td><strong>80%</strong></td><td><strong>53%</strong></td><td><strong>32%</strong></td></tr>
    <tr><td>去掉结构性排除（提取器可看 assistant）</td><td><strong>40%</strong></td><td><strong>11%</strong></td><td><strong>8%</strong></td></tr>
    <tr><td>去掉子任务分解（合并成单趟，同样可看 assistant）</td><td>55%</td><td>21%</td><td>4%</td></tr>
    <tr><td><strong>完全不干预（full context）</strong></td><td>60%</td><td>16%</td><td>4%</td></tr>
  </table>
  <p>两个读法必须分开记：</p>
  <ul>
    <li><strong>看见污染的读手，在 math 和 code 上比不干预更差</strong>（40 vs 60、11 vs 16）—— 清洗这个动作本身引入了新的伤害；</li>
    <li><strong>被污染的两步版比被污染的单趟版更差</strong>（math 上 40 vs 55）—— 因为第二趟把第一趟产出的<strong>有偏规格当成了 ground truth</strong>，错上加错。分步不救你，隔离才救你。</li>
  </ul>

  <h3>3.5 第五步：「叫它别看」为什么无效 —— 软注意力 vs 硬注意力</h3>
  <p>论文试过最直觉的修补：明确<strong>指示</strong>提取器「只从用户陈述的需求推理」。结果一句话：<strong>"Instructing it to ignore did not close the gap."</strong> 提示词层的叮嘱（软注意力）关不掉锚定，只有<strong>数据流上的物理排除</strong>（硬注意力）才行 —— 让助手轮次根本不进入读手的输入。</p>
  <p><strong>为什么这一点重要</strong>：这给了一条可以直接抄的工程铁律 —— <strong>隔离的实现层只有一种可靠做法：不让它进入，而不是让它别看。</strong>本库已有的两处同形证据在这里汇成一条线：<code>[[HumanInTheLoop]]</code> 说规则要「写在代码里」（执行层，不是提示层），Claude Tag 把凭证放在沙箱外的网络边界注入（模型看不到）—— 位置对，比措辞好使。</p>

  <h3>3.6 第六步：忠实摘要复现不出这个增益 —— 问题不在算力，在读到了什么</h3>
  <p>一个自然的反驳是：「你不过是多花了几次调用。」论文做了算力对齐的对照 —— 用一个<strong>忠实压缩</strong>（只摘要、不找错）的 condenser 替代 AC3（database 任务）：每轮 1 次调用 <strong>53.3%</strong>、每轮 2 次调用 <strong>47.7%</strong>，都不高于 full context 的 <strong>56.1%</strong>；而两次调用的 condenser 用的算力<strong>比 Reset 更多</strong>（调用 1.02–1.19 倍、token 1.62–2.14 倍），Gated Reset 只用 <strong>0.41 倍</strong>调用量拿到 <strong>+17.8 pp</strong>。</p>
  <p>机制上更狠的一条：去掉「找错误」条款后，condenser 在 <strong>340 份摘要里 0 次</strong>标记助手错误 —— <strong>忠实摘要会把失效推理原样带下去</strong>。它不判对错，所以它搬运的正是污染。</p>

  <h3>3.7 第七步：洗得掉 ≠ 洗得准 —— Reset 是重建，不是手术刀</h3>
  <p>最后一步是把 Reset 的机制说穿。论文做了两层注入 / 消融研究：</p>
  <table>
    <tr><th>层</th><th>设计</th><th>结果</th></tr>
    <tr><td><strong>Tier A</strong>（构造注入，n=126）</td><td>注入一条已知错误 + 一条已知正确的助手侧内容</td><td>Reset <strong>97.6%</strong>（123/126）移除污染内容；但<strong>真实内容的保留率只有 4.0%</strong>，编辑精度等于随机；注入的<strong>真实</strong>内容也有 <strong>42.1%</strong> 被误标为 issue</td></tr>
    <tr><td><strong>Tier B</strong>（自然出现的内容，30 对话 / 3357 助手轮）</td><td>无 LLM 参与标签路径的因果消融</td><td><strong>7 个可探查有害内容全部移除（100%）</strong>；<strong>因果有用内容的保留率 0%</strong>；移除组与保留组的平均效应差 <strong>−0.014</strong>（permutation p=0.85，选择性编辑器应为正）</td></tr>
  </table>
  <p>结论一句话：<strong>Reset 不是精准的段落清除，是「检测到污染 → 整侧丢弃 → 从用户侧重建规格」。</strong>增益来自<strong>重建</strong>，不来自删对了哪一段。真实但无用的内容会陪葬，真实且有用的内容也一样 —— 这个代价论文自己量出来了，引用时必须一起带上。</p>

  <h3>3.8 总账：增益有多大、稳不稳</h3>
  <table>
    <tr><th>基准</th><th>关键数字</th><th>读法</th></tr>
    <tr><td>Lost in Conversation（四任务：math / code / database / actions）</td><td>Gated Reset 关闭 full-context 与 AO 差距的 <strong>80% / 84% / 超 oracle / 55%</strong>；33/36 配对比较胜过 full context（平均 <strong>+15.9 pp</strong>，sign test p&lt;0.0001）；未筛选 database 池 Reset <strong>75.7%</strong> 超过两个 oracle</td><td>恢复能力强；但注意 ⚠️⑤ 的 math 泄漏问题</td></tr>
    <tr><td>tau2-bench（有状态工具）</td><td>AO 全线 <strong>0%</strong>；Gated Reset <strong>57.9 / 57.9 / 71.9</strong>，比 full context（68.4 / 70.2 / 78.9）差 <strong>7–12 pp</strong>（p&gt;0.14，不显著）</td><td><strong>viability 而非 superiority</strong>：不崩，也没赢</td></tr>
    <tr><td>WildChat（真实人机对话）</td><td>GPT-5-mini judge 配对胜率 <strong>71.6%–91.5%</strong>；干预了 72.3% 的轮次</td><td>偏好侧信号；<strong>三个其他 judge 偏好 AO</strong> ⇒ 带限定引用</td></tr>
    <tr><td>CollabLLM（协作模拟）</td><td>40 题中 Reset 与 full context 最多差 <strong>3 题</strong>；最清晰证据：DeepSeek-V4-Flash 在 BigCodeBench 三次重复运行每次 <strong>+15 pp</strong></td><td>结果混合（mixed）</td></tr>
  </table>
  <p>分析器换血也不翻车：跨 <strong>5 个模型（4 个家族）</strong>当分析器都拿到正的、单独显著的增益（<strong>+12.9 到 +39.9 pp</strong>），弱分析器的问题是<strong>漏报</strong>而不是<strong>误报</strong> —— 方法对这个角色是稳的。</p>
  <p class="takeaway"><strong>这一格的判据句：</strong>「<em>Pollution is contagious: the hand that cleans picks up what it reads.</em>」—— 清洗器与污染源必须<strong>结构隔离</strong>；提示词里的「请忽略」不是隔离，是愿望。</p>
</section>
'''

S4 = '''
<section>
  <h2>4 · 应用场景</h2>

  <h3>场景一 · 长程客服 / 助手的多轮会话</h3>
  <p><strong>背景</strong>：真实人机对话（WildChat）里，用户中途改主意、纠正早期误解是常态；每多一轮，被锚定的旧输出就多留一轮。</p>
  <p><strong>如何应用</strong>：在 harness 里、每轮生成前跑一个<strong>只看用户侧</strong>的规格归纳器，把「用户到底要什么」的判断与「助手之前做了什么」的审阅<strong>拆成两步、两种输入</strong>。发现偏离时才触发重建，平时只追加。</p>
  <p><strong>结果</strong>：配对胜率 71.6%–91.5%、干预 72.3% 的轮次 —— 但部署前必须先用自己的 judge 复核一遍，因为论文的偏好数字依赖单一判官。</p>

  <h3>场景二 · 有状态工具型 agent（客服后台 / 运维 agent）</h3>
  <p><strong>背景</strong>：tau2-bench 的教训 —— 这类 agent 的工作成果几乎全部沉淀在助手轮次里（查到的状态、做过的决定）。</p>
  <p><strong>如何应用</strong>：这里要抄的不是 AC3 的增益，而是它的<strong>下界论证</strong>：全删（AO）会归零，所以任何清洗方案都必须先证明「不把工作成果一起删掉」。</p>
  <p><strong>结果</strong>：Gated Reset 在 tau2 上 57.9–71.9，离 full context 7–12 pp —— 差距不显著，但<strong>也没赢</strong>。诚实的结论是「可用、无优势」；宣称「全面更好」就是过度销售。</p>

  <h3>场景三 · 「加个摘要器」的清洗方案评审</h3>
  <p><strong>背景</strong>：很多团队的多轮记忆方案 = 定期把历史摘要成一段塞回去。</p>
  <p><strong>如何应用</strong>：拿 3.6 那组数字当评审判据：<strong>忠实摘要 ≠ 清洗</strong>。摘要器不判对错，340 份摘要 0 次标出助手错误 —— 它搬运的正是污染。要清洗，摘要器必须先有一份<strong>独立于被摘要内容</strong>的基准（用户侧规格），否则多花的算力只是把污染抄写得更工整。</p>
</section>
'''

S5 = '''
<section>
  <h2>5 · 边界辨析</h2>

  <h3>5.1 不是什么</h3>
  <ul>
    <li><strong>不是「上下文太长了」</strong>。<code>[[ContextRot]]</code> 讲长度与位置稀释注意力；本条在<strong>很短的对话</strong>（平均约 8 轮）里就成立，退化来自<strong>内容的所有权</strong> —— 是模型自己说的话，所以被赋予了不应得的信任。</li>
    <li><strong>不是「有攻击者」</strong>。污染源是<strong>模型自己的正常输出</strong>，没有注入、没有诱导、没有对手。与扩展十（良性 Skill 的行为偏移）同属「<strong>无对手的失效</strong>」：无异常可检测，所以检测式防御（异常检测 / 来源校验 / 签名）结构上无效 —— 有效的是<strong>位置型防御</strong>：让污染进不了读手的输入。</li>
    <li><strong>不是「压缩的问题」</strong>。<code>[[Compaction]]</code> 问「保留哪段文本」；本条问的是<strong>「执行这个判断的读手干不干净」</strong> —— 是改写 / 拦截之外的第三问：执行者的洁净度。压缩线四天三篇都在优化「压什么」，这一篇量出「谁来判断压什么」这个变量值多少分。</li>
    <li><strong>不是「记忆被污染」</strong>。<code>[[MemoryPoisoning]]</code> 是<strong>持久化</strong>的写入污染（跨会话、有写入者）；本条是<strong>会话内的自我锚定</strong>，不跨会话、不落盘。</li>
    <li><strong>不是「窗外载荷」</strong>。11-07C（工具更新的信任失效）说载荷在上下文窗口<strong>之外</strong>，模型看不见所以防不住；本条恰好相反 —— 载荷就在窗口<strong>之内</strong>，谁都看得见，<strong>而负责清理它的那位看见了反而更糟</strong>。两条加起来是一句完整的话：<strong>看不见的防不住，看得见的也会中毒。</strong></li>
  </ul>

  <h3>5.2 常见误解</h3>
  <ul>
    <li><strong>误解一：「把旧输出删干净就好了。」</strong> tau2-bench 全线 0% —— 全删把工作成果一起删了。干净和可用是两个变量。</li>
    <li><strong>误解二：「在提示词里叮嘱它别受影响就行。」</strong> 论文原话：叮嘱不闭合差距。软注意力关不掉锚定，只有硬注意力（结构性排除）可以。</li>
    <li><strong>误解三：「AC3 能精准清掉坏内容、保留好内容。」</strong> 不能 —— 真实内容保留率 4.0% / 0%。它的增益来自<strong>从用户侧重建规格</strong>，不是来自删得准。宣传成「精准清洗」就是没读懂机制。</li>
    <li><strong>误解四：「math 上也提升了 80%，说明方法通用。」</strong> 47% 的分析器输出含答案（泄漏），去泄漏后 math 配对增益 −2.6 pp —— math 的增益与分析器自己解题不可分。站稳的数字是 code / database 的 +30.2 / +26.0 pp（泄漏率 0–1%）。</li>
    <li><strong>误解五：「这就是个摘要方法。」</strong> 算力对齐的忠实摘要版在同样甚至更多算力下失败（53.3 / 47.7 vs 56.1），Gated Reset 用 0.41 倍调用量拿到 +17.8 pp —— 差别不在压缩，在<strong>基准从哪来</strong>。</li>
  </ul>

  <h3>5.3 适用与不适用</h3>
  <table>
    <tr><th>这个结论适用于</th><th>这个结论不适用于</th></tr>
    <tr><td>多轮会话里<strong>清洗 / 压缩 / 过滤历史</strong>的任何方案 —— 先问「判断依据从哪来」</td><td>单轮任务（没有历史可污染）</td></tr>
    <tr><td>用户会<strong>中途纠正、改主意</strong>的助手场景（锚定型污染的重灾区）</td><td>自含型对话（AO 本来就近最优，不需要分析器）</td></tr>
    <tr><td>任何「让模型自己读全量再判断丢什么」的<strong>过滤式</strong>设计（11-05B 的决定论反例）</td><td>有状态工具密集型任务（tau2 上 AC3 也不赢 full context —— 别在这里期待增益）</td></tr>
    <tr><td>清洗判据与被清洗内容<strong>可以分离</strong>的场合（用户侧消息独立成立）</td><td>指涉对象<strong>只存在于助手轮次</strong>的场合 —— 论文自己标注「未测量规格提取在此的表现」</td></tr>
  </table>
</section>
'''

S6 = '''
<section>
  <h2>6 · 与既有知识网的位置</h2>
  <table>
    <tr><th>已有页</th><th>本页补的那一格</th><th>落点建议</th></tr>
    <tr><td><code>[[ContextRot]]</code></td><td>退化源从「长度 / 位置」补到第三个：<strong>内容所有权</strong> —— 模型信自己说过的话，约 8 轮即 −39%</td><td>该页退化来源清单 +1 项</td></tr>
    <tr><td><code>[[Compaction]]</code></td><td>「压哪段」的<strong>执行者洁净度</strong>：过滤必须读全量才能决定丢什么，而读手并不比被过滤内容干净 —— 传染实验（80→40）就是量化证据</td><td>「压缩 vs 过滤」节后新增一段</td></tr>
    <tr><td><code>[[ContextEngineering]]</code></td><td>组装规则缺一条：<strong>给判断组件的输入，要与被判断对象隔离</strong> —— 这是比「放什么进窗口」更高一层的组装约束</td><td>该页组装纪律节</td></tr>
    <tr><td><code>[[MemoryPoisoning]]</code></td><td>同为「污染」，但<strong>无对手、不落盘、会话内</strong> —— 两页互指以防腐蚀机制的混淆（写入者 vs 自己的输出）</td><td>该页边界段互指</td></tr>
    <tr><td><code>[[HumanInTheLoop]]</code></td><td>「写在代码里还不够」这条纪律的<strong>镜像版</strong>：规则要与被治理对象隔离在<strong>数据流</strong>层，不是叮嘱层；且本页 judge 依赖的教训（三个判官偏好 AO）与 11-08C「判官会被讨好」同族</td><td>该页 10-26B 节的反向引用</td></tr>
    <tr><td>11-05B 压缩 vs 过滤</td><td>那条讲过滤的<strong>决定论</strong>（丢什么按规则）；本条讲过滤的<strong>认识论</strong>（谁来判、他读了什么）—— 两问叠放才是完整的过滤</td><td>两节互指</td></tr>
    <tr><td>扩展十 / 11-07A（无对手的失效）</td><td>同类的第二例：无对手、无异常可检测；防御同为<strong>位置型</strong>（不给看 / 执行前再问）而非检测型</td><td>「无对手失效」小簇互指</td></tr>
  </table>
</section>
'''

S7 = '''
<section>
  <h2>7 · 你会怎么用它（自查清单）</h2>
  <ol>
    <li><strong>盘点你所有的「清洗 / 压缩 / 过滤」组件：它们的判断输入里有没有被判断对象本身？</strong> 有一条就算一处暴露面。这是本文唯一必须执行的工程动作。</li>
    <li><strong>隔离只认数据流层。</strong> 「在提示词里写请忽略」不算隔离；让内容<strong>物理上不进入</strong>读手的输入才算。凡是靠措辞做的隔离，按 3.5 的证据一律视为没有隔离。</li>
    <li><strong>判断基准必须独立于被判断内容。</strong> 先从用户侧立规格，再拿规格去审助手输出 —— 顺序反了，基准就被污染（被污染的两步版 40 分低于单趟版 55 分，就是顺序错误的价格）。</li>
    <li><strong>别用忠实摘要冒充清洗。</strong> 摘要器不判对错（340 份摘要 0 次标错），它搬运污染。要么给它独立基准，要么承认它只是压缩。</li>
    <li><strong>删内容的算子按需触发，加内容的算子才每轮触发。</strong> 这条纪律同时控制成本（0.41 倍调用量）与风险（不误伤正常对话）。</li>
    <li><strong>接受「洗得掉 ≠ 洗得准」的代价，把它写进设计文档。</strong> 真实但无用的内容会陪葬（保留率 4.0% / 0%）。如果你的场景里助手轮次里有必须保留的状态，先把那部分挪出被清洗的范围 —— 这正是 tau2 上「不崩但也不赢」的原因。</li>
    <li><strong>报告增益时把 judge 依赖带出来。</strong> 三个其他判官在同样的响应上偏好 AO —— 你的清洗方案上线前，先用你自己的判官跑一遍，别搬论文的胜率。</li>
  </ol>
</section>
'''

S8 = '''
<section>
  <h2>8 · 来源（均为 WebSearch / WebFetch 真实返回 [verified]）</h2>
  <ol>
    <li><strong>arXiv:2611.00518v1 —— 《Agentic Context Management for Multi-Turn Human-AI Conversations》</strong>（Matthew Ho + 7 人；<strong>cs.AI + cs.CL</strong>；v1 2026-10-31 01:13:55 UTC；813 KB）—— 支撑：污染形态化、AO 三类轮次与 tau2 归零、AC3 三步与三种算子、传染性消融 Table 4（80/53/32 vs 40/11/8）、「叮嘱无效」、算力对齐的忠实摘要对照、Reset 的 Tier A/B 检测研究（97.6% / 4.0% / 0%）、四基准总账、math 泄漏与去泄漏、自陈局限。<code>https://arxiv.org/abs/2611.00518</code> 🟢 <strong>一手论文</strong> 🔴 未同行评审</li>
    <li><strong>arXiv HTML 全文（一手，已抓取正文与表格）</strong> —— <code>https://arxiv.org/html/2611.00518v1</code> —— 支撑：本文全部逐格数字（Table 3 / 4 及附录）、Gated Reset 护栏（跳过前两轮 / 每对话最多 3 次）、分析器跨模型鲁棒性（5 模型 4 家族 +12.9 ~ +39.9 pp）、泄漏分析（47% / −2.6 pp / +30.2 / +26.0）。🟢 <strong>一手</strong></li>
  </ol>
  <p class="warn"><strong>来源面说明：</strong>本页只有两个来源，因为该论文 2026-10-31 才发布，<strong>尚无独立二手转述</strong>可交叉核对 —— 所有数字均直接取自一手 HTML 全文。凡第三方引用本文数字时，注意两处最易传错的口径：① <strong>「80 / 53 / 32 vs 40 / 11 / 8」是 Augment 算子、无记忆、单次试验的消融表</strong>，不是主结果表；② <strong>tau2 上 AC3 没有赢 full context</strong>（差 7–12 pp、不显著），把它引成「全面超越」是方向性错误。</p>
</section>
'''

S9 = '''
<section>
  <h2>9 · 一句话回顾</h2>
  <p class="takeaway"><strong>污染会传染 —— 量出来的那一刀是「让它看见，40 分；不给它看，80 分」。所以隔离只有一种可靠做法：不让它进入，而不是让它别看。</strong></p>
</section>
'''

FOOTER = '''
<footer>
草稿 · <code>output/pending-review/contagious-pollution.html</code> · 生成于 2026-11-09 · 由台账 11-08B「清洁工也会被污染」⭐⭐⭐ 成文（用户指令「按你的来」）· 受 README 人工核查承诺约束，<strong>未写入 <code>learning-materials/</code></strong>；核查通过后目标名 <code>learning-materials/contagious-pollution.html</code>，并需补一次「移入 <code>learning-materials/</code> → <code>raw/</code> → 摄取」链路<br />
由 concept-explainer Skill 自动生成 · 2026-11-09 · 待人工核查后入库
</footer>

</div>
</body>
</html>
'''

html = (HEAD.replace("ACCENTSOFT", ACCENT_SOFT).replace("ACCENT;", ACCENT + ";")
        + COVER + WARN + S1 + S2 + S3 + S4 + S5 + S6 + S7 + S8 + S9 + FOOTER)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "pending-review", "contagious-pollution.html")
out = os.path.normpath(out)
with open(out, "w", encoding="utf-8", newline="\n") as f:
    f.write(html)
print("written:", out)
print("bytes:", len(html.encode("utf-8")))
print("sections:", html.count("<section>"))
print("has </html>:", html.rstrip().endswith("</html>"))
