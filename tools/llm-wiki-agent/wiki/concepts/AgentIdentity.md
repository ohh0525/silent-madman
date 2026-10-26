---
title: "Agent Identity"
type: concept
tags: [agent-identity, delegation, iam, oauth, security, composition-audit]
sources: [agent-identity]
last_updated: 2026-10-25
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

## Per-hop narrowing is not narrowing over the batch *(ledger row 10-25A; applied 2026-10-25)*

> **Draft annotation, pending ingest.** Not yet backed by a source page in this wiki — verified against live sources on 2026-10-25 (recorded in `.workbuddy/memory/concept-radar/2026-10-25.md`, candidate 1; ledger row **10-25A**). Remove this banner when the material is ingested and human-reviewed, and move the source slug into the frontmatter `sources` field.

**The boundary step 3 above does not state.** *Per-hop attenuation* says: scope / magnitude / validity / delegation depth may only shrink. Read carefully — **every one of those four is a property of *one* credential**: this hop's scope, this hop's magnitude, this hop's lifetime, this hop's depth. The mechanism's verdict object is **one item**, and "each hop only narrows" is therefore a **per-item** guarantee.

**The Mosaic Effect** (`arXiv:2610.30418`, submitted ≈**2026-10-21**) is the case where **attenuation is fully satisfied and the outcome is still unauthorized**: each document is individually authorized, each access individually within scope, and the conclusion their **conjunction** supports is one that **no one authorized and no single hop contained**.

> ⇒ **Per-item pass is this mechanism's success criterion, not its boundary condition.** Attenuation has no notion of *the batch*: it can never be violated by a set of accesses that is dangerous only **taken together**.

- **Why this is a boundary and not a refutation.** Nothing above is wrong. Narrowing a credential per hop remains exactly as necessary as it was. What is missing is a **second question this page never asks**: not *"is this hop narrower?"* but **"is the set of hops I have now permitted, jointly, conclusive about something that was never authorized?"** — a question about the **joint** of the accesses, which no per-hop check can express.
- **Where the answer would have to live.** Not in the credential (that is what attenuation already governs) but in **the verdict that admits the set** ⇒ the missing cell is an **aggregate authorization**: a check over *what this principal may now be able to conclude*, evaluated at the level of the collection, not the request. No such cell exists anywhere in this wiki.
- **The shape to watch for.** The failure is invisible to per-hop audit **by construction** — every log line reads as compliant. Detection requires a verdict object that spans items, which is precisely what the four mechanisms above do not have.

**Boundaries (do not merge these).**
- **vs 10-16B protocol pivoting / [[MultiAgent]]** — that row asks *on whose authority the task content travels* (a failure **at the hand-off**, someone inherits more than they should); this row grants that **nobody over-stepped at any hand-off** and still fails ⇒ **scan line 11 vs scan line 19**, parallel rows that must name each other.
- **vs [[Abstention]]'s half of this row** — the same paper's other landing: here the mechanism is *authorization over accesses*; there it is *the refusal itself as a disclosure channel*. **Two instances of one variable, not two faces of one row.**
- **vs revocation propagation (step 4)** — revocation answers *"stop this credential"*; it has no notion of *"un-conclude what these credentials together now imply"*, and the mosaic conclusion is not stored anywhere to revoke.

⚠️ **Evidence grade:** preprint, no peer review, **30** synthetic scenarios, author-selected models, **no independent replication**. The claim carried here is the **shape** — *a per-item guarantee cannot bound a joint conclusion* — which holds independently of the paper's rates; **do not cite the 7.08% / 32.37% figures from this page** (their denominators differ; see [[Abstention]]).

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
