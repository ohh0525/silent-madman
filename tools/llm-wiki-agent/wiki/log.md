# Wiki Log

Append-only chronological record of all operations.

Format: `## [YYYY-MM-DD] <operation> | <title>`

Parse recent entries: `grep "^## \[" wiki/log.md | tail -10`

---

## [2026-09-09] ingest | AI Agent(智能体)
Source: `raw/learning-materials/agent.html`
Created: `wiki/sources/agent.md`, `wiki/concepts/Agent.md`, `wiki/concepts/ReAct.md`
Entities touched: `wiki/entities/Anthropic.md`, `wiki/entities/OpenAI.md`, `wiki/entities/SourceScore.md`
Updated: `wiki/index.md`, `wiki/overview.md`

## [2026-09-09] ingest | LLM Context Window(上下文窗口)
Source: `raw/learning-materials/llm-context.html`
Created: `wiki/sources/llm-context.md`, `wiki/concepts/LLMContext.md`, `wiki/concepts/Token.md`, `wiki/concepts/Transformer.md`, `wiki/concepts/ContextWindow.md`
Entities touched: `wiki/entities/Anthropic.md`, `wiki/entities/BaiduBaike.md`
Updated: `wiki/index.md`, `wiki/overview.md`

## [2026-09-09] ingest | Skill(技能)
Source: `raw/learning-materials/skill.html`
Created: `wiki/sources/skill.md`, `wiki/concepts/Skill.md`, `wiki/concepts/ProgressiveDisclosure.md`, `wiki/concepts/MCP.md`
Entities touched: `wiki/entities/Anthropic.md`, `wiki/entities/OpenAI.md`
Updated: `wiki/index.md`, `wiki/overview.md`

## [2026-09-16] graph | Knowledge graph rebuilt

17 nodes, 50 edges (50 extracted, 0 inferred).

## [2026-09-16] lint | Wiki health check

Tool: `python tools/health.py` (deterministic structural checks, no LLM calls)
Scanned: 17 wiki pages
Found: 1 issue — `wiki/sources/llm-context.md` had no matching `ingest` entry in `log.md`
Cause: frontmatter `title` was `LLM Context Window(大模型上下文窗口)`，while `log.md` and `index.md` both used `LLM Context Window(上下文窗口)`; `health.py` matches log titles against page titles exactly
Fixed: `wiki/sources/llm-context.md` title aligned to `LLM Context Window(上下文窗口)` (single-file edit; `log.md` left append-only)
Re-run result: Empty/Stub 0 ✅ · Index Sync 0 ✅ · Log Coverage 0 ✅
Note: `raw/` was not modified.

## [2026-09-16] ingest | 上下文工程(Context Engineering)

Source: `raw/learning-materials/context-engineering.html`
Created: `wiki/sources/context-engineering.md`, `wiki/concepts/ContextEngineering.md`, `wiki/concepts/ContextRot.md`, `wiki/concepts/Compaction.md`
Entities touched: `wiki/entities/Anthropic.md`
Updated: `wiki/index.md`, `wiki/overview.md`, `wiki/concepts/ProgressiveDisclosure.md` (cross-link)

## [2026-09-16] ingest | 带溯源的智能体长期记忆(Provenance-Aware Memory)

Source: `raw/learning-materials/agent-memory-provenance.html`
Created: `wiki/sources/agent-memory-provenance.md`, `wiki/concepts/LongTermMemory.md`, `wiki/concepts/Provenance.md`, `wiki/concepts/CitationLock.md`, `wiki/concepts/Abstention.md`, `wiki/entities/MemGPT.md`, `wiki/entities/AgentZeroMemory.md`, `wiki/entities/LongMemEval.md`, `wiki/entities/Zep.md`
Updated: `wiki/index.md`, `wiki/overview.md`

## [2026-09-16] ingest | MCP 2026-07-28 Specification(MCP 无状态化修订)

Source: `raw/specs/mcp-2026-07-28.md`
Created: `wiki/sources/mcp-2026-07-28.md`
Updated: `wiki/concepts/MCP.md` (rewritten: added primitives + protocol mechanics + statelessness; retained MCP-vs-Skill boundary), `wiki/index.md`, `wiki/overview.md`
Note: supersedes the pre-2026-07-28 (stateful, session-based) description previously implicit in `MCP.md`. Compiled from official spec blog + official architecture docs + AWS + GitHub changelog + AAIF roundup, all retrieved 2026-09-16.

## [2026-09-16] graph | Knowledge graph rebuilt

30 nodes, 115 edges (115 extracted, 0 inferred).

## [2026-09-16] graph | Knowledge graph rebuilt

31 nodes, 125 edges (125 extracted, 0 inferred).

## [2026-09-16] graph | Knowledge graph rebuilt

31 nodes, 125 edges (125 extracted, 0 inferred).

## [2026-09-16] report | Graph health report generated

