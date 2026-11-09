# Honesty gate (run's main session), 2026-10-23T23:27:25Z

claim: partial win p1 of tsunami-tide-gauge-signal-not-in-ncei, NCEI event 5942, stations Luganville (luga) and Lifou (lifo/lifo2).
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true. All three by fresh subagents that saw only a copy of claim/.

Checks against the downgrade list:
- hedging panelist: CRITERION calls Lifou "marginal" (R 5.24; per-gauge null 2/400 gated, 6/400 ungated) but finds every
  clause met; its confirmed_scope carries that caveat. REPRODUCE shows Lifou at R 8.06-8.45 against control max 4.84-4.98 in a
  5-120 min band (informative, not the stated band) and 3/1238 all-hours false alarms. Not a hedge on the verdict; the scope
  stays as narrow as CRITERION wrote it.
- reproduction mismatch: none material. R, peaks, peak-to-trough match to 0.01; onset labels are 1-min bin starts 34 s before
  the raw samples (noted in observations.csv); model ETAs vary 45.8-50.3 (luga) and 33.6-38.1 min (lifo) across grids, and
  every pick stays within +/-10 min, Luganville by 0.9 min with the ComCat epicentre (CRITERION W3).
- value vs live table: p1's bar is NCEI's runup table. Live re-fetch by NOVELTY at 2026-10-23T23:04:33Z (HTTP 200, sha256
  64268edc...c7ae, byte-identical to the scout copy): 2 rows, Port Vila and Lenakel; none for Luganville or Lifou under any
  name. Under 6 h old at this gate. CRITERION's re-fetch on 2026-10-24 found the same.
- stretched criterion / hidden quantifier: ">= 2 gauges" read as 2 distinct stations; lifo2 is not counted separately.
- sample as complete, capped search as exclusion, probable prime: not applicable.
- table access by evasion: none (plain GETs with a V3R1T4S User-Agent; no retries).
- bundling: one event, two stations, one claim.
Post-panel edits to claim/: credit name corrected (earthjay.com plot is by J. Patton, not "J. Parker", per NOVELTY);
a comment line on onset/peak time labels added to data/observations.csv (per REPRODUCE). No value changed.
Note on confirmed_scope: CRITERION's "re-fetched on 2026-10-24" is the local calendar date; its job 2386 ran on
2026-10-23 UTC (its log: runups 5942 totalItems 2, LENAKEL and PORT VILA). A later station-name scan in that job errored;
the claim does not rest on it.

status: CONFIRMED_PARTIAL
confirmed_scope: For NCEI tsunami event 5942 (2024-12-17 01:47:26 UTC, M7.3, Vanuatu Islands), two IOC SLSMF stations with no NCEI runup row for that event in the runups API re-fetched on 2026-10-24 (which lists only Port Vila and Lenakel) recorded band-passed (2-120 min) signals meeting the bank's per-gauge standard: Luganville (luga) clearly, with peak 0.078 m, R 8.4, rule-based onset 02:29 UTC and 0 of 400 random-time controls as large; and Lifou (lifo/lifo2, two sensors at one site) marginally, with peak 0.060 m, R 5.2, onset 02:21 UTC and 2 of 400 gated random-time controls as large; both onsets fall within 10 min of ETOPO1 shallow-water travel times from either the NCEI or the ComCat epicentre, and neither station detects on 11-12 control days.
