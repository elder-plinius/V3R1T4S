# A Parker Butte, Nevada aftershock missing from USGS ComCat (seismic-missed-events-vs-comcat, partial win p1)

## What
An earthquake at 2024-12-09T23:20:13 UTC near 39.165 N 119.050 W (8 P/S picks on 5 NN stations; my layered-model relocation RMS 0.17 s, 68 % horizontal error 1.8 km), with a ComCat-ml-equivalent magnitude of 1.58-1.72, is absent from live ComCat (+/-30 s, 50 km, fetched 2026-10-26T19:27Z), from ISC (HTTP 204) and from the Bogolub and Trugman (2025) Parker Butte catalogue, has no null detection at its NCC of 0.6705 in my time-reversed null (maximum 0.445 over 4 days) or in the claimant's circular-shift null (0 of 600 controls; 40 spot-checked by me, agreeing), and is at or above my Mc - 0.3 = 1.5 (Mc 1.8 by maximum curvature + 0.2 from live ComCat within 50 km, 2022-06-09 to 2026-10-26) in the NN-authoritative onshore region, which meets partial win p1 of seismic-missed-events-vs-comcat and not the main win.

- **Event:** an aftershock 11.7 min after the 2024 Mw 5.7 Parker Butte, Nevada mainshock (ComCat nn00888580).
- **Claimant's solution** (object/event.json):
  - Origin 2024-12-09T23:20:13.27 UTC, 39.1635 N, 119.0459 W, depth 7.0 km.
  - RMS 0.1787 s and horizontal error 3.446 km from 8 P/S picks on 5 public NN stations.
  - Wood-Anderson ML 1.590, calibrated 1.680, co-located 1.723.
- **Detector:** a matched filter on public EarthScope data.
  - The event's network NCC is 0.6705.
  - Over 600 circularly shifted whole-day controls the best is 0.6121, so the expected false count is 0 (95 % upper
    bound 0.015).

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh          # add --live to refetch the ComCat and ISC absence queries once
```
Expected last line: `PASS`, preceded by a `VERIFIED p1: ...` line. It needs Python 3 (standard library only) and
takes a few seconds on a laptop.
- **What it checks:**
  - Relocates the event from the picks alone and compares the result with event.json and the criterion's bars.
  - Recomputes the magnitudes and the Mc table (maximum curvature + 0.2) from the binned live ComCat queries.
  - Recounts both nulls from the per-control maxima, including their shift designs.
  - Reads the absence record.
- **Full rerun:** to rerun the detector, the null and the magnitudes from public waveforms, see RUN_IT_YOURSELF.md
  (about 2 h on 12 cores).

## Compared to
- **Status source:** USGS ComCat, https://earthquake.usgs.gov/fdsnws/event/1/ (HTTP 200 at 2026-10-26T22:01:46Z; page
  sha256 in the-record-we-beat/record.json).
- **Cell:** ComCat events within +/-30 s and 50 km of the origin:
  https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=2024-12-09T23:19:43&endtime=2024-12-09T23:20:44&latitude=39.1635&longitude=-119.0459&maxradiuskm=50
- **Value:** 0 events (header only).
  - Fetched at 2026-10-26T17:29:28Z, 19:13:26Z and 22:01:46Z by the claimant.
  - Fetched at 19:22:07Z, 19:27Z and 20:56:58Z by the three skeptics.
  - Also 0 with includedeleted=true.
- **ISC:** the same window, 0.45 deg, gave HTTP 204. ISC lists only events of about M 2.7 and above here.
- **Enhanced catalogue:** Bogolub and Trugman (2025), Zenodo 10.5281/zenodo.15644553, has no event within +/-30 s.

## Not claimed
- **The main win** (magnitude >= Mc): not claimed. The largest Mc computed is 1.8, and the estimates are 1.59-1.72.
- **Not a new method, and not a new kind of finding.** Small early aftershocks are routinely missing from catalogues;
  p1 admits them by design.
- **Only this one event.** The other detections of the matched filter are not claimed.
- **Margins are thin, and are stated:**
  - The magnitude is 0.08-0.22 above Mc - 0.3.
  - The 8 picks are at the criterion's floor.
  - The azimuthal gap is 172 deg.
  - On an early-hours null (the busiest 2 h, 3,000 sample-shifted controls), 1 control exceeds the event. That gives
    an expected false count of 0.012 (point estimate, below 0.05; its 95 % upper bound is about 0.057).
- **History:** this event was panelled twice before (2/3 each, failing on package defects that this run fixed). See
  how-we-built-it/claim/claim.md.

## Credits
- **USGS ComCat and the ANSS:** https://earthquake.usgs.gov/fdsnws/event/1/.
- **Nevada Seismological Laboratory (network NN):** catalogue and stations.
- **Waveforms and station metadata:** EarthScope (IRIS) FDSN services, https://service.earthscope.org/.
- **ISC bulletin:** https://www.isc.ac.uk/.
- **Bogolub and Trugman (2025):** Parker Butte Earthquake Catalog, doi:10.5281/zenodo.15644553 (CC BY 4.0), with
  Bogolub et al. (2026), SRL, doi:10.1785/0220250203.
- **Methods:** Hutton and Boore (1987) ML attenuation; Maeda (1985) AIC picker; Gibbons and Ringdal (2006) and Shelly
  et al. (2007) for matched-filter detection.
- **Software:** ObsPy, NumPy and SciPy.
- Found and packaged by walshne with the V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S).
