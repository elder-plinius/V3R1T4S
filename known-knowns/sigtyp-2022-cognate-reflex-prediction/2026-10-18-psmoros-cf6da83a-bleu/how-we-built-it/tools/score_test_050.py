#!/usr/bin/env python3
"""PREREG rule 11 test scoring, run 2026-10-18-0839 (cells N50, B50, L50 at proportion 0.50): an adapted copy of
tools/score_test.py (run 2026-10-18-0104's copy of run 2026-10-17-1806's tool), made by the tools engineer of run
2026-10-18-0839 (Opus 5.5) while the lenses were running. NEVER run by the tools engineer for real (it reads
surprise-test gold): the main session runs it only after selection.md exists. Changes, and nothing else:
  - (a) is unchanged: Mockingbird-I1's official totals (and every family value) are reproduced at ALL FIVE
    proportions bit for bit with left-to-right summation; if any ltr total differs, nothing is scored (kill
    criterion 1);
  - (b) is unchanged: FeVeT's published predictions are rescored at 0.10, 0.30 and 0.50;
  - (c) entries (every eligible entry, COMB-6 and COMB-8, from --entries) are scored at 0.50 ONLY; an entry without
    a test/0.50 folder gets one "skipped" line (as before), a missing family file inside it is an error;
  - the claim walk (PREREG rule 12 (i)) is per cell, for every entry, in both summation modes:
      N50: mean NED lower than FeVeT's recomputed 0.50 mean NED by more than 1e-9;
      B50: mean BCFS higher than FeVeT's recomputed 0.50 mean BCFS by more than 1e-9;
      L50: mean BLEU higher than FeVeT's recomputed 0.50 mean BLEU by more than 1e-9;
    it also prints, for information, the margin over Mockingbird-I1 (ltr: the official total; builtin: the
    recomputed total) on the same metric (the criterion's comparison) and whether the recomputed FeVeT value
    equals the PREREG table value. The AGG walk is dropped (not claimed in this run). --candidate NAME marks the
    rule 10 candidate's lines;
  - imports of the scorer happen only in real mode; --dry-run lists every file the real run would read (stat only:
    existence and size; no solutions file, FeVeT file or result file is opened) and exits;
  - --clone DIR, --calib-props, --fevet-props (defaults: the pinned clone, all five P, 0.10/0.30/0.50 as PREREG rule 11
    requires) let a claim package's reader rerun it on the package's official/ and fevet/ folders, which hold 0.50
    only (--clone official --fevet-dir fevet --calib-props 0.50 --fevet-props 0.50). The main session uses the
    defaults.
Original description:

(a) Reproduces Mockingbird-I1's official totals (and every family value) at all five proportions bit for bit with
    left-to-right summation; if any total differs, nothing is scored (charter kill criterion 1).
(b) Rescores FeVeT's published per-item predictions (Wientzek 2025; files fetched 2026-10-16 from
    github.com/TGH-2020/FeVeT at 31898c53, copies in resume/data/fevet) at 0.10, 0.30, 0.50.
(c) Scores every eligible entry of selection.md.
Every value is computed in both summation modes: 'ltr' (left-to-right sum shadowing the builtin in sigtypst2022 and
lingrex.util, as Python < 3.12 did in 2022) and 'builtin' (Python 3.13 compensated sum). The scorer is the pinned
repository's own compare_words; the family total is statistics.mean over the 10 families, as compare_systems does.

usage: STUB_MPL=1 <calibrator venv python> -I tools/score_test_050.py --entries E.json --json OUT.json
           [--fevet-dir DIR] [--candidate NAME]
       python3 -I tools/score_test_050.py --entries E.json --json OUT.json --dry-run
"""
import argparse
import builtins
import contextlib
import csv
import io
import json
import os
import statistics
import sys
import tempfile
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
st = None   # sigtypst2022, imported in real mode only (run 2026-10-18-0839)
lingrex_util = None

RUN = os.path.dirname(HERE)
CLONE = "WORKDIR/scratch_q15/ST2022"
PROPS = ["0.10", "0.20", "0.30", "0.40", "0.50"]
FAMS = ["bantubvd", "beidazihui", "birchallchapacuran", "bodtkhobwa", "bremerberta", "deepadungpalaung",
        "hillburmish", "kesslersignificance", "luangthongkumkaren", "wangbai"]
