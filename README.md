# Agent Collaboration Template

[简体中文](README.zh-CN.md)

A reusable, file-based workflow for switching between AI assistants and getting independent second opinions. A human chooses who participates at each checkpoint, opens peer review, and approves what goes back into the project.

## Quick start

1. **Set up the project.** Use the template directly for a new project. For an existing project, bring in the core files and ask one assistant to import the progress and available conversations. [New project and existing project setup](collaboration/ONBOARDING.md)
2. **Start on the mainline.** Fill in [PROJECT.md](PROJECT.md). When switching assistants, say “Continue from the mainline.”
3. **Start an independent round.** Say “Branch from N03. Invite Codex and Gemini.” The current assistant prepares a shared brief and records the selected participants. Open a separate conversation for each participant and give all of them the same node.
4. **Review, then decide.** After every selected participant delivers, say “Open review for N03.” Read the submissions and have the participants compare them. Tell one assistant what to adopt and ask it to merge and verify. The next assistant resumes from the updated mainline.

[Workflow and short prompts](collaboration/GUIDE.md) · [Participant examples](collaboration/PARTICIPANTS.md) · [Tool compatibility](collaboration/COMPATIBILITY.md) · [Complete fictional example](examples/report-layout/N03/)

## What the repo contains

| Path | Purpose |
|---|---|
| [AGENTS.md](AGENTS.md) | Shared instructions for assistants |
| [PROJECT.md](PROJECT.md) | Current state, decisions, and checkpoints |
| [collaboration/templates/](collaboration/templates/) | Shared brief, participant roster, submissions, approvals, and reviews |
| [collaboration/ARCHIVE.md](collaboration/ARCHIVE.md) | Links to transcripts and decisions |
| [examples/](examples/) | Fictional records that show a round with six participants |
| [tools/check_node.py](tools/check_node.py) | Optional local checker for the roster, review gate, and merge records |

Agents may have different access to chat history. They can share visible messages by exporting them to ordinary files. The independent phase follows an explicit read scope. Use workspace permissions when you need enforced isolation. Session exports, real working nodes, and branch artifacts should stay local by default. The included Git ignore rules cover the designated runtime folders.

## Local verification

The workflow works with Markdown and JSON files. The optional checker uses the Python 3.11+ standard library.

```sh
python tools/check_node.py examples/report-layout/N03
python -m unittest discover -s tests -v
```

The tests walk a fictional node from independent work to merge and check that incomplete rounds are blocked. Client-specific verification is listed in [Tool compatibility](collaboration/COMPATIBILITY.md).

## License

[MIT License](LICENSE).
