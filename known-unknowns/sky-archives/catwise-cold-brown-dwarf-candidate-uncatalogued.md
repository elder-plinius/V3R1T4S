# New cold (late-T or Y) brown dwarf candidate with significant motion in CatWISE2020 and unTimely, absent from SIMBAD and the ultracool-dwarf compilations

🔭 **Sky archives** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours (IRSA TAP queries of catwise_2020 with colour and motion cuts return tens of thousands of rows; unTimely per-tile catalogues are MB each) · open as of 2026-10-30

## The problem

CatWISE2020 (Marocco et al. 2021, ApJS 253, 8) gives positions and proper motions for ~1.9 billion WISE/NEOWISE sources. unTimely (Meisner et al. 2023, AJ 165, 36) gives time-resolved unWISE detections. The known nearby L, T and Y dwarfs are listed by the Backyard Worlds: Planet 9 citizen-science project (Kuchner, Faherty, Meisner, Kirkpatrick and volunteers), by Kirkpatrick et al. (2021, ApJS 253, 7; 2024 20-pc census) and by the UltracoolSheet (Best, Dupuy, Liu, Sanghi, Siverd, Zhang; v2.1.0, 2025-07-03). Yet the coldest, faintest objects are still incomplete beyond ~20 pc, and new Y-dwarf candidates keep appearing. NEOWISE ended in 2024, so the WISE time baseline is final. Open task: find a cold-brown-dwarf candidate with WISE colours of >= T7 and a significant, independently confirmed motion that is in no catalogue or paper.

## What counts as a win

A saved bundle (IRSA TAP queries, CatWISE2020 rows, unTimely detections, Legacy Surveys DR10 and Pan-STARRS1 cutout photometry, motion-fit code) for an object with: (1) CatWISE2020 W1-W2 >= 2.0 mag (or W1 undetected with W2 S/N >= 8 and a W1-W2 lower limit >= 2.0) and clean ab_flags/cc_flags; (2) a CatWISE2020 total proper motion >= 150 mas/yr at >= 6 sigma, matched within 3 sigma by an independent linear motion fit to >= 4 unTimely epochs spanning >= 6 yr, with a stationary neighbour fitted the same way as a control; (3) no Gaia DR3 source within 3 arcsec of the epoch-propagated position, and z - W2 >= 4, with z from Legacy Surveys DR10 in AB and W2 from CatWISE2020 in Vega, each as its own catalogue publishes it (converting W2 to AB, W2_AB = W2_Vega + 3.339, would exclude 48 of the 57 UltracoolSheet v2.1.0 dwarfs of type T6 and later that have a published z, so it is not the intended bar); or z undetected in Legacy Surveys DR10; north of the DR10 footprint the DR9 north coverage served by the Legacy Survey viewer may be used instead, stated as such in the bundle; (4) no SIMBAD object within 10 arcsec of the epoch-2000 and epoch-2016 positions unless its own SIMBAD position and proper motion show it is a different source, no UltracoolSheet entry, no entry in the Kirkpatrick et al. 2021/2024 tables, no arXiv paper, and no entry within 10 arcsec in the Backyard Worlds: Planet 9 published discovery compilations (Schneider et al. 2026 Table 1 and any successor table), and no post found by searching the project's Zooniverse Talk boards for its CatWISE designation and its coordinates WHERE THAT SEARCH IS SHOWN TO WORK: the claimant must run, and record, a positive control that retrieves a known indexed Talk comment containing a designation of the same form, and if the control returns nothing the Talk search is recorded as uninformative rather than passed, the compilation check standing in its place (all re-fetched immediately before claiming). The claim is 'new cold brown dwarf candidate', not a spectral type.

## Partial wins

