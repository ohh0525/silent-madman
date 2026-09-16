---
title: "LongMemEval"
type: entity
tags: [benchmark, memory, evaluation]
sources: [agent-memory-provenance]
last_updated: 2026-09-16
---

# LongMemEval

A benchmark for long-term interactive memory of chat assistants (Di Wu et al., ICLR 2025, arXiv:2410.10813). 500 curated questions over scalable chat histories (115K–1.5M tokens) testing five abilities: information extraction, multi-session reasoning, temporal reasoning, knowledge updates, and **[[Abstention]]**.

Key findings cited by [[agent-memory-provenance]]: long-context LLMs drop 30–60% accuracy when reading full histories instead of oracle evidence; commercial systems (e.g. GPT-4o) reach only 30–70%. Proposes an index → retrieve → read framework. Used as the primary evidence that naive long context is insufficient and that [[LongTermMemory]] needs structure + discipline.
