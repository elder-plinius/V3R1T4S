# Research charter v1, track A (2026-10-24): methods only (quarries, lenses, heuristics, kill criteria)

## Quarries

1. **id:** eaqecc-qutrit-codetables-gaps
   **question:** For some cell of the live qutrit EAQECC table, is there an explicit [[n,k,d;c]]_3 code (c ≥ 1) with d strictly above the tabulated lower bound?
   **shape:** record (table cell).
   **where defined:** bank entry `eaqecc-qutrit-codetables-gaps`; eaqecc.codetables.de qutrit table; Luo, Ezerman, Grassl and Ling (QIP 2024, arXiv:2207.05647); Grassl (PRA 2021).
   **status to confirm first:** the live table and this repo's known-knowns folder of the same name (cells already improved are not new).
   **why us:** thousands of cells with gaps between bounds; constructions from classical codes over GF(9) with a fast exact distance check.
   **weight:** 5 · **wild:** no

2. **id:** codetables-binary-linear
   **question:** Is there an [n,k] binary (or small-q) linear code with minimum distance strictly above the codetables.de lower bound?
   **shape:** record (table cell).
   **where defined:** bank entry `codetables-binary-linear`; codetables.de (Grassl).
   **status to confirm first:** the live cell and this repo's known-knowns folder of the same name.
   **why us:** constructions (shortening, puncturing, concatenation, quasi-cyclic search) where exact enumeration is cheap for moderate k.
   **weight:** 4 · **wild:** no

3. **id:** constant-weight-codes
   **question:** Is there a binary constant-weight code larger than Brouwer's tabulated lower bound for some (n,d,w)?
   **shape:** record (table cell).
   **where defined:** bank entry `constant-weight-codes`; A. E. Brouwer's tables at aeb.win.tue.nl/codes/Andw.html.
   **status to confirm first:** the live cell (the table moved on 15 Oct 2026) and TROPHY_CASE.md rows for this family.
   **why us:** local search seeded from published codes has produced many wins here; the skill is choosing cells not yet worked.
   **weight:** 3 · **wild:** no

4. **id:** degree-diameter-table
   **question:** For some (Δ, D) in the Comellas table, is there a graph with maximum degree ≤ Δ and diameter ≤ D with more vertices than the entry?
   **shape:** record (table cell).
   **where defined:** bank entry `degree-diameter-table`; F. Comellas' degree-diameter table at web.mat.upc.edu.
   **status to confirm first:** the live table and TROPHY_CASE.md rows for this family.
   **why us:** Cayley and voltage-graph constructions over structured groups, checked by all-pairs BFS.
   **weight:** 3 · **wild:** no

5. **id:** covering-designs-record
   **question:** Is there a (v,k,t) covering design with fewer blocks than every listed bound for that cell?
   **shape:** record (table cell).
   **where defined:** bank entry `covering-designs-record`; coveringrepository.com.
   **status to confirm first:** the live repository value and every other source the bank criterion lists.
   **why us:** simulated annealing and group-orbit constructions with an exhaustive coverage check.
   **weight:** 2 · **wild:** no

6. **id:** cage-upper-bounds
   **question:** Is there a k-regular graph of girth at least g with fewer vertices than the best known upper bound for some open (k,g)?
   **shape:** record.
   **where defined:** bank entry `cage-upper-bounds`; Exoo and Jajcay dynamic cage survey (DS16); arXiv:2511.07247.
   **status to confirm first:** DS16 and arXiv for newer records.
   **why us:** a hard, well-studied target; kept as the long shot.
   **weight:** 1 · **wild:** yes

## Lenses

1. **key:** cell-picker · **title:** Choose cells nobody worked · **skeptic:** no
   Fetch the live table once, diff it against the record holders' construction notes and this repo's known-knowns, and rank cells by gap size and by how cheaply an exact checker runs there. Dead when every cheap cell has been improved already.

2. **key:** constructor · **title:** Build from algebra · **skeptic:** no
   Build objects from algebraic families (cyclic and quasi-cyclic codes, codes over GF(9) traced down, Cayley and voltage graphs, group orbits of blocks), then search parameters. Dead when the family's best for the cell is at or below the entry.

3. **key:** optimizer · **title:** Warm-start from the record · **skeptic:** no
   Start from the current best object (or a published construction) and run local search, annealing or tabu moves with an exact objective. Dead when long runs plateau at the entry.

4. **key:** evaluator-first · **title:** Exact, fast, twice · **skeptic:** no
   Write two independent exact checkers (for example a full codeword enumeration and a different distance algorithm) and test them on the record holder and on a seeded flawed object before any search.

5. **key:** already-settled · **title:** Prove it is not new · **skeptic:** yes
   Assume any improvement is already known: re-read the live cell, the table's change log, this repo's TROPHY_CASE.md, known-knowns and open pull requests, and recent arXiv. Dead (for the cell) when it is listed or claimed.

## Heuristics

1. Exact checkers before search; floats never decide.
2. Prefer cells whose checker runs in seconds.
3. Seed from the record holder or its published construction.
4. A tie is not a record; one cell per claim.
5. Re-read the live cell right before claiming.
6. Skip cells this repo's contributors already improved.
7. Record the exact search space covered.
8. Move to the next cell after a documented plateau.

## Kill criteria

1. Two exact checkers disagree and it cannot be resolved.
2. The live cell already equals or beats the object.
3. The cell is improved in this repo, an open PR or the literature.
4. Local search plateaus at the entry across three distinct seeds.
5. The checker cannot run exactly at the cell's size on one laptop.
6. A claimed exhaustive search turns out capped.
