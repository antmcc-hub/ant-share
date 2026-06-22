#!/usr/bin/env python3
"""Build a Microsoft 365 app package for Copilot Cowork from ant-share skills."""

from __future__ import annotations

import argparse
import base64
import json
import re
import shutil
import uuid
import zipfile
from pathlib import Path


MAX_SKILLS_PER_PACKAGE = 20
NAMESPACE = uuid.UUID("1e0ed278-21ad-4733-9b37-3f0c4614d5b8")
COLOR_PNG = (
    "iVBORw0KGgoAAAANSUhEUgAAAMAAAADACAYAAABS3GwHAAAACXBIWXMAAAsTAAALEwEAmpwY"
    "AAABl0lEQVR4nO3TMQ0AAAgDsJz/aWFEUQSG0tnclwIAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAgLsGxhAAAdWk9VYAAAAASUVORK5CYII="
)
OUTLINE_PNG = (
    "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAAsTAAALEwEAmpwY"
    "AAAAKUlEQVR4nO3OMQEAAAgDoJvc6FJ4QZyAZN21AAAAAAAAAAAAAADgGwMeIAABk8OupQAA"
    "AABJRU5ErkJggg=="
)


def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return {}

    fields: dict[str, str] = {}
    lines = match.group(1).splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line or line.startswith((" ", "\t")) or ":" not in line:
            i += 1
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value in {"|", ">"}:
            block: list[str] = []
            i += 1
            while i < len(lines) and (lines[i].startswith((" ", "\t")) or not lines[i].strip()):
                block.append(lines[i].strip())
                i += 1
            fields[key] = "\n".join(block).strip()
            continue
        fields[key] = value.strip("\"'")
        i += 1
    return fields


def rewrite_skill_name(content: str, folder_name: str) -> str:
    match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not match:
        return content
    frontmatter = match.group(1)
    if re.search(r"^name:\s*.*$", frontmatter, flags=re.MULTILINE):
        frontmatter = re.sub(r"^name:\s*.*$", f"name: {folder_name}", frontmatter, count=1, flags=re.MULTILINE)
    else:
        frontmatter = f"name: {folder_name}\n{frontmatter}"
    return f"---\n{frontmatter}\n---\n{content[match.end():]}"


def plugin_metadata(root: Path) -> dict:
    plugin_json = root / ".claude-plugin" / "plugin.json"
    if not plugin_json.exists():
        return {}
    try:
        return json.loads(plugin_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def copy_skill(skill_md: Path, target_skills_dir: Path) -> str:
    folder_name = skill_md.parent.name
    target_dir = target_skills_dir / folder_name
    if target_dir.exists():
        shutil.rmtree(target_dir)
    shutil.copytree(
        skill_md.parent,
        target_dir,
        ignore=shutil.ignore_patterns(".DS_Store", "__pycache__", "*.pyc", ".*"),
    )
    skill_target = target_dir / "SKILL.md"
    skill_target.write_text(rewrite_skill_name(skill_target.read_text(encoding="utf-8"), folder_name), encoding="utf-8")
    return folder_name


def manifest(root: Path, package_name: str, skill_folders: list[str]) -> dict:
    metadata = plugin_metadata(root)
    display_name = package_name.replace("-", " ").title()
    description = metadata.get("description") or "Portable agent workflow skills for Copilot Cowork."
    if len(description) > 250:
        description = description[:247].rstrip() + "..."

    return {
        "$schema": "https://developer.microsoft.com/json-schemas/teams/v1.28/MicrosoftTeams.schema.json",
        "manifestVersion": "1.28",
        "version": metadata.get("version", "0.1.0"),
        "id": str(uuid.uuid5(NAMESPACE, package_name)),
        "developer": {
            "name": metadata.get("author", {}).get("name", "Leveragentic AI"),
            "websiteUrl": metadata.get("author", {}).get("url", "https://leveragentic.ai"),
            "privacyUrl": "https://leveragentic.ai/privacy",
            "termsOfUseUrl": "https://leveragentic.ai/terms",
        },
        "name": {
            "short": display_name[:30],
            "full": f"{display_name} for Copilot Cowork",
        },
        "description": {
            "short": description[:80],
            "full": description,
        },
        "icons": {
            "color": "color.png",
            "outline": "outline.png",
        },
        "accentColor": "#1A1A2E",
        "agentSkills": [{"folder": f"./skills/{folder}"} for folder in skill_folders],
    }


def zip_dir(source_dir: Path, zip_path: Path) -> None:
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source_dir.rglob("*")):
            if path == zip_path or path.is_dir():
                continue
            archive.write(path, path.relative_to(source_dir))


def chunks(items: list[Path], size: int) -> list[list[Path]]:
    return [items[index : index + size] for index in range(0, len(items), size)]


def build(root: Path, output_root: Path) -> list[Path]:
    skill_files = sorted((root / "skills").glob("*/SKILL.md"))
    if not skill_files:
        return []

    output_root.mkdir(parents=True, exist_ok=True)
    package_base = plugin_metadata(root).get("name", "ant-share")
    built: list[Path] = []
    for index, group in enumerate(chunks(skill_files, MAX_SKILLS_PER_PACKAGE), start=1):
        suffix = "" if len(skill_files) <= MAX_SKILLS_PER_PACKAGE else f"-part-{index}"
        package_name = f"{package_base}{suffix}"
        package_dir = output_root / package_name
        if package_dir.exists():
            shutil.rmtree(package_dir)
        (package_dir / "skills").mkdir(parents=True)

        skill_folders = [copy_skill(skill_md, package_dir / "skills") for skill_md in group]
        (package_dir / "manifest.json").write_text(
            json.dumps(manifest(root, package_name, skill_folders), indent=2) + "\n",
            encoding="utf-8",
        )
        (package_dir / "color.png").write_bytes(base64.b64decode(COLOR_PNG))
        (package_dir / "outline.png").write_bytes(base64.b64decode(OUTLINE_PNG))

        zip_path = output_root / f"{package_name}.zip"
        zip_dir(package_dir, zip_path)
        built.append(zip_path)
    return built


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument("--out", default="dist/m365", help="Output directory for package folders and ZIPs")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    output_root = (root / args.out).resolve()
    built = build(root, output_root)
    for package in built:
        try:
            display_path = package.relative_to(root)
        except ValueError:
            display_path = package
        print(f"packaged: {display_path}")
    print(f"\nDone. Built {len(built)} Copilot Cowork package(s).")
    return 0 if built else 1


if __name__ == "__main__":
    raise SystemExit(main())
