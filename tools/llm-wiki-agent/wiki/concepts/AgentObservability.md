---
title: "Agent Observability & Evaluation"
type: concept
tags: [observability, evaluation, otel-genai, openinference, trace, llm-as-judge, observability-envelope, inside-out-monitoring, activation-probes, trust-layer, evaluation-economics]
sources: []
last_updated: 2026-10-26
---

# Agent Observability & Evaluation (可观测性与评测)

**Trace answers「发生了什么」, eval answers「做得好不好」, and the trust layer answers the question nobody used to ask —「这条 pass 该不该被相信」.** Three positions on one evidence chain, not three parallel tools: without the first, the second has nothing to score; without the third, you do not know whether the score the second produced can be used to make decisions.

> **Draft annotation, pending ingest.** This page is the **structural merge of four ledger rows**, authorized by the user's instruction of 2026-10-26（「那就结构性合并」）: **10-08 Agent Observability & Evaluation ⭐**（记录侧 + 判官侧）· **09-17 Agent Evals**（判定侧 + 元层）· **10-09 candidate 3 Inside-Out Monitoring**（判官侧）· **09-25 Agent Evaluation Economics**（成本章）. Its material basis is the draft `output/pending-review/agent-observability.html`（2026-10-15 成文，受 README 人工核查承诺约束未入 `learning-materials/`）; all load-bearing numbers re-verified against live sources on 2026-10-26. Remove this banner on ingest; move the slugs into frontmatter `sources`.
>
> 🔴 **Evidence grades that must travel with every citation of this page:** OTel GenAI conventions are all **Development / zero tagged releases**; Goodfire's **$51 / $233 / $10,000, 94%, 8.7%, <2%** are **vendor-reported, no third-party replication** — three tiers quoted by one company, not three independent measurements; `arXiv:2610.07274` and `arXiv:2610.02066` are **preprints, single-benchmark / small-sample**; AgentRx's public records conflict (**115 vs 170 trajectories**); the Anthropic "quiet failure modes" item reached this page only via a **second-hand compilation, downgraded**.

## Why this page exists — three acceptance criteria pinned on a page that did not exist

Cluster E answers **who runs the loop**（[[AgentHarness]]）, **where it runs**（[[AgentSandbox]]）, **with whom**（[[MultiAgent]]）— but **no page answered「怎么看见它跑了什么、跑得对不对」**. The wiki's truth discipline（[[Provenance]] / [[CitationLock]] / [[Abstention]]）governs only whether **what the model says** is trustworthy, not whether **what the system did** is visible. Three pages' acceptance criteria simultaneously required this page: [[HumanInTheLoop]] must measure automation / override / **escape** rate; [[MultiAgent]] declares the verifier a precondition; [[AgentSandbox]]'s motivating evidence is the HF intrusion post-mortem — **all three require「看得见」, and the page that provides it did not exist.**

## Chapter A · 记录层 — what one run must leave behind

OpenTelemetry GenAI semantic conventions have become the de-facto record format. The four questions one run must answer, and their carriers:

| question | what in the trace answers it | if unanswered |
|---|---|---|
| 它做了什么 | span tree; **agent and tool are first-class spans**（`create_agent` / `invoke_agent` / `plan` / `invoke_workflow` / `execute_tool`） | only the result is known, not the path ⇒ no per-hop attribution |
| 花了多少 | `gen_ai.usage.input_tokens` / `output_tokens` | the bill cannot be attributed to steps |
| 谁回答的 | `gen_ai.request.model` vs **`gen_ai.response.model`（may differ — server-side fallback）** | a downgrade gets blamed on the wrong model |
| 对不对 | ❌ **not covered by the conventions** — every backend models this itself | this cell belongs to the eval layer, not semconv |

