# How we found it (contributor text, unverified)

Brief: the 2026-10-24 V3R1T4S weekend run on cap-set-dim7-dim8 (heavy effort, one laptop, CPU only) ran three lenses
one after another. The target asks for a cap of 237+ in F_3^7 or 513+ in F_3^8; a larger cap in F_3^9 or F_3^10 is
a partial win.

- What failed: exact neighbourhood searches around the record caps. Around the 236-cap of F_3^7 (rebuilt from
  Tyrrell's explicit collection), SAT proved that no cap of 237+ shares 223 or more points with it. Every examined
  re-optimisation of the 512-cap of F_3^8 (all five classes of its hard hyperplane cosets) was proven to give no gain.
  Orbit unions under many symmetry groups stayed at or below the records.
- What worked: the slice frame one dimension up (F_3^9 = F_3 x F_3^8). A set {0}xB0 u {1}xB1 u {2}xB2 is a cap when
  each slice is a cap and no b0 + b1 + b2 = 0. With B1 = B2 = C (the FunSearch 512-cap) the third slice must avoid
  -(C + C), which is everything. Twisting the second copy by sign diagonals D, i.e. B2 = D C, the lens scored all 256
  sign diagonals and 3000 random signed permutations by the number of points left for B0. Most leave 0 points; one class
  (D = diag(2,2,2,2,2,1,1,1) up to C's own sign symmetries) leaves 92, which hold an 80-point cap (CP-SAT, proven
  optimal). 512 + 512 + 80 = 1104, against 1082 published. The same recipe applied to the 236-cap gives 496, exactly
  Edel's old value for F_3^8, which made the construction plausible.
- Checks: the run's two-route exact checker and a separate numpy checker; the three skeptic reports (REPRODUCE,
  NOVELTY, CRITERION) are in panel/.
