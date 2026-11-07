# How we found it (contributor text, unverified)

**Brief.** Charter quarry 11 (added 2026-10-15) took Justin Sun Prize catalog problems; this run (2026-10-15-0724)
took JSP-000550 = Erdős Problem 677: must M(m, k) = lcm(m+1, …, m+k) differ from M(n, k) whenever m ≥ n + k? The
formal statement was frozen from google-deepmind/formal-conjectures. The pre-registration
(`how-we-built-it/PREREG.md`, frozen 2026-10-15T07:28:24Z before any attack program ran) said a full win needs a
kernel-checked proof or counterexample, and that a range verification counts as a partial win only if every (n, k) in
the stated range is covered with no cap on m, with the certificate saved. The problem page itself could not be read
from the contributor's machine that day (proxy 403).

**What worked.** Two lenses ran in parallel on the same brief.
- *structure-prover* proved on paper that a counterexample's later block contains no prime and has all prime powers
  at most n + k, and that m + k ≤ c_k·(n + k) with c_k = (lcm(1..k)/k)^(1/k) < 2.826 (Rosser–Schoenfeld). With
  n ≤ C·k and Schoenfeld's 1976 prime-in-short-interval theorem this caps m below 2010760 as long as
  2.826·(C + 1) < 16597, i.e. up to C = 5871. `range_nCk.py` then enumerates every prime-free block below that cap,
  pins the candidate n + k by the block's largest prime powers and primes, and compares lcms in exact integers. It
  was validated first at C = 1000 against a brute-force pair list (79844 pairs, m ≤ 20000) and an end-to-end brute
  force for n + k ≤ 400. The C = 5871 run finished at 08:07 (lens notes): 1449175 prime-free pairs, 7567449
  candidates, 7567420 exact comparisons, no counterexample. This is the object of this package.
- *signature-search* proved a similar size lemma independently and verified, with unpanelled computations, no
  counterexample with n + k ≤ 10^8 (any k, any m) and none with k ≤ 22, n ≤ 10^494. It also found the only two
  near-misses below 10^8 with equal large-prime parts, (k, n, m) = (3, 4, 13) and (4, 18, 53); the exact judge
  rejects both, and `verify-it-yourself/run_checks.sh` repeats that as a sanity check. These lens results are not
  part of this claim.

**What failed.** The full statement resisted: for every k ≥ 3 the lcm equation has genuine solutions with
overlapping blocks (lcm(3,4,5) = lcm(4,5,6)), so only disjointness rules them out and any proof needs a global
Diophantine argument for each k. k = 3 and k = 4 reduce to Thue equations (solved with PARI/GP, not kernel-checked);
k = 5 already reduces to seven genus-2 curves without elliptic factors, beyond what PARI/GP could do. The first C = 5871 launch stopped at a guard written
for C = 1000 (`assert M1 < 2010760`); the guard was replaced by the cap the Schoenfeld step actually gives and the
run was restarted, with the C = 1000 behaviour unchanged.

**Panel.** On 2026-10-15 REPRODUCE (reran the program, 133.8 s, byte-identical output; its own exact C checker over
all prime-free blocks with m ≤ 2010759: 19,745,817 pairs, 0 equalities) and CRITERION (reran it, 134 s, byte-identical;
an independent Python check for k ≤ 147 using neither cited paper) passed. NOVELTY could not read erdosproblems.com
and returned PENDING STATUS CHECK (`panel/novelty_round1_pending.md`), so the gate wrote PROMISING. After the owner
widened the environment's network access on 2026-10-23, a fresh NOVELTY skeptic read the problem page, its forum and
the other sources on 2026-10-24, found no recorded range verification and passed; the gate's second round
(2026-10-24T08:47:19Z) wrote CONFIRMED_PARTIAL (`panel/gate.md`).
