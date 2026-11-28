"""Read a PROJECT.md revision and apply a conditional replacement."""

import argparse
from contextlib import contextmanager
from hashlib import sha256
import os
from pathlib import Path
import re
import stat
import sys
from tempfile import NamedTemporaryFile


PROJECT = Path(__file__).resolve().parents[1] / "PROJECT.md"
LOCK = PROJECT.parent / "collaboration" / ".project-write.lock"


class StaleRevision(Exception):
    """Another writer changed PROJECT.md after the snapshot."""


class BusyWriter(Exception):
    """Another process holds the project write lock."""


@contextmanager
def write_lock():
    # Keep the lock file in place so every process locks the same file.
    with LOCK.open("a+b") as handle:
        try:
            if os.name == "nt":
                import msvcrt

                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl

                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except (BlockingIOError, PermissionError) as error:
            raise BusyWriter from error
        yield


def apply(expected, draft):
    draft.decode("utf-8-sig")
    if not draft.strip():
        raise ValueError("draft is empty")
    with write_lock():
        current = PROJECT.read_bytes()
        if sha256(current).hexdigest() != expected:
            raise StaleRevision
        if current == draft:
            return
        with NamedTemporaryFile(dir=PROJECT.parent, delete=False) as handle:
            staged = Path(handle.name)
            try:
                handle.write(draft)
                handle.close()
                staged.chmod(stat.S_IMODE(PROJECT.stat().st_mode))
                os.replace(staged, PROJECT)
            finally:
                staged.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_subparsers(dest="command", required=True)
    modes.add_parser("read", help="Print the revision followed by the current file")
    save = modes.add_parser("apply", help="Replace the file only if its revision still matches")
    save.add_argument("revision", help="SHA-256 printed by the read command")
    save.add_argument("draft", type=Path, help="Path to a complete updated UTF-8 draft")
    args = parser.parse_args()
    try:
        if args.command == "read":
            current = PROJECT.read_bytes()
            header = f"revision {sha256(current).hexdigest()}\n".encode("ascii")
            sys.stdout.buffer.write(header + current)
        else:
            if re.fullmatch("[0-9a-f]{64}", args.revision) is None:
                parser.error("apply requires the revision printed by read")
            apply(args.revision, args.draft.read_bytes())
            print("PROJECT.md saved.")
    except StaleRevision:
        print("PROJECT.md changed. Read it again and merge your changes into the latest version.", file=sys.stderr)
        return 2
    except BusyWriter:
        print("Another session is saving PROJECT.md. Retry with the same revision.", file=sys.stderr)
        return 3
    except (OSError, UnicodeError, ValueError) as error:
        print(f"PROJECT.md could not be updated: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
