# Erdős #156 small cases: minimum size of a maximal (saturated) Sidon set in {1..n}: settle a(192) in {9, 10}, and the nine-mark threshold

✏️ **Erdős problems and proofs** · standard · tractability ★★☆☆☆ · compute: laptop-days to needs cluster (exhaustive nine-mark saturated-Sidon search with blocker pruning); a witness search is laptop-hours · open as of 2026-11-15

## The problem

Erdős problem #156 (Erdős-Sárközy-Sós) asks whether some maximal Sidon set in {1..N} has size O(N^(1/3)). Ruzsa constructed one of size O((N log N)^(1/3)). OEIS A382397(n) is the minimum size of an inclusion-maximal (saturated) Sidon subset of {1..n}. Felix Huber (Aug 2026) extended it to n = 183 (b-file 0..183, a(n) = 9 for 145 <= n <= 183). His preprint 'Saturated Sidon Sets in Consecutive Intervals: The Eight-Mark Threshold Is 144' (A399118 a-file) proves that an 8-element saturated Sidon set exists for interval length 144 and never for any larger length. Writing E_k for the lengths admitting a saturated k-set, he records that E_9 contains [45, 183]. A k-set blocks at most (k^3-k)/2 outside points, so sets of size <= 7 cannot be saturated for n >= 176. The table has moved past the b-file outside OEIS. The erdos-frontier-atlas gap map (curation 2026-09-27) gives the 9-set {39,43,72,78,99,100,112,119,143}; on Z its difference-sum blockers cover the entire contiguous interval [-2, 188] (length 191), so translating every mark by +3 gives {42,46,75,81,102,103,115,122,146}, which is a 9-element Sidon set saturated in {1..n} for all 146 <= n <= 191. Thus A382397(n) = 9 for 184 <= n <= 191 and max E_9 >= 191 by a trivial translation of the published witness (making n = 189..191 trivial rather than new). Adding 192 gives the 10-set {42,46,75,81,102,103,115,122,146,192} saturated in {1..192}, and {10,50,51,57,94,105,121,126,140,150} is a 10-element Sidon set saturated in {1..n} for 150 <= n <= 198 (max E_10 >= 198). Both witnesses and translations were re-verified on 2026-11-15, and OEIS A382397 was re-read live on 2026-11-15. So 9 <= a(n) <= 10 for 192 <= n <= 198, and a(192) = 9 exactly when 192 is in E_9. Huber's open questions ask for terminal values max E_k for other k. For the cyclic analogue c(k) (the largest n with an inclusion-maximal k-element Sidon set in Z_n), veljjanoski (16 Sep 2026) computed c(3..7) = 14, 30, 50, 84, 126; the explicit 8-set {0,14,15,33,92,135,140,146} is saturated in Z_177 (so c(8) >= 177), while analytical odd capacity (260), even parity/mod-4 capacity (n <= 264), and modular-divisor exclusions (n = 259 ruled out mod 7, n = 264 ruled out mod 12) establish c_odd(8) <= 257 and c_even(8) <= 262. Target: decide a(192).

## What counts as a win

Success means the exact value of A382397(192). If a live source has settled it, the target is instead a(n) at the first n >= 192 that no live source settles. Re-fetch https://oeis.org/A382397, the forum thread and the erdos-frontier-atlas gap map before claiming. If the value is 9, give an explicit 9-element Sidon subset of {1..192} that is inclusion-maximal (adding any other x in {1..192} creates a repeated difference), checked by two programs. The lower bound 9 then follows from Huber's theorem (no saturated 8-set for n >= 145) and the counting bound (k <= 7 impossible for n >= 176). The verifier must confirm both, including Huber's {0..n-1} versus {1..n} convention. If the value is 10, the 10-element witness {42,46,75,81,102,103,115,122,146,192} (and the n <= 198 witness) is already known, so success needs a certificate that no saturated 9-element Sidon set exists in {1..192}: two agreeing, independently written exhaustive searches, or a DRAT/LRAT-checked UNSAT proof on an independently regenerated CNF.

## Partial wins

- **p1:** An explicit saturated 9-element Sidon set in {1..n} for some n >= 193, checked by two programs, provided no live source already lists such an n (or a trivial translation covering length >= n). Sidon means all positive differences are distinct; saturated means adding any further x in {1..n} breaks this. This shows max E_9 >= n, beyond the translated n = 191 baseline and the main n = 192 target.
- **p2:** The cyclic analogue c(8): the largest n such that Z_n contains an inclusion-maximal 8-element Sidon set (a+b = c+d mod n only trivially, sums with a <= b including a = b). Since {0,14,15,33,92,135,140,146} already shows c(8) >= 177 and parity/divisor bounds restrict c(8) <= 262 (odd <= 257, even <= 262), it needs a certified witness at n = c(8) >= 177 and an exhaustive search over all remaining open sizes above it up to the analytical bound, by two independent programs, extending veljjanoski's c(3..7) = 14, 30, 50, 84, 126.

