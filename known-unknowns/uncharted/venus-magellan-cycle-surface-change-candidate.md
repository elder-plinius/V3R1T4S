# MOONSHOT - New surface-change candidate on Venus between Magellan radar cycles, beyond the Maat Mons, Sif Mons and Niobe Planitia sites

🧭 **Uncharted maps** · moonshot (famous, long odds) · tractability ★★☆☆☆ · compute: laptop-days (Magellan F-BIDR swaths and F-MIDR mosaics at about 75 m/pixel are tens to hundreds of MB each; a regional search over the areas imaged twice is tens of GB) · open as of 2026-11-13

## The problem

Magellan mapped about 98% of Venus with synthetic aperture radar (SAR, a radar that builds images from echoes) in three cycles between 1990 and 1992; parts of the surface were imaged two or three times. Herrick and Hensley (2023, Science 379, 1205) found that a vent of about 2.2 km^2 on Maat Mons changed shape in the 8 months between two images. Sulcanese, Mitri and Mastrogiuseppe (2024, Nature Astronomy; EPSC 2024 abstract 891) compared cycle 1 and cycle 3 full-resolution images, both left-looking, and found brighter flow-like deposits of about 30 km^2 on the west flank of Sif Mons and about 45 km^2 of new bright sinuous lineations in western Niobe Planitia. Campbell and Hensley (Icarus 407, 115773, online 2023) discuss how differences in viewing geometry limit change detection. The detections are debated: Filiberto and 14 co-authors (2025, Geochemistry) assessed the evidence, Bhiravarasu and 10 co-authors questioned it in Nature Astronomy on 2026-04-22, and Sulcanese, Mitri and Mastrogiuseppe replied the same day. Gao and colleagues (2026, JGR Planets) proposed a change detector for Magellan images but tested it only on simulated changes and Earth analogues. Of the 90 works citing Herrick and Hensley in the Semantic Scholar list on 2026-11-13, none has a title announcing a further detection. All Magellan data are public, without use restrictions, at the PDS Geosciences Node. Open task: a further candidate change site.

## What counts as a win

A saved bundle (Magellan product IDs for both cycles, tie points, despeckled co-registered images, change map, code) where: (1) the two images share a look direction and their incidence angles at the site differ by at most 10 deg, and after an incidence correction (for example a Muhleman-law fit) the backscatter of the surrounding same-unit terrain differs by at most 1 dB; (2) the change region covers at least 1 km^2 (about 180 pixels at 75 m) with a mean backscatter change of at least 3 dB, above the 99.9th percentile of the change measured in at least 100 control windows of the same size from the same image pair; (3) the region avoids swath edges and data gaps, lies on local slopes under 10 deg from Magellan altimetry, and either follows topography downhill from a source or is confined to a vent; (4) it is more than 50 km from the Maat Mons, Sif Mons and Niobe Planitia change areas and from any change site reported in literature found through the status source or search, re-checked before claiming. The claim is a candidate surface change, never a confirmed eruption.

## Partial wins

- **p1:** A reproduction of the Sif Mons change of Sulcanese et al. (2024) with a stated automatic detector, giving a change area within 30% of about 30 km^2, with code and products saved.
- **p2:** A systematic search of at least 1,000,000 km^2 of area imaged in two cycles with the same look direction, listing every detection and the false-alarm rate measured on control windows.
- **p3:** A candidate meeting (2), (3) and (4) whose incidence angles differ by more than 10 deg, so that geometry is not fully excluded, with the incidence correction and its residual reported.

## How a win is checked

The skeptic downloads the cited F-BIDR or F-MIDR products from the PDS Geosciences Node, re-registers them with the saved tie points, applies the same despeckling and incidence correction, recomputes the change map and the control-window statistics, checks slopes from the Magellan altimetry products, and reads the literature listed by the status source. A few hours.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://api.semanticscholar.org/graph/v1/paper/DOI:10.1126/science.abm7735/citations?fields=title,year,venue,externalIds&limit=1000>

## Sources

- <https://pds-geosciences.wustl.edu/missions/magellan/index.htm>
- <https://doi.org/10.1126/science.abm7735>
- <https://meetingorganizer.copernicus.org/EPSC2024/EPSC2024-891.html>
- <https://doi.org/10.1038/s41550-024-02272-1>
- <https://doi.org/10.1016/j.icarus.2023.115773>
- <https://doi.org/10.1016/j.chemer.2025.126316>
- <https://doi.org/10.1038/s41550-026-02832-7>
- <https://doi.org/10.1038/s41550-026-02833-6>
- <https://doi.org/10.1029/2026JE009994>
- <https://www.ebi.ac.uk/europepmc/webservices/rest/MED/36921020/citations?format=json&pageSize=100>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Conventional: threshold-based change detection on despeckled, co-registered cycle 1 and cycle 3 pairs (as Sulcanese et al. did), applied systematically to every volcanic province imaged twice.
- Cross-domain import (Earth SAR volcano monitoring): log-ratio change detection with statistical thresholds used for Sentinel-1 lava-flow mapping, or the GB2KI ratio-image thresholding of Gao et al. (2026).

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Incidence-angle differences between cycles change radar brightness and can reveal or hide flows; a change that geometry could explain is not a win.
- The Europe PMC citation list of Herrick and Hensley held only 10 works on 2026-11-13 against 90 in Semantic Scholar; use the fuller list and also search planetary journals and conference abstracts before claiming.
- Speckle noise is strong at full resolution; single-pixel or small changes are noise unless they pass the control-window test in (2).
- The Bhiravarasu et al. (2026) critique shows that even published detections are contested; report every geometric and processing check, not only the change map.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/uncharted/venus-magellan-cycle-surface-change-candidate.md
```

Already set up? Say `run V3R1T4S on venus-magellan-cycle-surface-change-candidate`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `venus-magellan-cycle-surface-change-candidate`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
