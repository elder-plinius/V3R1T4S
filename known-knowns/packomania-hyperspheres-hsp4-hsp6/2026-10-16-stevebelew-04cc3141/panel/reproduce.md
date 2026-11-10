# REPRODUCE verdict for claim N80 (hsp4, N = 80)

context: subagent (Claude Code Agent tool, fresh context for this one claim)

## Scope

Files examined (names relative to the claim folder): CLAIM.md, hsp4-80-candidate.txt, hsp4-80-posted.txt, hsp4_radius_as_fetched.txt, and REPRODUCE.md (the last one read only after my own checker had been written and run). No web fetches were made; the live re-fetch / queue / history-of-updates steps in REPRODUCE.md are therefore NOT part of this verdict and remain for whoever owns the network check.

## Definition used (quoted from the success criterion in CLAIM.md)

"the FEASIBLE radius r* := min( min_{i lt j} |c_i - c_j| / 2, 1 - max_i |c_i| ) (unit container ball centred at the origin), computed in mpmath at 50 digits directly from the submitted coordinates with no tolerance, is STRICTLY GREATER (direction: max) than that file's 12-decimal value for N re-fetched live immediately before claiming, by at least 1e-10 [...] AND the configuration is not isometric to the posted hsp4-80.txt configuration (sorted pairwise-distance multisets differ by more than 1e-8 somewhere)"

(In the quote above the original pair index is written with the less-than sign, i strictly less than j; that one character is spelled out as "lt" here so this file contains no bracket characters. The checker loops j from i+1 to n-1, which is the same set of unordered pairs.)

Interpretation applied: coordinates parsed as exact decimal strings into mpf at mp.dps = 50; Euclidean norm via sqrt of the sum of squares; r* is the minimum of (half the smallest pairwise distance) and (1 minus the largest centre norm); no epsilon anywhere; table value taken from the row whose first token is exactly "80".

## My checker (written before reading REPRODUCE.md; run with the venv interpreter and -I from inside the claim folder, arguments: hsp4-80-candidate.txt hsp4-80-posted.txt hsp4_radius_as_fetched.txt)

