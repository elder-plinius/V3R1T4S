# Honesty gate (kit RUN.md step 7), claim run a100_1030_claim_run_2026-11-13-1615

target: apollo-moonquake-missed-vs-pds-catalog
claim: full success criterion, a second A100-like deep moonquake on S14 + S16, onset 1973-10-30 02:25:51.5 UTC (claim/CLAIM.md)
time: 2026-11-13T18:14Z (date -u at writing)
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true. Three fresh subagent contexts (Claude
Code Agent tool, subagent types reproduce, novelty and criterion), started 17:20Z with independent briefs, each told to
judge from claim/ only. NOVELTY finished 17:34Z, CRITERION 17:35Z, REPRODUCE 18:13Z.

## What the panel established

- REPRODUCE, with its own Steim2 reader and pipeline written from the prereg text before opening the claimant's code:
  Dt 0.2984 (claimed 0.2981); S14 MH2 0.630, S16 MH1 0.620; its own full-year null over all 365 days with all 401
  controls, best 0.1714 (claimant 0.1906); R6, R7, R8, R9, gap, thermal, glitch rule, G1/G2 pass; none of C1, C2, C3,
  C6, C6b holds; 6 A100 events in the reverse-search top 10 of 998; A6 0 of 984. It reran the claimant's full 12-nest
  scan (every science field identical on all 365 days) and n0_analyse.py (outputs byte for byte), and recomputed M1/M2
  exactly (z 17.47, p_FW = 1/402, GEV 4.655e-10).
- NOVELTY: the PDS index and all 12 tables fetched live 17:30:46-17:31:42Z (HTTP 200, every sha256 equal to the
  claimant's 16:15Z copies); no row within +/- 5 min, no span; Knapmeyer-Endrun and Hammer 2015 (own BIFF8 reader),
  Bulow 2005, Onodera, Shi, Li and Wang 2025 (Zenodo 15420872 / 16809589) and a 2026 GitHub ML scan of the archive:
  nothing within +/- 5 min. No 2025-2026 expanded deep-moonquake list found. The only public mention of the event is
  the claimant's own draft PR #1083 (package 2026-11-13-[credit]-9ff1c507), which calls it not claimed: prior work by
  the same claimant, not a publication that pre-empts it; this is a distinct, additional object.
- CRITERION: every bank clause met under readings fixed before the S14 + S16 measurement and fair; rejects as unfair
  the raw cross-template reading of "the same templates" (400 of 401 controls would exceed 0.298) and accepts the
  pre-registered per-template null plus the standardised max-T, which passes. Found in addition: the onset lies
  0.088-0.205 d from the times predicted by the catalogued 1973 A100 monthly sequence (P 0.015 for a random time),
  and the Liu et al. catalogue lists no S16 MH2 entries on days 297-304 while MH1 has 18-45 a day, an independent sign
  that MH2 was dead.

## Downgrade checklist (RUN.md step 7)

- Hedging panelist: no. Each states its limits and passes without hedging the verdict.
- Reproduction mismatch: none that changes a gate. Differences trace to implementation choices the prereg leaves
  open (gap dilation, MAD reading, filter order), as for the first claim: null maxima 0.1714 vs 0.1906, R8 nest median
  0.618 vs 0.82 s (5 vs 6 references), S14 MH2 0.630 vs 0.621. The frozen code reruns identically.
  Robustness, not gated: REPRODUCE's own stack rebuilt on the other decimation phase gives S14 MH2 0.5001 (the
  claimant's builder 0.621), and the S12 + S14 stack gives 0.37. The S14 match is the weakest part of the event; the
  scope sentence says so.
- Value vs live table: NOVELTY's fetch is 43 min old at this gate (< 6 h). No re-fetch needed.
- Stretched criterion or hidden quantifier: R7 per channel (fixed v4/v15, fair but favourable; S16 station mean 0.298
  because MH2 was unresponsive); PDS file URLs for FDSN URLs (access note, disclosed); null per template (fixed v15),
  with the 12-template max-T also passing. All in the scope sentence or the package's Not claimed.
- Multiplicity: the per-template null bounds the choice of the 2nd of several A100 peaks; max-T over the 12 templates
  p <= 1/402; the station-pair choice after the S12 + S14 near miss is not covered (55/402 = 0.14 over the parent
  run's scans, 26/402 = 0.065 for 1973). CRITERION's scope sentence carries these numbers, as the prereg's wording rule
  asked; the package README states them in its first paragraph.
- Scope wider than reproduced: no. The monthly-sequence clause of the scope is CRITERION's own computation from
  claim/ files (descriptive); the 55/402 bound is a stated weakness, not a strength.
- Sample presented as complete, capped search used as exclusion: no. Full year, 401 controls, three implementations.
- Evasion: no. One HTTP 403 (Wiley full text, NOVELTY) was not retried.
- Bundling: one event. The 1973-11-26 event is a separate claim and is not counted as support.
- Baseline: none applies.

## Corrections to claim/CLAIM.md found by the panel (claim/ itself left as panelled; fixed in the package and reports)

- "byte-identical to the lens scan": the scan files differ by a run-time field; every science field is identical.
- "A35 lies inside that ellipse": A35 is about 1.7 sigma from A100's location (outside 1 sigma, inside 2 sigma).
- "A100 median rank 2 of 98 nests" is fragile (17 of 98 in REPRODUCE's pipeline); the top-10 count holds in both.
- The headline sentence of CLAIM.md left the multiplicity numbers to its body; the scope sentence and the README
  headline carry them.

## Process notes

- tools/build_object_1030.py was copied into claim/code/c1030/ by mistake at about 17:21Z, after the panel was
  launched, and removed at 17:22:07Z. It writes package object files only and is used by no check.
- claim/code/tools/__pycache__/ (four .pyc files) was created 17:28-17:30Z by a panelist's process that imported the
  claimant's loader; REPRODUCE noted it; no source file changed. Left in place (claim/ is not
  packaged).

## Status

status: CONFIRMED_SOLUTION
confirmed_scope: In the saved PDS Apollo PSE data (Nunn et al. 2022 restoration), an S14 + S16 signal with onset 1973-10-30 02:25:51.5 UTC (MiniSEED Earth-received time) matches the frozen five-event 1973 S14 + S16 stack of catalogued deep-moonquake nest A100 with best single-channel NCC 0.621 on S14 MH2 and 0.620 on S16 MH1 (S16 MH2 unresponsive at the time; S14 reaches only 0.37 with the separate S12 + S14 A100 stack), an ATT-corrected S16-minus-S14 timing 0.10 s from the nest's median, an anomalistic phase of 161.5 deg inside the nest's 95% interval and about 0.1-0.2 d from the times predicted by the catalogued 1973 A100 monthly sequence, and a coincidence statistic of 0.298 above all 401 time-reversed and >= 1 h-shifted full-1973 controls of that template (best 0.191; p <= 1/402 per template and, by the pre-registered max-T test, family-wise over the scan's 12 templates; Bonferroni 12/402 = 0.03; the choice of the S14 + S16 lens after this event's S12 + S14 near miss is not covered, 55/402 = 0.14 over the parent run's scans), passes the pre-registered gap, thermal and glitch checks, and has no row of the 12 PDS catalogue tables as saved 2026-11-13T16:15Z within +/- 5 min or spanning it (nearest: an A1 deep moonquake 01:00-02:00), with the live re-fetch and the 24-month literature search left to NOVELTY, membership in A100 resting on the bank's tests and the attribution tests (a source without catalogued 1973 events and with A100-like waveform and moveout not excluded), and the event not independent of the earlier claimed 1973-11-26 event (same template, statistic, null and readings).
