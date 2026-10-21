#!/usr/bin/env python3
"""Build the V3R1T4S static site into site/public/ from this repository checkout.

    python3 site/build.py [--out site/public] [--offline]

Standard library only, Python 3.8+, no network except git's own transport. Cloudflare Workers Builds runs it on
every push to main and then deploys site/public/ as static assets (see site/README.md and wrangler.jsonc).

Everything shown on the page is derived from the checkout at build time:
  - counts: TROPHY_CASE.md "All rows", package INDEX.csv files, bank/targets.json;
  - daily discoveries: result packages known-knowns/<family>/<YYYY-MM-DD>-<credit>-<hash8>/, newest merge first.
    The merge day comes from git history (the commit that added the folder); without history, from the folder name.
    Each one links to its package folder in the repository, never to a pull request, so an anonymous credit stays
    anonymous on the site;
  - leaderboard: merged result packages per credit name, the name in the folder;
  - open problems (known unknowns): every target in bank/targets.json;
  - V3R1T4S Weekly: news/YYYY-MM-DD.md, in a strict plain-text grammar (see parse_news);
  - plain-English blurbs: site/src/plain.json, one line per result family and per category (see load_plain).

There is no GitHub API call, no credential and no vote or star count: the only network access is one optional
'git fetch --unshallow' over the clone's own remote when the build checkout is shallow.

Repository content is untrusted input (contributors write package READMEs, INDEX.csv files and folder names):
  - nothing from the repository is executed or imported; the only program run is git (rev-parse, log, fetch);
  - symlinks are never followed, files are size-capped, bad UTF-8 is replaced (news files: rejected), control and
    bidi characters are stripped, every string is length-capped;
  - names that become URL path segments must match strict patterns, otherwise the item is skipped;
  - from INDEX.csv only the value and table_value columns are used, and only when both parse as numbers (so a
    formula such as =HYPERLINK(...) is never shown); the page never exports CSV;
  - data.json carries ids and relative repo paths, never URLs: app.js builds every link from fixed
    github.com/elder-plinius/V3R1T4S prefixes and re-checks the ids, and renders text with textContent only;
  - HTML and XML written here (index.html with its no-JS snapshot, 404.html, feed.xml, sitemap.xml) escape every
    value; known-unknowns.txt strips tabs and newlines from every field.
"""
import argparse
import csv
import datetime
import html
import io
import json
import math
import os
import re
import shutil
import stat
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SRC = os.path.join(HERE, "src")
OWNER_REPO = "elder-plinius/V3R1T4S"
GH = "https://github.com/" + OWNER_REPO
SITE_URL_DEFAULT = "https://v3r1t4s.org"
SCHEMA = "v3r1t4s-site/2"
TEMPLATES = ("index.html", "404.html")  # rendered from site/src/, never copied raw
DATA_FILES = ("plain.json",)           # read from site/src/ into data.json, never copied raw

# ------------------------------------------------------------------ limits
MAX_MD = 512 * 1024          # a README or TROPHY_CASE.md
MAX_CSV = 512 * 1024         # one INDEX.csv
MAX_JSON = 16 * 1024 * 1024  # bank/targets.json (1.7 MB today)
MAX_ROWS = 500               # INDEX.csv rows read per package
MAX_PACKAGES = 20000
MAX_TARGETS = 20000
GIT_TIMEOUT = 120
MAX_NEWS = 52                # editions kept in data.json (a year of weeklies)
MAX_NEWS_SCAN = 200          # newest news/ file names looked at
MAX_NEWS_FILE = 16 * 1024    # one edition (the grammar allows about 4 KB)
NEWS_PARAS_MAX = 3           # 1 to 3 paragraphs
NEWS_PARAS_CHARS = 900       # all paragraphs together, under this
NEWS_BULLETS = 10
NEWS_BULLET_CHARS = 240      # one bullet's text (without its " → path"), under this
NEWS_PATH_CHARS = 200
FEED_DISCOVERIES = 30        # newest discoveries in feed.xml
MAX_PLAIN = 64 * 1024        # site/src/plain.json
PLAIN_CHARS = 110            # one blurb, under this

# ------------------------------------------------------------------ name patterns (anything else is skipped)
# \Z, not $: '$' also matches before a trailing newline
RE_SLUG = re.compile(r"^[a-z0-9][a-z0-9-]{0,99}\Z")                    # family, category, target ids
RE_PKG = re.compile(r"^(\d{4}-\d{2}-\d{2})-([A-Za-z0-9][A-Za-z0-9_.-]{0,63})-([0-9a-f]{8})\Z")
RE_PR = re.compile(r"\(#(\d{1,7})\)\s*$")
RE_SHA = re.compile(r"^[0-9a-f]{40}\Z")

TODAY = datetime.datetime.now(datetime.timezone.utc).date()


def valid_day(d):
    """d if it is a real calendar date YYYY-MM-DD between 2000-01-01 and tomorrow (UTC), else None."""
    if not isinstance(d, str) or not re.match(r"^\d{4}-\d{2}-\d{2}$", d):
        return None
    try:
        x = datetime.date(int(d[:4]), int(d[5:7]), int(d[8:10]))
    except ValueError:
        return None
    return d if datetime.date(2000, 1, 1) <= x <= TODAY + datetime.timedelta(days=1) else None

warnings = []


def warn(msg):
    warnings.append(msg)
    print("warn:", msg, file=sys.stderr)


class Unsafe(Exception):
    pass


# ------------------------------------------------------------------ safe file access
def _lstat_chain(rel):
    """lstat every component of rel below REPO; refuse symlinks, '..', empty and NUL parts."""
    parts = rel.split("/")
    cur = REPO
    st = None
    for p in parts:
        if p in ("", ".", "..") or "\x00" in p or "\\" in p:
            raise Unsafe("bad path %r" % rel)
        cur = os.path.join(cur, p)
        st = os.lstat(cur)
        if stat.S_ISLNK(st.st_mode):
            raise Unsafe("symlink %s" % rel)
    return cur, st


def read_bytes(rel, cap):
    path, st = _lstat_chain(rel)
    if not stat.S_ISREG(st.st_mode):
        raise Unsafe("not a regular file: %s" % rel)
    if st.st_size > cap:
        raise Unsafe("too big (%d bytes): %s" % (st.st_size, rel))
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    fd = os.open(path, flags)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise Unsafe("not a regular file: %s" % rel)
        with os.fdopen(fd, "rb") as f:
            fd = None
            data = f.read(cap + 1)
    finally:
        if fd is not None:
            os.close(fd)
    if len(data) > cap:
        raise Unsafe("too big: %s" % rel)
    return data


def read_text(rel, cap=MAX_MD):
    return read_bytes(rel, cap).decode("utf-8", "replace").replace("\r\n", "\n").replace("\x00", "")


def try_text(rel, cap=MAX_MD):
    try:
        return read_text(rel, cap)
    except (OSError, Unsafe) as e:
        warn("skip %s: %s" % (rel, e))
        return None


