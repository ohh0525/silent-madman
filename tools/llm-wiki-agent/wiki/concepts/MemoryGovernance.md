---
title: "Memory Governance"
type: concept
tags: [agent-memory, memory-governance, memory-lifecycle, forgetting, learned-policy, intrinsic-evaluation, scoped-revision, owner-attribution, protection-descriptor, discarded-column, memory-pricing, deletion-closure, upstream-invalidation, capture-feedback-loop]
sources: [memory-lifecycle, agent-memory-provenance]
last_updated: 2026-10-26
---

# Memory Governance

The discipline of treating an agent's durable memory **not as a store but as four actions that each fail differently** — Capture → Update → Recall → QA — and of answering, explicitly, the question every design otherwise answers by accident: **who holds the decision rights over what is written, when it is retrieved, and when it is deleted.**

Distinguish it from the two neighbours it is most often confused with: [[LongTermMemory]] asks *where does durable state live and how is it read credibly*; Memory Governance asks *how does it change over time, and under whose authority.* The framing question is not “can we store it?” but **“when should we let it be forgotten — and who is allowed to decide?”**

## The four actions (per [[memory-lifecycle]])
| Action | What it does | Characteristic failure |
|---|---|---|
| **Capture** | Write new memories out of this session | Systematically **low recall** — the thing you changed last week never got written |
| **Update** | Reconcile with the existing bank | **Coexistence instead of supersession** — two publication dates side by side, and the agent argues with itself |
| **Recall** | Select entries that are still valid | **Incomplete recall** — one of three relevant memories comes back |
| **QA** | Answer from the evidence | Answer looks right while the bank underneath is broken |

The reason to split them is diagnostic: an **end-to-end QA score stirs four different qualities together**. A correct answer can come out of a broken bank (lucky); a wrong answer tells you nothing about *which* stage to repair. [[DyadMem]] is the benchmark that makes the four stages separately measurable — and its headline result is a **measurement artefact, not a model ranking**: frontier models are strong **given gold memory**, and collapse once they must run the **full pipeline** themselves.

## Update can be triggered upstream — nothing in the bank has to change *(ledger row 10-26A; applied 2026-10-26)*

> **Draft annotation, pending ingest.** Not yet backed by a source page in this wiki — verified against live sources on 2026-10-26 (recorded in `.workbuddy/memory/concept-radar/2026-10-26.md`, candidate 1; ledger row **10-26A**). Remove this banner when the material is ingested and human-reviewed, and move the source slug into the frontmatter `sources` field.
>
> 🔴 **Preprint, not peer-reviewed. `62%` is measured on the authors' own synthetic world generator (Fallout); Tether's `0.3%` holds only when the dependency relation and the verdict are supplied in the same session — spread across sessions it degrades to 9.4–22.1%.**

**The trigger this page's four actions have never had.** Every row of the table above fires on **an event at the record**: Capture on something new, Update on a reconciliation with the bank, Recall on a selection, QA on an answer. ⇒ **the four actions share exactly one kind of trigger, and it is always "somebody did something to this memory."** **None of it is refuted.** What is displaced is that the table has no cell for an invalidation that **is not an action on a memory at all**.

**Tether** (`arXiv:2610.25123`; Yiqi Wang et al., 8 authors; cs.CL; v1 **2026-10-18 09:01:52 UTC**, v2 **2026-10-22**). A signing key is revoked; the verdicts built on it should fall with it; **the announcement names only the key**, and those verdicts never share a retrieval window with it.

- An agent reading **atomic-fact memory** republished **62%** of the objects that should have been voided upstream — **every one of those records true when written**, and **no memory was edited, deleted or touched** to produce that failure.
- **Tether** records at write time the exact version each conclusion depends on, and withdraws the whole record at read time if anything supporting it has lapsed anywhere in the store ⇒ **0.3%**, with **37% fewer verification calls** than re-verifying everything.
- For scale: **A-Mem / Graphiti 9%** (**0.83–0.86** checks per candidate); **Mem0 42%**; *"clear everything on any lapse"* equally safe at **+32% checks**.

> ⇒ **`UPDATE` acquires a second trigger.** Not only *"somebody changed this memory"* but ***"something this memory depends on lapsed"*** — and the second trigger does not arrive as an event on a record, so a pipeline that only polls records cannot see it.

