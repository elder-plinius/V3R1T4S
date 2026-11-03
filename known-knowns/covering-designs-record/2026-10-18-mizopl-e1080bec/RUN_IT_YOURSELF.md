# Run It Yourself

## 1. Verify the Design from the Package Root

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:
```text
self_tests: PASS (positive Fano C(7,3,2)=7 and negative controls)
parts_verified=5 reassembled_bytes=4704754 sha256=e1080beca9b83194c0ebe19400b30ebc7bdc3dab17230e7bf153eddc625bc908
check_94_13_5: b=125184 distinct=125184 L=42705 C(94,5)=54891018 uncovered=0
comparison: 125184 < 125236 (47+47 LJCR combining baseline, -52) < 129203 (CR 2026-10-18, -4019) < 129337 (LJCR 2026-10-18, -4153)
PASS
```

## 2. Reassemble the Single File (Optional)

```sh
cat object/design_94_13_5_part*.txt > design_94_13_5.txt
shasum -a 256 design_94_13_5.txt
```
Expected SHA-256 (`4,704,754` bytes, `125,184` lines):
`e1080beca9b83194c0ebe19400b30ebc7bdc3dab17230e7bf153eddc625bc908`

## 3. Rebuild from Scratch

See `how-we-built-it/COMMANDS.md` for self-contained instructions using `python3 how-we-built-it/build.py` (which verifies the six $v=47$ LJCR ingredient `sha256`s credited to Jan de Heer, Steve Muir, and Michael Dambmann and builds the `125,236`-block $47+47$ combining baseline `built/94-13-5.txt`, `sha256: 4ddf66cf9edf0cf96165e7514dbcd0cafb9c3dc67198326ea0586a63661ffcfb`) followed by `./merge 94 13 5 built/94-13-5.txt design_94_13_5.txt 60 200000` (pair-merge reduction removing `52` block pairs whose uniquely covered 5-subsets span at most 13 points, yielding `125,184` blocks, `sha256: e1080beca9b83194c0ebe19400b30ebc7bdc3dab17230e7bf153eddc625bc908`).
