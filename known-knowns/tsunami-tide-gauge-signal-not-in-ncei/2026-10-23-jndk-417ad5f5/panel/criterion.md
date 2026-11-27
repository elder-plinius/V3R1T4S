# Criterion skeptic: tsunami-tide-gauge-signal-not-in-ncei, partial win p1 (NCEI event 5942)

context: subagent (Claude Code Agent tool, fresh context)

Inputs read: CLAIM.md, REPRODUCE.md, data/observations.csv, data/candidate_record.json, data/null_summary.json,
data/FETCHLOG.tsv, data/ncei_event_5942.json, data/ncei_runups_*.gz, data/candidate_ncei5942.png, code/tsu.py,
code/check_p1.py, code/null.py. My own checks: mine/skeptic.py, run on the remote queue (output/job-2386/job.log;
an earlier attempt, which crashed on an ETOPO HTTP 500 after the NCEI and ComCat steps, is also under output/).

## Literal reading of p1

"Gauge observations (amplitude, arrival) for a listed NCEI event at >= 2 gauges where NCEI has no runup rows for those stations."

| Clause | Literal reading | Verdict |
|---|---|---|
| listed NCEI event | an event id in the NCEI HazEL tsunami events table | Met. Event 5942 (2024-12-17 01:47:26 UTC, M7.3, VANUATU ISLANDS, validity 4, numRunups 2) is in the table (data/ncei_event_5942.json). |
| gauge observations (amplitude, arrival) | a measured amplitude and an arrival time per gauge, taken from the gauge record | Met. data/observations.csv gives peak, peak-to-trough, onset time and the rule that produced them. The onset is rule-defined (first band-passed sample >= 3x RMS24 in [ETA-30, ETA+60] min). It is not hand-picked (see W3). |
| at >= 2 gauges | at least two distinct stations; two sensors at one site count once | Met with exactly 2: Luganville (luga) and Lifou (lifo). lifo2 is a second sensor at the same Lifou site, and the claim says so. It corroborates Lifou but does not count as a third gauge. Each of the 2 stations has to stand on its own, so Lifou carries half the claim. |
| NCEI has no runup rows for those stations | the NCEI runups table has no row for Luganville or Lifou for this event | Met. I re-fetched it live on 2026-10-24 (output/job-2386/job.log): totalItems 2, LENAKEL, TANNA and PORT VILA, EFATE ISLAND, both type 2 (tide gauge). In the same NCEI table, rows for other events include "LUGANVILLE" (type 2, for example 2008, 2011, 2022, 2023) and "LIFOU ISLAND" (type 2, for example 2021, 2022, 2023). So NCEI knows these stations and records them for other events. Their absence for 5942 is a real gap, not a naming mismatch. |

The claim also applies the full criterion's per-gauge evidence standard. I checked it clause by clause.

| Full-criterion clause | luga | lifo (lifo2) |
|---|---|---|
| raw IOC SLSMF series saved, de-tiding code, source parameters | yes (data/ioc_luga_*.gz, code/tsu.py) | yes (data/ioc_lifo_*.gz, data/ioc_lifo2_*.gz) |
| band-passed 2-120 min, peak > 5x RMS of the preceding 24 h | R 8.44 (reproduced) | R 5.24 (5.23) (reproduced). This is the marginal one. |
| arrival within +/-10 min of shallow-water travel time from the source (ComCat earthquake) | NCEI epicentre: dt -7.6 (claim) / -7.8 (my recompute). ComCat epicentre (us7000nzf3, -17.6914, 168.0842): dt -9.07. Passes by 0.9 min. | dt -1.2 / +0.4 / -0.9 (ComCat). Passes comfortably. |
| signal absent on the same gauges in the same hours on control days | 0 of 11 usable control days detect | 0 of 12 (max control R 3.8, never in the arrival window) |
| NCEI re-fetched live before claiming, no runup row for those gauges | claimant at 2026-10-23 ~23:02 UTC, and me on 2026-10-24: none | none |

## Weaknesses found and how they weigh

W1. Lifou is marginal (moderate weight; does not sink the claim).
- R = 5.24 (lifo) and 5.23 (lifo2), against a threshold of 5.
- Sensitivity, my job: Butterworth order 2 / 4 / 8 gives 5.19 / 5.24 / 5.24. Without the despike step or the harmonic fit it is 5.24. A 3-120 min band gives 5.98. RMS taken over the 24 h before the onset (instead of before the origin) gives 5.16-5.21. lifo2 behaves the same way.
- So R > 5 holds under every reasonable zero-phase implementation I tried, but the margin is only about 3-4%.
- A causal filter shifts the onset to 17 min and fails the arrival test. A causal filter is not a reasonable de-tiding choice for this purpose, so I do not count that against the claim.
- Visually (data/candidate_ncei5942.png), Lifou's background is broadband 3-10 min noise at +/-0.03-0.04 m. Event-day excursions of 0.05-0.06 m appear at about 45, 68 and 78 min. They are larger than the typical background, but not dramatically so. One control-day trace reaches about 0.06 m at about +185 min.

