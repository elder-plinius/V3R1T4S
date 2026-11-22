# PREREG (frozen Sun Nov 22 09:24:14 UTC 2026)
target: mertens-function-exact-values-next-terms, partial win p1 only (RH-adjacent computational side-question; NOT an attempt on RH).
criterion (verbatim p1): "New terms of A084235 beyond a(17): the least k with |M(k)| = 2^18 (expected in (2.97e11, 3.31e11) from Hurst's extrema list) and, for more, 2^19 and 2^20, each from a full segmented Mobius sieve from 1, verified by a second independent run, at indices absent from OEIS on the day of claiming."
statistic/checker: attempts/extender/code/msieve.c full segmented Mobius sieve from 1 in blocks of 1e8 (per-block sum, max/min relative prefix); combine.py finds first block reaching |M|=2^n; msieve scan mode returns exact k.
validation gates (all must pass before any candidate is reported): block sums reproduce A084237 M(10^8)=1928, M(10^9)=-222, M(10^10)=-33722, M(10^11)=-87856 (data/A084237_b.txt); combine reproduces A084235 a(14..17) (data/A084235.txt); contrarian lens: independent trial-division mu checker agrees with sieve on random windows.
thresholds: exact integer equality only.
compute bound: N_max = 3.4e11 (blocks 0..3399), nice 19, timeout 900 s, 8 threads; resumable (block lines appended).
second independent run: required by p1 for any claim; if not done this session, the candidate stays unclaimed (claim level progress at most) and a panel is needed.
null_test: not needed because the result is an explicit integer checked by a deterministic sieve against table values (no search/statistical claim).
no baseline: deterministic exact-value target, step 3c does not apply.
