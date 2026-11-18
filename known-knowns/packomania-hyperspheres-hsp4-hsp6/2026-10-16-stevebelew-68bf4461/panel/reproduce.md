# REPRODUCE verdict for claim N81 (hsp4, 81 balls in the unit 4-ball)

context: subagent (Claude Code Agent tool, fresh context for this one claim)

## Scope and method

I read only the claim folder: CLAIM.md, then hsp4-81-candidate.txt, hsp4-81-posted.txt, hsp4_radius_as_fetched.txt. I wrote my own checker from the definition BEFORE opening REPRODUCE.md, ran it twice with the project venv's Python (invoked with -I) and mpmath at 50 digits, and only then compared with the author's script. No web access was used; the live re-fetch, History-of-updates and pending-requests checks in the success criterion are outside this REPRODUCE lane and are not asserted here.

## Definition used (quoted from CLAIM.md, success criterion)

"the FEASIBLE radius r* := min( min over index pairs i,j with i before j of |c_i - c_j| / 2, 1 - max_i |c_i| ) (unit container ball centred at the origin), computed in mpmath at 50 digits directly from the submitted coordinates with no tolerance, is STRICTLY GREATER (direction: max) than that file's 12-decimal value for N re-fetched live immediately before claiming, by at least 1e-10 [...], AND the configuration is not isometric to the posted hsp[d]-[N].txt configuration (sorted pairwise-distance multisets differ by more than 1e-8 somewhere)"

(Quoted from CLAIM.md with two notational substitutions so this file carries no angle-bracket tokens: the pair condition is written out in words instead of the original subscript, and the file-name placeholders use square brackets; for d=4, N=81 that placeholder is hsp4-81-posted.txt.)

Inputs, by name relative to the claim folder:
- hsp4-81-candidate.txt: one comment line, then 81 lines of 4 coordinates.
- hsp4-81-posted.txt: first line is the posted radius, then 81 lines "index x1 x2 x3 x4".
- hsp4_radius_as_fetched.txt: 299 rows "N radius"; the row for N=81 reads "81 0.254058669351".

## My checker (check_n81.py, run as: python -I check_n81.py CLAIMDIR)

```python
# Independent REPRODUCE checker for claim N81 (hsp4), written from the definition:
#   r* := min( min_{i,j, i before j} |c_i - c_j| / 2 , 1 - max_i |c_i| )
#   unit container ball centred at the origin, mpmath at 50 digits, no tolerance.
import sys, math, operator as op
from mpmath import mp, mpf, sqrt, nstr
mp.dps = 50

claim_dir = sys.argv[1]
CAND = claim_dir + "/hsp4-81-candidate.txt"
POST = claim_dir + "/hsp4-81-posted.txt"
TABLE = claim_dir + "/hsp4_radius_as_fetched.txt"
N_EXPECTED = 81
D = 4

def load_candidate(path):
    pts = []
    for raw in open(path):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        toks = line.split()
        if len(toks) != D:
            raise SystemExit("candidate: bad token count %d on line %r" % (len(toks), line))
        pts.append([mpf(t) for t in toks])
    return pts

def load_posted(path):
    lines = [l.strip() for l in open(path) if l.strip()]
    header_r = mpf(lines[0])
    pts = []
    for line in lines[1:]:
        toks = line.split()
        if len(toks) != D + 1:
            raise SystemExit("posted: bad token count %d on line %r" % (len(toks), line))
        pts.append([mpf(t) for t in toks[1:]])
    return header_r, pts

def load_table(path, n):
    val = None
    for line in open(path):
        toks = line.split()
        if len(toks) == 2 and toks[0] == str(n):
            if val is not None:
                raise SystemExit("table: duplicate row for N")
            val = mpf(toks[1])
    if val is None:
        raise SystemExit("table: no row for N")
    return val

def all_finite(pts):
    return all(math.isfinite(float(x)) for p in pts for x in p)

def norm(p):
    return sqrt(sum(x * x for x in p))

def dist(p, q):
    return sqrt(sum((a - b) * (a - b) for a, b in zip(p, q)))

def feasible_radius(pts):
    n = len(pts)
    dmin = min(dist(pts[i], pts[j]) for i in range(n) for j in range(i + 1, n))
    maxnorm = max(norm(p) for p in pts)
    return min(dmin / 2, 1 - maxnorm), dmin, maxnorm

def sorted_pairdists(pts):
    n = len(pts)
    return sorted(dist(pts[i], pts[j]) for i in range(n) for j in range(i + 1, n))

cand = load_candidate(CAND)
post_hdr, post = load_posted(POST)
table = load_table(TABLE, N_EXPECTED)

ok = True
def prop(name, cond, detail=""):
    global ok
    print("[%s] %s %s" % ("PASS" if cond else "FAIL", name, detail))
    ok = ok and cond

prop("candidate has exactly 81 points", len(cand) == N_EXPECTED, "(got %d)" % len(cand))
prop("posted has exactly 81 points", len(post) == N_EXPECTED, "(got %d)" % len(post))
prop("candidate coordinates all finite", all_finite(cand))
prop("candidate dimension is 4", all(len(p) == D for p in cand))

r_cand, dmin_c, mx_c = feasible_radius(cand)
r_post, dmin_p, mx_p = feasible_radius(post)
print("table value N=81     :", nstr(table, 20))
print("posted header radius :", nstr(post_hdr, 20))
print("r*(posted)  50 digits:", nstr(r_post, 50))
print("   posted min dist/2 :", nstr(dmin_p / 2, 30), " 1-maxnorm:", nstr(1 - mx_p, 30))
print("r*(candidate) 50 dig :", nstr(r_cand, 50))
print("   cand min dist/2   :", nstr(dmin_c / 2, 30), " 1-maxnorm:", nstr(1 - mx_c, 30))
print("r*(cand) - table     :", nstr(r_cand - table, 20))

prop("parser sanity: r*(posted) within 1e-11 of table value", op.lt(abs(r_post - table), mpf("1e-11")),
     "(abs diff = %s)" % nstr(abs(r_post - table), 10))
prop("posted header equals table value", post_hdr == table)
prop("r*(candidate) exceeds table by at least 1e-10", op.ge(r_cand - table, mpf("1e-10")),
     "(margin = %s)" % nstr(r_cand - table, 15))
prop("r*(candidate) strictly exceeds table", op.gt(r_cand, table))
prop("candidate inside unit ball: max|c| + r* at most 1", op.le(mx_c + r_cand, 1))

# non-isometry: sorted pairwise-distance multisets differ by more than 1e-8 somewhere
sc = sorted_pairdists(cand)
sp = sorted_pairdists(post)
maxdev = max(abs(a - b) for a, b in zip(sc, sp))
count_big = sum(1 for a, b in zip(sc, sp) if op.gt(abs(a - b), mpf("1e-8")))
prop("not isometric: sorted pair-distance multisets differ by more than 1e-8 somewhere", op.gt(maxdev, mpf("1e-8")),
     "(max abs diff = %s, entries exceeding 1e-8: %d of %d)" % (nstr(maxdev, 10), count_big, len(sc)))

print("ALL_OK" if ok else "SOME_FAIL")
print("DETERMINISM_FINGERPRINT", nstr(r_cand, 50))
```