W2. The null model is weaker than its headline (moderate weight).
- The packaged null statistic is S = min over {luga, lifo, lifo2} of the gated R, and "best_control 0.0" just reflects how rarely all gauges produce an in-window onset at once. lifo and lifo2 are nearly identical, so S is effectively min(luga, lifo). It does not test Lifou on its own strongly.
- Per-gauge nulls are the honest measure.
  - Claimant: lifo 2/400, luga 0/400.
  - My rerun with the same seed and the same +/-60 d window, gated: lifo 2/400 >= real, luga 0/400.
  - Ungated (max |bp| over [ETA-10, ETA+190 min] divided by RMS24, no onset rule): lifo 6/400 >= 5.24 (1.5%), and 8/400 above 5. luga 0/400 >= 8.44, with a control maximum of 5.49.
- So Luganville is an unambiguous detection. Lifou alone is significant only at roughly the 0.5-1.5% level.
- The look-elsewhere effect is real: 14 usable gauges for this event, plus a sweep over other events that is not in the package.
- What carries Lifou is the combination of:
  - a definite NCEI tsunami (validity 4, observed at Port Vila 0.25 m and Lenakel 0.17 m);
  - the predicted timing;
  - two independent sensors (prs and rad) showing the same waveform, which rules out an instrument artefact (it does not rule out natural noise);
  - 0/12 control days.
- On balance a real but small tsunami signal at Lifou is the better explanation. It is not proven beyond doubt.

W3. The Luganville "arrival" is early and sits near the edge of the window (low-moderate weight).
- The onset rule fires at 42 min on a small precursor bump (0.033 m). The large first motion (trough about -0.06 m) comes at about 48-50 min, which matches the model ETA of 49.6-51.1 min.
- With the ComCat epicentre, the rule-based dt is -9.07 min, inside +/-10 by 0.9 min. If finite-source or bathymetry errors were a few minutes larger, the rule-based onset would fall outside the window.
- However, the evident main arrival is consistent within about 2-3 min, and with a causal filter the onset is at 48 min (dt -1.6). Literally the criterion is met either way.
- The reported luga arrival time (02:29:26Z) should be read as the rule-based onset, not the time of first major motion.

W4. Source parameters (low weight). The claim takes its epicentre from NCEI, while the criterion names USGS ComCat. ComCat (us7000nzf3, M7.3, 01:47:25.7 UTC, -17.6914, 168.0842, 54 km) is about 5 km from NCEI's epicentre. With it, both gauges still pass (luga -9.07, lifo -0.94). The ETA also depends on the model's ETOPO snapping: the claim lists lifo at 35.17 min, my recompute gives 33.55 min. Both pass.

W5. Bundle completeness (low weight). The control-day raw series appear in data/FETCHLOG.tsv but are not saved in data/. check_p1.py re-downloads them. The criterion's "raw IOC SLSMF series for >= 2 gauges" is met for the event window.

W6. Subsumption and bundling (no weight against).
- The main win is unavailable because NCEI does list this event, so p1 is the correct tier and is not subsumed by a main-win claim.
- The claim bundles exactly one event and two stations, with nothing extra counted.
- There are prior non-NCEI public reports: Parker's Luganville plot at 5.6 cm, and a GNS EGU25 abstract mentioning the Loyalty Islands. p1 asks only that NCEI lack the rows, so these do not defeat it. They corroborate both stations.
- I could not check whether another run already banked this same event/stations (outside my allowed view).

W7. Not weather or seiche? (low weight)
- Luganville shows coherent ~30-min oscillations, 0.06-0.08 m, starting at the ETA. That is far outside 120 days of background (0/400) and outside all control days, so a meteorological origin is implausible.
- Lifou's band is close to its normal 3-10 min background band, so local resonance excited by the tsunami and ordinary seiche look alike. Timing plus significance (W2) is all that separates them.

## Decision

Read literally, p1 is met by two distinct stations for a listed NCEI event, with no NCEI runup row for either station. My live re-fetch confirmed this, and it showed that NCEI does use these station names for other events. The full criterion's per-gauge standard, which the claim applies, also holds at both stations, including with the ComCat epicentre the criterion names. The weak points are the Lifou margin (R 5.24, per-gauge null p about 0.005 gated, 0.015 ungated) and the Luganville rule-based onset sitting 0.9 min inside the arrival tolerance under ComCat. These narrow the scope but do not break any clause, and Luganville by itself is a robust detection.

confirmed_scope: For NCEI tsunami event 5942 (2024-12-17 01:47:26 UTC, M7.3, Vanuatu Islands), two IOC SLSMF stations with no NCEI runup row for that event in the runups API re-fetched on 2026-10-24 (which lists only Port Vila and Lenakel) recorded band-passed (2-120 min) signals meeting the bank's per-gauge standard: Luganville (luga) clearly, with peak 0.078 m, R 8.4, rule-based onset 02:29 UTC and 0 of 400 random-time controls as large; and Lifou (lifo/lifo2, two sensors at one site) marginally, with peak 0.060 m, R 5.2, onset 02:21 UTC and 2 of 400 gated random-time controls as large; both onsets fall within 10 min of ETOPO1 shallow-water travel times from either the NCEI or the ComCat epicentre, and neither station detects on 11-12 control days.

pass: true
