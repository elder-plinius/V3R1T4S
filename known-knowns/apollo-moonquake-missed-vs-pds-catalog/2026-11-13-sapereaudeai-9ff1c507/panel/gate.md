# Honesty gate (kit RUN.md step 7), continuation fullwin_panel

target: apollo-moonquake-missed-vs-pds-catalog
claim: full success criterion, deep moonquake of nest A100 on S14 + S16, onset 1973-11-26 07:46:28.6 UTC (claim/CLAIM.md)
time: 2026-11-13T11:15Z (date -u at writing)
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true. All three are fresh subagent contexts
(Claude Code Agent tool, subagent types reproduce, novelty and criterion) that saw only claim/. The REPRODUCE verdict
comes from a fourth instance; three earlier instances died of an API authentication outage before writing anything.
The fourth reused their finished scans only after reading and spot-checking them, and its numbers come from its own code.

## Why the earlier gate stopped at PROMISING, and what changed

1. Unread published list. Knapmeyer-Endrun and Hammer (2015) Tables S1-S3 were downloaded by the human. Three readers
   checked them: the shipped reader, NOVELTY's own BIFF8 reader, and REPRODUCE's byte scan. No row lies within
   +/- 5 min, and the nearest is +54.9 h. Resolved.
2. Nest attribution. The S16 MH2 null was the doubt. PREREG.md (frozen 09:11:02Z, before any new number) fixed four
   contradiction tests: C1 another stacked nest, C2 a lag side lobe, C3 S16 MH2 polarisation, C6 a nest without a stack.
   None holds, in the author's code and in REPRODUCE's independent code. The evidence:
   - S16 MH2 did not respond to any catalogued deep moonquake on 1973-11-25 to 11-27. The response ratio r2 was
     0.015-0.13 for A203, A51, A252, A20 and A33, against 0.166-0.18 for the candidate. The S16 MH2 null is therefore an
     instrument state, not a source property.
   - The candidate's own waveform, scanned over 1973, ranks catalogued A100 events at the top of 998 catalogued deep
     moonquakes: 6 of the top 6 in the author's code; 5 of the top 5 and 6 of the top 10 in REPRODUCE's code.
   - Only A100 of the 12 stacks is above its own null, and the lag maxima over +/- 30 s are at the claimed lags.
   - The event continues A100's 1973 monthly sequence (descriptive, not a gate).

## Downgrade checklist (RUN.md step 7)

- Hedging panelist: no. Each panelist states limits (weak event, R7 on the best single channel, R9 wide, a source
  without catalogued 1973 events not excluded) and passes without hedging the verdict.
- Reproduction mismatch: none that changes a gate. Independent code differs slightly: S14 MH2 0.576 vs 0.562; R8 nest
  median 0.62-0.68 s vs 0.82 s; null maxima 0.172-0.179 vs 0.191. The differences trace to two pipeline details the
  prereg text leaves open: the reading of "running MAD", and a 20 s widening of gaps in the frozen code. The frozen
  code reruns byte-identically on all 365 days.
- Value vs live table: NOVELTY re-fetched the PDS index and all 12 tables at 09:40:32-09:41:22Z (HTTP 200,
  byte-identical to the claim's copies). There is no row within +/- 5 min and no span containing the onset. The
  fetch is 1.6 h old, under the 6 h limit.
- Stretched criterion or hidden quantifier: two readings decide the claim, and both were fixed before the scan.
  - R7 is read per channel. CRITERION found it fair but favourable: the station means are 0.494 and 0.343, and S16
    rests on MH1 because MH2 was unresponsive.
  - The bank's "FDSN request URLs" are given as PDS file URLs, under the human's access note.
  - R7 at S14 depends on the decimation grid: 0.470 on the other phase. At near-continuous lag it is 0.566 (CRITERION).
    The prereg declared this as reported, not gated.
- Scope wider than reproduced: no. The scope sentence below is CRITERION's. Its two open items, the live re-fetch and
  the 24-month search, were done by NOVELTY and passed.
- Sample presented as complete, capped search used as exclusion: no. The null spans all 365 days with 401 controls,
  in three implementations.
- Evasion: no. Every fetch was one honest request; nothing was blocked.
- Bundling: one event. The 1973-10-30 event is not part of the claim.
- Baseline: none applies (CRITERION agrees).

## Status

status: CONFIRMED_SOLUTION
confirmed_scope: In the saved PDS Apollo PSE data, a signal at 1973-11-26 07:46:28.6 (MiniSEED Earth-received time) on S14 and S16 matches the frozen 1973 stack of catalogued deep-moonquake nest A100 with best single-channel NCC 0.562 (S14 MH2) and 0.699 (S16 MH1), an ATT-corrected S16-minus-S14 timing 0.11 s from the nest's median, an anomalistic phase inside the nest's 95% interval, and a coincidence statistic of 0.343 above all 401 reversed and shifted controls over 1973 (maximum 0.191); it passes the pre-registered gap, thermal and glitch checks, and no row of the PDS catalogue tables as saved at 2026-11-13T04:29Z lies within 70 min, with the live re-fetch and the 24-month literature search left to NOVELTY.

Conditions:
- This gate could not run check_run.py on the workspace, because the coordination rules for this continuation reserve
  that run for the main session. RUN.md step 7 lets a CONFIRMED_* status stand only if that check prints
  CHECK_RUN: PASS. If it does not, this status is PROMISING.
- The package check (check_run.py --package) is run separately and recorded in the run report.
