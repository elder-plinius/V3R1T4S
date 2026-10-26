# REPRODUCE verdict (final)
context: fresh-context subagent session (no prior conversation), sees only claim/
Role: REPRODUCE (skeptic panel). Output file: reproduce.md. All file names relative to claim/.

## What I reproduced myself (own code, mine/sim.c, written before opening code/)
- Own simulator + own certificate W(s) ("window at s+104 equals window at s shifted by v on the whole future sweep"),
  criterion, soundness proof, converse and T_cap exactness in mine/CERTIFICATE.md. T_cap = L-103 = first step from which
  the motion is 104-periodic forever (comparable to lantx2 and lant4).
- 4x4: all 65,536 masks, columns mask tcap vx vy dir CAP identical to data/validation/enum4_lant2.txt.
- Hard cases: all 4096 per-chunk maxtcap_mask of data/user-chunk-sums/chunk_*.sum: all CAP, T_cap equal to the chunk maxtcap (0 mismatches);
  includes the global max 375,545 at mask 40920836116.
- Coverage: the 4096 summaries cover [0, 2^36) contiguously, every chunk 16,777,216 lines, all CAP, UNCAP 0, OOB 0, fix-ups 0.
- Sample (the independent recheck p1 requires): own implementation of METHOD.md section 4 selection (splitmix64(mask+SEED) mod 10000 < 100,
  pass = r div 25), and FULL re-simulation of all 16,384 units (4 passes x 4096 chunks) with mine/sim, files mine/units/p<P>_c<CCCC>.txt
  (job 2026-10-20 21:29-23:04 EDT, 4 workers, nice 19). Result: 687,234,013 masks re-simulated (= 1.000057% of 2^36), 687,234,013 captured,
  0 not captured (0 UNCAP, 0 OOB). Unit-by-unit comparison with data/sample/sample_units.txt (sh mine/compare.sh): 16,384 of 16,384 units
  equal in n, CAP, UNCAP+OOB, maxtcap, maxtcap_mask and sumtcap; differing units: none. Max sampled T_cap 271,692 at mask 61493184540
  (equals data/sample/sample_summary.txt). No unit's sample max exceeds its chunk's maxtcap.
- Determinism: units (0,0), (1,777), (2,2439), (3,4095) recomputed in the foreground byte-identical; hard-case and 4x4 runs repeated byte-identical.
- Steps and linehash were not compared (author-tool specific, as the prompt allows).

## Only consistency-checked (not reproduced)
- The exhaustive ~40 h lant4 run itself (per-mask output exists only as sha256 per chunk); I checked the summaries' internal consistency only.
- REPRODUCE.md: sh code/scripts/run_all.sh run with my job stopped: RUN_ALL: PASS (summaries, 4x4, 5x5 slice, hard, lant4 vs lantx2 small range,
  4 sample units IDENTICAL, Python selection recount, 8/8 tamper tests detected). Log: mine/run_all.log.

## Proof assessments (METHOD.md)
Certificate X (section 1, lantx2):
 1. B0 contains every black cell at s0 (black => initially in box or visited): sound.
 2. Predicted period from the heading ring, v must be (+-2,+-2): sound (only a prediction; it is verified by step 4).
 3. M = floor(min span/2); K >= M with V0+Kv strictly beyond B0: sound; code computes K conservatively (integer division can only enlarge K).
 4. Observed periods 0..K; induction: E_p(c) = XOR_{m=1..p} P0(c+mv); nonzero terms need c+mv in V0, i.e. 2m <= span in both coordinates, so m <= M;
    hence E_p = E_K for p >= K and period p repeats: sound. T_cap = L-103 is intrinsic (independent of detection time): sound.
Certificate C(s) (section 2, lant4):
 1. E_k for k >= k*: cells outside B (B = box + positions to t >= s+104) are white in G_s, P supported on V inside B: sound.
 2. Telescoping E_0..E_{k-1} to D_k: sound.
 3. Period lemma (same start heading and same colours on V+kv => same 104 steps translated): sound.
 4. Induction I_k using G_{s+104k}(x) = G_s(x) XOR sum P(x - mv) and D_k: sound. 5. Conclusion: sound.
 C(s) is equivalent to my W(s) (G_{s+104}(c+v) = G_s(c+v) XOR P(c+v)), and by my converse it holds at the intrinsic onset unless the k>1024
 window limit is hit (then -1, never a capture), so lant4's T_cap equals the intrinsic T_cap whenever it reports CAP; consistent with the per-mask equalities.
 Code reading: checkC compares G_s(c) with G_s(c+v) XOR P(c+v) after rewinding the grid to time s, bbox taken at t: matches the text.


## Verdict
Reproduced with independent code: the full 1% sample (all 16,384 units, 687,234,013 masks), all 4096 hard cases, all 65,536 4x4 masks,
with exact agreement on every compared quantity and no uncaptured mask; both certificate proofs re-derived and sound, my own certificate
proved (mine/CERTIFICATE.md). Only consistency-checked: the exhaustive 2^36 lant4 run (summaries contiguous, all CAP; not rerun, ~40 h),
REPRODUCE.md scripts (RUN_ALL: PASS). This confirms bank partial win p1 as stated (the conjecture itself is not claimed and not confirmed).
pass: true