Ecosystem: **OpenInference** six span kinds（LLM / CHAIN / TOOL / RETRIEVER / EMBEDDING / AGENT, instrumentors for 100+ frameworks）; **MCP-specific conventions**（`mcp.client` / `mcp.server` spans + four MCP metrics）; the market is converging — **Dynatrace signed to acquire Arize（2026-08）**; the **MCP 2026 roadmap（2026-03-09）** lists observability among four directions; Thoughtworks' 2026-04 radar puts「toxic flow analysis」in Assess, noting static SAST / SCA cannot see prompt / tool / memory / inter-agent traffic — *“干净的报告制造覆盖假象。”*

**有标准 ≠ 标准稳定.** OTel GenAI is all **Development, zero tagged releases**（cannot pin a version, only a commit / snapshot）, attribute names get renamed across versions, and **2026-06-12（semconv v1.42.0）the gen_ai.* / mcp.* conventions moved out of the main repo into `open-telemetry/semantic-conventions-genai`**（main repo v1.43.0, 2026-07-03, no longer contains gen-ai）⇒ *where to find the conventions is itself information*. Measured instrumentation overhead ≈ **12%（AgentOps）/ 15%（Langfuse）**. The standard's own sentence is the one to keep: **the conventions standardize what a model call looks like; they do not standardize what a good trace looks like — and they say nothing about evaluation scores.**

## Chapter B · 语义层 — the observability envelope is narrowing

看得见 ≠ 读得懂. **Transect**（`arXiv:2610.08364`; v1 2026-10-06 / v2 10-08, 27 pages, open source, built on Inspect Scout; **UK AI Security Institute + Meridian Labs** — affiliation re-verified 2026-10-26）formalizes the name: the **observability envelope** — *the range of what evaluators can reliably infer about an agent's behaviour* — **is narrowing** as long-horizon, multi-agent transcripts run to hundreds of pages. Its answer: make task context and behavioural vocabulary a reusable **evaluation-family configuration**（**separated from the judge model**）, and align events / token use / sub-agent activity / behavioural labels onto **one turn-based timeline**. Demonstrated on an AI-R&D evaluation of **almost 13 million tokens**, where the combined view showed the run **lacked a sustained hypothesis-generation stage** — this layer is not recording; it is **making the invisible show up**. ⇒ the envelope is a quantity that shrinks with run length, so evaluation-family configuration must be planned **at design time**, not improvised by re-reading transcripts afterwards.

Product face（「规范已 Final」与「生态已可用」必须分栏）: **Sentry JS SDK（2026-10-09）** ships agent spans（`invoke_agent` / `execute_tool` / …, `gen_ai.*`, MCP server auto-instrumentation; ⚠️ agent spans still **Development**, prompt/response content **Opt-In**）; **New Relic AI Evaluation（2026-10-06, public preview in November）** hangs LLM-as-judge scores as **attributes on existing OTel traces**（incl. RAG faithfulness / answer relevancy）⇒ 09-17's judgement「2026 的 evals 直接挂在 trace 上」is now product behaviour — ⚠️ no pricing, no framework list, no judge-accuracy figures（vendor-intent grade）.

## Chapter C · 判官层 — how to judge, at which layer, for how much

Two 2026-10 first-hand results overturn the default path of「外部逐条重读」: **① unaffordable**（a supervising model pays a second full inference per task）; **② the external channel itself misses information**（what the model did not write down is not in the transcript）. The new answer: **change the layer being observed — not the output, the internal activations.**

**Goodfire「由内而外」monitors**（2026-10-08, Baseten customers first; primary coverage TechCrunch）: small **probes** read internal activations **at every step**; **only an alarmed probe escalates to the expensive second look**. Vendor-reported（须降级）: on **Kimi K3**, **~1,500** sessions cost about **$51** total, vs **$233**（cheaper model reviewing every step）and **~$10,000**（top-tier judge）; **94%** of malicious intrusion sessions caught; **8.7%** of harmless sessions escalated; four concurrent probes add **<2%** latency. Cost mechanism per CEO Eric Ho: **probes reuse numbers the forward pass already computed** — a judge model pays a fresh full forward pass for the transcript. ⇒ **监控成本从「全量付费」变成「异常付费」.**

