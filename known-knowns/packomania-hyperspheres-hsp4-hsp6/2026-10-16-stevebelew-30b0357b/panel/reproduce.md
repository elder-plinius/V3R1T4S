# REPRODUCE verdict for claim N67 (hsp4, d=4, N=67)

context: subagent (Claude Code Agent tool, fresh context for this one claim)

## Definition used (quoted from CLAIM.md, "Success criterion" section)

"the FEASIBLE radius r* := min( min_{i<j} |c_i - c_j| / 2, 1 - max_i |c_i| ) (unit container ball centred at the origin), computed in mpmath at 50 digits directly from the submitted coordinates with no tolerance, is STRICTLY GREATER (direction: max) than that file's 12-decimal value for N re-fetched live immediately before claiming, by at least 1e-10 [...] AND the configuration is not isometric to the posted [...] configuration (sorted pairwise-distance multisets differ by more than 1e-8 somewhere)"

Note: the elided fragment in the quotation is the bank entry's generic file-name placeholder; in this claim folder that file is hsp4-67-posted.txt.

## Method

Checker written from the definition above BEFORE reading REPRODUCE.md. Inputs: hsp4-67-candidate.txt (comment line then 67 lines of 4 coordinates), hsp4-67-posted.txt (first line radius, then "index x1 x2 x3 x4"), hsp4_radius_as_fetched.txt (rows "N radius"). Run with the project venv interpreter in isolated mode (python -I), mpmath 1.4.1, mp.dps = 50. Parsing is strict: a candidate line must have exactly 4 tokens, a posted line exactly 5, every coordinate must be finite. Executed four times in total (two with the original comparison operators, two after a cosmetic rewrite to operator.lt/ge/gt); all four runs printed the same 50-digit r*.

## Checker code (as run)

```python
#!/usr/bin/env python
# Independent REPRODUCE checker for N=67, d=4.
# Definition used (verbatim from the bank entry):
#   r* := min( min_{i<j} |c_i - c_j| / 2 , 1 - max_i |c_i| )
#   unit container ball centred at the origin; mpmath at 50 digits, no tolerance.
import sys, math, hashlib, operator
from mpmath import mp, mpf, sqrt, nstr

mp.dps = 50
D = sys.argv[1].rstrip('/') + '/'
N_EXPECTED, DIM = 67, 4

def read_candidate(path):
    pts = []
    for ln in open(path):
        s = ln.strip()
        if not s or s.startswith('#'):
            continue
        toks = s.split()
        if len(toks) != DIM:
            raise SystemExit(f'bad token count in candidate line: {s!r}')
        for t in toks:
            if not math.isfinite(float(t)):
                raise SystemExit(f'non-finite coordinate: {t!r}')
        pts.append([mpf(t) for t in toks])
    return pts

def read_posted(path):
    lines = [l.strip() for l in open(path) if l.strip()]
    r_posted = mpf(lines[0])
    pts = []
    for s in lines[1:]:
        toks = s.split()
        if len(toks) != DIM + 1:
            raise SystemExit(f'bad token count in posted line: {s!r}')
        for t in toks[1:]:
            if not math.isfinite(float(t)):
                raise SystemExit(f'non-finite coordinate: {t!r}')
        pts.append([mpf(t) for t in toks[1:]])
    return r_posted, pts

def dist(a, b):
    return sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

def rstar(pts):
    n = len(pts)
    dmin = None
    for i in range(n):
        for j in range(i + 1, n):
            dij = dist(pts[i], pts[j])
            dmin = dij if dmin is None else min(dmin, dij)
    nmax = max(sqrt(sum(x * x for x in p)) for p in pts)
    return min(dmin / 2, 1 - nmax), dmin, nmax

def table_value(path, n):
    rows = {}
    for ln in open(path):
        toks = ln.split()
        if len(toks) == 2 and toks[0].isdigit():
            rows[int(toks[0])] = mpf(toks[1])
    if n not in rows:
        raise SystemExit(f'N={n} not in table')
    return rows[n], len(rows)

def sorted_dists(pts):
    out = []
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            out.append(dist(pts[i], pts[j]))
    return sorted(out)

ok = True
def check(name, cond, detail=''):
    global ok
    print(f'[{"PASS" if cond else "FAIL"}] {name} {detail}')
    ok = ok and bool(cond)

for f in ('hsp4-67-candidate.txt', 'hsp4-67-posted.txt', 'hsp4_radius_as_fetched.txt'):
    h = hashlib.sha256(open(D + f, 'rb').read()).hexdigest()
    print(f'sha256 {f} {h}')

cand = read_candidate(D + 'hsp4-67-candidate.txt')
r_posted_hdr, posted = read_posted(D + 'hsp4-67-posted.txt')
tbl, nrows = table_value(D + 'hsp4_radius_as_fetched.txt', N_EXPECTED)

check('candidate has exactly 67 points', len(cand) == N_EXPECTED, f'(got {len(cand)})')
check('posted has exactly 67 points', len(posted) == N_EXPECTED, f'(got {len(posted)})')
print(f'table rows parsed: {nrows}; table value N=67: {nstr(tbl, 15)}; posted header radius: {nstr(r_posted_hdr, 15)}')

rc, dmin_c, nmax_c = rstar(cand)
rp, dmin_p, nmax_p = rstar(posted)
print(f'candidate: dmin/2 = {nstr(dmin_c/2, 30)}  1-maxnorm = {nstr(1-nmax_c, 30)}  r* = {nstr(rc, 30)}')
print(f'posted:    dmin/2 = {nstr(dmin_p/2, 30)}  1-maxnorm = {nstr(1-nmax_p, 30)}  r* = {nstr(rp, 30)}')

check('posted r* reproduces table within 1e-11', operator.lt(abs(rp - tbl), mpf('1e-11')), f'(|diff| = {nstr(abs(rp-tbl), 5)})')
check('candidate r* exceeds table by at least 1e-10', operator.ge(rc - tbl, mpf('1e-10')), f'(gain = {nstr(rc - tbl, 10)})')
check('candidate r* matches claimed 0.264072205869627 prefix', nstr(rc, 15).startswith('0.26407220586962'), f'({nstr(rc, 18)})')

sc, sp = sorted_dists(cand), sorted_dists(posted)
maxdiff = max(abs(a - b) for a, b in zip(sc, sp))
check('not isometric: sorted distance multisets differ by more than 1e-8', operator.gt(maxdiff, mpf('1e-8')), f'(max |diff| = {nstr(maxdiff, 8)})')

print('RSTAR_FULL', nstr(rc, 50))
print('ALL_OK' if ok else 'SOME_FAIL')
```

