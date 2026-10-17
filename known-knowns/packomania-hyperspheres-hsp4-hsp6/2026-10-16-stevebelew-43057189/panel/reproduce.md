# REPRODUCE verdict for claim N89 (hsp4, 89 balls in the unit 4-ball)

context: subagent (Claude Code Agent tool, fresh context for this one claim)

Scope: only the claim folder was read (CLAIM.md, hsp4-89-candidate.txt, hsp4-89-posted.txt, hsp4_radius_as_fetched.txt, and REPRODUCE.md last). No web fetch was made, so the "re-fetched live" conditions (table value, History-of-updates, pending-requests queue) are judged ONLY against the snapshot files; see the caveat at the end.

## Definition used (quoted from CLAIM.md, success criterion)

"the FEASIBLE radius r* := min( min_{i<j} |c_i - c_j| / 2, 1 - max_i |c_i| ) (unit container ball centred at the origin), computed in mpmath at 50 digits directly from the submitted coordinates with no tolerance, is STRICTLY GREATER (direction: max) than that file's 12-decimal value for N re-fetched live immediately before claiming, by at least 1e-10 [...], AND the configuration is not isometric to the posted hsp[d]-[N].txt configuration (sorted pairwise-distance multisets differ by more than 1e-8 somewhere)"

Parsing rules I applied (from the Files section of CLAIM.md): candidate = skip lines starting with "#", each remaining non-empty line must have exactly 4 fields; posted = first line is the radius, each later line is "index x1 x2 x3 x4" (5 fields, index dropped); table = the unique row whose first field is "89".

## My checker (written before opening REPRODUCE.md; run with the panel venv python and -I; mpmath 1.4.1, Python 3.14.7)

```python
# Independent checker for the N=89 hsp4 claim, written from the definition:
#   r* := min( min_{i<j} |c_i - c_j| / 2 , 1 - max_i |c_i| ),  unit ball container centred at the origin,
#   computed in mpmath at 50 digits directly from the submitted coordinates with no tolerance.
import sys, re
from mpmath import mp, mpf, sqrt
mp.dps = 50
D = sys.argv[1]  # claim folder
N_EXPECT = 89
MARGIN = mpf('1e-10')
ISO_TOL = mpf('1e-8')
PARSE_TOL = mpf('1e-11')

def read_candidate(path):
    pts = []
    with open(path) as f:
        for ln in f:
            s = ln.strip()
            if not s or s.startswith('#'):
                continue
            parts = s.split()
            if len(parts) != 4:
                raise SystemExit(f'FAIL: candidate line with {len(parts)} fields: {s!r}')
            pts.append([mpf(p) for p in parts])
    return pts

def read_posted(path):
    with open(path) as f:
        lines = [l.strip() for l in f if l.strip()]
    head = mpf(lines[0])
    pts = []
    for s in lines[1:]:
        parts = s.split()
        if len(parts) != 5:
            raise SystemExit(f'FAIL: posted line with {len(parts)} fields: {s!r}')
        pts.append([mpf(p) for p in parts[1:]])
    return head, pts

def read_table(path, n):
    vals = []
    with open(path) as f:
        for l in f:
            parts = l.split()
            if len(parts) == 2 and parts[0] == str(n):
                vals.append(mpf(parts[1]))
    if len(vals) != 1:
        raise SystemExit(f'FAIL: table has {len(vals)} rows for N={n}')
    return vals[0]

def norm(v):
    return sqrt(sum(x*x for x in v))

def dist(a, b):
    return sqrt(sum((x-y)*(x-y) for x, y in zip(a, b)))

def rstar(pts):
    n = len(pts)
    dmin = None
    for i in range(n):
        for j in range(i+1, n):
            d = dist(pts[i], pts[j])
            if dmin is None or d < dmin:
                dmin = d
    rmax = max(norm(p) for p in pts)
    return min(dmin/2, 1 - rmax), dmin, rmax

def pairwise_sorted(pts):
    n = len(pts)
    return sorted(dist(pts[i], pts[j]) for i in range(n) for j in range(i+1, n))

ok = True
def check(name, cond, detail=''):
    global ok
    print(f'[{"PASS" if cond else "FAIL"}] {name} {detail}')
    ok = ok and bool(cond)

cand = read_candidate(f'{D}/hsp4-89-candidate.txt')
posted_head, posted = read_posted(f'{D}/hsp4-89-posted.txt')
table = read_table(f'{D}/hsp4_radius_as_fetched.txt', N_EXPECT)

check('candidate has exactly 89 points', len(cand) == N_EXPECT, f'count={len(cand)}')
check('posted has exactly 89 points', len(posted) == N_EXPECT, f'count={len(posted)}')
check('all candidate coords finite', all(x.is_finite for p in cand for x in p) if hasattr(mpf(0),'is_finite') else all(mp.isfinite(x) for p in cand for x in p))
check('all candidate coords |x|<1 (sanity)', all(abs(x) < 1 for p in cand for x in p))
check('no duplicate candidate points', len({tuple(str(x) for x in p) for p in cand}) == N_EXPECT)

print('table value N=89 :', mp.nstr(table, 20))
print('posted header     :', mp.nstr(posted_head, 20))
rp, dmin_p, rmax_p = rstar(posted)
print('r*(posted)        :', mp.nstr(rp, 30), ' dmin/2=', mp.nstr(dmin_p/2, 25), ' 1-rmax=', mp.nstr(1-rmax_p, 25))
check('posted reproduces table within 1e-11', abs(rp - table) <= PARSE_TOL, f'|diff|={mp.nstr(abs(rp-table), 5)}')

rc, dmin_c, rmax_c = rstar(cand)
print('r*(candidate)     :', mp.nstr(rc, 50))
print('   dmin/2          =', mp.nstr(dmin_c/2, 30))
print('   1 - max|c_i|    =', mp.nstr(1-rmax_c, 30))
print('   r* - table      =', mp.nstr(rc - table, 15))
check('r*(candidate) - table >= 1e-10', rc - table >= MARGIN, f'gain={mp.nstr(rc-table, 10)}')
check('r*(candidate) > table (strict)', rc > table)
check('r*(candidate) > r*(posted)', rc > rp)

pc = pairwise_sorted(cand)
pp = pairwise_sorted(posted)
check('pair counts equal (89*88/2=3916)', len(pc) == len(pp) == 3916, f'{len(pc)} {len(pp)}')
maxdev = max(abs(a-b) for a, b in zip(pc, pp))
print('max |sorted pairdist diff| =', mp.nstr(maxdev, 10))
check('not isometric to posted (max sorted-pairdist diff > 1e-8)', maxdev > ISO_TOL)

print('RSTAR_CANDIDATE_50DIGITS', mp.nstr(rc, 50))
print('OVERALL', 'PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
```

