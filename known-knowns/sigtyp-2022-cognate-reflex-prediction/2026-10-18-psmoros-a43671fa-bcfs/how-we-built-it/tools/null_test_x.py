#!/usr/bin/env python3
"""PREREG rule 13 null test, run 2026-10-18-0104: a copy of run 2026-10-17-1806's tools/null_test.py, made by the tools
engineer of run 2026-10-18-0104 while the lenses were running (never run by the tools engineer; it reads surprise-test
gold, so the main session runs it only after selection.md and tools/score_test.py). Changes, and nothing else:
  - seed base 20261018 (random.Random(20261018 + c));
  - --bar ours: the bar holder is run 2026-10-17-1806's frozen 0.10 combiner
    (attempts/combiner/frozen/PRIMARY/test/0.10/<fam>/result-0.10.tsv, same format as the candidate); --prop 0.10 only;
  - --agg: all five proportions in one null. Control c uses ONE random.Random(20261018 + c), drawing per P in the
    order 0.10, 0.20, 0.30, 0.40, 0.50, families in the FAMS order, sets in order of first appearance in that P's gold
    solutions file. Bar holder per P: FeVeT (published files) at 0.10, 0.30, 0.50, Mockingbird-I1 at 0.20, 0.40.
    --cand-dir then holds <P>/<fam>/result-<P>.tsv. d_c = (sum over P of (bar NED_P - cand NED_P), summed left to
    right in P order) / 5; real d likewise. The fast path is checked against compare_words on the real assignment and
    on the first 5 controls at every P;
  - FeVeT's published predictions are read from --fevet-dir (default: run 2026-10-17-1806's resume/data/fevet);
  - speed only: the fast path groups each family's items by gold language once (same values, same order, same
    left-to-right sums as the original per-language filter loop); the bit-identity check is unchanged;
  - output JSON also carries "controls_at_or_above_real" (= n_controls_ge_real).
Run 2026-10-18-0839 copy (tools engineer, Opus 5.5): unchanged logic; the output (stdout and JSON "command") also gives
the exact command line ("command: ..."), which null_test.md must quote.
Run 2026-10-18-1758 copy, tools/null_test_x.py (tools engineer, Opus 5.5; copied from tools/null_test.py of this run,
itself the run 2026-10-18-0839 file). Change, and nothing else:
  - new option --agg-bar mockingbird (valid only with --agg; PREREG 2026-10-18-1758 rule 13, cells NA): the aggregate
    null uses Mockingbird-I1's official per-item files at ALL five proportions as the bar side, i.e. for every P in
    0.10, 0.20, 0.30, 0.40, 0.50 and every FAM the bar file is
        CLONE/systems/mockingbird-i1/surprise/FAM/result-P.tsv
    (CLONE = the pinned clone WORKDIR/scratch_q15/ST2022, the same file the single-P mode reads for
    --bar mockingbird), instead of the AGG_BAR mix (FeVeT at 0.10, 0.30, 0.50). The bar-per-P map used is written
    to the JSON "bar" field and the "real P:" stdout lines, as before. Without --agg-bar (default) the --agg mode is
    the AGG_BAR mix exactly as in tools/null_test.py, and the single-P mode is unchanged. Everything else (seed
    base 20261018, one random.Random(20261018 + c) per control drawing P by P in the order 0.10 ... 0.50, families
    in FAMS order, sets in order of first appearance in that P's gold solutions file, d = (sum over P left to right
    of (bar NED_P - cand NED_P)) / 5, the compare_words bit-identity check on the real assignment and controls 0-4
    at every P, 400 controls, output fields) is unchanged.
  usage of the new mode (reads surprise-test gold CLONE/data-surprise/FAM/solutions-P.tsv; main session only, after
  selection.md):
       STUB_MPL=1 CALIBRATOR_VENV_PYTHON -I tools/null_test_x.py --agg --agg-bar mockingbird --cand-dir DIR --out OUT.json
           (DIR holds P/FAM/result-P.tsv for all five P; bar = CLONE/systems/mockingbird-i1/surprise/FAM/result-P.tsv)

Original description (run 2026-10-17-1806):
Paired permutation null between candidate(P) and the bar holder's per-item predictions at P, 400 controls.
In control c, for every cognate set (COGID without its "-i" suffix) of every family, the two systems' predictions for
all rows of that set are swapped with probability 1/2 (one draw per set, families in the FAMS order below, sets in
order of first appearance in the gold solutions file). d_c = NED(bar side) - NED(candidate side), computed with the
scorer's own per-item NED (sigtypst2022 nw_align rule) and the scorer's aggregation (per-language mean, sum over
languages / number of gold-header languages, statistics.mean over the 10 families) with left-to-right summation.
Real d = NED(bar holder) - NED(candidate). The per-item fast path is checked against the official compare_words on
the real assignment and on the first 5 controls (bit identity required).

usage: STUB_MPL=1 <calibrator venv python> -I tools/null_test.py --prop P --cand-dir DIR --bar fevet|mockingbird|ours
           --out OUT.json [--fevet-dir D]          (DIR holds <fam>/result-<P>.tsv)
       STUB_MPL=1 <calibrator venv python> -I tools/null_test.py --agg --cand-dir DIR --out OUT.json [--fevet-dir D]
                                                   (DIR holds <P>/<fam>/result-<P>.tsv)
"""
import argparse
import contextlib
import csv
import io
import json
import os
import random
import statistics
import sys
import tempfile
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mplstub  # noqa: F401,E402
with contextlib.redirect_stdout(io.StringIO()):
    import sigtypst2022 as st  # noqa: E402
