# REPRODUCE verdict for claim N79 (hsp4, 79 balls in the unit 4-ball)

context: subagent (Claude Code Agent tool, fresh context for this one claim)

## Definition used (quoted from CLAIM.md, success criterion)

"the FEASIBLE radius r* := min( min_{i less-than j} |c_i - c_j| / 2, 1 - max_i |c_i| ) (unit container ball centred at the origin), computed in mpmath at 50 digits directly from the submitted coordinates with no tolerance, is STRICTLY GREATER (direction: max) than that file's 12-decimal value for N [...] by at least 1e-10 [...] AND the configuration is not isometric to the posted hsp[d]-[N].txt configuration (sorted pairwise-distance multisets differ by more than 1e-8 somewhere)"

(The quotation above is reproduced with the two placeholder tokens of the bank entry rewritten in square brackets and the pair-index condition spelled out as "i less-than j" because this file may not contain angle-bracket characters; the formula is otherwise verbatim.)

## Method

The checker below was written from that definition BEFORE reading REPRODUCE.md. It parses the three data files itself (candidate: comment line then 79 rows of 4 coordinates; posted: header radius then 79 rows of "index x1 x2 x3 x4"; table: rows "N radius"), rejects non-finite tokens and malformed rows, computes r* for both the candidate and the posted packing with mp.dps = 50 (every coordinate converted to mpf from its decimal string, every distance an exact-precision sqrt, no tolerance anywhere), compares against the table row for N = 79, and compares the sorted multisets of the 3081 pairwise distances. It was run twice with the venv interpreter in isolated mode (python -I), from a directory outside the claim folder, with the claim folder passed as the only argument. The script contains no comparison glyphs by design: strict less-than is done through the method call `a.__lt__(b)`.

## Checker (inline, exactly as run)

```python
# Independent checker for claim N79 (hsp4). Written from the definition:
#   r* := min( min_{i!=j} |c_i - c_j| / 2 , 1 - max_i |c_i| )
# unit container ball centred at the origin, mpmath 50 digits, no tolerance.
import sys, math
from mpmath import mp, mpf, sqrt, nstr

mp.dps = 50
claim_dir = sys.argv[1]
N_EXPECT, D = 79, 4

def lt(a, b):          # strict a less-than b, written without comparison glyphs
    return bool(a.__lt__(b))

def read_pts(path, posted_format):
    pts = []
    with open(path) as f:
        for ln in f:
            s = ln.strip()
            if not s or s.startswith('#'):
                continue
            toks = s.split()
            if len(toks) == 1 and posted_format:
                continue   # posted file: first line is the radius
            if len(toks) == D + 1:
                toks = toks[1:]  # posted file: leading index
            if len(toks) != D:
                raise SystemExit("bad line in %s: %r" % (path, ln))
            for t in toks:
                if not math.isfinite(float(t)):
                    raise SystemExit("non-finite token %r in %s" % (t, path))
            pts.append([mpf(t) for t in toks])
    return pts

def pair_dists(pts):
    n = len(pts)
    return [sqrt(sum((pts[i][k] - pts[j][k]) ** 2 for k in range(D)))
            for i in range(n) for j in range(i + 1, n)]

def rstar(pts):
    dmin = min(pair_dists(pts))
    rmax = max(sqrt(sum(x * x for x in p)) for p in pts)
    return min(dmin / 2, 1 - rmax), dmin, rmax

cand = read_pts(claim_dir + "/hsp4-79-candidate.txt", False)
post = read_pts(claim_dir + "/hsp4-79-posted.txt", True)
with open(claim_dir + "/hsp4-79-posted.txt") as f:
    posted_header = mpf(f.readline().strip())

table = None
with open(claim_dir + "/hsp4_radius_as_fetched.txt") as f:
    for ln in f:
        t = ln.split()
        if len(t) == 2 and t[0] == str(N_EXPECT):
            if table is not None:
                raise SystemExit("duplicate table row for N=79")
            table = mpf(t[1])
print("table N=79:", nstr(table, 15))
print("posted header radius:", nstr(posted_header, 15))
print("candidate count:", len(cand), "posted count:", len(post))

rc, dmin_c, rmax_c = rstar(cand)
rp, dmin_p, rmax_p = rstar(post)
print("candidate r* =", nstr(rc, 40))
print("  dmin/2 =", nstr(dmin_c / 2, 30), " 1-rmax =", nstr(1 - rmax_c, 30))
print("posted    r* =", nstr(rp, 40))
print("  dmin/2 =", nstr(dmin_p / 2, 30), " 1-rmax =", nstr(1 - rmax_p, 30))

parser_ok = lt(abs(rp - table), mpf('1e-11'))
print("posted r* - table =", nstr(rp - table, 10), " within 1e-11:", parser_ok)
margin_ok = not lt(rc - table, mpf('1e-10'))
print("candidate r* - table =", nstr(rc - table, 15), " at least 1e-10:", margin_ok)

mc, mpst = sorted(pair_dists(cand)), sorted(pair_dists(post))
maxdiff = max(abs(a - b) for a, b in zip(mc, mpst)) if len(mc) == len(mpst) else None
iso_ok = maxdiff is not None and lt(mpf('1e-8'), maxdiff)
print("pairs:", len(mc), len(mpst), " max |sorted-dist diff| =", nstr(maxdiff, 10), " exceeds 1e-8:", iso_ok)

ok = (len(cand) == N_EXPECT and len(post) == N_EXPECT and parser_ok and margin_ok and iso_ok)
print("ALL_OK:", ok)
print("RSTAR_50:", nstr(rc, 50))
```

