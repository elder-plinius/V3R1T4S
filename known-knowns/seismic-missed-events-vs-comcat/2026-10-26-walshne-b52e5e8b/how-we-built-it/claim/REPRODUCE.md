# REPRODUCE

Every number in claim.md and event.json can be rerun from this folder.
- **Software:** Python 3 with ObsPy, NumPy and SciPy (the claimant used Python 3.13, ObsPy 1.5.1, NumPy 2.5.4,
  SciPy 1.18.1). Run every script from the claim/ folder with `python -I`.
- **Public data only:** EarthScope dataselect and station services, USGS ComCat and geoserve, ISC, Zenodo.
- **Request logs:** data/fetchlog_*.jsonl and data/evwin/_fetchlog.jsonl record the claimant's requests (URL, UTC time,
  HTTP status, bytes, sha256).

| Number | Command | Runtime |
|---|---|---|
| location, RMS, horizontal error, residuals | `python -I code/locate.py` | seconds |
| magnitudes | `python -I code/mag_check.py compute` | about 1 min |
| Mc table | `python -I code/mc_table.py` | seconds |
| S/P, local time, teleseisms, event types, enhanced catalogue, region | `python -I code/checks.py` | seconds |
| daytime table | `python -I code/blast_table.py` | seconds |
| detection, full null, per-control maxima | `python -I code/null_full.py fetch / prep / run 12 / summary` | about 95 min |
| early-hours sensitivity | `python -I code/early_null.py 12 3000` (after `null_full.py fetch`) | about 7 min |

## 1. Waveforms and picks
1. **Event windows** ([2024-12-09T23:19:42, 23:21:12] UTC) at 8 stations: the URLs are in event.json
   (`waveform_urls_event_window`). The files as fetched are data/cand_173378641275_NN.*.mseed. NN.YER..HHE is constant
   (dead) in this window.
2. **The 8 picks** (picks.csv): Maeda AIC on 4-pole causal Butterworth 2-15 Hz traces (demean, 5 % taper).
   - **P on Z:** PNT, BFC, KVN.
   - **S on the horizontal envelope sqrt(N^2 + E^2):** PNT, BFC, KVN, WASH, YER (YER on N only).
   - **Acceptance:** an RMS ratio (1 s after / 1 s before) >= 3 for P and >= 2 for S.
   - **No other picks are used or claimed.**

## 2. Relocation: `python -I code/locate.py`
Use any 1D grid search or HypoInverse-style locator. The bar is RMS <= 0.3 s and horizontal error <= 5 km.
- **The claimant's model and grid:** in the script's docstring. Homogeneous Vp 6.0 km/s and Vs 3.46 km/s with station
  elevations; lat/lon +/- 0.5 deg in 0.01 deg around 39.1535 N, 119.0559 W; depth 0-20 km in 0.5 km; origin = mean
  residual.
- **Output:**

      picks 8 on 5 stations
      best node 39.1635 N 119.0459 W depth 7.0 km; origin 2024-12-09T23:20:13.27; RMS 0.1787 s; horizontal error 3.446 km (276 nodes within +0.1 s)
      residuals (s): BFC P -0.153, BFC S -0.059, KVN P +0.126, KVN S +0.153, PNT P -0.074, PNT S +0.331, WASH S -0.266, YER S -0.059

- **Horizontal error definition:** the largest distance from the best node to any node with RMS <= best + 0.1 s.
- **Template distance:** 1.41 km from the detecting template's ComCat epicentre (39.1535 N, 119.0559 W).
- **Validation:** the same picker and locator relocate 6 calibration events within 0.86-2.39 km of ComCat
  (data/mc_gate.json, `validation`; their windows are data/evwin/nn*_NN.*.mseed).

## 3. Local magnitude: `python -I code/mag_check.py compute`
- **Inputs:** event windows for the event, the 6 calibration events and the 10 co-located events (data/evwin/;
  `python -I code/mag_check.py fetch` refetches any that are missing), plus the StationXML responses
  (data/resp_NN.*.xml). The method is in the script's docstring and in event.json `magnitude`.
