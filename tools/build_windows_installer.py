"""Build the Windows folder-picker launcher with the core template embedded."""

import argparse
import os
from pathlib import Path
import shutil
import subprocess
from tempfile import NamedTemporaryFile, TemporaryDirectory
from zipfile import ZIP_DEFLATED, ZipFile

from install import CORE_FILES, SOURCE


def build(output):
    compiler = (
        Path(os.environ.get("WINDIR", r"C:\Windows"))
        / "Microsoft.NET" / "Framework64" / "v4.0.30319" / "csc.exe"
    )
    if not compiler.is_file():
        raise FileNotFoundError("Building this launcher requires the Windows .NET Framework C# compiler.")

    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix="agent-collab-build-") as folder:
        work = Path(folder)
        with ZipFile(work / "template.zip", "w", compression=ZIP_DEFLATED) as template:
            for name in ("AGENTS.md", ".gitignore", "LICENSE", "tools/install.py", *CORE_FILES):
                template.write(SOURCE / name, name)

        executable = work / "setup.exe"
        subprocess.run(
            [
                str(compiler), "/nologo", "/utf8output", "/target:winexe",
                "/out:setup.exe", "/reference:System.Windows.Forms.dll",
                "/reference:System.IO.Compression.FileSystem.dll",
                "/resource:template.zip,TemplateData", str(SOURCE / "tools/windows_installer.cs"),
            ],
            cwd=work,
            check=True,
        )

        with NamedTemporaryFile(dir=output.parent, delete=False) as destination:
            pending = Path(destination.name)
            with executable.open("rb") as source:
                shutil.copyfileobj(source, destination)
        try:
            pending.replace(output)
        finally:
            pending.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="Path to the resulting Windows .exe")
    args = parser.parse_args()
    build(args.output)


if __name__ == "__main__":
    main()
