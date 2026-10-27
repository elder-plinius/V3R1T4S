# REPRODUCE skeptic verdict: claim 2026-10-26-1727 (seismic-missed-events-vs-comcat, partial win p1)

context: subagent (fresh Claude Code Agent context, sees only claim/)

Scope: I read only claim/ and worked in work/. I wrote my own checkers from the stated definitions before reading
claim/code/. Then I ran the author's code on a copy (work/claim_copy/) and compared its outputs with the shipped files
byte for byte. Network use was one plain GET per URL with a V3R1T4S User-Agent and no retries. Every request is logged
in work/fetchlog_days_skeptic.jsonl, work/evwin_refetch/_fetchlog.jsonl and work/live/fetchlog.jsonl.

## Definitions checked

The p1 criterion, verbatim from claim.md:

> "A missed event of magnitude >= Mc - 0.3 with the same location-quality requirements, in a ComCat-authoritative
> network region (not offshore)."

The main criterion, which supplies the requirements p1 refers to:

> "the skeptic's independent re-location (e.g. NonLinLoc/HypoInverse-style grid search) gives RMS <= 0.3 s and
> horizontal error <= 5 km; the detector run on a null set (the same continuous data with station traces circularly
> time-shifted against each other by >= 10 min, or time-reversed) yields an expected false count < 0.05 over the searched
> span at the candidate's statistic; the magnitude is >= the regional ComCat completeness magnitude Mc computed by the
> skeptic (maximum curvature + 0.2) from a live ComCat query for that region over the 5 surrounding years; not a quarry
> blast (...); and a live ComCat query (and the ISC bulletin if reachable) re-fetched immediately before claiming returns
> no event within +/- 30 s and 50 km."

## 1. Data provenance

- **Day files:** I refetched all 32 HHZ day files myself (work/scripts/fetch_days.py). All 32 sha256 hashes and byte
  counts are identical to claim/data/fetchlog_dayfiles.jsonl. None of the files has a gap.
- **Event windows:** I refetched the 8 event windows (claim/event.json `waveform_urls_event_window`). They are byte-identical
  to claim/data/cand_173378641275_NN.*.mseed. Their HHZ samples also equal the day-file samples.
- **Calibration and co-located windows:** all 128 HHZ traces in claim/data/evwin/ are sample-identical to the day files.
- **StationXML:** I refetched the 8 live responses. They agree with claim/data/resp_NN.*.xml to 1e-16 (1-15 Hz, all
  channels).
- **Enhanced catalogue:** I refetched the Zenodo catalogue (record 15644553: Bogolub and Trugman, CC BY 4.0). Its
  sha256 is identical to claim/data/Parker_Butte_Catalog.csv. The nearest catalogue event is 66.7 s from the origin, so there is
  none within +/-30 s.

## 2. Picks: own AIC re-pick (work/scripts/my_picks.py)

- **Method:** Maeda AIC on causal 4-pole 2-15 Hz traces. The search windows are +/-2 s and +/-3 s around arrivals
  predicted from the template's ComCat hypocentre, not from the claimant's picks.
- **Result:** all 8 picks are reproduced within 0.01 s.
- **Acceptance ratios:**
  - P: BFC 4.0, KVN 8.9, PNT 10.0 (each >= 3).
  - S: BFC 7.6, KVN 3.3, PNT 7.5, WASH 2.5, YER 2.6 (each >= 2).
- **Count:** 8 picks on 5 public stations, so the >= 8 on >= 4 requirement is met.

## 3. Relocation: own grid search (work/scripts/my_locate.py)

