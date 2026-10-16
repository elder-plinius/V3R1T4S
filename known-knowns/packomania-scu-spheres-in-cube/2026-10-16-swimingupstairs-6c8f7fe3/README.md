# Spheres in a cube, N=886: r* = 0.0554957384274815113100000 (Packomania scu table 0.055470027839216034700251427886)

## What

The 886 centres in claim_886/scu886_candidate.txt have feasible radius r* = 0.05549573842748151131 in the cube [-1/2,1/2]^3. That exceeds the live Packomania scu radius.txt value 0.055470027839216034700251427886 for N=886 (re-fetched 2026-10-16T16:20:40Z) by 2.57e-5, and the configuration is not isometric to the posted scu886.txt. This holds subject to the unresolved Moki & Julio bundle caveat.

## Check it yourself

Python 3.8+ and a POSIX shell, standard library only:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Under a few seconds on a laptop. Checks the number of centres, distinctness, every pair distance and the walls in exact integer arithmetic, and the margin to the table value.

## Compared to

Packomania "spheres in a cube" (scu) table by Eckard Specht, https://packomania.com/scu/txt/radius.txt, cell N = 886, value 0.055470027839216034700251427886 (row author: David W. Cantrell), fetched 2026-10-16T15:47:57Z (HTTP 200), unchanged at 2026-10-16T16:20:40Z. Margin 2.571059e-5. Moki & Julio's Zenodo v2.7 manifest value for N=886 is 0.05549302841883663184319175. Details in the-record-we-beat/.

## Not claimed

Not claimed optimal. Not submitted to Packomania. Caveat required by the criterion: Packomania's pending list (08-Oct-2026) contains a Moki & Julio bundle of 4666 candidates (26-Sep-2026) whose category is not stated; it cannot be resolved, the comparison with Moki & Julio relies only on their Zenodo v2.7 manifest radii, and N=886 must be re-checked once that bundle leaves the pending list. Literature search: web search (arXiv 2610.13978 covers N=203 only), this repo's TROPHY_CASE.md and open PRs; not exhaustive. Reviewers were fresh contexts of the same assistant, not humans.

## Credits

Submission credit: SwimingUpstairs. It came out of the same chain started from the posted scu880.txt by Lu Peng (https://packomania.com/scu/txt/scu880.txt): 6 spheres were inserted one at a time into Lu Peng's 880-sphere packing with heavy re-relaxation after each, so no centre is unchanged to 1e-4 but most stay within 1e-2 of Lu Peng's positions. The 886 table row being compared is by David W. Cantrell. Table and coordinate files: Eckard Specht, Packomania (https://packomania.com). Moki & Julio dataset: https://doi.org/10.5281/zenodo.22986800. Protocol: V3R1T4S, https://github.com/elder-plinius/V3R1T4S, commit c8ba8bc4258164998de76ab939b0748fe80f73a2.
