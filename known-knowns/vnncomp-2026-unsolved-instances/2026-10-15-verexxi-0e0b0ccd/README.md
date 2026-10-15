# VNN-COMP 2026 traffic signs: a counterexample for an instance no tool solved

## What

All three tools in VNN-COMP 2026 timed out on the traffic_signs_recognition_2023 instance
`3_48_48_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_BN_Dense_256_BN_Dense_43_ep_30` +
`model_48_idx_6371_eps_3.00000`. This package contains an input inside that instance's allowed range on which the
network ranks class 9 above the true class 17. That settles the instance, and the competition's own validator rates
it `correct` at zero tolerance.

The exact scope, as signed off by the three reviewers:

> The 6912-value witness_plain.txt is, against the 2.0 copies of the traffic_signs_recognition_2023 ONNX and model_48_idx_6371_eps_3.00000 vnnlib in the claim folder (ONNX identical in 1.0), a strictly-in-bounds float32 input on which onnxruntime CPU float32 (and onnx ReferenceEvaluator) give Y[0,9]-Y[0,17] about 0.7616 and the package's SCORING/counterexamples_v2.py returns 'correct', for a row that is timeout/timeout/timeout in the results.txt fetched 2026-10-15, with no counterexample for it found by my web search; upstream byte-identity of the package files was not independently re-verified.

## Check it yourself

`sh verify-it-yourself/run_checks.sh` needs Python 3 with numpy and onnxruntime. It downloads the two benchmark files,
checks their sha256 and should end with `PASS`, in under a minute on a laptop.

To run the competition's own validator: `python3 verify-it-yourself/official_validate.py` (also needs onnx and
vnnlib==1.0.2). Expected result: `('correct', ... input_tolerance=0.0, output_tolerance=0.0)`. Sample output is in
verify-it-yourself/RECEIPTS.md.

## Compared to

The VNN-COMP 2026 scoring table
(https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_results/main/SCORING/results.txt), fetched
2026-10-15T00:58:03Z, lists this row as `timeout`, `timeout`, `timeout` for alpha-beta-CROWN, PyRAT and vibecheck.
Details: the-record-we-beat/README.md.

## Not claimed

- Anything about the other six unresolved 48x48 and 64x64 instances, other benchmarks, or the network's robustness
  in general.
- That the competition has accepted it: the table is unchanged and the organisers have not seen this yet.
- Results on every runtime. Several hidden-layer decisions sit within 1e-3 of their thresholds. The result holds in
  onnxruntime CPU float32 and onnx.reference and did not depend on float32 summation order in our tests, but
  non-IEEE or reduced-precision runtimes are outside the claim.

## Credits

- VNN-COMP 2026 organisers: benchmarks at https://github.com/VNN-COMP/vnncomp2026_benchmarks, results and validator
  at https://github.com/VNN-COMP/vnncomp2026_results.
- Benchmark and networks: Andreea Postovan and Madalina Erascu, "Architecturing Binarized Neural Networks for Traffic
  Sign Recognition" (https://arxiv.org/abs/2303.15005) and "Benchmarking Local Robustness of High-Accuracy Binary
  Neural Networks for Enhanced Traffic Sign Recognition" (https://arxiv.org/abs/2310.03033).
- Tools compared against: alpha-beta-CROWN, PyRAT and vibecheck.
- Pixel map and folder layout: the earlier V3R1T4S result in known-knowns/vnncomp-2026-unsolved-instances/.
- Software: ONNX, onnxruntime, NumPy, JAX and Google OR-Tools. The search and the three independent reviews were run
  with Claude (Anthropic).
- Found by verexxi.
