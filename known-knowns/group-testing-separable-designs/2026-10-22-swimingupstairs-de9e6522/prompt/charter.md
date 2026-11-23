# Research charter v2 (2026-10-16)

## Thesis
The same patience and physical feel for systems that settle, now aimed where results can feed into medicine: pooled-testing designs, sequencing and DNA-storage codes, and fixed-split benchmarks for drug safety and protein variants. The edge is many patient nights of exact search on small, neglected cases that people with lab or GPU priorities skip. Health impact is mostly indirect: these objects are tools.

## Quarries
1. id: group-testing-separable-designs. Question: extend or improve the best known values for non-adaptive pooled-testing designs: max number of binary vectors of length n whose pairwise unions are all distinct (OEIS A054961), the same for 3-unions (OEIS A290492), and the min number of tests T(n,d) to identify exactly d defectives among n items (OEIS A361928). Shape: record / bound or proof (explicit matrix; new exact terms need a certified exhaustive search). Defined: OEIS A054961, A290492, A361928; Du and Hwang, Combinatorial Group Testing and Its Applications (2000), ch. 7; Erdos, Frankl, Furedi, J. Combin. Theory A 33 (1982). Status first: current OEIS terms and comments. Why us: exact small-case search, nightly SAT/ILP patience. Weight 5. Wild: no.
2. id: dna-gc-rc-codes. Question: a larger quaternary (DNA) code with constant GC-content n/2, minimum Hamming distance d and reverse-complement distance >= d than the best published value for some (n,d). Shape: record. Defined: Wang, Liu, Chen, arXiv 2409.06519 (2024), Tables 1 and 4; lexicographic DNA-code tables, Electron. J. Combin. (emis.de ft/7248); arXiv 1902.04419. Status first: the newest published value for the chosen (n,d). Why us: local search on codes is the same settling process as a particle system. Weight 4. Wild: no.
3. id: tdc-admet-group. Question: beat a Therapeutics Data Commons ADMET Benchmark Group leaderboard value (scaffold split, fixed metric) for one dataset, under the leaderboard's multi-seed protocol. Shape: record (statistical; null controls required). Defined: Huang et al., Therapeutics Data Commons (NeurIPS Datasets and Benchmarks 2021); https://tdcommons.ai/benchmark/admet_group/overview/. Status first: the dataset's live leaderboard. Why us: careful, cheap baselines and honest nulls where crowded boards overfit. Weight 3. Wild: no.
4. id: constant-weight-codes. Question: beat a lower bound A(n,d,w) in Brouwer's table. Shape: record. Defined: bank entry constant-weight-codes. Status first: the live table cell. Why us: the building block of many pooling matrices and barcodes. Weight 3. Wild: no.
5. id: covering-designs-record. Question: a smaller covering design C(v,k,t) than the repository entry. Shape: record. Defined: bank entry covering-designs-record. Status first: the live repository entry. Why us: local search on designs. Weight 2. Wild: no.
6. id: proteingym-substitutions. Question: a higher Spearman than the best published value on a named ProteinGym substitution subset (e.g. one taxon or MSA-depth bucket), scored by the benchmark's own code. Shape: record (statistical). Defined: Notin et al., ProteinGym (NeurIPS 2023); https://proteingym.org/benchmarks. Status first: the live benchmark table for that subset. Why us: cheap structured features on neglected subsets. Weight 1. Wild: no.
7. id: deletion-codes-beyond-vt. Question: a binary single-deletion-correcting code of length n in 12..15 larger than the Varshamov-Tenengolts code VT0(n) (316, 586, 1096, 2048), or a certified smaller upper bound. Shape: counterexample / bound. Defined: Sloane, "On single-deletion-correcting codes" (2002), arXiv math/0207197; OEIS A000016. Status first: newest literature on A(n,1) bounds. Why us: one machine, many nights, on a question most people consider closed. Weight 1. Wild: yes.

## Lenses
- search-engineer: Solver first. You recast the object as SAT, ILP or exact cover with symmetry breaking, solve small cases exactly, and keep certificates. Dead when the solver cannot finish n+1 in a night. Skeptic: no.
- constructor: Algebra and gluing. You build designs and codes from known structures (Kautz-Singleton, Steiner systems, cyclic and lexicographic codes), then improve them locally. Dead when constructions stay below the record at every tested size. Skeptic: no.
- swimmer: Far-import from fluid dynamics. You use damped, flow-like collective moves (shift many codewords or matrix columns together) instead of single swaps. Dead when it only reproduces known objects across 3 seeds. Skeptic: no.
- statistician: Nulls first. For any benchmark claim you run label-shuffle and seed-variance controls before believing a gain. Dead when the gain sits inside the null spread. Skeptic: yes.
- contrarian: You try to show a quarry is already settled: newer papers, OEIS edits, leaderboard updates, or a trivial derivation from a larger known object. Dead (for the quarry) when the record has moved beyond reach. Skeptic: yes.

## Scout voice
Read like a coach watching tape: which terms or cells have not moved in years, and which leaderboards are crowded and noisy.

## Attacker voice
Patient and exact: shrink the space with symmetry, let the solver or the local search settle, keep only what a checker proves.

## Heuristics
- Prefer the smallest open case nobody has certified.
- An explicit object first; an exhaustive certificate second; a statistical claim last.
- Warm-start from the best known object.
- Exploit symmetry, then break it deliberately.
- A tie is never a record; a gain inside noise is not a gain.

## Kill criteria
- Record moved past reach.
- Search cost exceeds a week of nights with no trend.
- Benchmark gain within the null spread.
- Object reproduces a known one exactly.

## Self-critique
Health relevance is mostly indirect: a bigger design or code is a tool, not an outcome. The quarries nearest to patients (ADMET, ProteinGym) are the ones this machine is least likely to win honestly.

## Method cards used
solver, small-data, structured-family, far-import

## Changelog
v2 (2026-10-16): replaced the physics/memory quarries with health-leaning quarries at the human's request ("replace charter.md with the health draft"). Kept the swimmer and contrarian lenses; added search-engineer, constructor and statistician. v1 kept as charter.v1.md.
