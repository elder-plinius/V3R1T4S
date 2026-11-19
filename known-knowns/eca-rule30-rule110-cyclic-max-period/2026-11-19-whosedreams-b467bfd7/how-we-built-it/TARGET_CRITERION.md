# success_criterion (verbatim from bank/targets.json)

Target id: `eca-rule30-rule110-cyclic-max-period`

The exact value of A334497(37) or A204371(37) (or any later term), from an exhaustive search over all 2^n states, or over all rotation orbits with the rotation factor accounted for. It must be run by two independent implementations that agree. Both must reproduce A334497(1..24) and A204371(1..30) exactly, and both must report their values for A334497(25..30). Where these differ from the listed terms, the claim must also meet partial p1's correction rule. A value below a listed term means a bug, because every listed term comes from an observed cycle. A witness state on the maximal cycle must be given, so a skeptic can confirm the cycle length by direct iteration. Bit order must follow the Wolfram rule-number convention, which the small-n reproduction checks. The term must not already be in the live OEIS entry at claim time.

## partial_wins p1

An independent exhaustive recomputation of A334497(25..36). OEIS took a(23..36) from a 2005 conference table whose full census stopped at width 24. The recomputation either confirms every term or corrects one, and a correction must exhibit a cycle longer than the listed value, verified by iteration.

## partial_wins p2

An independent exhaustive recomputation of A204371(31..36) by a second implementation, with the same confirm-or-correct rule.

## status_source

https://oeis.org/A334497
