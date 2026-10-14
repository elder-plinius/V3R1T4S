context: subagent (executor)

# CRITERION skeptic — Claim B, N = 3552 (partial win p1)

## Target
p1 (verbatim): "an N where a live table's posted energy is not reproduced by its own posted coordinates after mpmath polishing by more than 1e-6 ... reported with both energies to 12 digits."
Full success is not claimed and cannot apply (N = 3552 > 1500). p3 is not claimed.

## Literal checks
- "an N": no N <= 1500 bound is attached to p1. N = 3552 qualifies.
- "a live table": CCD Riesz s=1 index. I fetched it again live (2026-10-14, ~16:55 Berlin) and it still contains 6191355.6866585.
- "its own posted coordinates": points_3552_1.dat re-fetched live (HTTP 200). Its sha256 837f6c84... matches the claim. Note: the claim folder lacks data/points_3552_1.dat even though claim.md cites it. This is a packaging defect, but I fixed it for this check by fetching the file live.
- Independent energy check (my own extended-precision numpy summation, not the kit's scripts): posted file 6191355.68665850276, polished object 6191355.68664354541. Both agree with the claimed mpmath values to about 1e-11. Object sha256 4a2c00fc... matches.
- "not reproduced ... by more than 1e-6": posted cell − polished = 1.4955e-5 > 1e-6. That is about 15 times the threshold, far larger than the numerical error.
- Dictionary (Merriam-Webster, "reproduce": "to produce again"). After polishing, the posted coordinates produce 6191355.686644, not the posted 6191355.686659, so the posted value is not reproduced. Direction does not matter for p1 because Deeter's cited precedents are the same kind of finding.
- "mpmath polishing" stretch: the descent ran in float64 L-BFGS plus MPFR-170-bit Newton, not pure mpmath. The final energy was evaluated in mpmath at 30 digits, and the gradient reached 9.82e-22. Polishing at higher precision does not weaken the finding, so I accept it as meeting the intent and the threshold.
- "both energies to 12 digits": reported (6191355.6866585 cell / 6191355.68665850 raw; 6191355.68664355 polished).
- Null model: maybe the difference is just float noise or a different normalization. Ruled out: renormalizing to the unit sphere and summing in extended precision gives the same result, and the 1.5e-5 gap is well above rounding (~1e-9).
- Subsumption: a narrow claim, limited to table integrity. The polished configuration is the same basin as the posted one, so this is no new structure and no improvement claim. It is not subsumed by any wider claim, and it states no wider claim of its own.

confirmed_scope: For N = 3552, polishing the live CCD Riesz s=1 table's own posted coordinates (points_3552_1.dat) to a stationary point gives energy 6191355.68664355, which is 1.4955e-5 below the posted cell value 6191355.6866585, so the posted energy is not reproduced to within 1e-6 (table-integrity partial win p1 only, same basin, no new configuration).

pass: true
