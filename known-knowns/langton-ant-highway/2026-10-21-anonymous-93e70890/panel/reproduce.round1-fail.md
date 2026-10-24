# REPRODUCE verdict — Langton's ant 6x6 box, bank partial win p1

context: fresh-context subagent session (no prior conversation), sees only claim/

## Own checker (written before opening code/)
mine/ant.c. Built only from the convention in CLAIM.md: "Mask bit b (0..35) is the cell (x, y) = (b mod 6 - 2, floor(b/6) - 2) ... Ant starts at (0,0) with heading 0 (north). Directions: 0:(0,+1), 1:(+1,0), 2:(0,-1), 3:(-1,0). One step: g = colour of the ant's cell; heading d = (d + 1 + 2g) mod 4 ...; flip the cell; move one cell in direction d. Cap: 2,000,000 steps." For 4x4 the mapping is bit b -> (b%4-1, b//4-1).
Byte grid 4096x4096; stops as OOB within 64 cells of the edge.

Capture criterion (mine): h(u) is the heading after u steps; L is the last u with h(u) != h(u-104), where h(u-104) is undefined for u < 104. Once u - L >= 208, set s = u - 104. Period 0 is pos(s..s+103), with displacement v = pos(u) - pos(s), which must be (+-2,+-2). B is the bbox of the box plus every position up to u. M = floor(min(span_x, span_y)/2) of V0. K is the least K >= M for which bbox(V0) + K v lies strictly beyond B in a coordinate where v moves away. Then I keep simulating to s + 104(K+1) with no new mismatch. T_cap = L - 103, dir = h(T_cap).
Why this means the highway forever: for p >= K the cell c + p v (c in V0) lies outside B. So it was untouched before s, and its colour at the start of period p is XOR_{m=1..p} P0(c + m v), where P0 is the set of cells visited an odd number of times in period 0. A nonzero term needs c + m v in V0, so 2m <= span and m <= M <= K. That makes E_p the same for every p >= K, and period K was observed. Induction then gives periodicity forever, with no black cell of time s (so no initial black cell) in the sweep V0 + p v for p >= K. T_cap = L - 103 is the intrinsic start of the periodic motion.

## Results (all mine/ unless noted)
- (a) 4x4: all 65,536 masks. My (mask tcap vx vy dir status) is byte-identical to data/validation/enum4_lant2.txt (columns 1-5 and 7).
- (b) Summaries (mine/chk.py): the 4096 files chunk_0..4095.sum are contiguous with first = previous last + 1. Each has 2^24 lines, all CAP, UNCAP 0, OOB 0, fix-ups 0, and maxtcap_mask inside its range. Together they cover [0, 2^36) exactly, giving 68,719,476,736 CAP. Global max is 375,545 at mask 40920836116.
  Hard cases: I reran ALL 4096 per-chunk maxtcap masks with my simulator (8.7 s). All are CAP with T_cap equal to the summary (0 mismatches), and all 6 columns match data/hard-cases/hard_lantx2.txt (0 differences). The global max gives 40920836116 375545 -2 2 1 CAP.
- (c) Sample: my own implementation of the METHOD.md section 4 hash selection, with my simulator, on 107 units. That is 7 named units ((0,0) (1,777) (2,2439) (3,4095) (0,1234) (2,3000) (3,17)) plus 100 seeded-random units. n, CAP, maxtcap, maxtcap_mask and sumtcap equal data/sample/sample_units.txt in every unit (0 mismatches). Example: (0,0) gives n 41799, maxtcap 107010 at 14946136, sumtcap 173075090. (2,2439) gives n 41777, maxtcap 150778.
  Consistency only: data/sample/sample_units.txt has 16,384 units with n = 687,234,013 (1.000057% of 2^36), all CAP, no UNCAP/OOB, and 0 units whose max exceeds the chunk maxtcap.
- run_all.sh: RUN_ALL: PASS in 88 s. The 4x4, 5x5 chunk07 (sha a75f41cd...), hard (0 mismatches), lant4 vs lantx2 (65,536 masks), 4 sample units, sample summary and tamper (8 of 8) steps all match REPRODUCE.md.
- Determinism: my checker and the package's tools gave the same numbers. I found no non-determinism.

## Proof review
Certificate X (METHOD.md section 1):
- Step 1: sound. B0 contains every cell black at s0.
- Step 2: sound. The prediction comes from the ring and is only a hypothesis, which step 4 checks.
- Step 3: sound. For M, overlap requires 2m <= span. K's "strictly beyond in a coordinate moving away" is monotone in p.
- Step 4 and the induction: sound. E_p for p >= K equals XOR_{m=1..M} P0(. + m v) and does not depend on p, because p >= K >= M. The base case, period K, is observed.
- T_cap = L - 103 is intrinsic: sound.
I re-derived the same argument independently and my checker implements it. The T_cap values agree exactly.

Certificate C(s) (section 2): this is a SKETCH, not a proof. It compares the grid at detection time t, not at s, and the closure "beyond bbox all white" is asserted without the overlap/parity bookkeeping that X carries. It looks plausibly sound and agrees empirically on 4x4, 5x5, the hard cases and 3x2^20 masks. But it is the only certificate behind the ~99% of 6x6 masks outside the sample and hard set. That is not adequate as a proof for those masks, and the claim honestly labels it SKETCH.

## What was reproduced vs only checked for consistency
- Reproduced independently: all 4x4 masks; all 4096 hard cases; 107 of the 16,384 sample units (about 4.5M masks, about 0.65% of the 1% sample).
- Consistency only: the exhaustive 2^36 run (per-chunk summaries and sha256; it cannot be rerun here, ~40 h); the remaining 16,277 sample units; the full-chunk sha256 matches (claimed in data/validation, not rerun: over 8 minutes each).

## Objections
1. p1's independent re-check of the random 1% sample is not fully reproduced. Only about 0.65% of it was re-simulated (a spot check). The full sample needs about 9 CPU-hours with my checker, which does not fit the 20-minute, single-thread limit. Every checked unit matched exactly.
2. The exhaustive part rests on the lant4 summaries and on certificate C(s), which is only a sketch.
3. No mismatch of any kind was found.

Verdict: everything I could check agrees exactly, including all hard cases. But the p1 random-sample re-check is only spot-checked here, and the exhaustive coverage cannot be re-verified. By the rule that a sample is a spot check and an unfinished check is a fail, I cannot genuinely confirm.

pass: false
