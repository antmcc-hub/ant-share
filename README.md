# ant-share

Public, scrubbed agent workflow patterns shared by Ant McCallum.

This repository contains shareable skill drafts and notes that preserve the useful operating patterns while removing private project context, client references, internal infrastructure paths, and deployment-specific assumptions.

## Contents

- `slack/spec-writer-provenance-response.md` - Slack-ready provenance breakdown for the spec-writer/session-planning pattern.
- `skills/spec-writer/SKILL.md` - Spec writer skill with attribution to Nate B. Jones prompt-kit concepts and Leveragentic AI additions.
- `skills/session-closeout/SKILL.md` - Session closeout skill with optional OB1/Brain deposit support and markdown fallback via `AskUserQuestion`.
- `skills/weekly-retro/SKILL.md` - Weekly retro skill for reviewing closeout trails, preferences, agent handoffs, and improvement candidates.
- `scripts/build-brain-viewer-index.mjs` - Helper that builds `data/skills-index.json` for Brain Viewer-style skill maps.
- `docs/publishing-rules.md` - Rules for when a skill belongs in private `lev-plugins` vs public `ant-share`.

## Packaging Status

This repo includes the core triple packaging scaffolding:

- `.agents/plugins/marketplace.json` for marketplace discovery.
- `.claude-plugin/plugin.json` for Claude-style plugin metadata.
- `.codex-plugin/plugin.json` for Codex-style plugin metadata.
- `.app.json` and `.mcp.json` placeholders for app/MCP expansion.

Run `node scripts/build-brain-viewer-index.mjs` to refresh the Brain Viewer helper index.

See `docs/publishing-rules.md` for the full publishing boundary and scrub checklist.

## Attribution

The spec writer skill is based on Nate B. Jones' public/prompt-kit concepts around Specification Precision, The Stupid Button, The Model Router, and communicating with AI agents. Leveragentic AI added the execution architecture around run specs, probes, proof requirements, source hierarchy, and closeout routines.

These files are not copies of a private client system. They are scrubbed, portable patterns intended for adaptation.
