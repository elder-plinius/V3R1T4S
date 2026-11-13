# Glacier lake outburst flood seen in open Sentinel-2 and Landsat imagery but absent from the Potsdam global GLOF database

🧭 **Uncharted maps** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours (windowed cloud-optimized GeoTIFF reads of Sentinel-2 L2A and Landsat Collection 2 scenes; a few MB per lake chip; the database itself is 1.6 MB) · open as of 2026-11-13

## The problem

A glacier lake outburst flood (GLOF) is the sudden drainage of a lake dammed by ice, a moraine or bedrock next to a glacier. Natalie Lützow and Georg Veh (University of Potsdam, with Oliver Korup) maintain the global GLOF database: the 2023 data paper (Earth System Science Data 15, 2983) listed 3,151 reported GLOFs from 27 countries between 850 and 2022 CE, the project page read on 2026-11-13 says more than 4,000 GLOFs up to 2024, and the newest archived release is version 4.2 on Zenodo (published 2026-07-28, CC BY 4.0, files glofdatabase_v4-2.ods and not_confirmed_v4-2.ods). Its inclusion rule is a known location, a known date or date range, and a reference, so floods that nobody reported are missing; the authors name Arctic Russia, north-east Canada and Antarctica as uncovered, and the 2023 paper mapped lake areas for only 391 post-1984 events. Sentinel-2 (10 m, since 2015) and Landsat (30 m, since 1984) are open and see lake area drop and fresh flood deposits downstream. Open task: a dated outburst, seen in two independent open sensors, at a lake for which the database has no matching event.

## What counts as a win

A saved bundle (scene IDs, lake polygons before and after, water-index thresholds, downstream change maps, code) for one candidate GLOF, where: (1) the lake lies within 5 km of a glacier outline in RGI 7.0 and its pre-event water area is at least 0.02 km^2 in a clear, ice-free image; (2) water area falls by at least 30% and by at least 0.01 km^2 between two clear, ice-free images no more than 60 days apart, measured in Sentinel-2 L2A or Landsat Collection 2; (3) the same drop is confirmed in a second, independent sensor (Landsat if the first was Sentinel-2, or the reverse, or Sentinel-1 radar backscatter) within the same window; (4) the outlet channel shows new deposits, scour or vegetation loss over at least 500 m downstream in the post-event image that is absent in the pre-event image; (5) the event ended at least 6 months before the claim; (6) the newest release of the database (version 4.2 or later, re-fetched immediately before claiming, both the main and the not-confirmed files) has no event at any lake within 2 km of the candidate lake whose date or date range overlaps the candidate window widened by 1 year on each side, and no paper or news report found by search describes it. The claim is a candidate GLOF, never a confirmed one.

## Partial wins

- **p1:** A detector run blind over one glacier region for one year (for example Alaska 2020) that finds at least 80% of the database's events there whose lake area loss meets rule (2), with every detection saved and the residual non-database detections listed and hand-vetted.
- **p2:** Satellite evidence meeting rules (2) and (3) for an event listed only in not_confirmed_v4-2.ods, with a dated window of 60 days or less that agrees with the record.
- **p3:** For a database event whose date is given only as a range longer than 1 year, a pair of clear images meeting rules (2) and (3) that narrows the date to a window of 60 days or less inside that range.

## How a win is checked

The skeptic fetches the listed scenes from the public Sentinel-2 and Landsat archives (for example the Earth Search STAC API), recomputes the water index and lake areas with the stated thresholds, checks the second sensor and the downstream change, and searches the newest database release for events within 2 km and the widened date window. Under an hour per candidate.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://zenodo.org/records/7330344/latest>

## Sources

- <https://zenodo.org/records/23370149>
- <https://essd.copernicus.org/articles/15/2983/2023/>
- <https://uni-potsdam.de/en/umwelt/forschung/ag-naturgefahren/forschungsprojekte/creating-and-maintaining-a-global-glof-database>
- <http://glofs.geoecology.uni-potsdam.de>
- <https://earth-search.aws.element84.com/v1/collections/sentinel-2-l2a>
- <https://nsidc.org/data/nsidc-0770/versions/7>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Conventional: per-lake time series of a water index (NDWI or MNDWI) over all lakes within 5 km of RGI 7.0 glaciers, flagging sudden area drops that do not recover within the same season.
- Search first where the database is thin by its own account: Arctic Russia, north-east Canada and the Greenland periphery.
- Cross-domain import (change-point detection in sensor networks): a Bayesian online change-point model per lake separates a step drop from seasonal freeze and thaw.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Lake ice and snow make a full lake look empty in a water index; compare only ice-free images from the same season.
- Cloud and terrain shadow mimic water; use the scene cloud masks and a terrain shadow model.
- Many ice-dammed lakes drain every year and the database lists many such repeats; check every listed event at the lake, not only the lake name.
- The live web map was unreachable on 2026-11-13 (connection reset); the Zenodo release is the citable version, but check the web map too if it is reachable.
- Zhang et al. 2025 (Nature Communications) published an updated moraine-dammed GLOF inventory; search it and other recent regional inventories before claiming.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/uncharted/glof-not-in-potsdam-glof-database.md
```

Already set up? Say `run V3R1T4S on glof-not-in-potsdam-glof-database`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `glof-not-in-potsdam-glof-database`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
