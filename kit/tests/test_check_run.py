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


def w(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text)


def panel(d, gate_status="CONFIRMED_PARTIAL", contexts=("subagent", "subagent", "subagent"), passes=(True, True, True), scope="one cell, exactly as reproduced."):
    for role, ctx, ok in zip(check_run.PANEL, contexts, passes):
        w(os.path.join(d, role + ".md"), "# %s\ncontext: %s\nchecked %s independently.\n%spass: %s\n"
          % (role, ctx, role, ("confirmed_scope: %s\n" % scope) if role == "criterion" else "", "true" if ok else "false"))
    w(os.path.join(d, "gate.md"), "status: %s\nconfirmed_scope: %s\n" % (gate_status, scope))


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
        w(os.path.join(R, "data", "status.html"), "<p>open</p>\n")
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
            w(os.path.join(A, "report.md"), "claim level: %s\n%s" % (lv, dead))
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
        w(os.path.join(P, "verify-it-yourself", "run_checks.sh"), "python3 verify-it-yourself/check.py\n")
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
        panel(os.path.join(self.W, "private", "toy-cipher", "panel"), scope="key reproduces the ciphertext.")
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


class PackageBoundaries(Base):
    def symlink(self, target, link, directory=False):
        try:
            os.symlink(target, link, target_is_directory=directory)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks unavailable")

    def assertUnsafeWithoutReads(self, P, needle):
        # An unsafe entry must be rejected before reading any package data or
        # workspace settings, hashing files, or starting the package checker.
        with mock.patch.object(check_run, "read", side_effect=AssertionError("unexpected read")), \
                mock.patch.object(check_run, "rbytes", side_effect=AssertionError("unexpected hash read")), \
                mock.patch.object(check_run, "run_own_checker", side_effect=AssertionError("unexpected execution")):
            self.assertFail(needle, "--package", P, "--workdir", self.W)

    def test_regular_package_still_passes(self):
        self.assertPass("--package", self.package(), "--workdir", self.W)

    def test_file_symlink_rejected_before_reads(self):
        P = self.package()
        outside = os.path.join(self.tmp, "outside.txt")
        w(outside, "synthetic external content\n")
        self.symlink(outside, os.path.join(P, "external.txt"))
        self.assertUnsafeWithoutReads(P, "symbolic links are not allowed")

    def test_directory_symlink_rejected_before_reads(self):
        P = self.package()
        outside = os.path.join(self.tmp, "outside")
        w(os.path.join(outside, "fixture.txt"), "synthetic external content\n")
        self.symlink(outside, os.path.join(P, "external"), directory=True)
        self.assertUnsafeWithoutReads(P, "symbolic links are not allowed")

    def test_dangling_symlink_rejected_before_reads(self):
        P = self.package()
        self.symlink(os.path.join(self.tmp, "does-not-exist"), os.path.join(P, "dangling"))
        self.assertUnsafeWithoutReads(P, "symbolic links are not allowed")

    def test_package_root_symlink_rejected_before_reads(self):
        P = self.package()
        link = os.path.join(self.tmp, "linked-package")
        self.symlink(P, link, directory=True)
        self.assertUnsafeWithoutReads(link, "symbolic links are not allowed")

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFOs unavailable")
    def test_fifo_rejected_before_reads(self):
        P = self.package()
        os.mkfifo(os.path.join(P, "pipe.txt"))
        self.assertUnsafeWithoutReads(P, "unsupported file type")

    def test_hidden_directory_is_hashed_and_scanned(self):
        P = self.package()
        w(os.path.join(P, ".github", "fixture.txt"), "synthetic marker gh" + "p_" + "A" * 36 + "\n")
        self.assertFail(".github/fixture.txt is not listed", "--package", P, "--no-exec")
        self.assertIn("GitHub token", self.out)

    def test_hashed_hidden_directory_is_allowed(self):
        P = self.package()
        w(os.path.join(P, ".github", "notes.txt"), "public reproduction notes\n")
        self.sums(P)
        self.assertPass("--package", P)

    def test_hidden_file_size_is_checked(self):
        P = self.package()
        w(os.path.join(P, ".github", "large.bin"), "x" * 1_000_001)
        self.sums(P)
        self.assertFail(".github/large.bin is larger than 1 MB", "--package", P, "--no-exec")

    def test_plain_text_pem_private_key_marker_is_scanned(self):
        P = self.package()
        w(os.path.join(P, "how-we-built-it", "synthetic.pem"),
          "-----BEGIN PRIVATE KEY-----\nSYNTHETIC_NON_SECRET_FIXTURE\n-----END PRIVATE KEY-----\n")
        self.sums(P)
        self.assertFail("private key in how-we-built-it/synthetic.pem", "--package", P, "--no-exec")

    def test_unknown_text_extension_never_publish_is_scanned(self):
        P = self.package()
        w(os.path.join(P, "how-we-built-it", "notes.custom"), "Placeholder Realname\n")
        self.sums(P)
        self.assertFail("never_publish", "--package", P, "--workdir", self.W, "--no-exec")

    def envelope(self):
        P = os.path.join(self.W, "outbox", "sealed")
        w(os.path.join(self.R, "target.md"), "id: toy-cipher\n")
        panel(os.path.join(self.R, "panel"))
        w(os.path.join(P, "envelope.md"), "# Sealed envelope sealed\ntarget: toy-cipher\nproblem: Problem 7\n"
          "| file | frozen (UTC) | commitment |\n|---|---|---|\n"
          "| solution file 1 (key) | 2026-10-12T03:14:15Z | `%s` |\n" % HEX)
        return P

    def test_sealed_envelope_directory_and_file_still_pass(self):
        P = self.envelope()
        self.assertPass("--package", P, "--workdir", self.W)
        self.assertPass("--package", os.path.join(P, "envelope.md"), "--workdir", self.W)

    def test_nested_envelope_is_an_extra_file(self):
        P = self.envelope()
        w(os.path.join(P, "nested", "envelope.md"), "synthetic unsealed solution\n")
        self.assertFail("envelope.md only; found nested/envelope.md", "--package", P, "--workdir", self.W)

    def test_hidden_envelope_extra_file_is_rejected(self):
        P = self.envelope()
        w(os.path.join(P, ".github", "notes.txt"), "synthetic unsealed solution\n")
        self.assertFail("envelope.md only; found .github/notes.txt", "--package", P, "--workdir", self.W)

    def test_standalone_envelope_symlink_rejected_before_reads(self):
        P = self.envelope()
        link = os.path.join(self.tmp, "linked-envelope.md")
        self.symlink(os.path.join(P, "envelope.md"), link)
        self.assertUnsafeWithoutReads(link, "symbolic links are not allowed")

    def test_manifest_cannot_reference_outside_package(self):
        P = self.package()
        outside = os.path.join(os.path.dirname(P), "outside.txt")
        w(outside, "public synthetic fixture\n")
        with open(os.path.join(P, "SHA256SUMS"), "a") as f:
            f.write("%s  ../outside.txt\n" % hashlib.sha256(check_run.rbytes(outside)).hexdigest())
        self.assertFail("SHA256SUMS path leaves the package", "--package", P, "--no-exec")

    def test_unsafe_package_is_not_read_again_by_workspace_secret_scan(self):
        self.attack()
        P = self.package()
        outside = os.path.join(self.tmp, "outside.txt")
        w(outside, "synthetic external fixture\n")
        link = os.path.join(P, "external.txt")
        self.symlink(outside, link)
        w(os.path.join(self.W, "private", "toy-cipher", "plaintext.txt"), PLAINTEXT)
        original_is_text = check_run.is_text
        def guarded_is_text(path, *args, **kwargs):
            self.assertNotEqual(path, link, "workspace scanner revisited rejected package symlink")
            return original_is_text(path, *args, **kwargs)
        with mock.patch.object(check_run, "is_text", side_effect=guarded_is_text):
            self.assertFail("symbolic links are not allowed", self.W)

    def test_confirmed_workspace_does_not_read_index_symlink_before_preflight(self):
        self.attack(levels=("partial_win_claim", "negative"))
        panel(os.path.join(self.R, "panel"))
        P = self.package()
        outside = os.path.join(self.tmp, "outside-index.csv")
        w(outside, "target_id\ntoy-record\n")
        link = os.path.join(P, "INDEX.csv")
        os.remove(link)
        self.symlink(outside, link)
        original_read = check_run.read
        def guarded_read(path, *args, **kwargs):
            self.assertNotEqual(path, link, "confirmation presence check read unsafe package symlink")
            return original_read(path, *args, **kwargs)
        with mock.patch.object(check_run, "read", side_effect=guarded_read):
            self.assertFail("symbolic links are not allowed", self.W)

    def test_hidden_outbox_package_is_validated(self):
        self.attack()
        P = self.package(name=".hidden-package")
        w(os.path.join(P, "synthetic.pem"),
          "-----BEGIN PRIVATE KEY-----\nSYNTHETIC_NON_SECRET_FIXTURE\n-----END PRIVATE KEY-----\n")
        self.assertFail("synthetic.pem is not listed", self.W, "--no-exec")
        self.assertIn("private key in synthetic.pem", self.out)

    def test_valid_hidden_outbox_package_passes(self):
        self.attack()
        self.package(name=".hidden-package")
        self.assertPass(self.W)

    def test_hidden_outbox_directory_symlink_is_rejected(self):
        self.attack()
        P = self.package()
        outside = os.path.join(self.tmp, "outside-package")
        shutil.move(P, outside)
        link = os.path.join(self.W, "outbox", ".hidden-package")
        self.symlink(outside, link, directory=True)
        self.assertFail("symbolic links are not allowed", self.W)

    def test_hidden_outbox_file_symlink_is_not_read(self):
        self.attack()
        os.makedirs(os.path.join(self.W, "outbox"), exist_ok=True)
        outside = os.path.join(self.tmp, "outside.txt")
        w(outside, "synthetic external fixture\n")
        link = os.path.join(self.W, "outbox", ".hidden.txt")
        self.symlink(outside, link)
        w(os.path.join(self.W, "private", "toy-cipher", "plaintext.txt"), PLAINTEXT)
        original_is_text = check_run.is_text
        def guarded_is_text(path, *args, **kwargs):
            self.assertNotEqual(path, link, "workspace scanner opened an unsupported outbox symlink")
            return original_is_text(path, *args, **kwargs)
        with mock.patch.object(check_run, "is_text", side_effect=guarded_is_text):
            self.assertFail("outbox holds only package folders", self.W)

    def test_hidden_regular_outbox_files_are_skipped(self):
        self.attack()
        os.makedirs(os.path.join(self.W, "outbox"), exist_ok=True)
        with open(os.path.join(self.W, "outbox", ".DS_Store"), "wb") as f:
            f.write(b"\x00\x00\x00\x01Bud1" + b"\x00" * 64)
        w(os.path.join(self.W, "outbox", ".notes.txt"), "synthetic local note\n")
        self.assertPass(self.W)

    def test_hidden_regular_outbox_file_is_still_secret_scanned(self):
        self.attack()
        w(os.path.join(self.W, "private", "toy-cipher", "plaintext.txt"), PLAINTEXT)
        w(os.path.join(self.W, "outbox", ".notes.txt"), PLAINTEXT + "\n")
        self.assertFail("outbox/.notes.txt contains text from", self.W)

    def test_nonaffirmative_checker_terminal_lines_fail(self):
        for terminal in ("NOT PASS", "PASS: 0", "BYPASS", "PASS FAIL"):
            with self.subTest(terminal=terminal):
                P = self.package()
                w(os.path.join(P, "verify-it-yourself", "run_checks.sh"), "printf '%s\\n'\n" % terminal)
                self.sums(P)
                self.assertFail("did not pass from a clean copy", "--package", P)


