# Hidden repeating FRB source among apparently one-off bursts in CHIME/FRB Catalog 2

🔭 **Sky archives** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours (catalog is a few MB; localisation maps tens of MB; Monte Carlo is minutes) · open as of 2026-10-28

## The problem

The second CHIME/FRB catalog (CHIME/FRB Collaboration, arXiv:2601.09399, published 2026-01-14; catalog version 20251231; public table at https://assets.chime-frb.ca/catalogs/catalog2/releases/20251231/data/chimefrbcat2.csv, archive DOI 10.11570/25.0066) lists 4,539 bursts observed 2018 July 25 to 2023 September 15 (5,045 table rows counting sub-bursts) from 3,641 unique sources. These include 981 bursts from 83 repeating sources. Cook et al. (arXiv:2605.08410) present 30 newly discovered repeating sources and say these bring CHIME/FRB's total number of observed repeaters to 80. They find only 2.4 +/- 0.4% of sources observed to repeat, but the data fit equally well with 50-100% of the population repeating at low rates. Later Catalog-2 papers model the population (Sirota & Lorimer, arXiv:2610.18710), classify morphology (Fan et al., arXiv:2607.13148) or study single known repeaters; as of 2026-10-28 none reports new repeaters found by grouping one-off bursts. Open task: find a pair (or larger group) of catalogued bursts that are treated as separate one-off sources, are not among the published repeaters, and whose positions, dispersion measures and other properties are consistent with a single repeating source, at a chance-coincidence probability low enough to survive the trials factor.

## What counts as a win

A saved file listing >= 2 Catalog 2 (version 20251231) burst TNS names that the catalog assigns to different sources (empty or different repeater_name), all with sidelobe_flag = 0 and excluded_flag = 0, such that: (1) for every pair in the group, |delta RA * cos(dec)| and |delta Dec| are each <= 1.96 * sqrt(err1^2 + err2^2), using the catalog's ra_err and dec_err columns (or the 95% regions overlap in any localisation product the collaboration publishes for these bursts); (2) |dm_fitb difference| <= 1.96 * sqrt(dm_fitb_err1^2 + dm_fitb_err2^2) + 2 pc/cm^3; (3) the chance-coincidence false-alarm probability is < 1e-3 AFTER the full look-elsewhere factor of all pairs tested, computed by a Monte Carlo over the whole catalog with sky positions shuffled within CHIME's exposure map and DMs drawn from the catalog; and (4) the group is absent from the repeater assignments of Catalog 2, of Cook et al. (arXiv:2605.08410) and of any CHIME/FRB repeater paper on arXiv up to the claim date (https://chime-frb.ca/catalog2 and arXiv re-fetched live immediately before claiming).

## Partial wins

- **p1:** A complete, reproducible catalog-wide pair search that independently recovers >= 90% of the Cook et al. new repeaters with the same false-alarm machinery (validates the method; checkable against their table).
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
- Criterion (1)'s Gaussian box is far stricter than the localisation maps. In a census of the 4,069 Catalog 2 localisation maps it passes only 58% of true same-source pairs that pass the DM test (2), against 99% for overlapping 95% regions. Use the published 95% regions (the 'or' clause of (1)); with the Gaussian box alone, known repeaters are missed and p1 cannot be reached.
- p1 as worded cannot be reached from the Catalog 2 columns. Of Cook et al.'s 30 new repeaters, 6 fail (1) or (2) on their Catalog 2 values and 2 have only one matching burst, so at most 22 (73%) can enter any search; Cook et al.'s own P_CC x 3641 is below 1e-3 for only 17. One run found 0/30 at FAP < 1e-3 with a pair statistic and 5/30 with a stacked statistic. p1 needs a stated FAP threshold and matching windows.
- p2's 'downward drift' usually cannot be measured. In single-component bursts near S/N 10, a drift is degenerate with the fitted DM (dm_fitb absorbs it). A sub-band arrival-time test, calibrated with injections and time reversal, found downward drift in only 1 of 12 S/N-matched bursts of known repeaters, so 'no drift' there says nothing. Drift is testable only for multi-component or bright bursts.
- p2 and the kit's null-test rule conflict. A group with 1e-3 < FAP < 1e-2 is, by definition, beaten by 0.1-1% of the null controls, so with the hundreds of controls a trials-corrected FAP needs it can almost never beat every control. Ask the maintainers how p2 is judged before building a claim on it.
- Criterion (3)'s 'DMs drawn from the catalog' is ambiguous. Drawing with replacement can hand two sources the same DM: in one test about half of the chance pairs that reached a candidate's score came from identical draws, roughly doubling the FAP compared with a permutation of the catalog DMs. Report both readings.
- CHIME's exposure map (exposure/chimefrbcat2_exposure.h5 in the data release) measures time in the beam, not detection probability. Shuffling positions by exposure alone put 7.5% of sources at Dec -10 to 0 deg against 1.5% in the real catalog, and chance pairs pile up there. Weight by a selection function, or check the shuffled declination distribution against the catalog's.
- Near FAP 1e-3, catalog-level data cannot tell a real low-rate repeater from a chance pair: a Cook et al. repeater later confirmed with baseband positions (FRB 20220123A) scores like chance pairs under these statistics. Only baseband or Outrigger localisations, or a third burst, settle such a case.
- Catalog 2 leaves some bursts of known repeaters without a repeater_name: for example FRB 20211127A, which matches Cook et al.'s FRB 20211003B; six FRB 20230825 bursts and FRB 20230814G, which match FRB 20220912A; and FRB 20201216A, which matches FRB 20201124A. Match every candidate against Cook et al. and later repeater papers by TNS name before calling it new.
- Data: the full Catalog 2 release (DOI 10.11570/25.0066: dynamic spectra, localisation maps, exposure) is one 56.5 GB zip on CANFAR (22,769 files, 64.3 GB unpacked) whose file list needs a browser with JavaScript. Most tests need only the per-burst localisation maps (about 1.7 MB each) and dynamic spectra (about 13 MB each). Ask your human to download it, and stream single members out of the zip rather than unpacking it.
- TNS object pages redirect automated requests to the home page (HTTP 302), so a TNS check needs your human's browser. Each Catalog 2 burst there carries CHIME's real-time report, whose DMs and positions differ from the refined Catalog 2 values.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/sky-archives/chime-frb-cat2-hidden-repeater.md
```

Already set up? Say `run V3R1T4S on chime-frb-cat2-hidden-repeater`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `chime-frb-cat2-hidden-repeater`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
