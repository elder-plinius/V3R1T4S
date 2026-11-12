# REPRODUCE skeptic report: ddmu (2,0) Rayleigh-quotient certificate

context: subagent (fresh context, saw only claim/)

All file names are relative to claim/. My own code and outputs are in ../panel_work_reproduce/.

## Definition quoted (CLAIM.md, written down before opening check_cert.py)

> Hamiltonian (eq. 2), muon-atomic units: H = -(1/2X) Lap_1 - (1/2Y) Lap_2 - (1/2) Lap_3 - 1/r32 - 1/r31 + 1/r21, with X = m_a/m_mu, Y = m_b/m_mu.
> Masses (eq. 14): M_t = 5496.92153573 m_e, m_mu = 206.7682830 m_e, M_d = 3670.48296788 m_e.
> Function i is phi_i + P12 phi_i, phi_i = T_type(x, y) exp(-a X - b Y - c R), where x = r1 - r3 and y = r2 - r3 are the positions of the two nuclei relative to the muon, X = |x|, Y = |y|, R = |x - y|, P12 swaps the two nuclei, and T is a symmetric traceless Cartesian tensor of rank 2: type 0: x x, type 1: x y, type 2: y y, type 3: (x - y)(x - y) (for example T_jk = x_j x_k - delta_jk X^2/3 for type 0). Matrix elements are summed over the tensor components. The trial wavefunction is the sum over i of vector_i times function i.

Claimed value: Rayleigh quotient upper end -0.488708325061607741252510781472877154393258585; comparison value (Table I, ddmu (2,0), N = 3700) -0.4887083249914; required margin 1e-13.

## What I did

1. Source check. Extracted the text of source/arxiv_2503.17389v1.pdf with pdftotext. Eq. (2) reads as quoted. Eq. (14) reads "Mt = 5496.92153573 me , mµ = 206.7682830 me , Md = 3670.48296788 me". Table I, block "ddµ ion; (2, 0)−state", last row: "3700 -0.4887083249914" (previous rows 3400: -0.4887083248687, 3600: -0.4887083249605, so the published column is still dropping by about 3e-11 per 100 functions; a value 7e-11 lower does not contradict it).
2. Object check. cert/basis.txt has header L 2, masses 3670.48296788/206.7682830 twice and 1, charges 1 1 -1, sym 1, N 480, then 480 rows (120 of type 0, 120 of type 1, 240 of type 3); all imaginary parts are exactly 0; all a, b, c are positive (ranges a 0.228..1.101, b 0.121..1.608, c 0.187..3.265), so every function is square integrable. cert/vector.txt has 480 coefficients. My script asserts that the header masses equal the exact rational (3670.48296788/206.7682830) built from the eq. (14) digits I typed from the PDF, muon mass 1.
3. Own matrix elements (../panel_work_reproduce/derive.py, lib.py), derived from the definition only:
   - centre of mass removed: T = -(1/2m1) Lap_x - (1/2m2) Lap_y - (1/2m3)(grad_x + grad_y)^2, V = -1/X - 1/Y + 1/R;
   - kinetic energy in gradient (weak) form; sympy computes, for each of the 16 type pairs, the component-summed integrand as a polynomial in X, Y, R (rotational scalar, reduced on the configuration x = (X,0,0), y in the plane; odd powers of the out-of-line component are asserted absent);
   - every monomial is integrated with Integral d3x d3y X^(p-1) Y^(q-1) R^(r-1) exp(-al X - be Y - ga R) = 16 pi^2 (-d/dal)^p (-d/dbe)^q (-d/dga)^r [1/((al+be)(be+ga)(ga+al))], p, q, r >= 0 (asserted), expanded in closed form; all arithmetic in arb balls from exact rational inputs;
   - type 1 is taken as (x_j y_k + x_k y_j)/2 - delta_jk x.y/3; P12 maps type 0 <-> 2, 1 -> 1, 3 -> 3 and swaps a <-> b; <f_i|O|f_j> = 2(<phi_i|O|phi_j> + <phi_i|O|P12 phi_j>) for equal nuclear masses.
