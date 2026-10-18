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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--metric", choices=("bleu", "bcfs"), required=True)
    ap.add_argument("--gold-dir", required=True)
    ap.add_argument("--cand-dir", required=True)
    ap.add_argument("--bar-dir", required=True)
    ap.add_argument("--prop", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--controls", type=int, default=400)
    ap.add_argument("--seed", type=int, default=20261018)
    ap.add_argument("--fams")
    a = ap.parse_args()
    fams = a.fams.split(",") if a.fams else FAMS
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
