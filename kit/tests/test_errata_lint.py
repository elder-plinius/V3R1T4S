# SPDX-License-Identifier: AGPL-3.0-or-later
"""Tests for kit/errata_lint.py, the pre-push hook and check_run.py errata mode. Standard library only.

    python3 kit/tests/test_errata_lint.py
"""
import contextlib, hashlib, io, os, shutil, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
sys.path.insert(0, KIT)
import check_run  # noqa: E402
import errata_lint  # noqa: E402

HEX = "cd" * 32
README = """# Toy table: posted file does not certify the posted value for N = 7 (data-integrity erratum)

| | |
|---|---|
| **Claim** | Dated observation: the posted coordinates for N = 7 give r* below the table value. |
| **One-command repro** | `sh verify-it-yourself/run_checks.sh`. Expected last line: `PASS`. |
| **Not claimed** | No record and no new packing. Not a CONFIRMED_PARTIAL p3 win. |
| **Confidence** | High; deterministic. |

## Sources
See SOURCES.csv (URL, sha256, date only).

## Credits
- Toy table: https://example.org/table
"""
REPRO = "print('N=7 r* below table')\nprint('PASS')\n"


def w(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb" if isinstance(data, bytes) else "w") as f:
        f.write(data)


def sums(pkg):
    lines = []
    for d, _, files in os.walk(pkg):
        for f in files:
            p = os.path.join(d, f)
            r = os.path.relpath(p, pkg).replace(os.sep, "/")
            if r != "SHA256SUMS":
                lines.append("%s  %s" % (hashlib.sha256(errata_lint._rb(p)).hexdigest(), r))
    w(os.path.join(pkg, "SHA256SUMS"), "\n".join(sorted(lines, key=lambda l: l[66:])) + "\n")


def lean(pkg, repro=REPRO):
    w(os.path.join(pkg, "README.md"), README)
    w(os.path.join(pkg, "PR_BODY.md"), README)
    w(os.path.join(pkg, "SOURCES.csv"), "url,sha256,last_modified,fetched_utc,used_for\n"
      "https://example.org/t/radius.txt,%s,\"Thu, 15 Oct 2026 12:05:12 GMT\",2026-10-17T02:15:13Z,table\n" % HEX)
    w(os.path.join(pkg, "RUN_IT_YOURSELF.md"), "# Run it yourself\n    sh verify-it-yourself/run_checks.sh\n")
    w(os.path.join(pkg, "HOW_WE_FOUND_IT.md"), "# How we found it (contributor text, unverified)\n1. A sweep.\n")
    w(os.path.join(pkg, "verify-it-yourself", "run_checks.sh"),
      "#!/bin/sh\ncd \"$(dirname \"$0\")/..\" && exec python3 verify-it-yourself/repro.py \"$@\"\n")
    w(os.path.join(pkg, "verify-it-yourself", "repro.py"), repro)
    w(os.path.join(pkg, "how-we-built-it", "sweep.py"), "print('sweep')\n")
    w(os.path.join(pkg, "object", "errata_cells.csv"), "N,table,rstar,gap\n7,0.5,0.49,-0.01\n")
    w(os.path.join(pkg, "fixtures", "toy7.txt"), "".join("%d %.6f %.6f %.6f\n" % (i, i * .1, i * .2, i * .3) for i in range(1, 8)))
    sums(pkg)


def quiet(fn, *a, **k):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        rc = fn(*a, **k)
    return rc, out.getvalue()


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="errata_lint_test_")
        self.P = os.path.join(self.tmp, "2026-10-18-tester-aaaaaaaa")
        lean(self.P)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def lint(self, path=None):
        return quiet(errata_lint.main, [path or self.P])

    def add(self, rel, data, resum=True):
        w(os.path.join(self.P, rel), data)
        if resum:
            sums(self.P)

    def assertBlocked(self, needle, rel=None):
        rc, out = self.lint()
        self.assertEqual(rc, 1, out)
        self.assertIn("ERRATA_LINT: FAIL", out)
        line = [l for l in out.splitlines() if l.startswith("FAIL:") and needle in l and (rel is None or rel in l)]
        self.assertTrue(line, "expected a FAIL line with %r for %r in:\n%s" % (needle, rel, out))
        return out


