# Verification Receipts (`2026-10-18-mizopl-dd85465d`)

## 1. Standalone Python Verifier (`verify-it-yourself/run_checks.sh`)

Command:
```bash
sh verify-it-yourself/run_checks.sh
```

Real command output:
```text
w12_k3_improved.gm sha256  : dd85465d87f23d688778ff35175ed19e4c9f00e71cad28b535d7a9d73294f302 (72 bytes)
published_w12_k3.gm sha256 : c592519b57ad8104860b7e1559b28c2d37ef329db82298b151a65e056ce27f1d (72 bytes)
k_extension_k16_w12.csv sha: 88c4f8fcd0ea6d4308f4e1fc716bb901ea78d3c6112b7e70d4af42bb631bf2fa (1644 bytes)
Improved order (8 uint64s) : [4, 7, 1, 0, 6, 5, 2, 3]
Published order (8 uint64s): [8, 2, 8, 8, 0, 4, 1, 3]

--- Exact Expected DNA Density (over all 4^15 = 1,073,741,824 DNA windows) ---
Published w12_k3.gm (bit-plane exact)        : 149082035 / 2^30 = 0.1388434647
Improved  w12_k3_improved.gm (bit-plane)     : 146639789 / 2^30 = 0.1365689458
Improved  w12_k3_improved.gm (4-ary DP)      : 146639789 / 2^30 = 0.1365689458

--- Comparison vs All Listed Methods at (w=12, k=3) ---
  angle-based         : 0.138389448  (our order improves by -1.3155%)
  GreedyMini          : 0.138843000  (our order improves by -1.6379%)
  decycling           : 0.150863000  (our order improves by -9.4749%)
  double decycling    : 0.150863000  (our order improves by -9.4749%)
  mod-minimizer       : 0.222468000  (our order improves by -38.6119%)
Smallest listed value   : 0.1383894480 (angle-based)
Published GreedyMini .gm: 0.1388434647 (-1.638189%)
Our exact DNA density   : 0.1365689458
Relative reduction vs smallest listed: -1.315492% (required >= 0.500000%)

VERIFICATION: PASS
PASS
```
