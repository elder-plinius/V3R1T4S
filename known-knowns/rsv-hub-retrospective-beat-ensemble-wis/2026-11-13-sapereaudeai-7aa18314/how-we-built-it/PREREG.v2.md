# PREREG.v2 (amendment to PREREG.md, written 2026-11-13T01:24:18Z, date -u)

Why: profiling the archive (no forecast of ours exists yet; nothing of ours has been scored) showed two facts that make
R3's "latest file dated on or before O" unsafe:
1. target-data/archive/2023-12-08_rsvnet_hospitalization.csv holds data up to 2023-12-30 (same byte size as the
   2024-01-05 file): its label is earlier than its content. Using it for origin 2023-12-10 would read future weeks.
2. From 2025-01-27 the archive has two parallel families (Friday files with 11 age groups; Saturday/Monday files with
   13 age groups); a Saturday file can hold older data than the Friday file before it (2025-03-01 ends 2025-02-15,
   2025-02-28 ends 2025-02-22).

Amended R3 (replaces the choice rule of R3; everything else in PREREG.md stands):
- A vintage D is usable for origin O iff D <= O AND the latest date in it (any location, age group) <= O - 8 days
  (the hub's own convention: Friday pull, data to the Saturday 8 days before the Sunday origin).
- Among usable vintages, the data vintage is the one with the latest data date; ties go to the latest label.
- Revision estimates may use only usable vintages (the same test with the same O).
- The audit (contrarian lens) checks, for every origin, that no value of a week later than O - 8 days was read.

No other reading changes. PREREG.md sha256 (unchanged): ed4987b2fb9c1d94a721d5f608e8e1a74f987b056b04f0a8ef98d35dd6bc1998
