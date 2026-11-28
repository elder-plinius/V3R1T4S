# CRITERION skeptic verdict: LLRL ant g(6)=139 unique, target llrl-ant-minimal-seed (partial win p2)
context: fresh headless Grok Build CLI session (grok --prompt-file), started with no prior conversation in a copy of claim/

## what you read
- claim/TARGET_CRITERION.md (p2 = g(k) for k=1..6 with (i)+(ii); this claim is p2 only; p1/K0 background)
- claim/CLAIM.md, METHOD.md, REPRODUCE.md, code/METHOD_PACKAGE.md, NOVELTY_RECORD.md, data/scout.md, data/prior-p1/NOTE.txt
- claim/code/hsearch/hsearch.c (full), jobs_A.sh, merge_A.py, run_merge_A.sh, config.sh
- claim/code/lcone4/lcb_fast.c (full), merge_B.py, run_merge_B.sh
- claim/code/sim/ant.c, ccheck.py; claim/code/indep/sim_llrl.py
- claim/data/this-run/send_back.txt, audit/{COVERAGE_AUDIT.md,A_merged_recomputed.txt,B_merged_recomputed.txt}
- All A RESULT/SOL lines (21 box + 84 home), the unique B MIN line, C outputs, minimiser_k6.txt
- Local arXiv 2409.10124 abs HTML; public pages for GLR / Lutfalla / OEIS Langton sequences

## what you ran (commands and key output lines)
- Re-merge: `sh code/hsearch/run_merge_A.sh` → jobs_done=84/84 pieces_covered=40/40 complete=yes min_onset=139 n_minimisers=1 MINIMISER 0,1,3;0,2,2;1,2,3;1,4,3;2,1,3;3,0,1
- Re-merge: `sh code/lcone4/run_merge_B.sh` → pieces_done=400/400 complete=yes leaves=5011329083 violation_lines=0 min_lines=1 flags=0 BMIN same seed
- File audit: 21/21 box pieces K=6 split=/40@8 subtrees=41479; 19 NONE onset<=174, p16 best=173, p21 best=174, flagged=0; 84/84 home sub-pieces present, 82 NONE<=140, p22s2of4 best=139, p27s2of4 best=140; 400/400 B DONE K=6 T=139, 0 VIOLATION, 1 MIN, flags=0
- Independent Python sim (written this session): k=6 onset=139 P=384 D=(-4,-4) heading=3; blank onset=256241 P=384 D=(4,-4); k=6 period word is a rotation of blank H384 at offset 229; tube cert true at 139 / false at 138; k=5 seed tube cert true at 174 / false at 173
- Rebuild: `gcc -O2` of hsearch.c, lcb_fast.c, ant.c. Source sha256 prefixes match send_back (9849e2885cb2a908, cc15242f0c970a00, a6881fcb400fcca9, 155f62a8c6dad2fd)
- A spot-check: `./hsearch LLRL 6 140 256241 384 - 40 6 8 8 1` → RESULT split=6/40@8 subtrees=41479 ... NONE onset<=140 nodes=813055 tests=4282353 maxR=13 Dmin=238 sub=1/8 (byte-identical to data/this-run/A/done/p06s1of8.txt)
- A control k=3: `./hsearch LLRL 3 245 256241 384 -` → SOL onset=245 k=3 found_t=248 phase=264 cells: (1,0,2) (1,-1,1) (0,2,3); best_onset=245 minimisers=1 flagged=0
- B spot-check: `LCB_SPLITD=60 ./lcb LLRL 6 139 400 159` → blank: onset 256241 period 384; MIN t=139 p=229 k=6 cells: (0,1,3) (2,1,3) (0,2,2) (1,2,3) (1,4,3) (3,0,1); DONE leaves=8367759 viol=0 mins=1 flags=0 (identical to b0159.txt)
- B control k=3: `LCB_SPLITD=60 ./lcb LLRL 3 245 1 0` → MIN t=245 p=261 k=3 cells: (1,0,2) (1,-1,1) (0,2,3); leaves=1283843 viol=0 mins=1 flags=0. Same with LCB_NOTRIE=1 (trie does not change leaves/MIN/viol)
- C: ccheck.py, sim_llrl.py, ant.c all report onset=139 P=384 D=(-4,-4) cert true at 139, false at 138
- B-results-digest of concatenated B files = cbd7913df3b309c1 (matches send_back)

