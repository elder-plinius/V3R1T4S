# Verification Receipts: `gf2-polymult-8term-25-products` (`p2`, `GF(2^7)` mod `x^7 + x^3 + 1`)

## SHA-256 Digest of Claimed Certificate
```text
36e8f04dbd4563949141fa5aa0b4179fcdb2a55a9742aeb517f69004a452053f  object/gf128_0x89_81gates.slp.txt
```

## Baseline Calibration Output (`verify-it-yourself/verify_gf2m.py`)
- `data/gf128-730-mult.slp` (`GF(2^7)` mod `0x89`, NIST/CMT baseline): `85` gates (`40 AND + 45 XOR`, gate depth `5`, `16,384` pairs checked -> `PASS`).

## Exact Output of `sh verify-it-yourself/run_checks.sh`
```text
{"and": 32, "and_depth": 1, "gate_depth": 6, "gates": 81, "m": 7, "pairs_checked": 16384, "poly": "0x89", "xnor": 0, "xor": 49}
PASS
```