4. Independent validation of those elements (../panel_work_reproduce/validate.py): the Hamiltonian is applied in the strong form in all nine Cartesian coordinates of r1, r2, r3 (second derivatives by sympy, no centre-of-mass reduction, no closed-form integrals), translation/rotation invariance of the integrand is spot-checked, and the six-dimensional integral is done by 24-point Gauss-Laguerre quadrature in perimetric coordinates. 14 primitive pairs from the certificate (direct and exchanged, all type combinations used) plus 3 pairs with unequal masses (7/2, 13/3, 9/5) and charges (2, -3, 5).
5. Full recomputation (../panel_work_reproduce/rq_part.py, combine.py): all 480 x 481 / 2 symmetrised pairs (no sampling), v.Hv and v.Sv accumulated in ball arithmetic, at 1024 bits and again at 2048 bits, 2 processes.
6. Only after that: ran the author's check_cert.py twice and compared with expected_output.txt.

## Commands and outputs

(PY = the venv python with python-flint and sympy; run inside ../panel_work_reproduce/)

`PY derive.py formulas.pkl` (last lines):

    3 2 S terms 6 H terms 57 dens 12 24 maxdeg 7
    3 3 S terms 1 H terms 18 dens 3 3 maxdeg 7

`PY validate.py`:

    direct  i=360 j=365 types 0,0: S quad 1.54811159641062e+02 formula 1.54811159641062e+02 rel 2.2e-15 | H quad 2.78398476110937e+01 formula 2.78398476110936e+01 rel 2.0e-15
    exchg   i=360 Pj=365 types 0,2: S quad 3.58595955441739e+01 formula 3.58595955441739e+01 rel 2.0e-15 | H quad 4.21373517785419e+01 formula 4.21373517785421e+01 rel 4.8e-15
    direct  i=363 j=247 types 0,1: S quad 1.05661675130382e+01 formula 1.05661675130383e+01 rel 2.6e-15 | H quad 1.56340691950178e+01 formula 1.56340691950177e+01 rel 7.5e-15
    exchg   i=363 Pj=247 types 0,1: S quad 1.05788077875110e+01 formula 1.05788077875110e+01 rel 5.6e-16 | H quad 1.56403756137638e+01 formula 1.56403756137637e+01 rel 6.0e-15
    direct  i=242 j=249 types 1,1: S quad 8.90002059574520e+00 formula 8.90002059574522e+00 rel 2.0e-15 | H quad 9.10794330644722e+00 formula 9.10794330644724e+00 rel 1.8e-15
    exchg   i=242 Pj=249 types 1,1: S quad 9.23031479110351e+00 formula 9.23031479110352e+00 rel 1.8e-15 | H quad 9.38656744809392e+00 formula 9.38656744809392e+00 rel 5.6e-16
    direct  i=361 j=4 types 0,3: S quad 1.60492944323902e+00 formula 1.60492944323902e+00 rel 1.3e-15 | H quad -1.63994466178849e+00 formula -1.63994466178849e+00 rel 4.4e-16
    exchg   i=361 Pj=4 types 0,3: S quad 6.01714076235487e+00 formula 6.01714076235488e+00 rel 7.8e-16 | H quad -2.75469873171434e+00 formula -2.75469873171434e+00 rel 1.0e-15
    direct  i=251 j=100 types 1,3: S quad -3.40877076342778e-01 formula -3.40877076342779e-01 rel 3.8e-15 | H quad 1.85765703686840e-01 formula 1.85765703686841e-01 rel 2.6e-15
    exchg   i=251 Pj=100 types 1,3: S quad -3.36530258435065e-01 formula -3.36530258435066e-01 rel 4.1e-15 | H quad 1.81269801982953e-01 formula 1.81269801982953e-01 rel 2.9e-15
    direct  i=0 j=239 types 3,3: S quad 3.04067123236423e+00 formula 3.04067123236423e+00 rel 1.3e-15 | H quad -1.53619741823456e+00 formula -1.53619741823457e+00 rel 1.1e-15
    exchg   i=0 Pj=239 types 3,3: S quad 2.29777300388893e+00 formula 2.29777300388893e+00 rel 2.3e-15 | H quad -1.41056818304989e+00 formula -1.41056818304989e+00 rel 1.8e-15
    direct  i=17 j=420 types 3,0: S quad 2.47496674696577e-02 formula 2.47496674696573e-02 rel 1.6e-14 | H quad -3.53451219804271e-02 formula -3.53451219804279e-02 rel 2.2e-14
    exchg   i=17 Pj=420 types 3,2: S quad 1.03712259116370e-01 formula 1.03712259116370e-01 rel 2.2e-15 | H quad -2.33815363943075e-02 formula -2.33815363943079e-02 rel 1.6e-14
    generic masses/charges types 1,3: S quad -2.50537493982780e-01 formula -2.50537493982781e-01 rel 4.7e-15 | H quad 1.54902708690648e+00 formula 1.54902708690648e+00 rel 5.3e-15
    generic masses/charges types 2,0: S quad 2.18834477712984e+00 formula 2.18834477712984e+00 rel 7.8e-16 | H quad -2.47957521880046e+01 formula -2.47957521880046e+01 rel 8.9e-16
    generic masses/charges types 3,2: S quad 3.10251537888160e-01 formula 3.10251537888160e-01 rel 0.0e+00 | H quad 1.60569236840524e+00 formula 1.60569236840524e+00 rel 1.0e-15
    worst relative deviation 2.2426505097428162e-14
    VALIDATION OK

