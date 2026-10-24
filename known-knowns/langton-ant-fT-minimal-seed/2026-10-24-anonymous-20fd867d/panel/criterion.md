# CRITERION skeptic verdict: Langton's ant g(k) table, target langton-ant-fT-minimal-seed
context: fresh headless Grok Build CLI session (grok -p), started with no prior conversation in a copy of claim/

## What I read
- claim/TARGET_CRITERION.md (binding criterion), CLAIM.md, METHOD.md, REPRODUCE.md, data/TABLE.txt, data/minimisers.txt
- Both exhaustive checkers in full: code/fsearch/fsearch.c (phase first-read completion, NPER=80, Dmin flag) and code/lcone/lcone.c (turn-word forcing, c_back, Hp), plus dmin_radius.py, check_onset.py, verify.py, calib.py, brute/brute.c, lcone/RESULTS.md, brute/SUMMARY.md
- Saved outputs: data/this-run/fsearch (RESULT lines for k=1..11, below_k*, ctrl_k10_T0, verify_py), data/this-run/lcone (all k*_w*.out, ctrl_blank, ctrl_k3_T127, ctrl_k7_T46, k11_T0), prior-run summaries and k=10 intermediate new-best lines
- NOVELTY_RECORD.md (not re-searched)

## What I ran
Rebuilt with gcc -O2 into ./\_review. Independent script _review/indep.py (separate simulator). Every heavy command under nice -n 19 and timeout.

- indep.py on data/minimisers.txt:
  - blank onset 9977; 0 turn mismatches on updates 9977..39976 (simulation length 40081 = through index 9977+30103); drift (-2,2) stable for 200 periods
  - cback 18; max projection drop over 40 periods is 18; Hp[0]=472 Hp[103]=369; revisit-after-Hp checks 0 failures (phases 0,1,50,103, 8000 steps)
  - debris radius 48; period-80 first-read Chebyshev min 159; first reads translate by the drift for 80 periods; max |coord| 597 (inside the 2048 grid)
  - independent T=0 enumeration over all 104 phases: exactly 2 seeds, both k=11, cell sets equal to the claim (phases 4 and 37); phases with k<=10: 0
  - all 13 listed minimisers: computed onset equals the listed t, and 400 turns match the blank highway word at the listed phase
- python3 claim/code/verify/verify.py data/minimisers.txt → blank 9977, all 13 ok, PASS
- python3 claim/code/fsearch/dmin_radius.py → drift (-2,2); translation True through 9977+11440; debris radius 48; period 80..85 minima 159,161,163,165,167,169 (projection lower bounds 158.5, 160.5, ...)
- check_onset.py blank → ONSET=9976; (0,-2) → ONSET=309 (the documented t-1 indexing)
- brute 1 309 1 0 → HIT s=309 esc=0 cells (0,-2); DONE configs=5041 escapes=0 min_filter_s=309
- fsearch (rebuilt), flagged=0 and Dmin=159 on every hit:
  - 0 9976 → NONE; 0 9977 → best_t=9977 minimisers=1 (blank control)
  - 1 309 NONE / 1 310 best_t=310 minimisers=1 cells (0,-2) nodes=95
  - 3 125 NONE / 3 126 best_t=126 minimisers=1
  - 4 66 NONE / 4 67 best_t=67 minimisers=1
  - 7 44 NONE / 7 45 best_t=45 minimisers=2 (both listed 7-cell sets) nodes=1150524
  - 10 0 NONE; 10 16 NONE nodes=16719; 10 17 best_t=17 minimisers=1 nodes=26544 maxR=9
  - 11 0 → best_t=0 minimisers=2, phases 4 and 37, same cells as the claim
- lcone (rebuilt, 1 worker):
  - 0 9977 → viol=0 mins=1, MIN t=9977 p=0 k=0; cback=18 Hp[0]=472 Hp[103]=369
  - 11 0 → mins=2, same two 11-cell lines; 10 0 → mins=0 viol=0
  - 10 17 → leaves=26988 viol=0 mins=1, same 10-cell seed
  - 3 127 → viol=1 at t=126 p=0, MIN t=127 p=1 (same cells; phase advances by 1)
  - 1 310 → leaves=190 viol=0 mins=1 cell (0,-2)
  - 5 62 → leaves=410495 viol=0 mins=1, the listed 5-cell seed
  - 7 46 → leaves=2212874 viol=2 mins=2, both 7-cell seeds as VIOLATION at t=45 and MIN at t=46 p=1
- Summed saved this-run lcone workers (5 each): k=1..10 viol totals all 0; mins totals 1,1,1,1,1,1,2,1,1,1

