# Reproduce skeptic report: ttmu (2,0) cell, partial win p1

context: subagent (fresh context, saw only claim/)

All file names below are relative to claim/. My own code and outputs are in ../panel_work_reproduce/.

## Definition (quoted from CLAIM.md before any author code was read)

> Hamiltonian (eq. 2), muon-atomic units: H = -(1/2X) Lap_1 - (1/2Y) Lap_2 - (1/2) Lap_3 - 1/r32 - 1/r31 + 1/r21, with X = m_a/m_mu, Y = m_b/m_mu.
> Masses (eq. 14): M_t = 5496.92153573 m_e, m_mu = 206.7682830 m_e, M_d = 3670.48296788 m_e.
> Function i is phi_i + P12 phi_i, phi_i = T_type(x, y) exp(-a X - b Y - c R), where x = r1 - r3 and y = r2 - r3 are the positions of the two nuclei relative to the muon, X = |x|, Y = |y|, R = |x - y|, P12 swaps the two nuclei, and T is a symmetric traceless Cartesian tensor of rank 2: type 0: x x, type 1: x y, type 2: y y, type 3: (x - y)(x - y) (for example T_jk = x_j x_k - delta_jk X^2/3 for type 0). Matrix elements are summed over the tensor components. The trial wavefunction is the sum over i of vector_i times function i.

Claimed: Rayleigh quotient enclosure with upper end -0.512568647969898220243439490627127512105327902 (rounded to 45 digits), strictly lower than Frolov's Table I value -0.5125686450010 by more than 1e-13.

## What I did

1. Read source/arxiv_2503.17389v1.pdf (pdftotext). Eq. (2) is the Hamiltonian quoted above; eq. (14) gives
   Mt = 5496.92153573 me, mµ = 206.7682830 me; Table I, column "ttµ ion; (2,0)-state", last row: N = 3800, -0.5125686450010.
   These agree with CLAIM.md. The masses line of cert/basis.txt is `5496.92153573/206.7682830 5496.92153573/206.7682830 1`, charges `1 1 -1`.
2. Wrote my own matrix elements from the definition, before opening check_cert.py (../panel_work_reproduce/derive.py):
   - centre of mass removed with grad_1 = grad_x, grad_2 = grad_y, grad_3 = -grad_x - grad_y, so
     K = -(1/2)(1/M1 + 1) Lap_x - (1/2)(1/M2 + 1) Lap_y - grad_x.grad_y, V = -1/X - 1/Y + 1/R;
   - tensors T(x,x), T(x,y), T(y,y) are harmonic and have zero mixed Laplacian, so H(T g) = T (K+V) g + gradient cross terms that stay in the span of the three tensors; type 3 = T(x,x) - 2 T(x,y) + T(y,y);
   - tensor contraction T(u,v):T(u',v') = [(u.u')(v.v') + (u.v')(v.u')]/2 - (u.v)(u'.v')/3, with x.y = (X^2+Y^2-R^2)/2;
   - integration with measure X Y R dX dY dR, perimetric substitution X = u+v, Y = u+w, R = v+w, and
     int u^i v^j w^k exp(-pu-qv-rw) = i! j! k! / (p^(i+1) q^(j+1) r^(k+1)); sympy expands each of the 16 type pairs into integer-coefficient polynomials (generated file gen_elems.py);
   - P12 phi(type, a, b, c) = phi(swapped type 0<->2, b, a, c); with M1 = M2, <psi_i|H|psi_j> = 2(<phi_i|H|phi_j> + <phi_i|H|P12 phi_j>).
3. Validated these elements independently (../panel_work_reproduce/validate.py): the nine-coordinate Hamiltonian of eq. (2) (three Cartesian Laplacians with masses M1, M2, 1 plus the three Coulomb terms) is applied symbolically by sympy to the explicit Cartesian functions of r1, r2, r3 (P12 done by literally swapping r1 and r2), and the contracted integrand is integrated by 6x6x6 Gauss-Laguerre quadrature in perimetric coordinates (exact for these polynomial-times-exponential integrands) at an arbitrary rotation and translation of the triangle, 40 digits. 18 basis-function pairs (i, j), each with all four P12 terms, covering every one of the 12 type-pair routines that the certificate uses.
4. Recomputed v.Hv / v.Sv over ALL 480 x 480 pairs (upper triangle, weights 2) in arb ball arithmetic at 320, 384 and 512 bits (../panel_work_reproduce/rq.py, final.py); repeated the 384-bit run for determinism.
5. Checked the files: N, types, exponents, vector length, hermiticity of my elements (H on ket vs H on bra).
6. Only afterwards ran the author's check_cert.py and compared with expected_output.txt.

## Commands and real outputs

`python derive.py` -> `maxdeg 7`

`python validate.py` (two batches; columns: pair, types, quadrature value, my value, relative errors):