def read_json(rel, cap=MAX_JSON):
    try:
        return json.loads(read_text(rel, cap))
    except (OSError, Unsafe, ValueError, RecursionError) as e:
        warn("skip %s: %s" % (rel, e))
        return None


def is_file(rel):
    try:
        return stat.S_ISREG(_lstat_chain(rel)[1].st_mode)
    except (OSError, Unsafe):
        return False


def subdirs(rel):
    """Real (non-symlink) subdirectory names of rel, sorted."""
    try:
        path, st = _lstat_chain(rel)
        if not stat.S_ISDIR(st.st_mode):
            return []
        with os.scandir(path) as it:
            return sorted(e.name for e in it if e.is_dir(follow_symlinks=False))
    except (OSError, Unsafe) as e:
        warn("skip dir %s: %s" % (rel, e))
        return []


def files_in(rel):
    try:
        path, st = _lstat_chain(rel)
        if not stat.S_ISDIR(st.st_mode):
            return []
        with os.scandir(path) as it:
            return sorted(e.name for e in it if e.is_file(follow_symlinks=False))
    except (OSError, Unsafe):
        return []


# ------------------------------------------------------------------ text cleaning
# C0/C1 controls, zero-width and bidi controls, BOM, interlinear annotation, specials
_CTRL = re.compile("[\x00-\x1f\x7f-\x9f­؜ᅟᅠ᠎​-‏ -‮"
                   "⁠-⁯ㅤ︀-︎﻿￰-￻\U000e0000-\U000e007f]")


_SURROGATE = re.compile("[\ud800-\udfff]")


def clean(s, n):
    """Untrusted text -> one line, no control/bidi characters, at most n characters."""
    s = _SURROGATE.sub("", _CTRL.sub(" ", str(s)))  # lone surrogates can come from JSON "\\ud800" escapes
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def strip_md(s, cap=600):
    s = s[:cap]  # callers pass one heading or one news paragraph; never run these patterns on more (they backtrack)
    s = re.sub(r"!\[[^\]]{0,300}\]\([^)]{0,300}\)", "", s)
    s = re.sub(r"\[([^\]]{1,300})\]\([^)]{0,300}\)", r"\1", s)
    s = re.sub(r"</?[A-Za-z][^>]{0,300}>", "", s)
    s = s.replace("**", "").replace("`", "").replace("\\|", "|")
    s = re.sub(r"(?<![\w*])\*(?!\s)([^*]+?)\*(?!\w)", r"\1", s)
    return s


_EMOJI_OK = re.compile("^[©®‼-㊙\U0001f000-\U0001faff️‍]{1,8}$")


def emoji_ok(e):
    return e if e and _EMOJI_OK.match(e) else None


# ------------------------------------------------------------------ numbers and margins
_NUM = re.compile(r"^[+\-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?$")


def to_num(s):
    s = str(s).strip().replace("−", "-").replace(",", "").replace(" ", "")
    if len(s) > 80 or not _NUM.match(s):
        return None
    try:
        x = float(s)
    except ValueError:
        return None
    return x if math.isfinite(x) else None


def margin(value, table):
    """'new 50 · was 52' from INDEX.csv value and table_value: verbatim when both are short, otherwise rounded to
    the fewest decimals (or significant digits, for huge numbers) that still show the difference. Plain words, so a
    visitor sees which number is new without a tooltip (higher or lower can be better, depending on the problem)."""
    v, t = to_num(value), to_num(table)
    if v is None or t is None or v == t:
        return None
    rv, rt = (str(x).strip().replace("−", "-") for x in (value, table))
    if len(rv) <= 12 and len(rt) <= 12:
        return "new %s · was %s" % (rv, rt)
    if max(abs(v), abs(t)) < 1e12:
        for d in range(0, 16):
            a, b = "{:.{}f}".format(v, d), "{:.{}f}".format(t, d)
            if a != b:
                return "new %s · was %s" % (a, b)
        return None
    for sig in range(3, 18):
        a, b = "{:.{}e}".format(v, sig - 1), "{:.{}e}".format(t, sig - 1)
        if a != b:
            fa, ea = a.split("e")
            fb, eb = b.split("e")
            return "new %s×10^%d · was %s×10^%d" % (fa, int(ea), fb, int(eb))
    return None


# ------------------------------------------------------------------ git (local commands; one optional fetch)
def git(args, timeout=GIT_TIMEOUT):
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0", GIT_ASKPASS="true", GIT_OPTIONAL_LOCKS="0")
    cmd = ["git", "-C", REPO, "-c", "core.hooksPath=/dev/null", "-c", "core.fsmonitor=false",
           "-c", "protocol.file.allow=never", "-c", "diff.external="] + args
    try:
        r = subprocess.run(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           timeout=timeout, env=env)
    except (OSError, subprocess.SubprocessError) as e:
        warn("git %s: %s" % (args[0], e))
        return None
    if r.returncode != 0:
        warn("git %s exited %d: %s" % (args[0], r.returncode, clean(r.stderr.decode("utf-8", "replace"), 300)))
        return None
    return r.stdout.decode("utf-8", "replace")


def git_head():
    h = (git(["rev-parse", "HEAD"], 30) or "").strip()
    return h if RE_SHA.match(h) else None


def git_history():
    """{package folder name: (merge day YYYY-MM-DD in UTC, commit unix time)} from the commits that added each
    package, or None when history is unavailable (no git, or a shallow clone that cannot be deepened).

    A shallow clone is deepened with 'git fetch --unshallow' over the clone's own remote: git transport, no API, no
    credentials of ours, bounded by GIT_TIMEOUT. If that fails (no network), the caller uses the folder dates."""
    if git(["rev-parse", "--git-dir"], 30) is None:
        return None
    shallow = (git(["rev-parse", "--is-shallow-repository"], 30) or "").strip()
    if shallow == "true":
        print("shallow clone: trying git fetch --unshallow", file=sys.stderr)
        git(["fetch", "--unshallow", "--quiet", "--no-tags", "--no-recurse-submodules"], GIT_TIMEOUT)
        shallow = (git(["rev-parse", "--is-shallow-repository"], 30) or "").strip()
        if shallow != "false":
            warn("history unavailable (shallow clone); discovery dates come from folder names")
            return None
    out = git(["log", "--no-renames", "--diff-filter=A", "--name-only", "--no-textconv", "--no-ext-diff",
               "--format=%x1e%ct%x1f%s", "--", "known-knowns"])
    if out is None:
        return None
    first = {}
    for chunk in out.split("\x1e"):
        if not chunk.strip():
            continue
        header, _, body = chunk.partition("\n")
        date, _, subject = header.partition("\x1f")
        squash = RE_PR.search(subject) is not None
        ts = int(date) if re.match(r"^\d{1,12}$", date.strip()) else None
        try:
            day = valid_day(datetime.datetime.fromtimestamp(ts, datetime.timezone.utc).strftime("%Y-%m-%d"))
        except (TypeError, ValueError, OverflowError, OSError):
            day = None
        if not day:
            continue
        names = set()
        for line in body.split("\n"):
            parts = line.split("/")
            if len(parts) >= 3 and parts[0] == "known-knowns" and RE_PKG.match(parts[2]):
                names.add(parts[2])
        for n in names:
            # log is newest first, so the last commit seen is the oldest. Prefer the oldest squash-merge commit
            # (subject ends in "(#NNN)"): its committer date is the merge date even if branch commits came along.
            old = first.get(n)
            if old is None or squash or not old[2]:
                first[n] = (day, ts, squash)
    return {n: (v[0], v[1]) for n, v in first.items()}


