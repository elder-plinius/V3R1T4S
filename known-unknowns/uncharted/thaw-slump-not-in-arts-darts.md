# Retrogressive thaw slump seen in open Sentinel-2 imagery and ArcticDEM strips but absent from the ARTS and DARTS inventories

🧭 **Uncharted maps** · harvest (many cells or partial wins within reach) · tractability ★★★★☆ · compute: laptop-hours (Sentinel-2 L2A chips of a few MB and 2 m ArcticDEM strip windows of tens of MB; ARTS v6.0.0 is 53.8 MB) · open as of 2026-11-13

## The problem

A retrogressive thaw slump (RTS) is a landslide in ice-rich permafrost: a steep headwall of thawing ground retreats upslope each summer and leaves a bowl of bare mud. Two open inventories map them. ARTS (Yang, Rodenhizer, Rogers, Natali and 20 co-authors, Scientific Data 2025) pools 20 source data sets; its paper reports 23,529 RTS-present and 20,434 RTS-absent digitisations, and the newest Zenodo release on 2026-11-13 is v.6.0.0 (published 2025-09-22, CC0). DARTS (Nitze, Grosse and colleagues at AWI, Scientific Data 2025) holds more than 43,000 deep-learning footprints of RTS and active-layer detachment slides from PlanetScope imagery for 2018-2023, latest release v1.2 (DOI 10.18739/A22B8VD7C, CC0), but only over permafrost hotspots of about 1.6 million km^2. Large parts of the Arctic are not covered by either. Sentinel-2 L2A (10 m, open on AWS) shows the bare scar and ArcticDEM strips (2 m, repeat dates since 2007, open on AWS from the Polar Geospatial Center) show the elevation loss. Open task: an active slump absent from both inventories, shown by both data sets.

## What counts as a win

A saved bundle (Sentinel-2 scene IDs, ArcticDEM strip IDs, polygons, co-registration statistics, code) for one candidate where: (1) in Sentinel-2 L2A summer images the feature is a bare-ground scar (NDVI drop of at least 0.2 from surrounding tundra) of at least 0.5 ha, shaped as an amphitheatre opening downslope, and its area grows by at least 0.2 ha, or its headwall retreats by at least 20 m, between two summers at least 1 year apart; (2) two ArcticDEM strips at least 1 year apart, co-registered on stable ground around the feature with a normalized median absolute deviation of 0.5 m or less, show elevation loss of at least 1.0 m over at least 0.2 ha inside the scar and a headwall at least 1 m high; (3) the site lies in mapped permafrost and is not a road cut, quarry, river-bank or coastal-bluff retreat, or fire scar; (4) no RTS-present polygon in the newest ARTS release (v.6.0.0 or later, re-fetched immediately before claiming) and no polygon in the newest DARTS release (v1.2 or later) lies within 250 m of the candidate, and no other RTS inventory found by search contains it. The claim is a candidate slump.

## Partial wins

- **p1:** A detector tuned on one region that, on a held-out region with at least 50 ARTS RTS-present polygons of at least 1 ha, recovers at least 80% of them with at least 70% of its other detections confirmed as slumps by rule (2), all detections saved.
- **p2:** A candidate meeting rules (1), (3) and (4) where no pair of ArcticDEM strips covers it, with the Sentinel-2 growth confirmed in Landsat images.

## How a win is checked

The skeptic downloads the listed Sentinel-2 chips and ArcticDEM strips from the public AWS buckets, recomputes NDVI, scar area and growth, co-registers the strips and recomputes the elevation loss, and checks distances to every polygon in the newest ARTS and DARTS releases. Under an hour per candidate.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://zenodo.org/doi/10.5281/zenodo.10535025>

## Sources

- <https://pmc.ncbi.nlm.nih.gov/articles/PMC11704310/>
- <https://github.com/whrc/ARTS>
- <https://zenodo.org/doi/10.5281/zenodo.10535025>
- <https://apgc.awi.de/dataset/darts-db-ai-rts-rts-hotspots-circum-arctic-permafrost-region-v1-2>
- <https://registry.opendata.aws/pgc-arcticdem/>
- <https://earth-search.aws.element84.com/v1/collections/sentinel-2-l2a>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Conventional: difference ArcticDEM strips over ice-rich lowlands outside the DARTS coverage polygons and threshold closed elevation-loss blobs next to steep breaks of slope.
- Use the DARTS coverage layer to find permafrost terrain that neither inventory has looked at.
- Cross-domain import (planetary pit and crater detection): template matching on amphitheatre-shaped depressions in a DEM is cheap and orientation-aware.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Active-layer detachment slides, river-bank erosion and coastal bluff retreat look similar; require the amphitheatre headwall and the elevation loss inside the scar.
- ArcticDEM strips contain cloud, water and matching blunders; use the strip bitmasks and check that the loss is spatially coherent.
- ARTS also holds RTS-absent polygons; an overlap with one of those is allowed but must be reported.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/uncharted/thaw-slump-not-in-arts-darts.md
```

Already set up? Say `run V3R1T4S on thaw-slump-not-in-arts-darts`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `thaw-slump-not-in-arts-darts`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
