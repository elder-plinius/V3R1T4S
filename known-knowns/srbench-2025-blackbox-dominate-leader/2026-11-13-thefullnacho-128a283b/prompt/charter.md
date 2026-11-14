# Research charter v1 (2026-11-02)

## Thesis
Seeds were drawn at random: categories machine-learning and crypto-math, method cards construct-space, brute-scale, backwards. The edge is a small patient machine: one 4-core box, an hour a night, an exact checker built first, and a search that constructs rather than guesses. The crowd reaches for GPUs and famous problems; this charter hunts small checkable records a CPU can actually verify.

## Quarries
1. **mnist-smallest** — id `smallest-mnist-99-percent-network`. Question: what is the smallest parameter count of a network scoring >= 99.00% on official MNIST test (plain argmax, no augmentation, no ensembling)? Shape: record (explicit object beating a published table value). Defined in: bank entry, status source https://raw.githubusercontent.com/JoshWarn/Parameter-Efficient-MNIST/main/README.md. Status to confirm first: re-fetch the record live; count conservatively (every number in the forward pass that is not a universal constant). Why us: tiny exact construction on a CPU box; evaluator-first edge. Weight 5. Wild: no.
2. **srbench-one-dataset** — id `srbench-2025-blackbox-dominate-leader`. Question: for one named SRBench 2025 black-box dataset, can a closed-form expression beat the best median test R^2 over the 30 official splits? Shape: record. Defined in: bank entry, status source https://github.com/cavalab/srbench/tree/srbench_2025/results/black-box-tuning. Status to confirm first: re-fetch the leader for the chosen dataset; confirm split protocol (train_size 0.75, listed seeds, training subsampling rule). Why us: small exact expressions; construct-space + backwards. Weight 4. Wild: no.
3. **fev-one-task** — id `fev-bench-beat-best-task-sql`. Question: for one named fev-bench task, can a laptop-scale forecast with open-weight local models and classical methods (training data not including the task's dataset) beat the best fev-computed test_error? Shape: record. Defined in: bank entry, status source https://github.com/autogluon/fev/tree/main/benchmarks/fev_bench/results. Status to confirm first: re-fetch all result CSVs live; pick the task with the stalest bar. Why us: laptop-scale is the design constraint, not a handicap. Weight 4. Wild: no.
4. **noise-track1** — id `noise-backprop-free-pretraining-records`. Question: can a training script obeying the no-autograd, no-hand-written-backward rules (seed 0, one epoch, only data/train.pt) beat the live Track-1 validation loss record on the pinned data/val.pt? Shape: record. Defined in: bank entry, status source https://raw.githubusercontent.com/qlabs-eng/noise/main/README.md. Status to confirm first: re-read the README rules live; confirm the current record (3.338 on 2026-10-30) and any lower claim in an open PR. Why us: small model, exact rules, patience over brute force. Weight 3. Wild: no.
5. **m4-overall** — id `m4-competition-beat-nbeats-owa`. Question: can saved point forecasts for all 100,000 M4 series at official horizons beat N-BEATS-I+G overall OWA 0.795 with test-free training? Shape: record. Defined in: bank entry (arXiv:1905.10437 Table 1), status source https://arxiv.org/abs/1905.10437. Status to confirm first: confirm no lower credible post-2020 OWA for a test-free method; confirm the leak rule (frozen hashed script, rerun in a fresh environment). Why us: patience — one series family per night, classical methods the crowd abandoned. Weight 2. Wild: yes.

## Lenses
1. **constructor** — Build the object from parts: glue small verified pieces, then local-search around them. First moves: enumerate the smallest working pieces; combine two; measure. Dead when: no combination beats the current best after a full night of gluing.
2. **brute-scale** — The plainest method that could work, at a scale nobody bothered with. First moves: write the dumbest correct search; run it wider than anyone would by hand; checkpoint. Dead when: the scaling curve flattens below the bar with compute to spare.
3. **backwards** — Work back from what a winning object would have to look like. First moves: state the winner's necessary properties; search only where they hold; prove the rest impossible. Dead when: the necessary properties contradict each other.
4. **small-cases** — Solve tiny cases exhaustively, tabulate, find the pattern, lift it. First moves: smallest non-trivial case; full table; look for the regularity. Dead when: the pattern breaks at the next size with no repair.
5. **smuggler** — Import a technique from a distant field and make it do real work here. First moves: name the foreign method and the exact step it replaces; run it on the smallest case. Dead when: the import performs no better than the native method on the small case.
6. **skeptic** — Try to show the quarry is already settled, trivial, or ill-posed. First moves: re-fetch the table; search the last 24 months; attempt the trivial construction. Dead when: the quarry survives the attack (that is the lens succeeding by failing).

## Scout voice
Read like a clerk, not a fan: quote the table value, the URL, the fetch time. Distrust any status you did not read yourself. A solved target is a gift — it saves a night.

## Attacker voice
Patient, exact, unsentimental. Build the checker before the search. Prefer the construction you can explain over the accident you cannot reproduce. A clean negative with the covered space stated is a good night; a loud "found it" without a panel is a failure.

## Heuristics
1. Evaluator first: no search runs before the checker passes one positive and one negative case.
2. Smallest case first: prove the pipeline on the tiniest input, then scale.
3. One quarry per run; two lenses, both running real code.
4. Checkpoint every few minutes; record the PID; kill only that PID.
5. Re-fetch the live table immediately before any claim.
6. Null-test every search or statistical claim on at least 400 controls.
7. Dedupe before panelling: one carrier per object.
8. When in doubt, the cheaper decisive test runs first.

## Kill criteria
1. The target is solved or the record moved past reach (evidence in target.md).
2. The success criterion cannot be read from a primary source.
3. The compute needed exceeds a week of light nights on this box.
4. The baseline cannot be reproduced and the comparison is unresolved after diagnosis.
5. Three documented dead lines with no live lead.
6. The claim would need an outward action (login, signup, contact) to verify.

## Self-critique
This charter most likely fools itself in three ways: (1) the random seeds point at crowded categories, and the anti-collision filter may have kept the wrong obvious pick; (2) light effort on a 4-core box may be too small for every quarry except the MNIST one, so most nights will be clean negatives — which is fine, but the charter should not pretend otherwise; (3) "patience" as a strategy only pays if dossiers actually accumulate, so a run that does not update its dossier has failed even if it attacked. The skeptic lens exists to catch (1); the kill criteria exist to catch (2); the dossier is the check on (3).

## Method cards used
construct-space, brute-scale, backwards (drawn at random from the kit's list).
