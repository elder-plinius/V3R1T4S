# New lunar impact crater formed during the LRO mission, in public LROC NAC before-and-after images, absent from the LROC New Craters shapefile (version of 2025-02-25) and later papers

🧭 **Uncharted maps** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-days (LROC NAC frames are 100 to 500 MB each; finding pairs with matched lighting needs only the PDS index tables, but checking hundreds of pairs is tens to hundreds of GB) · open as of 2026-11-13

## The problem

The LROC Narrow Angle Cameras (NAC, 0.5 to 2 m/pixel) on the Lunar Reconnaissance Orbiter (LRO) have imaged the Moon since 2009, and every image is public through the PDS without use restrictions. Speyerer, Povilaitis, Robinson, Thomas and Wagner (2016, Nature 538, 215) compared about 14,000 NAC temporal pairs (the same place under the same lighting, years apart) and found 222 new impact craters and over 47,000 smaller reflectance changes called splotches. In a 2019 GSA abstract Speyerer, Povilaitis, Robinson and Wagner reported over 500 new craters, up to 70 m across, and over 120,000 splotches. The LROC team at Arizona State University publishes the craters as an RDR product, the New Craters shapefile (SHAPEFILE_GLOBAL_NEW_CRATERS in PDS volume LROLRC_2001, with fields lat, lon, before_img, after_img and diam_m), last updated 2025-02-25 (page read 2026-11-13). In September 2026 Robinson, Boyd, Mahanti, Manheim, Speyerer, Stopar and Wagner (Science Advances, doi 10.1126/sciadv.aeh7812) reported a 222 m crater that formed in spring 2024, found by a routine comparison of Wide Angle Camera (WAC) image sets; it is newer than the shapefile. Speyerer and colleagues (2026, Planetary Science Journal and GRL) and Powell and colleagues (2026, Science Advances) study the rays, photometry and night-time cold spots of new craters, but none of these abstracts announces an updated crater list (read 2026-11-13). The shapefile is built from pairs the team targeted; many other pairs of NAC images with similar lighting exist in the archive by chance, and baselines now exceed 15 years. Open task: a crater that formed during the mission and is not in the shapefile or in any later paper.

## What counts as a win

A saved bundle (NAC product IDs, calibrated and map-projected cutouts, ratio image, code) where: (1) a before and an after NAC image have solar incidence angles within 5 deg, sub-solar azimuths within 10 deg and pixel scales within a factor 1.5; (2) the after image shows a crater whose rim diameter spans at least 5 after-image pixels and at least 3 before-image pixels, with interior shadow on the side facing the Sun, and the before image shows no crater there; (3) the after-to-before ratio image shows a reflectance change (halo or rays) centred on the crater; (4) a second after NAC image from a different orbit shows the same crater; (5) no point in the New Craters shapefile, downloaded again immediately before claiming, lies within 300 m, and no paper found by search (including Robinson et al. 2026) lists it. The formation window is stated as the time between the two acquisitions. The claim is a candidate new crater.

## Partial wins

- **p1:** A detector that, on NAC pairs of at least 30 shapefile craters not used to tune it, recovers at least 80% of them, with the number of false candidates per pair reported and all candidates saved.
- **p2:** A candidate meeting (1), (2), (3) and (5) that has no second after image yet.
- **p3:** For a shapefile crater, a public NAC image taken between its before_img and after_img (meeting the lighting rule of (1) against one of them) that shows the crater present or absent, shortening the formation window by at least 50%.

## How a win is checked

The skeptic downloads the NAC products from the PDS, calibrates and map-projects them with ISIS (lronaccal, lronacecho, cam2map), checks the lighting geometry in the labels, rebuilds the ratio image, measures the crater in each image, checks the distance to every point in the freshly downloaded shapefile, and searches for later papers. Under an hour per candidate.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://data.lroc.im-ldi.com/lroc/view_rdr/SHAPEFILE_GLOBAL_NEW_CRATERS>

## Sources

- <https://data.lroc.im-ldi.com/lroc/view_rdr/SHAPEFILE_GLOBAL_NEW_CRATERS>
- <https://doi.org/10.1038/nature19829>
- <https://studio.m-anage.com/gsa/2019AM/webprogram/Paper340819.html>
- <https://doi.org/10.1126/sciadv.aeh7812>
- <https://doi.org/10.3847/PSJ/ae4a06>
- <https://pds.lroc.im-ldi.com/>
- <https://ode.rsl.wustl.edu/moon/>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Conventional: query the NAC index for all overlapping image pairs with matched lighting, then run a ratio-image change detector and review the strongest compact changes.
- Start from splotches: a splotch with a dark or bright centre larger than 5 pixels is the most likely place for an unlisted crater.
- Powell and colleagues (2026) report that new craters larger than about 30 m all leave a Diviner night-time cold spot; public Diviner data can point to where to look in the NAC archive.
- Cross-domain import (Earth change detection): coregistration and illumination-normalised differencing used for landslide and building change in very high resolution satellite imagery.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- The 222 m crater of Robinson et al. (2026), at about 1.35 deg N, 67.18 deg E and formed in spring 2024, is not in the 2025-02-25 shapefile but is published, so it does not count; the LROC team runs routine WAC comparisons and may publish more.
- Different lighting turns boulders and small existing craters into apparent changes; keep rule (1) strict.
- Most reflectance changes are splotches with no resolvable crater; a splotch alone is not a win.
- Single-image artefacts (cosmic-ray hits, compression blocks, NAC left-right seam) can mimic a small dark spot; rule (4) guards against them.
- The shapefile page did not state its number of features on 2026-11-13; download it and count before comparing.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/uncharted/lunar-new-crater-not-in-lroc-new-craters.md
```

Already set up? Say `run V3R1T4S on lunar-new-crater-not-in-lroc-new-craters`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `lunar-new-crater-not-in-lroc-new-craters`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
