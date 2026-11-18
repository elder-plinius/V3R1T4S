# REPRODUCE verdict for claim N91 (hsp4, N = 91)

context: subagent (Claude Code Agent tool, fresh context for this one claim)

Scope: only the claim folder was read (CLAIM.md, hsp4-91-candidate.txt, hsp4-91-posted.txt,
hsp4_radius_as_fetched.txt, and REPRODUCE.md last). No web fetches were made; the three curl
lines in REPRODUCE.md (live table, "Last update", pending-requests page) were NOT executed and
are outside this verdict. The queue-rule caveat about the category-unspecified
"Moki and Julio many 4666 candidates" bundle stands as stated in CLAIM.md.

## Definition used (quoted from CLAIM.md success criterion)

"the FEASIBLE radius r* := min( min_{i before j} |c_i - c_j| / 2, 1 - max_i |c_i| ) (unit container
ball centred at the origin), computed in mpmath at 50 digits directly from the submitted
coordinates with no tolerance, is STRICTLY GREATER (direction: max) than that file's 12-decimal
value for N re-fetched live immediately before claiming, by at least 1e-10 [...] AND the
configuration is not isometric to the posted hsp4-91.txt configuration (sorted pairwise-distance
multisets differ by more than 1e-8 somewhere)"

(The subscript "i before j" in the quote above is the pair condition i strictly less than j;
the symbol is spelled out here to keep this file free of angle brackets.)

## Checker (written by me from that definition BEFORE opening REPRODUCE.md)

Run with the project venv's Python in isolated mode (-I), from a scratch directory, passing the
claim folder as argv[1]. Executed twice; outputs byte-identical (diff empty).

