#!/usr/bin/env python3
"""Parse and verify the lenses' FROZEN.md freeze records, and emit the entries JSON that stage2.py / score_test.py /
val_table.py consume (run 2026-10-18-0202). Written by the tools engineer (Opus 5.5) while the lenses were running,
before any surprise-test gold was read. Standard library only; reads no gold.

Run 2026-10-18-0839 copy (tools engineer, Opus 5.5, while the lenses were running; the record parser, the hash
recomputation and the last-record-binds rule are unchanged). Changed for this run, and nothing else:
  - deadline 2026-10-18T12:40:00Z (PREREG rule 8 of this run);
  - required result files: val/0.50 and test/0.50 for all 10 surprise families (20 files);
  - the test-mode audit is now an eligibility condition: attempts/<lens>/frozen/<ROLE>/audit_test_0.50.txt must exist
    and its last non-empty line must be exactly "AUDIT PASS" (if that file is missing, out=/audit_test_0.50.txt of the
    record is used, with a warning);
  - a record whose lens= field differs from the folder it was read from is ineligible (and is kept apart from that
    lens's own records, so it cannot displace them);
  - the entries JSON carries "freeze_time" ([{"name","dir","freeze_time"}...]);
  - --carried FILE (RUN/carry/carry_entries.json) appends the carried entries of run 2026-10-18-0202 (PREREG rule 8):
    name r0202-<lens>/<ROLE>, dir = the carry folder carry/<lens>-<ROLE>. For each one the 0202 freeze record is read
    from <src>/../../FROZEN.md (the last record of that lens and ROLE binds; only FROZEN.md is opened there), and the
    entry is eligible only if: the record's time, code_tree_sha256 and results_tree_sha256 equal the carry file's
    values; the code tree of carry/<lens>-<ROLE>/code, recomputed exactly as q15h.tree() does, equals the record (tree
    hash and every per-file line); every carry/<lens>-<ROLE>/val/0.50/<fam>/result-0.50.tsv has the sha256 the record
    lists for val/0.50/<fam>/result-0.50.tsv (byte copies of the frozen val files); test/0.50 holds all 10 result files;
    run_test_0.50.txt shows all 10 families "ok"; audit_test_0.50.txt ends "AUDIT PASS"; freeze time <= deadline.
    If the 0202 record cannot be read, the carry file's values are used and the entry is reported with a warning.

For every <attempts-root>/*/FROZEN.md it reads each freeze record (a block headed `## frozen <utc>` with lines
ROLE=, lens=, code=, out=, code_tree_sha256=, results_tree_sha256=, then a `### code files` list and a
`### result files` list of "<sha256>  <relpath>" lines, exactly as tools/q15h.py `freeze` writes them). For each
record it:
  - checks the freeze time is <= the freeze deadline, else the record is reported INELIGIBLE (late);
  - recomputes the code tree hash and the results tree hash EXACTLY as q15h.tree() does (same file selection as
    q15h.cmd_freeze: code files are every file under code/ that is not a .pyc and not under __pycache__; result files
    are every file under the ROLE folder named result-*.tsv that is not under a parts/ directory), and compares both
    the aggregate tree hashes and every per-file line against the record;
  - checks the rule 8 result files exist (val 0.50 and test 0.50, all 10 surprise families);
  - checks the audit file (see above).
It keeps the LAST record per (lens, ROLE) (latest append wins, even if that record is late or broken), and writes, in
freeze-time order (new entries first, then the carried entries in the carry file's order):
  - an entries JSON: [{"name": "<lens>/<ROLE>", "dir": "<absolute ROLE folder>", "freeze_time": "<utc>"}] of the
    ELIGIBLE records;
  - a markdown table of every kept record with its verification columns (eligible or the reason it is not).

The code=/out= paths in a record are relative to the run root (the parent of the attempts root), as q15h.freeze
writes them; --attempts-root lets you point at a mock tree for testing (then the run root is its parent).

usage: python3 -I tools/check_freezes.py [--attempts-root DIR] [--carried RUN/carry/carry_entries.json]
           [--out-json FILE] [--out-md FILE] [--deadline UTC]
"""
import argparse
import calendar
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import q15h  # noqa: E402  (q15h.tree / q15h.sha256 / q15h.FAMS, so hashing is byte-identical to freeze)

DEADLINE = "2026-10-18T12:40:00Z"   # run 2026-10-18-0839 (was 2026-10-18T05:45:00Z)
P = "0.50"
REQUIRED = [("val", P), ("test", P)]   # run 2026-10-18-0839: 20 files (was 70: val 0.10-0.50, test 0.10-0.30)
N_REQUIRED = len(REQUIRED) * len(q15h.FAMS)
AUDIT_NAME = "audit_test_%s.txt" % P


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


