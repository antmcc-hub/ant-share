---
name: weekly-retro
metadata:
  version: "1.0.0"
  author: "Leveragentic AI"
  attribution: "Scrubbed public version of a Leveragentic AI weekly operating retro pattern. Influenced by Nate B. Jones' agent maintenance and skill-readiness ideas."
description: "Weekly retro for overlapping agent sessions. Reviews session closeouts, specs, proof trails, preferences, failures, and improvement candidates. Use for: weekly retro, weekly review, review this week's agent work, improve the skill system."
---

# Weekly Retro

Turn a week of agent work into a practical improvement loop. This skill reviews closeout trails, run specs, handoffs, user preferences, proof quality, and repeated failure patterns, then produces a short weekly retro with concrete changes.

## Attribution

Built by Leveragentic AI as a scrubbed operating pattern for teams using multiple agents or long-running AI workflows. It is influenced by Nate B. Jones' writing on agent maintenance, skill readiness, and preserving useful AI work beyond individual sessions.

## Why It Exists

Weekly retros are where isolated session learnings become system improvements. Without a weekly review, closeout notes pile up, user preferences get ignored, and the same mistakes repeat across agents.

Use this skill with:

- `spec-writer` to check whether specs produced executable work and usable proof;
- `session-closeout` to review completed sessions, dropped items, deposit preferences, and unresolved threads;
- any task tracker, memory backend, or markdown closeout folder that stores durable session trails.

Benefits:

- finds repeated agent failure modes before they become norms;
- promotes useful one-off patterns into reusable instructions;
- catches stale tasks and unresolved handoffs;
- reviews whether memory/deposit preferences are being respected;
- creates a concise improvement queue for the next week.

## Inputs

Use whatever is available:

- session closeout markdown files;
- OB1/Brain or other memory entries;
- task tracker updates;
- run specs or implementation specs;
- pull requests, commits, or deployment notes;
- user corrections and feedback;
- prior weekly retro output.

If inputs are missing, degrade gracefully. Ask one targeted question only when the missing input changes the recommendation.

## Review Window

Default to the last 7 days. Anchor dates from the system clock, not conversation memory.

```text
today: [YYYY-MM-DD]
lookback_start: today - 7 days
lookback_end: today
```

## Process

### Step 1: Build The Session Inventory

List sessions or work blocks reviewed:

```text
session: [name/date/thread/file]
source: [closeout file / memory entry / task tracker / user-provided]
status: complete | partial | blocked | unclear
spec_used: yes | no | unknown
closeout_used: yes | no | unknown
```

### Step 2: Review Spec-To-Proof Trails

For each session with a spec or run spec:

```text
goal: [what was supposed to happen]
required_proof: [what the spec requested]
actual_proof: [what closeout or artifacts show]
proof_gap: none | minor | material | unknown
decision: accept | verify | follow up | rewrite spec pattern
```

### Step 3: Review Closeout Quality

For each closeout:

```text
green_items: [count]
amber_items: [count]
red_items: [count]
dropped_reason_quality: clear | vague | missing
carry_forward_quality: actionable | vague | missing
memory_preference_respected: yes | no | unknown | not applicable
```

### Step 4: Identify Repeated Patterns

Group repeated issues:

- unclear source of truth;
- missing proof;
- too much user asking;
- not enough user asking;
- duplicated memory deposits;
- stale tasks resurfacing;
- tool retry loops;
- handoffs without permission boundaries;
- specs written while the work was still shape-mode.

Promote only repeated or high-impact patterns. Single occurrences stay as candidates.

### Step 5: Preference Review

Check whether the user gave feedback about workflow behavior:

```text
preference: [deposit behavior / asking style / proof depth / output format / model routing / other]
current_setting: [known setting or unknown]
observed_behavior: [what happened this week]
recommendation: keep | update | ask user | remove stale preference
```

If the user clearly changed a preference, surface it as AMBER before writing to shared memory or a preference file.

### Step 6: Improvement Queue

Create a small queue. Prefer fewer, sharper changes.

```text
improvement: [specific change]
target: [skill / prompt / checklist / task tracker / memory preference]
why_now: [evidence from the week]
owner: [person/agent/team]
effort: small | medium | large
priority: P1 | P2 | P3
```

## Output Contract

Produce:

```markdown
# Weekly Retro - [YYYY-MM-DD]

## Reviewed
[Sessions, files, memory sources, specs, and closeouts included.]

## What Worked
[Specific behaviors to keep.]

## Proof And Handoff Gaps
[Where specs, closeouts, or artifacts did not line up.]

## User Preferences
[Captured, changed, or unresolved preferences.]

## Repeated Patterns
[Pattern candidates and promoted patterns.]

## Improvement Queue
[P1/P2/P3 actions.]

## Recommended Updates
[Skill edits, docs, task tracker cleanup, memory preference changes.]

## Carry Forward
[What next week should start with.]
```

## Write Behavior

Default to a report-only retro. Mutating writes require explicit approval:

- updating a preference file;
- writing to OB1/Brain or another memory backend;
- changing skill instructions;
- closing or editing tasks;
- publishing a report.

If no memory backend is connected, offer a markdown output path:

`Project/Agents/Claude Share/weekly-retros/weekly-retro-[YYYY-MM-DD].md`

Use `AskUserQuestion` if the destination is unclear.

## Failure Modes

- If closeout files are absent, review available task/spec artifacts and note the gap.
- If specs are absent, review whether work still had clear proof and done conditions.
- If evidence is stale, put it in Carry Forward as "verify before acting".
- If a recommendation changes standing behavior, classify it as AMBER.
- If the user asks for planning rather than retro, produce a retro first, then a short next-week plan.

## Verification

- TRIGGER_POSITIVE: "Run the weekly retro on this week's agent work."
- TRIGGER_NEGATIVE: "Plan my week." That is planning; ask whether to run retro first if closeout trails exist.
- OUTPUT_CHECK: Output includes reviewed sources, proof gaps, preference review, repeated patterns, improvement queue, and carry-forward items.

