# REPRODUCE skeptic: A084235 a(18) = 330055906058

context: subagent (fresh executor, given only claim/)

Inputs read: claim/ only (CLAIM.md, candidate.md, TABLE_RECORD.md, REPRODUCE.md, result/a18.txt, data/, logs/; code/ only after my checker had finished), plus kit/RUN.md for the format. Work was done on a copy of claim/ in panel/continuations/2026-11-22-followup/reproduce_work/; claim/ was not modified. sha256 of the data/ files matches TABLE_RECORD.md.

## Definition (quoted)
data/A084235_page.html: "A084235 Smallest k such that |M(k)| = 2^n, where M(x) is Mertens's function A002321." OFFSET 0.
Mertens function: M(x) = sum_{n<=x} mu(n), with mu(n) = 0 if p^2 | n for some prime p, and otherwise (-1)^(number of prime factors of n).
Claimed object (result/a18.txt): "18 330055906058 262144 negative (M=-262144)".

## Method (my own code, written before reading code/)
- reproduce_work/mine/rsieve.c is a segmented Mobius sieve over 1..3.301e11, with segments of 2^20 and blocks of 1e8. Each block runs as one OpenMP task, with 6 threads at nice 19 (the box had about 6.7 GB free).
  - Every a[n] starts at 1. For each prime p <= sqrt(hi), a *= -p on the multiples of p and a = 0 on the multiples of p^2.
  - mu(n) = 0 if a = 0, and otherwise sign(a) * (|a| == n ? 1 : -1). This is valid because n/|a| is either 1 or a single prime greater than sqrt(hi).
- Per block it outputs the sum, the maximum prefix and the minimum prefix. The prefix is relative to the block start and runs over k in the block, not including the empty prefix.
- combine_mine.py finds the first block whose |M| range reaches 2^n, for n = 14..18. It then rescans that block exactly, k by k, with the same sieve, to find the first k where |M| >= 2^n. Since |M| changes by at most 1 per step, first |M| >= 2^n is the same as first |M| = 2^n.
- Brute-force validation, using trial factorisation in Python (brute.py): all 200 blocks of 1000 in 1..2e5 agree on sum, max and min. M(1e5) = -48. Also M(1e6) = 212, M(1e7) = 1037, M(1e8) = 1928.
- Full run: 3301 blocks, covering 1..330100000000, took 6 min 41 s wall time. Output is in blocks_full.txt, sha256 9605ed1d...12bc.

## Results (reproduce_work/mine/combine_mine_out.txt)
- Anchors (data/A084237_b.txt):
  - M(10^8) = 1928
  - M(10^9) = -222
  - M(10^10) = -33722
  - M(10^11) = -87856
  - All match.
- Earlier terms (data/A084235.txt):
  - a(14) = 2589994747 (M = -16384)
  - a(15) = 7613644886 (M = 32768)
  - a(16) = 37725066313 (M = -65536)
  - a(17) = 108500046711 (M = 131072)
  - All match.
- a(18):
  - The first block reaching |M| >= 262144 is block 3300, [330000000001, 330100000000], with M(330000000000) = -257128.
  - The exact scan gives the first hit at k = 330055906058, where M = -262144.
  - A direct scan to N = 330055906058 gives M(N) = -262144.
  - Over blocks 0..3299, which is all k <= 330000000000, max |M| = 257998 < 262144.
  - The scan of block 3300 shows that no k in [330000000001, 330055906057] has |M| >= 262144.
  - So no k < 330055906058 has |M(k)| = 262144. This is exhaustive over 1..N, not a sample.
- Agreement with the claimant's saved logs:
  - logs/msieve_out_blocks.txt (run 1, blocks of 1e8): all 3301 blocks 0..3300 agree on the sum.
    - Max and min also agree once the conventions are aligned. Run 1 counts the empty prefix 0 in max/min, and that convention difference is the whole difference in blocks 1166, 2683 and 2840.
    - That leaves 0 mismatches.
  - logs/msieve2_out_blocks_full.txt (run 2, blocks of 1.25e8, contiguous 0..2640): cumulative M agrees with mine at all 660 common boundaries, which are the multiples of 5e8. That gives 0 mismatches.
  - logs/*_combine.txt and logs/*_scans.txt give the same anchors, block indices, M-before-block values and first-hit k as I found.
- Claimant code (compiled from code/msieve.c and code/msieve2.c after my run; output in mine/author_code_out.txt):
  - msieve scan of block 3300 gives 330055906058, M = -262144.
  - msieve2 scan gives the same.
  - msieve2 reproduces the smaller known a(17) = 108500046711.
  - msieve gives M(1e9) = -222.
- Determinism: re-running my blocks 0..399 gave byte-identical output.

## Notes
- My checker uses the same sieve principle as the claimant's run 1 (product check), but I wrote it independently from the definition. It was validated against brute force, and it also agrees with run 2, which uses a different log-sum algorithm.
- The consistency checks at M(10^22), M(10^23) and M(2^74..75) are part of the full A084237 criterion, not the p1 partial win, and were not attempted. Judging whether p1 is satisfied is CRITERION's job.
- No mismatch, missing object or non-determinism was found.

pass: true