def audit_last_line(path):
    """run 2026-10-18-0839: (exists, last non-empty line stripped) of a saved audit output."""
    if not os.path.isfile(path):
        return False, None
    with open(path, encoding="utf-8", errors="replace") as fh:
        lines = [ln.strip() for ln in fh if ln.strip()]
    return True, (lines[-1] if lines else "")


def check_audit(rec, paths):
    """run 2026-10-18-0839: the first existing path of `paths` must end 'AUDIT PASS'."""
    for i, q in enumerate(paths):
        ok, last = audit_last_line(q)
        if ok:
            rec["audit_file"] = q
            rec["audit_last_line"] = last
            rec["audit_ok"] = (last == "AUDIT PASS")
            if i > 0:
                rec["reasons"].append("WARNING audit read from %s (not at the PREREG path)" % q)
            if not rec["audit_ok"]:
                rec["reasons"].append("audit file does not end 'AUDIT PASS' (last line %r)" % (last or "")[:60])
            return
    rec["audit_file"] = None
    rec["audit_last_line"] = None
    rec["audit_ok"] = False
    rec["reasons"].append("no %s" % AUDIT_NAME)


def rule8(rec, out_dir):
    missing = []
    for mode, p in REQUIRED:
        for fam in q15h.FAMS:
            q = os.path.join(out_dir, mode, p, fam, "result-%s.tsv" % p)
            if not os.path.isfile(q):
                missing.append("%s/%s/%s" % (mode, p, fam))
    rec["rule8_missing"] = missing
    rec["rule8_ok"] = not missing
    if missing:
        rec["reasons"].append("rule-8 files missing (%d; e.g. %s)" % (len(missing), ", ".join(missing[:3])))


def verify(rec, run_root, attempts_root=None, folder_lens=None):
    """Fill rec with verification results; set rec['eligible'] and rec['reasons']."""
    reasons = []
    rec["reasons"] = reasons
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
    # run 2026-10-18-0839: the record must name the lens folder it sits in
    rec["lens_ok"] = folder_lens is None or rec.get("lens") == folder_lens
    if not rec["lens_ok"]:
        reasons.append("lens= field %r differs from its folder %r" % (rec.get("lens"), folder_lens))
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
    if os.path.isdir(code_dir) and not rec["code_lines_match"]:
        reasons.append("code file lines differ from the record")
    if os.path.isdir(out_dir) and not rec["result_lines_match"]:
        reasons.append("result file lines differ from the record")
    # rule 8 files
    rule8(rec, out_dir)
    # audit file (run 2026-10-18-0839: required, at attempts/<lens>/frozen/<ROLE>/audit_test_0.50.txt)
    paths = []
    if attempts_root is not None:
        paths.append(os.path.join(attempts_root, rec.get("lens", "?"), "frozen", rec.get("ROLE", "?"), AUDIT_NAME))
    paths.append(os.path.join(out_dir, AUDIT_NAME))
    check_audit(rec, paths)
    audits, verdict = find_audit(out_dir) if os.path.isdir(out_dir) else ([], None)
    rec["audit_files"] = audits
    rec["audit_verdict"] = verdict
    rec["eligible"] = bool(not rec.get("late") and rec.get("lens_ok") and rec.get("code_hash_ok")
                           and rec.get("results_hash_ok") and rec.get("code_lines_match")
                           and rec.get("result_lines_match") and rec.get("rule8_ok") and rec.get("audit_ok"))
    return rec


def run_log_ok(path):
    """run 2026-10-18-0839: families whose line in a saved `q15h.py run --mode test` output says ok."""
    ok = set()
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8", errors="replace") as fh:
        for ln in fh:
            t = ln.split()
            # "<utc> test 0.50 <fam> ok <n> rows <s>s"
            if len(t) >= 5 and t[1] == "test" and t[2] == P and t[3] in q15h.FAMS and t[4] == "ok":
                ok.add(t[3])
    return ok


