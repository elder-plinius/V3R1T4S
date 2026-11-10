# CRITERION skeptic verdict

context: subagent (Claude Code Agent tool, fresh context, given only claim/)

Scope of what I read: everything in claim/ (CLAIM.md, PROOF.md, REPRODUCE.md, MANIFEST.sha256, code/*, outputs/*,
result/bound.json, table/literature_record.md). Nothing else in the workspace was read.

## Criterion, clause by clause (literal reading)

Criterion (CLAIM.md, verbatim from the charter): "Prove a new rigorous lower bound ... on p_c^site(Z^2) ... strictly
better than the best published rigorous bound, with every finite computation in the proof done in exact or verified
interval arithmetic and released as a certificate a stranger can recheck." No partial wins are enumerated, so only
the full criterion counts.

### 1. "new rigorous lower bound": is PROOF.md a complete proof? Yes, as far as I can find.

- Lemma 0. The logic is right: if 1-p > p_c(S), then theta_S(1-p) > 0, so theta_L(p) > 0. So p >= p_c(L) >= p_c(S*),
  and Fisher's inequality p_c(S) >= 1 - p_c(S*) gives a contradiction. The inequality is the correct direction for a
  lower bound. It is in any case implied by the known equality p_c(S) + p_c(S*) = 1 for the square-lattice matching
  pair, so the attribution to Fisher is not load-bearing. I checked the map phi by hand. It is a bijection from
  Z^2 x {0,1} onto Z^2. It sends in-layer edges to diagonals, (v,0)-(v,1) to vertical steps from points with b-a
  even, and (min,1)-(max,0) to horizontal steps, and every horizontal edge of S* is hit. So L is isomorphic to a
  spanning subgraph of S*, and p_c(S*) <= p_c(L) holds. An eps-path gives an open L-path: when a site uses both of
  its vertices, both are open, so the vertical edge between them is usable. p_c is the theta-based critical value
  throughout.
- Lemma 1. Condition (ii) needs every history of positive probability. Q_h is a Strassen coupling on a finite
  poset. Domination is equivalent to dominating on all nontrivial up-sets of {0,1}^3 (18 of them) and of {0,1}^4
  (166 of them). Both counts are right: the Dedekind numbers are 20 and 168, minus the 2 trivial sets. The
  die-out/survive split is correct. The i.i.d. claim for zeta (the "hybrid field" paragraph) is terse but standard.
- Lemma 2 ("for every history" against what Section 4 checks). The history is a deterministic function of the eta
  values on tree edges together with eps(O) being open. b2 is an unprocessed leaf of T attached only through
  c-b2, and its future children carry no tree constraint. So the posterior of eps(b2) is exactly BP on T, through c.
  I tested this independently, without Lemma 2, messages or cones. I enumerated the actual growth process on Z^2
  exactly, branching lazily over eps, and grouped by history. Steps 1 to 4 used one total order and steps 1 to 3 a
  second. Every real history dominates. The worst exact real margins are 1.4701e-2 at step 1, which equals the
  root-step value in outputs/validate_output.txt, then 3.19e-3, 3.47e-3 and 9.09e-4. All are above the cone margin
  1.6585e-4, as the superset argument predicts.
- Is the superset a superset? D_0 and U_0 contain every real message whatever the subtree depth. That gives
  universal outer cones, and by induction D_k and U_k are also universal supersets. The message states are
  restricted to open states of the receiving vertex. This is valid, because every vertex that sends or receives a
  message as a parent has xi = 1 and so is open. The absent slot (ones), the eta = 0 leaf and the unprocessed
  eta = 1 child are all generated. Ignoring geometry only enlarges the set. The orientation conventions are right:
  A(par, child, "max") = adj(par, child), and the slots are (max,max,min), (max,min,min) and the root's
  (max,max,min,min).
- Is the root step covered? Yes. validate.py root_step checks all 166 up-sets of {0,1}^4 exactly; it is not a cone
  case. P(xi(O)=1) = 1-(1-p)^2 >= 1-p.
- Are steps with fewer children covered? Yes. The imaginary children use the same w, and marginals of a dominating
  law dominate. A selected vertex always has at least one child.
- Every case Lemma 1 needs maps to a checked case: b2 a max or min child of c, and c the root or with its parent on
  the min or max side.
- Multilinear and cone argument: correct. The margin is linear in each message with nonnegative coefficients, and
  the check divides by sw > 0 per generator tuple. This preserves the sign; no division by zero occurred.

### 2. "strictly better than the best published rigorous bound"

0.5567 > 0.556, and it is also above the exact optimum of the 1996 method, 0.5560829132 (code/vdbe1996.py,
reproduced). The wording matches the package's evidence: table/literature_record.md quotes the 1996 abstract, lists
two later papers that cite 0.556 as the best known, and records a 2025 paper with weaker bounds. I did no literature
search (no web access, and that is the NOVELTY skeptic's job). From my own background knowledge, I know of no
published rigorous lower bound above 0.556. Whether 0.556 is the best published bound therefore rests on the
package's record and the novelty review.

### 3. "every finite computation ... exact or verified interval arithmetic". Met.

- window.py: every quantity is a Python Fraction. In round_out, int(c * GRID) is applied to a nonnegative Fraction,
  which gives an exact floor. The remainder r >= 0 goes to each coordinate in turn, so the triangle contains the
  point and the result is a superset. hull() uses exact Fraction cross products. bisection uses Fraction p, and
  best_bound is not used by the claim anyway. cert.py decides PASS as `m > 0` on a Fraction. float() is used only
  for printing and for the *_float fields in the JSON.
- I wrapped hull() and round_out() with an exact containment audit. In all 40 calls at p = 4433/10000 and depths 0
  to 3, all 2188 input generators lie in the cone of the returned rays, every value is a Fraction, and the worst
  margins are unchanged.
- code/independent/indep.py is exact, with no rounding and a hull self-check. Its exact depth-3 margin is
  1.658527536e-4 > 0, slightly above window.py's rounded 1.658527535e-4, as outward rounding requires. Its only
  float path is the optional `brute1` mode, which plays no part in the claim.
- The root step in validate.py is exact (Fractions). My own exact enumeration reproduces it: 1.470118695e-2.

### 4. "released as a certificate a stranger can recheck". Met.

I copied claim/ into my work folder and ran every step of REPRODUCE.md with the standard library only (Python 3.14).
- The MANIFEST check is clean.
- cert.py ran in about 1.5 s and printed exactly the expected lines. The bound_check.json it wrote is byte-identical
  to result/bound.json.
- indep.py, vdbe1996.py (13 of 13 table rows), `window.py 0 ...`, validate.py and `window.py 3` each matched
  REPRODUCE.md line for line.

### 5. Null models

PREREG says none are needed, and I agree: the claim is a deterministic exact inequality, not a statistical
inference. The depth-0 control reproduces the 1996 paper exactly (0.5560829, all 13 table rows), which calibrates
the method. My real-process enumeration showed no history below the cone margin.

## Issues (none blocking)

- LOW: the root step, which the proof needs, is not part of cert.py or result/bound.json. It sits only in
  validate.py, which prints the margin but never asserts it is positive; validate.py also imports window.py for adj
  and UPSETS. The value is exact and positive, and I confirmed it independently.
- LOW: Lemma 1's argument that zeta is i.i.d. (the hybrid fields) is compressed. It is standard and I found no gap.
- LOW: CLAIM.md says the window is "enlarged to the whole exploration-tree history". Strictly, the whole history is
  handled by universal outer cones, with exact structure only to depth 3. It is sound, but the phrase is a little
  generous.
- INFO: indep.py is independent as code (directions instead of labels, no symmetry reduction, no rounding, a
  different hull algorithm), but it implements the same mathematical relaxation. It confirms the computation, not
  the reduction. My own review of Sections 0 to 3 covers the reduction.
- INFO: REPRODUCE.md mixes `python` and `$PY`; this is cosmetic.
- DEFERRED to NOVELTY: whether 0.556 is still the best published rigorous lower bound.

## Verdict

The result meets the full success criterion literally. The proof is complete modulo two cited classical theorems.
Every computation that decides the result is exact rational arithmetic. A stranger can recheck the certificate from
claim/ alone in seconds. The improvement over 0.556 is strict. It is a genuine full win and not one subsumed by the
1996 method, whose exact optimum is 0.55608. My pass is on the criterion; whether 0.556 is still the published record
is for the novelty review.

confirmed_scope: Assuming Fisher's inequality p_c(S) + p_c(S*) >= 1 and Strassen's coupling theorem, claim/ proves p_c^site(Z^2) >= 5567/10000 = 0.5567 by the van den Berg-Ermakov growth-process comparison, with the deciding computations (window.py's depth-2 and depth-3 cone checks at p = 4433/10000 and validate.py's root step) in exact rational arithmetic and recheckable from claim/ with the Python standard library; that this beats the best published rigorous lower bound rests on the package's literature record naming 0.556 as that bound.

pass: true
