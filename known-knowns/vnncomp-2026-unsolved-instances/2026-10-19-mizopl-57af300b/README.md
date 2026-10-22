# Certified VNN-COMP 2026 Counterexample for Unsolved Instance tinyimagenet_eps1_wide_cnn7_idx7687_sample8

## What

An explicit VNN-COMP 2026 counterexample claim/tinyimagenet_eps1_wide_cnn7_idx7687_sample8.counterexample (276,643 bytes, sha256 57af300bffe53135b65e7c2f2704e91079814ed2a68aad03d486e964f6c9a9da) and VNN-LIB 2.0 companion claim/tinyimagenet_eps1_wide_cnn7_idx7687_sample8_v2.counterexample (150,938 bytes, sha256 a34ed0220c3d97b9e18aee27b1e44614853877a3c95036bd2a1718326fd491e4) for the unsolved 2026_challenging_certified_training_2026 instance tinyimagenet_eps1_wide_cnn7_idx7687_sample8 (True Result '-' in SCORING/results.txt across all 8 participating tools), with all 12,288 coordinates strictly inside the float32 input box (minimum boundary clearance 1.66893005e-06 above 0), violating the VNN-LIB safety specification via Y_179 - Y_153 = +0.04230213 in onnxruntime CPU, +0.04230690 in onnx.reference.ReferenceEvaluator, +0.04228902 in PyTorch float32, and +0.04230902 in PyTorch float64 (all at least 1e-6), and returning 'correct' under the official VNN-COMP 2026 validators counterexamples.py and counterexamples_v2.py with abs_tol=0.0, rel_tol=0.0.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same files, with identical bytes, are in `object/` (headlined by `object/tinyimagenet_eps1_wide_cnn7_idx7687_sample8.counterexample`).

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` with `numpy` (and optionally `onnx`, `onnxruntime`, `vnnlib`, `cachier` if the 141 MB `tinyimagenet_eps1_wide_cnn7.onnx` model is present locally for live multi-runtime replay).
- **Rough laptop time**: about 3 to 15 seconds.
- **Expected last line**: `ALL CHECKS PASS`

## Compared to

| Source | Cell / Instance | Competition Status | Ours | URL | UTC fetch time |
|---|---|---|---|---|---|
| VNN-COMP 2026 (`SCORING/results.txt`) | `2026_challenging_certified_training_2026 / tinyimagenet_eps1_wide_cnn7_idx7687_sample8` | `True Result: -` (`0/8` tools verified or falsified) | Certified `sat` counterexample (`Y_179 - Y_153 = +0.04230213`, `'correct'` at `abs_tol=0.0, rel_tol=0.0`) | https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_results/main/SCORING/results.txt | 2026-10-19T10:58:51Z |
| Benchmark authors (`kkaulen/vnncomp_challenging_certified_training`) | `tinyimagenet_eps1_wide_cnn7.json` key `"7687"` | `timeout` (`1001.67s` in `abCROWN`) | Certified `sat` counterexample (`strict_interior = True`, `min_clear = 1.669e-06`) | https://raw.githubusercontent.com/kkaulen/vnncomp_challenging_certified_training/main/verification_results/tinyimagenet_eps1_wide_cnn7.json | 2026-10-19T10:58:57Z |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Only the unsolved instance `tinyimagenet_eps1_wide_cnn7_idx7687_sample8` in `2026_challenging_certified_training_2026` is resolved here (`sat`); other undecided instances in `2026_challenging_certified_training_2026` (some of which may be genuinely `unsat`) are not claimed.
- The 141 MB ONNX weight file `onnx/tinyimagenet_eps1_wide_cnn7.onnx` (`sha256: 7bc65dc63a7f8536ed80aa0755cdc1870d2041358190ec0e8cba544c3b5d00c6`) is hosted in the official `VNN-COMP/vnncomp2026_benchmarks` repository and is omitted from `object/` to obey the 1 MB per-file repository limit; `object/linear_region_certificate_idx7687_sample8.npz` (`625,910` bytes) ships the exact penultimate-layer (`512`-unit) and full-input (`12,288`-unit) affine functional for instant offline verification, while `verify-it-yourself/check_vnncomp_cex.py` automatically runs full live `onnxruntime` + `ReferenceEvaluator` + `counterexamples.py` + `counterexamples_v2.py` replay whenever `tinyimagenet_eps1_wide_cnn7.onnx` is present.
- Not peer reviewed. Checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **VNN-COMP 2026 Organizers** (**Christopher Brix** et al., `VNN-COMP/vnncomp2026_benchmarks` and `VNN-COMP/vnncomp2026_results`, https://github.com/VNN-COMP/vnncomp2026_results), authors of the official `SCORING/counterexamples.py`, `SCORING/counterexamples_v2.py`, and `SCORING/cex_checks.py` validators included in `verify-it-yourself/`.
- **Konstantin Kaulen** et al. (`kkaulen/vnncomp_challenging_certified_training`, https://github.com/kkaulen/vnncomp_challenging_certified_training), authors of the `challenging_certified_training_2026` benchmark suite.
- Contributor credit: `mizopl`.
