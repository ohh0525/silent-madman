---
title: "Agent Sandbox"
type: concept
tags: [agent-sandbox, execution-isolation, kubernetes, gvisor, kata, containment]
sources: [agent-sandbox]
last_updated: 2026-09-26
---

# Agent Sandbox (执行隔离)

A hard boundary around the agent's execution that **the agent itself cannot alter**: kernel-level isolation (gVisor / Kata / per-sandbox VM — not an ordinary container sharing the host kernel) plus declarative allow-lists (egress / filesystem / tool reach, declared with the environment). It does not ask *should this happen* — it guarantees *even if everything else fails, the blast radius is this large*.

## Mechanism (per [[agent-sandbox]])
- **Isolation below the kernel, not in the app layer** — the K8s upstream primitive delegates isolation to the pod spec's `RuntimeClass` (gVisor by default — syscall interception, no shared host kernel; Kata when a full guest kernel is needed; Alibaba uses a per-sandbox VM). Ordinary containers share the host kernel and **do not count**. *The HF intrusion case is exactly an app-layer allow-list being routed around.*
- **Boundaries declared with the environment** — egress policy (exact-hostname allow-lists), filesystem and injection policies live in the `SandboxTemplate`, published and audited together with the environment ("change the template, not the architecture"). OpenAI's hosted sandbox has the same shape: egress three-state, `restricted` = 1–100 **exact** hostnames, **no wildcards**.
- **Lifecycle is half the product** — `SandboxWarmPool` keeps N pre-warmed sandboxes (GKE: 300/sec/cluster, p90 200ms, 10–15× faster than cold start); idle agents suspend via pod snapshot with second-level resume; `SandboxClaim` allocates without touching template details. *Agent load is bursty + long-lived; without warm pools and suspend/resume the cost curve cannot support millions of agents.*
- **It must exist independently of the permission system** — identity chains can narrow per hop and gates can stop irreversible actions, yet a **fully legitimate, fully approved** action can still run where it can write through the host kernel. Hence: **authority is not isolation**; the sandbox is an infrastructure property, not a permission field.

## Boundary
- **Not [[AgentIdentity]]** — logical authorisation vs physical containment; neither substitutes for the other.
- **Not [[HumanInTheLoop]]** — different dimensions, not a pipeline order: the gate asks *may it act, now* (before); the sandbox bounds *what the action can touch* (during).
- **Not [[ToolHallucination]]** — whether the called tool exists vs what its execution can reach.
- **Not [[AgentHarness]]** — who orchestrates vs where it runs and what it can touch. OpenAI splits them as separate `Agent` / `Environment` objects; choose them separately.
- **Not "an ordinary container"** — containers share the host kernel; that is precisely why `RuntimeClass` (gVisor/Kata) exists and why the K8s primitive is a distinct CRD on top of pods.

## Why It Matters
- **It completes the action-side chain.** `propose → resolve → authorize → gate → **execute**` — this page is the named `execute` leg that [[overview]] had listed as the missing third leg since 2026-09-24.
- **As of 2026-09 it is standardised infrastructure.** One week saw five vendors converge: `kubernetes-sigs/agent-sandbox` into **SIG Apps** (upstream), **Google AX** open-sourced (Apache 2.0), **Alibaba Cloud Agent Sandbox** commercialised (100k instances/min, per-sandbox VM, E2B/K8s-API compatible), plus Docker Cloud Sandboxes and Nvidia OpenShell. When infrastructure absorbs a thing, it stops being optional.
- **The strongest evidence it is necessary is a failure anatomy, not a product launch.** Hugging Face's 2026-07 intrusion post-mortem: the agent's SSRF was **correctly rejected** by an app-layer allow-list — then it **switched paths** (dataset-config file read → HDF5 external storage → pod secrets, plus Jinja2 template injection; entry via a zero-day in an *allowed* egress destination). Lesson: **a single layer of defence that denies one path does not close the surface.**
- **Honest limits:** the upstream primitive is orchestration, not operations (node images, RuntimeClass, warm-pool capacity, FQDN allow-lists, GPU scheduling remain yours); it targets long-running stateful singletons, not fire-and-forget. Vendor capacity numbers (AX "billions per cluster", Alibaba, GKE 16×) are direction-grade, not verified capacity facts.

## See Also
- [[agent-sandbox]] — source
- [[AgentIdentity]] · [[HumanInTheLoop]] · [[ToolHallucination]] — the decision mechanisms this page bounds the residual risk of
- [[AgentHarness]] — the orchestration layer that plugs into a sandbox as its execution environment
- [[Agent]] — whose action-side chain this page completes at `execute`
- [[OpenAI]] — hosted-sandbox defaults as the cautionary default-values case
