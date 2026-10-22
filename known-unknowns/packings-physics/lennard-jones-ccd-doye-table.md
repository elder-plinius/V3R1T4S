# Lennard-Jones clusters: lower a putative global minimum in the Cambridge Cluster Database / Doye tables (N = 3..150, 310..1000)

⚪ **Packings and physics** · standard · tractability ★★☆☆☆ · compute: laptop-hours · open as of 2026-10-08

## The problem

The Cambridge Cluster Database (mirrored on Doye's site) lists putative global minima of LJ_N (energy in units of the pair well depth, 6 decimals) with point files: N = 3..150 (tables.150.html, LJ.tar), N = 310..561 (LJ310-561.html, incorporating Barron 537-548, Takeuchi 506/521/537-541, Huang-Lai-Xu 326/533/536) and N = 562..1000 (LJ562-1000.html, Xiang-Cheng-Cai-Shao 2004 plus 580 by Huang-Lai-Xu). The N = 151..309 and 1001..1610 tables were hosted at Shao's Nankai site, which no longer resolves (2026-10-08). Pages last modified 2025-03-04 (server move); the CCD invites improvements by email. Decades of global-optimization benchmarking make N <= 150 near-certainly optimal, but N = 310..1000 were set by one 2004 lattice-construction method and only a handful of N have been revisited (DLS-TPIO improved 533, 536; Barron 537-548, 664, 813). Moonshot-ish within a harvest frame: realistic targets are N in 310..1000.

## What counts as a win

Success means Cartesian coordinates (>= 16 digits) for N atoms, N listed on one of the three live Doye/CCD LJ table pages, such that E* = sum_{i<j} 4(r^-12 - r^-6) computed in mpmath at 30 digits is STRICTLY LOWER (direction: min) than the table energy for N re-fetched live immediately before claiming, by at least 1e-5 (the tables carry 6 decimals; genuine new minima differ by >= 1e-3 historically), AND the configuration is a certified local minimum (mpmath or quad-precision Newton to gradient norm < 1e-15, Hessian positive semidefinite with exactly 6 zero modes), AND polishing the table's own point file for N with the same routine gives E_table_polished - E* >= 1e-5 (distinct basin), AND an arXiv/Google Scholar check finds no published lower value for that N (Barron's page https://academicos.azc.uam.mx/cbr/LennardJones/nw537-548.htm and the 2013 DLS-TPIO paper are known sources already folded into the table).

## Partial wins

- **p1:** A certified lower energy (same local-minimum and distinct-basin rules) for some N in 151..309 or 1001..1100 than a SPECIFIC published value that the skeptic can fetch (DOI or arXiv id plus page/table reference, the value quoted to the paper's precision); the CCD has no live table for these N (the Shao/Nankai host chinfo.nankai.edu.cn does not resolve, checked 2026-10-08), so this is reported as 'literature frontier', not a table record, and a claim without a fetchable published comparator is not a win.
- **p2:** A certified improvement to an (N, rho) row that exists on the live CCD Morse-cluster table (https://doye.chem.ox.ac.uk/jon/structures/Morse/tables.html), same local-minimum and distinct-basin rules with margin 1e-5, reported together with the best literature value found for that (N, rho) (the CCD Morse table is known to lag the literature).
- **p3:** Reproduction audit: re-polish every table point file for N = 310..1000 in double precision and report any N where the posted coordinates relax to an energy lower than the posted value by > 1e-5 (under-converged table row) or do not match the posted value within 1e-5.

## How a win is checked

Checker (< 15 minutes for N <= 1000): curl the live table page and parse the energy for N (multi-column HTML; pairs 'N energy'); load the claimed coordinates; mpmath mp.dps = 30 (or numpy float128 then mpmath for the final sum) compute E* with E = 4 sum (r^-12 - r^-6); Newton/BFGS polish in high precision and confirm E* stable to 1e-12 and gradient < 1e-15; eigen-decompose the 3N x 3N Hessian in double and assert exactly 6 zero modes and no negative eigenvalues; download the table point file (LJ310-561/<N>.TXT, LJ562-1000/<N>.TXT, or LJ.tar for N <= 150; all checked live 2026-10-08), polish it identically, assert its energy exceeds E* by >= 1e-5. For N = 664 and 813 also assert E* < Barron's -4596.1978 / -5712.2517 by >= 1e-5.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://doye.chem.ox.ac.uk/jon/structures/LJ.html>

## Sources

- <https://doye.chem.ox.ac.uk/jon/structures/LJ.html>
- <https://doye.chem.ox.ac.uk/jon/structures/LJ/tables.150.html>
- <https://doye.chem.ox.ac.uk/jon/structures/LJ/LJ310-561.html>
- <https://doye.chem.ox.ac.uk/jon/structures/LJ/LJ562-1000.html>
- <https://doye.chem.ox.ac.uk/jon/structures/LJ/LJ.tar>
- <https://doye.chem.ox.ac.uk/jon/structures/LJ/LJ562-1000.tar.gz>
- <https://www-wales.ch.cam.ac.uk/CCD.html>
- <https://academicos.azc.uam.mx/cbr/LennardJones/nw537-548.htm>
- <https://doye.chem.ox.ac.uk/jon/structures/Morse/tables.html>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- N = 562..1000 came from a single 2004 lattice-construction + GA pipeline (Xiang et al.) and only N = 580, 664, 813 have since been improved; run dynamic lattice searching (DLS) with two-phase local search plus surface-interior operations from the posted structures, focusing on N just below Mackay/anti-Mackay shell completions (e.g. 561, 923) where decahedral or fcc competitors win (as at 38, 75-77, 98, 102-104).
- Structural-competition scan: for each N in 310..1000 build the best icosahedral, decahedral (Marks), fcc truncated-octahedral, and Leary-tetrahedral candidates by filling/removing surface sites greedily, relax, and compare; the 2004 table only explored lattice-based icosahedral/decahedral families.
- Polish-and-audit first (p3): relaxing all posted point files in double precision is cheap and may reveal under-converged rows (the CCD Thomson tables had such rows); then target those N.
- Known table-vs-literature gap (checked 2026-10-08): Barron's 2010 page claims LJ664 = -4596.1978 and LJ813 = -5712.2517, while the live Doye 562-1000 table still shows -4596.197078 and -5712.249964. Reproducing Barron there is NOT novel; the bar for N = 664 and 813 is Barron's value. Use the same trick (icosahedral 'IC no center' and 'ID' variants of the posted structure) on neighbouring N where nobody has looked.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Literature beats the table for N = 664 and 813 (Barron 2010, not folded into the live Doye table). A 'record' at those N that does not also beat Barron's values fails NOVELTY; always compare against the published value, not just the table.
- Units: energies are in pair well-depth units with sigma = 1 (E = 4 sum (r^-12 - r^-6)); a different reduced form (e.g. epsilon=1 with minimum at r=1, E = sum (r^-12 - 2 r^-6)) gives different numbers for the same structure.
- Any 'improvement' under 1e-5 is numerical; historically new LJ minima differ by 1e-3 or more.
- A polished posted structure giving a lower number than the posted value is an under-converged row, not a new minimum (distinct-basin test is mandatory).
- The 151..309 and 1001+ tables are offline (Shao's site); claims there cannot be table records.
- Emailing the CCD maintainers is an outbound message needing explicit permission from the human.
- Morse point files (p2): the Morse table on the Oxford mirror (https://doye.chem.ox.ac.uk/jon/structures/Morse/tables.html) links point files by relative paths that return 404 there (points/32D, 32E, 32F and 38A, 2026-10-18); the files are served at https://www-wales.ch.cam.ac.uk/~jon/structures/Morse/points/. There points/32E (sha256 d34c05b2...6681) holds the 32F structure: it is stationary at rho = 6 at -125.126341 (the 32F row; the 32E row is -125.644966) and relaxes to the 32F values -116.415892 (rho = 10) and -115.246208 (rho = 14), while points/32F is 404. For N = 32 at rho 11.40-20.90, where 32E is the listed global minimum (-115.767561 at rho = 14), the table's own point file is therefore not available for the distinct-basin test.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/packings-physics/lennard-jones-ccd-doye-table.md
```

Already set up? Say `run V3R1T4S on lennard-jones-ccd-doye-table`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `lennard-jones-ccd-doye-table`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
