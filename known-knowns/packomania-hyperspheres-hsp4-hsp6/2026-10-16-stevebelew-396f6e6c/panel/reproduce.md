# REPRODUCE skeptic verdict: claim N74 (hsp4, 74 balls in the unit 4-ball)

context: subagent (Claude Code Agent tool, fresh context for this one claim)

## Definition used (quoted from CLAIM.md, success criterion)

"the FEASIBLE radius r* := min( min_{i<j} |c_i - c_j| / 2, 1 - max_i |c_i| ) (unit container ball centred at the origin), computed in mpmath at 50 digits directly from the submitted coordinates with no tolerance, is STRICTLY GREATER (direction: max) than that file's 12-decimal value for N re-fetched live immediately before claiming, by at least 1e-10 [...], AND the configuration is not isometric to the posted hsp[d]-[N].txt configuration (sorted pairwise-distance multisets differ by more than 1e-8 somewhere)"

Files used, relative to the claim folder: hsp4-74-candidate.txt, hsp4-74-posted.txt, hsp4_radius_as_fetched.txt. The author's REPRODUCE.md was read only after my checker had been written and run.

## Method

- Wrote my own checker (below) from the quoted definition alone. mp.dps = 50; every coordinate parsed as an mpf directly from its decimal string; distances via mp.sqrt; no tolerance anywhere in r*.
- Ran it with the project venv Python in isolated mode (-I), twice in separate processes, and diffed the full outputs.
- Only afterwards ran the mpmath block from REPRODUCE.md once (same interpreter, -I) and compared its printed numbers to mine. The three curl lines in REPRODUCE.md were NOT run (no web access in this panel); the table value is taken from the saved snapshot hsp4_radius_as_fetched.txt.

## Checker code (check_n74.py, run as: python -I check_n74.py [claim folder])

