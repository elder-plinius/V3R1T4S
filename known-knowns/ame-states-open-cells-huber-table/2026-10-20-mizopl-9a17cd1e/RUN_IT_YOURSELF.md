# Run It Yourself (`2026-10-20-mizopl-9a17cd1e`)

1. Ensure `python3` (`>= 3.9`) and `numpy` are installed.
2. From the root of this package directory, execute:
   ```sh
   sh verify-it-yourself/run_checks.sh
   ```
3. The script verifies in exact integer and finite-field ($\mathbb{F}_5$) arithmetic that:
   - `object/ame_9_10_certificate.json` satisfies all hypotheses of Theorem 1 across all $\binom{9}{4} = 126 / 126$ four-party cuts (`0` algebraic error);
   - `object/ame_11_10_certificate.json` satisfies all hypotheses of Theorem 1 across all $\binom{11}{5} = 462 / 462$ five-party cuts (`0` algebraic error);
   - `object/huber_wyderka_settled_blanks_audit.json` certifies all `22` settled blank cells and `2` impure `codetables.de` false positives;
   and prints `PASS` on the final line.
