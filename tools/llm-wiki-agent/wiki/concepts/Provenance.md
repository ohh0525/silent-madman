---
title: "Provenance"
type: concept
tags: [agent-memory, provenance, reliability, evidence-garment]
sources: [agent-memory-provenance]
last_updated: 2026-10-20
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

## See Also
- [[agent-memory-provenance]] — primary source
- [[LongTermMemory]] — the store that carries provenance
- [[CitationLock]] — the read-side companion
- [[Abstention]] — what happens when provenance is absent
- [[ToolHallucination]] — carries the matching scope note: existence is not the variable
- [[MemoryPoisoning]] — the content-side counterpart to this page's garment variable
