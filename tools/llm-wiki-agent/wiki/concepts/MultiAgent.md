---
title: "Multi-Agent Orchestration"
type: concept
tags: [multi-agent, test-time-communication, orchestration, verifier, cross-contamination, protocol-pivoting, substrate-centric, repair-gap, latent-communication]
sources: [multi-agent]
last_updated: 2026-10-20
---

# Multi-Agent Orchestration (多智能体协作)

Multiple agents with **independent context windows** working on one goal: exchanging **verified** partial results, failure paths and intermediate scores through a shared workspace, so that **less total compute beats best-of-k independent sampling** — **provided a verifier exists**. Without a verifier, or under tight compute, communication overhead exceeds its gains and independent agents do better.

## Mechanism (per [[multi-agent]])
- **The exchange object is verified progress, not messages** — k agents, same goal, same compute budget, no preset roles, no central orchestrator; a shared workspace holds partial results, failure paths and code. *The gain comes entirely from building on confirmed breakthroughs and not re-walking confirmed dead ends — not from workflow design.*
- **The verifier is the precondition of the gain.** Only when "who actually progressed" can be judged cheaply does "build on others' progress" work. On LP85, 64 independent attempts all failed while team@5 solved 65% — progress was verifiable. *This turns "should we go multi-agent" from taste into a predicate: first ask whether the task has a verifier.*
- **The counter-result ships with the result.** ARC-AGI-3: team@3 = best@13, team@5 = best@33 (≈4.3× / 6.6× equivalent compute); polyomino packing team@3 SOTA 0.945; MNIST 4-agent classifier 1,957 bytes @ 99.4%. But the paper's own abstract: the method "**fails without verifier or low compute**". *Cite the gain together with its boundary condition, or you are quoting a conditional result as a panacea.*
- **New failure surface: cross-contamination (互相污染).** One agent's unverified conclusion gets inherited by peers as a premise — a failure mode absent from the single-agent world, landing on [[Provenance]]'s extension line: team trust must cover the **verification status of peers' conclusions**, not just fact origin. *(2026-10-16: the authorization-inheritance variant of this failure now carries CVE-grade cross-vendor evidence — see the section below.)*

## Boundary
- **Not subagents** — subagents are threads *inside* one agent (returning a summary to the main context); multi-agent is a **peer team**, members each holding the full goal and an independent window. Claude Code Projects nests both: threads are the team, and each thread can spawn its own subagents.
- **Not shared memory** — [[LongTermMemory]] is one agent's persistence **across sessions** (time dimension); multi-agent is shared state **across agents at one moment** (space dimension). Complementary; the governance of team-shared memory is their open intersection.
- **Not a replacement for [[ContextEngineering]]** — context engineering places content *within* one window; multi-agent decides what to exchange *between* windows. The latter is the former's cross-window extension ([[Compaction]]'s "clean-window subagent returning 1–2k tokens" is the seed).
- **Not "more agents is always better"** — the paper carries its own counter-example (no verifier / tight compute → independent wins); the product carries its own cost (threads each burn quota). A bounded tool, not a free lunch.

## Cross-Protocol Authorization Inheritance — protocol pivoting *(added 2026-10-16)*

> **Draft annotation, pending ingest.** This section is **not yet backed by a source page in this wiki** — its claims were verified against live sources on 2026-10-16 (recorded in `.workbuddy/memory/concept-radar/2026-10-16.md`, candidate 2; ledger row **10-16B**). Remove this banner when the material is ingested and human-reviewed, and move the source slug into the frontmatter `sources` field.

**The seam this page had left empty.** Since 2026-09-26 cross-contamination has been recorded here as the collaboration leg's failure surface — with **no evidence at all** (the page is flagged secondhand throughout). What arrived is CVE-grade, cross-vendor confirmation of the same shape one boundary out: the flaw is not in the **credential** but in **on what authority the task itself travels**.

