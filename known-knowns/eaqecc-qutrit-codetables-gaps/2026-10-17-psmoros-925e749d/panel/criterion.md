saved by the main session from the subagent's returned text (CRITERION skeptic, model opus, returned 2026-10-17 about 19:00Z)
context: CRITERION skeptic, fresh subagent (Claude Agent tool), model opus, sees only claim/

# Criterion skeptic verdict: claim [[33,1,31;24]]_3 (target eaqecc-qutrit-codetables-gaps)

Scope of reading: claim/CLAIM.md, claim/REPRODUCE.md, claim/TABLE_RECORD.md, claim/verify/eacheck.py, claim/verify/parse_table.py, claim/object/S_33_1_31_24.txt, claim/data/qutrit.php.html. I read no other folder of the run. Scripts I wrote are in the skeptic's own work folder: work/indep.py, work/controls.py, work/soundness.py. I made one web request, listed under clause 2.

## Hashes
`shasum -a 256 object/S_33_1_31_24.txt data/qutrit.php.html` gives
- 925e749d364cd1e7c4f71101484aab051bd2dae5522ad57900fd022c11629edc (object, matches CLAIM.md)
- 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c (page, matches TABLE_RECORD.md)

## Clause by clause

**1. Explicit generator matrix over GF(3), symplectic form, 2n columns.** MET.
The object has 56 rows and 66 columns, and every entry is in {0,1,2}. Running work/indep.py prints `rows 56 cols 66 n 33 entries subset of {0,1,2}: True`. The layout is X part then Z part, as CLAIM.md states. The symplectic form is <u,v> = u_X.v_Z - u_Z.v_X. Weight counts position i when (x_i, z_i) != (0,0).

**2. A cell of the live table.** MET.
- I checked that (33,1,24) is a listed entry, not a c-value that falls between the listed ones. The raw HTML lists these entries for (n,k) = (33,1): `[[33,1,11-15;0]] [[33,1,24-32;1]] [[33,1,25-32;24]] [[33,1,26-32;25]] ... [[33,1,31-32;30]] [[33,1,32;31]] [[33,1,33;32]]`.
- So c = 24 is itself a listed entry, with d_lower = 25 and d_upper = 32. Its title is "lengthening of [[25,1,25;24]] increasing dimension of [[25,0,25;23]] from arXiv:2207.05647".
- The parser is complete. claim/verify/parse_table.py finds 3888 entries, and the raw page has exactly 3888 `class="EAQECC"` cells. The parsed row is `33 1 24 25 32 #ff9900 lengthening of [[25,1,25;24]] ...`.
- Live check: I made one honest GET with the run's code/vfetch.py, lens criterion-skeptic. It returned `status 200 fetched_at 2026-10-17T18:55:50Z sha256 37bbf731...c936c bytes 628039`. This is byte-identical to claim/data/qutrit.php.html. The page says "Last change: 10.07.2025".
- Before the request I checked the session stop list (empty) and every stop list changed in the last 24 h. None lists codetables, and nothing needed appending.

**3. s independent generators, c = rank(S J S^T)/2, k = n - s + c.** MET.
- work/indep.py prints `s(rank) 56 rank(SJS^T) 48 c 24 k 1`.
- s equals the row count, and I also confirmed this by hand. The 25 rows with a Z part have pairwise disjoint Z supports. Each of the 31 X-only rows has a private column. So rank = 56 (`Z-part supports pairwise disjoint: True`, `every X-only row has a private column: True`).
- Adding a dependent row leaves `s 56 c 24 k 1 d 31`, so s is computed as a rank, not as a row count.
- k = 33 - 56 + 24 = 1. I checked this in two more ways:
  - The extended stabilizer on 57 qudits is isotropic with rank 56, giving k = 1.
  - span(S)^perp, taken modulo its isotropic part, is spanned by two vectors with symplectic Gram matrix [[0,2],[1,0]]. That is nondegenerate, so there is a genuine logical X/Z pair.

