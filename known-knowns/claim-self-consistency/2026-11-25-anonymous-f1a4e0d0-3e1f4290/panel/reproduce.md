# REPRODUCE skeptic report: claim-self-consistency (White 2011 warp-field interferometer energy)

context: subagent (fresh, Claude Code Agent tool)

Scope: I read only files under claim/. My scratch code and outputs are in ../panel_work/reproduce/ (relative to claim/).
I wrote my checker (../panel_work/reproduce/my_check.py) from the definition below *before* reading code/.

## Definition quoted (source/20110015936.txt, section "Alcubierre Metric"; pdftotext glyphs normalised)

- Eq. (1): "ds^2 = -c^2 dt^2 + [dx - v_s(t) f(r_s) dt]^2 + dy^2 + dz^2" -- "vs is defined as the velocity of the
  spacecraft's moving frame, dxs/dt, and rs is the radial position in the commoving spherical space around the
  spacecraft's origin."
- f(r_s) = [tanh(sigma(r_s + R)) - tanh(sigma(r_s - R))] / (2 tanh(sigma R)); "The parameters σ and R ... control the
  wall thickness and radius of the warp bubble respectively."
- Eq. (3): T00 = -(1/8π) (v_s^2 ρ^2 / (4 r_s^2)) (df/dr_s)^2.
- "phi = 1/2 ln|1 - v_s^2 f(r_s)^2| and trivially, gamma = cosh(1/2 ln|1 - v_s^2 f(r_s)^2|)".
- Operating point (paper): "a 1cm diameter toroidal test article (something as simple as a very high-voltage capacitor
  ring) with a boost on the order of 1.0000001". Slide 21 (source/slide21_pdfpage31_ocr.txt): "a1 cm diameter
  toroidal-ring of positive energy density"; "necessary boost field is on the order of 1.0000001 to 1.0000002";
  "From a purely Special Relativistic perspective, this equates to a velocity of ~ 0.0004c".

## My own numbers (copied from ../panel_work/reproduce/my_check_output.txt and jstar_check_output.txt; mpmath, 25-40 digits)

```
Step1: max |f(0)-1|, |f(R)-1/(1+tanh^2 sR)| over 11 sR values: 1.1479e-41
Step1: rel err analytic f' vs mp.diff (max over grid): 6.5e-25  grid points with f outside [0,1]: 0
Step2: u* (root of source gamma = 1+1e-7) = 0.029900289342802633
Step2: closed form (2-u^2)/(2sqrt(1-u^2)) - source gamma at u*: 0.0
Step2: source gamma strictly increasing on u in [0,0.999] (1000-pt grid): True
aside: Lorentz 1/sqrt(1-0.0004^2) - 1 = 8.0e-8  source gamma(u=0.0004)-1 = 3.2e-15
Step3: int sin^2(theta) dOmega = 8.3775804095727819692  8pi/3 = 8.3775804095727819692
Step5: bound -(c^4/48G) u*^2 R = -1.12708491444e+37 J ; mass eq -1.2540511e+20 kg
Step6: slide 0.0004c bound = -2.01709260723e+33 J ; mass eq -2.2443182e+16 kg
sR, I/R, f(R)^2, E(u*) [1D], E(u*) [2D literal Eq3], E/bound
0.01 43.86721074 0.99980004 -1.977682859e+39 - 175.46884
0.1 4.409531065 0.98042474 -1.987966377e+38 - 17.638124
0.5 0.9945427666 0.67902072 -4.483736596e+37 -4.483736596e+37 rel 2.58e-26 3.9781711
1 0.6845905951 0.40056382 -3.086366929e+37 -3.086366929e+37 rel -1.29e-26 2.7383624
2 0.7724282599 0.26864473 -3.482368957e+37 -3.482368957e+37 rel -1.29e-26 3.089713
5 1.688470959 0.2500454 -7.612200583e+37 -7.612200583e+37 rel 0.0 6.7538838
20 6.672041117 0.25 -3.007982757e+38 - 26.688164
100 33.33440822 0.25 -1.502828346e+39 - 133.33763
min: sR* = 1.22904957  J* = 0.667476930928  E_min(u*) = -3.0092127183e+37 J  E_min/bound = 2.66990772
min: E_min(0.0004c) = -5.3854511315e+33 J
stationary sR* 1.22904956958192 J* 0.66747693092844554602 E_min -3.0092127183485e+37   (jstar_check, dps 40)
Step7: E(beta=0, sR=1) = 0.0
```

(The "2D literal Eq3" column integrates Eq. (3) over (r, theta) with rho = r sin(theta), without using the 8π/3
shortcut. The sigma sweep is only a spot check; the bound "for every sigma > 0" rests on the analytic Steps 1-5 below,
which I re-derived.)

