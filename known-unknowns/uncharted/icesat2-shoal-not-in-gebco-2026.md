# Uncharted shoal: ICESat-2 ATL24 laser soundings of seafloor at least 20 m shallower than the GEBCO_2026 grid in cells GEBCO marks as not directly measured

🧭 **Uncharted maps** · harvest (many cells or partial wins within reach) · tractability ★★★★☆ · compute: laptop-hours (ATL24 granules are HDF5 files of a few MB to tens of MB each; the GEBCO_2026 grid page gives the TID grid as a single 3.5 GB file, depth tiles fetched per region; Sentinel-2 chips are MBs) · open as of 2026-11-13

## The problem

ICESat-2 is a NASA laser altimeter satellite whose green photons can reach the seafloor in clear water down to about 40 m. ATL24 Version 3 (Magruder, Parrish, Perry, Swinski, Holwill, To and Kief, 2026, NSIDC DAAC, doi 10.5067/ATLAS/ATL24.003, released November 2026, October 2018 to present, free NASA Earthdata login or the public SlideRule service) labels each photon as bathymetry (class_ph 40) or sea surface (class_ph 41), with refraction-corrected heights relative to the EGM08 geoid and a classification confidence from 0 to 1. Version 3 removed the old low_confidence_flag. Parrish and colleagues (2025, Earth and Space Science, doi 10.1029/2025EA004391) assessed the first release, with depths of about 0.5 to 21.5 m along 13.7 million km of coast. The GEBCO_2026 grid (GEBCO Bathymetric Compilation Group, released 2026-04-27, 15 arc-second cells, public domain, doi 10.5285/4f68d5c7-45eb-f999-e063-7086abc036fa) comes with a Type Identifier (TID) grid: codes 10 to 17 mark direct measurements, 40 to 48 indirect sources such as 40 predicted from satellite gravity, 41 interpolated, 42 and 43 chart contours, and 70 to 72 unknown or steering points. In remote reef and bank areas many shallow cells are still indirect. Open task, read on 2026-11-13: a submerged shoal that ICESat-2 measured, missing from GEBCO_2026.

## What counts as a win

A saved bundle (ATL24 granule names, beam, photon indices, profiles, GEBCO_2026 depth and TID values, Sentinel-2 scene IDs and code) where: (1) at least 2 granules of the latest ATL24 version (Version 3 on 2026-11-13) acquired on different dates each contain at least 30 photons with class_ph 40 and confidence at least 0.6 forming a continuous seafloor profile at least 100 m long, with class_ph 41 sea-surface photons above them (the feature is submerged); (2) the median depth below the ATL24 sea surface along that profile is at most 20 m in each granule, and the two medians agree within 3 m at their closest approach; (3) in every GEBCO_2026 cell holding those photons the TID code is between 40 and 72 (no direct measurement) and the GEBCO_2026 depth is at least 20 m deeper than the ATL24 median; (4) the site is at least 1 km from any GEBCO_2026 land cell; (5) a second, independent data set agrees: a clear Sentinel-2 L2A scene shows a shallow-seabed or breaking-wave signature over the photons, and a band-ratio depth estimate calibrated on ATL24 photons outside a 5 km radius gives a depth within 5 m of the ATL24 median; (6) no GEBCO Gazetteer feature of type Shoal(s), Reef(s), Bank(s) or Ground lies within 2 km, re-queried live, and no openly downloadable bathymetry model or paper found by search gives a depth within 5 m of the ATL24 median within 2 km. The claim is a candidate discrepancy with GEBCO_2026, not a correction to any nautical chart.

## Partial wins

- **p1:** A site meeting (1) to (4) and (6) with a single granule (one date) instead of two.
- **p2:** A reproducible screening of all latest-version ATL24 granules over one ocean region of at least 1,000,000 km2 (for example the tropical South Pacific) that lists every site meeting (1) to (4), with code and the count of sites per TID code.
- **p3:** A site meeting (1), (2), (4) and (5) in a cell with a direct-measurement TID (10 to 17) where GEBCO_2026 is at least 20 m too deep, saved as evidence of an error in the compiled source data.

## How a win is checked

The skeptic downloads the cited ATL24 granules (free NASA Earthdata login, or the public SlideRule service), re-extracts the photons, recomputes depth below the sea surface and the two medians, samples the GEBCO_2026 depth and TID grids at the photon positions, re-runs the Sentinel-2 band-ratio check and queries the gazetteer. Under an hour.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://www.gebco.net/data-products-gridded-bathymetry-data/gebco2026-grid>

## Sources

- <https://nsidc.org/data/atl24>
- <https://nsidc.org/data/atl24/versions/3>
- <https://nsidc.org/sites/default/files/documents/user-guide/atl24-v003-userguide.pdf>
- <https://www.gebco.net/data-products/gridded-bathymetry-data>
- <https://www.gebco.net/data-products-gridded-bathymetry-data/gebco2026-grid>
- <https://www.gebco.net/news/release-gebco2026-grid>
- <https://services2.arcgis.com/C8EMgrsFcRFL6LrL/arcgis/rest/services/Undersea_Features/FeatureServer>
- <https://earth-search.aws.element84.com/v1/collections/sentinel-2-l2a>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Screen first with the TID grid: keep only shallow-looking GEBCO cells (depth under 100 m) with TID 40 to 72 that ICESat-2 tracks cross, then pull only those granules.
- Atolls and drowned banks in the central Pacific, the Coral Sea, the Chagos and Maldives region and the western Indian Ocean have clear water and sparse surveys.
- Cross-domain import (anomaly detection in sensor fusion): treat GEBCO as a prior and ATL24 as a measurement, and rank cells by the standardised residual.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- ATL24 heights are relative to the EGM08 geoid and uncorrected for tide; the 20 m threshold is set well above tide and datum errors, so do not lower it.
- ATL24 Version 3 removed low_confidence_flag and changed the classifier; criteria written for Version 2 must use the confidence value instead, and results from different versions should not be mixed in one claim.
- Turbid water, breaking waves and the sea-surface return can be mislabelled as seafloor; require confidence at least 0.6 and agreement between two dates.
- GEBCO cells near land can be wrong only because the coastline is misplaced; the 1 km land buffer removes most of these.
- Published satellite-derived bathymetry models already cover some reef groups (for example South China Sea island and reef models in ESSD); search before claiming.
- The Allen Coral Atlas publishes satellite-derived reef bathymetry, but its downloads need an account and licence acceptance, so checking it is a step for the human, outside the win.
- The claim is only the saved verified candidate; whether to tell any hydrographic office is for the human to decide.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/uncharted/icesat2-shoal-not-in-gebco-2026.md
```

Already set up? Say `run V3R1T4S on icesat2-shoal-not-in-gebco-2026`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `icesat2-shoal-not-in-gebco-2026`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
