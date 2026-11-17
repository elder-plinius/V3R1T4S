#!/usr/bin/env python3
"""Standalone checker for one new term of OEIS A389689 / A389690 (Python 3 standard library only).

Definition (OEIS entries, programs a389689_1.txt / a389690_2.txt): for a move set S with max S = n, values start at
position 0 (no move: loss, Sprague-Grundy value 0); a move s is allowed from p when s <= p. Win/lose: position p is a
win iff some allowed p - s is a loss. Sprague-Grundy: mex of the values at the allowed p - s. The window at p >= n-1 is
the n values at p-n+1..p; the eventual period is p - q at the first p whose window was already seen at q.
The term is the maximum period over all 2^(n-1) sets S of {1..n} that contain n.

Usage: check_term.py OBJECT_FILE [--quick]   (--quick skips the exhaustive pass)
Last line of output: PASS or FAIL."""
import sys, os
from multiprocessing import Pool

def period(S, mode):
    n = max(S); vals = []; seen = {}; p = 0
    while True:
        if mode == "wl":
            v = 0
            for s in S:
                if s <= p and vals[p - s] == 0:
                    v = 1; break
        else:
            opts = {vals[p - s] for s in S if s <= p}; v = 0
            while v in opts: v += 1
        vals.append(v)
        if p >= n - 1:
            w = tuple(vals[p - n + 1:p + 1])
            if w in seen: return p - seen[w]
            seen[w] = p
        p += 1

def chunk(args):
    mode, n, lo, hi = args
    h = {}
    for m in range(lo, hi):
        S = [i + 1 for i in range(n - 1) if m >> i & 1] + [n]
        q = period(S, mode); h[q] = h.get(q, 0) + 1
    return h

def fail(msg):
    print("FAIL: " + msg); print("FAIL"); sys.exit(1)

def main():
    path = sys.argv[1]; quick = "--quick" in sys.argv
    kv, hist, in_hist = {}, {}, False
    for line in open(path, encoding="ascii"):
        line = line.strip()
        if not line or line.startswith("#"): continue
        if in_hist:
            a, b = line.split(); hist[int(a)] = int(b); continue
        k, _, v = line.partition(" ")
        if k == "histogram":
            in_hist = True; kv[k] = int(v); continue
        kv[k] = v
    seq, mode, n, value = kv["sequence"], kv["mode"], int(kv["n"]), int(kv["value"])
    if (seq, mode) not in (("A389689", "wl"), ("A389690", "sg")): fail("unknown sequence/mode %s/%s" % (seq, mode))
    maxsets = [[int(x) for x in s.split()] for s in kv["maximising"].split(";")]
    if int(kv["sets"]) != 2 ** (n - 1): fail("sets line %s != 2^(n-1)" % kv["sets"])
    if len(hist) != kv["histogram"]: fail("histogram has %d lines, header says %d" % (len(hist), kv["histogram"]))
    if sum(hist.values()) != 2 ** (n - 1): fail("histogram counts sum to %d, not 2^(n-1)" % sum(hist.values()))
    if max(hist) != value: fail("largest period in the histogram %d != value %d" % (max(hist), value))
    if hist[value] != len(maxsets): fail("histogram count at the value %d != %d listed maximising sets" % (hist[value], len(maxsets)))
    for S in maxsets:
        if max(S) != n or len(set(S)) != len(S) or min(S) < 1: fail("bad set %s" % S)
        q = period(S, mode)
        if q != value: fail("set %s has period %d, not %d" % (S, q, value))
    print("object consistent: %s(%d) = %d, %d sets, %d distinct periods, maximising set(s) recomputed" % (seq, n, value, 2 ** (n - 1), len(hist)))
    if quick:
        print("PASS (quick: exhaustive pass skipped)"); return
    total = 2 ** (n - 1); K = 256; P = max(1, min(4, os.cpu_count() or 1))
    cuts = [total * i // K for i in range(K + 1)]
    with Pool(P) as pool:
        parts = pool.map(chunk, [(mode, n, cuts[i], cuts[i + 1]) for i in range(K)])
    full = {}
    for h in parts:
        for k, v in h.items(): full[k] = full.get(k, 0) + v
    if full != hist:
        diff = sorted(set(full) ^ set(hist)) or [k for k in sorted(full) if full[k] != hist.get(k)]
        fail("exhaustive histogram differs from the object (first differing period: %s)" % diff[:1])
    print("exhaustive pass over all %d sets (%d processes): histogram identical, maximum %d" % (total, P, max(full)))
    print("PASS")

if __name__ == "__main__":
    main()
