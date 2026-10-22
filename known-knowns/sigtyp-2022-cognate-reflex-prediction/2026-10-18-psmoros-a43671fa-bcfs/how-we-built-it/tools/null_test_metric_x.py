#!/usr/bin/env python3
"""Paired permutation null of PREREG.v2 (BLEU) and PREREG.v3 (BCFS), run 2026-10-18-0202 (standard library only).
Main session; written for the session that scores the BLEU/BCFS objects (validated here on validation data only).

In control c, for every cognate set (COGID without its last "-i" suffix) of every family (families in the fixed order,
sets in order of first appearance in the gold solutions file), one draw of random.Random(SEED + c) decides whether the
candidate's and the bar holder's predictions for all rows of that set are swapped (draw < 0.5). The family metric is
the official one (tools/metric_tools.py: BLEU item mean per language, or B-cubed F of the concatenated alignments per
language; sum over languages with items / header languages; left-to-right sums); the system value is the mean over
the families. d_c = M(candidate side) - M(bar side) (higher is better for both metrics); real d likewise without swaps.

usage: python3 -I tools/null_test_metric.py --metric bleu|bcfs --gold-dir G --cand-dir C --bar-dir B --prop P
           --out OUT.json [--controls 400] [--seed 20261018] [--fams a,b]
       (G holds FAM/solutions-P.tsv or FAM/solutions.tsv; C and B hold FAM/result-P.tsv)
Run 2026-10-18-0839 copy (tools engineer, Opus 5.5): unchanged logic; the output JSON also carries "real" (= real_d)
and "command", and stdout ends with "command: ..." (the exact command line, which null_test.md must quote). For the
cells B50/L50 the bar holder's files are FeVeT's published 0.50 predictions put into this layout by
tools/fevet_to_harness.py.
Run 2026-10-18-1758 copy, tools/null_test_metric_x.py (tools engineer, Opus 5.5; copied from tools/null_test_metric.py
of this run, itself the run 2026-10-18-0839 file). Change, and nothing else: a new --agg mode (PREREG 2026-10-18-1758
rule 13, cells BA and LA); without --agg the tool behaves exactly as tools/null_test_metric.py (--prop is still
required there; it is only no longer an argparse "required" option, the check is done in main()).
  --agg: all five proportions in one null, for --metric bcfs or bleu. PROPS = 0.10, 0.20, 0.30, 0.40, 0.50.
    Folder layout, per P, for each of --gold-dir G, --cand-dir C, --bar-dir B (decided per folder, all-or-none):
      (a) if all five subfolders DIR/0.10 ... DIR/0.50 exist, DIR/P is that P's folder (P/FAM/... layout);
      (b) if none exists, DIR itself is every P's folder (FAM/... layout, file names carry P, as in the pinned clone);
      (c) any other mix stops the tool.
    Inside that P folder the single-P conventions apply unchanged: gold = FAM/solutions-P.tsv, else FAM/solutions.tsv;
    candidate and bar = FAM/result-P.tsv. For the cells BA/LA (main session only, after selection.md):
      G = WORKDIR/scratch_q15/ST2022/data-surprise              (FAM/solutions-P.tsv, layout b)
      B = WORKDIR/scratch_q15/ST2022/systems/mockingbird-i1/surprise   (Mockingbird-I1's official
          FAM/result-P.tsv, layout b)
      C = the candidate's test folder holding P/FAM/result-P.tsv (layout a)
    The resolved file paths are printed ("input: ...") and listed in the JSON "inputs".
    Control c uses ONE random.Random(seed + c) (seed default 20261018), drawing per P in the order 0.10, 0.20, 0.30,
    0.40, 0.50, within a P families in FAMS order (or --fams order), sets in order of first appearance in that P's gold
    solutions file (one draw per set; swap if draw < 0.5), exactly the single-P draw repeated per P with the same
    generator. Advantage at P = M_P(candidate side) - M_P(bar side), M_P = the single-P system value (family mean,
    left-to-right sums). d_c = (sum over P, left to right in P order, of the advantage at P) / 5; real d likewise
    without swaps. A_m(candidate) and A_m(bar) = (left-to-right sum over P of M_P) / 5 are reported too.
    Built-in check (agg mode only): on the real assignment and controls 0-4 at every P, the fast per-item values are
    compared with tools/metric_tools.family_scores run on the swapped prediction files' contents (bit identity
    required; reported as "fast_path_all_identical"; the tool stops if any differs). The JSON also carries
    "d_controls", "candidate_by_prop", "bar_by_prop", "advantage_by_prop".
  usage (agg): python3 -I tools/null_test_metric_x.py --agg --metric bleu|bcfs --gold-dir G --cand-dir C --bar-dir B
           --out OUT.json [--controls 400] [--seed 20261018] [--fams a,b]
       (each of G, C, B: P/FAM/... for all five P, or FAM/... with P in the file names; e.g.
        B = PINNED_CLONE/systems/mockingbird-i1/surprise holding FAM/result-P.tsv)
"""
import argparse
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import metric_tools as m  # noqa: E402

