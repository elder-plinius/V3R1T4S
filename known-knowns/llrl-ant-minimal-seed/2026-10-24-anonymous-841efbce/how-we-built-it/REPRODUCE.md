# REPRODUCE (all from inside claim/; gcc -O2, python3; times on one core)
```
cd code/hsearch && gcc -O2 -o hsearch hsearch.c
# A: args RULE K TMAX t0 P canon [W wid SPLITD]; TMAX is the inclusive onset bound being proved (not a cap)
./hsearch LLRL 1 600 256241 384 - 1 0 6     # best_onset=555, 1 minimiser (1 s)
./hsearch LLRL 2 320 256241 384 - 1 0 6     # 318 (seconds)
./hsearch LLRL 3 250 256241 384 - 1 0 6     # 245 (seconds)
./hsearch LLRL 4 196 256241 384 - 4 $w 6    # w=0..3, 195 (about 4-5 CPU-min total)
./hsearch LLRL 5 175 256241 384 - 4 $w 6    # w=0..3, merge rule: min best_onset; union of SOL at it. Unbalanced: w2 took ~51 min, others 4-9 min (data/this-run/A/k5_T175_w*)
./hsearch LLRL 5 174 256241 384 - 40 $i 8   # i=0..39, balanced alternative (seconds to ~15 min each, ~1 CPU-hour total); second independent A pass, see data/this-run/A/q_k5_T174 if present
./hsearch LLRL 11 0 256241 384 - 1 0 6      # NONE (K0-1 negative)
./hsearch LLRL 12 0 256241 384 - 1 0 6      # best_onset=0, 10 minimisers
./hsearch RL 1 320 9977 104 - 1 0 6         # control: Langton 310 (also K=2 -> 162, K=3 -> 126)
cd ../lcone4 && gcc -O2 -o lcb_fast lcb_fast.c && gcc -O2 -o lcb lcb.c
# B: args RULE K T [NPIECES piece]; one run at T tests depth T-1 (VIOLATION lines) and T (MIN lines)
./lcb_fast LLRL 1 555 1 0                   # 0 VIOLATION, MIN = (1,0,1)
./lcb_fast LLRL 2 318 1 0 ; ./lcb_fast LLRL 3 245 1 0 ; ./lcb_fast LLRL 4 195 1 0   # k=4 ~1 CPU-min
./lcb_fast LLRL 2 319 1 0                   # planted-positive control: the 318 seed appears as VIOLATION at 318
LCB_SPLITD=25 ./lcb_fast LLRL 5 174 40 $i   # i=0..39; sum leaves 542179718, viol 0, one MIN (data/this-run/B/k5_T174)
./lcb_fast LLRL 11 0 1 0 ; ./lcb_fast LLRL 12 0 1 0   # none / 10 MIN
LCB_NOTRIE=1 ./lcb_fast ...                 # disables the prefilter (= original lcb.c test), for comparison
cd ../sim && python3 ccheck.py LLRL 20000 "0,1,3;2,1,3;0,2,2;1,2,3;3,0,1"   # C: onset=174 P=384 cert at onset True, onset-1 False
```
