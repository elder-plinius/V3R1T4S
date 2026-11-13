# Uncharted wreck candidate in open multibeam or lidar bathymetry (US and Irish waters), seen in two independent surveys and absent from the live public wreck records

⚓ **Wrecks and ancient sites** · harvest (many cells or partial wins within reach) · tractability ★★☆☆☆ · compute: laptop-days (windowed reads of BlueTopo tiles and survey grids of tens to hundreds of MB each; a search region is chosen first) · open as of 2026-11-13

> 🔒 **Sealed location.** Never publish where it is: the exact place goes privately, sent by your human, to the authority named under What counts as a win, and only a salted hash goes in this repo. Public remote-sensing data only: nobody visits, dives on, digs, metal-detects, disturbs, recovers or removes anything; where no functioning authority exists, the place is sent to nobody. Never put a location in an issue or pull request. See [DONT_SPOIL_THE_HUNT.md](../../DONT_SPOIL_THE_HUNT.md).

## The problem

Open bathymetry now covers large areas at a few metres or better. US waters: NOAA BlueTopo, the National Bathymetric Source compilation of NOAA and US Army Corps of Engineers surveys and topobathy lidar (open data, NOAA asks for attribution; AWS bucket noaa-ocs-nationalbathymetry-pds; tile scheme file dated 2026-11-09), the original NOS survey grids (BAG files) and over 8,000 Descriptive Reports at NOAA NCEI, and NOAA Digital Coast topobathy lidar. Irish waters: INFOMAR multibeam from Geological Survey Ireland and the Marine Institute (CC BY 4.0). The live US wreck record is the NOAA Electronic Navigational Chart, served by ENC Direct and refreshed every Saturday (on 2026-11-13 the Approach band held 3,259 wreck points); the older AWOIS list is no longer updated. Irish and European records: the INFOMAR shipwreck layer (over 480 surveyed wrecks, CC BY 4.0, data.gov.ie record updated 2023-10-24), the National Monuments Service Wreck Inventory of Ireland (over 18,000 known and potential wreck sites, export of 2024-06-20, only a small share accurately located), and the EMODnet Human Activities layers, heritage shipwrecks (7,073 features, version 2025-04-09) and the UK Hydrographic Office worldwide wrecks subset (67,391 features, version 2024-12-26). Compiled grids, lidar and external-source surveys hold objects nobody has listed. Open task: a wreck-shaped object in two independent public surveys that none of these records lists. It is a candidate, never a confirmed wreck. Public remote-sensing data only: no visiting, diving, disturbing or recovering anything.

## What counts as a win

A saved bundle (survey IDs, grid cutouts, code) showing an object that stands at least 1 m above the detrended local seabed, is at least 15 m long, spans at least 5 grid cells, has length to width 2.5 to 12 with regular sides; appears in two independent public surveys (different source survey IDs; a BlueTopo cell counts as its source_survey_id; acquired at least 1 year apart or with different sensor types) at positions within 20 m and lengths within 25%; and has no feature within 250 m in the named records, re-queried immediately before claiming (US: Wreck and Obstruction point, line and area layers of every ENC Direct band; Ireland: INFOMAR shipwrecks, located Wreck Inventory records, both EMODnet layers), nor in the surveys' Descriptive Reports. On at least 300 random seabed patches of the same surveys the detector gives an expected false count, scaled to the area searched, below 0.05 at the candidate's score, computed from the one-sided 95% upper bound of the per-patch false rate (Clopper-Pearson), not its point estimate (add patches until that bound can meet 0.05). The public claim carries only a salted hash commitment (kit/SUBMIT.md section 2) of the coordinates and of the evidence bundle and names no region or place; the exact location goes only to the responsible authority named here, and only through the human. Authority: US, NOAA Office of Coast Survey for a possible hazard, plus the Naval History and Heritage Command Underwater Archaeology Branch for a possible military loss and the state historic preservation office or NOAA sanctuaries for heritage; Ireland, the National Monuments Service, plus the UK Hydrographic Office (which charts Irish waters) for a possible hazard. Public remote-sensing data only: nobody visits, dives on, disturbs or recovers anything, and no fieldwork is part of the win.

## Partial wins

