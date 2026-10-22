#!/usr/bin/env python3
"""Parse and verify the lenses' FROZEN.md freeze records, and emit the entries JSON that stage2.py / score_test.py /
val_table.py consume (run 2026-10-18-0202). Written by the tools engineer (Opus 5.5) while the lenses were running,
before any surprise-test gold was read. Standard library only; reads no gold.

For every <attempts-root>/*/FROZEN.md it reads each freeze record (a block headed `## frozen <utc>` with lines
ROLE=, lens=, code=, out=, code_tree_sha256=, results_tree_sha256=, then a `### code files` list and a
`### result files` list of "<sha256>  <relpath>" lines, exactly as tools/q15h.py `freeze` writes them). For each
record it:
  - checks the freeze time is <= the freeze deadline (PREREG rule 8: 2026-10-18T05:45:00Z), else the record is
    reported INELIGIBLE (late);
  - recomputes the code tree hash and the results tree hash EXACTLY as q15h.tree() does (same file selection as
    q15h.cmd_freeze: code files are every file under code/ that is not a .pyc and not under __pycache__; result files
    are every file under the ROLE folder named result-*.tsv that is not under a parts/ directory), and compares both
    the aggregate tree hashes and every per-file line against the record;
  - checks the PREREG rule 8 result files exist (val 0.10, 0.20, 0.30, 0.50 and test 0.10, 0.20, 0.30, all 10
    surprise families: 70 files);
  - looks for a test-mode audit output file somewhere in the ROLE folder (any path whose name contains "audit"; the
    name is not fixed, so a missing one is reported as a warning, not an eligibility failure) and reports whether its
    text says AUDIT PASS / FAIL.
It keeps the LAST record per (lens, ROLE) (latest append wins), and writes, in freeze-time order:
  - an entries JSON: [{"name": "<lens>/<ROLE>", "dir": "<absolute ROLE folder>"}] of the ELIGIBLE records
    (eligibility = freeze time ok AND code tree hash matches AND results tree hash matches AND all 70 rule-8 files
    present);
  - a markdown table of every kept record with its verification columns (eligible or the reason it is not).

The code=/out= paths in a record are relative to the run root (the parent of the attempts root), as q15h.freeze
writes them; --attempts-root lets you point at a mock tree for testing (then the run root is its parent).

usage: python3 -I tools/check_freezes.py [--attempts-root DIR] [--out-json FILE] [--out-md FILE] [--deadline UTC]
"""
import argparse
import calendar
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import q15h  # noqa: E402  (q15h.tree / q15h.sha256 / q15h.FAMS, so hashing is byte-identical to freeze)

DEADLINE = "2026-10-18T05:45:00Z"
REQUIRED = [("val", p) for p in ("0.10", "0.20", "0.30", "0.50")] + [("test", p) for p in ("0.10", "0.20", "0.30")]


def parse_epoch(utc_str):
    return calendar.timegm(time.strptime(utc_str, "%Y-%m-%dT%H:%M:%SZ"))


