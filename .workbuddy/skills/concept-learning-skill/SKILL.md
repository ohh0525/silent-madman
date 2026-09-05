---
name: concept-explainer
description: This skill should be used when the user wants to deeply learn any new concept (a theory, term, technology, methodology, or framework). It generates structured learning materials that include personal explanation, core mechanism, application scenarios, boundary clarification, and source links. Trigger when the user says things like "explain this concept", "help me learn X", "what is X", "用通俗的话讲讲 X", "帮我深入理解 X", "X 是什么".
agent_created: true
---

# Concept Explainer

## Overview

This skill enables WorkBuddy to take any new concept as input and produce a structured, deep-learning material that helps the user truly understand it rather than just memorize a definition. The output combines a personal explanation (in the user's own words), the underlying mechanism (why it works), application scenarios (where to use it), boundary clarification (what it is not, common misconceptions), and verifiable source links.

## When to Use

Use this skill when the user wants to learn or deeply understand a concept, theory, term, technology, methodology, framework, or abbreviation. Typical triggers:

- "Explain X to me in plain language"
- "Help me understand X, including its mechanism and applications"
- "What is X? Give me a learning material"
- "用通俗易懂的方式给我讲讲 X"
- "我要深入理解 X，从原理到应用"
- "X 是什么 / X 怎么理解"
- Any request that takes a new term and asks for a structured deep dive

Do NOT use this skill for: simple dictionary-style one-line definitions, task execution (code, docs, spreadsheets), or factual Q&A about a specific known fact.

## Input Requirements

The skill accepts one mandatory input and several optional inputs.

**Mandatory:**

- `concept`: the concept name to learn. Could be a single word, phrase, or full term (e.g. "Mitosis", "Occam's Razor", "可转债", "Transformer architecture", "OKR").

**Optional (recommended to ask if the user did not specify):**

- `audience_level`: beginner / intermediate / expert. Default to intermediate when unknown.
- `context`: why the user is learning this (exam, work project, curiosity, technical decision). Affects which application scenarios to emphasize.
- `depth`: how deep to go on mechanism. Default = balanced personal-explanation + mechanism.
- `language`: output language. Default = the language the user used in the request.

If the concept is ambiguous (multiple meanings, e.g. "Python"), ask the user to disambiguate before generating.

## Generation Workflow

Follow these steps in order. Each step builds on the previous one; do not skip.

### Step 1: Concept Disambiguation

Before generating, verify the concept's intended meaning.

- If the concept has multiple common meanings (e.g., "Cell" could be biology / battery / prison / spreadsheet cell), surface the candidates and ask the user to pick one.
- If unambiguous, proceed and note the assumed scope at the top of the output (e.g. "Scope: biology (cell biology), not spreadsheet cell").

### Step 2: Source Gathering (Required, See Sources Section)

Gather material from at least the minimum required sources listed in the Sources Requirement section. For each source, capture:

- The URL
- The specific claim the source supports
- A 1-line snippet (quoted if direct)

If a minimum-source claim cannot be supported, explicitly mark it as "based on general knowledge, not directly cited" rather than fabricating a citation.

### Step 3: Internal Reasoning (Do This in Thinking)

Before writing, decide:

- The single best analogy for the personal explanation
- The minimum mechanism chain (cause → effect) needed for "why it works"
- 2–3 concrete application scenarios (mix classic + modern where possible)
- 1–2 boundary cases / common misconceptions

### Step 4: Write the Output

Follow the Output Structure section strictly. Each section has a purpose; do not rename or merge sections.

### Step 5: Self-Check (Required)

Run the Self-Check section before delivering. If any check fails, fix the output before presenting it to the user. See Self-Check Requirement section.

## Output Structure

Deliver the material as a single, well-organized Markdown document with these sections, in this order:

### 1. 一句话定义 / One-line definition

One sentence. Plain language. No jargon that the user has not seen. No deeper explanation here.

### 2. 个人解释 / Personal explanation

A 200–400 word explanation written as if the user were explaining the concept to a curious friend. Use:

- A concrete, real-world analogy drawn from the audience's likely context
- Plain language; define any technical terms inline when first used
- A flowing narrative, not bullet points
- One short hypothetical scenario showing the concept in action

The goal: after reading this, the user can paraphrase the concept correctly to someone else.

### 3. 核心机制 / Core mechanism

Explain why the concept works, not just what it is. Structure as:

- The mechanism in 2–4 numbered steps (cause → effect chain)
- For each step, one sentence on what happens + one sentence on why this matters
- A small diagram, equation, or pseudocode block if it materially helps (optional but encouraged for technical concepts)

Stop at depth where the user can answer "what would happen if X changed" about the concept.

### 4. 应用场景 / Application scenarios

Provide exactly 3 scenarios. For each:

- **场景 / Scenario name**
- **背景 / Context**: one sentence on the situation
- **如何应用 / How it applies**: 1–3 sentences on how the concept is used
- **结果 / Outcome**: one sentence on what the application achieves

Mix of classic canonical examples and at least one modern or unusual example. Skip generic filler like "widely used in industry" — every scenario must be specific.

### 5. 边界辨析 / Boundary clarification

Cover, in this order:

- **不是什么 / What it is NOT**: 2–4 bullets clearly contrasting with similar-but-different concepts
- **常见误解 / Common misconceptions**: 2–3 bullets about how people typically misunderstand it
- **适用与不适用 / When it applies vs. doesn't**: one short table or 2 bullets contrasting appropriate and inappropriate use

This is where the user avoids future confusion. Do not skip this section.

### 6. 来源链接 / Source links

All sources used, one per line, as numbered references:

```
[1] <Title> — <URL> — <specific claim supported>
[2] <Title> — <URL> — <specific claim supported>
```

Mark any claim that came from general knowledge without direct citation with `[unverified]` after the bullet. Do not fabricate URLs.

### 7. 一句话回顾 / One-line takeaway

A single sentence the user can save as their personal takeaway. Should compress the core idea, not repeat the one-line definition.

## Output Format

- Default to Markdown
- Use the user's input language for all content
- Length target: 800–1500 words; longer is fine for highly technical concepts, but never pad
- Save to `<workspace>/concept-learning/<concept-name>.md` so the user can re-access it later; also present the content inline in the response

## Sources Requirement

The minimum source requirement depends on audience level. Apply the strictest applicable rule:

- **General knowledge concepts** (history, philosophy, social science): minimum **3 sources** from authoritative encyclopedic / academic / official references. Examples: Wikipedia, Stanford Encyclopedia of Philosophy, official institutional pages, peer-reviewed papers.
- **Technical / engineering concepts** (software, hardware, finance products, scientific methods): minimum **2 official primary sources** (official docs, RFC, paper, regulatory filing) + **1 reputable secondary** (well-known authoritative tutorial, textbook, or established practitioner blog).
- **Legal / regulatory / medical concepts**: minimum **2 primary sources** (the law / regulation text, official body) + **1 secondary expert source**. Always prefer the primary text over commentary.

Additional rules:

- Prefer primary sources over aggregator pages when both exist.
- Do NOT cite SEO-spam content farms, AI-generated blogs of unknown authorship, or pages with no author / date.
- If WebSearch returns no qualifying source, explicitly state "未找到符合最低来源要求的资料，以下主要基于通用知识整理" before the Source links section and tag the unverified claims with `[unverified]`.
- For concepts invented after the model's training cutoff, the search is mandatory; do not rely on training data.

## Self-Check Requirement

Before delivering the material, run this checklist. Fix any failure before sending.

1. **Disambiguation done**: If the concept is multi-meaning, the intended scope was either confirmed by the user or explicitly assumed and stated.
2. **All 7 output sections present and in the correct order**: one-line definition, personal explanation, core mechanism, application scenarios, boundary clarification, source links, one-line takeaway.
3. **Personal explanation is plain language**: no paragraph relies on jargon the user has not seen. Technical terms are defined inline.
4. **Core mechanism is causal, not descriptive**: every step answers "why", not just "what".
5. **Application scenarios are specific**: 3 scenarios, each with a real named context, not generic placeholders.
6. **Boundary clarification distinguishes from neighbors**: at least 2 "what it is NOT" bullets that contrast with a different-but-similar concept.
7. **Source minimums met**: counting the link list, the minimum source rule for the domain is satisfied. Any unverified claim is tagged `[unverified]`.
8. **No fabricated URLs**: every URL in Source links is actually clickable and points to a real page the search returned.
9. **Length in target band**: 800–1500 words unless the concept genuinely needs more.
10. **One sentence each for one-line definition and one-line takeaway**: confirmed they are both single sentences, not paragraphs.

If any check fails, fix and re-verify before presenting.

## Resources

This skill does not require bundled scripts, references, or assets. All generation is reasoning over user input plus web search results.

If a user later asks to package a concept as a slide deck or PDF, recommend bundling a per-session generation transcript to a future `concept-explainer-deck` skill.
