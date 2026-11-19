# Research charter v2 (2026-11-15)

## Thesis
Combines deep fluency in AI/transformer internals and computer systems with an uncommon bridge between discrete game-engine simulation and quantum-information geometry. Rather than tuning black-box models or chasing crowded leaderboards, this charter treats open math, quantum, and algorithmic questions as concrete state-space puzzles—building fast exact evaluators first, importing physics-engine and SAT/SDP solver techniques, and hunting for surprising minimal objects or clean counterexamples that settle old questions.

## Quarries

- **id:** `adderboard-smallest-adder-transformer`
  **question:** Can an autoregressive transformer with fewer than 36 unique parameters add two 10-digit integers at ≥99% accuracy on `verify.py`?
  **shape:** record
  **where defined:** Bank entry `adderboard-smallest-adder-transformer` (`github.com/anadim/AdderBoard`)
  **status to confirm first:** Latest commit and current parameter-count leaders on `anadim/AdderBoard` README (both trained and hand-coded boards).
  **why us:** Treats the transformer as a minimal bit/digit circuit with circular-arc geometry and weight-tying rather than standard deep-learning scaling.
  **weight:** 5
  **wild:** no

- **id:** `game-of-sloanes-complex-line-packings`
  **question:** Can we find complex line packings in $\mathbb{C}P^{d-1}$ that beat the best-known maximum coherence on the Game of Sloanes table?
  **shape:** record
  **where defined:** Bank entry `game-of-sloanes-complex-line-packings` (Jasper, King, Mixon — Game of Sloanes)
  **status to confirm first:** Current best coherence values for target $(d, N)$ cells in the Game of Sloanes repository.
  **why us:** Bridges quantum state geometry with repulsive-particle physics-engine simulation and Riemannian optimization.
  **weight:** 4
  **wild:** no

- **id:** `life-smaller-orphan`
  **question:** Does there exist a Conway's Game of Life orphan with bounding-box area strictly below 96 (or an UNSAT certificate ruling out a new box size with height ≥ 5)?
  **shape:** existence / bound or proof
  **where defined:** Bank entry `life-smaller-orphan` (LifeWiki Garden of Eden page)
  **status to confirm first:** Smallest known orphan area and ruled-out box dimensions on LifeWiki.
  **why us:** Applies cellular-automaton game-state intuition paired with modern SAT encodings and symmetry breaking.
  **weight:** 4
  **wild:** no

- **id:** `etp-finite-magma-677-255`
  **question:** Can we settle either of the last two open finite-magma implications in the Equational Theories Project (`Eq677 => Eq255` or `Eq2910 => Eq47`) via a finite counterexample magma or a machine-checkable proof?
  **shape:** counterexample / bound or proof
  **where defined:** Bank entry `etp-finite-magma-677-255` (Equational Theories Project `finite_outcomes.json.gz`)
  **status to confirm first:** Whether `Equation677 => Equation255` and `Equation2910 => Equation47` remain `unknown` in the ETP dashboard and open issues.
  **why us:** Reduces an abstract algebraic conjecture to fast finite-table search, SAT/Mace4 model-finding, and orbit-symmetry pruning.
  **weight:** 4
  **wild:** no

- **id:** `grothendieck-kg3-werner-locality-bounds`
  **question:** Can we tighten the upper bound on Grothendieck's constant $K_G(3)$ / Werner state locality threshold via symmetric measurement polytopes on $S^2$?
  **shape:** bound or proof
  **where defined:** Bank entry `grothendieck-kg3-werner-locality-bounds`
  **status to confirm first:** Current best certified upper bound on $K_G(3)$ and Werner locality threshold in the literature.
  **why us:** Combines quantum nonlocality geometry with spherical-design game-mesh intuition and exact QUBO/SDP local-bound certification.
  **weight:** 3
  **wild:** no

- **id:** `langton-ant-highway`
  **question:** Does there exist a finite initial configuration of black cells for Langton's ant that provably never enters the period-104 diagonal highway?
  **shape:** counterexample
  **where defined:** Bank entry `langton-ant-highway`
  **status to confirm first:** Confirm the highway conjecture remains open.
  **why us:** Pure discrete-simulation moonshot looking for a surprising self-sustaining non-highway attractor or oscillator.
  **weight:** 2
  **wild:** yes

## Lenses

- **key:** `evaluator-first`
  **title:** Fast Exact Evaluator & Bit-Level Loop
  **text:** Before searching, build the fastest possible exact evaluator in C, Numba, or vectorized NumPy and benchmark its throughput. Treat the search space like a real-time engine tick: optimize memory layout, bit-pack states, and measure candidates per second before trying clever heuristics.
  **skeptic:** no