```
pair 0 0 types 3 3 H_quad -0.0008165209152607369565311232 H_mine -0.0008165209152607369565311232 relerr H 2.3e-41 relerr S 2.3e-41
pair 0 7 types 3 3 H_quad -0.00008670024809520567422642863 H_mine -0.00008670024809520567422642863 relerr H 1.38e-40 relerr S 2.3e-41
pair 7 0 types 3 3 H_quad -0.00008670024809520567422642863 H_mine -0.00008670024809520567422642863 relerr H 0.0 relerr S 3.44e-41
pair 7 130 types 3 3 H_quad 0.0001424984781656378594226758 H_mine 0.0001424984781656378594226758 relerr H 2.3e-41 relerr S 0.0
pair 130 7 types 3 3 H_quad 0.0001424984781656378594226758 H_mine 0.0001424984781656378594226758 relerr H 6.89e-41 relerr S 0.0
pair 130 200 types 3 3 H_quad -0.0009981943644331058754883892 H_mine -0.0009981943644331058754883892 relerr H 0.0 relerr S 3.44e-41
pair 250 3 types 1 3 H_quad 0.0001084557754798552313886033 H_mine 0.0001084557754798552313886033 relerr H 2.78e-39 relerr S 1.03e-40
pair 3 250 types 3 1 H_quad 0.0001084557754798552313886033 H_mine 0.0001084557754798552313886033 relerr H 4.18e-39 relerr S 1.03e-40
pair 479 300 types 0 1 H_quad 0.4171437162240748018607321 H_mine 0.4171437162240748018607321 relerr H 0.0 relerr S 4.59e-41
pair 125 125 types 3 3 H_quad -0.0005605819006148990964551109 H_mine -0.0005605819006148990964551109 relerr H 6.89e-41 relerr S 6.89e-41
pair 1 2 types 3 3 H_quad -0.00152918406812333225832096 H_mine -0.00152918406812333225832096 relerr H 3.44e-41 relerr S 4.59e-41
pair 200 479 types 3 0 H_quad -0.01646504594546439611933264 H_mine -0.01646504594546439611933264 relerr H 4.59e-41 relerr S 6.89e-41
worst relative error 4.18e-39
pair 400 410 types 0 0 H_quad 0.03786115928600645570475216 H_mine 0.03786115928600645570475216 relerr H 1.61e-40 relerr S 3.44e-41
pair 250 260 types 1 1 H_quad 0.4528781785219726494596642 H_mine 0.4528781785219726494596642 relerr H 7.81e-40 relerr S 3.44e-41
pair 300 400 types 1 0 H_quad 0.7552119599587565044885286 H_mine 0.7552119599587565044885286 relerr H 2.76e-40 relerr S 0.0
pair 400 100 types 0 3 H_quad -0.008458512099127561142429903 H_mine -0.008458512099127561142429903 relerr H 2.3e-41 relerr S 2.3e-41
pair 260 470 types 1 0 H_quad 1.476950331437676801376376 H_mine 1.476950331437676801376376 relerr H 4.59e-41 relerr S 1.15e-41
pair 100 300 types 3 1 H_quad 0.003167326650177816426164458 H_mine 0.003167326650177816426164458 relerr H 7.81e-40 relerr S 4.59e-41
worst relative error 7.81e-40
```

`python checks.py`:

```
header {'L': '2', 'prec': '512', 'masses': '5496.92153573/206.7682830 5496.92153573/206.7682830 1', 'charges': '1 1 -1', 'sym': '1', 'N': '480'}
masses strings equal eq.(14) quotient: True
M_t/m_mu = [26.5849358323974668784186789422 +/- 3.37e-29]
N funcs 480 N vec 480
all imaginary parts zero: True
types present: [0, 1, 3]
min pairwise exponent sum (must be > 0): 0.6813050570786161
min a, b, c: 0.22008124284427566 0.12956045028773366 0.5751615396081345
distinct basis lines: 480
vector all finite nonzero entries: 480 max |v| 5731273.281556021
t-mu threshold -mu/2 = [-0.48187416483264866415 +/- 2.02e-21]  E below threshold: True
binding energy (E + mu/2) * 5626.451612133 eV = [-172.701024131167 +/- 5.17e-14]
Frolov value binding, same formula = [-172.701007426805 +/- 2.30e-13]
```

`python final.py 320; python final.py 384; python final.py 512` (all 480 x 480 pairs, my elements):

