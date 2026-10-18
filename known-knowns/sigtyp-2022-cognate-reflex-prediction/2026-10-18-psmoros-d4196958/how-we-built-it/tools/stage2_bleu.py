#!/usr/bin/env python3
"""BLEU-MBR stage-2 combiner of PREREG.v2 (run 2026-10-18-0202). Main session, written after PREREG.v2.md was frozen.

For each item with candidate strings c_1..c_K (the entries' frozen predictions) output c_i with
  i = argmin_i sum_j w_j * (1 - BLEU(c_j -> c_i)) + 1e-7 * (3 - w_i) + 1e-9 * i,
BLEU(a -> b) = the official scorer's per-item bleu_score(a, b, n=4, trim=False), a in the gold slot (an empty b becomes
2*len(a) 'Ø' as in compare_words; an empty a contributes no risk). Weights in {0,1,2,3}^K minus the zero tuple, fit on all
10 val-P families by maximising the official mean BLEU (compare_words aggregation: per-language item mean, summed over the
languages that have items and divided by the number of languages in the gold header; statistics.mean over families).
The search ranks tuples with numpy; the 20 best are rescored exactly (left-to-right sums as in compare_words) and the
tie rule of PREREG.v2 picks among them (higher BLEU rounded to 12 decimals, smaller weight sum, smaller tuple).
Reads no surprise-test gold: test files are read only for their keys and masked language.

usage: STUB_MPL=1 <scorer python> -I tools/stage2_bleu.py --entries E.json --props 0.10 --val-test-root shared/val
           --gold-root main_only/val_gold --test-root data/view --out OUT
"""
import argparse
import contextlib
import io
import itertools
import json
import os
import statistics
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mplstub  # noqa: F401,E402
with contextlib.redirect_stdout(io.StringIO()):
    import sigtypst2022 as st  # noqa: E402

FAMS = ["bantubvd", "beidazihui", "birchallchapacuran", "bodtkhobwa", "bremerberta", "deepadungpalaung",
        "hillburmish", "kesslersignificance", "luangthongkumkaren", "wangbai"]


def bleu(a, b):
    if not " ".join(a):
        return None
    if not b:
        b = (2 * len(a)) * ["Ø"]
    return st.bleu_score(a, b, n=4, trim=False)


def items_of(gold_path):
    langs, _, g = st.load_cognate_file(gold_path)
    items = []
    for li, lg in enumerate(langs):
        for key in g:
            if lg in g[key] and " ".join(g[key][lg]):
                items.append((key, lg, li))
    return langs, g, items


def preds(path):
    return st.load_cognate_file(path)[2]


def family_arrays(p, fam, ents, a):
    langs, g, items = items_of(os.path.join(a.gold_root, p, fam, "solutions.tsv"))
    P = [preds(os.path.join(e["dir"], "val", p, fam, "result-%s.tsv" % p)) for e in ents]
    K = len(ents)
    n = len(items)
    G = np.zeros((n, K))
    R = np.zeros((n, K, K))      # R[n, j, i] = 1 - BLEU(c_j -> c_i), 0 if c_j empty
    for t, (key, lg, li) in enumerate(items):
        cands = [P[j].get(key, {}).get(lg, []) for j in range(K)]
        for i in range(K):
            G[t, i] = bleu(g[key][lg], cands[i])
        for j in range(K):
            for i in range(K):
                v = bleu(cands[j], cands[i])
                R[t, j, i] = 0.0 if v is None else 1.0 - v
    lang_idx = np.array([li for _, _, li in items])
    return dict(langs=langs, items=items, G=G, R=R, lang_idx=lang_idx, n_langs=len(langs))


def choose(R, w):
    K = len(w)
    adj = np.einsum("j,nji->ni", np.asarray(w, float), R) + 1e-7 * (3 - np.asarray(w, float))[None, :] + \
        1e-9 * np.arange(K)[None, :]
    return np.argmin(adj, axis=1)


def family_bleu_exact(fa, ch):
    per = {}
    for t, (key, lg, li) in enumerate(fa["items"]):
        per.setdefault(li, []).append(fa["G"][t, ch[t]])
    tot = 0.0
    for li in sorted(per):                       # languages in header order, as compare_words loops
        s = 0.0
        for v in per[li]:
            s += v
        tot += s / len(per[li])
    return tot / fa["n_langs"]


