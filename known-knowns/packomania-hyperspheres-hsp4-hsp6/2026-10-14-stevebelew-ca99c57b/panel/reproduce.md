# REPRODUCE skeptic verdict — packomania hsp4, N = 66

context: subagent (Claude Code Agent tool, fresh context)

## Scope

Read only the files under claim/: CLAIM.md, hsp4-66-candidate.txt, hsp4-66-posted.txt, hsp4_radius_as_fetched.txt, and (only after my own checker had run) REPRODUCE.md. No web access, no other files. Default verdict is fail unless every property is independently confirmed.

## Definition used (quoted from CLAIM.md, success criterion)

> "the FEASIBLE radius r* := min( min_{i<j} |c_i - c_j| / 2, 1 - max_i |c_i| ) (unit container ball centred at the origin), computed in mpmath at 50 digits directly from the submitted coordinates with no tolerance, is STRICTLY GREATER (direction: max) than that file's 12-decimal value for N re-fetched live immediately before claiming, by at least 1e-10 [...] AND the configuration is not isometric to the posted hsp<d>-<N>.txt configuration (sorted pairwise-distance multisets differ by more than 1e-8 somewhere)"

File formats (from CLAIM.md): candidate = one "#" comment line then 66 lines of 4 coordinates; posted = first line radius, then "index x1 x2 x3 x4"; table = rows "N radius".

## My checker (written from the definition BEFORE reading REPRODUCE.md; run with `python -I check.py <claim dir>`)

