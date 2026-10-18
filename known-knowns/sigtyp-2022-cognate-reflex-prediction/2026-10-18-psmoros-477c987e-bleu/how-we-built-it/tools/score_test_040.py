#!/usr/bin/env python3
"""PREREG rule 11 test scoring, run 2026-10-18-1758 (cells N40, B40, L40 at proportion 0.40 and the aggregate cells
NA, BA, LA over all five proportions): an adapted copy of tools/score_test_050.py (run 2026-10-18-0839's tool), made
by the tools engineer of run 2026-10-18-1758 (Opus 5.5) while the lenses were running. NEVER run by the tools engineer
in its scoring mode (it reads surprise-test gold): the main session runs it only after selection.md exists. The tools
engineer ran only --dry-run and --val-check (validation gold). Changes against tools/score_test_050.py, and nothing
else:
  - (a) is unchanged: Mockingbird-I1's official totals (and every family value) are reproduced at ALL FIVE
    proportions bit for bit with left-to-right summation; if any ltr total differs, nothing is scored (kill
    criterion 1). (score_dir, naive_sum, set_mode and the calibration loop are byte-for-byte the old code; gold()
    gained only the --val-check branch below.)
  - FeVeT rescoring (old (b)) is dropped: PREREG rule 11 of this run does not use FeVeT (every bar is Mockingbird-I1);
    --fevet-dir and --fevet-props are gone.
  - (b) entries: every entry of --entries (JSON list of {name, dir}) and every COMB folder of --combs (same format;
    optional; COMB folders may also simply be listed in --entries) are scored at 0.40 ONLY
    (dir/test/0.40/FAM/result-0.40.tsv); an entry without a test/0.40 folder gets one "skipped" line (as before), a
    missing family file inside an existing test/0.40 folder is an error (now checked before the scorer is imported).
  - (c) NEW: --candidate-dir DIR (layout DIR/test/P/FAM/result-P.tsv for all five P; all 50 files required, checked
    before the scorer is imported) is scored at every P; A_m = (S_m(0.10)+S_m(0.20)+S_m(0.30)+S_m(0.40)+S_m(0.50))/5
    is computed (i) left to right (naive_sum in the order 0.10 ... 0.50) over the ltr-mode totals and (ii) with the
    builtin sum over the builtin-mode totals; the two cross combinations are recorded for information.
    Mockingbird-I1's A_m is computed the same way from its official results-surprise-P.json totals (ltr) and from its
    recomputed builtin-mode totals (builtin). --candidate NAME is now only the candidate's label (default CANDIDATE);
    if NAME is also an entry of --entries/--combs, its 0.40 totals there are compared with the candidate-dir's 0.40
    totals (EQUAL/DIFFERENT, information).
  - (d) claim walk, PREREG rule 12 (i) only ((ii)-(iv) are checked separately), six cells, bars fixed in CELLS_P and
    CELLS_A (the PREREG rule 2 table): N40, B40, L40 (Mockingbird-I1 at 0.40) for every scored entry, COMB and the
    candidate's 0.40 output; NA, BA, LA (Mockingbird-I1 aggregates) for the candidate only. A value meets (i) iff its
    margin over the bar (bar minus value for NED; value minus bar for BCFS, BLEU) is > 1e-9 in BOTH summation modes
    (ltr value and builtin value, each against the PREREG bar). Before the walk the bars are asserted: the official
    0.40 totals and the ltr aggregates from the official totals must equal the PREREG bar strings (repr); if any
    differs, the walk is not run and the exit status is 1. For information each line also gives the margin against
    Mockingbird-I1's recomputed builtin-mode value. The 0.50 cells (N50, B50, L50) are dropped.
  - (e) --dry-run lists every file the real run would read (stat only: existence and size; no solutions file, results
    JSON or result file is opened) and exits; it now also lists --combs and the candidate's 50 files.
  - NEW --val-check (validation gold only, never test gold): scores the val/0.50 files of the first two entries of
    --entries against --val-root/0.50/FAM/solutions.tsv (default RUN/shared/val) through the same score_dir() in
    both summation modes, runs tools/val_scorer.py (the command q15h.py score-val runs) on the same two entries with
    --gold-root --val-root, and requires the builtin-mode family values and totals to be bit-identical
    (VALCHECK ... EXACT); it also exercises agg() and the walk code on validation numbers (five copies of entry 1's
    val totals against entry 2's; the printed outcomes have no claim meaning).
  - CLONE default line kept in the old form so claim builders can patch it; --clone and --calib-props kept.
Original description (of score_test.py):

(a) Reproduces Mockingbird-I1's official totals (and every family value) at all five proportions bit for bit with
    left-to-right summation; if any total differs, nothing is scored (charter kill criterion 1).
(c) Scores every eligible entry of selection.md.
Every value is computed in both summation modes: 'ltr' (left-to-right sum shadowing the builtin in sigtypst2022 and
lingrex.util, as Python < 3.12 did in 2022) and 'builtin' (Python 3.13 compensated sum). The scorer is the pinned
repository's own compare_words; the family total is statistics.mean over the 10 families, as compare_systems does.

usage (main session, after selection.md exists; reads surprise-test gold):
  STUB_MPL=1 WORKDIR/runs/2026-10-16-2026/attempts/calibrator/venv/bin/python -I \\
      tools/score_test_040.py --entries E.json [--combs C.json] --candidate-dir DIR [--candidate NAME] --json OUT.json
  python3 -I tools/score_test_040.py --entries E.json [--combs C.json] [--candidate-dir DIR] --json OUT.json --dry-run
  STUB_MPL=1 (same python) -I tools/score_test_040.py --entries E.json --json VAL.json --val-check [--val-root DIR]
"""
import argparse
import builtins
import contextlib
import io
import json
import os
import statistics
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
st = None   # sigtypst2022, imported in real mode only (run 2026-10-18-0839)
lingrex_util = None