- **Mechanism — "protocol pivoting" (independent researcher Syed Anas Mohiuddin, ~five months of work).** Attacker text is planted in content one agent reads; that agent passes it on **as a normal delegated task** to a peer it trusts; the peer sits inside the network and performs **SSRF** or another privileged action. The escalation gives the class its name: the text enters via **MCP** and crosses into **A2A** or the emerging **Agent Network Protocol** — "**trust or authorization gets effectively lost in translation**". Why an LLM-side guardrail does not catch it: "**since MCP servers store credentials for each agent — and agents are built to trust every other internal agent — an exploit that would have been rejected by the LLM succeeds.**"
- **Concrete instance — Google.** `googleapis/mcp-toolbox` initialised its Go HTTP client **with no `CheckRedirect` policy and no target-IP validation** ⇒ a crafted path parameter follows a redirect to an internal endpoint, potentially the cloud metadata address **169.254.169.254** (which hands out IAM credentials). **CVE-2026-14540, CVSS 8.0.** The *fix* is the teaching artifact: connection-time resolved-address checks plus IP allow/block lists, and **rejecting an unsafe base URL at startup rather than on first request**. Researcher's own line: "*That is what a real SSRF guard looks like. It is also more work than most MCP servers have done.*" ⇒ *the position of the control was the answer again* — same cross-cutting theme as the orchestration-layer cell.
- **Cross-vendor scope.** Confirmed and fixed at **Google, JPMorgan Chase, Weaviate, France's DINUM** (data.gouv.fr MCP) and **Indonesia's Tangerang city government**; **Rapid7** published **CVE-2026-97228** (CVSS **2.7**, fixed in September). Five MCP servers built for **US federal agencies** (incl. a VA-benefits one) were reported 2026-09-02 and **remain in triage**, described only at class level.
- **Root-cause sentence (Rapid7 · Douglas McKee):** "*Each protocol was built assuming it lived on its own, so each one checks its own front door while nobody watches the hallway in between.*" Operationally: **dependency scanners do not see tool arguments that arrive as delegated agent text**.
- **Counter-evidence, must sit beside the conclusion (X41 D-Sec · Markus Vervier):** the better term remains **indirect prompt injection**, and the cross-protocol hop "*is not strictly required for such attacks to work*". ⇒ **not a new class — an old class with a new reachable range.**

**Boundary vs [[AgentIdentity]]:** per-hop attenuation (RFC 8693) narrows the **credential** — scope / magnitude / validity / depth may only shrink — and says nothing about the **task content** inheriting authority. The rule this cell supplies is therefore *independent*: **every protocol transition should trigger fresh authorization rather than inherit an upstream decision.** Credential narrowing does not entail it.

**Boundary vs the existing 10-13「检索准入 × 跨主体状态隔离」row:** that row asks *whose state is this* (a leak **inside already-admitted shared state**); this row asks *on what authority did this instruction travel* (a leak **at the hand-off**). State ownership vs authorization inheritance — **not a duplicate**.

**Family note:** "*authority is not isolation*" ([[AgentSandbox]], execution side) · "*model output is not the permission*" (orchestration side, 10-16A) · "*access is not authority*" (protocol side, this row) — **three members of one family, one layer apart each**; the shared sentence is **"nobody is checking this stretch."**

⚠️ **Evidence grade:** pattern-level, largely the researcher's own framing amplified by Ars Technica (Dan Goodin, **2026-10-05**); **CVE-2026-14540** is attributed to his self-published write-up (Ars reports severity 8 **without naming the CVE**); **advisories were not re-opened first-hand** here; federal findings are **unpatched / in triage, class-level only**; **every named bug is already fixed** — what is new is the cross-vendor *pattern*, not a zero-day. Presented at **MCPCon North America, 2026-10-23**.

### The missing second half of this section — Substrate-Centric Coordination (ScaleMAS) *(added 2026-10-17, ledger row 10-17C)*

> **Draft annotation, pending ingest.** Not yet backed by a source page in this wiki — verified against live sources on 2026-10-17 (recorded in `.workbuddy/memory/concept-radar/2026-10-17.md`, candidate 3; ledger row **10-17C**). Kept **inside this section on purpose** (yesterday proved the failure exists, today supplies its shape; splitting them would let the two halves of one page drift apart).

**The gap this fills.** The section above establishes with CVE-grade evidence that **cross-agent contamination happens** — and offers **no proposal about shape**. ScaleMAS supplies the shape: **do not share a peer's output as context; make it a message that can be published, cited, retrieved by "relevance × citation count", and fetched by address.**