**`arXiv:2610.02066`**（Gupta & Buscaldi, 2026-10-01）: span-level（BIO-tagged）hallucination detection + the **cross-model setting** — one model observes another's internal representations: **an external observer can match or exceed the generating model's self-check, and the observer can be smaller** ⇒ *“自我检测不是定位幻觉起点的上限.”*

**AgentRx**（Microsoft Research, EMNLP Findings 2026, online 2026-10-02）supplies the failure-attribution order worth memorizing: convert the failure trajectory into **a chain of constraints** → check step by step → **record violations with evidence** → **only then** let the LLM judge localize the critical step and failure class; reports **+75% average step localization**（作者自报；⚠️ records conflict: 115 vs 170 trajectories）.

Line classification（长期可用）: AI-safety monitoring splits into **behavioural monitoring**（external, inputs/outputs）and **interpretability monitoring**（inside the box）— the latter is now being **productised into the agent runtime**. Three caveats that travel with the numbers: the cost advantage **presupposes access to weights and activations**（not possible on closed APIs — currently for those running open weights on their own inference stack）; the **8.7% false-escalation rate** can dominate cost in high-risk / low-base-rate deployments; the internal signals are **trained for specific risk classes**（intrusion / CBRN misuse / reward hacking）— **not a general judge of「对不对」**, which is exactly Chapter A's conclusion: **the conventions standardize what a call looks like, not how well it is judged.**

### C-bis · The judge has a preference of its own — the scoring function leans toward *using* memory *(ledger row 10-29C; applied 2026-10-29)*

> **Draft annotation, pending ingest.** Not yet backed by a source page in this wiki — verified against live sources on 2026-10-29 (`.workbuddy/memory/concept-radar/2026-10-29.md`, candidate 3; ledger row **10-29C**). Remove this banner on ingest; move the slug into frontmatter `sources`.

**The question this page never asks.** All five chapters ask some form of **「测得准不准」**: is the record complete (A), is it readable (B), is the judge affordable and well-placed (C), can the verdict itself be trusted (D), what does it cost (E). **None asks whether the scoring function systematically prefers one kind of answer** — i.e. whether the judge, like the system it grades, has a prior.

**Memory-Aware Reward Modeling**（`arXiv:2610.31272`, v1 **2026-10-22 13:43:33 UTC**; Yijiang River Dong 等 12 人, Cambridge / Stanford / TUM / Harvard / UT Austin）measures exactly that, and its **design** is what makes the number usable: **~1,000 pairwise judgments from 87 participants**, each judging **with their own real ChatGPT queries and their own exported memories**. The judge is therefore not answering *"which answer sounds better"* in the abstract — it is answering *"which answer do I prefer when my own memories are on the table."*

- **Memory-conditioned responses are not consistently preferred** over responses generated without memory, and **in some cases users strongly prefer the version without memory.**
- **Automatic evaluators agree with users only weakly**（prediction accuracy close to the majority baseline）**and select the memory-conditioned response substantially more often than users do.**
- Their memory-aware reward model, trained on those human judgments, reaches **72.8%** preference-prediction accuracy, above the baselines.
- The named failure family is **over-personalization** and its siblings: reusing an earlier stated preference in a request that does not warrant it. ⇒ **These are not memory-accuracy or retrieval failures.** The record is correct and retrieved correctly; **the error is in whether it should be used.**（This is why the row is filed here rather than on [[LongTermMemory]].）

⇒ **Consequence for this chapter.** Chapter D verifies the **provenance of a verdict**（D1 competence · D2 reward hacking · D3 deception · D4 stability）. This adds a **sixth check of a different kind**: **does the judge share the graded system's own preference?** A judge that rewards *the presence of memory* will report a memory layer as beneficial **by construction**, which is the measurement-side mirror of what [[RAG]] records on the accounting side — **two independent measurements, same direction: more memory is systematically over-credited.**

