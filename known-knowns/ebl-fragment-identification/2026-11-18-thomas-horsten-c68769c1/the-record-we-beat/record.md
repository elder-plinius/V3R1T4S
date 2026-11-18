# The record we beat (target: ebl-fragment-identification)

The "table" this target is judged against is the pre-registered success criterion
(criterion_verbatim.txt in this folder) and the live eBL corpus. The fragment record
and the corpus dumps are the public inputs; the claim is a candidate identification of
one unplaced fragment.

Status source (fetched honestly by the run's scout and re-checked by the NOVELTY
skeptic; no retries):
- URL: https://www.ebl.lmu.de/api/statistics
- Fetched: 2026-11-17T21:42:46Z (UTC) by the scout (HTTP 200), and again
  2026-11-18T00:31Z by the run's live (a) re-check (HTTP 200); the NOVELTY skeptic
  re-fetched /api/statistics, /api/fragments/BM.68403 (HTTP 200) and /match (HTTP 403)
  at 2026-11-18T02:06Z.
- Live value (2026-11-18T00:31Z snapshot, package-pinned in how-we-built-it/data/
  fragments_all_signs.json + object/record_BM.68403.json):
  `{"transliteratedFragments": 39106, "lines": 636203.0, "totalFragments": 328942}`
  (scout's 2026-11-17T21:42:46Z record: 39105 / 636187.0 / 328942 — the corpus grew
  by one transliterated fragment between the two fetches).
- sha256 of the scout's saved statistics file
  (runs/2026-11-17-2142/data/ebl_statistics_2026-11-17T2142.json):
  `20314f5d6c7a2f7ab4773e66dd17f5861e969cb1d37970fd588982953dd7af27`
- sha256 of the 2026-11-18T00:31Z re-check
  (runs/2026-11-17-2142/output/ebl_statistics_2026-11-18T0031.json):
  `1e14826c06f34a1228bf97bdc80b8b633fd6d1c55644460836eed23ff160b1a1`
- sha256 of the package-pinned eBL fragment record (object/record_BM.68403.json):
  `373beff3f84f61283e8e9a909e0b77fd523bac73b3c45f26dfa05fd19d80f1fe`

The eBL task is open-ended (identification still largely manual; the in-platform
lineToVec matcher is 403-public). The baseline the claim is compared against is eBL's
own **public** ngram-matcher (commit e8918de), re-implemented offline and frozen in
how-we-built-it/PREREG.md (condition (d) section); the empirical-benchmark record
(how-we-built-it/baseline/record.md) reproduces the eBL statistics endpoint exactly and
calibrates the independent aligner + TF-IDF matcher on 12 known-identified fragments
(12/12 aligner top-hit recovery; 9/12 TF-IDF top-10 membership).
