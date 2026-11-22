#!/usr/bin/env python3
"""Standalone checker for the A247413 / D = 33 package folder. Standard library only.

Run from the package folder:  python3 verify-it-yourself/check_kings.py
It prints one line per check and ends with PASS or FAIL.

Parts
  1. parse the object tables (strip eigenvalues, site-CTM ladder, domino ladder, the author's output)
  2. own Wynn epsilon algorithm in decimal arithmetic at 80 digits, applied to the ratios
     r_m = lambda_m / lambda_(m-1), m = 3..mmax, as PREREG_B.md specifies; reproduces E(mmax), mmax = 22..40,
     and the stable decimal counts of object/prereg_b_output.txt
  3. leading decimals shared by methods A and B, and with the published A247413 digits
  4. exact check from the definition: independent sets of the king graph on n x n grids, n = 1..7, against A063443;
     open-strip spectral radius for widths m = 1..6 by exact-integer power iteration against the listed lambda_m
"""
import os
import re
import sys
import hashlib
from decimal import Decimal, getcontext
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
getcontext().prec = 80
FAILS = []


def say(msg):
    print(msg)


def check(ok, msg):
    say(("ok    " if ok else "FAIL  ") + msg)
    if not ok:
        FAILS.append(msg)
    return ok


def read(rel):
    with open(os.path.join(ROOT, rel)) as f:
        return f.read()


def common_prefix(strings):
    n = 0
    for chars in zip(*strings):
        if len(set(chars)) > 1:
            break
        n += 1
    return n


def decimals_of(s):
    """digits after the decimal point of a numeric string"""
    return s.split(".", 1)[1]


# ---------------------------------------------------------------- part 0: INDEX.csv hashes
def part0():
    say("== part 0: INDEX.csv row and SHA256SUMS hashes of every object file")
    rows = read("INDEX.csv").strip().splitlines()
    header = rows[0].split(",")
    check(header == ["target_id", "cell", "value", "table_value", "table_fetched_utc", "file", "sha256"],
          "INDEX.csv header")
    check(len(rows) == 2, "INDEX.csv has one data row")
    for r in rows[1:]:
        f = r.split(",")
        h = hashlib.sha256(open(os.path.join(ROOT, f[5]), "rb").read()).hexdigest()
        check(h == f[6], "sha256 of " + f[5])
    sums = {}
    for line in read("SHA256SUMS").splitlines():
        parts = line.split(None, 1)
        if len(parts) == 2:
            sums[parts[1].strip().lstrip("*")] = parts[0]
    on_disk = sorted("object/" + n for n in os.listdir(os.path.join(ROOT, "object")))
    for f in on_disk:
        h = hashlib.sha256(open(os.path.join(ROOT, f), "rb").read()).hexdigest()
        check(sums.get(f) == h, "SHA256SUMS hash of " + f)
    check(len(on_disk) == 13, "object/ holds 13 files")


# ---------------------------------------------------------------- part 1: parse tables
def parse_lambda(rel):
    d = {}
    for line in read(rel).splitlines():
        p = line.split()
        if len(p) == 3:
            d[int(p[0])] = (int(p[1]), Decimal(p[2]))
    return d


def last_kappa(rel):
    last = None
    for line in read(rel).splitlines():
        p = line.split()
        if len(p) > 3 and p[0].isdigit() and p[1].startswith("1."):
            last = p[1]
    return last


def part1():
    say("== part 1: parse the object tables")
    lam_open = parse_lambda("object/lam_open.txt")
    lean = parse_lambda("object/lam_open_lean.txt")
    check(sorted(lam_open) == list(range(2, 29)), "lam_open.txt holds widths 2..28 (70 digits each)")
    check(sorted(lean) == [24, 28] + list(range(29, 41)), "lam_open_lean.txt holds widths 24, 28 and 29..40")
    lam = {m: v for m, (it, v) in lam_open.items()}
    for m, (it, v) in lean.items():
        if m > 28:
            lam[m] = v
    # the lean program reproduces the old program at m = 24, 28 (data check of the author's validation)
    for m in (24, 28):
        rel = abs(lean[m][1] - lam_open[m][1]) / lam_open[m][1]
        check(rel < Decimal("1e-50"), "lean vs old lambda_%d: relative difference %.1e" % (m, float(rel)))
    # site CTM ladder from the logs
    ladderA = {}
    for chi in (70, 80, 90, 100):
        ladderA[chi] = decimals_of(last_kappa("object/sitef_%d.log" % chi))
    ft = read("object/final_tables.txt")
    tableA = {}
    for line in ft.splitlines():
        p = line.split()
        if len(p) >= 4 and p[0].isdigit() and p[2] == "True":
            tableA[int(p[0])] = decimals_of(p[3])
    for chi in (70, 80, 90, 100):
        n = len(tableA[chi])
        check(ladderA[chi][:n] == tableA[chi], "sitef_%d.log last line agrees with Table A in final_tables.txt (%d decimals)" % (chi, n))
    # domino ladder (supporting only)
    ladderC = {}
    for chi in (100, 110, 120, 130):
        ladderC[chi] = decimals_of(last_kappa("object/domg_%d.log" % chi))
    return lam, ladderA, ladderC