## Real output, run 1 (invoked as: python -I check_n89.py [claim folder])

```
[PASS] candidate has exactly 89 points count=89
[PASS] posted has exactly 89 points count=89
[PASS] all candidate coords finite 
[PASS] all candidate coords |x|<1 (sanity) 
[PASS] no duplicate candidate points 
table value N=89 : 0.247998099891
posted header     : 0.247998099891
r*(posted)        : 0.247998099890338111219262697242  dmin/2= 0.2479980998904599218802714  1-rmax= 0.2479980998903381112192627
[PASS] posted reproduces table within 1e-11 |diff|=6.6189e-13
r*(candidate)     : 0.24800542008440667899066559596859197503166605598113
   dmin/2          = 0.248005420084733576975895069645
   1 - max|c_i|    = 0.248005420084406678990665595969
   r* - table      = 7.32019340667899e-6
[PASS] r*(candidate) - table >= 1e-10 gain=7.320193407e-6
[PASS] r*(candidate) > table (strict) 
[PASS] r*(candidate) > r*(posted) 
[PASS] pair counts equal (89*88/2=3916) 3916 3916
max |sorted pairdist diff| = 0.01120635152
[PASS] not isometric to posted (max sorted-pairdist diff > 1e-8) 
RSTAR_CANDIDATE_50DIGITS 0.24800542008440667899066559596859197503166605598113
OVERALL PASS
```

## Run 2 (determinism)

Run 2 output was byte-identical to run 1 (verified with diff). Both runs give
r*(candidate) = 0.24800542008440667899066559596859197503166605598113 (50 digits).

## Property-by-property verdict

| Property | Result | Verdict |
|---|---|---|
| Exactly 89 points in candidate (python count and an independent awk count) | 89, all lines have 4 fields | PASS |
| All candidate coordinates finite (mpmath isfinite), all |x| strictly below 1, no duplicate rows | true | PASS |
| Posted file parses to 89 points | 89 | PASS |
| Parser sanity: r*(posted) vs table value 0.247998099891 within 1e-11 | r*(posted) = 0.2479980998903381..., diff 6.6e-13 | PASS |
| r*(candidate) at 50 digits, no tolerance | 0.248005420084406678990665595968... ; binding term is 1 - max|c_i| (= 0.24800542008440667...), pair term dmin/2 = 0.24800542008473357... | computed |
| r*(candidate) strictly greater than table value by at least 1e-10 | gain = 7.3201934e-06 (about 73,000x the margin) | PASS |
| r*(candidate) greater than r*(posted) | 0.2480054... vs 0.2479981... | PASS |
| Not isometric to posted: sorted pairwise-distance multisets (3916 each) differ by more than 1e-8 somewhere | max abs difference = 0.0112 | PASS |
| Deterministic across two runs | identical output | PASS |
| Claimed value in CLAIM.md "0.248005420084407..." and comment-line r_float=0.24800542008440662 | consistent with the 50-digit value (rounded / double precision) | PASS |

Mismatches found: none.

## Comparison with the author's REPRODUCE.md (read only after my runs)

The author's snippet uses the same definition and the same parsing of the three files. I ran it from a scratch copy of the data files: N candidate = 89, N posted = 89, r* candidate = 0.2480054200844066789906656, r* posted = 0.2479980998903381112192627, table = 0.247998099891, gain = 7.3201934e-6 (margin met: True), max sorted-distance difference = 0.011206352. Every number agrees with my checker to all printed digits. Minor note: the author's loader accepts any line with at least 4 fields and takes the last 4, which is looser than my strict 4-field / 5-field parsing, but on these files both parsers yield the same 89 points.

The three curl commands in REPRODUCE.md (live table row, Last update, pending-requests) were NOT executed by me (no web access permitted for this role). The snapshot hsp4_radius_as_fetched.txt carries the row "89 0.247998099891" and CLAIM.md states it was byte-identical to the 2026-10-14 fetches; the History-of-updates and QUEUE RULE conditions, and the bank's caveat about the category-unspecified "Moki & Julio *many* 4666 candidates" bundle, remain for whichever panel member holds the live-fetch duty.

## Conclusion

Every property I could verify from the saved files holds, with a wide margin and no mismatch against the author's figures. The reproduce check of the mathematical object passes.

pass: true