31 nodes analyzed.

## [2026-09-16] graph | Knowledge graph rebuilt

31 nodes, 125 edges (125 extracted, 0 inferred).

## [2026-09-16] graph | Knowledge graph rebuilt

31 nodes, 125 edges (125 extracted, 0 inferred).

## [2026-09-17] graph | Knowledge graph rebuilt

31 nodes, 125 edges (125 extracted, 0 inferred).

## [2026-09-17] lint | Daily maintenance (health + custom lint)

Tool: `python tools/health.py` — 31 pages. Empty/Stub 0 ✅ · Index Sync 0 ✅ · Log Coverage 0 ✅
Custom lint over 33 `.md` (4 dimensions): broken `[[wikilinks]]` 0 ✅ · frontmatter issues 0 ✅ · invalid `sources` slugs 0 ✅
Fixed: `[[BaiduBaike]]` and `[[SourceScore]]` had no inbound wikilink (reachable only via `index.md`). Added inbound links — `[[BaiduBaike]]` from `sources/llm-context.md` and `sources/skill.md`, `[[SourceScore]]` from `sources/agent.md` — after verifying both references exist in the raw material (`raw/learning-materials/llm-context.html`, `skill.html`, `agent.html`). Bumped `last_updated` on those 3 source pages.
raw/: no new un-ingested material — all 6 `source_file` targets still resolve.
Note: `raw/` untouched; no files deleted; `overview.md` synthesis still current (no new sources today).

## [2026-09-17] graph | Knowledge graph rebuilt

31 nodes, 125 edges (125 extracted, 0 inferred).

## [2026-09-18] lint | Daily maintenance (health + custom lint)

Tool: `python tools/health.py` — 31 pages. Empty/Stub 0 ✅ · Index Sync 0 ✅ · Log Coverage 0 ✅
Custom lint over 33 `.md` (5 dimensions): broken wikilinks 0 ✅ · orphan pages 0 ✅ · frontmatter issues 0 ✅ · invalid `sources` slugs 0 ✅ · index↔disk mismatch 0 ✅
Note on the single scan alert: `log.md` line 94 contains the literal string `[[wikilinks]]` as narrative prose (not a page reference); `log.md` is a structural file and is excluded from the link dimension. Not a real broken link.
raw/: no new un-ingested material — all 6 `source_file` targets still resolve (5 concept HTML + 1 MCP spec).
Orphans: the two entity pages fixed on 2026-09-17 (`BaiduBaike`, `SourceScore`) still have inbound links — no regression.
Fixes: none needed (all dimensions clean). No wiki content page was modified; only this log entry was appended.
Graph: not rebuilt — no change in graph inputs (no new pages, no new cross-page links; this entry adds no wikilink), per the repo rule against meaningless diff / commit churn. Graph remains 31 nodes / 125 edges / 3 communities.
overview.md: synthesis judged still current (no new sources today) — left unchanged. Flagged for the human only, as a suggestion, that the 2026 "Agent Harness" signal may structurally refine the current Cluster A/B framing; nothing was edited.
Note: `raw/` untouched; no files deleted.

## [2026-09-19] lint | Daily maintenance (health + custom lint)

Tool: `python tools/health.py` — 31 pages. Empty/Stub 0 ✅ · Index Sync 0 ✅ · Log Coverage 0 ✅
Custom lint over 33 `.md` (5 dimensions): broken wikilinks 0 ✅ · orphan pages 0 ✅ · frontmatter issues 0 ✅ · invalid `sources` slugs 0 ✅ · index↔disk mismatch (forward + reverse) 0 ✅
Note on the single scan alert: `log.md` line ~94 contains the literal string `[[wikilinks]]` as narrative prose (not a page reference); `log.md` is a structural file and is excluded from the link dimension. Not a real broken link.
raw/: no new un-ingested material — all 6 `source_file` targets still resolve (5 concept HTML + 1 MCP spec).
Orphans: the two entity pages fixed on 2026-09-17 (`BaiduBaike`, `SourceScore`) still have inbound links — no regression; every non-structural page has ≥2 inbound links.
Fixes: none needed (all dimensions clean). No wiki content page was modified; only this log entry was appended.
Graph: not rebuilt — no change in graph inputs. Graph remains 31 nodes / 125 edges / 3 communities.
overview.md: synthesis judged still current (no new sources today) — left unchanged. Flagged for the human only, as a suggestion, that the A2A (Agent2Agent) horizontal-protocol signal may warrant a protocol-layer node next to [[MCP]] (MCP = agent→tool vertical, A2A = agent→agent horizontal); nothing was edited.
Note: `raw/` untouched; no files deleted.

## [2026-09-20] lint | Daily maintenance (health + custom lint)

