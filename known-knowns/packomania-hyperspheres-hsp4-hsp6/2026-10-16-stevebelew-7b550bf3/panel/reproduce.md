# REPRODUCE skeptic verdict for claim N104 (hsp4, N = 104)

context: subagent (Claude Code Agent tool, fresh context for this one claim)

## Scope

Read only the claim folder: CLAIM.md, hsp4-104-candidate.txt, hsp4-104-posted.txt, hsp4_radius_as_fetched.txt, and (only after my own checker had run) REPRODUCE.md. No web access, no other files. Checker written from the definition first; author's code consulted afterwards for comparison only.

## Definition used (quoted from CLAIM.md, success criterion)

"the FEASIBLE radius r* := min( min_{i<j} |c_i - c_j| / 2, 1 - max_i |c_i| ) (unit container ball centred at the origin), computed in mpmath at 50 digits directly from the submitted coordinates with no tolerance, is STRICTLY GREATER (direction: max) than that file's 12-decimal value for N re-fetched live immediately before claiming, by at least 1e-10 (...), AND the configuration is not isometric to the posted hsp4-104.txt configuration [placeholders for d and N instantiated here] (sorted pairwise-distance multisets differ by more than 1e-8 somewhere)"

Additional checks asked of this skeptic: exactly 104 points, all finite, posted file reproduces the table value within 1e-11 (parser sanity), r* deterministic across two runs.

## Environment

Interpreter: the project venv python run with -I (isolated mode). Python 3.14.7, mpmath 1.4.1, mp.dps = 50.

Input file checksums (sha256) at the time of checking:

- hsp4-104-candidate.txt  7b550bf3fbd594ed0d6e429f509c23e3ad5486f0a69c49d73d61c8d630a21b64
- hsp4-104-posted.txt     4b7b48f3fc900eced47a2ae1fe99ef43331c3fed977fe9d59700b451ed5f54a9
- hsp4_radius_as_fetched.txt  f3ddaa944aac014718bc9f5438700698abedac0189266198df8bb60772ac569f

## My checker (written before reading REPRODUCE.md), sha256 e4ae879b307d92797e2a1f9ae811cb6ad6e1fe8056c103e221f36e7a1bcb7a25

