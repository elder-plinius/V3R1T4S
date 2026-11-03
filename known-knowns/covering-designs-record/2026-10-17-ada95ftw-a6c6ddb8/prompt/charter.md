# Research charter v2 (2026-10-13)

## Thesis
Original seeds were random; v2 re-aims them at what one modest CPU machine (8 cores, ~3 GB RAM, no GPU, ~1 h nights) can really win. The edge is patience plus an exact evaluator built first: small combinatorial constructions and a cipher-machine search, where every candidate is checked in milliseconds and a stranger can rerun the check. No data-heavy archives, no GPU work.

## Quarries
1. id: constant-weight-codes | question: a binary constant-weight code beating a lower bound A(n,d,w) in Brouwer's table | shape: record | where defined: bank constant-weight-codes (Brouwer, https://aeb.win.tue.nl/codes/Andw.html) | status first: the live table cell | why us: exact pairwise-distance checker, structured (cyclic/group-orbit) search fits small RAM | weight 5 | wild no
2. id: degree-diameter-table | question: a larger graph for a small (Delta,D) cell of the degree-diameter table | shape: record | where defined: bank degree-diameter-table (Comellas table, https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html) | status first: the live cell value | why us: BFS diameter check is fast; voltage/Cayley-graph families keep search small | weight 4 | wild no
3. id: covering-designs-record | question: a covering design C(v,k,t) with fewer blocks than the La Jolla repository entry | shape: record | where defined: bank covering-designs-record (https://coveringrepository.com/) | status first: the repository entry for the chosen (v,k,t) | why us: local search with an exact coverage checker, tiny memory | weight 3 | wild no
4. id: cryptocellar-enigma-1941-remaining | question: a full Enigma key that decrypts one of the remaining unbroken 1941 German Army messages | shape: decipherment | where defined: bank cryptocellar-enigma-1941-remaining (https://www.cryptocellar.org/bgac/1941-msg-list-unbroken.html) | status first: the CryptoCellar unbroken list | why us: hill-climbing over known machine settings is CPU-only; simulator checked on solved siblings first | weight 3 | wild no
5. id: snake-coil-in-the-box | question: a longer snake or coil in a hypercube of dimension 9-13 than the listed record | shape: record | where defined: bank snake-coil-in-the-box (https://www.minortriad.com/snake/) | status first: the record list for the chosen dimension | why us: checker is trivial, symmetry-reduced search fits a night | weight 2 | wild no
6. id: life-smaller-orphan | question: a Game of Life orphan with a smaller bounding box than the known ones | shape: record | where defined: bank life-smaller-orphan (https://conwaylife.com/wiki/Garden_of_Eden) | status first: the smallest orphan listed | why us: looks too strange; SAT-style tiling search might just work | weight 1 | wild yes

## Lenses
- key: evaluator | title: Exact evaluator first | You build a fast exact checker and test it on a known record and a known non-example before any search. Dead sign: it cannot reproduce the table's current value. skeptic no
- key: structured | title: Search a structured family | You restrict to cyclic, group-orbit or voltage constructions so the space is small and complete. Dead sign: the family's exhaustive maximum is below the record. skeptic no
- key: obstruction | title: Search where invariants are silent | You compute counting, parity or symmetry bounds that forbid improvement and search only where they are silent. Dead sign: the bound equals the record. skeptic no
- key: solver | title: Let a solver argue | You recast the cell as SAT or ILP for small cases and let a solver run under a hard time cap. Dead sign: timeouts on the easiest open case. skeptic no
- key: footnotes | title: Footnotes and errata | You read open-question sections and errata of the source papers for near-misses, then test them. Dead sign: every lead is already in the table. skeptic no
- key: skeptic | title: Already settled? | You try to show the quarry is already beaten, a tie, or ill-posed, using the fresh table and recent arXiv. Dead sign for the quarry: a newer equal or better entry. skeptic yes

## Scout voice
Read for the exact definition and the newest number in the primary table; note the date of every status.

## Attacker voice
Patient and literal: checker first, then grind small cases night after night, unmoved by near-misses.

## Heuristics
- A tie is not a record.
- Small parameters first; scale only what works.
- Integer, exact certificates only.
- Cap every search with timeout and a checkpoint; say when it is capped.
- For the cipher, verify the simulator on a solved sibling message first.

## Kill criteria
- The live table already holds an equal or better value.
- The checker cannot verify a known positive.
- A search needs more than ~2 GB RAM or a week of nights on 8 cores.
- Cipher candidates do not beat a 400-control null.

## Self-critique
These tables are well worked; small cells may already be optimal, so most nights will end in ties or nothing. Enigma message keys may need more search than a 1 h night. The wild quarry is likely out of reach.

## Method cards used
footnotes, evaluator-first, obstruction-first (original random draw), plus structured-family and solver added in v2

## Changelog
v2: per the human's request ("swap to something you can handle"), replaced telescope-archive and fast-matrix-multiplication/packing quarries with CPU-light, small-memory bank targets with fast exact checkers. Kept the evaluator-first, obstruction, footnotes and skeptic lenses.
