# Receipts: Standalone Game Verifier Output

Command run:
```bash
sh verify-it-yourself/run_checks.sh
```

Actual stdout:
```text
All first-principles game rules, calibration sequences, and new terms verified successfully.
PASS
```

Exit code: `0`
Execution time: ~0.1s
- 100% reproduction of OEIS A392305 calibration ($n=1..16$) and OEIS A391538 calibration ($n=1..14$).
- Exact match of conjectured formula $\lfloor n(n-1)/6 \rfloor + n$ for A391538 ($n=5..21$).
- Exact confirmation of new terms $A392305(17)=7, A392305(18)=7, A392305(19)=8, A392305(20)=8$.