FAMS = ["bantubvd", "beidazihui", "birchallchapacuran", "bodtkhobwa", "bremerberta", "deepadungpalaung",
        "hillburmish", "kesslersignificance", "luangthongkumkaren", "wangbai"]


def gold_path(d, fam, p):
    for name in ("solutions-%s.tsv" % p, "solutions.tsv"):
        q = os.path.join(d, fam, name)
        if os.path.isfile(q):
            return q
    raise SystemExit("no gold for %s in %s" % (fam, d))


def prepare(gp, cand, bar):
    """Per language: list of (set id, cand item data, bar item data); item data = (bleu, almA, almB)."""
    langs, gold = m.load_cognate_file(gp)
    order = []
    for key in gold:
        s = key.rsplit("-", 1)[0]
        if s not in order:
            order.append(s)
    per = []
    for lg in langs:
        rows = []
        for key in gold:
            if lg in gold[key] and " ".join(gold[key][lg]):
                a = gold[key][lg]
                its = []
                for pr in (cand, bar):
                    b = pr.get(key, {}).get(lg, [])
                    if not b:
                        b = (2 * len(a)) * ["Ø"]
                    A, B = m.nw_align(a, b)[:2]
                    its.append((m.bleu_item(a, b), A, B))
                rows.append((key.rsplit("-", 1)[0], its[0], its[1]))
        per.append(rows)
    return len(langs), order, per


def fam_value(n_langs, per, swapped, metric, side):
    vals = []
    for rows in per:
        if not rows:
            continue
        if metric == "bleu":
            xs = []
            for s, ic, ib in rows:
                use_c = (side == 0) != (s in swapped)
                xs.append((ic if use_c else ib)[0])
            vals.append(m.ltr_sum(xs) / len(xs))
        else:
            almsA, almsB = [], []
            for s, ic, ib in rows:
                use_c = (side == 0) != (s in swapped)
                it = ic if use_c else ib
                almsA += it[1]
                almsB += it[2]
            vals.append(m.bcfs_of(almsA, almsB))
    return m.ltr_sum(vals) / n_langs


PROPS = ["0.10", "0.20", "0.30", "0.40", "0.50"]   # run 2026-10-18-1758: --agg order


def prop_dirs(d):
    """run 2026-10-18-1758 (--agg): per-P folder of d: d/P if all five exist, d if none exists, else stop."""
    have = [os.path.isdir(os.path.join(d, p)) for p in PROPS]
    if all(have):
        return {p: os.path.join(d, p) for p in PROPS}
    if not any(have):
        return {p: d for p in PROPS}
    raise SystemExit("%s holds some but not all of the P subfolders %s" % (d, ",".join(PROPS)))


