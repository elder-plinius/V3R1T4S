# REPRODUCE verdict for claim N111 (hsp4, N = 111)

context: subagent (Claude Code Agent tool, fresh context for this one claim)

Scope: I read only CLAIM.md, hsp4-111-candidate.txt, hsp4-111-posted.txt and hsp4_radius_as_fetched.txt, wrote my own checker from the definition below, ran it, and only afterwards read REPRODUCE.md. No web fetches were made.

## Definition used (quoted from the success criterion in CLAIM.md)

"the FEASIBLE radius r* := min( min_{i,j, i before j} |c_i - c_j| / 2, 1 - max_i |c_i| ) (unit container ball centred at the origin), computed in mpmath at 50 digits directly from the submitted coordinates with no tolerance, is STRICTLY GREATER (direction: max) than that file's 12-decimal value for N re-fetched live immediately before claiming, by at least 1e-10 [...], AND the configuration is not isometric to the posted hsp[d]-[N].txt configuration (sorted pairwise-distance multisets differ by more than 1e-8 somewhere)"

(Transcription note: the original writes the pair condition as "i less-than j" with the less-than symbol, and names the posted file with the dimension and N in angle brackets; both are spelled out here only to keep this file free of angle-bracket characters. The mathematics is unchanged.)

File-format assumptions I derived from the files themselves, not from the author's code:
- hsp4-111-candidate.txt: lines beginning with "#" are comments; every other non-blank line must have exactly 4 decimal tokens.
- hsp4-111-posted.txt: first line is the radius; every later line is "index x1 x2 x3 x4" (5 tokens, the index dropped).
- hsp4_radius_as_fetched.txt: rows "N radius"; exactly one row must start with the token "111".
- All coordinates are converted with mpf(decimal string) at mp.dps = 50, with no float64 round-trip.

## Checker (my own code, run with the project venv's python -I; argument = the claim folder)

