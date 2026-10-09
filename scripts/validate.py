#!/usr/bin/env python3
"""Validate this repository's packaging contract using only the standard library."""

import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
NAME = "alternancia-modelos"
PLUGIN = Path("plugins") / NAME


def package_files(directory):
    """Return sorted regular package files; never follow symbolic links."""
    directory = Path(directory)
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError(f"Invalid package directory: {directory}")
    files = []
    for path in sorted(directory.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"Symbolic links are not distributed: {path}")
        if path.is_dir():
            continue
        if not path.is_file() or path.suffix not in {".md", ".json"}:
            raise ValueError(f"Unexpected package file: {path}")
        files.append(path)
    return files


def validate(root=ROOT):
    root = Path(root).resolve()
    plugin = root / PLUGIN
    errors = []

    def check(condition, message):
        if not condition:
            errors.append(message)

    def read_json(path):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise ValueError("expected JSON object")
            return data
        except (OSError, ValueError) as error:
            errors.append(f"{path.relative_to(root)}: {error}")
            return {}

    try:
        files = package_files(plugin)
    except ValueError as error:
        return [str(error)]

    manifests = [read_json(plugin / name) for name in (
        "plugin.json", ".claude-plugin/plugin.json", ".codex-plugin/plugin.json"
    )]
    version = manifests[0].get("version", "")
    check(bool(re.fullmatch(r"\d+\.\d+\.\d+", version)), "Invalid release version")
    for manifest in manifests:
        check(manifest.get("name") == NAME, "Manifest name mismatch")
        check(manifest.get("version") == version, "Manifest version mismatch")
        check(bool(manifest.get("description")), "Manifest description missing")
    check(manifests[0].get("$schema") ==
          "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
          "Portable schema missing")
    check(manifests[2].get("skills") == "./skills/", "Incorrect Codex skills path")

    for location, portable in ((".claude-plugin/marketplace.json", False),
                               (".agents/plugins/marketplace.json", True)):
        market = read_json(root / location)
        check(market.get("name") == f"{NAME}-marketplace", "Marketplace name mismatch")
        entries = market.get("plugins", [])
        if not isinstance(entries, list) or len(entries) != 1 or not isinstance(entries[0], dict):
            errors.append(f"{location}: expected exactly one plugin entry")
            continue
        entry = entries[0]
        check(entry.get("name") == NAME, "Marketplace plugin name mismatch")
        expected = f"./{PLUGIN.as_posix()}"
        if portable:
            check(entry.get("source") == {"source": "local", "path": expected},
                  "Incorrect portable marketplace source")
            check(entry.get("policy") == {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                  "Incorrect marketplace policy")
            check(entry.get("category") == "Productivity", "Marketplace category missing")
        else:
            check(entry.get("source") == expected, "Incorrect Claude marketplace source")
            check(entry.get("version") == version, "Marketplace version mismatch")

    skill = plugin / "skills" / NAME / "SKILL.md"
    if not skill.is_file():
        errors.append("SKILL.md missing")
    for path in files:
        if path.suffix == ".json":
            read_json(path)
            continue
        text = path.read_text(encoding="utf-8")
        if path == skill or path.parent.name == "agents":
            sections = text.split("---", 2)
            check(text.startswith("---\n") and len(sections) == 3,
                  f"Frontmatter missing: {path.name}")
            if len(sections) == 3:
                check(bool(re.search(r"^name: [a-z0-9-]+$", sections[1], re.M)),
                      f"Frontmatter name missing: {path.name}")
                check("\ndescription: " in sections[1], f"Description missing: {path.name}")
        for target in re.findall(r"\]\(([^\s)]+)\)", text):
            if target.startswith(("https://", "http://", "#")):
                continue
            resolved = (path.parent / target.split("#", 1)[0]).resolve()
            check(resolved.is_relative_to(plugin.resolve()), f"Link leaves package: {target}")
            check(resolved.is_file(), f"Broken reference: {path.name} -> {target}")
    return errors


def main():
    errors = validate()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("OK: manifests, marketplaces, references and package files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
