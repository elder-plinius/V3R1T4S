# Claim

**One sentence:** A364417(20), the number of stones-and-bones tilings of the (20,37)-benzel (Propp, Problem 16),
equals 225354012176304818, obtained by exact frontier-DP enumeration in two independently written programs
(code/benzZQ.c and code/benzB64.c, different line family and sweep order, overflow-checked 64-bit counts, sound
pruning only) that agree exactly; Program A (benzZQ.c) also reproduces every published term A364416(3..20) and
A364417(3..19).

target id: benzel-stones-and-bones-next-terms

status_source: https://oeis.org/A364416 (and https://oeis.org/A364417 for this cell)

## Success criterion (verbatim, V3R1T4S bank)
The exact next term A364416(21) or A364417(20), not in the DATA when re-fetched immediately before claiming. It must
come from two independent runs that agree exactly, and the same code must reproduce every published term of A364416
and A364417.

## Definition (Propp, arXiv:2206.06472 v4; text in data/propp_2206.06472_text.txt)
The (a,b)-benzel is the union of the unit hexagonal cells lying fully inside the hexagon with vertices aw+b, -aw^2-b,
aw^2+bw, -a-bw, a+bw^2, -aw-bw^2 (w = e^{2 pi i/3}); in the paper's coordinates, the cells whose centres (i,j,k) satisfy
-(a-1) <= j-i, k-j, i-k <= b-1 (Program A uses k = 1-i-j). Prototiles: right stone, left stone (three
mutually adjacent cells) and vertical, rising and falling bones (three collinear cells). T113 counts tilings with all
five. A364416(n) = T113(n,2n-4), A364417(n) = T113(n,2n-3), offset 3.

## Files
- code/benzZQ.c: Program A. Row sweep along lines i = const, frontier DP on a 64-bit covered mask, u64 counts with
  every addition overflow-checked (overflow is reported, the result is void), sound pruning (a state is dropped only
  if an exhaustive MRV exact-cover search proves the next K rows cannot be covered; node-limited searches keep the
  state). Env: BENZ_M (check every M-th cell), BENZ_CKPT / BENZ_CKPT_SEC (checkpoint file / period).
  Usage: benzZQ a b K.
- code/benzB64.c: Program B. Region built from the complex-plane hexagon vertices, tiles from Euclidean distances,
  sweep by line k = const ascending then i descending, own hash table, own feasibility search, u64 overflow-flagged
  counts. Usage: benzB64 a b Z every. code/benzB128.c is the same program with unsigned 128-bit counts (used for B's
  published-term runs n = 3..18).
- code/indep_check.py: memoized exact cover from the complex-plane definition (no transfer matrix), small n only.
- code/repro_matrix.py: compares every saved output with the OEIS DATA; last line RESULT PASS / FAIL.
- code/timed.sh: wrapper that wrote the .out/.err/.time files (its peak_rss_kb samples the `timeout` wrapper process,
  not the counter, so it is not a memory measurement).
- result/A_final/: Program A on (20,37). The run was stopped once (SIGTERM, exit 143, *.seg1.*) to change thread
  count and resumed from its own checkpoint at t=210 (A364417_n20.*: "resumed t=210", exit 0, overflow=0).
- result/A_ckpt_test/: checkpoint-resume test of Program A on (16,28): resumed run gives 6902094928308 = A364416(16).
- result/B_final/: Program B (benzB64) on (20,37), one uninterrupted run, exit 0, overflow 0.
- result/A_repro/, result/B_repro/: published-term runs (.out value, .err log with overflow flag, .time exit code).
- result/out_indep_n3_8.txt, out_indep_n9_11.txt: indep_check.py output for A364416/7/8, A364438, n = 3..11.
- data/: OEIS records, b-file and draft page as fetched (table below), and the text of Propp's paper.

## Table record (one plain curl GET each, User-Agent "V3R1T4S-run (research agent)", no retries)
| URL | fetch time (UTC) | HTTP | file | sha256 |
|---|---|---|---|---|
| https://oeis.org/search?q=id:A364417&fmt=text | 2026-11-02T05:49:16Z | 200 | data/A364417.txt | 8b0c55d787cc7a9d9f25ee5f1d615cd753597d1430ab09a8a86f6db07c5537f7 |
| https://oeis.org/search?q=id:A364416&fmt=text | 2026-11-02T05:49:16Z | 200 | data/A364416.txt | c2c41c8ea6debb93043582bf6483f925683f5433a1585fa8f4383ddc1330ea4c |
| https://oeis.org/A364417/b364417.txt | 2026-11-02T05:49:17Z | 200 | data/b364417.txt | 0cd8e248ff06ebaa7c81a15799f6c3e295cb640730f998885756996283f0568e |
| https://oeis.org/draft/A364417 | 2026-11-02T05:49:17Z | 200 | data/draft_A364417.html | 67cd983f39058d2e3c8b516bec45f540c53e00ba742e49205888ad3efc154946 |

Read from those files: A364417 DATA ends at a(19) = 20915277691567206 (%I A364417 #26 Apr 25 2024), the b-file ends at n = 19,
the draft page says "No pending changes"; A364416 DATA ends at a(20) = 87817595880192684. The string
225354012176304818 occurs in none of them.
