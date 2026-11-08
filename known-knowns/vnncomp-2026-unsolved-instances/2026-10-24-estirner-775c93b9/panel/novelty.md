# Novelty skeptic verdict: vnncomp-2026-unsolved-instance-counterexample (cifar10_eps8_wide_cnn7_idx6249_sample7)

context: subagent (Claude Code Agent tool, opus, fresh context, saw only claim/)

novelty: NEW (no prior counterexample or verdict found for this exact ONNX + vnnlib pair; the instance is still all-tool-unsolved in the live table)

Scope: this verdict covers success criteria (a) and (e) in claim/CLAIM.md. Criterion (d) also holds: the instance is from challenging_certified_training_2026, not soundnessbench_2026 or test. Whether the witness is a valid counterexample (criteria (b) and (c): bounds, onnxruntime, second runtime, official validator) is for the other skeptics. I did not run the network. Novelty only counts if those checks pass.

injection_suspected: none (on 2026-10-24 I read claim/CLAIM.md, claim/REPRODUCE.md, claim/tools/official_validate_run.py, claim/table/results_txt_excerpt.txt and every page fetched below; none of them contains instructions to its reader.)

## Claim files examined (sha256 computed here, 2026-10-24T16:48:37Z)

| file | sha256 |
|---|---|
| `object/cifar10_eps8_wide_cnn7_idx6249_sample7.counterexample.txt` (3072 lines) | 775c93b9b508b63002b8da10ce73cf317537692b3ef7d0e2b84747f67367baca |
| `object/cifar10_eps8_wide_cnn7_idx6249_sample7_v2.counterexample` | 9910a4f00246b11f4d2c5cfd566804e0bebbe7d9fbd5dd373e35377ca4971dc3 |
| `object/cifar10_eps8_wide_cnn7_idx6249_sample7.counterexample.npy` | fdaea2ac5bbe2b2dceba9cddb64e9749a99b42334df44ee42aa697ea86327cf7 |
| `inputs/vnnlib/cifar10_eps8_wide_cnn7_idx6249_sample7.vnnlib.gz` | 3e9340de6e0237635a572457218e5c4f74b298e20ff69dc482a627e85206d1fe |
| `inputs/onnx/cifar10_eps8_wide_cnn7.onnx.gz` | 7e65aeddfcace3cecb65f4c91dcf51723a862236537ae1afb1db3912f309f5f8 |
| `CLAIM.md` | 47f809f8f25f16d67da798380a9e483bf486d55e71dc4a3f79cf422077d2ad1d |

All of these match the values stated in CLAIM.md.

## 1. Live deciding table (criterion (a)): fetched once, no retry

- URL: https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_results/main/SCORING/results.txt
- Request started 2026-10-24T16:34:09Z and finished 2026-10-24T16:34:44Z (date -u). HTTP 200, 7681226 bytes.
- sha256 ec1b6fcbdef79539ffee17adbda2e99add137ba963a5306b87904035289eb26f. This is byte-identical to the claimant's fetches at 15:07:03Z and 16:29:21Z, so the live table has not changed since the claimant read it.
- Category header (line 12618-12620): `Category 2026_challenging_certified_training_2026 has 60 (from agate)`, `8 participating tools: ['agate', 'alpha_beta_crown', 'n2v', 'neuralsat', 'nnv', 'pyrat', 'super_simple_vnn_comp', 'vibecheck']`.
- My own parse (ast.literal_eval of the Row list) finds exactly one Row line for the instance, line 13087:
  `Row: ['cifar10_eps8_wide_cnn7-cifar10_eps8_wide_cnn7_idx6249_sample7', '-', 'timeout', 'timeout', 'timeout', 'timeout', 'timeout', '-', 'timeout']`
  - cells = `['-', 'timeout', 'timeout', 'timeout', 'timeout', 'timeout', '-', 'timeout']`, any_h_or_v = **False**
  - The next line is `True Result: -`, and every one of the 8 tools has `score: 0, is_ver: False, is_fals: False`.
- So the instance is in the all-tool-unsolved set by my own parse of the live file.

### Results repository tree and per-tool results (criterion (a), second part)

