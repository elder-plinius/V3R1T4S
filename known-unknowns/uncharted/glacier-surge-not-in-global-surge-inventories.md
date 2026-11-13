# Glacier surge in open ITS_LIVE velocities and DEM elevation change at a glacier absent from the global surge-type inventories

🧭 **Uncharted maps** · harvest (many cells or partial wins within reach) · tractability ★★☆☆☆ · compute: laptop-hours (ITS_LIVE Zarr datacubes read per glacier, MB to a few hundred MB each; ArcticDEM or REMA strip windows; RGI 7.0 outlines) · open as of 2026-11-13

## The problem

A surge is a period of months to years when a glacier flows 10 to 100 times faster than normal, moving ice from an upper reservoir to the tongue, after decades of slow flow. Lovell and 14 co-authors (Nature Reviews Earth and Environment 7, 162-180, 2026) classify more than 3,100 glaciers worldwide as surge-type, with their inventory open on Zenodo (version v3, published 2026-02-12, CC BY 4.0). Guillet, Benn, King, Shean, Mannerfelt and Hugonnet (Journal of Glaciology 71, e88, 2025) screened 32,133 glaciers with ITS_LIVE velocities, DEM elevation change and Sentinel-1 backscatter and detected 261 surges on 246 glaciers in 2000-2024; their rule needs elevation change plus either a speed-up of at least 2 times baseline for at least 120 days or a backscatter change, and they say it is conservative and only analysed flowlines longer than about 2.4 km. ITS_LIVE (NASA JPL, Gardner and colleagues) is open on AWS with no account (CC0). Open task: a surge at a glacier that no inventory lists as surge-type.

## What counts as a win

A saved bundle (RGI 7.0 glacier ID, ITS_LIVE datacube extracts, DEM strip IDs, profiles, code) where: (1) along the glacier's RGI 7.0 flowline, ITS_LIVE image-pair velocities over a segment of at least 2 km are at least 3 times the glacier's own median velocity for that segment for at least 120 days, supported by at least 10 image pairs from at least 2 sensors; (2) a second, independent data set (two co-registered ArcticDEM or REMA strips, another public DEM pair, or ICESat-2 repeat tracks) shows the surge mass transfer: thinning of at least 5 m in the upper part and thickening of at least 5 m in the lower part of the glacier, or an advance of the front of at least 200 m with thickening behind it; (3) for a glacier ending in water, the speed-up starts upstream and the front advances, so it is not a retreat-driven acceleration; (4) the glacier (matched by RGI 7.0 ID and by outline overlap) is not listed in the newest Lovell et al. inventory (re-fetched immediately before claiming) in any class, is not among Guillet et al. 2025's 246 glaciers, and is not in any regional surge inventory found by search. The claim is a candidate surge-type glacier.

## Partial wins

- **p1:** A blind ITS_LIVE screening of one RGI region that recovers at least 80% of Guillet et al. 2025's surges in that region, with every other detection saved and hand-vetted.
- **p2:** A new surge event (onset in 2024 or later) meeting rules (1) and (2) at a glacier already known as surge-type, absent as an event from Guillet et al. 2025 and from the regional event lists found by search.
- **p3:** For a glacier that the newest Lovell et al. inventory lists only in a lower-confidence class (as its own class field states), evidence meeting rules (1) to (3).

## How a win is checked

The skeptic reads the ITS_LIVE datacube for the glacier from the public bucket, recomputes the velocity ratio and pair count along the RGI 7.0 flowline, recomputes the DEM differences after co-registration, and looks the glacier up in the newest Lovell et al. inventory, the Guillet et al. list and regional inventories. About an hour.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://zenodo.org/records/15600657/latest>

## Sources

- <https://zenodo.org/records/15600657/latest>
- <https://www.cambridge.org/core/product/F8F43F9A6A151A92FDD11C451213591F/core-reader>
- <https://registry.opendata.aws/its-live-data/>
- <https://registry.opendata.aws/pgc-arcticdem/>
- <https://nsidc.org/data/nsidc-0770/versions/7>
- <https://zenodo.org/records/18033216>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Screen short glaciers (flowlines under 2.4 km) that Guillet et al. did not analyse, with a lower velocity grid tolerance and DEM evidence.
- Cross-domain import (epidemic onset detection): a CUSUM detector per flowline cell flags a sustained speed-up that propagates downglacier.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- ITS_LIVE image pairs contain mismatches that produce isolated fast values; require many pairs and two sensors.
- Tidewater glaciers speed up when the front retreats; that is not a surge.
- Seasonal speed-ups in spring can double flow for weeks; the 120-day rule and the DEM evidence exclude them.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/uncharted/glacier-surge-not-in-global-surge-inventories.md
```

Already set up? Say `run V3R1T4S on glacier-surge-not-in-global-surge-inventories`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `glacier-surge-not-in-global-surge-inventories`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