def verify_carried(e, deadline):
    """run 2026-10-18-0839: one carried entry of run 2026-10-18-0202 (see the docstring)."""
    reasons = []
    lens, role = e["name"].split("/")
    d = os.path.abspath(e["dir"])
    rec = {"name": "r0202-%s/%s" % (lens, role), "dir": d, "out_dir": d, "carried": True, "reasons": reasons,
           "lens": "r0202-" + lens, "ROLE": role}
    # the 0202 freeze record (only FROZEN.md is opened in the 0202 folder)
    fmd = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(e["src"]))), "FROZEN.md")
    rec["frozen_md_0202"] = fmd
    r0 = None
    try:
        for r in parse_frozen(fmd):
            if r.get("lens") == lens and r.get("ROLE") == role:
                r0 = r   # last record binds
    except OSError as ex:
        reasons.append("WARNING 0202 record not readable (%s); carry file values used" % ex)
    if r0 is None and os.path.isfile(fmd):
        reasons.append("no record for %s/%s in the 0202 FROZEN.md" % (lens, role))
    rec["record_read"] = r0 is not None
    if r0 is not None:
        rec["time"] = r0["time"]
        rec["record_matches_carry_file"] = (r0["time"] == e.get("freeze_time") and
                                            r0.get("code_tree_sha256") == e.get("code_tree_sha256") and
                                            r0.get("results_tree_sha256") == e.get("results_tree_sha256_0202"))
        if not rec["record_matches_carry_file"]:
            reasons.append("0202 record differs from the carry file (time/code/results hash)")
        code_sha, code_lines = r0.get("code_tree_sha256"), [f"{h}  {p}" for h, p in r0["code_files"]]
        rec_vals = {p: h for h, p in r0["result_files"]}
    else:
        rec["time"] = e.get("freeze_time")
        rec["record_matches_carry_file"] = not os.path.isfile(fmd)   # only the fallback case passes
        code_sha, code_lines, rec_vals = e.get("code_tree_sha256"), None, None
    rec["freeze_time"] = rec["time"]
    try:
        rec["late"] = parse_epoch(rec["time"]) > parse_epoch(deadline)
    except (ValueError, KeyError, TypeError):
        rec["late"] = True
        reasons.append("unparseable freeze time")
    if rec["late"]:
        reasons.append("freeze after deadline %s" % deadline)
    # code tree re-verified
    cd = os.path.join(d, "code")
    if os.path.isdir(cd):
        lines, ch = q15h.tree(code_files(cd), cd)
        rec["code_hash_recomputed"] = ch
        rec["code_hash_ok"] = ch == code_sha == e.get("code_tree_sha256")
        rec["code_lines_match"] = (lines == code_lines) if code_lines is not None else rec["code_hash_ok"]
    else:
        rec["code_hash_ok"] = rec["code_lines_match"] = False
        reasons.append("code dir missing: %s" % cd)
    if os.path.isdir(cd) and not rec["code_hash_ok"]:
        reasons.append("code tree hash mismatch")
    if os.path.isdir(cd) and not rec["code_lines_match"]:
        reasons.append("code file lines differ from the 0202 record")
    # val-0.50 files are byte copies of the frozen ones
    bad_val = []
    for fam in q15h.FAMS:
        rel = "val/%s/%s/result-%s.tsv" % (P, fam, P)
        q = os.path.join(d, rel)
        if not os.path.isfile(q):
            bad_val.append(fam + " (missing)")
        elif rec_vals is not None and rec_vals.get(rel) != q15h.sha256(q):
            bad_val.append(fam + " (sha256 differs from the 0202 record)")
    rec["val_copies_ok"] = not bad_val
    if bad_val:
        reasons.append("val/0.50 files: %s" % ", ".join(bad_val[:3]))
    # rule 8 for carried entries: test/0.50 present (val/0.50 checked above)
    rule8(rec, d)
    # the main session's test run and audit
    ok = run_log_ok(os.path.join(d, "run_test_%s.txt" % P))
    rec["run_ok_families"] = 0 if ok is None else len(ok)
    rec["run_ok"] = ok is not None and len(ok) == len(q15h.FAMS)
    if ok is None:
        reasons.append("no run_test_%s.txt" % P)
    elif not rec["run_ok"]:
        reasons.append("run_test_%s.txt: %d of 10 families ok" % (P, len(ok)))
    check_audit(rec, [os.path.join(d, AUDIT_NAME)])
    rec["results_hash_ok"] = rec["val_copies_ok"]
    rec["n_result_files"] = len(result_files(d))
    rec["eligible"] = bool(not rec["late"] and rec["record_matches_carry_file"] and rec["code_hash_ok"]
                           and rec["code_lines_match"] and rec["val_copies_ok"] and rec["rule8_ok"]
                           and rec["run_ok"] and rec["audit_ok"])
    return rec


