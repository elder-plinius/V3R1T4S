# Spheres in a cube, N=619: r* = 0.0619587282294713999635096 (Packomania scu table 0.061950245135)

## What

The 619 centres in claim_619/scu619_candidate.txt (sha256 39f79632ebe0c658c423b40fd654a322368db4d2c662d790b7679a9bf4ffb469) have feasible radius r* = 0.06195872822947139996 in the cube [-1/2,1/2]^3. That exceeds the live Packomania scu radius.txt value 0.061950245135 for N=619 (fetched 2026-10-16T15:47:57Z; re-fetched 2026-10-16T16:20:40Z, unchanged) by 8.48e-6, and exceeds the Moki & Julio Zenodo v2.7 manifest radius 0.06195020774705905122608289. The posted scu619.txt is a different configuration. This holds subject to the unresolved Moki & Julio bundle caveat.

## Check it yourself

Python 3.8+ and a POSIX shell, standard library only:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Under a few seconds on a laptop. Checks the number of centres, distinctness, every pair distance and the walls in exact integer arithmetic, and the margin to the table value.

## Compared to

Packomania "spheres in a cube" (scu) table by Eckard Specht, https://packomania.com/scu/txt/radius.txt, cell N = 619, value 0.061950245135 (row author: Lu Peng), fetched 2026-10-16T15:47:57Z (HTTP 200), unchanged at 2026-10-16T16:20:40Z. Margin 8.483094e-6. Moki & Julio's Zenodo v2.7 manifest value for N=619 is 0.06195020774705905122608289. Details in the-record-we-beat/.

## Not claimed

Not claimed optimal. Not submitted to Packomania. Caveat required by the criterion: Packomania's pending list (08-Oct-2026) contains a Moki & Julio bundle of 4666 candidates (26-Sep-2026) whose category is not stated; it cannot be resolved, the comparison with Moki & Julio relies only on their Zenodo v2.7 manifest radii, and N=619 must be re-checked once that bundle leaves the pending list. Literature search: web search (arXiv 2610.13978 covers N=203 only), this repo's TROPHY_CASE.md and open PRs (cube: #206, #207 and our own drafts #235-#238 for N=884, 883, 882, 886); not exhaustive. Reviewers were fresh contexts of the same assistant, not humans.

## Credits

Submission credit: SwimingUpstairs. It extends the posted Packomania packing scu618.txt by Lu Peng (https://packomania.com/scu/txt/scu618.txt): one sphere was inserted into the largest hole of Lu Peng's 618-sphere packing and the configuration was locally relaxed (594 of Lu Peng's 618 centres are unchanged to 1e-4, all 618 within 1e-2). The posted scu619.txt is a different configuration (it lists 618 centres with a blank 619th row, and only a handful coincide with the candidate's to 1e-4); it is used here only for the not-isometric clause. Table and coordinate files: Eckard Specht, Packomania (https://packomania.com). Moki & Julio dataset: https://doi.org/10.5281/zenodo.22986800. Protocol: V3R1T4S, https://github.com/elder-plinius/V3R1T4S, commit c8ba8bc4258164998de76ab939b0748fe80f73a2.
