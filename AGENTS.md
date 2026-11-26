# Project collaboration

Follow the user's latest project instructions. On joining, switching assistants, or returning from a branch, read [PROJECT.md](PROJECT.md) for the current checkpoint, decisions, discussion handoff, and next action. Follow archive links when the original evidence matters.

## Setup and mainline

- Follow [project onboarding](collaboration/ONBOARDING.md). With the default checkpoint Git setting, initialize local Git at the project root during new-project setup. Reuse an existing repository at that root. For an existing project with no repository, initialize Git when writing the first verified historical checkpoint, or when recording the current import baseline if no earlier checkpoint can be verified. Commit each recovered record separately, then save the current baseline. Keep unverifiable history and missing materials visible as gaps.
- Update the current mainline record when verified progress, a user decision, a blocker, or the next action changes. Briefly update the discussion handoff when an unresolved question will matter to the next assistant or the user asks to switch. Record the question, useful findings or constraints, the next question, and any available source link. Keep routine exchanges in the conversation. A handoff stays at the current checkpoint.
- Record a new mainline checkpoint for a verified milestone, a verified merge, or a checkpoint the user requests. Write the result and its evidence in `PROJECT.md`. Use the same [local Git rules](collaboration/GUIDE.md#local-git-at-checkpoints) for automatic and requested checkpoints. Commit the verified changes and mainline record with a message such as `N03 Verify the first report layout`. A requested checkpoint may contain only the mainline record. Respect the project setting and use the project's own repository. Tell the user the short commit ID or why the commit could not be made. Pushing requires separate user authorization.

## Independent work

- Branch when the user requests it. Prepare a node using [the templates](collaboration/templates/). Record the selected participants in `node.json` and freeze the common task, acceptance checks, file versions, and available conversation through the chosen checkpoint in `BRIEF.md`. Keep later mainline work in place. Document material gaps before starting.
- Use a fresh session, the frozen inputs, and your own branch. Keep the output, submission, and available visible dialogue in that branch. Record source coverage and gaps. Verify the result, save the submission, and mark it delivered as part of finishing the task. Where enforced isolation is required, use access controls for the shared inputs and each branch.
- Check progress using the roster and status files. Mark substantive follow-ups as supplementing until delivered again. If the common task, inputs, criteria, or roster changes after work starts, freeze a fresh node. The user may explicitly restart the round after preserving prior outputs and archiving the old review and decision records.

## Review and merge

- Wait until every selected participant has delivered and the user opens review. The coordinator records the opening in `REVIEW-OPEN.md`. Participants can then review other branches' submissions, artifacts, and available dialogue against the shared criteria.
- The user decides what to adopt and picks one merge owner. Record the decision in `decision.json`. The owner applies it, verifies the result, writes `FINAL.md`, updates the [archive index](collaboration/ARCHIVE.md), and records the next mainline checkpoint. Apply the local Git rule at that checkpoint.
- On “Continue from the mainline,” reread `PROJECT.md`, including in an old branch session.

[Workflow and short prompts](collaboration/GUIDE.md) · [Compatibility](collaboration/COMPATIBILITY.md)
