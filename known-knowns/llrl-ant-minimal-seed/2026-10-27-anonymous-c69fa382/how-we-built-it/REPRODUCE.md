# REPRODUCE

## 1. Independent simulator (do this BEFORE reading code/sim or code/indep)
From the definition in CLAIM.md, write your own LLRL simulator + translate certificate. Check:
  seed 0,1,3;0,2,2;1,2,3;1,4,3;2,1,3;3,0,1  -> onset 139, P=384, cert true at 139, false at 138.
Optional: blank -> 256241; k=5 seed 0,1,3;2,1,3;0,2,2;1,2,3;3,0,1 -> 174.

## 2. Re-merge the shipped raw outputs (seconds)
  sh code/hsearch/run_merge_A.sh
  sh code/lcone4/run_merge_B.sh
Expect: A complete 84/84, min_onset=139, one MINIMISER; B pieces_done=400/400, leaves=5011329083, viol=0, mins=1, same BMIN.

## 3. Rebuild A and B; cheap controls
  gcc -O2 -o ./hsearch code/hsearch/hsearch.c
  gcc -O2 -o ./lcb code/lcone4/lcb_fast.c
Checker A argv: hsearch RULE K TMAX T0 P [canon] [SW SWID SPLITD] [SUBM SUBJ]
  ./hsearch LLRL 3 245 256241 384 -
Checker B argv: LCB_SPLITD=<depth> lcb RULE K T NPIECES WID
  LCB_SPLITD=60 ./lcb LLRL 3 245 1 0          # full k=3 at T=245 (no split)
  LCB_SPLITD=60 ./lcb LLRL 6 139 400 0        # one of 400 k=6 pieces (~1 min on this box)
Spot-check: re-run one home A sub-piece and one B piece; compare DONE/RESULT lines to data/this-run/.
Full k=6 A (84 jobs) or B (400 pieces, ~5.01e9 leaves) is hours — if you cannot finish, say so in scope; a sample is not a full re-execution.

## 4. Package C
  python3 code/sim/ccheck.py LLRL 30000 '0,1,3;0,2,2;1,2,3;1,4,3;2,1,3;3,0,1'
  python3 code/indep/sim_llrl.py '0,1,3;0,2,2;1,2,3;1,4,3;2,1,3;3,0,1' 30000
