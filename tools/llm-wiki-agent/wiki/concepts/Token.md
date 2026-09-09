---
title: "Token"
type: concept
tags: [llm, tokenization, bpe]
sources: [llm-context]
last_updated: 2026-09-09
---

# Token

The fundamental unit by which LLMs count, price, and truncate text — produced by BPE (Byte Pair Encoding) sub-word tokenization.

## Key Facts (per [[llm-context]])
- English: ~1 token / word on average
- Chinese: ~1.5–2 tokens / character (smaller unit = more tokens)
- Same text can yield different token counts across tokenizers — always measure with the target model's tokenizer

## Why It Matters
- Context window capacity is measured in tokens, not characters
- Pricing is per-token (input + output)
- Cross-lingual handling relies on consistent tokenization
- "Out of vocabulary" words are handled by BPE — no `<UNK>` failures

## See Also
- [[LLMContext]] — context window = token budget
- [[Transformer]] — operates on token sequences
- [[Skill]] — progressive disclosure optimizes per-token spend