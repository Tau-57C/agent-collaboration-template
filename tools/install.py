"""Install the core collaboration files into an existing project."""

import argparse
from dataclasses import dataclass
import os
from pathlib import Path
import stat
import sys
from tempfile import NamedTemporaryFile


SOURCE = Path(__file__).resolve().parents[1]
CORE_FILES = (
    "PROJECT.md",
    "collaboration/ARCHIVE.md",
    "collaboration/COMPATIBILITY.md",
    "collaboration/GUIDE.md",
    "collaboration/ONBOARDING.md",
    "collaboration/PARTICIPANTS.md",
    "collaboration/update_project.py",
    "collaboration/templates/BRIEF.md",
    "collaboration/templates/FINAL.md",
    "collaboration/templates/REVIEW-OPEN.md",
    "collaboration/templates/REVIEW.md",
    "collaboration/templates/SUBMISSION.md",
    "collaboration/templates/decision.json",
    "collaboration/templates/node.json",
    "collaboration/templates/status.json",
)
IGNORE_ENTRIES = (
    b"/collaboration/nodes/",
    b"/collaboration/.project-write.lock",
    b"/collaboration/mainline-notes/",
    b"/collaboration/mainline-transcripts/",
)
START = b"<!-- agent-collaboration:start -->"
END = b"<!-- agent-collaboration:end -->"


class InstallError(ValueError):
    """The target cannot be initialized without resolving a conflict."""


@dataclass(frozen=True)
class Change:
    path: Path
    before: bytes | None
    after: bytes
    reason: str

    @property
    def action(self):
        if self.before is None:
            return "ADD"
        if self.before == self.after:
            return "KEEP"
        return "APPEND"


def read_target(target, path):
    for item in (path, *path.parents):
        if item == target:
            break
        if item.is_symlink() or item.resolve() != item:
            raise InstallError(f"{item.relative_to(target)} points outside the installation path or is a link")
        if item != path and item.exists() and not item.is_dir():
            raise InstallError(f"{item.relative_to(target)} must be a directory")
    if not path.exists():
        return None
    if not path.is_file():
        raise InstallError(f"{path.relative_to(target)} must be a file")
    return path.read_bytes()


def append_block(original, block):
    original = original or b""
    newline = b"\r\n" if b"\r\n" in original else b"\n"
    head = original
    if original and not original.endswith(newline):
        head += newline
    if original and not head.endswith(newline * 2):
        head += newline
    return head + block.replace(b"\r\n", b"\n").replace(b"\n", newline) + newline


def merge_rules(original, template):
    if original is not None:
        original.decode("utf-8-sig")
        original_lf = original.replace(b"\r\n", b"\n").removeprefix(b"\xef\xbb\xbf")
        template_lf = template.replace(b"\r\n", b"\n").strip()
        lines = original_lf.splitlines()
        starts = lines.count(START)
        ends = lines.count(END)
        if starts or ends:
            if starts != 1 or ends != 1 or lines.index(START) >= lines.index(END):
                raise InstallError("AGENTS.md has an incomplete or repeated collaboration block")
            return original
        if template_lf in original_lf:
            return original
    block = b"\n".join((START, template.strip(), END))
    return append_block(original, block)


def merge_ignore(original):
    if original is not None:
        original.decode("utf-8-sig")
    lines = {line.strip() for line in (original or b"").removeprefix(b"\xef\xbb\xbf").splitlines()}
    additions = [entry for entry in IGNORE_ENTRIES if entry not in lines]
    if not additions:
        return original
    return append_block(original, b"\n".join(additions))


def make_plan(target):
    changes = []
    for name in CORE_FILES:
        path = target / name
        before = read_target(target, path)
        template = (SOURCE / name).read_bytes()
        if before is not None and name in {"PROJECT.md", "collaboration/ARCHIVE.md"}:
            changes.append(Change(path, before, before, "existing project progress or archive"))
        elif before is not None and before.replace(b"\r\n", b"\n") != template.replace(b"\r\n", b"\n"):
            raise InstallError(f"{name} already has different content. Merge it before installing.")
        else:
            changes.append(Change(path, before, template if before is None else before, "core template"))
    ignore = target / ".gitignore"
    before = read_target(target, ignore)
    changes.append(Change(ignore, before, merge_ignore(before), "local transcripts and node data"))
    rules = target / "AGENTS.md"
    before = read_target(target, rules)
    changes.append(Change(rules, before, merge_rules(before, (SOURCE / "AGENTS.md").read_bytes()), "collaboration rules"))
    return changes


def apply_change(target, change):
    if change.action == "KEEP":
        return
    path = change.path
    if read_target(target, path) != change.before:
        raise InstallError(f"{path.relative_to(target)} changed after the preview. Run the installer again.")
    if change.before is None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as handle:
            handle.write(change.after)
        return
    with NamedTemporaryFile(dir=path.parent, delete=False) as handle:
        replacement = Path(handle.name)
        try:
            handle.write(change.after)
            handle.close()
            replacement.chmod(stat.S_IMODE(path.stat().st_mode))
            os.replace(replacement, path)
        finally:
            replacement.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path, help="Path to an existing project folder")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--dry-run", action="store_true", help="Preview changes (default)")
    modes.add_argument("--apply", action="store_true", help="Apply changes to the target")
    options = parser.parse_args()
    try:
        target = options.target.expanduser().resolve(strict=True)
        if not target.is_dir() or target.is_relative_to(SOURCE):
            raise InstallError("Choose an existing project directory outside this template checkout")
        plan = make_plan(target)
        print(f"Project: {target}")
        for change in plan:
            print(f"{change.action:6} {change.path.relative_to(target).as_posix()} ({change.reason})")
        if options.apply:
            for change in plan:
                apply_change(target, change)
            print("Installed. Ask one assistant to import the existing project history.")
        else:
            print("Preview complete. Run again with --apply to write these changes.")
    except (InstallError, OSError, UnicodeError, RuntimeError) as error:
        print(f"Installation stopped: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