def write_result(test_path, out_path, choice_strings):
    langs, _, test = st.load_cognate_file(test_path)
    lines = ["COGID\t" + "\t".join(langs) + "\n"]
    for k, row in test.items():
        masked = [lg for lg in langs if row.get(lg) == ["?"]]
        assert len(masked) == 1, (test_path, k)
        cell = {masked[0]: choice_strings[k]}
        lines.append(k + "".join("\t" + " ".join(cell.get(lg, [])) for lg in langs) + "\n")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("".join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--entries", required=True)
    ap.add_argument("--props", required=True)
    ap.add_argument("--val-test-root", required=True)
    ap.add_argument("--gold-root", required=True)
    ap.add_argument("--test-root", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    ents = json.load(open(a.entries))
    K = len(ents)
    tuples = np.array([t for t in itertools.product(range(4), repeat=K) if any(t)], dtype=float)
    fit = {}
    for p in a.props.split(","):
        t0 = time.time()
        fas = {f: family_arrays(p, f, ents, a) for f in FAMS}
        print("%s val arrays %.1fs, items %d" % (p, time.time() - t0, sum(len(x["items"]) for x in fas.values())), flush=True)
        score = np.zeros(len(tuples))
        for f, fa in fas.items():
            R, G, li = fa["R"], fa["G"], fa["lang_idx"]
            nl = fa["n_langs"]
            cnt = np.bincount(li, minlength=nl).astype(float)
            fam_s = np.zeros(len(tuples))
            for c0 in range(0, len(tuples), 256):
                W = tuples[c0:c0 + 256]
                adj = np.einsum("tj,nji->tni", W, R) + 1e-7 * (3 - W)[:, None, :] + 1e-9 * np.arange(K)[None, None, :]
                ch = np.argmin(adj, axis=2)                       # t x n
                g = np.take_along_axis(np.broadcast_to(G, (len(W),) + G.shape), ch[:, :, None], axis=2)[:, :, 0]
                sums = np.zeros((len(W), nl))
                for L in range(nl):
                    m = li == L
                    if m.any():
                        sums[:, L] = g[:, m].sum(axis=1) / cnt[L]
                fam_s[c0:c0 + 256] = sums.sum(axis=1) / nl
            score += fam_s
        score /= len(FAMS)
        top = np.argsort(-score)[:20]
        exact = []
        for ti in top:
            w = tuples[ti]
            vals = [family_bleu_exact(fas[f], choose(fas[f]["R"], w)) for f in FAMS]
            exact.append((statistics.mean(vals), [int(x) for x in w]))
        exact.sort(key=lambda x: (-round(x[0], 12), sum(x[1]), x[1]))
        best_v, best_w = exact[0]
        print("%s weights %s val mean BLEU (in-sample) %r; runner-up %s %r" % (p, best_w, best_v, exact[1][1], exact[1][0]),
              flush=True)
        # write val (in-sample) and test predictions with the chosen weights
        for f in FAMS:
            fa = fas[f]
            ch = choose(fa["R"], best_w)
            P = [preds(os.path.join(e["dir"], "val", p, f, "result-%s.tsv" % p)) for e in ents]
            cs = {}
            for t, (key, lg, li) in enumerate(fa["items"]):
                cs[key] = P[ch[t]][key][lg]
            write_result(os.path.join(a.val_test_root, p, f, "test.tsv"), os.path.join(a.out, "val", p, f, "result-%s.tsv" % p), cs)
            tp = os.path.join(a.test_root, "surprise", f, "test-%s.tsv" % p)
            langs, _, test = st.load_cognate_file(tp)
            TP = [preds(os.path.join(e["dir"], "test", p, f, "result-%s.tsv" % p)) for e in ents]
            cs = {}
            for k, row in test.items():
                lg = [x for x in langs if row.get(x) == ["?"]][0]
                cands = [TP[j][k][lg] for j in range(K)]
                Rm = np.zeros((1, K, K))
                for j in range(K):
                    for i in range(K):
                        v = bleu(cands[j], cands[i])
                        Rm[0, j, i] = 0.0 if v is None else 1.0 - v
                cs[k] = cands[int(choose(Rm, best_w)[0])]
            write_result(tp, os.path.join(a.out, "test", p, f, "result-%s.tsv" % p), cs)
        fit[p] = {"weights_all10": best_w, "insample_val_mean_bleu": best_v, "top20_exact": exact,
                  "entries": [e["name"] for e in ents], "seconds": time.time() - t0}
        print("%s done %.1fs" % (p, time.time() - t0), flush=True)
    with open(os.path.join(a.out, "combiner_fit.json"), "w") as f:
        json.dump(fit, f, indent=1)


if __name__ == "__main__":
    main()
