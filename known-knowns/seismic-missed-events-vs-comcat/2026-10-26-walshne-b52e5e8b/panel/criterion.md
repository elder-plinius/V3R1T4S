# CRITERION skeptic: seismic-missed-events-vs-comcat, partial win p1

context: subagent (fresh Claude Code Agent context, sees only claim/)

- **Claim:** the event at 2024-12-09T23:20:13.27 UTC, 39.1635 N, 119.0459 W, is a missed event that meets p1.
- **p1, verbatim:** "A missed event of magnitude >= Mc - 0.3 with the same location-quality requirements, in a
  ComCat-authoritative network region (not offshore)."
- **What p1 brings in from the main criterion:** the package and pick count, RMS and horizontal error, the null (EFC <
  0.05), the blast checks, live ComCat/ISC absence and the enhanced-catalogue condition.
- **Main win:** not claimed, and not met. My Mc is 1.8 and no magnitude estimate reaches it.
- **Working copy:** I copied claim/ to work/cc/ and ran everything from the copy.
- **Live requests:** one plain GET each, with a V3R1T4S User-Agent; logged in work/live/_fetchlog.jsonl.

## Clause by clause

| Clause | My check | Result |
|---|---|---|
| Package: origin, location, depth, ML with method, >= 8 P/S picks on >= 4 public stations, EarthScope URLs, detection code | claim/event.json, claim/picks.csv, claim/code/ | 8 picks (3 P, 5 S) on 5 NN stations; URLs on service.earthscope.org; code shipped. **Met** |
| Picks are real | Plots (work/picks_overview.png, work/picks_zoom.png); independent kurtosis and STA/LTA re-pick (work/repick.py, work/repick.json); template moveout cross-check | All 8 picks show onsets. **Met** (detail 1) |
| Independent relocation: RMS <= 0.3 s, horizontal error <= 5 km | My own locator (work/reloc.py, work/reloc_out.json) with layered and homogeneous models and conventional errors | Layered Great Basin model: RMS 0.167 s, 68 % ellipse semi-major axis 1.84 km (90 %: 2.62 km). **Met** (detail 2) |
| Null EFC < 0.05 over the span at the candidate statistic | Event NCC rerun from refetched day files; **time-reversed null** over all 4 days (the criterion's alternative design); spot-check of 40 of the claimant's 600 controls (work/nullwrap.py, work/spot_compare.py) | Event NCC 0.6705 reproduced. Over 4 reversed days the maximum NCC is 0.445 and none reaches 0.6705. Spot controls: see detail 3. **Met** |
| Magnitude >= Mc - 0.3, with Mc computed by the skeptic | Live ComCat query (work/live/mc_50km_2019-06-09_now.csv, work/mc_mine.py); magnitude recomputed, plus SNR-gated and noise-corrected variants (work/mag_mine.py) | The highest Mc of any window or radius is 1.8, so the bar is 1.5. Every ComCat-ml-equivalent estimate is 1.58 to 1.72. **Met, with a thin margin** (detail 4) |
| Not a quarry blast | Daytime fraction, S/P, event types | **Met** (detail 5) |
| Live ComCat absence (+/-30 s, 50 km); ISC | Refetched at 2026-10-26T19:27:05-09Z | ComCat returned the header only, also with includedeleted=true; ISC returned HTTP 204. **Met** |
| Enhanced catalogue | Zenodo 15644553 md5; checks.py; one Zenodo search | No event within +/-30 s. **Met** (detail 6) |
| ComCat-authoritative region, not offshore | Geoserve refetched at 19:27:10Z (work/live/geoserve.json) | NN (REN, ANSS), on land in western Nevada. **Met** |

## Details

### 1. Picks
- **Template moveout cross-check.** Add the template moveouts `m` (claim/data/templates.json, nn00890362) to the aligned
  detection time 23:20:12.75.
  - The P picks then sit 0.91 s (BFC), 0.92 s (PNT) and 0.93 s (KVN) after each window start.
  - This constant 0.92 s lead confirms all three P picks against the matched-filter alignment to within 0.02 s.
- **Re-pick within +/-1.5 s of each pick.**
  - Kurtosis-rise and STA/LTA peaks fall within 0.0-0.22 s for BFC P, BFC S, KVN S, PNT P, PNT S and YER S.
  - For KVN P and WASH S they fall 0.65 s later. KVN P is emergent; WASH S is the weakest pick, with an RMS ratio of
    2.07 over 2 s and 5 s windows.
- **Visual check.** On the plots, both of those picks have real arrivals, so the count of 8 holds.
- **Weakest picks:** WASH S and YER S (a single horizontal, because YER HHE is dead).

### 2. Relocation (work/reloc.py)
- **Method:**
  - Ray shooting in flat layers, with head waves.
  - A 0.005 deg grid and 0-20 km depth.
  - Origin time = the mean residual.
  - Errors: linearised covariance with sigma^2 = SSR/(n-4), plus a grid-PDF (NonLinLoc-like) horizontal credible
    extent.
- **Primary result, layered model** (0-3 km Vp 5.2, 3-15 km 6.0, 15-30 km 6.4, then 7.9; Vp/Vs 1.73):
  - Epicentre 39.165 N, 119.050 W, depth 3.5 km, 0.39 km from the claimed epicentre.
  - RMS 0.167 s.
  - 1-sd semi-major axis 1.22 km; 68 % ellipse 1.84 km; 90 % ellipse 2.62 km; PDF 68/90 % extent 1.72/2.91 km.
  - The claimant's error definition (the RMS + 0.1 s contour) gives 4.10 km.
- **Other models:**
  - Slow layered model: RMS 0.250 s, 68 % ellipse 2.67 km.
  - Homogeneous 5.8/1.70: RMS 0.137 s, 68 % ellipse 1.67 km.
  - Homogeneous 6.2/1.70: RMS 0.279 s, 68 % ellipse 3.63 km.
  - Homogeneous 6.2/1.78: RMS 0.188 s, 68 % ellipse 2.07 km.
  - Homogeneous 6.0/1.734: RMS 0.136 s, 68 % ellipse 1.67 km.
  - Homogeneous 5.8/1.78 fails (RMS 0.453 s), but that is a poorly fitting Vp/Vs, not a defect of the picks.
- **Pick sensitivity.** Moving KVN P and WASH S to my later kurtosis times gives RMS 0.24-0.33 s and a 68 % ellipse of
  2.9-4.2 km. The KVN P residual then grows to +0.6 s, so the claimant's earlier onset is the more consistent pick.
- **Geometry.** The azimuthal gap is 172 deg, and KVN is the only station to the east. The criterion has no gap clause,
  so this is noted only.

### 3. Null
- **Data.** All 32 refetched HHZ day files match the sha256 values in claim/data/fetchlog_dayfiles.jsonl.
- **Shipped maxima.** claim/data/null_per_control_max.csv has 600 rows (400 `null`, 200 `null_d9`). The highest is
  0.6121, and none reaches 0.6705.
- **Pipeline.** The claimant's float64 pipeline (claim/code/null_full.py), run unchanged in Pool(4), reproduces the event
  at NCC 0.6705 (template nn00890362, 23:20:12.75).
- **Time-reversed null.** The criterion names "or time-reversed" as an alternative null. Reversing every station's day
  together keeps the post-mainshock non-stationarity across stations, which whole-day shifted controls dilute.
  - Over the 4 reversed days there are 20 declustered detections, with a maximum NCC of 0.445 (on 2024-12-12; 0.433 on
    2024-12-09, which includes the mainshock coda).
  - None reaches 0.6705, so the observed false count over the span is 0.
- **Spot-check of the claimant's controls:** I re-ran 40 of the claimant's 600 controls with a random draw (20 from `null_d9`, 20 from
  `null`).
  - All 40 per-control maxima match claim/data/null_per_control_max.csv exactly (max |diff| 0.0).
  - The best of the 40 is 0.5381, and none reaches 0.6705 (work/spot_compare_out.txt).
- **Early-hours sensitivity** (the claimant's own; not re-run by me):
  - 1 of 3,000 controls reaches the event's value, giving EFC 0.012.
  - The point estimate is below 0.05, but a 95 % upper bound on one exceedance (about 4.74/3000 x 36 = 0.057) would not
    be. The criterion asks for the expected false count, so this does not block. It is recorded here.

### 4. Magnitude against my Mc
- **Mc query.** Live ComCat, centred on the event, 50 km, eventtype=earthquake, 2019-06-09 to now: 3,042 events,
  fetched 2026-10-26T19:27:13Z. I subset it to 10/20/30/50 km and to several windows.
- **Mc results** (maximum curvature + 0.2, 0.1 bins):
  - The 5-year window centred on 2024-12-09, clipped at today (2022-06-09..now), gives Mc 1.7 with floor binning and
    1.8 with round binning, at 20, 30 and 50 km.
  - The following-years window and the last 5 years give the same.
  - The preceding 5 years give 1.3-1.4.
  - **The maximum over all variants is 1.8, so Mc - 0.3 = 1.5.**
- **Fragile bin.** The round-binning mode rests on bins 1.5 and 1.6, with 234 and 241 events. That only decides Mc 1.7
  against 1.8, so the bar is 1.4 or 1.5. Mc cannot reach 1.9: the 1.7 bin has 154 events against 241 in the 1.6 bin.
- **Claimant's values reproduced exactly:** raw WA ML 1.590, calibrated 1.680, M_coloc 1.723, SNR >= 2 median 1.627.
- **Skeptic variants** (Mc is in ComCat ml units, so the comparable numbers are calibrated or co-located):

| Variant | Value |
|---|---|
| SNR >= 2, noise-corrected (sqrt(A^2 - N^2)), calibrated | 1.696 |
| SNR >= 1.5, noise-corrected, calibrated | 1.581 |
| M_coloc on SNR >= 2 stations, noise-corrected | 1.699 |
| M_coloc on SNR >= 1.5 stations, noise-corrected | 1.663 |
| Co-located ml 1.4 event (nn00889287), the closest in size | 1.78-1.86 |

- **All ComCat-unit estimates are 1.58-1.72, so all are >= 1.5. The margin is 0.08-0.22.**
- **Caveat.** The uncalibrated Hutton-Boore WA ML falls to 1.491 (SNR >= 1.5, noise-corrected). That is just below
  1.5, but it is not on ComCat's ml scale.

### 5. Blast
- **Local time.** 15:20 PST is daytime. However, ComCat earthquakes within 50 km before the sequence (2019-06..2024-12-08)
  have a daytime (08-17 PST) fraction of 0.277, below the uniform 0.417. The claimant's added-detection table is 0.334.
  There is no daytime excess.
- **S/P (horizontal S peak / vertical P peak):** PNT 2.32, BFC 2.67, KVN 0.74 (at 83 km, not diagnostic).
- **ComCat event types within 50 km since 2019-06:** 3 explosions, all at least 45 km away.
- **Waveform similarity.** The event matches a catalogued earthquake 1.4 km away with CC 0.67, 11.7 min after the Mw 5.7
  mainshock.

### 6. Absence and enhanced catalogue
- **Wider ComCat window.** A ComCat query of +/-180 s with no location limit returns only nn00888575 (-120 s),
  nn00888578 (+67 s) and nn00888581 (+134 s). No mislocated or regional event explains the picks.
- **Published catalogue.** The md5 of claim/data/Parker_Butte_Catalog.csv equals Zenodo's checksum
  (f7e02c8ff479187fccef028bceb4a9f4), and the catalogue has nothing within +/-30 s.
- **Other catalogues.** A Zenodo search for "parker butte earthquake" finds no other catalogue of the sequence. I did not
  check other repositories.

## Verdict
- **Each clause is met under a literal reading,** using my own Mc, relocation, absence fetches and an independent
  time-reversed null.
- **Main residual risk: the magnitude margin.** It is 0.08-0.22 ML above Mc - 0.3 = 1.5, and it depends on the
  ComCat-ml-equivalent calibration. This does not fail the literal criterion.
- **Not a subsumed win:** the main win (M >= Mc = 1.8) is not met, so p1 is the right and highest tier.

confirmed_scope: An earthquake at 2024-12-09T23:20:13 UTC near 39.165 N 119.050 W (8 P/S picks on 5 NN stations; my layered-model relocation RMS 0.17 s, 68 % horizontal error 1.8 km), with a ComCat-ml-equivalent magnitude of 1.58-1.72, is absent from live ComCat (+/-30 s, 50 km, fetched 2026-10-26T19:27Z), from ISC (HTTP 204) and from the Bogolub and Trugman (2025) Parker Butte catalogue, has no null detection at its NCC of 0.6705 in my time-reversed null (maximum 0.445 over 4 days) or in the claimant's circular-shift null (0 of 600 controls; 40 spot-checked by me, agreeing), and is at or above my Mc - 0.3 = 1.5 (Mc 1.8 by maximum curvature + 0.2 from live ComCat within 50 km, 2022-06-09 to 2026-10-26) in the NN-authoritative onshore region, which meets partial win p1 of seismic-missed-events-vs-comcat and not the main win.
pass: true
