# PREREG (frozen Tue Nov  3 09:19:36 UTC 2026, before any attack output of this run)

criterion (verbatim, charter quarry 5): "extend the exact census of anomaly-free U(1) charge assignments of the
Standard Model fermions (with and without three right-handed neutrinos) with integer charges bounded by `Q_max`,
beyond the largest `Q_max` tabulated by Allanach, Davighi and Melville; new exact counts, with the full solution
list as the certificate."

null_test: not needed because the claim is an exact count of explicit objects, each checked by a deterministic checker against the definition; no search statistic or "beats chance" claim.

## Rule
1. Convention as fixed in run 2026-10-18-0552; code copied unchanged from run 2026-10-28-0820 claim/ (sha256 in
   attempts/*/code/SHA256SUMS); csenum2 called with NPASS = 80 (pass split only; output bytes do not depend on NPASS).
2. Claim rows: SMnuR Q_max 20 and SM Q_max 36, 37, 38 (both contents in one claim). A row is established only if, in
   THIS run, its full list is streamed through checklist.c with PASS and "valid solutions" = count − 1, its sha256 is
   recorded, and the count agrees with mitm.c (an independent code, as in the confirmed 2026-10-28 claim). count.c is
   an optional third code. All four rows must hold; otherwise no claim.
3. The three-skeptic panel cannot fit in this run's budget: a claim, if any, is assembled in claim/ and stays
   PROMISING (unpanelled) until a later run panels it. No CONFIRMED_* tonight.
4. Memory: csenum2's resident memory is logged every 30 s; the run stops it by hand above 6.0 GB (cgroup ~7.4 GB).
