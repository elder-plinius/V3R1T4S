# Run It Yourself

## 1. Verify the Design from the Package Root

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:
```text
self_tests: PASS (positive Fano C(7,3,2)=7 and negative controls)
reassembled_bytes=4704754 sha256=e1080beca9b83194c0ebe19400b30ebc7bdc3dab17230e7bf153eddc625bc908
check_94_13_5: b=125184 distinct=125184 L=42705 C(94,5)=54891018 uncovered=0
comparison: 125184 < 129203 (Covering Repository) and 125184 < 129337 (LJCR)
PASS
```

## 2. Reassemble the Single File (Optional)

```sh
cat object/design_94_13_5_part*.txt > design_94_13_5.txt
shasum -a 256 design_94_13_5.txt
```
Expected SHA-256:
`e1080beca9b83194c0ebe19400b30ebc7bdc3dab17230e7bf153eddc625bc908`

## 3. Rebuild from Scratch

See `how-we-built-it/COMMANDS.md` for instructions using `how-we-built-it/build.py` (generalized combining construction from $v=47$ LJCR ingredients, giving `125,236` blocks) followed by `how-we-built-it/merge.c` (pair-merge reduction removing `52` block pairs whose uniquely covered 5-subsets span at most 13 points, yielding `125,184` blocks).
