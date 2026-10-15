#!/usr/bin/env python3
"""consistency.py -- cross-n consistency of certificates (certifier lens).
The value of a position depends only on points needed: P_n(a, b, c) = P_m(a, b + m - n, c + m - n) for m >= n.
For every pair n < m among the given certificates, every position of cert n is mapped into cert m and the values
must be equal (exact rationals); actions must agree unless the position is an exact tie (continue == stop).
Usage: python3 -I consistency.py cert_dir   (expects cert_dir/n<k>.json for k = 1..K)
"""
import sys, os, json
from fractions import Fraction

def load(path):
    c = json.load(open(path))
    n = int(c["n"])
    P, A = {}, {}
    for a, b, cc, v, act in c["table"]:
        P[(int(a), int(b), int(cc))] = Fraction(v)
        A[(int(a), int(b), int(cc))] = ("toss" if act in ("toss", "continue") else "stop")
    return n, P, A

def main():
    d = sys.argv[1]
    certs = {}
    for f in sorted(os.listdir(d)):
        if f.startswith("n") and f.endswith(".json"):
            n, P, A = load(os.path.join(d, f))
            certs[n] = (P, A)
    ns = sorted(certs)
    pairs = 0; positions = 0; value_mismatch = 0; action_mismatch_nontie = 0; action_mismatch_tie = 0
    for n in ns:
        Pn, An = certs[n]
        for m in ns:
            if m <= n:
                continue
            Pm, Am = certs[m]
            pairs += 1
            for (a, b, c), v in Pn.items():
                key = (a, b + m - n, c + m - n)
                positions += 1
                if key not in Pm:
                    value_mismatch += 1
                    if value_mismatch <= 5: print("missing", n, m, (a, b, c), key)
                    continue
                if Pm[key] != v:
                    value_mismatch += 1
                    if value_mismatch <= 5: print("VALUE MISMATCH n=%d m=%d pos=%s -> %s: %s vs %s" % (n, m, (a, b, c), key, v, Pm[key]))
                if An[(a, b, c)] != Am[key]:
                    # tie check in cert m
                    if a >= 1:
                        half = Fraction(1, 2)
                        getm = lambda aa, bb, cc: Fraction(1) if aa + bb >= m else Pm[(aa, bb, cc)]
                        cont = half * (1 - getm(0, key[2], key[1])) + half * getm(a + 1, key[1], key[2])
                        stop = 1 - getm(0, key[2], a + key[1])
                        if cont == stop:
                            action_mismatch_tie += 1
                        else:
                            action_mismatch_nontie += 1
                            if action_mismatch_nontie <= 5: print("ACTION MISMATCH (non-tie)", n, m, (a, b, c), key)
                    else:
                        action_mismatch_nontie += 1
    print("certificates=%d pairs=%d positions_compared=%d value_mismatches=%d action_mismatches_nontie=%d action_mismatches_at_exact_ties=%d"
          % (len(ns), pairs, positions, value_mismatch, action_mismatch_nontie, action_mismatch_tie))
    print("CONSISTENT" if value_mismatch == 0 and action_mismatch_nontie == 0 else "INCONSISTENT")

if __name__ == "__main__":
    main()
