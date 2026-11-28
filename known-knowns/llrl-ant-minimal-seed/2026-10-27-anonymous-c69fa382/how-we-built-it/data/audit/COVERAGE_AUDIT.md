# Coverage audit of home llrl-k6 work (2026-10-27)

Source: data/incoming/llrl-k6-work.tar (sha256 fd345e9817febb851fc7b749b305ee43904f03b01411b945923263331c8a6bd2)
send_back: data/incoming/send_back.txt (sha256 528702e3ebd07b6fba31c08131ff2f17879f9821a02b4b36f33121f2f7a54340)

## Checker A
- jobs_A.sh: 84 jobs; work/A/done: 84 .txt; missing none; extras none.
- Every send_back A sub-piece line (84/84): nodes and NONE/best_onset match the corresponding done file RESULT.
- Independent merge_A.py: pieces_covered=40/40 complete=yes tmax=140 min_onset=139 n_minimisers=1
  MINIMISER 0,1,3;0,2,2;1,2,3;1,4,3;2,1,3;3,0,1  — identical to send_back.
- A-results-digest recomputed: bc8fc1f6719817ee (send_back: bc8fc1f6719817ee) — MATCH.
- SOL lines across box done_A + home done: onset 139 (p22s2of4, unique), 140 (p27s2of4), 173 (p16), 174 (p21).
- Box pieces 0-5,7-13,15-21,28: all RESULT at K=6 /40@8 with NONE onset<=174 or best_onset 173/174.
  TMAX=174 is strictly stronger than 140: a finished NONE<=174 piece cannot hide an onset-139 seed.
  best-cut starts at best=TMAX+1; for NONE pieces best never drops, so no pruning of better seeds.
- Home pieces 6,14,22-27,29-39: all finished at TMAX=140 (84 sub-pieces).

## Checker B
- work/B_T139/done: 400 .txt; leaf sum 5011329083; viol=0; mins=1; flags=0.
- Independent merge_B.py: identical to send_back (complete=yes, same leaves, BMIN same unique seed).
- B-results-digest recomputed: cbd7913df3b309c1 (send_back: cbd7913df3b309c1) — MATCH.
- B partition is independent of A's 40-piece split (400 pieces at LCB_SPLITD=60); B alone covers the full space at T=139.
- VIOLATION = onset <= 138; zero such lines => g(6) >= 139. One MIN at T=139 => g(6) = 139 unique.

## Verdict
Exhaustiveness holds: combined A (box TMAX=174 + home TMAX=140) covers all 40 pieces; B independently covers all seeds at T=139; A and B agree on the unique minimiser; digests match send_back.