# ---------------------------------------------------------------- part 2: Wynn epsilon
def wynn_last_even(seq):
    """Wynn epsilon table. Returns (order, last entry of the highest even column). Column 0 holds seq itself,
    column k+1 entry j = column k-1 entry j+1 + 1 / (column k entry j+1 - column k entry j)."""
    prev = [Decimal(0)] * (len(seq) + 1)
    cur = list(seq)
    cols = [cur]
    k = 0
    while len(cur) > 1:
        nxt = []
        for j in range(len(cur) - 1):
            d = cur[j + 1] - cur[j]
            nxt.append(prev[j + 1] + (1 / d if d != 0 else Decimal(10) ** 60))
        prev, cur = cur, nxt
        cols.append(cur)
        k += 1
    even = [(k, c) for k, c in enumerate(cols) if k % 2 == 0 and c]
    k, c = even[-1]
    return k // 2, c[-1]


def parse_prereg_output():
    E = {}
    win = {}
    for line in read("object/prereg_b_output.txt").splitlines():
        m = re.match(r"mmax=(\d+) order=(\d+) E=1\.(\d+)\s+common_with_siteCTM=(\d+)", line)
        if m:
            E[int(m.group(1))] = (int(m.group(2)), m.group(3), int(m.group(4)))
        m = re.match(r"window mmax=(\d+)\.\.(\d+) : common decimals = (\d+)", line)
        if m:
            win[int(m.group(2))] = int(m.group(3))
    return E, win


def part2(lam):
    say("== part 2: own Wynn epsilon at 80 digits on r_m = lambda_m / lambda_(m-1), m = 3..mmax")
    E_file, win_file = parse_prereg_output()
    mine = {}
    for mmax in range(22, 41):
        r = [lam[m] / lam[m - 1] for m in range(3, mmax + 1)]
        order, val = wynn_last_even(r)
        s = format(val, ".60f")
        mine[mmax] = (order, s.split(".")[1])
    bad = 0
    for mmax in range(22, 41):
        order_f, digs_f, _ = E_file[mmax]
        order_m, digs_m = mine[mmax]
        n = len(digs_f)
        if not (order_f == order_m and digs_m[:n] == digs_f):
            bad += 1
            say("      mmax=%d: file order %d, mine %d; file %s mine %s" % (mmax, order_f, order_m, digs_f, digs_m[:n]))
    check(bad == 0, "E(mmax) for mmax = 22..40 matches prereg_b_output.txt (order and %d printed decimals)" % len(E_file[40][1]))
    # stable counts, windows of four successive mmax
    bad = 0
    for end in range(25, 41):
        mine_w = common_prefix([mine[k][1] for k in range(end - 3, end + 1)])
        if mine_w != win_file[end]:
            bad += 1
            say("      window ending %d: file %d mine %d" % (end, win_file[end], mine_w))
    check(bad == 0, "window counts (four successive mmax) for windows ending 25..40 match the file")
    D_B = common_prefix([mine[k][1] for k in range(37, 41)])
    say("      method B: decimals common to E(37), E(38), E(39), E(40): %d" % D_B)
    say("      method B: window ending 34 (the original target width): %d" % common_prefix([mine[k][1] for k in range(31, 35)]))
    check(D_B == 33, "method B stable decimal count over mmax = 37..40 is 33")
    return mine, D_B


# ---------------------------------------------------------------- part 3: agreement
def parse_oeis_digits():
    txt = read("the-record-we-beat/README.md")
    m = re.search(r"DATA_BEGIN\n(.*?)\nDATA_END", txt, re.S)
    return [int(x) for x in m.group(1).strip().split(",")]


