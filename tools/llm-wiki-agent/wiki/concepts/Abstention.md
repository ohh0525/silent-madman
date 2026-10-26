---
title: "Abstention"
type: concept
tags: [agent-memory, abstention, reliability, abstention-not-terminal, composition-audit, action-conditioned-verification, threshold-ownership]
sources: [agent-memory-provenance]
last_updated: 2026-10-26
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

## Abstention is not binary — it is a budget decision priced by what happens next *(ledger row 10-24A; applied 2026-10-26)*

> **Draft annotation, pending ingest.** Not yet backed by a source page in this wiki — verified against live sources on 2026-10-24 and re-verified on 2026-10-26 (recorded in `.workbuddy/memory/concept-radar/2026-10-24.md`, candidate 1; ledger row **10-24A**). Remove this banner when the material is ingested and human-reviewed, and move the source slug into the frontmatter `sources` field.
>
> 🔴 **Preprint, not peer-reviewed. The 100% / 0% pair is measured *relative to a static policy given the same inputs* — it is not an absolute safety claim.**

**The assumption this page has always carried.** Every criterion above — no sourced evidence ⇒ refuse, [[Provenance]] for origin, [[CitationLock]] for what may be cited — is anchored on **the object**: *did we open it, where did it come from*. **None of it is refuted.** What is displaced is the inference the page never wrote down but has always relied on: **that the object is the only thing the decision depends on.** It is not. It also depends on **what you are about to do with it.**

**AMV-Guard** (`arXiv:2610.31446`, submitted **2026-10-22 15:43:50 UTC**; Yiqi Wang, Yifei Wang, Jiaqi Zhang et al. — Southern Queensland / SUSTech / Jiangsu / Sydney / Uploading; cs.MA; **22 pages / 5 figures / 12 tables**).

> **判据句 (verbatim): "*whether an entry must be re-checked before acting is not a property of the entry: the same remembered address can be used unchecked for a routine shipment but should be re-confirmed before a valuable one.*"**

Formulated as a **sequential stopping problem**: *a verification is worth its cost only if it can change what the agent does next.* Under suitable verifier reliability and cost conditions, **raising the magnitude of the action's consequence moves the same memory through three regimes**:

| Regime | Behaviour | Why |
|---|---|---|
| **Proceed** | act without checking | consequence trivial; the check cannot pay for itself |
| **Verify** | check, then act | the check is cheap, reliable, and could flip the decision |
| **Direct abstention** | refuse without checking | past a consequence level, **even a confirming observation cannot license execution** — the verifier itself has a failure rate |

⇒ **Abstention is the third regime, not the binary alternative to answering.** This is the part the page is missing: it grades abstention as *"did the model decline"*, while the decision variable is **"what would declining, checking, or proceeding each cost, given the next action."** And the counter-intuitive case falls out cleanly — *the most dangerous situation is sometimes the one that checks least and simply refuses*, because raising confidence to 95% is still not enough for an irreversible, high-loss act.

**Mechanism (three steps).** ① **premise extraction** with counterfactual filtering — narrow the retrieved memory to the premises the candidate action actually rests on; ② **calibrated memory-error beliefs** — estimate "this premise is wrong" from age, source reliability, correction history; ③ **bounded VOI selection** — a one-step greedy value-of-information selector with a depth-two fallback, i.e. verification itself is scheduled as an action sequence, not an all-or-nothing switch.

**Numbers.** On **ToolSandbox**, relative to a static policy given the same inputs: mean verification cost **−33.9%** (and **−42.3% / −58.9%** across three agent backbones at zero measured gate harm), **100%** safe-proceed recall, **0%** Gate harmful, Proceed coverage **38.83% → 44.17%**. In a **gate-core transfer to AppWorld** (stopping/VOI core carried over, full structured pipeline not), **−21.3%** cost at a small cost in safe-proceed recall and task success.

**Consequence for this page.** ⇒ **Verification effort must be set by what an agent is about to do, not only by how reliable a memory appears.** Any score computed from the memory alone is **constant in consequence** while the optimal decision changes ⇒ **no memory-only score can reproduce the correct policy.** Safety audits of long-lived agents should report **action-conditioned recall** (was the unsafe action stopped, given what it was about to do) rather than memory accuracy alone — high memory-side accuracy can coexist with failure exactly when the stakes are highest.

**Boundaries (do not merge these).**
- **vs the 10-25A section above (Mosaic Effect)** — that row asks **what a refusal discloses** (an output-channel variable); this row asks **whether refusing is the priced-optimal terminal decision** (a decision-variable). One is about leakage, the other about budgeting. Split columns.
- **vs [[Provenance]] / [[CitationLock]]** — those anchor on the **object** (origin; was it opened). This row anchors on the **action**. All three survive; this row adds the dimension the other two cannot see. It does **not** refute them.
- **vs [[MemoryGovernance]]'s reuse of `ABSTAIN`** — there abstention is an *action over the memory bank*; here it is a *terminal decision about an external act*. Only the second is priced by consequence.
- **vs [[HumanInTheLoop]]** — the gate grades **the final irreversible step**; this row grades **the premises that step rests on** ⇒ **upstream / downstream, in that order.** (The gate-side landing is a section on that page, filed 2026-10-26.)
- **vs ledger row 10-26A (Tether, [[Provenance]] / [[MemoryGovernance]])** — **upstream / downstream, read in that order.** AMV-Guard **presupposes that an invalidation signal arrives**; 10-26A shows that in the common *"the announcement names the key"* shape, **nothing arrives** ⇒ **arrival first, pricing second.**

**Scan-line assignment.** This is the **first instance of line 18 — threshold-ownership audit** ("who owns the threshold: the object being judged, or the act it feeds?"), registered in `.workbuddy/memory/concept-radar/SCAN-LINES.md`.

⚠️ **Evidence grade, must sit beside the numbers.** Preprint, **no peer review**, no independent replication; main results are **ToolSandbox** only, and the AppWorld column is a **partial transfer** that costs safe-proceed recall and task success. **100% / 0% are relative to a static policy with identical inputs — not absolute safety.** 🔴 **The gate's safety is bounded by its premise extractor, and the paper states this itself:** the counterfactual filter can *remove* a proposed premise but cannot *recover* one never proposed ⇒ **extractor recall upper-bounds the pipeline**; on the paper's own out-of-distribution strata, critical-premise recall is **92.45–95.91%** with Gate-harmful as high as **15.19%** (⚠️ these two figures come from a secondary summary of the paper and should be checked against the PDF's tables before being quoted as primary). AMV-Guard coincides with an information-constrained exact planner on every reported ToolSandbox metric — whether that agreement is a property of the policy or an artefact of the instance distribution is untested.

## See Also
- [[agent-memory-provenance]] — primary source
- [[AgentIdentity]] — where the same row lands on the action side (per-hop attenuation's boundary, 10-25A)
- [[CitationLock]] · [[Provenance]] — the enabling constraints
- [[LongMemEval]] — benchmark that scores abstention
- [[LongTermMemory]] — the system exercising it
