# Criterion skeptic verdict (partial win p1)

- Reran checks 2, 3 and a dsumcheck at N=40 (check 1 form). Results: U_D vs CX Table 4 and C(from U_D) vs Table 5 give checked=22 MISMATCH 0. U_A gives the same. b-file checks give MISMATCH 0 (29 terms, 28 terms). N=40 gives AGREE.
- Method D vs A are different implementations. D is per-type extraction plus a count-vector DP mod 2^521-1. A is a C histogram recurrence with CRT over word-size primes. Cheng-Xu also use a histogram recurrence, so A is not independent of their method. D is the genuinely independent one. D imports A's engine only for the optional per-type F_A column (off with --noA).
- Nonidentity types: the types count equals p(N) for every N=29..50 in results/Dsum_check_d4.txt (4565 at 29, 204226 at 50). The sum is a full Burnside sum over all partitions, not a sample. Two ERR rows exist in the N=30 files. The retried valid rows are used and the sums agree.
- Exact arithmetic: each F(lambda) <= F(1^N), about 64 digits at N=50, far below 2^520. The modulus exceeds the bound, so the values are exact. A uses CRT over primes, and D agrees with it.
- Agreement: D vs A on totals U for all 22 orders, and both vs the CX table. Connected C is obtained by inverse Euler for all 22 orders and equals Table 5. Per-type D vs A agreement is shown only at N=30 (2782 'ok' rows, plus the earlier small-N rows I did not inspect). For N=29 and 31..50 only the totals are compared, not per type. That is weaker than "per-type agreement", but the claim only requires a second implementation agreeing, and total agreement of 22 large integers is strong evidence.
- Disagreements with the table: none. Nothing is presented as a sample.
- This is NOT the full criterion: there is no order >= 51 and no new b-file term. A produces C_4(51) alone, with no second method, so it is not a win. The result is the bank's enumerated partial win p1 only.
- Caveat: the "did not cross-check nonidentity contributions" premise about CX is taken from the bank text, not verified here.

confirmed_scope: For every order N=29..50, an independent Burnside sum over all p(N) cycle types (method D, exact mod 2^521-1) gives unlabeled quartic totals equal to the C implementation of the histogram recurrence (method A) and to Cheng-Xu's Table 4, and the inverse-Euler connected counts equal Table 5 (MISMATCH 0), with per-type D vs A agreement shown only at N=30; nothing at order 51 or above.
context: subagent (fresh, general-purpose)
pass: true
