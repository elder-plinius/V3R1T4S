# Null and Perturbation Control Audit (`fmm-ternary-integer-ring-upgrade`, `2026-10-22-mizopl-5ab48b6b`)

controls: 3
best_control: rejected (corrupted Brent tensor produces 4/64 equation mismatches; non-ternary coefficient max_abs=2 rejected by ZT check; unconjugated identity permutation produces max_abs=2 and fails ZT check across all 6 formats)
real: 29648196/29648196 exact integer Brent equations PASS with 0 mismatches across all 7 schemes (6 ZT schemes with max_abs=1 and 1 Z scheme with max_abs=2)
command: sh verify-it-yourself/run_checks.sh
real_beats_all_controls: yes

## Summary of Positive, Negative, and Unconjugated Baseline Controls

1. **Positive Self-Test Control (`Strassen (2,2,2)` in `verify-it-yourself/verify.py`):** Evaluates Strassen's rank-7 ternary `(2, 2, 2)` scheme in exact `int64` arithmetic across all `64/64` Brent equations (`mismatches = 0`, `max_abs = 1`, `zero_terms = 0`).
2. **Negative Control 1 (Corrupted Brent Tensor):** Flipping a single entry `W[0][0] = 0` in Strassen's `(2, 2, 2)` scheme is immediately caught and rejected (`mismatches = 4` out of `64`).
3. **Negative Control 2 (Non-Ternary Coefficient):** Setting a single coefficient `U[0][0] = 2` is immediately caught and rejected by the `ZT` ring check (`max_abs = 2 > 1`).
4. **Unconjugated `SerendipitousProductBuilder` Baseline Control:** Under the identity sub-block permutation $\pi = \text{id}$ used by Perminov's `SerendipitousProductBuilder`, every single one of the 6 formats (`6x12x14`, `9x10x13`, `9x10x16`, `10x15x16`, `11x15x16`, `12x13x16`) produces $\pm 2$ coefficient collisions (`max_abs = 2`, failing the `ZT` ring check on `12/15`, `15/16`, `8/16`, `4/18`, `4/16`, and `19/26` bud groups respectively), whereas our higher-order $S_{b \cdot g}$ sub-block conjugations align the zero supports of $s_3$ with the bud columns of $s_1 \otimes s_2$, eliminating all $\pm 2$ collisions (`max_abs = 1`, `0` non-ternary terms across all 6 `ZT` schemes).
5. **1-Minimality & Term-Deletion Control:** Deleting any single rank-1 multiplication term $q \in \{0, \dots, m-1\}$ in any of the 7 schemes immediately violates the exact integer Brent equations over $\mathbb{Z}$ (`0` zero terms, `0` duplicate triples).
