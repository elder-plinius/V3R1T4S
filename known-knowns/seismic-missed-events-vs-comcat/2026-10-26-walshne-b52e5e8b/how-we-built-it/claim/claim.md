# Claim (partial win p1)

**Claim (one sentence):** an earthquake at 2024-12-09T23:20:13.27 UTC, 39.1635 N, 119.0459 W, depth 7.0 km, local
magnitude 1.59-1.72, is listed in neither USGS ComCat nor the ISC bulletin nor the published catalogue of the sequence.
- **Event:** an aftershock 11.7 min after the 2024 Mw 5.7 Parker Butte, Nevada earthquake (ComCat nn00888580).
- **Location:** 8 P/S picks on 5 public stations (RMS 0.179 s, horizontal error 3.45 km).
- **Magnitude estimates:** Wood-Anderson ML 1.590 (8-station median), or 1.627 over the 4 stations where the event
  exceeds the coda by 2x or more; 1.680 calibrated; 1.723 relative to 10 co-located ComCat ml events.
- **Completeness:** it is >= Mc - 0.3 for every regional completeness estimate computed (Mc 1.0-1.8: maximum curvature +
  0.2, live ComCat, three 5-year windows, 20-100 km).

**Target id:** seismic-missed-events-vs-comcat

**Partial win claimed:** p1 (verbatim, bank): "A missed event of magnitude >= Mc - 0.3 with the same location-quality requirements, in a ComCat-authoritative network region (not offshore)."

p1 takes the main criterion's location-quality requirements, and the main criterion also sets the absence, null,
blast and enhanced-catalogue conditions. The main criterion is quoted verbatim below. The main win (M >= Mc) is NOT
claimed: the claimant's rule needs M >= the largest Mc of the table (1.8).

