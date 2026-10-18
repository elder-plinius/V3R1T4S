#!/usr/bin/env python3
"""Stage-2 combiner of PREREG rule 9 (run 2026-10-18-0104). Written by the tools engineer of this run (Opus 5.5) while
the lenses were running, before any system of this run was frozen and before any surprise-test gold was read.

This is run 2026-10-17-1806's attempts/combiner/frozen/PRIMARY/code/combine.py with IDENTICAL per-item logic:
  per-item minimum-Bayes-risk choice under the official item NED over K entries' predictions:
  for an item with candidate strings c_1..c_K (one per entry), output argmin_i sum_j w_j * NED(c_j -> c_i),
  where NED(a -> b) is exactly the scorer's per-item value with a in the gold slot and b in the prediction slot
  (lingpy nw_align as imported by sigtypst2022; an empty prediction becomes 2*len(a) 'Ø', as in compare_words);
  an empty candidate carries no information as pseudo-gold (its row of the matrix stays 0).
  Ties: higher own weight first, then the entry order of --entries (1e-7 * (3 - w_i) + 1e-9 * i, as in combine.py).
  Weights w_j in {0,1,2,3}, all 4**K - 1 non-zero tuples, fit per proportion on val (val gold built from training
  files only). Val predictions are leave-one-family-out (weights fit on the other 9 val families); test predictions
  use the weights fit on all 10 val families. Weight-tuple ties: lower mean NED (rounded to 12 decimals), then
  smaller weight sum, then lexicographically smaller tuple. Each item's output depends only on that item's K
  candidates and the weights (row isolation by construction). Deterministic. Reads no surprise-test gold.

Changed against combine.py (and nothing else):
  - the entry list comes from --entries FILE: JSON list of {"name": str, "dir": ROLE folder holding
    val/<P>/<fam>/result-<P>.tsv and test/<P>/<fam>/result-<P>.tsv}, in the order that the tie rule uses;
  - paths: --val-test-root (<P>/<fam>/test.tsv, masked val rows), --gold-map (JSON {P: folder holding
    <P>/<fam>/solutions.tsv}), --test-root (surprise/<fam>/test-<P>.tsv), --out;
  - mplstub is imported from this script's own folder;
  - speed: the K x K item-NED matrices are computed per family in --procs worker processes (pure function of the
    candidate strings, so the values are those of combine.py); the weight search computes the per-item choice for
    all weight tuples at once with one matrix product per chunk (items whose K x K matrix is all zero, i.e. all K
    candidates identical or all empty, get combine.py's all-zero-row choice directly; their gold-NED row is constant
    over the candidates, so F is unaffected either way). Exactness guard: for every tuple whose
    vectorised scores have, on any item, a gap below 1e-11 between the best and second-best adjusted score (float
    rounding of the two summation orders differs by < 1e-13), that tuple's choices are recomputed with combine.py's
    own choose() (np.einsum). The family value of each tuple is then combine.py's own
    float(np.dot(wr, G[np.arange(R), ch])), so F (and therefore every weight choice) is bit-identical to combine.py.
    --verify-reference additionally runs combine.py's original per-tuple loop and asserts bit-identical choices and
    F for every tuple and family. Written predictions (LOFO val, test) always use combine.py's choose();
  - added outputs: wall times, and the official compare_words scores of the written LOFO val files (family mean =
    statistics.mean over the 10 families, builtin sum as tools/val_scorer.py does) as lofo_val_scorer_total
    [ED, NED, BCFS, BLEU]; combiner_fit.json is merged with an existing one (one key per proportion).

usage: STUB_MPL=1 <scorer venv python> -I tools/stage2.py --entries E.json --val-test-root VAL --gold-map G.json
           --test-root VIEW --out OUT [--props 0.10,...] [--procs 2] [--verify-reference]
"""
import argparse
import concurrent.futures as cf
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

