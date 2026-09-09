---
title: "Transformer"
type: concept
tags: [llm, architecture, attention]
sources: [llm-context]
last_updated: 2026-09-09
---

# Transformer

The neural architecture underlying modern LLMs, featuring self-attention that lets each token relate to every other token in the context.

## Key Cost Implication (per [[llm-context]])
- Self-attention is O(n²) in sequence length
- This is the **physical reason** context windows must be bounded
- Beyond training length, inference quality can degrade even within the named window

## Components
- Token embedding + positional encoding
- Multi-head self-attention
- Feed-forward layers
- Residual connections + layer normalization

## See Also
- [[LLMContext]] — bounded by Transformer's n² cost
- [[Token]] — input unit
- [[Skill]] — progressive disclosure works *around* the n² cost