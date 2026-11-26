# How we found it (contributor text, unverified)

**The target.** One of 14 VNN-COMP 2026 `challenging_certified_training_2026` instances that every participating tool
left unresolved (8 tools; the benchmark authors' own alpha-beta-CROWN run also timed out at about 1000 s) and that are
neither claimed elsewhere nor proved safe by the authors. A win needs an input strictly inside the box that the official
validator rates `correct` at zero tolerance.

**The judge first.** Our own checker (exact rational bounds, onnxruntime plus onnx.reference) and the unmodified
official validator were re-tested on a published positive and a negative control before any attack.

**What we ran.** A GPU multi-rival margin attack (sign-PGD with momentum and a cosine step schedule, thousands of
restarts from uniform, vertex and centre starts, then Adam on a sigmoid reparametrisation around the best points) on
every eligible certified-training row, the cora rows and the cifar100/tinyimagenet ResNets, each candidate replayed on
CPU onnxruntime. As a positive control it found a counterexample for the instance of open PR #566 (by mizopl) within 44 s,
so the attack is at least as strong as the one that found that one.

**What didn't work.** On most rows the attack plateaus well below zero (margins of -0.1 to -14) and long second stages
add almost nothing; growing the box (homotopy) and projecting crossing points back did not cross on this row.

**What worked.** On `cifar10_eps8_cnn7` idx 4688 sample 8 (true class 7, horse) the plain multi-rival attack
(300 s budget) crossed zero on rival 8 (ship) with margin +0.002304911613 (onnxruntime CPU float32); no focus run was needed.
The witness was then snapped to exactly representable float32 values strictly inside the box and checked in
onnxruntime, onnx.reference and torch float32/float64. GPU time for this row: 137.8 s on one RTX 5070 Ti.
