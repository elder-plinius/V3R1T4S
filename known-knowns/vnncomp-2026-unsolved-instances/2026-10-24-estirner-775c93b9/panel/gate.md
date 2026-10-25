# Honesty gate (run 2026-10-24-1500, main session)

status: CONFIRMED_SOLUTION
confirmed_scope: The 3072 float32 values in object/cifar10_eps8_wide_cnn7_idx6249_sample7.counterexample.txt (string-identical to the X block of object/cifar10_eps8_wide_cnn7_idx6249_sample7_v2.counterexample) lie strictly inside every input bound of inputs/vnnlib/cifar10_eps8_wide_cnn7_idx6249_sample7.vnnlib.gz (VNN-COMP 2026 challenging_certified_training_2026, version 2.0, an all-tool-unsolved row in the live results.txt fetched 2026-10-24T16:34:32Z) and, on the network inputs/onnx/cifar10_eps8_wide_cnn7.onnx.gz (identity with the benchmarks repo's setup.sh share file checked by exact size, an identical 31359037-byte prefix and a reproduced official sibling replay value, not by a full sha256 of the live share file), make every assertion true at zero tolerance through the single disjunct (<= Y[0,5] Y[0,2]) with margin 0.011762857437 under onnxruntime CPU float32 (0.011764973402 and 0.01176085948 under onnx2torch float32 and float64), and the unmodified live SCORING/counterexamples_v2.py returns correct at abs_tol 1e-4 and 0.

Gate written 2026-10-24T17:03:42Z (date -u) after reading reproduce.md, novelty.md and criterion.md in full.

- target: vnncomp-2026-unsolved-instance-counterexample; one instance: challenging_certified_training_2026 (2.0)
  onnx/cifar10_eps8_wide_cnn7.onnx + vnnlib/cifar10_eps8_wide_cnn7/cifar10_eps8_wide_cnn7_idx6249_sample7.vnnlib; object
  claim/object/cifar10_eps8_wide_cnn7_idx6249_sample7.counterexample.txt (sha256 775c93b9...baca).
- REPRODUCE: pass: true. Own exact checker; strict bounds (0 violations, min gap 2.37924438e-07); onnxruntime margin
  0.011762857437133789, deterministic across runs, threads and processes; onnx2torch f32 0.011764973402, f64
  0.0117608594799; onnx.reference 0.0117572247982; unmodified official validator `correct` at abs_tol 1e-4 and 0; full
  fetch of the network from the public share: 132594607 bytes, sha256 7e65aedd...f5f8 = the claim's file.
- NOVELTY: pass: true. Live results.txt fetched 16:34:09Z (sha256 ec1b6fcb...eb26f), the row has no (h)/(v); the results
  tree at eea564f5 has no file for the instance; no publication, repo result or PR for this pair (open PR #566 lists the
  instance only as an attack target in a script, with no witness or result).
- CRITERION: pass: true, criterion_met: full. Its one stated gap (its own fetch of the share file broke after
  31359037 bytes, so it confirmed the network by size, prefix and a reproduced sibling replay, not by a full hash) is
  closed by REPRODUCE's complete fetch with a matching sha256. The scope sentence is kept exactly as CRITERION wrote it.
- Downgrade checks: no hedging panelist; no reproduction mismatch (the claimed 0.01176285744 is the exact float32 margin
  rounded to 10 digits); the live table shows the instance unresolved by every tool; no stretched criterion or hidden
  quantifier found (the 1.0 property file is not claimed); scope no wider than what was reproduced; no sample presented
  as complete; no capped search used as an exclusion; no table value obtained by evasion (every fetch was one plain
  request; CRITERION did not retry its broken transfer); one object, one cell.
- Panel table fetches: 16:34-16:58Z, less than 6 h before this gate.
- claim/ was not changed after the panel started (its sha256 list at panel start equals the folder at the gate).
- Correction to the claim text (no effect on the result): CLAIM.md says version 2.0 is "named by act, agate, n2v and
  vibecheck's results.csv"; act is not in results.txt's participant list for this category (CRITERION); agate, n2v and
  vibecheck, all participants, name 2.0.
- Re-read (2026-10-24T21:16:56Z): reproduce.md was last written by its author at 17:04:04Z, 22 seconds after this gate was first written
  (17:03:42Z). I re-read the final file: verdict pass: true, and every number cited above (margins 0.011762857437133789,
  0.011764973402, 0.0117608594799, 0.0117572247982; min gap 2.37924438e-07; share-file sha256 7e65aedd...) is in it
  unchanged; this gate and its status stand. The package copies the final file.
