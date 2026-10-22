#!/usr/bin/env python3
"""Standard-library-only checker for the claim h2 = 0.662798972833745915155196234397725566 (36 decimals).
Run from the claim folder:  python3 -I verify-it-yourself/check_md.py   (the last output line is PASS or FAIL).

Parts
 0  INDEX.csv lists every file of object/ with its sha256 (and nothing else).
 1  Parse the open-strip table (ln of the largest eigenvalue of the open-row transfer matrix, widths 3..29, 70 digits each) and apply
    the recipe of PREREG_B3.md with my own Wynn epsilon in decimal arithmetic at 80 digits: r_m = L_m - L_{m-1}, m = 5..mmax,
    E3(mmax) = last entry of the highest even-index column, mmax = 21..29. Compare with object/B3_result.txt, count the decimals
    shared by the last four mmax, and compare with the 36 decimals of object/VALUE.txt.
 2  Method A (corner transfer matrix) ladder: parse object/ctm_ladder.json and object/ctm_ladder_ext.json, count decimals shared by the
    last four rungs of each ladder, and the agreement of A and B3 (object/B3_vs_A.txt).
 3  Kong's bracket [0.662798972831, 0.662798972845] and his value 0.662798972834 at 12 decimals (from table-record/README.md).
 4  Definition check: count monomer-dimer configurations (matchings) of n x n grids for n up to 6 and compare with the OEIS A028420
    terms quoted in table-record/README.md.
"""
import hashlib, json, os, re, sys, csv
from decimal import Decimal, getcontext, ROUND_DOWN, ROUND_HALF_UP

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OBJ = os.path.join(ROOT, "object")
fails = []
def ok(cond, msg):
    print(("ok    " if cond else "FAIL  ") + msg)
    if not cond: fails.append(msg)
def read(p): return open(os.path.join(ROOT, p), encoding="utf-8").read()

# ---------------------------------------------------------------- part 0
print("== part 0: INDEX.csv lists every object file with its sha256")
rows = list(csv.reader(open(os.path.join(ROOT, "verify-it-yourself", "object_files.csv"), encoding="utf-8")))
ok(rows[0] == ["target_id", "cell", "value", "table_value", "table_fetched_utc", "file", "sha256"], "INDEX.csv header")
listed = set()
bad = 0
for r in rows[1:]:
    f, h = r[5], r[6]
    listed.add(f)
    if hashlib.sha256(open(os.path.join(ROOT, f), "rb").read()).hexdigest() != h: bad += 1; print("FAIL  sha256 mismatch " + f)
ok(bad == 0, "sha256 of all %d indexed files" % len(listed))
onDisk = set()
for d, _, fs in os.walk(OBJ):
    for f in fs: onDisk.add(os.path.relpath(os.path.join(d, f), ROOT).replace(os.sep, "/"))
ok(listed == onDisk, "INDEX.csv lists exactly the files in object/ (%d files)" % len(onDisk))
ok(all(os.path.getsize(os.path.join(ROOT, f)) < 1000000 for f in onDisk), "every object file is below 1,000,000 bytes")

# ---------------------------------------------------------------- helpers
getcontext().prec = 80
def dec_digits(x, n=60):
    """decimals of a number in (0,1) as a string of n digits, truncated"""
    s = format(x.quantize(Decimal(1).scaleb(-n), rounding=ROUND_DOWN), "f")
    assert s.startswith("0.")
    return s[2:]
def common(strs):
    n = 0
    while n < min(len(s) for s in strs) and all(s[n] == strs[0][n] for s in strs): n += 1
    return n
def wynn_last(seq):
    """Wynn epsilon: eps_{-1} = 0, eps_0 = seq, eps_{k+1}[i] = eps_{k-1}[i+1] + 1/(eps_k[i+1] - eps_k[i]).
    Returns (k, value): the last entry of the highest even-index column."""
    prev = [Decimal(0)] * (len(seq) + 1); cur = list(seq); best = (0, cur[-1]); k = 0
    while len(cur) >= 2:
        new = []
        for i in range(len(cur) - 1):
            d = cur[i + 1] - cur[i]
            if d == 0: raise ZeroDivisionError("zero difference in Wynn table")
            new.append(prev[i + 1] + 1 / d)
        prev, cur = cur, new; k += 1
        if k % 2 == 0: best = (k, cur[-1])
    return best

