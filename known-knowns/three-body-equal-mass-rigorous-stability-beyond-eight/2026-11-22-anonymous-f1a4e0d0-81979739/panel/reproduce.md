# REPRODUCE skeptic report: row 2 (Intermediate-Moth, T = 14.8943...), claim p1

context: subagent (fresh context)

Scope: only the claim package (claim/). My own scripts and outputs are in panel_work/reproduce/ (check_A.py,
own_lemmas.py, own_numeric.py and their *_out.txt files, rerun_row2.txt, claim_lemmas_out.txt).

## Definition checked against
From target.md, quoting the source paper (Sect. 4): "elliptical stability, i.e. when the four eigenvalues that
determine the stability are two complex conjugate pairs on the unit circle". Bank criterion p1 asks for existence plus
"certified ellipticity of the reduced monodromy", and the full criterion says the nontrivial multipliers must be
"certified on the unit circle and distinct". The orbit must be near the listed initial condition of a listed row other
than the figure-eight. Row 2 (data/ics_971_100_num.txt) is not the figure-eight, which is row 1.

## 1. Package integrity and determinism
- `shasum -a 256 -c SHA256SUMS`: all 9 files OK.
- I reran the certificate on a copy: `nice python3 certify.py 2 55 0 448 96 384 72` (about 1266 s). The result is
  `CERT ROW 2: PASS`. Apart from wall-clock times, the output matches output/certify_row2.txt line for line, including
  the full step log (4110 centre steps, 7084 box steps, every logged rho and maxrad). The regenerated
  output/A_row2_r55.json is byte-identical to the saved one, so I found no non-determinism.

## 2. Own checker, written from the definition before I read the author's code (check_A.py)
I did rigorous arb linear algebra (400 bits) on the saved enclosure output/A_row2_r55.json, where A = D phi_{T/2}(x0).
I built my own J and my own reversor S(q1,q2,q3,v1,v2,v3) = (-q3,-q2,-q1,v3,v2,v1). From those:
A^{-1} = -J A^T J (valid for the true, symplectic A), M = S A^{-1} S A, and N = M - I. I took the characteristic
polynomial of N with my own Faddeev-LeVerrier and cross-checked it against arb_mat.charpoly (they overlap). The
coefficients in mu = lambda - 1 are the Taylor coefficients of charpoly(M) at 1. I then formed
q = sum_{k>=8} c_k mu^(k-8) and used the palindromic s-test.
- A^T J A - J contains 0 entrywise (maxrad 1.1e-27). S^2 = I and S^T J S = -J hold exactly.
- c0..c7 all contain 0 (max |.| 4.6e-7), which is consistent with 8 trivial multipliers.
- q = [1 +/- 1e-19, 0.915292648037022 +/- 1e-16, -0.161396344655378 +/- 2e-16, 0.915292648037022 +/- 1e-16, 1].
  This agrees with the claim's q_red. q0 contains 1 and q1 overlaps q3, so q is consistent with being palindromic.
- Route a = a3: discriminant [9.48334601017 +/- 2.1e-12] > 0. s1 = [-1.9973984152796446194 +/- 1.6e-20] and
  s2 = [1.0821057672426225198 +/- 2.2e-21] are both strictly inside (-2, 2) and distinct. Route a = a1 gives the same.
  So the true reduced multipliers are e^{+-i theta1} and e^{+-i theta2} with theta1 != theta2 in (0, pi): four
  distinct values on the unit circle, none equal to +-1.
- theta/2pi = [0.1590129389037642508104064 +/- 1.4e-26] and [0.491881305365955760282366 +/- 2.6e-25]. These match the
  claimed frequencies 0.15901293890376425081040... and 0.49188130536595576028236..., and the source file
  data/res_eig_angles.txt (i.c. 2).

## 3. Own structural lemmas (own_lemmas.py, exact sympy) and the factorization argument
My first version used sp.simplify and stalled for over 80 minutes. I stopped that single PID and replaced simplify
with exact expansion of the bases of the powers followed by expand. No check was dropped, and all of them pass:
- f(Sx) = -S f(x).
- omega(f,.) = dH and omega(Rx,.) = dL.
- Df e = 0 and Df b = e (for both x and y).
- Df Rx = R f.
- x0 is in Fix(S), and P = COM = L = 0 at x0.
- dH and dL vanish on U = span(e_x, e_y, b_x, b_y, f, Rx0) at x0.
- q1 x w = 0 together with q1 . w = 0 forces w = 0 when q1 != 0.

The claim's own code/lemmas.py also prints True for every line.

