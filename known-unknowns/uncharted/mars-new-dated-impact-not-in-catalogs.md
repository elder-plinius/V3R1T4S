# New dated impact on Mars in public CTX before-and-after images, absent from the Daubar 2022, Wagstaff 2022, Landis 2024 and Bickel 2025 new-impact catalogs and from HiRISE impact targets

🧭 **Uncharted maps** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-days (CTX images are about 50 to 300 MB each; a regional search of a few hundred image pairs is tens of GB; the HiRISE RDR index table is about 169 MB) · open as of 2026-11-13

## The problem

New impacts on Mars are found by comparing repeat orbital images: a new dark, light or dual-toned blast zone appears at one point between a before image and an after image. Daubar, Dundas, McEwen and 15 co-authors, including the Malin Space Science Systems team that runs CTX (Context Camera, about 6 m/pixel), catalogued 1,203 dated impact sites 1 to 58 m in effective diameter, formed within windows of 1 day to 33 years, averaging 4.5 years (Daubar et al. 2022, JGR Planets 127, e2021JE007145); the catalog is strongly biased toward dusty, low thermal inertia ground. Wagstaff, Daubar, Doran, Munje, Bickel, Gao, Pate and Wexler (2022, Icarus 386, 115146) ran a classifier over 112,207 CTX observations taken from 2006-09-27 to 2019-12-01 between 60 deg S and 60 deg N and added 69 HiRISE-checked new impacts. Bickel, Daubar and 10 co-authors (2025, GRL, doi 10.1029/2024GL109133) used machine learning on CTX images to catalog 123 impacts, 1 to 22.5 m, formed during the InSight mission within 50 deg of the lander. Landis, Dundas, McEwen, Daubar and 7 co-authors (2024, Icarus, doi 10.1016/j.icarus.2024.115977) report new dated impacts on the south polar layered deposits, and Podobnaya, Popova, Glazachev and Ivanov (2025, Solar System Research) classify clusters in an expanded catalog of fresh impact sites. HiRISE (University of Arizona) images many reported sites; its PDS RDR index (205,302 rows, updated 2026-11-03, read 2026-11-13) gives each observation a note (RATIONALE_DESC), and web titles such as Candidate New Impact Crater (ESP_087519_1965, 2025-03-28) mark sites not yet published. CTX, HiRISE, CaSSIS and HRSC images are public through the PDS or ESA PSA without use restrictions. Open task: a new impact in public images that none of these lists holds.

## What counts as a win

A saved bundle (product IDs, map-projected cutouts, difference images, code) where: (1) a before image (CTX, MOC narrow-angle or THEMIS VIS, 20 m/pixel or finer) shows no albedo feature at the site and an after CTX image shows a new albedo feature (spot, halo or rays) whose contrast exceeds 5 times the local noise standard deviation over at least 3 x 3 CTX pixels, with solar incidence angles of the two images within 15 deg; (2) the same feature appears in at least one more public orbital image from a different orbit (CTX, HiRISE, CaSSIS or HRSC) taken after the after image; (3) the feature is centred on one point (radial or circular pattern), and dust devil tracks, slope streaks, frost and wind streaks are ruled out by morphology and by an image from another season; (4) no site in the Daubar et al. 2022 catalog table, Tables 1 and 2 of Wagstaff et al. 2022, the Bickel et al. 2025 catalog or the Landis et al. 2024 list lies within 1 km; (5) no HiRISE observation in the live RDRCUMINDEX.TAB (re-fetched immediately before claiming) whose footprint contains the site has a RATIONALE_DESC containing impact or crater together with new, recent, fresh, dated or candidate; (6) no later paper or published table found by search reports it. The claim is a candidate new impact with a dated formation window, never a confirmed crater.

## Partial wins

- **p1:** A detector that, run blind on CTX before-and-after pairs covering at least 20 sites from the Daubar et al. 2022 catalog not used for tuning, recovers at least 80% of them, with the number of false candidates per 1,000 km^2 searched reported and all candidates saved.
- **p2:** A candidate meeting (1), (3), (4) and (5) that has no second after image yet.
- **p3:** A full candidate for which an existing public HiRISE image taken after the formation window shows a crater or crater cluster at the centre of the albedo feature, with its diameter (or effective diameter for a cluster) measured.
- **p4:** A full candidate on terrain with thermal inertia of at least 400 J m^-2 K^-1 s^-1/2 in the TES nighttime thermal inertia map of Putzig and Mellon (2007), where the existing catalogs are sparse.

## How a win is checked

The skeptic downloads the cited images from the PDS (or ESA PSA for CaSSIS and HRSC), map-projects them with ISIS, re-registers the pair, recomputes the difference image and the contrast-to-noise ratio, checks the second-orbit and other-season images, measures the distance to every site in the four catalog tables, filters the live HiRISE RDRCUMINDEX.TAB for footprints containing the site, and searches for later reports. Under an hour per candidate.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://hirise-pds.lpl.arizona.edu/PDS/INDEX/>

## Sources

- <https://doi.org/10.1029/2021JE007145>
- <https://wkiri.com/research/papers/daubar-impacts-22.pdf>
- <https://arxiv.org/abs/2207.05679>
- <https://doi.org/10.1029/2024GL109133>
- <https://wkiri.com/research/papers/bickel-insight-seismic-24.pdf>
- <https://doi.org/10.1016/j.icarus.2024.115977>
- <https://doi.org/10.1134/S003809462460207X>
- <https://hirise-pds.lpl.arizona.edu/PDS/INDEX/>
- <https://hirise-pds.lpl.arizona.edu/PDS/INDEX/RDRCUMINDEX.LBL>
- <https://ode.rsl.wustl.edu/mars/>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Conventional: a Siamese change detector on co-registered CTX pairs, trained on Daubar et al. 2022 sites, run on pairs whose after image is later than December 2019.
- Review candidates in thermal inertia bins rather than by confidence alone, as Wagstaff et al. 2022 did, to reach high thermal inertia ground.
- Cross-domain import (supernova searches): PSF-matched image subtraction (for example the ZOGY method) to cancel illumination and resolution differences between before and after images.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- The Daubar et al. 2022 catalog table is in the paper's supporting information on the Wiley site, which returned HTTP 403 to an automated fetch on 2026-11-13; a human may need to download it by hand.
- The expanded catalog of Podobnaya, Popova, Glazachev and Ivanov (2025) is behind a paywall and its site list was not read on 2026-11-13; if its table is public when you claim, check it as in (6).
- Large new craters reported outside these catalogs, such as the largest recent impact craters linked to InSight marsquakes (Posiolova et al. 2022, Science, doi 10.1126/science.abq7704), are published and do not count; rule (6) covers them.
- The CTX team keeps finding new impacts that are not yet published; the HiRISE observation notes in rule (5) are the only public trace of many of them.
- Seasonal frost, dust storms and dust devil tracks create and erase albedo features; a different incidence angle can make a small existing crater look new.
- Albedo features fade over years, so a feature missing from an old low-resolution image may only have been unresolved; respect the 20 m/pixel limit in (1).
- Craters of one cluster can be hundreds of metres apart; treat all spots within 1 km as one site.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/uncharted/mars-new-dated-impact-not-in-catalogs.md
```

Already set up? Say `run V3R1T4S on mars-new-dated-impact-not-in-catalogs`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `mars-new-dated-impact-not-in-catalogs`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