```python
# Independent checker written from the bank definition BEFORE reading REPRODUCE.md.
# Definition used (from CLAIM.md success criterion):
#   r* := min( min over pairs i,j (i not equal j) of |c_i - c_j| / 2 , 1 - max_i |c_i| )
#   (unit container ball centred at the origin), computed in mpmath at 50 digits
#   directly from the submitted coordinates with no tolerance.
import sys, math
from mpmath import mp, mpf, sqrt, nstr

mp.dps = 50
D = 4
N_EXPECTED = 80
cand_path, posted_path, radius_path = sys.argv[1:4]

def read_points(path, skip_comment=True):
    pts = []
    with open(path) as f:
        lines = f.read().splitlines()
    for ln in lines:
        s = ln.strip()
        if not s:
            continue
        if skip_comment and s.startswith('#'):
            continue
        toks = s.split()
        if len(toks) != D:
            raise SystemExit(f"FAIL: line with {len(toks)} coordinate tokens (expected {D}): {ln!r}")
        for t in toks:
            fv = float(t)
            if not math.isfinite(fv):
                raise SystemExit(f"FAIL: non-finite coordinate {t!r}")
        pts.append([mpf(t) for t in toks])   # exact decimal string to mpf at 50 digits
    return pts

def norm(v):
    return sqrt(sum(x*x for x in v))

def rstar(pts):
    n = len(pts)
    dmin = None
    dists = []
    for i in range(n):
        for j in range(i+1, n):
            d = norm([pts[i][k]-pts[j][k] for k in range(D)])
            dists.append(d)
            dmin = d if dmin is None else min(dmin, d)
    rmax = max(norm(p) for p in pts)
    return min(dmin/2, 1 - rmax), dmin, rmax, sorted(dists)

# --- candidate ---
cand = read_points(cand_path)
print("candidate: n_points =", len(cand))
if len(cand) != N_EXPECTED:
    raise SystemExit("FAIL: candidate does not have exactly 80 points")
rc, dmin_c, rmax_c, dist_c = rstar(cand)
print("candidate: min pair dist  =", nstr(dmin_c, 30))
print("candidate: max |c_i|      =", nstr(rmax_c, 30))
print("candidate: dmin/2         =", nstr(dmin_c/2, 30))
print("candidate: 1 - max|c_i|   =", nstr(1-rmax_c, 30))
print("candidate: r*             =", nstr(rc, 30))
print("candidate: binding term   =", "pair" if min(dmin_c/2, 1-rmax_c) == dmin_c/2 else "container")

# --- table value ---
table = None
rows = 0
with open(radius_path) as f:
    for ln in f:
        toks = ln.split()
        if len(toks) != 2:
            continue
        rows += 1
        if toks[0] == str(N_EXPECTED):
            if table is not None:
                raise SystemExit("FAIL: duplicate row for N=80 in radius file")
            table = mpf(toks[1])
print("radius file: rows parsed   =", rows)
if table is None:
    raise SystemExit("FAIL: no row for N=80 in radius file")
print("table value N=80           =", nstr(table, 20))

# --- posted packing (parser sanity) ---
with open(posted_path) as f:
    first = f.readline().strip()
posted_hdr = mpf(first)
print("posted header radius       =", nstr(posted_hdr, 20))
posted_lines = open(posted_path).read().splitlines()[1:]
posted = []
for ln in posted_lines:
    toks = ln.split()
    if not toks:
        continue
    if len(toks) != D+1:
        raise SystemExit(f"FAIL: posted line malformed: {ln!r}")
    for t in toks[1:]:
        if not math.isfinite(float(t)):
            raise SystemExit(f"FAIL: non-finite posted coordinate {t!r}")
    posted.append([mpf(t) for t in toks[1:]])
print("posted: n_points           =", len(posted))
if len(posted) != N_EXPECTED:
    raise SystemExit("FAIL: posted does not have exactly 80 points")
rp, dmin_p, rmax_p, dist_p = rstar(posted)
print("posted: r* recomputed      =", nstr(rp, 30))
print("posted: |r*_posted - table| =", nstr(abs(rp-table), 10))
print("posted: |hdr - table|       =", nstr(abs(posted_hdr-table), 10))
ok_posted = max(abs(rp-table), mpf('1e-11')) == mpf('1e-11')

# --- improvement ---
gain = rc - table
print("gain = r*_cand - table     =", nstr(gain, 20))
ok_gain = min(gain, mpf('1e-10')) == mpf('1e-10')

# --- non-isometry ---
if len(dist_c) != len(dist_p) or len(dist_c) != N_EXPECTED*(N_EXPECTED-1)//2:
    raise SystemExit("FAIL: distance multiset size mismatch")
maxdiff = max(abs(a-b) for a, b in zip(dist_c, dist_p))
print("sorted-dist multiset max |diff| =", nstr(maxdiff, 15))
ok_iso = (max(maxdiff, mpf('1e-8')) == maxdiff) and (maxdiff != mpf('1e-8'))

# --- claim's stated value ---
claimed = mpf('0.255469606984850')
print("|r*_cand - claimed 0.255469606984850| =", nstr(abs(rc-claimed), 10))

print("DETERMINISM_STRING r*_cand =", nstr(rc, 50))
print("PASS posted reproduces table within 1e-11:", ok_posted)
print("PASS gain at least 1e-10:", ok_gain)
print("PASS non-isometric (exceeds 1e-8):", ok_iso)
print("OVERALL:", "PASS" if (ok_posted and ok_gain and ok_iso) else "FAIL")
```

## Real output (run 1; run 2 was byte-identical, verified with cmp)

