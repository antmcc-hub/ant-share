# Publishing Rules: lev-plugins vs ant-share

This document keeps skill packaging consistent across the private Leveragentic skill library and this public share repo.

## Decision Rule

Publish to `antmcc-hub/lev-plugins` when the skill is:

- private operating infrastructure;
- client-specific or commercially sensitive;
- dependent on private tools, Brain schemas, internal folders, secrets, dashboards, scheduled tasks, or deployment paths;
- part of an internal delivery chain where downstream skills expect private metadata;
- not yet scrubbed for public reuse.

Publish to `antmcc-hub/ant-share` when the skill is:

- safe to share publicly;
- useful as a generic agent workflow pattern;
- free of client names, private infrastructure, secrets, proprietary paths, internal project state, and private repo references;
- attributed clearly when based on third-party ideas;
- portable across teams without requiring Leveragentic's private stack.

If a skill belongs in both, keep the private source in `lev-plugins` and create a scrubbed derivative in `ant-share`. Do not publish the private source directly.

## Scrubbing Rules For ant-share

Before publishing to `ant-share`, remove or generalize:

- client names and project-specific examples;
- private repo names except the destination repo itself;
- local filesystem paths;
- account IDs, project IDs, API URLs, tokens, secret names, phone numbers, and cloud resource IDs;
- private Brain table names or schema assumptions unless framed generically;
- scheduled-task details that expose private operations;
- internal team/vendor names unless explicitly intended for public attribution.

Keep:

- useful operating structure;
- verification behavior;
- failure modes;
- attribution to Nate B. Jones or other sources;
- attribution to Leveragentic AI for additions and adaptation;
- generic integration points such as OB1/Brain-style memory, markdown fallback, or task trackers.

## Triple Packaging Marketplace Standard

A public share repo is package-ready when it includes:

1. **Skill source**
   - `skills/<skill-name>/SKILL.md`
   - frontmatter `name`, `metadata.version`, `metadata.author`, and routing `description`
   - body sections covering intent, inputs, process, output contract, failure modes, and verification

2. **Marketplace metadata**
   - `.agents/plugins/marketplace.json`
   - `.claude-plugin/marketplace.json`
   - `.claude-plugin/plugin.json`
   - `.codex-plugin/plugin.json`

3. **Expansion placeholders**
   - `.app.json`
   - `.mcp.json`

4. **Viewer/helper artifacts**
   - `scripts/build-brain-viewer-index.mjs`
   - generated `data/skills-index.json`

5. **Documentation**
   - `README.md`
   - `docs/publishing-rules.md`
   - attribution notes for any borrowed or adapted method

## Update Workflow

For `lev-plugins`:

1. Edit canonical private skill under `[plugin]/skills/<skill-name>/SKILL.md`.
2. Regenerate generated skill copies and plugin map using the private repo scripts.
3. Package with the private repo's packaging workflow.
4. Run secret/private-context review before publishing.

For `ant-share`:

1. Decide whether the update is a scrubbed derivative or a public-native skill.
2. Edit `skills/<skill-name>/SKILL.md`.
3. Update README and docs if the package surface changes.
4. Run `node scripts/build-brain-viewer-index.mjs`.
5. Run a scrub scan for private terms.
6. Commit and push to `antmcc-hub/ant-share`.

## Required Scrub Scan

At minimum, scan for:

```text
secret|token|key|AWS|Supabase|Telegram|Business Brain|Personal Brain|/Users/|client names|project IDs|phone numbers
```

Review matches manually. Some generic terms like `key` may be harmless; IDs and private paths are not.

## Relationship To skill-ops

`skill-ops` remains the operational packaging skill for private repo-managed skills. This document extends the decision boundary for public sharing:

- `skill-ops` answers: how do we package and validate skills?
- this document answers: where should the skill live, and what must be scrubbed before it is public?

