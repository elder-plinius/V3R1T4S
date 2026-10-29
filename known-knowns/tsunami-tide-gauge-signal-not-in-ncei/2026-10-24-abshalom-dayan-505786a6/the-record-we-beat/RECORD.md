# What this map is compared against (snapshots; the pages themselves are not copied)

## The listing: NCEI Global Historical Tsunami Database
- Status source: https://www.ngdc.noaa.gov/hazel/view/hazards/tsunami/event-search
  fetched 2026-10-24T19:20:24Z, HTTP 200, 1765 bytes, sha256 3fec2a9935a8d6d3f351d6c2a0c49ccf4a904016e5ac2820e48c55e1122987b6
  (a JavaScript app shell; the listing is the events API behind it).
- Events API: https://www.ngdc.noaa.gov/hazel/hazard-service/api/v1/tsunamis/events?minYear=2015&maxYear=2026&itemsPerPage=200&page=1
  fetched 2026-10-24T19:20:31Z, HTTP 200, 85220 bytes, sha256 bdc6a6b4de4306b71a8f9e2f2992b001f7de93b8a5408166988ae3a43836b0f9;
  page=2 fetched 2026-10-24T19:20:37Z, HTTP 200, 12720 bytes, sha256 64745d27e0122df8646a0552ba6f1445d0095a7027ad58dfb34e97d5553e220a.
  Extracted: 230 events for 2015-2026, newest event id 6193 (2026-10-09). Matched to the 264 quakes: 115 quakes have an
  NCEI event (any validity) within +/-1 calendar day and 1000 km (object/map.csv, column listed).
- Per-event tide-gauge rows: runups API, typeMeasurementId=2 (fetch times and sha256 in how-we-built-it/inputs.tsv).
- Response headers of these fetches are not recorded in this package.

## The p3 cell
- p3 had no claimed or merged result in this repository at 2026-10-24T19:20Z (GitHub search API on
  elder-plinius/V3R1T4S for "tsunami", "completeness map" and "NCEI"; TROPHY_CASE.md at repo_commit 1ebdef4).
- Closest prior numbers, posted as data and not panelled: issue #253, comment by walshne-mit at 2026-10-16T19:58:51Z,
  fetched via https://api.github.com/repos/elder-plinius/V3R1T4S/issues/253/comments?per_page=100 at
  2026-10-24T19:21:04Z, HTTP 200, 15693 bytes, sha256 23b2c8b808500c44bc4ebf192a92a0f31c52c0841e43fde8a9088b77d296ccb5.
  Extracted: 195 of 265 quakes with a usable open 1-min gauge record; 60 of 195 detected (30.8 %); 45 of 82 covered
  NCEI-listed quakes caught; 14 of 351 fake windows pass (about 7 to 8 chance detections); real 0.315 vs at most 0.065
  over 400 fake catalogues. Different rules (travel time 15-150 min, at most 6 gauges per quake).

## Re-check by the panel (NOVELTY skeptic, panel/novelty.md)
- Status source re-fetched 2026-10-24T21:43:20Z, HTTP 200, 1765 bytes, sha256 identical to the 19:20:24Z fetch.
- GitHub search of this repository (issues and pull requests, open or closed) and TROPHY_CASE.md: no p3 claim,
  confirmation or merge; #253 holds maps posted as data ("Not claimed"), #642 is a p1 claim that excludes p3.