# ------------------------------------------------------------------ V3R1T4S Weekly (news/YYYY-MM-DD.md)
RE_NEWS_FILE = re.compile(r"^(\d{4}-\d{2}-\d{2})\.md\Z")
RE_NEWS_H1 = re.compile(r"^# V3R1T4S Weekly[ \t]+[·\-–—][ \t]+(\d{4}-\d{2}-\d{2})"
                        r"[ \t]+(?:→|->|–|—)[ \t]+(\d{4}-\d{2}-\d{2})\Z")
# "no HTML": a tag start (<a, </, <!, <?) or a character reference (&amp; &#60; &#x3c;) makes the file invalid
RE_NEWS_HTML = re.compile(r"<\s*[A-Za-z/!?]|&(?:#[0-9]{1,8}|#[xX][0-9A-Fa-f]{1,8}|[A-Za-z][A-Za-z0-9]{1,31});")
RE_NEWS_CTRL = re.compile("[\x00-\x08\x0b-\x1f\x7f-\x9f]")


def news_path(p):
    """A relative repo path for a news bullet, or None. Allowed: known-knowns/<family>[/<package>[/README.md]] and
    known-unknowns/<category>[/<id>.md | /README.md], every segment pattern-checked, and the path must exist in the
    checkout (a directory or a regular file, no symlink anywhere)."""
    if not isinstance(p, str) or len(p) > NEWS_PATH_CHARS:
        return None
    p = p[:-1] if p.endswith("/") else p
    parts = p.split("/")
    ok = False
    if parts[0] == "known-knowns" and 2 <= len(parts) <= 4 and RE_SLUG.match(parts[1]):
        ok = len(parts) == 2 or (RE_PKG.match(parts[2]) is not None and (len(parts) == 3 or parts[3] == "README.md"))
    elif parts[0] == "known-unknowns" and 2 <= len(parts) <= 3 and RE_SLUG.match(parts[1]):
        ok = len(parts) == 2 or parts[2] == "README.md" or (
            parts[2].endswith(".md") and RE_SLUG.match(parts[2][:-3]) is not None)
    if not ok:
        return None
    try:
        st = _lstat_chain(p)[1]
    except (OSError, Unsafe):
        return None
    return p if stat.S_ISDIR(st.st_mode) or stat.S_ISREG(st.st_mode) else None


_MD_LINK = re.compile(r"!?\[([^\[\]]{0,300})\]\((?:[^()\s]|\([^()\s]{0,100}\)){0,300}\)")


def news_text(s):
    """Plain text from a paragraph or bullet: inline markdown (links, bold, code) reduced to its text. Inputs are
    under NEWS_PARAS_CHARS (checked before this runs); a link target, even one with parentheses, is dropped."""
    return clean(strip_md(_MD_LINK.sub(r"\1", s[:1000]), 1000), NEWS_PARAS_CHARS)


def parse_news_file(name):
    """One edition, or None (with a warning) when the file breaks the grammar:

        # V3R1T4S Weekly · <from> → <to>          (line 1; dates YYYY-MM-DD, from <= to, at most 31 days apart)
        <blank>
        1 to 3 paragraphs of plain text, separated by blank lines, under 900 characters together
        <blank>
        up to 10 bullets "- <text>" (text under 240 characters), each optionally ending " → <relative repo path>"

    The file is news/<date>.md, where <date> is the publication day: from <to> to 7 days after it. No HTML, no
    headings, no other line types; strict UTF-8; at most 16 KB."""
    rel = "news/" + name
    fdate = valid_day(RE_NEWS_FILE.match(name).group(1))
    if not fdate:
        warn("news skipped (%s: date is not a real day, or is in the future)" % clean(name, 40))
        return None

    def bad(why):
        warn("news skipped (%s: %s)" % (clean(name, 40), why))

    try:
        raw = read_bytes(rel, MAX_NEWS_FILE)
    except (OSError, Unsafe) as e:
        return bad(clean(e, 120))
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return bad("not valid UTF-8")
    text = text.lstrip("﻿").replace("\r\n", "\n")
    if RE_NEWS_CTRL.search(text):
        return bad("control characters")
    if RE_NEWS_HTML.search(text):
        return bad("contains HTML")
    lines = [l.rstrip(" \t") for l in text.split("\n")]
    while lines and not lines[-1]:
        lines.pop()
    m = RE_NEWS_H1.match(lines[0].strip()) if lines else None
    if not m:
        return bad('line 1 is not "# V3R1T4S Weekly · YYYY-MM-DD → YYYY-MM-DD"')
    d_from, d_to = valid_day(m.group(1)), valid_day(m.group(2))
    if not d_from or not d_to or d_from > d_to:
        return bad("bad date range")
    f, t, p = (datetime.date.fromisoformat(x) for x in (d_from, d_to, fdate))
    if (t - f).days > 31 or not (t <= p <= t + datetime.timedelta(days=7)):
        return bad("range longer than 31 days, or file date not within 7 days after the range")
    paras, cur, bullets = [], [], []
    for line in lines[1:]:
        if line.startswith("- "):
            if cur:
                paras.append(" ".join(cur))
                cur = []
            bullets.append(line[2:].strip())
        elif not line.strip():
            if cur:
                paras.append(" ".join(cur))
                cur = []
        elif bullets:
            return bad("text after the bullets")
        elif re.match(r"^\s*(?:[#>|]|[*+-]\s|\d+[.)]\s|```|~~~)", line) or line.startswith(("    ", "\t")):
            return bad("only plain paragraphs and '- ' bullets are allowed")
        else:
            cur.append(line.strip())
    if cur:
        paras.append(" ".join(cur))
    if not 1 <= len(paras) <= NEWS_PARAS_MAX:
        return bad("needs 1 to %d paragraphs, found %d" % (NEWS_PARAS_MAX, len(paras)))
    if sum(len(x) for x in paras) >= NEWS_PARAS_CHARS:
        return bad("paragraphs are %d characters, the limit is under %d"
                   % (sum(len(x) for x in paras), NEWS_PARAS_CHARS))
    if len(bullets) > NEWS_BULLETS:
        return bad("%d bullets, the limit is %d" % (len(bullets), NEWS_BULLETS))
    out_b = []
    for b in bullets:
        # Only a final " → known-knowns/..." or " → known-unknowns/..." token is a link path. Any other tail
        # (5/6 → 6/7, 23:10 → 23:59, a URL) is ordinary text and stays. A path that fails the checks is kept
        # as plain text too, never as a link, so the bullet never loses words.
        body, path, shown = b, None, b
        head, sep, tail = b.rpartition(" → ")
        tail = tail.strip()
        if sep and tail and not re.search(r"\s", tail) and tail.startswith(("known-knowns/", "known-unknowns/")):
            body = head.strip()
            path = news_path(tail)
            if path is None:
                warn("news %s: link dropped, kept as text (not an existing known-knowns/ or known-unknowns/ "
                     "path): %r" % (clean(name, 40), clean(tail, 80)))
            else:
                shown = body
        if not body:
            return bad("empty bullet")
        if len(body) >= NEWS_BULLET_CHARS:
            return bad("a bullet is %d characters, the limit is under %d" % (len(body), NEWS_BULLET_CHARS))
        out_b.append({"t": news_text(shown), "path": path})
    return {
        "id": fdate, "title": "V3R1T4S Weekly · %s → %s" % (d_from, d_to), "from": d_from, "to": d_to,
        "paras": [news_text(x) for x in paras], "bullets": out_b,
    }


