#!/usr/bin/env python3
"""Produce deterministic plugin and standalone skill archives."""

import argparse
import hashlib
import json
from pathlib import Path
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
    artifacts = []
    for kind, source in (("plugin", plugin), ("skill", plugin / "skills" / NAME)):
        destination = output / f"{NAME}-{kind}-{version}.zip"
        write_archive(source, destination)
        artifacts.append(destination)
    sums = "".join(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n"
                   for path in artifacts)
    (output / "SHA256SUMS").write_text(sums, encoding="utf-8")
    return artifacts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Output directory (default: dist/)")
    args = parser.parse_args()
    for artifact in build(output=args.output):
        print(artifact)


if __name__ == "__main__":
    main()