FEVET_PROPS = ["0.10", "0.30", "0.50"]
FEVET_DIR_DEFAULT = "WORKDIR/runs/2026-10-17-1806/resume/data/fevet"
P = "0.50"   # run 2026-10-18-0839: entries are scored at this proportion only
# run 2026-10-18-0839: the three cells (index into [ED, NED, BCFS, BLEU], direction, PREREG table bar values)
CELLS = [("N50", "NED", 1, "lower", "0.30880111347517586", "0.35176136367373956"),
         ("B50", "BCFS", 2, "higher", "0.6423935720824072", "0.6050308536957327"),
         ("L50", "BLEU", 3, "higher", "0.5768215755932388", "0.5337187296541888")]


def naive_sum(iterable, start=0):
    acc = start
    for x in iterable:
        acc = acc + x
    return acc


def set_mode(mode):
    f = naive_sum if mode == "ltr" else builtins.sum
    st.sum = f
    lingrex_util.sum = f


def gold(p, fam):
    return os.path.join(CLONE, "data-surprise", fam, "solutions-%s.tsv" % p)


def score_dir(p, resdir_of):
    fam_scores = {}
    for fam in FAMS:
        with contextlib.redirect_stdout(io.StringIO()):
            fam_scores[fam] = list(st.compare_words(gold(p, fam), resdir_of(fam), report=False)[-1][1:])
    tot = [statistics.mean([fam_scores[f][i] for f in FAMS]) for i in range(4)]
    return fam_scores, tot


def fevet_files(p, tmp, fevet_dir):
    paths = {}
    checks = {}
    for fam in FAMS:
        with contextlib.redirect_stdout(io.StringIO()):
            langs, _, g = st.load_cognate_file(gold(p, fam))
        pred = defaultdict(dict)
        n = mism = 0
        with open(os.path.join(fevet_dir, "pred_%s_%s.tsv" % (p, fam)), encoding="utf-8") as fh:
            for row in csv.DictReader(fh, delimiter="\t"):
                n += 1
                pred[row["COGID"]][row["LANGUAGE"]] = row["PREDICTION"].split()
                gg = g.get(row["COGID"], {}).get(row["LANGUAGE"])
                if gg is None or gg != row["GOLD"].split():
                    mism += 1
        missing = sum(1 for k in g for lg in langs if g[k].get(lg) and lg not in pred.get(k, {}))
        out = os.path.join(tmp, "fevet", p, fam, "result-%s.tsv" % p)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as fh:
            fh.write("COGID\t" + "\t".join(langs) + "\n")
            for k in g:
                fh.write(k + "".join("\t" + " ".join(pred.get(k, {}).get(lg, [])) for lg in langs) + "\n")
        paths[fam] = out
        checks[fam] = {"rows": n, "missing": missing, "gold_column_mismatches": mism}
    return paths, checks


def dry_run(entries, fevet_dir, out_json):
    """run 2026-10-18-0839: list every input of the real run with os.path.getsize (stat only, nothing opened)."""
    plan = []
    for p in CALIB_PROPS:
        plan.append(("official results JSON", os.path.join(CLONE, "results", "results-surprise-%s.json" % p), "gold"))
        for fam in FAMS:
            plan.append(("Mockingbird-I1 predictions",
                         os.path.join(CLONE, "systems", "mockingbird-i1", "surprise", fam, "result-%s.tsv" % p), ""))
            plan.append(("surprise solutions", gold(p, fam), "gold"))
    for p in FEVET_PROPS:
        for fam in FAMS:
            plan.append(("FeVeT published predictions (has a GOLD column)",
                         os.path.join(fevet_dir, "pred_%s_%s.tsv" % (p, fam)), "gold"))
    for name, d in entries:
        if not os.path.isdir(os.path.join(d, "test", P)):
            plan.append(("entry %s (would be skipped: no test/%s folder)" % (name, P), os.path.join(d, "test", P), ""))
            continue
        for fam in FAMS:
            plan.append(("entry %s" % name, os.path.join(d, "test", P, fam, "result-%s.tsv" % P), ""))
    n_ok = n_miss = n_gold = 0
    print("DRY-RUN score_test_050: nothing is opened; one stat() per file. clone %s ; fevet %s" % (CLONE, fevet_dir))
    for what, q, g in plan:
        ok = os.path.isfile(q)
        n_ok += ok
        n_miss += not ok
        n_gold += bool(ok and g)
        print("%-8s %10s  %s  [%s]" % (("GOLD" if g else "ok") if ok else "MISSING",
                                      os.path.getsize(q) if ok else "-", q, what))
    print("dry-run: %d files present (%d gold-bearing, stat only), %d missing; would write %s" % (
        n_ok, n_gold, n_miss, out_json))
    print("DRY_RUN %s" % ("ALL_PRESENT" if n_miss == 0 else "MISSING %d" % n_miss))
    return 0 if n_miss == 0 else 2


