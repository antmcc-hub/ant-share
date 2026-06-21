---
name: public-spec-writer
metadata:
  version: "1.0.0"
  author: "Leveragentic AI"
  attribution: "Based on Nate B. Jones specification precision, Goal Prompt Generator, PromptKit #161, and PromptKit #247 concepts; extended by Leveragentic AI."
description: "Turns vague requests into executable specs or lightweight run specs. Use for: spec this out, brief this up, write a run spec, goal prompt generator, delegate this to an agent. Not for executing the task directly."
---

# Public Spec Writer

Turn vague instructions into executable specifications that an AI agent, human executor, or reviewer can act on without guessing.

## Attribution

Base concepts are attributed to Nate B. Jones:

- Specification Precision and Goal Prompt Generator patterns.
- PromptKit #161: The Stupid Button and The Model Router.
- PromptKit #247: Shape vs Execute, six-field briefs, and "flashlight" exclusions.

Leveragentic AI additions:

- Run Spec mode for bounded agent delegation.
- Day 0 probes for unknown external-state assumptions.
- Permission boundaries and required proof.
- Source hierarchy: primary, background, excluded.
- Review budget and escalation rules.
- Session architecture patterns for inline, parallel, sequential, and async execution.

## When To Use

Use this skill when a request needs to become executable before work starts:

- "Spec this out."
- "Brief this up."
- "Write a goal prompt."
- "Write a run spec."
- "Delegate this to an agent."
- "Make this task executable."

Do not use this skill when the user simply wants you to do a small, clear task now.

## Mode 1: Run Spec

Use Run Spec mode when the user needs a bounded assignment rather than a full implementation specification. Keep it short unless the work is high-risk.

```markdown
# Run Spec: [Task]

## Goal
[One sentence outcome.]

## Run Type
[Scout / Research / Build / Review / Verify / Repair]

## Source Of Truth
[Repo, doc, URL, note, ticket, pasted instruction, or explicit user direction.]

## Permission Boundary
[What the executor may change, inspect, create, or send. Include what is out of bounds.]

## Required Proof
[Files changed, tests run, screenshots, sources cited, exact command output, or review evidence.]

## Review Budget
[What the reviewer must inspect before accepting the work.]

## Escalation Rule
[When the executor must stop and ask.]

## Done Means
[Observable finish condition.]
```

## Mode 2: Full Spec

Use Full Spec mode when the work is high-risk, multi-step, multi-user, expensive, externally visible, or likely to be executed by someone other than the requester.

### Step 0: Shape vs Execute Gate

Ask internally: is the work decided, or is the user still shaping it?

| Signal | Mode | Action |
|---|---|---|
| Outcome, audience, and deliverable are clear | Execute | Write the spec. |
| User is weighing options or asking what to build | Shape | Do not write a full spec yet. Help shape the decision first. |
| User has a thesis but has not pressure-tested it | Shape | Map options, risks, and criteria before speccing. |

If the request is shape-mode work, say:

> This is shape-mode work, not execute-mode. A spec built now would lock in choices that are still open. I can help shape it first, then write the spec once the direction is decided.

### Step 1: Strategic Gate

Before speccing, answer:

1. What happens if this is not built?
2. Who asked for this, and why now?
3. Is there an existing solution we have not fully used?

Verdict:

- **Proceed**: clear impact, clear requestor, no adequate existing solution.
- **Challenge**: marginal impact, unclear owner, or speculative motivation.
- **Kill**: no meaningful impact and a better existing option is available.

### Step 2: Extract Intent

Answer:

1. What outcome is the user actually trying to achieve?
2. Who will use the output?
3. What would make the output rejected?
4. What does "good enough" look like?
5. What would make it surprisingly good?

Ask at most one or two clarifying questions. Infer the rest from provided context.

### Step 3: Three-Sentence Test

Before drafting the full spec, write:

```text
1. A successful output will [observable outcome].
2. It will include [specific elements] and exclude [specific exclusions].
3. An independent reviewer could verify quality by [checking method].
```

Use this as the anchor for the spec.

### Step 4: Progressive Depth Filter

Add sections only when needed:

| Question | If Yes, Add |
|---|---|
| Does this touch money, safety, compliance, or trust? | Risk and controls section |
| Does this have more than one caller or consumer? | Interface contract |
| Does this replace a manual process? | Current-state and migration plan |
| Will delivery take more than one week? | Milestones and checkpoints |
| Will someone else execute it? | Handoff checklist |

### Step 5: Specification Primitives

Every full spec should include:

- **Goal**: the outcome, not just the artifact.
- **Source of Truth**: primary sources, background sources, and excluded sources.
- **Acceptance Criteria**: each criterion must include a verification method.
- **Musts**: non-negotiable requirements.
- **Must-Nots**: exclusions tied to failure modes or edge-of-scope boundaries.
- **Preferences**: useful but non-essential improvements.
- **Day 0 Probes**: unknown premises that must be checked before execution.
- **Escalation Triggers**: conditions where work stops and asks.
- **Done Means**: observable finish condition.

Acceptance criteria format:

```markdown
- [ ] [Criterion] - VERIFY: [concrete test or inspection method with expected result]
```

Must-not format:

```markdown
- [Guardrail] <- PREVENTS: [named failure pattern or scope drift]
```

### Step 6: Model And Session Routing

Use model routing as a planning aid, not as a brand-specific dependency:

| Work Type | Suggested Tier |
|---|---|
| Formatting, extraction, simple cleanup | Low-cost model |
| Ordinary drafting, coding, synthesis | Standard strong model |
| Architecture, ambiguous strategy, high-risk reasoning | Strongest available model |

Session architecture options:

- **Inline**: one executor, one pass.
- **Parallel**: independent branches can run at the same time.
- **Sequential**: later work depends on earlier findings.
- **Async**: work should become a separate task/thread because it has its own proof loop.

## Output Contract

Return either a Run Spec or Full Spec. Do not mix formats unless the user asks.

For Full Spec, use:

```markdown
# Spec: [Name]

## Goal

## Source Of Truth
Primary:
Background:
Excluded:

## Acceptance Criteria

## Musts

## Must-Nots

## Preferences

## Day 0 Probes

## Escalation Triggers

## Session Architecture

## Done Means
```

## Failure Modes

- If the work is still shape-mode, do not write a full spec. Offer shaping help.
- If critical context is missing, ask one or two targeted questions.
- If the user wants execution, not specification, execute the task unless a spec is needed to prevent wasted work.
- If external facts are load-bearing and may have changed, mark them as Day 0 Probes.

## Verification

- TRIGGER_POSITIVE: "Write a run spec for an agent to audit this repo."
- TRIGGER_NEGATIVE: "Fix this typo." That should be executed directly, not routed to spec-writing.
- OUTPUT_CHECK: Output includes source of truth, permission boundary or acceptance criteria, verification method, escalation rule, and done condition.