```python
# Independent checker for claim N104 (written from the definition, before reading REPRODUCE.md).
# Definition used (quoted from CLAIM.md success criterion):
#   r* := min( min_{i<j} |c_i - c_j| / 2, 1 - max_i |c_i| )
#   unit container ball centred at the origin, mpmath at 50 digits, no tolerance.
import sys, re
from mpmath import mp, mpf, sqrt, fabs

mp.dps = 50
D = sys.argv[1].rstrip('/')
N_EXPECT = 104
TABLE_N = 104

def load_candidate(path):
    pts = []
    with open(path, 'r', encoding='ascii') as f:   # ascii: fail loudly on any odd byte
        for ln in f:
            s = ln.strip()
            if not s or s.startswith('#'):
                continue
            toks = s.split()
            if len(toks) != 4:
                raise ValueError('candidate line with %d tokens: %r' % (len(toks), s))
            pts.append([mpf(t) for t in toks])
    return pts

def load_posted(path):
    with open(path, 'r', encoding='ascii') as f:
        lines = [l.strip() for l in f if l.strip()]
    r_head = mpf(lines[0])
    pts = []
    idx_seen = []
    for s in lines[1:]:
        toks = s.split()
        if len(toks) != 5:
            raise ValueError('posted line with %d tokens: %r' % (len(toks), s))
        idx_seen.append(int(toks[0]))
        pts.append([mpf(t) for t in toks[1:]])
    assert idx_seen == list(range(1, len(pts) + 1)), 'posted indices not 1..n'
    return r_head, pts

def load_table(path):
    with open(path, 'r', encoding='ascii') as f:
        rows = {}
        for ln in f:
            s = ln.strip()
            if not s:
                continue
            n, r = s.split()
            n = int(n)
            assert n not in rows, 'duplicate row N=%d' % n
            rows[n] = r
    return rows

def norm(p):
    return sqrt(sum(x * x for x in p))

def dist(p, q):
    return sqrt(sum((a - b) * (a - b) for a, b in zip(p, q)))

def rstar(pts):
    n = len(pts)
    dmin = None
    dists = []
    for i in range(n):
        for j in range(i + 1, n):
            d = dist(pts[i], pts[j])
            dists.append(d)
            if dmin is None or d < dmin:
                dmin = d
    nmax = max(norm(p) for p in pts)
    return min(dmin / 2, 1 - nmax), dmin, nmax, sorted(dists)

def finite(x):
    return mp.isfinite(x) and not mp.isnan(x)

results = {}
cand = load_candidate(D + '/hsp4-104-candidate.txt')
r_head, posted = load_posted(D + '/hsp4-104-posted.txt')
table = load_table(D + '/hsp4_radius_as_fetched.txt')

# P1: counts and finiteness
results['P1 candidate has exactly 104 points'] = (len(cand) == N_EXPECT, len(cand))
results['P1 posted has exactly 104 points'] = (len(posted) == N_EXPECT, len(posted))
results['P1 all candidate coords finite'] = (all(finite(x) for p in cand for x in p), None)
results['P1 all posted coords finite'] = (all(finite(x) for p in posted for x in p), None)

# P2: table row and parser sanity on posted packing
t_str = table[TABLE_N]
t_val = mpf(t_str)
results['P2 table row 104 present'] = (TABLE_N in table, t_str)
r_posted, dmin_p, nmax_p, sd_posted = rstar(posted)
results['P2 posted header radius == table (exact string)'] = (r_head == t_val, mp.nstr(r_head, 20))
results['P2 posted r* within 1e-11 of table'] = (fabs(r_posted - t_val) <= mpf('1e-11'), mp.nstr(r_posted, 30))

# P3: candidate r*
r_cand, dmin_c, nmax_c, sd_cand = rstar(cand)
gain = r_cand - t_val
results['P3 candidate r* > table + 1e-10'] = (gain >= mpf('1e-10') and r_cand > t_val, mp.nstr(gain, 15))
# also check all centres inside container (implied by r*>0, but explicit)
results['P3 candidate r* > 0 (container/overlap feasibility)'] = (r_cand > 0, None)

# P4: non-isometry
assert len(sd_cand) == len(sd_posted) == N_EXPECT * (N_EXPECT - 1) // 2
maxdiff = max(fabs(a - b) for a, b in zip(sd_cand, sd_posted))
results['P4 sorted distance multisets differ > 1e-8 somewhere'] = (maxdiff > mpf('1e-8'), mp.nstr(maxdiff, 12))

print('mp.dps =', mp.dps)
print('table value N=104   :', t_str)
print('posted  r*          :', mp.nstr(r_posted, 50))
print('posted  dmin/2      :', mp.nstr(dmin_p / 2, 30), ' 1-maxnorm:', mp.nstr(1 - nmax_p, 30))
print('candidate r*        :', mp.nstr(r_cand, 50))
print('candidate dmin/2    :', mp.nstr(dmin_c / 2, 30), ' 1-maxnorm:', mp.nstr(1 - nmax_c, 30))
print('gain (cand - table) :', mp.nstr(gain, 20))
print('max |sorted-dist diff| cand vs posted:', mp.nstr(maxdiff, 15))
print('candidate rstar mpf repr (for determinism check):', repr(r_cand))
ok = True
for k, (v, info) in results.items():
    print('%-60s %s %s' % (k, 'PASS' if v else 'FAIL', '' if info is None else '(%s)' % info))
    ok = ok and v
print('OVERALL:', 'PASS' if ok else 'FAIL')
```

Invocation: `python -I check_n104.py CLAIMDIR` (argument is the claim folder; no other inputs). Files are opened with encoding ascii so any non-ASCII byte would abort the run; none did.

## Real output (run A; run B was byte-identical, see determinism below)

```
mp.dps = 50
table value N=104   : 0.240535464233
posted  r*          : 0.24053546423234634946500586269117756761221019569081
posted  dmin/2      : 0.240535464232346349465005862691  1-maxnorm: 0.240535464232387944681181371735
candidate r*        : 0.24053869762389658208934651593930039633912649358841
candidate dmin/2    : 0.240538697805011002440781031354  1-maxnorm: 0.240538697623896582089346515939
gain (cand - table) : 3.2333908965820893465e-6
max |sorted-dist diff| cand vs posted: 0.0052927922856769
candidate rstar mpf repr (for determinism check): mpf('0.2405386976238965820893465159393003963391264935884059')
P1 candidate has exactly 104 points                          PASS (104)
P1 posted has exactly 104 points                             PASS (104)
P1 all candidate coords finite                               PASS 
P1 all posted coords finite                                  PASS 
P2 table row 104 present                                     PASS (0.240535464233)
P2 posted header radius == table (exact string)              PASS (0.240535464233)
P2 posted r* within 1e-11 of table                           PASS (0.240535464232346349465005862691)
P3 candidate r* > table + 1e-10                              PASS (3.23339089658209e-6)
P3 candidate r* > 0 (container/overlap feasibility)          PASS 
P4 sorted distance multisets differ > 1e-8 somewhere         PASS (0.00529279228568)
OVERALL: PASS
```