- https://api.github.com/repos/VNN-COMP/vnncomp2026_results/branches/main fetched 2026-10-24T16:35:12Z, HTTP 200, 4993 bytes, sha256 caa7a9397cc58ce16f68faeca5ab3f1200fc00e83d1455b2814c8ca9d6539791. main = eea564f5d0a8751d8321a409214db14d03f452b8, committer date 2026-08-03T14:03:54Z. This is the same commit the claim names.
- https://api.github.com/repos/VNN-COMP/vnncomp2026_results/git/trees/main?recursive=1 fetched 2026-10-24T16:35:18Z, HTTP 200, 10027325 bytes, sha256 8f7b2c70b39e468007149f341da977236ef0287d2f34700aa08456163d716960. It is `truncated False` with 27250 entries.
  - 0 paths contain `idx6249_sample7`, so no tool directory holds a `.counterexample*` or `.counterexample.check.json` for this instance. The "no check.json with correct / correct_up_to_tolerance" condition holds trivially.
  - The only counterexample files for this network in the whole tree are for the solved siblings: `idx637_sample0` (6 tools) and `idx8397_sample9` (vibecheck).
  - 11 tool directories have this category: act, agate, alpha_beta_crown, cora, n2v, neuralsat, nnenum, nnv, pyrat, super_simple_vnn_comp, vibecheck. That is 3 more than the 8 scored tools.
- I fetched each tool's `<tool>/2026_challenging_certified_training_2026/results.csv` once from https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_results/main/... between 2026-10-24T16:36:28Z and 16:36:36Z. All 11 returned HTTP 200. The result each one records for this instance:

| tool | version dir | result | csv sha256 |
|---|---|---|---|
| act (not scored) | 2.0 | unknown | 1671c7d346c9bb5ce390260753f82c2ac3d95e50888501013dc3ba3e0756271c |
| agate | 2.0 | unknown | fd4cf8c4ce96ebbba664b53a9fbcae6b50a1610512164f1b96eb40c803b023cd |
| alpha_beta_crown | 1.0 | timeout | 40ffee2c369cbf3e6512e0fb1b87e39697843cab4668cf5b372394d68c01c380 |
| cora (not scored) | 1.0 | unknown | 26fa7313dbac743f7ab80a0a2a51f81c71ce3130c38aee2f53cf8cfd2c1428ba |
| n2v | 2.0 | run_instance_timeout | fdc826598717edacef126af9b0e406b6dd2af0670e56d19b64948bd9ee4bd978 |
| neuralsat | 1.0 | run_instance_timeout | 99d36c1240433682edd40519d4dd3d3673f4b114035d8456eb6168f6e59b9c6a |
| nnenum (not scored) | 1.0 | error_exit_code_1 | b7ce4367305d5899e30a0e9f0a8ecb58dfc5bcbfa53126f4ba058e49953d6465 |
| nnv | 1.0 | timeout | a1099307bfec84750eafffd5b3d042fc7c44ac3cfc56891ce65fcc4c59afbfd2 |
| pyrat | 1.0 | timeout | 19af4185ca8cbfb1b7da09d806197f210400c2128d0de812e5eaf9023502b9a3 |
| super_simple_vnn_comp | 1.0 | no_result_in_file | b5893d59c115b6b43e81d7aa02b61972bc10524052010d6ccde5cd26d4187498 |
| vibecheck | 2.0 | timeout | ae0c8bf7053c4d7adf7da722d6d796178fe53e0c61427681935f540a2bfe2bd7 |

No tool, scored or not, returned sat or unsat on this instance.

## 2. Status source (named in CLAIM.md): fetched once

- URL: https://github.com/VNN-COMP/vnncomp2026_benchmarks, request started 2026-10-24T16:36:52Z and finished 16:36:54Z, HTTP 200, 250886 bytes, sha256 14ad1607356e7a7f5d83672b7b37fd451d521309c147588a1215ee93916c4f3d.
- This HTML hash **differs** from the claimant's (5789ba9b...). That is expected for a dynamically rendered GitHub page and does not count against the claim. What matters is the content: the page's `"currentOid":"303f2327a8e8411efc4457da03d2016ce42733cf"` is the benchmark commit the claim names.
- Exact-pair identity: https://api.github.com/repos/VNN-COMP/vnncomp2026_benchmarks/git/trees/303f2327a8e8411efc4457da03d2016ce42733cf?recursive=1 fetched 2026-10-24T16:40:50Z, HTTP 200, 17616411 bytes, sha256 b8454c9360f88fbb201a2a5afd1d69970025bc3869321f5fef37af655d8b8069, not truncated.
  - It lists `benchmarks/challenging_certified_training_2026/2.0/vnnlib/cifar10_eps8_wide_cnn7/cifar10_eps8_wide_cnn7_idx6249_sample7.vnnlib.gz` with git blob sha1 812a0336e509de33a949ffe31e3107f5c78d5247 and size 35086.
  - The git blob sha1 I computed for `inputs/vnnlib/cifar10_eps8_wide_cnn7_idx6249_sample7.vnnlib.gz` is 812a0336e509de33a949ffe31e3107f5c78d5247 (35086 bytes). The claim's property file is byte-identical to the benchmark's 2.0 file.
  - The 1.0 file is a different blob (ee05feda86aaaa4aae434f8a67bd1e7fe752b85c, 42671 bytes). The claim is for the 2.0 pair, which agate, n2v and vibecheck (scored) and act ran.
