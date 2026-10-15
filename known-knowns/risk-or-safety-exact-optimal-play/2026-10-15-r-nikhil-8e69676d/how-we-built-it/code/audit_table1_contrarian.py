#!/usr/bin/env python3
"""audit_table1.py -- CONTRARIAN lens: audit Jehn's Table 1 and OEIS A394776 against exact optimal actions.

Inputs: code/needs_table_N30.json (from needs_minimax_solver.py), data/b394776.txt, data/arxiv_2603.01002.txt.
1. Re-derives the A394776 index encoding n = (j-1)^2 + i (i < j), n = i^2 - j + 1 (i >= j); checks it is a bijection
   [1,20]^2 -> [1,400] and checks the OEIS example a(3) = 2 at i = j = 2.
2. Parses Table 1 out of the pdftotext of the paper and diffs it against the b-file (transcription check).
3. Diffs the exact optimal on-path toss counts (heads collected before banking from (0,i,j)) against the b-file for
   all 1 <= i, j <= 20, printing exact continue/stop values and tie status at every mismatch.
4. Checks the Section 5 rules (j = 1: all in at EVERY a; i = 1: one toss) exactly.
5. Reports the smallest relative margins between the optimal and the runner-up plan (near-tie scan).
"""
import json, os, re
from fractions import Fraction as Fr

ATT = "."  # package copy: the run-folder path constant was replaced by "." for publication
DATA = "."  # package copy: the run-folder path constant was replaced by "." for publication


def F(s):
    a, b = s.split("/")
    return Fr(int(a), int(b))


def enc(i, j):
    return (j - 1) ** 2 + i if i < j else i * i - j + 1


