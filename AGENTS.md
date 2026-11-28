# Project collaboration

Follow the user's latest instructions. Read the current-state table in [PROJECT.md](PROJECT.md) before starting a new mainline task. For routine follow-ups on the same task, use the current context. Follow archive links for original evidence as needed.

## Setup and mainline

- Use [onboarding](collaboration/ONBOARDING.md). With checkpoint Git enabled by default, initialize local Git at the project root or reuse its repository. For an old project without Git, initialize at the first verified recovered checkpoint, or at the import baseline if none can be verified. Commit recovered records separately, then save the current baseline. Note missing materials and unverifiable history.
- Save new mainline deliverables under `output/` at the project root unless the user or project specifies a destination. Update the current record when verified progress, a user decision, a blocker, or the next action changes.
- Before sending each completed mainline reply, append a short [session note](collaboration/GUIDE.md#session-notes) from that exchange. Identify the chat without user input. Treat the title as a label. Archive important visible wording once and link it.
- Save all mainline changes to `PROJECT.md` using the [revision-checked save](collaboration/GUIDE.md#save-the-mainline-record). If the helper is unavailable, use one writing session.
- When joining the project, handing off, or returning to the mainline, read `PROJECT.md` including checkpoint history, then use the [handoff procedure](collaboration/GUIDE.md#hand-off-a-discussion) to cover unsummarized relevant sessions. Record open questions, constraints, next actions, and links. A handoff keeps the current checkpoint.
- Add a mainline checkpoint for a verified milestone, a verified merge, or a user request. Record the result and evidence in `PROJECT.md`. Apply the same [local Git rules](collaboration/GUIDE.md#local-git-at-checkpoints) to requested and automatic checkpoints. Respect the project setting and commit the record and verified changes in the project's own repository. A requested checkpoint can commit just the mainline record. Use a message such as `N03 Verify the first report layout` and report the short ID or the reason the commit could not be made. Push only with separate user authorization.

## Independent work

- Branch at the user's request using the [templates](collaboration/templates/). Record the roster in `node.json`. In `BRIEF.md`, freeze the shared task, acceptance checks, file versions, and available dialogue through the source checkpoint. Document gaps before starting and preserve later mainline work.
- Each assistant starts a fresh session and uses the frozen inputs and its own branch. Save the output, submission, and available visible dialogue there, with source coverage and gaps. Verify the result and save the submission before marking it delivered. Use access controls for the shared inputs and each branch when enforced isolation is required.
- Check progress from the roster and status files. Mark substantive follow-ups as supplementing until delivered again. If the shared task, inputs, criteria, or roster change after work starts, freeze a new node. With explicit user approval, restart after preserving prior outputs and archiving old review and decision records.

## Review and merge

- Wait for all selected participants to deliver and the user to open review. The coordinator records the opening in `REVIEW-OPEN.md`. Then review other branches' submissions, artifacts, and available dialogue against the shared criteria.
- After review, the user selects what to adopt and assigns one merge owner. Record the decision in `decision.json`. The owner applies it, verifies the result, writes `FINAL.md`, updates the [archive index](collaboration/ARCHIVE.md), and records the next mainline checkpoint using the local Git rule.
- On “Continue from the mainline,” check relevant unsummarized session notes when taking over, and reread `PROJECT.md`, including in an old branch session.

[Workflow and short prompts](collaboration/GUIDE.md) · [Compatibility](collaboration/COMPATIBILITY.md)
