# Verification Receipts — `2026-10-25-mizopl-fc241396` (`polytof-toffoli-tcount-benchmark-tensors`)

## Command Executed
```sh
sh verify-it-yourself/run_checks.sh
```

## Real Output (`4.64 s` Single-Thread on 16 GB M1 MacBook Air)
```text
[PASS] 0732 (GF(2^9) Mult, n=27): table=147, posted=147 -> claimed=139 (standalone=True, polytof=True)
[PASS] 0733 (GF(2^10) Mult, n=30): table=173, posted=173 -> claimed=161 (standalone=True, polytof=True)
[PASS] 0105 (CSLA MUX_3 (01xx variant), n=21): table=39, posted=41 -> claimed=39 (standalone=True, polytof=True)
[PASS] 0108 (Ham15 (low) (01xx variant), n=42): table=73, posted=77 -> claimed=73 (standalone=True, polytof=True)
[PASS] 0115 (Mod Red_21 (01xx variant), n=28): table=51, posted=55 -> claimed=51 (standalone=True, polytof=True)
[PASS] 0817 (QCLA Com_7 (08xx variant), n=42): table=59, posted=63 -> claimed=59 (standalone=True, polytof=True)
[0732 GF(2^9) Mult, n=27] T-count: 147 -> 139 (-8) | Z_8 Path-Sum Exact: True | 2^20-State GF(2^9) Oracle Match: True (mismatches=0)
[0733 GF(2^10) Mult, n=30] T-count: 173 -> 161 (-12) | Z_8 Path-Sum Exact: True | 2^20-State GF(2^10) Oracle Match: True (mismatches=0)
[0105 CSLA MUX_3, n=21] T-count: 41 -> 39 (-2) | Z_8 Path-Sum Exact: True | Exhaustive 2^21=2097152 Statevector Match: True

All Requirement (c) circuit syntheses & equivalence checks PASSED in 2.88s -> object/circuit_synthesis_verification.json
[PASS] Requirement (c): Explicit {CNOT, T, S, Z, CZ} circuit synthesis & Z_8 path-sum + statevector equivalence verified for 0732 (n=27), 0733 (n=30), and 0105 (n=21).
[PASS] Partial Win p2: Certified optimality proofs verified for 7 benchmark families.
[PASS] Partial Win p3: Complete 88-tensor audit & 5 Waring rank discrepancies + 2 dimension discrepancies documented.
[PASS] Law M5 400-Sample Null Control: 0732 naive matches=0/400 (mean dist=630.06), 0733 naive matches=0/400 (mean dist=764.04).

=== ALL VERIFICATION CHECKS PASSED IN 4.64s -> object/CERTIFICATE.json ===
PASS
```