```python
# Independent checker written from the definition in CLAIM.md:
#   r* := min( min_{i<j} |c_i - c_j| / 2 , 1 - max_i |c_i| )
#   unit container ball centred at the origin, mpmath at 50 digits, no tolerance.
import sys, re, hashlib
from mpmath import mp, mpf, sqrt

mp.dps = 50
claim_dir = sys.argv[1]
N_EXPECTED, D_EXPECTED = 66, 4

def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def parse_candidate(path):
    pts = []
    for ln in open(path, encoding='ascii'):
        s = ln.strip()
        if not s or s.startswith('#'):
            continue
        toks = s.split()
        assert len(toks) == D_EXPECTED, f"candidate line has {len(toks)} fields: {s!r}"
        pts.append([mpf(t) for t in toks])
    return pts

def parse_posted(path):
    lines = [l.strip() for l in open(path, encoding='ascii') if l.strip()]
    radius = mpf(lines[0])
    pts = []
    for k, s in enumerate(lines[1:], start=1):
        toks = s.split()
        assert len(toks) == D_EXPECTED + 1, f"posted line has {len(toks)} fields: {s!r}"
        assert int(toks[0]) == k, f"posted index mismatch {toks[0]} != {k}"
        pts.append([mpf(t) for t in toks[1:]])
    return radius, pts

def parse_table(path):
    tab = {}
    for ln in open(path, encoding='ascii'):
        s = ln.strip()
        if not s:
            continue
        n, r = s.split()
        assert re.fullmatch(r'\d+\.\d{12}', r), f"table value not 12-decimal: {r!r}"
        tab[int(n)] = mpf(r)
    return tab

def norm(v):
    return sqrt(sum(x*x for x in v))

def dist(a, b):
    return sqrt(sum((x-y)*(x-y) for x, y in zip(a, b)))

def feasible_radius(pts):
    # exactly the definition, no tolerance
    n = len(pts)
    dmin = None
    for i in range(n):
        for j in range(i+1, n):
            d = dist(pts[i], pts[j])
            if dmin is None or d < dmin:
                dmin = d
    rmax = max(norm(p) for p in pts)
    return min(dmin/2, 1 - rmax), dmin, rmax

def sorted_dists(pts):
    n = len(pts)
    return sorted(dist(pts[i], pts[j]) for i in range(n) for j in range(i+1, n))

def allfinite(pts):
    return all(mp.isfinite(x) and not mp.isnan(x) for p in pts for x in p)

cand_path = f"{claim_dir}/hsp4-66-candidate.txt"
post_path = f"{claim_dir}/hsp4-66-posted.txt"
tab_path  = f"{claim_dir}/hsp4_radius_as_fetched.txt"
for p in (cand_path, post_path, tab_path):
    print("sha256", p.split('/')[-1], sha(p))

cand = parse_candidate(cand_path)
post_r, post = parse_posted(post_path)
tab = parse_table(tab_path)

ok = True
def chk(name, cond, detail=""):
    global ok
    print(f"[{'PASS' if cond else 'FAIL'}] {name} {detail}")
    ok = ok and bool(cond)

chk("candidate has exactly 66 points", len(cand) == N_EXPECTED, f"(got {len(cand)})")
chk("candidate all entries finite", allfinite(cand))
chk("candidate dimension 4", all(len(p) == D_EXPECTED for p in cand))
chk("posted has exactly 66 points", len(post) == N_EXPECTED, f"(got {len(post)})")
chk("posted all entries finite", allfinite(post))
chk("table has 299 rows", len(tab) == 299, f"(got {len(tab)})")
chk("table has row N=66", 66 in tab)
T = tab[66]
print("table value N=66 :", mp.nstr(T, 20))
chk("table N=66 == 0.264968466676", T == mpf("0.264968466676"))

# parser sanity: posted packing reproduces table value within 1e-11
rp, dmin_p, rmax_p = feasible_radius(post)
print("posted  r*      :", mp.nstr(rp, 30))
print("posted  dmin/2  :", mp.nstr(dmin_p/2, 30), " 1-rmax:", mp.nstr(1-rmax_p, 30))
print("posted  header  :", mp.nstr(post_r, 20))
chk("posted r* within 1e-11 of table", abs(rp - T) < mpf("1e-11"), f"(|diff|={mp.nstr(abs(rp-T),5)})")
chk("posted header within 1e-11 of table", abs(post_r - T) < mpf("1e-11"))

# the claim
rc, dmin_c, rmax_c = feasible_radius(cand)
print("cand    r*      :", mp.nstr(rc, 40))
print("cand    dmin/2  :", mp.nstr(dmin_c/2, 30), " 1-rmax:", mp.nstr(1-rmax_c, 30))
gain = rc - T
print("gain r*-table   :", mp.nstr(gain, 20))
chk("candidate r* > table by >= 1e-10", gain >= mpf("1e-10"), f"(gain={mp.nstr(gain,8)})")
chk("candidate r* matches claimed 0.26497636751387...", mp.nstr(rc, 14) == "0.26497636751388" or str(rc).startswith("0.26497636751387"), f"(r*={mp.nstr(rc,20)})")
chk("all candidate points strictly inside unit ball", rmax_c < 1, f"(max|c|={mp.nstr(rmax_c,20)})")
chk("candidate r* > 0", rc > 0)

# non-isometry: sorted pairwise-distance multisets differ by > 1e-8 somewhere
sc, sp = sorted_dists(cand), sorted_dists(post)
chk("both multisets have 2145 distances", len(sc) == 2145 and len(sp) == 2145)
maxdiff = max(abs(a-b) for a, b in zip(sc, sp))
cnt = sum(1 for a, b in zip(sc, sp) if abs(a-b) > mpf("1e-8"))
print("max |sorted-dist diff| :", mp.nstr(maxdiff, 15), " count>1e-8:", cnt)
chk("not isometric (some sorted-dist diff > 1e-8)", maxdiff > mpf("1e-8"))

print("RSTAR_FULL", str(rc))
print("ALL_OK", ok)
```

## Real output (run 1)

```
sha256 hsp4-66-candidate.txt ca99c57be72385d9de9eba5271e5f4cbc7e32be01c9f53a988733fc8163c5b00
sha256 hsp4-66-posted.txt 57308d5c974118500d9cf7cc9f433c1dd431c8f31f801277593ec4cd4464af3f
sha256 hsp4_radius_as_fetched.txt f3ddaa944aac014718bc9f5438700698abedac0189266198df8bb60772ac569f
[PASS] candidate has exactly 66 points (got 66)
[PASS] candidate all entries finite 
[PASS] candidate dimension 4 
[PASS] posted has exactly 66 points (got 66)
[PASS] posted all entries finite 
[PASS] table has 299 rows (got 299)
[PASS] table has row N=66 
table value N=66 : 0.264968466676
[PASS] table N=66 == 0.264968466676 
posted  r*      : 0.264968466675015943360724251452
posted  dmin/2  : 0.264968466675254826108211627374  1-rmax: 0.264968466675015943360724251452
posted  header  : 0.264968466676
[PASS] posted r* within 1e-11 of table (|diff|=9.8406e-13)
[PASS] posted header within 1e-11 of table 
cand    r*      : 0.2649763675138760232890087127252488634598
cand    dmin/2  : 0.264976367514121836940619590717  1-rmax: 0.264976367513876023289008712725
gain r*-table   : 7.9008378760232890087e-6
[PASS] candidate r* > table by >= 1e-10 (gain=7.9008379e-6)
[PASS] candidate r* matches claimed 0.26497636751387... (r*=0.26497636751387602329)
[PASS] all candidate points strictly inside unit ball (max|c|=0.73502363248612397671)
[PASS] candidate r* > 0 
[PASS] both multisets have 2145 distances 
max |sorted-dist diff| : 0.0199570038758061  count>1e-8: 2145
[PASS] not isometric (some sorted-dist diff > 1e-8) 
RSTAR_FULL 0.26497636751387602328900871272524886345982755040961
ALL_OK True
```

