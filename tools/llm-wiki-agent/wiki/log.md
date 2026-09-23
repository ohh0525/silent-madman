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
