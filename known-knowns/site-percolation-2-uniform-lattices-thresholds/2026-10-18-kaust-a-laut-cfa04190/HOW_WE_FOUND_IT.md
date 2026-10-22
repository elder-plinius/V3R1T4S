# How we found it (contributor text, unverified)

- The bank target asks for any two-uniform site threshold 100 times more precise than the 2008 table. We picked the
  four "row" lattices (#20-#23), whose period is a single strip, so a transfer matrix on n x infinity cylinders is
  feasible, and built every lattice from geometry, checking vertex types against the Wikipedia row.
- Method A: the critical-polynomial root in Jacobsen's eigenvalue form on cylinders of circumference n = 1..16, then a
  frozen extrapolation rule (written before any two-uniform root existed), calibrated on Jacobsen's published
  square-site sequence and on the (3^3,4^2) bond threshold of Scullard and Jacobsen.
- Method B: Newman-Ziff wrapping-probability crossings on tori, a one-term finite-size fit, frozen in advance.
- What failed or worried us: at an interim look (20 blocks per size) the two methods were 3.04 combined sigma apart.
  We did not refit; the frozen plan already required 60 blocks per size (the Monte Carlo error was above 2e-6) plus
  calibrations (square site, (3^3,4^2) site, a common-offset test, a 2048 x 512 check torus). We also checked the
  Monte Carlo evaluator against exact enumeration on tiny tori and ran a block-position test on tori with exact
  crossings. At the single evaluation of the 60-block data every frozen rule passed (1.53 combined sigma).
- The #15 site series at n = 13 did not fit in 16 GB of memory and was dropped (not needed here).
- The run was cut off by a plan limit before its panel; the three-skeptic panel ran afterwards in fresh contexts,
  with a repair round in which the REPRODUCE skeptic recomputed every root n = 9..16 (bit-identical) and ran fresh-seed
  Monte Carlo at two sizes.
