# PREREG.v4 (frozen 2026-11-11T11:01:24Z; a data-file repair after a tool failure, before any PRE score of the affected groups)

PREREG.md, v2 and v3 stay in force except for this. The PRE runs of groups v2022-06-11 (10:59:04Z) and v2022-02-14
(11:00:35Z) failed at load: LIRICAL 2.4.1 aborts with "IllegalArgumentException: Numerator 112 must be less than or
equal to denominator 16" because those two HPOA releases contain frequency cells n/m with n > m (curation errors:
v2022-02-14 has 3 such rows, e.g. OMIM:300912 HP:0000750 11/9; v2022-06-11 has 1, OMIM:616281 HP:0001347 112/16).
No PRE output exists for these groups; no score of any case has been computed for them.

## Change
- In the mapped HPOA of those two releases, a frequency cell n/m with n > m is blanked (the annotation row is kept;
  LIRICAL then uses its default for an annotation without frequency). No other cell changes. A scan of all 13 mapped
  releases found no other n > m cell (one 0/0 cell in v2022-10-05, which LIRICAL loaded without error, is left as is).
  Files: cache hpoa_mapped_v4/, sha256 v2022-02-14 9586f44207679ee8db00ce92e0e8c892f9e4434ed0789745722bd07cf81f0356,
  v2022-06-11 687b5e689c37bb9d165ba40ccb8f825d909ab801c48bc73b03478cf96b150962.
- The PRE runs of these two groups are rerun with the repaired files after the main sequence, under the same E1 cap
  (11:25:00Z); a JVM still running at the cap is stopped by its PID and its group counts as missing.
