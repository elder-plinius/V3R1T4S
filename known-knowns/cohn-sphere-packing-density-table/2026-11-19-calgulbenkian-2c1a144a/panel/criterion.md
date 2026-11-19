context: Claude Code subagent, fresh context [Sonnet 5.5]

# CRITERION report, cohn-sphere-packing-density-table, claimed partial win p1

Word for word p1: "A new non-isometric packing matching the best known density in some dimension 10-31 (different kissing configuration), certified exactly."

## Clause checks
1. Packing in 10..31: yes. Dimension 19, 6 translates of a rank-19 lattice L_II (det Gram = 300), object/d19_nonisometric_periodic_packing_certificate.json.
2. Exactly matches the table density: yes. snapshot (the-record-we-beat/cohn_sphere_packing_snapshot.md) gives n=19 center density 3^(-9) 5^(-21/2) 13^(19/2), # = 6. I recomputed by hand: k=6, r^2 = 13/15 (min_sq 52/15), covol = sqrt(300); center_density^2 = 36 (13/15)^19 / 300 = 13^19 / (3^18 5^21) = 1461920290375446110677 / 184736485004425048828125. Equal, not greater (the package does not claim a full win; correct). I did not re-fetch Cohn's page (not my role); I used the package snapshot's value and the arXiv source (below).
3. Non-isometric proven by an isometry invariant: yes. The invariant is the sorted multiset of per-sphere kissing numbers of the whole periodic point set (contacts at squared distance 52/15, counted over all translate pairs): (4022,4022,4072,4072,4072,4072) versus (4110 x6) for the reference. A Euclidean isometry of point sets preserves this multiset, so it is a valid proof. A second invariant: with sym_trans_stab_size = 1 (no nonzero translate permutes the six classes mod the lattice; code checks all s), the translation group is exactly L, so norm-4 vector counts 6858 versus 6942 distinguish the lattices. Also the contact graph differs (connected 8/15 versus disconnected 6/15 pairs). "Different kissing configuration" is shown by the differing kissing numbers.
4. Reference is the published packing: the Chen-Hu-Li-Wang-Wu TeX source (fetched 2026-11-19T11:53:00Z, https://arxiv.org/e-print/2505.02394, HTTP 200, sha256 e114460c10a5770100eaafd647426bc5c7eb8e915aed9d2b3179cb36789a821e) gives dimension 19 as a 5x24 section matrix A, M = K^-1 (det 1/300), beta = 8/15, S = {0, v_1..v_5} from the rows of M's generator. The certificate's reference section rows match that A (e.g. first row has 4s at positions 4 and 8 in sqrt8 scaling, as the paper's 2 at positions 4 and 8 in 1/sqrt2 scaling). The paper does not state a second embedding; the new packing uses a Co_0-inequivalent saturated embedding of the same Gram K_19 (leech_sat = 1 by integer right inverse plus Smith normal form).
5. Exact certification, no floating point: yes. The Python verifier uses only fractions.Fraction, isqrt, json; Cholesky, enumeration bounds and ranks are rational. Grep finds no float/double/math.sqrt use; the C99 verifier uses int64 with no float types and builds with -mgeneral-regs-only. Fincke-Pohst is used as the main criterion requires: recursive Cholesky-based enumeration (fp_enumerate_fraction) over L with bound 4 (skip zero: min_sq 4, count 6858) and over each of the 15 translate-difference cosets with bound 52/15 (0 vectors strictly below, tight vectors counted). I checked the bound arithmetic (floor/ceil of isqrt(p q b^2)) and it is conservative-correct. Calibrated on E_8 (240, 1/16). Negative controls (perturbed translate, --corrupt) are rejected by both.

## Package checks in a copy (work-criterion/c)
sh verify-it-yourself/run_checks.sh: PASS (39 s). C99 and Python both print identical invariants for both packings, E_8 calibration passes, negative controls rejected. Note: both verifiers are by the same author; independence of implementation is a REPRODUCE matter, and I did not write a separate checker.

## Limits and hidden-quantifier hunt
- "New" holds only relative to the single published packing at this density (the paper's embedding). It is a second embedding of the paper's own section Gram and S-rule, so it is a variant of the same antipode construction, but it is not an isometric copy; p1 asks only for non-isometric with different kissing configuration, which is met.
- The 12166-contact stratum / Jacobian rank statements are extra and not needed for p1. They are bilateral only; the package says so itself (no jamming claim).
- Not a record: matches, not exceeds; p1 requires matching only.
- Novelty beyond the arXiv source (other repos, other lists) is not assessed here.

confirmed_scope: A 6-translate periodic packing in R^19 over a det-300 Leech cross-section lattice has exact minimal squared center distance 52/15 and exact center density equal to the table's 3^(-9) 5^(-21/2) 13^(19/2), and it is non-isometric to the Chen-Hu-Li-Wang-Wu antipode packing in that cell (per-sphere kissing multiset (4022,4022,4072,4072,4072,4072) versus six 4110s, and norm-4 counts 6858 versus 6942 with trivial translate stabilizer), all certified by exact rational Fincke-Pohst enumeration with no floating point.

pass: true
