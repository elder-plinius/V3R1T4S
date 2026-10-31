# Skeptic 1: Reproducibility & Independent Computation Audit

context: independent clean-room verification process started from package directory only

## Audit Summary

1. Executed `sh verify-it-yourself/run_checks.sh` from a clean temporary directory copy.
2. Verified that `check_dissections.py` uses only the Python 3 standard library and completes in ~2.5 seconds.
3. Confirmed that three genuinely distinct formulations are executed and compared:
   - Method 1: Bottom-to-Top 1-Bit Broken-Profile Vertex-Degree Continuity DP ($B = v_i \in \{0, 1\}$).
   - Method 2: Recursive Kronecker-Block Divide-and-Conquer on $(M_m, B_m)$ without profile sweep, plus full transpose symmetry verification $A116694(m, n) = A116694(n, m)$ across $0 \le m, n \le 15$.
   - Method 3: Vertical-Cut Open-Rectangle Fibonacci Transfer Matrix ($F(2m+1)$ states) verifying $0 \le m, n \le 6$.
4. Confirmed that all 13 entries of `b182275.txt`, all 210 entries of `b116694.txt`, and all 91 entries of `b333476.txt` are reproduced byte-for-byte (verified via SHA-256), and that mutating any digit in `object/a182275_dissections.json` causes `run_checks.sh` to exit with code 1 and output `FAIL`.

pass: true
