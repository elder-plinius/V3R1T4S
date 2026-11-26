# VNN-COMP 2026 challenging_certified_training_2026: a counterexample for cifar10_eps8_cnn7 idx 8072 sample 9, an instance no participating tool resolved

## What

The float32 input in object/cifar10_eps8_cnn7_idx8072_sample9.counterexample.txt (sha256 38855485249d98be61182cb41f1c3d370a4e3208e0cf8efb2796feabc7f3cc29) lies strictly inside every input bound of the unmodified live VNN-COMP 2026 challenging_certified_training_2026 version-2.0 instance given by inputs/onnx/cifar10_eps8_cnn7.onnx.gz (git blob f084be840473d8ebc88ccaaba50bbf1c57001c05) + inputs/vnnlib/cifar10_eps8_cnn7_idx8072_sample9.vnnlib.gz (git blob 6b2f50fefbd4871361c7d17e80477ec0cd24879e) and satisfies its output disjunct Y[0,3] <= Y[0,2] with margin 0.0029154419898986816 under onnxruntime 1.26.0 CPU float32 (0.0027802 to 0.0029127 under torch CPU/CUDA float32/float64 and an independent numpy float64 pass), the unmodified inputs/SCORING/counterexamples_v2.py returns correct at abs_tol 0.0, and the live results.txt (sha256 ec1b6fcbdef79539ffee17adbda2e99add137ba963a5306b87904035289eb26f, fetched 2026-10-24T21:02:15Z) shows no tool resolving it, with no counterexample file for it in the results tree at eea564f5.

Status (panel/gate.md): CONFIRMED_SOLUTION (three-skeptic panel, 3/3 pass). In plain words: the input in `object/` is a
CIFAR-10 input inside the property's box (an L-infinity ball of radius 8/255 in pixel units, written in the network's
normalised input coordinates) around the image of dataset index 8072 (property file comment; label 3, cat) on which the
certified-trained network `cifar10_eps8_cnn7` scores class 2 (bird) above class 3, so the robustness property of this VNN-COMP 2026
instance is violated; every one of the eight participating tools left this instance unresolved (results row:
`-, timeout, timeout, -, timeout, timeout, -, timeout`).

## Check it yourself

    sh verify-it-yourself/run_checks.sh          # VNN_PYTHON (or PYTHON)=<python with numpy and onnxruntime>; last line: PASS

It fetches the property file (34 kB) and the network file (65.2 MB) from the benchmarks repository on GitHub
(commit 303f2327) once, checks their pinned sha256, and checks the witness in exact rational arithmetic (bounds) and in
onnxruntime CPU float32 plus onnx.reference (outputs). Set `VNN_CACHE=<folder>` to reuse downloaded files. About a
minute on a laptop after the download. The official validator: `python3 verify-it-yourself/official_validate.py` (needs
`vnnlib==1.0.2` and `onnx`); expected `correct` at abs_tol 0 and 1e-4. Real output: verify-it-yourself/RECEIPTS.md.

## Compared to

| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| VNN-COMP 2026 SCORING/results.txt (results repo commit eea564f5) | `cifar10_eps8_cnn7-cifar10_eps8_cnn7_idx8072_sample9` (category 2026_challenging_certified_training_2026) | `-, timeout, timeout, -, timeout, timeout, -, timeout` (agate, alpha_beta_crown, n2v, neuralsat, nnv, pyrat, super_simple_vnn_comp, vibecheck): no tool resolved it, no tool counterexample file | https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_results/main/SCORING/results.txt | 2026-10-24T19:29:58Z; sha256 ec1b6fcbdef79539ffee17adbda2e99add137ba963a5306b87904035289eb26f (also the skeptics' fetches, panel/) |
| benchmark authors' own alpha-beta-CROWN run (kkaulen/vnncomp_challenging_certified_training, verification_results) | index 8072 of cifar10_eps8_cnn7 | timeout (1004.6 s) | https://github.com/kkaulen/vnncomp_challenging_certified_training | 2026-10-24 |

## Not claimed

- Only this one instance (the 2.0 property file named above) is resolved here; the 1.0 property file of the same row
  (used by five of the eight tools) is not claimed, nor is any other instance.
- No tool gave a wrong answer here: the tools timed out. This is not a soundness finding.
- The network file (cifar10_eps8_cnn7.onnx.gz, 65,214,983 bytes, sha256 172f2bb1f3cfebb70875c361a56ca3217a19d1463d241020bbb93fc705c3dd6d)
  is not in this package (over 1 MB); it is in the benchmarks repository at
  https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_benchmarks/303f2327a8e8411efc4457da03d2016ce42733cf/benchmarks/challenging_certified_training_2026/2.0/onnx/cifar10_eps8_cnn7.onnx.gz
- Not peer reviewed; checked by a three-skeptic panel (panel/) and by the standalone checker shipped here.

## Credits

- VNN-COMP 2026 organisers (results and benchmarks: https://github.com/VNN-COMP/vnncomp2026_results,
  https://github.com/VNN-COMP/vnncomp2026_benchmarks), authors of the official validator `SCORING/counterexamples_v2.py`
  used here unmodified. Latest report: K. Kaulen, T. Ladner, S. Bak, C. Brix, H. Duong, T. Flinkow, T. T. Johnson,
  L. Koller et al., The 6th International Verification of Neural Networks Competition (VNN-COMP 2025): Summary and
  Results, arXiv:2512.19007.
- The benchmark challenging_certified_training_2026: Konstantin Kaulen et al.,
  https://github.com/kkaulen/vnncomp_challenging_certified_training (source commit b4caf3d7).
- The participating tools whose results define "unsolved", as listed in results.txt for this category: agate,
  alpha_beta_crown, n2v, neuralsat, nnv, pyrat, super_simple_vnn_comp, vibecheck.
- Same run, same benchmark: packages 2026-10-24-estirner-775c93b9 and 2026-10-24-estirner-36afa0dd (cifar10_eps8_wide_cnn7
  idx 6249 sample 7 and idx 7490 sample 8). Open V3R1T4S PR #566 (contributor mizopl) showed this benchmark family was
  attackable; our attack was calibrated on its instance before it was trusted. Earlier V3R1T4S VNN-COMP results
  (known-knowns/vnncomp-2026-unsolved-instances/, including merged #146 by verexxi) set the package conventions.
- Software: onnx, onnxruntime, onnx2torch, PyTorch, NumPy and the vnnlib package.
