# REPRODUCE skeptic verdict: LLRL ant g(k) table k=0..5 and K0=12, target llrl-ant-minimal-seed (partial win p1)
context: fresh headless Grok Build CLI session (grok --prompt-file), started with no prior conversation in a copy of claim/

## what you read
- claim/CLAIM.md, claim/REPRODUCE.md, claim/METHOD.md, claim/TARGET_CRITERION.md, claim/code/sim/CERT.md (certificate statement only, after writing my own simulator)
- claim/data/minimisers.txt (16 seeds: k=0..5 plus 10 of k=12)
- claim/data/this-run/{A,B,C} stored RESULT/MIN/DONE lines for comparison (val_k1, val_k2_T318, val_k3_T245, k11_T0, k12_T0, B/k5_T174/p12 and p27, compare_k5.txt)
- claim/code/hsearch/hsearch.c and claim/code/lcone4/lcb_fast.c only after the independent simulator existed, in order to rebuild them

## what you ran
Independent simulator (rule from CLAIM.md: L on {0,1,3}, R on 2; write c+1 mod 4; start (0,0) heading N; N=(0,-1)). Translate certificate implemented from CERT.md.

`timeout 400 nice -n 19 python3 -u own_sim.py`
- blank 280000 updates; tail least period 384; onset by backward extension 256241; drift (4,-4)
- cert at onset True D=(4,-4); cert at onset-1 False; period-eq fails at onset-1
- all 16 minimisers: listed onset, cell count = k, cert True at onset, cert False / period-eq fails at onset-1 (k=12 onset-1 N/A)
- k=1 exhaustive: 133 unique blank first-reads in [0, 555+384); 399 colourings; min onset 555 seed=1,0,1; earlier_than_555=0

`timeout 400 nice -n 19 gcc -O2 -o own_exh own_exh.c && ./own_exh 1`
- BLANK_ONSET 256241 OK
- K1 RESULT tried=399 min_onset=555 seed=1,0,1 earlier_than_555=0

`timeout 400 nice -n 19 ./own_exh 2`
- k2 blank first-reads in [0,702): 112
- K2 RESULT tried=111765 min_onset_seen=-1 earlier_than_318=0

Rebuilt claim checkers: `gcc -O2` on hsearch.c and lcb_fast.c.
- `./bin/hsearch LLRL 1 600 256241 384 - 1 0 6` → best_onset=555 minimisers=1 cells (1,0,1); identical to this-run/A/val_k1.txt
- `./bin/hsearch LLRL 2 320 256241 384 - 1 0 6` → best_onset=318 cells (1,0,2) (1,-1,1)
- `./bin/hsearch LLRL 3 250 256241 384 - 1 0 6` → best_onset=245 cells (1,0,2) (1,-1,1) (0,2,3)
- `./bin/hsearch LLRL 11 0 ...` → NONE onset<=0 (matches this-run/A/k11_T0.txt)
- `./bin/hsearch LLRL 12 0 ...` → best_onset=0 minimisers=10 (matches this-run/A/k12_T0.txt and minimisers.txt as sets)
- `./bin/lcb_fast LLRL 1 555 1 0` → viol=0 mins=1 leaves=536 MIN (1,0,1)
- `./bin/lcb_fast LLRL 1 554 1 0` → viol=0 mins=0 leaves=536
- `./bin/lcb_fast LLRL 2 318 1 0` → viol=0 mins=1 leaves=32780
- `./bin/lcb_fast LLRL 3 245 1 0` → viol=0 mins=1 leaves=1283843
- `./bin/lcb_fast LLRL 11 0 1 0` → mins=0; `./bin/lcb_fast LLRL 12 0 1 0` → mins=10, same 10 cell-sets
- `LCB_SPLITD=25 ./bin/lcb_fast LLRL 5 174 40 27` → leaves=2896460 viol=0 mins=0 (matches p27.txt)
- `LCB_SPLITD=25 ./bin/lcb_fast LLRL 5 174 40 12` → MIN t=174 cells (0,1,3)(2,1,3)(0,2,2)(1,2,3)(3,0,1) leaves=11730989 viol=0 mins=1 (matches p12.txt)

No mismatch with the claimed table or with stored this-run logs for the commands above.

## findings
- Blank-grid onset is 256241 with exact period 384 and drift (4,-4). Translate certificate holds at 256241 and fails at 256240.
- Every seed in minimisers.txt has exactly its listed k, listed onset, certificate true at onset, and (when onset>0) onset-1 is not an onset.
- Own k=1 first-read enumeration recovers g(1)=555 with unique minimiser (1,0,1) and no earlier onset.
- Own k=2 first-read enumeration of all pairs whose non-zero first-reads fall in [0, 318+384) found no onset < 318. Combined with the certified 2-cell seed of onset 318, this is g(2)=318.
- Exhaustiveness argument: a seed is determined by first-read colours. For onset t < T, any non-zero first-read at time >= t+P cannot affect the first H384 period, so enumerating first-read colourings of cells visited in [0, T+P) with budget k is complete. For k=1 the single non-zero is first-read on the blank path; for k=2 the first is on the blank path and the second on the diverged 1-cell path. k=0/k=1 already cannot beat 318.
- Rebuilt A and B reproduce g(1), g(2), g(3) and the unique listed minimisers, K0=12 with 10 seeds, and K=11 at T=0 empty. Two k=5 B pieces reproduce the stored leaf counts; piece 12 reproduces the unique MIN at 174.

## caveats
- Own exhaustive completeness was carried out for k=1 and k=2 only. Completeness for k=3,4,5 is from rebuilt claim checkers A/B, not a second independent enumeration of those k.
- k=4 was not rerun. k=5 B was only two of forty pieces (p12 and p27); the full 542,179,718-leaf sum and the A 4-way k=5 split were not rerun.
- Persistence "forever" in the independent checks is the CERT.md translate certificate (sufficient condition) plus many recorded periods; the lemma itself was not re-proved.
- Novelty versus GLR/OEIS was not checked.

scope: Verified blank onset 256241/P=384, every listed minimiser (onset, k, onset-1), own exhaustive g(1) and no k=2 onset < 318, rebuilt A/B for k=1..3 and K0, and two k=5 B pieces; did not independently enumerate k=3..5 or rerun full k=4/k=5 A.
pass: true
