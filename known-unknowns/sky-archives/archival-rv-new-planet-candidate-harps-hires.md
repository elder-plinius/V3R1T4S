# New planet candidate from a periodic signal in public HARPS or Keck/HIRES radial velocities, absent from the exoplanet catalogues

🔭 **Sky archives** · harvest (many cells or partial wins within reach) · tractability ★★☆☆☆ · compute: laptop-hours (per-star radial-velocity files are kilobytes; the HARPS-RVBank second release holds 252,615 velocities of 5,239 stars, and the Butler et al. 2017 HIRES release 60,949 velocities of 1,624 stars) · open as of 2026-11-13

## The problem

A radial velocity (RV) is the speed of a star along our line of sight, measured from shifts in its spectrum; an orbiting planet makes it swing periodically. Two large public RV sets exist. The HARPS-RVBank (Trifonov, Tal-Or, Zechmeister, Kaminski, Zucker and Mazeh 2020, A&A 636, A74; second release by Perdelwitz, Trifonov, Teklu, Sreenivas and Tal-Or 2024, A&A 683, A125) gives 252,615 corrected HARPS velocities of 5,239 stars from all public spectra taken before January 2022, with activity indices (195,387 spectra have an R'HK value). The Keck HIRES release of Butler et al. 2017 (AJ 153, 208) gives 60,949 velocities of 1,624 stars and lists 357 significant signals: 225 published planets, 60 unpublished candidates, 54 signals needing more data and 18 likely due to activity. Archive searches keep finding planets: Sreenivas et al. 2022 (A&A 660, A124: HD 103891 b and HD 105779 b), Mignon et al. 2024 (A&A 689, A32: 200 HARPS M dwarfs, 97% of known planets recovered, 3 new candidates around GJ 300, GJ 654 and GJ 739) and Schorr, Binnenfeld and Zucker 2025 (A&A 694, A210: GJ 2126 b from 112 RVBank velocities). On 2026-11-13 the NASA Exoplanet Archive composite table listed 6,470 planets, 1,205 of them found by RV (62 in 2025 and 46 so far in 2026). Open task: a periodic RV signal of planetary minimum mass, in these public data, that no catalogue or paper reports. A win is a candidate, never a planet.

## What counts as a win

A saved bundle (star names, every RV file as downloaded with its SHA-256 and date, fit code, posterior chains, activity periodograms) where: (1) after removing any known planets, a generalised Lomb-Scargle periodogram peak has analytic false-alarm probability below 0.1%, and a Keplerian model beats the no-planet model by delta BIC > 10, with free jitter and separate offsets per instrument (HARPS before and after the 2015 fibre upgrade are separate instruments); (2) the semi-amplitude K exceeds 5 times its posterior 1-sigma error, the data cover at least 2 periods and at least 20 nights; (3) no peak with false-alarm probability below 1% lies within 5% of the period, or of its 1-day and 1-year aliases, in the periodograms of R'HK, H-alpha, chromatic index, line width or bisector from the same spectra, and the period is not within 10% of the published or TESS-derived stellar rotation period or its first two harmonics; (4) the chosen period beats its 1-day, sidereal-day and 1-year aliases by delta BIC > 5, and fits to each half of the data give K values that agree within 2 sigma; (5) the minimum mass is below 13 Jupiter masses; (6) no planet of this star with a period within 10% appears in the archive pscomppars or ps tables, the Butler et al. 2017 tables, Mignon et al. 2024, or any paper found by an ADS/arXiv search on the star's names, all re-fetched immediately before claiming.

## Partial wins

- **p1:** A blind pipeline that, run on all HARPS-RVBank stars with at least 50 velocities, recovers at least 90% of the archive's RV planets on those stars (period within 1%), with every other detection meeting (1) and (2) listed.
- **p2:** Independent confirmation of one of the 60 unpublished Butler et al. 2017 HIRES candidates: the HARPS-RVBank data alone give a signal meeting (1) to (4) whose period and K agree with the HIRES values within 2 sigma, not reported in any paper.
- **p3:** A signal meeting (1) to (4) and (6) whose minimum mass lies between 13 and 80 Jupiter masses: a new brown-dwarf companion candidate.

## How a win is checked

The skeptic downloads the same velocities, refits them with independent software (for example RadVel or the Exo-Striker), recomputes the periodograms of the velocities and of every activity index, checks the alias and half-split tests, and re-queries the archive and the literature. Under an hour per star.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+discoverymethod,count(*)+from+pscomppars+group+by+discoverymethod&format=csv>

## Sources

- <https://arxiv.org/abs/2311.12438>
- <https://arxiv.org/abs/2001.05942>
- <https://arxiv.org/abs/1702.03571>
- <https://arxiv.org/abs/2502.06513>
- <https://arxiv.org/abs/2502.11139>
- <https://arxiv.org/abs/2112.09029>
- <https://github.com/3fon3fonov/exostriker>
- <https://archive.eso.org/>
- <https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+discoverymethod,count(*)+from+pscomppars+group+by+discoverymethod&format=csv>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Conventional: an automated search of every star with enough nights, ranked by false-alarm probability, then the activity and alias tests on the top signals.
- Joint fits for stars observed by both HARPS and HIRES, where two instruments with independent systematics share one signal.
- Gaussian-process activity models trained on the activity indices, so that a signal surviving them is less likely to be rotation.
- Cross-domain import (seismology): multitaper spectra and coherence between the velocity series and each activity index separate a planet from a correlated stellar signal.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- The 2015 HARPS fibre upgrade shifted velocities by several metres per second depending on spectral type; one offset across it fakes a long-period signal.
- Nightly zero-point errors in both HARPS and HIRES were corrected after release (Trifonov et al. 2020; Tal-Or et al. 2019 for HIRES); use the corrected velocities.
- Yearly and daily sampling create aliases; a 1-year signal is often an alias of a real shorter one, or a systematic.
- Magnetic cycles produce long-period RV trends that mimic giant planets; check R'HK over the same span.
- Gaia DR4 (due 2026-12-02) will publish astrometric and epoch-RV companion solutions; after that date the absence check must include its non-single-star and exoplanet tables.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/sky-archives/archival-rv-new-planet-candidate-harps-hires.md
```

Already set up? Say `run V3R1T4S on archival-rv-new-planet-candidate-harps-hires`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `archival-rv-new-planet-candidate-harps-hires`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
