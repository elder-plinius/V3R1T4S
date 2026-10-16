# Spheres in a cube, N=881: r* = 0.0556442823224865415209170 (Packomania scu table 0.055610202148)

## What

The 881 centres in claim_881/scu881_candidate.txt (sha256 100f397499b4601ca7b5825912cbad69fa8e1725a4888ac89abb453420b4a70f) have feasible radius r* = 0.05564428232248654152 in the cube [-1/2,1/2]^3. That exceeds the live Packomania scu radius.txt value 0.055610202148 for N=881 (fetched 2026-10-16T15:47:57Z; re-fetched 2026-10-16T16:20:40Z, unchanged) by 3.41e-5, and exceeds the Moki & Julio Zenodo v2.7 manifest radius 0.05561020036646987854691501. The posted scu881.txt is a different configuration. This holds subject to the unresolved Moki & Julio bundle caveat.

## Check it yourself

Python 3.8+ and a POSIX shell, standard library only:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Under a few seconds on a laptop. Checks the number of centres, distinctness, every pair distance and the walls in exact integer arithmetic, and the margin to the table value.

## Compared to

Packomania "spheres in a cube" (scu) table by Eckard Specht, https://packomania.com/scu/txt/radius.txt, cell N = 881, value 0.055610202148 (row author: Lu Peng), fetched 2026-10-16T15:47:57Z (HTTP 200), unchanged at 2026-10-16T16:20:40Z. Margin 3.408017e-5. Moki & Julio's Zenodo v2.7 manifest value for N=881 is 0.05561020036646987854691501. Details in the-record-we-beat/.

## Not claimed

Not claimed optimal. Not submitted to Packomania. Caveat required by the criterion: Packomania's pending list (08-Oct-2026) contains a Moki & Julio bundle of 4666 candidates (26-Sep-2026) whose category is not stated; it cannot be resolved, the comparison with Moki & Julio relies only on their Zenodo v2.7 manifest radii, and N=881 must be re-checked once that bundle leaves the pending list. Literature search: web search (arXiv 2610.13978 covers N=203 only), this repo's TROPHY_CASE.md and open PRs (cube: #206, #207 and our own drafts #235-#238 for N=884, 883, 882, 886); not exhaustive. Reviewers were fresh contexts of the same assistant, not humans.

## Credits

Submission credit: SwimingUpstairs. It extends the posted Packomania packing scu880.txt by Lu Peng (https://packomania.com/scu/txt/scu880.txt): one sphere was inserted into the largest hole of Lu Peng's 880-sphere packing and the configuration was re-relaxed (842 of Lu Peng's 880 centres are unchanged to 1e-4, all 880 within 1e-2). The posted scu881.txt is a different configuration (it lists 880 centres with a blank 881st row, and only a handful of them coincide with the candidate's to 1e-4); it is used here only for the not-isometric clause. Table and coordinate files: Eckard Specht, Packomania (https://packomania.com). Moki & Julio dataset: https://doi.org/10.5281/zenodo.22986800. Protocol: V3R1T4S, https://github.com/elder-plinius/V3R1T4S, commit c8ba8bc4258164998de76ab939b0748fe80f73a2.
