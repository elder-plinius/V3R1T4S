context: subagent

# Criterion panel file (criterion skeptic)

Files read in claim/: CLAIM.md, PROOF.md, FORMAT.md, PREREG.md, REPRODUCE.md, table/ (the run's fetch records, not shipped; the-record-we-beat/record.md summarizes them), checkers/check_d.c (all), checkers/check_e.c (header), tests/ (lemma1_small.py and exact_small.py run). Not read: how-we-built-it/ (producer code), tests/sim_rate17.c, checkers/check_a17.c (not run, per memory limit), the saved status page and open-pull list beyond what the run's scout note reports. No request was blocked (no HTTP 401, 403 or 429).

## Clause-by-clause reading

1. "Rigorous bound on gamma_2, lower side." The claim is gamma_2 >= 833267/1048576 = 0.794665336609. Rechecked with Fractions: 13332272/2^24 = 833267/1048576 = 0.7946653366088867. The statement is deterministic (E-based inequality, no failure probability). The proof (PROOF.md sections 1 to 7) is short and I re-derived each step:
   - Increment form (section 2): sound.
   - Invariant F_p <= L(x, l+p) (section 3): sound.
   - Complement symmetry and the Markov property (section 4): sound.
   - Telescoping (section 6): sound.
   - Lemma 1: concatenating A_x A'_y against B_y B'_x, both of length n, gives 2 E L(x,y) <= E L(n,n) <= n gamma_2. Sound.
   - Lemma 2 uses McDiarmid's inequality plus a union bound on the exact expectation. It is an analytic step, not a sampled estimate, and leaves no residual failure probability.
   I found no error in the proof.

2. "Strictly better than the best rigorous bound at verification time." The bar is 0.792665992 (Heineman et al., arXiv 2407.10925). The table records show the Tao page 31a, Tomar's Zenodo record 23610945 (version 5, upper bounds only), and the open PRs. Per the run's scout note none changes the lower bound. The 0.79970 entry is labeled Monte Carlo with a Hoeffding margin and is correctly excluded under the criterion. The margin is 0.7946653366 - 0.792665992 = 0.001999345. That is about 2000 times the required 1e-6. My own single WebSearch found no newer binary lower bound than arXiv 2407.10925, but the search index may lag. I did not fetch arXiv directly. The scout's check for newer arXiv or Zenodo claims is only partly documented in table/.

3. "Not probabilistic." The Hoeffding-type tool (McDiarmid) appears only inside the proof of an exact-expectation inequality. The statement has no confidence level and no sampled estimate. The criterion's exclusion targets sampled bounds, so this does not trigger it. tests/sim_rate17.c and my own simulation are labeled numerical sanity checks and are not part of the bound.

4. "A certificate a skeptic re-runs ... finite-length computation with exact or outward-rounded arithmetic." The certificate is object/c17.{counts,states,V}: 242,084,334 states, with sha256 matching REPRODUCE.md for all three files. The finite computation is conditions C1, C2, C3 over all states in exact int64/int128 integers. The remaining step is an analytic T -> infinity limit, the same shape as the Lueker and Heineman arguments. I count it as meeting "finite-length computation" and flag it as a reading, not a free pass.
   Reruns, with binaries built in my own folder:
   - check_d 17 16777216 13332272: `N=17 states=242084334 rowStates=107272712 shiftStates=134811622 minE=13332272 (attained by 3 states, first index 4751) failures: structure=0 C1=0 C2=0 C3=0 ACCEPT m=13332272 K=16777216` (31 s).
   - check_e 17 16777216 13332272: `minE=13332272 sumE=3227536924871139 meanE=13332283.306160 violations C1=0 C2=0 C3=0 ACCEPT m=13332272 K=16777216`.
   - Negative control, check_e with m=13332273: `C3=3 ... first problem: C3: b=1 h=32865 pol=ROW E=13332272 < m=13332273 ... REJECT`. So the bound is tight at m and not over-claimed.
   - check_a17 was skipped (1.7 GB); the perturb and drop controls were not rerun.
   - Small cases: `python3 -I tests/lemma1_small.py` printed "Lemma 1 small cases hold: True". tests/exact_small.py on N=5 printed "ok=True", the telescoping inequality "True", and "exhaustive T=12: paths=131072, violations of F_p<=LCS: 0".
   Own test, run as `python3 -I mytest.py <claim dir> 3000 4` (mytest.py not shipped):
   - It reads object/c17.* by pread.
   - It re-implements the transitions independently in increment form.
   - It checks C3 at 3000 random states (1270 ROW, 1730 SHIFT): min E = 13332279 >= m, 0 violations.
   - It simulates the certificate's policy on random strings for 4 runs of 3000 steps each, all states found in S.
   - It checks against a true LCS DP that F_p <= L(x, l+p) for all p, and R <= L(x,l) <= L(x,y). This held in all 4 runs, e.g. R=1197, L(x,y)=1222.
   - Mean R/T = 0.3972 against m/(2K) = 0.3973, consistent with the claimed rate.

5. "At least 1e-6 absolute." The margin over the public bar is 0.001999. The margin over the unfiled N=16 own result (0.793914556503) is 7.5e-4, so the frozen package threshold 0.7939155565 is met too (Fractions test True).

6. Null model. PREREG's "null_test not needed" holds. The claim is a deterministic verification of an explicit object, not a search or statistical estimate, so there is no selection effect to calibrate. The negative controls reject. The one residual risk is a shared misreading of the format and proof by every checker. My independent increment-form implementation and the true-LCS simulation are the check against that, and they agree.

## What is not established
- The proof and certificate are unrefereed and appear on no source list. This is one contributor's result, and the three checkers (two of which I reran) are the same lineage as the producer's notation.
- check_a17 and the perturb and drop controls were not rerun by me.
- The sampled check covers 3000 states and 4 runs. The exhaustive check is the shipped checkers' only.
- Whether a newer arXiv or Zenodo lower-bound claim exists was checked only through table/ and one web search, not by direct arXiv fetch.
- The proof relies on cited standard results: Fekete's lemma and McDiarmid's inequality. I did not re-prove them.
- The Lueker, Heineman and Tomar sources were not read in full. I relied on the page text and the search summary.
- This is a lower bound only. It says nothing about the value of gamma_2.

confirmed_scope: Given the shipped certificate (object/c17.{counts,states,V}, N=17, K=2^24, m=13332272) and the proof in PROOF.md, both checkers I reran (check_d and check_e) accept in exact integer arithmetic over all 242,084,334 states (C1, C2 and C3 hold, minimum E equals m), so gamma_2 >= 833267/1048576 = 0.7946653366 holds as a deterministic, non-probabilistic lower bound that exceeds the bar 0.792665992 recorded in table/ by 0.001999, subject to the unrefereed status of the proof, the unrerun check_a17, and a bar check limited to table/ and one web search.
pass: true