**Success criterion of the main win (verbatim, bank; for p1's "same location-quality requirements" and the other checks):**
A saved event package (origin time, location, depth, local magnitude with method, >= 8 P/S picks on >= 4 public stations, FDSN request URLs on service.earthscope.org, detection code) such that: the skeptic's independent re-location (e.g. NonLinLoc/HypoInverse-style grid search) gives RMS <= 0.3 s and horizontal error <= 5 km; the detector run on a null set (the same continuous data with station traces circularly time-shifted against each other by >= 10 min, or time-reversed) yields an expected false count < 0.05 over the searched span at the candidate's statistic; the magnitude is >= the regional ComCat completeness magnitude Mc computed by the skeptic (maximum curvature + 0.2) from a live ComCat query for that region over the 5 surrounding years; not a quarry blast (daytime-cluster and S/P amplitude checks; ComCat eventtype filters); and a live ComCat query (and the ISC bulletin if reachable) re-fetched immediately before claiming returns no event within +/- 30 s and 50 km. Must not be inside the space-time window of a published enhanced catalogue (e.g. QTM Southern California, Ross et al. 2019) unless absent there too.

## Detector and searched span
- **Search:** a matched filter on 8 public NN vertical channels (YER, PNT, BFC, WASH, REDF, BMHS, CMK6, KVN). The
  templates are 385 of the 415 ComCat events (M < 4, within 20 km) of the search span; the other 30 were dropped for
  having fewer than 3 stations at SNR >= 3.
- **Searched span:** 2024-12-09T23:13:31Z to 2024-12-12T23:08:31Z (mainshock + 5 min to + 72 h).
- **Statistic:** the network-mean normalised CC (NCC) of the detecting template nn00890362: 0.6705 (station CCs at the
  exact lag: PNT 0.8370, YER 0.6857, BFC 0.6549, KVN 0.5045).
- **Null (the criterion's design):** 600 whole-day controls (400 on 2024-12-10..12, 200 on 2024-12-09). Stations 2-8 are
  circularly shifted by >= 10 min, and the full pipeline runs on each control.
  - **Result:** the best control reaches 0.6121, and no control reaches 0.6705.
  - **Expected false count:** 0 x 3.0 / 600 = 0 over the 3-day span (95 % upper bound 0.015).
  - **Per-control maxima:** the raw maximum NCC of every control is shipped (data/null_per_control_max.csv). The best
    on 2024-12-09 is 0.5351.
- **Early-hours sensitivity (stated, not the criterion's null):** the first 2 h of the span are the busiest. A null
  confined to them uses 3,000 controls with sample-level circular shifts inside the window (code/early_null.py).
  - **Result:** 1 of 3,000 controls reaches the event's 0.6706 (the best is 0.6887).
  - **Scaled to the 72-h span:** expected false count 1 / 3000 x 36 = 0.012, which is below 0.05.
- **Disclosure, detector numerics:** an earlier version of this detector used float32 FFTs with running-sum window
  norms. Near the mainshock, that gave spurious CC values (a panel reviewer found one of 0.705 against a true 0.189).
  This package uses float64 FFT numerators and computes each window's norm directly. A direct float64 Pearson check
  agrees to < 1e-11.
  - **Unchanged:** the event's NCC (0.6705) and, on 2024-12-10..12, the best control (0.6121) and the declustered
    detection count (13,888).
  - **Changed:** the 2024-12-09 control values (best 0.5609 to 0.5351; declustered detections 3,926 to 1,466) and the
    numbers derived from the real detections (the daytime table: n 1831 / 0.338 to n 1821 / 0.334).
- **Rerun:** code/null_full.py and code/early_null.py rerun all of it from public data (REPRODUCE.md section 6).

## ComCat-authoritative region
- **Geoserve point query** at the epicentre (data/point_v7.json):
  https://earthquake.usgs.gov/ws/geoserve/regions.json?latitude=39.1635&longitude=-119.0459&type=authoritative returns
  one authoritative region, network NN ("REN", the Nevada Seismological Laboratory, an ANSS regional network).
- **Network:** every ComCat event within 50 km in 2024-12-09..12 has net and locationSource "nn".
- **Setting:** on land in western Nevada, not offshore.

## Status source (bank)
https://earthquake.usgs.gov/fdsnws/event/1/ (the live ComCat FDSN event service).
- **Scout record:** the service page was fetched at 2026-10-26T17:29:27Z, HTTP 200 (data/comcat_status.html; logged in
  data/fetchlog_absence.jsonl).
- **Live absence queries:** the URLs are in REPRODUCE.md section 5. On 2026-10-26 at 17:29:28Z and again at 19:13:26Z,
  ComCat returned the header only, including with includedeleted=true. ISC returned HTTP 204. The responses and their
  sha256 are in data/ and data/fetchlog_absence.jsonl.
- **Nearest ComCat events in time:** nn00888575 at 23:18:12.80 (ml 2.6, 120 s earlier) and nn00888578 at 23:21:19.90
  (ml 2.3, 67 s later).

## Enhanced catalogues
- **The only published catalogue of this sequence:** Bogolub and Trugman (2025), "Parker Butte Earthquake Catalog",
  Zenodo doi:10.5281/zenodo.15644553, CC BY 4.0 (data/Parker_Butte_Catalog.csv). It covers 1 Dec 2024 to 10 May 2025
  and goes with Bogolub et al. (2026), SRL, doi:10.1785/0220250203.
  - It is a GrowClust relocation of the Nevada Seismological Laboratory's analyst-reviewed catalogue, and all its events
    share ComCat ids.
  - It has no event within +/-30 s of this one.
- **Trugman (2024), SRL 95, 3737-3745:** relocation, 2008-2023; ends before this window.

## History (disclosed)
- **Run 2026-10-23-1839:** found and selected the event; panel 2/3 (REPRODUCE failed: the full null could not be rerun).
- **Run 2026-10-24-0604:** the same event, picks and location, with standalone scripts; panel 2/3 again.
  - **NOVELTY and CRITERION passed.**
  - **REPRODUCE failed** on two package defects: the float32 detector artefact above made the stated 2024-12-09 control
    summary irreproducible, and a side statement (a 9-pick RMS) used a REDF S pick that was not shipped.
- **Run 2026-10-26-1727 (this package):** the same event, picks, location and magnitudes. Changes:
  - **Detector:** float64 numerics; the full null was rerun, and the per-control maxima are shipped.
  - **Early-hours sensitivity:** added as a pre-registered check.
  - **Side statements:** the 9-pick statement and the template-free STA/LTA statement are dropped.
  - **Template wording:** corrected (385 of 415).
  - **Absence queries:** refetched before the panel, with logs and responses shipped.

## Files
- **event.json:** origin, location, residuals, picks, magnitudes with methods and inputs, detection, null, checks, the
  event-window URLs and station coordinates.
- **picks.csv:** the 8 picks.
- **REPRODUCE.md:** a command for every number.
- **Scripts (code/):**
  - locate.py: relocation.
  - mag_check.py: magnitudes.
  - mc_table.py: Mc.
  - checks.py: S/P, local time, teleseisms, event types, the enhanced catalogue and the region.
  - blast_table.py: the daytime table.
  - null_full.py: detection and the full null.
  - early_null.py: the early-hours sensitivity.
- **Waveforms:**
  - The event: data/cand_173378641275_NN.*.mseed.
  - 6 calibration and 10 co-located events: data/evwin/.
  - StationXML responses: data/resp_NN.*.xml.
- **Detector and null data:**
  - data/templates.json: the templates.
  - data/null_jobs.json and data/null_d9_jobs.json: the control jobs.
  - data/null_summary.txt and data/null_per_control_max.csv: the null output.
  - data/early_summary.txt and data/early_per_control_max.csv: the early-hours output.
  - data/real_detections.json and data/detections_within_30s.json: the real detections.
- **Queries and logs:**
  - data/mc_*.csv and data/mc_gate.json: the Mc queries and the location validation.
  - Absence, geoserve, teleseism and event-type queries: data/*.csv and data/*.json.
  - Request logs: data/fetchlog_*.jsonl and data/evwin/_fetchlog.jsonl.
