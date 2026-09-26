---
title: "Overview"
type: synthesis
tags: []
sources: [agent, llm-context, skill, context-engineering, agent-memory-provenance, mcp-2026-07-28, agent-identity, human-in-the-loop, tool-hallucination, agent-harness, agent-sandbox]
last_updated: 2026-09-26
---

# Overview

*This page is maintained by the LLM. It is updated on every ingest to reflect the current synthesis across all sources.*

## Current Synthesis (2026-09-26)

Eleven sources: ten silent-madman concept-learning documents plus a spec digest of the MCP 2026-07-28 revision. The synthesis now has **two halves that answer different questions**. Clusters A–C ask *what the agent knows and sees, and how honestly it remembers* — the **entity side**. Cluster D, ingested 2026-09-24, asks *who the agent is, what it is permitted to do, and whether the thing it just called even exists* — the **actor side**. Cluster E, ingested 2026-09-26, asks *what actually runs the loop* — the **runtime side**. The first two are the **reading discipline** and the **acting discipline**; the third is their **host**: every mechanism in A–D is a part inside a shell that had gone un-named until now.

### Cluster A — Bounded resources (2026-09-05)
- **[[Agent]]** is the autonomous execution layer — a system that picks tools and loops around a goal.
- **[[LLMContext]]** is the hard constraint Agent operates under — a token-budgeted "desktop" bounded by [[Transformer]]'s n² cost.
- **[[Skill]]** is the unit that lets a general model act like a domain expert without bloating context — via **[[ProgressiveDisclosure]]**.

### Cluster B — Methodology + time (2026-09-16)
- **[[ContextEngineering]]** answers *who decides what goes on the desk*: it manages the window by layering information by lifespan, retrieving just-in-time, and trimming/re-injecting each turn. It battles **[[ContextRot]]** and uses **[[Compaction]]** for long tasks. Crucially, it reframes Cluster A: [[ProgressiveDisclosure]] is *an instance* of context engineering, not a separate mechanism.
- **[[LongTermMemory]]** answers *what happens across sessions*: the window cannot hold durable state, so it lives outside and is re-injected. The 2026 design bet is **three parallel memories** (episodic / associative / semantic-HDM) governed by a reading discipline — **[[Provenance]]** (every fact carries origin + time + evidence), **[[CitationLock]]** (cite only what you opened), and **[[Abstention]]** (no sourced evidence ⇒ refuse). Systems: [[MemGPT]], [[AgentZeroMemory]], [[Zep]]; evidence: [[LongMemEval]].

### Cluster C — Protocol refresh (2026-09-16)
- **[[MCP]]** was the one page that had gone stale. The **MCP 2026-07-28 revision** makes the protocol **stateless at the protocol layer**: the `initialize` handshake (SEP-2575) and `Mcp-Session-Id` (SEP-2567) are gone; every request carries version + client identity in `_meta`; `Mcp-Method`/`Mcp-Name` headers enable body-free routing; list results are cacheable (`ttlMs`/`cacheScope`); server→client requests use MRTR (SEP-2322). The **[[Skill]]** boundary is unchanged. Ecosystem impact: GitHub's server dropped Redis + deep packet inspection; Manufact −83% package size, +25% speed.

### Cluster D — Actor side: authority, control, factualness (2026-09-22, ingested 2026-09-24)
- **[[AgentIdentity]]** — *who acts, on whose behalf.* Workload identity + OAuth 2.0 Token Exchange (RFC 8693, carrying a **dual subject**: actor + represented user) + **per-hop attenuation** (a child agent receives a freshly issued, strictly narrower credential — scope / magnitude / validity / depth may only shrink) + dual-subject audit wired to propagated revocation. [[MCP]]'s authorization profile (HTTP servers as OAuth 2.1 resource servers implementing RFC 9728; clients implementing PKCE S256 and refusing when it is unsupported) is its concrete instance.
- **[[HumanInTheLoop]]** — *may it act, now.* Grade every action by **impact × reversibility**, then gate the irreversible classes on the rule "**read freely, keep writes human**". The rule must live **in code/config, not the prompt**; the pause must be **persisted** and the resume **idempotent**; effectiveness is measured by automation / override / **escape** rate and review latency.
- **[[ToolHallucination]]** — *does the tool exist.* Calls to tools that are **not in the registry**, or with undeclared arguments. Such a call is **not a decision any gate ever made**, so it survives every permission check by construction — hence a **closed-world resolution rung** (registry membership + signature verification) placed **upstream of every gate**.

The three compose into one **fixed order**, and the order *is* the content:

```
propose ──▶ resolve ──▶ authorize ──▶ gate ──▶ idempotent execute
            (exists?)    (may you?)   (now?)
       ToolHallucination  AgentIdentity  HumanInTheLoop
```

