context: subagent

# Reproduce — A204371(37) = 4403

## Definition used (quoted)

From how-we-built-it/TARGET_CRITERION.md (bank success criterion, verbatim in part):

> The exact value of A334497(37) or A204371(37) (or any later term), from an exhaustive search over all 2^n states, or over all rotation orbits with the rotation factor accounted for. It must be run by two independent implementations that agree. Both must reproduce A334497(1..24) and A204371(1..30) exactly, and both must report their values for A334497(25..30). [...] A witness state on the maximal cycle must be given, so a skeptic can confirm the cycle length by direct iteration. Bit order must follow the Wolfram rule-number convention, which the small-n reproduction checks.

The packaged object (object/a204371_37.txt) claims n=37, rule=110, max_period=4403, witness=0x1c7dbbb23e, under that convention: cell 0 is the least-significant bit of the state word; for cell i, L = cell (i-1) mod n, C = cell i, R = cell (i+1) mod n; neighborhood index idx = (L<<2)|(C<<1)|R; the next bit is (rule >> idx) & 1. The eventual period of a start is the length of the cycle reached after any transient (not the length of the transient). A204371(n) is the maximum of that quantity over all 2^n cyclic configurations of Rule 110.

This review wrote its own ring iterator and exhaustive search from that definition, before reading how-we-built-it/impl1/maxcycle.c or impl2/maxcycle.c, and did not use verify-it-yourself/check_period.py.

## Witness period (independent iterator)

From witness 0x1c7dbbb23e at width 37 under Rule 110:

- first return is at step 4403, and the state then is again 0x1c7dbbb23e
- 4403 = 7 * 17 * 37, so the positive divisors are 1, 7, 17, 37, 119, 259, 629, 4403
- after every proper divisor of steps, the state is not the start: 1 → 0x1647eefb23, 7 → 0x47d0fb23b, 17 → 0x11f43ecbec, 37 → 0x1f43b23ec8, 119 → 0x16eec8fb8f, 259 → 0x1b8fb23f77, 629 → 0x1d91f647ce
- the 4403 states on the claimed cycle are pairwise distinct

So the eventual period of the packaged witness is exactly 4403.

A single live cell (start 0x1) reaches a cycle of period 4403 after a transient of 192 steps, and the first state on that cycle is 0x1c7dbbb23e, the packaged witness. That period equals the live OEIS term A180001(37)=4403 (b-file https://oeis.org/A180001/b180001.txt, fetched 2026-11-18 20:39:20 ET, America/New_York, UTC-5). The witness therefore lies on the single-cell cycle; the exhaustive claim is that nothing longer exists.

## Independent exhaustive search at small width

A separate program walked the full functional graph with no rotation or reflection folding (each of the 2^n states is marked, each cycle is measured once from the eventual image). Compared with live OEIS b-files fetched at the same time as above (https://oeis.org/A204371/b204371.txt, https://oeis.org/A334497/b334497.txt):

- Rule 110, n=1..22: maximum periods 1, 1, 1, 2, 1, 9, 14, 16, 7, 25, 110, 18, 351, 91, 295, 32, 578, 81, 285, 240, 630, 462 — all equal A204371(n)
- Rule 30, n=1..20: maximum periods 1, 1, 1, 8, 5, 1, 63, 40, 171, 15, 154, 102, 832, 1428, 1455, 6016, 10846, 2844, 3705, 6150 — all equal A334497(n)

The bit-order convention and the eventual-period definition therefore match OEIS.

## Source audit of the two shipped implementations

Both programs use the same Wolfram step as the definition above (cell 0 = LSB, L=i-1, R=i+1, idx=(L<<2)|(C<<1)|R). Neither reduces by reflection.

how-we-built-it/impl1/maxcycle.c marks every rotation of a newly visited state in a 1-bit-per-state bitset, then follows the trajectory until it hits an already-marked state. If that state is a rotation of a state on the current walk, a new cycle has been found; otherwise the walk is a transient into a cycle already measured. Each rotation orbit is therefore taken to its eventual image and each cycle is walked once. If f^k(s) = rot_r(s), the configuration period is k when r=0 and k * n / gcd(r, n) otherwise; r is recomputed by actually iterating k steps from s, which is the correct conversion from a rotation-orbit return to a configuration period. A direct first-return check is then applied to the reported witness. No mirror images are marked.

how-we-built-it/impl2/maxcycle.c is a 3-colour (white / grey / black) walk with two bits per state and no rotation folding. A step onto grey closes a cycle whose period is the exact stack distance (no orbit-period conversion). A step onto black is a transient into a finished region and is not counted again. The walk stack is then painted black, so each cycle is measured once. A direct first-return check is applied to the reported witness.

The two search methods are independent of each other. No fault was found in either against the target's checks.

## Rebuild and re-run (not n=37)

Both programs were recompiled from the shipped sources with the same command as how-we-built-it/build.sh (`cc -O3 -march=native`). Binaries were kept outside the package. Jobs ran under nice -n 19, one at a time (one worker), and stayed under the 8 GiB cap and under half of available RAM. n=37 was not run (impl1 would need a 16 GiB bitset and impl2 a 32 GiB colour array; this machine has 15 GiB).

Rebuilt binaries vs the independent exhaustive search (periods and witnesses both agreed):

- Rule 110, n=1..22: both implementations returned the same max_period and the same witness as the independent census at every width, hence also A204371(1..22)
- Rule 30, n=1..16 and n=18, 20: both implementations likewise agreed with the independent census and with A334497 at every width run (including A334497(16)=6016, (18)=2844, (20)=6150)

Held-out width, chosen here, not the package's n=31 check: Rule 110, n=32. Live OEIS A204371(32)=2368.

- impl1: max_period=2368 witness=0xfb41f672 time_sec=62.6172, peak RSS 525884 kB, bitset 536870912 B; wall 20:42:12–20:43:15 ET (America/New_York, UTC-5)
- impl2: max_period=2368 witness=0xfb41f672 time_sec=710.8919, peak RSS 1050228 kB, colour 1073741824 B; wall 20:43:15–20:55:06 ET (America/New_York, UTC-5)

The independent iterator confirms that witness 0xfb41f672 has first return 2368, returns at no proper divisor of 2368, and has 2368 distinct states on the cycle.

## Packaged n=37 files

object/a204371_37.txt, how-we-built-it/results/result_impl1.txt, result_impl2.txt, witness_impl1.txt and witness_impl2.txt all record the same term: rule=110 n=37 max_period=4403 witness=0x1c7dbbb23e. The n=37 census itself was not repeated in this review.

## Verdict

The packaged witness has period exactly 4403. Both shipped implementations implement a correct exhaustive eventual-period search under the required bit order, without reflection reduction, and with a correct rotation-orbit conversion in impl1. Fresh rebuilds agree with an independent brute-force census and with live OEIS on Rule 110 n=1..22 and on several Rule 30 widths, and both return the listed term A204371(32)=2368 on a held-out width. This is not a sample of the 2^37 space offered as a census; the 2^37 run was not repeated here. On the checks above, the object reproduces.

pass: true
