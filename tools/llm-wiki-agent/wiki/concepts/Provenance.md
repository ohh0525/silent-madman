---
title: "Provenance"
type: concept
tags: [agent-memory, provenance, reliability, evidence-garment, enforcement-point, serialization, provenance-reversibility, deletion-closure, invalidation-nonlocality, dependency-closure]
sources: [agent-memory-provenance]
last_updated: 2026-10-26
---

# Provenance

The design constraint that every stored fact must carry its origin, timestamp, and an evidence pointer — so the system can always answer "why is this believed?" and can grade trust by *source*, not by *relevance alone*.

## Mechanism (per [[agent-memory-provenance]])
- A memory is not a string; it is a record answering: what claim is stored, which source produced it, is it fact/preference/inference, when observed or last verified, and what condition should replace or expire it.
- Write-time gate: reject unknown or untrusted sources; grade trust by origin (`human` / `verified_tool` / `self_inferred`), and the agent does not get to fully trust its own guesses.
- Read-time filter: drop expired / low-trust entries *before* they reach the context window; a retrieved memory without source and time metadata is "just a persuasive sentence occupying expensive context".

## Why It Matters
- Kills two compounding failure modes: **stale facts** (no TTL ⇒ presents a 3-week-old value with the same confidence as a 30-second-old one) and **unbounded growth** (append-only memory buries the right answer under near-duplicates).
- Makes trust *meaningful*: when every record carries its source, retrieval filters can act on it; without it, trust becomes uniform and therefore meaningless.
- Directly matches the silent-madman repo's own "人工核查承诺" instinct — nothing enters as fact without a traceable source.

## Evidence's outer garment — the same payload, four vessels *(ledger row 10-19A; applied 2026-10-20)*

> **Draft annotation, pending ingest.** Not yet backed by a source page in this wiki — verified against live sources on 2026-10-19 (recorded in `.workbuddy/memory/concept-radar/2026-10-19.md`, candidate 1). Remove this banner when the material is ingested and human-reviewed, and move the source slug into the frontmatter `sources` field.

**The inference this page never wrote down.** [[Provenance]] (origin / timestamp / evidence), [[CitationLock]] (cite only what you actually opened) and [[Abstention]] (abstain without sourced evidence) jointly make **"retrieved and actually opened"** the gold standard for trustworthy content. **None of the three is refuted here.** What is displaced is the inference they never stated but have always relied on: **opened ⇒ trustworthy.**

- **TRACER** (`arXiv:2610.19133`, submitted **2026-10-13**, **EMNLP 2026 Findings**; Kshitij Mishra / Salem Lahlou / Nils Lukas, MBZUAI). Holding the payload **fixed** and changing only the vessel, attack success runs **follow-up message 70% → agent message 92% → tool output 95% → retrieved context 96%**. Six checkpoints trained **only** against follow-up attacks: **18.0%** on the follow-up eval → **53%** on the RAG eval (**+35 percentage points, all of it from the garment**). TRACER's own defence does **not** close the gap: RAG garment **65.5% → 6.1%**, clean accuracy held at 78–82%; **3B** cross-garment average **13.9%**, **7B** single epoch **9.4%**.
- **Ignored, Not Refused** (`arXiv:2610.23254`, **2026-10-16**). Of what gets scored "attack failed", **76–80% is the model simply not engaging** and only **17–18% is actual refusal** — MiniCPM-2B names the injection in its reasoning and then transfers **$30,000** anyway. With **identical weights, changing only the system prompt**, InjecAgent ASR moves **0.2% → 43%**.
- **ATOM**: in **21.7%** of AgentDojo episodes the agent stayed safe but **did not complete the user's task** — safety bought at the price of the task.

> **The load-bearing sentence: the most trustworthy kind of evidence is also the most effective attack vessel.** Provenance metadata is exactly what makes content *credible* — and the same metadata is what makes the retrieved-context garment the **96%** channel. **The three disciplines are not bypassed; their column is missing a variable.** Provenance's object should extend from *the source of the evidence* to **the garment in which the evidence was delivered**.

