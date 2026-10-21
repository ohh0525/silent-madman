---
title: "Memory Poisoning"
type: concept
tags: [agent-memory, memory-poisoning, security, prompt-injection, persistent-corruption, owner-attribution, exposure-behaviour-state]
sources: [memory-lifecycle]
last_updated: 2026-10-21
---

# Memory Poisoning

The write-side attack surface of agent memory: an adversary who cannot change *what the agent does this turn* instead **changes what the agent will permanently believe**. Formally it is the **third decider** in [[MemoryGovernance]]'s table — not a bug in one of the four memory actions, but a **claim of authority over the same three decisions** (what gets written, when it is retrieved, when it is deleted) by someone who was never granted them.

Where a [[ToolHallucination]] is a single-turn factual defect and a bad completion is forgotten with the window, a poisoned memory is **durable and compounding**: it becomes a fixed input to every future plan, and it re-raises itself in every later session. The attacker does not need to return.

## Two mechanisms, one shape
| Mechanism | How the write happens | Evidence |
|---|---|---|
| **Induced self-write (indirect)** | The payload is embedded in a **benign** external source (web page, ticket, document). Reading it induces the *harness agent itself* to write the instruction into durable memory — no direct injection at the user, no forged storage. | **PMPA** (arXiv:2609.13889, Auckland/Fudan, 2026-09-12): OpenClaw ISR/C-ASR **73.7% / 55.5%**, **Claude Code 66.9% / 81.7%**, with **benign-task performance left unchanged** — i.e. the compromise is invisible on quality metrics |
| **Forged conversation history** | The agent's own local session store is treated as ground truth about what happened. Anyone who can write to it can manufacture a past — including a past in which the agent was already authorised. | **Darktrace** (Eric Rozon, published 2026-09-24; disclosed 2026-08-18 to Anthropic / OpenAI / AWS): **all four harnesses — Claude Code, Codex, Kiro-CLI, Pi — accept forged conversation history**; under Kiro-CLI the chain reaches **Active Directory domain takeover**; under Codex it persuades the agent to exfiltrate |

Both are the same shape: **the agent's memory is writable by something that is not the agent's principal, and the write is taken as fact.**

## Why prompt-level defence is not enough
Once the memory is poisoned, prompt-side defences are of limited value — the poisoned entry is, from the model's point of view, a **legitimate memory**. The project that measured PMPA reports exactly this: **prompt-level defences protect poorly after poisoning** has occurred. The defensive consequence is a **placement** rule of the same species as the wiki's existing ones (the resolution rung must precede every gate; the sandbox must sit under the kernel):

> **Memory writes need the same treatment as irreversible writes: an auditable chokepoint, provenance on every write, and a write-authority model — established *before* the content is trusted, because after the fact the content looks like memory.**

This is also why [[Provenance]] alone does not close the hole: PMPA's payload arrives **inside a benign document that carries legitimate provenance**. A clean entry does not imply a clean lifecycle.