**Boundaries.** **vs 10-25C（Repair, Not Detection）** — that row prices a **detector's precision**（"a flag earns its retry only when precision exceeds D/(R+D)"）; this one is about a **scoring function's bias** ⇒ *one cannot detect, the other detects crookedly.* **vs ledger row 10-27C（SciValidityBench, ⏸ not yet landed）** — that row says *"correctly remembered ≠ eligible to influence this decision"*（**object** layer）; this one says *"the judge cannot tell the difference"*（**measurement** layer）⇒ **two halves of one segment, cross-name, do not merge.** **vs ledger row 10-26C（Disclosure Begets Disclosure）** — that is a **system-side loop**（recall rewrites capture's input）; this is a **measurement-side loop**（evaluation rewards memory use）⇒ different causal direction. **vs Chapter D** — D audits the verdict against saved artifacts; this audits the **preference encoded in the judge**.

⚠️ **Evidence grade.** Preprint, not peer-reviewed; **87 participants** with **self-built memory profiles** is a small convenience sample; **72.8% is preference-prediction accuracy, not task accuracy**; the paper's own ask is to **change the optimization target**（from retrieval accuracy to user preference）, **not to remove memory** ⇒ **must not be read as「memory is useless」**.

## Chapter D · 元层 — is the verdict itself trustworthy

**A Trust Layer for Agent Evaluation**（`arXiv:2610.07274`, Centific Research）is an **additive post-hoc layer that never modifies the recorded score**, answering per pass:「这条 pass 该不该被相信」. Four dimensions — **D1 competence**（can the benchmark's own grading code reproduce it）· **D2 reward hacking**（was the passing answer actually computed, not hard-coded or copied from the prompt）· **D3 deception**（does the agent's completion claim match what happened）· **D4 stability**（does a rerun stay in the same score band）. The first three use only saved artifacts; only D4 re-runs the agent; model judgments only label evidence under majority voting — **every verdict is a deterministic rule**（「验证器本身尽量不是一个模型」— direct dialogue with [[MultiAgent]]'s「验证器是前提」）. Measured on **5 agent configurations × 108 Agents' Last Exam tasks**: **only 22.6% of recorded passes clear all four checks**（95% CI 15.0–32.6, n=84）; **every model shows passes with no traceable computation**（rates spread **tenfold**）; **confirmed false completion claims**; **18–46% of tasks do not stay in one score band over five runs**. The closing sentence is quotable whole: *「衡量一个 agent 能做什么，与验证它是否真的做了，是两个不同的问题，而现有 benchmark 只处理前者。」* Sibling results — AgentAbstain **59.5%**（`arXiv:2607.10059v1`）, file-review benchmark **67.9% unread / 80.4% of statements misleading**（`arXiv:2609.20812v3`）— converge on the same filing rule: **「agent 的自述」与「实际发生」必须分栏.**

Reading 22.6% correctly: it means **most recorded passes fail at least one check** — it is **not** an agent ranking; single benchmark（ALE）; **13–20 passes per configuration**, small overlapping samples; code released only upon acceptance.

## Chapter E · 成本章 — the economics of watching and judging *(ledger row 09-25)*

The judgement layer has a price structure, and the whole stack is taxed:

- **The biggest line of the production bill is the record itself.** Stanford Digital Economy Lab（*Agentic AI Cost Attribution*）attributes **~62% of agent inference bills to re-sent context** — the system prompt, tool definitions and state transmitted with every call（re-verified 2026-10-26 via multiple independent secondary sources; original report not opened; the landing lives on [[ContextEngineering]]'s resident-budget section）; agentic tasks consume **5–30×** the tokens of a chat query（Gartner, 2026-03）.
- **The judgement layer is metered per verdict.** LLM-as-judge runs **~$0.01–$0.10 per evaluated response**; a production suite can run 100 test variations per release — the three-tier comparison of Chapter C（$10,000 量级全量外部重读 / $233 量级便宜模型逐步检查 / $51 量级内部探针按需升级, ⚠️ 厂商自报）is the selection tool.
- **The tax compounds with model cadence.** McKinsey's July survey: ~**60%** of agentic spend already goes to response-refinement loops, **>90%** of enterprises report exceeding AI budgets; Gartner's 2026 hype-cycle warning: ~**40%** of AI-agent projects cancelled by 2027 **for cost overrun, not technical failure**.
- **And the observability gap is itself measured.** Elastic's 2026 enterprise survey: **85%** of IT organizations plan LLM observability, **only 8%** have implemented it — most teams cannot attribute cost to a prompt, tool call, retry, or escalation at all, so every number above is invisible on their invoices.

