"""Behavior tests through the spawn audit command's JSON/exit-status boundary."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


PLUGIN = Path(__file__).resolve().parents[1]
COMMAND = PLUGIN / "scripts" / "spawn-audit.py"
FIXTURES = Path(__file__).parent / "fixtures" / "session-records"


class SpawnAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "sessions"
        shutil.copytree(FIXTURES, self.root)
        self.request = {
            "start_time": "2026-09-14T07:43:00Z",
            "cwd": "/tmp/disposable-repo",
            "parent_thread_id": "parent",
            "records_root": str(self.root),
            "planned_subagents": [
                {"task_name": "smoke_a", "requested_model": "gpt-5.6-luna",
                 "requested_effort": "low"},
                {"task_name": "smoke_b", "requested_model": "gpt-5.6-luna",
                 "requested_effort": "low"},
            ],
        }

    def run_command(self, request=None, raw=None, env=None):
        environment = os.environ.copy()
        environment.pop("CODEX_THREAD_ID", None)
        if env:
            environment.update(env)
        return subprocess.run(
            [sys.executable, str(COMMAND)],
            input=raw if raw is not None else json.dumps(request or self.request),
            text=True, capture_output=True, env=environment, timeout=10,
        )

    def audit(self):
        result = self.run_command()
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def read_records(self, name):
        return [json.loads(line) for line in (self.root / name).read_text().splitlines()]

    def write_records(self, name, records):
        (self.root / name).write_text("".join(json.dumps(row) + "\n" for row in records))

    def use_issue14_seed(self):
        shutil.rmtree(self.root)
        shutil.copytree(FIXTURES.parent / "issue-14", self.root)
        self.request.update(
            start_time="2026-09-16T03:45:02Z",
            cwd="/tmp/codex-issue14-74o2zfxo/repair",
            parent_thread_id="01a0a851-0923-7893-8c0c-dcb4a2863055",
            planned_subagents=[
                {"task_name": "repair_invalid_input", "requested_model": "gpt-5.6-luna",
                 "requested_effort": "medium"},
                {"task_name": "review_invalid_input", "requested_model": "gpt-5.6-terra",
                 "requested_effort": "high"},
            ],
        )

    def test_parent_turn_open_at_start_is_reported_even_when_it_ends_later(self):
        self.use_issue14_seed()
        report = self.audit()
        self.assertEqual(report["parent"]["status"], "observable")
        self.assertEqual([(turn["timestamp"], turn["model"], turn["effort"], turn["line"])
                          for turn in report["parent"]["turns"]],
                         [("2026-09-16T03:44:43.375Z", "gpt-6-astra", "high", 3)])
        self.assertIs(report["parent_ran_at_ultra"], False)
        self.assertEqual([task["status"] for task in report["planned_subagents"]],
                         ["confirmed", "confirmed"])
        self.assertEqual(report["record_errors"], [])

    def test_unestablished_start_turn_keeps_readable_later_turns_but_ultra_unknown(self):
        self.use_issue14_seed()
        rows = self.read_records("parent.jsonl")
        later = json.loads(json.dumps(rows[2]))
        later["timestamp"] = "2026-09-16T03:46:00Z"
        later["payload"]["turn_id"] = "later-turn"
        self.write_records("parent.jsonl", [rows[0], rows[2], later])
        report = self.audit()
        self.assertEqual(report["parent"]["status"], "unobservable")
        self.assertEqual(report["parent"]["reason"], "Cannot establish the Parent turn open at run start")
        self.assertEqual([t["turn_id"] for t in report["parent"]["turns"]], ["later-turn"])
        self.assertIsNone(report["parent_ran_at_ultra"])

    def test_ultra_start_turn_counts_before_a_later_spawning_turn(self):
        self.use_issue14_seed()
        rows = self.read_records("parent.jsonl")
        rows[2]["payload"]["effort"] = "ultra"
        for multi_turn in (False, True):
            with self.subTest(multi_turn=multi_turn):
                if multi_turn:
                    rows[3]["timestamp"] = "2026-09-16T03:45:10Z"
                    later = json.loads(json.dumps(rows[1:]))
                    for row in later:
                        row["payload"]["turn_id"] = "spawning-turn"
                    later[0]["timestamp"] = "2026-09-16T03:45:20Z"
                    later[1]["timestamp"] = "2026-09-16T03:45:21Z"
                    later[1]["payload"]["effort"] = "high"
                    later[2]["timestamp"] = "2026-09-16T03:51:00Z"
                    rows += later
                self.write_records("parent.jsonl", rows)
                report = self.audit()
                self.assertEqual(report["parent"]["status"], "observable")
                self.assertEqual([t["effort"] for t in report["parent"]["turns"]],
                                 ["ultra", "high"] if multi_turn else ["ultra"])
                self.assertIs(report["parent_ran_at_ultra"], True)

    def test_ended_or_aborted_historical_turn_does_not_count(self):
        self.use_issue14_seed()
        rows = self.read_records("parent.jsonl")
        rows[2]["payload"]["effort"] = "ultra"
        later = json.loads(json.dumps(rows[2]))
        later["timestamp"] = "2026-09-16T03:46:00Z"
        later["payload"].update(turn_id="later-turn", effort="high")
        for end_kind in ("task_complete", "turn_aborted"):
            for end_time in ("2026-09-16T03:45:01Z", self.request["start_time"]):
                with self.subTest(end_kind=end_kind, end_time=end_time):
                    rows[3]["timestamp"] = end_time
                    rows[3]["payload"]["type"] = end_kind
                    self.write_records("parent.jsonl", rows + [later])
                    report = self.audit()
                    self.assertEqual(report["parent"]["status"], "observable")
                    self.assertEqual([t["turn_id"] for t in report["parent"]["turns"]], ["later-turn"])
                    self.assertIs(report["parent_ran_at_ultra"], False)

    def test_start_turn_contexts_are_collected_by_turn_id(self):
        self.use_issue14_seed()
        rows = self.read_records("parent.jsonl")
        compacted = json.loads(json.dumps(rows[2]))
        compacted["timestamp"] = "2026-09-16T03:47:00Z"
        self.write_records("parent.jsonl", rows[:3] + [compacted, rows[3]])
        report = self.audit()
        self.assertEqual(report["parent"]["status"], "observable")
        self.assertEqual([t["line"] for t in report["parent"]["turns"]], [3, 4])
        self.assertEqual(len({t["turn_id"] for t in report["parent"]["turns"]}), 1)

    def test_start_turn_is_selected_by_start_event_not_context_order(self):
        self.use_issue14_seed()
        rows = self.read_records("parent.jsonl")
        historical = json.loads(json.dumps(rows[1:]))
        for row in historical:
            row["payload"]["turn_id"] = "historical-turn"
        historical[0]["timestamp"] = "2026-09-16T03:44:38.331Z"
        historical[1]["timestamp"] = "2026-09-16T03:44:38.331Z"
        historical[2]["timestamp"] = "2026-09-16T03:44:38.331Z"
        repeated = json.loads(json.dumps(historical[1]))
        repeated["timestamp"] = "2026-09-16T03:45:01Z"
        rows[2]["payload"]["effort"] = "ultra"
        self.write_records("parent.jsonl", [rows[0]] + historical + rows[1:3] + [repeated, rows[3]])
        report = self.audit()
        self.assertEqual(report["parent"]["status"], "observable")
        self.assertEqual([t["effort"] for t in report["parent"]["turns"]], ["ultra"])
        self.assertIs(report["parent_ran_at_ultra"], True)

    def test_unestablished_start_does_not_hide_readable_ultra_later(self):
        self.use_issue14_seed()
        rows = self.read_records("parent.jsonl")
        later = json.loads(json.dumps(rows[2]))
        later["timestamp"] = "2026-09-16T03:46:00Z"
        later["payload"].update(turn_id="later-turn", effort="ultra")
        self.write_records("parent.jsonl", [rows[0], rows[2], later])
        report = self.audit()
        self.assertEqual(report["parent"]["status"], "unobservable")
        self.assertIs(report["parent_ran_at_ultra"], True)

    def test_missing_ambiguous_and_empty_parent_records_have_distinct_reasons(self):
        self.use_issue14_seed()
        rows = self.read_records("parent.jsonl")
        self.write_records("duplicate_parent.jsonl", rows)
        self.assertEqual(self.audit()["parent"]["reason"], "No unique Parent session record")
        (self.root / "duplicate_parent.jsonl").unlink()
        (self.root / "parent.jsonl").unlink()
        self.assertEqual(self.audit()["parent"]["reason"], "No unique Parent session record")
        self.write_records("parent.jsonl", rows[:1])
        self.assertEqual(self.audit()["parent"]["reason"], "No readable Parent turn in the run")

    def test_mismatch_on_followup_preserves_both_realized_settings(self):
        rows = self.read_records("smoke_a.jsonl")
        rows[-1]["payload"].update(model="gpt-6-astra", effort="high")
        self.write_records("smoke_a.jsonl", rows)
        task = self.audit()["planned_subagents"][0]
        self.assertEqual(task["status"], "mismatch")
        self.assertIsNone(task["realized_model"])
        self.assertIsNone(task["realized_effort"])
        self.assertEqual([(turn["model"], turn["effort"]) for turn in task["evidence"]],
                         [("gpt-5.6-luna", "low"), ("gpt-6-astra", "high")])

    def test_missing_records_are_unobservable_with_reasons(self):
        shutil.rmtree(self.root)
        report = self.audit()
        for task in report["planned_subagents"]:
            self.assertEqual(task["status"], "unobservable")
            self.assertTrue(task["reason"])
            self.assertIsNone(task["realized_model"])
        self.assertEqual(report["parent"]["status"], "unobservable")
        self.assertTrue(report["parent"]["reason"])
        self.assertIsNone(report["parent_ran_at_ultra"])
        self.assertTrue(report["record_errors"])

    def test_unreadable_or_malformed_record_never_confirms_settings(self):
        path = self.root / "smoke_a.jsonl"
        original = path.read_text()
        cases = ["", "{broken", "[]\n", '{"type":"session_meta","payload":[]}\n',
                 original.splitlines()[0] + "\n{truncated", original + "null\n",
                 original.replace('"effort": "low"', '"effort": null'),
                 original.replace('2026-09-14T07:44:24.484Z', 'not-a-time')]
        for content in cases:
            with self.subTest(content=content[:80]):
                path.write_text(content)
                report = self.audit()
                self.assertEqual(report["planned_subagents"][0]["status"], "unobservable")
                self.assertTrue(report["planned_subagents"][0]["reason"])
                self.assertEqual(report["planned_subagents"][1]["status"], "confirmed")
                self.assertTrue(report["record_errors"])
        path.unlink()
        path.symlink_to(self.root / "does-not-exist")
        self.assertEqual(self.audit()["planned_subagents"][0]["status"], "unobservable")

    def test_embedded_parent_history_is_not_subagent_evidence(self):
        self.request.update(start_time="2026-09-12T16:55:00Z",
                            cwd="/workspace/other-repo", parent_thread_id="parent-historical")
        self.request["planned_subagents"] = [
            {"task_name": "review_spec", "requested_model": "gpt-6-astra", "requested_effort": "high"}]
        task = self.audit()["planned_subagents"][0]
        self.assertEqual(task["status"], "unobservable")
        self.assertIn("inherited", task["reason"].lower())
        self.assertEqual(task["evidence"], [])
        self.assertEqual(self.audit()["parent"]["turns"], [])

    def test_parent_can_be_inferred_from_unique_matching_subagents(self):
        del self.request["parent_thread_id"]
        report = self.audit()
        self.assertEqual(report["parent"]["thread_id"], "parent")
        self.assertEqual(report["planned_subagents"][0]["status"], "confirmed")

    def test_unplanned_subagents_and_host_guardian_are_reported_separately(self):
        self.request["planned_subagents"].pop()
        guardian = self.read_records("smoke_b.jsonl")
        guardian[0]["payload"].update(id="guardian", agent_path=None,
                                      thread_source="guardian_review",
                                      source={"subagent": {"other": "guardian"}})
        guardian[1]["payload"].update(model="codex-auto-review", effort="low")
        self.write_records("guardian.jsonl", guardian)
        report = self.audit()
        self.assertEqual([item["agent_path"] for item in report["unplanned_subagents"]],
                         ["/root/smoke_b"])
        self.assertEqual(report["unplanned_subagents"][0]["realized_model"], "gpt-5.6-luna")
        self.assertEqual(report["host_sessions"][0]["classification"], "host_approval")
        self.assertIsNone(report["host_sessions"][0]["agent_path"])
        self.assertEqual(report["host_sessions"][0]["realized_model"], "codex-auto-review")

    def test_invalid_input_is_the_only_failure_exit(self):
        invalid = ["", "{", "null", "[]", "{}", "true", "{} {}"]
        for key, value in [("start_time", "yesterday"), ("start_time", "2026-09-14"),
                           ("start_time", 42), ("cwd", "relative/path"), ("cwd", None),
                           ("cwd", "/tmp/\x00"), ("records_root", 2),
                           ("parent_thread_id", []), ("planned_subagents", {}),
                           ("planned_subagents", [None]), ("planned_subagents", [{}]),
                           ("planned_subagents", [self.request["planned_subagents"][0]] * 2)]:
            invalid.append(json.dumps({**self.request, key: value}))
        for key, value in [("task_name", "../smoke_a"), ("requested_model", None),
                           ("requested_effort", "")]:
            task = {**self.request["planned_subagents"][0], key: value}
            invalid.append(json.dumps({**self.request, "planned_subagents": [task]}))
        for raw in invalid:
            with self.subTest(raw=raw):
                result = self.run_command(raw=raw)
                self.assertNotEqual(result.returncode, 0)
                self.assertTrue(json.loads(result.stdout)["error"])
                self.assertNotIn("Traceback", result.stderr)

    def test_unpinned_subagent_inheriting_parent_settings_is_a_mismatch(self):
        rows = self.read_records("smoke_a.jsonl")
        for row in rows[1:]:
            row["payload"].update(model="gpt-6-astra", effort="medium")
        self.write_records("smoke_a.jsonl", rows)
        task = self.audit()["planned_subagents"][0]
        self.assertEqual(task["status"], "mismatch")
        self.assertEqual((task["realized_model"], task["realized_effort"]), ("gpt-6-astra", "medium"))

    def test_other_session_directory_and_old_records_cannot_match(self):
        rows = self.read_records("smoke_a.jsonl")
        for filename, changes in [
            ("other_session.jsonl", {"id": "other-session", "parent_thread_id": "other-parent"}),
            ("other_cwd.jsonl", {"id": "other-cwd", "cwd": "/workspace/other-repo"}),
            ("before_start.jsonl", {"id": "old", "timestamp": "2026-09-14T07:42:59Z"}),
        ]:
            copy = json.loads(json.dumps(rows))
            copy[0]["payload"].update(changes)
            for row in copy[1:]:
                row["payload"].update(model="gpt-6-astra", effort="ultra")
            self.write_records(filename, copy)
        self.assertEqual(self.audit()["planned_subagents"][0]["status"], "confirmed")
        (self.root / "smoke_a.jsonl").unlink()
        self.assertEqual(self.audit()["planned_subagents"][0]["status"], "unobservable")

    def test_ambiguous_parent_is_unobservable_without_guessing(self):
        rows = self.read_records("smoke_a.jsonl")
        rows[0]["payload"].update(id="other-session", parent_thread_id="other-parent")
        self.write_records("other_session.jsonl", rows)
        del self.request["parent_thread_id"]
        report = self.audit()
        self.assertIsNone(report["parent"]["thread_id"])
        self.assertEqual(report["planned_subagents"][0]["status"], "unobservable")
        self.assertIsNone(report["parent_ran_at_ultra"])

    def test_duplicate_task_under_same_parent_is_unobservable(self):
        rows = self.read_records("smoke_a.jsonl")
        rows[0]["payload"]["id"] = "second-smoke-a"
        self.write_records("duplicate.jsonl", rows)
        report = self.audit()
        self.assertEqual(report["planned_subagents"][0]["status"], "unobservable")
        self.assertEqual({item["thread_id"] for item in report["unplanned_subagents"]},
                         {"smoke_a", "second-smoke-a"})
        self.assertTrue(all(item["realized_model"] == "gpt-5.6-luna"
                            for item in report["unplanned_subagents"]))

    def test_parent_reports_each_turn_and_ultra_only_within_run(self):
        rows = self.read_records("parent.jsonl")
        old = json.loads(json.dumps(rows[1]))
        old["timestamp"] = "2026-09-14T07:42:59Z"
        old["payload"].update(turn_id="old-turn", effort="ultra")
        self.write_records("parent.jsonl", rows + [old])
        self.assertIsNone(self.audit()["parent_ran_at_ultra"])
        current = json.loads(json.dumps(rows[1]))
        current["timestamp"] = "2026-09-14T07:45:00Z"
        current["payload"].update(turn_id="ultra-turn", effort="ultra")
        self.write_records("parent.jsonl", rows + [old, current])
        report = self.audit()
        self.assertEqual([turn["effort"] for turn in report["parent"]["turns"]], ["medium", "ultra"])
        self.assertIs(report["parent_ran_at_ultra"], True)

    def test_no_subagents_has_no_parent_effort_record(self):
        self.request["planned_subagents"] = []
        for path in self.root.glob("*.jsonl"):
            if path.name != "parent.jsonl":
                path.unlink()
        report = self.audit()
        self.assertEqual(report["planned_subagents"], [])
        self.assertEqual(report["unplanned_subagents"], [])
        self.assertEqual(report["parent"]["turns"], [])
        self.assertIsNone(report["parent_ran_at_ultra"])

    def test_guardian_only_run_has_no_parent_effort_record(self):
        guardian = self.read_records("smoke_a.jsonl")
        guardian[0]["payload"].update(id="guardian", agent_path=None,
                                      thread_source="guardian_review")
        for path in self.root.glob("*.jsonl"):
            if path.name != "parent.jsonl":
                path.unlink()
        self.write_records("guardian.jsonl", guardian)
        self.request["planned_subagents"] = []
        report = self.audit()
        self.assertEqual(len(report["host_sessions"]), 1)
        self.assertEqual(report["unplanned_subagents"], [])
        self.assertEqual(report["parent"]["turns"], [])
        self.assertIsNone(report["parent_ran_at_ultra"])

    def test_empty_plan_still_surfaces_unplanned_subagents(self):
        self.request["planned_subagents"] = []
        report = self.audit()
        self.assertEqual({task["agent_path"] for task in report["unplanned_subagents"]},
                         {"/root/smoke_a", "/root/smoke_b"})

    def test_missing_parent_does_not_hide_confirmed_subagent(self):
        (self.root / "parent.jsonl").unlink()
        report = self.audit()
        self.assertEqual(report["planned_subagents"][0]["status"], "confirmed")
        self.assertEqual(report["parent"]["status"], "unobservable")
        self.assertIsNone(report["parent_ran_at_ultra"])

    def test_default_host_root_and_parent_identity(self):
        del self.request["records_root"]
        del self.request["parent_thread_id"]
        self.request["planned_subagents"][0]["task_name"] = "/root/smoke_a"
        result = self.run_command(env={"CODEX_HOME": self.temp.name, "CODEX_THREAD_ID": "parent"})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["planned_subagents"][0]["status"], "confirmed")

    def test_partial_parent_evidence_cannot_rule_out_ultra(self):
        path = self.root / "parent.jsonl"
        path.write_text(path.read_text() + "{truncated")
        report = self.audit()
        self.assertEqual(len(report["parent"]["turns"]), 1)
        self.assertEqual(report["parent"]["status"], "unobservable")
        self.assertIsNone(report["parent_ran_at_ultra"])

    def test_malformed_identity_is_unobservable_instead_of_crashing(self):
        original = self.read_records("smoke_a.jsonl")
        del self.request["parent_thread_id"]
        for key, value in [("parent_thread_id", []), ("id", {}),
                           ("agent_path", []), ("timestamp", None)]:
            with self.subTest(key=key):
                rows = json.loads(json.dumps(original))
                rows[0]["payload"][key] = value
                self.write_records("smoke_a.jsonl", rows)
                report = self.audit()
                self.assertEqual(report["planned_subagents"][0]["status"], "unobservable")
                self.assertTrue(report["record_errors"])

    @unittest.skipIf(os.geteuid() == 0, "root bypasses fixture permission restrictions")
    def test_unreadable_directory_is_an_audit_outcome(self):
        self.root.chmod(0)
        try:
            report = self.audit()
            self.assertEqual(report["planned_subagents"][0]["status"], "unobservable")
            self.assertTrue(report["record_errors"])
        finally:
            self.root.chmod(0o700)

    def test_turns_before_session_creation_cannot_confirm_a_spawn(self):
        rows = self.read_records("smoke_a.jsonl")
        rows = rows[:2]
        rows[1]["timestamp"] = "2026-09-14T07:43:01Z"
        self.write_records("smoke_a.jsonl", rows)
        task = self.audit()["planned_subagents"][0]
        self.assertEqual(task["status"], "unobservable")
        self.assertEqual(task["evidence"], [])

    def test_pinned_subagent_matches_on_initial_and_followup_turns(self):
        report = self.audit()
        planned = report["planned_subagents"]
        self.assertEqual([item["status"] for item in planned], ["confirmed", "confirmed"])
        self.assertEqual(planned[0]["realized_model"], "gpt-5.6-luna")
        self.assertEqual(planned[0]["realized_effort"], "low")
        self.assertEqual([turn["turn_id"] for turn in planned[0]["evidence"]],
                         ["turn-6", "turn-7"])
        self.assertEqual(planned[0]["evidence"][0]["line"], 2)
        self.assertEqual(report["parent"]["thread_id"], "parent")
        self.assertEqual(report["parent"]["turns"][0]["effort"], "medium")
        self.assertIs(report["parent_ran_at_ultra"], False)


if __name__ == "__main__":
    unittest.main()