1. **Three problems that grow with group size** (`arXiv:2610.16120`, submitted **2026-10-12**; Zhenting Qi (Harvard) with Zhuokai Zhao / Rulin Shao / Kerem Oktar / Zhiyuan Yao / Himabindu Lakkaraju / Wen-tau Yih / Ansong Ni / Bhargavi Paranjape / Yilun Du — **FAIR at Meta + Harvard**): **read burden** grows with the group (message passing hands every sender's output to the receiver; an orchestrator routes every sub-agent result into one context) · **useful signal is diluted by shared work of unknown quality** · **failure becomes normal** (fixed workflow or single orchestrator ⇒ losing one member breaks the run). Diagnosed as a product of **agent-centric design**.
2. **The key judgement:** existing **blackboard-style** shared middle layers solve **only the third** of these (tolerance to agent failure). The first two remain — which is why "we already have a shared workspace" is not an answer.
3. **The mechanism — three operations over a *linked* message store:** **publish** (optionally carrying **citations to the messages it depends on**) · **search** (top-*k*, ranked by **relevance × citation count** — the authors find the latter to be an effective quality proxy) · **fetch by address**. Two consequences do the work: a bounded *k* makes **each agent's read volume bounded at any group size**, and messages persist after their producer leaves ⇒ **the team tolerates mid-run loss**.
4. **Results:** beats both **agent-centric** and **blackboard** baselines on four agentic tasks **at lower inference compute**, scaling to **128 agents**. The control is the number to remember: the orchestrator-style **AOrchestra loses more than half its score at only 20% agent drop-out**.

**What this repairs on the wiki.**
- **[[Provenance]] promoted from *after-the-fact audit* to *in-flight coordination*.** Citation count becomes a **ranking signal**, which is the runnable form of the prediction `overview.md` has carried since 2026-09-26 (that Provenance's object must expand from *a fact* to *the verification status of the conclusion you are treating as fact*).
- **A second form of [[Abstention]]:** top-*k* bounded reading is **architectural forced abstention** — the agent never sees the rest — as distinct from abstention *after* judgement. The wiki previously had only the latter.
- **The counterpart to the rows above:** 10-16B says *task content inherits upstream authority*; the countermeasure here is ***task content must arrive in citable form***. vs [[ContextEngineering]] — that page is bounded reading for a **single** principal; this is the **multi-principal** version.

⚠️ **Author-stated limits:** inference-time only (agents were **not trained** to use the substrate); **128 is a compute ceiling, not an architectural one**; **prompt-sensitive** — it depends on agents writing retrievable rationales and subtask descriptions.

#### Scope note — the three operations presuppose a text wire *(ledger row 10-19C; not ⭐; applied 2026-10-20)*

> **Draft annotation, pending ingest.** Not yet backed by a source page in this wiki — verified against live sources on 2026-10-19 (recorded in `.workbuddy/memory/concept-radar/2026-10-19.md`, candidate 3). Kept **inside this subsection on purpose**: this note states the *precondition* of the three operations above, so putting it anywhere else would let a mechanism and its precondition drift apart. Remove this banner when the material is ingested and human-reviewed, and move the source slug into the frontmatter `sources` field.

**Publish (with citations) · search top-*k* by relevance × citation count · fetch by address — every one of the three presupposes that the message is text.** 2026-10 work on **latent inter-agent communication** puts a term on that presupposition rather than refuting anything above.

- **Swarm Telepathy / SwaT** (`arXiv:2610.15095`; MIT CSAIL + MIT-IBM Watson AI Lab; Alabdulkareem / Tenison / Zhang / Zhu / Katz / Gutfreund) is described as the **first cross-family** KV-cache transfer method — prefill-free communication between multi-family multi-agent systems, both sender and receiver **frozen** (<50M training tokens, <1 GPU-day). With KV-cache compaction it reports a mean **40%** higher accuracy and **4×** faster wall clock **than text-to-text**, across **17** benchmarks / **12** LLMs / **6** families.
- **CacheFuse** (training-free; linear interpolation of the upstream KV cache into the downstream model) reports up to **+8.6 percentage points** and **12.2×** TTFT over text-based inter-model communication.
- **The argument landed here is the one 10-17 already made about the memory store.** 10-17's load-bearing sentence was **"you cannot cite a vector"**, written about where memory lives. Same argument, new location: the **wire** instead of the store. Let the channel become a KV cache and the three operations have **no object** — and [[Provenance]], promoted on 10-17 from after-the-fact audit to **in-flight coordination**, finds itself promoted onto a medium **that cannot carry a citation**; this page's own cross-contamination failure likewise loses the interface needed even to ask *who said this line*.
- **The numbers also cut the other way** (the half worth keeping in view): if the channel described above really is the more faithful carrier, then the text channel's lossiness was doing unnoticed work. An auxiliary instruction placed **in the middle** of a long context is retained at **15.6%** in natural language vs **73.3%** via KV cache; under injected noise (10 irrelevant sentences) NL accuracy falls to **47%** vs KV **93%** (UIUC DREAM Lab, **Agent Primitives**).

🔴 **Boundary, not finding — this is the strongest line in this note.** **None of these papers discusses provenance at all.** The inference that citations become unstatable on a continuous medium is **this wiki's own extrapolation, not a measured result**, and must be written as a boundary. Nothing above claims ScaleMAS is wrong; it says its precondition has a shelf life.

⚠️ **Evidence grade.** SwaT's gains are measured against **text-to-text** communication, **not** against a strong text baseline with good summarisation; cross-family transfer is trained on **text-only** data and the vision-transfer result is a **demonstration**; CacheFuse's figures came through second-hand reporting. ⚠️ **The instruction-retention pair (15.6% / 73.3% / 47% / 93%) is the weakest-sourced number in this row** — the only return for it this round was an unrelated lifestyle-domain repost that traces back to UIUC DREAM Lab (corresponding author Haohan Wang). It is recorded as **an observation to chase, not a load-bearing citation**; replace it with a first-hand source before quoting these figures anywhere.

## Finding ≠ Fixing — the repair gap *(ledger row 10-19B; applied 2026-10-20)*

> **Draft annotation, pending ingest.** Not yet backed by a source page in this wiki — verified against live sources on 2026-10-19 (recorded in `.workbuddy/memory/concept-radar/2026-10-19.md`, candidate 2). Remove this banner when the material is ingested and human-reviewed, and move the source slug into the frontmatter `sources` field.

**Every mechanism on this page is a detector.** The verifier predicate, cross-contamination, protocol pivoting, substrate-centric coordination — all four answer *"did something go wrong, and can we tell?"*. **Not one supplies the next verb.** Two 2026-10 instruments opened that gap explicitly.

**CLASHarness** (`arXiv:2610.19128`, submitted **2026-10-13**; Yuxiang Lai et al.) — **600** multi-turn tasks × **15** frontier models in the computer-use domain; layered scenario planning plus an eight-step verification micro-pipeline; deterministic visual facts committed **before** rendering; the scorer compiled **from already-executed reference trajectories** ⇒ solvable by construction. Three findings:
1. Weak models follow misleading information; strong models consult visual evidence.
2. **Resolving conflict is far harder than detecting it** — agents *can* see the inconsistency, but **acting to correct system state significantly lowers task success**.
3. Frontier models still fail **>58%** of **closing actions** — forgetting to release a shared lock, forgetting to hand off.

- 🔴 **Why this bites this page specifically:** the wiki's standing advice — *verify a peer's output before inheriting it* — is, in that benchmark, **precisely the step that lowers the score.**
- **The 58% is not a mechanism verb at all — it is protocol hygiene** (release the lock, hand off the task): a class for which this wiki has **no page and no line**.

**ARIA** (`arXiv:2610.20780`, submitted **2026-10-14**; Bolin Shen / Yushun Dong; code `github.com/LabRAI/ARIA`) — the **first** large-scale dataset pairing failed trajectories with **execution-verified repairs** (**24,000+** trajectories → **3,953** pairs), retained only when **the repaired run passes and the unmodified control fails**; three-stage training (SFT → preference learning → policy optimisation). The resulting **7B** model reports **SOTA repair accuracy both during execution and post-hoc, beating zero-shot frontier models.**
- ⇒ ARIA is a candidate repair apparatus for the gap 10-16A / ToFu exposed (*the model's refusal arrives after the tool has already returned*): it is explicitly about intervening **while execution is still in flight**.

**Why this is the missing half of this page, not a new topic:** since 2026-09-26 this page has been entirely **discovery-side** (verifier as precondition; contamination as the new failure surface). This section is its second half — the same rationale as 10-17C: **splitting them across pages would let the two halves of one page drift.**

**Boundaries.** vs **第十三条（见 `.workbuddy/memory/concept-radar/SCAN-LINES.md`）** — that line asks *does an existing verb actually work* (`DELETE` never measured; a technique works on half its objects); this row asks ***does the verb exist at all*** (repair was never written down). Parallel rows that must name each other, or they read as duplicates. vs **[[HumanInTheLoop]]** — that page is the wiki's **only** chain with a verb *after* detection (grade → gate → idempotent execution → audit); this row belongs **next to it**, and together they prove the wiki has had the "detect + follow-up action" shape all along — it simply implemented it in exactly one place. vs **[[MemoryGovernance]]** — the four actions are **memory**'s verb inventory; this is the **execution** side's missing one ⇒ the wiki did a verb inventory on memory and not on execution. vs 10-16A ToFu — ToFu is detection that fails to change execution; ARIA is a candidate fix for precisely that.

⚠️ **Limits, must sit beside the conclusion.** CLASHarness is a **generative** benchmark limited to computer-use; "resolving is harder than detecting" holds **on that construction's distribution**. ARIA's numbers are **author-reported**; its generalisation claim is "frameworks and host models unseen in the training pipeline"; and "**7B beats frontier**" is a **repair-specific** claim, **not** a general-capability one. ARIA's preconditions (exposed execution traces + support for continuation replacement) are themselves **deployment constraints** — **none of [[AgentHarness]]'s four duties promises either.**

**Structural recommendation (recorded here, not executed):** `overview.md`'s Cross-Cutting Themes should gain a line — *"this wiki's mechanism inventory is discovery-side; a repair-side inventory should be maintained in parallel."* Per the standing convention `overview.md` is revised **on ingest only**, so this awaits the next ingest or explicit authorisation.

## Why It Matters
- **It is the wiki's first "between agents" page.** All 39 prior pages and both connection diagrams describe a single agent; this page opens the space dimension the wiki had never covered.
- **September 2026 assembled three grades of evidence at once:** a reproducible experiment (team@k vs best@k, Microsoft Research + UC Berkeley), a product entry point (Anthropic's Claude Code Projects: coordinator → parallel cloud threads → shared memory → ordinary merge conflicts, with honest self-declared limits — quota per thread, cloud-only launch, CI/tests/human review as the integration boundary), and decentralised scale (Agensh: 1,024 agents, no central orchestrator, pandoc 33.89% → 55.06%). The question moved from *can multi-agent work* to *when is it worth it and who pays the coordination cost*.
- **The verifier predicate is portable.** "First find a cheap way to judge correctness, then form the team" is the single most reusable sentence in the material.
- **Evidence-grade honesty:** the team@k numbers are secondhand (AlphaSignal's report of the paper; arXiv not opened), Agensh is secondhand, Claude Projects' shared memory has "no detailed performance evaluation" — direction-and-magnitude grade throughout; verbatim citation requires the primary sources. **Still true after 2026-10-16:** the collaboration *gain* remains un-verified first-hand; what changed is that the authorization-inheritance *failure* now carries CVE numbers — **the failure surface has better evidence than the benefit it is meant to bound.**

## See Also
- [[multi-agent]] — source
- [[Compaction]] — whose clean-window-subagent note this page promotes from footnote to mainline
- [[Provenance]] — extended by cross-contamination: peer conclusions need verification status
- [[AgentHarness]] — multi-agent as a productised harness capability (subagent scheduling, duty ④)
- [[ContextEngineering]] — intra-window placement vs inter-window exchange
- [[Agent]] — the single-agent world this page extends
- [[Anthropic]] · [[OpenAI]] — the two productisation paths (Projects coordinator; Agents API subagent flag)
