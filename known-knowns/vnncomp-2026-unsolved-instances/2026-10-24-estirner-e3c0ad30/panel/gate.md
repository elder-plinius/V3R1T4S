# Honesty gate (run folder 2026-10-24-1928, main session)

status: CONFIRMED_SOLUTION
confirmed_scope: The 3072 float32 values in object/cifar10_eps8_cnn7_idx4688_sample8.counterexample.txt (identical to the X block of object/cifar10_eps8_cnn7_idx4688_sample8_v2.counterexample) lie strictly inside every input bound of inputs/vnnlib/cifar10_eps8_cnn7_idx4688_sample8.vnnlib.gz and, run through inputs/onnx/cifar10_eps8_cnn7.onnx.gz (both blob-identical, same git SHA-1 blob id, to challenging_certified_training_2026/2.0 at vnncomp2026_benchmarks commit 303f2327), satisfy its output disjunct Y[0,7] <= Y[0,8] with margin 0.002304911613 under onnxruntime 1.26.0 CPU float32, 0.002014860511 under onnx2torch/torch CPU float32 and 0.002339150315 in float64, are rated `correct` at abs_tol 0 by the unmodified live SCORING/counterexamples_v2.py, and that instance's Row line in the live SCORING/results.txt (sha256 ec1b6fcbdef79539ffee17adbda2e99add137ba963a5306b87904035289eb26f) has no (h) or (v) in any of its 8 tool cells.

Gate written 2026-10-24T21:15:20Z (date -u) after reading reproduce.md, novelty.md and criterion.md in full.

- target: vnncomp-2026-unsolved-instance-counterexample; one instance: challenging_certified_training_2026 (2.0)
  onnx/cifar10_eps8_cnn7.onnx + vnnlib/cifar10_eps8_cnn7/cifar10_eps8_cnn7_idx4688_sample8.vnnlib (both files in the
  benchmarks git tree at commit 303f2327); object claim/object/cifar10_eps8_cnn7_idx4688_sample8.counterexample.txt
  (sha256 e3c0ad30...cb75).
- REPRODUCE: pass: true. Own exact checker; strict bounds as written and after float32 rounding; onnxruntime margin
  0.002304911613 (without graph optimizations 0.002274960279); onnx2torch f32 0.002014860511, f64 0.002339150315;
  onnx.reference f32 0.002346128225 and a float64 copy 0.002339150315; unmodified official validator `correct` at abs_tol
  1e-4 and 0 (a coordinate moved 1e-5 outside the box gives correct_up_to_tolerance / spec_not_violated, as it should).
- NOVELTY: pass: true. Live results.txt fetched 19:31:45Z (sha256 ec1b6fcb...eb26f); row has no (h)/(v); results tree
  eea564f5 has no file for the instance; the benchmark authors' abCROWN run timed out (1002.77 s); no publication, repo
  result, PR or issue for this pair.
- CRITERION: pass: true, criterion_met: full. Live results.txt fetched once, same sha256; all 11 results.csv give
  unknown/timeout/error for the row; margin spread over onnxruntime settings at most 4.989e-05, and the largest
  cross-runtime gap (ORT vs torch f32) 3.392e-04, so the smallest measured margin (0.002015) is about 5.9 times that
  gap and 2000 times the 1e-6 floor; box centre and 200 random/vertex points violate nothing. The scope sentence is kept
  exactly as it wrote it.
- The panel was interrupted by an API usage limit (about 19:35Z) and resumed at 21:00Z with the same agents and
  scratch folders; NOVELTY's three fetches before the cut were not repeated.
- Downgrade checks: no hedging panelist; no reproduction mismatch; the live table shows the instance unresolved by
  every tool; no stretched criterion (1.0 property not claimed); scope no wider than reproduced; no table value obtained
  by evasion; one object, one cell. claim/ unchanged since the panel started.
- Note on the panel instructions (no effect): the onnx.reference speed warning in panel_common.md referred to the wide
  network of the sibling claims; this network has 17,192,650 parameters.
- Re-read (2026-10-24T21:16:22Z): reproduce.md was finalised by its author at 21:15:27Z, 7 seconds after this gate was first written
  (21:15:20Z). I re-read the final file in full: verdict pass: true, and every number cited above is unchanged; this gate
  and its status stand. The package copies the final file.
