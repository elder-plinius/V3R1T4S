context: subagent (executor)

# REPRODUCE skeptic — claim B (N = 3552, Riesz s=1, partial win p1)

Definition (criterion.txt, verbatim):
> p1: A table-integrity finding: an N where a live table's posted energy is not reproduced by its own posted coordinates after mpmath polishing by more than 1e-6 (Deeter documents such cases for CCD N = 263, 377, 380, 381), reported with both energies to 12 digits.

Own checker written before reading verify/ (author code not used): mpmath dps 40 (gmpy backend), each point normalized to the unit sphere, E = sum_{i<j} 1/|x_i - x_j| over all 6,306,576 pairs (exhaustive, no sampling, 8-way split by row index, summed exactly in mpmath); Euclidean gradient accumulated per point, projected onto each point's tangent plane, reported as the 2-norm.

Results:
- sha256 riesz_3552_polished.txt = 4a2c00fc...e2ad52, data/points_3552_1.dat = 837f6c84...55bcb0: match claim.md.
- Posted file data/points_3552_1.dat (3552 pts): E = 6191355.686658502748579249, tangent grad 2-norm 0.292 (not a stationary point at high precision). Matches claimed value to all 25 digits.
- Polished object (3552 pts): E = 6191355.686643545416998382, tangent grad 2-norm 9.82e-22 (< 1e-20). Matches claimed value and claimed grad to all digits.
- Posted cell from data/ccd_riesz_s1.html, row `<TR><TD>3552</TD><TD>6191355.6866585</TD>` (line 556-557): 6191355.6866585. Matches.
- Same basin: identity correspondence, max per-point displacement 5.67e-5 (rms 1.22e-5) versus minimum nearest-neighbour distance 0.0574 in the posted file; the polished object is a tiny relaxation of the posted configuration, no permutation or structural change.
- Gaps: posted raw − polished = 1.4957332e-5; posted cell − polished = 1.4954583e-5. Both > 1e-6.
- 12-digit report: posted 6191355.68666 (cell 6191355.6866585), polished 6191355.68664.
- Determinism: both energies reproduced bit-for-bit vs the claim's dps-30 values; independent runs.

Not re-run: the author's polish routine itself (only its saved output was verified, which suffices for p1: the stationary point exists in the posted basin, below the posted value). Hessian/ARPACK check optional, not needed for p1.

pass: true
