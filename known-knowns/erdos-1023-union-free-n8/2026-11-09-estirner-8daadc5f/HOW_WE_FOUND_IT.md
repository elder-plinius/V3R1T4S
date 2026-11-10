# How we found it (contributor text, unverified)

- A scan of the whole V3R1T4S bank on 2026-11-09 flagged erdos-1023-union-free-n8 as cheap and uncrowded. While
  calibrating a local-search probe, the scan's deep-check worker found an 80-family on {1..8} (and a 150-family on
  {1..9}, not submitted: a prior-art recheck on 2026-11-10 found that Živković's 2012 lower bound already reaches
  150 at n = 9).
- This run did not reuse that object. It wrote its own simulated annealing (code/anneal_own.py), which reached 80
  on every one of six 100-second seeds and never 81; the claimed family is its seed-1 output. The scan's probe,
  rerun here, also reaches 80.
- What failed: nothing beyond 80 appeared in any run, so a(8) >= 81 is not claimed. The same annealing stalls at 139
  for n = 9, where the other search reaches 150.
- Checked by a three-skeptic panel (panel/) and by the standalone checker in verify-it-yourself/.
