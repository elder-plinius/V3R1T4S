# How we found it (contributor text, unverified)

Target: bank entry square-grid-lattice-gas-exact-counts-oeis, partial win p1 restricted to A054759
(the bank's own "expected easy" target). Live OEIS re-fetch confirmed a(15) unknown (2026-11-04).

What worked:
- Row transfer matrix T over 2^15 states (state = vertical-edge bit column; T[s][s'] = the number of
  valid h-row completions of the ice rule). Validated against all 14 published terms before scaling.
- T commutes with cyclic bit-rotation, so Trace(T^15) = sum over the 15 Z_15 character (isotypic)
  blocks, each of dimension ~2182 instead of 32768. Block entries by pointwise extraction:
  T_k[O'][O] = sum_{x in O} T[canon(O')][x] * zeta^(k pos(x)) at a primitive 15th root mod p.
- Exact float64 modular linear algebra (every intermediate < 2^53, asserted in code), 14 primes
  1 (mod 15) chosen largest-first, CRT. Rigorous bound a(15) <= 2^15 * ||T||_inf^15 with the exact
  max row sum ||T||_inf = 1220 sizes the modulus set with a 2^40 margin.
- Two independent runs per the bank's rule: run-1 (row-integrated encoding, flip-set construction) and
  run-2 (h-tracked encoding, 2^16 states, independent walk-DFS construction, disjoint prime set).
  A column sweep was rejected as non-independent: the ice rule is 90-degree lattice-symmetric, so the
  column transfer element is the same function.

What failed on the way (kept in the run dossier):
- The sesquilinear b-basis extraction has no conjugation over F_p; the bilinear self-pairing vanishes
  for generic characters. The pointwise extraction replaced it (the validation ladder caught this
  at n >= 3).
- A scatter misalignment (sorted values vs unsorted positions) passed at n <= 4 and k = 0 only.
- Smallest-primes-first CRT sizing gave a modulus under the bound; largest-first fixed it.

Verification: both codes reproduce a(1)..a(14) exactly; fresh-prime residue check (29881) via both
programs; live OEIS re-fetches before claiming; three-skeptic panel (the first criterion lane failed
the literal growth clause - documented, repaired by a fresh criterion lane resolving the bank text's
inheritance question; see how-we-built-it/REPAIR.md and criterion_lane1_passfalse.md).
