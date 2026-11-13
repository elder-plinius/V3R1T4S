# Unrecognised co-orbital (Trojan, quasi-satellite or horseshoe) of Venus, Earth or Mars among catalogued asteroids, shown by clone integration

🔭 **Sky archives** · harvest (many cells or partial wins within reach) · tractability ★★★★☆ · compute: laptop-hours (orbits and covariances are kilobytes from the JPL SBDB API; 100 clones integrated for thousands of years take minutes, Mars Trojan integrations of 1 million years take hours) · open as of 2026-11-13

## The problem

A co-orbital shares a planet's mean orbital period (a 1:1 resonance). It may librate around the planet's L4 or L5 points (a Trojan), around the planet itself (a quasi-satellite) or around both (a horseshoe). Pan and Gallardo (2025, Celest Mech Dyn Astron 137, 2; arXiv 2410.20015) built a dynamical catalogue of 167 Solar System co-orbitals (all planets except Jupiter) and added 2021 FV1 as a Mars quasi-satellite. Venus has 21 known co-orbitals, the newest 2025 TV10, and none in a horseshoe configuration (Carruba, Sfair and Winter 2026, accepted as an A&A letter; arXiv 2601.21554). Earth has two known Trojans, both temporary (2010 TK7 and 2020 XL5; a 2026 survey of L4 by Lu and colleagues, arXiv 2606.31751, found no more), and eight quasi-satellites in the Wikipedia list read on 2026-11-13 (Cardea, 2006 FV35, 2013 LX28, 2014 OL339, Kamo'oalewa, 2022 YG, 2023 FW13 and 2025 PN7, found by Pan-STARRS on 2025-08-02). Mars has 17 Trojans with proper elements, 16 at L5 and 1 at L4 (Christou, Georgakarakos, Ćuk, Dell'Oro, Marshall-Lee and Humpage 2025, A&A 698, A42), and 2023 FW14 was reported as a second L4 Trojan by C. and R. de la Fuente Marcos (arXiv 2403.04061). On 2026-11-13 the JPL Small-Body Database held 252 objects with 0.99 < a < 1.01 au, 49 with 0.716 < a < 0.730 au and 48 with 1.517 < a < 1.530 au and e < 0.2 (35 of them with condition code 0 to 5), and the Rubin Observatory survey adds near-Earth objects every week. Many have never been integrated. Open task: show that a catalogued object is now co-orbital with Venus, Earth or Mars when no paper says so. This differs from uranus-neptune-coorbital-unrecognised, which covers only the giant planets.

## What counts as a win

A saved bundle (the SBDB orbit and covariance as fetched with date, at least 100 clones drawn from the covariance plus the nominal orbit, integration code and output) where: (1) the orbit has SBDB condition code at most 5; (2) the clones are integrated with the Sun, the eight planets with the Moon treated separately, and Pluto, initialised from JPL Horizons at the solution epoch, with IAS15 or an equivalent integrator (relative energy error below 1e-10) and any SBDB non-gravitational parameters included, at least 2,000 years backwards and forwards for Venus or Earth, or 1 million years for a Mars Trojan; (3) at least 90% of clones show the resonant angle (the object's mean longitude minus the planet's) librating, not circulating, over a continuous interval that contains the present and lasts at least 200 years (Venus or Earth) or 1 million years (Mars Trojan); the configuration (Trojan L4 or L5, quasi-satellite, horseshoe, or a compound state) is named, with libration centre and amplitude; (4) no paper or preprint found by an ADS/arXiv full-text search on the designation together with co-orbital, Trojan, quasi-satellite or horseshoe reports this state, and the object is not in Pan and Gallardo 2025, Carruba et al. 2026, Christou et al. 2025 or the Earth lists above, all re-checked immediately before claiming. The claim is a dynamical classification of a known object.

## Partial wins

- **p1:** The pipeline reproduces the published state of at least 15 known co-orbitals (all eight Earth quasi-satellites, both Earth Trojans, the Venus quasi-satellite Zoozve and at least four Mars Trojans) and finds circulation for 20 randomly chosen near-Earth objects outside 1:1 resonance, with all outputs saved.
- **p2:** An object with condition code 6 or 7 for which at least 70% of clones meet (3), reported as needing more astrometry, with the date range in which new observations would best reduce the uncertainty.
- **p3:** A Venus co-orbital in a horseshoe configuration meeting (1) to (4): the first of its kind according to Carruba et al. 2026.

## How a win is checked

The skeptic refetches the SBDB solution, draws new clones from its covariance, reruns the integration with a different integrator setting, plots the resonant angle and repeats the literature search. Under an hour per object.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://ssd-api.jpl.nasa.gov/sbdb_query.api?fields=full_name,a,e,i,condition_code,data_arc&sb-cdata=%7B%22AND%22%3A%5B%22a%7CRG%7C0.99%7C1.01%22%5D%7D>

## Sources

- <https://ssd-api.jpl.nasa.gov/sbdb_query.api?fields=full_name,a,e,i,condition_code,data_arc&sb-cdata=%7B%22AND%22%3A%5B%22a%7CRG%7C0.99%7C1.01%22%5D%7D>
- <https://arxiv.org/abs/2410.20015>
- <https://arxiv.org/abs/2601.21554>
- <https://arxiv.org/abs/2502.16231>
- <https://arxiv.org/abs/2403.04061>
- <https://arxiv.org/abs/2606.31751>
- <https://en.wikipedia.org/wiki/Quasi-satellite>
- <https://ssd.jpl.nasa.gov/horizons/>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Screen first with the nominal orbit only: compute the resonant angle over 500 years for every object with a near the planet's, then run clones on the few that librate.
- Newly designated Rubin-era objects are the least studied; sort by designation year.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Earth co-orbitals are short-lived and switch between quasi-satellite, horseshoe and Trojan states; describe the state at the present epoch and its duration, not a permanent class.
- Short arcs give wide covariances; a nominal orbit that librates while half the clones circulate is not a win.
- Close encounters with the Earth-Moon system are chaotic; a single Earth-Moon barycentre body misrepresents them.
- Osculating semimajor axes of eccentric co-orbitals wander: 2025 TV10 had a = 0.714 au on 2026-11-13, outside the 0.716 to 0.730 au window, so screening windows must be wider than the counts above.
- Spent rocket stages and other artificial objects sit in Earth-like orbits; check the JPL Horizons spacecraft list and any non-gravitational parameters before claiming.
- The MPC list pages (for example MarsTrojans.html) returned HTTP 403 to an automated fetch on 2026-11-13; do not work around it, use the literature for the Mars Trojan list.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/sky-archives/inner-planet-coorbital-unrecognised-neo.md
```

Already set up? Say `run V3R1T4S on inner-planet-coorbital-unrecognised-neo`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `inner-planet-coorbital-unrecognised-neo`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
