# Spheres in a cube, N=882: r* = 0.0556442546188088971200000 (Packomania scu table 0.055592641354)

## What

The 882 centres in claim_882/scu882_candidate.txt have feasible radius r* = 0.05564425461880889712 in the cube [-1/2,1/2]^3. That exceeds the live Packomania scu radius.txt value 0.055592641354 for N=882 (re-fetched 2026-10-16T16:20:40Z) by 5.16e-5. The posted scu882.txt has 881 rows, so it is not the same configuration. This holds subject to the unresolved Moki & Julio bundle caveat.

## Check it yourself

Python 3.8+ and a POSIX shell, standard library only:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Under a few seconds on a laptop. Checks the number of centres, distinctness, every pair distance and the walls in exact integer arithmetic, and the margin to the table value.

## Compared to

Packomania "spheres in a cube" (scu) table by Eckard Specht, https://packomania.com/scu/txt/radius.txt, cell N = 882, value 0.055592641354 (row author: Lu Peng), fetched 2026-10-16T15:47:57Z (HTTP 200), unchanged at 2026-10-16T16:20:40Z. Margin 5.161326e-5. Moki & Julio's Zenodo v2.7 manifest value for N=882 is 0.05559261042933890869338052. Details in the-record-we-beat/.

## Not claimed

Not claimed optimal. Not submitted to Packomania. Caveat required by the criterion: Packomania's pending list (08-Oct-2026) contains a Moki & Julio bundle of 4666 candidates (26-Sep-2026) whose category is not stated; it cannot be resolved, the comparison with Moki & Julio relies only on their Zenodo v2.7 manifest radii, and N=882 must be re-checked once that bundle leaves the pending list. Literature search: web search (arXiv 2610.13978 covers N=203 only), this repo's TROPHY_CASE.md and open PRs; not exhaustive. Reviewers were fresh contexts of the same assistant, not humans.

## Credits

Submission credit: SwimingUpstairs. It extends the posted Packomania packing scu880.txt by Lu Peng (https://packomania.com/scu/txt/scu880.txt): the run inserted 2 spheres into the largest holes of Lu Peng's 880-sphere packing, one at a time, and re-relaxed (chain from scu880). Most of Lu Peng's 880 centres are essentially unchanged, so the construction is Lu Peng's packing plus 2 fitted spheres. Table and coordinate files: Eckard Specht, Packomania (https://packomania.com). Moki & Julio dataset: https://doi.org/10.5281/zenodo.22986800. Protocol: V3R1T4S, https://github.com/elder-plinius/V3R1T4S, commit c8ba8bc4258164998de76ab939b0748fe80f73a2.
