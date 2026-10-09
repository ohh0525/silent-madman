---
title: "Memory Poisoning"
type: concept
tags: [agent-memory, memory-poisoning, security, prompt-injection, persistent-corruption]
sources: [memory-lifecycle]
last_updated: 2026-10-09
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
