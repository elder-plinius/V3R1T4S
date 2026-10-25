# VNN-COMP 2026 challenging_certified_training_2026: a counterexample for cifar10_eps8_wide_cnn7 idx 7490 sample 8, an instance no participating tool resolved

## What

The 3072 float32 values in `object/cifar10_eps8_wide_cnn7_idx7490_sample8.counterexample.txt` lie strictly inside every input bound of `inputs/vnnlib/cifar10_eps8_wide_cnn7_idx7490_sample8.vnnlib.gz` (the live vnncomp2026_benchmarks 2.0 file, sha256 c64e879e…1a59), and on `inputs/onnx/cifar10_eps8_wide_cnn7.onnx.gz` (sha256 7e65aedd…f5f8, identical to the file served on 2026-10-24 at the public-share path that the benchmarks repo's setup.sh downloads) they satisfy the property's only output assertion through the disjunct `(<= Y[0,4] Y[0,6])` with margin 0.0004062354565 in onnxruntime CPU float32 (0.0004063546658 and 0.0004040482089 in torch float32/float64), the unmodified live `SCORING/counterexamples_v2.py` returns `correct` at zero tolerance, and the instance's row in the live results.txt (fetched 2026-10-24T18:20:46Z, sha256 ec1b6fcb…eb26f) has no `(h)` or `(v)` and the results repository holds no counterexample file for it.

Status (panel/gate.md): CONFIRMED_SOLUTION (three-skeptic panel, 3/3 pass). In plain words: the input in `object/` is a
CIFAR-10 input inside the property's box (an L-infinity ball of radius 8/255 in pixel units, written in the network's
normalised input coordinates) around the image of dataset index 7490 (property file comment; label 4, deer) on which the certified-trained network `cifar10_eps8_wide_cnn7` scores class 6 (frog) above
class 4, so the robustness property of this VNN-COMP 2026 instance is violated; every one of the eight participating
tools left this instance unresolved (results row: `-, timeout, timeout, timeout, timeout, timeout, -, timeout`).

## Check it yourself

    sh verify-it-yourself/run_checks.sh          # VNN_PYTHON (or PYTHON)=<python with numpy and onnxruntime>; last line: PASS

It fetches the property file (33 kB, GitHub) and the network file (132.6 MB, the public share that the benchmarks
repository's setup.sh uses) once, checks their pinned sha256, and checks the witness in exact rational arithmetic
(bounds) and in onnxruntime CPU float32 plus onnx.reference (outputs). Set `VNN_CACHE=<folder>` to reuse downloaded
files. About 1-5 minutes on a laptop after the download. The official validator: `python3 verify-it-yourself/official_validate.py`
(needs `vnnlib==1.0.2` and `onnx`); expected `correct` at abs_tol 0 and 1e-4. Real output: verify-it-yourself/RECEIPTS.md.

## Compared to

| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| VNN-COMP 2026 SCORING/results.txt (results repo commit eea564f5) | `cifar10_eps8_wide_cnn7-cifar10_eps8_wide_cnn7_idx7490_sample8` (category 2026_challenging_certified_training_2026) | `-, timeout, timeout, timeout, timeout, timeout, -, timeout` (agate, alpha_beta_crown, n2v, neuralsat, nnv, pyrat, super_simple_vnn_comp, vibecheck): no tool resolved it, no tool counterexample file | https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_results/main/SCORING/results.txt | 2026-10-24T18:18:36Z (claimant), 18:20:11Z and 18:20:46Z (skeptics); sha256 ec1b6fcbdef79539ffee17adbda2e99add137ba963a5306b87904035289eb26f every time |
| benchmark authors' own alpha-beta-CROWN run (kkaulen/vnncomp_challenging_certified_training, verification_results) | index 7490 of cifar10_eps8_wide_cnn7 | timeout (1007.578 s) | https://github.com/kkaulen/vnncomp_challenging_certified_training | 2026-10-24 (panel/novelty.md) |

## Not claimed

- Only this one instance (the 2.0 property file named above) is resolved here; the 1.0 property file of the same row
  (used by five of the eight tools) is not claimed, nor is any other instance.
- No tool gave a wrong answer here: the tools timed out. This is not a soundness finding.
- The network file (cifar10_eps8_wide_cnn7.onnx.gz, 132,594,607 bytes, sha256
  7e65aeddfcace3cecb65f4c91dcf51723a862236537ae1afb1db3912f309f5f8; decompressed sha256
  e3940df279250819ea8f6776458429981c29ff1bdd719083cc5b4c1e9c3ff873) is not in this package (over 1 MB); it is the
  organisers' file at https://rwth-aachen.sciebo.de/public.php/dav/files/gEMDMstBiSHAAAS/challenging_certified_training_2026/2.0/onnx/cifar10_eps8_wide_cnn7.onnx.gz,
  the share that https://github.com/VNN-COMP/vnncomp2026_benchmarks/blob/303f2327a8e8411efc4457da03d2016ce42733cf/setup.sh downloads.
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
- The counterexample for the sibling instance idx 6249 sample 7 of the same network (package
  2026-10-24-estirner-775c93b9, same run) came first; this one was found by the same attack queue.
- Open V3R1T4S PR #566 (contributor mizopl), a counterexample on the sibling instance tinyimagenet_eps1_wide_cnn7 idx 7687
  sample 8, showed this benchmark family was attackable; our attack was calibrated on that instance before it was
  trusted. Earlier V3R1T4S VNN-COMP results (known-knowns/vnncomp-2026-unsolved-instances/, including merged #146 by
  verexxi) set the package conventions followed here.
- Software: onnx, onnxruntime, onnx2torch, PyTorch, NumPy and the vnnlib package.
