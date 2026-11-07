# REPRODUCE skeptic verdict: N = 83, hsp4 (unit 4-ball)

context: subagent (Claude Code Agent tool, fresh context for this one claim)

## Scope and method

I read only the claim folder: CLAIM.md, hsp4-83-candidate.txt, hsp4-83-posted.txt, hsp4_radius_as_fetched.txt, and (only after my own checker had run) REPRODUCE.md. No web fetches. The live-table / history / queue checks in REPRODUCE.md are out of my lane (they belong to the gate and novelty skeptics); I verify the mathematical object and the claimed value from the saved files only.

Interpreter: the project venv Python 3.14.7 with mpmath 1.4.1, invoked with -I (isolated mode) from a scratch directory outside the claim folder, with the claim folder passed as an argument.

## Definition used

Quoted from the success criterion in CLAIM.md (bank entry packomania-hyperspheres-hsp4-hsp6), with the pair-index condition written in words instead of the original symbol:

"the FEASIBLE radius r* := min( min over pairs i,j (i before j) of |c_i - c_j| / 2, 1 - max_i |c_i| ) (unit container ball centred at the origin), computed in mpmath at 50 digits directly from the submitted coordinates with no tolerance, is STRICTLY GREATER (direction: max) than that file's 12-decimal value for N re-fetched live immediately before claiming, by at least 1e-10 ... AND the configuration is not isometric to the posted hsp4-83.txt configuration (sorted pairwise-distance multisets differ by more than 1e-8 somewhere)"

Additional properties checked as instructed: exactly 83 points, all finite, 4 coordinates each, strictly inside the container, no duplicate points, posted file reproduces the table value within 1e-11 (parser sanity), candidate r* deterministic across two runs.

## My checker (written before reading REPRODUCE.md)