def main():
    T = json.load(open(os.path.join(ATT, "code", "needs_table_N30.json")))
    P = {tuple(map(int, k.split(","))): F(v) for k, v in T["P"].items()}
    ACT = {tuple(map(int, k.split(","))): (F(c), F(s)) for k, (c, s) in T["act"].items()}
    PLANS = {tuple(map(int, k.split(","))): v for k, v in T["plans"].items()}

    # ---- 1. encoding
    seen = {}
    for i in range(1, 21):
        for j in range(1, 21):
            seen.setdefault(enc(i, j), []).append((i, j))
    bij = sorted(seen) == list(range(1, 401)) and all(len(v) == 1 for v in seen.values())
    print("encoding is a bijection [1,20]^2 -> [1,400]:", bij)
    dec = {k: v[0] for k, v in seen.items()}
    b = {}
    for line in open(os.path.join(DATA, "b394776.txt")):
        line = line.strip()
        if line and not line.startswith("#"):
            k, v = line.split()
            b[int(k)] = int(v)
    print("b394776 entries:", len(b), "range", min(b), max(b))
    print("OEIS example a(3)=2 at i=j=2: enc(2,2)=%d, b-file a(%d)=%d" % (enc(2, 2), enc(2, 2), b[enc(2, 2)]))
    print("first shells decoded:", [(k, dec[k], b[k]) for k in range(1, 17)])

    # ---- 2. parse Table 1 from the pdftotext
    txt = open(os.path.join(DATA, "arxiv_2603.01002.txt"), encoding="utf-8", errors="replace").read()
    start = txt.index("Points Opponent needs")
    end = txt.index("Table 1:")
    block = txt[start:end]
    table1 = {}
    for line in block.splitlines():
        toks = line.split()
        if not toks or not all(t.isdigit() for t in toks):
            continue
        if len(toks) == 20 and int(toks[0]) in range(2, 21):
            i = int(toks[0])
            if toks[:3] == ["2", "3", "4"] and i == 2 and len(set(toks)) == 20:
                continue  # header row "2 3 ... 20"
            for jj, t in zip(range(2, 21), toks[1:]):
                table1[(i, jj)] = int(t)
    print("Table 1 parsed cells:", len(table1), "(expected 19*19 = 361)")
    tdiff = [(i, j, table1[(i, j)], b[enc(i, j)]) for (i, j) in sorted(table1) if table1[(i, j)] != b[enc(i, j)]]
    print("Table 1 (paper text) vs b394776 differences:", len(tdiff), tdiff[:20])

    # ---- 3. exact on-path toss counts vs b-file
    mism = []
    for i in range(1, 21):
        for j in range(1, 21):
            ks = PLANS[(i, j)]
            pub = b[enc(i, j)]
            if ks != [pub]:
                mism.append((i, j, ks, pub))
    print("exact optimal toss count vs b394776 over 1<=i,j<=20: %d mismatches" % len(mism))
    for (i, j, ks, pub) in mism:
        print("  MISMATCH i=%d j=%d exact optimal plan(s) %s, published %d" % (i, j, ks, pub))
        for a in range(1, i):
            c, s = ACT[(a, i, j)]
            print("     a=%d continue=%s stop=%s  %s  (cont-stop=%.3e)" % (
                a, c, s, "TIE" if c == s else ("continue" if c > s else "stop"), float(c - s)))
    # also against Table 1 directly
    mt = [(i, j, PLANS[(i, j)], table1[(i, j)]) for (i, j) in sorted(table1) if PLANS[(i, j)] != [table1[(i, j)]]]
    print("exact optimal toss count vs paper Table 1 (2<=i,j<=20): %d mismatches %s" % (len(mt), mt[:20]))

    # ---- 4. Section 5 rules, all positions (on- and off-path), i, j <= 30
    viol_allin = []
    for i in range(2, 31):
        for a in range(1, i):
            c, s = ACT[(a, i, 1)]
            if not c > s:
                viol_allin.append((a, i, 1, c, s))
    print("j=1 (opponent needs 1): positions (a,i,1), 1<=a<i<=30, where continue is NOT strictly better: %d %s"
          % (len(viol_allin), viol_allin[:5]))
    print("i=1 (mover needs 1): plan sets", sorted(set(tuple(PLANS[(1, j)]) for j in range(1, 31))))
    print("j=1 plan sets equal [i] for all i<=30:", all(PLANS[(i, 1)] == [i] for i in range(1, 31)))

    # ---- 5. near-tie scan over plans: margin between best and runner-up plan at (0,i,j), i,j <= 20 and <= 30
    def plan_values(i, j):
        y = P[(0, j, i)]
        vals = []
        for k in range(1, i + 1):
            p = Fr(1, 2 ** k)
            s = Fr(1) if k == i else 1 - P[(0, j, i - k)]
            vals.append((k, (1 - p) * (1 - y) + p * s))
        return vals
    rows = []
    for i in range(2, 31):
        for j in range(1, 31):
            vals = sorted(plan_values(i, j), key=lambda t: -t[1])
            (k1, v1), (k2, v2) = vals[0], vals[1]
            assert v1 == P[(0, i, j)] and [k1] == PLANS[(i, j)]
            rows.append((float((v1 - v2) / v1), i, j, k1, k2))
    rows.sort()
    print("smallest relative margins best-vs-runner-up plan at (0,i,j), 2<=i<=30, 1<=j<=30:")
    for r in rows[:12]:
        print("   rel.margin=%.3e  i=%d j=%d best k=%d runner-up k=%d %s" % (r[0], r[1], r[2], r[3], r[4],
              "(inside Table 1 range)" if r[1] <= 20 and r[2] <= 20 else ""))
    rows20 = [r for r in rows if r[1] <= 20 and r[2] <= 20 and r[2] >= 2]
    print("smallest margin inside 2<=i,j<=20: %.3e at i=%d j=%d" % (rows20[0][0], rows20[0][1], rows20[0][2]))
    # smallest |cont-stop| over ALL positions (a,i,j), i,j<=30 (action-level near ties, on- or off-path)
    acts = sorted((abs(float(c - s)), a, i, j) for (a, i, j), (c, s) in ACT.items())
    print("smallest |continue-stop| over all 1<=a<i<=30, j<=30:", [("%.3e" % t[0],) + t[1:] for t in acts[:6]])
    # extended table i,j <= 30 for the record
    print("exact toss-count table, rows i=2..30 (mover needs), columns j=2..30 (opponent needs):")
    for i in range(2, 31):
        print("  i=%2d: %s" % (i, " ".join("%2d" % PLANS[(i, j)][0] for j in range(2, 31))))


if __name__ == "__main__":
    main()
