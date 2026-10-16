# Spheres in a cube, N=806: r* = 0.0570208083064656470105186 (Packomania scu table 0.056998279608)

## What

The 806 centres in claim_806/scu806_candidate.txt (sha256 596503cd75b4f31d5d6dcb5d248e0cbb56f088acef07d045565e6e98b770e64d) have feasible radius r* = 0.05702080830646564701 in the cube [-1/2,1/2]^3. That exceeds the live Packomania scu radius.txt value 0.056998279608 for N=806 (fetched 2026-10-16T15:47:57Z; re-fetched 2026-10-16T16:20:40Z, unchanged) by 2.25e-5, and exceeds the Moki & Julio Zenodo v2.7 manifest radius 0.05699827673690576549947939. The posted scu806.txt is a different configuration. The radius is inherited from Lu Peng's posted 805 packing (r* equals the N=805 table value 0.057020808305 to about 1.5e-12); the claim is that one more sphere fits at that radius. This holds subject to the unresolved Moki & Julio bundle caveat.

## Check it yourself

Python 3.8+ and a POSIX shell, standard library only:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Under a few seconds on a laptop. Checks the number of centres, distinctness, every pair distance and the walls in exact integer arithmetic, and the margin to the table value.

## Compared to

Packomania "spheres in a cube" (scu) table by Eckard Specht, https://packomania.com/scu/txt/radius.txt, cell N = 806, value 0.056998279608 (row author: Lu Peng), fetched 2026-10-16T15:47:57Z (HTTP 200), unchanged at 2026-10-16T16:20:40Z. Margin 2.252870e-5. Moki & Julio's Zenodo v2.7 manifest value for N=806 is 0.05699827673690576549947939. Details in the-record-we-beat/.

## Not claimed

Not claimed optimal. Not submitted to Packomania. Caveat required by the criterion: Packomania's pending list (08-Oct-2026) contains a Moki & Julio bundle of 4666 candidates (26-Sep-2026) whose category is not stated; it cannot be resolved, the comparison with Moki & Julio relies only on their Zenodo v2.7 manifest radii, and N=806 must be re-checked once that bundle leaves the pending list. Literature search: web search (arXiv 2610.13978 covers N=203 only), this repo's TROPHY_CASE.md and open PRs (cube: #206, #207 and our own drafts #235-#238 for N=884, 883, 882, 886); not exhaustive. Reviewers were fresh contexts of the same assistant, not humans.

## Credits

Submission credit: SwimingUpstairs. It extends the posted Packomania packing scu805.txt by Lu Peng (https://packomania.com/scu/txt/scu805.txt). The candidate is scu805.txt unchanged (all 805 centres within 1e-4) plus one sphere placed in a free hole; there is no relaxation gain: r* equals Lu Peng's N=805 table radius 0.057020808305 to about 1.5e-12. The whole radius is Lu Peng's; this claim's contribution is showing that the posted 805 packing has room for an 806th sphere. The posted scu806.txt is a different configuration (it lists 805 centres with a blank 806th row, and only a handful coincide with scu805's to 1e-4); it is used here only for the not-isometric clause. Table and coordinate files: Eckard Specht, Packomania (https://packomania.com). Moki & Julio dataset: https://doi.org/10.5281/zenodo.22986800. Protocol: V3R1T4S, https://github.com/elder-plinius/V3R1T4S, commit c8ba8bc4258164998de76ab939b0748fe80f73a2.
