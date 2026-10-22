# p_c^site(Z^2) >= 0.5567: a rigorous lower bound for site percolation on the square lattice

## What

Assuming Fisher's inequality p_c(S) + p_c(S*) >= 1 and Strassen's coupling theorem, claim/ proves p_c^site(Z^2) >= 5567/10000 = 0.5567 by the van den Berg-Ermakov growth-process comparison, with the deciding computations (window.py's depth-2 and depth-3 cone checks at p = 4433/10000 and validate.py's root step) in exact rational arithmetic and recheckable from claim/ with the Python standard library; that this beats the best published rigorous lower bound rests on the package's literature record naming 0.556 as that bound.

The previous best published rigorous lower bound is 0.556 (J. van den Berg and A. Ermakov, 1996). The proof
(object/PROOF.md) keeps their growth-process comparison. Their conditioning window is replaced by exact belief
propagation over the exploration tree: exact to depth 3, with outer cones covering the rest of the history. The
finite part is an exact rational check at p = 4433/10000 (object/window.py, object/bound.json).

## Check it yourself

    sh verify-it-yourself/run_checks.sh

The expected last line is `PASS`. It takes a few seconds on a laptop and needs only Python 3 (standard library). It
checks the object's hashes and recomputes every margin with an independent implementation that does not use the
certificate's code and does no rounding. It also recomputes the root step from the definition. RUN_IT_YOURSELF.md
reruns the certificate itself.

## Compared to

| record | value | source | checked |
|---|---|---|---|
| best published rigorous lower bound for p_c^site(Z^2) | 0.556 | J. van den Berg and A. Ermakov, Random Structures Algorithms 8 (1996) 199-212, https://doi.org/10.1002/(SICI)1098-2418(199605)8:3%3C199::AID-RSA4%3E3.0.CO;2-T (abstract: https://ir.cwi.nl/pub/4915) | the-record-we-beat/TABLE_RECORD.md; literature fetches 2026-10-18T18:50:24Z to 18:54:23Z |

There is no record table for rigorous bounds; the record is the literature (searches and fetches in
the-record-we-beat/ and panel/novelty.md). 0.5567 is also above 0.5560829, the exact optimum of the 1996 method.

## Not claimed

- No upper bound. The best upper bound found is 0.666894 (Wierman and Oberly 2024), untouched.
- Nothing about the numerical value of p_c (about 0.59274605, Jacobsen 2015), which is not a rigorous bound.
- Not the best this method can give. The same relaxation passes up to p = 0.443214911 at depth 3, and saturates at
  0.556788090 by depth 8. Only p = 4433/10000 was frozen in the preregistration, so only 0.5567 is claimed.
- The proof rests on two classical theorems as cited: Fisher's inequality p_c(S) + p_c(S*) >= 1, and Strassen's
  coupling theorem.
- See ERRATA.md for small corrections to the panelled text. None changes the result.

## Credits

- Kaust-a-laut, with Claude Code (Anthropic) running claude-opus-5-5, using the V3R1T4S kit. The human contributor
  proposed the directions that led here, among them the larger windows and the realizable-history and perturbed-lattice
  ideas, and checked the plan at every step.
- The method and the bound improved: J. van den Berg and A. Ermakov, "A new lower bound for the critical probability
  of site percolation on the square lattice", Random Structures Algorithms 8 (1996) 199-212 (above); A. Ermakov's
  thesis, https://ir.cwi.nl/pub/25488/Thesis_AErmakov.pdf.
- The original method: M. V. Menshikov and K. D. Pelikh, "Percolation with several defect types. An estimate of
  critical probability for a square lattice", Mat. Zametki 46 (1989) 38-47; Math. Notes 46 (1990) 778-785.
- p_c(S) + p_c(S*) >= 1: M. E. Fisher, J. Math. Phys. 2 (1961) 620-627 (as cited in the 1996 paper, Theorem 1.2).
- The coupling theorem: V. Strassen, via T. M. Liggett, Interacting Particle Systems (Springer 1985), Chap. II,
  Thm 2.4 (as cited in the 1996 paper, Theorem 1.3).
- Upper bound for context: J. C. Wierman and Oberly (2024), https://doi.org/10.1007/978-3-031-62166-6_9.
- Numerical value for context: J. L. Jacobsen (2015), https://arxiv.org/abs/1507.03027.
