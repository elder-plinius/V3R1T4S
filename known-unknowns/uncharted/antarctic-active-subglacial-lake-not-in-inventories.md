# Active subglacial lake in ICESat-2 ATL15 height change, confirmed in REMA or CryoSat-2, absent from all published Antarctic lake inventories

🧭 **Uncharted maps** · standard · tractability ★★☆☆☆ · compute: laptop-hours (ATL15 1 km Antarctic grids read region by region, file sizes not stated on the NSIDC page; REMA 2 m strip windows of tens of MB) · open as of 2026-11-13

## The problem

Active subglacial lakes fill and drain under the Antarctic ice sheet; the ice surface above them rises and falls by decimetres to metres. Livingstone and colleagues (Nature Reviews Earth and Environment 2022) built the first global inventory of 773 subglacial lakes, 675 of them in Antarctica. Wilson, Hogg, Rigby, Gourmelen, Slater and Nias (Nature Communications 16, 8311, 2025) found 85 new active lakes in CryoSat-2 data for 2010-2020, raising the known active lakes from 146 to 231 and all Antarctic lakes to 766, but CryoSat-2 SARIn mode covers only 43% of the ice sheet and they state that over half the continent is unexplored. Regional ICESat-2 studies keep adding lakes: Arthur and colleagues (The Cryosphere 2025) found 7 in coastal Dronning Maud Land and Feng, Dong, Chen and Hao (The Cryosphere 20, 2417, 2026) found 14 at Recovery Ice Stream. ATL15 (Smith, Sutterley, Fricker and colleagues, version 6, NSIDC) grids ICESat-2 height change at 1 km every quarter from 2019 to the present over the whole ice sheet. On 2026-11-13 no continent-wide ATL15 lake census was found. Open task: a new active lake candidate.

## What counts as a win

A saved bundle (ATL15 granule names, anomaly time series, outline, REMA strip IDs or CryoSat-2 file names, code) where: (1) in ATL15 version 6 a contiguous area of at least 4 km^2 rises or falls, relative to a surrounding ring 5 to 15 km away, by at least 0.5 m and at least 5 times the ATL15 height-change uncertainty, either with at least one reversal (fill then drain or the reverse) or as a single sustained change of at least 1 m over at least 4 quarters; (2) the area is grounded ice at least 10 km inland of the grounding line, so that tides cannot explain it; (3) a second, independent data set confirms a change of the same sign and at least 50% of the ATL15 amplitude over the same area and an overlapping time span: two co-registered REMA strips, or a CryoSat-2 elevation time series; (4) the same detector, run over the searched area with ATL15 quarters randomly permuted (200 permutations), gives an expected false count below 0.05 at the candidate's score; (5) the candidate outline lies more than 10 km from every lake in the Wilson et al. 2025 outlines and supplementary table, the Livingstone et al. 2022 inventory, Arthur et al. 2025, Feng et al. 2026 and any other inventory or paper found by search immediately before claiming. The claim is a candidate active subglacial lake.

## Partial wins

- **p1:** A blind detector that finds at least 90% of the known active lakes whose published outlines contain an ATL15 height change of at least 0.5 m in 2019 or later, with at most 1 unexplained detection per 100,000 km^2 searched, all detections saved.
- **p2:** A candidate meeting rules (1), (2), (4) and (5) without the independent confirmation of rule (3).
- **p3:** First evidence of activity at a lake that Livingstone et al. 2022 list as a radar-detected lake with no active record: an ATL15 change meeting rule (1) over it, confirmed as in rule (3).

## How a win is checked

The skeptic downloads the cited ATL15 granules (free NASA Earthdata Login) and REMA strips (open AWS bucket, no account), recomputes the anomaly against the ring, the permutation null and the second data set's change, and measures distances to all lakes in the cited inventories. A few hours.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://zenodo.org/records/16330564>

## Sources

- <https://pmc.ncbi.nlm.nih.gov/articles/PMC12449472/>
- <https://zenodo.org/records/16330564>
- <https://nsidc.org/data/atl15/versions/6>
- <https://eprints.whiterose.ac.uk/180688/1/Livingstone_etal_accepted.pdf>
- <https://tc.copernicus.org/articles/19/375/2025/>
- <https://tc.copernicus.org/articles/20/2417/2026/>
- <https://registry.opendata.aws/pgc-rema/>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Search first outside the CryoSat-2 SARIn mask (the interior, where Wilson et al. could not look) and under slow ice, where small lakes give clean signals.
- Use hydraulic potential from BedMachine Antarctica to rank anomalies: lakes sit in potential minima along modelled water paths.
- Cross-domain import (astronomical transient search): treat each ATL15 cell as a light curve and run a matched filter for fill-drain shapes against a permutation null.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Ice-dynamic thinning on fast ice streams and firn compaction changes give broad, smooth height changes; a lake signal is local, bounded and differs from its ring.
- ATL15 edges and cells with few ICESat-2 crossings are noisy; use the product's own uncertainty fields.
- ATL15 needs a free NASA Earthdata Login, which a human must create; REMA strips need no account.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/uncharted/antarctic-active-subglacial-lake-not-in-inventories.md
```

Already set up? Say `run V3R1T4S on antarctic-active-subglacial-lake-not-in-inventories`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `antarctic-active-subglacial-lake-not-in-inventories`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