def parse_news():
    """Valid editions from news/, newest first, at most MAX_NEWS. A missing news/ folder means no editions."""
    names = [n for n in files_in("news") if RE_NEWS_FILE.match(n)]
    names.sort(reverse=True)
    out = []
    for n in names[:MAX_NEWS_SCAN]:
        if len(out) >= MAX_NEWS:
            break
        try:
            e = parse_news_file(n)
        except (TypeError, ValueError, KeyError, IndexError, RecursionError) as ex:  # backstop
            warn("news skipped (%s: %s)" % (clean(n, 40), type(ex).__name__))
            e = None
        if e:
            out.append(e)
    return out


# ------------------------------------------------------------------ repo parsers
def trophy_rows():
    md = try_text("TROPHY_CASE.md")
    if not md:
        return None
    body = md.split("## All rows", 1)
    if len(body) < 2:
        return None
    body = body[1].split("\n## ", 1)[0]
    return sum(1 for line in body.split("\n") if re.match(r"^\|\s*\d+\s*\|", line))


def readme_category_emoji():
    """{category id: emoji} from the README known-unknowns table (categories.json carries no emoji)."""
    md = try_text("README.md") or ""
    out = {}
    for m in re.finditer(r"^\|\s*(\S{1,12})\s+\[[^\]]{1,80}\]\(known-unknowns/([a-z0-9-]{1,100})/README\.md\)",
                         md, re.M):
        e = emoji_ok(m.group(1))
        if e and RE_SLUG.match(m.group(2)):
            out[m.group(2)] = e
    return out


# a blurb is one plain sentence or two: no digits (numbers belong to the data, and go stale), no markup of any kind
RE_PLAIN_BAD = re.compile(r"[0-9<>&*_`\[\]{}#|\\~=^$@]|https?:|www\.|\d", re.I)


def load_plain():
    """{"f": {family id: blurb}, "c": {category id: blurb}} from site/src/plain.json, which has the shape
    {"families": {id: blurb}, "categories": {id: blurb}}. Ids must be slugs; a blurb must be a string under
    PLAIN_CHARS characters after cleaning, with no digits and no markup. Anything else is skipped with a warning:
    a bad blurb never fails the build, the page just shows no blurb for that id. The file is also read by the
    maintainer's weekly digest (as layman context), so its shape is part of the contract."""
    out = {"f": {}, "c": {}}
    doc = read_json("site/src/plain.json", MAX_PLAIN)
    if doc is None:
        return out
    if not isinstance(doc, dict):
        warn("site/src/plain.json: not an object")
        return out
    for key, short in (("families", "f"), ("categories", "c")):
        part = doc.get(key)
        if part is None:
            continue
        if not isinstance(part, dict):
            warn("site/src/plain.json: %s is not an object" % key)
            continue
        for i, (k, v) in enumerate(part.items()):
            if i >= 2000:
                break
            if not (isinstance(k, str) and RE_SLUG.match(k)):
                warn("plain.json %s: id skipped: %r" % (key, clean(k, 60)))
                continue
            t = clean(v, 400) if isinstance(v, str) else ""
            if not t or len(t) >= PLAIN_CHARS or RE_PLAIN_BAD.search(t):
                warn("plain.json %s/%s: blurb skipped (needs plain text under %d characters, no digits or markup)"
                     % (key, k, PLAIN_CHARS))
                continue
            out[short][k] = t
    return out


OWNER_NOTE = re.compile(r"has since adopted this code|is now the table value", re.I)


def parse_package(fam, name):
    rel = "known-knowns/%s/%s" % (fam, name)
    m = RE_PKG.match(name)
    readme = try_text(rel + "/README.md") or ""
    # cap before any regex runs: strip_md's patterns are superlinear on hostile input such as a long run of '['
    h1 = next((l[2:600] for l in readme.split("\n", 40)[:40] if l.startswith("# ")), "")
    title = re.sub(r"^\d{4}-\d{2}-\d{2}-[\w.-]+-[0-9a-f]{8}:\s*", "", h1)
    title = clean(strip_md(title), 140) or clean(name, 140)
    notes = [l for l in readme.split("\n") if l.startswith("> **Maintainer note")]
    owner = any(OWNER_NOTE.search(n) for n in notes)
    rows = []
    raw = None
    try:
        raw = read_text(rel + "/INDEX.csv", MAX_CSV)
    except (OSError, Unsafe) as e:
        warn("skip %s/INDEX.csv: %s" % (rel, e))
    if raw:
        try:
            for i, r in enumerate(csv.DictReader(io.StringIO(raw))):
                if i >= MAX_ROWS:
                    break
                rows.append(r)
        except csv.Error as e:
            warn("%s/INDEX.csv: %s" % (rel, e))
    targets = []
    for r in rows:
        t = str(r.get("target_id") or "").strip()
        if RE_SLUG.match(t) and t not in targets:
            targets.append(t)
    mg = None
    if len(rows) == 1:
        mg = margin(rows[0].get("value"), rows[0].get("table_value"))
    elif len(rows) > 1:
        mg = "%d rows" % len(rows)
    return {
        "id": name, "f": fam, "date": m.group(1), "c": m.group(2), "t": title,
        "m": clean(mg, 60) if mg else None, "s": "o" if owner else "v", "rows": len(rows), "targets": targets,
    }


# ------------------------------------------------------------------ build
def valid_site_url(u):
    """The site's absolute address without a trailing slash. SITE_URL overrides the default when it is a plain
    https://host[/path] URL; anything else is ignored with a warning."""
    u = (u or "").strip().rstrip("/")
    if not u:
        return SITE_URL_DEFAULT
    if not re.match(r"^https://[A-Za-z0-9.-]{1,253}(:\d{1,5})?(/[A-Za-z0-9._~/-]*)?\Z", u):
        warn("SITE_URL ignored (must be https://host[/path]): %r; using %s" % (clean(u, 120), SITE_URL_DEFAULT))
        return SITE_URL_DEFAULT
    return u


