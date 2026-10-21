---
title: "Human-in-the-Loop"
type: concept
tags: [human-in-the-loop, approval-gate, escalation, control, persistence-of-directives, authority-erosion]
sources: [human-in-the-loop]
last_updated: 2026-10-21
---

# Human-in-the-Loop (Escalation Gate)

Grading an agent's actions by **impact × reversibility** and inserting an auditable, timeout-aware checkpoint *before* irreversible or consequential writes. The operating rule the field is converging on: **"read freely, keep writes human"** — 读放开，写留人.

## Mechanism (per [[human-in-the-loop]])
1. **Grade the actions** — sort every action by impact × reversibility, then choose a supervision mode **per class**: human-in-the-loop (approve first) / human-on-the-loop (may veto) / fully automatic (sampled afterwards).
2. **Split proposal from execution** — the model *proposes*; a **separate** path performs the side effect and must pass the gate. If the model can still call the side-effecting tool directly, the gate is decoration.
3. **Deterministic gate in code / config** — action class, amount or quantity thresholds, confidence, input novelty. *A threshold that lives only in a policy document and is not embedded in the execution path is not a threshold.*
4. **Persist before pausing; resume idempotently** — a review may take seconds or days, and the resuming process need not be the one that paused it. Measure **automation rate / override rate / escape rate / review latency**; without measurement the gate rots.

## Boundary
- **Not a confirmation dialog** — a real gate measures risk, can suspend execution, and supplies a **decision payload**: the inputs the agent saw, the action it intends, its reasoning, and three controls (approve / reject / modify-and-execute).
- **Not a prompt-resident rule** — approval rules are *executable policy*; prompt-resident thresholds can be ignored, overridden or talked around.
- **Not the model's self-restraint** — the sharpest seam in this cluster. [[Abstention]] and [[CitationLock]] have **the model** as their subject and govern **saying** (*honesty* mechanisms); the gate has **the system and the human** as its subject and governs **writing / paying / deleting** (*control* mechanism). Two layers, both required.
- **Not a sandbox** — a sandbox constrains *what the agent can reach* (capability); a gate constrains *whether to ask first* (decision).
- **Not "more review = more accurate"** — badly designed review imports **automation bias** plus latency and cost; HITL's benefit must be shown in the metrics, not assumed because "someone is watching".

## 指令的持久性 / Persistence of Directives — the missing time column *(added 2026-10-21, ledger row 10-20C)*

> **Draft annotation, pending ingest.** This section is **not yet backed by a source page in this wiki** — verified against live sources on 2026-10-20 (recorded in `.workbuddy/memory/concept-radar/2026-10-20.md`, candidate 3; ledger row **10-20C**). Remove this banner when the material is ingested and human-reviewed, and move the source slug into the frontmatter `sources` field.

**The column this page never had.** Everything above grades **an action**: does *this* write need approval, before it fires, with an idempotent resume. Nothing above asks **whether the directive itself is still in force N planning cycles later**. **Structured Authority Injection (SAI)** (`arXiv:2610.22373v1`, carried in the **cs.AI 2026-10-19** new-submission list; Ryan Tran et al., 9 authors) states the gap in one sentence: **there is no protocol-level mechanism for an operator to inject a binding directive that remains in force across planning cycles.** Two failure causes are named — **解释歧义 / interpretive ambiguity** (free-text directives carry no schema, so they can be read more than one way) and **authority erosion** (the operator's directive loses weight as context accumulates).

1. **Mechanism.** Operator corrections travel as **typed, schema-validated MCP tool calls**; each turn prepends a **ranked authority context**; and the authority channel is **unreachable from the planning process**. The asymmetry is the part worth keeping: **the override tool may be invoked only by the supervision interface — the planning agent can read these commands but can neither create nor delete them.**
2. **Three override types, each with its own expiry semantics — the most portable half:**

   | Type | Meaning | When it expires |
   |---|---|---|
   | **Constraint** | hard = never violated; soft = bypassed only when no compliant plan exists | **persists until explicitly released** |
   | **Priority** | urgency arriving on an outside channel | **auto-expires when the affected task or task class completes** |
   | **Strategy** | coordination heuristic | may hold for the whole run, or **expire after exactly N planning cycles** |

   Conflicts resolve by a fixed precedence **C > P > S**, computed **at prompt-construction time** ⇒ every always-resident directive acquires **a type, a priority and an explicit expiry**.
3. **Measured (9 models × 8 scenarios).** Interpretive ambiguity down, authority decay mitigated; prompt overhead **reduced by at most 38%** on the strongest model (GPT-4o), **31%** on DeepSeek-R1; GPT-OSS-20B goes **from zero to full completion** in two scenarios.
4. ⚠️ **Cost and instability, kept beside the result:** Gemini-2.0-Flash falls **1.00 → 0.50** on the region-allocation scenario; DeepSeek-R1 **exhausts a 4,096-token budget** in S7 as the authority context grows; and one tier (LLaMA / Qwen / Claude-Haiku) **only gains overhead without proportional improvement** — the authors themselves rank these as the weakest group. All eight scenarios are **simulation**, not deployment, and the design assumes **a single trusted supervisor** (how precedence is settled under multiple supervisors is not addressed). ⚠️ **Date discrepancy:** the `arxiv.org/abs/2610.22373` page metadata reads “Submitted on 27 Jul 2026”, contradicting both the `2610` arXiv ID and the 2026-10-19 new-submission list; this page follows the **new-submission list** and records the inconsistency as unresolved.

**Boundary.** vs this page's gate — the gate asks **“does this action need a human?”** (a question about *an act*); this section asks **“is this directive still binding?”** (a question about *time*). Same page, the half-column that was missing. vs [[MemoryGovernance]]'s *Permissioned* — the same discipline (**read right ≠ write right**) applied to a different object: that one governs **who may write shared memory**, this one governs **who may write the instruction**. vs [[ContextEngineering]] — that page places content **within one turn**; this is **across planning cycles**, and it upgrades “always-resident” from a **size** problem to a **type + expiry** problem.

**Why it lands on this page.** It is 🎯 ledger row 10-09「常驻上下文与指令预算」's first citable device: that row asks *what deserves a resident slot and how large the file should be*; this answers *what deserves a slot must also carry persistence semantics*.

## Why It Matters
- It answers a property unique to acting agents: unlike a chatbot, a wrong action is frequently **not recoverable** — a sent email, an executed payment, a deleted record. Model error rates can be low and the damage still lands before anyone notices.
- It makes "automatic" and "someone has a backstop" compatible: the agent absorbs the bulk of the work, the human spends seconds on the one irreversible step — speed comes from *narrowing the decision scope*, not from removing oversight.
- It produces the audit record "who approved what, when, at which model version" — [[Provenance]] applied to **decisions** rather than facts.
- It closes the loop with [[AgentIdentity]]: attenuation sets the ceiling, the gate handles the remainder.
- Its prerequisite is [[ToolHallucination]]: a gate can only adjudicate a call that resolves to a real tool.

## See Also
- [[human-in-the-loop]] — source
- [[AgentIdentity]] — upstream: who acts, and how far authority reaches
- [[ToolHallucination]] — upstream: the call must first resolve
- [[Abstention]] · [[CitationLock]] — the honesty mechanisms this page is *not*
- [[MemoryGovernance]] — the same “read right ≠ write right” discipline, applied to memory rather than directives
- [[Agent]] — sharpens its "not a fixed automation script" boundary from *can it decide* to *may it act*
- [[Provenance]] — the audit discipline this reuses for actions
