# REPRODUCE verdict — hsp4, N = 54

context: subagent (Claude Code Agent tool, fresh context; one context panelled 14 separate claims, each judged on its own files)

## Definition checked (quoted from CLAIM.md, section "Success criterion")

> Success means N centers in R^d (d in {4,5,6}) for one N listed in the live
> https://packomania.com/hsp(d)/txt/radius.txt such that the FEASIBLE radius
> r* := min( min_{i<j} |c_i - c_j| / 2, 1 - max_i |c_i| ) (unit container ball
> centred at the origin), computed in mpmath at 50 digits directly from the
> submitted coordinates with no tolerance, is STRICTLY GREATER (direction: max)
> than that file's 12-decimal value for N re-fetched live immediately before
> claiming, by at least 1e-10 (the table carries 12 decimals; 1e-10 is 200x its
> rounding), AND the configuration is not isometric to the posted hsp(d)-(N).txt
> configuration (sorted pairwise-distance multisets differ by more than 1e-8
> somewhere), AND (d, N) does not appear in a History-of-updates entry on the
> live hsp(d).html newer than the one the scout fetched. QUEUE RULE [...]

Only the parts of the criterion that are decidable from the saved files are judged here: the feasible radius r*, the >= 1e-10 margin over the table value stored in hsp4_radius_as_fetched.txt, and non-isometry against hsp4-54-posted.txt. The live re-fetch, History-of-updates and queue-rule parts need the web and are outside this REPRODUCE verdict (no web access was used).

## Method

The checker below was written from the definition above BEFORE the author's REPRODUCE.md was opened. It was run with the project's mpmath interpreter as `python -I check_hsp4.py the claim folder, then 54`, twice, and the two outputs were compared byte for byte. Inputs are the three files in the claim folder: hsp4-54-candidate.txt, hsp4-54-posted.txt, hsp4_radius_as_fetched.txt.

