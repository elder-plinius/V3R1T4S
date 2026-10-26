# The record we compared against

- table: VNN-COMP 2026 scoring table, https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_results/main/SCORING/results.txt
- fetched (UTC): 2026-10-24T15:07:03Z, 16:29:21Z and 18:18:36Z by the claimant (one plain curl each), HTTP 200, 7681226
  bytes, sha256 ec1b6fcbdef79539ffee17adbda2e99add137ba963a5306b87904035289eb26f every time (also the skeptics' fetches,
  panel/); results repo main = eea564f5d0a8751d8321a409214db14d03f452b8 (committed 2026-08-03T14:03:54Z).
- extracted cell (line 13098; tools in order agate, alpha_beta_crown, n2v, neuralsat, nnv, pyrat, super_simple_vnn_comp,
  vibecheck):
  `Row: ['cifar10_eps8_wide_cnn7-cifar10_eps8_wide_cnn7_idx7490_sample8', '-', 'timeout', 'timeout', 'timeout', 'timeout', 'timeout', '-', 'timeout']`
- the results tree at eea564f5 (27,250 entries, not truncated) has no file for this instance in any tool directory.
- instances.csv (2.0): `onnx/cifar10_eps8_wide_cnn7.onnx,vnnlib/cifar10_eps8_wide_cnn7/cifar10_eps8_wide_cnn7_idx7490_sample8.vnnlib,550`
  (timeout 550 s).
