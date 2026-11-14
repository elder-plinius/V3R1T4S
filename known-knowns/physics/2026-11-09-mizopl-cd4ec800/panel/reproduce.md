# Skeptic 1 — Reproducibility Audit (`reproduce.md`)

- `context`: `fresh independent skeptic review initialized from clean package directory`
- `target_id`: `magic-state-stabilizer-rank-exponents`
- `command_checked`: `sh verify-it-yourself/run_checks.sh`
- `corrupt_checked`: `python3 verify-it-yourself/verify.py --corrupt`

## Audit Findings

1. **Zero-Dependency First-Principles Execution**: `verify-it-yourself/verify.py` imports only Python 3 standard library modules and `numpy` (zero external dependencies on `stabrank` or `stabzoo`).
2. **Exact Constructive Verification (`W01..W10`)**: All 10 stabilizer decompositions (`60` QlAb stabilizer terms across `251` block-symmetry orbits) are evaluated on the full $2^m$ computational basis and verified in $\mathbb{Z}[i]$ and $\mathbb{Z}[i, \sqrt{3}]$ with `0` integer residual in `<0.2s`.
3. **Exact Lower-Bound & Obstruction Verification (`Certs #1..#4`)**: `verify.py` reconstructs all `1,080` 3-qubit stabilizer states $D_3$ across the `51` affine flats `[8, 28, 14, 1]` and `135` Pauli-Tableau fibers of `8` states each from `object/p2_p3_lower_bound_certificates.json`, verifies every state is a valid 3-qubit stabilizer state, and independently executes the $G_3$-reduced rank-4 exclusion for $|F\rangle^{\otimes 5,6}$ (`2,372` orbits -> `196` $u=01$ survivors -> `0` 5-qubit survivors) and $|T\rangle^{\otimes 5,6}$ (`2,406` orbits -> `30` $u=01$ survivors -> `0` 5-qubit survivors), the $|CS\rangle^{\otimes 3}$ even-qubit slice proof (`rank2_hits = 0`, `rank3_hits = 0`, explicit rank-4 witness `idx = [0, 7, 568, 624]`), and the $|H_3\rangle^{\otimes 4}$ untwisted 4-cycle closure proof across all `132` $g^2$-invariant flats in `~8.5s`.
4. **Adversarial Corruption Rejection**: Running `python3 verify-it-yourself/verify.py --corrupt` or perturbing any digit in `object/*.json` exits with status `1` and prints `FAIL`.

pass: true