⇒ 边界: this chapter owns the **watching-and-judging bill**; [[ContextEngineering]]'s resident-budget section owns the **re-sent-context bill** — the two biggest invisible lines of the same invoice, split by page. And [[AgentHarness]]'s LAM section（ledger row 10-09 candidate 2）bounds that invoice **from below, provably** — 厂商账单侧 vs 可证下界侧, cross-named, not merged.

## Boundaries (do not merge)

- **vs [[AgentHarness]]** — mechanism vs **witness**: it runs the loop, this page records and judges that loop（its LAM section prices the harness itself）.
- **vs [[Provenance]] / [[CitationLock]] / [[Abstention]]** — those govern **what the model said**; this governs **what the system did**, then extends to **the provenance of scores** — the same discipline with its object widened from「一句话」to「一次运行」to「一个分数」.
- **vs [[HumanInTheLoop]]** — the gate **needs** escape rate; this page **provides** it. The gate sits **downstream** of the detector.
- **vs [[MultiAgent]]** —「验证器是前提」; without trace visibility you cannot even decide **which step** to verify, and Chapter D further requires **the verifier itself be verified**.
- **vs [[AgentSandbox]]** — the container bounds **what can be touched**; this watches **what it intends** — `authority is not isolation` extended to the evidence layer（容器边界 vs 内部信号，互补且不同层）.
- **vs ledger row 09-28（记忆评测的可信度）** — 「基准的构造成立吗」vs「单次 pass 记录成立吗」— same family, object narrowed from benchmark to one record（row-to-row）.
- **vs [[MemoryGovernance]]** — governance governs **how state changes**; observability records **what this run actually did**: 前者是策略，后者是证据.
- **内部各章不可互并** — 记录层（span/trace）· 语义层（envelope/行为词表）· 判官层（怎么判/多少钱）· 元层（判本身可信吗）· 成本章（多少钱）是**同一证据链的五个位置**；合并任何两层都会丢掉「上层以下层的存在为前提」这条结构（C-bis 是**判官层内部的偏向检查**，不是第六层，故不破坏五层结构）。

## Judgement sentences (可直接引用的判据句)

- Trace 答「发生了什么」，eval 答「做得好不好」，trust layer 答「这条 pass 该不该被相信」。
- 有标准 ≠ 标准稳定（OTel GenAI 全 Development、zero tagged releases）。
- 看得见 ≠ 读得懂——observability envelope 是随运行长度收窄的量，不是定值。
- 约定标准化的是「调用长什么样」，不是「判断得好不好」。
- 衡量一个 agent 能做什么，与验证它是否真的做了，是两个不同的问题。
- 裁判也是模型——分数是给人看的信号，不是裁决。
- 「agent 的自述」与「实际发生」必须分栏。

## See Also

- [[AgentHarness]] — the mechanism this page witnesses（its LAM section prices the harness）
- [[AgentSandbox]] — container boundary vs internal signal: complementary layers
- [[HumanInTheLoop]] — this page supplies the escape-rate signal the gate needs
- [[MultiAgent]] — the verifier this page demands be verified
- [[Provenance]] / [[CitationLock]] / [[Abstention]] — the claims-truth discipline this page extends to runs and scores
- [[ContextEngineering]] — the resident budget (62% re-sent context) is the other big line of the same invoice
- [[LLMContext]] / [[Compaction]] — the resource being recorded and the technique whose losses must stay visible
- [[RAG]] — 判分的基线对象：本页的 judge 层要给「记忆值不值」打分，而那件事的零点在 RAG（added 2026-10-29）
- [[SourceScore]] — 第三方 agent 评级站点：trust layer 的产品形态之一；「评级」与「验证」是两件事（见 Chapter D）（added 2026-10-29）
