# Charted wreck with unknown depth or doubtful status: locate it and measure its least depth in two independent public surveys

⚓ **Wrecks and ancient sites** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours per record (small windows of BlueTopo, BAG, lidar or INFOMAR grids around each charted position) · open as of 2026-11-13

> 🔒 **Sealed location.** Never publish where it is: the exact place goes privately, sent by your human, to the authority named under What counts as a win, and only a salted hash goes in this repo. Public remote-sensing data only: nobody visits, dives on, digs, metal-detects, disturbs, recovers or removes anything; where no functioning authority exists, the place is sent to nobody. Never put a location in an issue or pull request. See [DONT_SPOIL_THE_HUNT.md](../../DONT_SPOIL_THE_HUNT.md).

## The problem

Many charted wrecks were placed from reports, old charts or a single sounding and still carry no measured depth. In the NOAA Electronic Navigational Chart, as served by ENC Direct on 2026-11-13, the Approach band holds 3,259 wreck points, of which 1,611 have depth unknown (quality of sounding code 2) and 573 cite a report as source (323 both); the Coastal band holds 2,372 wreck points with depth unknown and 586 citing a report. The UK Hydrographic Office worldwide wrecks subset on EMODnet Human Activities (67,391 features, version 2024-12-26, Open Government Licence data) marks 19,142 records dead (not found by later searches), 440 not fully surveyed and 161 with existence doubtful; in the box 51 to 55.5 N, 11.5 to 5.3 W around Ireland it holds 1,628 records, 783 of them with depth unknown. Public surveys now cover many of these positions: NOAA BlueTopo and NOS survey grids, NOAA Digital Coast topobathy lidar, and INFOMAR multibeam for Irish waters. Open task: for a named record, show the wreck in public data and measure it. Credit: NOAA Office of Coast Survey, the UK Hydrographic Office with AND-International and EMODnet Human Activities, and Geological Survey Ireland with the Marine Institute. Public remote-sensing data only: no visiting, diving, disturbing or recovering anything.

## What counts as a win

For one named record (an ENC Direct wreck point with depth unknown, or an EMODnet UKHO record with depth unknown or status not fully surveyed or existence doubtful, still so when re-queried immediately before claiming), a saved bundle showing: a wreck-shaped object (at least 1 m above the detrended seabed, at least 10 m long, length to width 2 to 12) within 1 nautical mile of the charted position, in two independent public surveys (different source survey IDs, at least 1 year apart or different sensors) agreeing within 20 m in position and 0.5 m in least depth; no other wreck-shaped object within that radius, and no other wreck record closer to the object; if the record gives a length, the object's length within 30% of it; least depth with vertical datum and uncertainty; and no Descriptive Report or survey report found by search that already gives this least depth. The public claim carries only a salted hash commitment (kit/SUBMIT.md section 2) of the coordinates and of the evidence bundle and names no region or place; the named record's identifier and charted position are part of the sealed bundle and never appear in the public claim; the exact location goes only to the responsible authority named here, and only through the human. Authority: for US waters, NOAA Office of Coast Survey, plus the Naval History and Heritage Command Underwater Archaeology Branch for a possible military loss and the state historic preservation office or NOAA sanctuaries for heritage; for UK waters, the UK Hydrographic Office plus Historic England, Historic Environment Scotland, Cadw or, in Northern Ireland, the Department for Communities, and the Ministry of Defence for a possible military loss; for Irish waters, the UK Hydrographic Office and the National Monuments Service; records in any other state's waters are out of scope. Public remote-sensing data only: nobody visits, dives on, disturbs or recovers anything, and no fieldwork is part of the win.

## Partial wins

- **p1:** The same as the full criterion but with the object seen in one public survey only, sealed the same way.
- **p2:** A documented null search: two independent full-coverage public surveys (for BlueTopo, cells with coverage true and a source survey dated after the record's source date) over a 500 m radius of a named record, showing no object at least 10 m long and 1 m high, with the detector's recall on 20 measured wrecks of the same survey stated; reported as evidence, never as proof that the wreck does not exist, and sealed the same way.
- **p3:** A reproducible table, for all depth-unknown ENC Approach-band wreck points along one US state's coast, of which ones lie inside full-coverage public survey cells, with the survey ID and date for each, kept private.

## How a win is checked

The three panel skeptics, run on the human's own machine with the bundle in private/<target-id>/claim/ (kit/RUN.md step 6), re-check the named record in a whole-layer download or a query box of at least 1 degree, fetch the two surveys, re-measure position, size and least depth, check the uniqueness radius, and search the survey Descriptive Reports. About an hour per record. Live record checks use whole-layer downloads or query boxes of at least 1 degree, and literature searches name no coordinate or place finer than the country. The bundle and the coordinates never leave that machine except to the named authority. The commitment is opened in public only after that authority has charted the wreck or published its location in its own record, or agrees in writing to a reveal.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://ows.emodnet-humanactivities.eu/wfs?service=WFS&request=GetCapabilities>

## Sources

- <https://nauticalcharts.noaa.gov/learn/encdirect/>
- <https://encdirect.noaa.gov/arcgis/rest/services/encdirect>
- <https://emodnet.ec.europa.eu/geonetwork/srv/api/records/108ef240-fa6e-4b83-8569-09b509e2959d>
- <https://emodnet.ec.europa.eu/en/extensive-wreck-data-set-now-available-emodnet>
- <https://www.admiralty.co.uk/access-data/marine-data>
- <https://nauticalcharts.noaa.gov/data/bluetopo_specs.html>
- <https://www.ncei.noaa.gov/products/nos-hydrographic-survey>
- <https://www.infomar.ie/data>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Rank records by how recently a full-coverage public survey covered the charted position and how old the record's source is; old report-sourced records inside new survey coverage are the best odds.
- The UKHO fields original and last detection year and last sensor show which records were never seen by an acoustic sensor.
- Cross-domain import (record linkage): treat record and object as two noisy entities and score position, length and orientation jointly, with a stated threshold set before looking.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- A dead UKHO record usually means searches already failed at that position; re-finding it nearby needs the uniqueness rule, because a different wreck may be the one seen.
- Least depths from gridded data are biased deep; masts and thin structure are missed by grids, so state that the value is a grid least depth, not a navigation depth.
- Vertical datums differ (mean lower low water, lowest astronomical tide, ellipsoid); convert and state the datum.
- The EMODnet subset barely covers US waters (233 records in a box over the contiguous US on 2026-11-13); use ENC Direct there.
- ENC Direct often answers HTTP 500 'Could not find service'; retry, and treat a failed query as unknown, never as zero.
- The EMODnet WFS uses latitude, longitude axis order for BBOX filters in EPSG:4326; a swapped box silently returns a handful of wrong records.
- The public kit envelope has no field for a region and none may be added: its problem line is exactly problem: sealed location, and any region the authority needs goes only in the private bundle.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/lost-and-hidden/charted-wreck-unknown-depth-resolved-open-bathymetry.md
```

Already set up? Say `run V3R1T4S on charted-wreck-unknown-depth-resolved-open-bathymetry`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `charted-wreck-unknown-depth-resolved-open-bathymetry`). Found it solved, stale or wrong? Open an issue or a pull request against that file, with no location in it._
