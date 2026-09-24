---
title: "MCP"
type: concept
tags: [anthropic, protocol, tools, mcp, stateless, authorization]
sources: [skill, mcp-2026-07-28, agent-identity, tool-hallucination]
last_updated: 2026-09-24
---

# MCP (Model Context Protocol)

A standard protocol for connecting LLMs to external data sources and tools, originated by [[Anthropic]]. As of the **2026-07-28 specification revision** it is a **stateless, request/response** protocol — see [[mcp-2026-07-28]].

## Core primitives
Servers expose three primitives; each has `/list`, `/get`, and (for tools) `tools/call`:

| Primitive | What it is |
|---|---|
| **Tools** | Executable functions the AI app can invoke (file ops, API calls, DB queries) |
| **Resources** | Data sources providing context (file contents, DB records, API responses) |
| **Prompts** | Reusable templates structuring interactions (system prompts, few-shot examples) |

Clients also expose primitives: **Elicitation** (server asks the user for input/confirmation).
**Sampling** and **Logging** are **deprecated** as of 2026-07-28.

## Protocol mechanics (post-2026-07-28)
- **Stateless core** — no `initialize`/`initialized` handshake (SEP-2575), no `Mcp-Session-Id` (SEP-2567). Protocol version, client identity, and capabilities travel in `_meta` **on every request**; an optional `server/discover` RPC can fetch capabilities up front.
- **Any instance can serve any request** — remote servers become plain HTTPS endpoints, scalable behind a round-robin load balancer with no shared session store.
- **State, when needed, becomes an explicit handle** — a tool returns e.g. `basket_id`; the model threads it back as an argument. This is *visible* state the model can reason about, preferred over hidden transport state.
- **Routing headers** — `Mcp-Method` and `Mcp-Name` are now required (SEP-2243) so gateways can route/meter without parsing bodies.
- **Cacheable listings** — `ttlMs` + `cacheScope` on list/read results (SEP-2549).
- **MRTR (SEP-2322)** — server→client requests (elicitation) use Multi Round-Trip Requests instead of a held-open stream: server returns `input_required`, client retries with `inputResponses`.

## Authorization (per [[agent-identity]]) — added 2026-09-24
MCP does not invent an identity model; it borrows the OAuth one, and the division of labour matters:
- An MCP server on **HTTP transport must act as an OAuth 2.1 resource server** and implement **OAuth 2.0 Protected Resource Metadata (RFC 9728)** so clients can discover the authorization server.
- **Clients must implement PKCE with S256**, and must **refuse to continue** when server metadata indicates PKCE is unsupported.
- Consequence: the caller's identity is issued by an **external, dedicated authorization server** (short-lived, audience-restricted) — **not** asserted in MCP protocol messages. A self-declared `clientInfo` field can only ever mean "it says it is X". See [[AgentIdentity]] for why *identity / delegation / authorization / runtime policy* are four distinct things.
- Note the interaction with the stateless revision above: statelessness removes *session* state, and the authorization profile is what carries *authority* instead — per request, verifiable.

## Namespace merging hazard (per [[tool-hallucination]]) — added 2026-09-24
Composing MCP servers is MCP's selling point, and it has a structural cost that the N×M framing hides:
- When several servers are merged into **one namespace**, new failure modes appear that **no single registry can express** — name **collision** and **shadowing**. Two servers both exposing `search` is an ambiguity, not a naming quirk.
- Merging therefore **adds a hallucination surface** rather than just adding tools: the source measures **154** hallucinations on a real merged MCP surface, including frontier models that were clean on a single-registry surface.
- Practical rule: treat a namespace merge as a **review-worthy change**, and run a **closed-world resolution rung** (registry membership + signature check) *before* any permission gate on the dispatch path. See [[ToolHallucination]].

## Boundary with Skill (per [[skill]])
- **MCP** = "connect the tool" (standardizes the interface)
- **Skill** = "teach the model how to use the tool" (organizes the workflow)
- Often used together — MCP server + Skill that documents when to call which tool
- Note: the 2026-07-28 revision changes MCP's *transport/state model*, **not** this boundary.

## Why It Matters
- Solves the "N×M integrations" problem (every LLM × every tool); a single MCP server serves multiple LLM clients.
- Statelessness makes production scaling cheap: GitHub's MCP server removed Redis session storage and deep packet inspection; Manufact cut package size ~83% and gained ~25% speed.
- Composable with [[ProgressiveDisclosure]] and [[ContextEngineering]] — a Skill can document an MCP tool without inlining its interface, and MCP's "code execution" mode keeps large tool payloads out of the context window.
- Adoption scale: >10,000 servers in production by mid-2026; Tier 1 SDK downloads near half-a-billion/month.

## See Also
- [[Skill]] — complementary concept
- [[mcp-2026-07-28]] — the stateless revision source
- [[Anthropic]] — MCP origin
- [[Agent]] — typical consumer that combines Skill + MCP
- [[ContextEngineering]] — MCP code-execution mode is a context-engineering technique
- [[OpenAI]] — adopted MCP in 2025
- [[AgentIdentity]] — MCP's authorization profile is that concept's concrete instance
- [[ToolHallucination]] — the failure mode that namespace merging *creates*; the resolution rung belongs on MCP's dispatch path