I re-derived these proof steps by hand:
- Step 2 (G = 0 implies x(t) in Fix(S), hence phi_{2t}(x0) = x0) holds.
- The monodromy formula holds: D phi_t(x(t)) = S A^{-1} S, so M = S A^{-1} S A.
- The factorization charpoly(M) = (lambda-1)^8 q_red holds:
  - M acts unipotently on U, and dim U = 6.
  - U ∩ U^omega = span(f, Rx0), because omega(e_x,b_x) = omega(e_y,b_y) = 3 makes omega non-degenerate on span(e, b).
  - U^omega / span(f, Rx0) is the 4-dimensional symplectic reduced space.
  - V / (U + U^omega) is omega-dual to span(f, Rx0), on which M = I, so it contributes (lambda-1)^2.
- q_red is the characteristic polynomial of a symplectic map, so it is palindromic. That makes the s-test with the
  a3 ball alone rigorous.

## 4. Independent numerics (own_numeric.py, non-rigorous cross-check)
- scipy DOP853 in float64 with the variational equations, from the listed row-2 data:
  - G(listed) ~ 1e-13.
  - max |A_float - mid(A_saved)| = 2.3e-10.
  - Direct full-period monodromy over [0, T] (no symmetry used) gives |x(T) - x0| = 8e-13. Its non-trivial
    multipliers are 0.54105288 +- 0.84098857 i and -0.99869921 +- 0.05098914 i, with |.| = 1 to 5e-12 and
    theta/2pi = 0.159012938905 and 0.491881305366.
- My own order-40 Taylor integrator at 300 bits, using arb midpoints only, gives G(listed) ~ 5e-23. That figure is
  limited by my crude step rule, and it is consistent with the certified G_centre of about 1e-65.

## 5. Audit of the claim's code for rigour holes
- **Taylor recurrences (code/vt3b.py).** The s^{-3/2} and s^{-5/2} recurrence weights (-m-2k)/2 and (-3m-2k)/2 are
  correct. The variational terms ds = 2(dx ddx + dy ddy) and dw3 = -3/2 w5 ds are correct. The coefficients are
  evaluated in ball arithmetic over the whole current ball.
- **Cauchy tail.**
  - The a priori set is checked as Z + D_rho F(B) ⊂ B over a complex square of half-side rho, which contains the disc
    |tau| <= rho. The argument works ray by ray: the integral lies in tau times the convex hull of f(B), which sits
    inside the acb box.
  - Re(s_ij) > 0 is checked on every candidate B, so f is holomorphic there.
  - Returning `new` instead of B is valid, because new = Z + D F(B) still contains the solution.
  - |x_k| <= sup_B |x - c| / rho^k with a constant centre c. The tail is dev kappa^N / (1 - kappa) for k >= N, and
    coefficients 0..N-1 are summed. Tangent components are included in both the containment test and dev.
  - I found no hole.
- **Final step onto the time interval.** It takes h = (t_end - t) + [-r, r] and checks that the upper bounds are at
  most kappa rho. The accumulated t can carry a rounding radius, which only widens h. No hole.
- **Krawczyk (certify.py).**
  - DG is evaluated on the full box and the full time interval; the d/dt column is grad G . f(Y), and the gradient
    entries are correct.
  - Fine point: dX = [-r, r] while the integrated box is xc + arb(0, r), which is slightly wider. The argument is still
    rigorous if you read it with x̂ = mid(xc) and X' = x̂ + [-r, r] ⊂ the integrated box: G(x̂) lies in G_centre,
    DG(X') lies in DG(box), and the test |K - xc| < r bounds |K - x̂|.
  - The margins are dev/r ≈ 1e-10 to 1e-9, so the zero lies within about 1e-64 of x̂. The claim's 1e-55 and 2e-55
    bounds therefore hold.
  - q1 != 0 at the zero follows from the collision-free enclosure (Re s > 0) together with q2 = 0.
- **C2.** The 6x6 minor (rows 0,1,2,3,6,7) is [-1.393335518 +/- 4.6e-10], a certified non-zero arb determinant, so
  dim U = 6.
- **C3 and C3'.** I reimplemented the 12x12 route independently and the results agree. In the 4x4 quotient route,
  z_j is in U^omega: it is COM-free, so omega with e and b is 0, and it is corrected so dH(z) = dL(z) = 0. The other
  six coordinates are certified to contain 0, as the theory requires. Either route alone suffices.

## Not done / limitations
- I did not write a second validated (interval) integrator, so existence (C1) and the rigour of the A enclosure rest
  on the audited code in code/vt3b.py and the deterministic rerun. They are cross-checked only non-rigorously by my
  own float and 300-bit integrations, which agree.
- I did not run the known-positive and known-negative controls listed in REPRODUCE.md.
- The literature-novelty condition of p1 is outside this reproduce role.
- KAM (non-resonance and twist) is not claimed and was not checked.

## Verdict
Every property and value in the claim reproduced. Existence holds in the 1e-55 box via the Krawczyk strict interior,
and the C2 minor is non-zero. The reduced multipliers are certified as four distinct values on the unit circle, with
the claimed frequencies. The rerun is deterministic and bit-identical. I found no rigour hole in the audited steps.

pass: true