# ---------------------------------------------------------------- part 1
print("== part 1: open strips + Wynn epsilon (recipe of PREREG_B3.md) at 80 digits")
L = {}
for m in range(3, 30):
    d = json.load(open(os.path.join(OBJ, "open_strips", "hp_P0_m%d.json" % m)))
    assert d["m"] == m and d["P"] == 0
    L[m] = Decimal(d["ln_lambda"])
ok(sorted(L) == list(range(3, 30)), "open_strips holds widths 3..29, ln(lambda) with %d characters each" % len(d["ln_lambda"]))
# the same widths listed in hprun_open.out (58 digits) agree with the json to those digits
hp = {}
for line in read("object/hprun_open.out").splitlines():
    f = line.split(); hp[int(f[0])] = f[1]
ok(all(str(L[m]).startswith(hp[m][:50]) for m in hp), "hprun_open.out agrees with the json values to 50 characters, widths 3..29")
pub = {}
for line in read("object/B3_result.txt").splitlines():
    mt = re.match(r"mmax\s+(\d+) terms\s+(\d+) eps_(\d+)\s+E = (0\.\d+)", line)
    if mt: pub[int(mt.group(1))] = (int(mt.group(2)), int(mt.group(3)), mt.group(4)[2:])
E = {}; mismatch = []
for mmax in range(21, 30):
    seq = [L[m] - L[m - 1] for m in range(5, mmax + 1)]
    k, e = wynn_last(seq); E[mmax] = dec_digits(e, 60)
    terms, kk, pubdigits = pub[mmax]
    if terms != len(seq) or kk != k: mismatch.append(mmax)
    agree = common([E[mmax], pubdigits])
    print("      mmax %2d: %2d terms, eps_%-2d, mine %s..., agrees with B3_result.txt on %d of its %d decimals" % (mmax, len(seq), k, E[mmax][:40], agree, len(pubdigits)))
    if agree < 44: mismatch.append(mmax)
ok(not mismatch, "my E3(mmax) for mmax = 21..29 reproduce B3_result.txt (terms, eps index, at least 44 of 48 printed decimals)")
wins = {}
for line in read("object/B3_result.txt").splitlines():
    mt = re.match(r"window \[(\d+), (\d+), (\d+), (\d+)\] common decimals (\d+)", line)
    if mt: wins[tuple(int(mt.group(i)) for i in range(1, 5))] = int(mt.group(5))
allmatch = True
for w, n in sorted(wins.items()):
    mine = common([E[x] for x in w]) if all(x in E for x in w) else None
    if mine is not None and mine != n: allmatch = False; print("      window %s: mine %d, file %d" % (list(w), mine, n))
ok(allmatch, "my four-term window counts equal those in B3_result.txt wherever mmax >= 21")
last4 = common([E[m] for m in (26, 27, 28, 29)])
ok(last4 == 36, "mmax = 26, 27, 28, 29 share exactly %d decimals (claimed 36; the 37th decimal differs)" % last4)
val = re.search(r"H2_36 = (0\.\d+)", read("object/VALUE.txt")).group(1)[2:]
ok(len(val) == 36, "VALUE.txt gives %d decimals: 0.%s" % (len(val), val))
ok(all(E[m].startswith(val) for m in (26, 27, 28, 29)), "the 36 decimals of VALUE.txt are the first 36 decimals of E3(26), E3(27), E3(28), E3(29)")

# ---------------------------------------------------------------- part 2
print("== part 2: method A (CTM) ladders and the A versus B3 agreement")
lad = json.load(open(os.path.join(OBJ, "ctm_ladder.json"))); lad.update(json.load(open(os.path.join(OBJ, "ctm_ladder_ext.json"))))
A = {int(k): dec_digits(Decimal(v), 60) for k, v in lad.items()}
ok(sorted(A) == [12, 16, 20, 24, 28, 32, 36, 40, 44, 48], "ladder rungs chi = " + ", ".join(str(k) for k in sorted(A)))
pre = common([A[c] for c in (16, 20, 24, 28)])
ext = common([A[c] for c in (36, 40, 44, 48)])
ok(pre == 30, "pre-registered ladder, last four rungs chi = 16, 20, 24, 28 share %d decimals (claimed 30)" % pre)
ok(ext == 43, "extended ladder, last four rungs chi = 36, 40, 44, 48 share %d decimals (claimed 43)" % ext)
ok(all(A[c].startswith(val) for c in (36, 40, 44, 48)), "chi = 36, 40, 44, 48 all begin with the 36 decimals of VALUE.txt")
vsA = {}
for line in read("object/B3_vs_A.txt").splitlines():
    mt = re.match(r"E3\((\d+)\) vs A\(chi=48\): (\d+) common decimals", line)
    if mt: vsA[int(mt.group(1))] = int(mt.group(2))