PROPS = ["0.10", "0.20", "0.30", "0.40", "0.50"]
FAMS = ["bantubvd", "beidazihui", "birchallchapacuran", "bodtkhobwa", "bremerberta", "deepadungpalaung",
        "hillburmish", "kesslersignificance", "luangthongkumkaren", "wangbai"]
LEVELS = (0, 1, 2, 3)
GUARD = 1e-11

_cache = {}


def ned(a, b):
    """Scorer's per-item normalized edit distance with a in the gold slot, b in the prediction slot."""
    key = (a, b)
    if key in _cache:
        return _cache[key]
    A = list(a)
    B = list(b) if b else (2 * len(A)) * ["Ø"]
    almA, almB, _ = st.nw_align(A, B)
    score = 0
    for x, y in zip(almA, almB):
        if x == y and x not in "Ø?-":
            pass
        elif x != y:
            score += 1
    v = score / len(almA)
    _cache[key] = v
    return v


def masked(row, langs):
    for lg in langs:
        if row.get(lg) == ["?"]:
            return lg
    raise SystemExit("no masked language")


def load(path):
    with contextlib.redirect_stdout(io.StringIO()):
        langs, _, data = st.load_cognate_file(path)
    return langs, data


def items(tpath):
    langs, data = load(tpath)
    keys = list(data)   # file order
    return langs, [(k, masked(data[k], langs)) for k in keys]


def candidates(entries, mode, p, fam, its):
    cands = []
    for e in entries:
        _, res = load(os.path.join(e["dir"], mode, p, fam, "result-%s.tsv" % p))
        cands.append([tuple(res.get(k, {}).get(lg, [])) for k, lg in its])
    return list(zip(*cands))   # per item: tuple of K candidate tuples


def matrices(cands, K):
    D = np.zeros((len(cands), K, K))
    for r, cs in enumerate(cands):
        for j in range(K):
            if not cs[j]:
                continue   # an empty candidate carries no information as pseudo-gold
            for i in range(K):
                if i != j:
                    D[r, j, i] = ned(cs[j], cs[i])
    return D


def choose(D, w):
    """combine.py's choose(), verbatim (K from the matrix instead of the global entry list)."""
    K = D.shape[1]
    S = np.einsum("rji,j->ri", D, w)
    adj = S + 1e-7 * (max(LEVELS) - w)[None, :] + 1e-9 * np.arange(K)[None, :]
    return np.argmin(adj, axis=1)


def val_test_path(root, p, fam):
    return os.path.join(root, p, fam, "test.tsv")


def family_job(args):
    """Worker: everything per family that depends only on files (no weights). Pure function of its inputs."""
    entries, p, fam, val_root, gold_root, test_root = args
    t0 = time.time()
    K = len(entries)
    langs, its = items(val_test_path(val_root, p, fam))
    cands = candidates(entries, "val", p, fam, its)
    glangs, gold = load(os.path.join(gold_root, p, fam, "solutions.tsv"))
    G = np.array([[ned(tuple(gold[k][lg]), c) for c in cs] for (k, lg), cs in zip(its, cands)])
    # exact family-mean weights: compare_words averages items per gold language, sums languages and
    # divides by the number of languages in the gold header
    n_lang = {}
    for k, lg in its:
        n_lang[lg] = n_lang.get(lg, 0) + 1
    wr = np.array([1.0 / (n_lang[lg] * len(glangs)) for k, lg in its])
    D = matrices(cands, K)
    tlangs, tits = items(os.path.join(test_root, "surprise", fam, "test-%s.tsv" % p))
    tcands = candidates(entries, "test", p, fam, tits)
    TD = matrices(tcands, K)
    empty_val = sum(1 for cs in cands for c in cs if not c)
    empty_test = sum(1 for cs in tcands for c in cs if not c)
    return {"fam": fam, "val": (langs, its, cands, D, G, wr), "test": (tlangs, tits, tcands, TD),
            "empty_val": empty_val, "empty_test": empty_test, "seconds": time.time() - t0}


