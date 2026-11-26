# Research charter v5 (2026-11-23)

**Next new target (human, 2026-11-23):** quarry 1, `dna-codes-gc-king-table`. Keep working quarry 15
(`regular-graph-counts-next-order`) as long as it has a live lead; when it has none, take quarry 1 as the next
`mode: new` target, ahead of the weights. Its dossier from 2026-10-18 still applies; read the reading pack named in
its hint first.

## Thesis

The first seeds were random (undeciphered scripts, biology; method cards invert, solver, obstruction-first); physics
and disease research were added by choice. The edge is patience on a small machine: an hour-long session to build
the code and about 23 hours of two cores and 3 GB to run it, every night, months on end. So the charter favours
exact, constraint-shaped questions, old tables that have sat still, digits and counts a transfer matrix can push one step further each night, and small public benchmarks a CPU can
score honestly.

## Quarries

1. **id:** dna-codes-gc-king-table
   **question:** an explicit quaternary code with constant GC content, length n, minimum distance d, strictly larger
   than an unmarked entry of King's A_4^GC(n,d,w) table.
   **shape:** record. **where defined:** bank entry `dna-codes-gc-king-table`; O. King, "Bounds for DNA codes with
   constant GC-content", Electronic Journal of Combinatorics 10 (2003) R33.
   **status to confirm first:** the live table and any 2024-2026 papers that improved its entries.
   **why us:** a table last updated in 2010, small parameters, and a natural fit for clique/ILP solvers seeded with
   group-invariant codes; nightly runs can sweep (n,d) cells one by one. **weight:** 5. **wild:** no.
   **reading (human, 2026-11-23):** `work/handoff/dna-codes-lit/` (start with `README.md`): `IDEAS.md` (status of
   the table, ranked constructions and searches, optimality proofs, checks, gaps), `STATUS.md` (values reported in
   the literature vs King's table), `DIGEST.md` and `cards/` (77 papers), King's page as fetched 2026-11-23. Cards
   are model summaries: check the cited table or theorem in the paper before relying on it.
   **hint (human, 2026-11-23):** checked by the human: King's own table has GC < 2 x GC,RC at (15,11) (34 vs 2 x 18)
   and (19,9) (7038 vs 2 x 3678); a strict RC code C gives the GC code C ∪ C^rc. The page links no codes for these
   cells, so the code has to be built (a group containing rc, e.g. dihedral orbits) or found. The averaging bound
   already makes (15,12)=15 and (20,16)=16 optimal and caps (14,11) at 21 and (19,15) at 19. Prime-length cells
   ((19,15), (13,10), (17,13), (11,8), (13,9)) need only a few cyclic or dihedral orbits to beat the table.
   From the full texts (`HUMAN_CHECK.md`): the record already moved at (10,6) (144, Smith et al. 2011) and (20,4)
   (378896384); the table's values were found at w in n/2-1 .. n/2+1, while the bank fixes w = floor(n/2);
   doubling Aboluion et al. 2012's published RC codes would give (16,8) 7552 and (16,11) 136, but that is close to
   a trivial edit of a published object.

2. **id:** burnt-pancake-even-n-exact-flips
   **question:** for an even n not yet decided, does the all-burnt sorted stack need 3n/2+1 or 3n/2+2 flips?
   **shape:** existence (an explicit sequence of 3n/2+1 flips) or exhaustive-search certificate.
   **where defined:** bank entry `burnt-pancake-even-n-exact-flips`; OEIS A078942; Jager and Oijid, arXiv:2601.09447.
   **status to confirm first:** which even n the live OEIS entry and its references already settle.
   **why us:** a pure search problem where backward search from the target shape and strong pruning bounds matter
   more than hardware. **weight:** 4. **wild:** no.

3. **id:** hp-lattice-folding-benchmark-energies
   **question:** a self-avoiding 3D cubic conformation of a long benchmark chain with energy strictly below the best
   published value.
   **shape:** record. **where defined:** bank entry `hp-lattice-folding-benchmark-energies`; Thachuk, Shmygelska and
   Hoos, BMC Bioinformatics 2007; Wüst and Landau, arXiv:1301.3466.
   **status to confirm first:** later papers reporting lower energies for 3D103, 3D124, 3D136.
   **why us:** checkpointed annealing or replica search can run a little further every night; an exact core-packing
   bound can also show where no improvement is possible. **weight:** 3. **wild:** no.

4. **id:** linear-a-kuro-arithmetic
   **question:** fraction-sign values that reconcile the fully preserved KU-RO totals, tested as a frozen assignment.
   **shape:** decipherment or prediction, judged by the bank's success criterion.
   **where defined:** bank entry `linear-a-kuro-arithmetic`; Corazza, Ferrara, Montecchi, Tamburini and Valério,
   Journal of Archaeological Science 125 (2021) 105214.
   **status to confirm first:** any 2024-2026 work on Linear A fraction values; the current SigLA corpus state.
   **why us:** the question is a small integer-constraint problem; a solver can enumerate every consistent value
   system, and an infeasibility proof for a section is a result in itself. **weight:** 3. **wild:** no.

5. **id:** proto-elamite-accounting-balance
   **question:** a deterministic, low-parameter rule for numeral-system assignment that reconciles held-out
   obverse/reverse totals better than current readings.
   **shape:** decipherment or prediction, judged by the bank's success criterion.
   **where defined:** bank entry `proto-elamite-accounting-balance`; Born, Monroe, Kelley and Sarkar (2025).
   **status to confirm first:** the CDLI data release in use and any newer computational studies.
   **why us:** tablet arithmetic is a constraint system; the solver card fits, with a held-out split frozen first.
   **weight:** 2. **wild:** no.

6. **id:** voynich-generator-heldout-fingerprints
   **question:** a manually executable generator that matches the held-out structural fingerprints listed in the bank
   entry, per Currier dialect, on both transcriptions.
   **shape:** existence of a generator, judged by the bank's success criterion.
   **where defined:** bank entry `voynich-generator-heldout-fingerprints`; Greshko, Cryptologia (2025); Parisel,
   arXiv:2604.25979; Rozanova and Temerev, arXiv:2608.17096.
   **status to confirm first:** any 2026 generator claiming the same fingerprints.
   **why us:** the invert card: build the generator from the statistics it must fail first, and learn from what
   breaks. **weight:** 1. **wild:** yes.

7. **id:** site-percolation-2-uniform-lattices-thresholds
   **question:** site percolation thresholds of the 2-uniform tilings to more digits than the published 2e-4.
   **shape:** record (a value with a certified or statistically justified error bar, judged by the bank criterion).
   **where defined:** bank entry `site-percolation-2-uniform-lattices-thresholds`; Neher, Mecke and Wagner,
   J. Stat. Mech. (2008), arXiv:0708.3250 and arXiv:0708.3251.
   **status to confirm first:** any newer remeasurement of the 2-uniform site column.
   **why us:** exact transfer-matrix critical polynomials on tori, extended one width per night; Monte Carlo
   (Newman-Ziff) only as a cross-check.
   **weight:** 0 (closed 2026-11-13, see the dossier HANDOFF). **wild:** no.

8. **id:** kings-hard-core-entropy-a247413-digits
   **question:** more correct digits of the entropy constant of the hard-core king lattice gas (OEIS A247413).
   **shape:** record (certified digits beyond the OEIS entry).
   **where defined:** bank entry `kings-hard-core-entropy-a247413-digits`; OEIS A247413; Liang, arXiv:2505.12776.
   **status to confirm first:** the live OEIS entry and any newer tensor-network computation.
   **why us:** a large transfer-matrix gap at unit activity; corner-transfer-matrix or boundary-MPS iterations can be
   resumed from a checkpoint. **weight:** 3. **wild:** no.

9. **id:** square-grid-lattice-gas-exact-counts-oeis
   **question:** new exact terms of the n x n lattice-gas counting sequences listed in the bank entry (A028420,
   A006506, A063443, A054759, A027683).
   **shape:** record (exact integers, checked by an independent modular recomputation).
   **where defined:** bank entry `square-grid-lattice-gas-exact-counts-oeis`; the OEIS entries and their b-files.
   **status to confirm first:** the live b-file length of each sequence.
   **why us:** column transfer matrices with modular arithmetic and Chinese remaindering; each prime is a separate,
   resumable night of work. **weight:** 4. **wild:** no.

10. **id:** eaqecc-qutrit-codetables-gaps
    **question:** an entanglement-assisted qutrit code [[n,k,d;c]]_3 that raises a lower bound in Grassl's table.
    **shape:** record (an explicit code whose parameters a checker recomputes).
    **where defined:** bank entry `eaqecc-qutrit-codetables-gaps`; Luo, Ezerman, Grassl and Ling, arXiv:2207.05647.
    **status to confirm first:** the table's last-change date and the current bounds for the chosen cells.
    **why us:** the solver card: small n cells, structured families (cyclic, quasi-cyclic) searched exhaustively.
    **weight:** 3. **wild:** no.

11. **id:** pycox-metabric-gbsg-breast-cancer-survival
    **question:** a survival model that beats the published time-dependent concordance on METABRIC or GBSG under the
    benchmark's fixed protocol.
    **shape:** record (a score on a fixed public protocol, judged by the bank criterion).
    **where defined:** bank entry `pycox-metabric-gbsg-breast-cancer-survival`; Kvamme, Borgan and Scheel, Journal of
    Machine Learning Research 20(129) (2019).
    **status to confirm first:** later papers reporting higher C_td on the same protocol.
    **why us:** tiny data, minutes per fit on a CPU; the edge is careful protocol hygiene, not compute.
    **weight:** 3. **wild:** no.

12. **id:** iedb-mhci-bd2009-blind-auc
    **question:** a peptide-MHC class I binding predictor trained only on BD2009 that beats the reference methods'
    AUC on the Blind set.
    **shape:** record (per-dataset AUC on a frozen public benchmark, judged by the bank criterion).
    **where defined:** bank entry `iedb-mhci-bd2009-blind-auc`; Kim, Peters, Nielsen et al., BMC Bioinformatics 15:241
    (2014).
    **status to confirm first:** the benchmark archive's current tables.
    **why us:** a frozen benchmark with genuinely later test data; small models trained on a CPU.
    **weight:** 2. **wild:** no.

13. **id:** tdc-drugcomb-css-mae
    **question:** a model that beats the leaderboard MAE on TDC DrugComb_CSS under TDC's prescribed protocol.
    **shape:** record (MAE over five runs via the benchmark group's evaluator).
    **where defined:** bank entry `tdc-drugcomb-css-mae`; Therapeutics Data Commons DrugCombo benchmark group.
    **status to confirm first:** the live leaderboard entries.
    **why us:** a thin leaderboard with one entry; tabular models with drug and cell-line features fit on a CPU.
    **weight:** 3. **wild:** no.

14. **id:** flusight-retrospective-beat-ensemble-wis
    **question:** a forecaster that beats the FluSight ensemble's weighted interval score on a completed season,
    with every forecast made from data available at its reference date.
    **shape:** record (WIS on a frozen completed season, judged by the bank criterion).
    **where defined:** bank entry `flusight-retrospective-beat-ensemble-wis`; CDC FluSight forecast hub and its
    evaluation reports.
    **status to confirm first:** the hub's latest evaluation report for the chosen season.
    **why us:** small public data and CPU-only scoring; the edge is strict as-of-date discipline.
    **weight:** 2. **wild:** no.

15. **id:** regular-graph-counts-next-order
    **question:** the number of connected unlabeled cubic graphs on 42 vertices, A002851(21), the first term beyond
    Robinson and Wormald (1983); then the next terms of A002851 and, if the method carries over, of A006821,
    A006822, A014377.
    **shape:** exact count, two independent methods or implementations that agree exactly (bank criterion).
    **where defined:** bank entry `regular-graph-counts-next-order`; OEIS A002851; Robinson and Wormald, "Numbers of cubic
    graphs", J. Graph Theory (1983); Cheng and Xu, arXiv:2609.31407 (quartic, orders 29-50).
    **status to confirm first:** the live A002851 (DATA ends at 2n = 40 on 2026-11-13, no b-file)
    and any 2026 paper that counts cubic graphs beyond 40 vertices.
    **why us:** an exact integer, no error bars; the count comes from symmetry (cycle-index / Burnside) formulas, not
    from generating the graphs, and nobody is working on the cubic case (no upstream PR, no 2026 paper as of
    2026-11-13). Reproduce every published term to 2n = 40 first.
    **hint (human, 2026-11-13):** compute everything modulo several ~61-bit primes and recover the answer with the
    Chinese remainder theorem; division by 42! and the inverse Euler transform both work mod p > 42.
    Use enough primes to exceed the labeled count (~1e72 at 42 vertices: 5 primes), one prime per night
    if needed, plus one extra prime as a check. This worked well for the domino-tiling counts.
    Method 1: Cheng-Xu PARI code run for degree 3. Method 2: own Howroyd-style program (labeled graphs
    fixed by each cycle type), written without looking at Cheng-Xu's code.
    Keep the by-products: for every order N computed, save a table (CSV, next to the code) with one row per
    cycle type: N, the cycle type, the number of permutations of that type, and the number of labeled cubic
    graphs that permutation fixes. Exact integers where cheap (small N), otherwise residues with their prime.
    A later phase will search these tables for patterns, so they must be complete and documented.
    Also record the wall time and peak memory of each method for every N, so the growth of the cost can be
    extrapolated to larger N.
    **reading (human, 2026-11-13):** `work/handoff/regular-graph-counts-lit/`: `IDEAS.md` (concrete leads for a
    second method and for later speed-ups, checks, gaps), `DIGEST.md` (papers by direction), `cards/` (one card per
    paper read, with theorem/equation numbers). Cards are model summaries: check the cited equation in the paper
    before relying on it. The key gap is Robinson-Wormald 1983 itself (paywalled, only the abstract was read).
    **weight:** 6. **wild:** no.

## Lenses

1. **key:** solver-first. **title:** Let the solver argue. **skeptic:** no.
   Recast the quarry as SAT, ILP or exact cover before writing any heuristic. First moves: write the exact model,
   solve the smallest open instance, measure the time growth. Dead when the model at the target size does not finish
   inside the run budget even with symmetry breaking.

2. **key:** obstruction-hunter. **title:** Find what forbids it. **skeptic:** no.
   Look for the invariant, counting bound or parity argument that would forbid the target, and search only where it is
   silent. First moves: list known bounds, compute them for the open cells, rank cells by slack. Dead when the bounds
   leave no slack anywhere you can reach, which you then state as a negative result.

3. **key:** inverter. **title:** Learn from the worst. **skeptic:** no.
   Invert the objective: build the worst codes, folds, flip sequences or generators on purpose and study what they
   lack. First moves: generate a worst-case family, compare it with the best known object, turn the difference into a
   search constraint. Dead when the inverted objects show no structure the best ones use.

4. **key:** nightly-extender. **title:** One more step every night. **skeptic:** no.
   Take the strongest published computation and push it a little further each run, with a checkpoint that the next run
   resumes. First moves: reproduce the published value, write the checkpoint format, record throughput. Dead when the
   projected time to beat the record exceeds a month of nights.

5. **key:** oldest-paper. **title:** Read the first source. **skeptic:** no.
   Start from the oldest source on the question and look for constructions or readings that were dropped, not refuted.
   First moves: find the original paper or edition, list its unused ideas, test the cheapest one. Dead when every idea
   was tested in later literature.

6. **key:** settled-skeptic. **title:** Is it already settled? **skeptic:** yes.
   Try to show the quarry is already solved, trivial, ill-posed or out of reach for this machine. First moves: search
   for the latest result, recompute the claimed open values, check the definition for loopholes. Dead when the quarry
   survives all three checks; then it is a fair target.

## Scout voice

Read every table and paper for the exact definition and the date of its last change. Prefer the primary source, note
what has stayed still for years, and treat any claim of optimality as a lead to check, not a fact.

## Attacker voice

Calm and exact. Start with the smallest instance that is still open, write the checker first, let a solver do the
arguing, and keep every partial computation resumable for the next night.

## Heuristics

- Exact model first, heuristic second.
- An infeasibility proof is a result; write it down as one.
- Symmetry shrinks the search; impose it, then break it on purpose.
- Prefer cells that have not moved in years.
- Checkpoint every few minutes; the next run must resume, not restart.
- One cell, one object, one claim.
- For scripts, freeze the held-out split and the rule before looking at the held-out data.
- This machine is small: the session has 1 h and 3 GB, the worker 2 cores, 3 GB and ~23 h. Run any heavy program
  under an address-space cap, e.g. `prlimit --as=2800000000 -- nice timeout <cap> <cmd>` (for Java, Go or similar
  runtimes set their own heap limit instead), so it fails with an out-of-memory error rather than taking the
  session or the job down. A line stopped by this machine's limits, not by the mathematics, is a live lead, never a
  dead line. It may be marked `needs bigger machine: <RAM> / <cores> / <hours> (estimated from <measurement>)` in
  the dossier and under "Needs you", with the resume command and the checkpoint path, only after every "Fit the
  machine" option in `kit/RUN.md` is estimated and none fits.

## Kill criteria

- The target cell or value moved since the bank entry and is now out of reach.
- The exact model would not finish at the target size in reasonable time even on a much larger machine, and no
  reduction is known. Running out of this machine's memory or time alone is not a kill.
- A null test shows the pattern appears in shuffled controls.
- The success criterion needs data whose terms the human has not accepted.
- Two consecutive runs on the same quarry produce no new covered space, no new lead and no gain on the target's own
  measure (digits, terms, width, error bar).

## Self-critique

The random seeds may pull the runs toward problems where two cores and one hour are not enough; the solver card can
hide that cost until late in a run. The script quarries risk drifting into readings that cannot be scored, which the
bank criteria forbid. The record quarries risk tying a table entry and calling it progress. The benchmark quarries
(survival, MHC binding, drug combinations, flu forecasts) risk tuning on the test split or leaking future data; model
choice must be frozen on training and validation data only, and the test split scored once. With 14 quarries, more
than the kit's usual 3-8, attention spreads thin; the weights, not the list length, decide what gets nights.

## Method cards used

invert, solver, obstruction-first (drawn at random).

## Changelog

- v2 (2026-10-17): lines blocked by this machine's resources are recorded as live leads with a resource estimate
  instead of being dropped; heavy programs run under a memory cap so the session survives them; the matching kill
  criterion now requires the model to be out of reach on a much larger machine too.
- v3 (2026-10-17): the human added eight quarries from physics (percolation thresholds, king lattice-gas entropy,
  exact lattice-gas counts, qutrit EAQECC codes) and disease research (breast-cancer survival, MHC-I binding, drug
  combinations, flu forecasting), knowingly going past the kit's 3-8 quarry range; thesis and self-critique updated.
- v4 (2026-11-13): the human closed quarry 7 (2-uniform percolation): the main criterion and both partial wins are
  taken by others (upstream PR #391, PR #239, Elisov arXiv:2610.31190). The human added quarry 15 (cubic graph
  counts) and made it the next new target.
- v5 (2026-11-23): quarry 15 continues while it has a live lead; quarry 1 (DNA codes) is the next new target after
  it, with a reading pack in `work/handoff/dna-codes-lit/` and a hint.