```python
# Independent checker for the N=83 hsp4 claim (written before reading REPRODUCE.md).
# Definition used (from the success criterion in CLAIM.md):
#   r* := min( [min over all pairs i,j with i different from j of |c_i - c_j| / 2] , 1 - max_i |c_i| )
#   unit container ball centred at the origin; mpmath at 50 digits,
#   directly from the submitted coordinates, no tolerance.
import sys, re
from mpmath import mp, mpf, sqrt, sign
mp.dps = 50
D = sys.argv[1].rstrip('/')
N = 83
TABLE_GAP = mpf('1e-10')
ISO_TOL = mpf('1e-8')
PARSER_TOL = mpf('1e-11')
def lt(a, b): return sign(a - b) == -1      # a strictly below b
def le(a, b): return sign(a - b) != 1       # a at most b
def gt(a, b): return sign(a - b) == 1       # a strictly above b
def ge(a, b): return sign(a - b) != -1      # a at least b

def read_candidate(p):
    pts = []
    for raw in open(p, encoding='ascii'):
        s = raw.strip()
        if not s or s.startswith('#'):
            continue
        toks = s.split()
        if len(toks) != 4:
            raise SystemExit('bad candidate line (expected 4 tokens): %r' % raw)
        pts.append([mpf(t) for t in toks])
    return pts

def read_posted(p):
    lines = [l.strip() for l in open(p, encoding='ascii') if l.strip()]
    rad = mpf(lines[0])
    pts = []
    for i, l in enumerate(lines[1:], 1):
        toks = l.split()
        if len(toks) != 5 or int(toks[0]) != i:
            raise SystemExit('bad posted line: %r' % l)
        pts.append([mpf(t) for t in toks[1:]])
    return rad, pts

def read_table(p, n):
    vals = []
    for l in open(p, encoding='ascii'):
        toks = l.split()
        if len(toks) == 2 and re.fullmatch(r'\d+', toks[0]) and int(toks[0]) == n:
            vals.append(toks[1])
    if len(vals) != 1:
        raise SystemExit('table rows for N=%d: %r' % (n, vals))
    if not re.fullmatch(r'0\.\d{12}', vals[0]):
        raise SystemExit('table value not 12-decimal: %s' % vals[0])
    return mpf(vals[0])

def norm(v):
    return sqrt(sum(x*x for x in v))

def dist(a, b):
    return sqrt(sum((x-y)*(x-y) for x, y in zip(a, b)))

def rstar(pts):
    mind = None
    for i in range(len(pts)):
        for j in range(i+1, len(pts)):
            d = dist(pts[i], pts[j])
            if mind is None or lt(d, mind):
                mind = d
    maxn = max(norm(p) for p in pts)
    return min(mind/2, 1 - maxn), mind, maxn

def sorted_dists(pts):
    return sorted(dist(pts[i], pts[j]) for i in range(len(pts)) for j in range(i+1, len(pts)))

cand = read_candidate('%s/hsp4-83-candidate.txt' % D)
prad, post = read_posted('%s/hsp4-83-posted.txt' % D)
table = read_table('%s/hsp4_radius_as_fetched.txt' % D, N)

ok = True
def chk(name, cond, detail=''):
    global ok
    print('[%s] %s %s' % ('PASS' if cond else 'FAIL', name, detail))
    ok = ok and bool(cond)

chk('candidate has exactly 83 points', len(cand) == N, '(got %d)' % len(cand))
chk('posted has exactly 83 points', len(post) == N, '(got %d)' % len(post))
chk('all candidate coords finite', all(x.ae(x) and lt(abs(x), mpf(10)) for p in cand for x in p))
chk('all candidate coords in R^4', all(len(p) == 4 for p in cand))
chk('all candidate norms strictly below 1 (inside container)', all(lt(norm(p), 1) for p in cand))

rc, mind_c, maxn_c = rstar(cand)
rp, mind_p, maxn_p = rstar(post)
print('table value N=83          :', mp.nstr(table, 20))
print('posted file first line     :', mp.nstr(prad, 20))
print('candidate r*               :', mp.nstr(rc, 40))
print('  candidate min pair dist  :', mp.nstr(mind_c, 40))
print('  candidate max norm       :', mp.nstr(maxn_c, 40))
print('  candidate 1-maxnorm      :', mp.nstr(1-maxn_c, 40))
print('  binding term             :', 'pairwise' if le(mind_c/2, 1-maxn_c) else 'container')
print('posted r*                  :', mp.nstr(rp, 40))
print('  posted min pair dist     :', mp.nstr(mind_p, 40))
print('  posted max norm          :', mp.nstr(maxn_p, 40))
print('gain = candidate r* - table:', mp.nstr(rc - table, 20))

chk('candidate min pair dist strictly positive (no duplicate points)', gt(mind_c, 0))
chk('posted r* reproduces table within 1e-11 (parser sanity)', le(abs(rp - table), PARSER_TOL), '|diff|=%s' % mp.nstr(abs(rp-table),10))
chk('posted r* reproduces posted first line within 1e-11', le(abs(rp - prad), PARSER_TOL), '|diff|=%s' % mp.nstr(abs(rp-prad),10))
chk('candidate r* exceeds table by at least 1e-10', ge(rc - table, TABLE_GAP), 'gain=%s' % mp.nstr(rc-table,12))
chk('candidate r* matches CLAIM.md 0.252010684947089 (15 digits)', mp.nstr(rc, 15) == '0.252010684947089', 'got %s' % mp.nstr(rc,15))

sc = sorted_dists(cand); sp = sorted_dists(post)
chk('distance multisets same length 3403', len(sc) == len(sp) == N*(N-1)//2)
maxdev = max(abs(a-b) for a, b in zip(sc, sp))
chk('not isometric: sorted pairwise-distance multisets differ by more than 1e-8 somewhere', gt(maxdev, ISO_TOL), 'max |diff|=%s' % mp.nstr(maxdev,10))

print('DETERMINISM_TOKEN', mp.nstr(rc, 50), mp.nstr(maxdev, 50))
print('ALL_OK' if ok else 'SOME_FAIL')
```

Invocation (two independent runs, outputs diffed):

```
python -I check83.py claim-folder   # run 1, stdout saved
python -I check83.py claim-folder   # run 2, stdout saved
diff run1.txt run2.txt
```

## Real output (run 1; run 2 was byte-identical, diff empty)

