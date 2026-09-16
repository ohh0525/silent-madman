---
title: "MemGPT"
type: entity
tags: [system, memory, os-analogy]
sources: [agent-memory-provenance]
last_updated: 2026-09-16
---

# MemGPT

An OS-inspired LLM system introducing **virtual context management** — treating the context window as constrained main memory and paging data between fast (context) and slow (external storage) tiers via function calls. Paper: *MemGPT: Towards LLMs as Operating Systems* (Packer et al., arXiv:2310.08560, 2023).

The ancestor of tiered agent memory: the source [[agent-memory-provenance]] notes that virtual memory alone, without [[Provenance|provenance]], merely lets bad state scale elegantly. Related systems: [[AgentZeroMemory]], [[Zep]].
