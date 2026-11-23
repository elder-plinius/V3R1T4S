# Honesty gate (run main session), Pb N = 121

Panel: reproduce.md pass: true, novelty.md pass: true, criterion.md pass: true. All three were fresh-context subagents,
each with only a copy of claim/.

Checks:
- Reproduction: two independent evaluators written from data/lead.f (REPRODUCE, CRITERION) and the authors' code
  agree on E = -198.47902916627225 eV to better than 1e-12 eV. A genuine 30-digit polish (CRITERION |g| 1.39e-23,
  REPRODUCE 2.1e-27) closes the gap left by the authors' float64 polish. Hessian: 6 zero modes, 0 negative, 7th 0.149.
- Live table: the gate re-fetched https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/lead/table.html once at
  2026-11-23T07:47:19Z, HTTP 200, sha256 dce45e7bfc9e7aa1887d2addfc710a6626b40a7c1684839da5186e1d08668bef (byte-identical
  to the scout and NOVELTY fetches). Row N = 121 is -198.211397. CRITERION's condition holds: the object is 0.267632 eV lower.
- Novelty: no published lower value. Trivial-edit bars (claim's and NOVELTY's own, 129,675 relaxations): none within
  0.2393 eV of the object. The 2- and 3-relocation families were sampled, not exhaustive; this is disclosed and does
  not widen the scope, which says nothing about trivial edits.
- One object, one cell (Pb, 121). No hedging panelist. No table value obtained by evasion. No benchmark baseline needed.
- Scope: a certified local minimum of a model potential, below the table row. It makes no claim about a global minimum
  or about real lead clusters.

status: CONFIRMED_SOLUTION
confirmed_scope: The 121 coordinates in result/Pb_121.xyz form a certified local minimum of the Lim-Ong-Ercolessi Pb glue potential (data/lead.f) at -198.47902916627225 eV, 0.26763 eV below the N = 121 value of the lead table as fetched 2026-11-23T07:06:49Z (-198.211397 eV), and 0.26763 eV below the polished posted N = 121 structure, with no lower published value found by web search; this is conditional on the gate's live re-fetch still showing -198.211397 (or any value above -198.479029) for N = 121.
