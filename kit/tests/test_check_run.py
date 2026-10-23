# SPDX-License-Identifier: AGPL-3.0-or-later
"""Unit tests for kit/check_run.py: good and bad fixtures, built in a temporary folder.

    python3 kit/tests/test_check_run.py        (standard library only)
"""
import builtins, contextlib, hashlib, io, json, os, shutil, sys, tempfile, unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import check_run  # noqa: E402

BANK = {"schema": "v3r1t4s.bank/1", "targets": [
    {"id": "toy-record", "category": "record-tables", "disclosure": "open"},
    {"id": "toy-cipher", "category": "unbroken-ciphers", "disclosure": "commit-only"},
]}
HEX = "ab" * 32
PLAINTEXT = "MEETMEATTHEOLDMILLATMIDNIGHTBRINGTHELANTERNANDTHEMAPOFTHERIVER"
CHECKER = """import sys
words = [l.strip() for l in open('object/code.txt') if l.strip()]
ok = len(words) == 3 and all(len(w) == 4 and w.count('1') == 2 for w in words)
print('PASS' if ok else 'FAIL')
"""


def w(path, text, newline=None):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline=newline) as f:
        f.write(text)


def panel(d, gate_status="CONFIRMED_PARTIAL", contexts=("subagent", "subagent", "subagent"), passes=(True, True, True)):
    for role, ctx, ok in zip(check_run.PANEL, contexts, passes):
        w(os.path.join(d, role + ".md"), "# %s\ncontext: %s\nchecked %s independently.\npass: %s\n"
          % (role, ctx, role, "true" if ok else "false"))
    w(os.path.join(d, "gate.md"), "status: %s\nconfirmed_scope: one cell, exactly as reproduced.\n" % gate_status)


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="v3r1t4s_test_")
        self.W = os.path.join(self.tmp, "ws")
        W = self.W
        w(os.path.join(W, "repo", "kit", "README"), "kit\n")
        w(os.path.join(W, "repo", "bank", "targets.json"), json.dumps(BANK))
        w(os.path.join(W, "settings.md"), "\n".join(
            "%s: %s" % (k, v) for k, v in [("credit", "tester"), ("github", "unknown"), ("curious_about", "surprise me"),
                                           ("effort", "light"), ("schedule", "manual"), ("publish_charter", "no"),
                                           ("memory", "no"), ("capabilities", "shell yes"), ("agent_run", "manual"),
                                           ("repo_tag", "none"), ("repo_commit", "c" * 40),
                                           ("tag_signature", "not checked")]) + "\n")
        w(os.path.join(W, "charter.md"), "# Research charter v1\n## Quarries\n- id: toy-record\n## Lenses\n- plain\n")
        w(os.path.join(W, "RUN_PROMPT.txt"), "V3R1T4S run. Workspace: %s.\n1. Read %s/repo/AGENTS.md\n" % (W, W))
        w(os.path.join(W, "private", "never_publish.txt"), "Placeholder Realname\n")
        w(os.path.join(W, "REPORT.md"), "# Report\nNothing found on toy-record; ruled out two lines.\n")
        w(os.path.join(W, "LOG.md"), "2026-10-12 | toy-record | plain, skeptic | nothing | NOTHING | 50\n")
        self.R = os.path.join(W, "runs", "2026-10-12-0300")
        R = self.R
        w(os.path.join(R, "target.md"), "id: toy-record\nwhy: practice\n")
        w(os.path.join(R, "scout.md"), "url: http://example.org/table\nstatus: 200\nsha256: %s\n" % HEX)
        w(os.path.join(R, "BRIEF.md"), "definition quoted\n")
        w(os.path.join(R, "data", "status.html"), "<p>open</p>\n", newline="")
        w(os.path.join(R, "scout.md"), "url: http://example.org/table\nstatus: 200\nsha256: %s\n"
          % hashlib.sha256(b"<p>open</p>\n").hexdigest())

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def attack(self, levels=("nothing", "negative"), null="not needed because a deterministic checker decides"):
        w(os.path.join(self.R, "PREREG.md"), "frozen: 2026-10-12T03:01:00Z\nnull_test: %s\n" % null)
        for i, lv in enumerate(levels):
            A = os.path.join(self.R, "attempts", "lens%d" % i)
            dead = "" if lv.endswith("_claim") else "dead lines:\n" + "".join(
                "- tried idea %d: real output said no; dead because the bound is tight\n" % k for k in range(3))
            w(os.path.join(A, "report.md"), "claim level: %s\n%s" % (lv, dead), newline="")
            w(os.path.join(A, "NOTES.md"), "hypotheses\n")
            w(os.path.join(A, "code", "try.py"), "print(1)\n")
            w(os.path.join(A, "code", "try.out"), "1\n")

    def run_check(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = check_run.main(list(argv))
        self.out = out.getvalue()
        return rc

    def assertPass(self, *argv):
        rc = self.run_check(*argv)
        self.assertEqual(rc, 0, self.out)
        self.assertIn("CHECK_RUN: PASS", self.out)

    def assertFail(self, needle, *argv):
        rc = self.run_check(*argv)
        self.assertEqual(rc, 1, self.out)
        self.assertIn(needle, self.out)

    def package(self, name="2026-10-12-tester-0123abcd", target="toy-record", corrupt_checker=False):
        P = os.path.join(self.W, "outbox", name)
        w(os.path.join(P, "README.md"), "# Claim\n## What\none cell, exactly as reproduced.\n## Check it yourself\nsh verify-it-yourself/run_checks.sh\n"
          "## Compared to\ntable value 2\n## Not claimed\noptimality\n## Credits\nthe table's maintainer\n")
        w(os.path.join(P, "RUN_IT_YOURSELF.md"), "sh verify-it-yourself/run_checks.sh  -> PASS\n")
        w(os.path.join(P, "INDEX.csv"), "target_id,cell,value,table_value,table_fetched_utc,file,sha256\n"
          "%s,A(4;2;2),3,2,2026-10-12T03:00:00Z,object/code.txt,%s\n" % (target, HEX))
        w(os.path.join(P, "object", "code.txt"), "1100\n1010\n0110\n")
        w(os.path.join(P, "verify-it-yourself", "check.py"), CHECKER if not corrupt_checker else "print('FAIL')\n")
        w(os.path.join(P, "verify-it-yourself", "run_checks.sh"), "python3 verify-it-yourself/check.py\n", newline="")
        w(os.path.join(P, "verify-it-yourself", "RECEIPTS.md"), "PASS\n")
        w(os.path.join(P, "how-we-built-it", "search.py"), "print('search')\n")
        w(os.path.join(P, "HOW_WE_FOUND_IT.md"), "Contributor text, unverified. Two lenses.\n")
        w(os.path.join(P, "the-record-we-beat", "table.md"), "url: http://example.org/table\nfetched: 2026-10-12T03:00:00Z\nsha256: %s\n" % HEX)
        panel(os.path.join(P, "panel"))
        self.sums(P)
        return P

    def sums(self, P):
        lines = []
        for d, _, fs in os.walk(P):
            for f in sorted(fs):
                p = os.path.join(d, f)
                r = os.path.relpath(p, P)
                if r != "SHA256SUMS":
                    lines.append("%s  %s" % (hashlib.sha256(check_run.rbytes(p)).hexdigest(), r))
        w(os.path.join(P, "SHA256SUMS"), "\n".join(sorted(lines, key=lambda l: l[66:])) + "\n")


class GoodFixtures(Base):
    def test_setup_dry_run_passes(self):
        self.assertPass(self.W, "--setup")

    def test_negative_run_passes(self):
        self.attack()
        self.assertPass(self.W)

    def test_promising_claim_without_panel_passes(self):
        self.attack(levels=("partial_win_claim", "negative"))
        w(os.path.join(self.W, "REPORT.md"), "# Report\nstatus: PROMISING (single-context, unpanelled), not CONFIRMED_PARTIAL.\n")
        self.assertPass(self.W)

    def test_confirmed_claim_with_panel_and_package_passes(self):
        self.attack(levels=("partial_win_claim", "negative"))
        panel(os.path.join(self.R, "panel"))
        w(os.path.join(self.W, "REPORT.md"), "# Report\nHeadline: CONFIRMED_PARTIAL on toy-record.\n")
        self.package()
        self.assertPass(self.W)

    def test_sealed_envelope_passes(self):
        w(os.path.join(self.R, "target.md"), "id: toy-cipher\n")
        self.attack(levels=("solution_claim", "negative"), null="required")
        w(os.path.join(self.R, "null_test.md"), "controls: 400\nbest_control: 0.41\nreal: 0.97\nreal_beats_all_controls: yes\ncommand: python3 null.py\n")
        panel(os.path.join(self.W, "private", "toy-cipher", "panel"))
        w(os.path.join(self.R, "panel", "gate.md"), "status: CONFIRMED_SOLUTION\nconfirmed_scope: key reproduces the ciphertext.\n")
        w(os.path.join(self.W, "private", "toy-cipher", "plaintext.txt"), PLAINTEXT)
        w(os.path.join(self.W, "outbox", "2026-10-12-tester-deadbeef", "envelope.md"),
          "# Sealed envelope 2026-10-12-tester-deadbeef\ntarget: toy-cipher\nproblem: Problem 7\n"
          "| file | frozen (UTC) | commitment |\n|---|---|---|\n| solution file 1 (key) | 2026-10-12T03:14:15Z | `%s` |\n" % HEX)
        self.assertPass(self.W)


class BadFixtures(Base):
    def test_stub_report(self):
        self.attack()
        w(os.path.join(self.W, "REPORT.md"), "STATUS: IN PROGRESS (run started 2026-10-12T03:00:00Z)\n")
        self.assertFail("in-progress stub", self.W)

    def test_placeholder_in_run_prompt(self):
        w(os.path.join(self.W, "RUN_PROMPT.txt"), "V3R1T4S run. Workspace: <WORKDIR>.\n")
        self.assertFail("placeholder <WORKDIR>", self.W, "--setup")

    def test_self_referential_run_prompt(self):
        w(os.path.join(self.W, "RUN_PROMPT.txt"), "V3R1T4S scheduled run: read %s/RUN_PROMPT.txt and follow it exactly.\n" % self.W)
        self.assertFail("tells the reader to read RUN_PROMPT.txt", self.W, "--setup")

    def test_missing_settings_keys(self):
        w(os.path.join(self.W, "settings.md"), "credit: tester\n")
        self.assertFail("settings.md lacks keys", self.W, "--setup")

    def test_stopped_before_attack(self):
        self.assertFail("stopped before the attack", self.W)

    def test_dead_excuse_rejected(self):
        w(os.path.join(self.R, "target.md"), "id: toy-record\ndead: run ended before attack step (smoke-test early stop)\n")
        self.assertFail("is not a dead target", self.W)

    def test_dead_target_allowed(self):
        w(os.path.join(self.R, "target.md"), "id: toy-record\ndead: solved by someone else on 2026-10-11 (status page)\n")
        self.assertPass(self.W)

    def test_empty_lens_report(self):
        self.attack()
        w(os.path.join(self.R, "attempts", "lens0", "report.md"), "claim level: negative\n")
        self.assertFail("needs 'dead lines:'", self.W)

    def test_lens_without_code(self):
        self.attack()
        shutil.rmtree(os.path.join(self.R, "attempts", "lens1", "code"))
        self.assertFail("at least one program", self.W)

    def test_unknown_target(self):
        self.attack()
        w(os.path.join(self.R, "target.md"), "id: made-up-quarry\n")
        self.assertFail("neither in the bank nor a quarry", self.W)

    def test_scout_without_status_record(self):
        self.attack()
        w(os.path.join(self.R, "scout.md"), "looked at the page, still open\n")
        self.assertFail("scout.md needs the status source", self.W)

    def test_commit_only_solution_in_run_folder(self):
        w(os.path.join(self.R, "target.md"), "id: toy-cipher\n")
        self.attack(null="required")
        w(os.path.join(self.R, "attempts", "lens0", "solution.txt"), "QGLVYF\n")
        self.assertFail("belongs in private/", self.W)

    def test_scout_hash_not_from_data(self):
        self.attack()
        w(os.path.join(self.R, "scout.md"), "url: http://example.org/table\nstatus: 200\nsha256: %s (placeholder)\n" % ("5f8e4c2a" * 8))
        self.assertFail("no sha256 in scout.md matches a file in data/", self.W)

    def test_unreachable_needs_failed_fetch(self):
        w(os.path.join(self.R, "target.md"), "id: toy-record\ndead: unreachable (files absent)\n")
        self.assertFail("'dead: unreachable' but scout.md records", self.W)

    def test_confirmed_but_not_packaged(self):
        self.attack(levels=("partial_win_claim", "negative"))
        panel(os.path.join(self.R, "panel"))
        self.assertFail("outbox/ has no package for it", self.W)

    def test_prereg_freeze_time_from_its_own_utc_line(self):
        w(os.path.join(self.R, "target.md"), "id: toy-cipher\n")
        self.attack(levels=("solution_claim", "negative"), null="required")
        w(os.path.join(self.R, "null_test.md"), "controls: 400\nbest_control: 0.4\nreal: 0.9\nreal_beats_all_controls: yes\ncommand: x\n")
        import time
        later = time.time() + 120
        os.utime(os.path.join(self.R, "PREREG.md"), (later, later))   # format fix after the null test
        self.run_check(self.W)
        self.assertNotIn("written after null_test.md", self.out)       # frozen: line (03:01Z) is earlier

    def test_one_lens_only(self):
        self.attack(levels=("negative",))
        self.assertFail("only one lens", self.W)

    def test_missing_prereg(self):
        self.attack()
        os.remove(os.path.join(self.R, "PREREG.md"))
        self.assertFail("PREREG.md missing", self.W)

    def test_self_confirmed_without_panel(self):
        self.attack(levels=("solution_claim", "negative"))
        w(os.path.join(self.W, "REPORT.md"), "# Report\nHeadline: CONFIRMED_SOLUTION on toy-record.\n")
        self.assertFail("only a three-skeptic panel can confirm", self.W)

    def test_panel_member_failed(self):
        self.attack(levels=("partial_win_claim", "negative"))
        panel(os.path.join(self.R, "panel"), passes=(True, False, True))
        self.assertFail("does not end with 'pass: true'", self.W)

    def test_role_played_panel(self):
        self.attack(levels=("partial_win_claim", "negative"))
        panel(os.path.join(self.R, "panel"), contexts=("role-play in the main session",) * 3)
        self.assertFail("is not a fresh context", self.W)

    def test_cipher_claim_without_null(self):
        w(os.path.join(self.R, "target.md"), "id: toy-cipher\n")
        self.attack(levels=("solution_claim", "negative"), null="required")
        self.assertFail("null test required", self.W)

    def test_cipher_null_too_small(self):
        w(os.path.join(self.R, "target.md"), "id: toy-cipher\n")
        self.attack(levels=("solution_claim", "negative"), null="required")
        w(os.path.join(self.R, "null_test.md"), "controls: 100\nbest_control: 0.4\nreal: 0.9\nreal_beats_all_controls: yes\ncommand: x\n")
        self.assertFail("at least 400 are required", self.W)

    def test_secret_leaks_from_private(self):
        w(os.path.join(self.R, "target.md"), "id: toy-cipher\n")
        self.attack(null="required")
        w(os.path.join(self.W, "private", "toy-cipher", "plaintext.txt"), PLAINTEXT)
        w(os.path.join(self.W, "REPORT.md"), "# Report\nDecrypt begins %s\n" % PLAINTEXT[:30].lower())
        self.assertFail("commit-only secrets stay in private", self.W)

    def test_unconfirmed_claim_in_outbox(self):
        self.attack(levels=("partial_win_claim", "negative"))
        P = self.package()
        shutil.rmtree(os.path.join(P, "panel"))
        self.sums(P)
        self.assertFail("required folder panel/", self.W)

    def test_package_missing_index(self):
        self.attack(levels=("partial_win_claim", "negative"))
        panel(os.path.join(self.R, "panel"))
        P = self.package()
        os.remove(os.path.join(P, "INDEX.csv"))
        self.sums(P)
        self.assertFail("INDEX.csv missing", "--package", P)

    def test_package_checker_fails(self):
        P = self.package(corrupt_checker=True)
        self.assertFail("did not pass from a clean copy", "--package", P)

    def test_package_readme_paraphrases_scope(self):
        P = self.package()
        w(os.path.join(P, "README.md"), "# Claim\n## What\na whole new record\n## Check it yourself\nx\n## Compared to\nx\n"
          "## Not claimed\nx\n## Credits\nx\n")
        self.sums(P)
        self.assertFail("must quote panel/gate.md's confirmed_scope", "--package", P, "--no-exec")

    def test_package_sha_mismatch(self):
        P = self.package()
        w(os.path.join(P, "HOW_WE_FOUND_IT.md"), "Contributor text, unverified. Edited later.\n")
        self.assertFail("SHA256SUMS mismatch", "--package", P, "--no-exec")

    def test_package_leaks_path_token_email(self):
        P = self.package()
        w(os.path.join(P, "how-we-built-it", "notes.md"),
          "ran in /" + "Users/alice/work\ntoken gh" + "p_" + "A" * 36 + "\nmail " + "alice" + "@" + "corp.example.io\n")
        self.sums(P)
        self.assertFail("absolute macOS user path", "--package", P, "--no-exec")
        self.assertIn("GitHub token", self.out)
        self.assertIn("email address", self.out)

    def test_package_never_publish(self):
        P = self.package()
        w(os.path.join(P, "HOW_WE_FOUND_IT.md"), "Contributor text, unverified. Thanks Placeholder Realname.\n")
        self.sums(P)
        self.assertFail("never_publish", "--package", P, "--workdir", self.W, "--no-exec")

    def test_commit_only_as_full_package(self):
        P = self.package(target="toy-cipher")
        self.assertFail("may leave the machine only as a sealed envelope", "--package", P, "--workdir", self.W, "--no-exec")

    def test_envelope_with_extra_text(self):
        E = os.path.join(self.W, "outbox", "x", "envelope.md")
        w(E, "# Sealed envelope x\ntarget: toy-cipher\nproblem: Problem 7\nhint: the plaintext is about a mill\n"
             "| file | frozen (UTC) | commitment |\n|---|---|---|\n| solution file 1 (key) | 2026-10-12T03:14:15Z | `%s` |\n" % HEX)
        self.assertFail("not part of the sealed-envelope template", "--package", os.path.dirname(E))

    def test_envelope_with_plain_key(self):
        E = os.path.join(self.W, "outbox", "x", "envelope.md")
        w(E, "# Sealed envelope x\ntarget: toy-cipher\nproblem: Problem 7\n"
             "| file | frozen (UTC) | commitment |\n|---|---|---|\n| solution file 1 (key) | 2026-10-12T03:14:15Z | `7:3,1,4,2,5,6,1,7` |\n")
        self.assertFail("not part of the sealed-envelope template", "--package", os.path.dirname(E))


class WindowsPortability(Base):
    """Issue #152: on Windows with Python <= 3.14 open() defaults to the locale encoding (often cp1252),
    and editors / PowerShell write CRLF line endings."""

    def utf8_bank(self, extra=None):
        bank = json.loads(json.dumps(BANK))
        bank["targets"][1]["note"] = "\u220f over the key schedule"  # UTF-8 bytes e2 88 8f; 0x8f is undefined in cp1252
        with open(os.path.join(self.W, "repo", "bank", "targets.json"), "wb") as f:
            f.write((extra if extra is not None else json.dumps(bank, ensure_ascii=False)).encode("utf-8"))

    @contextlib.contextmanager
    def cp1252_locale(self):
        real = builtins.open

        def fake(file, mode="r", buffering=-1, encoding=None, *a, **k):
            if "b" not in mode and encoding is None:
                encoding = "cp1252"
            return real(file, mode, buffering, encoding, *a, **k)
        with mock.patch("builtins.open", fake):
            yield

    def test_bank_loads_under_cp1252_locale(self):
        self.utf8_bank()
        with self.cp1252_locale():
            bank, _ = check_run.load_bank(self.W, {})
        self.assertIn("toy-cipher", bank)

    def test_commit_only_guard_under_cp1252_locale(self):
        self.utf8_bank()
        P = self.package(target="toy-cipher")
        with self.cp1252_locale():
            self.assertFail("may leave the machine only as a sealed envelope", "--package", P, "--workdir", self.W, "--no-exec")

    def test_unreadable_bank_fails_loudly(self):
        self.attack()
        self.utf8_bank(extra='{"targets": [')
        self.assertFail("could not read the bank", self.W)
        P = self.package()
        self.assertFail("could not read the bank", "--package", P, "--workdir", self.W, "--no-exec")

    def test_crlf_dead_lines_pass(self):
        self.attack()
        for l in ("lens0", "lens1"):
            p = os.path.join(self.R, "attempts", l, "report.md")
            data = check_run.rbytes(p)
            check_run.wbytes(p, data.replace(b"\n", b"\r\n"))
        self.assertPass(self.W)

    def test_crlf_report_without_dead_lines_still_fails(self):
        self.attack()
        check_run.wbytes(os.path.join(self.R, "attempts", "lens0", "report.md"), b"claim level: negative\r\ndead lines:\r\n- one\r\n")
        self.assertFail("needs 'dead lines:'", self.W)


class NullControlCounts(unittest.TestCase):
    def check_count(self, value):
        with tempfile.TemporaryDirectory(prefix="v3r1t4s_null_test_") as tmp:
            path = os.path.join(tmp, "null_test.md")
            w(path, "controls: %s\nbest_control: 0.4\nreal: 0.9\n"
              "real_beats_all_controls: yes\ncommand: python3 null.py\n" % value)
            c = check_run.Checker(quiet=True)
            return check_run.check_null(c, path, "fixture"), c.fails

    def test_plain_integer_counts_pass(self):
        for value in ("400", "401", "1000", " 400 "):
            with self.subTest(value=value):
                accepted, failures = self.check_count(value)
                self.assertTrue(accepted, failures)
                self.assertEqual(failures, [])

    def test_insufficient_integer_counts_fail(self):
        for value in ("0", "4", "399"):
            with self.subTest(value=value):
                accepted, failures = self.check_count(value)
                self.assertFalse(accepted)
                self.assertTrue(any("at least 400" in f for f in failures))

    def test_malformed_counts_fail(self):
        for value in ("", "-400", "+400", "4.00", "400.0", "4e2", "NaN", "Infinity",
                      "1,000", "4_000", "200 + 200", "400 controls", "400 # counted",
                      "400 or 500", "４００", "٤٠٠"):
            with self.subTest(value=value[:80]):
                accepted, failures = self.check_count(value)
                self.assertFalse(accepted)
                self.assertTrue(any("unsigned decimal integer" in f for f in failures))



class SourcePlaceholders(Base):
    """C/C++ sources may contain <word_word> tokens such as #include <unordered_map> (reported in pull request #8)."""

    def _confirmed(self):
        self.attack(levels=("partial_win_claim", "negative"))
        panel(os.path.join(self.R, "panel"))
        w(os.path.join(self.W, "REPORT.md"), "# Report\nHeadline: CONFIRMED_PARTIAL on toy-record.\n")
        return self.package()

    def test_cpp_include_is_not_a_placeholder(self):
        P = self._confirmed()
        w(os.path.join(P, "how-we-built-it", "search.cpp"), "#include <unordered_map>\n#include <unordered_set>\nint main(){return 0;}\n")
        self.sums(P)
        self.assertPass(self.W)

    def test_placeholder_in_document_still_fails(self):
        P = self._confirmed()
        w(os.path.join(P, "HOW_WE_FOUND_IT.md"), "Contributor text, unverified. Built by <credit_name>.\n")
        self.sums(P)
        self.assertFail("unfilled placeholder <credit_name>", self.W)

if __name__ == "__main__":
    unittest.main(verbosity=1)

