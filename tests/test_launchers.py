from pathlib import Path
import os
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest


ROOT = Path(__file__).resolve().parents[1]


class LauncherTests(unittest.TestCase):
    def check_install(self, command, project):
        project.mkdir()
        rules = project / "AGENTS.md"
        original = b"# Existing rules\n"
        rules.write_bytes(original)
        result = subprocess.run(
            [*command, str(project)], capture_output=True, encoding="utf-8",
            env={**os.environ, "PYTHONUTF8": "1"}, timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            {item.name for item in project.iterdir()},
            {"AGENTS.md", "PROJECT.md", "collaboration", ".gitignore"},
        )
        self.assertTrue(rules.read_bytes().startswith(original))
        guide = Path("collaboration/GUIDE.md")
        self.assertEqual((project / guide).read_bytes(), (ROOT / guide).read_bytes())

    @unittest.skipUnless(sys.platform == "win32", "Windows launcher")
    def test_windows_build_and_install(self):
        with TemporaryDirectory(prefix="agent-collab-windows-") as folder:
            work = Path(folder)
            launcher = work / "Agent-Collaboration-Setup.exe"
            subprocess.run(
                [sys.executable, str(ROOT / "tools/build_windows_installer.py"), str(launcher)],
                check=True, timeout=60,
            )
            self.check_install([str(launcher), "--install"], work / "Project 有空格")

    @unittest.skipUnless(sys.platform == "darwin", "macOS launcher")
    def test_macos_install(self):
        with TemporaryDirectory(prefix="agent-collab-macos-") as folder:
            self.check_install(
                [str(ROOT / "Install on macOS.command"), "--project"],
                Path(folder) / "Project 有空格",
            )


if __name__ == "__main__":
    unittest.main()