```python
# Independent checker for the N=111 hsp4 claim, written from the definition
# quoted in CLAIM.md (success criterion):
#   r* := min( min over pairs i,j (i before j) of |c_i - c_j| / 2 , 1 - max_i |c_i| )
#   unit container ball centred at the origin; computed in mpmath at 50 digits
#   directly from the submitted coordinates with no tolerance; must exceed the
#   table's 12-decimal value for N by at least 1e-10; and the configuration must
#   not be isometric to the posted one (sorted pairwise-distance multisets differ
#   by more than 1e-8 somewhere).
# Comparison operators are spelled via the operator module (lt/gt/ge) only so
# that this source contains no angle-bracket characters when pasted verbatim.
import sys, hashlib
from operator import lt, gt, ge
from mpmath import mp, mpf, sqrt, isfinite

mp.dps = 50
claim_dir = sys.argv[1]
N_EXPECT = 111
D_EXPECT = 4

def read_candidate(path):
    pts = []
    with open(path) as f:
        for ln in f:
            s = ln.strip()
            if not s or s.startswith('#'):
                continue
            toks = s.split()
            if len(toks) != D_EXPECT:
                raise SystemExit(f"FAIL candidate line has {len(toks)} tokens: {s!r}")
            pts.append([mpf(t) for t in toks])   # mpf from decimal string, no float round-trip
    return pts

def read_posted(path):
    with open(path) as f:
        lines = [l.strip() for l in f if l.strip()]
    rad = mpf(lines[0])
    pts = []
    for s in lines[1:]:
        toks = s.split()
        if len(toks) != D_EXPECT + 1:
            raise SystemExit(f"FAIL posted line has {len(toks)} tokens: {s!r}")
        pts.append([mpf(t) for t in toks[1:]])
    return rad, pts

def read_table(path, N):
    val = None; hits = 0
    with open(path) as f:
        for ln in f:
            toks = ln.split()
            if ge(len(toks), 2) and toks[0] == str(N):
                val = mpf(toks[1]); hits += 1
    if hits != 1:
        raise SystemExit(f"FAIL table has {hits} rows for N={N}")
    return val

def norm(p):
    return sqrt(sum(x*x for x in p))

def dist(p, q):
    return sqrt(sum((a-b)*(a-b) for a, b in zip(p, q)))

def rstar(pts, order="forward"):
    n = len(pts)
    pairs = [(i, j) for i in range(n) for j in range(i+1, n)]
    if order == "reverse":
        pairs = pairs[::-1]
    dmin = None
    for i, j in pairs:
        d = dist(pts[i], pts[j])
        if dmin is None or lt(d, dmin):
            dmin = d
    rmax = max(norm(p) for p in pts)
    return min(dmin / 2, 1 - rmax), dmin, rmax

def sorted_dists(pts):
    n = len(pts)
    return sorted(dist(pts[i], pts[j]) for i in range(n) for j in range(i+1, n))

ok = True
def prop(name, cond, detail=""):
    global ok
    print(f"[{'PASS' if cond else 'FAIL'}] {name} {detail}")
    ok = ok and bool(cond)

cand = read_candidate(f"{claim_dir}/hsp4-111-candidate.txt")
posted_rad, posted = read_posted(f"{claim_dir}/hsp4-111-posted.txt")
table = read_table(f"{claim_dir}/hsp4_radius_as_fetched.txt", N_EXPECT)

prop("candidate has exactly 111 points", len(cand) == N_EXPECT, f"(got {len(cand)})")
prop("candidate points all in R^4", all(len(p) == D_EXPECT for p in cand))
prop("candidate coords all finite", all(isfinite(x) for p in cand for x in p))
prop("posted has exactly 111 points", len(posted) == N_EXPECT, f"(got {len(posted)})")
prop("posted coords all finite", all(isfinite(x) for p in posted for x in p))
print("table value for N=111         :", mp.nstr(table, 20))
print("posted-file header radius      :", mp.nstr(posted_rad, 20))

rp, dminp, rmaxp = rstar(posted)
print("posted r* (50 digits)          :", mp.nstr(rp, 50))
print("  posted dmin/2, 1-rmax        :", mp.nstr(dminp/2, 25), mp.nstr(1-rmaxp, 25))
prop("posted r* reproduces table within 1e-11", lt(abs(rp - table), mpf("1e-11")), f"(|diff| = {mp.nstr(abs(rp-table), 5)})")

rc1, dminc, rmaxc = rstar(cand, "forward")
rc2, _, _ = rstar(cand, "reverse")
print("candidate r* (50 digits, fwd)  :", mp.nstr(rc1, 50))
print("candidate r* (50 digits, rev)  :", mp.nstr(rc2, 50))
print("  cand dmin/2, 1-rmax          :", mp.nstr(dminc/2, 25), mp.nstr(1-rmaxc, 25))
prop("candidate r* identical under reversed pair order", rc1 == rc2)
prop("candidate r* strictly greater than table", gt(rc1, table), f"(gain = {mp.nstr(rc1 - table, 10)})")
prop("candidate r* minus table at least 1e-10", ge(rc1 - table, mpf("1e-10")))
prop("all candidate balls inside unit ball (1 - rmax positive)", gt(1 - rmaxc, 0))
prop("no two candidate centres coincide (dmin positive)", gt(dminc, 0))
prop("claimed value 0.237359570027502... matches prefix", mp.nstr(rc1, 15).startswith("0.23735957002750"), f"(got {mp.nstr(rc1, 15)})")

sc = sorted_dists(cand); sp = sorted_dists(posted)
prop("pairwise-distance multisets same size", len(sc) == len(sp) == N_EXPECT*(N_EXPECT-1)//2)
maxdiff = max(abs(a-b) for a, b in zip(sc, sp))
prop("not isometric to posted: max |sorted-dist diff| exceeds 1e-8", gt(maxdiff, mpf("1e-8")), f"(max diff = {mp.nstr(maxdiff, 8)})")

# fingerprint of full-precision result for cross-run determinism check
fp = hashlib.sha256(mp.nstr(rc1, 50).encode()).hexdigest()
print("RSTAR_CAND_50 =", mp.nstr(rc1, 50))
print("FINGERPRINT   =", fp)
print("OVERALL:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
```

## Real output (run 1; run 2 produced a byte-identical file, sha256 e8da9d1bf60036475f4bb9551aee2b17ee481e94f9fc1c566c6c278b8f4a205a for both)