def main():
    ap = argparse.ArgumentParser(description="Verify FROZEN.md records and emit the stage2/score_test entries JSON")
    ap.add_argument("--attempts-root", default=os.path.join(q15h.RUN, "attempts"),
                    help="folder of <lens>/FROZEN.md (default RUN/attempts); code=/out= are relative to its parent")
    ap.add_argument("--carried", help="run 2026-10-18-0839: RUN/carry/carry_entries.json (appends the carried entries)")
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
                files.append((d, q))
    print("check_freezes: attempts-root %s ; run-root %s ; %d FROZEN.md files ; carried %s" % (
        attempts_root, run_root, len(files), a.carried or "(none)"), flush=True)
    all_records = []
    for d, q in files:
        for order, rec in enumerate(parse_frozen(q)):
            rec["deadline"] = a.deadline
            rec["order"] = (q, order)
            rec["folder_lens"] = d
            all_records.append(rec)
    # last record per (lens, ROLE) (run 2026-10-18-0839: keyed by folder too, so that a record naming another lens
    # cannot displace that lens's own record; such a record is kept separately and is ineligible)
    last = {}
    for rec in all_records:
        key = (rec["folder_lens"], rec.get("lens"), rec.get("ROLE"))
        last[key] = rec   # file order: later append overwrites
    kept = list(last.values())
    for rec in kept:
        verify(rec, run_root, attempts_root, rec["folder_lens"])
        rec["freeze_time"] = rec.get("time")
    kept.sort(key=lambda r: (r.get("time", ""), r["name"]))
    carried = []
    if a.carried:
        with open(a.carried) as f:
            for e in json.load(f):
                carried.append(verify_carried(e, a.deadline))
    eligible = [r for r in kept if r["eligible"]] + [r for r in carried if r["eligible"]]
    entries = [{"name": r["name"], "dir": os.path.abspath(r["out_dir"]), "freeze_time": r["freeze_time"]}
               for r in eligible]
    os.makedirs(os.path.dirname(os.path.abspath(a.out_json)), exist_ok=True)
    with open(a.out_json, "w") as f:
        json.dump(entries, f, indent=1)
    # markdown table
    hdr = ("| name | freeze time | eligible | code hash | results hash | result files | rule8 | "
           "audit | reasons / warnings |")
    sep = "|" + "---|" * 9
    rows = [hdr, sep]
    for r in kept + carried:
        audit = ("ends %r" % r["audit_last_line"]) if r.get("audit_file") else "MISSING"
        rows.append("| %s | %s | %s | %s | %s | %d | %s | %s | %s |" % (
            r["name"], r.get("time", "?"), "yes" if r["eligible"] else "NO",
            "ok" if r.get("code_hash_ok") and r.get("code_lines_match") else "MISMATCH",
            ("ok" if r.get("results_hash_ok") else "MISMATCH") + (" (val copies vs 0202 record)" if r.get("carried")
                                                                   else ""),
            r.get("n_result_files", 0),
            ("ok %d/%d" % (N_REQUIRED, N_REQUIRED)) if r.get("rule8_ok") else "MISSING %d" % len(r.get("rule8_missing", [])),
            audit, "; ".join(r["reasons"]) or "-"))
    md = ("# Frozen entries (run 2026-10-18-0839, P %s)\n\nattempts-root: `%s`\ncarried: `%s`\ndeadline: %s\n"
          "generated: %s\n\nEligible entries written to the entries JSON (new entries in freeze-time order, then the "
          "carried entries): %s\n\n%s\n" % (
              P, attempts_root, a.carried or "-", a.deadline, q15h.utc(),
              ", ".join(e["name"] for e in entries) or "(none)", "\n".join(rows)))
    os.makedirs(os.path.dirname(os.path.abspath(a.out_md)), exist_ok=True)
    with open(a.out_md, "w") as f:
        f.write(md)
    print(md)
    print("wrote %d eligible entries (%d new, %d carried) to %s and the table to %s" % (
        len(entries), sum(1 for r in kept if r["eligible"]), sum(1 for r in carried if r["eligible"]),
        a.out_json, a.out_md), flush=True)
    for r in kept + carried:
        print("  %-30s %s  code=%s results=%s rule8=%s audit=%s%s" % (
            r["name"], r.get("time"), "ok" if r.get("code_hash_ok") and r.get("code_lines_match") else "MISMATCH",
            "ok" if r.get("results_hash_ok") else "MISMATCH", "ok" if r.get("rule8_ok") else "MISSING",
            "PASS" if r.get("audit_ok") else ("none" if not r.get("audit_file") else "NOT PASS"),
            "" if r["eligible"] else "  -> INELIGIBLE (%s)" % "; ".join(r["reasons"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
