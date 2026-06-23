# ant-share

Public, scrubbed agent workflow patterns shared by Ant McCallum.

This repository contains shareable skill drafts and notes that preserve the useful operating patterns while removing private project context, client references, internal infrastructure paths, and deployment-specific assumptions.

The intent is community sharing and education. Use these skills as examples of how to build, customize, package, and share your own agent skills. They are starting points, not fixed products.

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

The Microsoft 365 Copilot Cowork package is published as a GitHub Release asset:

- Download `ant-share-m365-copilot-cowork.zip` from the `m365-copilot-latest` release.
- Upload that ZIP in Microsoft 365 Tenant Admin to sideload the skills into Copilot Cowork.

Run `node scripts/build-brain-viewer-index.mjs` to refresh the Brain Viewer helper index.

See `docs/publishing-rules.md` for the full publishing boundary and scrub checklist.

## Customize For Your Context

You should adapt these skills before using them in a real team. Replace the generic placeholders with your own:

- memory system or knowledge base;
- task tracker and project folders;
- approval rules;
- review cadence;
- preferred output formats;
- model-routing conventions;
- internal vocabulary and examples;
- team roles and ownership boundaries.

Keep the structure, but make the behavior yours. The highest-value skills usually encode how a specific person or team actually works.

## Build A Skill Catalogue

Skills become easier to adopt when people can see what exists, when to use each one, and how they connect. This repo includes `scripts/build-brain-viewer-index.mjs` to generate a simple `data/skills-index.json` file that can power an internal catalogue page.

A common pattern:

1. Store skills in a Git repo.
2. Add marketplace/plugin metadata so tools can install them.
3. Generate a skill index from `SKILL.md` frontmatter.
4. Publish an internal catalogue webpage with Vercel, Cloudflare Pages, GitHub Pages, or another static host.
5. Show each skill's trigger phrases, output contract, owner, maturity, and related skills.

The catalogue does not need to be complicated. A searchable webpage that answers "what skill should I use for this?" is often enough to make the library real for a team.

## Share Back

If you build from these examples, consider sharing a scrubbed version of your own pattern. Good shared skills usually include:

- a clear trigger description;
- an input contract;
- step-by-step processing rules;
- a predictable output contract;
- failure modes;
- attribution for borrowed ideas;
- a short note on what was customized for your context.

## Attribution

The spec writer skill is based on Nate B. Jones' public/prompt-kit concepts around Specification Precision, The Stupid Button, The Model Router, and communicating with AI agents. Leveragentic AI added the execution architecture around run specs, probes, proof requirements, source hierarchy, and closeout routines.

These files are not copies of a private client system. They are scrubbed, portable patterns intended for adaptation.
