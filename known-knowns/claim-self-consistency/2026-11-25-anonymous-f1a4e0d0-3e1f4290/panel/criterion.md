# Criterion skeptic: White 2011 interferometer energy bound

context: subagent (fresh, Claude Code Agent tool)

Criterion (verbatim): "counterexample (an explicit parameter set quoted from the source under which its own equations contradict its conclusion) or bound (a certified lower bound on the power, energy or field the claimed effect requires)." The claim takes the bound shape. No partial wins are listed.

## 1. Is the "claimed effect" read faithfully from the source?
- Boost: the paper says "a 1cm diameter toroidal test article ... with a boost on the order of 1.0000001 is necessary". Slide 21 says "1.0000001 to 1.0000002". I rendered PDF page 31 myself, and the OCR matches the slide. The claim takes 1 + 1e-7, the low end of that range, which is the conservative choice.
- Gamma: the claim uses the source's own formula, gamma = cosh(0.5 ln|1 - v^2 f^2|). Checked: u* = 0.0299002893 gives gamma - 1 = 1.000e-7. This matches the small-u form 1 + u^4/8. The SR speed "~0.0004c" comes from a different premise. The claim labels it secondary and does not rely on it.
- R = 5 mm: the slide figure draws the "resultant spherical field" with a "1 cm" dimension. The paper also says "small (~1cm) spherical region". The ring sits on that sphere, where Eq. (3) peaks at r ~ R, so R = 5 mm is a faithful reading.
  - "~1cm" is approximate, but the bound scales linearly in R, so a factor-of-2 change in R leaves the order of magnitude at about 1e36-1e37 J.
  - "On the order of" is a hidden quantifier. The bound scales as u*^2, which is proportional to sqrt(gamma - 1), so it is insensitive to that too.
- "Anywhere": since 0 <= f <= 1 and f(0) = 1, max gamma equals gamma(v_s), reached at the bubble centre. So "reaches 1 + 1e-7 anywhere" is the same as "inside the 1 cm sphere", which is the source's own condition. This wording does not stretch the source.

## 2. Is the bound certified (proved for every sigma, not sampled)?
Yes. I checked each step of PROOF.md:
- Steps 1-2: f(0) = 1, f(R) = 1/(1 + tanh^2 sR) > 1/2, and 0 <= f <= 1. Gamma is strictly monotone in u on [0, 1).
- Step 3: the angular integral is int sin^2 theta dOmega = 8 pi/3, which gives E = -(v^2/12) I. The unit conversion c^4/G is correct for G = c = 1 energy density.
- Step 4: Cauchy-Schwarz gives I >= a f(a)^2 for every a, so I >= R/4 for all sigma > 0. This is analytic; no sampling is involved.
- My own mpmath check reproduces bound = -1.12708491e37 J. A grid over sR in [1e-3, 1e3] gives min I/R = 0.6677 > 1/4 at sR ~ 1.26, which agrees with the claim's E_min/bound = 2.67.
- The bound sits about 2.7x below the true minimum, so it is valid but not tight. It is stated as an inequality, so that is fine.
- E is the integral of Eq. (3) over the flat slice. That is the source's own "integration of the total energy density". The claim openly says it is not an ADM mass, which is honest.

## 3. Positive-energy ring / "cannot supply"; subsumption
- "toroidal-ring of positive energy density" appears literally on slide 21. "very high-voltage capacitor ring" appears in the paper. Both are quoted correctly.
- Eq. (3) is minus a square, so it is <= 0. That part is correct.
- However, the source itself says "the energy density for the metric is negative" and that the metric "violates all three energy conditions ... because of the need for negative energy density".
  - So the sign half of the claim (that a positive-energy source cannot supply Eq. (3)) is already conceded by the source. It is not new.
  - What the claim adds on the sign side is only that the source contradicts itself by calling the test article "positive energy density".
- "Cannot supply" is fair only within the source's Eq. (1)/(3) framework. The slide also floats a different route: acting on the potential phi of ions with capacitors. Within the source's own equations, though, any field with that boost is an Eq. (1) metric, and Eq. (3) prices it. So the wording is acceptable if read as "under its own equations". The headline sentence is slightly wider than that.
- The source never quantifies the energy needed for the 1 cm, 1 + 1e-7 test article. It only says "not an easy task". The certified magnitude bound, |E| >= 1.127e37 J (about 1.25e20 kg), is therefore not subsumed. That bound is the genuine win.

## 4. Null model
I agree that none is needed. The result is a deterministic analytic inequality, not a statistical detection. The known-case checks (beta = 0 gives E = 0, and the thin-wall asymptote ratio is 1.0001) serve as the appropriate controls.

## Verdict
The claim meets the "bound" shape of the criterion. The bound is certified for every sigma > 0, and it is taken from the source's own Eq. (1), f, Eq. (3), gamma formula and stated operating point. The scope below is limited to the magnitude bound. The sign and "positive energy density" part is mostly conceded by the source and should not count as the win.

confirmed_scope: Under White 2011's own Eq. (1), top-hat f(r), Eq. (3) and gamma = cosh(0.5 ln|1 - v^2 f^2|), every field with bubble radius R = 5 mm whose boost reaches 1 + 1e-7 has a flat-slice integrated Eq. (3) energy E <= -(c^4/(48G)) u*^2 R = -1.127e37 J (u* = 0.0299002893) for every wall parameter sigma > 0, a negative energy that the source's proposed positive-energy capacitor ring cannot supply within its own equations.
pass: true
