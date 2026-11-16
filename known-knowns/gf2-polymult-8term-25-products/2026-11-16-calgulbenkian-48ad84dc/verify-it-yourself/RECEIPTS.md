# Verification Receipts: `gf2-polymult-8term-25-products` (`p2`, `GF(2^7)` mod `x^7 + x^4 + 1`)

## SHA-256 Digest of Claimed Certificate
```text
48ad84dc1afddd567bcccf6574447aa229e3371548afa57f386fe2779897f100  object/gf128_0x91_82gates.slp.txt
```

## Baseline Calibration Output (`verify-it-yourself/verify_gf2m.py`)
- `data/gf128-740-mult.slp` (`GF(2^7)` mod `0x91`, NIST/CMT baseline): `84` gates (`40 AND + 44 XOR`, gate depth `5`, `16,384` pairs checked -> `PASS`).

## Exact Output of `sh verify-it-yourself/run_checks.sh`
```text
{"and": 34, "and_depth": 1, "gate_depth": 6, "gates": 82, "m": 7, "pairs_checked": 16384, "poly": "0x91", "xnor": 0, "xor": 48}
PASS
```
