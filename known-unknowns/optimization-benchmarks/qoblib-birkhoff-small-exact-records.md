# QOBLIB minimum Birkhoff decomposition: an exact decomposition of B5_25_2 with at most 13 terms or B6_36_10 with at most 18

🚚 **Optimization benchmarks** · harvest (many cells or partial wins within reach) · tractability ★★★★☆ · compute: laptop-hours to laptop-days for search; exact checking takes seconds; 5x5 and 6x6 integer matrices, respectively 120 and 720 possible permutation columns · open as of 2026-10-26

## The problem

QOBLIB's Minimum Birkhoff Decomposition problem (ZIB-AOPT/QOBLIB, 03-birkhoff) asks for the fewest permutation matrices in an exact convex decomposition of a doubly stochastic matrix (Kulkarni, Lee and Singh, IPCO 2017; Dufosse and Ucar, Linear Algebra Appl. 2016). On 2026-10-26 the auto-generated best-known table still lists B5_25_2 at 14 and B6_36_10 at 20, both from the 20260111_MIP_Schicker submission (Maximilian Schicker, 2026-01-10). However, András Czégel's RCS preprint (arXiv:2610.25837v1, 2026-10-19, Appendix D, Table 8) already reports lengths 14 and 19 for these instances. Its exact decompositions are public in QOBLIB PR #95 (opened 2026-10-20, still unmerged when checked), submission 20261020_RecoverCertifySearch_Czegel. The 19-term B6_36_10 decomposition reconstructs the matrix exactly with positive integer weights summing to 10000, so a record improvement needs at most 18 terms even while the generated table shows 20. Both matrices are integer matrices with row and column sums 10000 (scale 10000) in qbench_05_dense.json and qbench_06_dense.json. The current solutions/B5_25_2.bst.json and B6_36_10.bst.json files list 13 and 17 terms with floating-point weights, but neither support reconstructs its matrix exactly over the rationals (re-checked for this entry: the exact linear systems are inconsistent, residuals about 12 and 24 in the scaled entries), so they do not settle these cells.

## What counts as a win

For either named matrix A, give pairwise distinct permutations and strictly positive rational weights w_k summing to 10000 such that A=sum_k w_k P_k entrywise exactly, with at most 13 terms for B5_25_2 or at most 18 for B6_36_10. This is a record win; global minimality need not be proved. Alternatively, close either exact optimum by an attaining decomposition and an independently checkable lower-bound certificate valid for arbitrary nonnegative real weights. A certificate restricted to integer weights does not establish the latter claim.

## How a win is checked

Locate instances by their id, not JSON insertion order. Check integer matrix entries, common row/column sum 10000 and each submitted permutation of 1..n. Merge duplicate permutations and discard zero weights before counting. Clear rational denominators and check all 25 or 36 reconstruction equations and the weight sum with arbitrary-precision integers; tolerance must be zero. Use row-major storage, as confirmed against the exact MIP incumbents. For an optimality claim, a rational MILP branch proof over all n! support indicators and continuous weights can be checked node by node using Farkas/dual certificates. The small audit script checks fixed supports, not optimality, and is not a substitute for a general lower-bound proof.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/main/03-birkhoff/solutions/README.md>

## Sources

- <https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/main/03-birkhoff/README.md>
- <https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/main/03-birkhoff/solutions/README.md>
- <https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/main/03-birkhoff/instances/qbench_05_dense.json>
- <https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/main/03-birkhoff/instances/qbench_06_dense.json>
- <https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/main/03-birkhoff/submissions/20260111_MIP_Schicker/B5_25_2/README.md>
- <https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/main/03-birkhoff/submissions/20260111_MIP_Schicker/B6_36_10/README.md>
- <https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/main/03-birkhoff/submissions/20260111_MIP_Schicker/B5_25_2/B5_25_2_solution.json>
- <https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/main/03-birkhoff/submissions/20260111_MIP_Schicker/B6_36_10/B6_36_10_solution.json>
- <https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/main/03-birkhoff/solutions/B5_25_2.bst.json>
- <https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/main/03-birkhoff/solutions/B6_36_10.bst.json>
- <https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/main/03-birkhoff/check/README.md>
- <https://arxiv.org/abs/2610.25837v1>
- <https://github.com/ZIB-AOPT/QOBLIB/pull/95>
- <https://raw.githubusercontent.com/tg90000/qoblib-03-min-birkhoff/ced56a4384c17482b7dd40ff8dd0a349d68fd091/03-birkhoff/submissions/20261020_RecoverCertifySearch_Czegel/B5_25_2/B5_25_2_solution.json>
- <https://raw.githubusercontent.com/tg90000/qoblib-03-min-birkhoff/ced56a4384c17482b7dd40ff8dd0a349d68fd091/03-birkhoff/submissions/20261020_RecoverCertifySearch_Czegel/B6_36_10/B6_36_10_solution.json>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Start with a support-selection MILP over 120 or 720 permutations, then solve its weights exactly. Integer-only models are useful for finding witnesses but restrict the mathematical problem.
- Use the approximate 13/17-term supports only as search seeds. They cannot be made exact just by increasing numerical precision; their exact systems are inconsistent.
- Favor local support replacement and exact nullspace reductions. Keep all matrix equations, not only row and column totals.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- The instance description and checker use different storage-language conventions; these MIP witnesses reconstruct the target in row-major order.
- A smaller approximate support is not an exact decomposition.
- The Schicker submission's 'optimality bounds' (13 for B5_25_2, 11 for B6_36_10) come from an integer-weight model solved numerically by Gurobi; they bound integer decompositions, not decompositions with real weights.
- Exact rational weights, including any strict improvement, require zero reconstruction tolerance.
- Benchmark libraries are open targets: publish the exact decomposition in full.
- The auto-generated best-known table can lag public unmerged submissions. Czégel's RCS preprint and QOBLIB PR #95 already publish an exact 19-term B6_36_10 decomposition; reproducing it is not a record. Check preprints and open QOBLIB submissions as well as the table before claiming novelty.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/optimization-benchmarks/qoblib-birkhoff-small-exact-records.md
```

Already set up? Say `run V3R1T4S on qoblib-birkhoff-small-exact-records`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `qoblib-birkhoff-small-exact-records`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
