# Agent Collaboration Template

[简体中文](README.zh-CN.md)

A file-based workflow for handing work between AI assistants and getting independent second opinions. Keep one mainline, choose participants for each independent round, and decide which results enter the project.

## Quick start

1. **Install the files.** Use the GitHub template for a new repository, copy the four core items into a local project, or use the Windows or macOS launcher. The command-line installer supports a read-only preview. [Installation and import](collaboration/ONBOARDING.md)
2. **Start or import.** Say “Initialize collaboration” for a new project or “Import the existing project” for ongoing work. `PROJECT.md` holds progress, decisions, open discussions, and the next action.
3. **Choose an independent round.** Name the participants and the source checkpoint. Open a fresh session for each. They use the same frozen inputs and save their results in their own branches.
4. **Open review and decide.** After all selected participants deliver, open peer review. Tell one merge owner what to adopt and ask them to verify it. Then resume from the mainline.

## Install

- **Windows.** Open the [Windows installer](https://github.com/Tau-57C/agent-collaboration-template/releases/latest/download/Agent-Collaboration-Setup.exe) and select the project folder. It needs Python 3.11 or later through `py -3` or `python`.
- **macOS.** Extract the [macOS installer ZIP](https://github.com/Tau-57C/agent-collaboration-template/releases/latest/download/Agent-Collaboration-Setup-macOS.zip), open `Install on macOS.command`, and select the project folder. It needs Python 3.11 or later as `python3`.
[Manual copy and command-line options](collaboration/ONBOARDING.md#install-the-collaboration-files) are available for other setups.

The file installer sets up collaboration files. Your assistant imports history and handles local checkpoint commits after you ask it to start or import. You can use the workflow with files alone by setting “Checkpoint Git” to “Files only.” [Local Git rules](collaboration/GUIDE.md#local-git-at-checkpoints)

## Copyable prompts

Replace N03 and bracketed placeholders with your checkpoint and task details.

### Set up

| When             | Who                 | Say                          |
| ---------------- | ------------------- | ---------------------------- |
| New project      | Project assistant   | Initialize collaboration.    |
| Existing project | Importing assistant | Import the existing project. |

### Mainline and handoff

For a new mainline task, the assistant first reads the current-state table. When switching chats or catching up on session notes, say “Continue from the mainline and do [task].”

| When                              | Who                          | Say                                                             |
| --------------------------------- | ---------------------------- | --------------------------------------------------------------- |
| Switch sessions or resume after merge | Next mainline session | Continue from the mainline. |
| Advance the work                  | Current assistant            | Continue on the mainline and do [task].                         |
| Add materials                     | Current assistant            | Use [file] as input for the current task.                       |
| Check progress                    | Current assistant            | What’s the current checkpoint and next step?                    |
| List all checkpoints              | Current assistant            | List all checkpoints.                                           |
| Record a checkpoint               | Current assistant            | Record a mainline checkpoint here.                              |
| Prepare a handoff (optional)      | Outgoing assistant           | Save open discussions for handoff.                              |
| Resume a specific topic           | Incoming assistant           | Continue from the mainline on [topic].                          |
| Supply missing chat excerpts      | Incoming assistant           | Continue from the mainline using these excerpts.                |

### Branch, review, and merge

| When                     | Who                       | Say                                                                                  |
| ------------------------ | ------------------------- | ------------------------------------------------------------------------------------ |
| Branch from a checkpoint | Mainline assistant        | Branch from N03. Invite [participants] to do [task] independently.                   |
| Start independent work   | Each fresh session        | Work independently on N03, then record delivery.                                     |
| Check deliveries         | Coordinator               | Who still needs to deliver for N03?                                                  |
| Follow up before review  | Selected branch assistant | Stay independent and add [item].                                                     |
| Open review              | Coordinator               | Open review for N03.                                                                 |
| Review peers             | Each branch assistant     | Review other branches’ work and dialogue using N03 criteria.                         |
| Decide and merge         | Designated merge owner    | For N03, adopt [items], then merge and verify.                                       |

### As needed

| When                        | Who                           | Say                                                              |
| --------------------------- | ----------------------------- | ---------------------------------------------------------------- |
| Archive the exact wording   | Assistant with the original   | Archive this excerpt verbatim.                                   |
| Inspect local versions      | Assistant with project access | Show the last five local Git commits.                            |
| Turn off checkpoint commits | Current assistant             | Record checkpoints in files only. Disable automatic Git commits. |

## Project files

| Path | Purpose |
|---|---|
| [AGENTS.md](AGENTS.md) | Shared instructions for assistants |
| [PROJECT.md](PROJECT.md) | Mainline progress, decisions, handoff, and checkpoints |
| [collaboration/GUIDE.md](collaboration/GUIDE.md) | Workflow details and bilingual prompts |
| [collaboration/PARTICIPANTS.md](collaboration/PARTICIPANTS.md) | Roster examples across clients and sessions |
| [collaboration/ARCHIVE.md](collaboration/ARCHIVE.md) | Index of dialogue, reviews, and decisions |
| [examples/](examples/) | A fictional six-participant round from delivery through merge |
| [tools/check_node.py](tools/check_node.py) | Optional check of records, participant statuses, review, and merge |

Clients differ in how they expose visible conversation history. Export or copy project dialogue as needed. The independent phase follows the shared read scope. Use workspace access controls when you require enforced isolation. [Client compatibility](collaboration/COMPATIBILITY.md)

## Verify the template or build the Windows installer

```sh
python tools/check_node.py examples/report-layout/N03
python -m unittest discover -s tests -v
```

On Windows, use Python 3.11 or later and the .NET Framework C# compiler to build the launcher from the repository:

```powershell
python tools/build_windows_installer.py Agent-Collaboration-Setup.exe
```

The test suite exercises the fictional workflow and installer. Live conversation export and sharing across specific clients are tracked in [client compatibility](collaboration/COMPATIBILITY.md).

[MIT License](LICENSE).
