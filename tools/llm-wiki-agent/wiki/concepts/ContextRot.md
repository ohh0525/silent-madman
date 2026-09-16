---
title: "Context Rot"
type: concept
tags: [context-engineering, degradation, anthropic]
sources: [context-engineering]
last_updated: 2026-09-16
---

# Context Rot

The phenomenon in which a model's ability to accurately retrieve information from its context *continuously declines* as the number of tokens in the window rises. Named by Anthropic.

## Mechanism (per [[context-engineering]])
- Informally called "context rot" in Anthropic's engineering writing.
- It is a *slope*, not a cliff: the model does not "crash" — it grows progressively more likely to misread long inputs.
- Root cause is the same architectural fact as [[LLMContext]]: attention is a finite budget spread across n² token-pair relationships.

## Why It Matters
- Explains why "open the window to 1M tokens and it fits everything" is a false solution — fitting ≠ using.
- Justifies [[ContextEngineering]] as active *curation* rather than passive accumulation.
- Corroborated downstream by [[LongMemEval]]: long-context models lose 30–60% accuracy when forced to read full 115K-token histories.

## See Also
- [[context-engineering]] — primary source
- [[ContextEngineering]] — the response to it
- [[LLMContext]] — capacity ceiling vs. effective capacity
- [[Transformer]] — n² attention cost as the root
