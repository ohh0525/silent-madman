---
title: "Agent Identity"
type: concept
tags: [agent-identity, delegation, iam, oauth, security]
sources: [agent-identity]
last_updated: 2026-09-24
---

# Agent Identity (Delegated Authority)

The verifiable claim an agent makes about **who it is, on whose behalf it acts, and what it is permitted to do** — plus the mechanisms that keep that authority from *widening* as it propagates between agents.

## Mechanism (per [[agent-identity]])
1. **Workload identity** — the running software instance is issued an identity a relying party can verify. Not a copy of a human account.
2. **Token exchange (OAuth 2.0 Token Exchange, RFC 8693)** — the agent trades the user's token for a **short-lived, audience-restricted** token carrying a **dual subject**: the *actor* (which agent is acting) and the *subject* (which user is represented).
3. **Per-hop attenuation** — a child agent receives a **freshly issued, strictly narrower** credential: scope / magnitude / validity / delegation depth may only shrink. RFC 8693 *records* delegation; it does not *guarantee* attenuation.
4. **Dual-subject audit + propagated revocation** — each request retains both the executing workload and the represented user, wired to revocation propagation so one revocation reaches every agent still holding an old token.

## Boundary
- **vs. a name in the prompt** — self-description is not identity; identity must be *issued* and *independently verifiable*.
- **vs. API keys / shared service accounts** — static secrets express no delegation ("on whose behalf"), produce no per-action trace, and cannot be revoked per action. A shared human account adds a silent failure: when the human leaves, the agent's access dies with them.
- **Not one thing but four** — identity (*who is calling*) / delegation (*on whose behalf*) / authorization (*what is allowed*) / runtime policy (*permitted right now*). No one of them substitutes for another.
- **vs. [[Provenance]]** — provenance attaches origin / time / evidence to **facts**; identity attaches actor / subject to **actions**. Same traceability instinct, different object.
- **vs. [[Abstention]] · [[CitationLock]]** — those constrain what the agent may **say** (honesty); identity constrains what it may **do** (authority).
- **vs. sandboxing** — logical authority vs. physical isolation; a fully legitimate agent can still run somewhere that can write through the host kernel.
- **vs. a permission list** — the list is an *input*; the mechanism is how it is issued, attenuated, revoked and independently verified.

## Why It Matters
- It is the axis [[Agent]] never had. Agent was defined as "bounded by permissions, token budget, stopping condition" — but *who grants that permission and how far it travels* was left unspecified. This page supplies it.
- Without per-hop attenuation, the effective authority at the end of a delegation chain is **unknowable** — a few hops deep, nobody can state what the chain may do.
- It is what makes [[HumanInTheLoop]] *enforceable* rather than aspirational: authority can be attenuated to zero (e.g. `pay_limit=0`), which forces the irreversible step back to a person.
- Its concrete protocol instance is [[MCP]]'s authorization profile — see that page.

## See Also
- [[agent-identity]] — source
- [[Agent]] — the entity being identified
- [[HumanInTheLoop]] · [[ToolHallucination]] — the other two actor-side pages
- [[MCP]] — the concrete authorization profile
- [[Provenance]] · [[Abstention]] · [[CitationLock]] — the entity-side cluster this pairs with