`PY pcheck.py`:

    P12 invariance <P f|O|P g> = <f|O|g>, <f|O|P g> = <P f|O|g>, and hermiticity on 4 pairs: True

`PY rq_part.py 0 2 1024 & PY rq_part.py 1 2 1024` (and the same with 2048); partial sums printed (identical digits at both precisions):

    part 0 vHv [75129353064324.93257962452665055892601569 +/- 9.09e-28] vSv [-200178023978047.9128070844227394639886356 +/- 4.57e-26]
    part 1 vHv [-75129353064325.42128794958825830017852647 +/- 2.39e-27] vSv [200178023978048.9128070844227394639886356 +/- 4.57e-26]

`PY combine.py 1024`:

    prec 1024 rows 480
    vSv = [1.000000000000000000000000000000000000000 +/- 3e-45]
    vHv = [-0.4887083250616077412525107814728771543933 +/- 4.15e-41]
    Rayleigh quotient = [-0.488708325061607741252510781472877154393258585262238940213760 +/- 4.10e-61]
    upper end         = -0.488708325061607741252510781472877154393258585262238940213760
    claimed upper end - my upper end = [2.622389402e-46 +/- 1.38e-56]
    my RQ <= claimed upper end: True | claimed within 1e-44 of my value: True
    bar - RQ = [7.02077412525107814728771543933e-11 +/- 4.15e-41] | bar - RQ > 1e-13: True | vSv > 0: True
    binding-energy consistency: threshold d-mu(1s) = -mu/2 with mu = Md/(Md+mmu):
      threshold = [-0.4733357126452572741764346 +/- 4.51e-26]  (E - threshold)*5626.451612133 eV = [-86.493259912670858089 +/- 4.84e-19]