- The category README (https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_benchmarks/303f2327a8e8411efc4457da03d2016ce42733cf/benchmarks/challenging_certified_training_2026/README.md, 2026-10-24T16:42:40Z, HTTP 200, 365 bytes, sha256 0a55af2f810585c4dc0b3e5f7a963caa1f36051961db71c5b3d52fd9f90ef49f) names source commit b4caf3d72d4f4442a640e1ef5aa1bce165815456 and generation seed 157191271. It contains no verdicts.

## 3. This repository (pinned copy at repo HEAD d14b0098c7dc3c372fa861a00175d3775aa097e7)

- `TROPHY_CASE.md` (sha256 b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1). Its only VNN-COMP rows are 51 and 52, both traffic_signs_recognition_2023 3_30_30 (model_30_idx_1703 and idx_178). Nothing for challenging_certified_training_2026 or cifar10_eps8_wide_cnn7.
- `known-knowns/vnncomp-2026-unsolved-instances/INDEX.csv` has the same two traffic_signs rows. A grep of the whole pinned repo (excluding .git) for `idx6249`, `cifar10_eps8_wide` and `challenging_certified` hits only the target definitions in `bank/targets.json` and `known-unknowns/ml-robustness/vnncomp-2026-unsolved-instance-counterexample.md`. Both list the benchmark only as part of the open unsolved set ("challenging_certified_training_2026 (21: ...)"). SHA256SUMS has 0 matches.

## 4. Live pull requests and issues of elder-plinius/V3R1T4S (read-only gh)

- `gh pr list --state all --search` for idx6249, cifar10_eps8_wide_cnn7, challenging_certified, 6249, sample7, wide_cnn7, cifar10 and eps8 returned no PRs (2026-10-24T16:37:38Z to 16:38:00Z). The searches for vnncomp, unsolved-instance, counterexample and "certified training" return only #566, #146, #632, #631, #9 and #399, none of which is about this instance.
- I listed the file paths of all 623 PRs (2026-10-24T16:44:42Z to 16:45:58Z). Only #632, #631, #566, #146 and #9 touch VNN-COMP paths, and no PR has a path containing 6249.
- Issues searched for idx6249, cifar10_eps8_wide_cnn7, "certified training" and vnncomp: only #623, #624 and #625 (bank criteria and errata), none about this instance.
- **Near miss, disclosed:** open PR #566 (a counterexample for a different instance in the same category, tinyimagenet_eps1_wide_cnn7_idx7687_sample8) lists `cifar10_eps8_wide_cnn7_idx6249_sample7.vnnlib` as one of eight attack targets in its script `how-we-built-it/polish_and_attack_cct.py`. The diff was fetched with `gh pr diff 566` at 2026-10-24T16:38:24Z: 785374 bytes, sha256 71244a584146012859a77ea720dda7de8a5a57ccc633db21171010f7877a27db.
  - No witness, result or claim for idx6249 appears anywhere in that PR. Its only `.counterexample*` files are for idx7687_sample8, and a grep of its .md/.json/.csv/.txt/.sh files for `eps8_wide` and `idx6249` is empty.
  - An attack attempt with no published witness is not a prior result. If anything, it supports novelty.

## 5. Literature and code, last 24 months (criterion (e))

