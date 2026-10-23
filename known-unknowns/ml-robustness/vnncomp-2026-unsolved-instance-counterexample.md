# VNN-COMP 2026: a validated counterexample for a benchmark instance that no participating verifier solved

🛡️ **ML robustness** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours · open as of 2026-10-09

## The problem

VNN-COMP 2026 (results published in https://github.com/VNN-COMP/vnncomp2026_results, last pushed 2026-08-03; 13 tools: act, agate, alpha_beta_crown, bright, cora, n2v, neuralsat, nnenum, nnv, pyrat, sobolbox, super_simple_vnn_comp, vibecheck; 3,618 scored instance rows over 30 benchmarks, independently re-parsed by the vetter on 2026-10-09) left 127 instances that NO tool resolved: every tool returned timeout/unknown/error, and no validated counterexample exists. Parsed from SCORING/results.txt on 2026-10-09 they are: cifar100_2024 (40: CIFAR100_resnet_medium/large local robustness at eps 0.0039 = 1/255), tinyimagenet_2024 (22: TinyImageNet_resnet_medium, eps 1/255), challenging_certified_training_2026 (21: cifar10_eps2/eps8 cnn7 and wide_cnn7, tinyimagenet_eps1 cnn7), cora_2024 (27: mostly mnist-trades img0-19, plus cifar10 set/point/trades), traffic_signs_recognition_2023 (9: quantised QConv GTSRB nets, eps 1 and 3 in 0-255 pixel units), yolo_2023 (6: TinyYOLO eps 1/255), metaroom_2023 (1), ml4acopf_2024 (1). Each instance is an ONNX network plus a VNN-LIB property (input box + output constraints). Whether each is SAT (a counterexample exists) or UNSAT is open. Finding a counterexample is pure attack work (PGD and its variants on a small ONNX network, CPU-trivial per instance) and the competition's own validator (SCORING/cex_checks.py: replay with onnxruntime CPU, inputs within the box with atol 1e-4, replayed outputs authoritative) makes checking mechanical. Participating tools already ran cheap PGD before verification, so the easy cases are gone; what remains needs stronger search, which is exactly what this target asks for. The 2025 edition (VNN-COMP/vnncomp2025_results, SCORING-ZERO-TOL/results.txt) had 177 all-tool-unsolved instances, many of which (vit_2023, relusplitter) were later resolved as 'holds' in 2026, so 2025-only sets are stale and the 2026 table is the primary frontier. SEMANTICS (verified against SCORING/counterexamples_v2.py validate_vnnlib2_counterexample): a VNN-LIB file encodes the violation condition; the official validator declares a witness 'correct' iff EVERY assertion in the .vnnlib file holds at zero tolerance on the assignment (inputs as given, outputs replayed by onnxruntime CPU), 'correct_up_to_tolerance' iff they hold with input tolerance Settings.COUNTEREXAMPLE_ATOL = 1e-4, else 'spec_not_violated'. A 'counterexample' here means an assignment making all assertions true.

## What counts as a win

Success means a saved counterexample input vector (plain text, one value per line, VNN-COMP witness format) for one instance (ONNX file + .vnnlib file taken unmodified from https://github.com/VNN-COMP/vnncomp2026_benchmarks at the version directory (1.0 or 2.0) that a participating tool's results.csv in the live results repo names for that benchmark, sha256 of both files recorded) such that ALL of the following hold: (a) in the live SCORING/results.txt of https://github.com/VNN-COMP/vnncomp2026_results (re-fetched live immediately before claiming, never a cached copy) NO tool's cell for that instance's 'Row:' line contains '(h)' or '(v)' (the instance is in the all-tool-unsolved set computed by the skeptic's OWN parse of the live file), and no *.counterexample.check.json for it in any tool directory has result 'correct' or 'correct_up_to_tolerance'; (b) every input coordinate lies STRICTLY inside its vnnlib input bounds (lo < x_i < hi, zero tolerance), and when the ONNX model is run on the input with onnxruntime CPUExecutionProvider in float32, EVERY assertion in the .vnnlib file evaluates to true exactly as written under VNN-COMP semantics (i.e. the official validator's zero-tolerance check `_assertions_hold(query, assignment, 0.0, 0.0)` is satisfied), and on the satisfied branch of each output assertion every atomic comparison holds with a strict margin >= 1e-6 (|lhs - rhs| >= 1e-6 in the required direction); (c) the same holds after rounding the input to float32 and re-running, AND in a second runtime that is not onnxruntime (onnx2pytorch/torch or onnx.reference.ReferenceEvaluator), AND the competition's own SCORING/counterexamples_v2.py (run unmodified from the live results repo against the live benchmark files) returns 'correct' (not merely 'correct_up_to_tolerance'); (d) the instance is not from soundnessbench_2026 or test; (e) a live web search finds no previously published counterexample for that exact ONNX+vnnlib pair (if one exists the result is a replication, not a win). A 'holds'/UNSAT claim for an unsolved instance is never a success under this target.

## Partial wins

- **p1:** A counterexample for an all-tool-unsolved 2026 instance (same set as criterion (a), criteria (d)-(e) also required) that satisfies all vnnlib assertions only with the competition's official input tolerance (inputs within the box up to atol 1e-4, outputs replayed by onnxruntime CPU), i.e. the unmodified SCORING/counterexamples_v2.py returns 'correct_up_to_tolerance' but not 'correct'; confirmed in a second non-onnxruntime runtime.
- **p2:** A strict counterexample (criteria (b)-(e) of the full criterion) for an instance in the VNN-COMP 2025 all-tool-unsolved set (parsed by the skeptic from the live https://raw.githubusercontent.com/VNN-COMP/vnncomp2025_results/main/SCORING-ZERO-TOL/results.txt: no '(h)'/'(v)' in any cell of its 'Row:' line; 177 such rows on 2026-10-09 in cora_2024, ml4acopf_2024, relusplitter, tinyimagenet_2024, traffic_signs_recognition_2023, vit_2023) whose identical ONNX+vnnlib pair (same sha256 of both files) is either NOT present anywhere in the live vnncomp2026_benchmarks repo, or is present and still all-tool-unsolved in the live 2026 results.txt.

## How a win is checked

Skeptic writes their own checker without reading the attacker's code: download the named ONNX (.onnx.gz) and .vnnlib files from the vnncomp2026_benchmarks repo at the named version directory, verify sha256 against the attacker's manifest; parse the vnnlib (SMT-LIB subset: declare-const, assert, <=, >=, and, or) with their own parser; check every input coordinate strictly within its bounds; run onnxruntime (CPU, float32) on the input; evaluate EVERY assertion exactly as written and require all of them true (VNN-COMP semantics: the file encodes the violation; the witness must satisfy it) with margin >= 1e-6 on each output comparison of the satisfied branch; repeat in a non-onnxruntime runtime; then run the unmodified SCORING/counterexamples_v2.py from the live results repo and require 'correct'. Re-parse the live results.txt ('Row:' lines, no '(h)'/'(v)' in any cell) and grep the tool directories' *.check.json to confirm the instance is still all-tool-unsolved. Web-search the instance name for prior published counterexamples. Total time: minutes per instance.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://github.com/VNN-COMP/vnncomp2026_benchmarks>

## Sources

- <https://github.com/VNN-COMP/vnncomp2026_benchmarks>
- <https://github.com/VNN-COMP/vnncomp2026_results>
- <https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_results/main/SCORING/results.txt>
- <https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_results/main/SCORING/cex_checks.py>
- <https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_results/main/SCORING/counterexamples_v2.py>
- <https://github.com/VNN-COMP/vnncomp2025_results>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Massive-restart PGD/APGD directly on the ONNX graph (convert with onnx2pytorch or run gradients through onnxruntime-training/torch export), with margin losses targeting each output disjunct of the vnnlib property separately; the tools' built-in attacks use small restart counts under a time limit, this run can use hours per instance.
- Exploit the box structure: the cifar100/tinyimagenet/certified-training instances are eps=1/255 or 2/255 local-robustness boxes around a test image; search the box vertices (sign patterns) with coordinate-wise flipping and simulated annealing, since ReLU networks' extremes on a box are often at vertices; combine with gradient-free CMA-ES in the few hundred most sensitive pixels.
- Branch-and-attack: use interval/CROWN bounds (auto_LiRPA on CPU) to split the input box, discard sub-boxes proven safe, and concentrate PGD on the surviving sub-boxes where the lower bound on the margin is most negative; a counterexample found in a tiny sub-box is still a counterexample for the instance.
- For traffic_signs_recognition (quantised QConv nets, integer-valued pixel eps 1/3) search integer perturbations exhaustively over the highest-gradient pixels and use the network's quantisation to exploit threshold flips; for TinyYOLO (eps 1/255, 6 instances) target the specific output constraints in the vnnlib (bounding-box/objectness) with a margin loss rather than classification loss.
- cora_2024 mnist-trades img0-19 (27 unsolved out of the TRADES-trained MNIST set): these are small MLP/CNNs where exact MILP (Gurobi-free: use OR-Tools CP-SAT or SCIP via pyscipopt) on the ReLU network with the box constraints is CPU-feasible and either produces a counterexample or an exact proof; the counterexample part is the claimed object.
- Cross-check candidate counterexamples with float64 replay and with the competition's counterexamples_v2.py before claiming; prefer inputs with margin >> 1e-6 (push further inside the violated region along the gradient after finding one).

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- INVERTED SEMANTICS TRAP: do not look for inputs that make the vnnlib assertions FALSE. The official validator (counterexamples_v2.py) declares 'correct' iff all assertions in the file HOLD on inputs + replayed outputs; the file already encodes the unsafe region. Evaluate the file literally.
- Counterexample valid only in one runtime or only in float32/float64 but not both; rounding at ReLU thresholds can flip tiny-margin violations. Require strict margin and two runtimes.
- Input coordinates on or outside the box boundary (equality with bound is allowed by the vnnlib semantics but keep strictly inside for the full criterion), or using the wrong ONNX input shape/order (NCHW vs flattened) or the wrong version directory (1.0 vs 2.0 vnnlib spelling) of the benchmark.
- Misreading the vnnlib: VNN-LIB properties are 'violation conditions' (the assertion describes the unsafe output region) in some benchmarks and 'safety conditions' in others; the skeptic must evaluate the file exactly as written using the competition's semantics (counterexamples_v2.py), not an informal reading.
- The instance was not actually unsolved: a tool may have a validated counterexample in its directory (check *.counterexample.check.json) even if the aggregate line is unclear; re-parse the live results.txt and the tool directories, not a cached copy.
- soundnessbench_2026 instances have planted counterexamples that may be public (SoundnessBench HF dataset); they are excluded. Likewise 'test' benchmark.
- Claiming 'holds' (UNSAT) for an unsolved instance: that is a verification claim, not an attack result, and is not checkable by a skeptic in under an hour unless an independently reproducible exact method (e.g. MILP with a certificate) is provided; it is not part of this target's criteria.
- The only 2026 rows where a '(v)' claim was rejected by the validator and no tool returned '(h)' are in soundnessbench_2026 (excluded); every other rejected claim (agate 'malformed_ce', neuralsat/nnenum 'spec_not_violated') sits on a row another tool resolved. There is therefore no 'rejected-claim-only' partial win on the live table; do not invent one.
- The 127 figure describes the competition log, not the remaining novel targets. ARCHIVED RESULTS ARE NOT OPEN: the two founding traffic_signs_recognition_2023 counterexamples for network 3_30_30 (model_30_idx_1703_eps_1.00000 and model_30_idx_178_eps_1.00000, TROPHY_CASE.md rows 51-52 and known-knowns/vnncomp-2026-unsolved-instances/INDEX.csv) and the merged community counterexample for network 3_48_48 (model_48_idx_6371_eps_3.00000, known-knowns/vnncomp-2026-unsolved-instances/2026-10-15-verexxi-0e0b0ccd/INDEX.csv) are already published here. These exact ONNX+vnnlib pairs are closed for novelty under criterion (e), even while the official results log still shows their rows as all-tool-unsolved; another witness for the same pair is a replication, not a win.
- Before spending search budget, and again when checking novelty, cross-check TROPHY_CASE.md, the family-level INDEX.csv and every nested community-package INDEX.csv under known-knowns/vnncomp-2026-unsolved-instances/, then inspect the linked package README and benchmark-file hashes; also check public claim PRs for overlap. Match the exact ONNX+vnnlib pair and version using both SHA-256 values, not just an image index or a similar name. Merged community results need not appear in the trophy case or the family-level index. Recompute exclusions from the current archive rather than assuming 127 minus two (or any fixed residual count); pending PRs are leads to inspect, not automatically confirmed results.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/ml-robustness/vnncomp-2026-unsolved-instance-counterexample.md
```

Already set up? Say `run V3R1T4S on vnncomp-2026-unsolved-instance-counterexample`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `vnncomp-2026-unsolved-instance-counterexample`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