class ConfirmationGates(Base):
    def test_duplicate_gate_fields_rejected(self):
        P = self.package()
        for extra in ("status: NOTHING", "status: CONFIRMED_PARTIAL",
                      "confirmed_scope: a different claim"):
            with self.subTest(extra=extra):
                panel(os.path.join(P, "panel"))
                path = os.path.join(P, "panel", "gate.md")
                w(path, check_run.read(path) + extra + "\n")
                self.sums(P)
                self.assertFail("duplicate critical field", "--package", P)

    def test_duplicate_panel_decisions_rejected(self):
        P = self.package()
        for fields in ("novelty: complete\nnovelty: PENDING STATUS CHECK\n",
                       "context: same session\n"):
            with self.subTest(fields=fields):
                w(os.path.join(P, "panel", "novelty.md"),
                  "context: subagent\n" + fields + "pass: true\n")
                self.sums(P)
                self.assertFail("duplicate critical field", "--package", P)

    def test_only_final_pass_line_decides(self):
        # Published panels quote checker transcripts and prose ("Pass: the object meets ...").
        # As on main, only the last nonempty line is the verdict; earlier "pass:" lines are not.
        P = self.package()
        quoted = ("Pass: the object meets the stated criterion.\n"
                  "```\n$ sh verify-it-yourself/run_checks.sh\npass: true\nPASS: all saved-object checks\n```\n"
                  "    pass: true\n")
        scope = "confirmed_scope: one cell, exactly as reproduced.\n"
        for role in check_run.PANEL:
            for body, final, ok in ((quoted, "pass: true", True), ("pass: false\n", "pass: true", True),
                                    (quoted, "pass: false", False)):
                with self.subTest(role=role, body=body[:12], final=final):
                    panel(os.path.join(P, "panel"))
                    w(os.path.join(P, "panel", role + ".md"), "# %s\ncontext: subagent\n%s%s%s\n"
                      % (role, scope if role == "criterion" else "", body, final))
                    self.sums(P)
                    if ok:
                        self.assertPass("--package", P, "--no-exec")
                        self.assertNotIn("duplicate critical field", self.out)
                    else:
                        self.assertFail("%s.md does not end with 'pass: true'" % role, "--package", P, "--no-exec")

    def test_duplicate_null_decisions_rejected(self):
        path = os.path.join(self.R, "null_test.md")
        base = ("controls: 400\nbest_control: 0.4\nreal: 0.9\n"
                "real_beats_all_controls: yes\ncommand: python3 null.py\n")
        for extra in ("controls: 4", "best_control: 1.0", "real: 0.1",
                      "real_beats_all_controls: no", "command: another.py"):
            with self.subTest(extra=extra):
                w(path, base + extra + "\n")
                c = check_run.Checker(quiet=True)
                self.assertFalse(check_run.check_null(c, path, "fixture"))
                self.assertTrue(any("duplicate critical field" in x for x in c.fails))

    def test_duplicate_prereg_null_decision_rejected(self):
        self.attack()
        path = os.path.join(self.R, "PREREG.md")
        w(path, check_run.read(path) + "null_test: required\n")
        self.assertFail("duplicate critical field 'null_test'", self.W)

    def test_duplicate_noncritical_metadata_remains_compatible(self):
        P = self.package()
        for filename in ("gate.md", "novelty.md"):
            path = os.path.join(P, "panel", filename)
            w(path, "note: first source\nnote: second source\n" + check_run.read(path))
        self.sums(P)
        self.assertPass("--package", P)

    def test_envelope_rejects_duplicate_gate_decision(self):
        w(os.path.join(self.R, "target.md"), "id: toy-cipher\n")
        panel(os.path.join(self.R, "panel"))
        path = os.path.join(self.R, "panel", "gate.md")
        w(path, check_run.read(path) + "status: NOTHING\n")
        self.assertFalse(check_run.find_confirmed_gate(self.W, "toy-cipher"))

    def test_empty_or_failed_status_cannot_confirm(self):
        self.attack(levels=("partial_win_claim", "negative"))
        panel(os.path.join(self.R, "panel"))
        self.package()
        digest = hashlib.sha256(b"<p>open</p>\n").hexdigest()
        for status in ("", "status: 403\ncontrols: 200", "http_status: 429",
                       "HTTP/2 503", "HTTP 301", "controls: 200"):
            with self.subTest(status=status):
                w(os.path.join(self.R, "scout.md"),
                  ("url: https://example.org/table\nsha256: %s\n%s\n" % (digest, status)) if status else "")
                self.assertFail("requires a completed status/table check", self.W)

    def test_explicit_successful_http_formats(self):
        self.attack()
        digest = hashlib.sha256(b"<p>open</p>\n").hexdigest()
        for status in ("status: 200", "http_status: 200 OK", "HTTP/2 200", "HTTP 200", "HTTP status: 200"):
            with self.subTest(status=status):
                w(os.path.join(self.R, "scout.md"), "url: https://example.org/table\nsha256: %s\n%s\n" % (digest, status))
                self.assertPass(self.W)

    def test_explicit_http_field_takes_precedence_over_generic_status(self):
        self.attack()
        digest = hashlib.sha256(b"<p>open</p>\n").hexdigest()
        for fields, ok in (("status: open\nhttp_status: 200", True), ("status: open\nhttp_code: 200", True),
                           ("http_status: 200 OK\nstatus: open", True), ("status: open\nhttp_status: 404", False),
                           ("status: 200\nhttp_status: 503", False), ("status: open", False)):
            with self.subTest(fields=fields):
                w(os.path.join(self.R, "scout.md"), "url: https://example.org/table\nsha256: %s\n%s\n" % (digest, fields))
                if ok:
                    self.assertPass(self.W)
                else:
                    self.assertFail("scout.md needs the status source's URL, HTTP status and page sha256", self.W)

    def test_confirmed_run_accepts_http_status_next_to_target_status(self):
        self.attack(levels=("partial_win_claim", "negative"))
        panel(os.path.join(self.R, "panel"))
        self.package()
        digest = hashlib.sha256(b"<p>open</p>\n").hexdigest()
        w(os.path.join(self.R, "scout.md"), "url: https://example.org/table\nstatus: open\nhttp_status: 200\nsha256: %s\n" % digest)
        self.assertPass(self.W, "--no-exec")
        self.assertIn("CONFIRMED status backed by three panel files", self.out)

    def test_nonexact_confirmed_gate_status_warns(self):
        self.attack(levels=("partial_win_claim", "negative"))
        for status in ("CONFIRMED_PARTIAL (pending table check)", "NOT_CONFIRMED_SOLUTION",
                       "confirmed_partial", "CONFIRMED_"):
            with self.subTest(status=status):
                panel(os.path.join(self.R, "panel"), gate_status=status)
                self.assertPass(self.W)
                self.assertIn("is not exactly CONFIRMED_SOLUTION or CONFIRMED_PARTIAL", self.out)
                self.assertIn("claim present, not confirmed", self.out)

    def test_exact_or_unconfirmed_gate_status_does_not_warn(self):
        self.attack(levels=("partial_win_claim", "negative"))
        panel(os.path.join(self.R, "panel"), gate_status="PROMISING")
        self.assertPass(self.W)
        self.assertNotIn("is not exactly CONFIRMED_", self.out)
        panel(os.path.join(self.R, "panel"))
        self.package()
        self.assertPass(self.W, "--no-exec")
        self.assertNotIn("is not exactly CONFIRMED_", self.out)
        self.assertIn("CONFIRMED status backed by three panel files", self.out)

    def test_pending_novelty_cannot_confirm_package(self):
        P = self.package()
        for status in ("PENDING STATUS CHECK", "pending   table check"):
            with self.subTest(status=status):
                w(os.path.join(P, "panel", "novelty.md"),
                  "context: subagent\nnovelty: %s\npass: true\n" % status)
                self.sums(P)
                self.assertFail("novelty.md reports a pending", "--package", P)

    def test_pending_status_blocks_confirmation(self):
        self.attack(levels=("partial_win_claim", "negative"))
        panel(os.path.join(self.R, "panel"))
        self.package()
        for status in ("PENDING STATUS CHECK", "PENDING TABLE CHECK", "pending   status check"):
            with self.subTest(status=status):
                w(os.path.join(self.R, "scout.md"), status + "\n")
                self.assertFail("requires a completed status/table check", self.W)

    def test_pending_status_allows_unconfirmed_run(self):
        self.attack()
        w(os.path.join(self.R, "scout.md"), "PENDING STATUS CHECK\n")
        self.assertPass(self.W)

    def test_package_requires_exact_confirmed_status(self):
        P = self.package()
        for status in ("NOT_CONFIRMED_PARTIAL", "CONFIRMED_SOLUTION_RETRACTED",
                       "not CONFIRMED_PARTIAL", "PROMISING"):
            with self.subTest(status=status):
                panel(os.path.join(P, "panel"), gate_status=status)
                self.sums(P)
                self.assertFail("not CONFIRMED_*", "--package", P)

    def test_envelope_cannot_use_negated_confirmation(self):
        w(os.path.join(self.R, "target.md"), "id: toy-cipher\n")
        panel(os.path.join(self.R, "panel"), gate_status="NOT_CONFIRMED_SOLUTION")
        self.assertFalse(check_run.find_confirmed_gate(self.W, "toy-cipher"))

    def test_package_rejects_failed_required_null_test(self):
        bank = {"targets": [{"id": "toy-record", "category": "undeciphered-scripts",
                             "disclosure": "open"}]}
        w(os.path.join(self.W, "repo", "bank", "targets.json"), json.dumps(bank))
        P = self.package()
        for verdict in ("no", "false"):
            with self.subTest(verdict=verdict):
                w(os.path.join(P, "how-we-built-it", "null_test.md"),
                  "controls: 400\nbest_control: 0.9\nreal: 0.4\n"
                  "real_beats_all_controls: %s\ncommand: python3 null.py\n" % verdict)
                self.sums(P)
                self.assertFail("requires a passing null test", "--package", P, "--workdir", self.W)

    def test_package_accepts_passing_required_null_test(self):
        bank = {"targets": [{"id": "toy-record", "category": "undeciphered-scripts",
                             "disclosure": "open"}]}
        w(os.path.join(self.W, "repo", "bank", "targets.json"), json.dumps(bank))
        P = self.package()
        w(os.path.join(P, "how-we-built-it", "null_test.md"),
          "controls: 400\nbest_control: 0.4\nreal: 0.9\n"
          "real_beats_all_controls: yes\ncommand: python3 null.py\n")
        self.sums(P)
        self.assertPass("--package", P, "--workdir", self.W)


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

