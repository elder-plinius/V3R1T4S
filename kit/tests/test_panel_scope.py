# SPDX-License-Identifier: AGPL-3.0-or-later
"""Own bounded fixtures; all package execution disabled and Git strictly mocked."""
import os
from pathlib import Path
from types import SimpleNamespace
from unittest import mock
import unittest
import test_check_run as f

c = f.check_run
NARROW = "one cell, exactly as reproduced."
BROAD = "all cells are optimal."


class ScopeBinding(f.Base):
    def build(self, mode, status="CONFIRMED_PARTIAL"):
        self.attack(levels=("partial_win_claim", "negative"))
        private = mode.startswith("envelope")
        if private:
            f.w(os.path.join(self.R, "target.md"), "id: toy-cipher\n")
            f.w(os.path.join(self.R, "PREREG.md"), "null_test: required\n")
            f.w(os.path.join(self.R, "null_test.md"), "controls: 400\nbest_control: 0.4\nreal: 0.9\nreal_beats_all_controls: yes\ncommand: synthetic\n")
            pd = Path(self.W) / "private/toy-cipher/panel"
            f.panel(str(pd))
            (pd / "gate.md").unlink()  # RUN.md: authoritative gate is in the run.
            gate = Path(self.R) / "panel/gate.md"
            P = Path(self.W) / "outbox/sealed"
            f.w(str(P / "envelope.md"), "# Sealed envelope sealed\ntarget: toy-cipher\nproblem: Problem 7\n| file | frozen (UTC) | commitment |\n|---|---|---|\n| solution file 1 (key) | 2026-10-12T03:14:15Z | "+chr(96)+f.HEX+chr(96)+" |\n")
        else:
            P = Path(self.package())
            f.panel(os.path.join(self.R, "panel"))
            pd = P / "panel" if mode == "package" else Path(self.R) / "panel"
            gate = pd / "gate.md"
        f.w(str(gate), "status: "+status+"\nconfirmed_scope: "+NARROW+"\n")
        argv = [self.W, "--no-exec"] if mode in ("workspace", "workspace_run_only", "envelope_workspace") else ["--package", str(P), "--workdir", self.W, "--no-exec"]
        return P, pd, gate, argv

    def invoke(self, argv):
        def git_only(cmd, **kwargs):
            self.assertEqual(cmd, ["git", "-C", os.path.join(self.W, "repo"), "rev-parse", "HEAD"])
            return SimpleNamespace(returncode=0, stdout=b"c"*40+b"\n")
        with mock.patch.object(c.subprocess, "run", side_effect=git_only):
            return self.run_check(*argv)

    def exercise(self, mode):
        for status in ("CONFIRMED_PARTIAL", "CONFIRMED_SOLUTION"):
            for variant in ("equal", "broader", "case", "spacing", "punctuation",
                            "missing", "empty", "duplicate_same", "duplicate_different",
                            "gate_missing", "gate_empty", "gate_duplicate"):
                with self.subTest(mode=mode, status=status, variant=variant):
                    # Each row owns a fresh workspace; no state left by a prior mutation.
                    self.tearDown()
                    self.setUp()
                    P, pd, gate, argv = self.build(mode, status)
                    cp = pd / "criterion.md"
                    if variant == "broader":
                        gate.write_text(gate.read_text().replace(NARROW, BROAD))
                        if mode in ("package", "workspace"):
                            gp = P / "panel/gate.md"
                            gp.write_text(gp.read_text().replace(NARROW, BROAD))
                            rp = P / "README.md"
                            rp.write_text(rp.read_text().replace(NARROW, BROAD))
                    elif variant in ("case", "spacing", "punctuation"):
                        altered = {"case": NARROW.upper(), "spacing": NARROW.replace("one cell", "one  cell"),
                                   "punctuation": NARROW.rstrip(".")}[variant]
                        cp.write_text(cp.read_text().replace(NARROW, altered))
                    elif variant in ("missing", "empty"):
                        replacement = "" if variant == "missing" else "confirmed_scope: \n"
                        cp.write_text(cp.read_text().replace("confirmed_scope: "+NARROW+"\n", replacement))
                    elif variant.startswith("duplicate"):
                        value = NARROW if variant == "duplicate_same" else BROAD
                        cp.write_text("confirmed_scope: "+value+"\n"+cp.read_text())
                    elif variant.startswith("gate_"):
                        if variant == "gate_duplicate":
                            gate.write_text(gate.read_text()+"confirmed_scope: "+NARROW+"\n")
                        else:
                            replacement = "" if variant == "gate_missing" else "confirmed_scope: \n"
                            gate.write_text(gate.read_text().replace("confirmed_scope: "+NARROW+"\n", replacement))
                    if not mode.startswith("envelope"):
                        self.sums(str(P))
                    self.assertEqual(self.invoke(argv), 0 if variant == "equal" else 1, self.out)

    def test_package(self):
        self.exercise("package")

    def test_workspace(self):
        self.exercise("workspace")

    def test_run_gate_only(self):
        self.exercise("workspace_run_only")

    def test_envelope(self):
        self.exercise("envelope")

    def test_private_workspace(self):
        self.exercise("envelope_workspace")

    def test_envelope_target_binding(self):
        for variant in ("different", "missing", "duplicate_same", "duplicate_different"):
            with self.subTest(variant=variant):
                self.tearDown()
                self.setUp()
                P, pd, gate, argv = self.build("envelope")
                target = Path(self.R) / "target.md"
                text = {"different": "id: toy-record\n", "missing": "",
                        "duplicate_same": "id: toy-cipher\nid: toy-cipher\n",
                        "duplicate_different": "id: toy-cipher\nid: toy-record\n"}[variant]
                target.write_text(text)
                self.assertEqual(self.invoke(argv), 1, self.out)

    def test_confirmed_target_is_unambiguous(self):
        P, pd, gate, argv = self.build("workspace_run_only")
        target = Path(self.R) / "target.md"
        target.write_text("id: toy-record\nid: toy-record\n")
        self.assertEqual(self.invoke(argv), 1, self.out)
        self.assertIn("duplicate critical field 'id'", self.out)

    def test_unconfirmed_target_policy_unchanged(self):
        self.attack()
        f.w(os.path.join(self.R, "target.md"), "id: toy-record\nid: toy-record\n")
        self.assertEqual(self.invoke([self.W, "--no-exec"]), 0, self.out)

    def test_existing_metadata_framing_only(self):
        P, pd, gate, argv = self.build("package")
        # Existing kv() framing equivalence, not semantic normalization.
        cp = pd / "criterion.md"
        cp.write_text(cp.read_text().replace("confirmed_scope: "+NARROW,
                                            "  confirmed_scope: "+chr(96)+NARROW+chr(96)+"  "))
        self.sums(str(P))
        self.assertEqual(self.invoke(argv), 0, self.out)


if __name__ == "__main__":
    unittest.main()
