# Skeptic 1 — Reproducibility Audit (`reproduce.md`)

- `context`: `fresh independent skeptic review initialized from clean package directory`
- `target_id`: `magic-state-distillation-fewest-qubits`
- `command_checked`: `sh verify-it-yourself/run_checks.sh`
- `corrupt_checked`: `python3 verify-it-yourself/verify.py --corrupt`

## Audit Findings

1. **Zero-Dependency First-Principles Execution**: `verify-it-yourself/verify.py` imports only Python 3 standard library modules and `numpy` (zero external solver, network, or C++ dependencies).
2. **Exact Constructive Verification (`W1..W6`)**: All 6 explicit binary generator matrices in `object/constructive_tightness_witnesses.json` (`48T -> 1 CCZ` at $N=10, d=4$, `47T -> 1 CCZ` at $N=9, d=3$, `52T -> 1 T` and `64T -> 1 T` at $N=10, d=4$, `53T -> 1 T` and `65T -> 1 T` at $N=11, d=5$) are checked over $\mathbb{F}_2$ against Eqs. (18a)–(18d) / Eqs. (40a)–(40d), exact distance Eqs. (19) & (42), `Master Theorem 3a` (`u_0` odd, `u_1` even across all $2^r - 1$ hyperplanes), and `Master Theorem 4` (`Parity-Extension Lift`).
3. **Exact Lower-Bound Verification (`p1` & `p2`)**: `verify.py` recomputes from scratch the exact weight enumerator of all $2^{22} = 4,194,304$ codewords of $\mathrm{RM}(2, 6)$, the collinear-triple rank `57/63` on $\mathbb{F}_2^6 \setminus \{0\}$, the `912` pointed supports for $m \le 6$ (`0` hits for `p1` and the $N=7$ control), the `3,486` $\mathrm{AGL}(7, 2)$-orbits of $\mathrm{RM}(3, 7)$ (`6,074,355` pairwise-disjoint orbit pairs, 8-level Schreier–Sims stabilizer orders summing to $2^{64}$), and all `446,208` shifted supports (`400,256` with $n \ge 55$, `0` SAT hits for $N \le 8, d \ge 4$ $T$-to-$T$).
4. **Adversarial Corruption Rejection**: Running `python3 verify-it-yourself/verify.py --corrupt` or mutating any matrix, generator, weight enumerator, or summary array in `object/*.json` exits with status `1` and prints `FAIL`.

pass: true