## Checker output (real, pasted from the final two runs; both identical)

```
sha256 hsp4-67-candidate.txt 30b0357b0e0fac886b7c32056596295be33bdbc5ab65b1223f80259be068e2eb
sha256 hsp4-67-posted.txt ec917e3b1e82deb1292877b25fb55f92d3a2d0ab82b7cc808cd740d45b9b4ee4
sha256 hsp4_radius_as_fetched.txt f3ddaa944aac014718bc9f5438700698abedac0189266198df8bb60772ac569f
[PASS] candidate has exactly 67 points (got 67)
[PASS] posted has exactly 67 points (got 67)
table rows parsed: 299; table value N=67: 0.264026543809; posted header radius: 0.264026543809
candidate: dmin/2 = 0.264072205869651371578326261546  1-maxnorm = 0.264072205869627219605564806722  r* = 0.264072205869627219605564806722
posted:    dmin/2 = 0.264026543808919647940136748252  1-maxnorm = 0.264026543808506680099370792774  r* = 0.264026543808506680099370792774
[PASS] posted r* reproduces table within 1e-11 (|diff| = 4.9332e-13)
[PASS] candidate r* exceeds table by at least 1e-10 (gain = 4.566206063e-5)
[PASS] candidate r* matches claimed 0.264072205869627 prefix (0.26407220586962722)
[PASS] not isometric: sorted distance multisets differ by more than 1e-8 (max |diff| = 0.015099516)
RSTAR_FULL 0.26407220586962721960556480672169240390901697055044
ALL_OK
```

Determinism: the two consecutive runs were diffed byte-for-byte and were identical (the earlier pair with the original operators likewise identical, same RSTAR_FULL line).

## Properties and verdicts

| Property | Result | Verdict |
|---|---|---|
| Exactly 67 points in hsp4-67-candidate.txt, each with 4 finite coordinates | 67 points, all finite, strict 4-token parse | PASS |
| Exactly 67 points in hsp4-67-posted.txt | 67 points, all finite | PASS |
| Table parser sanity: r* of posted file equals table row "67 0.264026543809" within 1e-11 | r*(posted) = 0.26402654380850668...; abs diff = 4.93e-13 | PASS |
| Posted file header radius equals table row | both 0.264026543809 | PASS |
| r*(candidate) at 50 digits, no tolerance | 0.26407220586962721960556480672169240390901697055044 (binding constraint: container, 1 - max norm; pair term is larger by 2.4e-14) | computed |
| Claimed value 0.264072205869627... reproduced | matches to all stated digits | PASS |
| r*(candidate) exceeds table value by at least 1e-10 | gain = 4.566206063e-05 (matches CLAIM.md "about 4.57e-05") | PASS |
| Not isometric to posted: sorted pairwise-distance multisets differ by more than 1e-8 somewhere | max abs difference between sorted multisets = 0.0151 | PASS |
| Determinism of r*(candidate) across two runs | byte-identical output | PASS |

## Comparison with the author's REPRODUCE.md (read only after the above)

The author's script implements the same definition (min over pairs of half-distance, min with 1 minus max norm; mp.dps = 50; sorted-distance comparison). Its loader is looser than mine (takes the last 4 tokens of any line with at least 4 tokens, and uses "len(parts) less than 4" to skip the posted header), but on these three files it selects exactly the same 67 + 67 points, so results agree. Its printed quantities (N, r* candidate, r* posted, table, gain, max sorted-distance difference) correspond one-to-one to the values above. No mismatch found.

Not performed: the three live curl checks listed at the end of REPRODUCE.md (live radius.txt row, "Last update" line, pending-requests page). Web access was outside this panel's remit; those items are the scout's and are not part of this REPRODUCE verdict. The queue caveat in CLAIM.md about the category-unspecified 26-Sep-2026 bundle therefore stands unresolved here, as the bank entry requires it to be stated.

## Mismatches

None. Every property in the success criterion that can be checked from the saved files holds, the claimed r* value and gain reproduce exactly, and the computation is deterministic.

pass: true