```python
#!/usr/bin/env python3
# Independent REPRODUCE checker for claim N74 (hsp4). Written from the definition only.
# Definition (quoted from CLAIM.md success criterion):
#   r* := min( min_{i<j} |c_i - c_j| / 2 , 1 - max_i |c_i| )
#   computed in mpmath at 50 digits directly from the submitted coordinates with no tolerance,
#   STRICTLY GREATER (i.e. sign(r* - table) == 1) than the table's 12-decimal value for N by at least 1e-10,
#   AND not isometric to the posted configuration
#   (sorted pairwise-distance multisets differ by more than 1e-8 somewhere).
import sys, re, hashlib, math
from mpmath import mp, mpf, sqrt, fabs, nstr, sign

mp.dps = 50
D = 4
N_EXPECTED = 74
NUM_RE = re.compile(r'^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$')

claim_dir = sys.argv[1]
fails = []

def ok(cond, label):
    print(("PASS " if cond else "FAIL ") + label)
    if not cond:
        fails.append(label)

def parse_coords(path, has_index, skip_first_line, skip_hash):
    pts = []
    with open(path) as f:
        lines = f.read().splitlines()
    if skip_first_line:
        lines = lines[1:]
    for raw in lines:
        s = raw.strip()
        if not s:
            continue
        if skip_hash and s.startswith('#'):
            continue
        toks = s.split()
        if has_index:
            idx = toks[0]; toks = toks[1:]
            assert idx == str(len(pts) + 1), f"bad index {idx} at point {len(pts)+1}"
        assert len(toks) == D, f"line has {len(toks)} coords, expected {D}: {raw!r}"
        for t in toks:
            assert NUM_RE.match(t), f"non-numeric/non-finite token {t!r}"
            assert math.isfinite(float(t)), f"token not finite as float: {t!r}"
        pts.append([mpf(t) for t in toks])
    return pts

def r_star(pts):
    n = len(pts)
    dists = []
    for i in range(n):
        for j in range(i + 1, n):
            d = sqrt(sum((pts[i][k] - pts[j][k]) ** 2 for k in range(D)))
            dists.append(d)
    dmin = min(dists)
    rmax = max(sqrt(sum(c * c for c in p)) for p in pts)
    return min(dmin / 2, 1 - rmax), dmin, rmax, sorted(dists)

# --- table value ---
table = None
rows = 0
with open(f"{claim_dir}/hsp4_radius_as_fetched.txt") as f:
    for line in f:
        t = line.split()
        if len(t) != 2:
            continue
        rows += 1
        if t[0] == str(N_EXPECTED):
            assert table is None, "duplicate N row"
            assert re.match(r'^0\.\d{12}$', t[1]), f"table value not 12-decimal: {t[1]}"
            table = mpf(t[1])
print(f"table rows parsed: {rows}; table[N={N_EXPECTED}] = {nstr(table, 20)}")
ok(table is not None, "table row for N=74 present")

# --- candidate ---
cand = parse_coords(f"{claim_dir}/hsp4-74-candidate.txt", has_index=False, skip_first_line=False, skip_hash=True)
ok(len(cand) == N_EXPECTED, f"candidate has exactly {N_EXPECTED} points (got {len(cand)})")
ok(all(len(p) == D for p in cand), "candidate points all 4-dimensional, all tokens finite numerics")
rc, dmin_c, rmax_c, dists_c = r_star(cand)
print(f"candidate: dmin/2 = {nstr(dmin_c/2, 50)}")
print(f"candidate: 1-rmax = {nstr(1-rmax_c, 50)}")
print(f"candidate: r*     = {nstr(rc, 50)}")
gain = rc - table
print(f"candidate: r* - table = {nstr(gain, 20)}")
ok(sign(rc - table) == 1, "candidate r* strictly greater than table value")
ok(sign(gain - mpf('1e-10')) != -1, "candidate r* exceeds table value by at least 1e-10")
ok(nstr(rc, 16).startswith("0.258529650660235"), "candidate r* matches claimed prefix 0.258529650660235")

# --- posted ---
posted = parse_coords(f"{claim_dir}/hsp4-74-posted.txt", has_index=True, skip_first_line=True, skip_hash=False)
with open(f"{claim_dir}/hsp4-74-posted.txt") as f:
    posted_header = mpf(f.readline().strip())
ok(len(posted) == N_EXPECTED, f"posted has exactly {N_EXPECTED} points (got {len(posted)})")
rp, dmin_p, rmax_p, dists_p = r_star(posted)
print(f"posted:    r*     = {nstr(rp, 50)}")
print(f"posted:    |r* - table| = {nstr(fabs(rp - table), 10)}")
ok(sign(fabs(rp - table) - mpf('1e-11')) != 1, "posted file reproduces table value within 1e-11 (parser sanity)")
ok(posted_header == table, "posted file header radius equals table value")

# --- non-isometry ---
ok(len(dists_c) == len(dists_p) == N_EXPECTED * (N_EXPECTED - 1) // 2, "both distance multisets have 2701 entries")
maxdiff = max(fabs(a - b) for a, b in zip(dists_c, dists_p))
print(f"max |sorted-dist diff| = {nstr(maxdiff, 10)}")
ok(sign(maxdiff - mpf('1e-8')) == 1, "candidate not isometric to posted (sorted distance multisets differ by more than 1e-8)")

# --- determinism fingerprint ---
fp = hashlib.sha256(nstr(rc, 50).encode()).hexdigest()
print(f"rstar50={nstr(rc, 50)} sha256={fp}")

print("ALL PASS" if not fails else f"FAILED: {fails}")
sys.exit(0 if not fails else 1)
```

## Real output (run 1; run 2 was byte-identical, see below)