⚠️ **Evidence grade, must sit beside the numbers.** The **authority gradient** (70 / 92 / 95 / 96) and the **18% → 53%** pair appeared in this search **only** in an AI-generated overview at `alphaxiv.org`; TRACER writes **65.5% → 6.1%** into its own abstract (first-hand). **The former two sets must be checked against arXiv figures 3 / 4 before being cited as first-hand.** TRACER's home ground is **GSM8K arithmetic on 3B models** — transfer to general agents is the authors' own stated transferability claim, and the gradient ordering is their reading of their own chart. **Ignored-Not-Refused** audits **11 open-source 2–14B models**; its "mostly ignoring" conclusion does **not** carry to frontier closed models (the paper itself reports **Kimi K3 refusing 97–99%** of attacks it did not execute). ASR is a **conditional** criterion (correct before injection, wrong after = one success).

### The open experiment this row defines (10-19A × 10-18B)

**The first cross-row open experiment in this wiki** — the 10-17 and 10-18 ones were both intra-row. Two rows both study *"the same content behaves differently under different conditions"*, but **one swaps the garment and the other swaps the interface**; **nobody has measured their interaction.**

- **TRACER's four garments** (follow-up message · agent message · tool output · retrieved context) × **MemForm's five interfaces** (Content · Evidence · Scope · Selection · Path — `arXiv:2610.14431`, ledger row 10-18B).
- **The question:** does a **Scope**-interface attack wearing the **retrieved-context garment** amplify the authority gradient — i.e. are the two axes independent, or does one modulate the other?
- **Minimum viable form:** one fixed payload set × 4 garments × 5 interfaces → **report the interaction matrix, not a leaderboard.**
- **Why it belongs on this page:** if the garment is the variable, then **provenance metadata is the garment's most legible component** — so this is the instrument that tests the sentence above rather than merely illustrating it.

**Boundaries.** vs **[[MemoryPoisoning]] / MemForm** — MemForm is *content-clean* distortion (the attack sits in the **formation process**); this row is *content-dirty* with the **garment** as the variable. Content-side failure vs container-side failure; **record side by side, never as one page.** vs **10-16A ToFu** — same shape, and ToFu is the **earliest instance** of this variable (sequence is a property of the framework / success rate is a property of the garment). vs **第十四条（见 `.workbuddy/memory/concept-radar/SCAN-LINES.md`）** — this row is that line's originating instance; ToFu and 10-18C are its other two. vs **10-17B FEB-30 / 10-18A** — **not the same line**: those are the verb-efficacy line, this is the container line.

## Provenance is a discipline; the check is an enforcement point *(added 2026-10-21, ledger row 10-21A)*

> **Draft annotation, pending ingest.** Not yet backed by a source page in this wiki — verified against live sources on 2026-10-21 (recorded in `.workbuddy/memory/concept-radar/2026-10-21.md`, candidate 1; ledger row **10-21A**). Remove this banner when the material is ingested and human-reviewed, and move the source slug into the frontmatter `sources` field.

**The boundary this page should state about itself.** This page, [[CitationLock]] and [[Abstention]] are **model-side reading discipline**: they say what the *model* should do with what it opened, and they are satisfied or violated by the model's behaviour. **ClawMMU** (`arXiv:2610.28093`) takes the **same object** — *where did this content come from* — and makes it a **harness-side enforcement point**: every representation of every memory carries **owner / scope / origins / authority**, and the harness checks those labels at **map · derive · reload · authorize** rather than asking the model to judge. ⇒ Same target, **different executor and different location** — the textbook instance of scan line 16 (see `SCAN-LINES.md`): this page governs by **discipline on the model**, that design governs by **a check at the access point**; they are complements, not duplicates.

