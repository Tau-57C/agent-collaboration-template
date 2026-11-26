import json
from pathlib import Path
from tempfile import TemporaryDirectory, gettempdir
import unittest
from unittest.mock import patch

from tools.check_node import NodeError, inspect_node


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        directory = TemporaryDirectory(prefix="agent-collaboration-test-")
        base = Path(directory.name).resolve()
        self.assertTrue(base.is_relative_to(Path(gettempdir()).resolve()))
        self.addCleanup(directory.cleanup)
        self.node = base / "N03"
        self.write("BRIEF.md", "Use the frozen report and verify the outline.")
        self.members = ["writer", "checker", "third"]
        self.set_roster(self.members)

    def write(self, name, content):
        destination = self.node / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")

    def json_record(self, name, record):
        self.write(name, json.dumps(record))

    def set_roster(self, members):
        self.json_record("node.json", {
            "id": self.node.name,
            "participants": [{"id": member, "label": member.title()} for member in members],
        })

    def status(self, member, value):
        self.json_record(f"branches/{member}/status.json", {"status": value})

    def deliver(self, member):
        self.write(f"branches/{member}/SUBMISSION.md", "Saved candidate and validation result.")
        self.status(member, "delivered")

    def assert_stage(self, expected):
        stage, _ = inspect_node(self.node)
        self.assertEqual(stage, expected)

    def record_reviews(self):
        for member in self.members:
            self.deliver(member)
        self.write("REVIEW-OPEN.md", "User opened review.")
        for member in self.members:
            self.write(f"branches/{member}/REVIEW.md", "Comparison against the common brief.")

    def decision(self, adopted):
        self.json_record("decision.json", {
            "approved_by": "Example user",
            "merge_owner": "writer",
            "adopt": adopted,
            "notes": "Apply the selected headings and run the acceptance checks.",
        })

    def test_three_participants_from_sealing_to_verified_merge(self):
        self.assert_stage("sealed")
        self.status("writer", "working")
        self.assert_stage("independent")
        self.deliver("writer")
        self.deliver("checker")
        self.assert_stage("independent")
        self.deliver("third")
        self.assert_stage("awaiting-user-opening")
        self.write("REVIEW-OPEN.md", "User opened review.")
        self.assert_stage("review")
        for member in self.members:
            self.write(f"branches/{member}/REVIEW.md", "Evidence against the same criteria.")
        self.assert_stage("awaiting-user-decision")
        self.decision(["checker", "third"])
        self.assert_stage("awaiting-merge-verification")
        self.write("FINAL.md", "User-approved artifact verified. Continue at N04.")
        self.assert_stage("merged")

    def test_two_selected_participants_need_no_third(self):
        self.set_roster(["writer", "third"])
        self.deliver("writer")
        self.deliver("third")
        stage, statuses = inspect_node(self.node)
        self.assertEqual(stage, "awaiting-user-opening")
        self.assertEqual(set(statuses), {"writer", "third"})

    def test_distinct_sessions_can_share_a_non_english_label(self):
        self.json_record("node.json", {
            "id": "N03",
            "participants": [
                {"id": "browser-a", "label": "浏览器助手"},
                {"id": "browser-b", "label": "浏览器助手"},
            ],
        })
        self.deliver("browser-a")
        self.assert_stage("independent")
        self.deliver("browser-b")
        self.assert_stage("awaiting-user-opening")

    def test_opening_before_last_delivery_is_rejected(self):
        self.deliver("writer")
        self.deliver("checker")
        self.write("REVIEW-OPEN.md", "Opened too soon.")
        with self.assertRaisesRegex(NodeError, "every selected participant"):
            inspect_node(self.node)

    def test_material_follow_up_closes_readiness(self):
        for member in self.members:
            self.deliver(member)
        self.assert_stage("awaiting-user-opening")
        self.status("checker", "supplementing")
        self.assert_stage("independent")
        self.deliver("checker")
        self.assert_stage("awaiting-user-opening")

    def test_delivered_requires_submission(self):
        self.status("writer", "delivered")
        with self.assertRaisesRegex(NodeError, "SUBMISSION.md"):
            inspect_node(self.node)

    def test_unlisted_branch_is_rejected(self):
        self.status("uninvited", "working")
        with self.assertRaisesRegex(NodeError, "Unlisted branches"):
            inspect_node(self.node)

    def test_duplicate_participant_ids_are_rejected(self):
        self.set_roster(["writer", "writer"])
        with self.assertRaisesRegex(NodeError, "unique"):
            inspect_node(self.node)

    def test_decision_requires_all_reviews(self):
        for member in self.members:
            self.deliver(member)
        self.write("REVIEW-OPEN.md", "User opened review.")
        self.decision(["writer"])
        with self.assertRaisesRegex(NodeError, "participant must record a review"):
            inspect_node(self.node)

    def test_decision_cannot_adopt_unlisted_participant(self):
        self.record_reviews()
        self.decision(["uninvited"])
        with self.assertRaisesRegex(NodeError, "selected participant IDs"):
            inspect_node(self.node)

    def test_final_requires_a_user_decision(self):
        self.record_reviews()
        self.write("FINAL.md", "Recorded prematurely.")
        with self.assertRaisesRegex(NodeError, "recorded user decision"):
            inspect_node(self.node)

    def test_progress_checks_never_read_branch_conversation_or_candidate(self):
        self.deliver("writer")
        self.write("branches/writer/TRANSCRIPT.md", "Independent conversation.")
        with patch.object(Path, "read_text", autospec=True, side_effect=Path.read_text) as read:
            self.assert_stage("independent")
        self.assertEqual({call.args[0].name for call in read.call_args_list}, {"node.json", "status.json"})


if __name__ == "__main__":
    unittest.main()
