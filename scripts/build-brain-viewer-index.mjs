#!/usr/bin/env node
import { mkdir, readFile, readdir, writeFile } from "node:fs/promises";
import path from "node:path";

const root = process.cwd();
const skillsDir = path.join(root, "skills");
const outDir = path.join(root, "data");
const outFile = path.join(outDir, "skills-index.json");

function parseFrontmatter(text) {
  if (!text.startsWith("---\n")) return {};
  const end = text.indexOf("\n---", 4);
  if (end === -1) return {};
  const block = text.slice(4, end).trim();
  const result = {};
  let current = null;
  for (const line of block.split("\n")) {
    const top = line.match(/^([a-zA-Z0-9_-]+):\s*(.*)$/);
    const nested = line.match(/^\s+([a-zA-Z0-9_-]+):\s*(.*)$/);
    if (top) {
      current = top[1];
      result[current] = top[2].replace(/^["']|["']$/g, "");
    } else if (nested && current === "metadata") {
      result.metadata ||= {};
      result.metadata[nested[1]] = nested[2].replace(/^["']|["']$/g, "");
    }
  }
  return result;
}

const skills = {};
for (const entry of await readdir(skillsDir, { withFileTypes: true })) {
  if (!entry.isDirectory()) continue;
  const skillPath = path.join(skillsDir, entry.name, "SKILL.md");
  const text = await readFile(skillPath, "utf8");
  const frontmatter = parseFrontmatter(text);
  const name = frontmatter.name || entry.name;
  skills[name] = {
    version: frontmatter.metadata?.version || "unknown",
    desc: frontmatter.description || "",
    path: path.relative(root, skillPath),
    plugin: "ant-share",
    col: "workflow",
    status: "live",
    profiles: ["Agent workflow"]
  };
}

const index = {
  meta: {
    repo: "antmcc-hub/ant-share",
    updated: new Date().toISOString(),
    helper: "scripts/build-brain-viewer-index.mjs"
  },
  plugins: ["ant-share"],
  skills,
  chain: ["spec-writer", "session-closeout", "weekly-retro"],
  pmap: {
    "Agent workflow": Object.keys(skills)
  }
};

await mkdir(outDir, { recursive: true });
await writeFile(outFile, `${JSON.stringify(index, null, 2)}\n`);
console.log(`Wrote ${path.relative(root, outFile)} (${Object.keys(skills).length} skills)`);
