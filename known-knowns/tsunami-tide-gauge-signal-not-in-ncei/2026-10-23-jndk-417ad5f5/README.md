# NCEI tsunami event 5942 (Vanuatu, 2024-12-17): gauge observations at Luganville and Lifou missing from NCEI's runup table

Target: `tsunami-tide-gauge-signal-not-in-ncei`, partial win **p1** ("Gauge observations (amplitude, arrival) for a
listed NCEI event at >= 2 gauges where NCEI has no runup rows for those stations.").

## What

For NCEI tsunami event 5942 (2024-12-17 01:47:26 UTC, M7.3, Vanuatu Islands), two IOC SLSMF stations with no NCEI runup row for that event in the runups API re-fetched on 2026-10-24 (which lists only Port Vila and Lenakel) recorded band-passed (2-120 min) signals meeting the bank's per-gauge standard: Luganville (luga) clearly, with peak 0.078 m, R 8.4, rule-based onset 02:29 UTC and 0 of 400 random-time controls as large; and Lifou (lifo/lifo2, two sensors at one site) marginally, with peak 0.060 m, R 5.2, onset 02:21 UTC and 2 of 400 gated random-time controls as large; both onsets fall within 10 min of ETOPO1 shallow-water travel times from either the NCEI or the ComCat epicentre, and neither station detects on 11-12 control days.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```
Python 3 standard library only, needs internet (re-downloads three IOC SLSMF series, about 0.9 MB). Expected last line:
`PASS`. Under a minute on a laptop. Real output: verify-it-yourself/RECEIPTS.md.

## Compared to

| table | cell | value at fetch | URL | fetched (UTC) |
|---|---|---|---|---|
| NOAA NCEI/WDS Global Historical Tsunami Database, runups | event 5942, rows for Luganville or Lifou | none (2 rows in total: PORT VILA, EFATE ISLAND 0.25 m; LENAKEL, TANNA 0.17 m) | https://www.ngdc.noaa.gov/hazel/hazard-service/api/v1/tsunamis/runups?tsunamiEventId=5942 | 2026-10-23T22:13:36Z (scout), 2026-10-23T23:04:33Z (novelty skeptic), same sha256 |

Snapshot record: the-record-we-beat/RECORD.md.

## Not claimed

- Not a main win: NCEI lists the event itself (5942, validity 4).
- No claim about Luganville or Lifou being unobserved elsewhere: a Luganville plot (J. Patton, earthjay.com) and a GNS
  Science EGU25 abstract (Loyalty Islands mentioned) exist; the claim is only that NCEI's runup table lacks these rows.
- Lifou is marginal under the stated rule (R 5.24 against a threshold of 5; 2 of 400 random-time controls as large).
- Model travel times vary by a few minutes with the bathymetry grid (Luganville 45.8-50.3 min, Lifou 33.6-38.1 min
  across the panel's grids); every pick stays within +/-10 min, Luganville by 0.9 min with the ComCat epicentre.
- Onset and peak times in object/observations.csv label 1-min bins that start 34 s before the raw samples.
- No claim about other events; no completeness fraction (p3).

## Credits

- IOC Sea Level Station Monitoring Facility (VLIZ for UNESCO/IOC), https://www.ioc-sealevelmonitoring.org/, and the
  operators of the Luganville (Vanuatu) and Lifou (New Caledonia) gauges.
- NOAA NCEI/WDS Global Historical Tsunami Database (HazEL), https://www.ngdc.noaa.gov/hazel/.
- ETOPO1 global relief model (Amante and Eakins 2009, NOAA NCEI), via NCEI THREDDS.
- USGS ComCat, https://earthquake.usgs.gov/ (event us7000nzf3, used by the criterion skeptic).
- J. Patton, Luganville tide-gauge plot, https://earthjay.com/earthquakes/20241217_vanuatu/20241217_vanuatu_tide_gage_plot_luganville.pdf
- GNS Science, EGU25-7588, https://meetingorganizer.copernicus.org/EGU25/EGU25-7588.html
- Open-Meteo ERA5 archive (weather check), https://open-meteo.com/.
- Repo issue #253 and draft PR #371 (travel-time scatter against NCEI arrivals), which shaped the near-field design.
