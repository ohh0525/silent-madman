---
title: "Multi-Agent Orchestration"
type: concept
tags: [multi-agent, test-time-communication, orchestration, verifier, cross-contamination, protocol-pivoting]
sources: [multi-agent]
last_updated: 2026-10-16
---

# Multi-Agent Orchestration (多智能体协作)

Multiple agents with **independent context windows** working on one goal: exchanging **verified** partial results, failure paths and intermediate scores through a shared workspace, so that **less total compute beats best-of-k independent sampling** — **provided a verifier exists**. Without a verifier, or under tight compute, communication overhead exceeds its gains and independent agents do better.

## Mechanism (per [[multi-agent]])
- **The exchange object is verified progress, not messages** — k agents, same goal, same compute budget, no preset roles, no central orchestrator; a shared workspace holds partial results, failure paths and code. *The gain comes entirely from building on confirmed breakthroughs and not re-walking confirmed dead ends — not from workflow design.*
- **The verifier is the precondition of the gain.** Only when "who actually progressed" can be judged cheaply does "build on others' progress" work. On LP85, 64 independent attempts all failed while team@5 solved 65% — progress was verifiable. *This turns "should we go multi-agent" from taste into a predicate: first ask whether the task has a verifier.*
- **The counter-result ships with the result.** ARC-AGI-3: team@3 = best@13, team@5 = best@33 (≈4.3× / 6.6× equivalent compute); polyomino packing team@3 SOTA 0.945; MNIST 4-agent classifier 1,957 bytes @ 99.4%. But the paper's own abstract: the method "**fails without verifier or low compute**". *Cite the gain together with its boundary condition, or you are quoting a conditional result as a panacea.*
- **New failure surface: cross-contamination (互相污染).** One agent's unverified conclusion gets inherited by peers as a premise — a failure mode absent from the single-agent world, landing on [[Provenance]]'s extension line: team trust must cover the **verification status of peers' conclusions**, not just fact origin. *(2026-10-16: the authorization-inheritance variant of this failure now carries CVE-grade cross-vendor evidence — see the section below.)*

## Boundary
- **Not subagents** — subagents are threads *inside* one agent (returning a summary to the main context); multi-agent is a **peer team**, members each holding the full goal and an independent window. Claude Code Projects nests both: threads are the team, and each thread can spawn its own subagents.
- **Not shared memory** — [[LongTermMemory]] is one agent's persistence **across sessions** (time dimension); multi-agent is shared state **across agents at one moment** (space dimension). Complementary; the governance of team-shared memory is their open intersection.
- **Not a replacement for [[ContextEngineering]]** — context engineering places content *within* one window; multi-agent decides what to exchange *between* windows. The latter is the former's cross-window extension ([[Compaction]]'s "clean-window subagent returning 1–2k tokens" is the seed).
- **Not "more agents is always better"** — the paper carries its own counter-example (no verifier / tight compute → independent wins); the product carries its own cost (threads each burn quota). A bounded tool, not a free lunch.

## Cross-Protocol Authorization Inheritance — protocol pivoting *(added 2026-10-16)*

> **Draft annotation, pending ingest.** This section is **not yet backed by a source page in this wiki** — its claims were verified against live sources on 2026-10-16 (recorded in `.workbuddy/memory/concept-radar/2026-10-16.md`, candidate 2; ledger row **10-16B**). Remove this banner when the material is ingested and human-reviewed, and move the source slug into the frontmatter `sources` field.

**The seam this page had left empty.** Since 2026-09-26 cross-contamination has been recorded here as the collaboration leg's failure surface — with **no evidence at all** (the page is flagged secondhand throughout). What arrived is CVE-grade, cross-vendor confirmation of the same shape one boundary out: the flaw is not in the **credential** but in **on what authority the task itself travels**.

