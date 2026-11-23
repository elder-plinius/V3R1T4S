context: Claude Code subagent, fresh context [Sonnet 5.5]

# REPRODUCE report, perfect-cuboid, partial win p1

[Edited 2026-11-19 when the package was assembled: this report reviewed the first version of the package; the ancillary rank and PARI material it mentions has since been removed, and the Lean proof file is byte-identical. One file name that no longer exists was replaced with a plain description. The checks and verdict are unchanged.]

## Verdict in one paragraph
The Lean file proves, with only the three standard axioms, that for all nonzero integers p, q with p^2 != q^2 the
"squared third edge" of each de Grey-Gibbs-Helm internal-ratio family is never an integer square (and so, by the
rescaling lemma, never a rational square). That is exactly the statement that no perfect cuboid lies in either family.
No elliptic-curve rank, Mordell-Weil or Selmer fact is used in the chain; the only arithmetic input is Fermat/Euler
descent on x^4+x^2y^2+y^4=z^2, which is proved inside the file (no axioms, no sorry). I re-derived the chain by hand and
checked it numerically with my own code. The rank/Selmer material (15a8 bridge, torsor obstructions, C99/Python/PARI
checks) is ancillary and not needed.

## 1. What the Lean file states and where the arithmetic enters
File: object/dgh_internal_edge_cuboids_proof.lean (1644 lines, `import`-free, `namespace PerfectCuboidDGH`).
- grep for sorry, admit, native_decide, decide, axiom, unsafe, macro, elab, implemented_by, extern, ofReduceBool,
  set_option: none (only the word "axioms" in a comment and in `#print axioms`).
- Main theorems: `dghInternalFamilyA_cSq_not_square`, `dghInternalFamilyB_cSq_not_square`
  (hp : p != 0, hq : q != 0, hpq : p^2 != q^2 gives cSq p q != K^2 for all integer K), via
  `no_dgh_unified_square` (a, e nonzero, a^2+e^2=g^2 gives dghUnified_cSq a e != K^2) via
  `dgh_quartic_to_euler_sum_sq` and `no_euler_quartic_pos` (Euler/Fermat descent, proved by strong induction on x*y
  in `no_coprime_euler_quartic`). All inside the file.
- `dghInternalFamilyA/B_no_scaled_perfect_cuboid` (Theorems C, D): conclusion is (lam*C)^2 != mu^2 * cSq for lam, mu > 0.
  The hypothesis `_hPC : IsPerfectCuboid A B C` is UNUSED (underscore), and the theorem does not mention A, B or
  e1, e2. It is the rational-rescaling corollary of the raw theorems. This is a presentational gap, not a
  mathematical one: since a perfect cuboid in the family would need its third edge c = sqrt(cSq) to be rational,
  "cSq is never a rational square" is exactly (and more than) what is needed. The statement a reader should cite is
  Theorems A/B, not C/D as worded.
- The families as defined in Lean were compared with the paper's Section 7.4 formulas (see 3): identical.
- Not used by the main chain: `dgh_quartic_to_15a8_bridge`, `edgh_15a8_phi_neg_obstruction`,
  `edgh_15a8_phi_torsor2_mod5`, `edgh_15a3_dual_torsors_mod16` (local-obstruction lemmas on the Cremona 15a curves;
  they are decoration for the "rank 0" narrative). The README's counts of "12 theorems" include them and the
  positive-edge-cuboid existence theorems.
- Rank-0 claims: not an input to the proof. They are only recomputed by the package's own C99/Python code.

## 2. Compilation (own run)
`lean +v4.35.0 object/dgh_internal_edge_cuboids_proof.lean` (elan toolchain leanprover--lean4---v4.35.0), copy of the
package, 14 s wall. No errors, no warnings, no `sorry` messages. `#print axioms` for all 12 names printed
`[propext, Classical.choice, Quot.sound]` and nothing else, including the main theorems
no_euler_quartic_pos, no_dgh_unified_square, dghInternalFamilyA_cSq_not_square, dghInternalFamilyB_cSq_not_square,
dghInternalFamilyA/B_no_scaled_perfect_cuboid. Result: PASS.