def part3(mine, ladderA, ladderC):
    say("== part 3: agreement counts")
    data = parse_oeis_digits()
    check(len(data) == 18, "A247413 DATA excerpt has 18 terms")
    oeis_dec = "".join(str(x) for x in data[1:])  # first term is the integer part
    check(data[0] == 1, "first term is the integer part 1; %d published decimals follow" % len(oeis_dec))
    A = ladderA[100]
    B = mine[40][1]
    D_A = common_prefix([ladderA[c] for c in (70, 80, 90, 100)])
    say("      method A: decimals common to chi = 70, 80, 90, 100: %d" % D_A)
    say("      method A: decimals common to chi = 80, 90, 100: %d" % common_prefix([ladderA[c] for c in (80, 90, 100)]))
    check(D_A == 36, "method A stable decimal count over chi = 70..100 is 36")
    ab = common_prefix([A, B])
    say("      A (chi = 100) vs B (E(40)): %d common decimals" % ab)
    check(ab >= 33, "A and B share at least 33 leading decimals (%d)" % ab)
    check(A[:len(oeis_dec)] == oeis_dec and B[:len(oeis_dec)] == oeis_dec,
          "A and B both begin with the %d published decimals" % len(oeis_dec))
    # the 33-decimal value
    kv = read("object/KINGS_VALUE.txt")
    m = re.search(r"^VALUE_33 = 1\.(\d{33})$", kv, re.M)
    check(m is not None, "KINGS_VALUE.txt carries the 33-decimal value")
    if m:
        v33 = m.group(1)
        check(A[:33] == v33 and B[:33] == v33, "the 33 decimals equal the first 33 decimals of A (chi = 100) and of B (E(40))")
        check(A[33:35] == "39" and B[33:35] == "39", "decimals 34-35 of A and of B are 39 (truncation and rounding give the same 33 decimals)")
    say("      method C (domino CTM, supporting): decimals common to chi = 100, 110, 120, 130 last lines: %d; with A (chi = 100): %s"
        % (common_prefix([ladderC[c] for c in (100, 110, 120, 130)]),
           ", ".join("%d:%d" % (c, common_prefix([A, ladderC[c]])) for c in (100, 110, 120, 130))))
    # Liang bracket
    lo = Decimal("1." + "34264395112460129" + "7851")
    hi = Decimal("1." + "34264395112460129" + "8092")
    a_val = Decimal("1." + A[:60])
    say("      published bracket (Liang) low %s high %s; method A value inside it: %s" % (lo, hi, lo <= a_val < hi))


# ---------------------------------------------------------------- part 4: definition checks
def king_states(m):
    return [s for s in range(1 << m) if not (s & (s >> 1))]


def compatible(s, t):
    # no site of t within one row (same, above, below) of an occupied site of s
    return (s & t) == 0 and (s & (t << 1)) == 0 and (s & (t >> 1)) == 0


def count_independent_sets(rows, cols):
    """Z(rows, cols): independent sets of the king graph on a rows x cols grid, by column transfer, exact integers."""
    states = king_states(rows)
    vec = {s: 1 for s in states}
    for _ in range(cols - 1):
        new = {}
        for t in states:
            new[t] = sum(vec[s] for s in states if compatible(s, t))
        vec = new
    return sum(vec.values())


def parse_a063443():
    txt = read("the-record-we-beat/README.md")
    m = re.search(r"A063443_BEGIN\n(.*?)\nA063443_END", txt, re.S)
    d = {}
    for line in m.group(1).strip().splitlines():
        a, b = line.split()
        d[int(a)] = int(b)
    return d


def spectral_radius_exact(m, iters=240):
    """Dominant eigenvalue of the symmetric 0/1 matrix T(s, t) of the open strip of m rows, from exact integer power
    iteration: v <- T v (integers), lambda^2 ~ |Tv|^2 / |v|^2 (exact Fraction, converted to 80-digit Decimal)."""
    states = king_states(m)
    nbrs = {s: [t for t in states if compatible(s, t)] for s in states}
    v = {s: 1 for s in states}
    for _ in range(iters):
        v = {s: sum(v[t] for t in nbrs[s]) for s in states}
    w = {s: sum(v[t] for t in nbrs[s]) for s in states}
    num = sum(x * x for x in w.values())
    den = sum(x * x for x in v.values())
    q = Fraction(num, den)  # lambda^2
    ctx_val = Decimal(q.numerator) / Decimal(q.denominator)
    return ctx_val.sqrt()


def part4(lam):
    say("== part 4: checks from the definition")
    a = parse_a063443()
    for n in range(1, 8):
        z = count_independent_sets(n, n)
        check(z == a[n + 1], "independent sets of the king graph on the %dx%d grid = %d = A063443(%d)" % (n, n, z, n + 1))
    # a rectangular spot check against the table too: Z(m, m+1) is not in A063443, so only the transposition symmetry
    check(count_independent_sets(3, 5) == count_independent_sets(5, 3), "Z(3,5) = Z(5,3) (grid symmetry)")
    for m in range(1, 7):
        r = spectral_radius_exact(m)
        if m == 1:
            phi = (1 + Decimal(5).sqrt()) / 2
            rel = abs(r - phi) / phi
            check(rel < Decimal("1e-40"), "open strip m = 1: exact power iteration gives %s, golden ratio %s (rel diff %.1e)"
                  % (format(r, ".40f"), format(phi, ".40f"), float(rel)))
        else:
            ref = lam[m]
            rel = abs(r - ref) / ref
            check(rel < Decimal("1e-40"), "open strip m = %d: exact power iteration %s vs listed lambda_m %s (rel diff %.1e)"
                  % (m, format(r, ".30f"), format(ref, ".30f"), float(rel)))


def main():
    part0()
    lam, ladderA, ladderC = part1()
    mine, D_B = part2(lam)
    part3(mine, ladderA, ladderC)
    part4(lam)
    say("")
    say("failed checks: %d" % len(FAILS))
    say("PASS" if not FAILS else "FAIL")
    return 0 if not FAILS else 1


if __name__ == "__main__":
    sys.exit(main())
