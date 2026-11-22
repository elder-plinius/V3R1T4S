# CRITERION skeptic: mertens-function-exact-values-next-terms, claim A084235(18) = 330055906058

context: subagent (fresh executor, given only claim/)

Read: claim/ (CLAIM.md, REPRODUCE.md, TABLE_RECORD.md, candidate.md, result/a18.txt, code/, data/, logs/), kit format, and the bank entry. I did not read the run report, LOG, other panel files, dossiers or private/.

## Criterion text (verbatim, bank/targets.json)

success_criterion: "Success means a new term of A084237 (n = 24) or A084236 (n >= 76), at an index absent from the live OEIS entry and b-file when re-fetched immediately before claiming, computed twice with different algorithm parameters or different code and agreeing exactly. The claim states the exact integer, the code, the run logs, and a consistency check: the same code reproduces M(10^22), M(10^23), M(2^74) and M(2^75). The skeptic reproduces at least one smaller known value with the claimant's code and re-runs the new value if compute allows. Direction: a new term (higher index)."

partial win p1: "New terms of A084235 beyond a(17): the least k with |M(k)| = 2^18 (expected in (2.97e11, 3.31e11) from Hurst's extrema list) and, for more, 2^19 and 2^20, each from a full segmented Mobius sieve from 1, verified by a second independent run, at indices absent from OEIS on the day of claiming."

## Full criterion
Not met. The claim gives no term of A084237 or A084236. Only p1 is at issue.

## p1, clause by clause
1. **"New terms of A084235 beyond a(17)": met.** The OEIS page (data/A084235_page.html) uses offset 0 with a(0)=1. Its data run 1, 5, ..., a(17)=108500046711, with keyword "more". The offset fix (Mar 2026), which the bank names as a pitfall, matches the claim's indexing: n=18 means |M| = 262144 = 2^18. Both codes also reproduce a(14)..a(17) under this indexing (logs/msieve_out_scans.txt, logs/msieve2_out_scans.txt).
2. **"the least k with |M(k)| = 2^18": met.** The hidden quantifier is "least". It is covered because:
   - Each run reports, for every block, the block sum plus the max and min prefix. Both combiners (code/combine.py, code/combine2.py) mark the first block where M_before + maxprefix >= 2^18 or M_before + minprefix <= -2^18. So no earlier block reaches |M| >= 2^18, in either sign.
   - A scan from the start of that block then returns the first exact hit.
   - M changes by at most 1 per step, so the first k with |M| >= 2^18 has |M| = 2^18.
   - Run 1 (blocks of 1e8) and run 2 (blocks of 1.25e8) place the crossing in different block grids. Both give first k = 330055906058 with M = -262144.
   - I re-ran both combiners on the shipped block logs, and their output matches logs/*_combine.txt exactly.
3. **"expected in (2.97e11, 3.31e11)": consistent.** 3.30056e11 is inside the interval. This is a plausibility note, not a requirement.
4. **"for more, 2^19 and 2^20": optional.** These are extra terms, not a conjunct. One new term is enough for p1. 2^19 is not reached by 3.4e11, as expected.
5. **"each from a full segmented Mobius sieve from 1": met by both runs.**
   - Run 1: blocks 0..3399, covering 1..3.4e11.
   - Run 2: contiguous blocks 0..2640, covering 1..3.30125e11, which is past k.
   - Neither run seeds from a published M value. Each starts from k = 1, and the scan's M0 comes from that run's own block sums.
6. **"verified by a second independent run": met, with a caveat.** Run 2 uses different code:
   - Its square-free sign is set by a log-sum test (12·log2 n threshold) rather than run 1's product check.
   - Segment sizes differ (2^15 vs 2^17), block sizes differ (1.25e8 vs 1e8), and the combiner is separate.
   - Their prefix sums agree at all 660 common grid points up to 3.3e11, with 0 mismatches (logs/grid_compare.txt).
   - I checked run 2's log-sum test. At n ~ 3e11, the margin is about 150 units (1/16 bit each), well above the worst-case rounding of about 6 units. The uint16 accumulator stays well below overflow.
   - Caveat: both codes share the same sieve skeleton, author and machine. The bank's verification_method suggests "re-run on separate hardware", but that is not in the p1 text. I judge "independent" met in the literal sense: a different algorithm for mu, run separately from 1.
7. **"at indices absent from OEIS on the day of claiming": met for A084235.**
   - TABLE_RECORD.md records fetches of the A084235 page and b-file on 2026-11-22, 09:23 UTC (03:23 CST), plus a re-fetch at 16:56 UTC (10:56 CST). The sha256 is unchanged, and the data ends at a(17).
   - The shipped data/A084235.txt matches the recorded sha256 e40ebda7...
   - Note: the "b-file" is synthesized from the entry (that is the OEIS b-file for this sequence), so it is the same data as the page.
   - Hidden-quantifier flag: the page's FORMULA says a(n) = A051402(2^n). If the A051402 b-file ever listed index 262144, the value would already be "in OEIS". The claim package has no A051402 fetch. This is NOVELTY's job to confirm; candidate.md lists it as outstanding. I do not fail on it, because p1 names A084235 indices.
8. **Consistency checks (by analogy with the full criterion):**
   - Both codes reproduce M(10^9), M(10^10) and M(10^11) from data/A084237_b.txt. Run 1 also reproduces M(10^8).
   - Both reproduce A084235 a(14)..a(17).
   - The sympy trial-factorisation spot check agrees on 9 blocks of 1000 near 3e11, plus M(30) (logs/check_windows_out.txt).

## Null model / independent re-run (scratch: panel/continuations/2026-11-22-followup/criterion_work/)
- I wrote a third mu method (criterion_work/xchk.c): a residual-division sieve that divides out each prime and flips sign when the leftover cofactor exceeds 1.
- I scanned [330000000001, 330055906058] from M(3.3e11) = -257128, the value both full runs agree on. Result: first |M| = 262144 at k = 330055906058, with M = -262144. The window's max is -254152 and its min is -262144, reached only at k, so there is no earlier hit of either sign in the window.
- Sanity check on a known value: the same tool scanned from 7500000001 with M0 = 17705 (run 2's value) and gave 7613644886 = a(15), matching OEIS.
- This check depends on M(3.3e11) from the claimant's runs. I did not re-sieve from 1 myself; the "least" claim before 3.3e11 rests on the two shipped full runs.

## Stretched definitions checked
- Exact equality vs ≥: equivalent here (unit steps).
- Sign: either sign counts, and the hit is negative. That is fine, since the definition uses |M|.
- Off-by-one in the block/scan boundary: blocks are [bB+1, (b+1)B]. The scan starts at bB+1 with M0 = M(bB). This is consistent in both codes.
- Not subsumed: no full win is claimed. p1 is an enumerated partial win, and a(18) is a new index, not a re-derivation of a(17).

confirmed_scope: Two separately written full segmented Mobius sieves from k = 1 (to 3.4e11 and 3.30125e11) agree that the least k with |M(k)| = 2^18 is 330055906058, where M(k) = -262144, and A084235 on OEIS ended at a(17) when re-fetched on 2026-11-22. This meets bank partial win p1 for a(18) only (not 2^19 or 2^20, and not the full criterion), with novelty against A051402 and outside sources left to the NOVELTY skeptic.

pass: true