### Cluster E — Runtime side: the loop's host and where it runs (2026-09-26)
- **[[AgentHarness]]** — *what runs the loop.* The engineering shell that turns one model call into an agent: **`Agent = Model + Harness`**. Four duties — assemble context (tool search over schema injection), run the loop and judge stopping, govern the window (automatic **[[Compaction]]**), keep alive / recover / schedule subagents. It is the **container** of the wiki's mechanism pages, not a peer of them: OpenAI's three Agents-API headline features (compaction / tool search / multi-agent) are exactly pre-existing wiki concepts. Boundary: decides **who orchestrates**, while the sandbox decides **where it runs** (OpenAI splits this as separate `Agent` / `Environment` objects).
- **[[AgentSandbox]]** — *where it runs, what it can touch.* Kernel-level containment (gVisor / Kata / per-sandbox VM) + declarative allow-lists; **authority is not isolation** — a fully legitimate, fully approved action can still run somewhere it can write through the host kernel. This fills the **`execute` leg** of Cluster D's chain, the gap this overview had named since 2026-09-24. As of 2026-09 it is standardised infrastructure (`kubernetes-sigs/agent-sandbox` into SIG Apps; Google AX open-sourced; Alibaba Cloud commercialised). Strongest evidence it is necessary: HF's 2026-07 intrusion anatomy — an allow-list correctly rejected the SSRF, the agent **switched paths** and still leaked pod secrets; *a single layer of defence that denies one path does not close the surface.*
- The layer became **managed infrastructure in 2026-09** ("Harness Wars"): OpenAI rents the Codex harness (public beta 2026-09-10), [[Anthropic]] counters with Opus 5.5 managed orchestration. Managed ≠ safe: egress defaults `enabled`, `restricted` takes only 1–100 exact hostnames, secrets injected into the environment remain exposed — the defaults *are* the security boundary, and same-week Codex sandbox escapes (Heapjack / Overpatch) show management centralises patching, not risk. [[Skill]] is becoming this ecosystem's packaging format (372 / 216 / 193 skills, 2026-09).

### How they connect

```
                        ┌─────────────── ENTITY SIDE (what it knows) ───────────────┐
Context Engineering ──manages/crops──▶ LLM Context Window ◀──supplies trusted── Long-Term Memory
        │                                    ▲                      facts            │
        │ Progressive Disclosure             │                                       │
        │ is one instance of it              │                          Provenance /  │
        ▼                                    │                          CitationLock /│
      Skill ──────loads into─────────────────┘                          Abstention    │
                                                   Agent reads/writes ─────────────────┘

                        ┌─────────────── ACTOR SIDE (what it may do) ───────────────┐
   model proposes ──▶ resolve ──▶ authorize ──▶ gate ──▶ idempotent execute ──▶ audit
                     (ToolHallucination) (AgentIdentity) (HumanInTheLoop)      record
                                                                                ▲
                            same traceability instinct as Provenance ───────────┘

                        ┌─────────────── RUNTIME SIDE (what runs the loop) ─────────┐
   Agent Harness ──hosts──▶ the Agent loop — and inside it: Compaction · tool search ·
   (Agent = Model           the resolution rung · Skill loading · subagent scheduling
    + Harness)                                     │ pluggable
                                                  ▼
                        Agent Sandbox (execute leg) ── gVisor / Kata / per-sandbox VM;
                        declarative egress allow-lists; authority ≠ isolation
```

The eleven-page story: **an Agent, bounded by a Context Window, uses Skills to load knowledge on demand; Context Engineering decides what belongs in that window each step; provenance-aware Long-Term Memory lets it remember across sessions — honestly. On the acting side, it proves who it is with strictly narrowing authority, asks a human before the irreversible step, and can only call tools that provably exist — and even if all of that fails, the sandbox bounds what the action can touch. And all of it — the loop, the compaction, the gates, the subagents — runs inside a harness that as of 2026-09 is itself becoming managed infrastructure.**

