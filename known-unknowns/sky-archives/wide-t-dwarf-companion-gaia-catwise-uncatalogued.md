# New wide T or Y dwarf companion to a Gaia star by common proper motion in CatWISE2020 and unTimely, absent from the companion lists

🔭 **Sky archives** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours (IRSA TAP queries of catwise_2020 around nearby Gaia stars return thousands of rows; unTimely per-tile catalogues are megabytes each) · open as of 2026-11-13

## The problem

Brown dwarfs too faint for Gaia but bound to a Gaia star are benchmarks: the star gives their distance, age and composition. The coolest (T and Y dwarfs) are a few to a few tens of Jupiter masses. Rothermich, Faherty, Bardalez-Gagliuffi, Schneider, Kirkpatrick, Meisner, Burgasser, Kuchner and 38 others, including Backyard Worlds: Planet 9 volunteers (2024, AJ; arXiv 2403.04592), reported 89 new systems with ultracool companions, raising the number known around FGK stars by about 42% and more than tripling those wider than 1,000 au. Further hauls followed: Marocco, Kirkpatrick, Schneider, Meisner and 80 others (2024, ApJ; arXiv 2404.14324: 13 new M plus T pairs), Bravo, Schneider, Casewell and colleagues (2024, AJ; arXiv 2412.04597: 51 white dwarfs with candidate ultracool companions), Kiwy et al. 2022 (34 co-moving systems from the NOIRLab Source Catalog), Zhang et al. 2025 (MNRAS; arXiv 2505.24560: L 122-88 AB, an M2 plus T5 pair 215.6 arcsec apart), Schneider, Kuchner, Faherty, Meisner, Kirkpatrick, Burgasser and 70 others (2026, accepted to AJ; arXiv 2604.01323: 3,006 motion-confirmed L and T dwarfs including 28 new co-moving companions) and the RMSTAR catalogue of LeBlanc et al. 2026 (arXiv 2609.17729: 305 wide stellar and 9 brown-dwarf companions of the 3,352 nearest M dwarf systems, found with Gaia alone). WISE stopped observing in 2024, so the motion baseline is final; Gaia DR4 (due 2026-12-02) will sharpen host motions. Open task: a new T or Y dwarf that shares the motion of a Gaia star and is in no list. A win is a companion candidate.

## What counts as a win

A saved bundle (IRSA TAP queries, CatWISE2020 and unTimely rows, Gaia DR3 host row, motion-fit and chance-alignment code) where: (1) the companion has CatWISE2020 W1-W2 of at least 1.0 mag with clean ab_flags and cc_flags, and no Gaia DR3 source within 3 arcsec of its epoch-propagated position; (2) its CatWISE2020 proper motion is significant at 5 sigma or more and is matched within 3 sigma by an independent linear fit to at least 4 unTimely epochs spanning at least 6 years; (3) the host is a Gaia DR3 star with parallax above 5 mas at more than 10 sigma, the two proper motions agree within 3 sigma in each component (errors combined), and the companion's photometric distance from its W2 absolute magnitude for its W1-W2 colour (Kirkpatrick et al. 2021 relations, 0.5 mag scatter) agrees with the host parallax within 2 sigma; (4) the projected separation is at most 10,000 au, and the same cuts applied around at least 100 positions offset by 1 to 3 deg at the same Galactic latitude yield a chance-alignment probability below 0.1%; (5) no SIMBAD object within 10 arcsec, unless its own position and motion show it is a different source, and no entry in the UltracoolSheet, Rothermich et al. 2024, Schneider et al. 2026, Kirkpatrick et al. 2021 or 2024, LeBlanc et al. 2026, Zhang et al. 2025, Kiwy et al. 2022, Marocco et al. 2024, Bravo et al. 2024, or any arXiv paper or Backyard Worlds Talk post found by its CatWISE name and coordinates, all re-fetched immediately before claiming.

## Partial wins

- **p1:** The pipeline recovers at least 80% of the Rothermich et al. 2024 companions with W1-W2 of at least 1.0 under the same cuts, and lists every other pair it finds with its chance-alignment probability.
- **p2:** A new pair meeting (2) to (5) whose companion has W1-W2 between 0.4 and 1.0 (late L or early T colours) and no Gaia DR3 counterpart.
- **p3:** A pair meeting (1) to (5) whose host belongs to a young moving group with BANYAN Sigma membership probability above 90%, making the companion a planetary-mass candidate by its age.

## How a win is checked

The skeptic reruns the TAP queries, refits the unTimely positions, recomputes the motion match, photometric distance and chance-alignment probability with new offset fields, and searches the listed catalogues and SIMBAD. Under an hour.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://export.arxiv.org/api/query?search_query=%28abs:ultracool+OR+abs:%22T+dwarf%22+OR+abs:%22brown+dwarf%22%29+AND+%28abs:comoving+OR+abs:co-moving+OR+abs:%22wide+companion%22+OR+abs:%22wide+companions%22%29&sortBy=submittedDate&sortOrder=descending&max_results=25>

## Sources

- <https://arxiv.org/abs/2403.04592>
- <https://arxiv.org/abs/2404.14324>
- <https://arxiv.org/abs/2604.01323>
- <https://arxiv.org/abs/2505.24560>
- <https://arxiv.org/abs/2609.17729>
- <https://arxiv.org/abs/2204.09739>
- <https://arxiv.org/abs/2412.04597>
- <https://irsa.ipac.caltech.edu/TAP/sync?QUERY=SELECT+TOP+1+source_name,ra,dec,pmra,pmdec,w1mpro,w2mpro+FROM+catwise_2020&FORMAT=csv>
- <https://unwise.me/data/neo7/untimely-catalog/>
- <https://docs.google.com/spreadsheets/d/1i98ft8g5mzPp2DNno0kcz4B9nzMxdpyz5UquAVhz-U8/edit#gid=0>
- <https://backyardworlds.org/>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Search outward from Gaia stars within 100 pc rather than from red WISE sources, which reaches companions with modest motions that isolated-object searches skip.
- The Galactic plane and crowded fields, where volunteer searches and earlier cross-matches were least complete.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- A companion with W1-W2 of at least 2.0 and motion of at least 150 mas/yr also meets the cuts of catwise-cold-brown-dwarf-candidate-uncatalogued; claim it under one entry only.
- Unresolved blends and diffraction spikes near bright hosts give spurious CatWISE motions; require the unTimely confirmation and clean flags.
- Wide pairs in young moving groups share motions without being bound; the chance-alignment test must use comparison fields, not only the field population.
- The UltracoolSheet was last updated on 2025-07-03 (v2.1.0), before Schneider et al. 2026 and LeBlanc et al. 2026; check those papers' tables directly.
- The status query misses some papers whose abstracts say co-moving companions in other words (it did not return Rothermich et al. 2024 or Marocco et al. 2024 on 2026-11-13); also search by name and coordinates.
- Gaia DR4 (due 2026-12-02) may detect some late-L companions directly; after release, check its tables too.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/sky-archives/wide-t-dwarf-companion-gaia-catwise-uncatalogued.md
```

Already set up? Say `run V3R1T4S on wide-t-dwarf-companion-gaia-catwise-uncatalogued`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `wide-t-dwarf-companion-gaia-catwise-uncatalogued`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
