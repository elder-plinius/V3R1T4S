# Honesty gate (main session, Sun Oct 18 10:29:58 UTC 2026)

Panel: reproduce pass: true (own counter and own strict checker, all 25 rows regenerated in full, hashes and line
counts equal to claim/object/counts.txt, determinism checked); criterion pass: true; novelty pass: false with
"novelty: PENDING STATUS CHECK" (the atlas paper, erratum and Zenodo record refused by the proxy at 09:53 UTC; no
Q_max >= 11 count in the last 24 months of literature, TROPHY_CASE.md or open pull-request titles).

Read by the main session: all three files. No reproduction mismatch. Downgrade: the status source could not be read,
so the record is not confirmed: PROMISING. Noted: published calibration values come from search-tool text;
checker/checklist.c does not compare its count with an expected one (the skeptic's own checker does; line counts
were compared separately); rows SMnuR 14..16 and SM 21..31 come from one lister each (counts from three counters).
My own streamed check of SMnuR 16 finished at 10:09 UTC: PASS, 1002483710 (attempts/extender/check/stream_checks.log).
To confirm: a human reads the atlas table (arXiv:1812.04602 v5, erratum JHEP08(2019)064, Zenodo 3345889) and checks
that 10 is the largest published Q_max for both contents; then a fresh NOVELTY skeptic reruns for this claim and
for run 2026-10-18-0552's Q_max 11 claim.

round-1 status: PROMISING (superseded below)
round-1 confirmed_scope (unchanged): Under the inequivalence convention inferred from, and reproducing all ten of, the Allanach-Davighi-Melville values available here (SM Q_max 1, 3, 5, 7, 10 and SMnuR Q_max 6..10, as reported by search-tool text, not primary-checked), the exact counts in object/counts.txt for SM plus three right-handed neutrinos at Q_max = 12..16 and for the SM at Q_max = 12..31 (Q_max = 11 not included) each agree with an independent no-list counter and with a deterministic canonical solution list of count - 1 lines (the all-zero assignment is counted but not listed), regenerable from source and identified by the sha256 of its uncompressed stream rather than stored, and all lie beyond Q_max = 10, the largest value that source reports for either content.

## Round 2 (Fri Oct 23 19:44:32 UTC 2026)

The owner supplied the primary sources (arXiv:1812.04602 v5 and erratum JHEP 08 (2019) 064; status/anomaly-free-atlas/,
sha256 in SHA256SUMS). A fresh NOVELTY skeptic read them: largest published Q_max is 10 for SM and SMnuR; every
claimed row is strictly beyond it; no later count found (panel/novelty.md, pass: true; the round-1 verdict is kept as
panel/novelty_round1_pending.md). The main session also checked all 40 published values (solutions and symmetry
columns, both contents, Q_max 1..10) against this workspace's counters: all match (status/anomaly-free-atlas/
table_comparison.txt), so the counting convention is the paper's. Reproduce and criterion verdicts unchanged (pass).

status: CONFIRMED_SOLUTION
confirmed_scope: Under the inequivalence convention inferred from, and reproducing all ten of, the Allanach-Davighi-Melville values available here (SM Q_max 1, 3, 5, 7, 10 and SMnuR Q_max 6..10, as reported by search-tool text, not primary-checked), the exact counts in object/counts.txt for SM plus three right-handed neutrinos at Q_max = 12..16 and for the SM at Q_max = 12..31 (Q_max = 11 not included) each agree with an independent no-list counter and with a deterministic canonical solution list of count - 1 lines (the all-zero assignment is counted but not listed), regenerable from source and identified by the sha256 of its uncompressed stream rather than stored, and all lie beyond Q_max = 10, the largest value that source reports for either content.
