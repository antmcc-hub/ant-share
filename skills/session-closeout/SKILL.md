---
name: public-session-closeout
metadata:
  version: "1.0.0"
  author: "Leveragentic AI"
  attribution: "Scrubbed public version of a Leveragentic AI session closeout pattern. Influenced by Nate B. Jones' agent maintenance and skill-readiness ideas."
description: "Explicit-trigger session closeout. Gathers outcomes, classifies items GREEN/AMBER/RED, writes an audit, optionally deposits durable memory if OB1/Brain is connected, or asks to write a markdown closeout file via AskUserQuestion."
---

# Public Session Closeout

This skill closes a work session without relying on memory or vibes. It gathers what happened, classifies what is safe to write, asks only for uncertain decisions, and leaves a durable audit trail.

**Explicit trigger only.** Never run automatically.

## Core Model

Use a gather-then-judge workflow:

1. Gather session evidence silently.
2. Classify every candidate item as GREEN, AMBER, or RED.
3. Ask the user only about AMBER items.
4. Execute approved writes.
5. Produce a final closeout summary.

Classification:

- **GREEN**: traceable to session evidence and safe to write.
- **AMBER**: plausible but uncertain, mutates shared state, changes standing instructions, or needs user judgement.
- **RED**: out of scope, stale, duplicate, not evidenced, or unsafe to write.

## Pre-Flight Summary

Start with:

```text
Session Summary
---------------
Projects touched: [list]
Skills/workflows used: [list]
Files created or edited: [count/list]
External sends: [count/list]
Open decisions: [count/list]
Memory backend: [OB1/Brain connected? yes/no/unknown]
```

If the session is trivial, report:

> Clean session - nothing to close out. Safe to archive.

## Memory Destination Gate

Before any durable memory write, determine the destination.

1. If an OB1/Brain-style memory backend is connected and authorized:
   - Ask whether the user wants memory deposits this run.
   - Use `AskUserQuestion` if the answer is not already explicit.
   - If yes, write GREEN deposits with a pending/reviewable status where supported.
   - If no, skip memory deposits and use the markdown fallback if requested.

2. If no OB1/Brain-style backend is connected:
   - Use `AskUserQuestion` to ask whether to write a markdown closeout file.
   - Default destination: `Project/Agents/Claude Share/session-closeouts/`.
   - If that path does not exist, ask for the correct shared project folder or write the file in the current project under `session-closeouts/`.

Suggested `AskUserQuestion` prompt:

```text
No OB1/Brain memory backend is available. Should I write this closeout as a markdown file in Project/Agents/Claude Share/session-closeouts/?
```

Options:

- `Yes - write markdown closeout`
- `No - summary only`
- `Use a different path`

## Gather Phases

Run all gather phases before presenting a review.

### G1: Work Summary

Capture:

- tasks completed
- tasks started but not completed
- decisions made
- files created or changed
- commands/tests/checks run
- external sends or publishes

Only include items directly actioned in this session.

### G2: Durable Artifacts

Identify durable artifacts worth preserving:

- specs
- implementation notes
- decisions
- reports
- runbooks
- reusable prompts
- code changes with operational significance

For each artifact, capture:

```text
artifact: [name/path]
why_it_matters: [one sentence]
source_evidence: [file path, message, command output, or explicit user instruction]
recommended_destination: [memory backend / markdown closeout / skip]
```

### G3: Skill Or Workflow Retrospective

For every skill, agent, or workflow used:

```text
name: [skill/workflow/agent]
worked: [specific behavior that helped]
iteration: [specific correction requested, or None]
improvement: [concrete change, or No change needed]
```

Do not write vague retrospectives.

### G4: Pattern Capture

Look for repeatable operational lessons:

- retry loops
- failure modes
- commands that worked after failed alternatives
- useful prompts
- new guardrails
- missing tools

First occurrence: capture as a candidate, not a standing rule.

Second confirmed occurrence: surface as AMBER before adding to standing instructions.

### G5: Resolution Capture

When a problem was solved, capture:

```text
problem_addressed: [user-language description]
root_cause: [known or unknown]
resolution: [what changed]
verification: [how it was checked]
residual_risk: [remaining concern or None]
search_aliases: [phrases future agents might search]
```

