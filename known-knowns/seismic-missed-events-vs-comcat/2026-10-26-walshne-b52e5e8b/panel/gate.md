# Honesty gate (RUN.md step 7), run 2026-10-26-1727

status: CONFIRMED_PARTIAL
confirmed_scope: An earthquake at 2024-12-09T23:20:13 UTC near 39.165 N 119.050 W (8 P/S picks on 5 NN stations; my layered-model relocation RMS 0.17 s, 68 % horizontal error 1.8 km), with a ComCat-ml-equivalent magnitude of 1.58-1.72, is absent from live ComCat (+/-30 s, 50 km, fetched 2026-10-26T19:27Z), from ISC (HTTP 204) and from the Bogolub and Trugman (2025) Parker Butte catalogue, has no null detection at its NCC of 0.6705 in my time-reversed null (maximum 0.445 over 4 days) or in the claimant's circular-shift null (0 of 600 controls; 40 spot-checked by me, agreeing), and is at or above my Mc - 0.3 = 1.5 (Mc 1.8 by maximum curvature + 0.2 from live ComCat within 50 km, 2022-06-09 to 2026-10-26) in the NN-authoritative onshore region, which meets partial win p1 of seismic-missed-events-vs-comcat and not the main win.

## Panel (three fresh subagent contexts, each seeing only its own copy of claim/)
- **reproduce.md: pass: true.**
  - **Coverage:** exhaustive. All 600 shifted controls and all 3,000 early-hours controls were checked with its own
    float64 implementation; the largest differences were 0.0028 and 0.0076, from the day-taper and per-day prep. It found
    0 controls at or above 0.6705, and exactly 1 of 3,000 in the early-hours set.
  - **Author's code, rerun with 10 workers:** byte-identical to every shipped output, so it is deterministic.
  - **Pearson agreement:** 3.5e-12 at 1,023 points, 223 of them in the mainshock chunk.
  - **Data refetches:** all byte-identical.
  - **Picks, location, magnitudes, Mc and the calibration relocations:** reproduced exactly.
  - **Live absence:** checked at 20:56:58Z, with positive controls.
- **novelty.md: pass: true.**
  - **Absent from:** the status source (read 19:22:06Z), ComCat including deleted events, the Bogolub and Trugman
    catalogue (md5 matches Zenodo, a single version), the last 24 months of literature, TROPHY_CASE.md and open or closed PRs.
  - **ISC limit:** ISC lists only M about 2.7 and above here, so its HTTP 204 is weak evidence for an ML 1.6. The
    criterion asks for ISC only "if reachable", and the comprehensive absence rests on ComCat and the enhanced catalogue.
- **criterion.md: pass: true.**
  - **Clauses:** every clause is met literally.
  - **Own checks:** its own layered relocation (RMS 0.167 s, 68 % ellipse 1.84 km), a time-reversed null (maximum 0.445
    over 4 days), 40 controls exact, its own live Mc 1.8 (bar 1.5), and ComCat-scale magnitudes 1.58-1.72.
  - **Main win:** not met, and not claimed.

## Gate reading
- **Hedging:** none. All three verdicts are unqualified passes.
- **Reproduction mismatches:** none. REPRODUCE found byte-identity with the author's code and a < 0.003 difference in
  its own null.
- **Stretched criterion or hidden quantifier:** none found.
  - **Magnitude:** "magnitude >= Mc - 0.3" is met by every ComCat-scale estimate against the largest Mc of any window or
    radius (1.8). One uncalibrated Wood-Anderson variant (1.491) is not on ComCat's ml scale.
  - **Early-hours sensitivity:** its 95 % upper bound (about 0.057) exceeds 0.05. The criterion's quantity is the
    expected false count, which is 0 on the criterion's null (bound 0.015) and 0.012 on the stricter lens.
  - **Recorded, not blocking:** both points above, plus the azimuthal gap of 172 deg and the 8 picks at the floor.
- **Scope:** the CRITERION sentence does not exceed what was reproduced. REPRODUCE independently covers the full null that
  CRITERION spot-checked.
- **Samples presented as complete:** none.
- **Evasion:** none. Every fetch was a plain GET with an identifying User-Agent and no retries.
- **Bundled objects:** none. This is a single event.
- **Freshness:** the panel's latest table fetch was at 20:56:58Z (REPRODUCE) and the gate is at 21:02Z,
  within 6 h.
- **Disclosure:** this event was panelled twice before (2026-10-23-1839 and 2026-10-24-0604, both 2/3, failing on
  package defects). This package fixes those defects, which claim.md discloses.
