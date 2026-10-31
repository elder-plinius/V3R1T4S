context: subagent
lens: CRITERION (skeptic 2)

## What I did
- Built venv (python-flint 0.9.0, numpy, scipy) in my scratch folder; ran from claim/:
  - `code/verify_final.py 40 1000`: last line `CERTIFIED (Arb, modulo the Residual trust list) density <= 1 - 4.501166e-15` (45 states re-certified, scheme checks all True, q=6, q_v=7, m_v=3, good/tet=96, rho(0,40)>=5.342391e-12).
  - `code/k4_bb.py 1 1000`: `RESULT: PROVED (all boxes certified)` (28959 main + 228811 shell boxes, 0 unresolved). Negative control `k4_bb.py -1 100`: `RESULT: NOT PROVED` (as it must: 3/sqrt2 is tight).
  - `fullchain.py build 1000 40` and `fullchain.py scheme 1000 40`: regenerated rho_cert.json and scheme_best_40.json byte-identical to the stored copies; verify_final again gives the same final line.
- Hand-recomputed b = 96/6 * rho * (4pi/3) u^3 / v_t with u=0.0114, rho=5.3424e-12: 4.5016e-15 -> matches.

## Literal criterion check (p2)
- Bound strictly below 1 - 2.6e-25: yes, 1 - 4.501166e-15 is a far larger deficit.
- "Machine-checked OR re-runnable exact/interval computation re-executed by skeptic, with a written reduction that matches": the OR branch is met. I re-ran Arb chain + exact integer K4 branch-and-bound. REDUCTION_FULL.md maps function by function (section 12): a_lo = formula (3.1), E2_up_exact/E_up = section 5.2 cells, cert_lt1 = (R1), cert_gt1 = (R2) with orderings/prefix_types = type sequences sigma, gamma_lo/qmin = K2 radii, scheme_cert = Claims 1-3 (checks d>2r_v, R0<=sqrt(2/3)d, R''<sqrt(2/3), vertex_count = floor((1-Omega)/a(r_v/R'')), m_v, good=6k-4q_v m_v, b formula). No mismatch found.
- Statement form: code computes dl = down(b/(1+b)), i.e. density <= 1/(1+b) = 1 - b/(1+b), not the mis-simplified 1/(1+b)-as-1-b. The printed 4.501166e-15 is that dl (b/(1+b) = b - 2e-29; the 1 - 4.5011e-15 rounding in the Theorem is safe; strictly "1 - 4.501166e-15" is b/(1+b) rounded down by the code, fine).
- General (non-periodic) packings, limsup density: section 8 "Boundary / general packings" argues for arbitrary cubes x+[0,L]^3, sup over x, L->inf, with O(L^2) boundary terms uniform in the packing (shell count by volume/v_t). Meets the criterion's need. Theorem is stated for limsup_L sup_x.
- Hidden constants: K4' is proved only with eps=1/1000 (C=9018009/2000000); this is honestly stated (Residual trust item 5) and the scheme uses exactly kappa_p = (3/sqrt2)/(1.001) in scheme_cert, consistent. Not a problem for the claim, only a stated slack; 3/sqrt2 itself is tight (negative control).
- Lemmas used: K1 (closed form derived), K2, K3 (nested-ball replacement, with new Lemmas Z, N, assembly), V2 (replaces GEK 3.1, whose printed step is said to be false: edge_dist_counter), A, R, K4'(Step N + computer Step R + shell + far field + symmetry), K5, Claims 1-3, boundary. All have written proofs in the file. I spot-checked: K1 minimisation (two critical points), Lemma A convex vertex argument, V2 slice decomposition and monotonicity of the cell bounds, R1/R2 logic (min(delta,1) cube factor, type-class inclusion, ties), Claim 1-3 geometry (spacings, adjacent-edge distance s^2+t^2-st>=d^2, B(w,R'')subset B(c',sqrt(2/3)d)), far-field ratio 2.06<sqrt(4.509), T_d fundamental domain x>=y>=|z|. Found no error; the proofs are careful and self-consistent.
- No null-model/trivialization found: the 1 - 4.5e-15 gain is not from a trivial route; it comes from many centres per edge (k=30), which GEK's weaker counting did not exploit, and every ingredient is tied to proved lemmas.

## Residual trust (must appear in scope)
Software (Arb/python-flint 0.9.0, CPython ints, correctness of fullchain.py and k4_bb.py vs the text); hand-checked, not machine-checked paper proofs (K1, K3 incl. planar three-region fact, V2 identities, Lemma A, Lemma R logic, K4 Step N and box-test/shell/symmetry/far-field reductions, Claims 1-3, boundary count); STANDARD geometry facts used without proof (sphere area element, cap formulas, vertex solid angle 3*theta-pi, etc.); float-to-Arb handling. Not refereed, not formalised in a proof assistant. Sanity scripts (k1, k3, v2 etc.) are numerical only and not proof inputs; I did not re-run those.

## Not done
Did not re-run k3_check.py (8 min, numerical only), k1_check, v2_check, k4_num/relax. Novelty (subsumption by a better published bound) is another lens; a quick search found only the GEK paper and Wikipedia citing 1 - 2.6e-25.

confirmed_scope: Every packing of congruent regular tetrahedra in R^3 has limsup density at most 1 - 4.501166e-15 (strictly below 1 - 2.6e-25), by a Gravel-Elser-Kallus-style argument with all lemmas given written proofs in REDUCTION_FULL.md plus an Arb interval-arithmetic chain and an exact-integer K4' branch-and-bound (with eps=1/1000 slack) that I re-ran and that reproduced the stored outputs, resting on residual trust in the software and in human-checked, unrefereed paper proofs and standard-geometry facts (not machine-checked in a proof assistant).
pass: true
