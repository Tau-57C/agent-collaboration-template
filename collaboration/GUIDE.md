# Workflow and prompts

[Project mainline](../PROJECT.md) · [Archive](ARCHIVE.md) · [Templates](templates/) · [Participant examples](PARTICIPANTS.md) · [New and existing project setup](ONBOARDING.md)

## 1. Work on the mainline

| Situation | Record |
|---|---|
| The assistant completes a mainline reply | Append one short session note before sending, even if related user messages were answered together. |
| An ongoing discussion could matter later, or the user requests a handoff | Update the discussion handoff in `PROJECT.md`. State the open question, useful findings or constraints, and what to ask next. Link an available source. |
| Verified progress, a decision, blocker, or next action changes | Refresh the current state in `PROJECT.md`. Group small related updates. |
| Starting a new mainline task | Read the current-state table in `PROJECT.md` first. Reuse context for routine follow-ups on the same task. |
| A verifiable milestone, verified merge, or user-requested checkpoint | Add a mainline checkpoint and apply the local Git rules below. |

For “List all checkpoints,” use the history in `PROJECT.md` and independent node records under `collaboration/nodes/`. List IDs, types, and known stages in ID order. Mark the current mainline checkpoint and follow existing access rules.

### Session notes

- Save mainline notes in `collaboration/mainline-notes/` under a stable, unique name. When a durable client session ID is available, record it with the client name in the note and use it to recover the file. Otherwise reuse the note path previously recorded in this chat. When creating a note without a client session ID, include its link once in this chat so the assistant can recover the path in a later reply.
- Use the visible title or discussion topic as the heading and update it when a new title is available. If no session ID or previous link identifies the note, start a new note and retain the older notes for handoff. Do not match by title or require the user to recall a name, ID, or path.
- Append a numbered line stating the topic and outcome or open issue. Use the current exchange and the end of the note. Preserve selected visible wording in the [archive](ARCHIVE.md) when a decision, constraint, or evidence needs exact wording. Link to an existing copy when available.
- During an independent round, keep any branch session notes with that branch under its access rules.

### Hand off a discussion

1. Tell the incoming assistant “Continue from the mainline.” If the outgoing assistant has details that are still missing, you can first say “Save open discussions for handoff.” The assistant handling the handoff finds the relevant mainline notes in the project. For a general handoff, check all mainline notes for entries still to cover. If the user names a task, use that scope. When the outgoing assistant is unavailable, the incoming assistant follows these same steps. Note any known missing source.
2. Read `PROJECT.md`, including checkpoint history. List the note paths and check their headings and latest entry numbers against the “Session notes covered” table. For relevant notes, read entries after the recorded number. Start at the first entry if the file has no prior coverage. Follow original material links as needed.
3. Update the current state and discussion handoff. Consolidate repeated points across notes and link their sources. Keep other active discussions and label handoff items by topic. Advance each file’s coverage only through the last entry actually accounted for. Keep the coverage record after a discussion ends.
4. To resume a specific discussion, say “Continue from the mainline on [topic].” If key details are missing, share excerpts or exports you have. For pasted excerpts, say “Continue from the mainline using these excerpts.” Unresolved ideas stay in the handoff until the user decides.

### Save the mainline record

Every mainline session uses this save procedure to update `PROJECT.md`, including during setup, handoff, and checkpoint creation. It uses Python 3.11 or later. Run from the project root.

1. Run `python collaboration/update_project.py read` before drafting the update. Save the revision printed on the first line and use the Markdown that follows as the base.
2. Put the complete updated Markdown in a private temporary UTF-8 file. Preserve changes and notes from other sessions in that base. Run `python collaboration/update_project.py apply REVISION DRAFT_PATH` with the revision from step 1.
3. An overlapping save can hold the write lock briefly. If the command returns 3, retry with the same revision and draft. If it returns 2, read again and merge the intended changes with the latest record before retrying. If two updates disagree on a decision or a checkpoint, resolve the discrepancy before saving. Advance note coverage only for entries actually included.
4. Wait for a successful save before reporting the mainline update or proceeding to its checkpoint commit. When the helper cannot run, have one session write back and let the others save their session notes.

