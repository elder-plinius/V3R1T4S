# REPRODUCE panel — A384209(11) = 71

context: subagent (REPRODUCE skeptic, fresh context), working only on a copy of `claim/` (made with `cp -a`); did not read attempts/, REPORT or other panel files. Box shared (load avg 24–42 on 8 cores); all heavy jobs run under `nice -n 19`. Wall time 2026-11-03 02:56–04:54 EST.

## Definition (quoted, claim/data/A384209.txt)
> %N A384209 Maximum period for Game of Life on a simple graph with n vertices.
> %C A384209 The usual rules of Game of Life apply: A live vertex lives on to the next generation only if it has 2 or 3 living neighbors. A dead vertex comes alive if it has exactly 3 living neighbors.

So a(n) = max, over all simple n-vertex graphs (disconnected included) and all 2^n start states, of the length of the eventual cycle.

## My checker (written from the definition before reading any author code)
- `chk.c` (C, sha256 0a6064cb…b26c), reads graph6 on stdin. Per graph it parses graph6 itself (upper triangle, column-wise; state bit v = vertex v), computes the successor of **every** one of the 2^n states by walking a Gray code and updating neighbour counts packed as 4-bit nibbles (next = count==3 or (count==2 and live)), then runs an exact cycle search over the whole functional graph (every state is visited once; a walk that comes back to its own visit stamp gives cycle length = step − pos). The per-graph maximum is binned into a histogram, all graphs and the connected subset kept apart (connectivity worked out by BFS on bitmasks). Any graph with max ≥ 55 is printed together with one state on its max cycle. It shares no code with lifeA11.c, lifeB2.c or stepper.py. Its connectivity test is independent of geng -c.
- `sim.py` (pure Python, sha256 e3e0cd26…4984), a separate set-based simulator from the definition, used for the witnesses.
- Enumeration: `tools/geng`. sha256 checked: 75d1bf016a93b090ca471254605b735865162a864e4682c544df90a81e91f450 (matches the claim).

## What I re-ran (all of it exhaustive, no sampling)
1. n = 1..9: `tools/geng -q k | ./chk` → max = 1,1,1,1,2,4,8,14,27 (matches OEIS DATA). Graph counts 1,2,4,11,34,156,1044,12346,274668 (= A000088).
2. n = 10: all 12005168 graphs (11716571 connected) → max 46. My full per-graph-max histogram is **identical** to claim/result/A10_r0of1.txt hist_all.
3. n = 11: **all 64 residue classes** `seq 0 63 | nice -n 19 xargs -P 8 … tools/geng -q 11 r/64 | ./chk 55`. All 64 finished. Each output has exactly one summary line (64/64).
4. Witnesses with sim.py.

I did **not** re-run the author's lifeA11.c / lifeB2.c / combine.py. My own exhaustive run over ALL 11-vertex graphs, connected and disconnected, is a full independent recompute of a(11) directly from the definition, with no lcm step. Program B + combine are just an alternative route to the same number.

## Results (n = 11)
- Total graphs = **1018997864** (= A000088(11)). Connected = **1006700565** (= A001349(11)). Both summed over the 64 residues.
- **Maximum cycle length = 71.** Exactly 2 graphs reach it, both connected:
  - J?qrdjivb}_ (state 752 lies on the 71-cycle)
  - JCpbdo}ttv_ (state 1728 lies on the 71-cycle)
- Next values: 61 (JCpbbqkVt^_, JCRbd\]ms~_), 60 (JCxvEyz\~\_), 59 (JCQbUemnm}_, J?befRVmvZ_). This matches the claim's "next best" statement.
- Top of the histogram (value:all/connected): 49:32/32 50:34/34 51:12/12 52:19/19 53:11/11 54:7/7 55:4/4 56:5/5 59:2/2 60:1/1 61:2/2 71:2/2
  For every value ≥ 49 the all-graph count equals the connected count, so no disconnected graph reaches 49 (the claim says the disconnected max is ≤ 46). This is consistent.
- Per-residue histograms: for all 64 residues my histogram is **identical** to hist_all in claim/result/A11_r{r}of64.txt (0 diffs). That is an independent full recompute agreeing with the saved Program A output, residue by residue.
- Determinism: the n = 10 and all 64 n = 11 per-residue histograms agree exactly with the author's independently produced files. Every residue output is complete (one summary line each).
- Witness simulation (sim.py, from the definition):
  - J?qrdjivb}_ 752: n=11, 31 edges, preperiod 0, cycle 71
  - JCpbdo}ttv_ 1728: n=11, 31 edges, preperiod 0, cycle 71
  - HCZJtzm 47: cycle 27 (OEIS n = 9 example)
- Saved claim/result/B_order11.txt (not re-run by me): 1006700565 connected, max_cycle 71. This is consistent with my connected subset.

## Verdict
Every property checked by a full exhaustive recompute: graph counts, a(1..10), a(11) = 71, both witnesses, and the next-best values. No mismatch, nothing missing, no non-determinism.

pass: true