CALIB_PROPS = PROPS


def main():
    global st, lingrex_util, CLONE, CALIB_PROPS, FEVET_PROPS
    ap = argparse.ArgumentParser(description="PREREG rule 11 test scoring at 0.50 (reads surprise-test gold; main "
                                             "session only, after selection.md exists)")
    ap.add_argument("--json", required=True)
    ap.add_argument("--entries", required=True, help="JSON list of {name, dir}; dir holds test/0.50/<fam>/result-0.50.tsv")
    ap.add_argument("--fevet-dir", default=FEVET_DIR_DEFAULT, help="folder with pred_<P>_<fam>.tsv (FeVeT published)")
    ap.add_argument("--candidate", help="name of the rule 10 candidate (its claim-walk lines are marked)")
    ap.add_argument("--dry-run", action="store_true", help="list the inputs (stat only) and exit; opens nothing")
    ap.add_argument("--clone", default=CLONE, help="pinned clone (or a claim package's official/ folder)")
    ap.add_argument("--calib-props", default=",".join(PROPS), help="Mockingbird-I1 calibration proportions "
                                                                 "(PREREG rule 11 (a): all five)")
    ap.add_argument("--fevet-props", default=",".join(FEVET_PROPS), help="FeVeT rescoring proportions (must include 0.50)")
    a = ap.parse_args()
    CLONE = os.path.abspath(a.clone)
    CALIB_PROPS = a.calib_props.split(",")
    FEVET_PROPS = a.fevet_props.split(",")
    if P not in CALIB_PROPS or P not in FEVET_PROPS:
        raise SystemExit("--calib-props and --fevet-props must include %s" % P)
    if CALIB_PROPS != PROPS:
        print("NOTE: Mockingbird-I1 calibration at %s only (PREREG rule 11 (a) needs all five P for the main "
              "session's scoring)" % ",".join(CALIB_PROPS))
    with open(a.entries) as f:
        ENTRIES = [(e["name"], os.path.abspath(e["dir"])) for e in json.load(f)]
    if a.candidate and a.candidate not in [e for e, _ in ENTRIES]:
        raise SystemExit("--candidate %s is not in --entries" % a.candidate)
    if a.dry_run:
        return dry_run(ENTRIES, a.fevet_dir, a.json)
    import mplstub  # noqa: F401
    with contextlib.redirect_stdout(io.StringIO()):
        import sigtypst2022 as _st
    import lingrex.util as _lu
    st, lingrex_util = _st, _lu
    res = {"ltr": {}, "builtin": {}}
    with tempfile.TemporaryDirectory() as tmp:
        for mode in ("ltr", "builtin"):
            set_mode(mode)
            R = res[mode]
            # (a) calibration on Mockingbird-I1
            bad = 0
            for p in CALIB_PROPS:
                off = json.load(open(os.path.join(CLONE, "results", "results-surprise-%s.json" % p)))["Mockingbird-I1"]
                fs, tot = score_dir(p, lambda fam: os.path.join(CLONE, "systems", "mockingbird-i1", "surprise", fam,
                                                                 "result-%s.tsv" % p))
                exact_tot = tot == off["total"]
                exact_fam = all(fs[f] == off[f] for f in FAMS)
                R.setdefault(p, {})["Mockingbird-I1"] = {"total": tot, "families": fs, "official_total": off["total"],
                                                         "total_bit_identical": exact_tot,
                                                         "families_bit_identical": exact_fam}
                print("%s %s Mockingbird-I1 NED %r official %r total %s families %s" % (
                    mode, p, tot[1], off["total"][1], "EXACT" if exact_tot else "DIFF", "EXACT" if exact_fam else "DIFF"),
                    flush=True)
                bad += not exact_tot
            if mode == "ltr" and bad:
                print("CALIBRATION FAILED in ltr mode: nothing is scored (kill criterion 1)")
                with open(a.json, "w") as f:
                    json.dump(res, f, indent=1)
                return 1
            # (b) FeVeT published predictions
            for p in FEVET_PROPS:
                paths, checks = fevet_files(p, os.path.join(tmp, mode), a.fevet_dir)
                fs, tot = score_dir(p, lambda fam: paths[fam])
                R[p]["FeVeT-published"] = {"total": tot, "families": fs, "checks": checks}
                print("%s %s FeVeT NED %r BCFS %r BLEU %r (checks: missing %d, gold mismatches %d)" % (
                    mode, p, tot[1], tot[2], tot[3], sum(c["missing"] for c in checks.values()),
                    sum(c["gold_column_mismatches"] for c in checks.values())), flush=True)
            # (c) eligible entries, COMB-6, COMB-8: P 0.50 only (run 2026-10-18-0839)
            for e, edir in ENTRIES:
                if not os.path.isdir(os.path.join(edir, "test", P)):
                    print("%s %s %-30s skipped (no test/%s folder)" % (mode, P, e, P), flush=True)
                    continue
                fs, tot = score_dir(P, lambda fam: os.path.join(edir, "test", P, fam, "result-%s.tsv" % P))
                R[P][e] = {"total": tot, "families": fs}
                print("%s %s %-30s ED %.6f NED %r BCFS %r BLEU %r" % (mode, P, e, tot[0], tot[1], tot[2], tot[3]),
                      flush=True)
    # claim walk, rule 12 (i) only ((ii)-(iv) are checked separately); run 2026-10-18-0839: cells N50, B50, L50
    print()
    walk = {}
    for cell, metric, idx, direction, prereg_bar, prereg_mb in CELLS:
        fv = {m: res[m][P]["FeVeT-published"]["total"][idx] for m in ("ltr", "builtin")}
        mb = {"ltr": res["ltr"][P]["Mockingbird-I1"]["official_total"][idx],
              "builtin": res["builtin"][P]["Mockingbird-I1"]["total"][idx]}
        print("%s (mean %s, %s is better): bar FeVeT recomputed ltr %r builtin %r (PREREG table %s: %s); "
              "Mockingbird-I1 official %r (PREREG table %s)" % (
                  cell, metric, direction, fv["ltr"], fv["builtin"], prereg_bar,
                  "EQUAL" if repr(fv["ltr"]) == prereg_bar else "DIFFERENT (the recomputed value binds)",
                  mb["ltr"], prereg_mb))
        walk[cell] = {"metric": metric, "direction": direction, "bar_fevet": fv, "mockingbird": mb,
                      "prereg_bar": prereg_bar, "entries": {}}
        for e, _ in ENTRIES:
            if e not in res["ltr"].get(P, {}):
                continue
            line, meets_all = [], True
            ent = {}
            for mode in ("ltr", "builtin"):
                c = res[mode][P][e]["total"][idx]
                margin = (fv[mode] - c) if direction == "lower" else (c - fv[mode])
                mmb = (mb[mode] - c) if direction == "lower" else (c - mb[mode])
                meets = margin > 1e-9
                meets_all &= meets
                ent[mode] = {"value": c, "margin_vs_fevet": margin, "meets_i": meets, "margin_vs_mockingbird": mmb}
                line.append("%s: %s %r bar %r margin %.12f -> %s; vs Mockingbird-I1 %.12f" % (
                    mode, metric, c, fv[mode], margin, "MEETS (i)" if meets else "fails (i)", mmb))
            ent["meets_i_both_modes"] = meets_all
            walk[cell]["entries"][e] = ent
            print("%s%s %s | %s | both modes: %s" % ("CANDIDATE " if e == a.candidate else "", cell, e,
                                                      " | ".join(line), "MEETS (i)" if meets_all else "fails (i)"))
        print()
    res["claim_walk_050"] = walk
    with open(a.json, "w") as f:
        json.dump(res, f, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
