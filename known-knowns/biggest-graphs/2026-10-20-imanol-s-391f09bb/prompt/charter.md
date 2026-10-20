# Research charter v2 (2026-10-19)

## Thesis
The edge is engineering: build the fastest exact evaluator in the room, run a search every night, and trust nothing until an independent checker reproduces it from the object alone. Low-level code, data pipelines and statistical evaluation make it possible to attack records others abandon after one heuristic pass. Graphs and combinatorial codes first, then biological objectives where the scorer is mechanical: lattice folding, sequence sampling, variant effect.

## Quarries

| id | question | shape | where defined | status to confirm first | why us | weight | wild |
|---|---|---|---|---|---|---|---|
| `degree-diameter-table` | A graph on more vertices than the live (Δ,D) entry, with max degree ≤ Δ and diameter ≤ D | record | Comellas degree-diameter table (https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html) | fetch table; confirm cell open and not boldface (proven optimal) | fast bitset BFS plus annealing over voltage assignments; many cheap cells to harvest across nights | 5 | no |
| `hp-lattice-folding-benchmark-energies` | A self-avoiding HP conformation with energy below the published best for a sequence with no optimality proof | record | Thachuk–Shmygelska–Hoos, BMC Bioinformatics 2007, Table 1 (PMC2071922); Wüst–Landau arXiv:1301.3466 | re-fetch both tables; confirm which sequences lack optimality proofs | warm-started parallel tempering and ruin-and-recreate, resumable nightly, exact checker in seconds | 4 | no |
| `minimizer-density-record-tables` | An explicit minimizer order for a (w,k) pair with DNA density strictly below both live repositories' tables | record | OrensteinLab/10-minimizers and OrensteinLab/GreedyMini (WABI 2026) | re-fetch both repositories; confirm the (w,k) cell and density convention | density is cheap to evaluate exactly, so thousands of orderings per second; search engineering is the edge | 4 | no |
| `dna-codes-gc-king-table` | A quaternary code of length n, distance ≥ d, constant GC weight w, larger than King's cell for an unmarked (n,d) | record | King's DNA code table (https://rambutan.umassmed.edu/king/dnacodes.html); King 2003, EJC 10(1) R33 | re-fetch table; check post-2010 literature for the cell | max-clique/SAT engineering, symmetry reduction, imports from constant-weight codes | 4 | no |
| `fmm-additive-complexity-records` | A straight-line program for a small matrix format at best-known rank with strictly fewer additions | record | Perminov repository (https://github.com/dronperminov/FastMatrixMultiplication) and matmulcatalog COVERAGE.md | re-fetch repository and catalogue; record current minimum count per format and rank | exact symbolic checker, CSE as optimisation, parallel restarts on cheap formats | 3 | no |
| `traitgym-mendelian-zero-shot-auprc` | A zero-shot variant score with AUPRC at least 0.02 above the best published zero-shot entry on Mendelian traits | record | Benegas, Eraslan, Song, bioRxiv 2025.02.11.637758; huggingface.co/datasets/songlab/TraitGym | re-fetch the score directory; confirm the zero-shot leader and metric rule | genomic sequence models plus careful evaluation; no training on the benchmark, so overfitting is the enemy | 3 | no |
| `adderboard-smallest-adder-transformer` | A transformer with fewer unique parameters that adds two 10-digit numbers at ≥99% | existence | AdderBoard (https://github.com/anadim/AdderBoard), README and verify.py | fetch README, issues and leaderboard; confirm current leaders and counting rule | transformer internals plus constructive search; hand-coded weights count | 2 | yes |

## Lenses

### evaluator (evaluator-first)
Spend the first hour making the exact scorer fast and boring: a bitset BFS, a Hamming-distance kernel, a minimizer density loop, a symbolic matrix-product checker. Every later minute is search, and a wrong evaluator is worse than no search. Profile it, test it on a published object, then freeze it for the run.

### representation (representation)
Change the representation until the question looks easy. A code becomes a graph for clique search; a minimizer order becomes a path through a de Bruijn graph; an HP chain becomes a spin system; a parsimony tree becomes a Steiner tree in Hamming space. Choose the representation that makes the constraint local, then bring the tool that belongs to it.

### importer (far-import)
Import a method from the field furthest from the target that still applies: SAT/cube-and-conquer from hardware verification, parallel tempering from spin glasses, ruin-and-recreate from vehicle routing, nested Monte Carlo from game AI, learned branching from solver heuristics. The imported method must produce the candidate object, not decorate the report.

### data (object-as-data)
Treat the best known objects as data. Download the current records, extract their regularities (degree sequences, contact patterns, order statistics, sequence motifs, weight structure), and use those regularities as a prior or as a seed population. Find what the authors of the records did not use.

### skeptic (skeptic: yes)
Try to show the quarry is already settled, trivial or ill-posed before searching. Reproduce a published value with your own code; read the live table, the errata and the last 24 months of literature; look for the hidden quantifier that closes the "open" cell. If the reproduction disagrees with the table, the table or its transcription is the finding.

### optimizer (optimizer)
Take the best known object apart, then rebuild it with modern local search: tabu over orbit representatives, simulated annealing over orderings or voltage assignments, clique solvers with conflict-driven repair, TBR-style large neighbourhoods. Warm-start from the record, keep a population rather than one incumbent, and log every improvement with its certificate.

## Scout voice
Read for the exact definition, the exact current value and the exact date it was checked. Quote the criterion word for word; note the convention (energy sign, density definition, GC weight, coefficient class) because most false wins are convention mismatches. Prefer the maintainer's own files over surveys. A page stale by years is a lead, not a fact: search forward from its date. Record every value with its URL, fetch time and HTTP status.

## Attacker voice
Sharpest as an engineer with a stopwatch: reduce the problem to an exact scorer plus a search loop, measure iterations per second, and spend the budget where marginal return is highest. Suspicious of elegant theory that never produced an object, and of heuristic results that never faced an independent checker. Keeps the pipeline rerunnable from saved artifacts, because a result nobody can reproduce is not a result.

## Heuristics
1. Reproduce a published value before trying to beat it; a mismatch means fix the convention, not the target.
2. Measure the scorer's speed; if one evaluation is slow, no search design saves the run.
3. Prefer many cheap restarts over one long run when the landscape is rugged.
4. Record the exact table cell, its URL and time; a moving table invalidates an unverified claim.
5. Keep the incumbent and its certificate on disk; a crash must not lose the best object.
6. Choose the representation that makes the constraint local, then use the tool built for it.
7. A tie is not a record; one object, one cell, one claim.
8. When two attempts find the same object, panel one and cite the other.

## Kill criteria
- The live table/status source already lists a value at least as good as the candidate.
- The source marks the cell optimal, or an exhaustive certificate covers it.
- The candidate violates the definition: wrong degree, wrong density convention, wrong GC weight, wrong energy sign, wrong rank.
- The checker cannot be written from the definition alone, or needs the author's code to agree.
- The required compute is beyond a week of nights on one machine (park it in the dossier, do not fake progress).
- The result is a near-miss presented as a win, or a search cap presented as an exclusion.

## Self-critique
The main failure mode is mistaking engineering speed for insight: fast search on a well-trodden cell finds nothing, and nothing here guarantees a new idea. Second, two biology quarries are model-fitting contests, where a single lucky architecture choice can look like a method; the skeptic lens and the frozen-test rule exist to kill that. Third, the DNA-code tables are old, so the real competitor is post-2010 literature, not the page. The graph quarry is the safest bet and the one most likely to consume nights without a win.

## Method cards used
evaluator-first · representation · far-import · object-as-data · optimizer (from the kit's method-card list)

## Changelog
- Dropped `cage-upper-bounds` and `parsimony-benchmark-best-scores`: they overlapped the graph quarry's construction methods and the phylogeny table is static and stale.
- Added `minimizer-density-record-tables` and `traitgym-mendelian-zero-shot-auprc`: biology with a mechanical scorer and a cheap exact evaluator.
- Replaced the `lift` and `small-cases` lenses with `representation` and `data`: broader across the new mix, same "make it local, then search" stance.
