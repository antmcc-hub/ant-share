# ant-share

Public, scrubbed agent workflow patterns shared by Ant McCallum.

This repository contains public-facing skill drafts and notes that preserve the useful operating patterns while removing private project context, client references, internal infrastructure paths, and deployment-specific assumptions.

## Contents

- `slack/spec-writer-provenance-response.md` - Slack-ready provenance breakdown for the spec-writer/session-planning pattern.
- `skills/spec-writer/SKILL.md` - Public spec writer skill with attribution to Nate B. Jones prompt-kit concepts and Leveragentic AI additions.
- `skills/session-closeout/SKILL.md` - Public session closeout skill with optional OB1/Brain deposit support and markdown fallback via `AskUserQuestion`.

## Attribution

The spec writer skill is based on Nate B. Jones' public/prompt-kit concepts around Specification Precision, The Stupid Button, The Model Router, and communicating with AI agents. Leveragentic AI added the execution architecture around run specs, probes, proof requirements, source hierarchy, and closeout routines.

These files are not copies of a private client system. They are scrubbed, portable patterns intended for adaptation.

