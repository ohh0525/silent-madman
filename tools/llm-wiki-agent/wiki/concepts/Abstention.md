---
title: "Abstention"
type: concept
tags: [agent-memory, abstention, reliability, abstention-not-terminal, composition-audit]
sources: [agent-memory-provenance]
last_updated: 2026-10-25
---

# Abstention

The ability of a memory system to refuse to answer when it lacks sourced evidence — treating "I don't know" / "unknown" as a correct state transition rather than a failure.

## Mechanism (per [[agent-memory-provenance]])
- Built into the reading discipline: if no sourced evidence was opened, the system returns an abstention instead of a plausible guess.
- One of LongMemEval's five core long-term-memory abilities (information extraction, multi-session reasoning, temporal reasoning, knowledge updates, **abstention**).
- Depends on [[Provenance]] and [[CitationLock]]: without them the system cannot tell an established sourced fact from something merely asserted once.

## Why It Matters
- The dangerous failure is not a wrong answer per se, but confidently stating something that cannot be traced to a source — poisoning future plans.
- Benchmark evidence ([[LongMemEval]]): abstention is one of the abilities where commercial assistants and long-context LLMs degrade most.
- "Abstention is not the system being dumb" — hard-answering with a reasonable-sounding guess is what writes hallucination into the future.

## Abstention is not a terminal state — a refusal can carry the payload *(ledger row 10-25A; applied 2026-10-25)*

> **Draft annotation, pending ingest.** Not yet backed by a source page in this wiki — verified against live sources on 2026-10-25 (recorded in `.workbuddy/memory/concept-radar/2026-10-25.md`, candidate 1; ledger row **10-25A**). Remove this banner when the material is ingested and human-reviewed, and move the source slug into the frontmatter `sources` field.
>
> 🔴 **Preprint, not peer-reviewed. The two headline rates come from 30 hand-constructed scenarios, not from naturally occurring leakage — quote them as a ceiling on a construction, never as an incident rate.**

**The assumption this page has always carried.** Everything above treats abstention as the **safe terminal state**: no sourced evidence ⇒ refuse ⇒ the dangerous thing was not said. **None of it is refuted.** What is displaced is the inference the page never wrote down but has always relied on: **that a refusal is an empty output.**

**The Mosaic Effect** (`arXiv:2610.30418`, submitted ≈**2026-10-21**; Daniel C. Ruiz / Luca Luceri / Emilio Ferrara): **30** synthetic composition scenarios (cybersecurity / medical / military) ⇒ **10,800** final answers from three LLM agents under controlled simulation, plus **1,440** from live agents in two open-source shells. Every individual document is **authorized**; the conclusion their combination supports is **not — and nobody authorized that**.

- Even under **benign queries** — ones deliberately designed to be answerable from a single document — the best measured model, **GPT-5.6-Sol**, still leaked the prohibited composed conclusion **7.08%** of the time (95% CI **3.75–10.67**); **live shells did worse**.
- Adding visible classification headers plus an explicit aggregation rule **reduced** leakage substantially, but **32.37%** (95% CI **28.33–36.19**) of unsafe disclosures remained **across all intents** ⇒ **telling the agent "do not aggregate" is not sufficient.**
- 🔴 **The load-bearing sentence, verbatim: "*increased refusals do not guarantee confidentiality, since significant refusals reveal the prohibited conclusion regardless*".**

> ⇒ **A refusal is an output channel.** An agent that declines to state X, in a context where X is the only interesting thing to decline, has communicated X.

**Consequence for this page.** [[Abstention]] is currently graded on **whether the model declined**. The variable it is missing is **what the decline disclosed**. ⇒ **The evaluation must move from the wording layer to the answer layer**: score what the exchange leaves the asker able to conclude, not whether the polite form was used. A refusal that narrows the space to one remaining possibility is a disclosure wearing the costume of a refusal.

**Boundaries (do not merge these).**
- **vs [[CitationLock]]** — that page governs *what an answer may cite*; this row governs *what a non-answer can still convey*. They are not in tension; [[CitationLock]] has no jurisdiction over an output that cites nothing.
- **vs [[Provenance]]「Evidence's outer garment」** — that section holds the payload **fixed** and swaps the vessel (a **container** variable, scan line 14). Here the payload is **new**, assembled from several individually legitimate pieces (a **composition** variable, scan line 19). Different axes; the two rows must name each other and stay apart.
- **vs [[MemoryGovernance]]'s reuse of `ABSTAIN`** — there abstention is an *action* over the memory bank; here it is an *output* directed at a counterparty. Only the second has a disclosure channel.

**Scan-line assignment.** This is an instance of **line 19 — composition audit** ("how many items does one verdict carry? if every item passes, does the conclusion they jointly entail also pass?"), registered in `.workbuddy/memory/concept-radar/SCAN-LINES.md`. Its paired revision is [[AgentIdentity]]'s per-hop attenuation, where **per-item pass is written as the success criterion rather than as the boundary.**

⚠️ **Evidence grade, must sit beside the numbers.** **30** hand-built scenarios, human-reviewed but **not validated for realism**; models are the authors' selection; automated judging was checked against **120** human-graded answers but is **not** a full human audit; and **7.08%** and **32.37%** have **different denominators** (best model under benign queries vs. pooled across all intents) ⇒ **they must never be quoted as a before/after pair.** No independent replication.

## See Also
- [[agent-memory-provenance]] — primary source
- [[AgentIdentity]] — where the same row lands on the action side (per-hop attenuation's boundary, 10-25A)
- [[CitationLock]] · [[Provenance]] — the enabling constraints
- [[LongMemEval]] — benchmark that scores abstention
- [[LongTermMemory]] — the system exercising it