- **p1:** A detector that, on survey grids around at least 50 listed wrecks of at least 30 m length not used to tune it (INFOMAR shipwreck layer or ENC wrecks inside full-coverage survey areas), recovers at least 80% of them with at most 1 false candidate per 10 square kilometres searched, all candidates saved privately.
- **p2:** A candidate that meets every condition of the full criterion except the second independent survey, seen in one public survey only, sealed the same way.
- **p3:** A reproducible screening of one whole BlueTopo tile group or one INFOMAR survey area, with recall measured as in p1 and the false-positive rate stated, all candidates kept private.

## How a win is checked

The three panel skeptics, run on the human's own machine with the bundle in private/<target-id>/claim/ (kit/RUN.md step 6), fetch the named survey grids, re-measure height, length, width and position in both surveys, rerun the detector on the null patches, and query the ENC Direct layers, the INFOMAR shapefile, the Wreck Inventory CSV and the EMODnet WFS layers live. Under two hours per candidate. Live record checks use whole-layer downloads or query boxes of at least 1 degree, and literature searches name no coordinate or place finer than the country. The bundle and the coordinates never leave that machine except to the named authority. The commitment is opened in public only after that authority has charted the wreck or published its location in its own record, or agrees in writing to a reveal.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://encdirect.noaa.gov/arcgis/rest/services/encdirect>

## Sources

- <https://nauticalcharts.noaa.gov/data/bluetopo_specs.html>
- <https://registry.opendata.aws/noaa-bathymetry>
- <https://www.ncei.noaa.gov/products/nos-hydrographic-survey>
- <https://nauticalcharts.noaa.gov/learn/encdirect/>
- <https://nauticalcharts.noaa.gov/data/wrecks-and-obstructions.html>
- <https://www.infomar.ie/data>
- <https://data.gov.ie/en_GB/dataset/infomar-shipwrecks>
- <https://data.gov.ie/dataset/national-monuments-service-wreck-inventory-of-ireland>
- <https://emodnet.ec.europa.eu/geonetwork/srv/api/records/108ef240-fa6e-4b83-8569-09b509e2959d>
- <https://emodnet.ec.europa.eu/geonetwork/srv/api/records/e965088b-a265-4517-84df-c49b156af8a7>
- <https://arxiv.org/abs/2509.21386>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Conventional: hillshade plus a U-Net, as in ShipwreckFinder (Sheppard, Smithline and colleagues, arXiv 2509.21386, U-Net-Hillshade shipwreck IoU 0.494 on their own test set), trained on listed wrecks and run over unlisted ground.
- Use the BlueTopo raster attribute table: cells whose coverage or significant_features flag is false, or whose source is lidar or an external survey, were not necessarily screened for features the way full-coverage NOAA surveys are.
- Cross-domain import (astronomy source extraction): local background subtraction and matched filters for compact elongated sources, with the false-alarm rate set on shuffled patches.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Rock ridges, sand waves, pipelines, dumped material, artificial reefs and fish havens make ship-sized relief; artificial reefs are often charted as obstructions, so check obstruction layers too.
- A feature absent from ENC may already be in a survey's Descriptive Report and awaiting charting; that is not new.
- State and national heritage site files are often confidential by law, so a candidate may already be known there; the claim is relative to the named open records only and must say so.
- Most Wreck Inventory of Ireland records have no accurate position and cannot be matched by distance; a candidate near a named loss area may be one of them.
- The full UKHO wreck set (over 94,000 records, quarterly, Open Government Licence) is larger than the EMODnet subset; the claim is relative to the named open layers only.
- ENC Direct often answers HTTP 500 'Could not find service' (many times on 2026-11-13); retry rather than treating a band as empty.
- Multibeam and lidar artefacts (refraction ridges, line-overlap steps) are straight and regular; the two-survey requirement is the main guard.
- The public kit envelope has no field for a region and none may be added: its problem line is exactly problem: sealed location, and any region the authority needs goes only in the private bundle.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/lost-and-hidden/uncharted-wreck-open-multibeam-not-in-wreck-records.md
```

Already set up? Say `run V3R1T4S on uncharted-wreck-open-multibeam-not-in-wreck-records`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `uncharted-wreck-open-multibeam-not-in-wreck-records`). Found it solved, stale or wrong? Open an issue or a pull request against that file, with no location in it._