```python
# Independent checker written from the definition in CLAIM.md:
#   r* := min( min over pairs i before j of |c_i - c_j| / 2 , 1 - max_i |c_i| )
#   unit container ball centred at the origin, mpmath at 50 digits, no tolerance.
# (operator.lt / gt / ge are used in place of comparison symbols on purpose.)
import sys, re, hashlib
from operator import lt, gt, ge
from mpmath import mp, mpf, sqrt, fabs
mp.dps = 50
D = sys.argv[1].rstrip('/')
CAND = D + '/hsp4-91-candidate.txt'
POST = D + '/hsp4-91-posted.txt'
TABLE = D + '/hsp4_radius_as_fetched.txt'
N_EXPECT = 91
DIM = 4
FLOAT_RE = re.compile(r'^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$')

def sha(p):
    return hashlib.sha256(open(p,'rb').read()).hexdigest()

def ascii_only(raw):
    return all(lt(b, 128) for b in raw)

def load_candidate(p):
    raw = open(p,'rb').read()
    assert ascii_only(raw), "non-ASCII bytes in candidate"
    pts = []
    for ln in raw.decode('ascii').splitlines():
        s = ln.strip()
        if not s or s.startswith('#'):
            continue
        toks = s.split()
        assert len(toks) == DIM, f"bad token count {len(toks)} in line: {ln!r}"
        for t in toks:
            assert FLOAT_RE.match(t), f"non-finite / non-numeric token {t!r}"
        pts.append([mpf(t) for t in toks])
    return pts

def load_posted(p):
    raw = open(p,'rb').read()
    assert ascii_only(raw), "non-ASCII bytes in posted"
    lines = [l for l in raw.decode('ascii').splitlines() if l.strip()]
    hdr = lines[0].strip()
    assert FLOAT_RE.match(hdr), f"bad header {hdr!r}"
    r_hdr = mpf(hdr)
    pts = []
    idx_seen = []
    for ln in lines[1:]:
        toks = ln.split()
        assert len(toks) == DIM + 1, f"bad token count in posted line {ln!r}"
        assert toks[0].isdigit(), f"bad index {toks[0]!r}"
        idx_seen.append(int(toks[0]))
        for t in toks[1:]:
            assert FLOAT_RE.match(t), f"non-finite / non-numeric token {t!r}"
        pts.append([mpf(t) for t in toks[1:]])
    assert idx_seen == list(range(1, len(pts) + 1)), "posted indices not 1..n in order"
    return r_hdr, pts

def table_value(p, n):
    raw = open(p,'rb').read()
    assert ascii_only(raw), "non-ASCII bytes in table"
    hits = []
    for ln in raw.decode('ascii').splitlines():
        toks = ln.split()
        if len(toks) == 2 and toks[0] == str(n):
            assert FLOAT_RE.match(toks[1]), f"bad table value {toks[1]!r}"
            hits.append(toks[1])
    assert len(hits) == 1, f"expected exactly one row for N={n}, found {len(hits)}"
    return hits[0]

def norm(v):
    return sqrt(sum(x * x for x in v))

def dist(a, b):
    return sqrt(sum((x - y) * (x - y) for x, y in zip(a, b)))

def rstar(pts):
    n = len(pts)
    dmin = None
    pair = None
    for i in range(n):
        for j in range(i + 1, n):
            d = dist(pts[i], pts[j])
            if dmin is None or lt(d, dmin):
                dmin, pair = d, (i, j)
    nmax = max(norm(p) for p in pts)
    return min(dmin / 2, 1 - nmax), dmin / 2, 1 - nmax, pair

def sorted_pair_dists(pts):
    n = len(pts)
    return sorted(dist(pts[i], pts[j]) for i in range(n) for j in range(i + 1, n))

print("sha256 candidate", sha(CAND))
print("sha256 posted   ", sha(POST))
print("sha256 table    ", sha(TABLE))

cand = load_candidate(CAND)
r_hdr, post = load_posted(POST)
tbl_str = table_value(TABLE, N_EXPECT)
tbl = mpf(tbl_str)
print("table row N=91 value string:", tbl_str)
print("posted header radius       :", mp.nstr(r_hdr, 15))

ok = True
def check(name, cond, detail=""):
    global ok
    print(("PASS " if cond else "FAIL ") + name + ("  " + detail if detail else ""))
    ok = ok and bool(cond)

check("candidate has exactly 91 points", len(cand) == N_EXPECT, f"n={len(cand)}")
check("posted has exactly 91 points", len(post) == N_EXPECT, f"n={len(post)}")
check("candidate all coords finite and in dimension 4",
      all(len(p) == DIM and all(mp.isfinite(x) for x in p) for p in cand))
check("posted header equals table value exactly", abs(r_hdr - tbl) == 0,
      f"|diff|={mp.nstr(abs(r_hdr - tbl), 5)}")

rp, rp_pair, rp_cont, pp = rstar(post)
print("posted   r* =", mp.nstr(rp, 50))
print("         min pair dist/2 =", mp.nstr(rp_pair, 50), "pair", pp)
print("         1 - max|c|      =", mp.nstr(rp_cont, 50))
check("posted r* reproduces table value within 1e-11 (parser sanity)",
      lt(abs(rp - tbl), mpf('1e-11')), f"|r*_posted - table| = {mp.nstr(abs(rp - tbl), 8)}")

rc, rc_pair, rc_cont, pc = rstar(cand)
print("candidate r* =", mp.nstr(rc, 50))
print("         min pair dist/2 =", mp.nstr(rc_pair, 50), "pair", pc)
print("         1 - max|c|      =", mp.nstr(rc_cont, 50))
gain = rc - tbl
print("candidate r* - table =", mp.nstr(gain, 20))
check("candidate r* exceeds table by at least 1e-10", ge(gain, mpf('1e-10')), f"gain = {mp.nstr(gain, 12)}")
check("candidate r* matches CLAIM.md 0.246998182873809...",
      mp.nstr(rc, 15).startswith("0.24699818287380"), mp.nstr(rc, 18))

sc = sorted_pair_dists(cand)
sp = sorted_pair_dists(post)
check("pairwise multisets both of size 91*90/2", len(sc) == len(sp) == N_EXPECT * (N_EXPECT - 1) // 2, f"{len(sc)} {len(sp)}")
maxdiff = max(fabs(a - b) for a, b in zip(sc, sp))
cnt = sum(1 for a, b in zip(sc, sp) if gt(fabs(a - b), mpf('1e-8')))
print("max |sorted-dist difference| =", mp.nstr(maxdiff, 12), "; entries differing by more than 1e-8:", cnt)
check("not isometric to posted (sorted dist multisets differ by more than 1e-8 somewhere)", gt(maxdiff, mpf('1e-8')))

print("DETERMINISM_FINGERPRINT", mp.nstr(rc, 50), mp.nstr(rp, 50), mp.nstr(maxdiff, 30))
print("OVERALL", "PASS" if ok else "FAIL")
```

## Real output (run 1; run 2 was byte-identical)