- **Output** (also written to mag_check_out.json):
  - **WA ML:** 1.590, the median of 8 stations.
  - **Calibration:** offset 0.089, the median (ComCat ml - WA ML) over nn00889312, nn00888992, nn00889115, nn00888959,
    nn00889068 and nn00889009. Calibrated WA ML 1.680.
  - **M_coloc:** 1.723, over the 10 nearest same-day ComCat ml events within 5 km (ids in the output).
  - **M_rel:** 2.45, from the detecting template's ml 1.5 plus the RMS ratio. It is biased high and listed only.
  - **M_cons** = min(M_rel, calibrated WA, M_coloc) = 1.680.
  - **Stations with event/noise WA amplitude >= 2** (YER, PNT, BFC, WASH): median ML 1.627.

## 4. Mc (maximum curvature + 0.2, 0.1 bins): `python -I code/mc_table.py`
The live ComCat queries (saved as data/mc_*.csv; times in data/fetchlog_comcat.jsonl):
https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=START&endtime=END&latitude=39.1675&longitude=-119.0238&maxradiuskm=R&eventtype=earthquake&orderby=time-asc&limit=20000

Each cell is floor binning / round binning (numpy's round half to even):

| R | 2020-01-01..2025-01-01 | 2021-01-01..2026-01-01 | 2022-06-01..query time |
|---|---|---|---|
| 20 km | 1.6 / 1.6 | 1.4 / 1.4 | 1.7 / 1.8 |
| 30 km | 1.6 / 1.6 | 1.4 / 1.4 | 1.7 / 1.8 |
| 50 km | 1.6 / 1.6 | 1.4 / 1.4 | 1.7 / 1.8 |
| 100 km | 1.6 / 1.0 | 1.6 / 1.0 | 1.3 / 1.3 |

p1 needs M >= Mc - 0.3, which is at most 1.5. The smallest magnitude estimate above, 1.590, clears it.

## 5. Absence (live)
- **ComCat** (+/-30 s fully covered; all types; 50 km):
  https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=2024-12-09T23:19:43&endtime=2024-12-09T23:20:44&latitude=39.1635&longitude=-119.0459&maxradiuskm=50
  - **Expected:** the header only. The claimant got the header only at 2026-10-26T17:29:28Z and 19:13:26Z, and also
    with `&includedeleted=true` (data/absence_comcat*.csv).
- **ISC:** https://www.isc.ac.uk/fdsnws/event/1/query?starttime=2024-12-09T23:19:43&endtime=2024-12-09T23:20:44&latitude=39.1635&longitude=-119.0459&maxradius=0.45&format=text
  - The claimant got HTTP 204 at 19:13:26Z.
- **Log:** all of these requests, with sha256, are in data/fetchlog_absence.jsonl.
- **Published catalogue:** data/Parker_Butte_Catalog.csv (Zenodo 10.5281/zenodo.15644553, Bogolub and Trugman 2025) has
  no event within +/-30 s (`code/checks.py`).

## 6. Detection and the null
### 6a. The full null (the criterion's design): `code/null_full.py`
Run these from claim/. They need about 2-3 GB of disk; `run 12` took about 95 min on the claimant's 14-core machine.

    python -I code/null_full.py fetch
    python -I code/null_full.py prep
    python -I code/null_full.py run 12
    python -I code/null_full.py summary

- **fetch:** downloads the 32 HHZ day files (8 stations x 2024-12-09..12) from EarthScope and logs each request in
  nullwork/wf/_fetchlog.jsonl. The claimant's fetch of the 32 files (URL, time, sha256) is data/fetchlog_dayfiles.jsonl.
- **prep:** zero-phase 2-8 Hz, decimate to 20 Hz, gap masks.
- **run:** runs the full pipeline (all 385 templates in data/templates.json, archived at doi:10.5281/zenodo.23679540) on the 4 real days and on all 600 control
  jobs (data/null_jobs.json: 400 on 2024-12-10..12; data/null_d9_jobs.json: 200 on 2024-12-09).
  - **Control design:** stations 2-8 circularly shifted by distinct whole minutes in [10, 1430], >= 10 min apart (shifts
    in samples at 20 Hz).
  - **Numerics:** each station's normalised cross-correlation has a float64 FFT numerator, and each 120-sample window's
    norm is computed directly. A direct float64 Pearson computation agrees to < 1e-11 at 200 random points, including
    50 inside the FFT chunk that holds the mainshock.
- **summary:** prints the event's NCC, each control set's best value and count >= the event NCC, the expected false
  count, and the raw per-control maxima. It writes nullwork/null_per_control_max.csv, nullwork/real_detections.json and
  nullwork/detections_within_30s.json (copies are in data/).
- **The claimant's output (data/null_summary.txt):**

      event: best real detection within 0.5 s of 2024-12-09T23:20:12.75: NCC 0.6705 (template nn00890362, 23:20:12.75)
      null     controls 400, declustered detections 13888, best 0.6121, >= 0.6705: 0
      null_d9  controls 200, declustered detections 1466, best 0.5351, >= 0.6705: 0
      ALL: controls 600, best_control 0.6121, count >= event NCC 0, EFC over the 3.0-day span = 0 x 3.0 / 600 = 0.0000 (95% upper bound 0.0150)
      raw per-control maxima: best 0.6121 (null 2024-12-10), 12-09 best 0.5351, 12-10..12 best 0.6121, >= event NCC: 0; written to null_per_control_max.csv
      real detections: 14677 over the 4 days (real_detections.json); 29 within +/-30 s of the event (detections_within_30s.json)

- **The 12-09 best, unrounded:** 0.535149 (control job shown first among null_d9 rows in data/null_per_control_max.csv,
  template nn00888600 at 2024-12-09T16:56:04.85), so it prints as 0.5351.
- **The event's station CCs at the exact aligned lag:** PNT 0.8370, YER 0.6857, BFC 0.6549, KVN 0.5045; their mean is
  0.6705.

### 6b. Early-hours sensitivity (a stated check, not the criterion's null): `python -I code/early_null.py 12 3000`
- **Design (in the script's docstring):**
  - **Window:** 2024-12-09T23:13:31 to 2024-12-10T01:13:31 (the first 2 h of the span), 144,000 samples at 20 Hz.
  - **Controls:** 3,000, seed 20261026. YER is fixed, and the other 7 stations are circularly shifted inside the window
    by integers in [12000, 132000], with all 8 pairwise >= 12,000 samples (10 min) apart.
  - **Statistic:** each control's maximum NCC over all samples and all 385 templates.
- **Output (data/early_summary.txt, data/early_per_control_max.csv):**

      E2 (event, unshifted, +/-0.5 s of 2024-12-09T23:20:12.75): 0.6706 (template nn00890362)
      best control 0.6887; controls >= E2: 1; EFC_early = 1 / 3000 x 36 = 0.0120

## 7. Blast and other checks: `python -I code/checks.py` and `python -I code/blast_table.py`
- **S/P peak ratio** at PNT (horizontal envelope over [S, S + 2 s] / |Z| over [P, P + 1 s], causal 2-15 Hz): 2.32.
- **Depth:** 7 km.
- **Local time:** 15:20 PST.
- **Daytime-cluster check** (data/blast_table_out.txt), fraction of events in 08-17 PST against 0.417 for a uniform
  spread:
  - ComCat earthquakes within 50 km, 2020-2025: 0.348 (n 2059).
  - The matched filter's added detections in the search span: 0.334 (n 1821).
  - No daytime excess.
- **ComCat event types within 50 km:**
  - Centred on the mainshock, 2020-2025 (data/all_types_2020_2025_50km.csv): earthquakes only.
  - Centred on this event, 2019-12-09 to the query time (data/alltypes_5y_event_centred.csv): two explosions (2025-06-28
    and 2025-06-30, M2.0 and 1.9, 13 km NNW of Stagecoach, 49.1-49.3 km away).
- **The mainshock:** ComCat's preferred id nn00888580 (2024-12-09T23:08:31.577 UTC, mwr 5.71).
- **Teleseisms:** no ComCat global M >= 5.5 event has a TauP P-type arrival at YER within +/-60 s
  (data/global_m55_window.csv).
- **Authoritative region:** geoserve returns NN (REN, ANSS) at the epicentre (data/point_v7.json).
- **Nearby detections:** data/detections_within_30s.json lists every real detection within +/-30 s. Apart from the event
  (23:20:12.40-13.20, best 0.6705), only a weaker uncatalogued group 25 s earlier is listed (23:19:47.40-47.85,
  NCC <= 0.383).