## Proof steps (PROOF.md) and re-derivation

| Step | Statement | Re-derived? |
|---|---|---|
| 1 | f(0)=1, f(R)=1/(1+tanh^2 sR) >= 1/2, f -> 0, f continuous | Yes. tanh(2x)=2tanh x/(1+tanh^2 x) gives f(R); strict > 1/2 holds for finite sR (numerically equal to 1/2 at sR=1000 only to working precision). Numerically confirmed to 1e-41. |
| 2 | max gamma >= g iff v >= u*; gamma = (2-u^2)/(2 sqrt(1-u^2)) for u<1, strictly increasing | Yes. cosh(½ ln w) = (w^½ + w^-½)/2, decreasing in w on (0,1]. 0 <= f <= 1 on r >= 0 (derivative sech^2(s(r+R)) - sech^2(s(r-R)) <= 0 since |r+R| >= |r-R|) and IVT give both directions; u >= 1 cases imply v >= 1 > u*. u* = 0.029900289342802633 matches CLAIM to all quoted digits. |
| 3 | E = ∫Eq.(3) dV over flat slice = -(c^4/(12G)) beta^2 I, I = ∫ f'^2 r^2 dr | Yes. t=const slice of Eq. (1) is dx^2+dy^2+dz^2; ∫ sin^2θ dΩ = 8π/3; (1/8π)(1/4)(8π/3) = 1/12; c^4/G converts m^-2 to J/m^3. Confirmed by literal 2D integration to 1e-26. |
| 4 | I >= R f(R)^2 >= R/4 | Yes. f(a) = ∫_a^∞ (-f') dr <= (∫ f'^2 r^2)^½ (∫_a^∞ r^-2)^½ (Cauchy-Schwarz), so I >= a f(a)^2; a = R, f(R) >= 1/2. Numerically asserted at all 8 sR values. |
| 5 | max gamma >= 1+1e-7 implies E <= -(c^4/(48G)) u*^2 R | Yes (Steps 2-4). |
| 6 | -1.127084914e37 J (-1.25405e20 kg); 0.0004c: -2.017092607e33 J (-2.24432e16 kg); true min ~2.7x | Yes: -1.12708491444e37 J, -1.2540511e20 kg; -2.01709260723e33 J, -2.2443182e16 kg; E_min/bound = 2.66990772. |
| 7 | T00 <= 0 everywhere; E < 0 strictly for v > 0 | Yes: -(1/8π) × product of squares; f' is continuous and not identically 0 since f goes from 1 to 0. |

## Author's commands (REPRODUCE.md)

`python3 code/check_bound.py` and `python3 code/eval3d.py`, each run twice (with nice): all four outputs are
byte-identical to result/check_bound_output.txt and result/eval3d_output.txt (diff empty). Deterministic. eval3d prints
the overflow / IntegrationWarning messages that REPRODUCE.md predicts. Every line in result/check_bound_output.txt
matches my independent table digit for digit (u*, bound, all 8 E(sigma) values and ratios, both beta readings).

## Mismatches / notes

1. Minor numerical mismatch in a supporting value (not the claimed value): result/values.json and
   result/eval3d_output.txt give least |E| over sigma at u* as -3.0092127195e37 J; my value (two independent
   computations, 25 and 40 digits) is -3.0092127183485e37 J (relative difference 3.8e-10). Cause, found after reading
   code/eval3d.py: it uses scipy brentq's u* = 0.029900289348511896, which is ill-conditioned in double precision
   (gamma - 1 ~ u^4/8) and off by 5.7e-12 (the script prints this diff itself); E ∝ u*^2 gives 3.8e-10. The slide
   0.0004c E_min (-5.3854511315e33 J) and sR* (1.22904955 vs my 1.2290495696) agree, as does E_min/bound = 2.66990772.
   This does not affect the claimed bound, the inequality E_min <= bound, or any proof step.
2. Premise notes (not errors): R = 5 mm takes the "1cm diameter" as the bubble diameter; this is stated in CLAIM.md.
   The secondary 0.0004c reading is the slide's Lorentz-gamma speed (1/sqrt(1-0.0004^2) - 1 = 8e-8); under the
   source's own gamma formula, v = 0.0004 gives boost only 1 + 3.2e-15. CLAIM.md correctly labels it "on a different
   premise"; its arithmetic is correct.
3. "Energy" is the integral of Eq. (3) over the flat slice (not an ADM mass), as CLAIM.md states.

No missing objects; no non-determinism. The claimed value (E <= -1.127e37 J, -1.254e20 kg, for every sigma > 0) and
the sign statement are confirmed analytically and numerically. The only discrepancy is the last ~2 digits of an
auxiliary, non-claimed minimum value.

pass: true