import lingrex.util  # noqa: E402

RUN = os.path.dirname(HERE)
CLONE = "WORKDIR/scratch_q15/ST2022"
FEVET_DIR_DEFAULT = "WORKDIR/runs/2026-10-17-1806/resume/data/fevet"
OURS_DIR = "WORKDIR/runs/2026-10-17-1806/attempts/combiner/frozen/PRIMARY/test"
PROPS = ["0.10", "0.20", "0.30", "0.40", "0.50"]
AGG_BAR = {"0.10": "fevet", "0.20": "mockingbird", "0.30": "fevet", "0.40": "mockingbird", "0.50": "fevet"}
FAMS = ["bantubvd", "beidazihui", "birchallchapacuran", "bodtkhobwa", "bremerberta", "deepadungpalaung",
        "hillburmish", "kesslersignificance", "luangthongkumkaren", "wangbai"]
N_CONTROLS = 400
SEED_BASE = 20261018


def ltr_sum(iterable, start=0):
    acc = start
    for x in iterable:
        acc = acc + x
    return acc


st.sum = ltr_sum
lingrex.util.sum = ltr_sum


def load(path):
    with contextlib.redirect_stdout(io.StringIO()):
        langs, _, data = st.load_cognate_file(path)
    return langs, data


def item_ned(entryA, entryB):
    """compare_words' per-item scoreD, verbatim logic."""
    if not entryB:
        entryB = (2 * len(entryA)) * ["Ø"]
    almA, almB, _ = st.nw_align(entryA, entryB)
    score = 0
    for a, b in zip(almA, almB):
        if a == b and a not in "Ø?-":
            pass
        elif a != b:
            score += 1
    return score / len(almA)


def bar_predictions(bar, p, fam, glangs, gold, fevet_dir):
    if bar == "mockingbird":
        _, d = load(os.path.join(CLONE, "systems", "mockingbird-i1", "surprise", fam, "result-%s.tsv" % p))
        return d
    if bar == "ours":
        _, d = load(os.path.join(OURS_DIR, p, fam, "result-%s.tsv" % p))
        return d
    pred = defaultdict(dict)
    with open(os.path.join(fevet_dir, "pred_%s_%s.tsv" % (p, fam)), encoding="utf-8") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            pred[row["COGID"]][row["LANGUAGE"]] = row["PREDICTION"].split()
    return pred


def family_items(p, fam, cand_dir, bar, fevet_dir):
    glangs, gold = load(os.path.join(CLONE, "data-surprise", fam, "solutions-%s.tsv" % p))
    _, cand = load(os.path.join(cand_dir, fam, "result-%s.tsv" % p))
    barp = bar_predictions(bar, p, fam, glangs, gold, fevet_dir)
    items = []   # in compare_words order: languages (gold header), then gold file key order
    for lg in glangs:
        for key in gold:
            if lg in gold[key]:
                eA = gold[key][lg]
                if " ".join(eA):
                    c = cand.get(key, {}).get(lg, [])
                    b = barp.get(key, {}).get(lg, [])
                    items.append((lg, key, item_ned(eA, c), item_ned(eA, b)))
    order = []
    for key in gold:
        base = key.rsplit("-", 1)[0]
        if base not in order:
            order.append(base)
    by_lang = defaultdict(list)   # same items, same order, grouped once (speed only)
    for (l, key, nc, nb) in items:
        by_lang[l].append((key.rsplit("-", 1)[0], nc, nb))
    return glangs, items, order, gold, cand, barp, dict(by_lang)


def fam_ned(glangs, by_lang, swapped, side):
    """side 0 = candidate slot, 1 = bar slot; swapped = set of base COGIDs whose two predictions are exchanged.
    Per language: the values of its items in compare_words order, summed left to right (as the original loop)."""
    per_lang = []
    for lg in glangs:
        its = by_lang.get(lg)
        if not its:
            continue
        vals = [nc if ((side == 0) != (base in swapped)) else nb for base, nc, nb in its]
        per_lang.append(ltr_sum(vals) / len(vals))
    return ltr_sum(per_lang) / len(glangs)