```
table rows parsed: 299; table[N=74] = 0.258522851648
PASS table row for N=74 present
PASS candidate has exactly 74 points (got 74)
PASS candidate points all 4-dimensional, all tokens finite numerics
candidate: dmin/2 = 0.25852965066045076358574077801755662335652785354473
candidate: 1-rmax = 0.2585296506602351930912926620395159844831432365609
candidate: r*     = 0.2585296506602351930912926620395159844831432365609
candidate: r* - table = 6.7990122351930912927e-6
PASS candidate r* strictly greater than table value
PASS candidate r* exceeds table value by at least 1e-10
PASS candidate r* matches claimed prefix 0.258529650660235
PASS posted has exactly 74 points (got 74)
posted:    r*     = 0.25852285164722350934031567238681935996897324470926
posted:    |r* - table| = 7.764906597e-13
PASS posted file reproduces table value within 1e-11 (parser sanity)
PASS posted file header radius equals table value
PASS both distance multisets have 2701 entries
max |sorted-dist diff| = 0.007284087164
PASS candidate not isometric to posted (sorted distance multisets differ by more than 1e-8)
rstar50=0.2585296506602351930912926620395159844831432365609 sha256=c1e72ba369015d390609e0dfa3f758e1a0c0739fd4e93d5248d987fca9632c73
ALL PASS
```

Determinism: run 2 produced exactly the same output (diff empty); both runs print
rstar50=0.2585296506602351930912926620395159844831432365609 with sha256 c1e72ba369015d390609e0dfa3f758e1a0c0739fd4e93d5248d987fca9632c73.

## Author's REPRODUCE.md block, run once for comparison (its curl lines were not run; two angle-bracket characters in its printed text are replaced by "[arrow]" and "more than" below, numbers untouched)

```
N candidate = 74  N posted = 74
r* candidate = 0.2585296506602351930912927
r* posted    = 0.2585228516472235093403157  (parser sanity: must equal the table value within 1e-11)
table        = 0.258522851648
gain = r*cand - table = 6.7990122e-6  [arrow] meets 1e-10 margin: True
max |sorted distance difference| vs posted = 0.0072840872  (more than 1e-8 means not isometric)
```

## Property-by-property verdict

| Property | Result | Verdict |
|---|---|---|
| Exactly 74 points in hsp4-74-candidate.txt (one # comment line, 74 data lines, 4 tokens each) | 74 | pass |
| All coordinates finite numeric literals (regex + float isfinite), each parsed exactly as mpf at 50 digits | all 296 tokens ok | pass |
| r* of candidate at 50 digits, no tolerance | 0.25852965066023519309129266203951598448314323656 (binding term is 1 - max norm; min-distance term is 0.2585296506604507..., larger by about 2.2e-13) | computed |
| Claimed value r* = 0.258529650660235... | matches to all 15 claimed decimals; the comment-line r_float 0.25852965066023514 is the double rounding of the same number | pass |
| Table value for N = 74 in hsp4_radius_as_fetched.txt (299 rows, row parsed exactly) | 0.258522851648 | pass |
| r* candidate strictly greater than table | sign(r* - table) = +1 | pass |
| Margin at least 1e-10 | r* - table = 6.7990122e-6 (about 68000 times the margin; agrees with the claimed "about 6.80e-06") | pass |
| Posted file reproduces table within 1e-11 (parser sanity) | r* posted = 0.258522851647223..., difference from table 7.76e-13; header line equals table value | pass |
| Posted file has exactly 74 points with indices 1..74 | 74 | pass |
| Not isometric to posted: sorted 2701-element pairwise-distance multisets differ by more than 1e-8 somewhere | max difference 7.284e-3 | pass |
| Deterministic r* across two separate -I runs | identical output, identical sha256 | pass |
| Author's REPRODUCE.md numbers vs mine | r* cand, r* posted, table, gain and max distance difference agree to every printed digit (25 / 8 digits) | pass |

Mismatches found: none. Missing objects: none. Non-determinism: none.

## Caveats (outside what can be checked from the saved files)

- The live re-fetch of radius.txt, the History-of-updates check on hsp4.html, and the pending-requests queue rule could not be exercised here (no web); this verdict covers the mathematical content against the saved snapshot only. Per the bank entry, the "Moki & Julio *many* 4666 candidates" bundle of 26-Sep-2026 is category-unspecified, so N = 74 must be re-checked against the live table once that bundle leaves the pending list.
- The posted packing's own r* (0.258522851647223) is 7.8e-13 below the posted 12-decimal value, i.e. the table rounds up at the 12th decimal; this is within the 1e-11 parser-sanity window and does not affect the comparison.

pass: true