## 3. Hand re-derivation of the reduction (paper de Grey-Gibbs-Helm, arXiv:2401.06784 v1, Sections 7.4 and 10.2)
Fetch log: 2026-11-19T05:50:01Z, https://arxiv.org/pdf/2401.06784, HTTP 200, sha256
8498dd781d31d15d4ccbf06f4429fa41cd49ade051f954578bfc5b741fd123d4 (v1, 16 Jan 2024; Section 7.4 Theorem 5 and Section 10.2
match the claim's description).
- Step 1, Lean families A, B equal the paper's formulas (integer edge, perpendicular face diagonal, other integer
  edge 4pq(p^4-q^4)^2 resp. 8p^2q^2(p^2-q^2)(p^2+q^2)^2, third edge squared): VALID. Checked by reading and by
  reproducing the paper's worked examples with my own code: (p,q)=(2,1) gives edges 1443, 1800; (4,1) gives 552968,
  554880, as in the paper.
- Step 2, with a = p^2-q^2, e = 2pq (A) or a = 2pq, e = p^2-q^2 (B), both families equal
  e1 = a(a^4+a^2e^2+e^4), e2 = 2e a^2 (a^2+e^2), c^2 = e^2 (e^4 - a^2e^2 - a^4)(e^4 + 3a^2e^2 + 3a^4), with
  a^2+e^2 = g^2: VALID (my code checked equality of the integer triples for all |p|,|q| <= 30 and the Lean proves it
  symbolically).
- Step 3, with u = g^2, v = a^2: e^4 - a^2e^2 - a^4 = u^2 - 3uv + v^2 and e^4+3a^2e^2+3a^4 = u^2+uv+v^2, so
  c^2 = e^2 (u^2-3uv+v^2)(u^2+uv+v^2): VALID (hand expansion, and numeric check).
- Step 4, c^2 a rational square forces (u^2-3uv+v^2)(u^2+uv+v^2) a rational square, hence an integer square.
  Reduce to a primitive triple (divide by d = gcd(a,g); e divisible by d): VALID. For coprime u, v the two factors are
  coprime (gcd divides 4uv, coprime to uv, and u^2+uv+v^2 is odd), the product is nonnegative and not zero (the first
  factor has irrational roots), so the odd factor u^2+uv+v^2 = g^4+g^2a^2+a^4 is itself a square: VALID.
- Step 5, x^4 + x^2y^2 + y^4 = z^2 has no solution in positive integers (Euler; Fermat descent, also reproduced by
  Lean's no_euler_quartic_pos): VALID. Brute force x<=y<400: zero hits.
- Step 6, perfect cuboid in the family means e1, e2, c all rational multiples of an integer triple, so c^2 would be a
  rational square, contradicting step 5: VALID. Degenerate parameters are excluded (p=0, q=0, p^2=q^2 give zero
  or degenerate edges); the family is homogeneous in (p,q), so integer p,q suffice for rational parameters: VALID.
- Sanity on the identities themselves: for all nonzero integer (p,q), |p|,|q| <= 60, p^2 != q^2, both families satisfy
  all four required "is a square" conditions (e1^2+e2^2, e1^2+c^2, e2^2+c^2, e1^2+e2^2+c^2), c^2 is never a square
  (0 of 2 * about 14000 pairs), and c^2 > 0 occurs 12120 times (so the families are real edge cuboids, as claimed).
No GAP and no WRONG in the chain. One presentational GAP: Theorems C/D carry an unused perfect-cuboid hypothesis and
do not mention the edges (see 1).

## 4. Rank and descent claims
None are needed for the proof. PARI/GP was not installed and `pip install cypari2` failed in a fresh venv (no PARI
library available); I did not try a brew build. So I could not independently recompute the quoted ranks of
15a8 (y^2 = x(x^2-7x+16)) and of the dual and Euler-quartic Jacobians, or run the ancillary PARI script (removed from this package after this review). The package's own
run_checks.sh (run in a copy) printed PASS: C99 and Python verifiers, and all 12 axiom blocks inside the allowlist.
Those ancillary numbers are therefore only "package self-reported plus its own code", which do not matter because the main
theorem does not depend on them.

## 5. Own checker versus author's code
My checker (written from the paper's formulas before running anything of theirs) agrees with theirs on all points:
identities hold, c^2 never a square, Euler quartic no hits, witnesses (101,100) and (100,1) exist as stated
(the package's output reproduces them; I did not independently re-verify those two big integers beyond the identity
test on small range, which is the same polynomial code).

## 6. Pass assessment
The whole chain from "perfect cuboid in either DGH internal-ratio family" to contradiction is kernel-checked in Lean
with standard axioms only, and I re-derived each step independently. The criterion text for p1 wants "every
rank/descent computation rerunnable by the verifier in PARI or Magma"; here no rank computation is load-bearing,
and the only descent (Euler's quartic) is a Lean theorem. Remaining limits: PARI ancillary ranks not rerun by me;
novelty (whether this reduction to Euler's quartic is already published) and criterion scope are outside this role.

pass: true
