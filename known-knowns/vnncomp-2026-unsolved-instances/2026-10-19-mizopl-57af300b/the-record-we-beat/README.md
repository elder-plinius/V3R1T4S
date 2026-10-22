# The Record We Beat (`vnncomp-2026-unsolved-instance-counterexample`)

## 1. Official VNN-COMP 2026 Scoring Log (`SCORING/results.txt`)
- **URL:** https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_results/main/SCORING/results.txt
- **UTC fetch timestamp:** `2026-10-19T10:58:51Z`
- **HTTP status:** `HTTP/2 200`
- **Full-file byte size:** `7,681,226` bytes
- **Full-file SHA-256:** `ec1b6fcbdef79539ffee17adbda2e99add137ba963a5306b87904035289eb26f`
- **Local excerpt:** `the-record-we-beat/results_challenging_certified_training_2026_excerpt.txt` (lines 12619–13625 of `SCORING/results.txt`, covering the entire `2026_challenging_certified_training_2026` category).
- **Instance 58 (`tinyimagenet_eps1_wide_cnn7-tinyimagenet_eps1_wide_cnn7_idx7687_sample8`):**
  ```text
  Row: ['tinyimagenet_eps1_wide_cnn7-tinyimagenet_eps1_wide_cnn7_idx7687_sample8', '-', '-', 'timeout', 'timeout', 'error', 'error', '-', '-']
  True Result: -
  58: agate score: 0, is_ver: False, is_fals: False, is_fastest: False
  58: alpha_beta_crown score: 0, is_ver: False, is_fals: False, is_fastest: False
  58: n2v score: 0, is_ver: False, is_fals: False, is_fastest: False
  58: neuralsat score: 0, is_ver: False, is_fals: False, is_fastest: False
  58: nnv score: 0, is_ver: False, is_fals: False, is_fastest: False
  58: pyrat score: 0, is_ver: False, is_fals: False, is_fastest: False
  58: super_simple_vnn_comp score: 0, is_ver: False, is_fals: False, is_fastest: False
  58: vibecheck score: 0, is_ver: False, is_fals: False, is_fastest: False
  ```

## 2. Benchmark Authors' Baseline Evaluation (`tinyimagenet_eps1_wide_cnn7.json`)
- **URL:** https://raw.githubusercontent.com/kkaulen/vnncomp_challenging_certified_training/main/verification_results/tinyimagenet_eps1_wide_cnn7.json
- **UTC fetch timestamp:** `2026-10-19T10:58:57Z`
- **HTTP status:** `HTTP/2 200`
- **Byte size:** `1,024,188` bytes
- **SHA-256:** `f73b774cceeff790a1cf9dfdacc2e009235d00615aa919d7cebbd97fa3a3dda8`
- **Entry `"7687"` (`sample 8`):** `{"result": "timeout", "method": "abCROWN", "running_time": 1001.6661100387573}`

## 3. Official VNN-LIB 1.0 and 2.0 Property Files Included Here
- `the-record-we-beat/tinyimagenet_eps1_wide_cnn7_idx7687_sample8.vnnlib.gz` (`149,155` bytes, `sha256: a0d735b14a2797b25abc8cf27e74450a791196ccce28dc31f1305847e30ad688`; uncompressed `1,195,158` bytes, `sha256: 1e626b4cb58eb1b691ce67e3d0932f8367719113461985b849f6b43030781b7b`)
- `the-record-we-beat/tinyimagenet_eps1_wide_cnn7_idx7687_sample8_v2.vnnlib.gz` (`120,566` bytes, `sha256: c4133f011d4d610af5916b6b95cb3120079eedc17e89d6f6174387e4d79d2567`; uncompressed `983,379` bytes, `sha256: a7a28ac63604a368c36f653968c217abb28a723d162fb0dd9e1399c42d415657`)
