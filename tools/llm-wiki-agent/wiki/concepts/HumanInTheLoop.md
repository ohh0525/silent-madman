---
title: "Human-in-the-Loop"
type: concept
tags: [human-in-the-loop, approval-gate, escalation, control]
sources: [human-in-the-loop]
last_updated: 2026-09-24
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
- [[Agent]] — sharpens its "not a fixed automation script" boundary from *can it decide* to *may it act*
- [[Provenance]] — the audit discipline this reuses for actions