- **Why it still does not replace this page:** the verdict there depends **only on origin, never on content** — it does not tell you whether the sourced fact is true, current, or well-evidenced. Provenance's three questions (*what claim, which source, when observed or last verified*) are exactly the ones it does not ask.
- **The prerequisite, and where it breaks:** those descriptors presuppose **stable page identities** (ClawMMU is built on ClawVM's addressable pages). On [[LongTermMemory]]'s third carrier — latent / soft-token memory — **there is no page to attach a descriptor to** (scan line 12; same applicability boundary as ledger row 10-17A).
- 🔴 **Status:** **not implemented** — Appendix C states verbatim *“ClawMMU is not yet implemented”*; **no measured numbers** anywhere in the paper; **6-page non-archival workshop paper** (AgenticOS @ NeurIPS 2026), no peer review. ⇒ Cite as a shape, not as evidence. (Cross-reference [[HumanInTheLoop]]「The Gate Does Not Know Where Its Arguments Came From」and [[MemoryGovernance]]'s *Permissioned*.)

## Serialization precedes the model *(ledger row 10-22A; applied 2026-10-22)*

> **Draft annotation, pending ingest.** Verified against live sources on 2026-10-22, recorded in `.workbuddy/memory/concept-radar/2026-10-22.md` (candidate 1). Remove this banner on ingest; move the slug into frontmatter `sources`.
>
> 🔴 **Preprint, not peer-reviewed; single institution (Pixee, a code-security vendor). The failure occurs only in flattening harnesses — the four role-typed harnesses measured 0%.**

The section above draws this page's boundary by **executor**: a **discipline on the model** versus **a check at the access point**. **Compaction Laundering** (`arXiv:2610.29869`, submitted 2026-10-21) adds the column that ordering cannot express — **the failure had been attributed to the wrong executor**:

> Prior work describes this failure as a **limitation of the model** (the model cannot reliably tell where content came from). In a flattening harness the origin is destroyed **before the model ever sees the text** ⇒ **"Susceptibility is therefore a property of the serialization strategy, not of the model."**

- **Consequence for this page's boundary.** A discipline on the model and a check at the access point are both **downstream of serialization**. Where the harness flattens typed roles into unescaped inline labels, **there is no provenance left for either to act on** — the check has nothing to check, and the discipline is being asked to recover what code destroyed deterministically. ⇒ **No prompt-level defence can recover it**; the authors measured **77%** detection with a **code-level** origin check, at **2%** degradation of legitimate summary content (self-measured).
- **Consequence for the governance-vs-window split.** This page and [[MemoryPoisoning]] sit on the "outside the window" side, [[Compaction]] on the "inside, per-turn" side. That split is **wrong at the joint**: compaction is where transient injection becomes durable memory — the step `overview.md` lists as an open item. The corrected statement is that **compaction is a governance boundary that happens to run inside the window, per turn.**
- **Where this page's authority stops.** Provenance can only be preserved by something that exists **prior to** the model's input. Once the origin is gone, the honest verdict is not "the model failed to track it" but **"there was nothing left to track."**

## Provenance must be reversible — the backward pointer is only half of it *(ledger row 10-25B; applied 2026-10-25)*

> **Draft annotation, pending ingest.** Not yet backed by a source page in this wiki — verified against live sources on 2026-10-25 (recorded in `.workbuddy/memory/concept-radar/2026-10-25.md`, candidate 2; ledger row **10-25B**). Remove this banner when the material is ingested and human-reviewed, and move the source slug into the frontmatter `sources` field.
>
> 🔴 **The 62–99% reconstruction rate is measured on secrets *constructed to be splittable*, on 7B-class models. It is not a production leakage rate.**

**The direction this page has never had.** Everything above — and every section of this page — defines provenance as a **backward** pointer: each stored fact carries *which source produced it*, *when*, *with what evidence*. Descendant ⇒ ancestor. **None of it is refuted.** What is missing is the **forward** direction: **given this source, what has been derived from it?** This page has never had that cell, and it is not optional — it is what "delete the source" has to traverse.

**AfterDeleteBench** (`arXiv:2610.31366`; Ehsan Saleh / Roozbeh Nahavandi / Sama Salarian / Raef Bassily / Andrew Perrault; **25 pp / 7 figs / 12 tabs**; cs.CR + cs.CL + cs.LG). For each synthetic secret the design compares an agent **exposed and then deleted** against a **paired never-exposed control** ⇒ recovery is attributable to the original exposure rather than to guessing.

- Main setting: a **single query** recovered the deleted secret in roughly **two-thirds** of cases from **Qwen2.5-7B-Instruct**; the never-exposed control recovered **zero**.
- 🔴 **The load-bearing result: no verbatim copy needs to survive.** When the complete secret string is already gone and only **separately stored components** remain — with the **combination rule public** — exact reconstruction succeeds **62–99%** across **Qwen / Mistral / Phi-3**.
- **Two repairs, and the difference between them is the point:**
  - **provenance-aware closure** (delete the derived records together with the source) ⇒ **eliminates the observed recovery**;
  - **exact-literal write filter** (block verbatim re-insertion) ⇒ blocks re-insertion but **does not erase information already present in the system**.
- *Methodological note worth keeping:* **the response interface is part of the measurement system** — format / parser mismatches cause a reply that **does** contain the target information to be scored as a failure. ⇒ A deletion audit that reports clean may be measuring its own parser.

> ⇒ **Provenance must be reversible.** A backward pointer alone lets a system swear that every record carries its origin while being unable to answer the only question deletion asks.

**Consequence for this page's own object.** The three questions above (*what claim, which source, when observed or last verified*) are all **ancestor-facing**. The fourth question this page should own is **descendant-facing**: **what does this source currently license, and what has been derived from it?** Without it, "this fact carries provenance" and "this fact can be erased" are compatible statements — and the second is false.

**Boundaries (do not merge these).**
- **vs [[MemoryGovernance]]'s half of this row** — that page supplies the **action** (`DELETE` needs closure semantics); this page supplies the **pointer** the action has to traverse. Two halves of one row, filed separately on purpose.
- **vs ledger row 10-18A (Bemula / MemCut)** — that row asks **"was the deletion request executed at all?"** (end-to-end ≤1.5%; 39–76% residue after removing the direct disclosure sentence). This row **grants that the source record really was deleted** and asks about **derivations**. ⇒ **scan line 13 vs scan line 19**: ask them in that order, never as one question.
- **vs ledger row 10-24B (governed-state corruption)** — **mirror images**: 10-24B is *"the content is all present, but the subset selected to take effect was swapped"*; this row is *"the source is gone, but the derived subset is still in effect."*
- **vs [[Compaction]]** — compaction loses provenance by **destroying it before the model sees the text**; here provenance is intact and **complete**, and the secret survives anyway. A serialization fix does not address this row.

⚠️ **Evidence grade, must sit beside the numbers.** Secrets are **synthetic and constructed to be splittable**; models are **7B-class** ⇒ **99% must not be read as a production leakage rate**. "Provenance-aware closure eliminates recovery" was obtained **in a setting that had a positive control recovery** ⇒ it does **not** establish that a given deployment has that oracle. Preprint; **no independent replication**.

## Invalidation is non-local, dependency is local — a record's truth expires where its metadata cannot see *(ledger row 10-26A; applied 2026-10-26)*

> **Draft annotation, pending ingest.** Not yet backed by a source page in this wiki — verified against live sources on 2026-10-26 (recorded in `.workbuddy/memory/concept-radar/2026-10-26.md`, candidate 1; ledger row **10-26A**). Remove this banner when the material is ingested and human-reviewed, and move the source slug into the frontmatter `sources` field.
>
> 🔴 **Preprint, not peer-reviewed. `62%` is measured on the authors' own synthetic world generator (Fallout); Tether's `0.3%` holds only when the dependency relation and the verdict are supplied in the same session — spread across sessions it degrades to 9.4–22.1%.**

**The assumption this page has always carried.** Every section above treats a record's **truth** as a property *of that record*: it carries origin, time and evidence, and the fourth question (*what condition should replace or expire it*) is likewise asked **per record**. **None of it is refuted.** What is displaced is an inference none of it states: **that a record's expiry is a property of the record itself.** It is not — it is a property of **what the record depends on**, and that dependency appears nowhere in the record's own metadata.

**Tether** (`arXiv:2610.25123`; Yiqi Wang · Jinqian Ju · Jiaqi Zhang · Zhangkai Wu · Yiqun Duan · Zequn Sun · Taotao Cai · Mingkai Zheng, 8 authors; cs.CL; v1 **2026-10-18 09:01:52 UTC**, v2 **2026-10-22**). A signing key is revoked; every verification verdict built on it ought to fall with it — **but the announcement names only the key**, and those downstream verdicts **never share a retrieval window with it**:

> *"This non-locality of invalidation turns memory into a liability."*

- In long simulated dialogues, an agent reading **atomic-fact memory** republished **62%** of the objects that should have been voided by an upstream invalidation — **and every one of those records was true at the moment it was written.** ⇒ **逐条审查全部通过；错的不是其中任何一条记录。**
- **The device — Tether:** record, **at write time, the exact version each conclusion depends on**; **at read time withdraw the whole record** if anything supporting it has lapsed anywhere in the store. The agent reads the same fields as before — it simply does not see that one. ⇒ **0.3%**, using **37% fewer verification calls** than re-verifying everything.
- Neighbours, for scale: **A-Mem / Graphiti** re-verify most candidates (**0.83–0.86** checks each) and still publish **9%**; **Mem0**, leaning harder on memory, publishes **42%**; *"clear every conclusion the moment anything lapses"* is equally safe but costs **32% more checks**.

> ⇒ **A record can be perfectly sourced and perfectly current — and still be a live lie, because what it depended on died somewhere it never looks.**

**Consequence for this page's own object.** The three questions (*what claim, which source, when observed or last verified*) and the fourth (*what should expire it*) are all **asked of one record at a time**. The unit this row says they must be asked of is **the record together with its dependency closure** — and that closure is not enumerable from the record itself, which is the shape this page already knows how to complain about (see「Provenance must be reversible」, where the missing direction was *forward*). ⇒ **This page now has two traversals and is missing a third: backward (*where from*) · forward (*what was derived*) · and now propagation (*what lapsed*).** Three different walks over the same graph; none substitutes for another.

**Boundaries (do not merge these).**
- **vs「Provenance must be reversible」(10-25B, this page)** — the **forward pointer** answers *what was derived from this source*; this row answers *a derived record must be withdrawn when an ancestor lapses*. **Pointer vs propagation**: the first is what deletion traverses, the second is what invalidation traverses. **Adjacent cells on one page; named, not merged.**
- **vs ledger row 10-24A (AMV-Guard)** — **upstream / downstream, and they must be read in that order.** AMV-Guard prices *whether this premise deserves re-verification given what you are about to do*, and therefore **presupposes that an invalidation signal has already arrived**. This row shows that in the common shape — *the announcement names the key, not the verdicts* — **no signal arrives at all** ⇒ **first arrival, then pricing.** ✅ **10-24A landed 2026-10-26** — as sections on [[Abstention]] / [[MemoryGovernance]] / [[HumanInTheLoop]] ⇒ this cross-reference is now **section-to-section**, no longer row-to-row.
- **vs ledger row 10-25B / [[MemoryGovernance]]'s `DELETE` closure** — that row **has an action** (`DELETE` was executed; ask whether the closure is complete). This row has **no action at all**: nothing was deleted, nothing was edited ⇒ ask *what propagates invalidation when there is no deletion event*. **Split columns.**
- **vs ledger row 10-24B (governed-state corruption)** — that row's **control plane was modified**; here **nothing touched the control plane**. Split columns.
- **vs [[Compaction]]** — compaction loses provenance by **destroying it before the model sees the text**; here provenance is intact and complete, and the verdict is wrong anyway.

**Scan-line assignment.** An instance of **line 19 — composition audit** ("how many items does one verdict carry? if every item passes, does the conclusion they jointly entail also pass?"): **each record is true when written ⇒ per-record review passes 100%**, while the unit that should have been judged is *the conclusion plus its dependency closure*. Registered in `.workbuddy/memory/concept-radar/SCAN-LINES.md`. Its paired landing is [[MemoryGovernance]]「Update can be triggered upstream」, where the same row lands as an **action**.

⚠️ **Evidence grade, must sit beside the numbers.** Preprint, **not peer-reviewed**; **Fallout is the authors' own synthetic world generator**; **0.3%** is conditional on **relations and verdicts being supplied in the same session** and degrades to **9.4–22.1%** when spread across sessions; the authors themselves state it degrades with **weaker writers** (who miss dependencies or miss invalidation events). **62% is a property of atomic-fact memory in that generator — not a production staleness rate.**

## See Also
- [[agent-memory-provenance]] — primary source
- [[MemoryGovernance]] — where the same row lands as an action (`DELETE` closure, 10-25B; upstream-triggered `UPDATE`, 10-26A)
- [[Compaction]] — the trust boundary this page's discipline sits downstream of (10-22A)
- [[LongTermMemory]] — the store that carries provenance
- [[CitationLock]] — the read-side companion
- [[Abstention]] — what happens when provenance is absent
- [[ToolHallucination]] — carries the matching scope note: existence is not the variable
- [[MemoryPoisoning]] — the content-side counterpart to this page's garment variable
