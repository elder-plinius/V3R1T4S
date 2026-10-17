# Spheres in a cube, N=881-884 ("Lu Peng 880 + k"): N=884 r* = 0.0556439109093014305800000 (Packomania scu table 0.055518673263)

## What

The 884 centres in object/scu884.txt (sha256 below) have feasible radius r* = 0.05564391090930143058 in the cube [-1/2,1/2]^3. That exceeds the live Packomania scu radius.txt value 0.055518673263 for N=884 (re-fetched 2026-10-16T16:20:40Z, unchanged) by 1.25e-4, and the configuration is not isometric to the posted scu884.txt. This holds subject to a re-check once the category-unspecified Moki & Julio 4666-candidate bundle leaves the pending list.

## Check it yourself

Python 3.8+ and a POSIX shell, standard library only:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Under a minute on a laptop. For object/scu884.txt (N=884) and object/scu881.txt (N=881) it checks that each object matches its sha256 in INDEX.csv, then the number of centres, distinctness, every pair distance and the walls in exact integer arithmetic, and the margin to the table value; the final PASS needs both.

## Compared to

Packomania "spheres in a cube" (scu) table by Eckard Specht, https://packomania.com/scu/txt/radius.txt, cell N = 884, value 0.055518673263 (row author: Lu Peng), fetched 2026-10-16T15:47:57Z (HTTP 200), unchanged at 2026-10-16T16:20:40Z. Margin 1.252376e-4. Moki & Julio's Zenodo v2.7 manifest value for N=884 is 0.05551867320477953249122448. Details in the-record-we-beat/.

## Also N=881-883 (one "Lu Peng 880 + k" package, at the maintainer's request)

Deletion relation: removing spheres cannot shrink any centre distance or wall gap, so deleting any 1, 2 or 3 spheres from object/scu884.txt leaves 883, 882 or 881 centres with r* >= 0.05564391090930143058. That beats the live table values for N=883 (0.055542517155) by 1.013938e-4, N=882 (0.055592641354) by 5.126956e-5 and N=881 (0.055610202148) by 3.370876e-5, by plain deletion. The N=883 and N=882 packages (#236, #237) were deletion-plus-relax versions of this object (re-relaxing gains only about 1e-7) and are folded in here as this note.

N=881 secondary object: object/scu881.txt (sha256 100f397499b4601ca7b5825912cbad69fa8e1725a4888ac89abb453420b4a70f), first submitted as #263 and folded in here, is Lu Peng's scu880 plus one sphere, re-relaxed. 879 of its 881 centres lie within 1e-3 of centres of object/scu884.txt, so it is essentially this packing minus three spheres. It has r* = 0.05564428232248654152, which beats the N=881 table value by 3.408017e-5; the separate relaxation adds 3.714132e-7 over plain deletion. Its gate and three-skeptic panel are in panel/n881/ (status CONFIRMED_SOLUTION), and verify-it-yourself/run_checks.sh checks it too.

## Not claimed

Not claimed optimal. Not submitted to Packomania. Caveat required by the criterion: Packomania's pending list (08-Oct-2026) contains a Moki & Julio bundle of 4666 candidates (26-Sep-2026) whose category is not stated; the cells are re-checked against the live table if Packomania later posts a higher value. Moki & Julio comparison, resolved against their latest public dataset (Zenodo 10.5281/zenodo.22986800 v2.7, 2026-09-27, the day after their 26-Sep-2026 pending-list entry): their scu radii are 0.05561020036646987854691501 (N=881), 0.05559261042933890869338052 (N=882), 0.05554253628883839949629888 (N=883) and 0.05551867320477953249122448 (N=884). This package beats them by 3.408196e-5 (N=881, object/scu881.txt; 3.371054e-5 by deletion alone), 5.130048e-5 (N=882), 1.013746e-4 (N=883) and 1.252377e-4 (N=884). Only their manifest radii were used, not their coordinate archive. Literature search: web search (arXiv 2610.13978 covers N=203 only), this repo's TROPHY_CASE.md and PRs (cube: #206, #207; ours: #238 for N=886, now merged; #236, #237 and #263 for N=883, 882 and 881, folded into this PR); not exhaustive. Reviewers were fresh contexts of the same assistant, not humans.

## Credits

Submission credit: SwimingUpstairs. It extends the posted Packomania packing scu880.txt by Lu Peng (https://packomania.com/scu/txt/scu880.txt): the run inserted 4 spheres into the largest holes of Lu Peng's 880-sphere packing, one at a time, and re-relaxed (chain from scu880). Most of Lu Peng's 880 centres are essentially unchanged, so the construction is Lu Peng's packing plus 4 fitted spheres. object/scu881.txt is the same chain stopped after one insertion (842 of Lu Peng's 880 centres unchanged to 1e-4, all 880 within 1e-2). Table and coordinate files: Eckard Specht, Packomania (https://packomania.com). Moki & Julio dataset: https://doi.org/10.5281/zenodo.22986800. Protocol: V3R1T4S, https://github.com/elder-plinius/V3R1T4S, commit c8ba8bc4258164998de76ab939b0748fe80f73a2.
