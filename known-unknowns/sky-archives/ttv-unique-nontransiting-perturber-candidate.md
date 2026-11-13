# Non-transiting planet candidate uniquely determined from the transit-timing variations of a Kepler or TESS planet, absent from the archive

🔭 **Sky archives** · standard · tractability ★★☆☆☆ · compute: laptop-days (transit times are kilobytes; a global N-body search over perturber period, mass and eccentricity is many millions of fast TTV model calls; Kepler and TESS light curves are megabytes per star at MAST) · open as of 2026-11-13

## The problem

Transit-timing variations (TTVs) are shifts in the times at which a planet crosses its star, caused by the pull of another planet. When the perturber does not transit, the TTVs are the only evidence for it. On 2026-11-13 the NASA Exoplanet Archive listed 29 planets discovered this way, the newest TOI-5624 f and TOI-1232 c (2026). Lammers and Winn (2026, accepted to AJ; arXiv 2604.16297) re-examined all 12 published cases where a non-transiting perturber was said to be uniquely characterised: only KOI-142 and Kepler-419 have compelling unique solutions; KOI-872 and KOI-884 have a best solution among complex degeneracies; Kepler-82, Kepler-411, Kepler-725, KOI-134, Kepler-138 and TOI-4562 admit very different solutions; and the evidence at WASP-18 and WASP-126 is weak. Short-timescale TTV structure tied to conjunctions (chopping, or close approaches on eccentric orbits) is necessary but not sufficient for a unique answer. Unexplained TTVs are catalogued by Holczer et al. 2016 (Kepler: 274 of 2,599 KOIs significant), Naponiello 2026 (A&A 705, A5: 423 single-planet TESS systems, 11 significant of which 5 known, 10 marginal) and Nabbie, Huang, Wittenmyer and Zhou 2026 (arXiv 2606.17218, accepted to ApJS: 175 multi-planet TESS systems, 20 significant, 13 new). Preprints keep proposing perturbers the archive does not yet list, for example TOI-3850 c (arXiv 2608.11328), a third planet of Kepler-50 (arXiv 2608.25035) and a possible companion of TOI-2109 b (arXiv 2611.13505, 2026-11-10); those systems are taken. Open task: a non-transiting perturber whose period and mass the public transit times pin down uniquely, in a system where no such planet is listed or published.

## What counts as a win

A saved bundle (transit times with errors, from public Kepler or TESS light curves with saved code or from a cited public table, N-body TTV code, global-search output, posterior chains) where: (1) the transiting planet has at least 15 transit times and a linear ephemeris loses to the best perturber model by delta BIC > 20; (2) a full N-body model beats a pure sinusoid at the super-period by delta chi^2 > 25, showing the short-timescale structure that Lammers and Winn require; (3) a global search over perturber period ratio 0.2 to 5 (at least 10 starts near every first- and second-order resonance and their synodic aliases), mass 0.1 Earth to 13 Jupiter masses and eccentricity 0 to 0.5 finds that every solution within delta chi^2 = 25 of the best lies within 5% of its period and a factor 2 of its mass; (4) the best system is stable in a 10^6-orbit integration; (5) a search of the light curve at the perturber's predicted transit windows finds no transit with signal-to-noise above 7 at its expected depth for coplanar orbits, or the solution's inclination excludes transits; (6) the TTVs are not explained by starspot crossings (no anti-correlation with transit depth or duration), a stellar companion's light-travel time, or a blend; (7) the archive pscomppars and ps tables, the TOI and CTOI tables and an ADS/arXiv search show no planet or proposed perturber within 5% of that period in the system, all re-fetched immediately before claiming. A win is a candidate.

## Partial wins

- **p1:** Pipeline validation: the global search reproduces the published KOI-142 c period and mass within 1 sigma and passes test (3) for KOI-142, and fails test (3) for at least two of Kepler-82, Kepler-411, Kepler-725, KOI-134, Kepler-138 and TOI-4562, matching Lammers and Winn.
- **p2:** For one of the six multi-solution systems above, adding public TESS transit times that Lammers and Winn did not use makes test (3) pass, with the surviving solution reported.
- **p3:** For a significant but unexplained TTV system in Naponiello 2026 or Nabbie et al. 2026, a list of at most 3 distinct solution families meeting (1), (2) and (4), each with frozen predicted times for the next 5 transits whose predictions differ by at least 10 minutes, so that a future public TESS sector can decide between them.

## How a win is checked

The skeptic re-measures a random third of the transit times from the MAST light curves, reruns the global search with fresh starting points and seeds, checks that no distant solution lies within delta chi^2 = 25, repeats the stability integration and re-queries the archive and literature. A day of laptop time.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+pl_name,disc_year,disc_facility,sy_dist+from+pscomppars+where+discoverymethod='Transit+Timing+Variations'+order+by+disc_year&format=csv>

## Sources

- <https://arxiv.org/abs/2604.16297>
- <https://arxiv.org/abs/1606.01744>
- <https://arxiv.org/abs/2511.16504>
- <https://arxiv.org/abs/2606.17218>
- <https://arxiv.org/abs/2611.13505>
- <https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+pl_name,disc_year,disc_facility,sy_dist+from+pscomppars+where+discoverymethod='Transit+Timing+Variations'+order+by+disc_year&format=csv>
- <https://archive.stsci.edu/tess/bulk_downloads/bulk_downloads_ffi-tp-lc-dv.html>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Systems with a long Kepler baseline plus later TESS transits: the 10-year gap breaks super-period aliases.
- Eccentric perturbers produce phase-dependent kicks at close approach, the second route to uniqueness Lammers and Winn name.
- Cross-domain import (satellite orbit determination): treat the global search as a multimodal inverse problem and map every local minimum, rather than reporting the first good fit.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- A single sinusoidal TTV fits many perturber periods and masses; without chopping a unique solution is very unlikely.
- Kepler long-cadence transit times of shallow planets have non-Gaussian errors; outliers can fake structure, so use robust likelihoods and report the effect of removing them.
- Spot crossings on active stars shift measured mid-times; the Holczer et al. catalogue flags anti-correlated depth and timing changes.
- Archive discovery-method flags lag the literature; the novelty check must include a paper search, which on 2026-11-13 already turned up three 2026 perturber proposals not yet in the archive.
- The same analysis may also give a first mass for the transiting planet, which is the separate target archive-mr-mass-planet-first-dynamical-mass; claim each result under its own entry.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/sky-archives/ttv-unique-nontransiting-perturber-candidate.md
```

Already set up? Say `run V3R1T4S on ttv-unique-nontransiting-perturber-candidate`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `ttv-unique-nontransiting-perturber-candidate`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