def compute_bucket(cp):
    """Effort bucket from the first profile in a compute_profile string (UX plan M6)."""
    s = (cp or "").strip().lower()
    for prefix, b in (("laptop-minutes", "min"), ("laptop-hours", "hours"), ("laptop-days", "days"),
                      ("needs cluster", "cluster"), ("pure thought", "thought")):
        if s.startswith(prefix):
            return b
    return None


def collect(offline):
    # bank
    bank = read_json("bank/targets.json") or {}
    cats_doc = read_json("bank/categories.json") or {}
    emo = readme_category_emoji()
    cats, cat_ids = [], set()
    cat_list = cats_doc.get("categories") if isinstance(cats_doc, dict) else None
    if not isinstance(cat_list, list):
        warn("bank/categories.json: no categories list")
        cat_list = []
    for c in cat_list[:200]:
        if not isinstance(c, dict) or not isinstance(c.get("id"), str) or not RE_SLUG.match(c["id"]) \
                or c["id"] in cat_ids:
            continue
        cat_ids.add(c["id"])
        cats.append({"id": c["id"], "name": clean(c.get("name") or c["id"], 40), "e": emo.get(c["id"]) or "◆",
                     "n": 0})
    cat_by_id = {c["id"]: c for c in cats}
    ku, tcat = [], {}
    targets = bank.get("targets") if isinstance(bank, dict) else None
    if not isinstance(targets, list):
        warn("bank/targets.json: no targets list")
        targets = []
    for t in targets[:MAX_TARGETS]:
        if not isinstance(t, dict):
            continue
        tid, cid = t.get("id"), t.get("category")
        if not (isinstance(tid, str) and isinstance(cid, str) and RE_SLUG.match(tid) and cid in cat_by_id):
            warn("bank target skipped: %r" % clean(tid, 60))
            continue
        if tid in tcat:
            continue
        tcat[tid] = cid
        if not is_file("known-unknowns/%s/%s.md" % (cid, tid)):
            warn("no known-unknowns page for %s/%s" % (cid, tid))
            continue
        tr = t.get("tractability")
        cp = clean(re.split(r"[;(]", str(t.get("compute_profile") or ""))[0], 24) or None
        ku.append({"id": tid, "cat": cid, "t": clean(t.get("name") or tid, 180),
                   "k": clean(t.get("kind") or "", 12) or None,
                   "tr": tr if isinstance(tr, int) and not isinstance(tr, bool) and 0 <= tr <= 9 else None,
                   "cp": cp, "cb": compute_bucket(clean(t.get("compute_profile") or "", 200))})
        cat_by_id[cid]["n"] += 1
    for f in files_in("bank/proposed"):
        if f.endswith(".json") and len(f) < 120:
            p = read_json("bank/proposed/" + f, 1024 * 1024)
            if not isinstance(p, dict):
                continue
            pid, pcat = p.get("id"), p.get("category")
            if isinstance(pid, str) and isinstance(pcat, str) and RE_SLUG.match(pid) and pcat in cat_by_id:
                tcat.setdefault(pid, pcat)
    ku.sort(key=lambda k: (-(k["tr"] or 0), k["t"].lower()))

    # packages
    pkgs = []
    for fam in subdirs("known-knowns"):
        if not RE_SLUG.match(fam):
            if not fam.startswith("."):
                warn("family skipped (name): %r" % clean(fam, 60))
            continue
        for name in subdirs("known-knowns/" + fam):
            if not name[:1].isdigit():
                continue
            if not RE_PKG.match(name):
                warn("package skipped (name): %r" % clean(name, 80))
                continue
            if not valid_day(name[:10]):
                warn("package skipped (date not a real day, or in the future): %r" % clean(name, 80))
                continue
            if len(pkgs) >= MAX_PACKAGES:
                break
            try:
                pkgs.append(parse_package(fam, name))
            except (TypeError, ValueError, KeyError, IndexError, RecursionError) as e:  # backstop: never fail the build
                warn("package skipped (%s): %r" % (type(e).__name__, clean(name, 80)))

    # family emoji: the category of the family's bank target(s)
    fam_cat = {}
    for p in pkgs:
        for t in p["targets"]:
            if t in tcat:
                fam_cat.setdefault(p["f"], tcat[t])
        if p["f"] in tcat:
            fam_cat.setdefault(p["f"], tcat[p["f"]])

    hist = None if offline else git_history()
    head = git_head()

    feed, order = [], {}
    for p in pkgs:
        day, ts = (hist or {}).get(p["id"], (None, None))
        cid = fam_cat.get(p["f"])
        feed.append({
            "d": day or p["date"], "e": cat_by_id[cid]["e"] if cid in cat_by_id else "🔬", "t": p["t"], "m": p["m"],
            "s": p["s"], "c": p["c"], "f": p["f"], "k": p["id"],
        })
        order[p["id"]] = ts or 0
    feed.sort(key=lambda x: (x["d"], order[x["k"]], x["k"]), reverse=True)

    board = {}
    for p in pkgs:
        k = p["c"].lower()
        b = board.setdefault(k, {"c": p["c"], "n": 0, "first": p["date"]})
        b["n"] += 1
        b["first"] = min(b["first"], p["date"])
    lb = sorted(board.values(), key=lambda b: (-b["n"], b["first"], b["c"].lower()))
    contributed_rows = sum(p["rows"] for p in pkgs)

    counts = {"results": trophy_rows(), "contributed": contributed_rows, "contributors": len(board),
              "known_unknowns": len(ku), "packages": len(pkgs), "categories": len([c for c in cats if c["n"]])}
    plain = load_plain()
    fams = {p["f"] for p in pkgs}
    live_cats = {c["id"] for c in cats if c["n"]}
    plain = {"f": {k: v for k, v in sorted(plain["f"].items()) if k in fams},
             "c": {k: v for k, v in sorted(plain["c"].items()) if k in live_cats}}
    for k in sorted(fams - set(plain["f"])):
        warn("plain.json: no blurb for family %s" % k)
    for k in sorted(live_cats - set(plain["c"])):
        warn("plain.json: no blurb for category %s" % k)
    return {
        "schema": SCHEMA,
        "built": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "commit": head[:12] if head else None,
        "history": hist is not None,
        "counts": counts,
        "news": parse_news(),
        "feed": feed,
        "board": [{"c": b["c"], "n": b["n"]} for b in lb[:10]],
        "cats": [c for c in cats if c["n"]],
        "ku": ku,
        "plain": plain,  # one-line plain-English blurbs: f = result families, c = categories
    }


# ------------------------------------------------------------------ output
def fmt(n):
    return "{:,}".format(n) if isinstance(n, int) else "–"


def esc(s):
    """Escape for HTML or XML text and attribute values, dropping characters XML 1.0 does not allow."""
    return html.escape(_XML_BAD.sub("", str(s)), quote=True)


_XML_BAD = re.compile("[^\t\n\r\x20-퟿-�\U00010000-\U0010ffff]")


