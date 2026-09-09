---
title: "LLM Context"
type: concept
tags: [llm, context-window, transformer]
sources: [llm-context]
last_updated: 2026-09-09
---

# LLM Context

The maximum number of tokens the model can simultaneously read and reference in a single inference pass.

## Definition
Per [[llm-context]] source: Sizing unit is **token** (BPE sub-word), not character.
- English: ~1 token / word
- Chinese: ~1.5–2 tokens / character

The window includes: system prompt + history + retrieved docs + reserved output, and must satisfy `total ≤ N tokens`.

## Core Mechanism
1. **BPE tokenization** — uniform processing across languages and out-of-vocab words
2. **Positional encoding + self-attention** — O(n²) cost scaling (1000 → 1M relations, 10000 → 100M)
3. **Truncation policy** — most APIs silently truncate oldest content rather than raising
4. **Attention bias** — strong at start (system) + end (current); middle weakened ("Lost in the Middle")

## Boundary
- **Not = training knowledge** — parameters (long-term) ≠ context (this session)
- **Not = bigger is better** — cost and latency scale with size; needs business-case ROI
- **Not = character count** — use the target model's tokenizer

## Practical Use
| Use Large Window | Use RAG / Summary |
|---|---|
| Full-document cross-section QA | Sparse info, only fragments needed |
| Long-chain Agent (multi-step state) | High-frequency, low-latency, low-cost |
| Truncation-sensitive review | Acceptable chunk + merge for summarization |

## See Also
- [[ContextWindow]] — English-name redirect
- [[Token]] — fundamental unit
- [[Agent]] — bounded by context budget
- [[Skill]] — progressive disclosure extends effective "memory"
- [[Transformer]] — architecture whose n² cost sets the bound