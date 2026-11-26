# Workflow and prompts

[Project mainline](../PROJECT.md) · [Archive](ARCHIVE.md) · [Templates](templates/) · [Participant examples](PARTICIPANTS.md) · [New and existing project setup](ONBOARDING.md)

## 1. Work on the mainline

Update the current checkpoint as you work. Record a new checkpoint when a meaningful, verified result is ready. An assistant can continue from the saved next action when another assistant runs out of quota. Keep user corrections and decisions traceable to their visible source.

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

| Step | Prompt |
|---|---|
| Initialize | Initialize this project. / 初始化协作。 |
| Import | Import the existing project. / 导入旧项目。 |
| Resume | Continue from the mainline. / 从主线继续。 |
| Prepare | Branch from N03. Invite [participants]. / 从 N03 分岔，请【助手名单】参加。 |
| Work | Complete N03 independently and record your delivery. / 按 N03 独立作答，做完就交付。 |
| Check | Has everyone on the N03 roster delivered? / N03 名单上的助手都交付了吗？ |
| Follow up | Stay independent and add [check]. / 保持独立，补做【事项】。 |
| Review | Open N03 review. Compare the other submissions and evidence. / 开放 N03 互评，请看对方成果和对话。 |
| Decide | Adopt [items] and verify the merge into the mainline. / 采用【方案】，验收后合回主线。 |
