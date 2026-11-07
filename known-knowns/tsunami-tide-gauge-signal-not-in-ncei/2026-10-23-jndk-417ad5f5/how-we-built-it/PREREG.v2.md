# PREREG v2 (frozen 2026-10-23T23:05:02Z)

Scope extension only; every rule, threshold and the null design of PREREG.md is unchanged (tsu.py sha256
61bccc50777e893634ff2e199a836fa79c8a30e50a13aa796de0f0f6e6f85a54).
Reason: PREREG.md's p1 lens covered NCEI earthquake events since 2024-01-01 (job 2287: one survivor, NCEI 5942, now
with the panel). This adds NCEI earthquake events (causeCode 1) dated 2019-01-01 to 2023-12-31 to the same p1 pipeline
(sweep.py p1 with P1_MINYEAR=2019, P1_MAXYEAR=2023), as leads for later runs. Any survivor gets the same control-day
test and 400-control null before it is called a candidate.
null_test: required