## Findings
Clause (i). Every table value and every listed minimiser was re-simulated by verify.py and, separately, by indep.py, which checks the future turn sequence against the blank period-104 word itself (not only periodicity). Blank onset is 9977. All 13 seeds match the claimed onset, phase, and word for 400 steps, with 104-step drift a rotation of (-2,2).

Clause (ii). The two checkers share no code: separate files, no common header, different tests (static 104-phase first-read lists versus forced turn word plus back-reach). diff reports the sources differ. Both are uncapped first-read searches on the infinite grid (grid 2048 only as storage; the ant stays at Chebyshev ≤597 over 40081 steps).

fsearch's completion test is the right criterion for "future turns = highway word": the path is determined by colours at future first reads. The 80-period truncation is justified for these runs. Dmin=159 is the min Chebyshev of period-80 first reads; later periods are the same list translated by (-2,2), so the distance increases by 2 each period (measured through period 108). Black debris at every phase lies in Chebyshev radius 48 < 159, so those far first reads are white in the phase. Placed cells satisfy 2*maxR+4 < 159 (maxR≤13 on k=1..10, maxR=29 on the blank K=0 run) and flagged=0, so a placed cell cannot sit on a far first read. The flag is global and only grows, so it covers every configuration the search accepts.

lcone's stop rule is sound on the same assumption. c_back=18 is the exact max of pi(start)-min pi over the next period, and the same drop bound holds for 40 further periods (the per-period pi shift is +8 and the worst drop stays 18). After Hp steps the projection test keeps every later ant cell strictly above the pre-history and above cells visited before T; sampled phases had no revisit for 8000 steps. Onset is persistent for a periodic word, so viol=0 at T-1 and the minimiser list at T is a complete search for g(k)=T. Depth-8 worker splits partition the tree; single-worker re-runs match the summed five-worker logs.

Controls. fsearch: blank K=0 gives NONE at 9976 and the unique onset 9977 at 9977; known seeds are found at the table T and absent at T-1 (k=1,3,4,7,10). lcone: blank viol=0 at 9976 with the onset at 9977; planted K=3,T=127 and K=7,T=46 report the known seeds as violations. k=0 is the classical blank value, re-simulated. k=11: onset 0 is minimal; both checkers and the independent 104-phase enumeration give exactly the same two 11-cell seeds, and K=10 at T=0 is empty in all three.

Clause (iii). CLAIM.md states the assumption explicitly: the blank highway from update 9977 repeats forever (drift (-2,2) per 104 steps). It is checked numerically, not proved. lcone's blank pre-pass and indep.py both see a pure period from 9977 through at least 9977+30000 updates.

Hidden quantifiers. The ant pose is fixed (origin, north, y down); minimiser counts are for that frame, as the criterion requires. Never-read black cells are excluded; starred cells are read after onset and are part of the seed; every listed seed uses exactly k cells. The onset used in the table is "updates already done" with blank 9977. check_onset.py and brute.c report one less (9976 / 309); CLAIM.md and METHOD.md say so, and it is an indexing difference, not a second answer. Prior-run fsearch node counts are larger because those runs used a looser TMAX (k=10 prior log shows intermediate onsets 27,25,22,20 before 17); best_t and the minimiser cells agree with this-run and with the rebuild.

## Caveats
The infinite continuation of the highway is an assumption, verified numerically through update index 9977+30103 and by the translation structure inside that window, and not given a formal proof here. I rebuilt representative cases (k=0,1,3,4,7,10,11 for fsearch; k=0,1,3,5,7,10,11 for lcone) rather than every saved worker log; the rebuilt RESULT/DONE lines match the saved this-run files on those cases, including node and leaf counts. I did not re-execute the k=2 box brute (12.7M pairs); I read its saved escapes=0, min filter-s=161 result. I did not repeat the OEIS / Jillhewar / H. Ke novelty search (OEIS fetch was blocked in this environment).

confirmed_scope: For Langton's ant (white right, black left), ant fixed at the origin facing north with y downward, g(k) for k=0..11 is 9977, 310, 162, 126, 67, 62, 49, 45, 40, 24, 17, 0 with minimiser counts 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2 in that frame modulo never-read cells, the 13 seeds in data/minimisers.txt, assuming the blank period-104 highway from update 9977 repeats forever.
scope: Verified clauses (i)–(iii) for the full k=0..11 table: both checkers' proofs by reading the code, independent word-level re-simulation of every minimiser and the blank grid, an independent exhaustive T=0 phase enumeration, a full k=1 box brute force, and rebuilt spot runs of both checkers including blank and planted-positive controls; did not re-run every saved multi-worker log, did not prove the highway runs forever, and did not repeat the novelty literature search.
pass: true
