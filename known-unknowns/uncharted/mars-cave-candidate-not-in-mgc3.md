# New Mars cave-entrance candidate (skylight or atypical pit crater) in public HiRISE and CTX images, absent from the Mars Global Cave Candidate Catalog v1.0 and later published lists

🧭 **Uncharted maps** · harvest (many cells or partial wins within reach) · tractability ★★☆☆☆ · compute: laptop-days (HiRISE RDR images are 0.1 to 2 GB each and CTX images 50 to 300 MB; searches restricted to volcanic plains, lava-tube chains and pit-crater chains) · open as of 2026-11-13

## The problem

Possible cave entrances on Mars include lava-tube skylights, atypical pit craters (rimless, steep-walled pits with no ejecta), deep fractures and other voids. Glen E. Cushing (USGS Astrogeology) compiled the Mars Global Cave Candidate Catalog (MGC3), announced by USGS on 2019-07-26 with more than a thousand candidate entrances, each with a priority rating and comment. The PDS registers it as the Mars Global Cave Candidate Catalog Archive Bundle, urn:nasa:pds:mars_cave_catalog::1.0 (author Cushing, version 1.0, page read 2026-11-13), with its files hosted by USGS Astrogeology; the data.nasa.gov record gives a public-domain licence. Watson and Baldini (2024, Icarus, doi 10.1016/j.icarus.2024.115952) trained a neural network (CaveFinder) on MGC3 images and reported 61 new candidates in four regions, while noting too many false positives for a planet-wide search. Later papers add single candidates outside MGC3, for example a possible lava-tube skylight on the western flank of Elysium Mons (2025, Astronomical Journal, doi 10.3847/1538-3881/adbe32) and possible karstic caves in Hebrus Valles (2025, Astrophysical Journal Letters, doi 10.3847/2041-8213/ae0f1c). No MGC3 version after 1.0 was found on 2026-11-13. HiRISE (0.25 to 0.5 m/pixel) and CTX (about 6 m/pixel) images are public through the PDS. The bank already has the lunar version of this problem against the LROC Pits Atlas; this entry is the Mars catalog. Open task: a cave-entrance candidate that MGC3 v1.0 and later published lists do not hold.

## What counts as a win

A saved bundle (product IDs, map-projected cutouts, illumination geometry from the labels, shadow measurements, code) where: (1) the feature is seen in at least 2 images, at least one from HiRISE, whose solar incidence angles differ by at least 10 deg; (2) the steep-walled opening has a maximum diameter of at least 10 m and spans at least 5 pixels in each image; (3) in each image the shadow edge falls on the floor and the depths from shadow length (corrected for local slope from a HiRISE or CTX DTM or MOLA) agree within 30%, with depth / diameter of at least 0.3; (4) there is no raised rim or ejecta, shown with a radial brightness profile; (5) no MGC3 v1.0 entry lies within 500 m, and the feature is not in the CaveFinder candidate list, the Elysium Mons and Hebrus Valles papers named in the statement, any other published cave or pit list found by search, or the Mars new-impact catalogs (it is not a fresh crater). The claim is a candidate cave entrance, never a confirmed cave.

## Partial wins

- **p1:** A detector that, on images of at least 50 MGC3 entries not used to tune it, recovers at least 80% of them with at most 1 false candidate per 10 km^2 searched, with all candidates saved.
- **p2:** A candidate meeting (2), (4) and (5) in a single HiRISE image, with a single-image depth estimate giving depth / diameter of at least 0.3.

## How a win is checked

The skeptic downloads the cited HiRISE and CTX products from the PDS, re-projects them, re-measures the shadow lengths and incidence angles from the labels, recomputes depth and diameter with the stated slope correction, and checks distances to every MGC3 v1.0 entry and to the published candidate lists. Under an hour per candidate.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://pds.nasa.gov/ds-view/pds/viewBundle.jsp?identifier=urn%3Anasa%3Apds%3Amars_cave_catalog&version=1.0>

## Sources

- <https://pds.nasa.gov/ds-view/pds/viewBundle.jsp?identifier=urn%3Anasa%3Apds%3Amars_cave_catalog&version=1.0>
- <https://astrogeology.usgs.gov/search/map/Mars/MarsCaveCatalog/mars_cave_catalog>
- <https://data.nasa.gov/dataset/mars-global-cave-candidate-catalog-archive-bundle-a89b7>
- <https://www.usgs.gov/news/caves-mars>
- <https://doi.org/10.1016/j.icarus.2024.115952>
- <https://doi.org/10.3847/1538-3881/adbe32>
- <https://doi.org/10.3847/2041-8213/ae0f1c>
- <https://hirise-pds.lpl.arizona.edu/PDS/INDEX/>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Conventional: search along collapse-pit chains and sinuous rilles on the Tharsis and Elysium lava plains with a small CNN trained on MGC3 entries, then confirm with shadow geometry.
- Use the incidence-angle diversity of HiRISE repeat images: a pit's shadow fraction grows faster with incidence than a bowl crater's.
- Cross-domain import (karst mapping on Earth): closed-depression and wall-steepness features used to detect sinkholes in lidar DTMs carry over to HiRISE DTMs.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- The MGC3 files are hosted only by USGS Astrogeology, whose product page returned HTTP 403 to an automated fetch on 2026-11-13, and the data.nasa.gov record lists no files; a human may need to download the catalog by hand, and the exact number of entries must be counted from it.
- Fresh impact craters, dark sand in crater floors and shadows of mesas can mimic pits; the rim, ejecta and two-image depth tests are the safeguards.
- Candidates outside MGC3 keep appearing in single-site papers and reviews (for example the Elysium Mons cave-zone study in npj Space Exploration, 2026, and the review of potential Mars caves in Space Habitation, 2026), and the 2025 University of Kent thesis by Daniel Le Corre searched for cave entrances with machine learning; check them all before claiming.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/uncharted/mars-cave-candidate-not-in-mgc3.md
```

Already set up? Say `run V3R1T4S on mars-cave-candidate-not-in-mgc3`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `mars-cave-candidate-not-in-mgc3`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
