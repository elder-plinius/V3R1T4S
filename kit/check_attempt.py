#!/usr/bin/env python3
"""Check an attempt record, attempts/<target-id>/<attempt-id>.md (format: kit/ATTEMPTS.md). Standard library only.

Usage: python3 kit/check_attempt.py FILE [FILE ...]
The last output line is CHECK_ATTEMPT: PASS or CHECK_ATTEMPT: FAIL (exit status 0 or 1).
"""
import datetime
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUN_STATUS = ("NOTHING", "PROMISING", "REFUTED", "CONFIRMED_PARTIAL", "CONFIRMED_SOLUTION")
LEVELS = ("nothing", "negative", "progress", "partial_win_claim", "solution_claim")
OPEN_KEYS = ("target", "date", "credit", "run_status", "prereg_sha256", "budget", "compared_with", "closest", "lenses", "claims")
OPTIONAL_KEYS = ("prereg_url",)
COMMIT_KEYS = ("target", "date", "credit", "run_status", "commitment")
SECTIONS = ("## What was tried", "## Why it fell short")
MAX_BYTES = 32768
LEAKS = (
    (r"(?<![\w.~-])/(Users|home|root|private/var|var/folders)/", "absolute path"),
    (r"\b[A-Za-z]:\\", "Windows path"),
    (r"[\w.+-]+@[\w-]+(\.[\w-]+)+", "e-mail address"),
    (r"\b(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}|\bgithub_pat_[A-Za-z0-9_]{20,}|\bsk-[A-Za-z0-9]{20,}|\bAKIA[0-9A-Z]{16}\b|\bxox[abp]-[A-Za-z0-9-]{10,}",
     "token-like string"),
)


def load_targets(root=None):
    with open(os.path.join(root or ROOT, "bank", "targets.json"), encoding="utf-8") as f:
        data = json.load(f)
    items = data if isinstance(data, list) else data.get("targets", data)
    return {e["id"]: e for e in items}


def parse(text):
    """Return (title line, header dict, duplicate keys, remaining lines)."""
    lines = text.split("\n")
    title = lines[0].strip() if lines else ""
    header, dups, i = {}, [], 1
    while i < len(lines) and not lines[i].strip():
        i += 1
    while i < len(lines) and lines[i].strip():
        m = re.match(r"([a-z0-9_]+):[ \t]*(.*)$", lines[i])
        if not m:
            break
        key, value = m.group(1), m.group(2).strip()
        if key in header:
            dups.append(key)
        header[key] = value
        i += 1
    return title, header, dups, lines[i:]


def check(path, root=None, today=None):
    """Return a list of problems (empty when the record passes)."""
    root = root or ROOT
    problems = []
    with open(path, "rb") as f:
        raw = f.read()
    if len(raw) > MAX_BYTES:
        problems.append(f"larger than {MAX_BYTES} bytes")
    try:
        text = raw.decode("utf-8").replace("\r\n", "\n")
    except UnicodeDecodeError:
        return problems + ["not UTF-8"]
    title, h, dups, rest = parse(text)
    for k in dups:
        problems.append(f"field {k} given twice")
    targets = load_targets(root)
    tid = h.get("target", "")
    if tid not in targets:
        problems.append(f"target {tid!r} is not an id in bank/targets.json")
    commit_only = targets.get(tid, {}).get("disclosure") == "commit-only"
    keys = COMMIT_KEYS if commit_only else OPEN_KEYS
    allowed = set(keys) | (set() if commit_only else set(OPTIONAL_KEYS))
    for k in keys:
        if not h.get(k):
            problems.append(f"missing field {k}")
    for k in h:
        if k not in allowed:
            problems.append(f"field {k} is not allowed" + (" for a commit-only target" if commit_only else ""))
    date = h.get("date", "")
    try:
        d = datetime.date.fromisoformat(date) if re.fullmatch(r"\d{4}-\d{2}-\d{2}", date) else None
    except ValueError:
        d = None
    today = today or datetime.datetime.now(datetime.timezone.utc).date()
    if d is None:
        problems.append("date must be YYYY-MM-DD (UTC date of the run)")
    elif d > today:
        problems.append("date lies in the future")
    credit = h.get("credit", "")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", credit):
        problems.append("credit must be lowercase letters, digits and hyphens (as in submission ids)")
    if h.get("run_status", "") not in RUN_STATUS:
        problems.append("run_status must be one of " + ", ".join(RUN_STATUS))
    if commit_only:
        digest = h.get("commitment", "")
        if not re.fullmatch(r"[0-9a-f]{64}", digest):
            problems.append("commitment must be a lowercase sha256 hex digest (of the private salt and notes)")
        if any(line.strip() for line in rest):
            problems.append("a commit-only record is the header only: no method text (DONT_SPOIL_THE_HUNT.md)")
    else:
        digest = h.get("prereg_sha256", "")
        if not re.fullmatch(r"[0-9a-f]{64}", digest):
            problems.append("prereg_sha256 must be a lowercase sha256 hex digest of the run's PREREG.md")
        lenses = [x.strip() for x in h.get("lenses", "").split(",") if x.strip()]
        for item in lenses:
            m = re.fullmatch(r"([a-z0-9]+(?:-[a-z0-9]+)*)=([a-z_]+)", item)
            if not m or m.group(2) not in LEVELS:
                problems.append(f"lens entry {item!r} must be name=level with level one of " + ", ".join(LEVELS))
        if h.get("lenses") and not lenses:
            problems.append("lenses lists no lens")
        claims = h.get("claims", "")
        if claims and not re.fullmatch(r"none|#\d+(, #\d+)*", claims):
            problems.append("claims must be 'none' or pull request numbers like '#484, #485'")
        body = "\n".join(rest)
        for s in SECTIONS:
            if not re.search(r"(?m)^" + re.escape(s) + r"[ \t]*$", body):
                problems.append(f"missing section '{s}'")
    expected = f"{date}-{credit}-{digest[:8]}"
    if title != f"# Attempt {expected}":
        problems.append(f"title must be '# Attempt {expected}'")
    if os.path.basename(path) != expected + ".md":
        problems.append(f"file name must be {expected}.md")
    if os.path.basename(os.path.dirname(os.path.abspath(path))) != tid:
        problems.append(f"the record must sit in attempts/{tid}/")
    for pattern, what in LEAKS:
        if re.search(pattern, text):
            problems.append(f"contains a {what}")
    return problems


def main(argv=None):
    paths = sys.argv[1:] if argv is None else argv
    if not paths:
        print(__doc__.strip())
        print("CHECK_ATTEMPT: FAIL")
        return 1
    bad = 0
    for p in paths:
        probs = check(p)
        for msg in probs:
            print(f"{p}: {msg}")
        bad += bool(probs)
    print("CHECK_ATTEMPT: " + ("PASS" if not bad else "FAIL"))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
