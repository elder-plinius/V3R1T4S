# How we found it (contributor text, unverified)

**The brief.** One lens of a V3R1T4S run was given the six traffic_signs_recognition_2023 rows at eps 1 that every tool
left unsolved, on the binarized 48x48 and 64x64 networks, with the rule that long searches run on the GPU (the
machine's CPU overheats, so the CP-SAT method that solved the 30x30 network's rows was not available for long runs).
The matching eps-3 rows of the 64x64 network had been falsified by alpha-beta-CROWN in seconds, which suggested that the
eps-1 boxes might be satisfiable too.

**What failed.** An exact integer model of the network on the GPU (checked against onnxruntime layer by layer) made
every candidate exact to score. Pixel-level tabu search stalled far below zero (64x64, image 6371: from -276 logit units
at the box centre to -252). Clipping alpha-beta-CROWN's eps-3 witnesses into the eps-1 box did not help (-264). A
moment-propagation search over per-pixel distributions reached -112. A search over freely chosen first-layer sign
patterns (a relaxation, not realisable in general) crossed easily (+100), which showed that the bottleneck was
realising a first-layer pattern with pixels.

**What worked.** Iterated target propagation (after Khalil, Gupta and Dilkina 2019): choose a first-layer sign pattern
that crosses in the relaxed problem at the lowest flip cost, then realise it with a continuous pixel step (hinge losses
on the first-layer thresholds, pixels kept strictly inside the box and snapped to a 2^-9 grid that keeps the first layer
exact in float32), score the realised point exactly, and re-plan from it. On image 6371 the rounds went -88, -36, -12,
-4, -8, 0 (a tie, not a counterexample) in 160 s; continuing from the tie with a higher weight on keeping the realised
bits crossed at +8 logit units within 66 s. One pixel was then moved by 0.5 so that the first-layer neuron closest to
its threshold (0.0064 pre-BN units) moved to at least 0.48 away without changing any sign; the logits stayed the same.
The witness was written as exact float32 values and checked by the run's own checker and the unmodified official
validator before the panel saw it. GPU time for the crossing: about 10 minutes of the lens's jobs (300-s jobs on one
RTX 5070 Ti).
