# Criterion skeptic report: q171-1, qubit cell [[171,1]] (bank entry codetables-qubit-upper-bounds-n101-256)
context: subagent (Claude Code on the owner's PC, fresh context, Sonnet)
confirmed_scope: No qubit stabilizer code [[171,1,d]] with d >= 56 exists (exact integer Farkas certificates of the quantum weight-enumerator LP with Rains shadow rows verify for d = 56 and for the live bound d = 57 under the shipped checker and my own re-implementation), so the live codetables.de upper bound 57 for [[171,1]] (re-fetched 2026-10-17T00:30:36Z, HTTP 200, byte-identical to the claim-time page) falls to at most 55, which the live table's propagation closure (R1-R3, 57) does not already give; nothing is confirmed about the lower bound 34, the true LP optimum, or any other cell.

## Verdict

The full success criterion is met literally, clause by clause (table below). I found no hidden quantifier or stretched definition that changes this. The one caveat that needed a decision (the k=0 cell) is discussed under "Hunt".

## What I read (only claim/)

CLAIM.md, REPRODUCE.md, check/check_cert.py, check/parse_table.py, check/propagate.py, check/propagation_check.txt, check/checker_output.txt, data/QECC_q4_n171_k1_claimtime.html, data/TROPHY_CASE_pinned_9b1d444.md (a results list of other families; no quantum-code row; rows 38-42 show the repository already files LP-certificate upper bounds as "new only as a table entry"), data/qubit_table_full_n1-256.html (parsed, not read line by line), result/cert_171_1_56_sh.json, result/cert_171_1_57_sh.json (structure and checks). No other folder opened, no web search, no literature search.

## What I fetched (live table; each page once, curl default client, no retries)

| what | URL | UTC start | HTTP | value found |
|---|---|---|---|---|
| cell page | https://codetables.de/QECC.php?q=4&n=171&k=1 | 2026-10-17T00:30:36Z | 200 (1523 bytes) | lower bound 34, upper bound 57, "Last change: 10.06.2024"; sha256 c92ff9802e79dc6a595112491da66a27a8bb2f2fec0d11465d8d55477287c20c; `cmp` says byte-identical to data/QECC_q4_n171_k1_claimtime.html |
| full qubit table | https://www.codetables.de/QECC/Tables_color.php?q=4&n0=1&n1=256&k0=0&k1=256 | 2026-10-17T00:30:45Z (done 00:31:21Z) | 200 (5547032 bytes) | sha256 26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6; `cmp` says byte-identical to data/qubit_table_full_n1-256.html |

No 401/403/429/503, no challenge page. So the saved table in the package is the live table as of my fetch, and the live upper bound at (171,1) is 57 (the claimant's own fetch times, 2026-10-16T20:55:59Z and 21:01:19Z, are only as stated in CLAIM.md; my byte-identical re-fetch makes them moot).

## What I ran

1. Shipped checker, `python -I check/check_cert.py result/cert_171_1_5{6,7}_sh.json` (Python 3.14.4, 2026-10-17T00:25:25Z):
   `VERIFIED [[171,1,56]] shadow=True: value=1827 digits, max column coefficient <= 0, 55+2+56 multipliers` (exit 0);
   `VERIFIED [[171,1,57]] shadow=True: value=2066 digits, max column coefficient <= 0, 56+2+57 multipliers` (exit 0). Matches check/checker_output.txt.
   File hashes (sha256sum): result/cert_171_1_56_sh.json 3d36de83e6a4a4c5a48ec948cbe1026275636edd8bae75ac4aaa7deb0f8b14e6; result/cert_171_1_57_sh.json 6ca15493014ccafdecb1058f1c7a5bfd1dbd6f626d4348c865c21166b400ae32; check/check_cert.py 3c4e89d40124f80751290db7b9190387cdbd6590d4fd48f25ac9c7e996cf3fe4.
2. My own checker work/my_verify.py (2026-10-17T00:31:48Z). It does not import the shipped one. It builds every LP row explicitly (E0, E1, Q_j for j<d, G_j for j>=d, H_j for all j), takes the Krawtchouk numbers from polynomial expansion of (1+3y)^(n-i)(1-y)^i instead of the binomial sum, combines the rows with the certificate multipliers, and tests "every column <= 0 and right-hand side > 0". Both certificates: VERIFIED. d=56 uses 55 Q multipliers (1..55), 2 G multipliers (j = 58, 59), 56 H multipliers (j in 0..61), right-hand side 1827 digits, exactly 1 zero column. d=57 uses 56 Q (1..56), 2 G (j = 59, 60), 57 H (j in 0..62), 2066 digits. The two Krawtchouk constructions agree on all 29584 entries at n=171 (0 mismatches), and the orthogonality identity holds on sampled (j,l).
3. Negative controls (work/mutation_tests.py): the original d=56 certificate is VERIFIED by both checkers; 9 corrupted copies (drop one shadow multiplier, negate one, drop one G multiplier, perturb u_Q[30] by 1, relabel as d=55, push the value non-positive, set the shadow flag false with multipliers kept, remove all shadow multipliers, relabel k=2) are all FAILED by both. So the check is not vacuous, and this certificate depends on its shadow multipliers.
4. Brute-force validation of the LP rows on real stabilizer codes (work/bf_check.py, 2026-10-17T00:32:54Z): 432 random stabilizer codes, n = 3..7, k = 0..3 (including 5 impure codes with k>=1 and the [[5,1,3]] code). For each, enumerated S, N = S^perp and the shadow {p : <p,s> = wt(s) mod 2 for all s in S} by brute force; verified B_j = 2^-(n-k) sum_i K_j(i) A_i, Sh_j = 2^-(n-k) sum_i (-1)^i K_j(i) A_i (the shadow enumerator is exactly this and is >= 0), A_0 = 1, sum A = 2^(n-k), A_j = B_j for 1<=j<d, A_j <= B_j for j>=d. All passed. So each row the certificate may use is a true necessary condition for an actual stabilizer code, pure or impure.
5. Null model: my own float LP (work/lp_scan.py; scipy HiGHS, orthonormally scaled) built from the same rows, run for k=1, n = 5..57 (2026-10-17T00:39:49Z): the largest d for which the LP with shadow rows is feasible equals the table upper bound in 53 of 53 rows, never falls below a known-code lower bound, and without the shadow rows the bound is weaker in 45 of 53 rows. So the LP as formulated reproduces the table's own method (Rains LP) and does not exclude existing codes. For n >= 58 HiGHS reports numerical difficulty (status 4) in the shadow LP in places, so I do not use floats above n=57 and I did not try to solve the n=171 LP in floating point (the quantities that matter near weight 56 are far below double-precision tolerance there). At n=171 the proof is the exact certificate only.
6. Propagation (work/myparse.py, work/my_prop.py, plus the claimant's scripts): my own regex parse finds 33152 cells (all 33152 anchors), 32896 with k>=1. Closure over the live table at (171,1): 57 under R1 (k>=2 only), R2 (n+1,k), R3 (n-1,k+1)+1; still 57 when I add the conservative R4 d(n,k) <= d(n-1,k)+1. Neighbours: (172,1) = [34,58], (170,2) = [33,57], (170,1) = [33,57]; R2 gives 58, R3 gives 58, R4 gives 58. The claimant's `parse_table.py` + `propagate.py` print `[34, 57] 57`. Note: the table is not propagation-closed for n>100 (1075 cells have live bound above their implied bound, 1072 of them at n>100), but (171,1) is not one of them.
7. Consistency with lower bounds: the largest lower bound among cells with n<=171, k>=1 (each would force d(171,1) >= that value) is 34 at (171,1) itself; no live code contradicts an upper bound of 55.

## Criterion, clause by clause

- "some qubit cell (n,k) with 101 <= n <= 256": (171,1), qubit table (q=4). Met.
- "no [[n,k,d]] stabilizer code exists for d equal to the live table upper bound (re-fetched live)": live upper bound 57 (re-fetched by me, see above). result/cert_171_1_57_sh.json is exactly that statement, VERIFIED twice. Met literally. result/cert_171_1_56_sh.json is stronger (d >= 56 excluded; any code with distance >= 56 satisfies the d=56 rows, because equalities for j<56 imply the inequalities of any smaller d).
- "lowering it by at least 1": 57 -> at most 56 (literal certificate), 57 -> at most 55 (d=56 certificate). Met.
- "exact rational infeasibility certificate (Farkas dual) of the quantum weight-enumerator LP (MacWilliams link, A_i <= B_i, A_i = B_i for 0<i<d, nonnegativity, plus shadow nonnegativity where used)": the rows are exactly those, plus A_0 = 1 and sum A_i = 2^(n-k) (B_0 = 1, the normalisation of the MacWilliams link). Integer multipliers on rows scaled by 2^(n-k). Only validated rows are used (step 4). Met.
- "checked in exact integer arithmetic by an independent script": check/check_cert.py (standard library, integers only, separate from the unshipped solver) and my second implementation, both pass; corrupted certificates fail. Met.
- "NOT already implied by the standard propagation rules applied to other live cells": closure 57 > 55, confirmed on an independent parse of the byte-identical live table, with and without an extra puncturing rule. Met.

## Hunt: hidden quantifiers, stretched definitions, null models

- Meaning of d: the rows hold for every code with minimum distance >= d (not only exactly d), pure or impure (A_j = B_j, not A_j = 0). Tested on impure codes. No gap.
- Real relaxation: infeasibility over nonnegative reals excludes integer weight distributions too. No gap.
- Wrong-LP risk (over-constraint): ruled out by the brute-force row validation (step 4) and by the 53/53 reproduction of the table's own k=1 upper bounds (step 5). Under-constraint would only weaken the proof, not invalidate it.
- Shadow sign convention: verified against the brute-force shadow set, not assumed from the paper.
- Checker soundness: the Farkas rule (value = u_E0 + u_E1 * 2^(n-k) > 0 and every column coefficient <= 0, with sign-free equality multipliers and nonnegative inequality multipliers) was re-derived by hand and matches both implementations; mutation tests show it rejects bad input.
- Stale table: byte-identical re-fetch of both pages (HTTP 200, hashes above).
- The k=0 cell (decision): the live cell (171,0) is [21,50]. Applying "[[n,1,d]] gives [[n,0,d]]" would cap pure codes at 50. That is not one of the criterion's rules (its k-1 rule is stated for k>=2 only), it holds for k=1 only for pure codes (a self-dual extension of an impure code can have smaller minimum weight), and the table itself leaves (171,1) at 57 despite (171,0) = 50. The certificate's bound covers impure codes too, which that inference does not. I do not count it as subsumption. Flag for the owner: the claimed 55 is probably not the LP optimum (the table's k=0 bounds at n>=126 sit well below the closed-form shadow bound), so a stronger bound may be reachable by the same method; that would not affect this claim.
- Not verified: how the certificates were generated (solver not shipped; irrelevant to the proof), the LP optimum at n=171, anything in the literature outside the table (no web allowed). The criterion is defined against the live table and propagation only, which I did check.

## Conclusion

Genuine and not subsumed under the criterion as written: the exact certificates verify independently, the LP rows are validated on real codes and reproduce the table's own bounds where floats are trustworthy, the live bound is 57, and the propagation closure leaves 57, so the new bound 55 (and the literal 56) is a real lowering of the live upper bound.

pass: true
