# Workflow and prompts

[Project mainline](../PROJECT.md) · [Archive](ARCHIVE.md) · [Templates](templates/) · [Participant examples](PARTICIPANTS.md) · [New and existing project setup](ONBOARDING.md)

## 1. Work on the mainline

| Situation | Record |
|---|---|
| A question is answered and has no follow-up | Leave the exchange in the conversation. |
| An ongoing discussion could matter later, or the user requests a handoff | Update the discussion handoff in `PROJECT.md`. State the open question, useful findings or constraints, and what to ask next. Link an available source. |
| Verified progress, a decision, blocker, or next action changes | Refresh the current state in `PROJECT.md`. Group small related updates. |
| A verifiable milestone, verified merge, or user-requested checkpoint | Add a mainline checkpoint and apply the local Git rules below. |

Before switching, tell the outgoing assistant “Save this discussion for a handoff.” Tell the incoming assistant “Continue from the mainline and resume our last discussion.” If the old assistant is unavailable, give the new one the relevant excerpt or export and ask it to continue. Save original dialogue when its wording or evidence matters. Unresolved ideas stay in the handoff until the user decides.

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

| When                              | Who                          | English                                                         | 简体中文                         |
| --------------------------------- | ---------------------------- | --------------------------------------------------------------- | -------------------------------- |
| Advance the work                  | Current assistant            | Continue on the mainline and do [task].                         | 继续主线，做【任务】。           |
| Add materials                     | Current assistant            | Use [file] as input for the current task.                       | 把【文件】作为当前任务的材料。   |
| Check progress                    | Current assistant            | What checkpoint are we at, and what is next?                    | 现在到哪个节点了？下一步是什么？ |
| Record a checkpoint               | Current assistant            | Record a mainline checkpoint here.                              | 把这里记为主线节点。             |
| Save an open discussion           | Outgoing assistant           | Save this discussion for a handoff.                             | 记下这段讨论，我要换助手。       |
| Resume or return after merge      | Incoming or branch assistant | Continue from the mainline.                                     | 从主线继续。                     |
| Resume a discussion               | Incoming assistant           | Continue from the mainline and resume our last discussion.      | 从主线继续，接着上次讨论。       |
| Outgoing assistant is unavailable | Incoming assistant           | Continue from the mainline using the earlier messages I pasted. | 从主线继续，结合我贴的旧问答。   |

### Branch, review, and merge

| When                     | Who                       | English                                                                              | 简体中文                                    |
| ------------------------ | ------------------------- | ------------------------------------------------------------------------------------ | ------------------------------------------- |
| Branch from a checkpoint | Mainline assistant        | Branch from N03. Invite [participants] to do [task] independently.                   | 从 N03 分岔，请【助手名单】独立做【任务】。 |
| Start independent work   | Each fresh session        | Work independently on N03 and record your delivery.                                  | 按 N03 独立作答，做完就交付。               |
| Check deliveries         | Coordinator               | Who still needs to deliver for N03?                                                  | N03 谁还没交付？                            |
| Follow up before review  | Selected branch assistant | Stay independent and add [item].                                                     | 保持独立，补做【事项】。                    |
| Open review              | Coordinator               | Open review for N03.                                                                 | 开放 N03 互评。                             |
| Review peers             | Each branch assistant     | Review the other N03 submissions and available dialogue against the shared criteria. | 按 N03 的标准，评审其他分支的成果和对话。   |
| Decide and merge         | Designated merge owner    | For N03, adopt [items], then merge and verify.                                       | N03 采用【方案】，由你合并并验收。          |

### As needed

| When                        | Who                           | English                                                          | 简体中文                              |
| --------------------------- | ----------------------------- | ---------------------------------------------------------------- | ------------------------------------- |
| Archive the exact wording   | Assistant with the original   | Archive this conversation.                                       | 把这段对话原文归档。                  |
| Inspect local versions      | Assistant with project access | Show the last five local Git commits.                            | 看最近 5 次本地 Git 提交。            |
| Turn off checkpoint commits | Current assistant             | Record checkpoints in files only. Disable automatic Git commits. | 这个项目只记节点，关闭自动 Git 提交。 |
