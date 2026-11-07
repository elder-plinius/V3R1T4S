# PREREG (frozen Wed Oct 28 08:21:31 UTC 2026, before any attack output of this run)

criterion (verbatim, charter quarry 5): "extend the exact census of anomaly-free U(1) charge assignments of the
Standard Model fermions (with and without three right-handed neutrinos) with integer charges bounded by `Q_max`,
beyond the largest `Q_max` tabulated by Allanach, Davighi and Melville; new exact counts, with the full solution
list as the certificate."

null_test: not needed because the claim is an exact count of explicit objects, each checked by a deterministic
checker against the definition; no search statistic or "beats chance" claim.

## Rule
1. Convention as fixed in run 2026-10-18-0552 and confirmed against the published tables (status/anomaly-free-atlas/).
2. The claim covers SMnuR Q_max 19 and SM Q_max 32..35 together (both contents). A row is established only if, in
   THIS run (after this timestamp), a full list is streamed through checker/checklist.c with PASS and "valid
   solutions" = count − 1, its sha256 recorded, and the count agrees with at least two independent counters (different
   code). All five rows must hold; otherwise no claim.
3. NOVELTY reads the arXiv record and the owner-supplied atlas PDFs (status/anomaly-free-atlas/).