## Real output (run 1; run 2 produced a byte-identical transcript, confirmed with cmp)

```
table N=79: 0.256468324828
posted header radius: 0.256468324828
candidate count: 79 posted count: 79
candidate r* = 0.2565657831344563132756969767574347247701
  dmin/2 = 0.256565783134627406964032400385  1-rmax = 0.256565783134456313275696976757
posted    r* = 0.2564683248265893489180661025023985844415
  dmin/2 = 0.256468324826928894310045679862  1-rmax = 0.256468324826589348918066102502
posted r* - table = -1.410651082e-12  within 1e-11: True
candidate r* - table = 9.74583064563133e-5  at least 1e-10: True
pairs: 3081 3081  max |sorted-dist diff| = 0.01576311991  exceeds 1e-8: True
ALL_OK: True
RSTAR_50: 0.25656578313445631327569697675743472477008114347708
```

## Properties and verdicts

| property | observed | verdict |
|---|---|---|
| exactly 79 points in hsp4-79-candidate.txt | 79 rows of 4 coordinates (comment line skipped) | pass |
| exactly 79 points in hsp4-79-posted.txt | 79 rows (header radius line skipped, index column dropped) | pass |
| all coordinates finite | every token passed math.isfinite(float(t)); no malformed row | pass |
| parser sanity: r*(posted) reproduces table value within 1e-11 | r*(posted) - table = -1.41e-12 | pass |
| table row for N=79 in hsp4_radius_as_fetched.txt | single row "79 0.256468324828"; posted header radius agrees | pass |
| r*(candidate) at 50 digits | 0.25656578313445631327569697675743472477008114347708; binding term is the container term 1 - max|c_i| = 0.2565657831344563..., the half-separation term is 0.2565657831346274... (slightly larger) | consistent with CLAIM.md value 0.256565783134456... and with the file comment r_float=0.25656578313445633 |
| r*(candidate) - table at least 1e-10 | 9.74583064563133e-05 (about 975000 times the margin) | pass |
| not isometric to posted packing (sorted distance multisets differ by more than 1e-8 somewhere) | 3081 vs 3081 distances; max absolute difference of sorted lists = 0.01576 | pass |
| determinism across two runs | two separate python -I invocations; transcripts byte-identical (cmp) | pass |

## Comparison with the author's REPRODUCE.md (read only after the above)

The author's script implements the same formula (min over pairs of half-distance vs 1 - max norm, mp.dps = 50, no tolerance), loads both files via the last four tokens of each line, and performs the same three checks (counts, margin against the table row, sorted-distance multiset difference). Its expected outputs agree with mine: r*(candidate) = 0.2565657831344563..., r*(posted) = 0.2564683248265893..., gain about 9.7458e-05, max sorted-distance difference about 0.015763. No mismatch between my independent computation and the author's claimed numbers.

## Not verified here (outside this skeptic's remit)

The success criterion also requires a live re-fetch of radius.txt, the hsp4.html history-of-updates and the pending-requests queue page. I did not fetch the web; I verified only against the saved snapshot hsp4_radius_as_fetched.txt (row "79 0.256468324828"). The CLAIM.md caveat about the category-unspecified "Moki and Julio many 4666 candidates" bundle on the pending list stands and must be re-checked by whoever owns the live-status check. My pass is therefore for the mathematical object and the margin against the snapshot table, which is what this REPRODUCE role was asked to confirm.

## Mismatches

None found.

pass: true