```
[PASS] candidate has exactly 111 points (got 111)
[PASS] candidate points all in R^4 
[PASS] candidate coords all finite 
[PASS] posted has exactly 111 points (got 111)
[PASS] posted coords all finite 
table value for N=111         : 0.237355353009
posted-file header radius      : 0.237355353009
posted r* (50 digits)          : 0.23735535300820492223693554669958508173698186289496
  posted dmin/2, 1-rmax        : 0.2373553530082618577947255 0.2373553530082049222369355
[PASS] posted r* reproduces table within 1e-11 (|diff| = 7.9508e-13)
candidate r* (50 digits, fwd)  : 0.23735957002750166280229786794662708494149688154608
candidate r* (50 digits, rev)  : 0.23735957002750166280229786794662708494149688154608
  cand dmin/2, 1-rmax          : 0.2373595700277416870958524 0.2373595700275016628022979
[PASS] candidate r* identical under reversed pair order 
[PASS] candidate r* strictly greater than table (gain = 4.217018502e-6)
[PASS] candidate r* minus table at least 1e-10 
[PASS] all candidate balls inside unit ball (1 - rmax positive) 
[PASS] no two candidate centres coincide (dmin positive) 
[PASS] claimed value 0.237359570027502... matches prefix (got 0.237359570027502)
[PASS] pairwise-distance multisets same size 
[PASS] not isometric to posted: max |sorted-dist diff| exceeds 1e-8 (max diff = 0.0043084619)
RSTAR_CAND_50 = 0.23735957002750166280229786794662708494149688154608
FINGERPRINT   = 829ded5707eafe8f029daac5d1e2a6a0b458d215d14cf75da9c1041b0adddc1c
OVERALL: PASS
```

Both runs exited 0. The 50-digit r* fingerprint (sha256 of the 50-digit decimal string) 829ded5707eafe8f029daac5d1e2a6a0b458d215d14cf75da9c1041b0adddc1c was also identical to an earlier draft of the checker that used ordinary comparison operators, so the value does not depend on operator spelling, pair iteration order, or process.

## Properties, each with verdict

1. Exactly 111 points in the candidate, each with 4 coordinates: PASS (111 lines of 4 tokens after the single "#" comment line).
2. All candidate coordinates finite: PASS (mpmath isfinite on all 444 values).
3. Posted file parses to exactly 111 finite points: PASS.
4. Parser sanity, posted r* reproduces the table value within 1e-11: PASS. Posted r* = 0.237355353008204922... ; table = 0.237355353009; |diff| = 7.95e-13. (The posted packing is container-limited: 1 - rmax = 0.2373553530082049 is the binding term, dmin/2 = 0.2373553530082619.)
5. Candidate r* computed at 50 digits with no tolerance: r* = 0.23735957002750166280229786794662708494149688154608. Binding term is 1 - rmax = 0.2373595700275016628...; dmin/2 = 0.2373595700277416871... (the two terms agree to about 2.4e-13, so the packing is tight in both senses and r* is well inside the container, 1 - rmax positive, and dmin positive).
6. Candidate r* strictly greater than table value: PASS. gain = 4.217018502e-06.
7. gain at least 1e-10: PASS (4.2e-06 is about 42,000 times the required margin).
8. Claimed value "0.237359570027502..." in CLAIM.md: PASS, matches my r* to the 15 digits stated. The comment line in the candidate file gives r_float = 0.23735957002750163, which differs from the exact 50-digit value 0.2373595700275016628 by about 3e-17, i.e. one float64 ulp; consistent with a double-precision evaluation, not a mismatch in the certified quantity.
9. Not isometric to the posted packing: PASS. Both sorted pairwise-distance multisets have 6105 entries; the maximum absolute difference between corresponding sorted entries is 4.308e-03, far above 1e-8.
10. Determinism of r* across two separate runs: PASS. Two independent process invocations produced byte-identical output (same sha256), and forward versus reversed pair iteration gave the same 50-digit value within one run.

## Comparison with the author's REPRODUCE.md (read only after the above)

- The author's script implements the same r* formula (min of dmin/2 and 1 - max norm) at mp.dps = 50 from mpf(decimal string), and the same isometry test (sorted pairwise distances, max absolute difference compared with 1e-8). Its parser takes the last 4 tokens of each line, which handles both file layouts; my parser is stricter (exact token counts) and reaches the same 111 points for each file. No discrepancy between their method and the quoted definition.
- Their printed quantities (r* candidate to 25 digits, r* posted, table, gain, max sorted-distance difference) agree with mine to every digit shown.
- The three curl commands in REPRODUCE.md (live radius.txt row, "Last update" line on hsp4.html, pending-requests page) are outside my remit: I made no network requests, so the live re-fetch, the History-of-updates check and the QUEUE RULE are NOT verified here and remain for the panel's scout/liveness skeptic. Per the success criterion, the "Moki & Julio *many* 4666 candidates" bundle caveat applies and must be stated in the final verdict; I cannot resolve it offline.

## Mismatches

None found in anything I could check from the saved files. No missing objects, no non-determinism.

Verdict on the REPRODUCE scope (object properties, claimed value, margin, non-isometry, parser sanity, determinism): all confirmed by my own checker from the definition.

pass: true
