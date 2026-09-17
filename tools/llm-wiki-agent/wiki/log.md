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
