# Honesty gate (run folder 2026-10-24-1929, main session)

status: CONFIRMED_SOLUTION
confirmed_scope: The float32 input in object/cifar10_eps8_cnn7_idx8072_sample9.counterexample.txt (sha256 38855485249d98be61182cb41f1c3d370a4e3208e0cf8efb2796feabc7f3cc29) lies strictly inside every input bound of the unmodified live VNN-COMP 2026 challenging_certified_training_2026 version-2.0 instance given by inputs/onnx/cifar10_eps8_cnn7.onnx.gz (git blob f084be840473d8ebc88ccaaba50bbf1c57001c05) + inputs/vnnlib/cifar10_eps8_cnn7_idx8072_sample9.vnnlib.gz (git blob 6b2f50fefbd4871361c7d17e80477ec0cd24879e) and satisfies its output disjunct Y[0,3] <= Y[0,2] with margin 0.0029154419898986816 under onnxruntime 1.26.0 CPU float32 (0.0027802 to 0.0029127 under torch CPU/CUDA float32/float64 and an independent numpy float64 pass), the unmodified inputs/SCORING/counterexamples_v2.py returns correct at abs_tol 0.0, and the live results.txt (sha256 ec1b6fcbdef79539ffee17adbda2e99add137ba963a5306b87904035289eb26f, fetched 2026-10-24T21:02:15Z) shows no tool resolving it, with no counterexample file for it in the results tree at eea564f5.

Gate written 2026-10-24T21:14:08Z (date -u) after reading reproduce.md, novelty.md and criterion.md in full.

- target: vnncomp-2026-unsolved-instance-counterexample; one instance: challenging_certified_training_2026 (2.0)
  onnx/cifar10_eps8_cnn7.onnx + vnnlib/cifar10_eps8_cnn7/cifar10_eps8_cnn7_idx8072_sample9.vnnlib (both files in the
  benchmarks git tree at commit 303f2327); object claim/object/cifar10_eps8_cnn7_idx8072_sample9.counterexample.txt
  (sha256 38855485...cc29).
- REPRODUCE: pass: true. Own exact checker; strict bounds as written and after float32 rounding (closest 2.379e-7
  inside); onnxruntime margin 48913/2^24 = 0.0029154419898986816, bitwise deterministic across repeats, sessions, thread
  counts and processes; onnx2torch f32 0.00278023, f64 0.00291268; onnx.reference f32 0.00290838, f64 0.00291268; own numpy
  forward pass agrees; unmodified official validator `correct` at abs_tol 1e-4 and 0; all files equal the live GitHub
  copies (git blobs f084be84..., 6b2f50fe...).
- NOVELTY: pass: true. Live results.txt fetched 21:01:24Z (sha256 ec1b6fcb...eb26f); row has no (h)/(v); results tree
  eea564f5 has no file for the instance; the benchmark authors' abCROWN run timed out (1004.6 s); no publication or repo
  result (open PR #566 lists this instance only as an attack target in a script, with no witness or result).
- CRITERION: pass: true, criterion_met: full. Live results.txt fetched 21:02:15Z, same sha256; margin spread over
  onnxruntime option sets at most 6.06e-05 against a margin of 0.0029; the box centre is classified as the true label
  and 0 of 200 random box points satisfy any disjunct. The scope sentence is kept exactly as it wrote it.
- The panel was interrupted by an API usage limit (about 19:35Z) and resumed at 21:00Z with the same agents and
  scratch folders; NOVELTY made no fetch before the cut; nothing was re-fetched.
- Downgrade checks: no hedging panelist; no reproduction mismatch; the live table shows the instance unresolved by
  every tool; no stretched criterion found (1.0 property not claimed); scope no wider than reproduced; no table value
  obtained by evasion (NOVELTY recorded one non-required page that redirected to a sign-in page as blocked, not
  retried); one object, one cell. Panel table fetches 21:01-21:02Z. claim/ unchanged since the panel started.
- Note on the panel instructions (no effect): panel_common.md warned that onnx.reference is slow on a 33M-parameter
  network; that applied to the wide network of the sibling claims; this network has 17,192,650 parameters.