Run 2 (same command, fresh interpreter): `diff run1.txt run2.txt` is empty — output byte-identical, including the full 50-digit `RSTAR_FULL 0.26497636751387602328900871272524886345982755040961`.

File hashes (sha256) of the inputs I checked are printed at the top of the output.

## Property-by-property verdicts

| # | Property | Result | Evidence |
|---|----------|--------|----------|
| 1 | hsp4-66-candidate.txt contains exactly 66 points | PASS | parser counted 66 non-comment lines, each 4 fields |
| 2 | All candidate coordinates finite (no nan/inf) | PASS | mp.isfinite on all 264 entries |
| 3 | Dimension is 4 | PASS | every line has exactly 4 tokens |
| 4 | hsp4-66-posted.txt parses to 66 indexed points, header radius present | PASS | indices 1..66 contiguous, 4 coords each |
| 5 | hsp4_radius_as_fetched.txt has 299 rows, all 12-decimal, row 66 = 0.264968466676 | PASS | regex `\d+\.\d{12}` on every row; exact equality for N=66 |
| 6 | Parser sanity: r*(posted) reproduces table value within 1e-11 | PASS | r*(posted) = 0.264968466675015943..., diff from table = 9.84e-13 (< 1e-11); posted header line also equals table |
| 7 | r*(candidate), mpmath dps=50, no tolerance | PASS | r* = 0.26497636751387602328900871272524886345982755040961; binding constraint is the container (1 - max|c| = 0.2649763675138760..., min-dist/2 = 0.2649763675141218...) |
| 8 | r*(candidate) - table >= 1e-10 | PASS | gain = 7.9008378760e-6 (about 79,000x the required margin) |
| 9 | r*(candidate) agrees with the value stated in CLAIM.md (0.26497636751387...) and in the candidate's comment line (r_float=0.26497636751387599) | PASS | 0.264976367513876023... matches both to all stated digits |
| 10 | All candidate centres strictly inside the unit ball | PASS | max|c| = 0.735023632486123976... < 1 |
| 11 | Not isometric to posted: sorted pairwise-distance multisets differ by > 1e-8 somewhere | PASS | both multisets have C(66,2)=2145 entries; max |difference| = 0.0199570038758; all 2145 positions differ by > 1e-8 |
| 12 | Determinism of r*(candidate) across two independent runs | PASS | run outputs byte-identical |

## Comparison with the author's REPRODUCE.md (read only after the above)

The author's embedded script computes the same definition (dmin/2 vs 1 - max norm, mp.dps = 50, no tolerance; sorted-distance comparison for isometry). I ran it once offline (the three `curl` lines were NOT executed — no network allowed for this role; the live re-fetch / History-of-updates / pending-queue checks are outside my scope and remain for the other skeptics). Its output:

```
N candidate = 66  N posted = 66
r* candidate = 0.2649763675138760232890087
r* posted    = 0.2649684666750159433607243
table        = 0.264968466676
gain = r*cand - table = 7.9008379e-6  -> meets 1e-10 margin: True
max |sorted distance difference| vs posted = 0.019957004
```

Every number agrees with my independent checker to all printed digits. No mismatch found.

## Mismatches / caveats

- No numerical or structural mismatch anywhere.
- Not verified here (out of scope for REPRODUCE, no web): that the live radius.txt row 66 is still 0.264968466676, that no newer History-of-updates entry covers (4, 66), and the pending-requests queue rule (including the category-unspecified "Moki & Julio *many* 4666 candidates" bundle caveat that CLAIM.md itself flags). Those must be covered by the other panel members.
- Minor note: the candidate's r* is container-bound (1 - max|c|), with the pairwise constraint only 2.5e-13 larger; this does not affect any criterion.

pass: true