Tool: `python tools/health.py` — 31 pages. Empty/Stub 0 ✅ · Index Sync 0 ✅ · Log Coverage 0 ✅
Custom lint over 33 `.md` (5 dimensions): broken wikilinks 0 ✅ · orphan pages 0 ✅ · frontmatter issues 0 ✅ · invalid `sources` slugs 0 ✅ · index↔disk mismatch (forward + reverse) 0 ✅
Note on the single scan alert: `log.md` contained the literal string `[[wikilinks]]` as narrative prose (not a page reference); `log.md` is a structural file and is excluded from the link dimension. Not a real broken link.
raw/: no new un-ingested material — all 6 `source_file` targets still resolve (5 concept HTML + 1 MCP spec).
Orphans: the two entity pages fixed on 2026-09-17 (`BaiduBaike`, `SourceScore`) still have inbound links — no regression; every non-structural page has ≥2 inbound links (29/29).
Fixes: none needed (all dimensions clean). No wiki content page was modified; only this log entry was appended.
Graph: not rebuilt — no change in graph inputs. Graph remains 31 nodes / 125 edges / 3 communities.
overview.md: synthesis judged still current (no new sources today) — left unchanged. Flagged for the human only, as a suggestion, that the "context economics" signal (prompt caching / KV cache as a *price* axis, next to the existing *quantity* axis of [[Token]] / [[LLMContext]]) may refine the Cluster A framing; nothing was edited.
Note: `raw/` untouched; no files deleted.

## [2026-09-21] lint | Daily maintenance (health + custom lint)

