#!/usr/bin/env python3
"""Independent period checker for an elementary CA on a ring (standard library only).

Usage: check_period.py --rule R --n N --witness 0xHEX --period P
   or: check_period.py --file witness_implX.txt   (lines rule=, n=, max_period=, witness=)

Wolfram rule-number order: cell 0 = least-significant bit; neighbourhood
(L, C, R) = cells (i-1, i, i+1) cyclic; idx = (L<<2)|(C<<1)|R; next bit =
(rule >> idx) & 1. The step is computed bit-parallel from the rule's minterms,
derived only from that definition.

Passes only if the witness returns to itself after exactly P steps and not
after P/q steps for any prime q dividing P (so P is the least period).
Prints PASS or FAIL as the last line; exit status 0 only on PASS.
"""
import argparse, sys, time


def make_step(rule, n):
    mask = (1 << n) - 1
    terms = [idx for idx in range(8) if (rule >> idx) & 1]

    def step(s):
        L = ((s << 1) | (s >> (n - 1))) & mask   # bit i holds cell i-1
        R = ((s >> 1) | (s << (n - 1))) & mask   # bit i holds cell i+1
        C = s
        nL, nC, nR = L ^ mask, C ^ mask, R ^ mask
        out = 0
        for idx in terms:
            out |= ((L if idx & 4 else nL) & (C if idx & 2 else nC) & (R if idx & 1 else nR))
        return out
    return step


def slow_step(rule, n, s):
    out = 0
    for i in range(n):
        L = (s >> ((i - 1) % n)) & 1
        C = (s >> i) & 1
        R = (s >> ((i + 1) % n)) & 1
        if (rule >> ((L << 2) | (C << 1) | R)) & 1:
            out |= 1 << i
    return out


def prime_factors(p):
    fs, d = [], 2
    while d * d <= p:
        if p % d == 0:
            fs.append(d)
            while p % d == 0:
                p //= d
        d += 1
    if p > 1:
        fs.append(p)
    return fs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file")
    ap.add_argument("--rule", type=int)
    ap.add_argument("--n", type=int)
    ap.add_argument("--witness")
    ap.add_argument("--period", type=int)
    a = ap.parse_args()
    if a.file:
        kv = {}
        for line in open(a.file):
            if "=" in line:
                k, v = line.strip().split("=", 1)
                kv[k] = v
        rule, n, wit, period = int(kv["rule"]), int(kv["n"]), int(kv["witness"], 0), int(kv["max_period"])
    else:
        rule, n, wit, period = a.rule, a.n, int(a.witness, 0), a.period
    if not (0 <= rule <= 255 and 3 <= n <= 63 and 0 <= wit < (1 << n) and period >= 1):
        print("bad input"); print("FAIL"); return 1
    step = make_step(rule, n)
    # cross-check the bit-parallel step against the per-cell definition on a few states
    probe = [wit, 1, (1 << n) - 1, 0x5555555555555555 & ((1 << n) - 1)]
    for s in probe:
        if step(s) != slow_step(rule, n, s):
            print("step self-check mismatch"); print("FAIL"); return 1
    checkpoints = {period // q: q for q in prime_factors(period)}
    print("rule=%d n=%d witness=0x%x claimed_period=%d" % (rule, n, wit, period))
    print("bit_order: cell0=LSB, idx=(L<<2)|(C<<1)|R, L=i-1, R=i+1 cyclic")
    print("proper divisors checked: %s" % " ".join("%d(=P/%d)" % (d, q) for d, q in sorted(checkpoints.items())))
    t0 = time.time()
    s = wit
    ok = True
    for i in range(1, period + 1):
        s = step(s)
        if i in checkpoints:
            eq = (s == wit)
            print("after %d steps: equals_start=%s" % (i, "yes" if eq else "no"))
            if eq:
                ok = False
        if s == wit and i < period and i not in checkpoints:
            # an earlier return that is not one of P/q would still mean a smaller period
            print("early return at step %d" % i); ok = False; break
    if ok:
        eq = (s == wit)
        print("after %d steps: equals_start=%s" % (period, "yes" if eq else "no"))
        ok = eq
    print("elapsed_sec=%.1f" % (time.time() - t0))
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