`PY combine.py 2048`:

    prec 2048 rows 480
    vSv = [1.000000000000000000000000000000000000000 +/- 3e-45]
    vHv = [-0.4887083250616077412525107814728771543933 +/- 4.15e-41]
    Rayleigh quotient = [-0.488708325061607741252510781472877154393258585262238940213760 +/- 4.10e-61]
    upper end         = -0.488708325061607741252510781472877154393258585262238940213760
    claimed upper end - my upper end = [2.622389402e-46 +/- 1.38e-56]
    my RQ <= claimed upper end: True | claimed within 1e-44 of my value: True
    bar - RQ = [7.02077412525107814728771543933e-11 +/- 4.15e-41] | bar - RQ > 1e-13: True | vSv > 0: True
    binding-energy consistency: threshold d-mu(1s) = -mu/2 with mu = Md/(Md+mmu):
      threshold = [-0.4733357126452572741764346 +/- 4.51e-26]  (E - threshold)*5626.451612133 eV = [-86.493259912670858089 +/- 4.84e-19]

Author's checker, run twice from an empty folder: `PY check_cert.py cert/basis.txt cert/vector.txt --bar -0.4887083249914 --margin 1e-13 --procs 2`:

    basis cert/basis.txt L 2 N 480 sym 1 masses 3670.48296788/206.7682830 3670.48296788/206.7682830 1 complex False prec 320
    Rayleigh quotient (upper bound on the lowest root of the block)
    enclosure: [-0.48870832506160774125251078147287715439325858526224 +/- 1.06e-51]
    upper end: -0.488708325061607741252510781472877154393258585
    bar -0.4887083249914 margin 1e-13 bar - upper end = [7.0207741252510781473e-11 +/- 1.24e-31]
    CERTIFIED: upper end < bar - margin
    exit status 0

Both runs byte-identical; after removing the path prefix the output is identical to expected_output.txt (diff empty).

## Findings

- Value: my independently derived Rayleigh quotient is -0.488708325061607741252510781472877154393258585262238940213760 (60 digits shown, same at 1024 and 2048 bits). The claimed upper end -0.488708325061607741252510781472877154393258585 lies 2.62e-46 above it, i.e. it is a correct outward rounding. Agreement with the author's enclosure to all 50 printed digits.
- Comparison: Table I value -0.4887083249914 minus my value = 7.0208e-11 > 1e-13. Margin satisfied by a factor of about 700.
- Masses: header masses equal the exact eq. (14) ratio M_d/m_mu for both nuclei, muon mass 1, charges (1, 1, -1) (asserted in rq_part.py).
- Symmetry: each function is a symmetric traceless rank-2 tensor built from the polar vectors x, y times a function of X, Y, R only, hence L = 2 and parity +1 = (-1)^L (natural). It is phi + P12 phi, hence symmetric under d <-> d. The component-summed matrix elements are the sum over the five M components of a scalar operator, each M giving the same value, so the ratio is the Rayleigh quotient of a genuine L = 2 function. P12 invariance and hermiticity of my elements confirmed numerically (pcheck).
- Logic: v.Sv = 1 > 0 so the vector is a nonzero function in the span; by Rayleigh-Ritz, lowest root of the 480-function block <= Rayleigh quotient < bar - 1e-13, and the lowest root is itself an upper bound on the lowest L = 2 natural-parity exchange-symmetric level. The certificate bounds the root from above only, which is all the p1 criterion needs.
- Validation: worst relative deviation between my closed-form elements and the nine-coordinate quadrature is 2.2e-14 (double-precision quadrature), including unequal-mass and odd-charge cases that exercise each kinetic and potential term separately.
- Consistency: (E - E_threshold) x 5626.451612133 eV with E_threshold = -M_d/(2(M_d + m_mu)) gives a binding energy of 86.4933 eV, the right size for the ddmu (2,0) state.
- Determinism: my result identical at two precisions; author's checker identical in two runs and equal to expected_output.txt.
- Not checked by me: whether a lower published value at identical masses exists elsewhere (I saw only claim/; source/scout_table_record.md reports none). The comparison here is with Table I of the saved PDF only.

No mismatch, no missing object, no non-determinism found.

pass: true