def official(p, fam, preds, tmp, tag, glangs):
    path = os.path.join(tmp, tag, fam, "result-%s.tsv" % p)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("COGID\t" + "\t".join(glangs) + "\n")
        for k, v in preds.items():
            fh.write(k + "".join("\t" + " ".join(v.get(lg, [])) for lg in glangs) + "\n")
    with contextlib.redirect_stdout(io.StringIO()):
        return st.compare_words(os.path.join(CLONE, "data-surprise", fam, "solutions-%s.tsv" % p), path,
                                report=False)[-1][2]


def total(Fp, swaps, side):
    return statistics.mean([fam_ned(Fp[f][0], Fp[f][6], swaps.get(f, set()), side) for f in FAMS])


def check_prop(p, Fp, sw, tmp, tag):
    """compare_words on the assignment sw (both sides) vs the fast path; returns (official, fast, identical)."""
    vals = []
    for side in (0, 1):
        fams = []
        for f in FAMS:
            glangs, items, order, gold, cand, barp, _ = Fp[f]
            preds = {}
            for key in gold:
                base = key.rsplit("-", 1)[0]
                use_c = (side == 0) != (base in sw.get(f, set()))
                src = cand if use_c else barp
                preds[key] = {lg: src.get(key, {}).get(lg, []) for lg in glangs if gold[key].get(lg)}
            fams.append(official(p, f, preds, tmp, "%s_s%d" % (tag, side), glangs))
        vals.append(statistics.mean(fams))
    fast = (total(Fp, sw, 0), total(Fp, sw, 1))
    return vals, list(fast), fast[0] == vals[0] and fast[1] == vals[1]


def run_single(a):
    p = a.prop
    if a.bar == "ours" and p != "0.10":
        raise SystemExit("--bar ours exists at P 0.10 only")
    F = {fam: family_items(p, fam, a.cand_dir, a.bar, a.fevet_dir) for fam in FAMS}

    def swaps_for(c):
        rng = random.Random(SEED_BASE + c)
        return {f: {b for b in F[f][2] if rng.random() < 0.5} for f in FAMS}

    real_c, real_b = total(F, {}, 0), total(F, {}, 1)
    real = real_b - real_c
    print("real: candidate NED %r, bar NED %r, d = %r" % (real_c, real_b, real))
    # bit-identity check of the fast path against compare_words
    checks = []
    with tempfile.TemporaryDirectory() as tmp:
        for c in [None, 0, 1, 2, 3, 4]:
            sw = {} if c is None else swaps_for(c)
            vals, fast, ok = check_prop(p, F, sw, tmp, "c%s" % c)
            checks.append({"control": c, "official": vals, "fast": fast, "bit_identical": ok})
            print("check control %s: official %r / %r, fast %r / %r -> %s" % (
                c, vals[0], vals[1], fast[0], fast[1], "IDENTICAL" if ok else "DIFFERENT"), flush=True)
    ds = []
    for c in range(N_CONTROLS):
        sw = swaps_for(c)
        ds.append(total(F, sw, 1) - total(F, sw, 0))
    best = max(ds)
    n_ge = sum(1 for d in ds if d >= real)
    res = {"prop": p, "bar": a.bar, "seed_base": SEED_BASE, "controls": N_CONTROLS, "best_control": best,
           "real": real, "real_beats_all_controls": real > best, "candidate_ned": real_c, "bar_ned": real_b,
           "control_mean": statistics.mean(ds), "control_sd": statistics.pstdev(ds),
           "n_controls_ge_real": n_ge, "controls_at_or_above_real": n_ge,
           "fast_path_checks": checks, "fast_path_all_identical": all(c["bit_identical"] for c in checks),
           "d_controls": ds}
    return res


