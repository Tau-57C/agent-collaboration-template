# Start a project or import an existing one

[Project mainline](../PROJECT.md) · [Workflow and prompts](GUIDE.md) · [Conversation index](ARCHIVE.md)

## New project

Create the project from the template or copy its core files into the new folder. Open the project with one assistant and say:

> Initialize this project. Record my goal and the next action in PROJECT.md.
>
> 初始化协作，写好项目目标和下一步。

Start ordinary work on the mainline. The assistant adds checkpoints as work produces verifiable results. Choose the participants when you request the first independent round.

## Existing project

### 1. Bring in the core files

- Copy or merge `AGENTS.md` and `PROJECT.md` at the project root, and copy `collaboration/`. Keep existing project rules, documents, and directories. If a destination file already exists, merge the relevant sections into it.
- Add the runtime ignore entries from the template's `.gitignore` when using Git. The local verifier in `tools/` is optional.
- Pick one assistant for the import. Give it the current project folder and access to the relevant histories or exported files.

### 2. Import history with that assistant

> Import the existing project into the collaboration template. Reconstruct the verified progress, decisions, and next action. Archive every available project conversation and list any gaps.
>
> 导入旧项目。梳理过去的任务、进度和决定，归档可取得的全部项目会话。缺哪段请列出来。

| Source | Where the assistant puts it |
|---|---|
| Current project state and next action | `PROJECT.md` current state |
| Earlier tasks, decisions, changes, and verifiable milestones | The checkpoint history in `PROJECT.md`, with links to evidence or preserved historical records |
| Available project conversation text and attachments | `collaboration/mainline-transcripts/`, keeping the visible messages or original export intact |
| Session source, time range, cutoff, attachments, and gaps | `collaboration/ARCHIVE.md`, linked to the saved originals |

Check the project files, existing handoffs, and Git or file history where available. Use them to separate verified progress from plans and earlier guesses. Preserve existing files and exports. Reuse a previously archived source instead of importing the same messages twice. Keep the original wording of user decisions.

Collect visible project conversations from the current client and any other histories the user supplies. Export or copy them as needed. Record inaccessible sessions, incomplete ranges, missing attachments, and old file versions that cannot be recovered. If an old checkpoint can be identified but its original materials are missing, record the checkpoint and the gap together.

### 3. Finish the import and continue

Check that the cited files open and that the current checkpoint, accepted decisions, outstanding work, and next action are clear. Report which sessions were imported and what is still missing. Ask the user to resolve only the gaps that could affect the next step. Verify the resumed project against the existing evidence.

The next assistant can say “Continue from the mainline.” If the user requests independent work, choose that node's participants and freeze its shared materials. Assistants can consult the complete available archive by following its links while starting from the short mainline summary.