## Real output (run 1; run 2 was byte-identical under diff)

```
[PASS] candidate has exactly 81 points (got 81)
[PASS] posted has exactly 81 points (got 81)
[PASS] candidate coordinates all finite 
[PASS] candidate dimension is 4 
table value N=81     : 0.254058669351
posted header radius : 0.254058669351
r*(posted)  50 digits: 0.25405866935045098640760589110865608346550841384954
   posted min dist/2 : 0.254058669350700479247719891533  1-maxnorm: 0.254058669350450986407605891109
r*(candidate) 50 dig : 0.25408038179177490302490222756670917019602502200718
   cand min dist/2   : 0.25408038179202321225441021624  1-maxnorm: 0.254080381791774903024902227567
r*(cand) - table     : 0.000021712440774903024902
[PASS] parser sanity: r*(posted) within 1e-11 of table value (abs diff = 5.490135924e-13)
[PASS] posted header equals table value 
[PASS] r*(candidate) exceeds table by at least 1e-10 (margin = 2.1712440774903e-5)
[PASS] r*(candidate) strictly exceeds table 
[PASS] candidate inside unit ball: max|c| + r* at most 1 
[PASS] not isometric: sorted pair-distance multisets differ by more than 1e-8 somewhere (max abs diff = 0.06457333035, entries exceeding 1e-8: 3240 of 3240)
ALL_OK
DETERMINISM_FINGERPRINT 0.25408038179177490302490222756670917019602502200718
```

## Properties, each with verdict

1. Exactly 81 points in the candidate: PASS (81 non-comment lines, each with exactly 4 tokens; my loader rejects any other token count).
2. All candidate coordinates finite: PASS.
3. Dimension 4: PASS.
4. Parser sanity on the posted packing: r*(posted) = 0.25405866935045098... differs from the table value 0.254058669351 by 5.49e-13, well within 1e-11: PASS. The posted file's own header radius also equals the table value exactly: PASS.
5. r*(candidate) at 50 digits = 0.25408038179177490302490222756670917019602502200718. The binding term is the container term 1 - max|c| (0.2540803817917749...), while min pair distance / 2 is slightly larger (0.2540803817920232...). CLAIM.md states 0.254080381791775... and the candidate's comment line states r_float=0.25408038179177495; both agree with my value to their stated precision: PASS.
6. r*(candidate) - table = 2.1712440774903e-05, which is at least 1e-10 and strictly positive: PASS. (CLAIM.md says "about 2.17e-05": consistent.)
7. Feasibility inside the unit ball, max|c| + r* at most 1: PASS (holds with equality by construction of the min, since the container term is the binding one).
8. Non-isometry: sorted pairwise-distance multisets (3240 entries each) differ by up to 0.0646, and every one of the 3240 sorted entries differs by more than 1e-8: PASS.
9. Determinism: two independent runs of my checker produced byte-identical output, including the 50-digit r*: PASS.

## Comparison with the author's REPRODUCE.md (read only after the above)

The author's script implements the same definition (min over pairs of Euclidean distance / 2, versus 1 - max norm, mp.dps = 50, no tolerance) and the same non-isometry test (max absolute difference of sorted pair distances). My independently computed values agree with what their script would print. One difference in strictness, not in result: the author's loader takes the last 4 tokens of any line with at least 4 tokens (parts[-4:]), which would silently accept a malformed line with extra tokens; my loader requires exactly 4 tokens (candidate) or exactly 5 (posted), and both files pass that stricter check. The three curl commands in REPRODUCE.md (live radius row, hsp4.html last-update, pending-requests) were NOT run by me; they belong to the live-status lane and the claim's own caveat about the category-unspecified 26-Sep-2026 pending bundle still stands.

## Mismatches found

None. No missing object, no non-determinism, no value disagreement between CLAIM.md, the candidate's comment line, the table snapshot, and my 50-digit recomputation.

pass: true