def run_agg(a, fams):
    """run 2026-10-18-1758: the aggregate null over PROPS (see the module docstring)."""
    G, C, B = prop_dirs(a.gold_dir), prop_dirs(a.cand_dir), prop_dirs(a.bar_dir)
    data, raw, inputs = {}, {}, []
    for p in PROPS:
        data[p], raw[p] = [], []
        for f in fams:
            cp = os.path.join(C[p], f, "result-%s.tsv" % p)
            bp = os.path.join(B[p], f, "result-%s.tsv" % p)
            gp = gold_path(G[p], f, p)
            for role, q in (("gold", gp), ("candidate", cp), ("bar", bp)):
                if not os.path.isfile(q):
                    raise SystemExit("missing %s file %s" % (role, q))
                inputs.append({"prop": p, "family": f, "role": role, "path": q})
            cand = m.load_cognate_file(cp)[1]
            bar = m.load_cognate_file(bp)[1]
            data[p].append(prepare(gp, cand, bar))
            raw[p].append((gp, cand, bar))
    for it in inputs:
        print("input: %s %s %s %s" % (it["prop"], it["family"], it["role"], it["path"]))

    def system(p, swapped_by_fam, side):
        return m.ltr_sum([fam_value(n, per, swapped_by_fam[i], a.metric, side)
                          for i, (n, order, per) in enumerate(data[p])]) / len(data[p])

    def swaps_for(c):
        rng = random.Random(a.seed + c)   # one generator per control, drawn P by P, family by family, set by set
        sw = {}
        for p in PROPS:
            sw[p] = []
            for n, order, per in data[p]:
                sw[p].append({s for s in order if rng.random() < 0.5})
        return sw

    def d_of(sw):
        return m.ltr_sum([system(p, sw[p], 0) - system(p, sw[p], 1) for p in PROPS]) / len(PROPS)

    none = {p: [set() for _ in data[p]] for p in PROPS}
    c_by = {p: system(p, none[p], 0) for p in PROPS}
    b_by = {p: system(p, none[p], 1) for p in PROPS}
    adv_by = {p: c_by[p] - b_by[p] for p in PROPS}
    real = d_of(none)
    c_agg = m.ltr_sum([c_by[p] for p in PROPS]) / len(PROPS)
    b_agg = m.ltr_sum([b_by[p] for p in PROPS]) / len(PROPS)
    for p in PROPS:
        print("real %s: candidate %s %r, bar %r, advantage %r" % (p, a.metric, c_by[p], b_by[p], adv_by[p]))
    print("real aggregate: candidate A_%s %r, bar A_%s %r, d = %r" % (a.metric, c_agg, a.metric, b_agg, real))
    # built-in check of the fast path against metric_tools.family_scores on swapped prediction contents
    k = 0 if a.metric == "bleu" else 1
    checks = []
    for c in [None, 0, 1, 2, 3, 4]:
        sw = none if c is None else swaps_for(c)
        for p in PROPS:
            ref = []
            for side in (0, 1):
                vals = []
                for i, (gp, cand, bar) in enumerate(raw[p]):
                    langs, gold = m.load_cognate_file(gp)
                    preds = {}
                    for key in gold:
                        use_c = (side == 0) != (key.rsplit("-", 1)[0] in sw[p][i])
                        src = cand if use_c else bar
                        preds[key] = {lg: src.get(key, {}).get(lg, []) for lg in langs}
                    vals.append(m.family_scores(gp, preds)[k])
                ref.append(m.ltr_sum(vals) / len(vals))
            fast = [system(p, sw[p], 0), system(p, sw[p], 1)]
            ok = fast[0] == ref[0] and fast[1] == ref[1]
            checks.append({"control": c, "prop": p, "metric_tools": ref, "fast": fast, "bit_identical": ok})
            print("check control %s P %s: metric_tools %r / %r, fast %r / %r -> %s" % (
                c, p, ref[0], ref[1], fast[0], fast[1], "IDENTICAL" if ok else "DIFFERENT"), flush=True)
    all_ok = all(x["bit_identical"] for x in checks)
    if not all_ok:
        raise SystemExit("fast path differs from metric_tools.family_scores: stop")
    ds = []
    for c in range(a.controls):
        ds.append(d_of(swaps_for(c)))
    best = max(ds)
    import shlex
    cmd = shlex.join([sys.executable] + (["-I"] if sys.flags.isolated else []) + sys.argv)
    res = {"metric": a.metric, "prop": "AGG", "props": PROPS, "candidate": c_agg, "bar": b_agg, "real_d": real,
           "real": real, "command": cmd, "controls": a.controls, "best_control": best,
           "controls_ge_real": sum(1 for d in ds if d >= real), "real_beats_all_controls": real > best,
           "seed": a.seed, "families": fams, "candidate_by_prop": c_by, "bar_by_prop": b_by,
           "advantage_by_prop": adv_by, "fast_path_checks": checks, "fast_path_all_identical": all_ok,
           "d_controls": ds, "inputs": inputs}
    json.dump(res, open(a.out, "w"), indent=1)
    print("fast path bit-identical in every check: %s" % ("yes" if all_ok else "NO"))
    print("controls: %d" % a.controls)
    print("best_control: %r" % best)
    print("real: %r" % real)
    print("real_beats_all_controls: %s" % ("yes" if real > best else "no"))
    print("controls >= real: %d" % res["controls_ge_real"])
    print("command: %s" % cmd)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--metric", choices=("bleu", "bcfs"), required=True)
    ap.add_argument("--gold-dir", required=True)
    ap.add_argument("--cand-dir", required=True)
    ap.add_argument("--bar-dir", required=True)
    ap.add_argument("--prop")   # run 2026-10-18-1758: required unless --agg (checked below)
    ap.add_argument("--agg", action="store_true",
                    help="run 2026-10-18-1758: aggregate null over P 0.10..0.50 (G, C, B: P/FAM/... or FAM/...)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--controls", type=int, default=400)
    ap.add_argument("--seed", type=int, default=20261018)
    ap.add_argument("--fams")
    a = ap.parse_args()
    fams = a.fams.split(",") if a.fams else FAMS
    if a.agg:
        if a.prop:
            raise SystemExit("--agg fixes the proportions; do not pass --prop")
        run_agg(a, fams)
        return
    if not a.prop:
        raise SystemExit("single-P mode needs --prop")
    data = []
    for f in fams:
        cand = m.load_cognate_file(os.path.join(a.cand_dir, f, "result-%s.tsv" % a.prop))[1]
        bar = m.load_cognate_file(os.path.join(a.bar_dir, f, "result-%s.tsv" % a.prop))[1]
        data.append(prepare(gold_path(a.gold_dir, f, a.prop), cand, bar))

    def system(swapped_by_fam, side):
        return m.ltr_sum([fam_value(n, per, swapped_by_fam[i], a.metric, side)
                          for i, (n, order, per) in enumerate(data)]) / len(data)

    none = [set() for _ in data]
    c_real, b_real = system(none, 0), system(none, 1)
    real = c_real - b_real
    ds = []
    for c in range(a.controls):
        rng = random.Random(a.seed + c)
        sw = []
        for n, order, per in data:
            sw.append({s for s in order if rng.random() < 0.5})
        ds.append(system(sw, 0) - system(sw, 1))
    best = max(ds)
    import shlex
    cmd = shlex.join([sys.executable] + (["-I"] if sys.flags.isolated else []) + sys.argv)
    res = {"metric": a.metric, "prop": a.prop, "candidate": c_real, "bar": b_real, "real_d": real, "real": real,
           "command": cmd,
           "controls": a.controls, "best_control": best, "controls_ge_real": sum(1 for d in ds if d >= real),
           "real_beats_all_controls": real > best, "seed": a.seed, "families": fams}
    json.dump(res, open(a.out, "w"), indent=1)
    print("real: candidate %s %r, bar %r, d = %r" % (a.metric, c_real, b_real, real))
    print("controls: %d" % a.controls)
    print("best_control: %r" % best)
    print("real: %r" % real)
    print("real_beats_all_controls: %s" % ("yes" if real > best else "no"))
    print("controls >= real: %d" % res["controls_ge_real"])
    print("command: %s" % cmd)


if __name__ == "__main__":
    main()