**What this does to the table above.**
- **Update** gains a trigger with a different provenance — a **dependency edge**, not a write. ⇒ the Update row's characteristic failure (*coexistence instead of supersession*) is now only **half** the column; the other half is **"there is still only one entry, and it should no longer be believed."**
- **Recall** is where it becomes visible: the agent retrieves a record that is **locally perfect and globally void**.
- **QA** is where it is scored as correct — which is exactly why the four-action split does not surface it: **no single stage is wrong.**
- ⇒ **The prior question for the whole table:** is the dependency graph enumerable? If it is not, no trigger can be computed and `UPDATE` silently degrades to *"wait until somebody rewrites it."* (Same applicability shape as this page's scope note on enumerability, ledger row 10-17A — reached here from the **trigger** side rather than the audit side.)

**Boundaries (do not merge these).**
- **vs ledger row 10-25B (`DELETE` closure, this page)** — that row **has an action** and asks whether its closure is complete; this row has **no action**. Sequential questions: first *"was anything done?"*, then *"what propagates when nothing was done?"* ⇒ **split columns.**
- **vs ledger row 10-24A (AMV-Guard)** — **upstream / downstream, read in that order.** AMV-Guard prices *whether this premise is worth re-verifying given your next action*, which **presupposes that an invalidation signal arrived**; this row shows that in the *announcement names the key* shape **nothing arrives** ⇒ **arrival first, pricing second.** ⚠️ **10-24A is still a ledger suggestion, not a landed section** ⇒ this cross-reference is **row-to-row** until it lands.
- **vs the FAMA penalty above** — FAMA penalises reliance on **deleted or superseded** memories, i.e. it scores **the reader**; this row shows the **store** can be clean by every such score and still feed a voided conclusion. Complementary, and this one is the prior condition.
- **vs ledger row 10-24B (governed-state corruption)** — that row's **control plane was modified**; here **nothing touched the control plane**.

**Scan-line assignment / paired landing.** **Line 19 — composition audit** (see `SCAN-LINES.md`): per-record review passes, the closure fails. Its paired landing is [[Provenance]]「Invalidation is non-local, dependency is local」, which supplies the **traversal** this trigger has to follow.

⚠️ **Evidence grade, must sit beside the numbers.** Preprint, **not peer-reviewed**; **Fallout is the authors' own synthetic world generator**; **0.3%** conditional on **same-session relations**, degrading to **9.4–22.1%** across sessions; authors self-report degradation with **weaker writers**. **62% is not a production staleness rate.**

## Recall rewrites the input to Capture — the pipeline has no return edge *(ledger row 10-26C; applied 2026-10-26)*

> **Draft annotation, pending ingest.** Not yet backed by a source page in this wiki — verified against live sources on 2026-10-26 (recorded in `.workbuddy/memory/concept-radar/2026-10-26.md`, candidate 3; ledger row **10-26C**). Remove this banner when the material is ingested and human-reviewed, and move the source slug into the frontmatter `sources` field.
>
> 🔴 **Simulated users, not real ones; "leakage" is an inference-accuracy proxy, not a recorded leakage incident; the four support models are not named; the repair is one instruction whose robustness was never tested.**

**The edge this page's pipeline does not have.** Capture → Update → Recall → QA is **one-way**: each stage consumes the previous one's output, and **no stage feeds an earlier one**. **None of it is refuted.** What is displaced is the assumption the diagram makes by drawing no arrow back: **that Capture's intake is produced by the world, not by the system's own Recall.**

**Disclosure Begets Disclosure** (`arXiv:2610.28315`; Masahiro Kaneko · Hiromi Arai · Timothy Baldwin). Simulated users holding **24** personal attributes talk to a support agent **with vs without memory**, across sessions; attributes are inferred from the **full accumulated record**; **4 support models**:

- memory raises reply **quality** and **empirical leakage** **at the same time**, and the gap **widens with each further session**;
- **the mechanism is entirely non-adversarial** — a memory-conditioned reply brings an earlier value out as a **presupposition**, the user confirms it or does not correct it, and **the cue plus the agent's own guess become the recorded value** ⇒ the loop **reinforces itself**;
- **the load-bearing measurement:** deleting the agent's mention of one attribute reduces its **later** leakage by **about twice** what a single-turn effect would predict ⇒ the damage lives **in the loop, not in the turn**;
- **the user cannot walk out of it:** correcting a value **discloses** the attribute; refusing to discuss it pushes later predictions toward **more sensitive** values; an uncorrected wrong value **settles**.

> ⇒ **Recall changes what Capture will next be given.** Nobody wrote anything, nobody attacked anything, the user was present throughout — and the store still ended up holding a value the system produced itself.

**Consequence for the four actions.**
- **Capture is not an independent stage.** Part of what it captures was generated by Recall ⇒ alongside *"the thing you changed last week never got written"* there is now ***"the thing that did get written was manufactured by an earlier read."***
- ⇒ **The missing return edge is currently unowned.** Neither `UPDATE` nor `QA` asks *did this value come from the user, or from our own previous answer?* — so a write nobody authorised is still recorded as a fact with an owner.
- **The repair lands on the reply side, not the storage side.** Instructing the agent **not to state or presuppose** user attributes returns leakage to **the no-memory level while keeping most of the quality gain**; filtering / anonymising *what the user said* or *what is stored* **gives up most of the gain** ⇒ **a measured payoff for the [[Abstention]] side of the house (不陈述), which is the first time that page's advice has a number attached to it.**

**Boundaries (do not merge these).**
- **vs [[MemoryPoisoning]]** — that is the **third decider**: *an attacker* writes. This row has **no attacker**; it is **"nobody decided, and it was recorded anyway."** ⇒ **Do not read it as a fourth decider**; read it as a **decider-less write**.
- **vs ledger row 10-25A (Mosaic Effect)** — that is a **one-shot** event (the refusal itself carries the prohibited conclusion); this is a **cross-session accumulating loop**. This row **has a repair**; 10-25A's numbers are harder. Split columns.
- **vs the FAMA / "failed to forget" machinery above** — that scores reliance on **deleted** content; here nothing was deleted, and the content is being **actively re-created**.
- **Cross-reference 🎯 ledger row 10-09「常驻上下文与指令预算」** — the repair is exactly a claim about *what a resident context must not carry into a reply*, i.e. the question that row has been asking for **17 days**.

**Scan-line assignment.** Reported as an instance of **line 15 — granularity audit** ("does this number survive a change of observation scale?"): measured **per turn** the loop is invisible; measured **per session** it is about **2×** larger. Recorded in `.workbuddy/memory/concept-radar/2026-10-26.md` §三 as **not** warranting a new scan line.

⚠️ **Evidence grade, must sit beside the numbers.** **Simulated** users; leakage = **attribute-inference accuracy**, not a leakage event; **4 support models unnamed**; the repair is a **single instruction** with untested robustness; a **single protocol**; no independent replication.

## Forgetting is a capability, not a failure
- **“Failed to forget” is now a deductible score.** Memora's **FAMA** = recall score − **stale-dependency penalty** (it explicitly penalises reliance on deleted or superseded memories). This turns *“the agent is quoting a superseded runbook as current”* from rhetoric into a number.
- **The opposite failure must also be measured.** **Unsafe deletion** — removing a fact that is still under reference — is the other end, and DyadMem quantifies both.
- **Retention is per-type, never one global TTL.** The three stores [[LongTermMemory]] defines do not expire alike: episodic (high volume, timestamp-bound, expires first) → semantic (durable; the main **merge** target) → procedural (lowest volume, highest value, retained longest, hardest to prune).
- The sharpest seam: **deletion vs [[Provenance]]**. Provenance wants every fact to keep origin + time + evidence so it stays auditable; the right to erasure wants the same fact removed at the root. Deleting it **breaks the citation chain** — so the deletion itself must leave a trace (a receipt, a failure list, a rollback-capable snapshot).

## The load-bearing variable: who decides
There are exactly three classes of decider, and picking one is the design decision that matters.

| Decider | Write / retrieve / delete | Representative evidence | Core weakness |
|---|---|---|---|
| **Human-written rules** (today's default) | Thresholds, TTL, extraction counts, top-k hard-coded by an engineer | Layered memory (resident core + external retrieval + explicit forgetting policy) is the 2026 production form | Rules have **no judgement about what counts as stale**; every new domain needs re-tuning |
| **Trained policy** (2026's new answer) | **ADD / UPDATE / DELETE / NOOP placed in the action space**, trained by RL on task-success reward | Memory-R1 (152 QA pairs ⇒ LoCoMo F1 **+68.9%** vs Mem0); ATMem (cost-aware reward + STR-GRPO; **76.6%** on AndroidWorld at ≈**1/29** the parameters) — six independent teams | **None deployed in production**; benchmarks exclude distribution shift and adversarial input; no single system owns write + retrieval + transformation |
| **Attacker** (the decider nobody wants) | Write timing and content chosen by the injector | **PMPA** and **Darktrace** — see [[MemoryPoisoning]] | **The fix is vendor-side**, so the defending operator cannot deploy it |

> **The rule that makes this page worth having: if memory has no owner, the owner slot does not stay vacant — it flows to whoever wants to exploit it.**

The middle row is why this is a *2026* page: the whole point of putting `DELETE` **into the action space** is that *“when is this stale?”* stops being a hand-tuned constant and becomes a learned decision that the task-success reward can correct.

## The four governance bottom lines
1. **Auditable** — every write / supersede / delete traceable like a git commit (who, when, on which source). This is [[Provenance]]'s instinct, applied to *change* rather than to *storage*.
2. **Rollbackable** — deletion is a real, recorded, provable operation with a version history, not an invisible manual sweep of an undocumented store.
3. **Permissioned** — **who may write to shared memory** managed as explicitly as database permissions (this is the *governance* half of the wiki's long-open “multi-agent shared memory” question).
4. **Signature-verified** — against forged-history attacks the only root fix is **cryptographically signed model replies validated server-side every turn**. Until that ships, the local session-history store must be treated as a **security-sensitive file**.

Bottom lines 1–3 govern *your own mistakes*; bottom line 4 governs *someone else's malice*. **The reliability discipline and the security discipline merge at the memory layer** — which is why [[MemoryPoisoning]] is a decider in the table above rather than a separate topic.

> **Scope note — where the four bottom lines stop applying *(added 2026-10-17, ledger row 10-17A)*.** All four are written against a bank that is **enumerable**: auditable = *which entry changed*; rollbackable = *restore that entry*; permissioned = *who may write that entry*; signature-verified = *that entry's origin is signed*. **Remove enumerability and three of the four lose their conditions of statement** — only *signature-verified* survives, because signatures attach to the write, not to the entry. Concretely: **latent / soft-token memory** (see [[LongTermMemory]]「The third carrier」) stores state as learned vectors or merged weight updates with **no address** ⇒ you cannot audit *which* memory changed, roll back *that* memory, or grant permission *per* memory. **This is not a counterexample to the bottom lines; it is their boundary.** The design consequence is a new prior question, to be asked *before* the four: **is the thing being governed addressable at all — and if not, what replaces the audit?** A candidate replacement, currently untested: govern the **write event** (who/when/source, plus a pre-write and post-write behavioural diff) instead of the entry, since write events remain enumerable even when the stored state does not.

> **Refinement from the ownership side *(added 2026-10-21, ledger row 10-20B; draft annotation, pending ingest — see the banner below)*.** Bottom line 3 **Permissioned** — *who may write to shared memory* — is stated only for a bank that has **lines**. The audit behind ledger row 10-20B makes the dependence explicit: marking the owner **before or within each credential line** drops credential misuse from **92/305** paired runs to **1/305**, and the reason it works is that there **is** a line to carry the label. On a continuous carrier there is no line, so *Permissioned* has nothing to attach to ⇒ **the same applicability boundary as the scope note above, reached from the defence side rather than the audit side.** (Cross-reference [[MemoryPoisoning]]「Exposure ≠ Behaviour ≠ State」, and ledger row 10-17A.)

> **The mechanism bottom line 3 has been missing *(added 2026-10-21, ledger row 10-21A; draft annotation, pending ingest — see the banner above)*.** Until now *Permissioned* has been a **principle**. **ClawMMU** (`arXiv:2610.28093`, submitted **2026-10-20 12:09:53 UTC**; MPI-SWS · EPFL · Aarhus · Toronto) makes it four **structural fields carried by every representation of every memory** — **owner** (who produced it) · **scope** (which tasks and sessions may use it) · **origins** (which pages it was derived from) · **authority** (what it may justify, on an ordered ladder: **Evidence** lowest = tool output / web retrieval, *read but never act on* → user preferences / a teammate's instruction file → **Policy** highest = the user's own message) — plus an inheritance rule that is the load-bearing sentence: **take the minimum authority among inputs, and count the model itself as the lowest-authority input** ⇒ **a memory the model wrote for itself is always Evidence, and only its owner can raise it**. Checking is enforced where content crosses a boundary, four times: **map** (entering context) · **derive** (being written to storage) · **reload** (being retrieved or restored) · **authorize** (driving a tool call, per argument).
> - **Consequence for this page:** *Permissioned* stops being “manage write rights like database permissions” and becomes “**every memory carries who-may-do-what, and the harness re-checks it every time it crosses a boundary**”. Two further notes for the bottom lines above: **(a)** bottom line 4 *signature-verified* is **not sufficient by itself** — `reload` needs a **revocation counter** to catch use-after-revoke; **(b)** the verdict depends **only on where content came from, not on what it says**, which is why the claim is that the attack is caught **even when the model is fooled**.
> - 🔴 **Status — design, not result:** Appendix C states verbatim *“ClawMMU is not yet implemented”*; the paper carries **no measured numbers** (§5 lists planned evaluations only), is a **6-page non-archival workshop paper** (AgenticOS @ NeurIPS 2026), and leaves **four open items**: scaling human review of capability schemas · where authority sits under multi-agent · actions already taken before a revocation · auditing approval-scope widening. ⇒ **Record as the shape this cell could take, never as evidence that it works.** (Cross-reference [[HumanInTheLoop]]「The Gate Does Not Know Where Its Arguments Came From」, and [[Provenance]].)

## Deletion is not closed at the record layer — `DELETE` needs closure semantics *(ledger row 10-25B; applied 2026-10-25)*

> **Draft annotation, pending ingest.** Not yet backed by a source page in this wiki — verified against live sources on 2026-10-25 (recorded in `.workbuddy/memory/concept-radar/2026-10-25.md`, candidate 2; ledger row **10-25B**). Remove this banner when the material is ingested and human-reviewed, and move the source slug into the frontmatter `sources` field.
>
> 🔴 **62–99% is measured on secrets constructed to be splittable, on 7B-class models. It is not a production leakage rate.**

**The clean failure this page's `DELETE` currently permits.** The four-action table above grades `DELETE` at the **record layer**: was the entry removed? **AfterDeleteBench** (`arXiv:2610.31366`; 25 pp / 7 figs / 12 tabs; cs.CR + cs.CL + cs.LG) shows that grading is compatible with total failure. Each synthetic secret is tested on an agent **exposed and then deleted** against a **paired never-exposed control**:

- **one query** recovered the deleted secret in roughly **two-thirds** of cases from **Qwen2.5-7B-Instruct**; the never-exposed control recovered **zero** ⇒ the recovery is attributable to the exposure, not to guessing;
- **no verbatim copy needs to survive** — with the full secret string already gone and only **separately stored components** remaining, the **combination rule public**, exact reconstruction succeeds **62–99%** across **Qwen / Mistral / Phi-3**.

> ⇒ **`DELETE` can be judged "correctly executed" — the record is genuinely gone — while the secret remains 100% reconstructible.** The four-action model has no column in which that failure is visible.

**What this does to the four bottom lines above.** Bottom line 1 **Auditable** is currently written as *"every write / supersede / delete traceable like a git commit (who, when, on which source)"* — i.e. it audits **the record that changed**. A deletion can satisfy that sentence completely and still leave the content fully recoverable from what it produced. ⇒ **Auditable must additionally require that the derivation relation be enumerable**: for any deleted record, the system must be able to list **what was derived from it**, and those descendants must be inside the same closure. Without that, `auditable` certifies the ledger and not the erasure.

- ⇒ **`DELETE` acquires a second success criterion.** Not only *"the record is gone"* but ***"nothing derived from it still licenses the same conclusion"*** — closure semantics, not record semantics.
- **The two candidate repairs, and why only one is a repair.** **Provenance-aware closure** (delete derived records together with the source) **eliminates the observed recovery**. An **exact-literal write filter** (block verbatim re-insertion) blocks re-insertion but **does not erase information already present in the system** ⇒ it is a **containment**, not a deletion, and must never be recorded as one.
- **Where the pointer has to come from.** Closure traversal needs a **forward** provenance pointer (source ⇒ descendants). [[Provenance]] has only the **backward** one (descendant ⇒ ancestor) — see that page's「Provenance must be reversible」section, filed as the other half of this row.

**Boundaries (do not merge these).**
- **vs ledger row 10-18A (Bemula / MemCut)** — that row asks **"was the deletion request executed at all?"** (end-to-end ≤1.5%; 39–76% residue after removing the direct-disclosure sentence) ⇒ **scan line 13**. This row **grants that execution succeeded** and asks about derivations ⇒ **scan line 19**. **Sequential questions; never one.**
- **vs ledger row 10-24B (governed-state corruption)** — **mirror images**: 10-24B is *"content all present, the subset selected to take effect was swapped"*; this row is *"source gone, the derived subset still in effect."*
- **vs the "Failed to forget" penalty above** — FAMA penalises reliance on **deleted or superseded** memories, i.e. it scores the *reader*; this row shows the *store* can be clean by that score and still leak. Complementary, and this one is the prior condition.

⚠️ **Evidence grade, must sit beside the numbers.** Synthetic secrets **constructed to be splittable**; **7B-class** models ⇒ **99% must not be read as a production leakage rate**. Provenance-aware closure was measured **in a setting that had a positive control recovery** ⇒ it does not establish that a given deployment has that oracle. Preprint; **no independent replication**. *One methodological note travels with the whole row:* **the response interface is part of the measurement system** — a deletion audit reporting clean may be measuring its own parser.

## "Right answer" ≠ "right memory" — intrinsic vs extrinsic evaluation *(added 2026-10-17, ledger row 10-17B)*

> **Draft annotation, pending ingest.** Two draft annotations below (this section and the open experiment) are **not yet backed by a source page in this wiki** — verified against live sources on 2026-10-17, recorded in `.workbuddy/memory/concept-radar/2026-10-17.md` (candidates 1–2; ledger rows **10-17A / 10-17B**). Remove this banner when the material is ingested and human-reviewed, and move the source slugs into the frontmatter `sources` field.
A **third** annotation was appended *inside* the open experiment below on 2026-10-21 (ledger row **10-20A**, verified 2026-10-20, recorded in `.workbuddy/memory/concept-radar/2026-10-20.md` candidate 1), and a **fourth** as the scope refinement after the four bottom lines (ledger row **10-20B**, same report candidate 2).

**The instrument's own target.** This page's headline result — *gold-memory strong ⇒ full-pipeline collapse*, and [[DyadMem]]'s staged scores — is measured with **downstream QA accuracy** as the proxy for memory quality. **FEB-30** (`arXiv:2610.22209`, **2026-10-15**; Sebastian-Antonio Toma / Jean de Kernier / Mike Ply / Oliviu Matei; 14 pages; code and data at `github.com/amazon-science/feb-30-benchmark`) argues that proxy **conflates memory correctness with retrieval and generation quality** ⇒ **a right answer can mask a broken bank**, and **a wrong answer can convict a good one**.

- **Method — a paradigm inversion.** Rather than labelling documents, it **generates documents backwards from known fact trajectories**, yielding **deterministic ground truth with no human annotation**: **30 fact-evolution trajectories × 6 diagnostic categories × 3 difficulty levels**. Each trajectory dictates how one fact should evolve **across multi-author artifacts** (documents / mail / conversation) ⇒ the memory store's **body can be opened and inspected after every single ingestion**.
- **Results.** Intrinsic and extrinsic evaluation **diverge by 16 percentage points on average**; **44%** of trajectories exceed the meaningful-divergence threshold; of the four memory operations (create / update / reinforce / **supersede**) **only 20% are judged correct** — and that failure is **completely invisible to extrinsic evaluation**. Failure modes differ systematically by category and difficulty.
- **Why this is a seam on *this* page and not a new topic.** FEB-30's operation taxonomy is nearly isomorphic to the four actions above (Capture / Update / Recall / QA) and to the trained-policy branch's **ADD · UPDATE · DELETE · NOOP** ⇒ **this is the first instrument that scores the operation layer directly**; everything before it had to infer the bank's state from the answer. It also sharpens `overview.md`'s open question ("Cluster F evidence is entirely author-reported; needs independent reproduction") into a harder form: **reproduce whether the ruler can see the failure, before reproducing the numbers.**

**Boundaries.** vs [[DyadMem]] — that page supplies the **measurement skeleton** (Capture/Update/Recall + per-stage gold labels); this section critiques **the act of measuring itself**. vs ledger row 10-08「评测的评测」(`arXiv:2610.07274`, only **22.6%** of records pass four checks) — that row calibrates **the agent's score**; this row calibrates **the memory's operations**: the same metrology problem one layer down, **not a repeat page**. vs [[CitationLock]] — that page governs *what an answer may cite*; this governs *whether the object judged is the answer or the store's body*. vs ledger row 10-13「检索准入」— that row is the **read** side (semantically relevant ≠ usable now); this is the **write** side.

⚠️ **Limits, must sit beside the conclusion:** demonstrated on a **single "representative" memory system**, **not a cross-system universal result**; 30 trajectories is a small scale; published days ago with **no independent replication**.

### The open experiment these two rows define *(10-17A × 10-17B)*

**One action, not two.** Point FEB-30's instrument — *fact evolution, with the store's body inspected after every ingestion* — at a **continuous / latent memory**. **No paper has done this**, and it is the place where compressed continuous storage is most likely to break on first principles: with no enumerable entries there is **no interface for "which older fact is being superseded"**, so `supersede` — the operation FEB-30 already finds correct only **20%** of the time in *addressable* stores — has nowhere to be performed at all.

- **Predicted outcome (a hypothesis, not a result):** extrinsic scores stay competitive while intrinsic correctness collapses, i.e. the **16-point divergence widens** precisely where the numbers look best. That would make the divergence **a property of the carrier**, not of the system under test.
- **Why it is worth doing here rather than anywhere else:** it is the only experiment that simultaneously tests this page's scope note (does governing **write events** replace governing entries?) and [[LongTermMemory]]'s load-bearing sentence (**you cannot cite a vector** — is that merely a citation problem, or also a *correctness* problem?).
- **Minimum viable form:** take one FEB-30 trajectory set; run it through an addressable store (baseline) and a soft-token store (Memorilla-style or REMORY-style) at matched input budgets; score **both** intrinsically and extrinsically after each ingestion; report the divergence, not the leaderboard.
- **The first half-leg of that experiment now exists *(added 2026-10-21, ledger row 10-20A; draft annotation, pending ingest — see the banner above)*.** **ScopeMem** (`arXiv:2610.26503`, submitted **2026-10-19 14:38 UTC**; Zhicheng Zheng / Cheng Zhang / Shengping Yu / Tianxiang Zhao; 13 pp / 5 figs / 9 tabs) puts a learned **prefix** memory in front of a **frozen VLM** on GUI-agent tasks, and its ablation inverts the natural attribution: **the gain from latent memory comes mainly from *revision of the model's default action*, not from “history encoded into the prefix”.** That revision is **unscoped** — step-wise cross-entropy training pushes the output toward the reference action **at every step**, with no term that explicitly preserves decisions already correct ⇒ **it repairs errors and damages 8–13% of answers that were already right**. The authors' own sentence is the load-bearing one: **“Overall accuracy metrics hide these losses.”**
  - **New variable for this page: 修订是否有作用域 — scoped vs unscoped revision.** The counterfactual is not “do not revise” but “**revise with a scope**”: conditioning the encoder on **the model's initial answer** and training it to correct errors **and** preserve correct decisions drops damaged correct decisions to **5.6%** on the authors' controlled ablation set, **while repairing more errors than any CE-trained prefix tested**. ⇒ the Update action above acquires a fourth property beyond *whether* it happened: **did it carry a scope?**
  - **Why this is a foothold and not yet a result for the experiment above:** FEB-30 shows **extrinsic** evaluation cannot see **intrinsic** operation failure in an *addressable* store; ScopeMem shows **aggregate** accuracy cannot see **per-decision** revision loss in a *continuous* one. Same sentence, second landing — which lets the experiment's hypothesis be stated harder: **if the aggregate score is a property of the *granularity*, then the extrinsic/intrinsic divergence should widen on the continuous carrier, and should widen precisely where the aggregate number looks best.** (The granularity question itself is scan line 15 — see `SCAN-LINES.md`.)
  - ⚠️ **Limits:** **5.6%** is on the authors' own controlled ablation set; **8–13%** is measured for **CE-trained prefixes**, not for latent memory in general; every result is GUI-agent tasks on a **single frozen `Qwen3-VL-8B`**; submitted **2026-10-19** with **no independent replication**; transfer to general agents is the authors' own stated loading claim.

## The discarded column *(ledger row 10-22B; applied 2026-10-22 — ⚠️ weak evidence, deliberately down-weighted)*

> **Draft annotation, pending ingest.** Verified against live sources on 2026-10-20/21, recorded in `.workbuddy/memory/concept-radar/2026-10-22.md` (candidate 2). Remove this banner on ingest; move the slugs into frontmatter `sources`.
>
> 🔴 **Ruling recorded with this section: this row is filed as a BOUNDARY, not as a load-bearing conclusion.** The only number likely to be quoted from it (**99%**) is **n = 1** — one conversation, one run per cell, single author. **It must never be cited as "memory is useless."** The honest citation is: **"where the model can search for itself, the marginal benefit of designed memory needs to be re-priced."**

**The gap.** This page's load-bearing claim is that the bottleneck is the **quality of the four actions** (Capture → Update → Recall → QA). Two same-week, independent papers arrive at a **different variable**: the bottleneck is **the model that writes the memory**, and **what the act of compression throws away**. The four actions have **no column for "the discarded thing"** — nothing here measures it.

**Evidence 1 — MemDev-Bench** (`arXiv:2610.27524`, submitted 2026-10-20 02:39:26 UTC; 12 authors). **4,869** executable history tasks / **555** base tasks / **22** repositories / **4** languages, **annotated for relevance** (the increment over prior benchmarks).
- **(i)** memory does help the tasks that fail without it, and the gain comes from **finer-grained localisation and editing**;
- **(ii)** memory also **makes solvable tasks fail** — **even when the retrieved history is relevant**, amplified by irrelevant history ⇒ the cause is **the agent reusing memory without re-assessing whether it applies**;
- **(iii)** **giving the raw history trajectory directly reduces step count significantly versus giving a memory system** ⇒ because **compressed memory tends to discard the process information the agent was actually reusing**.

**(ii) is a failure mode the four actions do not contain** — not *"the memory is wrong"* but **"the memory is right and the context is wrong"** (a **Recall**-side failure).

**Evidence 2 — MemoryTax** (`arXiv:2610.29823`, submitted 2026-10-21; Zedong Peng). ⚠️ **Directional support only.** One LoCoMo conversation (**419 turns / 152 questions**) × four memory methods (full context / BM25 / Mem0 / Zep) × three coding agents × three models, costed line by line. ⇒ *"Agent memory is a costly patch for a weak model"*: Mem0 beat full context **only on GPT-4o-mini**, and **building the index alone cost more than one entire round of full context**; and *"a ceiling, set by the model that writes it: a stronger reader does not recover what a weaker writer left out."*

🔴 **Why it is down-weighted:** **n = 1** — *"a short empirical study, with one conversation and one run per cell"* (author's own words). The author further notes the lead comes partly from **figure captions only the agent could read**: after removing the **88** image-bearing questions, the leading agent and full context differ by **one answer**. ⇒ The 99% figure is not evidence about memory in general.

**The pricing angle.** Mem0's index-build cost exceeding a full round of full context makes this the **first instrument able to put a price on scan line 4** since 2026-10-09 — the one thing this page's four actions never charged for.

**Boundaries (do not merge these):**
- **vs 10-21B (cache engineering)** — that row says *"rewriting text invalidates the downstream cache ⇒ context engineering reflexively manufactures its own cost"*; this row says *"compression discards process information ⇒ retaining the raw history is cheaper."* **Two opposite ends reaching the same verdict. Filed adjacently, mutually named, not merged.**
- **vs [[LongTermMemory]]'s third carrier** — that row asks *"what if memory is not addressable"*; this one asks **"is addressable compression worth it at all"** — the opposite direction.
- **vs [[Compaction]]'s 10-22A section** — that row shows a case where **discarding the original is exactly what enables the attack**. The two rows are **in tension, not agreement**: here retention is cheaper, there retention is safer. **Both are filed; neither is resolved.**

## Boundaries
- **vs [[LongTermMemory]]** — that page is the **first half** of a memory's life (store it, split it by purpose, read it credibly); this page is the **second half** (update, forget, decide). Neither subsumes the other: you can have a perfectly sourced bank that is also a governance disaster. *(Its 2026-10-17 section「The third carrier」is this page's **applicability boundary**: non-addressable latent memory is where the four bottom lines below stop being statable.)*
- **vs [[Compaction]]** — compaction is **inside** the window, per turn, lossy; governance is **outside** it, across sessions, offline, and does not participate in the current inference turn. Adjacent in one direction only: anything compaction drops that still matters should *land in long-term memory rather than evaporate*.
- **vs [[Provenance]] / [[CitationLock]] / [[Abstention]]** — those are **entry and exit discipline** (writes carry origin; cite only what you opened; abstain without sourced evidence); this is the **whole lifecycle in between**. Not redundant: **a clean entry does not imply a clean lifecycle** — PMPA's payload arrives inside a benign document wearing legitimate provenance. (`ABSTAIN` on incomplete recall is this page *reusing* [[Abstention]], the way [[ContextEngineering]] reuses [[ProgressiveDisclosure]].)
- **vs a bigger context window** — window is capacity; governance is structure and discipline. The counter-evidence is directional and specific: **Gold-Memory strong ⇒ Full-Pipeline collapse** means the bottleneck is the four actions, not the fit.
- **vs [[ContextEngineering]]** — context engineering decides what goes on the desk **this step**; governance decides what survives **between** sessions.
- **vs [[MemoryPoisoning]]** — poisoning is not *one more failure mode of a broken action*; it is **the third decider**, i.e. a claim of authority over the same three decisions. That is why it is treated as an owner, not as a bug.

## Why It Matters
- It reframes memory from a **personalisation feature** to a **reliability subsystem**: write one wrong entry and every future plan runs on bad input; poison one entry and the attack recurs in every later session.
- It supplies the missing pass over [[LongTermMemory]]: the wiki could already say *where* memory lives and *how* to read it honestly; it could not yet say **how it expires, and who is entitled to expire it.**
- It closes the “governance side” of the shared-memory question [[MultiAgent]] left open (verified ✅ vs speculation inside a team's shared memory; who may write what), and it makes the security and reliability disciplines meet on one object.

## See Also
- [[memory-lifecycle]] — primary source (2026-10-06 material, ingested 2026-10-09)
- [[agent-memory-provenance]] — the entry/exit discipline it extends
- [[LongTermMemory]] — the store whose second half this page governs
- [[MemoryPoisoning]] — the third decider
- [[Provenance]] · [[CitationLock]] · [[Abstention]] — adjacent reading discipline
- [[Compaction]] · [[ContextEngineering]] · [[LLMContext]] — the in-window neighbours
- [[DyadMem]] — the staged benchmark · [[LongMemEval]] — the end-to-end generation it corrects
- [[MemGPT]] · [[AgentZeroMemory]] · [[Zep]] — the systems whose next question is governance
- [[AgentSandbox]] — containment bounds what the agent can touch; governance bounds what it will remember
