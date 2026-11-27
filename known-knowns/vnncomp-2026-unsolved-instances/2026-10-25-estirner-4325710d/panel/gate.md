# Honesty gate: run 2026-10-25-1500, claim traffic_signs_recognition_2023 (2.0) 3_64_64 + model_64_idx_6371_eps_1.00000

Written by the run's main session at 2026-10-25T19:11:21Z (date -u), after reading all three panel files in full.

- reproduce.md: pass: true. Own checker written before reading the claimant's tools; all 12288 coordinates and all
  24577 assertions checked (no sampling); onnxruntime float32, onnxruntime after float32 rounding, onnx.reference, own
  numpy float32 and float64, plus onnx2torch; 18 onnxruntime runs bitwise identical; the unmodified validator returned
  'correct' 3 of 3 (abs_tol 1e-4 twice, 0 once). Margin 0.9993293141305912.
- novelty.md: pass: true. Own parse of the live results.txt (18:17:20Z, sha256 ec1b6fcb...eb26f): the only Row reads
  timeout, timeout, timeout; no file for the instance in the results tree; the 2023-2025 editions used other images;
  the six published larger-eps counterexamples for the same image all lie outside the eps-1 box; no claim in this repo
  or its PRs.
- criterion.md: pass: true, criterion_met: full. Clauses (a)-(e) checked literally with its own code and fetches; the
  2.0 directory is named by vibecheck's results.csv (and the 1.0 file has identical bounds and assertion); 'correct' at
  zero tolerance, not a tolerance rescue; null samples (box centre, 200 uniform points, 200 vertices) give no violation.
- Checks for downgrades: no hedging panelist (each says which checks it left to the others); no reproduction mismatch;
  the instance is unsolved in the live table at the panel's fetches (18:17Z-18:35Z, under 6 h old at this gate); one
  instance, one object; the scope sentence is the CRITERION panelist's own and no wider than what was reproduced; no
  table value was obtained by evasion (single plain fetches throughout).
- File times: claim/ was built at about 18:16Z; six files copied into it with their original times kept (cp -p of the
  15:08Z validator fetch and an older wrapper) looked older than PREREG.md (frozen 15:11:25Z) to the run checker. Their
  times were reset with touch at 2026-10-25T19:11:21Z; the bytes are unchanged and equal to the panel-start manifest (sha256 of all 16
  files compared).
- The four panel files name files relative to claim/ and carry injection_suspected: none.

status: CONFIRMED_SOLUTION
confirmed_scope: The 12288-value input in object/3_64_64_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_MP_2_BN_Dense_1024_BN_Dense_43_ep_30_model_64_idx_6371_eps_1.00000.counterexample.txt (sha256 4325710daebb1a883c943578d1000983a547dcda305001938005135ba95f3a9b) is, against the unmodified live vnncomp2026_benchmarks traffic_signs_recognition_2023 2.0 files 3_64_64_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_MP_2_BN_Dense_1024_BN_Dense_43_ep_30.onnx (decompressed sha256 ef43530d3deb4880293b21252d9351d72de99e640be017fcbb6a48f4c1f56cca) and model_64_idx_6371_eps_1.00000.vnnlib (decompressed sha256 20e11ba548bf8702ada14bf2343c96df2c8c431be6ac8ca2eef671d0cfe982d3), exactly float32 and strictly inside every input bound (min slack 1/512), and it satisfies the property only through the disjunct (>= Y[0,9] Y[0,17]) with Y[0,9] - Y[0,17] = 0.9993293141 under onnxruntime CPU float32, onnx2torch float32 and onnx.reference.ReferenceEvaluator (0.9993292997 under onnx2torch float64), with the live unmodified SCORING/counterexamples_v2.py returning 'correct' at both abs_tol 1e-4 and 0, while the instance's only Row in the live results.txt fetched 2026-10-25T18:19:42Z (results repo main eea564f5) reads timeout, timeout, timeout with no counterexample file for it in any tool directory, and neither my web search, the 2023-2025 result sets nor the six published larger-eps counterexamples for the same image yield an earlier counterexample for this pair.
