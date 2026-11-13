# Predict unmapped seafloor: a depth grid built only from data public before a cutoff that beats GEBCO_2026 on multibeam surveys of seafloor first measured after the cutoff

🧭 **Uncharted maps** · standard · tractability ★★☆☆☆ · compute: laptop-days (GEBCO_2026 grid 7 GB uncompressed; SWOT and conventional gravity grids 1 to 2 GB each; evaluation surveys tens of GB of multibeam) · open as of 2026-11-13

## The problem

About 71% of the seafloor is not yet mapped to modern standards (Seabed 2030 figure of 28.7% mapped, announced with GEBCO_2026 on 2026-04-27); depths there in global grids are interpolated or predicted from satellite gravity. Harper and Sandwell (2024, Earth and Space Science 11, doi 10.1029/2023EA003199) trained a neural network on about 50 million soundings and cut the RMS (root mean square) error of predicted depth on geographic hold-out bins from 165 m to 138 m. The SRTM15+ V2.8 base of the GEBCO_2026 grid uses SWOT gravity and machine learning (Sandwell and colleagues, 2025), and GEBCO_2026 flags these predicted cells with TID 40 in its Type Identifier grid. Other groups report lower errors on their own test sets (for example BathDNN25 from the University of Tasmania, 2025), which are not comparable. New multibeam surveys reach the public archives (NOAA NCEI, GMRT v4.5.0 of June 2026) every month, so predictions fixed now can be scored on seafloor nobody had measured. Open task, read on 2026-11-13: a predicted depth grid that beats GEBCO_2026 in its own predicted cells, scored on seafloor first surveyed after the predictions were fixed.

## What counts as a win

The claimant fixes a cutoff date C no earlier than 2026-04-27 and releases code that builds a depth grid, on the GEBCO 15 arc-second lattice, using only data sets published before C (for example GEBCO_2026, SWOT-based and conventional gravity grids, sediment-thickness grids and soundings already public), each named with its source, version and checksum. The skeptic re-runs the code offline with only those inputs and gets the same grid. Evaluation set: every GEBCO_2026 cell with TID 40 that holds at least 3 multibeam soundings from public NCEI or GMRT surveys whose acquisition began after C, and that lies more than 1 km from any sounding of a survey acquired before C in the NCEI multibeam and trackline archives, with at least 20,000 such cells from at least 3 surveys in at least 2 ocean basins; the measured depth of a cell is the median of its soundings. The grid wins if its RMS error over these cells is STRICTLY LOWER (direction: min) than that of GEBCO_2026 by at least 5% relative, its median absolute error is also lower, the improvement holds in a bootstrap over surveys (95% interval of the RMS difference excludes zero), and it also beats, on the same cells, any other public global depth grid released before C that the NOVELTY skeptic finds.

## Partial wins

- **p1:** The same test on a single survey of at least 2,000 evaluation cells (same rules for C and for excluding cells near earlier soundings), with RMS lower than GEBCO_2026 by at least 5% relative.
- **p2:** A frozen, re-runnable pipeline (inputs published before C only) whose RMS on at least 20,000 evaluation cells from at least 3 post-C surveys is within 2% of GEBCO_2026, with full residual maps saved.
- **p3:** Lower RMS than GEBCO_2026 on the evaluation cells within 20 km of SDUST2026SM seamounts (at least 5,000 cells), where gravity prediction of steep relief is hardest.

## How a win is checked

The skeptic checks the input list and publication dates, re-runs the code offline, lists post-C multibeam surveys from the NCEI and GMRT archives, bins their soundings into 15 arc-second cells, keeps cells with TID 40 in GEBCO_2026 that are more than 1 km from any pre-C sounding in the NCEI archives, and computes RMS, median absolute error and the survey bootstrap for both grids. A few hours.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://www.gebco.net/data-products/gridded-bathymetry-data>

## Sources

- <https://www.gebco.net/data-products/gridded-bathymetry-data>
- <https://www.gebco.net/data-products-gridded-bathymetry-data/gebco2026-grid>
- <https://www.gebco.net/news/release-gebco2026-grid>
- <https://www.ncei.noaa.gov/products/seafloor-mapping>
- <https://www.gmrt.org/about/>
- <https://seabed2030.org/wp-content/uploads/2023/09/3.3_HughHarper-predicted-depth.pdf>
- <https://zenodo.org/records/21408557>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Combine two SWOT-based gravity fields with conventional altimetry and use the GEBCO_2026 TID grid to weight training cells by measurement type.
- Model seamounts explicitly (cones fitted to the SDUST2026SM catalog) on top of a smooth gravity-predicted background, since gravity prediction tends to underestimate steep relief.
- Cross-domain import (image super-resolution): train on multibeam-covered tiles to map the gravity grid plus the coarse GEBCO depth to the measured depth, with geographic hold-out blocks.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Random train and test splits of soundings leak information; Harper and Sandwell split by geographic bins, and so must any internal validation.
- Cells already surveyed before C by surveys missing from GEBCO_2026 would let a grid win by copying newer soundings instead of predicting; the 1 km exclusion from pre-C soundings removes them, so do not drop it.
- A survey acquired after C may already be inside a grid released between C and the evaluation; only inputs published before C are allowed, which the offline re-run enforces.
- Multibeam soundings and GEBCO use slightly different vertical references and grid registrations; use cell medians and the GEBCO cell centres exactly as the GEBCO documentation defines them.
- The evaluation needs post-C surveys of new seafloor to exist in the archives; early claims may have to wait until at least 3 surveys are public.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/uncharted/unmapped-seafloor-depth-forecast-beat-gebco-2026.md
```

Already set up? Say `run V3R1T4S on unmapped-seafloor-depth-forecast-beat-gebco-2026`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `unmapped-seafloor-depth-forecast-beat-gebco-2026`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
