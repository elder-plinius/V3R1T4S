# Phantom seamount: a peak of at least 1,000 m relief in the GEBCO_2026 grid that satellite gravity and public soundings show does not exist

🧭 **Uncharted maps** · standard · tractability ★★☆☆☆ · compute: laptop-hours (the GEBCO_2026 grid page gives the global grid as a single 7.0 GB file and the TID grid as a single 3.5 GB file; SDUST2025GRA_SWOT gravity 1.8 GB; DTU21 gravity about 1 GB; catalogs a few MB) · open as of 2026-11-13

## The problem

Global depth grids contain false features. Yesson, Letessier, Nimmo-Smith, Hosegood, Brierley, Hardouin and Proud (2021, UCL Open Environment 3, e030, doi 10.14324/111.444/ucloe.000030) found 15 phantom seamounts that persist in global grids, listed by peak ID in their Table 1; they traced them to old chart soundings marked no bottom at this depth being read as summits, after a 2016 survey in the British Indian Ocean Territory found no trace of two predicted seamounts. GEBCO_2026 (released 2026-04-27, public domain) records the source of each cell in its Type Identifier (TID) grid, and its gravity-predicted base, SRTM15+ V2.8, uses SWOT gravity and machine learning (Sandwell and colleagues, 2025). A real edifice 1,000 m tall leaves a clear signal in modern satellite gravity: SDUST2026SM (Gao and colleagues, Zenodo 23277209) lists a peak vertical gravity gradient for each of its 67,374 accepted seamounts. Independent gravity fields are public: SDUST2025GRA_SWOT (Zhang, Guo, Ya, Bian, Jia and Liu; Zenodo 21408557, 2026-07-17, CC BY 4.0, ESSD preprint essd-2026-712 under review, 3.82 mGal RMS against ship gravity) from SWOT, and DTU21 (Andersen and Knudsen, DTU Space) from conventional altimeters. Open task, read on 2026-11-13: a large peak in GEBCO_2026 that the gravity and the soundings both contradict.

## What counts as a win

A saved bundle (grid windows, gravity profiles, survey identifiers, code) for one peak where: (1) it is a local maximum of the GEBCO_2026 grid between 77 S and 77 N whose summit stands at least 1,000 m above the median depth on a ring 15 to 25 km away; (2) no GEBCO_2026 cell within 2 km of the summit has TID 11, 15, 16 or 17 (multibeam, lidar, optical or combined direct); (3) the vertical gravity gradient computed from the SDUST2025GRA_SWOT grid (standard wavenumber-domain vertical derivative after removing a 50 km regional median) has its largest value within 5 km of the summit below the 5th percentile of the same quantity computed at at least 50 SDUST2026SM accepted seamounts whose height is within 25% of the GEBCO relief and whose base depth is within 1,000 m; (4) at least one public direct survey (an NCEI multibeam or single-beam trackline, or a GMRT swath) passes within 2 km of the summit and, along 10 km of track centred on its closest approach, is nowhere shallower than the ring median minus 200 m; (5) it is not one of the 15 phantoms in Table 1 of Yesson and colleagues and no paper found by search reports it as a phantom. The claim is a candidate phantom, never an official correction.

## Partial wins

- **p1:** A peak meeting (1), (2), (3) and (5) without a crossing survey (gravity evidence only).
- **p2:** A GEBCO Gazetteer point feature of type Seamount, Guyot, Tablemount, Knoll, Peak, Bank or Shoal where at least 90% of the GEBCO_2026 cells within 10 km have TID 11 (multibeam) and no closed high of at least 100 m relief (500 m for Seamount, Guyot or Tablemount) lies within 10 km, with the gazetteer re-queried live.
- **p3:** A reproducible global screen listing every GEBCO_2026 peak that meets (1) and (2), with its gravity score from (3), saved with code.

## How a win is checked

The skeptic downloads GEBCO_2026 windows and TID values, recomputes relief, recomputes the gravity gradient from both gravity grids and the reference percentile from SDUST2026SM, downloads the crossing survey from NCEI or GMRT and plots the profile, and checks the peak against Table 1 of Yesson and colleagues. Under an hour.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://www.gebco.net/data-products/gridded-bathymetry-data/data-set-errata>

## Sources

- <https://www.gebco.net/data-products-gridded-bathymetry-data/gebco2026-grid>
- <https://www.gebco.net/data-products/gridded-bathymetry-data>
- <https://researchportal.plymouth.ac.uk/en/publications/improved-bathymetry-leads-to-gt4000-new-seamount-predictions-in-t-2/>
- <https://pmc.ncbi.nlm.nih.gov/articles/PMC10171409>
- <https://doi.pangaea.de/10.1594/PANGAEA.921688>
- <https://zenodo.org/records/23277209>
- <https://zenodo.org/records/21408557>
- <https://essd.copernicus.org/preprints/essd-2026-712/>
- <https://ftp.space.dtu.dk/pub/DTU21/>
- <https://services2.arcgis.com/C8EMgrsFcRFL6LrL/arcgis/rest/services/Undersea_Features/FeatureServer>
- <https://www.gebco.net/news/release-gebco2026-grid>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Rank all GEBCO_2026 peaks by the ratio of observed to expected gravity gradient, where the expected value comes from a regression on SDUST2026SM seamounts of similar height and base depth.
- Look at cells with TID 42 or 43 (chart contours) and 10 or 13 (single soundings), where Yesson and colleagues found the known phantoms came from.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Seamounts buried in sediment or sitting on thick crust can have weak gravity signals; the percentile test against similar seamounts is the safeguard, and a crossing survey is required for the full win.
- Peaks next to trenches, fracture zones or large islands sit in large regional gravity signals; remove a regional trend before computing the gradient.
- The reference seamounts come from a catalog built from SWOT gravity, so they are biased towards strong gravity signals; that is one more reason the full win needs a crossing survey.
- Pre-SWOT gravity fields such as DTU21 do not resolve seamounts below about 1.5 km reliably; use them only as a supporting view, never as the test in (3).
- SDUST2025GRA_SWOT is a preprint data set under review and holds gravity anomaly and deflection of the vertical, not the gradient itself; compute the gradient and cite the Zenodo version used.
- The UCL Press article page showed a bot check on 2026-11-11 and 2026-11-13; the PubMed Central copy opened on 2026-11-13 and holds Table 1 with the 15 phantom peak IDs, which are the IDs of the PANGAEA 921688 list.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/uncharted/phantom-seamount-in-gebco-2026.md
```

Already set up? Say `run V3R1T4S on phantom-seamount-in-gebco-2026`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `phantom-seamount-in-gebco-2026`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
