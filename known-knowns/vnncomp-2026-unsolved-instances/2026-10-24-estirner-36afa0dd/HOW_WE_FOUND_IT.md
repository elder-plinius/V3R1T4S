# How we found it (contributor text, unverified)

**The target.** One of the 14 VNN-COMP 2026 `challenging_certified_training_2026` instances that every participating tool
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

**What worked.** On `cifar10_eps8_wide_cnn7` idx 7490 sample 8 (true class 4, deer) the plain multi-rival attack
(300 s) crossed zero in its second stage on rival 6 (frog), at a thin margin of +7.98e-5. A focused run warm-started
from that point raised it to +4.06e-4 (onnxruntime CPU float32), about 400 times the 1e-6 floor; the witness was then
snapped to exactly representable float32 values strictly inside the box and checked in onnxruntime, onnx.reference and
torch float32/float64. GPU time for this row: 311 s (plain attack) plus 611 s (focused attack) on one RTX 5070 Ti.
