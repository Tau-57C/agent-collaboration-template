# Project collaboration

Follow the user's latest instructions. On joining, switching assistants, or returning from a branch, read [PROJECT.md](PROJECT.md) for the current checkpoint, decisions, discussion handoff, and next action. Follow archive links for original evidence as needed.

## Setup and mainline

- Use [onboarding](collaboration/ONBOARDING.md). With checkpoint Git enabled by default, initialize local Git at the project root or reuse its repository. For an old project without Git, initialize at the first verified recovered checkpoint, or at the import baseline if none can be verified. Commit recovered records separately, then save the current baseline. Note missing materials and unverifiable history.
- Save new mainline deliverable files under `output/` at the project root unless the user or project specifies a destination. Update the current record when verified progress, a user decision, a blocker, or the next action changes. Keep routine exchanges in the chat.
- In the discussion handoff, briefly record the question, findings or constraints, and next question when the user asks to switch or the unresolved issue matters to the next assistant. Link available sources. A handoff keeps the current checkpoint.
- Add a mainline checkpoint for a verified milestone, a verified merge, or a user request. Record the result and evidence in `PROJECT.md`. Apply the same [local Git rules](collaboration/GUIDE.md#local-git-at-checkpoints) to requested and automatic checkpoints. Respect the project setting and commit the record and verified changes in the project's own repository. A requested checkpoint can commit just the mainline record. Use a message such as `N03 Verify the first report layout` and report the short ID or the reason the commit could not be made. Push only with separate user authorization.

## Independent work

- Branch at the user's request using the [templates](collaboration/templates/). Record the roster in `node.json`. In `BRIEF.md`, freeze the shared task, acceptance checks, file versions, and available dialogue through the source checkpoint. Document gaps before starting and preserve later mainline work.
- Each assistant starts a fresh session and uses the frozen inputs and its own branch. Save the output, submission, and available visible dialogue there, with source coverage and gaps. Verify the result and save the submission before marking it delivered. Use access controls for the shared inputs and each branch when enforced isolation is required.
- Check progress from the roster and status files. Mark substantive follow-ups as supplementing until delivered again. If the shared task, inputs, criteria, or roster change after work starts, freeze a new node. With explicit user approval, restart after preserving prior outputs and archiving old review and decision records.

## Review and merge

- Wait for all selected participants to deliver and the user to open review. The coordinator records the opening in `REVIEW-OPEN.md`. Then review other branches' submissions, artifacts, and available dialogue against the shared criteria.
- After review, the user selects what to adopt and assigns one merge owner. Record the decision in `decision.json`. The owner applies it, verifies the result, writes `FINAL.md`, updates the [archive index](collaboration/ARCHIVE.md), and records the next mainline checkpoint using the local Git rule.
- On “Continue from the mainline,” reread `PROJECT.md`, including in an old branch session.

[Workflow and short prompts](collaboration/GUIDE.md) · [Compatibility](collaboration/COMPATIBILITY.md)
