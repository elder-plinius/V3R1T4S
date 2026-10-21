# REPRODUCE skeptic verdict: N=884

context: subagent (fresh knowledgeWork context, given only this claim folder + kit/RULES.md), run 2026-10-16T16:07Z
verdict: PASS (REPRODUCE scope only: geometry of scu884_candidate.txt and its margin over radius.txt)

## Definition used (quoted from CRITERION_VERBATIM.md)
"r* := min( min_{i<j} |c_i - c_j| / 2, 1/2 - max_i max(|x_i|,|y_i|,|z_i|) ) for the cube [-1/2, 1/2]^3",
i.e. spheres of radius r with centres c_i inside the unit cube [-1/2,1/2]^3: no overlap iff |c_i-c_j| >= 2r for all
i<j, containment iff max|coord| <= 1/2 - r.

## Own checker (written before reading the folder's exact.py / scu_check.py; not derived from them)
- Strict parse: every non-empty line must be exactly 3 ASCII decimal tokens (regex), no exponents/NaN/inf; file is
  pure ASCII, no CR. Each coordinate -> exact Fraction -> integer over the common denominator 10^K.
- ALL n(n-1)/2 pairs, squared distances in exact integer arithmetic (no floats, no near-pair filter, no sampling).
- Pass test with no sqrt: D2_min >= 4 (t + 1e-11)^2 and (1/2 - max|coord|) >= t + 1e-11, exact rationals,
  t = row 884 of radius.txt. Overlap/containment re-tested exactly at the CLAIMED r* too. r* printed via mpmath 60 dp.
- Isometry: own parser for scu884.txt (index + x y z [+ r] rows); exact min squared distance of both sets compared,
  and when sizes match, sorted pairwise-distance multisets compared.

## Files checked
- scu884_candidate.txt sha256 4d82b0351f3f7c21f1326f9310055cf9ded17317e2a396c0a112f696abc3f430
- scu884.txt sha256 0ab133cbeb1c5c9b16aacef11f04ebac1971f12f3b7783d14ecde99a5fdf75cc
- radius.txt (identical across all claim folders)

## Own checker output (verbatim)
    file=claim/scu884_candidate.txt rows=884 bad_lines=0 N_expected=884 count_ok=True distinct=True
      minD2_exact=123849792851292553648607908934624704859/10000000000000000000000000000000000000000  closest_pair=(793, 794)
      r_pair=0.0556439109093017817617908896787 r_wall=0.05564391090930143058 r*=0.05564391090930143058
      claimed r*=0.05564391090930143058 matches(1e-19)=True  no_overlap@claimed=True contained@claimed=True
      table=0.055518673263 r*-table=0.000125237646301  pairs_ok@t+1e-11=True wall_ok@t+1e-11=True  BEATS=True
      posted claim/scu884.txt: rows=0 nonrow_lines=[(1, '1                    -0.351320595151                    -0.444481326737         '), (2, '2                    -0.036325178930                    -0.444481326737         '), (3, '3                     0.130159914959                    -0.444481326737         '), (4, '4                     0.287199314205                    -0.444481326737         '), (5, '5                     0.444481326737                    -0.444481326737         '), (6, '6                    -0.193662118512                    -0.444481325801         '), (7, '7                    -0.444481326737                    -0.380735675299         '), (8, '8                     0.046947344872                    -0.370962890252         ')]
      sizes differ (884 vs 0) -> not isometric

## Own isometry check (verbatim)
    cand n=884 posted coord rows=884 blank-index rows=0  cand minD2>posted minD2  (cand 0.0123849792851293 posted 0.012329292323383)
    sorted dist max diff=2.247e-02 ISOMETRIC=False

## Cross-check: folder's exact.py (run only after my own result; agrees, deterministic)
    scu884_candidate.txt n=884 r*=0.05564391090930143058 table=0.055518673263 diff=0.000125238 pass_1e-11=True

## Findings
1. Sphere count: 884 rows, exactly 3 decimal columns each, no bad lines, all centres distinct; matches N=884 in CLAIM.md. PASS.
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