- **Mechanism — "protocol pivoting" (independent researcher Syed Anas Mohiuddin, ~five months of work).** Attacker text is planted in content one agent reads; that agent passes it on **as a normal delegated task** to a peer it trusts; the peer sits inside the network and performs **SSRF** or another privileged action. The escalation gives the class its name: the text enters via **MCP** and crosses into **A2A** or the emerging **Agent Network Protocol** — "**trust or authorization gets effectively lost in translation**". Why an LLM-side guardrail does not catch it: "**since MCP servers store credentials for each agent — and agents are built to trust every other internal agent — an exploit that would have been rejected by the LLM succeeds.**"
- **Concrete instance — Google.** `googleapis/mcp-toolbox` initialised its Go HTTP client **with no `CheckRedirect` policy and no target-IP validation** ⇒ a crafted path parameter follows a redirect to an internal endpoint, potentially the cloud metadata address **169.254.169.254** (which hands out IAM credentials). **CVE-2026-14540, CVSS 8.0.** The *fix* is the teaching artifact: connection-time resolved-address checks plus IP allow/block lists, and **rejecting an unsafe base URL at startup rather than on first request**. Researcher's own line: "*That is what a real SSRF guard looks like. It is also more work than most MCP servers have done.*" ⇒ *the position of the control was the answer again* — same cross-cutting theme as the orchestration-layer cell.
- **Cross-vendor scope.** Confirmed and fixed at **Google, JPMorgan Chase, Weaviate, France's DINUM** (data.gouv.fr MCP) and **Indonesia's Tangerang city government**; **Rapid7** published **CVE-2026-97228** (CVSS **2.7**, fixed in September). Five MCP servers built for **US federal agencies** (incl. a VA-benefits one) were reported 2026-09-02 and **remain in triage**, described only at class level.
- **Root-cause sentence (Rapid7 · Douglas McKee):** "*Each protocol was built assuming it lived on its own, so each one checks its own front door while nobody watches the hallway in between.*" Operationally: **dependency scanners do not see tool arguments that arrive as delegated agent text**.
- **Counter-evidence, must sit beside the conclusion (X41 D-Sec · Markus Vervier):** the better term remains **indirect prompt injection**, and the cross-protocol hop "*is not strictly required for such attacks to work*". ⇒ **not a new class — an old class with a new reachable range.**

**Boundary vs [[AgentIdentity]]:** per-hop attenuation (RFC 8693) narrows the **credential** — scope / magnitude / validity / depth may only shrink — and says nothing about the **task content** inheriting authority. The rule this cell supplies is therefore *independent*: **every protocol transition should trigger fresh authorization rather than inherit an upstream decision.** Credential narrowing does not entail it.

**Boundary vs the existing 10-13「检索准入 × 跨主体状态隔离」row:** that row asks *whose state is this* (a leak **inside already-admitted shared state**); this row asks *on what authority did this instruction travel* (a leak **at the hand-off**). State ownership vs authorization inheritance — **not a duplicate**.

**Family note:** "*authority is not isolation*" ([[AgentSandbox]], execution side) · "*model output is not the permission*" (orchestration side, 10-16A) · "*access is not authority*" (protocol side, this row) — **three members of one family, one layer apart each**; the shared sentence is **"nobody is checking this stretch."**

⚠️ **Evidence grade:** pattern-level, largely the researcher's own framing amplified by Ars Technica (Dan Goodin, **2026-10-05**); **CVE-2026-14540** is attributed to his self-published write-up (Ars reports severity 8 **without naming the CVE**); **advisories were not re-opened first-hand** here; federal findings are **unpatched / in triage, class-level only**; **every named bug is already fixed** — what is new is the cross-vendor *pattern*, not a zero-day. Presented at **MCPCon North America, 2026-10-23**.

## Why It Matters
- **It is the wiki's first "between agents" page.** All 39 prior pages and both connection diagrams describe a single agent; this page opens the space dimension the wiki had never covered.
- **September 2026 assembled three grades of evidence at once:** a reproducible experiment (team@k vs best@k, Microsoft Research + UC Berkeley), a product entry point (Anthropic's Claude Code Projects: coordinator → parallel cloud threads → shared memory → ordinary merge conflicts, with honest self-declared limits — quota per thread, cloud-only launch, CI/tests/human review as the integration boundary), and decentralised scale (Agensh: 1,024 agents, no central orchestrator, pandoc 33.89% → 55.06%). The question moved from *can multi-agent work* to *when is it worth it and who pays the coordination cost*.
- **The verifier predicate is portable.** "First find a cheap way to judge correctness, then form the team" is the single most reusable sentence in the material.
- **Evidence-grade honesty:** the team@k numbers are secondhand (AlphaSignal's report of the paper; arXiv not opened), Agensh is secondhand, Claude Projects' shared memory has "no detailed performance evaluation" — direction-and-magnitude grade throughout; verbatim citation requires the primary sources. **Still true after 2026-10-16:** the collaboration *gain* remains un-verified first-hand; what changed is that the authorization-inheritance *failure* now carries CVE numbers — **the failure surface has better evidence than the benefit it is meant to bound.**

## See Also
- [[multi-agent]] — source
- [[Compaction]] — whose clean-window-subagent note this page promotes from footnote to mainline
- [[Provenance]] — extended by cross-contamination: peer conclusions need verification status
- [[AgentHarness]] — multi-agent as a productised harness capability (subagent scheduling, duty ④)
- [[ContextEngineering]] — intra-window placement vs inter-window exchange
- [[Agent]] — the single-agent world this page extends
- [[Anthropic]] · [[OpenAI]] — the two productisation paths (Projects coordinator; Agents API subagent flag)
