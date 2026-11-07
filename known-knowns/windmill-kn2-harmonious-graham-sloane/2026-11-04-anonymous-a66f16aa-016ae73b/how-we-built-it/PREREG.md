# Preregistered n=10 continuation
frozen_utc: 2026-11-04T18:05:18+00:00
target: windmill-kn2-harmonious-graham-sloane
null_test: not needed because this is a deterministic finite graph-labeling decision with exact integer verification, not a statistical score or a claim of beating chance.

## Full bank criterion (verbatim)
Success means, for n = 8, EITHER (a) an explicit assignment of 15 distinct residues mod 56 to the vertices of K_8^(2) such that the 56 edge sums are pairwise distinct mod 56 (refuting the conjecture), OR (b) a certified proof that no such labeling exists: an exhaustive search by two independent programs, or a SAT/CP encoding whose UNSAT result carries a DRAT/LRAT proof checked by drat-trim or cake_lpr plus an independent second method, with every symmetry reduction used (translation f -> f+t, multiplication by a unit mod 56) justified in the write-up. Before claiming, re-check the latest DS6 edition (Table 2, 'windmills') and the literature for a published decision of K_8^(2).

## Selected partial win (verbatim)
The same (a) or (b) decision for n = 10 (19 vertices, q = 90).

## Scored instance and acceptance
Two K10 cliques sharing one vertex. Exactly 19 distinct labels modulo 90 and all 90 within-clique edge sums distinct. Positive requires an explicit labeling and independent edge-by-edge verification. Negative requires two independent complete exhaustive methods, with every pruning and normalization justified. No capped computation proves impossibility. Every promising result requires fresh independent reproduce, criterion and novelty reviews.

## Search design
Independently widen the prior two authors' own methods to at least 90 bits. Neither author reads the other's implementation. Calibrate against the completed n=8 case and n=4 positive. Benchmark n=10 small prefixes with explicit time/memory caps before scaling. Complement matching stores exact edge masks; direct constraint search builds both cliques. Permitted reductions are center translation, sorted clique vertices and proved necessary parity constraints; any further reduction needs its own proof written before use.

## Novelty status
DS6 current edition and prior PR894 leave n=10 unclaimed in the checked material. A fresh GitHub API search of all harmonious pull requests returned only PR894 at 18:03 UTC. This is provisional coverage, not proof of novelty. Any claim needs a fresh panel.