def run_agg(a):
    # run 2026-10-18-1758 (null_test_x.py): --agg-bar mockingbird puts Mockingbird-I1 at every P; default = AGG_BAR
    bar_by_p = {p: "mockingbird" for p in PROPS} if a.agg_bar == "mockingbird" else dict(AGG_BAR)
    FP = {p: {fam: family_items(p, fam, os.path.join(a.cand_dir, p), bar_by_p[p], a.fevet_dir) for fam in FAMS}
          for p in PROPS}

    def swaps_for(c):
        rng = random.Random(SEED_BASE + c)   # one generator per control, drawn P by P, family by family, set by set
        return {p: {f: {b for b in FP[p][f][2] if rng.random() < 0.5} for f in FAMS} for p in PROPS}

    def d_of(sw):
        return ltr_sum([total(FP[p], sw.get(p, {}), 1) - total(FP[p], sw.get(p, {}), 0) for p in PROPS]) / len(PROPS)

    real_c = {p: total(FP[p], {}, 0) for p in PROPS}
    real_b = {p: total(FP[p], {}, 1) for p in PROPS}
    real = d_of({})
    cand_agg = ltr_sum([real_c[p] for p in PROPS]) / len(PROPS)
    bar_agg = ltr_sum([real_b[p] for p in PROPS]) / len(PROPS)
    for p in PROPS:
        print("real %s: candidate NED %r, bar (%s) NED %r" % (p, real_c[p], bar_by_p[p], real_b[p]))
    print("real aggregate: candidate %r, bar %r, d = %r" % (cand_agg, bar_agg, real))
    checks = []
    with tempfile.TemporaryDirectory() as tmp:
        for c in [None, 0, 1, 2, 3, 4]:
            sw = {} if c is None else swaps_for(c)
            for p in PROPS:
                vals, fast, ok = check_prop(p, FP[p], sw.get(p, {}), tmp, "c%s_%s" % (c, p))
                checks.append({"control": c, "prop": p, "official": vals, "fast": fast, "bit_identical": ok})
                print("check control %s P %s: official %r / %r, fast %r / %r -> %s" % (
                    c, p, vals[0], vals[1], fast[0], fast[1], "IDENTICAL" if ok else "DIFFERENT"), flush=True)
    ds = []
    for c in range(N_CONTROLS):
        ds.append(d_of(swaps_for(c)))
    best = max(ds)
    n_ge = sum(1 for d in ds if d >= real)
    res = {"prop": "AGG", "bar": dict(bar_by_p), "seed_base": SEED_BASE, "controls": N_CONTROLS,
           "best_control": best, "real": real, "real_beats_all_controls": real > best,
           "candidate_ned": cand_agg, "bar_ned": bar_agg, "candidate_ned_by_prop": real_c,
           "bar_ned_by_prop": real_b, "control_mean": statistics.mean(ds), "control_sd": statistics.pstdev(ds),
           "n_controls_ge_real": n_ge, "controls_at_or_above_real": n_ge, "fast_path_checks": checks,
           "fast_path_all_identical": all(c["bit_identical"] for c in checks), "d_controls": ds}
    return res


def command_line():
    """run 2026-10-18-0839: the exact command line, for null_test.md's 'command:' field."""
    import shlex
    env = "STUB_MPL=%s " % os.environ["STUB_MPL"] if os.environ.get("STUB_MPL") else ""
    return env + shlex.join([sys.executable] + (["-I"] if sys.flags.isolated else []) + sys.argv)


def main():
    ap = argparse.ArgumentParser(description="PREREG rule 13 paired permutation null (reads surprise-test gold; main "
                                             "session only)")
    ap.add_argument("--prop", help="single-P mode: the proportion")
    ap.add_argument("--agg", action="store_true", help="aggregate null over all five proportions")
    ap.add_argument("--cand-dir", required=True,
                    help="single-P: DIR/<fam>/result-<P>.tsv; --agg: DIR/<P>/<fam>/result-<P>.tsv")
    ap.add_argument("--bar", choices=("fevet", "mockingbird", "ours"), help="single-P mode: the bar holder")
    ap.add_argument("--fevet-dir", default=FEVET_DIR_DEFAULT)
    ap.add_argument("--agg-bar", choices=("mockingbird",),
                    help="run 2026-10-18-1758: with --agg, the bar side is Mockingbird-I1 at all five P "
                         "(CLONE/systems/mockingbird-i1/surprise/FAM/result-P.tsv); default: the AGG_BAR mix")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    if a.agg_bar and not a.agg:
        raise SystemExit("--agg-bar is valid only with --agg")
    if a.agg:
        if a.prop or a.bar:
            raise SystemExit("--agg fixes the proportions and bar holders; do not pass --prop or --bar")
        res = run_agg(a)
    else:
        if not a.prop or not a.bar:
            raise SystemExit("single-P mode needs --prop and --bar")
        res = run_single(a)
    res["command"] = command_line()
    with open(a.out, "w") as f:
        json.dump(res, f, indent=1)
    print("fast path bit-identical in every check: %s" % ("yes" if res["fast_path_all_identical"] else "NO"))
    print("controls: %d" % N_CONTROLS)
    print("best_control: %r" % res["best_control"])
    print("real: %r" % res["real"])
    print("real_beats_all_controls: %s" % ("yes" if res["real_beats_all_controls"] else "no"))
    print("control mean %r sd %r; controls >= real: %d" % (res["control_mean"], res["control_sd"],
                                                           res["n_controls_ge_real"]))
    print("command: %s" % res["command"])


if __name__ == "__main__":
    main()