- **key:** `solver-reduction`
  **title:** Constraint & SAT/SDP Reformulation
  **text:** Recast the target from an ad-hoc search into a clean SAT, SMT, MILP, or SDP instance with explicit symmetry-breaking predicates. Let an exact solver argue over small-to-medium instances and produce verifiable certificates or UNSAT proofs.
  **skeptic:** no

- **key:** `physics-geometry`
  **title:** Repulsive Potential & Manifold Annealing
  **text:** View discrete or algebraic configurations as particles interacting on a continuous manifold (unit spheres, $\mathbb{C}P^{d-1}$, or circular arcs). Minimize a smooth surrogate potential with Riemannian L-BFGS or simulated annealing, then project or polish onto the exact constraint set.
  **skeptic:** no

- **key:** `circuit-minimalism`
  **title:** Minimal-Circuit & Representation Shift
  **text:** Strip the problem to its smallest possible representation—shared weights, low-rank bases, periodic embeddings, or quotient orbits. Ask what structure a minimal winning object *must* have, and search only the space of those constructions.
  **skeptic:** no

- **key:** `colab-gpu-solver`
  **title:** Cloud GPU & CDCL Solver Offload (Google Colab)
  **text:** When local CPU/stdlib is not enough (e.g. PyTorch training on AdderBoard, Riemannian GPU optimization on complex line packings, or CaDiCaL/Kissat + DRAT proofs on Life orphans and ETP magmas), write a self-contained script locally in `code/`, offload execution to a Google Colab notebook via the browser subagent, and bring back verbatim outputs and verifiable weights/certificates.
  **skeptic:** no

- **key:** `skeptic-adversary`
  **title:** Skeptic: Triviality, Saturation & Null Check
  **text:** Assume the current lead is either already solved in an overlooked issue, an artifact of a loose evaluator, or no better than 400+ random/shuffled controls. Try to break the evaluator on known negative cases and verify the primary source before trusting any promising signal.
  **skeptic:** yes

## Scout voice
Read primary sources and repositories as raw engineering specs, not hype. First check whether an open issue, recent commit, or arXiv preprint already closed the target or raised the bar. Extract the exact mathematical definition, scoring script, and hardware/memory footprint of a single evaluation before committing a run's budget.

## Attacker voice
Patient, skeptical, and concrete. Prefer one clean, fast, reproducible experiment over ten speculative sketches. Log exact seeds, timings, and negative controls; treat a crisp negative result or an UNSAT boundary as real progress, never as a reason to stop early.

## Heuristics
- Always build and test the exact checker on one known positive and one known negative example before starting any search.
- Measure memory and runtime on a tiny slice first; never launch parallel workers that exceed half of free RAM.
- For continuous/quantum packings, pair smooth surrogate optimization with exact algebraic or active-set polishing.
- For finite combinatorics and cellular automata, exploit dihedral/orbit symmetries early to collapse the search factor.
- Keep checkpoints every few minutes so multi-run searches accumulate coverage across sessions.
- For minimal neural/transformer targets, test weight-tying and analytical parameterizations alongside gradient descent.

## Kill criteria
- Primary source or leaderboard confirms the exact target cell/question is already solved or superseded.
- Exact evaluation of a single candidate exceeds available RAM or cannot reach meaningful sample counts within the run budget.
- 400+ null/random controls match or beat the best observed candidate under the frozen `PREREG.md` metric.
- Verification requires proprietary data, gated login, or non-reproducible hardware not available locally.

## Self-critique
This charter leans heavily on finite-state search, SAT/optimization, and small-scale geometry, which risks spreading effort too thin across six quite different targets or hitting hard combinatorial walls on moonshots like `langton-ant-highway` and `etp-finite-magma-677-255`. Keeping `adderboard-smallest-adder-transformer` and `game-of-sloanes-complex-line-packings` at higher weights balances moonshots with tractable, fast-feedback targets, provided each run commits to one quarry and builds an exact evaluator before searching.

## Method cards used
- `evaluator-first`
- `representation`
- `solver`
- `symmetry`
- `counterexample-shape`
- `far-import`

## Changelog
- **v2 (2026-11-15):** Added `colab-gpu-solver` lens to offload PyTorch/GPU and CDCL SAT/DRAT computations to Google Colab via the browser subagent, paired with `intra` / `extra` looping modes in `RUN.md`.
