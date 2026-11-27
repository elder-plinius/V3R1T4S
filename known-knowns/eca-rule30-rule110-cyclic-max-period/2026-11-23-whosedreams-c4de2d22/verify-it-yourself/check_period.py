#!/usr/bin/env python3
"""Re-iterate the packaged Rule 30 witness and confirm its eventual period.

Standard library only. Wolfram bit order, as required by the bank target
eca-rule30-rule110-cyclic-max-period:

  cell 0 = least-significant bit of the state word
  neighbourhood (L, C, R) = cells (i-1, i, i+1) cyclic
  idx = (L << 2) | (C << 1) | R
  next bit = (rule >> idx) & 1

The checker reads object/a334497_37.txt, iterates the witness for the claimed
number of steps, requires a return to the start at that length, and requires
that no proper divisor of the claimed length is also a period (so the claimed
length is the least period). Because the claimed period is about 4.9e7 steps,
the step is computed bit-parallel from the rule's minterms; it is cross-checked
against a per-cell implementation of the definition for the first 2000 steps.
"""
from __future__ import print_function

import os
import sys
import time


def parse_object(path):
    fields = {}
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                raise ValueError("unrecognized object line: %r" % line)
            k, v = line.split("=", 1)
            fields[k.strip()] = v.strip()
    needed = ("n", "rule", "max_period", "witness")
    missing = [k for k in needed if k not in fields]
    if missing:
        raise ValueError("object file missing fields: %s" % ", ".join(missing))
    n = int(fields["n"], 10)
    rule = int(fields["rule"], 10)
    period = int(fields["max_period"], 10)
    wit_s = fields["witness"]
    witness = int(wit_s, 16) if wit_s.lower().startswith("0x") else int(wit_s, 10)
    if n < 3 or n > 63:
        raise ValueError("n out of range: %d" % n)
    if not 0 <= rule <= 255:
        raise ValueError("rule out of range: %d" % rule)
    if witness < 0 or witness >= (1 << n):
        raise ValueError("witness does not fit in n bits")
    if period < 1:
        raise ValueError("max_period must be positive")
    return n, rule, period, witness


def slow_step(state, n, rule):
    """Per-cell step, straight from the definition."""
    out = 0
    for i in range(n):
        L = (state >> ((i + n - 1) % n)) & 1
        C = (state >> i) & 1
        R = (state >> ((i + 1) % n)) & 1
        idx = (L << 2) | (C << 1) | R
        if (rule >> idx) & 1:
            out |= 1 << i
    return out


def make_fast_step(n, rule):
    mask = (1 << n) - 1
    terms = [idx for idx in range(8) if (rule >> idx) & 1]

    def step(s):
        L = ((s << 1) | (s >> (n - 1))) & mask   # bit i holds cell i-1
        R = ((s >> 1) | (s << (n - 1))) & mask   # bit i holds cell i+1
        nL, nC, nR = L ^ mask, s ^ mask, R ^ mask
        out = 0
        for idx in terms:
            out |= (L if idx & 4 else nL) & (s if idx & 2 else nC) & (R if idx & 1 else nR)
        return out
    return step


def divisors(p):
    out = set()
    d = 1
    while d * d <= p:
        if p % d == 0:
            out.add(d)
            out.add(p // d)
        d += 1
    return sorted(out)


def main(argv):
    here = os.path.dirname(os.path.abspath(__file__))
    pkg = os.path.dirname(here)
    obj = os.path.join(pkg, "object", "a334497_37.txt")
    if len(argv) > 1:
        obj = argv[1]
    n, rule, period, witness = parse_object(obj)
    print("object: %s" % os.path.relpath(obj, pkg))
    print("n=%d rule=%d claimed_period=%d witness=0x%x" % (n, rule, period, witness))
    print("bit_order: cell0=LSB, idx=(L<<2)|(C<<1)|R, L=i-1, R=i+1 cyclic")
    step = make_fast_step(n, rule)

    # cross-check fast step against the per-cell definition
    s = witness
    for _ in range(min(2000, period)):
        t = step(s)
        if t != slow_step(s, n, rule):
            print("fast/slow step mismatch at state 0x%x" % s)
            print("result: fail")
            return 1
        s = t
    print("step_crosscheck: fast step equals per-cell definition for the first %d steps" % min(2000, period))

    divs = divisors(period)
    dset = set(divs)
    print("divisors: %s" % " ".join(str(d) for d in divs))
    t0 = time.time()
    cur = witness
    at = {}
    first = None
    for i in range(1, period + 1):
        cur = step(cur)
        if i in dset:
            at[i] = cur
        if cur == witness and first is None:
            first = i
            if i < period:
                break
    returned = at.get(period) == witness
    print("after %d steps: state=0x%x start=0x%x returned=%s" % (
        period, at.get(period, -1), witness, "yes" if returned else "no"))
    shorter = []
    for d in divs:
        if d == period or d not in at:
            continue
        hit = at[d] == witness
        print("divisor %d: state=0x%x equals_start=%s" % (d, at[d], "yes" if hit else "no"))
        if hit:
            shorter.append(d)
    print("first_return: %s" % (first if first is not None else "none"))
    print("shorter_period_divisors: %s" % (shorter if shorter else "none"))
    print("elapsed_sec: %.1f" % (time.time() - t0))
    ok = returned and not shorter and first == period
    if ok:
        print("period_confirmed: %d" % period)
        print("result: ok")
        return 0
    print("result: fail")
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except Exception as e:
        print("error: %s" % e)
        print("result: fail")
        sys.exit(1)