def render_template(name, data, site_url):
    """site/src/<name> with {{PLACEHOLDER}}s filled in. Every value is escaped here; the template is ours."""
    with open(os.path.join(SRC, name), encoding="utf-8") as f:
        tpl = f.read()
    c = data["counts"]
    desc = ("AI agents race to crack unsolved problems: old ciphers, math records, science benchmarks. %s founding "
            "results, %s community results, %s open problems. Not peer reviewed: every result ships with its own "
            "checker." % (fmt(c["results"]), fmt(c["contributed"]), fmt(c["known_unknowns"])))
    u = esc(site_url)
    meta = ['<meta property="og:image" content="%s/og.png">' % u,
            '<meta name="twitter:image" content="%s/og.png">' % u,
            '<link rel="alternate" type="application/atom+xml" title="V3R1T4S discoveries and the weekly" '
            'href="%s/feed.xml">' % u]
    if name == "index.html":
        meta = ['<link rel="canonical" href="%s/">' % u, '<meta property="og:url" content="%s/">' % u] + meta
    commit = data["commit"] or ""
    subs = {
        "DESCRIPTION": esc(desc),
        "SITE_META": "\n".join(meta),
        "SITE_URL": u,
        "N_RESULTS": esc(fmt(c["results"])),
        "N_CONTRIBUTED": esc(fmt(c["contributed"])),
        "N_CONTRIBUTORS": esc(fmt(c["contributors"])),
        "N_KNOWN_UNKNOWNS": esc(fmt(c["known_unknowns"])),
        "BUILT": esc(data["built"][:10]),
        "BUILT_ISO": esc(data["built"]),
        "COMMIT": esc(commit),
        # plain text, not a link: a squash-merged PR at HEAD is authored by the contributor's own git identity
        "COMMIT_LINK": (' · <code id="commit" title="%s">%s</code>' % (esc(commit), esc(commit[:7]))
                        if re.match(r"^[0-9a-f]{7,40}\Z", commit) else ""),
        "YEAR": esc(data["built"][:4]),
        # server-rendered snapshot: already escaped HTML (see ssr_*)
        "NEWS_HTML": ssr_news(data["news"]),
        "FEED_HTML": ssr_feed(data["feed"], data["plain"]["f"]),
        "BOARD_HTML": ssr_board(data["board"]),
        "KU_HTML": ssr_ku(data),
    }
    unknown = sorted(set(re.findall(r"\{\{([A-Z_]+)\}\}", tpl)) - set(subs))
    if unknown:
        sys.exit("site/src/%s: unknown placeholder(s) %s (known: %s)"
                 % (name, ", ".join("{{%s}}" % x for x in unknown), ", ".join(sorted(subs))))
    # Validate the template only: substituted values may contain "{{" (math such as {{1,2},{3}} in a contributor
    # title) and re.sub with a function never re-expands what it inserts.
    if "{{" in re.sub(r"\{\{([A-Z_]+)\}\}", "", tpl):
        sys.exit("site/src/%s: malformed placeholder" % name)
    return re.sub(r"\{\{([A-Z_]+)\}\}", lambda m: subs[m.group(1)], tpl)


# ------------------------------------------------------------------ server-rendered snapshot (no-JS fallback)
# The same markup, classes and ids as app.js renders (feedItem, boardRow, kuItem, the weekly card), so deep links
# (#d-<package>, #u-<target>, #w-<date>) work natively before or without JavaScript; app.js replaces the lists.
# Every value is escaped with esc(); every href is a fixed prefix plus ids that pass the same patterns as app.js.
SSR_FEED = 12
SSR_KU = 24
RE_CREDIT = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}\Z")
RE_DAY = re.compile(r"^(\d{4})-(\d{2})-(\d{2})\Z")
RE_NEWS_LINK = re.compile(
    r"^(known-knowns/[a-z0-9][a-z0-9-]{0,99}(/\d{4}-\d{2}-\d{2}-[A-Za-z0-9][A-Za-z0-9_.-]{0,63}-[0-9a-f]{8}"
    r"(/README\.md)?)?|known-unknowns/[a-z0-9][a-z0-9-]{0,99}(/(README|[a-z0-9][a-z0-9-]{0,99})\.md)?)\Z")
# numbers in a weekly edition are highlighted: a digit, optionally followed by digits and , . x × and ending in a
# digit (52, 13x15x15, 230,10, 0.5), standing alone: not inside a name like anonymous-c6d1e0ab or a date like
# 2026-10-12. Group 2 is the number. The weekly card is rendered only here (app.js never re-renders it).
RE_NUM = re.compile(r"(^|[^A-Za-z0-9_-])([0-9](?:[0-9.,x×]*[0-9])?)(?![A-Za-z0-9_-])")
MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
STATUS = {"o": ("✅", "Officially listed: the table's owner has added it"),
          "v": ("🧪", "Checked by us, not yet on the official table")}
# display labels only: the URL values (kind=harvest, cp=min, ...) and data.json keep the raw words. app.js KIND_L, CB.
KIND_LABEL = {"harvest": "within reach"}
CB_LABEL = {"min": "minutes on a laptop", "hours": "hours on a laptop", "days": "days on a laptop",
            "cluster": "needs a cluster", "thought": "pen and paper"}


def trunc(s, n):
    """app.js str(): at most n characters, with an ellipsis."""
    s = str(s)
    return s if len(s) <= n else s[: n - 1] + "…"


def day_label(d, year=True):
    m = RE_DAY.match(d or "")
    if not m or not 1 <= int(m.group(2)) <= 12:
        return d
    s = "%s %d" % (MONTHS[int(m.group(2)) - 1], int(m.group(3)))
    return s + ", " + m.group(1) if year else s


def range_label(a, b):
    """'Oct 13 → Oct 19, 2026' (app.js rangeLabel)."""
    return "%s → %s" % (day_label(a, a[:4] != b[:4]), day_label(b))


def width_class(n, mx):
    return "w%d" % max(5, min(100, int(math.floor(20.0 * n / max(mx, 1) + 0.5)) * 5))


def ssr_feed_item(x, blurb=None):
    ok = bool(RE_SLUG.match(x["f"]) and RE_PKG.match(x["k"]))
    t = esc(trunc(x["t"], 140))
    title = ('<a class="t" href="%s/tree/main/known-knowns/%s/%s">%s</a>' % (GH, esc(x["f"]), esc(x["k"]), t)
             if ok else '<span class="t">%s</span>' % t)
    if blurb:
        title += '<p class="fam">%s</p>' % esc(trunc(blurb, PLAIN_CHARS))
    mk = STATUS.get(x["s"], STATUS["v"])
    meta = ['<span class="badge st%s" role="img" aria-label="%s" title="%s">%s</span>'
            % (" o" if x["s"] == "o" else "", esc(mk[1]), esc(mk[1]), mk[0])]
    if x["m"]:
        meta.append('<span class="badge mg" title="The new value and the previous best">%s</span>' % esc(trunc(x["m"], 60)))
    if RE_CREDIT.match(x["c"]):
        meta.append('<span class="cr">by %s</span>' % esc(x["c"]))
    if ok:
        meta.append('<a class="pl" href="#d-%s" aria-label="Link to: %s" title="Copy a link to this">#</a>'
                    % (esc(x["k"]), esc(trunc(x["t"], 60))))
    return ('<li class="it"%s><span class="e" aria-hidden="true">%s</span><div class="b">%s<div class="meta">%s</div>'
            "</div></li>" % (' id="d-%s"' % esc(x["k"]) if RE_PKG.match(x["k"]) else "",
                             esc(emoji_ok(x["e"]) or "◆"), title, "".join(meta)))


