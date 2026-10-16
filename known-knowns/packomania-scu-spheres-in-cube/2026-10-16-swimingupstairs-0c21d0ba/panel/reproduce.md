# REPRODUCE skeptic verdict: N=883

context: subagent (fresh knowledgeWork context, given only this claim folder + kit/RULES.md), run 2026-10-16T16:07Z
verdict: PASS (REPRODUCE scope only: geometry of scu883_candidate.txt and its margin over radius.txt)

## Definition used (quoted from CRITERION_VERBATIM.md)
"r* := min( min_{i<j} |c_i - c_j| / 2, 1/2 - max_i max(|x_i|,|y_i|,|z_i|) ) for the cube [-1/2, 1/2]^3",
i.e. spheres of radius r with centres c_i inside the unit cube [-1/2,1/2]^3: no overlap iff |c_i-c_j| >= 2r for all
i<j, containment iff max|coord| <= 1/2 - r.

## Own checker (written before reading the folder's exact.py / scu_check.py; not derived from them)
- Strict parse: every non-empty line must be exactly 3 ASCII decimal tokens (regex), no exponents/NaN/inf; file is
  pure ASCII, no CR. Each coordinate -> exact Fraction -> integer over the common denominator 10^K.
- ALL n(n-1)/2 pairs, squared distances in exact integer arithmetic (no floats, no near-pair filter, no sampling).
- Pass test with no sqrt: D2_min >= 4 (t + 1e-11)^2 and (1/2 - max|coord|) >= t + 1e-11, exact rationals,
  t = row 883 of radius.txt. Overlap/containment re-tested exactly at the CLAIMED r* too. r* printed via mpmath 60 dp.
- Isometry: own parser for scu883.txt (index + x y z [+ r] rows); exact min squared distance of both sets compared,
  and when sizes match, sorted pairwise-distance multisets compared.

## Files checked
- scu883_candidate.txt sha256 0c21d0ba63ae82e4add18753bd3626d77bc483cb5e9937fac0b8536605e4f7cc
- scu883.txt sha256 10787891a72dfd317b2e25287b2e79f609677427203af76e4ff482bae90ce0d1
- radius.txt (identical across all claim folders)

## Own checker output (verbatim)
    file=claim_883/scu883_candidate.txt rows=883 bad_lines=0 N_expected=883 count_ok=True distinct=True
      minD2_exact=123850370110045092598611485322706053123/10000000000000000000000000000000000000000  closest_pair=(713, 882)
      r_pair=0.0556440405861321982679037439293 r_wall=0.05564404058613009463 r*=0.05564404058613009463
      claimed r*=0.05564404058613009463 matches(1e-19)=True  no_overlap@claimed=True contained@claimed=True
      table=0.055542517155 r*-table=0.00010152343113  pairs_ok@t+1e-11=True wall_ok@t+1e-11=True  BEATS=True
      posted claim_883/scu883.txt: rows=882 nonrow_lines=[(1, '0.055542517155'), (889, '883')]
      sizes differ (883 vs 882) -> not isometric

## Own isometry check (verbatim)
    cand n=883 posted coord rows=882 blank-index rows=1  cand minD2>posted minD2  (cand 0.0123850370110045 posted 0.012339884847526)

## Cross-check: folder's exact.py (run only after my own result; agrees, deterministic)
    scu883_candidate.txt n=883 r*=0.05564404058613009463 table=0.055542517155 diff=0.000101523 pass_1e-11=True

## Findings
1. Sphere count: 883 rows, exactly 3 decimal columns each, no bad lines, all centres distinct; matches N=883 in CLAIM.md. PASS.
2. Overlaps: exact all-pairs minimum shown above; no pair closer than 2·(claimed r*), and none closer than 2·(t+1e-11). PASS.
3. Containment: every centre has max|coord| <= 1/2 - (claimed r*) exactly. PASS.
4. Radius: recomputed r* equals the claimed r* in CLAIM.md to all 20 stated digits; r* - t exceeds 1e-11 by a wide
   margin (exact rational test). PASS.
5. Non-isometry to the posted file: exact minimum distance of the candidate is strictly larger than that of the posted
   coordinates, so the sorted distance multisets cannot coincide. PASS.

## Caveats for the other skeptics (outside REPRODUCE scope, not judged here)
- REPRODUCE.md step 2 (isometry.py) needs scipy, which is not installed in this environment; I did not install it
  (RULES.md 10) and used my own isometry check above instead.
- radius.txt in this folder carries only 12 decimals for this row (criterion text says 30); irrelevant here because
  the margin is >= 8e-6, but CRITERION should confirm against the live file.
- For N in {619, 806, 881, 882, 883} the posted scuN.txt lists N-1 coordinate rows plus a final index-only row with
  no coordinates. For N=806 the candidate r* is also about 1.5e-12 above the table value for N-1=805, and the
  881-884 candidates all sit near the 880 table value. That suggests these may be (N-1)-records with one more sphere
  added. This does not affect feasibility, but NOVELTY/CRITERION should check it against the queue/MJ bundle and the
  live table.
- Table freshness, queue rule and the category-unspecified Moki & Julio bundle were not checked here (outside REPRODUCE scope).

pass: true
