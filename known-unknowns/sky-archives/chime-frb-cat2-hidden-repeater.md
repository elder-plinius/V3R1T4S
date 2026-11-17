# Hidden repeating FRB source among apparently one-off bursts in CHIME/FRB Catalog 2

🔭 **Sky archives** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours (catalog is a few MB; localisation maps tens of MB; Monte Carlo is minutes) · open as of 2026-10-28

## The problem

The second CHIME/FRB catalog (CHIME/FRB Collaboration, arXiv:2601.09399, published 2026-01-14; catalog version 20251231; public table at https://assets.chime-frb.ca/catalogs/catalog2/releases/20251231/data/chimefrbcat2.csv, archive DOI 10.11570/25.0066) lists 4,539 bursts observed 2018 July 25 to 2023 September 15 (5,045 table rows counting sub-bursts) from 3,641 unique sources. These include 981 bursts from 83 repeating sources. Cook et al. (arXiv:2605.08410) present 30 newly discovered repeating sources and say these bring CHIME/FRB's total number of observed repeaters to 80. They find only 2.4 +/- 0.4% of sources observed to repeat, but the data fit equally well with 50-100% of the population repeating at low rates. Later Catalog-2 papers model the population (Sirota & Lorimer, arXiv:2610.18710), classify morphology (Fan et al., arXiv:2607.13148) or study single known repeaters; as of 2026-10-28 none reports new repeaters found by grouping one-off bursts. Open task: find a pair (or larger group) of catalogued bursts that are treated as separate one-off sources, are not among the published repeaters, and whose positions, dispersion measures and other properties are consistent with a single repeating source, at a chance-coincidence probability low enough to survive the trials factor.

## What counts as a win

A saved file listing >= 2 Catalog 2 (version 20251231) burst TNS names that the catalog assigns to different sources (empty or different repeater_name), all with sidelobe_flag = 0 and excluded_flag = 0, such that: (1) for every pair in the group, |delta RA * cos(dec)| and |delta Dec| are each <= 1.96 * sqrt(err1^2 + err2^2), using the catalog's ra_err and dec_err columns (or the 95% regions overlap in any localisation product the collaboration publishes for these bursts); (2) |dm_fitb difference| <= 1.96 * sqrt(dm_fitb_err1^2 + dm_fitb_err2^2) + 2 pc/cm^3; (3) the chance-coincidence false-alarm probability is < 1e-3 AFTER the full look-elsewhere factor of all pairs tested, computed by a Monte Carlo over the whole catalog with sky positions shuffled within CHIME's exposure map and DMs drawn from the catalog; and (4) the group is absent from the repeater assignments of Catalog 2, of Cook et al. (arXiv:2605.08410) and of any CHIME/FRB repeater paper on arXiv up to the claim date (https://chime-frb.ca/catalog2 and arXiv re-fetched live immediately before claiming).

## Partial wins

- **p1:** A complete, reproducible catalogue-wide pair search that recovers >= 85% of the Cook et al. new repeaters THAT CONDITIONS (1) AND (2) OF THIS CRITERION ADMIT AT ALL, at a stated catalogue-wide false-alarm rate of at most one expected false source pair, with the same false-alarm machinery used for the main criterion and its calibration shown (validates the method; checkable against their table). The admissible set, and the reason each excluded source is excluded, must be reported with the recall. Measured from Catalog 2 version 20251231: 25 of the 30 new repeaters have two or more bursts in the criterion's clean set, and 20 of 30 (Gaussian reading of (1)) or 21 of 30 (the criterion's 95%-region option) have an internal pair that passes (1) and (2), so a 90% bar on all 30 cannot be met by any pair search, statistic or threshold. Five sources lack a second unflagged burst (FRB 20180907D, 20191026A, 20210330B, 20220207A, 20220211A); one fails (1) (FRB 20190208C, best |dRA cos dec| 0.798 deg against a 0.141 deg limit, 95% regions disjoint); three fail (2) on dispersion measure (FRB 20190716C, 20211030A, 20211120C: smallest |dDM| 4.43, 5.07 and 2.15 against limits of 2.11, 2.00 and 2.04 pc/cm^3), which is the drift this criterion's per-burst errors do not allow for. A search that instead uses the baseband or outrigger localisations the discovery paper used is outside what Catalog 2's released columns support.
- **p2:** A candidate group meeting every criterion except the false-alarm threshold (1e-3 < FAP < 1e-2 after trials), with morphology (narrowband, downward drift) supporting repetition.
- **p3:** A Catalog-1 one-off whose position and DM match a Catalog-2 burst from a different source ID, giving a multi-year repetition baseline, with FAP < 1e-2 after trials.

## How a win is checked

Skeptic downloads the Catalog 2 CSV/FITS from https://chime-frb.ca/catalog2 (minutes), reruns the supplied pair-FAP script with a new random seed and an independently written trials count, recomputes the position and DM agreement from the catalog columns, checks the sidelobe and excluded flags, and greps the published repeater tables. Under an hour.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://chime-frb.ca/catalog2>

## Sources

- <https://chime-frb.ca/catalog2>
- <https://assets.chime-frb.ca/catalogs/catalog2/releases/20251231/data/chimefrbcat2.csv>
- <https://www.canfar.net/storage/list/AstroDataCitationDOI/CISTI.CANFAR/25.0066/data>
- <https://arxiv.org/abs/2601.09399>
- <https://arxiv.org/abs/2605.08410>
- <https://chime-frb-open-data.github.io/>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Conventional: pairwise overlap of localisation contours with a DM window, then a catalog-wide shuffled-sky Monte Carlo for the false-alarm rate (the method used for CHIME repeater discovery).
- Use morphology as a prior: Sun et al. and the semi-supervised Catalog 2 classification find repeater-like narrowband bursts cluster separately; rank one-offs by repeater-likeness and search those first to cut the trials factor honestly (pre-registered ranking).
- Cross-domain import (record linkage / genealogy): treat bursts as noisy records and use Fellegi-Sunter probabilistic linkage with match weights from position, DM, scattering and spectral index.
- Cross-domain import (gamma-ray astronomy): borrow the 'stacking' likelihood used to find weak neutrino or GRB counterpart clusters - an unbinned likelihood over all bursts near a trial position, instead of pair counting.
- Cross-domain import (seismology): repeating-earthquake detection uses waveform similarity; use dynamic-spectrum template similarity between bursts at the same position as extra evidence.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- CHIME has huge, elongated sidelobe-shaped localisation regions near the zenith band; overlapping contours are common by chance - the trials factor over all pairs dominates.
- Low-DM Galactic-plane bursts and RRAT-like Galactic sources contaminate; check DM against the NE2001/YMW16 Galactic maximum.
- Some 'new' groupings are already merged in Cook et al. or later CHIME repeater papers under a different source name; compare TNS names, not internal IDs.
- Sidelobe detections are assigned wrong positions; the catalog flags them - exclude flagged events.
- Do not post to TNS or contact CHIME; the claim is a vetted candidate only.
- Partial win p1 is measured against a subset the criterion itself defines: compute the admissible set first (sources with two or more bursts passing conditions (1) and (2)) and report recall against it, with the excluded sources named. A recall quoted against all 30 Cook sources cannot exceed 70% and says more about the criterion than about the method.
- Repeater dispersion measures drift by about 0.1 to 12 pc/cm^3 per year, so a DM agreement test built from per-burst measurement errors (about 2 pc/cm^3 here) rejects genuine repeats years apart. The discovery paper used a 13 pc/cm^3 window for that reason.
- CHIME header localisation errors have heavy tails: in an injection test, a second burst planted at a real same-source offset passed the 1.96-sigma box only 51.6% of the time against the 90% a Gaussian reading predicts. Any false-alarm machinery calibrated on Gaussian errors will mis-state both recall and significance.
- Count candidate sources, not pairs. An apparent catalogue-wide excess of coincident one-off pairs (24 observed against 3.8 to 6.0 expected) collapsed to 9 against 3.8 to 5.3, and to non-significance, once 16 of the 24 pairs were seen to belong to one connected component sitting on a known repeater.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/sky-archives/chime-frb-cat2-hidden-repeater.md
```

Already set up? Say `run V3R1T4S on chime-frb-cat2-hidden-repeater`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `chime-frb-cat2-hidden-repeater`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
