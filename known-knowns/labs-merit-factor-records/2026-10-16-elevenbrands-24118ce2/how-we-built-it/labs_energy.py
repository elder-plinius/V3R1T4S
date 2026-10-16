#!/usr/bin/env python3
"""LABS checker written from the bank definition (labs-merit-factor-records), before any attack.

Definition (bank statement, verbatim): "For a +-1 sequence s of length L, the aperiodic autocorrelations are
C_k = sum_i s_i s_{i+k}, the energy is E = sum_{k=1}^{L-1} C_k^2, and the merit factor is F = L^2/(2E)."

Exact integer arithmetic only (Python ints, O(L^2) loop). Never compares rounded merit factors.
Usage: labs_energy.py <sequence>     sequence as +/- characters (e.g. +++++--++-+-+) or as 1/-1 tokens.
Exit 0 and print "L E F skew" on success; exit 2 with a reason if the input is not a +-1 sequence.
"""
import sys


def parse(text):
    t = text.strip()
    if all(ch in "+-" for ch in t) and t:
        return [1 if ch == "+" else -1 for ch in t]
    toks = t.replace(",", " ").split()
    seq = []
    for tok in toks:
        if tok in ("1", "+1"):
            seq.append(1)
        elif tok == "-1":
            seq.append(-1)
        else:
            raise ValueError("not a +-1 sequence: token %r" % tok)
    if not seq:
        raise ValueError("empty sequence")
    return seq


def autocorrelations(s):
    L = len(s)
    return [sum(s[i] * s[i + k] for i in range(L - k)) for k in range(1, L)]


def energy(s):
    return sum(c * c for c in autocorrelations(s))


def is_skew_symmetric(s):
    """Odd L = 2m+1, 0-indexed: s[m+k] == (-1)^k * s[m-k] for k = 1..m."""
    L = len(s)
    if L % 2 == 0:
        return False
    m = L // 2
    return all(s[m + k] == (-1) ** k * s[m - k] for k in range(1, m + 1))


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    try:
        s = parse(argv[1])
    except ValueError as e:
        print("REJECT:", e)
        return 2
    L = len(s)
    E = energy(s)
    F = "inf" if E == 0 else "%.6f" % (L * L / (2.0 * E))
    print("L=%d E=%d F=%s skew_symmetric=%s" % (L, E, F, is_skew_symmetric(s)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
