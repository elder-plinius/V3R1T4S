#!/usr/bin/env python3
"""ros_cert_check.py -- independent Bellman-certificate checker for the coin game "Risk or Safety"
(V3R1T4S target risk-or-safety-exact-optimal-play). Written from the bank definition only:

  position (a, b, c): a open points and b banked points of the player to move, c banked points of the opponent;
  P(a, b, c) = 1 when a + b >= n (reaching n with open points is a win);
  a = 0 (forced toss): P(0, b, c) = (1/2)(1 - P(0, c, b)) + (1/2) P(1, b, c);
  a >= 1:              P(a, b, c) = max(continue, stop), with
                       continue = (1/2)(1 - P(0, c, b)) + (1/2) P(a + 1, b, c)   and   stop = 1 - P(0, c, a + b).

Certificate JSON: {"n": n, "P000": "num/den", "table": [[a, b, c, "num/den", "toss"|"stop"], ...]}
("continue" is accepted as a synonym of "toss"). The table must list every position (a, b, c) with
0 <= b < n, 0 <= c < n, 0 <= a < n - b  (that is n^2 (n+1)/2 positions), each exactly once.
Every equation is checked with exact rationals (fractions.Fraction). PASS only if all hold.

Usage: python3 -I ros_cert_check.py [--oeis DIR_WITH_b387261.txt_b387262.txt] [--expect num/den] cert.json [...]
Exit code 0 iff every certificate passes (and matches --expect / the OEIS term when given).
"""
import sys, json, os
from fractions import Fraction

def parse_frac(s):
    if isinstance(s, str):
        s = s.strip()
        if '/' in s:
            a, b = s.split('/')
            return Fraction(int(a), int(b))
        return Fraction(int(s))
    if isinstance(s, int):
        return Fraction(s)
    if isinstance(s, (list, tuple)) and len(s) == 2:
        return Fraction(int(s[0]), int(s[1]))
    raise ValueError("bad fraction %r" % (s,))

def check(cert):
    errors = []
    n = int(cert["n"])
    if n < 1:
        return False, ["n must be >= 1"], None, 0
    P, act = {}, {}
    for row in cert["table"]:
        a, b, c = int(row[0]), int(row[1]), int(row[2])
        key = (a, b, c)
        if key in P:
            errors.append("duplicate position %r" % (key,)); continue
        if not (0 <= b < n and 0 <= c < n and 0 <= a and a + b < n):
            errors.append("position out of range or terminal %r" % (key,)); continue
        val = parse_frac(row[3])
        if not (0 <= val <= 1):
            errors.append("value outside [0,1] at %r" % (key,))
        action = str(row[4]).strip().lower()
        if action == "continue":
            action = "toss"
        if action not in ("toss", "stop"):
            errors.append("bad action %r at %r" % (row[4], key))
        P[key] = val
        act[key] = action
    expected_count = n * n * (n + 1) // 2
    if len(P) != expected_count:
        errors.append("table lists %d positions, expected n^2(n+1)/2 = %d" % (len(P), expected_count))
    missing = 0
    for b in range(n):
        for c in range(n):
            for a in range(n - b):
                if (a, b, c) not in P:
                    missing += 1
                    if missing <= 5:
                        errors.append("missing position %r" % ((a, b, c),))
    if missing:
        errors.append("%d positions missing" % missing)
    if errors:
        return False, errors, None, 0

    def get(a, b, c):
        if a + b >= n:
            return Fraction(1)
        return P[(a, b, c)]

    half = Fraction(1, 2)
    nchecked = 0
    for (a, b, c), val in P.items():
        tail = half * (1 - get(0, c, b))
        cont = tail + half * get(a + 1, b, c)
        if a == 0:
            if act[(a, b, c)] != "toss":
                errors.append("a = 0 is a forced toss but action is %r at %r" % (act[(a, b, c)], (a, b, c)))
            if val != cont:
                errors.append("forced-toss equation fails at %r: table %s, computed %s" % ((a, b, c), val, cont))
        else:
            stop = 1 - get(0, c, a + b)
            best = max(cont, stop)
            if val != best:
                errors.append("Bellman max fails at %r: table %s, max(continue=%s, stop=%s)=%s"
                              % ((a, b, c), val, cont, stop, best))
            attained = cont if act[(a, b, c)] == "toss" else stop
            if attained != best:
                errors.append("claimed action %r does not attain the max at %r (continue=%s, stop=%s)"
                              % (act[(a, b, c)], (a, b, c), cont, stop))
        nchecked += 1
        if len(errors) > 25:
            errors.append("... (further errors suppressed)")
            break
    p000 = P[(0, 0, 0)]
    if "P000" in cert and parse_frac(cert["P000"]) != p000:
        errors.append("P000 field %s differs from table P(0,0,0) = %s" % (cert["P000"], p000))
    return (len(errors) == 0), errors, p000, nchecked

def load_oeis(d):
    num, den = {}, {}
    for fn, dst in (("b387261.txt", num), ("b387262.txt", den)):
        for line in open(os.path.join(d, fn)):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            k, v = line.split()
            dst[int(k)] = int(v)
    return {k: Fraction(num[k], den[k]) for k in num if k in den}

def main(argv):
    oeis, expect, files = None, None, []
    i = 0
    while i < len(argv):
        if argv[i] == "--oeis":
            oeis = load_oeis(argv[i + 1]); i += 2
        elif argv[i] == "--expect":
            expect = parse_frac(argv[i + 1]); i += 2
        else:
            files.append(argv[i]); i += 1
    all_ok = True
    for f in files:
        cert = json.load(open(f))
        ok, errors, p000, nchecked = check(cert)
        n = int(cert.get("n", -1))
        line = "%s: n=%d positions_checked=%d" % (os.path.basename(f), n, nchecked)
        if ok:
            line += " P000=%s/%s" % (p000.numerator, p000.denominator)
            if expect is not None:
                m = (p000 == expect); line += " expect_match=%s" % ("yes" if m else "NO"); all_ok &= m
            if oeis is not None and n in oeis:
                m = (p000 == oeis[n]); line += " oeis_match=%s" % ("yes" if m else "NO"); all_ok &= m
            elif oeis is not None:
                line += " oeis_match=n/a(no published term)"
            line += " PASS"
        else:
            all_ok = False
            line += " FAIL"
            for e in errors[:30]:
                line += "\n    - " + e
        print(line)
    print("ALL_PASS" if all_ok else "SOME_FAIL")
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