def parse_frozen(path):
    """Yield one dict per '## frozen' block in a FROZEN.md file, in file order."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    records = []
    cur = None
    section = None
    for line in text.splitlines():
        if line.startswith("## frozen "):
            if cur is not None:
                records.append(cur)
            cur = {"time": line[len("## frozen "):].strip(), "code_files": [], "result_files": [],
                   "src": path}
            section = None
            continue
        if cur is None:
            continue
        if line.startswith("ROLE="):
            for tok in line.split():
                if "=" in tok:
                    k, v = tok.split("=", 1)
                    if k in ("ROLE", "lens", "code", "out"):
                        cur[k] = v
        elif line.startswith("code_tree_sha256="):
            cur["code_tree_sha256"] = line.split("=", 1)[1].strip()
        elif line.startswith("results_tree_sha256="):
            cur["results_tree_sha256"] = line.split("=", 1)[1].strip()
        elif line.strip() == "### code files":
            section = "code_files"
        elif line.strip() == "### result files":
            section = "result_files"
        elif section and line.strip():
            parts = line.split("  ", 1)
            if len(parts) == 2:
                cur[section].append((parts[0].strip(), parts[1].strip()))
    if cur is not None:
        records.append(cur)
    return records


def code_files(code_dir):
    return [os.path.join(r, f) for r, _, fs in os.walk(code_dir) for f in fs
            if not f.endswith(".pyc") and "__pycache__" not in r]


def result_files(out_dir):
    return [os.path.join(r, f) for r, _, fs in os.walk(out_dir) for f in fs
            if f.startswith("result-") and f.endswith(".tsv") and os.sep + "parts" not in r]


def find_audit(out_dir):
    hits = []
    for r, _, fs in os.walk(out_dir):
        for f in fs:
            if "audit" in f.lower():
                hits.append(os.path.join(r, f))
    verdict = None
    for h in hits:
        try:
            with open(h, encoding="utf-8", errors="replace") as fh:
                t = fh.read()
            if "AUDIT PASS" in t or "AUDIT\tPASS" in t:
                verdict = "PASS" if verdict in (None, "PASS") else verdict
            if "AUDIT FAIL" in t or "FAIL" in t and "AUDIT" in t:
                verdict = "FAIL"
        except OSError:
            pass
    return sorted(hits), verdict


def verify(rec, run_root):
    """Fill rec with verification results; set rec['eligible'] and rec['reasons']."""
    reasons = []
    rec["name"] = "%s/%s" % (rec.get("lens", "?"), rec.get("ROLE", "?"))
    code_dir = os.path.join(run_root, rec.get("code", ""))
    out_dir = os.path.join(run_root, rec.get("out", ""))
    rec["code_dir"], rec["out_dir"] = code_dir, out_dir
    # freeze time
    try:
        rec["late"] = parse_epoch(rec["time"]) > parse_epoch(rec["deadline"])
    except (ValueError, KeyError):
        rec["late"] = True
        reasons.append("unparseable freeze time")
    if rec.get("late"):
        reasons.append("freeze after deadline %s" % rec.get("deadline"))
    # code tree
    if os.path.isdir(code_dir):
        _, ch = q15h.tree(code_files(code_dir), code_dir)
        rec["code_hash_recomputed"] = ch
        rec["code_hash_ok"] = (ch == rec.get("code_tree_sha256"))
    else:
        rec["code_hash_ok"] = False
        reasons.append("code dir missing: %s" % code_dir)
    if not rec.get("code_hash_ok", False) and os.path.isdir(code_dir):
        reasons.append("code tree hash mismatch")
    # results tree
    if os.path.isdir(out_dir):
        rlines, rh = q15h.tree(result_files(out_dir), out_dir)
        rec["results_hash_recomputed"] = rh
        rec["results_hash_ok"] = (rh == rec.get("results_tree_sha256"))
        rec["n_result_files"] = len(rlines)
    else:
        rec["results_hash_ok"] = False
        rec["n_result_files"] = 0
        reasons.append("out dir missing: %s" % out_dir)
    if not rec.get("results_hash_ok", False) and os.path.isdir(out_dir):
        reasons.append("results tree hash mismatch")
    # per-file line agreement (stronger than the aggregate hash alone)
    rec["code_lines_match"] = (q15h.tree(code_files(code_dir), code_dir)[0] ==
                               [f"{h}  {p}" for h, p in rec["code_files"]]) if os.path.isdir(code_dir) else False
    rec["result_lines_match"] = (q15h.tree(result_files(out_dir), out_dir)[0] ==
                                  [f"{h}  {p}" for h, p in rec["result_files"]]) if os.path.isdir(out_dir) else False
    # rule 8 files
    missing = []
    for mode, p in REQUIRED:
        for fam in q15h.FAMS:
            q = os.path.join(out_dir, mode, p, fam, "result-%s.tsv" % p)
            if not os.path.isfile(q):
                missing.append("%s/%s/%s" % (mode, p, fam))
    rec["rule8_missing"] = missing
    rec["rule8_ok"] = not missing
    if missing:
        reasons.append("rule-8 files missing (%d; e.g. %s)" % (len(missing), ", ".join(missing[:3])))
    # audit file
    audits, verdict = find_audit(out_dir) if os.path.isdir(out_dir) else ([], None)
    rec["audit_files"] = audits
    rec["audit_verdict"] = verdict
    if not audits:
        reasons.append("WARNING no audit output file found (reported, not an eligibility failure)")
    rec["eligible"] = (not rec.get("late") and rec.get("code_hash_ok") and rec.get("results_hash_ok")
                       and rec.get("rule8_ok"))
    rec["reasons"] = reasons
    return rec


def main():
    ap = argparse.ArgumentParser(description="Verify FROZEN.md records and emit the stage2/score_test entries JSON")
    ap.add_argument("--attempts-root", default=os.path.join(q15h.RUN, "attempts"),
                    help="folder of <lens>/FROZEN.md (default RUN/attempts); code=/out= are relative to its parent")
    ap.add_argument("--out-json", default=os.path.join(q15h.RUN, "out", "frozen_entries.json"))
    ap.add_argument("--out-md", default=os.path.join(q15h.RUN, "out", "frozen_entries.md"))
    ap.add_argument("--deadline", default=DEADLINE)
    a = ap.parse_args()
    attempts_root = os.path.abspath(a.attempts_root)
    run_root = os.path.dirname(attempts_root)
    files = []
    if os.path.isdir(attempts_root):
        for d in sorted(os.listdir(attempts_root)):
            q = os.path.join(attempts_root, d, "FROZEN.md")
            if os.path.isfile(q):
                files.append(q)
    print("check_freezes: attempts-root %s ; run-root %s ; %d FROZEN.md files" % (
        attempts_root, run_root, len(files)), flush=True)
    all_records = []
    for q in files:
        for order, rec in enumerate(parse_frozen(q)):
            rec["deadline"] = a.deadline
            rec["order"] = (q, order)
            all_records.append(rec)
    # last record per (lens, ROLE)
    last = {}
    for rec in all_records:
        key = (rec.get("lens"), rec.get("ROLE"))
        last[key] = rec   # file order: later append overwrites
    kept = list(last.values())
    for rec in kept:
        verify(rec, run_root)
    kept.sort(key=lambda r: (r.get("time", ""), r["name"]))
    eligible = [r for r in kept if r["eligible"]]
    entries = [{"name": r["name"], "dir": os.path.abspath(r["out_dir"])} for r in eligible]
    os.makedirs(os.path.dirname(os.path.abspath(a.out_json)), exist_ok=True)
    import json
    with open(a.out_json, "w") as f:
        json.dump(entries, f, indent=1)
    # markdown table
    hdr = ("| name | freeze time | eligible | code hash | results hash | result files | rule8 | "
           "audit file | reasons / warnings |")
    sep = "|" + "---|" * 9
    rows = [hdr, sep]
    for r in kept:
        audit = ("%d file(s), verdict %s" % (len(r["audit_files"]), r["audit_verdict"])) if r["audit_files"] else "MISSING"
        rows.append("| %s | %s | %s | %s | %s | %d/70 | %s | %s | %s |" % (
            r["name"], r.get("time", "?"), "yes" if r["eligible"] else "NO",
            "ok" if r.get("code_hash_ok") else "MISMATCH",
            "ok" if r.get("results_hash_ok") else "MISMATCH",
            70 - len(r.get("rule8_missing", [])),
            "ok" if r.get("rule8_ok") else "MISSING %d" % len(r.get("rule8_missing", [])),
            audit, "; ".join(r["reasons"]) or "-"))
    md = ("# Frozen entries (run 2026-10-18-0202)\n\nattempts-root: `%s`\ndeadline: %s\ngenerated: %s\n\n"
          "Eligible entries written to the entries JSON (freeze-time order): %s\n\n%s\n" % (
              attempts_root, a.deadline, q15h.utc(), ", ".join(e["name"] for e in entries) or "(none)",
              "\n".join(rows)))
    os.makedirs(os.path.dirname(os.path.abspath(a.out_md)), exist_ok=True)
    with open(a.out_md, "w") as f:
        f.write(md)
    print(md)
    print("wrote %d eligible entries to %s and the table to %s" % (len(entries), a.out_json, a.out_md), flush=True)
    for r in kept:
        print("  %-28s %s  code=%s results=%s rule8=%s audit=%s%s" % (
            r["name"], r.get("time"), "ok" if r.get("code_hash_ok") else "MISMATCH",
            "ok" if r.get("results_hash_ok") else "MISMATCH", "ok" if r.get("rule8_ok") else "MISSING",
            r["audit_verdict"] or ("none" if not r["audit_files"] else "?"),
            "" if r["eligible"] else "  -> INELIGIBLE (%s)" % "; ".join(r["reasons"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
