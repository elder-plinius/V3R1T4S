#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""V3R1T4S mechanical gate. Python 3.8+, standard library only.

An agent runs this before it reports a claim, packages one, or ends a run. It checks files, never science:
a PASS means the paperwork is honest and complete, not that the result is true.

  python3 check_run.py WORKDIR                 end of a run: setup, latest run, outbox, private-secret leaks
  python3 check_run.py WORKDIR --setup         end of setup (after the dry run)
  python3 check_run.py WORKDIR --run RUN_DIR   a specific run folder instead of the latest
  python3 check_run.py --package DIR [--workdir WORKDIR] [--no-exec]   one outbox package or sealed envelope

Last line: "CHECK_RUN: PASS" or "CHECK_RUN: FAIL (<n> problems)". Exit status 0 or 1.
"""
import argparse, calendar, csv, hashlib, io, json, os, re, shutil, stat, subprocess, sys, tempfile

TEXT_EXT = {".md", ".txt", ".json", ".csv", ".log", ".tsv", ".yaml", ".yml", ""}
CODE_EXT = {".py", ".sh", ".c", ".h", ".js", ".ipynb", ".rs", ".go", ".java", ".jl", ".r", ".cpp", ".hpp"}
MAX_SCAN = 2_000_000
SETTINGS_KEYS = ["credit", "github", "curious_about", "effort", "schedule", "publish_charter", "memory",
                 "capabilities", "agent_run", "repo_tag", "repo_commit", "tag_signature"]
PANEL = ["reproduce", "novelty", "criterion"]
NULL_CATEGORIES = {"unbroken-ciphers", "undeciphered-scripts"}
CONFIRMED_RE = re.compile(r"CONFIRMED_(SOLUTION|PARTIAL)")
CONFIRMED_STATUSES = {"CONFIRMED_SOLUTION", "CONFIRMED_PARTIAL"}
PENDING_CHECK_RE = re.compile(r"\bPENDING\s+(?:STATUS|TABLE)\s+CHECK\b", re.IGNORECASE)
NEGATION_RE = re.compile(r"(?i)\b(not|no|never|without|nor|cannot|can't|isn't|aren't|wasn't|unless|until|only|may|"
                         r"would|could|should|requires?|if|before|instead|neither|none|nothing|downgraded|zero)\b|n't\b")
PLACEHOLDER_RE = re.compile(r"<(WORKDIR|[A-Za-z]+(?:[-_][A-Za-z]+)+|YYYY[^>]{0,20}|date|time|tag|id|lens|credit|"
                            r"value|url|family|n|path|name)>")
# Source code legitimately contains <word_word> tokens (e.g. C++ #include <unordered_map>), so it is exempt from the
# placeholder check; documents, data and receipts are not.
SOURCE_EXTS = (".py", ".sh", ".c", ".cc", ".cpp", ".cxx", ".h", ".hh", ".hpp", ".hxx", ".rs", ".go", ".jl", ".java")
LEAK_RES = [
    (re.compile(r"/" r"Users/[^/\s'\"`)]+"), "absolute macOS user path"),
    (re.compile(r"/" r"home/[^/\s'\"`)]+"), "absolute Linux home path"),
    (re.compile(r"(?i)[A-Z]:\\Users\\"), "absolute Windows user path"),
    (re.compile(r"/" r"private/(?:var|tmp)/"), "temporary-folder path"),
    (re.compile(r"(?<![\w.])/" r"tmp/"), "temporary-folder path"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}"), "GitHub token"),
    (re.compile(r"\bgithub" r"_pat_[A-Za-z0-9_]{20,}"), "GitHub token"),
    (re.compile(r"\bsk-[A-Za-z0-9_-]{20,}"), "API key"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS key"),
    (re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}"), "Slack token"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key"),
]
EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
EMAIL_OK = re.compile(r"(?i)@(users\.noreply\.github\.com|example\.(com|org|net))$")
SETTLED_RE = re.compile(r"(?i)\b(settles?|settled|exhaustive(ly)?|proof|proved|proves|complete search)\b")
DEAD_OK = re.compile(r"(?i)\W*(solved|off-limits|off limits|unreachable|overtaken|record moved|out of reach|withdrawn|closed)")
DEAD_BAD = re.compile(r"(?i)budget|time|early|smoke|test|light|commit-only|effort|skip|harness|constraint")
ENVELOPE_LABELS = "key|settings|decryption|plaintext|verification output|other"


class Checker:
    def __init__(self, quiet=False):
        self.fails, self.warns, self.quiet = [], [], quiet

    def say(self, msg):
        if not self.quiet:
            print(msg)

    def fail(self, msg):
        self.fails.append(msg)
        self.say("FAIL: " + msg)

    def warn(self, msg):
        self.warns.append(msg)
        self.say("WARN: " + msg)

    def ok(self, msg):
        self.say("ok:   " + msg)

    def finish(self):
        if self.fails:
            print("CHECK_RUN: FAIL (%d problems)" % len(self.fails))
            return 1
        print("CHECK_RUN: PASS" + (" (%d warnings)" % len(self.warns) if self.warns else ""))
        return 0


# ---------- helpers ----------

def rbytes(path):
    with open(path, "rb") as f:
        return f.read()


def wbytes(path, data):
    with open(path, "wb") as f:
        f.write(data)


def read(path, limit=MAX_SCAN):
    """Text of a file as UTF-8, with CRLF line endings folded to LF (hashes use rbytes, not this)."""
    try:
        with open(path, "rb") as f:
            return f.read(limit).decode("utf-8", "replace").replace("\r\n", "\n")
    except OSError:
        return ""


def is_text(path, require_known_extension=True):
    ext = os.path.splitext(path)[1].lower()
    if require_known_extension and ext not in TEXT_EXT and ext not in CODE_EXT:
        return False
    try:
        with open(path, "rb") as f:
            return b"\0" not in f.read(4096)
    except OSError:
        return False


def walk(root, skip_dirs=()):
    for d, dirs, files in os.walk(root):
        dirs[:] = sorted(x for x in dirs if x not in skip_dirs and not x.startswith(".git"))
        for f in sorted(files):
            yield os.path.join(d, f)


def regular_file_no_follow(path):
    """True for a regular file, judged by lstat (a symbolic link is never a regular file here)."""
    try:
        return stat.S_ISREG(os.lstat(path).st_mode)
    except OSError:
        return False


def rel(path, base):
    try:
        return os.path.relpath(path, base)
    except ValueError:
        return path


def kv(text):
    out = {}
    for line in text.splitlines():
        m = re.match(r"^\s*[-*]?\s*`?([A-Za-z_][A-Za-z0-9_ ]*?)`?\s*:\s*(.*?)\s*$", line)
        if m:
            out.setdefault(m.group(1).strip().lower().replace(" ", "_"), m.group(2).strip().strip("`*"))
    return out


def last_nonempty(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    return lines[-1] if lines else ""


def critical_kv(c, text, label, keys):
    """Retain ordinary metadata parsing, but reject repeated decision fields."""
    seen = set()
    for line in text.splitlines():
        for key in kv(line):
            if key in keys:
                if key in seen:
                    c.fail("%s: duplicate critical field '%s'" % (label, key))
                seen.add(key)
    return kv(text)


def successful_http_status(text):
    """Read explicit HTTP evidence, never incidental numbers elsewhere in a scout.

    http_status/http_code fields take precedence: when present, a generic 'status:' field
    (often the target's own status, such as 'open') is not read as HTTP evidence."""
    explicit, generic = [], []
    for line in text.splitlines():
        d = kv(line)
        explicit.extend(d[k] for k in ("http_status", "http_code") if k in d)
        if "status" in d:
            generic.append(d["status"])
    named = explicit or generic
    if named:
        codes = [re.fullmatch(r"([0-9]{3})(?:\s+[A-Za-z][A-Za-z -]*)?", value) for value in named]
        return all(m and 200 <= int(m.group(1)) < 300 for m in codes)
    codes = re.findall(r"\bHTTP(?:/[0-9.]+)?\s+(?:(?:status|code)\s*:\s*)?([0-9]{3})\b",
                       text, re.IGNORECASE)
    return bool(codes) and all(200 <= int(code) < 300 for code in codes)


def load_bank(workdir, settings, errors=None):
    """First readable bank among the candidates. A candidate that exists but cannot be read or
    parsed is appended to `errors` (if given) so the caller can fail loudly instead of running
    without the bank's guards."""
    paths = []
    if settings.get("bank"):
        b = settings["bank"].split()[0]
        paths.append(b if os.path.isabs(b) else os.path.join(workdir or ".", b))
    if workdir:
        paths.append(os.path.join(workdir, "repo", "bank", "targets.json"))
    here = os.path.dirname(os.path.abspath(__file__))
    paths.append(os.path.join(here, "..", "bank", "targets.json"))
    for p in paths:
        try:
            with open(p, encoding="utf-8") as f:
                data = json.load(f)
            return {t["id"]: t for t in data.get("targets", [])}, os.path.dirname(os.path.abspath(p))
        except FileNotFoundError:
            continue
        except (OSError, ValueError, KeyError, TypeError, AttributeError) as e:
            if errors is not None:
                errors.append("%s: %s: %s" % (p, type(e).__name__, str(e)[:120]))
            continue
    return {}, None


def confirmed_mentions(path):
    """Lines that assert a CONFIRMED_* status (mentions after a negation word on the same line are ignored)."""
    hits = []
    for i, line in enumerate(read(path).splitlines(), 1):
        for m in CONFIRMED_RE.finditer(line):
            if not NEGATION_RE.search(line[:m.start()]):
                hits.append((i, line.strip()[:120]))
                break
    return hits


def check_panel_scope(c, panel_dir, gate_path, label):
    """Bind the chosen CRITERION scope to the authoritative gate's parsed value."""
    before = len(c.fails)
    source = critical_kv(c, read(os.path.join(panel_dir, "criterion.md")),
                         "%s: criterion.md" % label, {"confirmed_scope"})
    gate = critical_kv(c, read(gate_path), "%s: gate.md" % label, {"confirmed_scope"})
    expected = source.get("confirmed_scope", "")
    actual = gate.get("confirmed_scope", "")
    if not expected:
        c.fail("%s: criterion.md has no nonempty confirmed_scope" % label)
    if not actual:
        c.fail("%s: gate.md has no nonempty confirmed_scope" % label)
    if expected and actual and expected != actual:
        c.fail("%s: gate.md confirmed_scope differs from criterion.md" % label)
    return len(c.fails) == before


def check_panel(c, panel_dir, label, require_confirmed=True):
    """Three panel files with context and pass: true, plus gate.md. Returns True if all good."""
    good = True
    texts = []
    gate_dirs = [panel_dir]
    for role in PANEL:
        p = os.path.join(panel_dir, role + ".md")
        if not os.path.isfile(p):
            c.fail("%s: panel file %s missing (only a three-skeptic panel can confirm)" % (label, rel(p, panel_dir + "/..")))
            good = False
            continue
        t = read(p)
        texts.append(t)
        before = len(c.fails)
        # The verdict is the file's final line alone (checked below). Earlier "pass:" lines, such as
        # transcripts in code blocks or prose like "Pass: the object meets ...", are not decisions.
        fields = critical_kv(c, t, "%s: %s.md" % (label, role), {"context", "novelty"})
        if len(c.fails) != before:
            good = False
        if last_nonempty(t).lower().replace(" ", "") != "pass:true":
            c.fail("%s: %s.md does not end with 'pass: true'" % (label, role))
            good = False
        ctx = fields.get("context", "")
        if role == "novelty" and PENDING_CHECK_RE.search(fields.get("novelty", "")):
            c.fail("%s: novelty.md reports a pending status/table check" % label)
            good = False
        if not ctx:
            c.fail("%s: %s.md has no 'context:' line saying how this fresh skeptic was started" % (label, role))
            good = False
        elif re.search(r"(?i)same (session|context)|role-?play|single[- ]context|myself|main session", ctx):
            c.fail("%s: %s.md context '%s' is not a fresh context" % (label, role, ctx[:60]))
            good = False
    if len(texts) == 3 and len(set(t.strip() for t in texts)) < 3:
        c.fail("%s: panel files are identical copies" % label)
        good = False
    gate = os.path.join(panel_dir, "gate.md")
    if require_confirmed:
        before = len(c.fails)
        g = critical_kv(c, read(gate), "%s: gate.md" % label, {"status", "confirmed_scope"}) if os.path.isfile(gate) else {}
        if len(c.fails) != before:
            good = False
        st = g.get("status", "")
        if not os.path.isfile(gate):
            c.fail("%s: gate.md missing" % label)
            good = False
        elif st not in CONFIRMED_STATUSES:
            c.fail("%s: gate.md status is '%s', not CONFIRMED_*" % (label, st[:40]))
            good = False
        elif not g.get("confirmed_scope"):
            c.fail("%s: gate.md has no confirmed_scope line" % label)
            good = False
        if not check_panel_scope(c, panel_dir, gate, label):
            good = False
    return good


def check_null(c, path, label):
    if not os.path.isfile(path):
        c.fail("%s: null test required but %s is missing (>= 400 controls through the same pipeline)" % (label, os.path.basename(path)))
        return False
    before = len(c.fails)
    d = critical_kv(c, read(path), "%s: null_test.md" % label,
                    {"controls", "best_control", "real", "real_beats_all_controls", "command"})
    controls = d.get("controls", "")
    try:
        if not re.fullmatch(r"[0-9]+", controls):
            raise ValueError
        n = int(controls)
    except ValueError:
        c.fail("%s: null_test.md controls must be an unsigned decimal integer" % label)
        n = None
    good = len(c.fails) == before
    if n is None:
        good = False
    elif n < 400:
        c.fail("%s: null_test.md reports %d controls; at least 400 are required" % (label, n))
        good = False
    for k in ("best_control", "real", "command"):
        if not d.get(k):
            c.fail("%s: null_test.md lacks '%s:'" % (label, k))
            good = False
    beats = d.get("real_beats_all_controls", "").lower()
    if beats not in ("yes", "no", "true", "false"):
        c.fail("%s: null_test.md lacks 'real_beats_all_controls: yes|no'" % label)
        good = False
    return good and beats in ("yes", "true")


def leak_scan(c, root, label, never_publish=(), workdir=None, skip_prompt=True, files=None):
    user = os.environ.get("USER") or os.environ.get("USERNAME") or ""
    for p in walk(root) if files is None else files:
        r = rel(p, root)
        # Publication scans inspect text by content, including .pem and unknown suffixes.
        if not is_text(p, require_known_extension=False):
            continue
        t = read(p)
        for rx, what in LEAK_RES:
            m = rx.search(t)
            if m:
                c.fail("%s: %s in %s (line %d)" % (label, what, r, t[:m.start()].count("\n") + 1))
        for m in EMAIL_RE.finditer(t):
            if not EMAIL_OK.search(m.group(0)):
                c.fail("%s: email address in %s (line %d)" % (label, r, t[:m.start()].count("\n") + 1))
                break
        if workdir and workdir in t:
            c.fail("%s: the workspace's absolute path appears in %s" % (label, r))
        if not (skip_prompt and r.split(os.sep)[0] == "prompt") and PLACEHOLDER_RE.search(t) and not r.endswith(SOURCE_EXTS):
            c.fail("%s: unfilled placeholder %s in %s" % (label, PLACEHOLDER_RE.search(t).group(0), r))
        low = t.lower()
        for e in never_publish:
            if e.lower() in low:
                c.fail("%s: an entry of private/never_publish.txt appears in %s" % (label, r))
        if len(user) >= 4 and re.search(r"\b%s\b" % re.escape(user), t):
            c.warn("%s: your login name appears in %s; make sure it is not personal" % (label, r))


def never_publish_list(workdir):
    if not workdir:
        return []
    t = read(os.path.join(workdir, "private", "never_publish.txt"))
    return [l.strip() for l in t.splitlines() if len(l.strip()) >= 3 and not l.strip().startswith("#")]


# ---------- envelope ----------

def check_envelope(c, path, workdir=None, bank=None, files=None):
    label = "envelope %s" % os.path.basename(os.path.dirname(path)) if os.path.basename(path) == "envelope.md" else "envelope %s" % os.path.basename(path)
    t = read(path)
    rows, target, problem, title = 0, None, None, 0
    allowed_static = {"| file | frozen (UTC) | commitment |", "|---|---|---|"}
    row_re = re.compile(r"^\| solution file \d+ \((%s)\) \| \d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ \| `[0-9a-f]{64}` \|$" % ENVELOPE_LABELS)
    for i, line in enumerate(t.splitlines(), 1):
        s = line.rstrip()
        if not s.strip():
            continue
        if re.match(r"^# Sealed envelope [a-z0-9][a-z0-9-]*$", s):
            title += 1
        elif re.match(r"^target: [a-z0-9][a-z0-9-]*$", s):
            target = s.split(": ", 1)[1]
        elif re.match(r"^problem: [A-Za-z0-9 .#()-]{1,40}$", s):
            problem = s
        elif s in allowed_static:
            pass
        elif row_re.match(s):
            rows += 1
        else:
            c.fail("%s: line %d is not part of the sealed-envelope template (only hashes and labels may appear)" % (label, i))
    if title != 1 or not target or not problem or rows < 1:
        c.fail("%s: needs exactly one title, a target line, a problem line and at least one commitment row" % label)
    if bank and target and target not in bank:
        c.warn("%s: target %s is not in the bank" % (label, target))
    if bank and target in (bank or {}) and bank[target].get("disclosure") != "commit-only":
        c.warn("%s: target %s is not commit-only; open results are published as full packages" % (label, target))
    if workdir and target:
        if not find_confirmed_gate(workdir, target):
            c.fail("%s: no run in this workspace has a panel-confirmed gate for %s" % (label, target))
    leak_scan(c, os.path.dirname(path), label, never_publish_list(workdir), workdir, files=files)
    return target


def find_confirmed_gate(workdir, target):
    for run in sorted(os.listdir(os.path.join(workdir, "runs"))) if os.path.isdir(os.path.join(workdir, "runs")) else []:
        rd = os.path.join(workdir, "runs", run)
        target_check = Checker(quiet=True)
        tid = critical_kv(target_check, read(os.path.join(rd, "target.md")),
                          "target.md", {"id"}).get("id", "")
        if target_check.fails or tid != target:
            continue
        gate = os.path.join(rd, "panel", "gate.md")
        gate_check = Checker(quiet=True)
        fields = critical_kv(gate_check, read(gate), "gate.md", {"status", "confirmed_scope"})
        if not gate_check.fails and fields.get("status", "") in CONFIRMED_STATUSES:
            for pd in (os.path.join(rd, "panel"), os.path.join(workdir, "private", target, "panel")):
                if all(os.path.isfile(os.path.join(pd, r + ".md")) for r in PANEL):
                    sub = Checker(quiet=True)
                    check_panel(sub, pd, "x", require_confirmed=False)
                    check_panel_scope(sub, pd, gate, "x")
                    if not sub.fails:
                        return True
    return False


# ---------- package ----------

def package_inventory(c, root, label):
    """Inventory every entry without following links, before opening any package file.

    Packages contain only directories and regular files. This static preflight is not
    a sandbox or protection against concurrent filesystem changes or checker code.
    """
    files, dirs, pending = {}, set(), [root]
    invalid = False
    while pending:
        p = pending.pop()
        try:
            st = os.lstat(p)
        except OSError as e:
            c.fail("%s: cannot inspect %s (%s)" % (label, rel(p, root), e.strerror))
            invalid = True
            continue
        if stat.S_ISLNK(st.st_mode):
            c.fail("%s: symbolic links are not allowed: %s" % (label, rel(p, root)))
            invalid = True
        elif stat.S_ISREG(st.st_mode):
            files[p] = st.st_size
        elif stat.S_ISDIR(st.st_mode):
            dirs.add(p)
            try:
                with os.scandir(p) as entries:
                    pending.extend(sorted((entry.path for entry in entries), reverse=True))
            except OSError as e:
                c.fail("%s: cannot inspect directory %s (%s)" % (label, rel(p, root), e.strerror))
                invalid = True
        else:
            c.fail("%s: unsupported file type: %s (regular files and directories only)" % (label, rel(p, root)))
            invalid = True
    return (None, None) if invalid else (dict(sorted(files.items())), dirs)


def check_package(c, pkg, workdir=None, execute=True, timeout=900):
    pkg = os.path.abspath(pkg)
    label = "package %s" % os.path.basename(pkg)
    files, dirs = package_inventory(c, pkg, label)
    if files is None:
        return False
    for p, size in files.items():
        if size > 1_000_000:
            c.fail("%s: %s is larger than 1 MB (kit/SUBMIT.md section 1)" % (label, rel(p, pkg)))
    if sum(files.values()) > 50_000_000:
        c.fail("%s: package larger than 50 MB" % label)
    settings = kv(read(os.path.join(workdir, "settings.md"))) if workdir else {}
    bank_errors = []
    bank, _ = load_bank(workdir, settings, bank_errors)
    for e in bank_errors:
        c.fail("could not read the bank %s" % e)
    if not bank:
        c.warn("could not load the bank (settings.md 'bank:', repo/bank/targets.json or kit/../bank/targets.json); bank-based guards were skipped")
    if pkg in files and pkg.endswith(".md"):
        check_envelope(c, pkg, workdir, bank, files=files)
        return
    if pkg not in dirs:
        c.fail("%s: not a package directory or envelope .md" % label)
        return
    if os.path.join(pkg, "envelope.md") in files:
        extra = [rel(p, pkg) for p in files if rel(p, pkg) != "envelope.md"]
        if extra:
            c.fail("%s: a sealed-envelope package holds envelope.md only; found %s" % (label, ", ".join(extra[:5])))
        check_envelope(c, os.path.join(pkg, "envelope.md"), workdir, bank, files=files)
        return
    need_files = ["README.md", "RUN_IT_YOURSELF.md", "INDEX.csv", "HOW_WE_FOUND_IT.md", "SHA256SUMS",
                  "verify-it-yourself/run_checks.sh", "verify-it-yourself/RECEIPTS.md"]
    need_dirs = ["object", "verify-it-yourself", "how-we-built-it", "the-record-we-beat", "panel"]
    for f in need_files:
        if os.path.join(pkg, f) not in files:
            c.fail("%s: required file %s missing (kit/SUBMIT.md section 1)" % (label, f))
    for d in need_dirs:
        dp = os.path.join(pkg, d)
        if dp not in dirs or not any(p.startswith(dp + os.sep) for p in files):
            c.fail("%s: required folder %s/ missing or empty" % (label, d))
    vd = os.path.join(pkg, "verify-it-yourself")
    if vd in dirs and not any(p.startswith(vd + os.sep) and os.path.basename(p) not in ("run_checks.sh", "RECEIPTS.md") for p in files):
        c.fail("%s: verify-it-yourself/ has no checker besides run_checks.sh" % label)
    readme = read(os.path.join(pkg, "README.md"))
    for h in ("what", "check it yourself", "compared to", "not claimed", "credits"):
        if not re.search(r"(?im)^#+\s*%s\b" % re.escape(h), readme):
            c.fail("%s: README.md lacks a '## %s' section" % (label, h.title()))
    scope = kv(read(os.path.join(pkg, "panel", "gate.md"))).get("confirmed_scope", "")
    squash = lambda t: re.sub(r"[\s`*_>\"']+", " ", t).strip().lower()
    if scope and squash(scope) not in squash(readme):
        c.fail("%s: README.md must quote panel/gate.md's confirmed_scope word for word (under '## What')" % label)
    if "unverified" not in read(os.path.join(pkg, "HOW_WE_FOUND_IT.md")).lower():
        c.fail("%s: HOW_WE_FOUND_IT.md must be marked 'contributor text, unverified'" % label)
    target = None
    try:
        rows = list(csv.reader(io.StringIO(read(os.path.join(pkg, "INDEX.csv")))))
        if len(rows) < 2 or "target_id" not in rows[0]:
            c.fail("%s: INDEX.csv needs a header with target_id and one data row" % label)
        else:
            target = rows[1][rows[0].index("target_id")].strip()
    except (csv.Error, IndexError):
        c.fail("%s: INDEX.csv is not valid CSV" % label)
    rec_dir = os.path.join(pkg, "the-record-we-beat") + os.sep
    rec = " ".join(read(p) for p in files if p.startswith(rec_dir) and is_text(p))
    if not (re.search(r"https?://", rec) and re.search(r"\b[0-9a-f]{64}\b", rec) and re.search(r"\d{4}-\d\d-\d\dT\d\d:\d\d", rec)):
        c.fail("%s: the-record-we-beat/ needs the table URL, a UTC fetch time and the page's sha256" % label)
    if target and bank:
        t = bank.get(target)
        if t is None:
            c.warn("%s: target_id %s is not in the bank" % (label, target))
        elif t.get("disclosure") == "commit-only":
            c.fail("%s: %s is commit-only; it may leave the machine only as a sealed envelope" % (label, target))
        if t and (t.get("category") in NULL_CATEGORIES):
            nulls = [p for p in files if os.path.basename(p) == "null_test.md"]
            if not nulls:
                c.fail("%s: a %s claim needs null_test.md (>= 400 controls) in the package" % (label, t.get("category")))
            else:
                if not check_null(c, nulls[0], label):
                    c.fail("%s: a confirmed package requires a passing null test" % label)
    if os.path.isdir(os.path.join(pkg, "panel")):
        check_panel(c, os.path.join(pkg, "panel"), label)
    # sha256sums
    try:
        # Use the filesystem's lossless filename decoding, not read()'s UTF-8
        # replacement: distinct raw names must not collapse onto U+FFFD.
        with open(os.path.join(pkg, "SHA256SUMS"), "rb") as manifest:
            raw_sums = manifest.read(MAX_SCAN + 1)
        if len(raw_sums) > MAX_SCAN:
            c.fail("%s: SHA256SUMS exceeds the scan limit" % label)
            sums = ""
        else:
            sums = os.fsdecode(raw_sums)
    except OSError as e:
        c.fail("%s: cannot read SHA256SUMS (%s)" % (label, e.strerror))
        sums = ""
    listed = {}
    # Read physical records, not splitlines(): filenames can contain VT/FF or
    # Unicode separators. Preserve filename whitespace and GNU name escapes.
    for number, line in enumerate(sums.split("\n"), 1):
        line = line[:-1] if line.endswith("\r") else line
        if not line or line.startswith("#"):
            continue
        m = re.fullmatch(r"(\\?)([0-9a-fA-F]{64}) ([ *])(.+)", line)
        if not m:
            c.fail("%s: malformed SHA256SUMS record on line %d" % (label, number))
            continue
        name = m.group(4)
        if m.group(1):
            if not re.fullmatch(r"(?:[^\\]|\\[\\nr])*", name):
                c.fail("%s: invalid SHA256SUMS filename escape on line %d" % (label, number))
                continue
            name = re.sub(r"\\([\\nr])", lambda x: {"\\": "\\", "n": "\n", "r": "\r"}[x.group(1)], name)
        if "\0" in name:
            c.fail("%s: NUL in SHA256SUMS filename on line %d" % (label, number))
            continue
        if name == "-":
            c.fail("%s: SHA256SUMS '-' means stdin; use './-' for that filename" % label)
            continue
        r = os.path.normpath(name)
        if os.path.isabs(r) or r == os.pardir or r.startswith(os.pardir + os.sep):
            c.fail("%s: SHA256SUMS path leaves the package: %s" % (label, r))
        elif r == "SHA256SUMS":
            c.fail("%s: SHA256SUMS must not list itself" % label)
        elif r in listed:
            c.fail("%s: duplicate SHA256SUMS path: %s" % (label, r))
        else:
            # Preflight already rejected symlinks. Do not let normalization
            # invent a path such as missing/../README.md or README.md/.
            if not os.path.isfile(os.path.join(pkg, name)):
                c.fail("%s: SHA256SUMS filename does not resolve to a regular file: %s" % (label, name))
            listed[r] = m.group(2).lower()
    for p in files:
        r = os.path.normpath(rel(p, pkg))
        if r == "SHA256SUMS":
            continue
        try:
            h = hashlib.sha256(rbytes(p)).hexdigest()
        except OSError as e:
            c.fail("%s: cannot read %s (%s)" % (label, r, e.strerror))
            continue
        if r not in listed:
            c.fail("%s: %s is not listed in SHA256SUMS" % (label, r))
        elif listed[r] != h:
            c.fail("%s: SHA256SUMS mismatch for %s" % (label, r))
    for r in listed:
        if os.path.join(pkg, r) not in files:
            c.fail("%s: SHA256SUMS lists missing file %s" % (label, r))
    leak_scan(c, pkg, label, never_publish_list(workdir), workdir, files=files)
    if execute and os.path.join(pkg, "verify-it-yourself", "run_checks.sh") in files:
        run_own_checker(c, pkg, label, timeout)


def _run_checks(root, timeout):
    sh = shutil.which("sh") or shutil.which("bash")
    if not sh:
        return None, "no sh"
    try:
        r = subprocess.run([sh, "verify-it-yourself/run_checks.sh"], cwd=root, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=timeout)
        return r.returncode, r.stdout.decode("utf-8", "replace")
    except subprocess.TimeoutExpired:
        return -1, "TIMEOUT"
    except OSError as e:
        return -1, "could not run checker: %s" % e


def run_own_checker(c, pkg, label, timeout):
    tmp = tempfile.mkdtemp(prefix="v3r1t4s_check_")
    try:
        clean = os.path.join(tmp, "clean")
        shutil.copytree(pkg, clean)
        rc, out = _run_checks(clean, timeout)
        if rc is None:
            c.warn("%s: no sh found; could not run run_checks.sh" % label)
            return
        last = last_nonempty(out)
        if rc != 0 or last != "PASS":
            c.fail("%s: its own checker did not pass from a clean copy (exit %s, last line: %s)" % (label, rc, last[:80]))
            return
        c.ok("%s: run_checks.sh prints PASS from a clean copy" % label)
        # corrupt one digit of the first object file and expect a FAIL
        bad = os.path.join(tmp, "bad")
        shutil.copytree(pkg, bad)
        objs = [p for p in walk(os.path.join(bad, "object")) if is_text(p)]
        changed = False
        for p in objs:
            t = rbytes(p)
            idx = [i for i, b in enumerate(t) if 48 <= b <= 57]
            if idx:
                i = idx[len(idx) // 2]
                t = t[:i] + (b"1" if t[i] != 49 else b"0") + t[i + 1:]
                wbytes(p, t)
                changed = True
                break
        if not changed:
            c.warn("%s: could not build a corrupted copy of object/ to test the checker" % label)
            return
        rc2, out2 = _run_checks(bad, timeout)
        if rc2 == 0 and last_nonempty(out2) == "PASS":
            c.warn("%s: the checker still printed PASS after one digit of the object was changed; make sure it really checks the object" % label)
        elif rc2 is not None and rc2 > 0 and last_nonempty(out2) == "FAIL":
            # SUBMIT.md defines terminal PASS/FAIL. Negative statuses are
            # signals or our execution-error sentinel, not protocol rejection.
            c.ok("%s: a corrupted copy of the object is rejected" % label)
        else:
            c.warn("%s: corrupted-copy check is inconclusive (exit %s); no semantic rejection was established" % (label, rc2))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ---------- workspace ----------

def norm(t):
    return re.sub(r"[^A-Z0-9]", "", t.upper())


def secret_windows(workdir, public_texts, bank=None):
    """16-char windows of commit-only secrets in private/<target-id>/ (non-code files), minus public data."""
    W = 16
    secrets = {}
    priv = os.path.join(workdir, "private")
    if not os.path.isdir(priv):
        return secrets
    public = set()
    # Short exclusions require an exact complete line, never normalized substrings.
    # LF is the line boundary; Unicode separators are ordinary text. read() already
    # folds CRLF. Replacement characters cannot establish exact decoded identity.
    public_lines = set()
    for t in public_texts:
        public_lines.update(line for line in t.split("\n") if "\ufffd" not in line)
        n = norm(t)
        for i in range(0, max(0, len(n) - W + 1)):
            public.add(n[i:i + W])
    for tid in sorted(os.listdir(priv)):
        d = os.path.join(priv, tid)
        if not os.path.isdir(d) or (bank and tid in bank and bank[tid].get("disclosure") != "commit-only"):
            continue
        for p in walk(d, skip_dirs=("panel", "claim")):
            if os.path.splitext(p)[1].lower() in CODE_EXT or not is_text(p):
                continue
            text = read(p, 200_000)
            n = norm(text)
            if len(n) < 8:
                continue
            if len(n) < W:
                line = text[:-1] if text.endswith("\n") else text
                try:
                    complete = os.path.getsize(p) <= 200_000
                except OSError:
                    complete = False
                if not complete or "\n" in line or "\ufffd" in line or line not in public_lines:
                    secrets.setdefault(n, (tid, rel(p, workdir)))
                continue
            for i in range(0, len(n) - W + 1, 4):
                w = n[i:i + W]
                if w not in public and len(set(w)) > 3:
                    secrets.setdefault(w, (tid, rel(p, workdir)))
    return secrets


def check_setup(c, workdir, settings, dry):
    sp = os.path.join(workdir, "settings.md")
    if not os.path.isfile(sp):
        c.fail("settings.md missing (kit/SETUP.md step 2)")
    else:
        missing = [k for k in SETTINGS_KEYS if k not in settings]
        if missing:
            c.fail("settings.md lacks keys: %s" % ", ".join(missing))
        if settings.get("github", "").lower().lstrip("@") == "elder-plinius":
            c.warn("settings.md github is the repository owner's handle; it must be your human's own (or 'unknown')")
        rc = settings.get("repo_commit", "")
        if rc and not re.fullmatch(r"[0-9a-f]{40}", rc):
            c.fail("settings.md repo_commit is not a 40-hex commit id")
        head = None
        if os.path.isdir(os.path.join(workdir, "repo")) and shutil.which("git"):
            try:
                head = subprocess.run(["git", "-C", os.path.join(workdir, "repo"), "rev-parse", "HEAD"],
                                      stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=30).stdout.decode().strip()
            except (OSError, subprocess.TimeoutExpired):
                head = None
        if head and rc and head != rc:
            c.fail("repo/ is at %s but settings.md says repo_commit %s (the repo copy must stay pinned)" % (head[:12], rc[:12]))
        for k, v in settings.items():
            if PLACEHOLDER_RE.search(v):
                c.fail("settings.md %s still holds a placeholder" % k)
    ch = read(os.path.join(workdir, "charter.md"))
    if not ch:
        c.fail("charter.md missing (kit/CHARTER.md)")
    elif not (re.search(r"(?im)^##\s*Quarries", ch) and re.search(r"(?im)^##\s*Lenses", ch)):
        c.fail("charter.md lacks '## Quarries' or '## Lenses'")
    rp = read(os.path.join(workdir, "RUN_PROMPT.txt"))
    if not rp:
        c.fail("RUN_PROMPT.txt missing (kit/SETUP.md step 5)")
    else:
        m = PLACEHOLDER_RE.search(rp)
        if m:
            c.fail("RUN_PROMPT.txt still contains the placeholder %s" % m.group(0))
        if re.search(r"(?i)read\s+\S*RUN_PROMPT\.txt", rp):
            c.fail("RUN_PROMPT.txt tells the reader to read RUN_PROMPT.txt (copy the numbered block, not the scheduler line)")
        if not mentions_dir(rp, workdir):
            c.fail("RUN_PROMPT.txt does not contain this workspace's absolute path")
    if not os.path.isfile(os.path.join(workdir, "private", "never_publish.txt")):
        c.fail("private/never_publish.txt missing (kit/SETUP.md step 3)")
    if not os.path.isdir(os.path.join(workdir, "repo", "kit")):
        c.fail("repo/ (the pinned copy of the repository) is missing")


def mentions_dir(text, d):
    if d in text or os.path.realpath(d) in text:
        return True
    for m in re.finditer(r"(?:[A-Za-z]:)?[/\\][^\s`'\"<>]+", text):
        cand = m.group(0).rstrip(".,;:)")
        try:
            if os.path.isdir(cand) and os.path.samefile(cand, d):
                return True
        except OSError:
            pass
    return False


def frozen_time(pre):
    """When PREREG.md was frozen: its file time, or the first UTC time written in it (date -u) if earlier,
    so that a later format-only fix does not move the freeze."""
    t = os.path.getmtime(pre)
    m = re.search(r"(\d{4})-(\d\d)-(\d\d)[T ](\d\d):(\d\d)(?::(\d\d))?(?:Z| ?UTC)", read(pre))
    if m:
        y, mo, d, h, mi, sec = (int(x or 0) for x in m.groups())
        try:
            t = min(t, calendar.timegm((y, mo, d, h, mi, sec, 0, 0, 0)))
        except (OverflowError, ValueError):
            pass
    return t


def packaged(workdir, tid):
    ob = os.path.join(workdir, "outbox")
    if not os.path.isdir(ob):
        return False
    # The confirmation check reaches outbox before check_package does. Do not
    # open its INDEX/envelope files until a no-follow inventory is safe.
    files, _ = package_inventory(Checker(quiet=True), ob, "outbox")
    if files is None:
        return False
    for p in files:
        b = os.path.basename(p)
        if b == "envelope.md" and re.search(r"(?m)^target: %s\s*$" % re.escape(tid), read(p)):
            return True
        if b == "INDEX.csv" and tid in read(p):
            return True
    return False


def latest_run(workdir):
    rd = os.path.join(workdir, "runs")
    if not os.path.isdir(rd):
        return None
    runs = sorted(d for d in os.listdir(rd) if os.path.isdir(os.path.join(rd, d)) and not d.startswith("."))
    return os.path.join(rd, runs[-1]) if runs else None


def check_report_log(c, workdir):
    rep = read(os.path.join(workdir, "REPORT.md"))
    if not rep.strip():
        c.fail("REPORT.md missing at the workspace root")
    elif re.match(r"(?i)\s*STATUS:\s*IN PROGRESS", rep):
        c.fail("REPORT.md is still the in-progress stub; write the final report")
    log = [l for l in read(os.path.join(workdir, "LOG.md")).splitlines() if l.strip()]
    if not log:
        c.fail("LOG.md missing or empty (one line per run)")
    return log


def check_run_dir(c, workdir, run, bank, dry):
    label = "run %s" % os.path.basename(run)
    tgt = kv(read(os.path.join(run, "target.md")))
    tid = tgt.get("id", "").strip("`* ")
    if not os.path.isfile(os.path.join(run, "target.md")):
        c.fail("%s: target.md missing" % label)
    elif not tid:
        c.fail("%s: target.md has no 'id: <target-id>' line" % label)
    entry = bank.get(tid) if bank else None
    if tid and bank and entry is None:
        if tid in read(os.path.join(workdir, "charter.md")):
            c.warn("%s: target %s is not in the bank; fine for a charter quarry with a published definition" % (label, tid))
        else:
            c.fail("%s: target %s is neither in the bank nor a quarry of charter.md" % (label, tid))
    scout = read(os.path.join(run, "scout.md"))
    pending = bool(PENDING_CHECK_RE.search(scout))
    completed_status = bool(scout.strip() and not pending and
                            re.search(r"https?://", scout) and successful_http_status(scout) and
                            re.search(r"\b[0-9a-f]{64}\b", scout))
    if not pending and not completed_status:
        c.fail("%s: scout.md needs the status source's URL, HTTP status and page sha256 (from command output), "
               "or 'PENDING STATUS CHECK'" % label)
    elif completed_status:
        hashes = set(re.findall(r"\b[0-9a-f]{64}\b", scout))
        data = os.path.join(run, "data")
        have = {hashlib.sha256(rbytes(p)).hexdigest() for p in walk(data)} if os.path.isdir(data) else set()
        if not hashes & have:
            c.fail("%s: no sha256 in scout.md matches a file in data/; save the fetched status page in data/ exactly "
                   "as fetched and record its real sha256" % label)
    for f in ("scout.md", "BRIEF.md"):
        if not os.path.isfile(os.path.join(run, f)):
            c.fail("%s: %s missing (kit/RUN.md step 3)" % (label, f))
    dead = tgt.get("dead") or kv(read(os.path.join(run, "scout.md"))).get("dead")
    if dead and re.fullmatch(r"(?i)\W*(no|false|none|n/?a|not dead|open)\W*", dead):
        dead = None
    if dead and re.match(r"(?i)\W*unreachable", dead) and not re.search(
            r"PENDING (STATUS|TABLE) CHECK|\b(000|40[0-9]|429|5\d\d)\b", read(os.path.join(run, "scout.md"))):
        c.fail("%s: 'dead: unreachable' but scout.md records neither a failed fetch (4xx/5xx/no connection) nor "
               "PENDING STATUS CHECK" % label)
        dead = None
    if dead and (not DEAD_OK.match(dead) or DEAD_BAD.search(dead)):
        c.fail("%s: 'dead: %s' is not a dead target. Only solved, off-limits or unreachable targets (or a record "
               "moved out of reach) end a run before the attack; time, effort, tests and commit-only never do" % (label, dead[:60]))
        dead = None
    att = os.path.join(run, "attempts")
    lenses = sorted(d for d in os.listdir(att) if os.path.isdir(os.path.join(att, d))) if os.path.isdir(att) else []
    if dry:
        return tid, entry
    if not lenses and not dead:
        c.fail("%s: no attempts/<lens>/ folders: the run stopped before the attack (write 'dead: <reason>' in target.md only if the target is solved, off-limits or unreachable)" % label)
    elif 0 < len(lenses) < 2 and not dead:
        c.fail("%s: only one lens in attempts/; every effort level runs at least two" % label)
    claim_levels = []
    for l in lenses:
        r = read(os.path.join(att, l, "report.md"))
        m = re.search(r"(?im)^\W*claim[ _]level\W*\s*[:=]\s*`?([a-z_]+)", r)
        if not r:
            c.fail("%s: attempts/%s/report.md missing" % (label, l))
        elif not m:
            c.fail("%s: attempts/%s/report.md has no 'claim level:' line" % (label, l))
        else:
            claim_levels.append(m.group(1))
            if m.group(1) not in ("partial_win_claim", "solution_claim"):
                dl = re.search(r"(?im)^[ \t#*>-]*dead[ _]lines[ \t*`]*:?[ \t]*$", r)
                bullets = re.findall(r"(?m)^\s*(?:[-*+]|\d+[.)])\s+(\S.{10,})", r[dl.end():]) if dl else []
                settled = any(SETTLED_RE.search(b) for b in bullets)
                if len(bullets) < 3 and not (bullets and settled):
                    c.fail("%s: attempts/%s/report.md needs 'dead lines:' with at least 3 bullets (what was tried, "
                           "the real result, why it died), or one bullet that settles the question; found %d" % (label, l, len(bullets)))
        files = [p for p in walk(os.path.join(att, l))]
        code = [p for p in files if os.path.splitext(p)[1].lower() in CODE_EXT]
        outs = [p for p in files if os.path.splitext(p)[1].lower() not in CODE_EXT
                and os.path.basename(p) not in ("NOTES.md", "report.md", "REPRODUCE.md")]
        commit_only = (entry or {}).get("disclosure") == "commit-only"
        if not outs and commit_only and tid and os.path.isdir(os.path.join(workdir, "private", tid)):
            outs = [p for p in walk(os.path.join(workdir, "private", tid)) if os.path.splitext(p)[1].lower() not in CODE_EXT]
        if not code or not outs:
            c.fail("%s: attempts/%s/ needs at least one program it ran and that program's saved output" % (label, l))
        if not os.path.isfile(os.path.join(att, l, "NOTES.md")):
            c.fail("%s: attempts/%s/NOTES.md missing (hypotheses)" % (label, l))
    if (entry or {}).get("disclosure") == "commit-only":
        for p in walk(run, skip_dirs=("data",)):
            b = os.path.basename(p).lower()
            if re.search(r"(key|plaintext|solution|decrypt|crib)", b) and os.path.splitext(b)[1] not in CODE_EXT \
                    and not re.search(r"(test|neg|pos|sibling|wrong|fake|sample|example|control|null)", b):
                c.fail("%s: %s looks like a key or plaintext of a commit-only target; it belongs in private/%s/" % (label, rel(p, workdir), tid))
    pre = os.path.join(run, "PREREG.md")
    if lenses and not os.path.isfile(pre):
        c.fail("%s: PREREG.md missing; freeze criterion, statistic, thresholds and null design before measuring" % label)
    prereg = critical_kv(c, read(pre), "%s: PREREG.md" % label, {"null_test"})
    nt = prereg.get("null_test", "").lower()
    if lenses and os.path.isfile(pre) and not (nt.startswith("required") or nt.startswith("not needed because")):
        c.fail("%s: PREREG.md needs 'null_test: required' or 'null_test: not needed because <reason>'" % label)
    priv_panel = os.path.join(workdir, "private", tid, "panel") if tid else None
    panel_dir = os.path.join(run, "panel")
    gate = critical_kv(c, read(os.path.join(panel_dir, "gate.md")),
                       "%s: gate.md" % label, {"status", "confirmed_scope"})
    gate_status = gate.get("status", "")
    if re.search(r"(?i)CONFIRMED_", gate_status) and gate_status not in CONFIRMED_STATUSES:
        c.warn("%s: panel/gate.md status '%s' is not exactly CONFIRMED_SOLUTION or CONFIRMED_PARTIAL, "
               "so the run is not treated as confirmed" % (label, gate_status[:60]))
    has_claim = any(x in ("partial_win_claim", "solution_claim") for x in claim_levels) or \
        os.path.isdir(os.path.join(run, "claim")) or bool(gate) or \
        (tid and os.path.isdir(os.path.join(workdir, "private", tid, "claim")))
    null_required = nt.startswith("required") or (entry or {}).get("category") in NULL_CATEGORIES
    null_ok = None
    if has_claim and null_required:
        null_ok = check_null(c, os.path.join(run, "null_test.md"), label)
        if os.path.isfile(pre) and os.path.isfile(os.path.join(run, "null_test.md")) and \
                frozen_time(pre) > os.path.getmtime(os.path.join(run, "null_test.md")) + 1:
            c.fail("%s: PREREG.md was written after null_test.md (freeze before you measure)" % label)
    if os.path.isfile(pre):
        later = [p for d in (os.path.join(run, "claim"), os.path.join(workdir, "private", tid or "-", "claim"))
                 if os.path.isdir(d) for p in walk(d) if os.path.getmtime(p) + 1 < frozen_time(pre)]
        if later:
            c.fail("%s: PREREG.md was written after the claim was built (%s); freeze before you measure" % (label, rel(later[0], workdir)))
    # status words
    mentions = []
    scan = [os.path.join(workdir, "REPORT.md")]
    quoted = {"target.md", "PREREG.md", "BRIEF.md", "scout.md"}   # hold verbatim bank criteria, which use the word
    for p in walk(run, skip_dirs=("panel", "data")):
        if os.path.basename(p) in quoted and os.path.dirname(p) == run:
            continue
        if is_text(p) and os.path.splitext(p)[1].lower() not in CODE_EXT:
            scan.append(p)
    for p in scan:
        for ln, line in confirmed_mentions(p):
            mentions.append("%s:%d" % (rel(p, workdir), ln))
    log = [l for l in read(os.path.join(workdir, "LOG.md")).splitlines() if l.strip()]
    if log and CONFIRMED_RE.search(log[-1]) and not NEGATION_RE.search(log[-1].split("CONFIRMED_")[0]):
        mentions.append("LOG.md (last line)")
    confirmed = bool(mentions) or gate.get("status", "") in CONFIRMED_STATUSES
    if confirmed:
        critical_kv(c, read(os.path.join(run, "target.md")), label + ": target.md", {"id"})
        if not completed_status:
            c.fail("%s: CONFIRMED_* requires a completed status/table check" % label)
        where = [d for d in (panel_dir, priv_panel) if d and all(os.path.isfile(os.path.join(d, r + ".md")) for r in PANEL)]
        pd = where[0] if where else panel_dir
        ok = True
        sub_fails = len(c.fails)
        for role in PANEL:
            if not os.path.isfile(os.path.join(pd, role + ".md")):
                c.fail("%s: CONFIRMED_* written (%s) but panel/%s.md is missing; only a three-skeptic panel can confirm. Write PROMISING instead." % (label, ", ".join(mentions[:3]) or "gate.md", role))
                ok = False
        if ok:
            check_panel(c, pd, label, require_confirmed=False)
            check_panel_scope(c, pd, os.path.join(panel_dir, "gate.md"), label)
            if gate.get("status", "") not in CONFIRMED_STATUSES:
                c.fail("%s: CONFIRMED_* written (%s) but panel/gate.md does not say status: CONFIRMED_*" % (label, ", ".join(mentions[:3])))
            elif not gate.get("confirmed_scope"):
                c.fail("%s: panel/gate.md lacks confirmed_scope" % label)
        if null_required and null_ok is False:
            c.fail("%s: CONFIRMED_* without a passing null test" % label)
        if len(c.fails) == sub_fails:
            c.ok("%s: CONFIRMED status backed by three panel files and gate.md" % label)
        if gate.get("status", "") in CONFIRMED_STATUSES and tid and not packaged(workdir, tid):
            kind = "a sealed envelope outbox/<submission-id>/envelope.md" if (entry or {}).get("disclosure") == "commit-only" \
                else "a package outbox/<submission-id>/ whose INDEX.csv names it"
            c.fail("%s: %s is CONFIRMED but outbox/ has no package for it; build %s (kit/SUBMIT.md)" % (label, tid, kind))
    elif has_claim:
        c.ok("%s: claim present, not confirmed (PROMISING or lower)" % label)
    return tid, entry


def check_workspace(c, workdir, run=None, setup_only=False, execute=True, timeout=900):
    workdir = os.path.abspath(workdir)
    if not os.path.isdir(workdir):
        c.fail("workspace %s not found" % workdir)
        return
    settings = kv(read(os.path.join(workdir, "settings.md")))
    bank_errors = []
    bank, bank_dir = load_bank(workdir, settings, bank_errors)
    for e in bank_errors:
        c.fail("could not read the bank %s" % e)
    if not bank:
        c.warn("could not load the bank (settings.md 'bank:' or repo/bank/targets.json)")
    check_setup(c, workdir, settings, setup_only)
    check_report_log(c, workdir)
    run = os.path.abspath(run) if run else latest_run(workdir)
    if not run:
        c.fail("no run folder in runs/ (setup ends with a dry run, kit/SETUP.md step 7)")
    else:
        check_run_dir(c, workdir, run, bank, setup_only)
    # outbox: only confirmed, valid packages
    ob = os.path.join(workdir, "outbox")
    unsafe_packages = []
    if os.path.isdir(ob):
        for d in sorted(os.listdir(ob)):
            p = os.path.join(ob, d)
            if d.startswith(".") and regular_file_no_follow(p):
                continue  # e.g. .DS_Store: not a package; the secret scan below still reads text files
            if os.path.isdir(p) or p.endswith(".md"):
                if check_package(c, p, workdir, execute=execute, timeout=timeout) is False:
                    unsafe_packages.append(p)
            else:
                c.fail("outbox/%s: outbox holds only package folders (confirmed claims)" % d)
                unsafe_packages.append(p)
    # commit-only secrets must not leave private/
    public_texts = []
    for root in [bank_dir] + [os.path.join(workdir, "runs", r, "data") for r in (os.listdir(os.path.join(workdir, "runs")) if os.path.isdir(os.path.join(workdir, "runs")) else [])]:
        if root and os.path.isdir(root):
            for p in walk(root):
                if is_text(p) and os.path.getsize(p) < MAX_SCAN:
                    public_texts.append(read(p))
    secrets = secret_windows(workdir, public_texts, bank)
    if secrets:
        leaked = {}
        targets = [os.path.join(workdir, f) for f in ("REPORT.md", "LOG.md")]
        for sub in ("runs", "outbox", "dossiers"):
            if os.path.isdir(os.path.join(workdir, sub)):
                targets += list(walk(os.path.join(workdir, sub), skip_dirs=("data",)))
        for p in targets:
            if any(p == root or p.startswith(root + os.sep) for root in unsafe_packages):
                continue  # Already failed inventory; never read unsafe package entries.
            if not os.path.isfile(p) or not is_text(p) or os.path.splitext(p)[1].lower() in CODE_EXT:
                continue
            n = norm(read(p))
            for w, (tid, src) in secrets.items():
                if w in n:
                    leaked.setdefault(rel(p, workdir), (tid, src))
                    break
        for p, (tid, src) in sorted(leaked.items()):
            c.fail("%s contains text from %s (commit-only secrets stay in private/%s/; refer to them by path and sha256)" % (p, src, tid))
        if not leaked:
            c.ok("no text from private/ found outside it")


def main(argv=None):
    ap = argparse.ArgumentParser(description="V3R1T4S mechanical gate (kit/check_run.py)")
    ap.add_argument("workdir", nargs="?", help="the V3R1T4S workspace folder")
    ap.add_argument("--setup", action="store_true", help="end-of-setup check (dry run: no attack expected)")
    ap.add_argument("--run", help="check this run folder instead of the latest")
    ap.add_argument("--package", help="check one outbox package folder (or a sealed envelope .md)")
    ap.add_argument("--workdir", dest="workdir2", help="workspace for --package (bank, never-publish list, panels)")
    ap.add_argument("--no-exec", action="store_true", help="do not run the package's own checker")
    ap.add_argument("--timeout", type=int, default=900, help="seconds allowed for run_checks.sh")
    a = ap.parse_args(argv)
    c = Checker()
    if a.package:
        wd = a.workdir2 or a.workdir
        check_package(c, a.package, os.path.abspath(wd) if wd else None, execute=not a.no_exec, timeout=a.timeout)
    elif a.workdir:
        check_workspace(c, a.workdir, a.run, a.setup, execute=not a.no_exec, timeout=a.timeout)
    else:
        ap.print_help()
        return 2
    return c.finish()


if __name__ == "__main__":
    sys.exit(main())

