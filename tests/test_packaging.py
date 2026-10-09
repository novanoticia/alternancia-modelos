import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build import build
from validate import NAME, PLUGIN, validate


class PackagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        for folder in ("plugins", ".agents", ".claude-plugin"):
            shutil.copytree(ROOT / folder, self.root / folder)

    def test_release_is_reproducible_complete_and_self_contained(self):
        original = self.root / "upstream" / "secret-original.md"
        original.parent.mkdir()
        original.write_text("Never include history in install artifacts")
        first = build(self.root, Path(self.temp.name) / "one")
        second = build(self.root, Path(self.temp.name) / "two")
        for a, b in zip(first, second):
            self.assertEqual(a.read_bytes(), b.read_bytes())
            with zipfile.ZipFile(a) as archive:
                names = archive.namelist()
                self.assertTrue(all(n.startswith(f"{NAME}/") for n in names))
                self.assertFalse(any("upstream" in n or "secret" in n for n in names))
                extracted = Path(self.temp.name) / a.stem
                archive.extractall(extracted)
                base = extracted / NAME
                skill = base / "skills" / NAME if "-plugin-" in a.name else base
                self.assertTrue((skill / "SKILL.md").is_file())
                self.assertEqual(len(list((skill / "references").glob("*.md"))), 6)
                if "-plugin-" in a.name:
                    for manifest in ("plugin.json", ".claude-plugin/plugin.json", ".codex-plugin/plugin.json"):
                        self.assertEqual(json.loads((base / manifest).read_text())["name"], NAME)
        sums = (first[0].parent / "SHA256SUMS").read_text()
        for artifact in first:
            self.assertIn(hashlib.sha256(artifact.read_bytes()).hexdigest(), sums)

    def test_broken_reference_blocks_release(self):
        (self.root / PLUGIN / "skills" / NAME / "references" / "contrato.md").unlink()
        self.assertTrue(any("Broken reference" in e for e in validate(self.root)))
        with self.assertRaises(ValueError):
            build(self.root)

    def test_divergent_manifest_blocks_release(self):
        path = self.root / PLUGIN / ".claude-plugin" / "plugin.json"
        data = json.loads(path.read_text())
        data["version"] = "0.0.0"
        path.write_text(json.dumps(data))
        self.assertIn("Manifest version mismatch", validate(self.root))

    def test_symlink_cannot_include_outside_content(self):
        outside = Path(self.temp.name) / "private.md"
        outside.write_text("private")
        (self.root / PLUGIN / "leak.md").symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "Symbolic links"):
            build(self.root)

    def test_output_cannot_pollute_plugin(self):
        with self.assertRaisesRegex(ValueError, "outside the plugin"):
            build(self.root, self.root / PLUGIN / "dist")


if __name__ == "__main__":
    unittest.main()
