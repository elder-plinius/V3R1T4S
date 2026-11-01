# PREREG: cubic-graphs-graceful-knuth-beyond-14

frozen_at_utc: 2026-11-01T15:20:55Z

Nothing has been computed for this target before this file (only geng graph counts for 4..18 as a tool smoke test).

## Criterion (verbatim, bank)
Success means EITHER (a) a certificate that every connected cubic graph on 16, 18, 20 and 22 vertices is graceful: one file per order giving each graph (graph6, as produced by nauty geng -c -d3 -D3 n or genreg) with a graceful labeling, where an independent checker regenerates the complete list, confirms the counts 4,060 / 41,301 / 510,489 / 7,319,447 (A002851), matches every generated graph to a certificate entry by canonical form, and checks that the labels are distinct integers in [0, 3n/2] and the edge differences are exactly {1,...,3n/2}; OR (b) a connected cubic graph with no graceful labeling, certified by two independent exhaustive methods (for example a SAT/CP encoding with a DRAT/LRAT proof checked by drat-trim or cake_lpr, plus an independent backtracking search). Before claiming, re-read the latest DS6 edition and Knuth's TAOCP errata/pre-fascicles for a newer verification bound; orders already covered there do not count.

## Partial wins (verbatim, bank)
- p1: Certificate (as in (a)) that every connected cubic graph on 16 vertices (4,060 graphs) is graceful.
- p2: Certificate that every connected cubic graph on at most 18 vertices is graceful (adds the 41,301 graphs on 18 vertices).
- p3: Certificate that every connected cubic graph on at most 20 vertices is graceful (adds the 510,489 graphs on 20 vertices).

## Checker and thresholds
- Certificate file per order n in {16,18,20,22} (regression also 4..14): one line per graph,
  "<graph6 exactly as output by geng -c -d3 -D3 n> <f(0)> ... <f(n-1)>".
- Checker K (C, separate code from the searcher): for each line (1) decode graph6, check n vertices, every degree 3,
  connected; (2) labels are distinct integers in [0, 3n/2]; (3) the multiset {|f(u)-f(v)| : uv edge} equals
  {1..3n/2}. Coverage: (4) canonical labelling (nauty labelg, built from source) of every certificate graph; the set
  of canonical forms has no duplicates and equals exactly the set of canonical forms of a fresh geng -c -d3 -D3 n
  regeneration; (5) the line count equals A002851(n) from data/b002851.txt (4060 / 41301 / 510489 / 7319447).
- Checker P (Python, independent code, no nauty): (1)-(3) again with its own graph6 decoder; coverage by an
  invariant that is not from nauty (a vertex-refinement hash seeded with closed-walk / short-cycle counts); any
  invariant collision is resolved by an exact isomorphism test written in the checker; number of distinct classes
  must equal A002851(n).
- Full win (a): K PASS and P PASS for each of 16, 18, 20, 22, and orders 18, 20, 22 not covered by any source found
  at the re-check before claiming (order 16 is KNOWN from Knuth F7A ex. 96; it is included because criterion (a)
  lists it, and it is reported as a regression, not as new). p1 = 16 (already known: will NOT be claimed as new);
  p2 adds 18; p3 adds 20.
- Counterexample route (b): any graph the searcher fails on gets a complete uncapped backtracking search plus an
  independent SAT/CP model with an UNSAT proof before any claim; a capped/heuristic failure is never evidence.

null_test: not needed because the result is a set of explicit labelings checked deterministically, with coverage checked against an independent regeneration and A002851; there is no search score or statistic to beat chance.

Baseline (step 3c): not applicable (no empirical benchmark).