- Benchmark source repository https://github.com/kkaulen/vnncomp_challenging_certified_training:
  - API metadata fetched 2026-10-24T16:39:41Z, HTTP 200, 6696 bytes. It was created 2026-05-10 and last pushed 2026-05-11T12:45:45Z. Tree fetched 16:39:49Z, HTTP 200, 5043 bytes, sha256 9e3e8bc5086a5373cac16113fab8007163510c4b3c81fcc8b5734c16c64f414f: 15 entries, no counterexample files.
  - `verification_results/cifar10_eps8_wide_cnn7.json` (raw main, 2026-10-24T16:40:01Z, HTTP 200, 1022150 bytes, sha256 ed78b19e771aa6c0c2202fe283ab750f9425501c18ff463893346954a97b25fe) has 10000 entries: sat 6408, unsat 3460, timeout 132. Entry `"6249"` is `{'result': 'timeout', 'method': 'abCROWN', 'running_time': 1001.0547182559967}`, so abCROWN gave no verdict even with a 1000 s cutoff on an H100.
  - README fetched 16:39:58Z, HTTP 200, 5564 bytes, sha256 d6b4a44719293e8fc57e0927865f43974199fd51ea51f5d378c4c374f49b4112. `metadata/sampled_instances.json` fetched 16:39:59Z, HTTP 200, 34835 bytes, sha256 167c3d02596709393eca150d92aa76ef73e07b68d40405fb5b005e6c6501407a. That file is a seed-42 example, not the competition seed, and does not contain 6249.
- Fork https://api.github.com/repos/Lemutisme/vnncomp_CCT/git/trees/HEAD?recursive=1 fetched 2026-10-24T16:40:49Z, HTTP 200, 3546 bytes, sha256 58b6fd8d52828227fd451e676c1a28302cd2b82988f0ea46cb3eb29621aa56d9. It holds only the generator and the same six verification_results files (identical sizes), with no counterexamples.
- GitHub code search, 2026-10-24T16:39:10Z to 16:39:20Z:
  - `cifar10_eps8_wide_cnn7_idx6249_sample7` and `idx6249_sample7` match only the benchmarks repo's 1.0 and 2.0 instances.csv and the 11 results.csv files above.
  - `cifar10_eps8_wide_cnn7` additionally matches the source repo and its fork, plus the competition's idx637_sample0 and idx8397_sample9 check.json files.
- GitHub-wide issue and PR search, 2026-10-24T16:44:23Z:
  - `idx6249_sample7` and `eps8_wide_cnn7` return 0 results.
  - `challenging_certified_training_2026` returns only V3R1T4S #566, VNN-COMP/vnncomp2026#6 (benchmark voting) and tool-support PRs (n2v, nnv), none with a witness for this instance.
  - The results repo has 0 PRs and 1 issue (#1, about VNNLIB 1.0/2.0 input-bound precision).
- arXiv API (https://export.arxiv.org/api/query, all HTTP 200, 2026-10-24T16:43:11Z to 16:43:58Z):
  - `all:"VNN-COMP 2026"`, `all:"VNN-COMP" AND all:"certified training"`, `all:"challenging certified training"` and `all:CTRAIN AND all:verification` return 0 results each.
  - `ti:"Verification of Neural Networks Competition"` returns 6 results, the newest being the VNN-COMP 2025 report arXiv:2512.19007. No 2026 competition report is on arXiv.
  - `abs:VNN AND abs:COMP` (sha256 2f8ec91ecc066779ba86bb04a67c7e2f7b8e9ed2a9707cfb05879a04f2b6feab) returns 24 results. The 12 since 2024-10 include 2606.09377 (FSDP/TP for alpha-beta-CROWN) and 2603.23878 (Luna). None mentions this benchmark, wide_cnn7, CTRAIN or a counterexample for it.
- Web search (standard and extended) for "cifar10_eps8_wide_cnn7" and "VNN-COMP 2026 ... challenging certified training ... counterexample" finds no page with this instance. The only related hit is V3R1T4S PR #566 (a different instance).
- https://vnn-comp.github.io/ fetched 2026-10-24T16:44:11Z, HTTP 200, 70242 bytes, sha256 8e85c596eac5562422354664e59cffa3265ddadf7cf5ec70daa11fa02fbb69bb. It has the 2026 edition announcement (SAIV 2026 @ CAV/FLoC, July 24-25) and no per-instance results.

## Assessment

- What is known for this exact pair (challenging_certified_training_2026 2.0 `onnx/cifar10_eps8_wide_cnn7.onnx` + `vnnlib/cifar10_eps8_wide_cnn7/cifar10_eps8_wide_cnn7_idx6249_sample7.vnnlib`):
  - every competition tool timed out, errored or returned unknown;
  - the benchmark author's own abCROWN run timed out at 1001 s;
  - no counterexample or verdict has been published in the results repository, this repository's archive or PRs, GitHub, arXiv or the web.
- A strict counterexample would therefore be the first resolution of the instance. That beats everything known; it is not a tie and not a replication.
- This pass holds only if the reproduction and criterion skeptics confirm that the witness is valid (criteria (b) and (c)).

pass: true