RUN = os.path.dirname(HERE)
CLONE = "WORKDIR/scratch_q15/ST2022"
PROPS = ["0.10", "0.20", "0.30", "0.40", "0.50"]
FAMS = ["bantubvd", "beidazihui", "birchallchapacuran", "bodtkhobwa", "bremerberta", "deepadungpalaung",
        "hillburmish", "kesslersignificance", "luangthongkumkaren", "wangbai"]
P = "0.40"   # run 2026-10-18-1758: entries and COMBs are scored at this proportion only
# run 2026-10-18-1758: cells (name, metric, index into [ED, NED, BCFS, BLEU], direction, PREREG rule 2 bar)
CELLS_P = [("N40", "NED", 1, "lower", "0.316240240534308"),
           ("B40", "BCFS", 2, "higher", "0.6428278176401176"),
           ("L40", "BLEU", 3, "higher", "0.5723601982335171")]
CELLS_A = [("NA", "NED", 1, "lower", "0.2931673956342817"),
           ("BA", "BCFS", 2, "higher", "0.6797616040522236"),
           ("LA", "BLEU", 3, "higher", "0.6015772270938825")]
MARGIN = 1e-9
VAL_ROOT_DEFAULT = os.path.join(RUN, "shared", "val")
SCORER_PY = "WORKDIR/runs/2026-10-16-2026/attempts/calibrator/venv/bin/python"
GOLD_ROOT = None   # run 2026-10-18-1758: set only by --val-check (validation gold); None = surprise-test gold


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
    if GOLD_ROOT is not None:   # run 2026-10-18-1758: --val-check only
        return os.path.join(GOLD_ROOT, p, fam, "solutions.tsv")
    return os.path.join(CLONE, "data-surprise", fam, "solutions-%s.tsv" % p)


def score_dir(p, resdir_of):
    fam_scores = {}
    for fam in FAMS:
        with contextlib.redirect_stdout(io.StringIO()):
            fam_scores[fam] = list(st.compare_words(gold(p, fam), resdir_of(fam), report=False)[-1][1:])
    tot = [statistics.mean([fam_scores[f][i] for f in FAMS]) for i in range(4)]
    return fam_scores, tot


def agg(s_by_p, how):
    """run 2026-10-18-1758: A = (S(0.10)+S(0.20)+S(0.30)+S(0.40)+S(0.50))/5; how = 'ltr' (left to right in PROPS
    order) or 'builtin' (Python's builtin sum)."""
    vals = [s_by_p[p] for p in PROPS]
    return (naive_sum(vals) if how == "ltr" else builtins.sum(vals)) / 5


