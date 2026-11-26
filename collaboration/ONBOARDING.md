# Start a project or import an existing one

[Project mainline](../PROJECT.md) · [Workflow and prompts](GUIDE.md) · [Conversation index](ARCHIVE.md)

## Install the collaboration files

For a new repository, use GitHub's template option. To bring collaboration into a local project, put `AGENTS.md`, `PROJECT.md`, `collaboration/`, and `.gitignore` at its root. You can use any of these methods:

- **Windows launcher.** Get `Agent-Collaboration-Setup.exe` from the [published releases](https://github.com/Tau-57C/agent-collaboration-template/releases), open it, and select the project root. It needs Python 3.11 or later, accessible through `py -3` or `python`. It uses the same file installer as the command below.
- **macOS launcher.** Extract the [macOS installer ZIP](https://github.com/Tau-57C/agent-collaboration-template/releases/latest/download/Agent-Collaboration-Setup-macOS.zip), open `Install on macOS.command` in the extracted folder, and choose the project root. It needs Python 3.11 or later as `python3`. If Finder cannot launch the script, use the command-line method below from that same folder.
- **Command line.** Run the preview first, then apply it after checking the file changes. The script needs Python 3.11 or later. Use `python3` on systems where that is the Python 3 command.

  ```sh
  python tools/install.py "/path/to/project"
  python tools/install.py "/path/to/project" --apply
  ```

- **Manual copy.** Copy the four items. For files with the same name, merge in the collaboration rules and ignore entries while preserving any existing progress, archives, and project instructions.

The installer preserves existing `PROJECT.md` and `collaboration/ARCHIVE.md`, adds the collaboration block to existing assistant instructions, and extends existing ignore rules. It stops if a guide or template has conflicting content. To update an installed copy, merge the newer rules and guides into it and keep the project's records. The installer adds the files. An assistant runs the workflows below.

## New project

Open the project in an assistant and say “Initialize collaboration.” The assistant records the goal and next action, checks the ignore rules, and initializes local Git at the project root when checkpoint Git is enabled. An existing repository at that root is reused. Save the first commit at the first mainline checkpoint. Choose the roster when you request an independent round.

## Existing project

### Recover available history

Pick one assistant and say “Import the existing project.” Give it the project folder and any available chat exports or older file copies. The assistant can begin with the project files alone.

| Source | Where it goes |
|---|---|
| Verified current state, decisions, and next action | Current state in `PROJECT.md` |
| Earlier verified milestones | Checkpoint history in `PROJECT.md`, labeled as recovered records with evidence |
| Available visible conversation and attachments | `collaboration/mainline-transcripts/` |
| Conversation sources, coverage, and missing material | `collaboration/ARCHIVE.md` |

Inspect existing files, outputs, available chats, and backups. Reuse archived originals. Record missing conversations or file versions and mark uncertain conclusions as such. Preserve existing checkpoint IDs. If you can verify only the current state, start with an import baseline.

### Record checkpoints and verify the baseline

1. For a project with no Git repository, default to initializing local Git at its root when writing the first recovered checkpoint. Verify the ignore rules. Write and commit each recovered record before proceeding to the next. Use messages like `N01 Backfill the approved requirements`. If checkpoint Git is disabled, record the checkpoints in the project files.
2. A recovered record can describe an old milestone when the corresponding files are missing. Record the gap. Capture a historical file snapshot only if a complete earlier version can be verified. Keep that snapshot in an independent copy, link its Git reference, and label it as recovered at import. Keep present-day project files for the import baseline.
3. Verify the current state and record the next available mainline checkpoint, such as `N03 Import the current project`. Commit the verified current files and the mainline record. If there are no recoverable checkpoints and no repository, initialize and make the first commit here. For an existing repository, use the normal checkpoint rules and preserve existing history.
4. Tell the user what was recovered, what is missing, and the commit IDs or any failure. Hand off with “Continue from the mainline.”
