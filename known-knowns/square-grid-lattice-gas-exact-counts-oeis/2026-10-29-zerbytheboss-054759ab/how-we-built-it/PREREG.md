# Preregistered Evaluation Bar (`square-grid-lattice-gas-exact-counts-oeis`)

frozen_utc: 2026-10-29T15:08:00Z
target_id: square-grid-lattice-gas-exact-counts-oeis
category: physics
null_test: not needed because outputs are exact integers certified by multi-prime Chinese Remainder Theorem, two independent solvers across disjoint prime sets and sweeps, exact reproduction of all published terms for n <= N-1, and single-prime Freivalds audits.

## 1. Verbatim Target Bank Criteria
> Success means the exact integer value of the first unknown term a(N) of A028420, A006506 or A063443, where N is one more than the largest index in the sequence's DATA and b-file re-fetched live immediately before claiming, computed by two independent runs that agree exactly (different primes/CRT moduli sets AND a different decomposition, e.g. row vs column sweep or a different state encoding, or one exact big-integer run), with the same code reproducing every published term for n <= N-1 exactly, and the result consistent with the known growth constant (a(N)^(1/N^2) within 1e-3 of the corresponding entropy constant).

## 2. Partial Wins (Verbatim)
- **p1**: The next unknown term(s) of A054759 (square ice on the n x n torus) or A027683 (hard squares on the n x n torus), same two-run and reproduction rules; A054759 is expected to be easy (row transfer matrix with 2^n states plus one tracked boundary edge) and is a partial only.
- **p2**: A new row of an associated rectangular table (A210662 monomer-dimer m x n, A089980 hard squares m x n) extending the largest published m by one for all n up to the published range, same rules.

## 3. Preregistered Thresholds and Checkers
1. **Lens 1 (p1 - Square Ice on Torus A054759)**:
   - Reproduce exact published values for $n = 1..14$ ($a(1) = 4, a(2) = 18, \dots, a(14) = 15844635835975276495290739119895808472$).
   - Compute exact new terms $a(15)$ and $a(16)$.
   - Check consistency with Lieb's exact infinite-volume growth constant $W = (4/3)^{3/2} \approx 1.5396007178...$.
2. **Lens 2 (p2 - Rectangular Extensions A089980 & A210662)**:
   - Compute Row 28 of $A089980$ for widths $k = 1..20$, base $F_{30} = 832040$.
   - Compute Row 28 of $A210662$ for widths $k = 1..18$, base $F_{29} = 514229$.
3. **Monomer-Dimer Dual-Solver CRT Engine Calibration & Scaling**:
   - Verify dual compiled Rust solvers on calibration sizes ($N = 6, 10, 22$):
     - **Solver A**: Row-sweep broken-profile DP with in-place pair-stride kernel over 14 62-bit primes (Prime Set A).
     - **Solver B**: Column-sweep broken-profile DP over 14 disjoint 62-bit primes (Prime Set B).
   - Reconstruct integers via Gauss CRT over 14 primes (262 decimal digits capacity).
   - Exact parity verification: $\text{Result}_A == \text{Result}_B$ (100% digit-for-digit match).
   - Freivalds skeptic verification: Evaluate $a(N) \pmod{q}$ for independent 62-bit prime $q = 4611686018427386911$, asserting $X \equiv r_q \pmod q$.
   - Milestone claim restricted strictly to Partial Wins `p1` and `p2`. Full $N=28$ scaling verified ($2^{28}$ states, $4.29$ GB RAM, $5.6$h compute) with production execution in progress.