def margin_of(value, bar, direction):
    return (bar - value) if direction == "lower" else (value - bar)


def walk_line(values, bar, direction, info_bar):
    """run 2026-10-18-1758: values/info_bar = {'ltr': x, 'builtin': y}; bar = float (PREREG). Returns (dict, text)."""
    ent, parts, meets_all = {}, [], True
    for mode in ("ltr", "builtin"):
        m = margin_of(values[mode], bar, direction)
        mi = margin_of(values[mode], info_bar[mode], direction) if info_bar else None
        meets = m > MARGIN
        meets_all = meets_all and meets
        ent[mode] = {"value": values[mode], "bar": bar, "margin": m, "meets_i": meets,
                     "margin_vs_mockingbird_recomputed": mi}
        parts.append("%s: %r bar %r margin %.12f -> %s%s" % (
            mode, values[mode], bar, m, "MEETS (i)" if meets else "fails (i)",
            "" if mi is None else "; vs Mockingbird-I1 recomputed %.12f" % mi))
    ent["meets_i_both_modes"] = meets_all
    return ent, " | ".join(parts) + " | both modes: %s" % ("MEETS (i)" if meets_all else "fails (i)")


def entry_files(d, p):
    return [os.path.join(d, "test", p, fam, "result-%s.tsv" % p) for fam in FAMS]


def dry_run(entries, cand, out_json):
    """run 2026-10-18-0839: list every input of the real run with os.path.getsize (stat only, nothing opened).
    run 2026-10-18-1758: entries/COMBs at 0.40, candidate at all five P, no FeVeT."""
    plan = []
    for p in CALIB_PROPS:
        plan.append(("official results JSON", os.path.join(CLONE, "results", "results-surprise-%s.json" % p), "gold"))
        for fam in FAMS:
            plan.append(("Mockingbird-I1 predictions",
                         os.path.join(CLONE, "systems", "mockingbird-i1", "surprise", fam, "result-%s.tsv" % p), ""))
            plan.append(("surprise solutions", gold(p, fam), "gold"))
    if cand:
        for p in PROPS:
            if p not in CALIB_PROPS:
                for fam in FAMS:
                    plan.append(("surprise solutions", gold(p, fam), "gold"))
    for name, d in entries:
        if not os.path.isdir(os.path.join(d, "test", P)):
            plan.append(("entry %s (would be skipped: no test/%s folder)" % (name, P), os.path.join(d, "test", P), ""))
            continue
        for q in entry_files(d, P):
            plan.append(("entry %s" % name, q, ""))
    if cand:
        cname, cdir = cand
        for p in PROPS:
            for q in entry_files(cdir, p):
                plan.append(("candidate %s" % cname, q, ""))
    n_ok = n_miss = n_gold = 0
    print("DRY-RUN score_test_040: nothing is opened; one stat() per file. clone %s" % CLONE)
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


def import_scorer():
    global st, lingrex_util
    import mplstub  # noqa: F401
    with contextlib.redirect_stdout(io.StringIO()):
        import sigtypst2022 as _st
    import lingrex.util as _lu
    st, lingrex_util = _st, _lu


