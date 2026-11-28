from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest


SOURCE = Path(__file__).resolve().parents[1] / "collaboration" / "update_project.py"


class ProjectSaveTests(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory(prefix="agent-project-save-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.project = self.root / "PROJECT.md"
        self.initial = "# 项目主线\n\nN01\n".encode("utf-8")
        self.project.write_bytes(self.initial)
        self.script = self.root / "collaboration" / SOURCE.name
        self.script.parent.mkdir()
        shutil.copy2(SOURCE, self.script)

    def command(self, *args):
        return [sys.executable, str(self.script), *args]

    def read(self):
        result = subprocess.run(self.command("read"), capture_output=True, check=True, timeout=10)
        revision, content = result.stdout.split(b"\n", 1)
        return revision.decode("ascii").removeprefix("revision "), content

    def test_parallel_sessions_cannot_overwrite_each_other(self):
        revision, base = self.read()
        self.assertEqual(base, self.initial)
        entries = [b"Session A finished.\n", b"Session B finished.\n"]
        drafts = [self.root / f"draft-{index}.md" for index in range(len(entries))]
        for draft, entry in zip(drafts, entries):
            draft.write_bytes(base + entry)

        with subprocess.Popen(self.command("apply", revision, str(drafts[0])), stdout=subprocess.PIPE) as first:
            with subprocess.Popen(self.command("apply", revision, str(drafts[1])), stdout=subprocess.PIPE) as second:
                first.communicate(timeout=10)
                second.communicate(timeout=10)
        results = [first.returncode, second.returncode]
        self.assertEqual(results.count(0), 1, results)
        winner = results.index(0)
        loser = 1 - winner
        self.assertIn(results[loser], (2, 3))
        self.assertEqual(self.project.read_bytes(), base + entries[winner])

        retry = subprocess.run(self.command("apply", revision, str(drafts[loser])), capture_output=True, timeout=10)
        self.assertEqual(retry.returncode, 2)
        latest, content = self.read()
        drafts[loser].write_bytes(content + entries[loser])
        subprocess.run(self.command("apply", latest, str(drafts[loser])), check=True, capture_output=True, timeout=10)
        self.assertEqual(self.project.read_bytes(), base + entries[winner] + entries[loser])

    def test_rejects_invalid_draft_without_changing_project(self):
        revision, _ = self.read()
        draft = self.root / "bad.md"
        draft.write_bytes(b"\xff")
        result = subprocess.run(self.command("apply", revision, str(draft)), capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.project.read_bytes(), self.initial)


if __name__ == "__main__":
    unittest.main()
