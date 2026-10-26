# SPDX-License-Identifier: AGPL-3.0-or-later
"""Baseline evidence checks, using local synthetic benchmark records only."""
import hashlib
import json
import os
import shutil
import unittest

import test_check_run as fixtures


class BaselineChecks(fixtures.Base):
    def setUp(self):
        super().setUp()
        self.attack()
        self.B = os.path.join(self.R, "baseline")
        self.plan = {
            "source": "https://example.org/paper, Table 2",
            "revision": "reference implementation release 1",
            "data": "benchmark release 1, sha256 " + fixtures.HEX,
            "split": "published test split, sha256 " + fixtures.HEX,
            "preprocessing": "published tokenization, no additional filtering",
            "metrics": {
                "hit_at_5": {"definition": "token-level hit@5", "expected": "0.89", "tolerance": "0.02"}
            },
        }
        self.result = {
            "status": "reproduced",
            "command": "python3 baseline/reference.py",
            "exit_code": 0,
            "scores": {"hit_at_5": "0.8951"},
        }
        fixtures.w(os.path.join(self.B, "output.txt"), "hit_at_5: 0.8951\n")
        self.write_result()
        self.freeze()

    def freeze(self):
        plan_path = os.path.join(self.B, "plan.json")
        fixtures.w(plan_path, json.dumps(self.plan))
        digest = hashlib.sha256(fixtures.check_run.rbytes(plan_path)).hexdigest()
        fixtures.w(os.path.join(self.R, "PREREG.md"),
                   "frozen: 2026-10-12T03:01:00Z\n"
                   "null_test: not needed because a deterministic checker decides\n"
                   "baseline_test: required\nbaseline_plan_sha256: %s\n" % digest)

    def write_result(self):
        self.result["output_sha256"] = hashlib.sha256(
            fixtures.check_run.rbytes(os.path.join(self.B, "output.txt"))).hexdigest()
        fixtures.w(os.path.join(self.B, "result.json"), json.dumps(self.result))

    def claim(self):
        fixtures.w(os.path.join(self.R, "attempts", "lens0", "report.md"),
                   "claim level: partial_win_claim\n")

    def package_with_baseline(self):
        P = self.package()
        shutil.copytree(self.B, os.path.join(P, "how-we-built-it", "baseline"))
        shutil.copyfile(os.path.join(self.R, "PREREG.md"),
                        os.path.join(P, "how-we-built-it", "PREREG.md"))
        self.sums(P)
        return P

    def test_reproduced_baseline_allows_claim(self):
        self.claim()
        self.assertPass(self.W)
        self.assertIn("baseline reproduced", self.out)

    def test_tolerance_boundary_is_inclusive(self):
        for score in ("0.87", "0.91"):
            with self.subTest(score=score):
                self.result["scores"]["hit_at_5"] = score
                self.write_result()
                self.claim()
                self.assertPass(self.W)

    def test_outside_tolerance_cannot_be_reported_as_reproduced(self):
        self.result["scores"]["hit_at_5"] = "0.9100000001"
        self.write_result()
        self.assertFail("baseline", self.W)

    def test_unquoted_decimal_scores_do_not_round_into_tolerance(self):
        text = json.dumps(self.result).replace('"0.8951"', "0.91000000000000000000000000001")
        fixtures.w(os.path.join(self.B, "result.json"), text)
        self.assertFail("tolerance", self.W)

    def test_small_finite_scores_do_not_underflow_into_tolerance(self):
        self.plan["metrics"]["hit_at_5"].update(expected="1e-1000100", tolerance="1e-1000100")
        self.freeze()
        self.result["scores"]["hit_at_5"] = "2e-1000100"
        self.write_result()
        self.assertPass(self.W)
        self.result["scores"]["hit_at_5"] = "4e-1000100"
        self.write_result()
        self.assertFail("tolerance", self.W)

    def test_mismatch_allows_negative_run(self):
        self.result.update(status="mismatch", scores={"hit_at_5": "0.55"},
                           reason="The published score has not been reproduced.")
        self.write_result()
        self.assertPass(self.W)
        self.assertIn("baseline", self.out)
        self.assertIn("WARN:", self.out)

    def test_mismatch_blocks_improvement_claim(self):
        self.result.update(status="mismatch", scores={"hit_at_5": "0.55"},
                           reason="The published score has not been reproduced.")
        self.write_result()
        self.claim()
        self.assertFail("baseline", self.W)

    def test_blocked_baseline_allows_negative_run_but_not_claim(self):
        self.result.update(status="blocked", exit_code=1, scores={},
                           reason="The required reference data is unavailable.")
        self.write_result()
        self.assertPass(self.W)
        self.claim()
        self.assertFail("baseline", self.W)

    def test_unresolved_baseline_needs_reason(self):
        self.result.update(status="blocked", exit_code=1, scores={})
        self.write_result()
        self.assertFail("reason", self.W)

    def test_reproduced_baseline_requires_successful_command(self):
        for code in (1, None, True, "0"):
            with self.subTest(code=code):
                self.result["exit_code"] = code
                self.write_result()
                self.assertFail("exit_code", self.W)

    def test_each_metric_must_reproduce(self):
        self.plan["metrics"]["mrr"] = {"definition": "token-level MRR", "expected": "0.83", "tolerance": "0.02"}
        self.freeze()
        self.result["scores"]["mrr"] = "0.84"
        self.write_result()
        self.claim()
        self.assertPass(self.W)
        self.result["scores"]["mrr"] = "0.85"
        self.write_result()
        self.assertPass(self.W)
        self.result["scores"]["mrr"] = "0.850001"
        self.write_result()
        self.assertFail("mrr", self.W)

    def test_score_names_must_match_plan(self):
        for scores in ({}, {"wrong_unit": "0.8951"}, {"hit_at_5": "0.8951", "extra": "1"}):
            with self.subTest(scores=scores):
                self.result["scores"] = scores
                self.write_result()
                self.assertFail("scores", self.W)

    def test_invalid_numbers_fail_explicitly(self):
        for bad in ("NaN", "Infinity", "-Infinity", "nonsense", "", None, True, [], {}):
            for field in ("expected", "tolerance", "score"):
                with self.subTest(bad=bad, field=field):
                    self.plan["metrics"]["hit_at_5"].update(expected="0.89", tolerance="0.02")
                    self.result["scores"]["hit_at_5"] = "0.8951"
                    if field == "score":
                        self.result["scores"]["hit_at_5"] = bad
                    else:
                        self.plan["metrics"]["hit_at_5"][field] = bad
                    self.freeze()
                    self.write_result()
                    self.assertFail("baseline", self.W)

    def test_negative_tolerance_fails(self):
        self.plan["metrics"]["hit_at_5"]["tolerance"] = "-0.02"
        self.freeze()
        self.assertFail("tolerance", self.W)

    def test_plan_protocol_fields_are_required(self):
        for field in ("source", "revision", "data", "split", "preprocessing"):
            with self.subTest(field=field):
                original = self.plan[field]
                self.plan[field] = " "
                self.freeze()
                self.assertFail(field, self.W)
                self.plan[field] = original

    def test_empty_metrics_and_missing_definition_fail(self):
        self.plan["metrics"] = {}
        self.freeze()
        self.assertFail("metrics", self.W)
        self.plan["metrics"] = {"hit_at_5": {"expected": "0.89", "tolerance": "0.02"}}
        self.freeze()
        self.assertFail("definition", self.W)

    def test_missing_evidence_fails(self):
        for name in ("plan.json", "result.json", "output.txt"):
            with self.subTest(name=name):
                path = os.path.join(self.B, name)
                original = fixtures.check_run.rbytes(path)
                os.remove(path)
                self.assertFail(name, self.W)
                fixtures.check_run.wbytes(path, original)

    def test_changed_plan_fails_without_refreezing(self):
        self.plan["metrics"]["hit_at_5"]["tolerance"] = "0.5"
        fixtures.w(os.path.join(self.B, "plan.json"), json.dumps(self.plan))
        self.assertFail("baseline_plan_sha256", self.W)

    def test_changed_output_fails(self):
        fixtures.w(os.path.join(self.B, "output.txt"), "different output\n")
        self.assertFail("output_sha256", self.W)

    def test_untyped_or_malformed_json_fails(self):
        for name in ("plan.json", "result.json"):
            path = os.path.join(self.B, name)
            original = fixtures.check_run.rbytes(path)
            for text in ("{", "[]", "null", "42"):
                with self.subTest(name=name, text=text):
                    fixtures.w(path, text)
                    self.assertFail("baseline", self.W)
            fixtures.check_run.wbytes(path, original)

    def test_unknown_status_and_empty_command_fail(self):
        self.result["status"] = "looks good"
        self.write_result()
        self.assertFail("status", self.W)
        self.result.update(status="reproduced", command=" ")
        self.write_result()
        self.assertFail("command", self.W)

    def test_freeze_must_precede_baseline_output(self):
        earlier = 1_000_000_000
        os.utime(os.path.join(self.B, "output.txt"), (earlier, earlier))
        self.assertFail("before", self.W)

    def test_not_needed_requires_explanation_and_no_baseline(self):
        shutil.rmtree(self.B)
        pre = os.path.join(self.R, "PREREG.md")
        original = fixtures.check_run.read(pre).split("baseline_test:")[0]
        fixtures.w(pre, original + "baseline_test: not needed because an exact object is checked\n")
        self.assertPass(self.W)
        fixtures.w(pre, original + "baseline_test: not needed because\n")
        self.assertFail("baseline_test", self.W)

    def test_existing_evidence_cannot_be_undeclared_or_exempted(self):
        pre = os.path.join(self.R, "PREREG.md")
        original = fixtures.check_run.read(pre).split("baseline_test:")[0]
        fixtures.w(pre, original)
        self.assertFail("baseline_test", self.W)
        fixtures.w(pre, original + "baseline_test: not needed because an exact object is checked\n")
        self.assertFail("baseline", self.W)

    def test_legacy_run_warns_without_failing(self):
        shutil.rmtree(self.B)
        pre = os.path.join(self.R, "PREREG.md")
        fixtures.w(pre, fixtures.check_run.read(pre).split("baseline_test:")[0])
        self.assertPass(self.W)
        self.assertIn("legacy", self.out)

    def test_package_rechecks_baseline(self):
        P = self.package_with_baseline()
        self.assertPass("--package", P, "--no-exec")
        self.result.update(status="mismatch", scores={"hit_at_5": "0.55"},
                           reason="The baseline could not be reproduced.")
        self.write_result()
        shutil.copyfile(os.path.join(self.B, "result.json"),
                        os.path.join(P, "how-we-built-it", "baseline", "result.json"))
        self.sums(P)
        self.assertFail("baseline", "--package", P, "--no-exec")

    def test_package_cannot_omit_baseline_evidence(self):
        P = self.package_with_baseline()
        shutil.rmtree(os.path.join(P, "how-we-built-it", "baseline"))
        self.sums(P)
        self.assertFail("baseline", "--package", P, "--no-exec")

    def test_commit_only_baseline_is_checked_in_private_storage(self):
        fixtures.w(os.path.join(self.R, "target.md"), "id: toy-cipher\n")
        private = os.path.join(self.W, "private", "toy-cipher", os.path.basename(self.R))
        os.makedirs(private)
        shutil.move(self.B, os.path.join(private, "baseline"))
        self.assertPass(self.W)
        self.assertIn("baseline reproduced", self.out)
        shutil.copytree(os.path.join(private, "baseline"), self.B)
        self.assertFail("private", self.W)

    def test_sealed_envelope_rechecks_private_baseline(self):
        fixtures.w(os.path.join(self.R, "target.md"), "id: toy-cipher\n")
        private = os.path.join(self.W, "private", "toy-cipher", os.path.basename(self.R))
        os.makedirs(private)
        shutil.move(self.B, os.path.join(private, "baseline"))
        self.B = os.path.join(private, "baseline")
        fixtures.panel(os.path.join(self.W, "private", "toy-cipher", "panel"))
        fixtures.w(os.path.join(self.R, "panel", "gate.md"),
                   "status: CONFIRMED_SOLUTION\nconfirmed_scope: one cell, exactly as reproduced.\n")
        envelope = os.path.join(self.W, "outbox", "test-envelope", "envelope.md")
        fixtures.w(envelope, "# Sealed envelope test-envelope\ntarget: toy-cipher\nproblem: Problem 7\n"
                   "| file | frozen (UTC) | commitment |\n|---|---|---|\n"
                   "| solution file 1 (key) | 2026-10-12T03:14:15Z | `%s` |\n" % fixtures.HEX)
        for path in (envelope, os.path.dirname(envelope)):
            with self.subTest(path=path):
                self.assertPass("--package", path, "--workdir", self.W, "--no-exec")
                self.result.update(status="blocked", exit_code=1, scores={},
                                   reason="The required reference data is unavailable.")
                self.write_result()
                self.assertFail("baseline", "--package", path, "--workdir", self.W, "--no-exec")
                self.result.update(status="reproduced", exit_code=0, scores={"hit_at_5": "0.8951"})
                self.write_result()

    def test_dry_run_does_not_require_baseline_execution(self):
        shutil.rmtree(self.B)
        self.assertPass(self.W, "--setup")


if __name__ == "__main__":
    unittest.main(verbosity=2)
