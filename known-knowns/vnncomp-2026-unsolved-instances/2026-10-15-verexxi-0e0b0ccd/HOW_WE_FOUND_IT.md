# How we found it (contributor text, unverified)

**The target.** One of seven VNN-COMP 2026 traffic-sign instances on the binarized 48x48 and 64x64 networks that all
three tools left at timeout. A win needs an input strictly inside the allowed box that the official validator rates
`correct` at zero tolerance.

**An exact model first.** We rewrote the network (+-1 convolutions, max-pool before batch norm, sign activations) as
exact integer threshold tests on a float32-exact pixel grid, x = v + off + m*d (the pixel map from the earlier
V3R1T4S 3_30_30 work). Its logits match onnxruntime exactly.

**What didn't work.** A gradient search through a smoothed version of the network stalled at a logit gap of -18 (a
win needs +2). Exact local search guided by gradients got to -10. CP-SAT on windows of the exact model never improved
a local optimum. Tabu search, kicked iterated local search, shrinking down from a larger box (eps 4 and 5) and crossing
over good solutions all stalled at -2.

**What worked.** Many independent restarts (smoothed search, then exact local search) produced a few solutions at -2.
Comparing them showed that only 8 of the 107 hidden units that matter ever changed, and that two of them (147 and
209) were never both on the helpful side. That pointed to the one unit each solution was missing. A local search
that rewarded unit 109's distance to its threshold, started from the right solution, reached +2 in about 4.5 minutes.
Total compute: about 5 hours on a 4-core cloud machine, most of it spent on dead ends.