```
sha256 candidate 60ff0e29ee286c3b2a38c134eaac572db5031d97ce12072a7d4163e5ee7e96a9
sha256 posted    de33341e2fac7aec23b961b3c1837129abe914dd49f350f0a94b4c45370605bf
sha256 table     f3ddaa944aac014718bc9f5438700698abedac0189266198df8bb60772ac569f
table row N=91 value string: 0.246960900415
posted header radius       : 0.246960900415
PASS candidate has exactly 91 points  n=91
PASS posted has exactly 91 points  n=91
PASS candidate all coords finite and in dimension 4
PASS posted header equals table value exactly  |diff|=0.0
posted   r* = 0.24696090041418810620039171094692623694478183604276
         min pair dist/2 = 0.24696090041450862232446887749977996781287796572533 pair (79, 87)
         1 - max|c|      = 0.24696090041418810620039171094692623694478183604276
PASS posted r* reproduces table value within 1e-11 (parser sanity)  |r*_posted - table| = 8.118938e-13
candidate r* = 0.24699818287380882063495515293045887856895962747508
         min pair dist/2 = 0.24699818287386051216622127656028823329929679073846 pair (7, 37)
         1 - max|c|      = 0.24699818287380882063495515293045887856895962747508
candidate r* - table = 0.000037282458808820634955
PASS candidate r* exceeds table by at least 1e-10  gain = 3.72824588088e-5
PASS candidate r* matches CLAIM.md 0.246998182873809...  0.246998182873808821
PASS pairwise multisets both of size 91*90/2  4095 4095
max |sorted-dist difference| = 0.00858147704625 ; entries differing by more than 1e-8: 4095
PASS not isometric to posted (sorted dist multisets differ by more than 1e-8 somewhere)
DETERMINISM_FINGERPRINT 0.24699818287380882063495515293045887856895962747508 0.24696090041418810620039171094692623694478183604276 0.00858147704625424668205982118199
OVERALL PASS
```

## Properties, each with verdict

| Property | Result | Verdict |
|---|---|---|
| Candidate file parses: one comment line, then 91 lines of 4 numeric tokens, all ASCII | n = 91, every token matches a finite-decimal regex, mp.isfinite on all 364 coords | PASS |
| Posted file parses: header radius then rows "index x1 x2 x3 x4", indices 1..91 in order | n = 91, header 0.246960900415 | PASS |
| Table has exactly one row for N = 91 | row "91 0.246960900415" (line 90 of 299) | PASS |
| Posted header equals the table value | exact string and mpf equality, diff 0 | PASS |
| Parser sanity: r* of posted packing reproduces table value within 1e-11 | r*_posted = 0.24696090041418810620..., diff from table 8.12e-13 (binding term is the container, 1 - max norm) | PASS |
| Candidate r* at 50 digits, no tolerance | r*_cand = 0.24699818287380882063495515293045887856895962747508 (binding term: container, 1 - max norm; closest pair (7,37) gives 0.2469981828738605...) | computed |
| Candidate r* matches the value stated in CLAIM.md (0.246998182873809...) and the candidate header (r_float 0.24699818287380881) | 0.246998182873808821 rounds to ...809 at 15 places; the header's 17-digit double is the nearest float | PASS |
| Candidate r* exceeds the table value by at least 1e-10 | gain = 3.72824588088e-5 (about 3.73e-5 as claimed; 1e-10 margin exceeded by a factor of about 3.7e5) | PASS |
| Not isometric to posted: sorted pairwise-distance multisets differ by more than 1e-8 somewhere | both multisets have 4095 entries; max difference 0.00858147704625; all 4095 entries differ by more than 1e-8 | PASS |
| Determinism of r* across two runs | DETERMINISM_FINGERPRINT identical; full stdout identical | PASS |
| File identity (for the record) | sha256 candidate 60ff0e29...5ee7e96a9, posted de33341e...370605bf, table f3ddaa94...72ac569f (full hashes in the output above) | recorded |

## Comparison with the author's REPRODUCE.md (read only after my checker ran)

The author's Python block implements the same definition (min over i before j of the pairwise
distance halved, versus 1 minus the max norm, mpmath dps 50, no tolerance; posted rows parsed
by taking the last four tokens; table row selected by first token == '91'). I ran that block
offline (isolated Python, cwd = claim folder, no network). Its output, pasted (two arrow /
comparison symbols in its print strings rewritten in words to keep this file bracket-free):

```
N candidate = 91  N posted = 91
r* candidate = 0.2469981828738088206349552
r* posted    = 0.2469609004141881062003917  (parser sanity: must equal the table value within 1e-11)
table        = 0.246960900415
gain = r*cand - table = 3.7282459e-5  -- meets 1e-10 margin: True
max |sorted distance difference| vs posted = 0.008581477  (more than 1e-8 means not isometric)
```

Author r* candidate 0.2469981828738088206349552 and r* posted 0.2469609004141881062003917 agree
with my 50-digit values to every printed digit; gain 3.7282459e-5 and max sorted-distance
difference 0.008581477 agree with mine. No mismatch between my checker, the author's script,
CLAIM.md, and the candidate file's header comment.

## Mismatches found

None. No missing objects, no non-finite or non-ASCII data, no duplicate table rows, no
non-determinism.

## Not verified here (outside my scope / forbidden)

- Live re-fetch of radius.txt, the hsp4.html history-of-updates, and pending-requests.html
  (network use is prohibited for this skeptic). The claim's snapshot file is what was checked.
- Whether the "Moki and Julio" pending bundle contains hsp4 N = 91 cannot be resolved from the
  claim folder; CLAIM.md itself flags this caveat.

pass: true
