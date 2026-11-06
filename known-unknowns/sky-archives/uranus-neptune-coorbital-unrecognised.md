# Unrecognised Uranus or Neptune co-orbital (Trojan, horseshoe or quasi-satellite) among catalogued small bodies, shown by clone integration

🔭 **Sky archives** · harvest (many cells or partial wins within reach) · tractability ★★★★☆ · compute: laptop-hours (SBDB orbit and covariance per object; 100-clone N-body runs over 1 Myr with the giant planets take minutes to an hour each) · open as of 2026-11-06

## The problem

The Minor Planet Center lists 35 Neptune Trojans (page re-fetched 2026-10-30, elements at epoch 2025-11-21), including 2025 MD138, 2025 MH348 and 2025 NN80, the first L5 objects found in Rubin Observatory Science Validation data (Schwamb, Bernardinelli, Volk and collaborators, arXiv:2610.38309, 2026-10-28, who confirm 2025 MH348 and 2025 NN80 as long-term stable and leave 2025 MD138, with a 38-day arc, as a candidate). Its Uranus Trojan list is empty, although the literature reports two Uranus Trojans: 2011 QF99 (Alexandersen et al. 2013) and 2014 YX49 (de la Fuente Marcos and de la Fuente Marcos 2017). On 2026-10-30 the JPL SBDB holds 62 objects with 29.7 < a < 30.5 au and 30 with 18.9 < a < 19.5 au. Several low-eccentricity ones near Neptune's a are not on the MPC list: 2020 VK45 and 2020 VN45 have condition codes 4 and 3, while 2023 LH7, 2025 LV7, 2025 NE203 and 2025 OA697 still have short arcs (condition codes 6-8); new trans-Neptunian orbits keep arriving from DECam and Rubin. Whether any of these is already published as a co-orbital was not settled here, so the literature check in the criterion matters. Correction (2026-11-06): the LiDO survey paper (Alexandersen et al., arXiv:2610.19865, 2026-10-14, Tables 1 and 2) classifies 2020 VK45 and 2020 VN45 as 1:1 resonators with all clones resonant and a libration centre near 63 deg, i.e. Neptune L4 Trojans, so neither is open. SBDB carries no orbit covariance for these two, whose orbits it takes from the MPC. Integrating an object's orbit together with its uncertainty settles whether it is co-orbital. Open task: identify a catalogued object as a Uranus or Neptune co-orbital that is not on the MPC lists and has not been reported as one.

## What counts as a win

A saved bundle (SBDB orbit solution and covariance as fetched, >= 100 clones drawn from that covariance plus the nominal orbit, integration code and output) where: (1) the orbit has a data arc of >= 2 oppositions and condition code <= 5; (2) the clones are integrated together with the Sun (inner-planet masses added), Jupiter, Saturn, Uranus and Neptune, taken from JPL Horizons at the solution epoch (e.g. REBOUND WHFast or IAS15, relative energy error < 1e-8), for >= 1 Myr for Neptune or >= 100 kyr for Uranus; (3) for >= 90% of clones the resonant angle lambda - lambda_planet librates (does not circulate) for at least the first 10 libration cycles, and the classification (L4/L5 tadpole, horseshoe or quasi-satellite) and libration period are stated; (4) the object is on neither https://minorplanetcenter.net/iau/lists/NeptuneTrojans.html nor UranusTrojans.html, and no MPEC, RNAAS or arXiv paper identifies it as co-orbital (re-fetched immediately before claiming).

## Partial wins

- **p1:** The pipeline reproduces the MPC classification ( > = 90% of clones librating about the listed L4/L5 point) for >= 90% of the listed Neptune Trojans whose orbits meet (1), and the published co-orbital state of 2011 QF99 and 2014 YX49, with plots saved and every mismatch listed.
- **p2:** An object meeting (1), (2) and (4) for which 50-90% of clones librate: a candidate whose status needs a longer arc.
- **p3:** An object on an MPC Trojan list whose orbit meets (1) and for which >= 90% of clones circulate under procedure (2)-(3): a documented classification correction.

## How a win is checked

Skeptic fetches the same SBDB solution (orbit id saved), regenerates the clones with the saved seed, reruns the integration with an independent integrator or step size, and checks the resonant-angle plots and the MPC lists. Under an hour per object.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://minorplanetcenter.net/iau/lists/NeptuneTrojans.html>

## Sources

- <https://minorplanetcenter.net/iau/lists/NeptuneTrojans.html>
- <https://minorplanetcenter.net/iau/lists/UranusTrojans.html>
- <https://ssd-api.jpl.nasa.gov/sbdb_query.api?fields=full_name%2Ca%2Ce%2Ci%2Com%2Cw%2Cma%2Cepoch%2Cdata_arc%2Ccondition_code&sb-cdata=%7B%22AND%22%3A%5B%22a%7CRG%7C29.7%7C30.5%22%5D%7D>
- <https://ssd-api.jpl.nasa.gov/sbdb_query.api?fields=full_name%2Ca%2Ce%2Ci%2Com%2Cw%2Cma%2Cepoch%2Cdata_arc%2Ccondition_code&sb-cdata=%7B%22AND%22%3A%5B%22a%7CRG%7C18.9%7C19.5%22%5D%7D>
- <https://ssd-api.jpl.nasa.gov/doc/sbdb.html>
- <https://ssd.jpl.nasa.gov/horizons/>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Start with SBDB objects with |a - a_planet| < 0.3 au and e < 0.15 that are missing from the MPC lists, then widen to higher-e Centaurs that may be temporary co-orbitals.
- Compute the resonant angle at the solution epoch first: objects whose angle is far from 60 deg or 0 deg, with a large amplitude, are usually horseshoe or circulating.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Short-arc orbits (condition code >= 6) give clones that diverge; the criterion excludes them.
- Osculating heliocentric elements, used in place of barycentric ones, shift a enough to misclassify; integrate in a barycentric frame.
- de la Fuente Marcos and others publish many co-orbital identifications in RNAAS and MNRAS; check the literature by designation.
- The MPC lists omit published co-orbitals: the SBDB sets include (309239) 2007 RW10, a published Neptune quasi-satellite, and (83982) Crantor, a published Uranus horseshoe companion; absence from the MPC lists is not enough.
- 2012 UW177 is a published Neptune co-orbital that the MPC Neptune Trojan list does not include: Alexandersen et al. (arXiv:1411.7953, AJ 2016) found it librating about L4 (tadpole 35-75 deg ahead of Neptune) as a temporary co-orbital that leaves the resonance within about 1.5 Myr. A 100-clone run that shows it librating is a known positive for calibration, not a find.
- SBDB has no orbit covariance for objects whose orbit it takes from the MPC (2020 VK45 and 2020 VN45 are examples), so the criterion's clone bundle cannot be built from SBDB for them. Check that the SBDB response contains a covariance before planning a run around an object.
- Searching arXiv by designation misses survey papers that list objects only in data tables: LiDO (arXiv:2610.19865) names 2020 VK45 and 2020 VN45 only in its Tables 1-2. Search the HTML or PDF tables of recent survey papers (LiDO, OSSOS, DES, Rubin/LSST) and journal pages, not only abstracts.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/sky-archives/uranus-neptune-coorbital-unrecognised.md
```

Already set up? Say `run V3R1T4S on uranus-neptune-coorbital-unrecognised`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `uranus-neptune-coorbital-unrecognised`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
