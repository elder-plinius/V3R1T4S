# PREREG (frozen Sun Oct 18 08:18:58 UTC 2026, before any attack output of this run)

criterion (verbatim, charter quarry 5): "extend the exact census of anomaly-free U(1) charge assignments of the
Standard Model fermions (with and without three right-handed neutrinos) with integer charges bounded by `Q_max`,
beyond the largest `Q_max` tabulated by Allanach, Davighi and Melville; new exact counts, with the full solution
list as the certificate."

null_test: not needed because the claim is an exact count of explicit objects, each checked by a deterministic
checker against the definition; no search statistic or "beats chance" claim. (The asymptotic fit is reported as
analysis, never as a count.)

## Rule

1. Convention: as fixed in run 2026-10-18-0552 (reproduces all ten published values).
2. A count for a given (content, Q_max) is established only if (a) an explicit list exists, (b) checker/check_list.py
   (or a C checker shown to agree with it on every list it has checked, including negatives) prints PASS with
   "valid solutions" equal to the list's line count, and (c) an independent counter (different algorithm: raw count,
   Burnside, Moebius) gives that count + 1.
3. The claim of this run: the census rows that meet rule 2 beyond Q_max 11 (SMnuR Q_max 12 and, if listed and
   checked, 13; SM Q_max 12..20), one census table, certified row by row.
4. No extrapolated value is a count. Asymptotic fits are labelled as heuristics.
5. NOVELTY is expected to be PENDING STATUS CHECK (status source blocked): status at most PROMISING.