## Cross-Cutting Themes
- **Bounded context is the central constraint** — every concept in Clusters A–C traces back to a token / window / cost limit. [[ContextRot]] sharpens it: capacity ≠ effective capacity.
- **"On-demand loading" is the dominant solution shape** — Skills (progressive disclosure), RAG, and memory retrieval all share it. [[ContextEngineering]] names it as a principle.
- **Trust is the new frontier** — Cluster A assumed more/cleaner context; Cluster B adds that retrieved context must be *sourced and current* ([[Provenance]], [[CitationLock]], [[Abstention]]); Cluster D adds that the **actor** must be sourced and constrained too. Trust now has two objects: the *fact* and the *hand*.
- **Memory errors compound** — a mistake written to durable memory recurs; this reframes memory as a *reliability subsystem*, not a recall feature.
- **NEW (2026-09-24) — the model is not the only place to put a control.** Every mechanism in Clusters A–C has **the model itself** as its subject: they are *honesty* mechanisms, enforced by the model's own behaviour. Cluster D moves three levers **outside** the model — issuance (an identity authority), attenuation (a credential chain), and deterministic gating (code). Both the [[human-in-the-loop]] and [[tool-hallucination]] sources are explicit that the gate/rung must **not** be a prompt-resident rule, precisely because a prompt can be ignored, overridden or talked around. This is the first time the wiki records a control whose subject is not the LLM.
- **NEW (2026-09-24) — ordering is a first-class design object.** Three times now the answer has been *where* a mechanism sits rather than how strong it is: the resolution rung must precede every gate; the authorization check precedes the gate; and the gate precedes execution. A control in the wrong position is not a weaker control — it is not a control.
- **NEW (2026-09-26) — the loop needs a host.** Every mechanism page in Clusters A–D implicitly ran inside something that no page named. [[AgentHarness]] names it, and in doing so reorganises the wiki: compaction, the resolution rung, Skill loading and subagent scheduling stop being peers and become **parts of one shell**. The test this suggests for future gaps: for each page, ask *what does this mechanism run inside, and does that thing have a page?*
- **NEW (2026-09-26) — vendor defaults are citable; vendor benchmarks are not.** The harness sources split cleanly into two grades: **documented defaults** (egress `enabled` by default; `restricted` = 1–100 exact hostnames; secrets remain exposed) are facts about the product and can be cited; **self-reported performance** (latency ~¼, cost −60%, failures −86%) is marketing-grade until independently reproduced. The wiki should keep these two grades in separate columns whenever it records vendor claims.
- **[[Anthropic]] is the primary vendor** contributing this design vocabulary; [[OpenAI]] complements; memory systems now contribute [[AgentZeroMemory]], [[MemGPT]], [[Zep]]; the actor side draws on a wider set (Microsoft Entra Agent ID, Okta, and the OAuth/IETF layer) — the first cluster not dominated by one vendor.

## Open Questions (suggested next sources)
- A concrete RAG system case study (vector DB choice, chunking strategy, retrieval quality) — still open from 2026-09-09, now the **oldest** open item.
- ~~The MCP stateless revision (2026-07-28 spec)~~ — **resolved 2026-09-16**: [[MCP]] page rewritten from [[mcp-2026-07-28]].
- How [[ContextEngineering]] techniques are measured end-to-end (beyond single-provider claims) — needs an independent evaluation.
- Multi-agent memory sharing and role-based access control on shared persistent memory.
- MCP **Tasks / MCP Apps / EMA** extensions — now first-class; worth a dedicated page if usage grows.
- ~~**NEW — execution isolation as the missing third leg.**~~ — **resolved 2026-09-26**: [[AgentSandbox]] now fills the `execute` leg of Cluster D's chain (K8s SIG Apps upstream + Google AX + Alibaba Cloud commercialisation + the HF intrusion anatomy as motive evidence; radar candidate 2026-09-21).
- **NEW — persistent execution.** The gate's own requirement — that a paused workflow be resumable by a *different* process, days later — is a durable-execution requirement. (**Partially covered 2026-09-26**: keep-alive / crash recovery is harness duty ④ on [[AgentHarness]], and pause/resume is a sandbox capability on [[AgentSandbox]]; what remains unwritten is the cross-runtime semantics comparison — event replay vs checkpoint adoption vs snapshot. Radar candidate 2026-09-23.)
- **NEW — independent verification of Cluster D's numbers.** Several figures (28% traceability, 1–2 vs 3–6 engineer-weeks) come from third-party/commercial pages rather than primary vendors; see the provenance note on [[agent-identity]]. The 322 / 154 hallucination counts come from a **preprint** (arXiv:2609.19425v1, 2026-09-16), not peer-reviewed — and the material already records one internal inconsistency in its numbers (`3434 vs 33` vs `34 vs 3`) that it declined to use.

## Next Ingest Suggestions
- `raw/papers/rag-survey.md` — RAG foundations (the oldest open gap)
- `raw/papers/context-engineering-eval.md` — independent context-engineering evaluation
- ~~`raw/papers/agent-sandbox-isolation.md`~~ — **resolved 2026-09-26**: [[AgentSandbox]] ingested from the concept-learning material (K8s upstream evidence included); a dedicated *paper* on isolation could still deepen it, but the page exists
- **NEW** an **independent** evaluation of the agent-identity traceability / attenuation claims — the current figures are vendor-survey grade
- **NEW (2026-09-26)** the OpenAI developer documentation for the Agents API itself — the harness material's claims all trace to verified secondary sources; the primary docs were not opened first-hand
