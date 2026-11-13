# Seamount or knoll at least 300 m tall in public multibeam sonar data, absent from every global seamount catalog including SDUST2026SM and the Souche-Hartz-Schmid prominence catalog

🧭 **Uncharted maps** · harvest (many cells or partial wins within reach) · tractability ★★☆☆☆ · compute: laptop-hours (catalogs are small: SDUST2026SM 12.7 MB, SIO 2023 zip 4.1 MB, Yesson list 5.3 MB, Souche GeoPackages from PANGAEA; GMRT multibeam tiles are fetched per region, tens of MB each) · open as of 2026-11-13

## The problem

Seamounts are undersea volcanic mountains; smaller ones are called knolls and hills. Most are known only from satellite altimetry: the sea surface bulges over the extra mass, and the vertical gravity gradient (VGG, the change of gravity with height) shows them as spots. Global catalogs, read on 2026-11-13: Kim and Wessel (2011) listed 24,643 seamounts; Gevorgian, Sandwell, Yu, Kim and Wessel (2023, Zenodo 7718512, CC BY 4.0) added 19,325 from the SIO VGG; Yesson, Letessier, Nimmo-Smith, Hosegood, Brierley, Hardouin and Proud predicted 37,889 from a depth grid (PANGAEA 921688). Souche, Hartz and Schmid (2026, Scientific Data 13, 902; PANGAEA 992546, CC BY 4.0) list 125,514 features with prominence of at least 300 m in the GEBCO_2025 grid, plus 143,888 detected peaks. The newest is SDUST2026SM by Gao, Guo, Ya, Yu, Liu and Hwang (ESSD preprint essd-2026-860, comments open to 2026-12-11; Zenodo 23277209, v1.0 of 2026-10-10, CC BY 4.0): 68,934 candidates at least 100 m tall from the Scripps SWOT_04 VGG and GEBCO_2025, 67,374 accepted. The GEBCO Gazetteer of Undersea Feature Names (SCUFN) had 5,412 features on 2026-11-13, 961 of them Seamount points. Multibeam sonar (ship swath echosounders that measure depth directly) covers about 28.7 percent of the seafloor (GEBCO_2026, 2026-04-27) and is gridded in GMRT v4.5.0 (June 2026, CC BY 4.0). Ziolkowski, Devey and Koschmider (2025) found that 16 of 30 seamounts in one multibeam transit were missing from the satellite catalogs. Open task: an edifice that multibeam shows but no catalog lists.

## What counts as a win

A saved bundle (survey or GMRT tile identifiers, masked depth grid of the area, profiles, code) for one edifice where: (1) it lies between 77 S and 77 N; (2) direct multibeam soundings, from the GMRT GridServer topo-mask layer (high-resolution data only) or raw NCEI multibeam files, never interpolated or gravity-predicted cells, cover at least 80% of the area inside its half-height contour, including the summit in inner (non-outer-beam) coverage; (3) its relief, summit depth minus the median depth on a ring at 1.5 times its base radius, is at least 300 m, and its half-height contour is closed with a long to short axis ratio of at most 3; (4) the summit lies inside no polygon of the Souche-Hartz-Schmid catalog (PANGAEA 992546) and no entry of these lies within the larger of 5 km and its base radius of the summit: the Souche detected-peak points (all, including rejected), SDUST2026SM latest Zenodo version (all candidates, visual_pass_flag 1 or 0), the SIO 2023 catalog (Seamounts_Modeled, all), the Kim-Wessel 2011 list (KWSMTSV0.1, including KW_badlist), the Yesson PANGAEA 921688 list, and GEBCO Gazetteer point or polygon features of type Seamount(s), Knoll(s), Hill(s), Guyot(s), Tablemount, Peak, Cone or Bank, all re-fetched just before claiming; (5) no published seamount list or paper found by search names it or gives a seamount within 5 km. The claim is a candidate absent from these catalogs, never a first discovery: a public survey already shows it.

## Partial wins

- **p1:** An edifice meeting (1), (2), (4) and (5) with relief of 150 to 300 m.
- **p2:** Confirmation by direct multibeam soundings, as in (2) and (3), that an SDUST2026SM candidate rejected at visual inspection (visual_pass_flag 0) is a real edifice of at least 300 m relief, with no entry of the other catalogs in (4) within 5 km.
- **p3:** A reproducible comparison of SDUST2026SM and the Souche-Hartz-Schmid catalog against the GMRT topo-mask layer over at least 1,000,000 km2 of multibeam coverage, listing every edifice of at least 300 m relief with its catalog matches or none, and the recall of each catalog by height class.

## How a win is checked

The skeptic downloads the cited GMRT topo-mask grid or the raw NCEI multibeam files, re-grids them, recomputes relief, contour closure and axis ratio, checks that the summit is in inner-beam coverage, and runs the polygon and distance tests against freshly downloaded copies of the six catalogs and a live gazetteer query. Under an hour per candidate.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://zenodo.org/records/23277209>

## Sources

- <https://essd.copernicus.org/preprints/essd-2026-860/>
- <https://zenodo.org/records/23277209>
- <https://zenodo.org/record/7718512>
- <https://doi.pangaea.de/10.1594/PANGAEA.921688>
- <https://doi.pangaea.de/10.1594/PANGAEA.992546>
- <https://www.frontiersin.org/articles/10.3389/fmars.2025.1613061/full>
- <https://services2.arcgis.com/C8EMgrsFcRFL6LrL/arcgis/rest/services/Undersea_Features/FeatureServer>
- <https://www.gebco.net/data-products/undersea-feature-names>
- <https://www.gmrt.org/about/>
- <https://www.gmrt.org/services/gridserverinfo.php>
- <https://www.ncei.noaa.gov/products/seafloor-mapping>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Look where gravity detection is weakest: thick sediment margins, near trenches and ridge axes where large tectonic gravity signals mask small cones, and seamount chains where neighbours merge into one VGG spot.
- Multibeam surveys newer than the GEBCO_2025 grid are the best hunting ground, because the Souche-Hartz-Schmid catalog was built from GEBCO_2025 and already sees older multibeam; compare GMRT v4.5.0 survey dates with the GEBCO_2025 source list.
- Cones on sloping flanks can have relief above 300 m but prominence below 300 m, so they can be missing from a prominence catalog.
- Use the SDUST2026SM rejected candidates (visual_pass_flag 0) as a ready list to check against multibeam for p2.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- GMRT and GEBCO fill unsurveyed cells with gravity-predicted depths; only the GMRT topo-mask layer or raw soundings count as direct data.
- Outer-beam noise, refraction errors and spikes in single swaths can create false cones; require inner-beam coverage of the summit and look at the raw soundings.
- SDUST2026SM is a preprint under review and may change; use the latest Zenodo version at claim time and count rejected candidates as catalog entries.
- SDUST2026SM stores each seamount at a 1 arc-minute grid cell, so positions are uncertain by about 1 to 2 km; that is why the matching radius is at least 5 km.
- Ziolkowski, Devey and Koschmider (2025) already reported multibeam seamounts missing from the satellite catalogs on the SO305-2 transit in the Indian Ocean; those are published and do not count.
- North of 77 N and south of 77 S the SWOT-based catalogs have no coverage, so finds there would say nothing about catalog completeness; they are excluded.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/uncharted/seamount-in-multibeam-not-in-seamount-catalogs.md
```

Already set up? Say `run V3R1T4S on seamount-in-multibeam-not-in-seamount-catalogs`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `seamount-in-multibeam-not-in-seamount-catalogs`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