```
candidate: n_points = 80
candidate: min pair dist  = 0.510939213998247082182979046493
candidate: max |c_i|      = 0.744530393015150238856197520052
candidate: dmin/2         = 0.255469606999123541091489523247
candidate: 1 - max|c_i|   = 0.255469606984849761143802479948
candidate: r*             = 0.255469606984849761143802479948
candidate: binding term   = container
radius file: rows parsed   = 299
table value N=80           = 0.255463163131
posted header radius       = 0.255463163131
posted: n_points           = 80
posted: r* recomputed      = 0.255463163130597809686736932998
posted: |r*_posted - table| = 4.021903133e-13
posted: |hdr - table|       = 0.0
gain = r*_cand - table     = 6.4438538497611438025e-6
sorted-dist multiset max |diff| = 0.0122062833609007
|r*_cand - claimed 0.255469606984850| = 2.388561975e-16
DETERMINISM_STRING r*_cand = 0.25546960698484976114380247994819295250762415251867
PASS posted reproduces table within 1e-11: True
PASS gain at least 1e-10: True
PASS non-isometric (exceeds 1e-8): True
OVERALL: PASS
```

## Property-by-property verdicts

1. Exactly 80 points in the candidate, each with 4 coordinates: PASS (n_points = 80; one leading comment line skipped; every data line has exactly 4 tokens).
2. All coordinates finite: PASS (each token passes float() and math.isfinite(); same check applied to the posted file).
3. r* of candidate at 50 digits, no tolerance: 0.25546960698484976114380247994819295250762415251867. The binding constraint is the container (1 - max|c_i|), and half the minimum pair distance is about 1.4e-11 larger, so the packing is container-limited with the pair constraint essentially active as well. PASS (computed; matches the claim's stated 0.255469606984850... to 2.4e-16, i.e. the claimed value is a correct rounding).
4. Table value for N = 80 parsed from hsp4_radius_as_fetched.txt: 0.255463163131 (299 rows parsed, exactly one row for 80). PASS.
5. Parser sanity, posted file reproduces the table value within 1e-11: PASS (r* recomputed from the 80 posted coordinates = 0.2554631631305978..., differing from the table by 4.02e-13; the file's first-line radius equals the table value exactly).
6. Improvement margin at least 1e-10: PASS (gain = 6.44385384976e-06, about 64,000 times the required margin; strictly greater).
7. Not isometric to posted packing (sorted pairwise-distance multisets differ by more than 1e-8 somewhere): PASS (3160 distances each; maximum absolute difference between the sorted multisets = 0.0122, six orders of magnitude above the threshold).
8. Determinism of r* across two runs: PASS (two independent runs of the checker produced byte-identical output, including the 50-digit r* string).

## Comparison with the author's REPRODUCE.md (read afterwards)

The author's Python block uses the same definition (min of dmin/2 and 1 - max norm, mp.dps = 50, no tolerance, mpf from decimal strings). I extracted that block and ran it offline once; its printed values agree with mine to every printed digit: r* candidate 0.2554696069848497611438025, r* posted 0.2554631631305978096867369, table 0.255463163131, gain 6.4438538e-6, max sorted-distance difference 0.012206283. No mismatch found between the author's reproduction and my independent one.

Author parsing note: their loader takes the last 4 tokens of any line with at least 4 tokens, which happens to be correct for both files here (comment line excluded by the '#' test, and the posted file's index column is dropped). My loader is stricter (requires exactly 4 or exactly 5 tokens respectively) and reached the same point sets.

## Caveats (outside what this verdict can certify)

- The live re-fetch of radius.txt, the hsp4.html history-of-updates check, and the pending-requests queue check (including the category-unspecified 26-Sep-2026 bundle caveat named in the success criterion) were not performed here; no network access was used.
- hsp4-80-posted.txt was taken as the posted packing as supplied in the claim folder; its provenance from the tarball was not independently verified.

## Mismatches

None.

pass: true