class LintPositive(Base):
    def test_clean_lean_package_passes(self):
        rc, out = self.lint()
        self.assertEqual(rc, 0, out)
        self.assertTrue(out.strip().endswith("ERRATA_LINT: PASS (11 files in 1 errata package)"), out)

    def test_jargon_false_positives_pass(self):
        self.add("README.md", README + "\n## Notes\nA promising lead, still pending; confirmed by the maintainer. "
                 "The THRESHOLD and the HOLDER, Moe's table, panel data and a hold-out set are fine. "
                 "This is not a CONFIRMED_PARTIAL claim; it is never CONFIRMED.\nThe record held for ten years.\n")
        rc, out = self.lint()
        self.assertEqual(rc, 0, out)

    def test_coordinate_rows_allowed_under_fixtures(self):
        self.add("fixtures/big.txt", "".join("%d %.9f %.9f %.9f\n" % (i, i * .1, i * .2, i * .3) for i in range(400)))
        self.assertEqual(self.lint()[0], 0)

    def test_tree_with_known_knowns_layout(self):
        tree = os.path.join(self.tmp, "tree")
        dest = os.path.join(tree, "known-knowns", "toy-family", os.path.basename(self.P))
        shutil.copytree(self.P, dest)
        rc, out = self.lint(tree)
        self.assertEqual(rc, 0, out)
        w(os.path.join(tree, "TROPHY_CASE.md"), "edited\n")
        rc, out = self.lint(tree)
        self.assertEqual(rc, 1)
        self.assertIn("TROPHY_CASE.md: outside any known-knowns", out)


class LintBlocked(Base):
    def test_pending_md(self):
        self.add("PENDING.md", "notes\n")
        self.assertBlocked("blocked: internal filing note (PENDING.md)", "PENDING.md")

    def test_pending_md_in_subfolder(self):
        self.add("panel/PENDING.md", "notes\n")
        self.assertBlocked("blocked:", "panel/PENDING.md")

    def test_placement_md(self):
        self.add("PLACEMENT.md", "where to file\n")
        self.assertBlocked("PLACEMENT.md", "PLACEMENT.md")

    def test_panel_folders(self):
        for rel in ("panel/reproduce.md", "panel-evidence/novelty/fetch_log.tsv", "panel-scripts/criterion/x.py"):
            self.add(rel, "seat\n")
        out = self.assertBlocked("internal panel folder")
        for rel in ("panel/reproduce.md", "panel-evidence/novelty/fetch_log.tsv", "panel-scripts/criterion/x.py"):
            self.assertIn("FAIL: %s: blocked: internal panel folder" % rel, out)

    def test_gate_md(self):
        self.add("how-we-built-it/gate.md", "status: x\n")
        self.assertBlocked("honesty-gate", "gate.md")

    def test_not_allowlisted(self):
        self.add("novelty-evidence/FETCH_LOG.md", "urls\n")
        self.assertBlocked("not on the errata allowlist", "novelty-evidence/FETCH_LOG.md")

    def test_not_allowlisted_extension(self):
        self.add("object/page.html", "<p>x</p>\n")
        self.assertBlocked("not on the errata allowlist", "object/page.html")

    def test_jargon_panel_status(self):
        self.add("README.md", README + "\nPanel status: reproduce PASS\n")
        self.assertBlocked("'Panel status' text", "README.md")

    def test_jargon_confirmed_asserted(self):
        self.add("README.md", README + "\nstatus: CONFIRMED_PARTIAL\n")
        self.assertBlocked("CONFIRMED*", "README.md")

    def test_jargon_promising(self):
        self.add("how-we-built-it/CLAIM.md", "status: PROMISING\n")
        self.assertBlocked("PROMISING", "how-we-built-it/CLAIM.md")

    def test_jargon_moe(self):
        self.add("README.md", README + "\nheld for review by moe\n")
        self.assertBlocked("'moe'", "README.md")

    def test_jargon_need_human_pending_hold(self):
        for word in ("NEED-HUMAN", "PENDING STATUS CHECK", "HOLD", "ERRATUM-READY", "Expected FAIL"):
            lean(self.P)
            self.add("object/notes.md", "label: %s\n" % word)
            self.assertBlocked("internal", "object/notes.md")

    def test_jargon_in_code_and_seat_lines(self):
        self.add("how-we-built-it/sweep.py", "# run by SuperProtoBot\nprint(1)\n")
        self.assertBlocked("fleet seat name", "sweep.py")
        lean(self.P)
        self.add("verify-it-yourself/RECEIPTS.md", "verdict: NEED-HUMAN\npass: false\n")
        self.assertBlocked("verdict", "RECEIPTS.md")

    def test_reference_to_internal_file(self):
        self.add("README.md", README + "\nThe 14-row sample in panel/criterion.md lies inside this bound.\n")
        self.assertBlocked("references internal file 'panel/'", "README.md")

    def test_data_dump_size(self):
        self.add("object/radius_copy.csv", "N,r\n" + "".join("%d,0.%012d\n" % (i, i) for i in range(5000)))
        self.assertBlocked("copied data dump", "object/radius_copy.csv")

    def test_data_dump_coordinate_rows(self):
        self.add("how-we-built-it/ssp1055.txt", "".join("%.12f %.12f %.12f\n" % (i * .1, i * .2, i * .3) for i in range(120)))
        self.assertBlocked("coordinate-style number rows", "ssp1055.txt")

    def test_html_page(self):
        self.add("the-record-we-beat/SNAPSHOT.md", "<!DOCTYPE html><html><body>table</body></html>\n")
        self.assertBlocked("HTML page", "SNAPSHOT.md")

    def test_over_1mb_and_binary(self):
        self.add("how-we-built-it/big.txt", "x" * 1_000_001)
        self.assertBlocked("larger than 1 MB", "big.txt")
        lean(self.P)
        self.add("how-we-built-it/blob.json", b"\0\1\2binary")
        self.assertBlocked("binary file", "blob.json")

    def test_oversized_fixture(self):
        self.add("fixtures/huge.txt", "1 0.1 0.2 0.3\n" * 20000)
        self.assertBlocked("fixture larger", "fixtures/huge.txt")

    def test_leaks_from_check_run(self):
        self.add("RUN_IT_YOURSELF.md", "cd /tmp/work && sh run.sh\nmail someone@private-mail.net\n")
        out = self.assertBlocked("temporary-folder path", "RUN_IT_YOURSELF.md")
        self.assertIn("email address", out)

    def test_stale_sha256sums(self):
        self.add("panel/novelty.md", "seat\n")
        os.remove(os.path.join(self.P, "panel", "novelty.md"))
        os.rmdir(os.path.join(self.P, "panel"))
        self.assertBlocked("lists panel/novelty.md, which is not in the package", "SHA256SUMS")
        self.add("object/extra.csv", "N\n1\n", resum=False)
        self.assertBlocked("does not list object/extra.csv", "SHA256SUMS")

    def test_record_package_is_skipped(self):
        rec = os.path.join(self.tmp, "rec")
        w(os.path.join(rec, "README.md"), "# A record\n## What\nx\n")
        w(os.path.join(rec, "panel", "gate.md"), "status: CONFIRMED_PARTIAL\nconfirmed_scope: one cell.\n")
        rc, out = self.lint(rec)
        self.assertEqual(rc, 0, out)
        self.assertIn("SKIP:", out)