## Determinism

Two consecutive isolated runs of the checker on the same files produced byte-identical output:

```
49bdeac4628700b4986fb3d611a1b3e4581163e9a7491d9f7062388ac34da04e  n104_runA.txt
49bdeac4628700b4986fb3d611a1b3e4581163e9a7491d9f7062388ac34da04e  n104_runB.txt
CMP: identical
```

Candidate r* at 50 digits, both runs: 0.2405386976238965820893465159393003963391264935884059

(A first attempt at the determinism comparison was discarded: the shared scratch directory's output file was overwritten by an unrelated process between runs. The comparison above was redone in a private directory with unique filenames and is the one relied on.)

## Property-by-property verdicts

| Property | Result | Evidence |
|---|---|---|
| Candidate file holds exactly 104 points, 4 coordinates each | PASS | 1 comment line + 104 data lines; every line has 4 tokens |
| All candidate coordinates finite | PASS | mp.isfinite on all 416 values |
| Posted file holds exactly 104 points, indices 1..104 in order | PASS | header radius line + 104 lines "index x1 x2 x3 x4" |
| All posted coordinates finite | PASS | mp.isfinite on all 416 values |
| Table row for N=104 present, value 0.240535464233 | PASS | line 103 of hsp4_radius_as_fetched.txt; no duplicate N rows |
| Posted file header radius equals table value | PASS | both parse to the same mpf |
| Parser sanity: r*(posted) within 1e-11 of table | PASS | r*(posted) = 0.24053546423234634946..., diff = -6.5e-13 |
| r*(candidate) computed at 50 digits, no tolerance | PASS | 0.24053869762389658208934651593930039633912649358841; binding term is 1 - max norm (dmin/2 = 0.2405386978050... is larger) |
| r*(candidate) > table value strictly, by >= 1e-10 | PASS | gain = 3.2333908965820893465e-6 (about 3.2e4 times the 1e-10 margin) |
| Candidate feasible (r* > 0: no overlap, all centres inside) | PASS | r* > 0 |
| Not isometric to posted packing (sorted distance multisets differ > 1e-8) | PASS | both multisets have 5356 entries; max absolute difference 0.0052927922856769 |
| Claimed value in CLAIM.md "0.240538697623897..." matches | PASS | my 50-digit value rounds to 0.240538697623897 |
| Claimed gain "about 3.23e-06" matches | PASS | 3.2334e-06 |
| Candidate header comment r_float=0.24053869762389657 consistent | PASS | agrees with 50-digit value to double precision |
| Deterministic across two runs | PASS | byte-identical output, identical sha256 |

No mismatch found. No missing object. No non-determinism.

## Comparison with the author's REPRODUCE.md (read only after my checker had passed)

The author's Python block uses the same definition (min of half the minimum pairwise distance and 1 minus the max norm, mp.dps = 50, mpf parsing of the raw text). It parses coordinates as the last 4 tokens per line, which handles both the candidate format and the posted "index x1..x4" format; its table lookup selects the line whose first token is "104". I extracted that block verbatim and ran it with the same isolated interpreter. Its output:

```
N candidate = 104  N posted = 104
r* candidate = 0.2405386976238965820893465
r* posted    = 0.2405354642323463494650059  (parser sanity: must equal the table value within 1e-11)
table        = 0.240535464233
gain = r*cand - table = 3.2333909e-6  -> meets 1e-10 margin: True
max |sorted distance difference| vs posted = 0.0052927923  (> 1e-8 means not isometric)
```

Every printed digit agrees with my independent checker. The REPRODUCE.md also lists three curl commands against the live site (table row, hsp4.html last-update, pending-requests page); those are out of scope for this skeptic (no web access) and were not run, so the live-table, history-of-updates and queue-rule conditions of the success criterion are NOT confirmed here and must be covered by another panel member. This verdict is limited to the mathematical content of the saved files.

## Caveats carried forward (not failures of the mathematical claim)

- Live re-fetch of radius.txt, the hsp4.html history of updates, and the pending-requests queue page were not checked by me.
- As the bank entry requires, the category-unspecified "Moki & Julio *many* 4666 candidates" bundle on the pending list cannot be resolved from the saved files; the N must be re-checked against the live table once that bundle disappears.

## Verdict

From the saved files alone, with an independently written 50-digit mpmath checker: the candidate is a valid packing of 104 equal balls in the unit 4-ball with feasible radius 0.24053869762389658..., exceeding the table value 0.240535464233 by 3.2334e-6 (well above the 1e-10 margin), and it is not isometric to the posted configuration. All required properties hold, the result is deterministic, and the author's reproduction script agrees to every printed digit.

pass: true