def val_check(entries, val_root, out_json):
    """run 2026-10-18-1758: validation-gold check of the scoring code path (never reads surprise-test gold)."""
    global GOLD_ROOT
    vp = "0.50"
    GOLD_ROOT = os.path.abspath(val_root)
    two = entries[:2]
    if len(two) < 2:
        raise SystemExit("--val-check needs at least two entries in --entries")
    for name, d in two:
        for fam in FAMS:
            for q in (os.path.join(d, "val", vp, fam, "result-%s.tsv" % vp), gold(vp, fam)):
                if not os.path.isfile(q):
                    raise SystemExit("--val-check: missing %s" % q)
    import_scorer()
    res = {"ltr": {}, "builtin": {}, "val_scorer": {}, "checks": {}}
    for mode in ("ltr", "builtin"):
        set_mode(mode)
        for name, d in two:
            fs, tot = score_dir(vp, lambda fam: os.path.join(d, "val", vp, fam, "result-%s.tsv" % vp))
            res[mode][name] = {"total": tot, "families": fs}
            print("%s val %s %-32s ED %r NED %r BCFS %r BLEU %r" % (mode, vp, name, *tot), flush=True)
    bad = 0
    with tempfile.TemporaryDirectory() as tmp:
        env = dict(os.environ, STUB_MPL="1", HOME=tmp, MPLCONFIGDIR=os.path.join(tmp, "mpl"), OMP_NUM_THREADS="1",
                   OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1")
        for k, (name, d) in enumerate(two):
            jf = os.path.join(tmp, "vs%d.json" % k)
            cmd = [SCORER_PY, "-I", os.path.join(HERE, "val_scorer.py"), "--pred", d, "--props", vp,
                   "--fams", ",".join(FAMS), "--json", jf, "--gold-root", GOLD_ROOT]
            r = subprocess.run(cmd, env=env, stdout=subprocess.DEVNULL)
            if r.returncode != 0:
                raise SystemExit("val_scorer.py failed (%d) for %s" % (r.returncode, name))
            with open(jf) as f:
                vs = json.load(f)[vp]
            res["val_scorer"][name] = vs
            mine = res["builtin"][name]
            fam_ok = all(mine["families"][fam] == vs[fam] for fam in FAMS)
            tot_ok = mine["total"] == vs["total"]
            bad += not (fam_ok and tot_ok)
            ltr_eq = res["ltr"][name]["total"] == mine["total"]
            res["checks"][name] = {"builtin_families_bit_identical_to_val_scorer": fam_ok,
                                   "builtin_total_bit_identical_to_val_scorer": tot_ok,
                                   "ltr_total_equals_builtin_total": ltr_eq}
            print("VALCHECK %-32s builtin vs val_scorer.py: families %s total %s (NED %r vs %r); ltr total %s builtin" % (
                name, "EXACT" if fam_ok else "DIFF", "EXACT" if tot_ok else "DIFF", mine["total"][1], vs["total"][1],
                "==" if ltr_eq else "!="), flush=True)
    # code-path exercise of agg() and the walk on validation numbers (no claim meaning)
    (n1, _), (n2, _) = two
    ex = {}
    for cell, metric, idx, direction, _bar in CELLS_A:
        a = {m: agg({p: res[m][n1]["total"][idx] for p in PROPS}, m) for m in ("ltr", "builtin")}
        b = {m: res[m][n2]["total"][idx] for m in ("ltr", "builtin")}
        ent, text = walk_line(a, b["ltr"], direction, b)
        ent["agg_ltr_equals_5x_over_5"] = a["ltr"] == naive_sum([res["ltr"][n1]["total"][idx]] * 5) / 5
        ex[cell] = ent
        print("EXERCISE (val, no claim meaning) %s-like %s: A(%s x5) vs %s | %s" % (cell, metric, n1, n2, text))
    res["exercise"] = ex
    res["valcheck_pass"] = bad == 0
    with open(out_json, "w") as f:
        json.dump(res, f, indent=1)
    print("VALCHECK %s" % ("PASS" if bad == 0 else "FAIL %d" % bad))
    return 0 if bad == 0 else 1


def load_list(path):
    with open(path) as f:
        return [(e["name"], os.path.abspath(e["dir"])) for e in json.load(f)]


def main():
    global CLONE, CALIB_PROPS
    ap = argparse.ArgumentParser(description="PREREG rule 11 test scoring at 0.40 and the five-P aggregate (reads "
                                             "surprise-test gold; main session only, after selection.md exists)")
    ap.add_argument("--json", required=True)
    ap.add_argument("--entries", required=True, help="JSON list of {name, dir}; dir holds test/0.40/FAM/result-0.40.tsv")
    ap.add_argument("--combs", help="JSON list of {name, dir} of COMB folders (stage2x OUT), scored like entries")
    ap.add_argument("--candidate-dir", help="rule 10 candidate folder holding test/P/FAM/result-P.tsv for all five P")
    ap.add_argument("--candidate", default="CANDIDATE", help="label of the rule 10 candidate")
    ap.add_argument("--dry-run", action="store_true", help="list the inputs (stat only) and exit; opens nothing")
    ap.add_argument("--val-check", action="store_true", help="validation-gold check of the scoring path (first two "
                                                             "entries' val/0.50 files vs --val-root); no test gold")
    ap.add_argument("--val-root", default=VAL_ROOT_DEFAULT, help="validation gold root (P/FAM/solutions.tsv)")
    ap.add_argument("--clone", default=CLONE, help="pinned clone (or a claim package's official/ folder)")
    ap.add_argument("--calib-props", default=",".join(PROPS), help="Mockingbird-I1 calibration proportions "
                                                                 "(PREREG rule 11 (a): all five)")
    a = ap.parse_args()
    CLONE = os.path.abspath(a.clone)
    CALIB_PROPS = a.calib_props.split(",")
    ENTRIES = load_list(a.entries)
    if a.val_check:
        return val_check(ENTRIES, a.val_root, a.json)
    if a.combs:
        ENTRIES += load_list(a.combs)
    names = [e for e, _ in ENTRIES]
    if len(set(names)) != len(names):
        raise SystemExit("duplicate names in --entries/--combs")
    if P not in CALIB_PROPS:
        raise SystemExit("--calib-props must include %s" % P)
    if CALIB_PROPS != PROPS:
        print("NOTE: Mockingbird-I1 calibration at %s only (PREREG rule 11 (a) needs all five P for the main "
              "session's scoring; the aggregate bars cannot be asserted)" % ",".join(CALIB_PROPS))
    cand = (a.candidate, os.path.abspath(a.candidate_dir)) if a.candidate_dir else None
    if a.dry_run:
        return dry_run(ENTRIES, cand, a.json)
    # run 2026-10-18-1758: every prediction file is checked to exist before the scorer is imported
    missing = [q for _, d in ENTRIES if os.path.isdir(os.path.join(d, "test", P)) for q in entry_files(d, P)
               if not os.path.isfile(q)]
    if cand:
        missing += [q for p in PROPS for q in entry_files(cand[1], p) if not os.path.isfile(q)]
    if missing:
        raise SystemExit("missing prediction files (nothing scored):\n" + "\n".join(missing))
    import_scorer()
    res = {"ltr": {}, "builtin": {}}
    with tempfile.TemporaryDirectory():
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
            # (b) eligible entries, COMB-6, COMB-8, COMB-10: P 0.40 only (run 2026-10-18-1758)
            for e, edir in ENTRIES:
                if not os.path.isdir(os.path.join(edir, "test", P)):
                    print("%s %s %-30s skipped (no test/%s folder)" % (mode, P, e, P), flush=True)
                    continue
                fs, tot = score_dir(P, lambda fam: os.path.join(edir, "test", P, fam, "result-%s.tsv" % P))
                R[P][e] = {"total": tot, "families": fs}
                print("%s %s %-30s ED %.6f NED %r BCFS %r BLEU %r" % (mode, P, e, tot[0], tot[1], tot[2], tot[3]),
                      flush=True)
            # (c) the candidate at all five P (run 2026-10-18-1758)
            if cand:
                cname, cdir = cand
                R["candidate"] = {"name": cname, "dir": cdir}
                for p in PROPS:
                    fs, tot = score_dir(p, lambda fam: os.path.join(cdir, "test", p, fam, "result-%s.tsv" % p))
                    R["candidate"][p] = {"total": tot, "families": fs}
                    print("%s %s CANDIDATE %-20s ED %.6f NED %r BCFS %r BLEU %r" % (
                        mode, p, cname, tot[0], tot[1], tot[2], tot[3]), flush=True)
    # bars (run 2026-10-18-1758): assert the PREREG table against the official totals
    print()
    bars_ok = True
    off40 = res["ltr"][P]["Mockingbird-I1"]["official_total"]
    for cell, metric, idx, direction, bar in CELLS_P:
        eq = repr(off40[idx]) == bar
        bars_ok &= eq
        print("BAR %s Mockingbird-I1 official 0.40 %s %r PREREG %s: %s" % (cell, metric, off40[idx], bar,
                                                                         "EQUAL" if eq else "DIFFERENT"))
    mb_agg = {}
    if CALIB_PROPS == PROPS:
        for cell, metric, idx, direction, bar in CELLS_A:
            off = {p: res["ltr"][p]["Mockingbird-I1"]["official_total"][idx] for p in PROPS}
            rec = {p: res["builtin"][p]["Mockingbird-I1"]["total"][idx] for p in PROPS}
            mb_agg[cell] = {"ltr_from_official": agg(off, "ltr"), "builtin_from_official": agg(off, "builtin"),
                            "builtin_from_recomputed": agg(rec, "builtin")}
            eq = repr(mb_agg[cell]["ltr_from_official"]) == bar
            bars_ok &= eq
            print("BAR %s Mockingbird-I1 A_%s from official totals ltr %r builtin-sum %r (recomputed builtin %r) "
                  "PREREG %s: %s" % (cell, metric, mb_agg[cell]["ltr_from_official"],
                                     mb_agg[cell]["builtin_from_official"], mb_agg[cell]["builtin_from_recomputed"],
                                     bar, "EQUAL" if eq else "DIFFERENT"))
    res["mockingbird_aggregates"] = mb_agg
    res["bars_equal_prereg"] = bars_ok
    if not bars_ok:
        print("BAR CHECK FAILED: the claim walk is not run")
        with open(a.json, "w") as f:
            json.dump(res, f, indent=1)
        return 1
    # candidate consistency with its entry line (information)
    if cand and cand[0] in res["ltr"][P]:
        for mode in ("ltr", "builtin"):
            eq = res[mode][P][cand[0]]["total"] == res[mode]["candidate"][P]["total"]
            print("candidate %s 0.40 totals (%s) from --candidate-dir vs its --entries line: %s" % (
                cand[0], mode, "EQUAL" if eq else "DIFFERENT"))
    # claim walk, rule 12 (i) only ((ii)-(iv) are checked separately); run 2026-10-18-1758: six cells
    print()
    walk = {}
    for cell, metric, idx, direction, bar in CELLS_P:
        info = {"ltr": res["ltr"][P]["Mockingbird-I1"]["official_total"][idx],
                "builtin": res["builtin"][P]["Mockingbird-I1"]["total"][idx]}
        print("%s (mean %s at %s, %s is better): bar Mockingbird-I1 %s" % (cell, metric, P, direction, bar))
        walk[cell] = {"metric": metric, "direction": direction, "bar": bar, "entries": {}}
        rows = [(e, {m: res[m][P][e]["total"][idx] for m in ("ltr", "builtin")}) for e, _ in ENTRIES
                if e in res["ltr"][P]]
        if cand:
            rows.append(("candidate-dir:" + cand[0], {m: res[m]["candidate"][P]["total"][idx]
                                                      for m in ("ltr", "builtin")}))
        for e, vals in rows:
            ent, text = walk_line(vals, float(bar), direction, info)
            walk[cell]["entries"][e] = ent
            mark = "CANDIDATE " if (cand and (e == cand[0] or e == "candidate-dir:" + cand[0])) else ""
            print("%s%s %s | %s" % (mark, cell, e, text))
        print()
    if cand and CALIB_PROPS == PROPS:
        for cell, metric, idx, direction, bar in CELLS_A:
            s = {m: {p: res[m]["candidate"][p]["total"][idx] for p in PROPS} for m in ("ltr", "builtin")}
            vals = {"ltr": agg(s["ltr"], "ltr"), "builtin": agg(s["builtin"], "builtin")}
            cross = {"ltr_totals_builtin_sum": agg(s["ltr"], "builtin"),
                     "builtin_totals_ltr_sum": agg(s["builtin"], "ltr")}
            info = {"ltr": mb_agg[cell]["ltr_from_official"], "builtin": mb_agg[cell]["builtin_from_recomputed"]}
            ent, text = walk_line(vals, float(bar), direction, info)
            ent["cross_combinations"] = cross
            ent["S_by_P"] = s
            walk[cell] = {"metric": metric, "direction": direction, "bar": bar, "candidate": cand[0], "entry": ent}
            print("%s (A_%s over %s, %s is better): bar Mockingbird-I1 %s" % (cell, metric, ",".join(PROPS),
                                                                             direction, bar))
            print("CANDIDATE %s %s | %s | cross: ltr totals + builtin sum %r, builtin totals + ltr sum %r" % (
                cell, cand[0], text, cross["ltr_totals_builtin_sum"], cross["builtin_totals_ltr_sum"]))
            print()
    elif not cand:
        print("no --candidate-dir: aggregate cells NA, BA, LA not walked")
    res["claim_walk_040"] = walk
    with open(a.json, "w") as f:
        json.dump(res, f, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
