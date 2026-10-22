# How we found it (contributor text, unverified)

Found by Kaust-a-laut with Claude Code (Anthropic) running claude-opus-5-5, in a V3R1T4S live session and run on
2026-10-19.

## Brief

The same session had just proved the upper bound p_c^site(Z^3) <= 0.4427. On the lower side, the gap to the
numerical value (about 0.3116) looked wide. The scout's record was 1/mu = 0.21103, from the self-avoiding-walk
connective constant. That turned out to be wrong: the panel later found the higher record 0.2522. Torquato and Jiao
had proposed 5/19 = 0.2632 without proof.

## What failed

- Neighbour-avoiding walks alone. A shortest open path is a neighbour-avoiding walk (NAW), so p_c >= 1/lambda_NAW.
  - We counted NAWs exactly to n = 18.
  - Alm's matrix method with an exact Collatz-Wielandt certificate then gave 0.243582, which the route cannot pass
    (its limit is about 0.2445).
  - That is above the scout's 0.21103 but below the real record 0.2522, so on its own it would not have been a
    result.
- Stitching short pieces with forced-closed weights (Alm-style windows) is unsound. A site can be charged twice when
  the path returns near itself. We dropped it.

## What worked

- Make the shortest path canonical. Each site's parent is its neighbour one step closer to the origin, in the
  smallest direction index. Then more sites are forced closed:
  - every off-path site adjacent to two path sites at least 3 steps apart;
  - at about half of the turns, the corner site, which would otherwise be the preferred parent.
- Koenig's lemma and independence on disjoint site sets give theta <= K_N theta.
- An exhaustive parallel enumeration with exact integers, using the 8 sign-flip symmetries, gave these thresholds:

  | N | threshold |
  |---|---|
  | 10 | 0.250856 |
  | 12 | 0.254646 |
  | 14 | 0.257568 |
  | 16 | 0.259894 |
  | 18 | 0.261794 |
  | 20 | 0.263376 |

  The N = 20 run took 140 minutes on 6 cores.

## Checks before the panel (how-we-built-it/selfbreak/)

- Ground truth: true parent trees in 300 random configurations, with negative controls.
- An independent enumeration from complete paths: the full N = 9 table, and full-depth subtrees at N = 18 and 20.
- All 24 ordered pairs of perpendicular steps for the corner rule.
- Plain against parallel enumerators at N = 12 and 14.
- An outside AI audit, relayed by the human, that ran the checks itself.

## Panel and gate

- The panel's REPRODUCE skeptic wrote its own enumerator, with a different symmetry reduction, and regenerated the
  N = 20 table exactly.
- Its NOVELTY skeptic found the 0.2522 record the scout had missed. We corrected the record everywhere, and the
  claim's margin shrank from 0.052 to 0.011.
- At the gate the citation was corrected again: 0.2522 is Theorem 7.1 of the journal paper.
- Lesson: chase every search snippet that mentions an improved bound before writing the record down.
