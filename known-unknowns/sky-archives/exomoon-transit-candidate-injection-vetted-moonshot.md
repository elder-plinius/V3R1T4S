# MOONSHOT - An exomoon transit candidate in public Kepler or TESS light curves whose injection-retrieval false-positive rate is below 0.1%

🔭 **Sky archives** · moonshot (famous, long odds) · tractability ★☆☆☆☆ · compute: laptop-days (nested sampling of a photodynamical planet-plus-moon model, repeated for at least 1,000 injections per star; light curves are megabytes per star at MAST) · open as of 2026-11-13

## The problem

An exomoon is a moon of a planet outside the Solar System. None is confirmed. The two Kepler candidates are Kepler-1625 b-i (Teachey and Kipping 2018) and Kepler-1708 b-i (Kipping, Bryson, Burke, Christiansen, Hardegree-Ullman, Quarles, Hansen, Szulágyi and Teachey 2022, Nature Astronomy: a survey of 70 cool giants; a 4.8-sigma effect with a 1% false-positive probability by injection-recovery). Heller and Hippke (2024, Nature Astronomy; arXiv 2312.03786), using their open Pandora code, found false-positive rates of 10.9% and 1.6% for these two and argue that large moons around them are unlikely. Kipping, Cassese, Changeat, Yahalomi, Teachey and Edwards (accepted to AJ; arXiv 2511.15317, revised 2026-05-29) found that 7 of 12 analysis choices for a JWST transit of Kepler-167e favour a moon, but the signal is degenerate with a starspot crossing; they urge observing the next transit in October 2027. Pérez-Rodrigo and Rebollido (2026, accepted to A&A; arXiv 2609.07320) compiled 24 proposed candidates and found that 8 of 13 meet at least one stability criterion. The 25 newest arXiv abstracts mentioning exomoons, read on 2026-11-13, contain no new transit candidate (the only other claims, around CD-35 2722 B and HD 206893 B, use radial velocities or astrometry). Open task: an exomoon transit candidate in public data that clears a stated statistical bar far above the existing ones. A win is a candidate, never a discovery.

## What counts as a win

A saved bundle for a transiting planet with at least 3 transits in public Kepler or TESS light curves: (1) an analysis plan (detrending methods, priors, model, sampler settings) frozen and SHA-256 hashed before the first moon fit; (2) a planet-plus-moon photodynamical model (Pandora or an equivalent open code) beats the planet-only model with natural-log Bayes factor ln K of at least 5 in each of at least 3 independent detrendings (for example biweight, cosine filtering and a Gaussian process); (3) at least 1,000 planet-only transits with the best-fit planet parameters, injected into the same star's own out-of-transit data and analysed with the identical frozen pipeline, give ln K at least as large as the candidate's in fewer than 0.1% of cases (with exactly 1,000 injections, in none); (4) leave-one-transit-out fits keep ln K of at least 3 in every case; (5) the moon orbits between the Roche limit and 0.5 Hill radii; (6) the planet passes standard vetting (DR25 or TOI disposition of planet candidate or confirmed, no centroid shift in transit) and its timing variations are not better explained by another known planet. Kepler-1625 b and Kepler-1708 b may be used, but the claim must then also show the published false-positive rates of Heller and Hippke 2024 reproduced with the same pipeline before the new bar is applied.

## Partial wins

- **p1:** An independent pipeline that reproduces the Heller and Hippke 2024 false-positive rate for Kepler-1708 b (1.6%) within a factor 2 from at least 300 injections, with code and injections saved.
- **p2:** A candidate meeting (1), (2), (4), (5) and (6) whose false-positive rate in test (3) lies between 0.1% and 1%, at or below the Kepler-1708 b-i level.
- **p3:** A frozen, injection-calibrated table for at least 20 Kepler or TESS giant planets with at least 3 transits giving, for each, the moon radius excluded at 95% confidence across 0.1 to 0.5 Hill radii, with the injection results saved.

## How a win is checked

The skeptic checks the plan hash against the commit date, reruns the moon and planet-only fits with new seeds, draws a fresh set of at least 1,000 injections from the out-of-transit data with their own random positions, and recomputes the false-positive fraction and the leave-one-out tests. Days of laptop time.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://export.arxiv.org/api/query?search_query=abs:exomoon&sortBy=submittedDate&sortOrder=descending&max_results=25>

## Sources

- <https://arxiv.org/abs/2201.04643>
- <https://arxiv.org/abs/2312.03786>
- <https://arxiv.org/abs/2511.15317>
- <https://arxiv.org/abs/2609.07320>
- <https://github.com/hippke/Pandora>
- <https://archive.stsci.edu/tess/bulk_downloads/bulk_downloads_ffi-tp-lc-dv.html>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Long-period giants with many Kepler transits, where the Hill sphere is large and the moon signal adds up over transits.
- Pre-register the target list and the bar for every star, then report all results, so that one striking fit is not cherry-picked from many.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Starspot crossings and detrending residuals mimic moon dips; this is why the Kepler-167e JWST result stays ambiguous.
- Kepler long-cadence (30-minute) integration smears ingress and egress; models must be supersampled.
- Unseen planets cause timing variations that a moon model can absorb; check against the archive system architecture and TTV catalogues.
- Bayes factors from different samplers and priors are not comparable; the bar applies only with the frozen pipeline used for the injections.
- With 1,000 injections a zero count still allows a true rate of about 0.3% at 95% confidence; more injections make the claim stronger.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/sky-archives/exomoon-transit-candidate-injection-vetted-moonshot.md
```

Already set up? Say `run V3R1T4S on exomoon-transit-candidate-injection-vetted-moonshot`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `exomoon-transit-candidate-injection-vetted-moonshot`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