| Model | Best node | RMS | Claimant-style "RMS <= best + 0.1 s" extent | HypoInverse-style ERH (1-sigma semi-major axis) | NonLinLoc-style 68 % region (max horizontal distance) |
|---|---|---|---|---|---|
| Homogeneous Vp 6.0 / Vs 3.46 km/s (the claimant's model, own code) | 39.1635 N, 119.0459 W, 7.0 km; origin 23:20:13.27 | **0.1787 s** | 3.446 km | 1.04 km (sigma = max(RMS, 0.1)); 1.48 km (unbiased sigma); 1.75 km (sigma = 0.3 s) | 1.41-2.39 km (sigma 0.15-0.3 s) |
| Layered Basin-and-Range-like 1D (TauP, own model) | 39.1635 N, 119.0559 W, 7.0 km | **0.2234 s** | 4.531 km | 1.32-1.87 km | 2.39-3.45 km |

- **Residuals:** with the homogeneous model they are identical to claim/event.json.
- **Distance to the template epicentre:** 1.41 km.
- **Author's code:** claim/code/locate.py prints the same numbers.
- **Verdict:** RMS <= 0.3 s and horizontal error <= 5 km under every definition and both models. **Pass.**

## 4. Magnitude: own Wood-Anderson ML (work/scripts/my_ml.py)

I followed claim/event.json `wa_method`: response removed, Wood-Anderson simulated, Hutton and Boore (1987) attenuation, and r
taken as hypocentral distance including station elevation.

| Quantity | Mine | Claimed |
|---|---|---|
| WA ML, median of 8 stations | 1.590 | 1.590 |
| Calibration offset over 6 events | 0.0895 | 0.0895 |
| Calibrated ML | 1.680 | 1.680 |
| M_coloc over 10 events | 1.723 | 1.723 |
| Median over stations with event/noise >= 2 | 1.628 (my noise window) | 1.627 |

- **Station values:** every station ML agrees to 0.001.
- **Author's code:** claim/code/mag_check.py compute reproduces the claimed values exactly.
- **M_rel:** no shipped script recomputes it; the value is read from claim/event.json. I recomputed 2.45 from the author's
  prepped 20 Hz data. It is non-binding, because M_cons takes the minimum.

## 5. Mc (work/scripts/my_mc.py)

- **Shipped CSVs:** my own maximum-curvature + 0.2 code reproduces all 24 cells of the REPRODUCE.md table.
- **My live ComCat queries:**

  | Query | Mc (floor / round binning) |
  |---|---|
  | Event-centred, 50 km, 2022-06-09 to now | 1.7 / 1.8 |
  | Event-centred, 50 km, 2019-12-09 to 2024-12-09 | 1.3 / 1.3 |
  | Mainshock-centred, 20 km, 2022-06 to now | 1.7 / 1.8 (vs the shipped CSV: 2 new events, 0 missing) |

- **p1 gate:** the largest Mc is 1.8, so the gate is Mc - 0.3 = 1.5. The smallest magnitude estimate is 1.590 >= 1.5.
  **Pass.**
- The main win (M >= Mc) is not claimed, and is not met against Mc 1.8.

## 6. Null: exhaustive, all 600 + 3000 controls

### 6a. My own implementation (work/scripts/mynull.py, run_mynull.py)

- **Design:**
  - 4-pole zero-phase 2-8 Hz filter, 20 Hz grid on absolute UTC (calibrated against the stored template waveforms;
    correlation >= 0.99998).
  - Pearson CC with float64 chunked FFT numerators and directly computed window norms.
  - Circular CC traces. Each control is NCC(t) = mean_s CC_s((t + m_s - k_s) mod N), which equals the CC on circularly
    rolled traces.
  - I check all 600 jobs on all 385 templates.
- **Event:** NCC 0.67056 for template nn00890362 at 23:20:12.75. Station CCs: PNT 0.8369, YER 0.6860, BFC 0.6548,
  KVN 0.5045.
- **Per-control maxima (work/mynull_per_control_max.csv) vs claim/data/null_per_control_max.csv:**
  - Agreement: max absolute difference 0.0028, mean 8e-5. 597 of 600 rows have the same template and time.
  - The differences come from the author's whole-day 5 % cosine taper, which I did not apply.
  - Best values: 0.612052 (12-10..12) and 0.535149 (12-09).
  - **Controls >= 0.6705: 0.** The margin, 0.058, is 20 times my largest discrepancy.
- **EFC:** 0 x 3.0 / 600 = 0 (95 % upper bound 0.015). Using only the 400 controls on 12-10..12, the upper bound is
  0.0225. Both are below 0.05.

### 6b. My own early-hours null (work/scripts/run_myearly.py)

- **Setup:** the 2 h window, circular within it, with the shifts taken from claim/data/early_per_control_max.csv.
- **Result:** E2 0.67056. Best control 0.688698 (control 1220, nn00893224). **Exactly 1 of 3000 >= E2**, as claimed.
- **Agreement with the shipped file:** max difference 0.0076, at the 00:00 day boundary, because I prep per day. 2999 of
  3000 rows have the same template and time. The second-best control is 0.662, so no control flips.

### 6c. The author's code on a copy (work/claim_copy/), with 10 workers (the claimant used 12)

- **Commands:** `null_full.py prep / run 10 / summary`, then `early_null.py 10 3000`.
- **Byte-identical to the shipped files:**
  - claim/data/null_summary.txt and claim/data/null_per_control_max.csv (all 600 rows).
  - claim/data/real_detections.json (14677) and claim/data/detections_within_30s.json (29).
  - The 13888 and 1466 declustered detection counts.
  - claim/data/early_summary.txt and claim/data/early_per_control_max.csv (all 3000 rows).
- **Determinism:** the outputs do not depend on the worker count.
- **Author's code:** claim/code/checks.py and claim/code/blast_table.py reproduce every printed value (S/P 2.32, 15:20 PST, no
  teleseism, two explosions 49 km away, daytime fractions 0.348 and 0.334). I recomputed S/P, local time, teleseisms
  and the ComCat daytime histogram independently (work/scripts/my_small.py).

