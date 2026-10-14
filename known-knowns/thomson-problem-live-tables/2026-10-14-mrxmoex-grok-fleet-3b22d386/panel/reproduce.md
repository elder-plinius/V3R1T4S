context: subagent (executor)

# REPRODUCE skeptic — claim C, Thomson N=550, partial win p1

Definition (quoted, criterion.txt p1): "A table-integrity finding: an N where a live table's posted energy is not reproduced by its own posted coordinates after mpmath polishing by more than 1e-6 (Deeter documents such cases for CCD N = 263, 377, 380, 381), reported with both energies to 12 digits."
Energy: E = sum_{i<j} 1/|x_i - x_j|, points normalized to the unit sphere, mpmath dps 30 (per verification_method step 2).

Own checker, written before reading verify/: pure mpmath at dps 30, fsum over all 150975 pairs. Tangent gradient = Euclidean gradient minus its radial component, 2-norm.

## Results
- sha256: t2_550_polished.txt = 3b22d386...4d5329, data/t2_550.xyz = 3ec7218c...ef8382. Both match claim.md.
- Both files hold 550 points.
- E(posted data/t2_550.xyz) = 144126.092799999221179309258. Matches the claim (…1793093).
- E(polished object) = 144126.092799999221178765513. Matches the claim (…1787655).
- Tangent gradient 2-norm of the polished object = 2.8e-27. The claim says 2.8e-29; the gap sits at the dps-30 roundoff floor for E ~ 1.4e5, and both values are far below the 1e-20 threshold.
- Same basin: the largest coordinate deviation between posted and polished points is 3.0e-10 (the posted file has 10 decimals). Polishing changes the energy by 5.4e-19.
- Posted cell, data/ccd_thomson2.html row 550: 144126.0927100. The number appears only once in the file.
- Gap: E_polished − cell = +8.99992e-5 > 1e-6. To 12 digits: posted cell 144126.092710, reproduced 144126.092800.
- Determinism: two full runs gave byte-identical output.
- Not checked here: Hessian certification (p1 does not require it) and a live re-fetch (I judged from the saved files only). Direction note: the cell is LOWER than its own coordinates reproduce. The p1 wording ("not reproduced ... by more than 1e-6") is still met literally.

pass: true
