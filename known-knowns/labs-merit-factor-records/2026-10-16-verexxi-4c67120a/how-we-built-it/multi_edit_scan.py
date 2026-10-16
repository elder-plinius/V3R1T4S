#!/usr/bin/env python3
"""Scan k-element end operators (trim up to KT elements in total from the two ends of a longer published sequence, or
append up to KA elements in total to a shorter one) for lengths where the result beats the baseline and beats every
one/two-element edit. Exact energies (numpy int64, cross-checked with labs_energy for each reported best)."""
import csv, sys, itertools
import numpy as np
sys.path.insert(0, sys.argv[1] + "/tools"); from labs_energy import energy, to_pm
KT, KA = 8, 3
rows = list(csv.DictReader(open(sys.argv[1] + "/baseline/rows.tsv"), delimiter="\t"))
base = {int(r["L"]): int(r["baseline_E"]) for r in csv.DictReader(open(sys.argv[1] + "/baseline/baseline.tsv"), delimiter="\t")}
gap = {int(r["L"]): int(r["best_edit_E"]) for r in csv.DictReader(open(sys.argv[1] + "/baseline/gaps.tsv"), delimiter="\t")}
seqs = {}
for r in rows:
    if r["seq"] and "?" not in r["kind"]: seqs.setdefault(int(r["L"]), set()).add(r["seq"])
def E(b):
    s = np.array([1 if c == "0" else -1 for c in b], dtype=np.int64); return int((np.correlate(s, s, "full")[len(s):] ** 2).sum())
best = {}
for M, ss in seqs.items():
    for s in ss:
        for k in range(3, KT + 1):          # trims
            L = M - k
            if L in base:
                for i in range(k + 1):
                    e = E(s[i:M - (k - i)])
                    if e < best.get(L, (10 ** 9,))[0]: best[L] = (e, s[i:M - (k - i)], f"trim {i} start {k - i} end of L={M}")
        for k in range(3, KA + 1):          # appends
            L = M + k
            if L in base:
                for a in range(k + 1):
                    for bits in itertools.product("01", repeat=k):
                        b = "".join(bits); t = b[:a] + s + b[a:]
                        e = E(t)
                        if e < best.get(L, (10 ** 9,))[0]: best[L] = (e, t, f"prepend '{b[:a]}' append '{b[a:]}' to L={M}")
print("# L baseline best_1or2_edit best_multi gap_vs_baseline how")
for L in sorted(best):
    e, t, how = best[L]
    if e < base[L] and e < gap.get(L, 10 ** 9):
        assert energy(to_pm(t)) == e
        print(L, base[L], gap.get(L, "-"), e, base[L] - e, how)
