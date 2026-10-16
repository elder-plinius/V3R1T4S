# Spheres in a cube, N=884: r* = 0.0556439109093014305800000 (Packomania scu table 0.055518673263)

## What

The 884 centres in claim/scu884_candidate.txt (sha256 below) have feasible radius r* = 0.05564391090930143058 in the cube [-1/2,1/2]^3. That exceeds the live Packomania scu radius.txt value 0.055518673263 for N=884 (re-fetched 2026-10-16T16:20:40Z, unchanged) by 1.25e-4, and the configuration is not isometric to the posted scu884.txt. This holds subject to a re-check once the category-unspecified Moki confirmed_scope: The 883 centres in claim_883/scu883_candidate.txt have feasible radius r* = 0.05564404058613009463 in the cube [-1/2,1/2]^3. That exceeds the live Packomania scu radius.txt value 0.055542517155 for N=884 (re-fetched 2026-10-16T16:20:40Z) by 1.02e-4. The posted scu883.txt has 882 rows, so it is not the same configuration. This holds subject to the unresolved Moki & Julio bundle caveat. Julio 4666-candidate bundle leaves the pending list.

## Check it yourself

Python 3.8+ and a POSIX shell, standard library only:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Under a few seconds on a laptop. Checks the number of centres, distinctness, every pair distance and the walls in exact integer arithmetic, and the margin to the table value.

## Compared to

Packomania "spheres in a cube" (scu) table by Eckard Specht, https://packomania.com/scu/txt/radius.txt, cell N = 884, value 0.055518673263 (row author: Lu Peng), fetched 2026-10-16T15:47:57Z (HTTP 200), unchanged at 2026-10-16T16:20:40Z. Margin 1.252376e-4. Moki & Julio's Zenodo v2.7 manifest value for N=884 is 0.05551867320477953249122448. Details in the-record-we-beat/.

## Not claimed

Not claimed optimal. Not submitted to Packomania. Caveat required by the criterion: Packomania's pending list (08-Oct-2026) contains a Moki & Julio bundle of 4666 candidates (26-Sep-2026) whose category is not stated; it cannot be resolved, the comparison with Moki & Julio relies only on their Zenodo v2.7 manifest radii, and N=884 must be re-checked once that bundle leaves the pending list. Literature search: web search (arXiv 2610.13978 covers N=203 only), this repo's TROPHY_CASE.md and open PRs; not exhaustive. Reviewers were fresh contexts of the same assistant, not humans.

## Credits

Submission credit: SwimingUpstairs. It extends the posted Packomania packing scu880.txt by Lu Peng (https://packomania.com/scu/txt/scu880.txt): the run inserted 4 spheres into the largest holes of Lu Peng's 880-sphere packing, one at a time, and re-relaxed (chain from scu880). Most of Lu Peng's 880 centres are essentially unchanged, so the construction is Lu Peng's packing plus 4 fitted spheres. Table and coordinate files: Eckard Specht, Packomania (https://packomania.com). Moki & Julio dataset: https://doi.org/10.5281/zenodo.22986800. Protocol: V3R1T4S, https://github.com/elder-plinius/V3R1T4S, commit c8ba8bc4258164998de76ab939b0748fe80f73a2.