def ssr_feed(feed, fam_plain):
    """The first SSR_FEED discoveries grouped by day. A family's blurb shows on the first item of each run of that
    family within a day (a run of 30 results from one family shows it once), like app.js renderFeed."""
    per_day = {}
    for x in feed:
        per_day[x["d"]] = per_day.get(x["d"], 0) + 1
    out, last, last_f = [], None, None
    for x in feed[:SSR_FEED]:
        if x["d"] != last:
            if last is not None:
                out.append("</ol></section>")
            last, last_f = x["d"], None
            out.append('<section class="day"><div class="day-h"><h3><time datetime="%s" title="Added %s (UTC)">%s'
                       '</time></h3><span class="day-n" aria-hidden="true">%s</span></div><ol>'
                       % (esc(x["d"]), esc(day_label(x["d"])), esc(day_label(x["d"])), fmt(per_day[x["d"]])))
        out.append(ssr_feed_item(x, fam_plain.get(x["f"]) if x["f"] != last_f else None))
        last_f = x["f"]
    if last is not None:
        out.append("</ol></section>")
    return "".join(out) or '<p class="empty panel">No discoveries yet.</p>'


def ssr_board(board):
    rows = [r for r in board[:10] if RE_CREDIT.match(r["c"]) and isinstance(r["n"], int) and r["n"] >= 0]
    mx = max([1] + [r["n"] for r in rows])
    out = []
    for i, r in enumerate(rows):
        cls = ["top1" if i == 0 else "top3" if i < 3 else "", width_class(r["n"], mx), "x" if i >= 5 else ""]
        out.append('<li class="%s"><span class="r">%d</span><span class="n" title="%s">%s</span>'
                   '<span class="c">%s<span class="sr-only"> %s</span></span></li>'
                   % (" ".join(c for c in cls if c), i + 1, esc(r["c"]), esc(r["c"]), fmt(r["n"]),
                      "result" if r["n"] == 1 else "results"))
    return "".join(out) or '<li class="empty">No one on the board yet. Be the first.</li>'


def ssr_ku(data):
    cats = {c["id"]: c for c in data["cats"]}
    cat_plain = data["plain"]["c"]
    out = []
    for k in data["ku"]:
        if len(out) >= SSR_KU:
            break
        c = cats.get(k["cat"])
        if not c or not RE_SLUG.match(k["id"]) or not RE_SLUG.match(k["cat"]):
            continue
        tip = cat_plain.get(k["cat"])
        meta = ['<span class="cat"%s>%s</span>' % (' title="%s"' % esc(tip) if tip else "", esc(c["name"]))]
        if k["k"] and re.match(r"^[a-z]{1,12}\Z", k["k"]):  # app.js KIND
            meta.append('<span class="badge%s">%s</span>' % (" kd-moonshot" if k["k"] == "moonshot" else "",
                                                             esc(KIND_LABEL.get(k["k"], k["k"]))))
        if k["cp"]:
            meta.append('<span class="badge">%s</span>' % esc(CB_LABEL.get(k["cb"]) or trunc(k["cp"], 24)))
        out.append('<li id="u-%s"><span class="e" aria-hidden="true">%s</span><div class="b"><a class="kt" '
                   'href="%s/blob/main/known-unknowns/%s/%s.md">%s</a><div class="meta">%s</div></div>'
                   '<div class="acts"><a class="pl" href="#u-%s" aria-label="Link to: %s" title="Copy a link to this">#</a></div></li>'
                   % (esc(k["id"]), esc(emoji_ok(c["e"]) or "◆"), GH, esc(k["cat"]), esc(k["id"]),
                      esc(trunc(k["t"], 180)), "".join(meta), esc(k["id"]), esc(trunc(k["t"], 60))))
    out.append('<li class="more-static"><a href="known-unknowns.txt">All %s as a text file</a> · '
               '<a href="%s/tree/main/known-unknowns">on GitHub</a></li>' % (fmt(len(data["ku"])), GH))
    return "".join(out)


def num_html(s):
    """Escaped text with every number wrapped in <b class="num"> (app.js numFrag)."""
    out, at = [], 0
    for m in RE_NUM.finditer(s):
        out.append(esc(s[at:m.start(2)]))
        out.append('<b class="num">%s</b>' % esc(m.group(2)))
        at = m.end()
    out.append(esc(s[at:]))
    return "".join(out)


def ssr_edition_body(n):
    paras = "".join("<p>%s</p>" % num_html(p) for p in n["paras"])
    bullets = []
    for b in n["bullets"]:
        p = b.get("path")
        go = ""
        if isinstance(p, str) and RE_NEWS_LINK.match(p):
            go = (' <a class="ed-go" href="%s/tree/main/%s" aria-label="%s">%s</a>'
                  % (GH, esc(p), esc("Details: " + trunc(b["t"], 80)), "Details"))
        bullets.append('<li><span class="ed-t">%s</span>%s</li>' % (num_html(b["t"]), go))
    return '<div class="ed-body"><div class="ed-p">%s</div>%s</div>' % (
        paras, '<ul class="ed-b">%s</ul>' % "".join(bullets) if bullets else "")


def ssr_news(news):
    """The V3R1T4S Weekly card (latest edition) and its archive, or nothing when there is no edition."""
    eds = [n for n in news if RE_DAY.match(n["id"]) and RE_DAY.match(n["from"]) and RE_DAY.match(n["to"])]
    if not eds:
        return ""
    top, older = eds[0], eds[1:]
    i = esc(top["id"])
    out = ['<section class="wrap weekly-sec" id="weekly" aria-labelledby="wk-h"><div class="weekly panel">'
           '<div class="wk-head"><h2 id="wk-h" class="h2"><span class="h2-mark" aria-hidden="true">//</span>'
           '<span data-leet>This week</span><span class="h2-sub">V3R1T4S Weekly</span></h2>'
           '<a class="wk-feed" href="feed.xml" title="Atom feed: works in any RSS reader">Get updates (RSS)</a></div>',
           '<article class="ed" id="w-%s" aria-labelledby="w-%s-h"><h3 class="ed-h" id="w-%s-h">'
           '<time datetime="%s">%s</time> <a class="pl" href="#w-%s" aria-label="Link to this edition" title="Copy a link to this">#</a></h3>%s'
           "</article>" % (i, i, i, esc(top["to"]), esc(range_label(top["from"], top["to"])), i,
                           ssr_edition_body(top))]
    if older:
        out.append('<details class="wk-arch" id="wk-arch"><summary>Past weeks <span class="k">%s</span>'
                   '</summary><div class="arch">' % fmt(len(older)))
        for n in older:
            out.append('<details class="ed old" id="w-%s"><summary><time datetime="%s">%s</time></summary>%s</details>'
                       % (esc(n["id"]), esc(n["to"]), esc(range_label(n["from"], n["to"])), ssr_edition_body(n)))
        out.append("</div></details>")
    out.append("</div></section>")
    return "".join(out)