## 7. Absence and region (live, immediately before this verdict)

- **ComCat** (+/-30 s, 50 km, all types), at 2026-10-26T20:56:58Z: header only. Header only also with
  `includedeleted=true`, and with +/-60 s and 150 km.
- **ISC** (+/-30 s, 0.45 deg): HTTP 204.
- **Positive controls:** the same query shapes do return the known events.
  - ComCat returns nn00888575 at 23:18:12.8.
  - ISC returns the mainshock and the 23:18:13 NEIC event.
  - So the empty answers are real.
- **Authoritative region:** geoserve (claim/data/point_v7.json) gives NN/REN (ANSS), on land in Nevada.

## 8. Further checks of stated properties

- **Station coordinates:** I compared the live StationXML (work/live/resp/) with claim/picks.csv and
  claim/event.json `station_coordinates`. All 8 stations are identical in latitude, longitude and elevation.
- **The "< 1e-11 Pearson" statement:** no shipped mode runs this check, so I ran it myself (work/scripts/pearson_check.py).
  - I compared the author's `xcorr` on the author's prepped 2024-12-09 data with np.corrcoef on the raw 120-sample
    windows.
  - The check covers 1023 points over 8 stations and 32 templates. 223 of them are inside the FFT chunk that holds the
    mainshock.
  - Maximum error: 3.5e-12. **Confirmed.**
- **Calibration-event validation ("6 events within 0.86-2.39 km of ComCat"):** no command or pick times are shipped for
  this.
  - **The claimant's picks, rebuilt:** I rebuilt them from claim/data/mc_gate.json (origin + model travel time +
    residual) and relocated them with my locator, on a grid centred at the ComCat epicentre. All 6 locations, RMS
    values and offsets (2.39, 2.39, 2.39, 0.86, 1.41, 0.86 km) match exactly
    (work/scripts/calval_exact.py).
  - **Checking the rebuilt picks:** my own AIC picks on claim/data/evwin/ agree with them to <= 0.05 s, with two
    exceptions: nn00889115 CMK6 S (0.18 s) and nn00889009 BFC S (0.11 s).
  - **My picks, relocated:** with my own picks and my standard grid, the offsets are 0.98-2.65 km (the claimant's pick
    set) or 0.25-2.61 km (all my accepted picks). That reproduces the stated range approximately; it is a side
    statement and does not enter the criterion.
- **Network and templates:**
  - Network: all 419 events in claim/data/window_50km_alltypes.csv have net = locationSource = nn.
  - Template count: the ComCat events with M < 4 within 20 km of the mainshock, from mainshock + 5 min to + 72 h, number
    exactly 415. They are the same ids as the 385 templates plus the 30 dropped ones.
  - Template stations: every kept template has >= 3 stations, all with SNR >= 3. Every dropped entry has 0-2 such
    stations.
- **Early-null design:** all 3000 controls satisfy the design. Shifts are in [12000, 132000], and all 8 stations are
  pairwise >= 12000 samples apart in circular distance in N = 144000. The seed-drawn shifts reproduce exactly, because
  the CSV is byte-identical.
- **Region:** a live geoserve query at 2026-10-26 returned NN/REN (anss).

## Notes (non-blocking)

- **Day taper:** null_full.py applies a 5 % cosine taper to each whole day, which is 72 min at each end. The event at
  23:20 and the detecting template at 00:12 both lie in the tapered parts.
  - Normalised CC is barely affected; it explains my differences of at most 0.003.
  - It also explains why the template RMS is small and M_rel (2.45) is biased high, as the claim already says.
- **Null design:** 200 of the 600 controls are 12-09 whole days, which are mostly before the mainshock. The criterion is
  still met without them (upper bound 0.0225).

## Verdict

Every property and claimed value I could test reproduces from the saved files, from my own independent code and from
the author's code:
- picks;
- location and its error under standard definitions;
- magnitudes;
- the Mc table and the live Mc;
- the full 600-control null and the 3000-control early null, exhaustively, with no control flipping;
- live absence.

The author's code is deterministic and byte-identical to the shipped outputs. I found no mismatch, no missing object
and no non-determinism.

pass: true
