# CRITERION skeptic: run 2026-11-22-1906, partial win p1

context: subagent (fresh context)

Inputs read: claim/CLAIM.md, claim/PROOF.md, claim/REPRODUCE.md, claim/target.md, claim/status_record.md,
claim/code/certify.py, claim/code/lemmas.py, claim/code/ic.py, claim/code/vt3b.py (integrate and a priori enclosure parts),
claim/output/certify_row2.txt, the row-2 entries of claim/data/ics_971_100_num.txt and claim/data/res_eig_angles.txt.
`shasum -a 256 -c SHA256SUMS` passes for every listed file. I did not re-run the 20-minute certificate; a
reproduction skeptic covers that. My verdict depends on the logged output in claim/output/certify_row2.txt.

## Which criterion is claimed
Only p1 is claimed: "A computer-assisted proof of existence and linear stability (certified ellipticity of the reduced
monodromy) for one listed solution other than the figure-eight, with no prior rigorous linear-stability proof found by
a literature search." The full criterion (KAM: non-resonance and twist) is explicitly not claimed, and the CLAIM
sentence doesn't hint at KAM or nonlinear stability. p2 (one orbit per region) is not claimed. Good.

## Clause by clause

1. **"listed solution other than the figure-eight".** Row 2 of claim/data/ics_971_100_num.txt (vx 0.46444517..., vy
   0.39606001..., T 14.8943...). Row 1 is the figure-eight (T 6.3259). Row 2 is a different orbit and is in the list.
   The certified box is centred on the listed 100-digit values. Met.
   Note: these values match the Moth I orbit of Suvakov and Dmitrasinovic (2013: 0.464445, 0.396060, T 14.893925).
   CLAIM.md does not name it that way (it says "first orbit of the Intermediate-Moth region").

2. **Existence.** G(vx, vy, t) = (x2, y2, (v1 - v3).q1) at t = T/2. The Krawczyk check K(X) in int X passes with
   dev/r of about 1e-9 to 1e-10 in all three components. This proves a unique zero (vx*, vy*, t*) in the box. The
   argument from a zero of G to periodicity is correct. G = 0 together with exactly conserved P = COM = L = 0 and
   q1 != 0 puts x(t*) in Fix(S). S is a reversor (checked symbolically in code/lemmas.py L1 to L3), so
   phi_{2t*}(x0) = x0. The orbit is periodic with period T* = 2t*, where |T* - T_listed| <= 2e-55 (plus a negligible
   string-to-ball rounding radius). The claim does not assert that this period is the minimal one, and p1 doesn't
   need that.
   Collision-free: every integration step needs a complex Picard inclusion with Re(r_ij^2) > 0 on the a priori box
   (code/vt3b.py raises otherwise). This also gives q1 = q1 - q2 != 0 at the end. Met.
   The phrase "within 1e-55" is literal up to the radius of the arb conversion of the listed strings, which is about
   1e-115. That is immaterial.

3. **Linear stability = certified ellipticity of the reduced monodromy.**
   - Monodromy: M = S A^-1 S A, with A = D phi_{t}(x0) enclosed over the whole box, including the end-time interval.
     A^-1 = -J A^T J holds exactly for the true symplectic A, so the enclosure contains the true M. The derivation
     from reversibility is correct (D phi_t at S-fixed x(t) is S A^-1 S).
   - Removal of the trivial multipliers is structural, not a tolerance check. That is the key point for "reduced". U =
     span(e, b, f, Rx0) has certified dimension 6 (a 6x6 minor, -1.393 +/- 5e-10, which excludes 0). The z_j are
     COM-free vectors corrected so that dH = dL = 0, so they lie in U^omega exactly by construction. The basis [z1..z4,
     f, Rx0, e, b, g1, g2] is certified non-singular, because the ball solve succeeds. The true M leaves U^omega
     invariant, so the true coordinates of M z_j outside the first six are exactly 0 (and the logged enclosures do
     contain 0). The 4x4 block therefore encloses the map induced on U^omega / span(f, Rx0). Since span(f, Rx0) =
     U intersect U^omega, this is the standard symplectic reduced monodromy, so its true characteristic polynomial is
     palindromic.
   - Ellipticity and distinctness: with s = lambda + 1/lambda, disc = 9.4833 +/- 2e-10 > 0, s1 = -1.99739841527964462
     +/- 2e-20 and s2 = 1.08210576724262252 +/- 2e-21. Both are strictly inside (-2, 2), and this is certified
     separately using a3 and using a1. So the four non-trivial multipliers are e^{+-i theta1} and e^{+-i theta2}, all
     on the unit circle, pairwise distinct, and none equal to +-1. s1 sits only 2.6e-3 from -2 (the multiplier is near
     -1), but the margin is 17 orders larger than the enclosure radius.
   - The 12x12 route (charpoly divided by (lambda-1)^8) independently agrees. The frequencies 0.159012938903764250810406
     and 0.491881305365955760282366 match the source's 40-digit stability angles. Met.

4. **"No prior rigorous linear-stability proof found by a literature search."** claim/status_record.md records the
   search. The only rigorous results found are Kapela-Simo for the figure-eight and two rotating eights (not
   zero-angular-momentum list members other than row 1). I ran one extra web search under the orbit's other name
   (Suvakov-Dmitrasinovic "moth"). It found no rigorous stability or existence proof, only the same Kapela-Simo
   papers. Residual risk: the claimant's search was keyed to the 971-list and may not have searched for "Moth I"
   specifically. Literature on Moth I that I know of (Suvakov-Dmitrasinovic 2013; Dmitrasinovic et al. 2018) is
   numerical. I would recommend searching "Moth I" by name before the claim is published. This does not block p1.

## Stretched definitions / hidden quantifiers checked
- "Existence" means an isolated zero in a 1e-55 box. It is not existence for every listed digit; the claim wording
  matches this. Fine.
- "Period" means 2t*, not necessarily the minimal period. The claim says "period", not "minimal period". Fine.
- "Distinct" means the four non-trivial multipliers are distinct. It doesn't say they are distinct from the
  eight trivial multipliers at 1; s in (-2,2) strictly does give that. Fine.
- Not claimed and not shown: non-resonance, twist, KAM or nonlinear stability, other rows, other regions.

## Null models / controls
REPRODUCE.md names a known positive (row 1, the figure-eight, which should pass) and a known negative (row 2 with vx
shifted by 1e-6, which should fail C1). Their outputs are not included in claim/output/, so I could not confirm them
from the package. Only the row-2 run is logged. The source-frequency match is a further internal consistency check.
This is a gap in evidence for the reproduction skeptic. It does not affect whether the logged certificate meets p1.

## Verdict
The logged certificate meets p1 literally. The orbit is a listed non-figure-eight solution, existence is proved by
Krawczyk plus reversibility, and the orbit is collision-free. The reduced monodromy is obtained by an exact structural
quotient and is certified elliptic with distinct multipliers. The literature search found no prior rigorous result.
Nothing broader than this is claimed. The win is not subsumed by the figure-eight or rotating-eight results.

confirmed_scope: For row 2 of the Hristov-Hristova-Tanikawa 971-orbit list (T about 14.8943), outward-rounded ball arithmetic plus a Krawczyk test and a reversibility argument proves that a collision-free periodic orbit of the planar equal-mass zero-angular-momentum three-body problem exists, with Euler half-twist data within 1e-55 of the listed (vx, vy) and period 2t* within 2e-55 of the listed T; it also proves that the four non-trivial multipliers of its reduced monodromy are distinct and lie on the unit circle (linear stability only; no KAM, non-resonance or twist result).
pass: true
