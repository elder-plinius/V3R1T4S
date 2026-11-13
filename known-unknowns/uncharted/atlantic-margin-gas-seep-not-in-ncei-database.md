# Seafloor gas seep (bubble flare) in public water-column sonar data off the US Atlantic coast, absent from the NCEI US Atlantic margin cold seeps database

🧭 **Uncharted maps** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-days (raw multibeam water-column files are several GB per survey day on the public noaa-wcsd-pds bucket; a targeted search reads tens to hundreds of GB) · open as of 2026-11-13

## The problem

Cold seeps are places where methane gas bubbles out of the seafloor. Bubble streams show up in water-column sonar images as tall, thin flares rising from the bottom. Skarke, Ruppel, Kodis, Brothers and Lobecker (2014, Nature Geoscience 7, 657-661) found about 570 seeps between Cape Hatteras and Georges Bank in NOAA Ship Okeanos Explorer data. The current inventory is the US Atlantic margin cold seeps database 2011-2016 (NCEI, doi 10.25921/xm5q-p940, issued 2024-04-18, CC0, no updates planned; Skarke, Ruppel, Kidiwela, Kodis, Danforth and Baldwin), described by Ruppel, Skarke, Miller, Kidiwela, Kluesner and Baldwin (2024, Marine Geology 471, 107287): 2,052 raw flare identifications, 1,139 unique seeps after merging points within 40 m, and 274 locations after 400 m clustering, between about 32.4 N and 40.8 N at about 50 to 2,650 m depth. It covers surveys from 2011 to 2016 only. Later surveys are public in the NOAA Water-Column Sonar Data Archive (run by NCEI with CIRES) on the AWS bucket noaa-wcsd-pds, which can be read without an account: for example EM302 and EK60 water-column data from Okeanos Explorer cruise EX1903 (June to July 2019, southeastern US margin, CC0) and EK60 and EK80 data from NOAA fisheries surveys. Open task, read on 2026-11-13: a seep in these later data that the database does not list.

## What counts as a win

A saved bundle (cruise IDs, file names, ping times, echogram images, positions and code) where: (1) a flare of elevated backscatter, at least 6 dB above the surrounding water column, rises continuously from the seafloor for at least 50 m or 20% of the water depth, whichever is smaller, and is anchored at the seafloor in every ping showing it; (2) it is seen on at least 2 separate passes at least 1 day apart (different survey lines or cruises), with seafloor origins within 100 m of each other, which rules out fish schools and single-ping noise; (3) it lies inside the database bounding box (32.37 N to 40.81 N, 67.30 W to 76.43 W) at a water depth of 50 to 2,700 m; (4) the seafloor origin is more than 500 m from every entry of the database raw identification table (all 2,052, any quality), downloaded fresh from NCEI just before claiming; (5) no published seep list, cruise report or paper found by search gives a seep within 500 m. The claim is a candidate seep absent from the database, not a confirmed methane source.

## Partial wins

- **p1:** A flare meeting (1), (3), (4) and (5) on a single pass.
- **p2:** A detector that, run blind on at least 3 survey days of 2011 to 2016 water-column data on the bucket, recovers at least 80% of the database raw identifications on those lines (a detection matches when its seafloor origin is within 100 m of an identification from the same cruise), with at most 1 unmatched detection per 10 km of track, all saved.
- **p3:** A seep cluster of the database re-observed in post-2016 data on at least 3 passes on different days, each pass with a flare meeting (1) whose origin is within 400 m of a cluster member, with a saved per-pass flare count.

## How a win is checked

The skeptic downloads the cited raw files from the public noaa-wcsd-pds bucket, regenerates the echograms with open tools (for example echopype or MB-System), checks seafloor anchoring and the two-pass agreement, and runs the 500 m distance test against a fresh download of the NCEI database. About an hour per candidate.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://catalog.data.gov/dataset/us-atlantic-margin-cold-seeps-database-2011-2016>

## Sources

- <https://catalog.data.gov/dataset/us-atlantic-margin-cold-seeps-database-2011-2016>
- <https://doi.org/10.25921/xm5q-p940>
- <https://www.usgs.gov/publications/methane-seeps-us-atlantic-margin-updated-inventory-and-interpretative-framework>
- <https://registry.opendata.aws/ncei-wcsd-archive/>
- <https://cires.gitbook.io/ncei-wcsd-archive>
- <https://catalog.data.gov/dataset/em302-water-column-sonar-data-collected-during-ex1903l2>
- <https://catalog.data.gov/dataset/ek60-water-column-sonar-data-collected-during-ex1903l1>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Start from post-2016 cruises that crossed the database's dense seep clusters (shelf break and upper slope at 150 to 550 m) and search their surroundings, where new neighbours are most likely.
- Fisheries echosounder surveys (EK60, EK80 at 18 and 38 kHz) cross the shelf break many times a year; flares there are long-lived and can be checked across years.
- Cross-domain import (particle-track finding in physics): a Hough transform for near-vertical lines anchored at the bottom echo separates flares from horizontal fish layers.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Fish schools, the deep scattering layer, side-lobe echoes and seafloor multiples can mimic flares; require bottom anchoring and two passes on different days.
- Positions of flares far off nadir in multibeam data need the beam angle and sound-speed correction; use the processed seafloor origin, not the ship position.
- Seeps are intermittent; a flare missing on one pass does not disprove it, but a single pass is only partial win p1.
- The database covers 2011 to 2016 surveys only; seeps found in later cruise reports may exist in papers but not in the database, so search the literature.
- Unmatched detections in p2 may be real seeps the database missed, so p2 counts them all as unmatched; report them separately rather than arguing them away.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/uncharted/atlantic-margin-gas-seep-not-in-ncei-database.md
```

Already set up? Say `run V3R1T4S on atlantic-margin-gas-seep-not-in-ncei-database`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `atlantic-margin-gas-seep-not-in-ncei-database`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
