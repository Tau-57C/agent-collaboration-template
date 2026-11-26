# Project collaboration

Follow the user's latest project instructions. Start with [PROJECT.md](PROJECT.md) when joining or returning to the mainline. Read the current checkpoint, accepted decisions, and next action. Record a checkpoint for each verified milestone. For routine progress, blockers, or handoffs, update the current checkpoint.

When the user asks to initialize a new project or import an existing one, follow [project onboarding](collaboration/ONBOARDING.md). For an existing project, complete the history import before starting independent collaboration.

## Independent work

- Branch when the user requests it. Prepare a node using [the templates](collaboration/templates/). Record the selected participants in `node.json` and freeze the common task, acceptance checks, file versions, and available conversation through the chosen checkpoint in `BRIEF.md`. Keep any newer mainline work in place. Document material gaps before starting.
- In an independent session, use the frozen inputs and your own branch. Read project evidence on demand. Work on the same inputs in parallel or in sequence. Keep your output, submission, and visible transcript export in your branch. Record the transcript's range and any gaps. Complete required checks and save the submission before marking your branch delivered.
- The roster belongs to the node. Use the selected participants for progress and review gates. Follow-up questions may extend a branch. Mark substantive follow-ups as in progress until delivered again. If the common task, inputs, criteria, or roster changes after work starts, freeze a fresh node, or have the user explicitly restart the round after archiving the previous outputs and clearing its review/decision records.

## Review and merge

- During progress checks, inspect the roster and status files. When every selected participant has delivered, wait for the user's opening instruction. The coordinator records that instruction in `REVIEW-OPEN.md`. Participants can then inspect each other's submissions, artifacts, and available visible transcript files and write reviews against the shared criteria.
- The user makes the final decision and picks one merge owner. Record it in `decision.json` after the required reviews. The owner applies the approved changes, verifies the result, and writes `FINAL.md`. Record the next mainline checkpoint and update the [archive index](collaboration/ARCHIVE.md).
- On “Continue from the mainline,” reread `PROJECT.md`, even in an old branch session. The archive points to original records by path so that an assistant can look up the relevant material.

[Workflow and short prompts](collaboration/GUIDE.md) · [Compatibility](collaboration/COMPATIBILITY.md)