```
prec 320 RQ mid -0.5125686479698982202434394906271275121053279016764581442433562791095446 rad 2.0456e-81
  vSv rad 1.3166e-81 vSv > 0: True
  overlaps claimed enclosure [-0.51256864796989822024343949062712751210532790167646 +/- 1.86e-51]: True
  |my mid - claimed mid| upper bound 1.8558e-51
  45-digit claimed "upper end" minus my upper end: [-3.2354186e-46 +/- 4.25e-54]
  my upper end < bar - 1e-13: True  bar - upper end = [2.96889822024343949062712751211e-9 +/- 4.68e-39]
prec 384 RQ mid -0.5125686479698982202434394906271275121053279016764581442433562791095446 rad 1.0994e-100
  vSv rad 7.0796e-101 vSv > 0: True
  overlaps claimed enclosure [-0.51256864796989822024343949062712751210532790167646 +/- 1.86e-51]: True
  |my mid - claimed mid| upper bound 1.8558e-51
  45-digit claimed "upper end" minus my upper end: [-3.2354186e-46 +/- 4.25e-54]
  my upper end < bar - 1e-13: True  bar - upper end = [2.96889822024343949062712751211e-9 +/- 4.68e-39]
  hermiticity (H on ket vs H on bra), 300 random pairs, worst relative difference upper bound: 3.976157306513943e-111
prec 512 RQ mid -0.5125686479698982202434394906271275121053279016764581442433562791095446 rad 3.2446e-139
  vSv rad 2.0927e-139 vSv > 0: True
  overlaps claimed enclosure [-0.51256864796989822024343949062712751210532790167646 +/- 1.86e-51]: True
  |my mid - claimed mid| upper bound 1.8558e-51
  45-digit claimed "upper end" minus my upper end: [-3.2354186e-46 +/- 4.25e-54]
  my upper end < bar - 1e-13: True  bar - upper end = [2.96889822024343949062712751211e-9 +/- 4.68e-39]
```

`python rq.py 384` run twice, outputs compared with cmp (timing line excluded): `DETERMINISTIC_384_IDENTICAL`. One run takes about 11 s on 3 processes.

Author's checker, run last: `python check_cert.py cert/basis.txt cert/vector.txt --bar -0.5125686450010 --margin 1e-13 --procs 2`

```
enclosure: [-0.51256864796989822024343949062712751210532790167646 +/- 1.86e-51]
upper end (rounded to 45 digits): -0.512568647969898220243439490627127512105327902
bar -0.5125686450010 margin 1e-13 bar - upper end = [2.9688982202434394906e-9 +/- 2.72e-29]
CERTIFIED: upper end < bar - margin
exit status 0
```

diff against expected_output.txt (path prefix aside): identical (`AUTHOR_OUTPUT_MATCHES_EXPECTED`).

sha256: cert/basis.txt 2e9f66fb6bcf8bc2f25dbec1de05659ac3f9b8c404fbaa6d984928d811cebe87, cert/vector.txt b4fcb8160b75f3ae4e8f25e6a1da9b62bc3fc4e4a050100d5219d848c7381230, source/arxiv_2503.17389v1.pdf 6d35b4b6876974670174af39b2592c06479278708802f4143c0d70ad2e2ef81f (the PDF hash equals the one recorded in source/scout_table_record.md).

## Property checks and proof steps

- Masses: the basis header carries exactly the eq. (14) quotient M_t/m_mu for both nuclei and 1 for the muon; my computation uses the ball of that quotient. Charges (+1, +1, -1) are the potential -1/X - 1/Y + 1/R of eq. (2).
- L = 2, natural parity: every function is a rank-2 symmetric traceless Cartesian tensor built from the polar vectors x, y, times a rotation-invariant scalar; that is a pure L = 2 object with parity (+1) = (-1)^2. Summing matrix elements over tensor components equals summing over M, which is common to H and S.
- Exchange symmetry: each function is phi + P12 phi, so it is symmetric under exchange of the two tritons; my quadrature check applied P12 by literally swapping r1 and r2 in the Cartesian function.
- Integrability: all exponents are real, min pairwise sum 0.68 > 0, so all integrals converge; 480 distinct functions; vSv > 0 is certified by the ball, so the trial function is nonzero.
- Logic: S is a Gram matrix and v.Sv > 0, hence v.Hv / v.Sv >= lowest root of the generalized eigenproblem of the block, which by the variational principle is >= the lowest L = 2, natural-parity, exchange-symmetric level. So the lowest root of the block is <= -0.5125686479698982..., which is below the bar -0.5125686450010 by 2.9689e-9 > 1e-13. The certificate certifies an upper bound on the lowest root (not the root itself); for the "strictly lower" direction this is sufficient.
- Comparison value: Table I of the PDF, ttmu (2,0), N = 3800: -0.5125686450010, as claimed.

## Remarks (not failures)

- The 45-digit number printed as "upper end" in CLAIM.md is rounded to nearest, which for this negative number moves it 3.2e-46 below the true quotient; it is therefore the quotient rounded to 45 digits, not strictly an upper bound at the 46th digit. CLAIM.md labels it as rounded, my value agrees with it to all 45 digits, and the margin in question is 1e-13, so this has no effect.
- I checked what the claim states (the Rayleigh quotient of the saved vector). I did not compute the lowest generalized eigenvalue itself, and I did not search the literature for other published values at these masses; neither is part of the reproduce check.
- The quadrature validation is a spot check of my formulas (18 pairs, every type-pair routine used); the Rayleigh quotient itself was recomputed exhaustively over all pairs.

pass: true