Tool: `python tools/health.py` — 31 pages. Empty/Stub 0 ✅ · Index Sync 0 ✅ · Log Coverage 0 ✅
Custom lint over 33 `.md` (5 dimensions): broken wikilinks 0 ✅ · orphan pages 0 ✅ · frontmatter issues 0 ✅ · invalid `sources` slugs 0 ✅ · index↔disk mismatch (forward + reverse) 0 ✅
Note on the single scan alert: `log.md` contains the literal string `[[wikilinks]]` as narrative prose (4 occurrences, not page references); `log.md` is a structural file and is excluded from the link dimension. Not a real broken link.
raw/: no new un-ingested material — all 6 `source_file` targets still resolve (5 concept HTML + 1 MCP spec); newest `raw/` mtime is still 2026-09-16.
Orphans: no regression — all 30 non-structural pages have ≥2 distinct inbound linking pages (min = 2: `concepts/ContextWindow.md`, `concepts/ReAct.md`, `entities/SourceScore.md`, `sources/mcp-2026-07-28.md`).
Fixes: none needed (all dimensions clean). No wiki content page was modified; only this log entry was appended.
Graph: not rebuilt — no change in graph inputs. Graph remains 31 nodes / 125 edges / 3 communities.
overview.md: synthesis judged still current (no new sources today) — left unchanged. Flagged for the human only, as a suggestion, that the 2026-09-16/17 evidence on **compaction fidelity & safety** (OpenAI's official disclosure of model-generated instructions written into compaction summaries; the 176-config harness ablation finding that rule-based elision *before* summarization beats summarization-first) may require a *fidelity/safety* axis next to [[Compaction]] in the Cluster B framing; nothing was edited.
Note: `raw/` untouched; no files deleted.

## [2026-09-22] lint | Daily maintenance (health + custom lint)

Tool: `python tools/health.py` — 31 pages. Empty/Stub 0 ✅ · Index Sync 0 ✅ · Log Coverage 0 ✅
Custom lint over 33 `.md` (5 dimensions): broken wikilinks 0 ✅ · pages missing from `index.md` 0 ✅ · frontmatter issues 0 ✅ · invalid `sources` slugs 0 ✅ · index↔disk mismatch (forward + reverse) 0 ✅
Note on the recurring scan alert: `log.md` contains the literal string `[[wikilinks]]` as narrative prose (not page references); structural files (`index.md` / `log.md` / `overview.md`) are excluded from the link dimension. Not a real broken link.
raw/: no new un-ingested material — all 6 `source_file` targets still resolve (5 concept HTML + 1 MCP spec); newest `raw/` mtime is still 2026-09-16.
Reachability: measured strictly as *distinct non-structural pages that wikilink to a page* (structural files excluded, self-links excluded). Two nodes sit at 1 inbound — `entities/SourceScore.md` (cited only by `sources/agent.md`) and `sources/mcp-2026-07-28.md` (cited by `concepts/MCP.md`). Both are legitimately single-source nodes and both are listed in `index.md`, so neither is an orphan. The previous days' "min = 2" figure came from a looser count that also credited structural-file mentions (`log.md` / `overview.md`); the difference is a counting rule, not a regression. No link was added — `SourceScore` is cited in only one raw document, so a second inbound link could not be sourced.
Fixes: none needed (all dimensions clean). No wiki content page was modified; only this log entry was appended.
Graph: not rebuilt — no change in graph inputs. Graph remains 31 nodes / 125 edges / 3 communities.
overview.md: synthesis judged still current (no new sources today) — left unchanged. Flagged for the human only, as a suggestion, that two unreviewed radar themes from 2026-09-18 through 2026-09-21 are now each tabled for the third or second time (**compaction fidelity & safety** against [[Compaction]]; **memory-use timing as a learned policy** against [[LongTermMemory]]). Both would be *revisions* to existing pages, not new nodes; per standing constraint nothing was edited.
Note: `raw/` untouched; no files deleted.

## [2026-09-23] lint | Daily maintenance (health + custom lint)

Tool: `python tools/health.py` — 31 pages. Empty/Stub 0 ✅ · Index Sync 0 ✅ · Log Coverage 0 ✅
Custom lint over 33 `.md` (5 dimensions): broken wikilinks 0 ✅ · pages missing from `index.md` 0 ✅ · frontmatter issues 0 ✅ (incl. `sources/` pages checked for `date` + `source_file`) · invalid `sources` slugs 0 ✅ · index↔disk mismatch (forward + reverse) 0 ✅
Note on the recurring scan alert: `log.md` / `index.md` / `overview.md` contain literal `[[...]]` strings as narrative prose (not page references); structural files are excluded from the link dimension. Not a real broken link.
raw/: no new un-ingested material — all 6 `source_file` targets still resolve (5 concept HTML + 1 MCP spec); newest `raw/` mtime is still 2026-09-16. Coverage check 6/6, un-ingested 0.
Reachability (strict rule, unchanged from 2026-09-22: distinct non-structural pages that wikilink to a page; structural files and self-links excluded): still no dead ends — min = 1 (`entities/SourceScore.md`, `sources/mcp-2026-07-28.md`), both legitimately single-source and both listed in `index.md`, so neither is an orphan. No regression; no link was added (neither node has a second documented source in `raw/`, and inventing one would fabricate a relation).
Fixes: none needed (all dimensions clean). No wiki content page was modified; only this log entry was appended.
Graph: not rebuilt — no change in graph inputs. Graph remains 31 nodes / 125 edges / 3 communities.
overview.md: synthesis judged still current (no new sources today) — left unchanged.
⚠️ Flag for the human (not acted on): commit `bc022af` added **three** new learning materials at repo root — `learning-materials/agent-identity.html`, `human-in-the-loop.html`, `tool-hallucination.html` (the 2026-09-22 radar's candidates 1–3, "行动侧"), and registered them in `README.md` and `concept-relationship.md` ("扩展二 · 行动侧"). They are **not** under `raw/`, and the README labels each of them **待核查** (pending human review). Per the ingest workflow (whose entry point is `raw/`) and the README's 人工核查承诺, both conditions point the same way, so they were **not** ingested, **no** wiki page was written, and nothing was copied into `raw/`. Note the wiki layer itself is unchanged (33 `.md`, 31 pages) — this does **not** make `overview.md` stale in Phase-1 terms. Suggested (human-gated) sequence: human review → place the three files at `raw/learning-materials/` → ingest (would take sources from 6 to 9) → then `overview.md` would need a genuine synthesis **revision**, not an annotation: the wiki would gain its first **actor-side** cluster (identity / approval gate / tool factualness) to set against the existing entity-side [[Provenance]] / [[CitationLock]] / [[Abstention]] cluster.
Note: `raw/` untouched; no files deleted.

## [2026-09-24] lint | Daily maintenance (health + custom lint)

Tool: `python tools/health.py` — 31 pages. Empty/Stub 0 ✅ · Index Sync 0 ✅ · Log Coverage 0 ✅
Custom lint over 33 `.md` (5 dimensions): broken wikilinks 0 ✅ · pages missing from `index.md` 0 ✅ · frontmatter issues 0 ✅ (incl. `sources/` pages checked for `date` + `source_file`) · invalid `sources` slugs 0 ✅ · index↔disk mismatch (forward + reverse) 0 ✅
Note on the recurring scan alert: `log.md` / `index.md` / `overview.md` contain literal `[[...]]` strings as narrative prose (not page references); structural files are excluded from the link dimension — 8th consecutive day for this same false positive. Not a real broken link.
raw/: no new un-ingested material — all 6 `source_file` targets still resolve (5 concept HTML + 1 MCP spec); newest `raw/` mtime is still 2026-09-16 for the 8th consecutive day. Coverage check 6/6, un-ingested 0.
Reachability (strict rule, unchanged since 2026-09-22: distinct non-structural pages that wikilink to a page; structural files and self-links excluded): identical, node for node, to 2026-09-22 and 2026-09-23 — no dead ends, min = 1 (`entities/SourceScore.md`, `sources/mcp-2026-07-28.md`), both legitimately single-source and both listed in `index.md`, so neither is an orphan. No regression; no link was added (neither node has a second documented source in `raw/`, and inventing one would fabricate a relation).
Fixes: none needed (all dimensions clean). No wiki content page was modified; only this log entry was appended.
Graph: not rebuilt — no change in graph inputs. Graph remains 31 nodes / 125 edges / 3 communities.
overview.md: synthesis judged still current (no new sources today) — left unchanged.
⚠️ Flag for the human (unchanged, not acted on): the three 待核查 materials from commit `bc022af` — `learning-materials/agent-identity.html`, `human-in-the-loop.html`, `tool-hallucination.html` — are still **not** under `raw/`, **not** ingested, and **no** wiki page was written for them. Status is identical to 2026-09-22 / 2026-09-23; the wiki layer is unchanged (33 `.md`, 31 pages). The "learning-materials/ → raw/" delivery step remains an unclaimed process gap that the human must either perform or explicitly delegate.
Note: `raw/` untouched; no files deleted.

## [2026-09-24] note | Boundary annotation added to LongTermMemory.md (memory lifecycle / forgetting)

Operation label `note` (outside the documented set ingest/query/health/lint/graph) is used deliberately: this was **neither a full ingest nor a lint**. No source page was written and no new `sources` slug was created, so the source pages count stays at 6.
Trigger: concept-radar 2026-09-24, candidate 1 — the memory cluster ([[LongTermMemory]] / [[Provenance]] / [[CitationLock]] / [[Abstention]]) documented only the *first half* of a memory's life (store it, split it by purpose, read it credibly) and had **no page discussing deletion**.
Change: appended one `## Boundary Note — the other half of a memory's life` section to `wiki/concepts/LongTermMemory.md`; bumped `last_updated` 2026-09-16 → 2026-09-24; added tag `memory-lifecycle`. Added wikilinks: [[Provenance]] and [[Compaction]] — both existing pages, no new dangling link. No existing text was altered or removed.
Content in one line: retention is per-type (episodic → semantic → procedural), the sharpest seam is **deletion vs [[Provenance]]** (erasing a fact breaks the citation chain, so deletion must itself leave a receipt + failure list + rollback snapshot), and this is **not [[Compaction]]** — compaction is in-window, per-turn; lifecycle governance is out-of-window, cross-session, offline.
⚠️ **The section carries a `pending ingest` banner.** Its claims were verified against live primary sources on 2026-09-24 (recorded in `.workbuddy/memory/concept-radar/2026-09-24.md`), but they are **not yet backed by a source page in this wiki** and have **not** been human-reviewed. When the material is ingested, the banner should be removed and the source slug moved into the frontmatter `sources` field. Frontmatter `sources` was intentionally **left untouched** (`[agent-memory-provenance]`) because referencing a slug that does not exist would break the lint's `sources`-slug dimension.
Post-change validation: `python tools/health.py` → 31 pages, Empty/Stub 0 ✅ · Index Sync 0 ✅ · Log Coverage 0 ✅. No files deleted; `raw/` untouched.

## [2026-09-24] ingest | 智能体身份与委派授权(Agent Identity & Delegated Authority)

Authorised by the human this session ("授权摄取这 3 份 HTML") — the previously-flagged `learning-materials/ → raw/` process gap. **Copies only:** the three HTMLs were copied from `learning-materials/` to `raw/learning-materials/` and verified **byte-identical** by sha256 (`6c0f79d4…`, `b4f15b67…`, `fd3a52b0…`); the originals were **not** moved or deleted.
Source: `raw/learning-materials/agent-identity.html` (silent-madman concept-learning HTML, generated 2026-09-22). Source page: `wiki/sources/agent-identity.md`.
Core: identity ≠ a name in the prompt; the agent never holds the user's raw credentials (OAuth 2.0 Token Exchange, RFC 8693, dual subject = actor + subject); **per-hop attenuation** (a child agent gets a fresh, strictly narrower credential — RFC 8693 records delegation but does not guarantee attenuation); four distinct things (identity / delegation / authorization / runtime policy); [[MCP]]'s authorization profile (OAuth 2.1 resource server + RFC 9728 + PKCE S256) as the concrete instance; explicitly **not** a sandbox; 2026 adoption (Entra Agent ID GA 2026-05-01, Okta for AI Agents GA 2026-04-29, APASS >1,000,000 agents / 442 providers).
New concept page: `wiki/concepts/AgentIdentity.md`.
Provenance caution recorded on the source page: the 28% traceability figure and the 1–2 / 3–6 engineer-week estimates come from third-party/commercial pages (ZDNet Inside, mm-ais), i.e. **vendor-survey grade**.

## [2026-09-24] ingest | 人在环审批闸门(Human-in-the-Loop / Escalation Gate)

Source: `raw/learning-materials/human-in-the-loop.html` (same 2026-09-22 batch). Source page: `wiki/sources/human-in-the-loop.md`.
Core: grade actions by **impact × reversibility**; supervision mode chosen **per action class** (in-the-loop / on-the-loop / automatic + sampling); split **proposal** from **side-effecting execution**; the gate's decision must be **deterministic and live in code/config, not the prompt**; pause must be **persisted** and resume **idempotent** (the resuming process need not be the pausing one); measure automation / override / **escape** rate / review latency. Operating rule: "**read freely, keep writes human**".
Boundary the source draws explicitly (recorded because it sharpens this wiki): **[[Abstention]] and [[CitationLock]] have the model as their subject and govern *saying* (honesty mechanisms); a gate has the system and the human as subject and governs *writing / paying / deleting* (a control mechanism).**
New concept page: `wiki/concepts/HumanInTheLoop.md`.
Provenance cautions carried over from the material, and **excluded from being used as evidence**: the uncited "HITL ≈ 99.9% vs ≈ 80%" blog number (deliberately not used); the `< 0.92` confidence threshold (an illustrative example, not a finding); the Bain (n=951) and MIT SMR figures (second-hand).

## [2026-09-24] ingest | 工具幻觉与封闭世界消解(Tool Hallucination & Closed-World Resolution)

Source: `raw/learning-materials/tool-hallucination.html` (same 2026-09-22 batch). Source page: `wiki/sources/tool-hallucination.md`. Primary source: **arXiv:2609.19425v1 (2026-09-16, preprint — not peer-reviewed).**
Core: tool hallucination = invoking a tool that is **not in the registry**, or passing arguments **no schema declared**; such a call is **structurally not a decision any gate ever made**, so no permission gate can refuse it; the fix is a **Resolution Rung** (registry membership + signature verification) whose value is **in its position, not its algorithm** — upstream of every gate. Measured: **322** hallucinations over 10 hosted models / two invocation surfaces; **154** on a real MCP surface after merging; **scale gives no immunity** (675B ≈ 7–8B); merging MCP servers into one namespace **adds** a surface via **collision / shadowing**; an irreducible residual exists ("borrowed parameters" are schema-indistinguishable from legitimate calls). Release artifact: benchmark **HTB**.
New concept page: `wiki/concepts/ToolHallucination.md`.
⚠️ **Discrepancy recorded, not resolved:** the arXiv abstract writes `3434 vs. 33` for surface concentration while two secondary sources transcribe `34 vs. 3`; `322` with `34/3` is self-consistent and `3434` is not. The material (and this wiki) therefore cite **only 322 / 154 / 675B ≈ 7–8B**, and neither uses that ratio. Resolve against the arXiv body text before citing.

## [2026-09-24] ingest | Post-ingest validation (3 action-side sources)

Sources 6 → **9**; wiki pages 31 → **34** (3 new source pages, 3 new concept pages; 2 existing concept pages updated additively: [[MCP]], [[Agent]]).
`[[MCP]]` gained two sections contributed by this batch — an **authorization** profile (OAuth 2.1 resource server, RFC 9728, PKCE S256) and a **namespace-merging hazard** (collision / shadowing; merging adds a hallucination surface) — plus its frontmatter `sources` grew to `[skill, mcp-2026-07-28, agent-identity, tool-hallucination]`. `[[Agent]]` gained an **Authority axis** section and its frontmatter `sources` now includes the three new slugs; its previously implicit gap (the loop can be correct and still unauthorized / unapproved / aimed at a non-existent tool) is now explicit.
`wiki/index.md` updated: 3 new Sources entries + 3 new Concepts entries.
`wiki/overview.md`: **revised, not annotated** — this batch is the wiki's first **actor-side** cluster, so the synthesis gained a Cluster D, a two-halves table (entity side = what it knows / actor side = what it may do), an updated connection diagram, two new cross-cutting themes ("the model is not the only place to put a control"; "ordering is a first-class design object"), three new open questions (execution isolation, persistent execution, independent verification of Cluster D's numbers) and two new ingest suggestions.
No dangling `[[wikilink]]` introduced: every new link targets a page that now exists ([[AgentIdentity]], [[HumanInTheLoop]], [[ToolHallucination]], the three new source slugs) or already existed ([[Agent]], [[MCP]], [[Skill]], [[Provenance]], [[Abstention]], [[CitationLock]], [[ContextEngineering]], [[Transformer]], [[LLMContext]], [[ProgressiveDisclosure]], [[ContextRot]], [[Compaction]], [[LongTermMemory]], [[MemGPT]], [[AgentZeroMemory]], [[Zep]], [[LongMemEval]], [[Anthropic]], [[OpenAI]]).
`wiki/concepts/LongTermMemory.md` keeps the `pending ingest` banner added earlier the same day — that note's claims are still sourced only to the concept-radar report, not to a source page, so the banner stays until that material is ingested.
`raw/` was **not modified**: three files were **added** to `raw/learning-materials/` under explicit human authorisation; nothing in `raw/` was edited or deleted, and no file anywhere was deleted.

## [2026-09-25] lint | Daily maintenance (health + custom lint)

First maintenance day after the 2026-09-24 actor-side triple ingest. Wiki now at **9 sources / 37 pages**.
`tools/health.py`: 37 pages · Empty/Stub 0 ✅ · Index Sync 0 ✅ · Log Coverage 0 ✅.
Custom 5-dimension lint: dangling `[[wikilink]]` 0 ✅ · orphan pages (0 inbound links) 0 ✅ · frontmatter completeness 0 issues (incl. `sources/` pages' `date` + `source_file`) · `sources` slugs all valid (9/9) · `index.md` ↔ disk 0 divergence (forward + reverse).
`raw/` scan: **0 un-ingested files** (9/9 `source_file` targets exist; latest addition 2026-09-24). No fixes required; **no wiki content page modified today**. `overview.md` synthesis (2026-09-24) remains current — Cluster D's three open questions (execution isolation / persistent execution / independent verification of Cluster D's numbers) all remain open.
External signal note (for the record, not ingested): this week's news independently converges on two of those open questions — execution isolation (Docker Cloud Sandboxes + OCI-standard Kits, 2026-09-24; Nvidia OpenShell, 2026-09-21) and agent-memory evaluation (Agent Memory Challenge Cycle 2, opened 2026-09-20). Details in `.workbuddy/memory/concept-radar/2026-09-25.md`.

## [2026-09-26] lint | Daily maintenance (health + custom lint)

Second maintenance day after the 2026-09-24 actor-side triple ingest. Wiki unchanged at **9 sources / 37 pages**.
`tools/health.py`: 37 pages · Empty/Stub 0 ✅ · Index Sync 0 ✅ · Log Coverage 0 ✅.
Custom 5-dimension lint: dangling `[[wikilink]]` 0 ✅ · orphan pages (0 inbound links) 0 ✅ · frontmatter completeness 0 issues (incl. `sources/` pages' `date` + `source_file`) · `sources` slugs all valid (9/9) · `index.md` ↔ disk 0 divergence (forward + reverse).
Recurring scan alert (10th consecutive day, same false positive): `log.md` contains 10 literal `[[wikilinks]]` / `[[...]]` / `[[wikilink]]` strings as narrative prose describing the lint rule itself, not page references; structural files are excluded from the link dimension.
Reachability (strict rule, unchanged since 2026-09-22: distinct non-structural pages that wikilink to a page; structural files and self-links excluded): identical, node for node, to 2026-09-22 → 2026-09-25 — no dead ends, min = 1 (`entities/SourceScore.md`, `sources/mcp-2026-07-28.md`), both legitimately single-source and both listed in `index.md`, so neither is an orphan. No regression; no link added (neither node has a second documented source in `raw/`, and inventing one would fabricate a relation).
`raw/` scan: **0 un-ingested files** (9/9 `source_file` targets exist; latest addition still 2026-09-24).
Fixes: none needed (all dimensions clean). No wiki content page was modified; only this log entry was appended.
Graph: not rebuilt — no change in graph inputs. Graph remains 31 nodes / 125 edges / 3 communities.
`overview.md`: synthesis judged still current (no new sources today) — left unchanged. Its three Cluster-D open questions (execution isolation / persistent execution / independent verification of Cluster D's numbers) all remain open. Note for the human: this week's external evidence has moved **execution isolation** from "vendors shipping products" to "**being standardised as infrastructure**" — see the radar note below — but that is a change in the world, not in this wiki's synthesis, so nothing was edited.
External signal note (for the record, not ingested): the three radar candidates for 2026-09-26 are the three layers of the agent **runtime** — orchestration (agent harness; OpenAI Agents API / Codex harness public beta 2026-09-10, Anthropic Opus 5.5), execution (sandbox; `kubernetes-sigs/agent-sandbox` as a SIG Apps subproject, Google AX open-sourced, Alibaba Cloud Agent Sandbox commercialised 2026-09-22) and collaboration (multi-agent; Microsoft Research + UC Berkeley `team@k` vs `best@k`). The wiki covers the **model side** of all three and none of the runtime layers. Details in `.workbuddy/memory/concept-radar/2026-09-26.md`.

## [2026-09-26] ingest | Agent Harness(智能体外壳)

Sources 9 → **10**; wiki pages 37 → **39** (1 new source page, 1 new concept page; 1 existing concept page updated additively: [[Agent]]).
**Authorisation note:** ingested under explicit user instruction ("你帮我做完", 2026-09-26) — the material was generated the same day by the concept-explainer skill and the user directed the automation to complete the full chain (raw → ingest → graph revision) without the usual line-by-line personal check. All factual claims trace to the 2026-09-26 concept radar's WebSearch/WebFetch-verified sources; the OpenAI primary developer docs were not opened first-hand and this limitation is recorded on the source page.
`raw/` was **not modified**: one file was **added** to `raw/learning-materials/` (byte-identical copy, md5-verified) under explicit user authorisation; nothing in `raw/` was edited or deleted, and no file anywhere was deleted.
New pages: `wiki/sources/agent-harness.md` and `wiki/concepts/AgentHarness.md`. `[[Agent]]` gained a **Runtime axis** section (semantics vs implementation, `Agent = Model + Harness`, parts-vs-container reading of the wiki's mechanism pages) and its frontmatter `sources` grew to include `agent-harness`.
`wiki/index.md` updated: 1 new Sources entry + 1 new Concepts entry.
`wiki/overview.md`: **revised** — new **Cluster E (runtime side: the loop's host)**; connection diagram gains a third RUNTIME SIDE row; the nine-page story became the ten-page story; two new cross-cutting themes ("the loop needs a host" — the what-does-this-run-inside test for future gaps; "vendor defaults are citable, vendor benchmarks are not"); open questions updated (execution isolation sharpened to the named `execute` leg; persistent execution partially covered by harness duty ④, cross-runtime semantics comparison still unwritten); one new ingest suggestion (the OpenAI primary docs).
No dangling `[[wikilink]]` introduced: every new link targets a page that now exists ([[AgentHarness]], the new source slug) or already existed ([[Agent]], [[Compaction]], [[ToolHallucination]], [[Skill]], [[ContextEngineering]], [[HumanInTheLoop]], [[MCP]], [[OpenAI]], [[Anthropic]]).
Outside the wiki, the repo-level `concept-relationship.md` gained a "扩展三 · 运行时底座" section (Mermaid diagram: harness as the base layer hosting the existing parts, pluggable environment below); its stale "行动侧三份待核查" banner (superseded by the 2026-09-24 ingest) was corrected in the same pass.
`graph/`: **not rebuilt**. `build_graph.py` pass 1 extracted 256 edges from the 39 pages, but pass 2 (semantic inference) requires `litellm`, which is not installed in this environment — running `--no-infer` would overwrite the tracked graph.json (which contains INFERRED edges) with an extracted-only downgrade, so the graph was left untouched, consistent with the 2026-09-24 ingest. **Note for the human:** the tracked graph dates to 2026-09-17 and therefore predates both the 09-24 and 09-26 ingests; when an inference-capable environment is available, one rebuild will catch up both. (Suggestion only — not executed.)

## [2026-09-26] ingest | Agent 沙箱与执行隔离(Agent Sandbox / Execution Isolation)

Sources 10 → **11**; wiki pages 39 → **41** (1 new source page, 1 new concept page; 1 existing concept page updated additively: [[AgentHarness]] — sandbox boundary link + See Also).
**Authorisation note:** ingested under explicit user instruction ("继续做", 2026-09-26) continuing the same-day authorised chain; not a line-by-line human check. All factual claims trace to the 2026-09-26 concept radar's WebSearch/WebFetch-verified sources; vendor capacity numbers (GKE 16×, AX, Alibaba) are flagged as direction-grade on the source page.
`raw/`: one file **added** (`agent-sandbox.html`, byte-identical, md5-verified); nothing in `raw/` edited or deleted.
New pages: `wiki/sources/agent-sandbox.md` and `wiki/concepts/AgentSandbox.md` — kernel-level containment (gVisor/Kata/per-sandbox VM), declarative allow-lists, K8s SIG Apps upstream CRDs, warm-pool lifecycle, **authority ≠ isolation**, and the HF 2026-07 intrusion anatomy ("a single layer of defence that denies one path does not close the surface").
`wiki/index.md`: +1 Sources entry, +1 Concepts entry. `wiki/overview.md`: Cluster E extended with the [[AgentSandbox]] bullet (title now "the loop's host and where it runs"); the RUNTIME SIDE diagram's "still an open page" placeholder replaced with the sandbox; the eleven-page story adds "even if all of that fails, the sandbox bounds what the action can touch"; open question **"execution isolation as the missing third leg" marked resolved** (the `execute` leg of Cluster D's chain is now filled); persistent-execution open question updated (pause/resume partially covered by harness duty ④ + sandbox); sandbox ingest suggestion marked resolved.
**Post-ingest validation incident, recorded for honesty:** two overview.md edits made during the previous (agent-harness) ingest — the "sharpened 2026-09-26" open-question revision and the "OpenAI primary docs" next-ingest suggestion — were found **missing** from both disk and the previous commit (cause unknown; all other files from that batch verified intact). Both were re-applied during this ingest and are now included. Lesson applied: run the post-ingest grep verification over *content anchors*, not just structural health, before committing.
Outside the wiki, the repo-level `concept-relationship.md` gained "扩展四 · 执行隔离" (decision-makers vs containment-shell diagram; the `execute` cell of the action-side chain filled) and the 扩展三 sandbox node was updated from "页待建" to built.
