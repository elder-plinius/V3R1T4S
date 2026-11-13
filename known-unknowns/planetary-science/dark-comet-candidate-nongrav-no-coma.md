# New dark comet candidate: a near-Earth asteroid with a non-gravitational acceleration that radiation forces cannot explain and no coma in archival images

🪐 **Planets and moons** · standard · tractability ★★☆☆☆ · compute: laptop-hours (MPC astrometry is kilobytes to megabytes per object; an orbit fit with non-gravitational terms runs in minutes; archival image cutouts are megabytes) · open as of 2026-11-13

## The problem

Dark comets are near-Earth objects whose orbits show comet-like non-gravitational accelerations although no coma has ever been seen. The acceleration is written as A1 (radial), A2 (along-track) and A3 (normal) terms. Seven were reported in 2023 by Seligman, Farnocchia, Micheli and colleagues; Taylor, Farnocchia, Vokrouhlicky, Seligman, Steckloff and Micheli (2023, Icarus) explained most of them by seasonally varying outgassing, and Taylor and colleagues (2024, arXiv 2407.01839) proposed their dynamical origin. Seligman, Farnocchia, Micheli, Hainaut, Hsieh, Feinstein, Chesley, Taylor, Masiero and Meech (2024, PNAS 121; arXiv 2412.07603) added seven more, doubling the class to about 14 and splitting it into an outer and an inner population. On 2026-11-13 the JPL Small-Body Database listed 23 asteroids with a fitted A1, including tiny objects pushed by sunlight (such as the temporary minimoons 2006 RH120 and 2020 CD3), 1I/'Oumuamua and the new 2026 QQ8. The 9 arXiv abstracts mentioning dark comets, read on 2026-11-13, report no new dark comet after December 2024; later papers debate whether 2005 VL1 and 1998 KY26 are lost spacecraft. Open task: a new object that meets the dark-comet criteria. It complements nea-yarkovsky-detection-not-in-sbdb-neocc, which only accepts accelerations that Yarkovsky drift can explain. A win is a candidate.

## What counts as a win

A saved bundle (MPC get-obs astrometry with fetch date, weights, fit code, covariance, image list and cutouts) where: (1) the fit includes the Sun, planets, Moon and Pluto from DE440, the 16 SB441-N16 perturbers, general relativity, star-catalogue debiasing (Eggl et al. 2020) and Veres et al. 2017 weights, 3-sigma outlier rejection, and A1, A2 and A3 with an inverse-square law; (2) the non-gravitational fit lowers chi^2 by at least 25 relative to the gravity-only fit, and either A1 or A3 is non-zero at 4 sigma or more, or A2 is non-zero at 4 sigma or more and its size exceeds 10 times the largest Yarkovsky value for the object (diameter from H with any albedo from 0.05 to 0.5, density 1,000 kg/m^3, as in Farnocchia et al. 2013); (3) a significant A1 exceeds 3 times the solar radiation pressure acceleration of the smallest plausible body (albedo 0.5, density 1,000 kg/m^3, 1,361 W/m^2 at 1 au); (4) the result holds when the 10% most influential observations are removed and under a second weighting scheme; (5) on at least 2 nights of public archival images at the Horizons position the profile matches a trailed field-star profile, with the coma upper limit stated; (6) no spacecraft or rocket stage in the JPL Horizons spacecraft list matches the orbit; (7) the live SBDB solution for the object fits no A1 or A3 and no A2 that meets the bound in (2), and the object is in none of the published dark-comet lists or any paper found by search, re-checked just before claiming.

## Partial wins

- **p1:** The pipeline reproduces the published non-gravitational parameters of at least 5 of the known dark comets within 1 sigma, with fits saved.
- **p2:** An object meeting (1) to (4), (6) and (7) for which no public archival images cover a usable apparition, reported as a candidate awaiting a coma check.
- **p3:** An object meeting every criterion except that the significance in (2) lies between 3 and 4 sigma.

## How a win is checked

The skeptic refetches the MPC astrometry, refits with independent orbit software (for example OpenOrb or Find_Orb with the same force model), recomputes the significance and the radiation-pressure and Yarkovsky bounds, inspects the image cutouts and repeats the catalogue and literature checks. Under two hours.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://export.arxiv.org/api/query?search_query=abs:%22dark+comet%22+OR+abs:%22dark+comets%22&sortBy=submittedDate&sortOrder=descending&max_results=20>

## Sources

- <https://arxiv.org/abs/2412.07603>
- <https://arxiv.org/abs/2310.02733>
- <https://arxiv.org/abs/2407.01839>
- <https://ssd-api.jpl.nasa.gov/sbdb_query.api?fields=full_name,A1,A1_sigma,A2,A2_sigma,A3,data_arc,H&sb-kind=a&sb-cdata=%7B%22AND%22%3A%5B%22A1%7CDF%22%5D%7D>
- <https://docs.minorplanetcenter.net/mpc-ops-docs/apis/get-obs/>
- <https://ssd.jpl.nasa.gov/horizons/>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Rank near-Earth objects with long arcs and many apparitions by the drop in chi^2 when non-gravitational terms are added, then vet the top few.
- The inner population of Seligman et al. 2024 has small, near-circular orbits; search similar orbits first.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Metre-sized objects are pushed by sunlight; a radial A1 alone is expected for them and is not a dark-comet signature unless it beats the bound in (3).
- Old astrometry has catalogue biases that fake accelerations; debiasing and weighting are required, and the result must survive (4).
- Some objects in Earth-like orbits are lost spacecraft or rocket stages; check before claiming.
- An apparent acceleration can come from one bad night or from mislinked observations; inspect residuals per apparition.
- Some known dark comets (for example 2003 RM) carry only an A2 in the SBDB, so the A1 query above does not list them all; use the published lists for the novelty check.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/planetary-science/dark-comet-candidate-nongrav-no-coma.md
```

Already set up? Say `run V3R1T4S on dark-comet-candidate-nongrav-no-coma`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `dark-comet-candidate-nongrav-no-coma`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
