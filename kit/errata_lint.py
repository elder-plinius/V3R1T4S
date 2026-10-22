#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""V3R1T4S errata whitelist lint. Python 3.8+, standard library only.

An erratum package ships only the lean set: the note/body, the one-command repro, the sources (URL + sha256 +
date) and minimal fixtures. Anything else is internal scaffolding and must not leave the machine. See
kit/ERRATA-LINT.md for the rationale and the meaning of every rule.

  python3 kit/errata_lint.py DIR                  one package folder, or a tree holding known-knowns/<family>/<id>/
  python3 kit/errata_lint.py --git BASE..HEAD     every package the commits BASE..HEAD touch (full package at HEAD)
  python3 kit/errata_lint.py --git BASE           same as BASE...HEAD (changes since the merge base)
      [--repo PATH]  git repository (default: current directory)
      [--only-if-errata]  exit 0 quietly when the range touches no known-knowns/ package (used by the pre-push hook)

Last line: "ERRATA_LINT: PASS (...)" or "ERRATA_LINT: FAIL (<n> problems in <m> files)". Exit status 0, 1, or 2 (usage).
"""
import argparse, fnmatch, hashlib, os, re, subprocess, sys

# =====================================================================================================
# CONFIG: the errata allowlist. Keep this small; every entry is a file the lean errata PRs actually ship
# (#311 and #333, both reviewed as "exactly what we asked for") or that kit/SUBMIT.md section 1 names.
# =====================================================================================================
ALLOWED_TOP_FILES = {
    "README.md",            # the erratum note: Claim, One-command repro, Not claimed, Confidence, Sources, Credits
    "PR_BODY.md",           # the PR body (usually identical to README.md)
    "SOURCES.csv",          # url, sha256, last_modified, fetched_utc, used_for (no third-party bytes)
    "NOT_CLAIMED.md",       # optional separate not-claimed note
    "SHA256SUMS",           # sha256 of every other file
    "RUN_IT_YOURSELF.md",   # exact commands for the repro
    "HOW_WE_FOUND_IT.md",   # short account, marked "contributor text, unverified"
    "INDEX.csv",            # one row per erratum cell (optional for errata)
}
TEXT_EXTS = {".py", ".sh", ".md", ".txt", ".csv", ".tsv", ".json"}
ALLOWED_DIRS = {                                   # folder -> allowed file extensions (any depth below it)
    "verify-it-yourself": TEXT_EXTS,               # run_checks.sh, the repro script, CLAIM.json, RECEIPTS.md
    "how-we-built-it": TEXT_EXTS,                  # the code that found it, its dated output, PREREG.md
    "object": {".csv", ".tsv", ".json", ".txt", ".md"},   # the erratum cells / file lists we derived
    "the-record-we-beat": {".md", ".txt", ".csv", ".json"},  # snapshot: URL, fetch time, status, sha256 only
    "fixtures": TEXT_EXTS,                         # minimal fixtures for the repro
}
FIXTURE_DIRS = ("fixtures/", "verify-it-yourself/fixtures/", "how-we-built-it/fixtures/")

# Blocked names: checked on every path component (case-insensitive glob). Reason shown on failure.
BLOCKED_NAMES = [
    ("panel*", "internal panel folder/file (panel*, panel-evidence, panel-scripts); errata are not panel-gated"),
    ("pending*", "internal filing note (PENDING.md)"),
    ("placement*", "internal filing note (PLACEMENT.md)"),
    ("gate.md", "internal honesty-gate file (gate.md)"),
    ("check_run_output*", "internal check_run transcript"),
    ("open-facts*", "internal maintainer-facts note (OPEN-FACTS.md)"),
    ("_archive", "internal archive folder"),
    (".ds_store", "editor/OS junk"),
]

# Internal jargon: case-sensitive, whole words, so ordinary prose ("promising", "pending", "confirmed by the
# maintainer", "threshold", "Moe") never trips it. CONFIRMED* is allowed when directly negated
# ("not a CONFIRMED_PARTIAL p3 win" is the maintainer's own requested wording, #206/#311).
JARGON = [
    (r"\b[Pp]anel status\b", "'Panel status' text"),
    (r"\bCONFIRMED(?:_PARTIAL|_SOLUTION)?\b", "internal gate status CONFIRMED*"),
    (r"\bPROMISING\b", "internal hold status PROMISING"),
    (r"\bNEED-HUMAN\b", "panel verdict NEED-HUMAN"),
    (r"\bPENDING\b", "internal status PENDING (PENDING STATUS/TABLE CHECK)"),
    (r"\bERRATUM-READY\b", "internal errata status ERRATUM-READY"),
    (r"\bHOLD\b", "internal errata status HOLD"),
    (r"\b[Ee]xpected FAIL\b", "check_run 'expected FAIL' chatter"),
    (r"\bmoe\b", "internal owner name 'moe' (filing notes like 'held ... for moe')"),
    (r"(?m)^\s*pass:\s*(?:true|false)\s*$", "panel seat verdict line 'pass: true/false'"),
    (r"(?m)^\s*verdict:\s*(?:PASS|FAIL|TIE|NEED-HUMAN)\b", "panel seat verdict line"),
    (r"\binjection_suspected\b", "internal run note injection_suspected"),
    (r"\b(?:RanPi|Botministrator|botministrator|botmin|Bot-Admin|SuperProtoBot|SPB|el-Gringo|TiHQ|Hephaestus|"
     r"Prototyper|Errand Boy|Ops Desk|BotOps)\b|R\u00aa\u207f\u00de\u00a1", "internal fleet seat name"),
]
NEGATED_BEFORE = re.compile(r"(?i)\b(?:not|no|never|nor|without)\b(?:\W+\w+){0,2}\W*$")
INTERNAL_REF = re.compile(r"(?i)(?<![\w-])(?:panel[\w-]*/|(?:PENDING|PLACEMENT|gate)\.md\b)")
HTML_PAGE = re.compile(r"(?i)<!doctype\s+html|<html[\s>]|<body[\s>]")
NUM = r"[-+]?(?:\d+\.\d*|\.\d+)(?:[eEdD][-+]?\d+)?"
COORD_ROW = re.compile(r"^\s*(?:\[?\d+\]?[\s:]+)?%s(?:\s+%s)+\s*$" % (NUM, NUM))  # whitespace number rows (x y z)
DATA_EXTS = {".txt", ".csv", ".tsv", ".json", ".dat", ".xyz"}

FILE_MAX = 1_000_000        # any file (kit/SUBMIT.md section 1)
PACKAGE_MAX = 50_000_000    # whole package (kit/SUBMIT.md section 1)
DATA_CAP = 64_000           # a data/text file outside fixtures/ larger than this looks like a copied dump
FIXTURE_CAP = 256_000       # a single fixture file
DUMP_ROWS = 50              # >= this many coordinate-style rows (and >= half the lines) outside fixtures/
# =====================================================================================================

PKG_RE = re.compile(r"^known-knowns/[^/]+/[^/]+(?=/)")
ZERO = "0" * 40


def _leak_patterns():
    here = os.path.dirname(os.path.abspath(__file__))
    if here not in sys.path:
        sys.path.insert(0, here)
    try:
        import check_run
        return check_run.LEAK_RES, check_run.EMAIL_RE, check_run.EMAIL_OK
    except Exception:  # pragma: no cover - check_run ships next to this file
        return [], re.compile(r"$^"), re.compile(r"$^")


class Package:
    """name, files: {relpath: (size, getter)}, where getter() returns bytes."""

    def __init__(self, name):
        self.name, self.files = name, {}


def _rb(path):
    with open(path, "rb") as f:
        return f.read()


def from_dir(root):
    pkg = Package(os.path.basename(os.path.abspath(root)))
    for d, dirs, files in os.walk(root):
        dirs[:] = sorted(x for x in dirs if x != ".git")
        for f in sorted(files):
            p = os.path.join(d, f)
            r = os.path.relpath(p, root).replace(os.sep, "/")
            pkg.files[r] = (os.path.getsize(p), (lambda p=p: _rb(p)))
    return pkg


def is_record(pkg):
    """A record package (panel-confirmed gate, not titled as an erratum) is out of scope for this lint."""
    gate = pkg.files.get("panel/gate.md")
    if not gate or not re.search(rb"(?m)^\s*status:\s*`?CONFIRMED_(SOLUTION|PARTIAL)", gate[1]()):
        return False
    for f in ("README.md", "PR_BODY.md"):
        if f in pkg.files:
            first = pkg.files[f][1]().decode("utf-8", "replace").strip().splitlines()[:1]
            if first and re.search(r"(?i)errat", first[0]):
                return False
    return True


def allowed(path):
    parts = path.split("/")
    if len(parts) == 1:
        return path in ALLOWED_TOP_FILES
    top, ext = parts[0], os.path.splitext(path)[1].lower()
    if top in ALLOWED_DIRS:
        return ext in ALLOWED_DIRS[top] or os.path.basename(path) == "SHA256SUMS"
    return False


def jargon_hits(text):
    hits = []
    for rx, what in JARGON:
        for m in re.finditer(rx, text):
            if what.startswith("internal gate status"):
                ls = text.rfind("\n", 0, m.start()) + 1
                if NEGATED_BEFORE.search(text[ls:m.start()]):
                    continue
            hits.append((text.count("\n", 0, m.start()) + 1, m.group(0).strip(), what))
            break
    return hits


def lint_package(pkg):
    """Returns a list of (relpath, reason). An empty list means the package passes."""
    leak_res, email_re, email_ok = _leak_patterns()
    probs, total = [], 0
    for path in sorted(pkg.files):
        size, get = pkg.files[path]
        total += size
        blocked = None
        for comp in path.split("/"):
            for pat, why in BLOCKED_NAMES:
                if fnmatch.fnmatch(comp.lower(), pat):
                    blocked = why
                    break
            if blocked:
                break
        if blocked:
            probs.append((path, "blocked: " + blocked))
            continue
        if not allowed(path):
            probs.append((path, "not on the errata allowlist (see ALLOWED_TOP_FILES / ALLOWED_DIRS in kit/errata_lint.py)"))
            continue
        if size > FILE_MAX:
            probs.append((path, "larger than 1 MB (%d bytes)" % size))
            continue
        data = get()
        if b"\0" in data[:8192]:
            probs.append((path, "binary file; errata ship text only"))
            continue
        text = data.decode("utf-8", "replace")
        in_fix = path.startswith(FIXTURE_DIRS)
        ext = os.path.splitext(path)[1].lower()
        if in_fix and size > FIXTURE_CAP:
            probs.append((path, "fixture larger than %d bytes; fixtures must be minimal" % FIXTURE_CAP))
        elif not in_fix and ext in DATA_EXTS and size > DATA_CAP:
            probs.append((path, "data file larger than %d bytes outside fixtures/ (copied data dump?)" % DATA_CAP))
        if HTML_PAGE.search(text):
            probs.append((path, "contains an HTML page (copied third-party page?); keep only URL, sha256 and date"))
        if not in_fix:
            lines = [l for l in text.splitlines() if l.strip()]
            rows = sum(1 for l in lines if COORD_ROW.match(l))
            if rows >= DUMP_ROWS and rows * 2 >= len(lines):
                probs.append((path, "%d coordinate-style number rows (copied upstream data?); ship URL + sha256, or a "
                                    "minimal file under fixtures/" % rows))
        for ln, word, what in jargon_hits(text):
            probs.append((path, "internal jargon %s ('%s', line %d)" % (what, word[:40], ln)))
        m = INTERNAL_REF.search(text)
        if m:
            probs.append((path, "references internal file '%s' (line %d)" % (m.group(0), text.count("\n", 0, m.start()) + 1)))
        for rx, what in leak_res:
            m = rx.search(text)
            if m:
                probs.append((path, "%s (line %d)" % (what, text.count("\n", 0, m.start()) + 1)))
        for m in email_re.finditer(text):
            if not email_ok.search(m.group(0)):
                probs.append((path, "email address (line %d)" % (text.count("\n", 0, m.start()) + 1)))
                break
    if total > PACKAGE_MAX:
        probs.append(("(package)", "package larger than 50 MB (%d bytes)" % total))
    if "SHA256SUMS" in pkg.files:
        listed = {}
        for line in pkg.files["SHA256SUMS"][1]().decode("utf-8", "replace").splitlines():
            m = re.match(r"^([0-9a-f]{64})\s+\*?(.+)$", line.strip())
            if m:
                listed[os.path.normpath(m.group(2).strip().lstrip("./")).replace(os.sep, "/")] = m.group(1)
        for r, h in sorted(listed.items()):
            if r not in pkg.files:
                probs.append(("SHA256SUMS", "lists %s, which is not in the package (regenerate SHA256SUMS)" % r))
            elif hashlib.sha256(pkg.files[r][1]()).hexdigest() != h:
                probs.append(("SHA256SUMS", "sha256 mismatch for %s" % r))
        for r in sorted(pkg.files):
            if r != "SHA256SUMS" and r not in listed:
                probs.append(("SHA256SUMS", "does not list %s" % r))
    return probs


# ---------- inputs ----------

def packages_from_tree(root):
    """A package folder itself, or every known-knowns/<family>/<id>/ under a tree. Returns (packages, stray)."""
    kk = os.path.join(root, "known-knowns")
    if not os.path.isdir(kk):
        return [from_dir(root)], []
    pkgs, stray = [], []
    for fam in sorted(os.listdir(kk)):
        fd = os.path.join(kk, fam)
        if not os.path.isdir(fd):
            stray.append("known-knowns/" + fam)
            continue
        for sid in sorted(os.listdir(fd)):
            sd = os.path.join(fd, sid)
            if os.path.isdir(sd):
                p = from_dir(sd)
                p.name = "known-knowns/%s/%s" % (fam, sid)
                pkgs.append(p)
            else:
                stray.append("known-knowns/%s/%s" % (fam, sid))
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x != ".git" and os.path.join(d, x) != kk]
        stray += [os.path.relpath(os.path.join(d, f), root).replace(os.sep, "/") for f in files]
    return pkgs, stray


def git(repo, *args):
    return subprocess.run(["git", "-C", repo] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          check=True).stdout


def packages_from_git(repo, spec):
    """Touched packages (full tree at HEAD side) and changed paths outside any package."""
    if "..." in spec:
        base, head = spec.split("...", 1)
        diff = [base + "..." + (head or "HEAD")]
        head = head or "HEAD"
    elif ".." in spec:
        base, head = spec.split("..", 1)
        head = head or "HEAD"
        diff = [base, head]
    else:
        base, head = spec, "HEAD"
        diff = [base + "...HEAD"]
    if base.strip("0") == "":   # new branch with no remote base: everything reachable is outgoing
        names = git(repo, "ls-tree", "-r", "-z", "--name-only", head).decode().split("\0")
    else:
        names = git(repo, "diff", "--name-only", "-z", "--no-renames", *diff).decode().split("\0")
    names = [n for n in names if n]
    roots, stray = set(), []
    for n in names:
        m = PKG_RE.match(n)
        if m:
            roots.add(m.group(0))
        else:
            stray.append(n)
    pkgs = []
    for root in sorted(roots):
        p = Package(root)
        out = git(repo, "ls-tree", "-r", "-z", "--long", head, "--", root + "/").decode()
        for ent in out.split("\0"):
            if not ent:
                continue
            meta, path = ent.split("\t", 1)
            _mode, typ, sha, size = meta.split()
            if typ != "blob":
                continue
            p.files[path[len(root) + 1:]] = (int(size), (lambda sha=sha: git(repo, "cat-file", "blob", sha)))
        pkgs.append(p)
    return pkgs, stray, bool(roots)


def main(argv=None):
    ap = argparse.ArgumentParser(description="V3R1T4S errata whitelist lint (kit/errata_lint.py)")
    ap.add_argument("path", nargs="?", help="package folder, or a tree holding known-knowns/<family>/<id>/")
    ap.add_argument("--git", metavar="RANGE", help="BASE..HEAD, BASE...HEAD or BASE (= BASE...HEAD)")
    ap.add_argument("--repo", default=".", help="git repository for --git (default: .)")
    ap.add_argument("--only-if-errata", action="store_true", help="exit 0 if the range touches no known-knowns/ package")
    a = ap.parse_args(argv)
    if bool(a.path) == bool(a.git):
        ap.print_help()
        return 2
    if a.git:
        try:
            pkgs, stray, touched = packages_from_git(a.repo, a.git)
        except subprocess.CalledProcessError as e:
            print("ERRATA_LINT: ERROR git: %s" % e.stderr.decode("utf-8", "replace").strip()[:200])
            return 2
        if not touched and a.only_if_errata:
            print("ERRATA_LINT: SKIP (no known-knowns/ package in %s)" % a.git)
            return 0
    else:
        if not os.path.isdir(a.path):
            print("ERRATA_LINT: ERROR %s is not a folder" % a.path)
            return 2
        pkgs, stray = packages_from_tree(a.path)
    problems = [(s, "outside any known-knowns/<family>/<id>/ package (an erratum changes nothing else)") for s in stray]
    linted = 0
    if len(pkgs) > 1:
        problems.append(("(push)", "%d packages in one change set; one erratum package per PR" % len(pkgs)))
    for p in pkgs:
        if is_record(p):
            print("SKIP: %s is a panel-confirmed record package; use check_run.py --package" % p.name)
            continue
        linted += 1
        for path, why in lint_package(p):
            problems.append(("%s/%s" % (p.name, path) if len(pkgs) > 1 or a.git else path, why))
    for path, why in problems:
        print("FAIL: %s: %s" % (path, why))
    nfiles = sum(len(p.files) for p in pkgs)
    if problems:
        print("ERRATA_LINT: FAIL (%d problems in %d files)" % (len(problems), len({p for p, _ in problems})))
        return 1
    print("ERRATA_LINT: PASS (%d files in %d errata package%s)" % (nfiles, linted, "" if linted == 1 else "s"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