def search_family(D, G, wr, grid_arr, chunk_elems=8_000_000, ref_chs=None):
    """F[g] = combine.py's family value for weight tuple g, with the exactness guard described in the docstring.
    Items whose matrix is all zero (all K candidates identical, or all empty) get combine.py's choice for an all-zero
    score row (the tie rule alone: argmin of 1e-7 * (3 - w) + 1e-9 * i); their G row is constant anyway.
    ref_chs (verify mode): combine.py's choices per tuple; returns the number of tuples whose choices differ."""
    R, K = G.shape
    n_g = grid_arr.shape[0]
    act = np.flatnonzero(np.any(D.reshape(R, K * K) != 0, axis=1))
    Ra = len(act)
    Da = D[act]
    MT = np.ascontiguousarray(Da.reshape(Ra, K * K).T.reshape(K, K, Ra).transpose(0, 2, 1).reshape(K, Ra * K))
    # MT[j, a*K + i] = D[act[a], j, i]
    F = np.empty(n_g)
    rows = np.arange(R)
    fallback = 0
    n_diff = 0
    chunk = max(1, chunk_elems // max(1, Ra * K))
    tie_idx = 1e-9 * np.arange(K)
    for s in range(0, n_g, chunk):
        Wc = grid_arr[s:s + chunk]                                   # (n, K)
        n = Wc.shape[0]
        t1 = 1e-7 * (max(LEVELS) - Wc)                               # (n, K)
        zero_choice = np.argmin(t1 + tie_idx[None, :], axis=1)       # combine.py's choice on an all-zero row
        if Ra:
            adj = (Wc @ MT).reshape(n, Ra, K)                        # S[g, a, i]
            adj += t1[:, None, :]
            adj += tie_idx[None, None, :]
            ch = adj.argmin(axis=2)                                  # (n, Ra)
            if K > 1:
                gap = adj - np.take_along_axis(adj, ch[:, :, None], 2)
                np.put_along_axis(gap, ch[:, :, None], np.inf, 2)
                unsafe = (gap.min(axis=2) < GUARD).any(axis=1)
                del gap
            else:
                unsafe = np.zeros(n, dtype=bool)
            del adj
        else:
            unsafe = np.zeros(n, dtype=bool)
        C = np.repeat(zero_choice[:, None], R, axis=1)               # (n, R)
        if Ra:
            C[:, act] = ch
        for t in range(n):
            if unsafe[t]:
                c = choose(D, grid_arr[s + t])
                fallback += 1
            else:
                c = C[t]
            if ref_chs is not None and not np.array_equal(c, ref_chs[s + t]):
                n_diff += 1
            F[s + t] = float(np.dot(wr, G[rows, c]))
    return F, fallback, n_diff


def reference_family(D, G, wr, grid):
    """combine.py's original loop for one family (used by --verify-reference)."""
    out = np.zeros(len(grid))
    chs = []
    for gi, w in enumerate(grid):
        ch = choose(D, w)
        out[gi] = float(np.dot(wr, G[np.arange(len(ch)), ch]))
        chs.append(ch)
    return out, chs


def write(out, mode, p, fam, langs, its, preds):
    d = os.path.join(out, mode, p, fam)
    os.makedirs(d, exist_ok=True)
    data = {k: {lg: list(pr)} for (k, lg), pr in zip(its, preds)}
    with open(os.path.join(d, "result-%s.tsv" % p), "w") as f:
        f.write("COGID\t" + "\t".join(langs) + "\n")
        for k, v in data.items():
            f.write("{0}".format(k))
            for lg in langs:
                f.write("\t" + " ".join(v.get(lg, [])))
            f.write("\n")


def main():
    ap = argparse.ArgumentParser(description="Stage-2 MBR combiner (combine.py of run 2026-10-17-1806, generalised)")
    ap.add_argument("--entries", required=True, help="JSON list of {name, dir} in tie-rule order")
    ap.add_argument("--val-test-root", required=True, help="folder with <P>/<fam>/test.tsv (masked val rows)")
    ap.add_argument("--gold-map", required=True, help="JSON {P: folder holding <P>/<fam>/solutions.tsv}")
    ap.add_argument("--test-root", required=True, help="folder with surprise/<fam>/test-<P>.tsv (data/view)")
    ap.add_argument("--props", default=",".join(PROPS))
    ap.add_argument("--out", required=True)
    ap.add_argument("--procs", type=int, default=2, help="worker processes for the item-NED matrices")
    ap.add_argument("--verify-reference", action="store_true",
                    help="also run combine.py's per-tuple loop and require bit-identical choices and F")
    a = ap.parse_args()
    T0 = time.time()
    with open(a.entries) as f:
        entries = json.load(f)
    if not entries or any(set(e) < {"name", "dir"} for e in entries):
        raise SystemExit("--entries: need a non-empty list of {name, dir}")
    entries = [{"name": e["name"], "dir": os.path.abspath(e["dir"])} for e in entries]
    names = [e["name"] for e in entries]
    if len(set(names)) != len(names):
        raise SystemExit("--entries: duplicate names")
    with open(a.gold_map) as f:
        gold_map = {k: os.path.abspath(v) for k, v in json.load(f).items()}
    out = os.path.abspath(a.out)
    val_root, test_root = os.path.abspath(a.val_test_root), os.path.abspath(a.test_root)
    K = len(entries)
    grid = [np.array(t, dtype=float) for t in itertools.product(LEVELS, repeat=K) if any(t)]
    grid_arr = np.array(grid)
    print("stage2: K=%d entries %s; %d weight tuples; out %s" % (K, names, len(grid), out), flush=True)
    report = {}
    for p in a.props.split(","):
        if p not in gold_map:
            raise SystemExit("--gold-map has no folder for %s" % p)
        tp = time.time()
        jobs = [(entries, p, fam, val_root, gold_map[p], test_root) for fam in FAMS]
        if a.procs > 1:
            with cf.ProcessPoolExecutor(max_workers=a.procs) as ex:
                res = list(ex.map(family_job, jobs))
        else:
            res = [family_job(j) for j in jobs]
        res = {r["fam"]: r for r in res}
        t_mat = time.time() - tp
        print("%s matrices: %.1fs (sum of worker times %.1fs); empty candidates val %d test %d" % (
            p, t_mat, sum(r["seconds"] for r in res.values()), sum(r["empty_val"] for r in res.values()),
            sum(r["empty_test"] for r in res.values())), flush=True)
        fam_rows = {fam: res[fam]["val"] for fam in FAMS}
        # family NED for every weight tuple
        ts = time.time()
        F = np.zeros((len(grid), len(FAMS)))
        n_fb = 0
        for fi, fam in enumerate(FAMS):
            _, _, _, D, G, wr = fam_rows[fam]
            F[:, fi], fb, _ = search_family(D, G, wr, grid_arr)
            n_fb += fb
        t_search = time.time() - ts
        print("%s weight search (vectorised): %.1fs, %d tuple-family pairs recomputed by the exactness guard" % (
            p, t_search, n_fb), flush=True)
        verify = None
        if a.verify_reference:
            tv = time.time()
            Fref = np.zeros((len(grid), len(FAMS)))
            n_ch = 0
            for fi, fam in enumerate(FAMS):
                _, _, _, D, G, wr = fam_rows[fam]
                Fref[:, fi], chs = reference_family(D, G, wr, grid)
                _, _, nd = search_family(D, G, wr, grid_arr, ref_chs=chs)
                n_ch += nd
                del chs
            identical = bool(np.array_equal(F, Fref))
            verify = {"F_bit_identical": identical, "tuples_with_different_choices": n_ch,
                      "seconds": time.time() - tv}
            print("%s verify-reference (combine.py per-tuple loop): F bit-identical %s; tuple-family pairs with "
                  "different item choices %d (%.1fs)" % (p, identical, n_ch, verify["seconds"]), flush=True)
            if not identical or n_ch:
                raise SystemExit("VERIFY FAILED at %s" % p)
        wsum = np.array([w.sum() for w in grid])

        def best(cols):
            m = F[:, cols].mean(axis=1)
            order = sorted(range(len(grid)), key=lambda g: (round(m[g], 12), wsum[g], tuple(grid[g])))
            return order[0], m[order[0]]

        single = {names[j]: float(F[[gi for gi, w in enumerate(grid) if w.sum() == 1 and w[j] == 1][0]].mean())
                  for j in range(K)}
        lofo = {}
        for fi, fam in enumerate(FAMS):
            g, _ = best([c for c in range(len(FAMS)) if c != fi])
            lofo[fam] = (tuple(int(x) for x in grid[g]), float(F[g, fi]))
            langs, its, cands, D, G, wr = fam_rows[fam]
            ch = choose(D, grid[g])
            write(out, "val", p, fam, langs, its, [cands[r][ch[r]] for r in range(len(its))])
        gall, mall = best(list(range(len(FAMS))))
        wall = grid[gall]
        for fam in FAMS:
            langs, its, cands, TD = res[fam]["test"]
            ch = choose(TD, wall)
            write(out, "test", p, fam, langs, its, [cands[r][ch[r]] for r in range(len(its))])
        # official scorer on the written LOFO val files (as tools/val_scorer.py: builtin sum, statistics.mean)
        fam_sc = {}
        for fam in FAMS:
            with contextlib.redirect_stdout(io.StringIO()):
                fam_sc[fam] = list(st.compare_words(os.path.join(gold_map[p], p, fam, "solutions.tsv"),
                                                    os.path.join(out, "val", p, fam, "result-%s.tsv" % p),
                                                    report=False)[-1][1:])
        sc_tot = [statistics.mean([fam_sc[f][i] for f in FAMS]) for i in range(4)]
        report[p] = {"weights_all10": [int(x) for x in wall], "insample_mean_all10": float(mall),
                     "lofo_val_mean": float(np.mean([v[1] for v in lofo.values()])),
                     "lofo_weights": {f: list(v[0]) for f, v in lofo.items()},
                     "single_entry_val_mean": single, "entries": names,
                     "entry_dirs": [e["dir"] for e in entries],
                     "lofo_val_scorer_total": sc_tot, "lofo_val_scorer_families": fam_sc,
                     "guard_recomputed_tuple_family_pairs": n_fb, "verify_reference": verify,
                     "seconds": {"matrices": t_mat, "search": t_search, "total_this_prop": time.time() - tp}}
        print(p, "weights(all 10)", report[p]["weights_all10"], "in-sample %.6f" % mall,
              "LOFO %.6f" % report[p]["lofo_val_mean"], flush=True)
        print("%s LOFO val mean (combine.py value) %r; official compare_words on the written val files: "
              "NED %r (ED %r BCFS %r BLEU %r)" % (p, report[p]["lofo_val_mean"], sc_tot[1], sc_tot[0], sc_tot[2],
                                                    sc_tot[3]), flush=True)
        for e, v in single.items():
            print("   single %-30s %.6f" % (e, v))
        print("%s wall time %.1fs" % (p, time.time() - tp), flush=True)
    os.makedirs(out, exist_ok=True)
    jpath = os.path.join(out, "combiner_fit.json")
    old = {}
    if os.path.isfile(jpath):
        with open(jpath) as f:
            old = json.load(f)
    old.update(report)
    with open(jpath, "w") as f:
        json.dump(old, f, indent=1)
    print("stage2 done, total wall time %.1fs" % (time.time() - T0), flush=True)


if __name__ == "__main__":
    main()
