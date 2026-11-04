# PREREG — frozen 2026-11-04T16:40Z

Target: `square-grid-lattice-gas-exact-counts-oeis`, partial win p1 restricted to A054759: a(15).

## Ordering note, stated plainly

Exploratory work ran BEFORE this freeze: the row transfer matrix was implemented and validated against the
b-file for n = 1..8 (all match exactly), sparsity at n = 15 was measured (~431 nnz/row), and the live OEIS
fetch was done. No n > 8 value has been computed before this freeze. The two lens pipelines (isotypic row;
h-tracked) are specified below before any n > 8 output exists.

## Criterion (verbatim, from bank/targets.json)

Success means the exact integer value of the first unknown term a(N) of A028420, A006506 or A063443, where N
is one more than the largest index in the sequence's DATA and b-file re-fetched live immediately before
claiming, computed by two independent runs that agree exactly (different primes/CRT moduli sets AND a
different decomposition, e.g. row vs column sweep or a different state encoding, or one exact big-integer
run), with the same code reproducing every published term for n <= N-1 exactly, and the result consistent
with the known growth constant (a(N)^(1/N^2) within 1e-3 of the corresponding entropy constant).
This run claims the partial win p1 for A054759 with N = 15 (bank p1: "same two-run and reproduction rules").

## Statistic and checker (frozen)

Deterministic integer arithmetic. Checker = exact equality against the published table for n = 1..14 and
exact agreement of the two runs' CRT-reconstructed a(15). Growth check: |ln(a(15))/225 - ln((4/3)^(3/2))|
< 1e-3.

## Claim paths (declared before scoring)

| id | pipeline | outcome |
|---|---|---|
| R1 | lens 1: row-integrated transfer matrix (2^15 states), Z_15 isotypic blocks, primes P1 (12 distinct primes = 1 mod 15, each < 2^15), CRT | a(15) candidate |
| R2 | lens 2: h-tracked encoding (2^16 states, explicit wrap-edge bit), independent block construction, primes P2 (12 DISTINCT primes = 1 mod 15, P1 and P2 disjoint), CRT | must equal R1 exactly |
| L  | ladder: both codes reproduce a(1)..a(14); for n <= 13 both are cross-checked against a direct dense modular trace (no symmetry machinery) | gate for R1/R2 |

If R1 and R2 agree and the ladder passes: partial_win_claim (p1). If they disagree: the discrepancy is the
report; claim level stays at whatever the ladder supports.

## Thresholds

- CRT modulus product P = prod(P1) (resp. prod(P2)) must exceed 2^165 (~4.6e49), i.e. a rigorous upper bound
  on a(15) times a margin of at least 1e6. Rigorous bound used: a(15) <= ||T||_inf^15 where ||T||_inf is the
  exact max row sum of the integer transfer matrix; ||T||_inf is computed and recorded.
- Growth check tolerance 1e-3 (from the criterion verbatim).
- Every intermediate in the modular matmul must stay < 2^53 (float64 exactness); asserted in code.

## Null design

null_test: not needed because the claim is an explicit integer checked by deterministic exact arithmetic
against published table values (all 14 terms), with the two-run agreement and the growth-constant check as
the falsification tests; no chance-level statistic is involved.

## Baseline note (step 3c)

"An explicit object checked by a deterministic checker against a table value needs none of this" — the
published table a(1)..a(14) IS the baseline and is reproduced by both codes as part of the ladder (recorded
in attempts/*/output/ladder_*.json). No separate baseline/ folder is needed; if check_run.py disagrees, a
baseline/ folder will be added with the ladder outputs.

## Skeptic hook (bank verification_method)

A skeptic reruns either lens program with `--prime P` for any fresh prime P = 1 (mod 15), P < 2^31 not in P1
or P2, and checks Trace(T^15) mod P against the claimed a(15) mod P. Runtime ~1-2 min.
