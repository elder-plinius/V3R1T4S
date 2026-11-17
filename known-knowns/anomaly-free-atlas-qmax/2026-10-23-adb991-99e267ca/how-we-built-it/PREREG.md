# PREREG (frozen Sun Oct 18 05:56:28 UTC 2026, before any attack output)

criterion (verbatim, charter quarry 5): "extend the exact census of anomaly-free U(1) charge assignments of the
Standard Model fermions (with and without three right-handed neutrinos) with integer charges bounded by `Q_max`,
beyond the largest `Q_max` tabulated by Allanach, Davighi and Melville; new exact counts, with the full solution
list as the certificate."

null_test: not needed because the claim is an exact count of explicit objects, each checked by a deterministic
checker (checker/check_list.py) against the definition; there is no search statistic or "beats chance" claim.

## Rule

1. Conventions are fixed by calibration only: a counting convention is adopted only if the enumerator reproduces
   EVERY published value listed in BRIEF.md (SM: Q_max 1, 3, 5, 7, 10; SMnuR: Q_max 6, 7, 8, 9, 10) exactly.
   If no convention reproduces all of them, there is no claim.
2. A new count N(content, Q_max) for Q_max >= 11 counts as established only if two enumerators with different
   algorithms (different split or method; at least one of them listing the solutions explicitly) give the same
   integer, and checker/check_list.py prints PASS on the full list with exactly that many valid lines.
3. The certificate is the full list (one canonical solution per line), identified by its sha256 and line count.
4. A record needs the published maximum to be Q_max = 10 for the content in question; since the table could not be
   read from this machine, NOVELTY is expected to be PENDING STATUS CHECK and the status at most PROMISING.
5. Nothing is claimed for a Q_max whose run did not finish (no extrapolation, no partial counts).

Note added Sun Oct 18 05:56:54 UTC 2026, still before any attack output: checker/check_list.py now checks the hypercharge-squared
condition in integer form (x6), reads .gz lists, and replaces its in-memory duplicate set by a strictly-increasing
order check, so it can read lists of 10^8 lines. The rule above is unchanged.
