context: subagent
lens: CRITERION (partial win p2)

## What I did
- Read CLAIM.md, REDUCTION_prev.md, REDUCTION2.md, REPRODUCE.md and the GEK paper (arXiv:1008.2830, main text + appendix).
- Built a fresh venv, installed python-flint and numpy, and copied the claim folder to scratch.
- Ran `code/verify_final2.py 40` from scratch (about 35 s, exit 0). It recomputes the E2 table and re-certifies all 155 states and the scheme. Its printed lines match REPRODUCE.md and the stored `verify_final2.out` exactly:
  - "directly verified states: 155 closure-justified: 0"
  - rho_hat(0,5) >= 1.273839e-11
  - scheme2 (Q=40, k=30, u=0.01140): q=6, q_v=7, m_v=3, good/tet=96
  - rho_hat(0,Q) = 5.342361e-12
  - b >= 4.501141e-15
  - "CERTIFIED density <= 1 - 4.501141e-15"
  - ratio to GEK's deficit: 1.731e+10
- I did not run `rig2.py` or `scheme2.py` end to end. I re-executed only the verifier and the sanity checks below.

## Literal criterion check
- The criterion for p2 asks for a rigorous upper bound strictly below 1 - 2.6e-25. It must be machine-checked, or be a re-runnable interval-arithmetic computation that the skeptic re-executes, with a written reduction that matches it.
- Numerically 1 - 4.501e-15 < 1 - 2.6e-25, so the threshold is met. I found no hidden quantifier. The claim covers all packings of congruent regular tetrahedra.
- The Arb/python-flint computation was re-executed by me and reproduces. It is not machine-checked in a proof assistant. This is the second alternative of the wording, and it is satisfied.

## Reduction versus code (function by function)
- I read `rig_dp.py` (`E_up`, `a_lo`, `orderings`, `prefix_types`, `cert_lt1`, `cert_gt1`), `scheme2.py` (`gamma_lo`, `qmin`, `vertex_count`, `cert`) and `verify_final2.py`. They implement REDUCTION2 sections 1-2 and REDUCTION_prev sections 2.3 and 3 as written. The rounding is outward: lower ends for coverage and volume, upper ends for excess and the cube-root radii.
- Soundness details I confirmed:
  - `cert_gt1` only checks fully populated type sequences. Configurations with absent objects are covered by monotonicity of rho_hat under the GEK partial order. I checked `rho_cert2.json` (168 entries): rho_hat is monotone for every comparable pair, with 0 violations. This is not asserted in `verify_final2`, but it holds.
  - Lemma V2: I re-derived the edge-distance formula and the W\C / C\W slice formulas. A Monte-Carlo check (4e6 points, e = 0.05 to 0.85, wedge family from the proof) gave excess below the certified E2 at every e, within about 1.5% above it (for example 0.1097 vs 0.1112 at e = 0.3).
  - The wedge-area function a(r) is the exact minimiser from GEK's appendix proof (Gauss-Bonnet). I checked it by Monte Carlo over random wedges with edge distance r (r = 0.3, 0.6, 0.788, 0.9). The minimum matches a(r) to about 1e-4.
  - Lemma A: the convexity and vertex argument is correct.
  - Claim 2' (multiplicity q = 6): the chain from K5 to K2 is logically sound.
  - Claim 3' (vertex area count, q_v = 7): the logic is sound.
  - The boundary and limsup argument is correct, with O(L^2) boundary terms.
- Minor documentation gaps, none affecting the claimed number:
  - REDUCTION_prev refers to `scheme.py`, `verify_final.py`, `a_check.out` and `profile_dp.py`, which are not in the claim folder. REDUCTION2 supersedes the scheme section (it cites `scheme2.py`).
  - Lemma V is still used inside `E_up_combined` as min(V, V2). Its proof (|s2| <= e) is valid.

## Density definition and form of the bound
- The density is the limsup over cubes of vol(P ∩ C_L)/vol(C_L) for arbitrary, not just periodic, packings. REDUCTION_prev section 4 handles this by restricting to tetrahedra inside C_{L-1}. Bad and good centre counts are local, and the boundary error is O(L^2).
- The bound is stated correctly as density <= 1/(1+b) = 1 - b/(1+b). The code computes dl = down(b_lo/(1+b_lo)), not 1 - b. The printed "4.501141e-15" is `%.6e` of the rounded-down value, so any rounding is below 1e-21. This is irrelevant against the 2.6e-25 threshold.

## Conditionality ("rigorous")
- The result depends on GEK's published Lemma 3.3, Lemma 3.5 and the Lemma 4.2 construction. These are not re-proved here.
- The criterion's reference bound (GEK, Discrete Comput. Geom. 2011) rests on the same lemmas. Being conditional on them is therefore the same standing as the benchmark, and I accept it as "rigorous" under this wording.
- The result also depends on the new lemmas V, V2, A, R and Claims 1-3', whose proofs are written in the reductions. I read them and found no error, but they are not machine-checked. It also depends on Arb being correct.
- The GEK Lemma 3.3 statement is only a Taylor bound for a(r). The claim uses the exact a(r) from GEK's proof (it is exact in the appendix), not the statement.
- GEK's own appendix proofs of Lemma 3.3 (planar minimisation "an exercise in planar geometry") and Lemma 3.5 are terse. If they were wrong, both GEK's bound and this one would fail.
- Residual risk: the extension of the K3 construction to several simultaneous caps (REDUCTION_prev R1/R2) is a generalisation of GEK's step, not verbatim.

confirmed_scope: Conditional on GEK's published Lemma 3.3 (wedge-area minimiser a(r)), Lemma 3.5 (the 3/sqrt2 constant) and the Lemma 4.2 nested-ball construction, plus the newly written elementary lemmas in REDUCTION2.md/REDUCTION_prev.md (not machine-checked in a proof assistant), the re-executed Arb interval computation (verify_final2.py, 155 states + scheme, reproduced here) certifies that every packing of congruent regular tetrahedra has limsup density at most 1/(1+b) <= 1 - 4.501141e-15 with b >= 4.501141e-15, which is strictly below 1 - 2.6e-25.
pass: true
