#!/usr/bin/env python3
"""PREREG rule 8 eligibility for run 2026-10-18-1758 (cell N40; the same entries serve every cell of this session).
Written by the tools engineer of session 2026-10-18-1758 (Opus 5.5) while the lenses were running, before any
surprise-test gold was read in this session. Standard library only; reads no gold (only FROZEN.md records, code
files, result files of predictions, audit and run logs, and the carry/newent JSON files).

Copied from tools/check_freezes.py (run 2026-10-18-0839 version). Unchanged: the FROZEN.md record parser
(parse_frozen), the file selections (code_files, result_files), the hash recomputation exactly as q15h.tree() does,
the per-file line comparison, check_audit / audit_last_line / find_audit / rule8 / verify, the lens= field vs folder
rule, the output formats (entries JSON of [{"name","dir","freeze_time"}], markdown table) and the output order (new
entries in freeze-time order, then the carried entries in the carry file's order). Changed for this run, and nothing
else:
  1. deadline 2026-10-18T21:50:00Z (PREREG rule 8 of this run; was 2026-10-18T12:40:00Z).
  2. required result files: val/0.50 and test/0.40 for all 10 surprise families (20 files; was val/0.50 + test/0.50);
     the audit file is attempts/LENS/frozen/ROLE/audit_test_0.40.txt (was audit_test_0.50.txt) and its last non-empty
     line must be exactly "AUDIT PASS" (fallback to out=/audit_test_0.40.txt of the record with a warning, as before).
  3. binding record: PREREG rule 8 says "the binding record of a role is its last record written by then". So the
     binding record of (lens folder, lens=, ROLE=) is now the LAST record in file order whose `## frozen` time is
     at or before the deadline; records written after the deadline (or with an unparseable time) are ignored and
     listed in the table as "ignored (written after the deadline)". (The 0839 copy let the last record bind even when
     it was late, which made the role ineligible.) A role whose every record is late is reported INELIGIBLE (late).
  4. --newent FILE (RUN/newent/new_entries.json): the entry dir of an eligible new entry is its newent copy (the main
     session's copy holding the same code, the val/0.50 + test/0.40 files and later the aggregate test runs at the
     other P). The copy is verified against the binding lens record: same freeze_time, code_tree_sha256 and
     results_tree_sha256 in new_entries.json as in the record; the copy's code tree recomputed (q15h.tree over
     code_files of DIR/code) equal to the record (tree hash and every per-file line); every result file listed in the
     record (val/0.50 and test/0.40) present in the copy with the record's sha256 (extra files such as test/0.10 are
     allowed: they are the aggregate runs); DIR/audit_test_0.40.txt ends "AUDIT PASS". If the copy verifies, the
     entries JSON gets dir = the newent copy. If an eligible entry has no newent copy, or its copy fails a check, the
     entry stays eligible under rule 8 (eligibility is a property of the lens freeze), the JSON gets dir = the lens's
     attempts ROLE folder, the table says why, and the program exits with status 3 so that the main session notices
     (it must make or repair the copy and rerun). Newent copies with no eligible binding record are listed and not
     used. Without --newent the dir is the attempts ROLE folder, as before.
  5. --carried FILE (RUN/carry/carry_entries.json; this run's format: name "r0839-LENS/ROLE" or "r0202-LENS/ROLE",
     src_frozen, dir, freeze_time, code_tree_sha256): the 21 carried entries of runs 2026-10-18-0202 and -0839. For
     each one the source run's freeze record is read from src_frozen (the last record of that lens and ROLE binds, as
     before; only that FROZEN.md is opened in the source run) and the entry is eligible only if: the record's time and
     code_tree_sha256 equal the carry file's freeze_time and code_tree_sha256 (this carry file holds no results tree
     hash, so that comparison of the 0839 copy is dropped); the code tree of DIR/code recomputed equals the record and
     the carry file (tree hash and every per-file line); every DIR/val/0.50/FAM/result-0.50.tsv has the sha256 the
     record lists (byte copies of the frozen val files); DIR/test/0.40 holds all 10 result files; run_test_0.40.txt
     shows all 10 families "ok"; DIR/audit_test_0.40.txt ends "AUDIT PASS"; freeze time at or before the deadline.
     The entry name is the carry file's name as given (it already carries its r0202-/r0839- prefix).
  6. titles and messages name run 2026-10-18-1758 and P 0.40; docstrings and comments avoid angle brackets.

For every ATTEMPTS_ROOT/LENS/FROZEN.md it reads each freeze record (a block headed `## frozen UTC` with lines ROLE=,
lens=, code=, out=, code_tree_sha256=, results_tree_sha256=, then a `### code files` list and a `### result files`
list of "SHA256  RELPATH" lines, exactly as tools/q15h.py freeze writes them), picks the binding record per role
(change 3) and verifies it: freeze time, code and results tree hashes recomputed against the record (code files: every
file under code/ that is not a .pyc and not under __pycache__; result files: every file under the ROLE folder named
result-*.tsv not under a parts/ directory), the rule-8 result files, and the audit file. The code=/out= paths of a
record are relative to the run root (the parent of the attempts root).

usage: python3 -I tools/check_freezes_040.py [--attempts-root DIR] [--newent RUN/newent/new_entries.json]
           [--carried RUN/carry/carry_entries.json] [--out-json FILE] [--out-md FILE] [--deadline UTC]
exit status: 0 = done; 3 = done, but an eligible new entry has no verified newent copy (see change 4).
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

DEADLINE = "2026-10-18T21:50:00Z"   # run 2026-10-18-1758 (was 2026-10-18T12:40:00Z)
VALP, TESTP = "0.50", "0.40"
P = TESTP                            # the test proportion of the audit and run logs
REQUIRED = [("val", VALP), ("test", TESTP)]   # run 1758: 20 files (was val 0.50 + test 0.50)
N_REQUIRED = len(REQUIRED) * len(q15h.FAMS)
AUDIT_NAME = "audit_test_%s.txt" % TESTP


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
    # audit file (run 2026-10-18-0839: required, at attempts/LENS/frozen/ROLE/AUDIT_NAME; run 1758: AUDIT_NAME = audit_test_0.40.txt)
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
    """run 2026-10-18-0839: families whose line in a saved `q15h.py run --mode test` output says ok (run 1758: P 0.40)."""
    ok = set()
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8", errors="replace") as fh:
        for ln in fh:
            t = ln.split()
            # "UTC test 0.40 FAM ok N rows Ss"
            if len(t) >= 5 and t[1] == "test" and t[2] == P and t[3] in q15h.FAMS and t[4] == "ok":
                ok.add(t[3])
    return ok


def verify_newent(rec, ne):
    """run 1758 (change 4): verify a newent copy `ne` (an item of new_entries.json) against the binding record."""
    probs = []
    d = os.path.abspath(ne["dir"])
    if ne.get("freeze_time") != rec.get("time"):
        probs.append("freeze_time %r differs from the record %r" % (ne.get("freeze_time"), rec.get("time")))
    if ne.get("code_tree_sha256") != rec.get("code_tree_sha256"):
        probs.append("new_entries.json code_tree_sha256 differs from the record")
    if ne.get("results_tree_sha256") != rec.get("results_tree_sha256"):
        probs.append("new_entries.json results_tree_sha256 differs from the record")
    cd = os.path.join(d, "code")
    if os.path.isdir(cd):
        lines, ch = q15h.tree(code_files(cd), cd)
        if ch != rec.get("code_tree_sha256"):
            probs.append("copy code tree hash mismatch")
        if lines != [f"{h}  {p}" for h, p in rec["code_files"]]:
            probs.append("copy code file lines differ from the record")
    else:
        probs.append("copy code dir missing")
    bad = []
    for h, rel in rec["result_files"]:
        q = os.path.join(d, rel)
        if not os.path.isfile(q):
            bad.append(rel + " (missing)")
        elif q15h.sha256(q) != h:
            bad.append(rel + " (sha256 differs)")
    if bad:
        probs.append("copy result files: %d bad (e.g. %s)" % (len(bad), ", ".join(bad[:2])))
    ok, last = audit_last_line(os.path.join(d, AUDIT_NAME))
    if not ok:
        probs.append("copy has no %s" % AUDIT_NAME)
    elif last != "AUDIT PASS":
        probs.append("copy %s does not end 'AUDIT PASS'" % AUDIT_NAME)
    return d, probs


def verify_carried(e, deadline):
    """run 2026-10-18-0839, adapted for run 1758 (change 5): one carried entry (see the docstring)."""
    reasons = []
    name = e["name"]
    pref, rest = name.split("-", 1)
    lens, role = rest.split("/")
    d = os.path.abspath(e["dir"])
    rec = {"name": name, "dir": d, "out_dir": d, "carried": True, "reasons": reasons,
           "lens": pref + "-" + lens, "ROLE": role}
    # the source run's freeze record (only FROZEN.md is opened in the source run)
    fmd = os.path.abspath(e["src_frozen"])
    rec["frozen_md_src"] = fmd
    r0 = None
    try:
        for r in parse_frozen(fmd):
            if r.get("lens") == lens and r.get("ROLE") == role:
                r0 = r   # last record binds
    except OSError as ex:
        reasons.append("WARNING source record not readable (%s); carry file values used" % ex)
    if r0 is None and os.path.isfile(fmd):
        reasons.append("no record for %s/%s in %s" % (lens, role, fmd))
    rec["record_read"] = r0 is not None
    if r0 is not None:
        rec["time"] = r0["time"]
        rec["record_matches_carry_file"] = (r0["time"] == e.get("freeze_time") and
                                            r0.get("code_tree_sha256") == e.get("code_tree_sha256"))
        if not rec["record_matches_carry_file"]:
            reasons.append("source record differs from the carry file (time/code hash)")
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
        reasons.append("code file lines differ from the source record")
    # val-0.50 files are byte copies of the frozen ones
    bad_val = []
    for fam in q15h.FAMS:
        rel = "val/%s/%s/result-%s.tsv" % (VALP, fam, VALP)
        q = os.path.join(d, rel)
        if not os.path.isfile(q):
            bad_val.append(fam + " (missing)")
        elif rec_vals is not None and rec_vals.get(rel) != q15h.sha256(q):
            bad_val.append(fam + " (sha256 differs from the source record)")
    rec["val_copies_ok"] = not bad_val
    if bad_val:
        reasons.append("val/0.50 files: %s" % ", ".join(bad_val[:3]))
    # rule 8 for carried entries: val/0.50 and test/0.40 present
    rule8(rec, d)
    # the main session's test run and audit at 0.40
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


def in_time(rec, deadline):
    try:
        return parse_epoch(rec["time"]) <= parse_epoch(deadline)
    except (ValueError, KeyError):
        return False


def main():
    ap = argparse.ArgumentParser(description="PREREG rule 8 (run 2026-10-18-1758): verify FROZEN.md records, newent "
                                             "copies and carried entries; emit the entries JSON")
    ap.add_argument("--attempts-root", default=os.path.join(q15h.RUN, "attempts"),
                    help="folder of LENS/FROZEN.md (default RUN/attempts); code=/out= are relative to its parent")
    ap.add_argument("--newent", help="run 1758: RUN/newent/new_entries.json (entry dirs of new entries)")
    ap.add_argument("--carried", help="RUN/carry/carry_entries.json (appends the carried entries)")
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
    print("check_freezes_040: attempts-root %s ; run-root %s ; %d FROZEN.md files ; newent %s ; carried %s" % (
        attempts_root, run_root, len(files), a.newent or "(none)", a.carried or "(none)"), flush=True)
    all_records = []
    for d, q in files:
        for order, rec in enumerate(parse_frozen(q)):
            rec["deadline"] = a.deadline
            rec["order"] = (q, order)
            rec["folder_lens"] = d
            all_records.append(rec)
    # run 1758 (change 3): binding record per (folder, lens, ROLE) = the last record written by the deadline
    last, ignored, seen = {}, [], {}
    for rec in all_records:
        key = (rec["folder_lens"], rec.get("lens"), rec.get("ROLE"))
        seen.setdefault(key, []).append(rec)
        if in_time(rec, a.deadline):
            last[key] = rec   # file order: later append (written by the deadline) overwrites
        else:
            ignored.append(rec)
    kept = list(last.values())
    for key, recs in seen.items():
        if key not in last:   # every record of this role is late: report the last one as INELIGIBLE (late)
            kept.append(recs[-1])
            ignored.remove(recs[-1])
    for rec in kept:
        verify(rec, run_root, attempts_root, rec["folder_lens"])
        rec["freeze_time"] = rec.get("time")
    kept.sort(key=lambda r: (r.get("time", ""), r["name"]))
    # run 1758 (change 4): newent copies as entry dirs
    newent = {}
    if a.newent:
        with open(a.newent) as f:
            for ne in json.load(f):
                newent[ne["name"]] = ne
    missing_copy = 0
    used_copies = set()
    for rec in kept:
        rec["entry_dir"] = os.path.abspath(rec["out_dir"])
        rec["newent_status"] = "-"
        if not a.newent:
            continue
        ne = newent.get(rec["name"])
        if not rec["eligible"]:
            rec["newent_status"] = "not used (record ineligible)" if ne else "-"
            continue
        if ne is None:
            rec["newent_status"] = "NO COPY"
            rec["reasons"].append("WARNING no newent copy: entry dir = attempts folder")
            missing_copy += 1
            continue
        used_copies.add(rec["name"])
        d, probs = verify_newent(rec, ne)
        if probs:
            rec["newent_status"] = "COPY MISMATCH"
            rec["reasons"].append("WARNING newent copy %s fails: %s; entry dir = attempts folder" % (d, "; ".join(probs)))
            missing_copy += 1
        else:
            rec["newent_status"] = "verified"
            rec["entry_dir"] = d
    orphan = [n for n in newent if n not in used_copies and not any(r["name"] == n for r in kept)]
    carried = []
    if a.carried:
        with open(a.carried) as f:
            for e in json.load(f):
                r = verify_carried(e, a.deadline)
                r["entry_dir"] = r["dir"]
                r["newent_status"] = "-"
                carried.append(r)
    eligible = [r for r in kept if r["eligible"]] + [r for r in carried if r["eligible"]]
    entries = [{"name": r["name"], "dir": r["entry_dir"], "freeze_time": r["freeze_time"]} for r in eligible]
    os.makedirs(os.path.dirname(os.path.abspath(a.out_json)), exist_ok=True)
    with open(a.out_json, "w") as f:
        json.dump(entries, f, indent=1)
    # markdown table
    hdr = ("| name | freeze time | eligible | code hash | results hash | result files | rule8 | "
           "audit | newent copy | entry dir | reasons / warnings |")
    sep = "|" + "---|" * 11
    rows = [hdr, sep]
    for r in kept + carried:
        audit = ("ends %r" % r["audit_last_line"]) if r.get("audit_file") else "MISSING"
        rows.append("| %s | %s | %s | %s | %s | %d | %s | %s | %s | %s | %s |" % (
            r["name"], r.get("time", "?"), "yes" if r["eligible"] else "NO",
            "ok" if r.get("code_hash_ok") and r.get("code_lines_match") else "MISMATCH",
            ("ok" if r.get("results_hash_ok") else "MISMATCH") + (" (val copies vs source record)" if r.get("carried")
                                                                   else ""),
            r.get("n_result_files", 0),
            ("ok %d/%d" % (N_REQUIRED, N_REQUIRED)) if r.get("rule8_ok") else "MISSING %d" % len(r.get("rule8_missing", [])),
            audit, r["newent_status"], r["entry_dir"], "; ".join(r["reasons"]) or "-"))
    extra = []
    for r in ignored:
        extra.append("- ignored (written after the deadline or unparseable time): %s/%s record of %s in %s" % (
            r.get("lens"), r.get("ROLE"), r.get("time"), r["order"][0]))
    for n in orphan:
        extra.append("- newent copy %s has no binding lens record: not used" % n)
    md = ("# Frozen entries (run 2026-10-18-1758, rule 8: val %s + test %s)\n\nattempts-root: `%s`\nnewent: `%s`\n"
          "carried: `%s`\ndeadline: %s\ngenerated: %s\n\nEligible entries written to the entries JSON (new entries in "
          "freeze-time order, then the carried entries): %s\n\n%s\n%s\n" % (
              VALP, TESTP, attempts_root, a.newent or "-", a.carried or "-", a.deadline, q15h.utc(),
              ", ".join(e["name"] for e in entries) or "(none)", "\n".join(rows),
              ("\n" + "\n".join(extra) + "\n") if extra else ""))
    os.makedirs(os.path.dirname(os.path.abspath(a.out_md)), exist_ok=True)
    with open(a.out_md, "w") as f:
        f.write(md)
    print(md)
    print("wrote %d eligible entries (%d new, %d carried) to %s and the table to %s" % (
        len(entries), sum(1 for r in kept if r["eligible"]), sum(1 for r in carried if r["eligible"]),
        a.out_json, a.out_md), flush=True)
    for r in kept + carried:
        print("  %-32s %s  code=%s results=%s rule8=%s audit=%s newent=%s%s" % (
            r["name"], r.get("time"), "ok" if r.get("code_hash_ok") and r.get("code_lines_match") else "MISMATCH",
            "ok" if r.get("results_hash_ok") else "MISMATCH", "ok" if r.get("rule8_ok") else "MISSING",
            "PASS" if r.get("audit_ok") else ("none" if not r.get("audit_file") else "NOT PASS"),
            r["newent_status"], "" if r["eligible"] else "  -> INELIGIBLE (%s)" % "; ".join(r["reasons"])))
    if missing_copy:
        print("EXIT 3: %d eligible new entr%s without a verified newent copy (dir = attempts folder)" % (
            missing_copy, "y" if missing_copy == 1 else "ies"), flush=True)
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