- **p1:** Pipeline recovers >= 90% of the UltracoolSheet T7-Y dwarfs inside a declared region of >= 1000 deg^2 with the same cuts (as written this is unreachable: the criterion's own motion cut, CatWISE2020 total proper motion >= 150 mas/yr at >= 6 sigma, itself recovers only 15 of the 21 such dwarfs in a declared high-latitude region of a few thousand square degrees, so either the 90% bar or the requirement to use the same cuts has to give), and lists the false positives left after automated vetting (no visual inspection).
- **p2:** A batch of >= 5 new candidates with W1-W2 between 1.5 and 2.0 (mid-T colours) meeting (2)-(4).
- **p3:** An object of any colour with total motion >= 1 arcsec/yr confirmed in two independent surveys (e.g. CatWISE2020 and Legacy Surveys/Pan-STARRS epochs), absent from SIMBAD and with no Gaia DR3 counterpart of consistent motion: a missing high-proper-motion nearby object.

## How a win is checked

Skeptic re-runs the IRSA TAP query, refits the unTimely positions with the saved code, checks Gaia DR3, Legacy Surveys and SIMBAD cones at both epochs, and searches the UltracoolSheet CSV export. Under an hour.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://docs.google.com/spreadsheets/d/1i98ft8g5mzPp2DNno0kcz4B9nzMxdpyz5UquAVhz-U8/edit#gid=0>

## Sources

- <https://irsa.ipac.caltech.edu/TAP/sync?QUERY=SELECT+TOP+1+source_name,ra,dec,pmra,pmdec,w1mpro,w2mpro+FROM+catwise_2020&FORMAT=csv>
- <https://unwise.me/data/neo7/untimely-catalog/>
- <https://docs.google.com/spreadsheets/d/1i98ft8g5mzPp2DNno0kcz4B9nzMxdpyz5UquAVhz-U8/edit#gid=0>
- <https://backyardworlds.org/>
- <https://ui.adsabs.harvard.edu/abs/2021ApJS..253....7K>
- <https://ui.adsabs.harvard.edu/abs/2021ApJS..253....8M>
- <https://simbad.cds.unistra.fr/simbad/sim-tap/sync?REQUEST=doQuery&LANG=ADQL&FORMAT=csv&QUERY=select+top+1+main_id+from+basic>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Galactic-plane and crowded fields, where Backyard Worlds volunteers and earlier colour cuts were least complete.
- Objects with moderate CatWISE motion (150-400 mas/yr), i.e. Y dwarfs at 20-50 pc, rather than the fast movers already harvested.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- CatWISE2020 has spurious motions from blends, latent images and diffraction spikes; require the unTimely confirmation and clean flags.
- Red, faint W2-only sources include high-redshift galaxies and AGN; demand significant motion.
- The UltracoolSheet is complete only for objects known by 2015 plus selected later ones; absence there is not enough, so SIMBAD and the literature must be checked too.
- The Zooniverse Talk search cannot retrieve coordinate-style designations at all: a comment containing the verbatim string J203232.78-275607.5 is returned by none of the queries J203232, 203232, J2032, the full designation, the decimal coordinate or 275607, and a comment containing WISEA J083011.95+283716.0 is likewise unfindable. An empty Talk result is therefore not evidence of absence unless a positive control is recorded alongside it. A site-restricted outside search fails the same controls, so its coverage of Talk comment bodies is undemonstrated.
- Magnitude systems: Legacy Surveys publishes z in AB and CatWISE2020 publishes W2 in Vega, and the difference between the two readings of z - W2 is 3.339 mag, which decides condition (3) on its own. State the system used.
- Legacy Surveys DR10 does not cover the northern sky; the Legacy Survey viewer serves DR9 there. A search region that crosses the footprint boundary cannot satisfy condition (3) as worded everywhere inside it.
- CDS Strasbourg can be wholly down (404 on every SIMBAD and VizieR path) while mirrors answer; a mirror may also return HTTP 200 carrying QUERY_STATUS=ERROR, which reads as an empty cone unless the body is inspected. Treat every null cone as unproven until a positive control returns a known source from the same service.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/sky-archives/catwise-cold-brown-dwarf-candidate-uncatalogued.md
```

Already set up? Say `run V3R1T4S on catwise-cold-brown-dwarf-candidate-uncatalogued`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `catwise-cold-brown-dwarf-candidate-uncatalogued`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