**4. d computed exactly as min weight over span(S)^perp minus span(S) ∩ span(S)^perp, strictly greater than d_lower.** MET: d = 31 > 25.
- The claim's checker (`python3 -I verify/eacheck.py object/S_33_1_31_24.txt --expect 33,1,31,24`) prints `n 33 s 56 c 24 k 1 d 31`, then `PASS`.
- My checker, work/indep.py, was written from scratch. It finds dim span(S)^perp = 10 and dim of the isotropic part = 8 (= s - 2c). It enumerates all 59049 = 3^10 vectors, of which 6561 lie in the isotropic part.
  - Route A (the criterion's literal definition): `d = 31`. Weight distribution of the non-isotropic vectors: `{31: 17496, 32: 17496, 33: 17496}`.
  - Route B (operational definition): I built Bob's halves by symplectic Gram-Schmidt (24 pairs, 8 isotropic). An Alice-only error E⊗I_B lies in N(S') and also in span(S') for exactly the same 6561 vectors (`same set as route-A isotropic part: True`). Route B gives `d = 31`.
- Impure (degenerate) code: the code is degenerate. The isotropic part contains weight-2 vectors (`min weight of nonzero iso-part vectors: 2`), and the overall minimum nonzero weight of span(S)^perp is 2. The criterion's definition excludes the isotropic part explicitly. Route B shows that this matches the code's real error-correcting power: every Alice-only error of weight up to 30 that the stabilizer cannot detect lies in the extended stabilizer, so it does nothing to the encoded state. The definition is not stretched.
- The minimum is attained (weight-31 logicals exist), so the parameters are exactly [[33,1,31;24]]_3.

**5. d <= d_upper.** MET: 31 <= 32.
As a consistency check, I applied the d > (n+2)/2 entanglement-assisted Singleton-type bound from memory (Grassl-Huber-Winter): k <= (n-d+1)(c+2(d-1)-n)/(3(d-1)-n).
- d = 31 gives k <= 3·51/57 = 2.68, so k = 1 is allowed.
- d = 33 gives k <= 55/63 < 1, so it is forbidden, which agrees with the table's upper bound of 32.

**6. c >= 1, not c = 0.** MET: c = 24.

**7. Non-catalytic.** MET.
k = n - s + c is the standard entanglement-assisted stabilizer count, in which the c pairs are consumed and not returned. The page says it uses "c: number of required maximally entangled pairs ... (non-catalytic setting)". Its catalytic note covers only c >= k > 1 conversions, and here k = 1. No other convention is needed.

## Hidden quantifiers and subsumption
- **Does the table already imply d >= 31 here?** No. Every propagation rule the table lists (subcode, lengthening, puncturing, quantum shortening, increasing dimension, length reduction using teleportation, and more pairs never hurting) needs a source code with d >= 31 and c <= 24.
  - Across all 3888 entries, `awk '$4>=30 && $3<=25'` returns nothing: no entry anywhere has d_lower >= 30 with c <= 25.
  - At n = 33, no entry with c <= 24 has d_lower >= 26.
  - The (33,1) entries with c <= 24 have d_lower of at most 25 (11 at c=0, 24 at c=1, 25 at c=24).
  - The table first reaches d_lower = 31 for (33,1) at c = 30.
  - So the win is not subsumed.
- **Partial wins:** none is claimed. The full criterion is met, so a partial win is not needed.

## Null model (prereg said "none needed")
This holds. The claim is about one explicit finite object. d comes from exhaustive enumeration of all 3^10 vectors, so there is no sampling uncertainty that a statistical null could address. The real risk was a wrong checker or a wrong definition, so I tested the checker instead:
1. **Independent recomputation by two routes**, described in clause 4. It agrees with claim/verify/eacheck.py.
2. **Negative controls**, run with work/controls.py:
   - Moving row 1 onto a different single position gives d = 1.
   - Replacing row 56 by Z_33 gives d = 1.
   - Dropping the last row gives c = 23, k = 1, d = 1.
   - Changing one entry of row 56 gives c = 23, k = 0.
   - The checker catches every perturbation.
3. **Soundness test against the table**, with work/soundness.py: a 150 s random search over n = 2..6.
   - It hit 40 listed cells.
   - 0 cases exceeded the table's d_upper.
   - It reached d_lower in 22 cells, for example [[3,1,3;2]] and [[4,1,4;3]].
   - It never exceeded d_lower in these small, mostly tight cells.
   - So the definition and implementation follow the table's conventions and do not overcount.

## Minor notes (not blocking)
- The object's header comment ("replaces d=28 file") is not relevant to the criterion.
- REPRODUCE step 2 uses `grep -P`. This works on this machine.

confirmed_scope: The 56-row, 66-column GF(3) symplectic generator matrix object/S_33_1_31_24.txt (sha256 925e749d…629edc) defines a degenerate entanglement-assisted qutrit code with n = 33, s = 56 independent generators, c = 24, k = 1 and exact minimum distance d = 31 under the criterion's definition (exhaustive over all 3^10 vectors of span(S)^perp, excluding span(S) ∩ span(S)^perp), which is strictly greater than d_lower = 25 and at most d_upper = 32 of the cell [[33,1,25-32;24]]_3 of the live table eaqecc.codetables.de/qutrit.php (page "Last change: 10.07.2025", sha256 37bbf731…c936c, re-fetched 2026-10-17T18:55:50Z), and no table entry with c <= 25 has d_lower >= 30.

pass: true