def git(repo, *args):
    return subprocess.run(["git", "-C", repo] + list(args), check=True, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE).stdout.decode().strip()


@unittest.skipUnless(shutil.which("git"), "git not installed")
class GitModeAndHook(Base):
    def setUp(self):
        super().setUp()
        self.G = os.path.join(self.tmp, "clone")
        os.makedirs(self.G)
        git(self.G, "init", "-q", "-b", "main")
        git(self.G, "config", "user.email", "t@example.com")
        git(self.G, "config", "user.name", "t")
        w(os.path.join(self.G, "README.md"), "repo\n")
        git(self.G, "add", "-A")
        git(self.G, "commit", "-q", "-m", "base")
        self.base = git(self.G, "rev-parse", "HEAD")
        git(self.G, "switch", "-q", "-c", "claim/x")
        self.pkg = os.path.join(self.G, "known-knowns", "toy", os.path.basename(self.P))
        shutil.copytree(self.P, self.pkg)
        git(self.G, "add", "-A")
        git(self.G, "commit", "-q", "-m", "erratum")

    def glint(self, spec, *extra):
        return quiet(errata_lint.main, ["--repo", self.G, "--git", spec] + list(extra))

    def hook(self, rsha=None):
        head = git(self.G, "rev-parse", "HEAD")
        line = "refs/heads/claim/x %s refs/heads/claim/x %s\n" % (head, rsha or self.base)
        r = subprocess.run(["sh", os.path.join(KIT, "hooks", "pre-push"), "origin", "https://example.org/x.git"],
                           cwd=self.G, input=line.encode(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return r.returncode, r.stdout.decode()

    def test_git_range_clean(self):
        rc, out = self.glint(self.base + "..HEAD")
        self.assertEqual(rc, 0, out)
        rc, out = self.glint("main")
        self.assertEqual(rc, 0, out)

    def test_git_range_blocks_pending_and_lints_whole_package(self):
        w(os.path.join(self.pkg, "PENDING.md"), "x\n")
        git(self.G, "add", "-A")
        git(self.G, "commit", "-q", "-m", "oops")
        prev = git(self.G, "rev-parse", "HEAD~1")
        rc, out = self.glint(prev + "..HEAD")   # only PENDING.md changed; the whole package at HEAD is linted
        self.assertEqual(rc, 1, out)
        self.assertIn("PENDING.md: blocked", out)
        self.assertIn("SHA256SUMS: does not list PENDING.md", out)

    def test_git_range_stray_file(self):
        w(os.path.join(self.G, "TROPHY_CASE.md"), "mine\n")
        git(self.G, "add", "-A")
        git(self.G, "commit", "-q", "-m", "stray")
        rc, out = self.glint("main")
        self.assertEqual(rc, 1)
        self.assertIn("TROPHY_CASE.md: outside any known-knowns", out)

    def test_only_if_errata_skips_non_package_push(self):
        git(self.G, "switch", "-q", "-c", "kit/y", "main")
        w(os.path.join(self.G, "kit.md"), "x\n")
        git(self.G, "add", "-A")
        git(self.G, "commit", "-q", "-m", "kit")
        rc, out = self.glint("main", "--only-if-errata")
        self.assertEqual(rc, 0)
        self.assertIn("ERRATA_LINT: SKIP", out)

    def test_hook_passes_clean_and_blocks_bad(self):
        rc, out = self.hook()
        self.assertEqual(rc, 0, out)
        self.assertIn("ERRATA_LINT: PASS", out)
        rc, out = self.hook(rsha="0" * 40)          # new remote branch: base = merge base with main
        self.assertEqual(rc, 0, out)
        w(os.path.join(self.pkg, "panel", "gate.md"), "status: PROMISING\n")
        git(self.G, "add", "-A")
        git(self.G, "commit", "-q", "-m", "leak")
        rc, out = self.hook()
        self.assertEqual(rc, 1, out)
        self.assertIn("panel/gate.md: blocked", out)
        self.assertIn("BLOCKED by kit/errata_lint.py", out)


class CheckRunErrataMode(Base):
    def cr(self, *argv):
        return quiet(check_run.main, list(argv))

    def test_auto_detected_errata_passes_without_panel(self):
        rc, out = self.cr("--package", self.P)
        self.assertEqual(rc, 0, out)
        self.assertIn("errata mode", out)
        self.assertIn("run_checks.sh prints PASS from a clean copy", out)
        self.assertFalse([l for l in out.splitlines() if l.startswith("FAIL")], out)
        self.assertNotRegex(out, r"(?i)expected fail")
        self.assertTrue(out.strip().endswith("CHECK_RUN: PASS"), out)

    def test_explicit_flag_and_lint_failures(self):
        self.add("PENDING.md", "x\n")
        rc, out = self.cr("--package", self.P, "--errata", "--no-exec")
        self.assertEqual(rc, 1)
        self.assertIn("errata lint: PENDING.md: blocked", out)

    def test_record_flag_keeps_record_behaviour(self):
        rc, out = self.cr("--package", self.P, "--record", "--no-exec")
        self.assertEqual(rc, 1)
        self.assertIn("required folder panel/ missing or empty", out)
        self.assertNotIn("errata mode", out)

    def test_non_errata_package_still_record_mode(self):
        self.add("README.md", README.replace("(data-integrity erratum)", "(new value)"))
        self.add("PR_BODY.md", README.replace("(data-integrity erratum)", "(new value)"))
        rc, out = self.cr("--package", self.P, "--no-exec")
        self.assertEqual(rc, 1)
        self.assertNotIn("errata mode", out)
        self.assertIn("panel", out)

    def test_lean_body_required(self):
        self.add("README.md", "# Toy (data-integrity erratum)\n## Claim\nx\n")
        rc, out = self.cr("--package", self.P, "--no-exec")
        self.assertEqual(rc, 1)
        for what in ("One-command repro", "Not claimed", "Confidence"):
            self.assertIn("lacks a '%s'" % what, out)

    def test_sources_required(self):
        os.remove(os.path.join(self.P, "SOURCES.csv"))
        sums(self.P)
        rc, out = self.cr("--package", self.P, "--no-exec")
        self.assertEqual(rc, 1)
        self.assertIn("needs SOURCES.csv", out)

    def test_repro_fail_and_replaced_upstream(self):
        lean(self.P, repro="print('FAIL N=7')\nraise SystemExit(1)\n")
        rc, out = self.cr("--package", self.P)
        self.assertEqual(rc, 1)
        self.assertIn("its repro did not pass", out)
        lean(self.P, repro="print('REPLACED UPSTREAM (N=7)')\n")
        rc, out = self.cr("--package", self.P)
        self.assertEqual(rc, 0, out)
        self.assertIn("WARN", out)
        self.assertIn("dated observation", out)


if __name__ == "__main__":
    unittest.main(verbosity=1)
