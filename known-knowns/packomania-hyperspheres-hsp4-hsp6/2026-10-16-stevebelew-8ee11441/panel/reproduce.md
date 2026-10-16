# REPRODUCE verdict for claim N94 (hsp4, N = 94)

context: subagent (Claude Code Agent tool, fresh context for this one claim)

## Definition used (quoted from CLAIM.md, success criterion)

> the FEASIBLE radius r* := min( min_{i<j} |c_i - c_j| / 2, 1 - max_i |c_i| ) (unit container ball centred at the origin), computed in mpmath at 50 digits directly from the submitted coordinates with no tolerance, is STRICTLY GREATER (direction: max) than that file's 12-decimal value for N re-fetched live immediately before claiming, by at least 1e-10 [...], AND the configuration is not isometric to the posted hsp4-94.txt [placeholders d, N substituted with 4, 94] configuration (sorted pairwise-distance multisets differ by more than 1e-8 somewhere)

Files read (all relative to the claim folder): CLAIM.md, hsp4-94-candidate.txt, hsp4-94-posted.txt, hsp4_radius_as_fetched.txt, and only afterwards REPRODUCE.md. No web fetches were made.

## Method

I wrote the checker below from the definition BEFORE opening REPRODUCE.md. It parses each coordinate string straight into a 50-digit mpf (no float round-trip for the arithmetic; float() is used only for the finiteness check), computes all 4371 pairwise distances, the max norm, r*, and the sorted distance multisets. It was run with the venv interpreter under -I, twice, and the two outputs were diffed.

## Checker (check.py, run as: python -I check.py claim-folder)

```python
# Independent checker written from the definition in CLAIM.md:
#   r* := min( min_{i<j} |c_i - c_j| / 2 , 1 - max_i |c_i| )
#   computed in mpmath at 50 digits directly from the coordinates, no tolerance.
import sys, math
from mpmath import mp, mpf, sqrt

mp.dps = 50
D = 4
N_EXPECTED = 94

def load_points(path, skip_index_col, skip_first_line):
    pts = []
    with open(path) as f:
        lines = f.read().split('\n')
    if skip_first_line:
        lines = lines[1:]
    for ln in lines:
        s = ln.strip()
        if not s or s.startswith('#'):
            continue
        tok = s.split()
        if skip_index_col:
            tok = tok[1:]
        if len(tok) != D:
            raise SystemExit(f"FAIL: line with {len(tok)} coords: {ln!r}")
        row = []
        for t in tok:
            fl = float(t)
            if not math.isfinite(fl):
                raise SystemExit(f"FAIL: non-finite coord {t!r}")
            row.append(mpf(t))  # exact decimal -> 50-digit mpf
        pts.append(row)
    return pts

def norm(v):
    return sqrt(sum(x*x for x in v))

def rstar(pts):
    n = len(pts)
    dmin = None
    for i in range(n):
        for j in range(i+1, n):
            d = norm([pts[i][k]-pts[j][k] for k in range(D)])
            if dmin is None or d < dmin:
                dmin = d
    rmax = max(norm(p) for p in pts)
    half = dmin/2
    wall = 1 - rmax
    return min(half, wall), half, wall

def dist_multiset(pts):
    n = len(pts)
    out = []
    for i in range(n):
        for j in range(i+1, n):
            out.append(norm([pts[i][k]-pts[j][k] for k in range(D)]))
    out.sort()
    return out

def table_value(path, n):
    vals = []
    with open(path) as f:
        for ln in f:
            tok = ln.split()
            if len(tok) == 2 and tok[0] == str(n):
                vals.append(tok[1])
    if len(vals) != 1:
        raise SystemExit(f"FAIL: expected exactly one row for N={n}, got {vals}")
    return mpf(vals[0]), vals[0]

folder = sys.argv[1]
cand = load_points(folder + '/hsp4-94-candidate.txt', False, False)
post = load_points(folder + '/hsp4-94-posted.txt', True, True)
tab, tab_str = table_value(folder + '/hsp4_radius_as_fetched.txt', N_EXPECTED)

ok = True
def chk(name, cond, detail):
    global ok
    print(f"[{'PASS' if cond else 'FAIL'}] {name}: {detail}")
    ok = ok and cond

chk("candidate has 94 points", len(cand) == N_EXPECTED, f"n={len(cand)}")
chk("posted has 94 points", len(post) == N_EXPECTED, f"n={len(post)}")
chk("all coords finite (candidate)", all(all(math.isfinite(float(x)) for x in p) for p in cand), "checked via float()")

rc, hc, wc = rstar(cand)
rp, hp, wp = rstar(post)
print(f"table N=94 string: {tab_str}")
print(f"candidate r*     = {mp.nstr(rc, 40)}  (half-min-dist={mp.nstr(hc,30)}, wall={mp.nstr(wc,30)})")
print(f"posted    r*     = {mp.nstr(rp, 40)}  (half-min-dist={mp.nstr(hp,30)}, wall={mp.nstr(wp,30)})")
print(f"candidate - table = {mp.nstr(rc - tab, 15)}")
print(f"|posted - table|  = {mp.nstr(abs(rp - tab), 15)}")

chk("posted reproduces table within 1e-11", abs(rp - tab) < mpf('1e-11'), f"|diff|={mp.nstr(abs(rp-tab),6)}")
chk("candidate r* > table by >= 1e-10", (rc - tab) >= mpf('1e-10'), f"gain={mp.nstr(rc-tab,10)}")
chk("candidate r* strictly > table", rc > tab, "")
chk("candidate r* ~ 0.245941019536845 (claim text)", abs(rc - mpf('0.245941019536845')) < mpf('1e-15'), f"r*={mp.nstr(rc,20)}")

mc = dist_multiset(cand)
mpost = dist_multiset(post)
chk("multisets same length", len(mc) == len(mpost), f"{len(mc)} vs {len(mpost)}")
maxdiff = max(abs(a-b) for a, b in zip(mc, mpost))
chk("not isometric (max sorted-dist diff > 1e-8)", maxdiff > mpf('1e-8'), f"max diff={mp.nstr(maxdiff,10)}")
chk("candidate points strictly inside unit ball", wc > 0, f"1-max|c|={mp.nstr(wc,10)}")
chk("candidate points pairwise distinct", hc > 0, "")

# full-precision string for determinism comparison across runs
print("RSTAR50:", mp.nstr(rc, 50))
print("OVERALL:", "PASS" if ok else "FAIL")
```