## The mitigation asymmetry (the part that matters operationally)
- The **root fix for the forged-history class is vendor-side**: cryptographically signed model replies, **validated server-side on every turn**. Until that ships, **a defending operator cannot deploy the fix**. This is the same structural pattern the wiki already records for the memory-integrity radar rows — *the vulnerability is disclosed, but the mitigation is not yours to apply.*
- The **interim** posture is therefore detection and containment: treat the local session-history store (typically a client-side, often plaintext SQLite file) as a **security-sensitive file**, where **any write by a non-harness process is an unambiguous attack signal** — a package-install `postinstall` script touching it is the canonical case. Treat “session resume / rollback edits” as **untrusted input**.
- **Record model choice as a security decision, not a default.** The material's pointed example: *a cheap model default is an unregistered security decision* — the attack's success rate varies by model and harness (Opus 5's guardrails held under Claude Code), but **the structural defect in history management was common to all four**.
- **Egress behaviour monitoring detects this class better than tool approval does**, precisely because a hijacked agent's actions **look entirely legitimate** — from the inside it is doing permitted things for a reason it now believes.

## Exposure ≠ Behaviour ≠ State — the ownership column *(added 2026-10-21, ledger row 10-20B)*

> **Draft annotation, pending ingest.** This section is **not yet backed by a source page in this wiki** — verified against live sources on 2026-10-20 (recorded in `.workbuddy/memory/concept-radar/2026-10-20.md`, candidate 2; ledger row **10-20B**). Remove this banner when the material is ingested and human-reviewed, and move the source slug into the frontmatter `sources` field.

**What the two mechanisms above never measured.** PMPA and Darktrace — and the formation-surface work on the neighbouring row (MemForm) — are entirely a **content** story: a malicious payload, a forged history, clean content arriving in a poisonous order. The audit behind this section changes the **object**: the retrieved content is **entirely legitimate**; what is wrong is **who it belongs to**. It also splits the single event this page has been calling “poisoned” into three stages:

| Stage | Question | Measured |
|---|---|---|
| **暴露 / Exposure** | Did a foreign credential reach the prompt? | A memory bank mixing **763** cross-user historical logins returned **another user's** credential for **84.7%** of the required apps — **and the agent almost never acted on it** |
| **行为 / Behaviour** | Did the agent actually use it? | Under stress (the user's own credential missing, a single foreign credential presented as if it were their own), **7 agents used it in 80–94% of runs** |
| **状态 / State** | Did the victim's account really change? | In **up to 43%** of those runs the victim's account was modified, **sometimes passing the official checks** |

⇒ **84.7% of exposure produces almost no behaviour; once behaviour appears, 43% lands on state.** A benchmark that reports exposure alone misreads the risk **in both directions** — it exaggerates when the agent ignores what it retrieved, and under-counts when it does not. Source: `arXiv:2610.25707` (submitted **2026-10-19 02:53 UTC**; Hau-Sing So et al., 6 authors; 19 pp / 14 figs / 12 tabs; AppWorld).

- **The fix is per-line — and that is the finding.** Marking the owner **before or within each credential line** drops misuse from **92 / 305** paired runs to **1 / 305** (it still holds when usernames contain no personal name). ⇒ **attribution depends on there being a line.**
- **Cost and fragility, beside the fix:** owner-bound annotations cost **3–5 successful tasks per model** even on *clean* memory; **writing the owner incorrectly roughly restores the abuse**; and **trailing owner tags plus appended safety instructions work on only some models**.
- **The previous hop in the same cell.** **MemLeak** (`arXiv:2610.04195`) measures **leakage** only — **70–100%** non-adversarial leakage under same-team pooled retrieval, **90–100%** adversarially constructed top-k, end-to-end contamination **5.00/5** — and finds that of three architectural mitigations **only post-retrieval hard attribution gating** reliably restores the clean baseline (**1.00/5**, ≈**1.4 ms/query**). MemLeak stops at **exposure**; this section walks the two stages after it.

**Boundaries.** vs the two mechanisms above — **not a fourth poisoning mechanism**: the payload is *correct*; the *owner* is wrong. It is the **归属 / ownership** column of this page, not another row of the content table. vs ledger row 10-13「检索准入 × 跨主体状态隔离」— that row names the **variables** (attribution ≠ permission; reasoning state split per principal); this section supplies the **instrument** and the counter-intuitive measurement (*high exposure ≠ high harm*); record side by side and cross-reference, do not merge. vs [[LongTermMemory]]「The third carrier」(ledger row 10-17A) — the fix here **requires enumerability**, so on a continuous carrier **there is no line to mark**: **an addressable defence fails on non-addressable memory** — the exact complement of ledger row 10-20A, which shows the same carrier performing **unscoped revision**.

⚠️ **Limits:** the stress condition is **constructed** (own credential absent + one foreign credential presented as the user's own), not an estimate of real-world incidence; **84.7%** is one specific mixed store inside AppWorld; MemLeak self-reports **hand-written synthetic samples and small samples**, i.e. it demonstrates a **mechanism**, not a frequency; submitted **2026-10-19**, **no independent replication**.

## Boundaries
- **vs [[ToolHallucination]]** — existence of the tool vs **integrity of the record**. A poisoned agent calls tools that really exist; the closed-world rung passes it.
- **vs indirect prompt injection in general** — ordinary indirect injection is **transient**: it acts within the turn that carried it. Memory poisoning is the *persistence* step that converts a transient injection into a **standing instruction**. That step is what makes this page a separate concept rather than a section of an injection page.
- **vs [[AgentSandbox]]** — containment bounds **what the agent can touch** while it runs; governance bounds **what it will still believe after it stops**. The Darktrace chain shows container hygiene is not sufficient: the store being written was *supposed* to be the agent's own memory.
- **vs [[Provenance]] / [[CitationLock]] / [[Abstention]]** — the entry/exit reading discipline. Useful, necessary, and **not sufficient**: provenance records where a fact came from, not whether the *writer had authority* (see [[AgentIdentity]] for the authority half).
- **vs [[MultiAgent]]'s cross-contamination** — the same failure shape one layer out: **an unverified premise inherited as fact.** Cross-contamination moves it between peers in one shared workspace; poisoning moves it from an adversary into durable storage. Both extend [[Provenance]]'s object from *facts* to *the verification status of what you are treating as fact.*
- **vs [[HumanInTheLoop]]** — the gate grades actions by impact × reversibility. **Memory writes sit on the irreversible side** and are largely ungated today; that is the gap this page names.

## Why It Matters
- It supplies the **security leg** of [[MemoryGovernance]] and explains why that page's bottom line ④ (*signature-verified*) is not an extra: without it, “who may write” is enforced only by convention.
- It inverts the usual priority. Teams deploy memory for personalisation; the wiki's evidence says the failure mode to design against first is **the memory that someone else wrote**.
- It gives the wiki a concrete, first-party instance of a rule it had only stated abstractly: **“disclosed ≠ mitigable by you.”**

## See Also
- [[memory-lifecycle]] — primary source (PMPA + Darktrace evidence; 2026-10-06 material, ingested 2026-10-09)
- [[MemoryGovernance]] — the parent page; poisoning is its third *decider*
- [[LongTermMemory]] — the store being attacked
- [[Provenance]] · [[CitationLock]] · [[Abstention]] — why entry discipline alone is insufficient
- [[AgentIdentity]] — the authority half of the write question
- [[AgentSandbox]] — containment vs belief
- [[HumanInTheLoop]] — why memory writes deserve gate treatment
- [[MultiAgent]] — cross-contamination, the same shape one layer out
- [[ToolHallucination]] — the adjacent “does the world match the call” rung, at a different object