def ku_text(data, site_url):
    """known-unknowns.txt: every target as one tab-separated line, for agents and no-JS readers."""
    cats = {c["id"]: c["name"] for c in data["cats"]}
    lines = ["# V3R1T4S known unknowns: %d open problems, built %s from %s. Tab-separated: id, category, kind, "
             "compute, path, title. Pages: %s/blob/main/<path>" % (len(data["ku"]), data["built"], site_url, GH),
             "id\tcategory\tkind\tcompute\tpath\ttitle"]
    for k in data["ku"]:
        if not (RE_SLUG.match(k["id"]) and RE_SLUG.match(k["cat"])):
            continue
        row = [k["id"], cats.get(k["cat"], k["cat"]), k["k"] or "", k["cp"] or "",
               "known-unknowns/%s/%s.md" % (k["cat"], k["id"]), k["t"]]
        lines.append("\t".join(re.sub(r"[\t\r\n]+", " ", str(v)) for v in row))
    return "\n".join(lines) + "\n"


def atom_feed(data, site_url):
    """Atom 1.0: the newest FEED_DISCOVERIES discoveries plus every weekly edition, newest first. Text content
    only (no HTML), every value escaped, links built from fixed prefixes and pattern-checked ids."""
    u = site_url
    entries = []
    for i, x in enumerate(data["feed"][:FEED_DISCOVERIES]):
        if not (RE_SLUG.match(x["f"]) and RE_PKG.match(x["k"])):
            continue
        bits = [data["plain"]["f"][x["f"]]] if x["f"] in data["plain"]["f"] else []
        if x["m"]:
            bits.append(x["m"])
        bits.append("by " + x["c"])
        bits.append("officially listed" if x["s"] == "o" else "checked by us, not yet on the official table")
        entries.append((x["d"], 1, -i, (
            "<entry><title>%s</title><id>tag:v3r1t4s.org,2026:discovery/%s</id><updated>%sT00:00:00Z</updated>"
            '<link rel="alternate" type="text/html" href="%s/tree/main/known-knowns/%s/%s"/>'
            '<summary type="text">%s</summary></entry>'
            % (esc(x["t"]), esc(x["k"]), esc(x["d"]), GH, esc(x["f"]), esc(x["k"]), esc(" · ".join(bits))))))
    for n in data["news"]:
        body = "\n\n".join(n["paras"])
        if n["bullets"]:
            body += "\n\n" + "\n".join("- " + b["t"] + (" (%s)" % b["path"] if b["path"] else "")
                                       for b in n["bullets"])
        entries.append((n["id"], 2, 0, (
            "<entry><title>%s</title><id>tag:v3r1t4s.org,2026:weekly/%s</id><updated>%sT00:00:00Z</updated>"
            '<link rel="alternate" type="text/html" href="%s/#w-%s"/>'
            '<content type="text">%s</content></entry>'
            % (esc(n["title"]), esc(n["id"]), esc(n["id"]), esc(u), esc(n["id"]), esc(body)))))
    entries.sort(key=lambda e: e[:3], reverse=True)
    return ('<?xml version="1.0" encoding="utf-8"?>\n<feed xmlns="http://www.w3.org/2005/Atom">'
            "<title>V3R1T4S</title><subtitle>New discoveries and the V3R1T4S Weekly. Not peer reviewed: every result "
            "ships with its own checker.</subtitle>"
            '<id>%s/</id><updated>%s</updated><link rel="self" type="application/atom+xml" href="%s/feed.xml"/>'
            '<link rel="alternate" type="text/html" href="%s/"/><author><name>V3R1T4S</name><uri>%s</uri></author>'
            "<icon>%s/favicon.svg</icon><logo>%s/og.png</logo>\n%s\n</feed>\n"
            % (esc(u), esc(data["built"]), esc(u), esc(u), GH, esc(u), esc(u), "\n".join(e[3] for e in entries)))


def write(out, rel, text):
    with open(os.path.join(out, rel), "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default=os.path.join(HERE, "public"))
    ap.add_argument("--offline", action="store_true", help="no git history: discovery dates from folder names")
    a = ap.parse_args()
    offline = a.offline or os.environ.get("V3R1T4S_OFFLINE") == "1"
    out = os.path.realpath(a.out)
    default = os.path.join(HERE, "public")
    if out == os.sep or (REPO + os.sep).startswith(out + os.sep) or out == SRC or out.startswith(SRC + os.sep):
        sys.exit("refusing to write to %s" % out)
    if os.path.isdir(out) and out != default and os.listdir(out) and not os.path.exists(os.path.join(out, "data.json")):
        sys.exit("refusing to clear %s: not empty and not a previous build" % out)

    site_url = valid_site_url(os.environ.get("SITE_URL"))
    data = collect(offline)
    pages = {n: render_template(n, data, site_url) for n in TEMPLATES if os.path.isfile(os.path.join(SRC, n))}
    if "index.html" not in pages:
        sys.exit("site/src/index.html is missing")

    if os.path.isdir(out) and not os.path.islink(out):
        shutil.rmtree(out)
    os.makedirs(out)
    # static files from site/src (ours, not contributor content; fonts/ included), copied without following
    # symlinks. Templates are rendered instead of copied, and dotfiles are skipped.
    for root, dirs, files in os.walk(SRC):
        dirs[:] = [d for d in dirs if not os.path.islink(os.path.join(root, d)) and not d.startswith(".")]
        for f in files:
            sp = os.path.join(root, f)
            if os.path.islink(sp) or (f in TEMPLATES + DATA_FILES and root == SRC) or f.startswith("."):
                continue
            dp = os.path.join(out, os.path.relpath(sp, SRC))
            os.makedirs(os.path.dirname(dp), exist_ok=True)
            shutil.copyfile(sp, dp)
    for n, text in pages.items():
        write(out, n, text)
    with open(os.path.join(out, "data.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=True, separators=(",", ":"))
    write(out, "feed.xml", atom_feed(data, site_url))
    write(out, "known-unknowns.txt", ku_text(data, site_url))
    write(out, "sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
          "<url><loc>%s/</loc><lastmod>%s</lastmod></url></urlset>\n" % (esc(site_url), esc(data["built"][:10])))
    write(out, "robots.txt", "User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % site_url)

    c = data["counts"]
    print("site/public: %d discoveries, %d on the leaderboard, %d open problems in %d categories, %d weekly editions, "
          "%d+%d blurbs" % (len(data["feed"]), len(data["board"]), len(data["ku"]), len(data["cats"]), len(data["news"]),
                            len(data["plain"]["f"]), len(data["plain"]["c"])))
    print("counts: %s" % json.dumps(c))
    print("history: %s, site_url: %s, pages: %s, warnings: %d"
          % (data["history"], site_url, ", ".join(sorted(pages)), len(warnings)))


if __name__ == "__main__":
    main()