```
[PASS] candidate has exactly 83 points (got 83)
[PASS] posted has exactly 83 points (got 83)
[PASS] all candidate coords finite 
[PASS] all candidate coords in R^4 
[PASS] all candidate norms strictly below 1 (inside container) 
table value N=83          : 0.252008330509
posted file first line     : 0.252008330509
candidate r*               : 0.2520106849470888866431014207400833300947
  candidate min pair dist  : 0.5040213698942857517042532414039278349901
  candidate max norm       : 0.7479893150529111133568985792599166699053
  candidate 1-maxnorm      : 0.2520106849470888866431014207400833300947
  binding term             : container
posted r*                  : 0.2520083305081919912031267005440039230589
  posted min pair dist     : 0.5040166610168043837660682140488235795316
  posted max norm          : 0.7479916694918080087968732994559960769411
gain = candidate r* - table: 2.3544380888866431014e-6
[PASS] candidate min pair dist strictly positive (no duplicate points) 
[PASS] posted r* reproduces table within 1e-11 (parser sanity) |diff|=8.080087969e-13
[PASS] posted r* reproduces posted first line within 1e-11 |diff|=8.080087969e-13
[PASS] candidate r* exceeds table by at least 1e-10 gain=2.35443808889e-6
[PASS] candidate r* matches CLAIM.md 0.252010684947089 (15 digits) got 0.252010684947089
[PASS] distance multisets same length 3403 
[PASS] not isometric: sorted pairwise-distance multisets differ by more than 1e-8 somewhere max |diff|=0.01185410297
DETERMINISM_TOKEN 0.25201068494708888664310142074008333009469420727062 0.011854102972066849078426854514160184702815530477215
ALL_OK
---
IDENTICAL_RUNS
```

## Property-by-property verdict

| Property | Result | Evidence |
|---|---|---|
| Exactly 83 points in candidate | PASS | 83 non-comment lines, 4 tokens each |
| Exactly 83 points in posted file | PASS | indices 1..83 contiguous, 5 tokens each |
| All coordinates finite and in R^4 | PASS | every token parsed by mpf, each row has 4 entries |
| All centres strictly inside the unit ball | PASS | max norm 0.74798931505291... (below 1) |
| No duplicate centres | PASS | min pair distance 0.50402136989428... (strictly positive) |
| Parser sanity: posted packing reproduces the table value within 1e-11 | PASS | posted r* = 0.252008330508191991..., table 0.252008330509, diff 8.08e-13 |
| Parser sanity: posted r* matches the first line of hsp4-83-posted.txt within 1e-11 | PASS | same 8.08e-13 |
| Candidate r* (50-digit mpmath, no tolerance) | PASS | r* = 0.2520106849470888866431014207400833300947 |
| Candidate r* matches CLAIM.md "0.252010684947089..." | PASS | 15-digit rounding agrees exactly |
| Candidate r* matches candidate header r_float=0.25201068494708889 | PASS | 17-digit rounding agrees |
| Candidate r* exceeds the table value by at least 1e-10 | PASS | gain = 2.3544380888866e-06 (about 23,500 times the margin); CLAIM.md says "about 2.35e-06", header says 2.354e-06; agree |
| Not isometric to posted (sorted distance multisets differ by more than 1e-8 somewhere) | PASS | max absolute difference over the 3403 sorted distances = 0.01185410297 (about 1.2e6 times the threshold) |
| Deterministic across two runs | PASS | full stdout byte-identical, including both 50-digit tokens |

Observation (not a defect): the candidate's r* is bound by the container term (1 - max norm = 0.25201068494708888...), while its pairwise term is marginally larger (min dist / 2 = 0.25201068494714287...). The two terms agree to about 5e-14, which is what a converged polish looks like; the criterion takes the min, and the min is what I report. The posted packing is likewise container-bound.

## Mismatches

None. No missing object, no non-finite values, no parse ambiguity (the table has exactly one row for N = 83, with a 12-decimal value as expected), no run-to-run variation.

## Comparison with the author's REPRODUCE.md (read only after the above)

The author's script implements the same definition: pairwise min over i before j, halved; container term 1 - max norm; min of the two; mp.dps = 50; no tolerance. Its loader takes the last four tokens of each line (so it handles the posted file's leading index column) and skips the "#" header; its table parse selects the row whose first token is "83". Those choices match my independent parser, and the values it prints (r* candidate to 25 digits, gain, max sorted-distance difference) are the same quantities I computed. I did not run the author's script; my checker is the evidence. The three curl commands at the end of REPRODUCE.md (live table row, "Last update" line, pending-requests page) are not reproduced here: I made no network requests, and those checks are the gate and novelty skeptics' responsibility. The claim's own caveat about the category-unspecified 26-Sep-2026 pending bundle is noted and left to them.

## Verdict

The object exists, is well-formed, is deterministic, and under the quoted definition its feasible radius at 50 digits is 0.25201068494708888664..., which exceeds the saved table value 0.252008330509 by 2.354438e-06 (margin requirement 1e-10 met), and it is not isometric to the posted N = 83 packing (sorted-distance multisets differ by up to 0.0119). Every property I was asked to verify holds from the saved files.

pass: true
