from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory, gettempdir
import unittest

from tools.install import CORE_FILES, IGNORE_ENTRIES, START, END


INSTALLER = Path(__file__).resolve().parents[1] / "tools" / "install.py"


class InstallTests(unittest.TestCase):
    def setUp(self):
        directory = TemporaryDirectory(prefix="agent-collab-install-")
        base = Path(directory.name).resolve()
        self.assertTrue(base.is_relative_to(Path(gettempdir()).resolve()))
        self.addCleanup(directory.cleanup)
        self.project = base / "已有项目 with spaces"
        self.project.mkdir()

    def install(self, *options):
        return subprocess.run(
            [sys.executable, "-X", "utf8", str(INSTALLER), str(self.project), *options],
            capture_output=True,
            encoding="utf-8",
            check=False,
        )

    def snapshot(self):
        return {
            path.relative_to(self.project).as_posix(): path.read_bytes()
            for path in self.project.rglob("*")
            if path.is_file()
        }

    def write(self, name, data):
        path = self.project / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def test_preview_is_read_only_by_default(self):
        self.write("AGENTS.md", b"# Existing rules\n")
        before = self.snapshot()
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("ADD    PROJECT.md", result.stdout)
        self.assertIn("APPEND AGENTS.md", result.stdout)
        self.assertEqual(self.snapshot(), before)

    def test_install_copies_the_core_files_into_an_empty_project(self):
        result = self.install("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        files = self.snapshot()
        self.assertEqual(set(files), set(CORE_FILES) | {"AGENTS.md", ".gitignore"})
        self.assertIn(START, files["AGENTS.md"])
        self.assertIn(END, files["AGENTS.md"])
        for entry in IGNORE_ENTRIES:
            self.assertIn(entry, files[".gitignore"].splitlines())

    def test_install_preserves_progress_rules_transcript_and_archive_on_rerun(self):
        rules = b"\xef\xbb\xbf# Existing rules\r\nKeep the report format.\r\n"
        progress = b"# Current progress\nSection one is approved.\n"
        archive = b"# Original history index\n"
        ignored = b"dist/\r\n" + IGNORE_ENTRIES[0] + b"\r\n"
        transcript = b"User: Keep all approved findings.\n"
        self.write("AGENTS.md", rules)
        self.write("PROJECT.md", progress)
        self.write(".gitignore", ignored)
        self.write("collaboration/ARCHIVE.md", archive)
        self.write("collaboration/mainline-transcripts/session.md", transcript)

        result = self.install("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        installed = self.snapshot()
        self.assertTrue(installed["AGENTS.md"].startswith(rules))
        self.assertTrue(installed[".gitignore"].startswith(ignored))
        self.assertEqual(installed["PROJECT.md"], progress)
        self.assertEqual(installed["collaboration/ARCHIVE.md"], archive)
        self.assertEqual(installed["collaboration/mainline-transcripts/session.md"], transcript)
        self.assertEqual(installed["AGENTS.md"].count(START), 1)
        for entry in IGNORE_ENTRIES:
            self.assertEqual(installed[".gitignore"].splitlines().count(entry), 1)

        result = self.install("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.snapshot(), installed)

    def test_conflicting_template_stops_before_any_writes(self):
        self.write("collaboration/templates/BRIEF.md", b"# Unrelated project brief\n")
        self.write(".gitignore", b"dist/\n")
        before = self.snapshot()
        result = self.install("--apply")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("BRIEF.md already has different content", result.stderr)
        self.assertEqual(self.snapshot(), before)

    def test_incomplete_agent_block_stops_before_any_writes(self):
        self.write("AGENTS.md", b"# Rules\n" + START + b"\n")
        before = self.snapshot()
        result = self.install("--apply")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("incomplete or repeated collaboration block", result.stderr)
        self.assertEqual(self.snapshot(), before)


if __name__ == "__main__":
    unittest.main()
