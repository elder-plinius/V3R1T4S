# Verification Receipts — `polytof-toffoli-tcount-benchmark-tensors` (`p2`: Row `0725` / $\mathrm{GF}(2^2)$ mult)

## Command Executed
```bash
bash verify-it-yourself/run_checks.sh
```

## Raw Output
```text
=== [1/2] Checking SHA256SUMS ===
object/p2_0725_optimality_certificate.json: OK
...
=== [2/2] Recomputing 0725 (GF(2^2) mult) CP=3 and Waring=17 optimality certificate from scratch ===
PASS: 0725 (GF(2^2) mult, n=6) p2 optimality verified in 0.21s (CP=3: 0/1395 at R=1, 0/972315 at R=2, 120 triples at R=3; Waring=17: 0/4194304 at r<=16, 1008 schemes at r=17)
```

## Exit Code
`0`
