# REPRODUCE skeptic verdict: LLRL ant g(6)=139 unique, target llrl-ant-minimal-seed (partial win p2)
context: fresh headless Grok Build CLI session (grok --prompt-file), started with no prior conversation in a copy of claim/

## what you read
- claim/CLAIM.md, METHOD.md, REPRODUCE.md, TARGET_CRITERION.md, NOVELTY_RECORD.md
- claim/data/minimiser_k6.txt, data/this-run/send_back.txt, data/this-run/audit/{COVERAGE_AUDIT.md,A_merged_recomputed.txt,B_merged_recomputed.txt}
- claim/data/this-run/C/*.txt (shipped C outputs); A/done/p22s2of4.txt, p06s1of8.txt; B/done/b0000.txt, b0159.txt; box_done_A/p16.txt
- After writing an independent simulator: claim/code/hsearch/{hsearch.c,merge_A.py,run_merge_A.sh,config.sh,jobs_A.sh}, claim/code/lcone4/{lcb_fast.c,merge_B.py,run_merge_B.sh}, claim/code/sim/ccheck.py, claim/code/indep/sim_llrl.py (usage only; logic not copied into the independent sim)

## what you ran (commands and key output lines)
Independent simulator written from CLAIM.md/METHOD.md (indep_sim_llrl.py) before opening claim/code. Rule: LEFT on {0,1,3}, RIGHT on 2; write c+1 mod 4; start (0,0) facing N; y down; H384 extracted from blank at t=256241.

```
H384 extracted: P=384 D_blank=(4, -4) h_blank=3
seed 0,1,3;0,2,2;1,2,3;1,4,3;2,1,3;3,0,1
read-match onset candidate: 139
cert at 139: True  (OK D=(-4, -4) phase=229 h=3 ...)
cert at 138: False  (heading 2->0)
blank cert at 256241: True  (OK D=(4, -4) ...)
blank cert at 256240: False  (heading 0->2)
k=5 seed 0,1,3;2,1,3;0,2,2;1,2,3;3,0,1 -> onset 174, cert True at 174, False at 173
```
All table minimisers k=1..6 independently certified at the claimed onset and failed at onset-1.

Rebuild and merge:
```
gcc -O2 -o ./hsearch claim/code/hsearch/hsearch.c
gcc -O2 -o ./lcb claim/code/lcone4/lcb_fast.c
sha256 prefixes: 9849e2885cb2a908 hsearch.c, cc15242f0c970a00 lcb_fast.c (match send_back)
sh code/hsearch/run_merge_A.sh
  jobs_total=84 jobs_done=84 pieces_covered=40/40 complete=yes tmax=140
  min_onset=139 n_minimisers=1
  MINIMISER 0,1,3;0,2,2;1,2,3;1,4,3;2,1,3;3,0,1
sh code/lcone4/run_merge_B.sh
  pieces_done=400/400 complete=yes
  leaves=5011329083 violation_lines=0 min_lines=1 flags=0
  n_min_seeds=1 n_violation_seeds=0
  BMIN 0,1,3;0,2,2;1,2,3;1,4,3;2,1,3;3,0,1
```
Independent sum over 400 B DONE files: same leaves/viol/mins/flags; single MIN in b0159.txt at p=229 (matches independent cert phase).

Cheap re-execution of rebuilt binaries:
```
./hsearch LLRL 1 555 256241 384 -  -> best_onset=555 minimisers=1 cells: (1,0,1)
./hsearch LLRL 2 318 256241 384 -  -> best_onset=318 minimisers=1 cells: (1,0,2) (1,-1,1)
./hsearch LLRL 3 245 256241 384 -  -> best_onset=245 minimisers=1 cells: (1,0,2) (1,-1,1) (0,2,3)
LCB_SPLITD=60 ./lcb LLRL 1 555 1 0 -> MIN t=555 ... (1,0,1) leaves=536 viol=0 mins=1 flags=0
LCB_SPLITD=60 ./lcb LLRL 2 318 1 0 -> MIN t=318 ... (1,0,2) (1,-1,1) leaves=32780 viol=0 mins=1
LCB_SPLITD=60 ./lcb LLRL 3 245 1 0 -> MIN t=245 p=261 k=3 cells: (1,0,2) (1,-1,1) (0,2,3)
                                      DONE ... leaves=1283843 viol=0 mins=1 flags=0
./hsearch LLRL 6 140 256241 384 - 40 6 8 8 1
  RESULT split=6/40@8 subtrees=41479 rule=LLRL K=6 NONE onset<=140 nodes=813055 tests=4282353 maxR=13 Dmin=238 sub=1/8
  (byte-identical to data/this-run/A/done/p06s1of8.txt)
LCB_SPLITD=60 ./lcb LLRL 6 139 400 0
  DONE rule=LLRL K=6 T=139 wid=0/400 leaves=207800322 viol=0 mins=0 flags=0
  (identical to data/this-run/B/done/b0000.txt)
LCB_SPLITD=60 ./lcb LLRL 6 139 400 159
  MIN t=139 p=229 k=6 cells: (0,1,3) (2,1,3) (0,2,2) (1,2,3) (1,4,3) (3,0,1)
  DONE rule=LLRL K=6 T=139 wid=159/400 leaves=8367759 viol=0 mins=1 flags=0
  (identical to data/this-run/B/done/b0159.txt)
python3 claim/code/sim/ccheck.py LLRL 30000 '0,1,3;...'
  C rule=LLRL onset=139 P=384 D=(-4, -4) cert_onset=True cert_onset-1=False
python3 claim/code/indep/sim_llrl.py '0,1,3;...' 30000
  INDEP onset=139 P=384 D=(-4, -4) cert_onset=True cert_onset-1=False heading=3 k=6
```
B-results-digest of concatenated sorted B/done/b*.txt = cbd7913df3b309c1 (matches send_back). A merge text matches send_back and audit/A_merged_recomputed.txt. Box A: 21/21 pieces present; 19 NONE onset<=174, p16 best=173, p21 best=174; all subtrees=41479.

## findings
- The stated 6-cell seed has onset 139 under an independent translate certificate; the certificate fails at 138. This matches checkers A, B, C, and the package indep sim (D=(-4,-4), heading=3, H384 phase 229).
- Blank onset 256241 and k=5 onset 174 also reproduce. Claimed unique minimisers for k=1,2,3 re-execute on both rebuilt A and B with viol=0 / unique MIN, matching the table.
- Re-merge of all shipped A and B outputs yields g(6)=139 with one minimiser, B covering 400/400 pieces, 0 VIOLATION (onset<=138), 1 MIN, flags=0. Sample k=6 A sub-piece and two k=6 B pieces replay identically, including leaf/node counts, so the shipped files are outputs of this source.
- A's SOL found_t=144 phase=234 is consistent with onset 139 phase 229 (234-(144-139)=229). Removing cell (1,4,3) recovers the k=5 minimiser at 174, so that cell is essential.
- No mismatch found in anything I re-executed.

## caveats
- Full k=6 checker A (84 sub-pieces / 40 pieces) and full checker B (~5.01e9 leaves, 400 pieces) were not re-run end-to-end; k=6 exhaustiveness is a merge plus two B pieces and one A sub-piece against shipped files.
- A-results-digest bc8fc1f6719817ee was not reconstructed from a known concatenation of the files in this tree (B digest was). Merge contents still match send_back.
- Binaries here used gcc -O2; send_back used -O3 -march=native. Search statistics still matched.
- K0 and exhaustive k=4,5 were not re-opened (p1). Novelty vs arXiv/OEIS was not independently re-searched beyond the shipped note.

scope: Independently simulated LLRL+H384 and certified the k=6 seed onset 139 (false at 138), blank 256241 and k=1..5 table seeds; rebuilt A/B, re-merged all shipped outputs, fully re-executed k=1..3 on both checkers, and replayed one home A sub-piece plus B pieces 0 and 159; did not re-run the remaining 82 A sub-pieces, 19 box A pieces, or 398 B pieces.
pass: true
