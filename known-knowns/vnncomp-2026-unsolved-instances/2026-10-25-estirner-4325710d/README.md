# VNN-COMP 2026 traffic_signs_recognition_2023: a counterexample for the 64x64 network, image 6371, eps 1, an instance no participating tool resolved

## What

The 12288-value input in object/3_64_64_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_MP_2_BN_Dense_1024_BN_Dense_43_ep_30_model_64_idx_6371_eps_1.00000.counterexample.txt (sha256 4325710daebb1a883c943578d1000983a547dcda305001938005135ba95f3a9b) is, against the unmodified live vnncomp2026_benchmarks traffic_signs_recognition_2023 2.0 files 3_64_64_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_MP_2_BN_Dense_1024_BN_Dense_43_ep_30.onnx (decompressed sha256 ef43530d3deb4880293b21252d9351d72de99e640be017fcbb6a48f4c1f56cca) and model_64_idx_6371_eps_1.00000.vnnlib (decompressed sha256 20e11ba548bf8702ada14bf2343c96df2c8c431be6ac8ca2eef671d0cfe982d3), exactly float32 and strictly inside every input bound (min slack 1/512), and it satisfies the property only through the disjunct (>= Y[0,9] Y[0,17]) with Y[0,9] - Y[0,17] = 0.9993293141 under onnxruntime CPU float32, onnx2torch float32 and onnx.reference.ReferenceEvaluator (0.9993292997 under onnx2torch float64), with the live unmodified SCORING/counterexamples_v2.py returning 'correct' at both abs_tol 1e-4 and 0, while the instance's only Row in the live results.txt fetched 2026-10-25T18:19:42Z (results repo main eea564f5) reads timeout, timeout, timeout with no counterexample file for it in any tool directory, and neither my web search, the 2023-2025 result sets nor the six published larger-eps counterexamples for the same image yield an earlier counterexample for this pair.

Status (panel/gate.md): CONFIRMED_SOLUTION (three-skeptic panel, 3/3 pass). In plain words: the input in `object/` is a
64x64x3 input inside the property's box (each value within 1 unit, on the 0-255 pixel scale, of the benchmark's image
6371, clipped to [0, 255]; 9707 of the 12288 values are fractional, so it is not an 8-bit image) on which the binarized traffic-sign network `3_64_64_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_MP_2_BN_Dense_1024_BN_Dense_43_ep_30` gives class 9 the largest output instead of the
true class 17, so the robustness property of this VNN-COMP 2026 instance is violated. None of the three participating
tools (alpha-beta-CROWN, PyRAT, vibecheck) resolved this instance within the 480 s limit (results row: `timeout, timeout, timeout`).

## Check it yourself

    sh verify-it-yourself/run_checks.sh          # VNN_PYTHON (or PYTHON)=<python with numpy and onnxruntime>; last line: PASS

It fetches the property file (89 kB) and the network file (0.43 MB) from the benchmarks repository on GitHub (commit
303f2327) once, checks their pinned sha256, and checks the witness in exact rational arithmetic (bounds) and in
onnxruntime CPU float32 plus onnx.reference (outputs). Set `VNN_CACHE=<folder>` to reuse downloaded files. Seconds on a
laptop after the download. The official validator: `python3 verify-it-yourself/official_validate.py` (needs
`vnnlib==1.0.2` and `onnx`); expected `correct` at abs_tol 0 and 1e-4. Real output: verify-it-yourself/RECEIPTS.md.

## Compared to

| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| VNN-COMP 2026 SCORING/results.txt (results repo commit eea564f5) | `3_64_64_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_MP_2_BN_Dense_1024_BN_Dense_43_ep_30-model_64_idx_6371_eps_1.00000` (category 2026_traffic_signs_recognition_2023) | `timeout, timeout, timeout` (alpha_beta_crown, pyrat, vibecheck): no tool resolved it, no tool counterexample file | https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_results/main/SCORING/results.txt | 2026-10-25T15:07:01Z and 18:11:59Z; sha256 ec1b6fcbdef79539ffee17adbda2e99add137ba963a5306b87904035289eb26f (also the skeptics' fetches, panel/) |

## Not claimed

- Only this one instance (the 2.0 property file named above; the 1.0 file of the same row has the same bounds and
  assertion) is resolved here; no other instance of this benchmark is claimed. The eps 3, 5, 10 and 15 rows of the same
  image were already resolved by the tools.
- No tool gave a wrong answer here: the tools timed out. This is not a soundness finding.
- "Unsolved" means that no participating tool finished within the competition's 480 s limit for this instance.
- Not peer reviewed; checked by a three-skeptic panel (panel/) and by the standalone checker shipped here. This is a
  certified computational result (an explicit input checked by the official validator), not a proof of anything else.

## Credits

- VNN-COMP 2026 organisers (results and benchmarks: https://github.com/VNN-COMP/vnncomp2026_results,
  https://github.com/VNN-COMP/vnncomp2026_benchmarks), authors of the official validator `SCORING/counterexamples_v2.py`
  used here unmodified. Latest report: K. Kaulen, T. Ladner, S. Bak, C. Brix, H. Duong, T. Flinkow, T. T. Johnson,
  L. Koller et al., The 6th International Verification of Neural Networks Competition (VNN-COMP 2025): Summary and
  Results, arXiv:2512.19007.
- The benchmark traffic_signs_recognition_2023: Andreea Postovan and Mădălina Eraşcu, arXiv:2310.03033
  (https://github.com/apostovan21/vnncomp2023).
- The participating tools whose results define "unsolved": alpha-beta-CROWN, PyRAT, vibecheck.
- Method credits: the exact integer model and the strict-interior pixel map follow the earlier V3R1T4S package for the
  3_30_30 network (known-knowns/vnncomp-2026-unsolved-instances/how-we-built-it/); the target-propagation search follows
  Khalil, Gupta and Dilkina, Combinatorial Attacks on Binarized Neural Networks, ICLR 2019; the moment propagation follows
  Peters and Welling 2018 and Soudry et al. 2014. Merged V3R1T4S #146 (verexxi) attacked the same benchmark's 48x48 network.
- Software: PyTorch, onnx, onnxruntime, onnx2torch, NumPy and the vnnlib package.
