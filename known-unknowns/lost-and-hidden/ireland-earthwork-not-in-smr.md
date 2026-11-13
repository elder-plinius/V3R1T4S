# Unrecorded earthwork (ringfort, enclosure, barrow or similar) in open Irish LiDAR, absent from the National Monuments Service Sites and Monuments Record

⚓ **Wrecks and ancient sites** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours (GSI LiDAR GeoTIFF terrain tiles of 0.13 m to 2 m cells, tens of MB each; SMR points by live query or a bulk CSV of about 151,000 rows) · open as of 2026-11-13

> 🔒 **Sealed location.** Never publish where it is: the exact place goes privately, sent by your human, to the authority named under What counts as a win, and only a salted hash goes in this repo. Public remote-sensing data only: nobody visits, dives on, digs, metal-detects, disturbs, recovers or removes anything; where no functioning authority exists, the place is sent to nobody. Never put a location in an issue or pull request. See [DONT_SPOIL_THE_HUNT.md](../../DONT_SPOIL_THE_HUNT.md).

## The problem

The Archaeological Survey of Ireland, part of the National Monuments Service (NMS, Department of Housing, Local Government and Heritage), keeps the Sites and Monuments Record (SMR), a national record of known and possible monuments that is continually updated. It is open data under CC BY 4.0: a live ArcGIS feature service of points (SMROpenData), zone polygons (SMRZoneOpenData) and bulk CSV and shapefile downloads (bulk version 2025-12-01; dataset updated 2026-07-30). The live point service returned 151,308 records on 2026-11-13. Geological Survey Ireland (GSI) serves open topographic LiDAR from GSI, the Office of Public Works, Transport Infrastructure Ireland, the Discovery Programme and Heritage Council, New York University and Westmeath County Council: GeoTIFF terrain models of 0.13 m to 2 m cells collected 2015 to 2021, also CC BY 4.0. Earthworks such as ringforts (circular banked enclosures, mostly early medieval), barrows, enclosures and field systems survive as low relief that LiDAR shows under grass and trees. James O'Driscoll's study of the Baltinglass cursus complex, County Wicklow (Antiquity 98, 636 to 653, 2024), reports that a LiDAR survey of 122 km^2 doubled the number of known monuments there. Open task: a candidate earthwork in the open LiDAR that the SMR does not record.

## What counts as a win

A saved private bundle (LiDAR tile names and providers, terrain cutouts, relief visualisations, outline, code) showing a closed or near-closed earthwork: a bank, ditch or platform of at least 0.3 m relief, traced around at least 70% of its perimeter, with a largest dimension of 15 m to 300 m, and not explained by modern field boundaries, roads, drains, quarries or forestry on current OpenStreetMap and the basemaps of the NMS Historic Environment Viewer. A second independent source must confirm it: a second open LiDAR acquisition of another year or provider, or a matching boundary on the historic Ordnance Survey 6-inch or 25-inch map in that viewer that is not annotated as a monument, or, for a feature at least 50 m across, a crop or soil mark of matching size (within 20%) in at least two Sentinel-2 L2A scenes from different years. Absent means: no SMR point of any class within 150 m of the feature centre and the feature outside every SMRZone polygon, both re-queried live just before claiming, and no published report found by search. The claim is a candidate, never a confirmed discovery. The public claim carries only a salted hash commitment (kit/SUBMIT.md section 2) of the coordinates and of the evidence bundle and names no region or place. The exact location goes only to the National Monuments Service, and only through the human. Public remote-sensing data only: nobody visits, digs, metal-detects, disturbs or removes anything at the site, and no fieldwork is part of the win.

## Partial wins

- **p1:** A detector that, on LiDAR blocks from at least two providers held out from tuning, recovers at least 50% of the SMR points of the classes Ringfort - rath and Enclosure inside those blocks, with at most 1 false candidate per 5 km^2 and all candidates kept private.
- **p2:** A candidate meeting every condition of the success criterion except the second independent source, sealed the same way.

## How a win is checked

The three panel skeptics, run on the human's own machine with the bundle in private/<target-id>/claim/ (kit/RUN.md step 6), open the private bundle, re-download the named GSI tiles, recompute the relief visualisations, outline and relief, check the second source, and re-query the SMR point and zone services for the 150 m and polygon rules. Live record checks use whole-layer downloads or query boxes of at least 1 degree, and literature searches name no coordinate or place finer than the country. The bundle and the coordinates never leave that machine except to the named authority. In public, the commitment is opened only after the authority has published the site's location in its own record or agrees in writing to a reveal.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://services-eu1.arcgis.com/HyjXgkV6KGMSF3jt/ArcGIS/rest/services/SMROpenData/FeatureServer/0/query?where=1%3D1&returnCountOnly=true&f=json>

## Sources

- <https://data.gov.ie/en_GB/dataset/national-monuments-service-archaeological-survey-of-ireland>
- <https://services-eu1.arcgis.com/HyjXgkV6KGMSF3jt/ArcGIS/rest/services/SMROpenData/FeatureServer>
- <https://www.archaeology.ie/collections-and-publications/open-data/>
- <https://data.gov.ie/en_GB/dataset/open-topographic-lidar-data>
- <https://gsi.geodata.gov.ie/server/rest/services/Lidar>
- <https://doi.org/10.15184/aqy.2024.39>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Conventional: local relief model and sky-view factor visualisations with a small CNN trained on SMR ringfort and enclosure points.
- Cross-domain import (crater counting on planetary images): circular Hough transforms and rim-profile fitting suit ringforts, which are close to circular.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- SMR points sit at one spot per record, sometimes the centre of a large complex; read the descriptions of the nearest records as well as applying the 150 m rule.
- Levelled field boundaries, silage pits, lazy-bed cultivation ridges and forestry drains make convincing circles and rectangles.
- Most forts drawn on the first-edition 6-inch maps were entered in the SMR from those maps; a feature annotated there as a fort or rath is very unlikely to be new.
- Recent LiDAR discoveries, such as those at Baltinglass, may already be in the SMR; query the live service, not an old bulk file.
- Sentinel-2 pixels are 10 m, so crop marks confirm only large enclosures; smaller features need a second LiDAR acquisition or the historic map.
- The public kit envelope has no field for a region and none may be added: its problem line is exactly problem: sealed location, and any region the authority needs goes only in the private bundle.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/lost-and-hidden/ireland-earthwork-not-in-smr.md
```

Already set up? Say `run V3R1T4S on ireland-earthwork-not-in-smr`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `ireland-earthwork-not-in-smr`). Found it solved, stale or wrong? Open an issue or a pull request against that file, with no location in it._
