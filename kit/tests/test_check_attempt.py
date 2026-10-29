import datetime
import glob
import io
import json
import os
import sys
import tempfile
import unittest

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KIT)
import check_attempt as ca  # noqa: E402

SHA = "4bd424069b2dd02b6f53b26bfd66136833b87806b826c42b273076e34f64ba3c"
GOOD = """# Attempt 2026-10-19-someone-4bd42406

target: open-target
date: 2026-10-19
credit: someone
run_status: NOTHING
prereg_sha256: {sha}
budget: one hour on a laptop
compared_with: https://example.org/table.html fetched 2026-10-19
closest: N = 7, 0.01 above the table
lenses: seeding=negative, basin-hopping=nothing
claims: none

## What was tried

Two lenses.

## Why it fell short

Both stayed above the table.
""".replace("{sha}", SHA)


class AttemptRecordTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = self.tmp.name
        os.makedirs(os.path.join(root, "bank"))
        with open(os.path.join(root, "bank", "targets.json"), "w", encoding="utf-8") as f:
            json.dump([{"id": "open-target", "disclosure": "open"}, {"id": "live-puzzle", "disclosure": "commit-only"}], f)
        self.root = root

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, text, target="open-target", name="2026-10-19-someone-4bd42406.md"):
        d = os.path.join(self.root, "attempts", target)
        os.makedirs(d, exist_ok=True)
        p = os.path.join(d, name)
        with open(p, "w", encoding="utf-8", newline="") as f:  # exact bytes, also on Windows
            f.write(text)
        return p

    def problems(self, text, **kw):
        return ca.check(self.write(text, **kw), root=self.root, today=datetime.date(2026, 10, 20))

    def test_good_record_passes(self):
        self.assertEqual(self.problems(GOOD), [])

    def test_crlf_record_passes(self):
        self.assertEqual(self.problems(GOOD.replace("\n", "\r\n")), [])

    def test_missing_field_fails(self):
        self.assertIn("missing field budget", self.problems(GOOD.replace("budget: one hour on a laptop\n", "")))

    def test_unknown_target_fails(self):
        p = self.problems(GOOD.replace("target: open-target", "target: no-such-target"))
        self.assertTrue(any("not an id in bank/targets.json" in x for x in p))

    def test_id_title_and_folder_must_agree(self):
        self.assertTrue(any(x.startswith("title must be") for x in self.problems(GOOD.replace("4bd42406\n", "00000000\n", 1))))
        self.assertTrue(any(x.startswith("file name must be") for x in self.problems(GOOD, name="other.md")))
        self.assertTrue(any("must sit in attempts/open-target/" in x for x in self.problems(GOOD, target="elsewhere")))

    def test_bad_values_fail(self):
        self.assertTrue(any("lens entry" in x for x in self.problems(GOOD.replace("seeding=negative", "seeding=great"))))
        self.assertTrue(any("run_status" in x for x in self.problems(GOOD.replace("run_status: NOTHING", "run_status: DONE"))))
        self.assertTrue(any("claims must be" in x for x in self.problems(GOOD.replace("claims: none", "claims: PR 12"))))
        self.assertTrue(any("prereg_sha256" in x for x in self.problems(GOOD.replace(SHA, "abc"))))
        self.assertTrue(any("future" in x for x in self.problems(GOOD.replace("2026-10-19", "2026-12-01"),
                                                                   name="2026-12-01-someone-4bd42406.md")))

    def test_missing_section_fails(self):
        self.assertIn("missing section '## Why it fell short'", self.problems(GOOD.replace("## Why it fell short", "## Notes")))

    def test_duplicate_and_unknown_fields_fail(self):
        p = self.problems(GOOD.replace("claims: none", "claims: none\nclaims: none\nmood: fine"))
        self.assertIn("field claims given twice", p)
        self.assertIn("field mood is not allowed", p)

    def test_leaks_fail(self):
        for leak, what in (("/Users/someone/run", "absolute path"), ("me@example.org", "e-mail address"),
                           ("ghp_" + "a" * 30, "token-like string"), ("C:\\\\work", "Windows path")):
            self.assertIn(f"contains a {what}", self.problems(GOOD.replace("Two lenses.", "Two lenses " + leak)), leak)

    def test_commit_only_target(self):
        rec = ("# Attempt 2026-10-19-someone-{c8}\n\ntarget: live-puzzle\ndate: 2026-10-19\ncredit: someone\nrun_status: NOTHING\n"
               "commitment: {c}\n").format(c8=SHA[:8], c=SHA)
        self.assertEqual(self.problems(rec, target="live-puzzle"), [])
        self.assertTrue(any("header only" in x for x in self.problems(rec + "\n## What was tried\nkeys\n", target="live-puzzle")))
        self.assertTrue(any("not allowed for a commit-only target" in x
                            for x in self.problems(rec.replace("run_status: NOTHING", "run_status: NOTHING\nbudget: 1 h"), target="live-puzzle")))

    def test_cli_last_line(self):
        p = self.write(GOOD)
        out = io.StringIO()
        old, sys.stdout = sys.stdout, out
        try:
            saved = ca.ROOT
            ca.ROOT = self.root
            rc = ca.main([p])
        finally:
            sys.stdout = old
            ca.ROOT = saved
        self.assertEqual(out.getvalue().strip().splitlines()[-1], "CHECK_ATTEMPT: PASS")
        self.assertEqual(rc, 0)

    def test_shipped_records_pass(self):
        root = os.path.dirname(KIT)
        files = [f for f in glob.glob(os.path.join(root, "attempts", "*", "*.md"))]
        for f in files:
            self.assertEqual(ca.check(f, root=root), [], f)


if __name__ == "__main__":
    unittest.main()