### G6: Tool Failure Audit

Capture tool failures by operational meaning:

```text
operation: [search/read/write/test/deploy/github/memory/other]
failure_pattern: [what happened]
classification: [expected_miss / blocked / real_error / unclear]
recovery: [how it recovered]
recommended_change: [specific wrapper, rule, or documentation change]
```

Do not treat every non-zero exit or empty search result as a real failure.

## Judge Phase

After gathering, classify every item.

### GREEN

Auto-proceed if:

- evidence is traceable to this session
- the write is low-risk
- the item does not change external state beyond the selected closeout destination
- the item is not a duplicate

### AMBER

Ask the user if:

- evidence is incomplete
- the item changes standing instructions
- the item writes to shared memory without explicit permission
- the item publishes, sends, deletes, or changes access
- the item marks a high-stakes issue fully solved without verification
- the memory destination is unclear

### RED

Drop if:

- it is from a prior session and not touched here
- it is not evidenced
- it duplicates an existing durable note
- the file or artifact cannot be found
- it exposes private or sensitive information

## Consolidated Review

If there are no AMBER items, do not ask for approval. Execute GREEN writes, log RED drops, and report:

> Clean closeout: all items GREEN or RED-dropped. Safe to archive.

If AMBER items exist, present only the uncertain items:

```markdown
# Session Closeout Review - [Date]

## Auto-Proceed
[Counts by phase]

## Needs Review
[AMBER items with reason and proposed action]

## Dropped
[RED items with one-line reason]

## Decision
Accept AMBER / Edit [section] / Decline AMBER
```

## Execution Pass

On approval, execute writes in this order:

1. Write or update task/status notes if the current project has a task file.
2. Write the markdown closeout file if selected.
3. Write memory deposits only if OB1/Brain is connected and the user opted in.
4. Write skill/workflow retrospective notes.
5. Write pattern candidates or approved standing-pattern updates.
6. Write the action audit.
7. Report final status.

## Markdown Closeout Format

If using the markdown fallback, write:

```markdown
# Session Closeout - [YYYY-MM-DD HH:mm]

## Summary

## Completed

## Decisions

## Files And Artifacts

## Open Threads

## Memory Deposits
[Skipped / Written to OB1 or Brain / Not available]

## Skill And Workflow Notes

## Patterns And Failures

## Dropped Items

## Carry Forward

## Safe To Archive
[Yes/No and why]
```

## Musts

- Run only on explicit closeout/archive/wrap-up request.
- Gather before judging.
- Classify every write candidate GREEN/AMBER/RED.
- Ask only for AMBER items.
- Use `AskUserQuestion` when the memory destination is unclear.
- Make OB1/Brain deposits optional, never assumed.
- Use markdown fallback when no memory backend is connected or the user declines memory deposits.
- Never silently omit RED items; list the reason.
- Never publish, send, delete, or change access without explicit approval.

## Must-Nots

- Do not run automatically.
- Do not infer completed tasks from old context.
- Do not write private project details into public artifacts.
- Do not write to memory if OB1/Brain is unavailable or not authorized.
- Do not treat the markdown fallback as lower quality; it is the durable record when memory is absent.

## Final Confirmation

```text
Session Closeout Complete
-------------------------
Tasks/status: [updated/skipped]
Markdown closeout: [path/skipped]
Memory deposits: [written/skipped/not available]
Retrospectives: [count]
Patterns: [count]
Dropped: [count]
Approval gate: [skipped/presented]

Session closed out. Safe to archive.
```

## Metadata

side_effects: "optional memory writes, optional markdown file write, optional task/status note write"
trust_tier: "mutating"
requires_approval: "amber_items_only"
tool_dependencies: "AskUserQuestion plus available file and memory tools"
context_cost: "medium"

## Verification

- TRIGGER_POSITIVE: "close out this session" / "archive this chat" / "wrap up session"
- TRIGGER_NEGATIVE: "summarize this chat" should produce a summary only, not durable writes.
- OUTPUT_CHECK: Closeout includes GREEN/AMBER/RED classification, optional OB1/Brain deposit decision, markdown fallback path decision, dropped-item reasons, and final safe-to-archive statement.