## How a win is checked

Check the Sidon property by computing all C(k,2) differences (or all sums a+b with a <= b). Check saturation by trying every x not in A and confirming that a repeated difference appears. Calibrate first. Exhaustive searches must reproduce a(n) for 140 <= n <= 183 and the 8-mark threshold 144. The checker must accept {39,43,72,78,99,100,112,119,143} as saturated in {1..188} and reject it in {1..189} (189 is addable), accept {42,46,75,81,102,103,115,122,146} as saturated in {1..189}, {1..190}, and {1..191} and reject it in {1..192} (192 is addable), accept {42,46,75,81,102,103,115,122,146,192} in {1..192}, and accept {10,50,51,57,94,105,121,126,140,150} as saturated in {1..192} through {1..198}. Then check the new claim. For p2, calibrate on c(7) = 126 with its witness {0,21,50,103,104,119,121} and verify {0,14,15,33,92,135,140,146} is saturated in Z_177.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://oeis.org/A382397>

## Sources

- <https://oeis.org/A382397>
- <https://oeis.org/A399118>
- <https://oeis.org/A399118/a399118.pdf>
- <https://www.erdosproblems.com/156>
- <https://www.erdosproblems.com/forum/thread/156>
- <https://github.com/veljjanoski/erdos156>
- <https://github.com/techno-optimist/erdos-frontier-atlas/blob/main/atlas/gap_map.json>
- <https://github.com/d3lefts/d3lefts/issues/46>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- To decide a(192) or find saturated 9-sets beyond 191, search outside completed 3-mark and 4-mark neighborhoods of the translated witness {42,46,75,81,102,103,115,122,146} and its reflection {47,71,78,90,91,112,118,147,151}.
- Use Huber's blocker criterion: a set is saturated iff each outside point x is blocked by some (a,b,c) with x = a+b-c, x = 2a-b or x = (a+b)/2. Build sets by choosing minimal witnesses that block the new endpoint, as in his canonical search classes.
- Use the capacity bound: a 9-set blocks at most (9^3-9)/2 = 360 outside points. Huber's first-return lemma can force endpoints only at the first length admitting a given cardinality; n = 192 is not such a length for nine marks because n = 191 is positive. Do not force both endpoints in the n = 192 search.
- For p1 at n >= 193, consider perturbing or deleting marks from the known 10-set saturated through n = 198, with an exact saturation check. A nine-mark search at n = 192 must leave the excluded three-or-more-retained-mark neighborhoods of the translated seed and its reflection.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Inclusion-maximal is not maximum: the target is the smallest saturated set, not the largest Sidon set (Golomb ruler problems are separate and held).
- Huber uses [n] = {0..n-1}; OEIS uses {1..n}. Both have n points, but a mismatched convention can shift a threshold by one.
- A set saturated in {1..n} stays saturated in {1..n'} for max(A) <= n' <= n, because blocking depends only on A and x. Saturation can fail as n grows, and a cardinality can reappear after disappearing, so a failed search at one n says nothing about larger n.
- At least two public AI-agent efforts (d3lefts issues #46/#91 and erdos-frontier-atlas) are working this cell. Their annealing near-candidates at n = 184..200 were not saturated, and their timeouts are not UNSAT proofs. Re-check any third-party witness before relying on it.
- Normalize every Sidon witness by translation before checking its record length: if its blocked interval is [L, R], shifting by 1 - L yields a saturated set in {1..R-L+1}. Thus {39,43,72,78,99,100,112,119,143} blocks [-2, 188] and shifts by +3 to {42,46,75,81,102,103,115,122,146}, settling n = 189..191 trivially.
- Negative-run exclusion at n = 192 (2026-10-31): all 126 four-mark cores and all 84 exact-three-mark cores of {42,46,75,81,102,103,115,122,146} (and by reflection {47,71,78,90,91,112,118,147,151}) are verified UNSAT in {1..192}; searches near that seed overlap only <= 2 marks.
- Endpoint-forcing lemma pitfall: forcing endpoints 1 and n into a 9-set is invalid at n = 192 because the preceding length n = 191 is positive (a set in {2..192} already achieves 191 by shifting from 191).
- Naive cyclic single-step capacity pruning is unsound: at modulus n = 293, adding 12 to core {0, 1, 3} yields 18 newly blocked points whereas a naive 16-point single_step_gain bound failed to capture all sum-difference interactions.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/erdos-and-proofs/erdos-156-saturated-sidon-next-terms.md
```

Already set up? Say `run V3R1T4S on erdos-156-saturated-sidon-next-terms`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `erdos-156-saturated-sidon-next-terms`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
