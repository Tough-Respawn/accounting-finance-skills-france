"""Behavioral checks for installation and portable context exports; no third-party packages."""

import contextlib
import importlib.util
import io
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("skill_tool", ROOT / "scripts/skill.py")
skill = importlib.util.module_from_spec(spec)
spec.loader.exec_module(skill)


class PortableSkillTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="accounting finance ")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.project = self.base / "project with spaces"
        self.project.mkdir()

    def run_tool(self, *args):
        capture = io.StringIO()
        with contextlib.redirect_stdout(capture), contextlib.redirect_stderr(capture):
            code = skill.main([str(arg) for arg in args])
        return code, capture.getvalue()

    def assert_ok(self, *args):
        code, output = self.run_tool(*args)
        self.assertEqual(code, 0, output)
        return output

    def test_all_native_targets_copy_a_complete_relocatable_skill(self):
        self.assert_ok("install", "--agent", *skill.AGENTS, "--project", self.project)
        for directory in set(skill.AGENTS.values()):
            installed = self.project / directory / skill.NAME
            self.assertEqual((installed / "SKILL.md").read_bytes(), (skill.SOURCE / "SKILL.md").read_bytes())
            self.assertEqual((installed / "methodology.md").read_bytes(), (skill.SOURCE / "methodology.md").read_bytes())
            self.assertEqual((installed / "LICENSE").read_bytes(), (ROOT / "LICENSE").read_bytes())
            originals = list((skill.SOURCE / "references").glob("*.md"))
            self.assertEqual(len(originals), 13)
            for original in originals:
                self.assertEqual((installed / "references" / original.name).read_bytes(), original.read_bytes())
            # Resolve links from the installed skill, with no dependency on repository layout.
            text = (installed / "SKILL.md").read_text(encoding="utf-8")
            for link in re.findall(r"\]\(([^)]+)\)", text):
                if "://" not in link:
                    self.assertTrue((installed / link.split("#")[0]).is_file(), link)
            self.assertFalse((installed / "commands").exists())
            self.assertFalse((installed / ".claude-plugin").exists())

    def test_repeated_install_preserves_identical_files(self):
        args = ("install", "--agent", "codex", "--project", self.project)
        self.assert_ok(*args)
        destination = self.project / ".agents/skills/accounting-finance/SKILL.md"
        before = destination.stat().st_mtime_ns
        output = self.assert_ok(*args)
        self.assertEqual(destination.stat().st_mtime_ns, before)
        self.assertIn("Wrote 0 file(s)", output)

    def test_conflict_is_detected_before_any_destination_is_written(self):
        conflict = self.project / ".cline/skills/accounting-finance/SKILL.md"
        conflict.parent.mkdir(parents=True)
        conflict.write_text("locally maintained instructions", encoding="utf-8")
        code, _ = self.run_tool("install", "--agent", "codex", "cline", "--project", self.project)
        self.assertEqual(code, 1)
        self.assertFalse((self.project / ".agents").exists())
        self.assertEqual(conflict.read_text(encoding="utf-8"), "locally maintained instructions")

    def test_force_updates_shipped_files_and_preserves_extra_files(self):
        destination = self.project / ".agents/skills/accounting-finance"
        destination.mkdir(parents=True)
        (destination / "SKILL.md").write_text("older copy", encoding="utf-8")
        extra = destination / "personal-notes.txt"
        extra.write_text("keep this", encoding="utf-8")
        self.assert_ok("install", "--agent", "codex", "--project", self.project, "--force")
        self.assertEqual((destination / "SKILL.md").read_bytes(), (skill.SOURCE / "SKILL.md").read_bytes())
        self.assertEqual(extra.read_text(encoding="utf-8"), "keep this")

    def test_dry_run_writes_nothing_for_install_and_export(self):
        self.assert_ok("install", "--agent", "claude-code", "--project", self.project, "--dry-run")
        self.assert_ok("export", "--domain", "paie", "--output", self.project / "new/bundle.md", "--dry-run")
        self.assertEqual(list(self.project.iterdir()), [])

    def test_custom_directory_and_source_overlap(self):
        custom = self.base / "personal skills"
        self.assert_ok("install", "--skills-dir", custom)
        self.assertTrue((custom / skill.NAME / "SKILL.md").is_file())
        before = (skill.SOURCE / "SKILL.md").read_bytes()
        code, _ = self.run_tool("install", "--skills-dir", skill.SOURCE.parent, "--force")
        self.assertEqual(code, 1)
        self.assertEqual((skill.SOURCE / "SKILL.md").read_bytes(), before)

    def test_non_directory_parent_fails_without_writes(self):
        parent = self.project / ".agents"
        parent.write_text("a regular file", encoding="utf-8")
        code, _ = self.run_tool("install", "--agent", "codex", "--project", self.project)
        self.assertEqual(code, 1)
        self.assertEqual(parent.read_text(encoding="utf-8"), "a regular file")

    def test_symlink_destination_is_rejected(self):
        external = self.base / "external"
        external.mkdir()
        link = self.project / ".agents"
        try:
            link.symlink_to(external, target_is_directory=True)
        except OSError:
            self.skipTest("Creating symlinks requires privileges on this machine")
        code, _ = self.run_tool("install", "--agent", "codex", "--project", self.project, "--force")
        self.assertEqual(code, 1)
        self.assertEqual(list(external.iterdir()), [])

    @unittest.skipUnless(sys.platform == "win32", "Windows junction test")
    def test_windows_junction_destination_is_rejected(self):
        external = self.base / "junction target"
        external.mkdir()
        link = self.project / ".agents"
        quote = lambda path: "'" + str(path).replace("'", "''") + "'"
        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command",
             "$ErrorActionPreference = 'Stop'\nNew-Item -ItemType Junction -Path "
             + quote(link) + " -Target " + quote(external) + " | Out-Null"],
            capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW,
        )
        if result.returncode:
            self.skipTest("Junction creation unavailable: " + result.stderr.strip())
        self.addCleanup(link.rmdir)
        code, _ = self.run_tool("install", "--agent", "codex", "--project", self.project, "--force")
        self.assertEqual(code, 1)
        self.assertEqual(list(external.iterdir()), [])

    def test_export_keeps_selected_resources_and_conditional_dependencies(self):
        for domain in ("fiscalite", "ifrs"):
            output = self.base / (domain + ".md")
            self.assert_ok("export", "--domain", domain, "--output", output)
            bundle = output.read_text(encoding="utf-8")
            for resource in ("SKILL.md", "methodology.md", "references/sources.md", f"references/{domain}.md"):
                self.assertIn((skill.SOURCE / resource).read_text(encoding="utf-8").rstrip(), bundle)
                self.assertEqual(bundle.count(f"# RESOURCE: {resource}\n"), 1)
            for dependency in ("taux-baremes", "pcg-index"):
                marker = f"# RESOURCE: references/{dependency}.md\n"
                if domain == "fiscalite":
                    self.assertIn(marker, bundle)
                else:
                    self.assertNotIn(marker, bundle)
            self.assertNotIn("# RESOURCE: references/paie.md\n", bundle)

    def test_export_all_and_extras_do_not_duplicate_resources(self):
        output = self.base / "all.md"
        self.assert_ok("export", "--domain", "all", "finance", "--extra", "glossaire", "glossaire", "decisions-cles", "--output", output)
        bundle = output.read_text(encoding="utf-8")
        for reference in (skill.SOURCE / "references").glob("*.md"):
            self.assertEqual(bundle.count(f"# RESOURCE: references/{reference.name}\n"), 1)

    def test_export_refuses_to_overwrite_existing_content_or_source(self):
        output = self.base / "bundle.md"
        output.write_text("keep", encoding="utf-8")
        code, _ = self.run_tool("export", "--domain", "audit", "--output", output)
        self.assertEqual(code, 1)
        self.assertEqual(output.read_text(encoding="utf-8"), "keep")
        code, _ = self.run_tool("export", "--domain", "audit", "--output", skill.SOURCE / "SKILL.md", "--force")
        self.assertEqual(code, 1)

    def test_cli_runs_from_an_unrelated_working_directory(self):
        output = self.base / "result.md"
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/skill.py"), "export", "--domain", "audit", "--output", str(output)],
            cwd=self.project, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(output.is_file())

    def test_unknown_agent_is_not_silently_installed(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/skill.py"), "install", "--agent", "deepseek", "--project", str(self.project)],
            capture_output=True, text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(list(self.project.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