### Local Git at checkpoints

1. At setup, use the project root and its own repository. [New projects](ONBOARDING.md#new-project) initialize Git during collaboration setup. [Existing projects without Git](ONBOARDING.md#existing-project) record recovered checkpoints one at a time and preserve the current baseline separately. To use files only, set “Checkpoint Git” to “Files only” in `PROJECT.md`.
2. With checkpoint Git enabled, commit once for each new mainline checkpoint, whether the assistant created it at a verified milestone or the user requested it. Save the mainline record and only verified changes in scope. A manual checkpoint can commit just `PROJECT.md`. Preserve existing staged changes. If related and unrelated changes cannot be separated safely, record the problem and leave the commit pending.
3. Use a message like `N03 Verify first report layout`. Record the message in the checkpoint and report the resulting short ID. If a commit fails or no changes are eligible, preserve the checkpoint and state why. Before retrying, look for an existing commit for that checkpoint.
4. Conversation exports and independent branch material remain in their archive paths. Discussions, handoffs, and independent deliveries stay at the current mainline checkpoint. Git operations stop at local commits. A push needs a separate request.

## 2. Prepare an independent round

Choose the source checkpoint. When revisiting an older checkpoint, give the new round its own node ID and cite that checkpoint as the source. Later mainline work stays available. Copy the relevant templates, then record only the assistants invited to this round in `node.json`. Each entry has a stable lowercase ID such as `codex-a` and a human-readable `label`. The label can be any client or model name. Two sessions in the same client use separate IDs. The list for one node can differ from the next.

Freeze the brief and the inputs that both or all participants may use. Preserve the user’s acceptance criteria, saved file versions, and available visible dialogue through the source checkpoint. Link to fixed copies or immutable references. If coverage is incomplete, record the missing period and resolve any gap that could change the result.

```text
collaboration/nodes/N03/
  node.json                  selected participants
  BRIEF.md                   task, inputs, conversation cutoff, checks
  branches/
    <participant-id>/
      status.json            status only
      SUBMISSION.md          result, evidence, links, incomplete items
      TRANSCRIPT.md          visible conversation, or link to a readable export
      REVIEW.md              created after the user opens review
      artifacts/             optional branch outputs
  REVIEW-OPEN.md             recorded user instruction to open review
  decision.json              user-approved changes and one merge owner
  FINAL.md                   verification and next mainline checkpoint
```

One session per participant can work in parallel or sequentially. During independent work, use only the common materials and the participant's own workspace. Progress reads need only the roster and status files. A scope rule governs agent behavior. Where enforced isolation is required, give each session access only to its own workspace and the shared read-only inputs.

Each participant saves work locally and updates `status.json`. Valid statuses are `working`, `blocked`, `supplementing`, and `delivered`. An absent file means that the participant has not started. Set `delivered` after validating the requested work and writing the submission. Participants can consult actual transcript files only if their client can read the files. Record what is missing and use the application's export function or copy the visible text when needed.

## 3. Open review and merge

When every roster member has delivered, tell the coordinator to open review. The coordinator saves the user's instruction in `REVIEW-OPEN.md`. Each participant reviews the other candidates against the shared criteria and cites evidence from the artifacts or visible dialogue. If a follow-up would affect delivered results, either hold review until the affected work is resubmitted or explicitly open a new round. Once review has opened, independent reassessment requires fresh sessions and a brief that excludes candidate outputs.

When reviews are ready, the user selects what to adopt and picks a single merge owner. The owner records the decision, applies the approved changes, verifies the outcome, and writes `FINAL.md`. Update the project mainline and link the branch records in the archive. The optional checker shows the derived stage from these files. The checker validates records and dependencies. Human instructions still govern when reading, review, and merging are authorized.

## Copyable prompts

Replace N03 with the actual node. To try again from an earlier checkpoint, put that checkpoint in the branch prompt. Start one new session per participant. When all selected participants deliver, ask the coordinator to open review, then ask each branch to review the others.

### Set up

| When             | Who                 | English                      | 简体中文     |
| ---------------- | ------------------- | ---------------------------- | ------------ |
| New project      | Project assistant   | Initialize collaboration.    | 初始化协作。 |
| Existing project | Importing assistant | Import the existing project. | 导入旧项目。 |

### Mainline and handoff

For a new mainline task, the assistant first reads the current-state table. When switching chats or catching up on session notes, say “Continue from the mainline and do [task].”

| When                              | Who                          | English                                                         | 简体中文                         |
| --------------------------------- | ---------------------------- | --------------------------------------------------------------- | -------------------------------- |
| Switch sessions or resume after merge | Next mainline session | Continue from the mainline. | 从主线继续。 |
| Advance the work                  | Current assistant            | Continue on the mainline and do [task].                         | 继续主线，做【任务】。           |
| Add materials                     | Current assistant            | Use [file] as input for the current task.                       | 把【文件】作为当前任务的材料。   |
| Check progress                    | Current assistant            | What’s the current checkpoint and next step?                    | 当前节点和下一步是什么？         |
| List all checkpoints              | Current assistant            | List all checkpoints.                                           | 列出所有节点。                   |
| Record a checkpoint               | Current assistant            | Record a mainline checkpoint here.                              | 把这里记为主线节点。             |
| Prepare a handoff (optional)      | Outgoing assistant           | Save open discussions for handoff.                              | 记下待续讨论，我要换助手。       |
| Resume a specific topic           | Incoming assistant           | Continue from the mainline on [topic].                          | 从主线继续，接着聊【主题】。     |
| Supply missing chat excerpts      | Incoming assistant           | Continue from the mainline using these excerpts.                | 从主线继续，参考我贴的旧问答。   |

### Branch, review, and merge

| When                     | Who                       | English                                                                              | 简体中文                                    |
| ------------------------ | ------------------------- | ------------------------------------------------------------------------------------ | ------------------------------------------- |
| Branch from a checkpoint | Mainline assistant        | Branch from N03. Invite [participants] to do [task] independently.                   | 从 N03 分岔，请【助手名单】独立做【任务】。 |
| Start independent work   | Each fresh session        | Work independently on N03, then record delivery.                                     | 按 N03 独立做，完成后交付。                 |
| Check deliveries         | Coordinator               | Who still needs to deliver for N03?                                                  | N03 谁还没交付？                            |
| Follow up before review  | Selected branch assistant | Stay independent and add [item].                                                     | 保持独立，补做【事项】。                    |
| Open review              | Coordinator               | Open review for N03.                                                                 | 开放 N03 互评。                             |
| Review peers             | Each branch assistant     | Review other branches’ work and dialogue using N03 criteria.                         | 按 N03 标准评审其他分支的成果和对话。       |
| Decide and merge         | Designated merge owner    | For N03, adopt [items], then merge and verify.                                       | N03 采用【方案】，由你合并并验收。          |

### As needed

| When                        | Who                           | English                                                          | 简体中文                              |
| --------------------------- | ----------------------------- | ---------------------------------------------------------------- | ------------------------------------- |
| Archive the exact wording   | Assistant with the original   | Archive this excerpt verbatim.                                   | 归档这段对话原文。                    |
| Inspect local versions      | Assistant with project access | Show the last five local Git commits.                            | 看最近 5 次本地 Git 提交。            |
| Turn off checkpoint commits | Current assistant             | Record checkpoints in files only. Disable automatic Git commits. | 这个项目只记节点，关闭自动 Git 提交。 |
