---
title: "MCP"
type: concept
tags: [anthropic, protocol, tools, mcp]
sources: [skill]
last_updated: 2026-09-09
---

# MCP (Model Context Protocol)

A standard protocol for connecting LLMs to external data sources and tools, originated by [[Anthropic]].

## Boundary with Skill (per [[skill]])
- **MCP** = "connect the tool" (standardizes the interface)
- **Skill** = "teach the model how to use the tool" (organizes the workflow)
- Often used together — MCP server + Skill that documents when to call which tool

## Why It Matters
- Solves the "N×M integrations" problem (every LLM × every tool)
- A single MCP server can serve multiple LLM clients
- Composable with progressive disclosure — the Skill can document an MCP tool without inlining its interface

## See Also
- [[Skill]] — complementary concept
- [[Anthropic]] — MCP origin
- [[Agent]] — typical consumer that combines Skill + MCP