## findings
(i) holds for k=6. The unique 6-cell seed has onset 139 under the stated LLRL conventions (origin facing north, y down, L on {0,1,3} R on 2, write c+1 mod 4). Four simulators (package C pair, package indep sim, and a reviewer simulator) agree. Tube translate certificate holds at 139 and fails at 138. The period-384 read word is a rotation of the blank-grid H384 word at offset 229, which equals B's reported phase and A's onset phase (A found_t=144 phase=234 ⇒ 234-(144-139)=229). The seed is exactly the p1 k=5 minimiser plus (1,4,3); k=5 onset 174 re-checked by tube cert, no contradiction.

(ii) holds for k=6 by two independently written exhaustive checkers.
- A (hsearch.c): first-read DFS, budget K=6 (at most 6, not exactly 6). Phase-completion every STRIDE=8 against 384 H384 phases; exact_onset by backward word extension. best starts at TMAX+1. Cut `t>TMAX` always; best-cut `t>=best` only when dd>=SPLITD, so split numbering is identical across jobs (all 105 RESULT lines have subtrees=41479). SUBM/SUBJ keeps (sc/SW)%SUBM==SUBJ and partitions a piece. A finished TMAX=174 piece with NONE onset<=174 never lowered best, so it excludes every onset<=174 in that piece, including 139; p16/p21 best 173/174 still test at t=144<173, so they cannot hide an onset-139 seed. Home remainder ran at TMAX=140 (last STRIDE test at t=144, which is how p22s2of4 actually found found_t=144 onset=139). Combined coverage 40/40, one minimiser. flagged=0; maxR<=15 vs Dmin=238, so the NPER first-read list covers the search radius. zreqbad=0, min forced non-zeros=12 (consistent with background K0=12).
- B (lcb_fast.c): light-cone DFS to fixed T=139; VIOLATION = certified at t=T-1 (onset<=138); MIN = certified at t=T (onset exactly T once viol=0). 0 VIOLATION and 1 MIN ⇒ g(6)=139 unique. Split at step depth 60 into 400 jobs, independent of A's first-read split; B alone covers the space. Trie (DF=48) is a prefix necessary condition only: unknown/known cell rules match test_phase; LCB_NOTRIE on k=3 reproduced the same MIN/leaves/viol. flags=0 so no uncertified leaf.
- A and B share no code (different grids, search, highway test, split; identifier overlap is C stdlib plus SPLITD). They agree on the unique k=6 seed and, as a control, on unique g(3)=245 with matching phase arithmetic (A 264 at found_t=248 ⇒ onset phase 261 = B).
- Controls: blank onset 256241 P=384 (B discovers it; reviewer sim agrees); planted positives k=3 and k=6; known negatives B viol=0 at T=139 and cert failure at 138. Hidden quantifiers: fixed frame; first-read colouring implements modulo never-read; onset is least t with H384 word match (not found_t); budget is at most k.

## caveats
- Full k=6 A (84 jobs) and B (400 pieces, 5.01e9 leaves) were not re-executed; only source-rebuild plus cheap controls and one A sub-piece / one B piece. Those spot-checks matched the shipped RESULT/DONE lines exactly.
- A-results-digest bc8fc1f6719817ee was not reproduced by an obvious hash of the shipped A files; coverage and merge were recomputed from the files themselves.
- Package sim_llrl.py is the same certificate method as ccheck.py; H384 identity was therefore checked by comparing period words, not by trusting C alone.
- Completeness for k=1,2,4,5 was not re-proven here (p1 background). k=3 was re-run as a control.

confirmed_scope: LLRL g(6)=139 with unique minimiser (0,1,3)(0,2,2)(1,2,3)(1,4,3)(2,1,3)(3,0,1) in the claimed frame, re-confirmed by independent simulation plus translate certificate, with exhaustive at-most-6 completeness from shipped hsearch.c and lcb_fast.c outputs whose code, splits, TMAX=174 semantics, and B T=139 VIOLATION/MIN/trie I checked; k=1..5 left as p1 background.
scope: Verified (i) for the k=6 seed (onset, H384 word, cert at 139 not 138) and (ii) for k=6 by reading A/B, re-merging all shipped pieces, and re-running cheap A/B/C controls; did not re-execute the full k=6 searches or re-open p1/K0.
pass: true
