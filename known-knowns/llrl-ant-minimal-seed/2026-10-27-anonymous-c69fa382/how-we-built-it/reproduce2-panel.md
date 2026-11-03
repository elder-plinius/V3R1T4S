# REPRODUCE-EXHAUSTIVE skeptic verdict: LLRL ant g(6)=139 unique, target llrl-ant-minimal-seed (partial win p2)
context: fresh headless Grok Build CLI session (grok --prompt-file), started with no prior conversation in a copy of claim/; this file closes a prior same-directory session that re-ran all 400 B pieces then hit the wall-clock timeout before writing the verdict

## What I read
- `claim/CLAIM.md`, `claim/REPRODUCE.md`, `claim/TARGET_CRITERION.md` (partial win p2: g(6)=139, one minimiser).
- `claim/data/this-run/audit/B_merged_recomputed.txt` and `COVERAGE_AUDIT.md`: expected `pieces_done=400/400`, `leaves=5011329083`, `violation_lines=0`, `min_lines=1`, `flags=0`, one `BMIN`.
- `claim/data/this-run/send_back.txt` hash block: `B-results-digest cbd7913df3b309c1`.
- `claim/code/lcone4/merge_B.py` and `claim/code/lcone4/lcb_fast.c` (DONE line, MIN at depth T, VIOLATION at T-1, `flags` on a missing certificate, blank-grid line on stderr, split at `LCB_SPLITD` by `(splitc++) % NPIECES == wid`).
- `scratch/run_b.py`, `scratch/progress.log` (400 lines), `session.out` (prior session stopped before a verdict).
- Shipped A files compared below: `claim/data/this-run/box_done_A/p16.txt`, `claim/data/this-run/A/done/p27s2of4.txt`.

## What I ran
On-disk compare (this session, no re-execution of the 400): every `scratch/bout/b0000.txt`..`b0399.txt` against `claim/data/this-run/B/done/bXXXX.txt`, plus a sum of the DONE counters and the MIN cells sorted the way `merge_B.py` sorts them. `scratch/progress.log` was checked only as a second record of the prior run.

Spot re-runs, 3 workers, `nice -n 19`, `timeout 400`, existing `scratch/lcb` (not recompiled here):

```
LCB_SPLITD=60 timeout 400 nice -n 19 ./scratch/lcb LLRL 6 139 400 0
LCB_SPLITD=60 timeout 400 nice -n 19 ./scratch/lcb LLRL 6 139 400 159
LCB_SPLITD=60 timeout 400 nice -n 19 ./scratch/lcb LLRL 6 139 400 399
```

Key lines from those three processes (rc=0):

```
piece 0   dt=63.96s
DONE rule=LLRL K=6 T=139 wid=0/400 leaves=207800322 viol=0 mins=0 flags=0
piece 159 dt=11.70s
MIN t=139 p=229 k=6 cells: (0,1,3) (2,1,3) (0,2,2) (1,2,3) (1,4,3) (3,0,1)
DONE rule=LLRL K=6 T=139 wid=159/400 leaves=8367759 viol=0 mins=1 flags=0
piece 399 dt=12.53s
DONE rule=LLRL K=6 T=139 wid=399/400 leaves=10952920 viol=0 mins=0 flags=0
```

Each stderr was `blank: onset 256241 period 384`. Stdout of each piece matched both `scratch/bout/` and `claim/data/this-run/B/done/` byte for byte.

## Findings
- All 400 bout files `b0000.txt`..`b0399.txt` exist. Each whole file equals the shipped done file (stronger than the DONE line alone). DONE-line mismatches: 0. Missing pieces: 0.
- Sum of the 400 DONE lines: `leaves=5011329083`, `viol=0`, `mins=1`, `flags=0`.
- One MIN line, in piece 159: `MIN t=139 p=229 k=6 cells: (0,1,3) (2,1,3) (0,2,2) (1,2,3) (1,4,3) (3,0,1)`. Sorted cell tuple is the single seed `0,1,3;0,2,2;1,2,3;1,4,3;2,1,3;3,0,1`. VIOLATION lines: 0.
- Concatenated sha256 of `b0000.txt`..`b0399.txt` (bout and claim, same bytes) is `cbd7913df3b309c10ed8428baf12f7644c685c55e104270181a7c09a34ae62f3`. The first 16 hex digits are the shipped `B-results-digest cbd7913df3b309c1`.
- `scratch/progress.log` has 400 lines, piece ids 0..399 once each, every line `rc=0` and `match=1`. Recorded prior-run times include piece 0 at 58.26s, piece 159 at 10.89s (MIN line present), piece 399 at 10.93s. Sum of the 400 logged durations is 4592.3s.
- All 400 `scratch/bout/bXXXX.err` files are the single line `blank: onset 256241 period 384`.
- The three live spot re-runs reproduced the shipped DONE lines, and piece 159 reproduced the MIN line.
- A outputs already on disk: `scratch/aout/p16.txt` equals `claim/data/this-run/box_done_A/p16.txt`, including `RESULT split=16/40@8 ... best_onset=173 minimisers=1 nodes=28310602 tests=164900314 maxR=15 Dmin=238 flagged=0`. `scratch/aout/p27s2of4.txt` contains the shipped `# new best 140` and `SOL onset=140 ...` lines and stops before a RESULT line, so that A job has no RESULT to compare.

## Caveats
- This closing session verified the 400 piece logs already written by the prior session in this directory and re-ran 3 pieces on `scratch/lcb`. It did not launch another 400-piece sweep.
- `scratch/lcb` is the prior session's binary (21880 bytes, mtime 2026-10-27 19:18). `send_back.txt` records the home build as `gcc -O3 -march=native`. The spot re-runs used this binary as it stands. Their stdout matched the shipped pieces.
- `scratch/bout/time164.txt` is empty and `time164.err` is `env: ‘/usr/bin/time’: No such file or directory`. That pair is outside the `b0000`..`b0399` set.
- Checker A is only the two files in `scratch/aout/`. p16 finished and matched. p27s2of4 did not reach RESULT. Checker C and `code/indep/sim_llrl.py` were not run in this closing session. Coverage of the 400-way split is the `LCB_SPLITD=60` stripe in `lcb_fast.c` (`(splitc++) % 400 == wid` at depth 60); this session checked that the 400 outputs agree with the shipped logs.

scope: Verified all 400 on-disk checker-B piece logs against the shipped B done files (totals and the unique MIN) and re-ran pieces 0, 159, and 399 with scratch/lcb; A was compared only for the two aout files already present, and checker C was left unrun.

pass: true