mine = {m: common([E[m], A[48]]) for m in (26, 27, 28, 29)}
ok(mine == vsA, "A (chi = 48) versus E3(26..29): shared decimals %s, equal to B3_vs_A.txt %s" % (mine, vsA))
ok(min(ext, last4, mine[29]) == 36, "rule D = min(A stable %d, B3 stable %d, A versus B3 %d) = %d" % (ext, last4, mine[29], min(ext, last4, mine[29])))
print("      for information, with the pre-registered A rungs: E3(29) shares %s decimals with the A values chi = 16, 20, 24, 28" % [common([E[29], A[c]]) for c in (16, 20, 24, 28)])

# ---------------------------------------------------------------- part 3
print("== part 3: Kong's bracket")
tr = read("the-record-we-beat/README.md")
kb = re.search(r"KONG_BEGIN\s+value (0\.\d+)\s+low (0\.\d+)\s+high (0\.\d+)\s+KONG_END", tr)
kv, klo, khi = (Decimal(kb.group(i)) for i in (1, 2, 3))
H = Decimal("0." + val)
ok(klo < H < khi, "0.%s lies inside [%s, %s]" % (val, klo, khi))
ok(H.quantize(Decimal("1e-12"), rounding=ROUND_HALF_UP) == kv, "rounded to 12 decimals the value is %s = Kong's printed value" % kv)
big = Decimal("0." + E[29])
ok(klo < big < khi, "E3(29) at 60 decimals also lies inside the bracket")

# ---------------------------------------------------------------- part 4
print("== part 4: definition check, matchings of n x n grids against A028420")
blk = re.search(r"A028420_BEGIN\n(.*?)\nA028420_END", tr, re.S).group(1)
oeis = {int(a): int(b) for a, b in (l.split() for l in blk.splitlines())}
def edges(n):
    es = []
    for i in range(n):
        for j in range(n):
            if j + 1 < n: es.append((i * n + j, i * n + j + 1))
            if i + 1 < n: es.append((i * n + j, (i + 1) * n + j))
    return es
def enumerate_matchings(n):
    """explicit enumeration: every set of pairwise vertex-disjoint edges is visited once"""
    es = edges(n); cnt = 0
    stack = [(0, 0)]
    while stack:
        k, used = stack.pop()
        if k == len(es): cnt += 1; continue
        stack.append((k + 1, used))
        a, b = es[k]
        if not (used >> a) & 1 and not (used >> b) & 1: stack.append((k + 1, used | (1 << a) | (1 << b)))
    return cnt
def frontier_count(n):
    """cell by cell: the first undecided cell is a monomer or is paired with a free right or lower neighbour; memoised on the decided-set"""
    memo = {}
    def rec(mask, pos):
        while pos < n * n and (mask >> pos) & 1: pos += 1
        if pos == n * n: return 1
        key = (mask >> pos, pos)
        if key in memo: return memo[key]
        r = rec(mask | (1 << pos), pos + 1)
        i, j = divmod(pos, n)
        if j + 1 < n and not (mask >> (pos + 1)) & 1: r += rec(mask | (1 << pos) | (1 << (pos + 1)), pos + 1)
        if i + 1 < n and not (mask >> (pos + n)) & 1: r += rec(mask | (1 << pos) | (1 << (pos + n)), pos + 1)
        memo[key] = r; return r
    return rec(0, 0)
for n in range(0, 6):
    c = enumerate_matchings(n) if n > 0 else 1
    ok(c == oeis[n], "n = %d: explicit enumeration of edge sets gives %d, A028420(%d) = %d" % (n, c, n, oeis[n]))
for n in range(1, 7):
    c = frontier_count(n)
    ok(c == oeis[n], "n = %d: cell-by-cell count gives %d, A028420(%d) = %d" % (n, c, n, oeis[n]))

print("failed checks: %d" % len(fails))
print("PASS" if not fails else "FAIL")
sys.exit(0 if not fails else 1)