Parsing rules I imposed (stricter than the author's): every non-comment candidate line must have exactly 4 plain finite decimal tokens; every posted line after the radius header must be `index x1 x2 x3 x4` with consecutive indices; the table may not contain a duplicate row for N; files are read as ASCII.

## Checker (check_hsp4.py)

```python
#!/usr/bin/env python3 -I
"""Independent REPRODUCE checker written from the CLAIM.md definition:

  r* := min( min_{i<j} |c_i - c_j| / 2 , 1 - max_i |c_i| )   (unit ball container
  centred at the origin), computed in mpmath at 50 digits directly from the
  submitted coordinates with no tolerance; must be STRICTLY GREATER than the
  table's 12-decimal value for N by at least 1e-10; and the configuration must
  not be isometric to the posted hsp4-(N).txt (sorted pairwise-distance
  multisets differ by more than 1e-8 somewhere).

Usage: python -I check_hsp4.py the claim folder, then N
Output is fully deterministic (no timestamps, no randomness).
"""
import sys, os, re
from mpmath import mp, mpf, sqrt, nstr, isfinite

mp.dps = 50
claim_dir, N = sys.argv[1], int(sys.argv[2])
ok = True
def report(name, good, detail=""):
    global ok
    ok = ok and bool(good)
    print(f"[{'OK  ' if good else 'FAIL'}] {name}" + (f": {detail}" if detail else ""))

NUM = re.compile(r'^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$')
def tok2mpf(t):
    if not NUM.match(t):
        raise ValueError(f"token {t!r} is not a plain finite decimal literal")
    v = mpf(t)
    if not isfinite(v):
        raise ValueError(f"token {t!r} is not finite")
    return v

def read_candidate(path):
    pts = []
    with open(path, encoding="ascii") as f:
        for ln, line in enumerate(f, 1):
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            toks = s.split()
            if len(toks) != 4:
                raise ValueError(f"line {ln}: expected 4 coordinates, got {len(toks)}")
            pts.append([tok2mpf(t) for t in toks])
    return pts

def read_posted(path):
    pts = []
    with open(path, encoding="ascii") as f:
        lines = [l.strip() for l in f if l.strip()]
    radius = tok2mpf(lines[0])
    for ln, s in enumerate(lines[1:], 2):
        toks = s.split()
        if len(toks) != 5:
            raise ValueError(f"posted line {ln}: expected 'index x1 x2 x3 x4', got {len(toks)} tokens")
        if int(toks[0]) != ln - 1:
            raise ValueError(f"posted line {ln}: index {toks[0]} != {ln-1}")
        pts.append([tok2mpf(t) for t in toks[1:]])
    return radius, pts

def read_table(path, n):
    rows = {}
    with open(path, encoding="ascii") as f:
        for s in f:
            toks = s.split()
            if len(toks) != 2:
                continue
            k = int(toks[0])
            if k in rows:
                raise ValueError(f"duplicate table row for N={k}")
            rows[k] = (tok2mpf(toks[1]), toks[1])
    if n not in rows:
        raise ValueError(f"no table row for N={n}")
    return rows[n]

def norm(p):
    return sqrt(sum(x * x for x in p))

def pair_dists(pts):
    d = []
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            d.append(sqrt(sum((a - b) ** 2 for a, b in zip(pts[i], pts[j]))))
    return d

def rstar(pts):
    dmin = min(pair_dists(pts))
    rmax = max(norm(p) for p in pts)
    return min(dmin / 2, 1 - rmax), dmin, rmax

cand_path = os.path.join(claim_dir, f"hsp4-{N}-candidate.txt")
post_path = os.path.join(claim_dir, f"hsp4-{N}-posted.txt")
tab_path = os.path.join(claim_dir, "hsp4_radius_as_fetched.txt")
for p in (cand_path, post_path, tab_path):
    report(f"file present {os.path.basename(p)}", os.path.isfile(p))
if not ok:
    print("pass: false"); sys.exit(1)

print(f"mpmath dps = {mp.dps}; N = {N}")
cand = read_candidate(cand_path)
report("candidate has exactly N finite 4-vectors", len(cand) == N, f"count={len(cand)}")
prad, post = read_posted(post_path)
report("posted has exactly N finite 4-vectors", len(post) == N, f"count={len(post)}")
tval, tstr = read_table(tab_path, N)
print(f"table row N={N}: {tstr}")
report("posted-file header radius equals table string", prad == tval, f"header={nstr(prad, 15)}")

# parser sanity: posted packing reproduces the table value within 1e-11
rp, dp, mp_ = rstar(post)
diff_p = abs(rp - tval)
print(f"posted  r* = {nstr(rp, 25)}  (dmin/2={nstr(dp/2, 20)}, 1-rmax={nstr(1-mp_, 20)})")
report("posted r* within 1e-11 of table value", diff_p <= mpf("1e-11"), f"|diff|={nstr(diff_p, 6)}")

# candidate feasible radius
rc, dc, mc = rstar(cand)
print(f"cand    r* = {nstr(rc, 25)}  (dmin/2={nstr(dc/2, 20)}, 1-rmax={nstr(1-mc, 20)})")
print(f"cand    binding term = {'contact (dmin/2)' if dc/2 <= 1-mc else 'container (1-rmax)'}")
gain = rc - tval
print(f"gain = r*(cand) - table = {nstr(gain, 20)}")
report("gain >= 1e-10", gain >= mpf("1e-10"), f"gain={nstr(gain, 18)}  (strictly > 1e-10: {gain > mpf('1e-10')})")
report("r*(cand) strictly > table", rc > tval)

# non-isometry via sorted pairwise-distance multisets
sc, sp = sorted(pair_dists(cand)), sorted(pair_dists(post))
report("distance multisets same size", len(sc) == len(sp) == N * (N - 1) // 2)
maxdiff = max(abs(a - b) for a, b in zip(sc, sp))
report("not isometric (max |sorted-dist diff| > 1e-8)", maxdiff > mpf("1e-8"), f"maxdiff={nstr(maxdiff, 8)}")

print("pass: " + ("true" if ok else "false"))
sys.exit(0 if ok else 1)
```

## Real output for this claim (run 1; run 2 was byte-identical)

```
[OK  ] file present hsp4-54-candidate.txt
[OK  ] file present hsp4-54-posted.txt
[OK  ] file present hsp4_radius_as_fetched.txt
mpmath dps = 50; N = 54
[OK  ] candidate has exactly N finite 4-vectors: count=54
[OK  ] posted has exactly N finite 4-vectors: count=54
table row N=54: 0.276798004181
[OK  ] posted-file header radius equals table string: header=0.276798004181
posted  r* = 0.2767980041803679641154472  (dmin/2=0.2767980041806115729, 1-rmax=0.27679800418036796412)
[OK  ] posted r* within 1e-11 of table value: |diff|=6.32036e-13
cand    r* = 0.2767986956871073856588077  (dmin/2=0.27679869568712578496, 1-rmax=0.27679869568710738566)
cand    binding term = container (1-rmax)
gain = r*(cand) - table = 6.9150610738565880774e-7
[OK  ] gain >= 1e-10: gain=6.91506107385658808e-7  (strictly > 1e-10: True)
[OK  ] r*(cand) strictly > table
[OK  ] distance multisets same size
[OK  ] not isometric (max |sorted-dist diff| > 1e-8): maxdiff=0.0037362048
pass: true
```

## Properties

- Files present (hsp4-54-candidate.txt, hsp4-54-posted.txt, hsp4_radius_as_fetched.txt): PASS
- Exactly N = 54 finite points in R^4 in the candidate (and in the posted file): PASS
- Parser sanity — posted packing reproduces its table value 0.276798004181 within 1e-11: PASS (posted r* = 0.2767980041803679641154472, |diff| = 6.32036e-13; the posted-file header radius also equals the table string)
- r* of candidate (mpmath, 50 digits, no tolerance): 0.2767986956871073856588077; binding term = container (1-rmax)
- Gain r*(cand) - table = 6.9150610738565880774e-7 (20 significant digits); gain >= 1e-10: PASS; strictly > 1e-10: True
- r*(cand) strictly greater than the table value: PASS
- Non-isometry — max |sorted pairwise-distance difference| vs posted = 0.0037362048 > 1e-8: PASS (both multisets have 1431 entries)
- Determinism — two independent runs of the checker produced byte-identical output: PASS
- CLAIM.md consistency — the r* and gain stated in CLAIM.md and in the candidate's `#` header line agree with my values to the digits given: PASS

## Comparison with the author's REPRODUCE.md (read only after my checker had been run)

The author's script uses the same formula (min of half the minimum pairwise distance and 1 - max norm, mp.dps = 50, mpf parsing, sorted distance multisets, >= mpf('1e-10')). It differs only in a looser loader (it keeps the last 4 tokens of any line with >= 4 tokens, so it silently skips the posted file's radius header, which my checker instead reads and cross-checks against the table). Its three curl steps against the live site were NOT executed by me and are not part of this verdict. My numbers match what the author reports in CLAIM.md.

## Verdict

All file-decidable properties of the criterion hold for N = 54: the candidate has exactly 54 finite points, its feasible radius 0.2767986956871073... exceeds the table value 0.276798004181 by 6.9150610738... (>= 1e-10), and it is not isometric to the posted packing. Output is deterministic.

pass: true
