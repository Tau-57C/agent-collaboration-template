"""Check collaboration records without reading any candidate's conversation or output."""

import argparse
import json
from pathlib import Path
import re
import sys


NODE_ID = re.compile(r"N[0-9]{2,}")
PARTICIPANT_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
STATUSES = {"working", "blocked", "supplementing", "delivered"}


class NodeError(ValueError):
    """A record is missing, malformed, or out of order."""


def read_object(path):
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise NodeError(f"{path.name}: {error}") from error
    if not isinstance(record, dict):
        raise NodeError(f"{path.name}: expected a JSON object")
    return record


def text_present(path, node):
    if not path.exists():
        return False
    if not path.resolve().is_relative_to(node) or not path.is_file():
        raise NodeError(f"Expected a local file: {path.relative_to(node)}")
    return path.stat().st_size > 0


def roster(record, node):
    node_id = record.get("id")
    if not isinstance(node_id, str) or not NODE_ID.fullmatch(node_id) or node_id != node.name:
        raise NodeError("node.json: id must match the node folder, for example N03")
    members = record.get("participants")
    if not isinstance(members, list) or len(members) < 2:
        raise NodeError("node.json: select at least two participants for an independent round")
    participant_ids = []
    for member in members:
        if not isinstance(member, dict):
            raise NodeError("node.json: each participant needs an id and a label")
        participant_id = member.get("id")
        label = member.get("label")
        if not isinstance(participant_id, str) or not PARTICIPANT_ID.fullmatch(participant_id):
            raise NodeError("node.json: participant IDs must use lowercase letters, digits, and hyphens")
        if not isinstance(label, str) or not label.strip():
            raise NodeError(f"node.json: {participant_id} needs a readable label")
        participant_ids.append(participant_id)
    if len(set(participant_ids)) != len(participant_ids):
        raise NodeError("node.json: participant IDs must be unique")
    return participant_ids


def branch_status(branch, node):
    path = branch / "status.json"
    if not path.exists():
        return "not-started"
    if not text_present(path, node):
        raise NodeError(f"{branch.name}: status.json is empty")
    status = read_object(path).get("status")
    if not isinstance(status, str) or status not in STATUSES:
        raise NodeError(f"{branch.name}: invalid branch status")
    if status == "delivered" and not text_present(branch / "SUBMISSION.md", node):
        raise NodeError(f"{branch.name}: delivered requires a saved SUBMISSION.md")
    return status


def check_decision(path, selected):
    decision = read_object(path)
    for key in ("approved_by", "merge_owner", "notes"):
        value = decision.get(key)
        if not isinstance(value, str) or not value.strip():
            raise NodeError(f"decision.json: {key} is required")
    adopted = decision.get("adopt")
    if not isinstance(adopted, list) or any(
        not isinstance(member, str) or member not in selected for member in adopted
    ):
        raise NodeError("decision.json: adopt must list selected participant IDs")
    if len(set(adopted)) != len(adopted):
        raise NodeError("decision.json: adopt contains duplicate participant IDs")


def inspect_node(folder):
    """Return the derived stage and selected statuses, or raise NodeError."""
    node = Path(folder).resolve()
    roster_path = node / "node.json"
    if not text_present(roster_path, node):
        raise NodeError("Missing or empty node.json")
    selected = roster(read_object(roster_path), node)
    if not text_present(node / "BRIEF.md", node):
        raise NodeError("Missing or empty BRIEF.md")

    branch_root = node / "branches"
    if branch_root.exists():
        if not branch_root.is_dir() or not branch_root.resolve().is_relative_to(node):
            raise NodeError("Expected a local branches directory")
        unexpected = {entry.name for entry in branch_root.iterdir() if entry.is_dir()} - set(selected)
        if unexpected:
            raise NodeError(f"Unlisted branches: {', '.join(sorted(unexpected))}")

    statuses = {member: branch_status(branch_root / member, node) for member in selected}
    opened = text_present(node / "REVIEW-OPEN.md", node)
    reviewed = {
        member for member in selected
        if text_present(branch_root / member / "REVIEW.md", node)
    }
    decision_path = node / "decision.json"
    has_decision = text_present(decision_path, node)
    has_final = text_present(node / "FINAL.md", node)
    delivered = all(status == "delivered" for status in statuses.values())

    if not delivered and (opened or reviewed or has_decision or has_final):
        raise NodeError("Review and merge records require delivery from every selected participant")
    if not opened and (reviewed or has_decision or has_final):
        raise NodeError("Save the user's review opening before recording reviews or merge decisions")
    if len(reviewed) != len(selected) and (has_decision or has_final):
        raise NodeError("Each selected participant must record a review before the decision")
    if has_final and not has_decision:
        raise NodeError("A verified merge requires a recorded user decision")
    if has_decision:
        check_decision(decision_path, set(selected))

    if has_final:
        stage = "merged"
    elif has_decision:
        stage = "awaiting-merge-verification"
    elif reviewed == set(selected):
        stage = "awaiting-user-decision"
    elif opened:
        stage = "review"
    elif delivered:
        stage = "awaiting-user-opening"
    elif any(status != "not-started" for status in statuses.values()):
        stage = "independent"
    else:
        stage = "sealed"

    return stage, statuses


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("node", type=Path, help="Path to a node directory, such as collaboration/nodes/N03")
    options = parser.parse_args()
    try:
        stage, statuses = inspect_node(options.node)
    except (NodeError, OSError) as error:
        print(f"Invalid node: {error}", file=sys.stderr)
        return 1
    print(f"Stage: {stage}")
    for participant, status in statuses.items():
        print(f"{participant}: {status}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
