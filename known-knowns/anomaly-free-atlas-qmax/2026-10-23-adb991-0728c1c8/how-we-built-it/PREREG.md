# PREREG (frozen Tue Oct 20 08:18:25 UTC 2026, before any attack output of this run)

criterion (verbatim, charter quarry 5): "extend the exact census of anomaly-free U(1) charge assignments of the
Standard Model fermions (with and without three right-handed neutrinos) with integer charges bounded by `Q_max`,
beyond the largest `Q_max` tabulated by Allanach, Davighi and Melville; new exact counts, with the full solution
list as the certificate."

null_test: not needed because the claim is an exact count of explicit objects, each checked by a deterministic
checker against the definition; no search statistic or "beats chance" claim.

## Rule
1. Convention as fixed in run 2026-10-18-0552.
2. A row (SMnuR Q_max 17, and 18 if time allows) is established only if a full list is streamed through checker/checklist.c
   with PASS and "valid solutions" = claimed count - 1, its sha256 recorded, and the count agrees with at least two
   independent counters (different code).
3. Rows that do not finish are not claimed. NOVELTY expected PENDING STATUS CHECK: status at most PROMISING.
