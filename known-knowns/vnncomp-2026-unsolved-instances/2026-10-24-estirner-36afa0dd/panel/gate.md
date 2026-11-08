# Honesty gate (run folder 2026-10-24-1817, main session)

status: CONFIRMED_SOLUTION
confirmed_scope: The 3072 float32 values in `object/cifar10_eps8_wide_cnn7_idx7490_sample8.counterexample.txt` lie strictly inside every input bound of `inputs/vnnlib/cifar10_eps8_wide_cnn7_idx7490_sample8.vnnlib.gz` (the live vnncomp2026_benchmarks 2.0 file, sha256 c64e879e…1a59), and on `inputs/onnx/cifar10_eps8_wide_cnn7.onnx.gz` (sha256 7e65aedd…f5f8, identical to the file served on 2026-10-24 at the public-share path that the benchmarks repo's setup.sh downloads) they satisfy the property's only output assertion through the disjunct `(<= Y[0,4] Y[0,6])` with margin 0.0004062354565 in onnxruntime CPU float32 (0.0004063546658 and 0.0004040482089 in torch float32/float64), the unmodified live `SCORING/counterexamples_v2.py` returns `correct` at zero tolerance, and the instance's row in the live results.txt (fetched 2026-10-24T18:20:46Z, sha256 ec1b6fcb…eb26f) has no `(h)` or `(v)` and the results repository holds no counterexample file for it.

Gate written 2026-10-24T19:02:01Z (date -u) after reading reproduce.md, novelty.md and criterion.md in full.

- target: vnncomp-2026-unsolved-instance-counterexample; one instance: challenging_certified_training_2026 (2.0)
  onnx/cifar10_eps8_wide_cnn7.onnx + vnnlib/cifar10_eps8_wide_cnn7/cifar10_eps8_wide_cnn7_idx7490_sample8.vnnlib; object
  claim/object/cifar10_eps8_wide_cnn7_idx7490_sample8.counterexample.txt (sha256 36afa0dd...96b4).
- REPRODUCE: pass: true. Own exact checker; 0 strict-bound violations under every reading (min slack 2.379464e-07,
  0.998 float32 ulps); onnxruntime margin 0.0004062354564666748, deterministic across processes and settings; onnx2torch
  f32 0.0004063546657562256, f64 0.0004040482088896735; its own numpy forward pass f64 and long double agree; onnx.reference
  0.00040721893310546875; unmodified official validator `correct` at abs_tol 1e-4 and 0 (box-centre negative control:
  spec_not_violated); network file byte-identical to the public share copy (full fetch 18:40:55-18:41:52Z). Its section
  5b was first written as pending and completed after its onnx.reference job ended; the verdict did not change.
- NOVELTY: pass: true. Live results.txt fetched 18:20:11Z (sha256 ec1b6fcb...eb26f); row 13098 has no (h)/(v); results
  tree eea564f5 has no file for the instance; the benchmark authors' abCROWN run timed out (1007.578 s); no repo result,
  PR or publication for this pair.
- CRITERION: pass: true, criterion_met: full. It fetched the share file in full itself (sha256 7e65aedd...f5f8, equal to
  the claim's), measured the margin's spread over 12 onnxruntime settings (at most 1.818e-06), and replayed two
  competition-accepted sibling witnesses on the network. The scope sentence is kept exactly as it wrote it.
- Downgrade checks: no hedging panelist; no reproduction mismatch (claimed 0.0004062354565 is the exact float32 margin
  rounded to 13 digits); the live table shows the instance unresolved by every tool; no stretched criterion or hidden
  quantifier found (1.0 property not claimed); the margin is small but 400x the 1e-6 floor and about 100x the largest
  measured cross-runtime spread; scope no wider than reproduced; no table value obtained by evasion; one object, one cell.
- Panel table fetches 18:20-18:41Z, less than 6 h before this gate. claim/ unchanged since the panel started.
- Relation to run folder 2026-10-24-1500: a different instance of the same benchmark (idx6249 s7 there); no bundling.
