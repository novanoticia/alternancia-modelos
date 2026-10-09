#!/usr/bin/env python3
"""Produce deterministic plugin and standalone skill archives."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import zipfile

from validate import NAME, PLUGIN, ROOT, package_files, validate


def write_archive(source, destination):
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED,
                         compresslevel=9) as archive:
        for path in package_files(source):
            relative = Path(NAME) / path.relative_to(source)
            info = zipfile.ZipInfo(relative.as_posix(), date_time=(2026, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, path.read_bytes(), compresslevel=9)


def build(root=ROOT, output=None):
    root = Path(root).resolve()
    errors = validate(root)
    if errors:
        raise ValueError("\n".join(errors))
    plugin = root / PLUGIN
    output = Path(output) if output else root / "dist"
    output = output.resolve()
    if output.is_relative_to(plugin):
        raise ValueError("Build output must be outside the plugin")
    output.mkdir(parents=True, exist_ok=True)
    version = json.loads((plugin / "plugin.json").read_text(encoding="utf-8"))["version"]
    sources = (plugin, plugin / "skills" / NAME)
    artifacts = [output / f"{NAME}-{kind}-{version}.zip" for kind in ("plugin", "skill")]
    targets = [*artifacts, output / "SHA256SUMS"]
    for target in targets:
        if target.is_symlink() or (target.exists() and not target.is_file()):
            raise ValueError(f"Unsafe output target: {target}")
    # Generate everything before replacing existing artifacts. os.replace replaces
    # a directory entry rather than following a symlink created during the build.
    # Each replacement is atomic; the three-file release is not a transaction.
    with tempfile.TemporaryDirectory(prefix=".alternancia-build-", dir=output) as staging:
        staged = [Path(staging) / target.name for target in targets]
        for source, destination in zip(sources, staged[:2]):
            write_archive(source, destination)
        sums = "".join(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n"
                       for path in staged[:2])
        staged[2].write_text(sums, encoding="utf-8")
        for source, target in zip(staged, targets):
            os.replace(source, target)
    return artifacts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Output directory (default: dist/)")
    args = parser.parse_args()
    try:
        artifacts = build(output=args.output)
    except (OSError, ValueError) as error:
        print(f"Build failed: {error}", file=sys.stderr)
        return 1
    for artifact in artifacts:
        print(artifact)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
