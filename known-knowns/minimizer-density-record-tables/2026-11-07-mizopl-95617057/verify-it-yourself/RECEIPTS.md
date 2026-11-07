# Verification Receipts (`2026-11-07-mizopl-95617057`)

## 1. Standalone Python Verifier (`verify-it-yourself/run_checks.sh`)

Command:
```bash
sh verify-it-yourself/run_checks.sh
```

Real command output:
```text
object/w12_k4_4ary.gm  sha256 : 956170573df55e04f43e55c20d6bba0b134c9b8054a92f995428dc9df4410ddb (2056 bytes)
object/w12_k4_4ary.csv sha256 : 72557c44cc3c4b10d4735faeee9d6745f40872674c54118a311e258f775431d1 (4518 bytes)
OrensteinLab/Minimizers k4-w12.txt sha256 : 9a8f7447e569399a594588e695a963da59078b34cf4aac23a6fd3d998d06d877 (58 bytes)
OrensteinLab/10-minimizers w12_k4.gm sha256: 7c04487e1489e8d37302230424f32522f3c9af537680c6319009fb49ef180131 (136 bytes)

--- Exact Expected DNA Density (over all 4^16 = 4,294,967,296 DNA windows) ---
OrensteinLab/10-minimizers w12_k4.gm          : 584312429 / 2^32 = 0.1360458389
OrensteinLab/Minimizers    k4-w12.txt         : 574313157 / 2^32 = 0.1337177020
Claimed 4-ary DNA order    w12_k4_4ary (DP 1) : 570244411 / 2^32 = 0.1327703733 (pref=283110423, suff=287133988)
Claimed 4-ary DNA order    w12_k4_4ary (DP 2) : 570244411 / 2^32 = 0.1327703733
k_extension_k16_w12.csv sha256               : 88c4f8fcd0ea6d4308f4e1fc716bb901ea78d3c6112b7e70d4af42bb631bf2fa (1644 bytes)

--- Comparison vs All Listed Methods at (w=12, k=4) ---
  Minimizers (k4-w12) : 0.1337177020  (our order improves by -0.7085%)
  GreedyMini          : 0.136046000   (our order improves by -2.4077%)
  angle-based         : 0.138322748   (our order improves by -4.0141%)
  decycling           : 0.143956000   (our order improves by -7.7702%)
  double decycling    : 0.145236000   (our order improves by -8.5830%)
  miniception         : 0.156164000   (our order improves by -14.9802%)
  mod-minimizer       : 0.156164000   (our order improves by -14.9802%)
  open-close-syncmer  : 0.156164000   (our order improves by -14.9802%)

Smallest published DNA density (k4-w12.txt) : 0.1337177020 (574,313,157 / 2^32)
Required <= 0.5% relative threshold         : 0.1330491135 (571,441,591 / 2^32)
Our exact DNA density (w12_k4_4ary.gm)      : 0.1327703733 (570,244,411 / 2^32)
Relative reduction vs OrensteinLab/Minimizers: -0.7085% (required >= 0.5000%)
Relative reduction vs OrensteinLab/10-minim. : -2.4076% (required >= 0.5000%)

VERIFICATION: PASS
PASS
```