## Real output (run 1; run 2 was byte-identical per diff)

```
[PASS] candidate has 94 points: n=94
[PASS] posted has 94 points: n=94
[PASS] all coords finite (candidate): checked via float()
table N=94 string: 0.245932827006
candidate r*     = 0.2459410195368451990247712207741077391216  (half-min-dist=0.245941019536988887585924842684, wall=0.245941019536845199024771220774)
posted    r*     = 0.2459328270048503541459008227741407444214  (half-min-dist=0.245932827005040583357902222056, wall=0.245932827004850354145900822774)
candidate - table = 8.19253084519902e-6
|posted - table|  = 1.14964585409918e-12
[PASS] posted reproduces table within 1e-11: |diff|=1.14965e-12
[PASS] candidate r* > table by >= 1e-10: gain=8.192530845e-6
[PASS] candidate r* strictly > table: 
[PASS] candidate r* ~ 0.245941019536845 (claim text): r*=0.24594101953684519902
[PASS] multisets same length: 4371 vs 4371
[PASS] not isometric (max sorted-dist diff > 1e-8): max diff=0.009623924484
[PASS] candidate points strictly inside unit ball: 1-max|c|=0.2459410195
[PASS] candidate points pairwise distinct: 
RSTAR50: 0.24594101953684519902477122077410773912161071382492
OVERALL: PASS
```

Determinism: `diff run1.txt run2.txt` printed nothing and the 50-digit r* string was identical in both runs:
`0.24594101953684519902477122077410773912161071382492`.

## Property-by-property verdict

| Property | Result | Evidence |
|---|---|---|
| Exactly 94 points in candidate | PASS | 94 coordinate lines (1 comment line skipped), each with 4 fields |
| Exactly 94 points in posted file | PASS | 94 indexed rows after the radius header line |
| All candidate coordinates finite | PASS | every field parses as a finite float and as mpf |
| All centres strictly inside the unit ball | PASS | 1 - max norm = 0.2459410195... > 0 |
| Centres pairwise distinct | PASS | min pairwise distance = 0.4918820390739... > 0 |
| r* (candidate), mpmath 50 digits, no tolerance | PASS | r* = 0.24594101953684519902...; binding term is the wall term (1 - max norm); the half-min-distance term is larger by about 1.4e-13 |
| Claimed value 0.245941019536845... | PASS | matches to all digits stated in CLAIM.md; header comment r_float=0.24594101953684522 is the nearest double of my value |
| Parser sanity: posted file reproduces the table value within 1e-11 | PASS | r*(posted) = 0.24593282700485035...; table 0.245932827006; abs diff = 1.15e-12 |
| Candidate r* exceeds table value for N=94 | PASS | gain = 8.19253084519902e-06, strictly positive |
| Gain at least 1e-10 | PASS | 8.19e-06 is about 8.2e4 times the margin |
| Not isometric to posted packing (sorted distance multisets differ by more than 1e-8 somewhere) | PASS | both multisets have 4371 entries; max abs difference of sorted lists = 0.0096239, far above 1e-8 |
| Determinism across two runs | PASS | outputs byte-identical |
| Table row for N=94 present exactly once in hsp4_radius_as_fetched.txt | PASS | one row "94 0.245932827006" (file has 299 rows, 2..300) |

## Comparison with the author's REPRODUCE.md (read only after my checker had run)

The author's script uses the identical definition (min of half-min-distance and 1 - max norm, mp.dps = 50, no tolerance). I executed only its local Python block (not the curl lines, which are live-web checks outside my remit). Its output:

```
N candidate = 94  N posted = 94
r* candidate = 0.2459410195368451990247712
r* posted    = 0.2459328270048503541459008
table        = 0.245932827006
gain = r*cand - table = 8.1925308e-6  -> meets 1e-10 margin: True
max |sorted distance difference| vs posted = 0.0096239245
```

Every number agrees with my independent checker to all printed digits. No mismatch found.

## Mismatches / caveats

- No mismatch between the claim, the data files, my checker, and the author's script.
- Parsing note: the author's loader takes the last 4 fields of any line with at least 4 fields, which silently drops the posted file's index column and header radius line; my loader handles the two formats explicitly. Both yield the same 94 points.
- Out of my scope (not verified here, by instruction): the live re-fetch of radius.txt, the History-of-updates check on the live hsp4.html, and the pending-requests queue rule, including the category-unspecified 26-Sep-2026 bundle caveat stated in the success criterion. Those belong to the other panel skeptics; this verdict covers only what can be confirmed from the saved files.

pass: true
