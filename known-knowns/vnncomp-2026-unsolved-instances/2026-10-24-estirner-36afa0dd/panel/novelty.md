# Novelty skeptic verdict: vnncomp-2026-unsolved-instance-counterexample

context: subagent (Claude Code Agent tool, opus, fresh context, saw only claim/)

novelty: NEW (the instance `cifar10_eps8_wide_cnn7-cifar10_eps8_wide_cnn7_idx7490_sample8` of `2026_challenging_certified_training_2026` is still all-tool-unsolved in the live results table; no counterexample or verdict for this exact ONNX + vnnlib pair was found in the results repo, the benchmarks repo, the benchmark's source repository, this project's repository and pull requests, GitHub code search, arXiv, or the web)

Scope: novelty only (criteria (a) and (e) of `CLAIM.md`). I did not re-run the network or the validator; that is for the other skeptics. I matched the property file to the live benchmarks tree byte for byte, but did not re-download the ONNX from the sciebo share, so ONNX identity is left to the criterion and reproduce skeptics. This does not affect the novelty verdict.

Every web request below was one plain request with `curl -A "V3R1T4S-research-agent (curl)"` or read-only `gh`, with no retries. None was blocked.

## 1. Deciding table, live (criterion (a), first half)

- URL: https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_results/main/SCORING/results.txt
- Fetch started 2026-10-24T18:20:11Z (`date -u`) and ended 2026-10-24T18:20:14Z. HTTP 200, 7681226 bytes.
- sha256 `ec1b6fcbdef79539ffee17adbda2e99add137ba963a5306b87904035289eb26f`. This equals the sha256 quoted in `CLAIM.md`, and the table did not change between the claimant's fetches and mine.
- Response headers: `date: Sat, 24 Oct 2026 18:20:11 GMT`, `etag: "3aaa631e8ff8cd8b7906e9dd4ef03db1d7dd1094ebd8586ddaf40ac13d84cea6"`, `x-cache: HIT`. The CDN served a cached copy, but the commits API (section 2) confirms that main has had no new commit since then, so this is the current file.
- The section header (line 12618 onward) reads `Category 2026_challenging_certified_training_2026`, `has 60 (from agate)`, `8 participating tools: ['agate', 'alpha_beta_crown', 'n2v', 'neuralsat', 'nnv', 'pyrat', 'super_simple_vnn_comp', 'vibecheck']`.
- The instance's row (line 13098), copied from the fetched file:
  `Row: ['cifar10_eps8_wide_cnn7-cifar10_eps8_wide_cnn7_idx7490_sample8', '-', 'timeout', 'timeout', 'timeout', 'timeout', 'timeout', '-', 'timeout']`
  The next line is `True Result: -`, and all 8 tools have `score: 0, is_ver: False, is_fals: False`. This row matches `table/results_txt_excerpt.txt`.
- My own parse (`ast.literal_eval` of every `Row:` line, mapped onto the participating-tools list):
  - The instance has exactly one `Row:` line: agate `-`, alpha_beta_crown `timeout`, n2v `timeout`, neuralsat `timeout`, nnv `timeout`, pyrat `timeout`, super_simple_vnn_comp `-`, vibecheck `timeout`.
  - No cell contains `(h)` or `(v)`.
  - The category has 60 rows, 21 of them all-tool-unsolved, and the target is in that unsolved set. The figure of 21 matches the count of 21 for this category in the pinned repo's target statement, which was computed independently on 2026-10-09.

## 2. Results repo tree and per-tool results (criterion (a), second half)

- Head commit: https://api.github.com/repos/VNN-COMP/vnncomp2026_results/commits/main, fetched 2026-10-24T18:27:45Z, HTTP 200, response sha256 `1239eff0c7f3271dd3e96fb32c9722e18d4a9131d3c70bb3bb42cdcc80a0e474`. Main is `eea564f5d0a8751d8321a409214db14d03f452b8`, committed 2026-08-03T14:03:54Z ("Add VNN-COMP 2026 competition results and scoring report"), which is the commit named in `CLAIM.md`.
- Tree: https://api.github.com/repos/VNN-COMP/vnncomp2026_results/git/trees/main?recursive=1, fetched 2026-10-24T18:20:50Z, HTTP 200, 10027325 bytes, sha256 `8f7b2c70b39e468007149f341da977236ef0287d2f34700aa08456163d716960`.
  - The tree reports sha `eea564f5d0a8751d8321a409214db14d03f452b8`, `truncated: False`, 27250 entries.
  - **0 paths contain `idx7490`.** No tool directory holds any counterexample, `.counterexample.gz` or `.counterexample.check.json` file for this instance, so no check.json rates it `correct` or `correct_up_to_tolerance`.
  - The only counterexample files for `cifar10_eps8_wide_cnn7` are for the solved siblings: idx637_sample0 (agate, alpha_beta_crown, neuralsat, pyrat, super_simple_vnn_comp, vibecheck) and idx8397_sample9 (vibecheck).
- Per-tool `results.csv` for this category: all 11 tool directories that have one were fetched once each from `https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_results/main/<tool>/2026_challenging_certified_training_2026/results.csv`, between 2026-10-24T18:21:16Z and 18:21:23Z, all HTTP 200. The instance's result column is never `sat` or `unsat`:

  | tool | file version | result | sha256 of results.csv |
  |---|---|---|---|
  | act | 2.0 | unknown | 1671c7d346c9bb5ce390260753f82c2ac3d95e50888501013dc3ba3e0756271c |
  | agate | 2.0 | unknown | fd4cf8c4ce96ebbba664b53a9fbcae6b50a1610512164f1b96eb40c803b023cd |
  | alpha_beta_crown | 1.0 | timeout | 40ffee2c369cbf3e6512e0fb1b87e39697843cab4668cf5b372394d68c01c380 |
  | cora | 1.0 | unknown | 26fa7313dbac743f7ab80a0a2a51f81c71ce3130c38aee2f53cf8cfd2c1428ba |
  | n2v | 2.0 | run_instance_timeout | fdc826598717edacef126af9b0e406b6dd2af0670e56d19b64948bd9ee4bd978 |
  | neuralsat | 1.0 | timeout | 99d36c1240433682edd40519d4dd3d3673f4b114035d8456eb6168f6e59b9c6a |
  | nnenum | 1.0 | error_exit_code_1 | b7ce4367305d5899e30a0e9f0a8ecb58dfc5bcbfa53126f4ba058e49953d6465 |
  | nnv | 1.0 | timeout | a1099307bfec84750eafffd5b3d042fc7c44ac3cfc56891ce65fcc4c59afbfd2 |
  | pyrat | 1.0 | timeout | 19af4185ca8cbfb1b7da09d806197f210400c2128d0de812e5eaf9023502b9a3 |
  | super_simple_vnn_comp | 1.0 | no_result_in_file | b5893d59c115b6b43e81d7aa02b61972bc10524052010d6ccde5cd26d4187498 |
  | vibecheck | 2.0 | timeout | ae0c8bf7053c4d7adf7da722d6d796178fe53e0c61427681935f540a2bfe2bd7 |

  act, cora and nnenum are not in the table's participant list, and they did not solve the instance either. Of the table participants, agate, n2v and vibecheck name version 2.0, the version the claim uses.

## 3. Status source

- URL: https://github.com/VNN-COMP/vnncomp2026_benchmarks, fetched 2026-10-24T18:21:32Z (ended 18:21:34Z), HTTP 200, 250890 bytes.
- sha256 `c015c6fa0c3e22e9fd814437f095bad19d3c1ff82956a48cadc435874679bf49`. This differs from the claim's `5789ba9b…`, which is expected because GitHub's HTML is rendered fresh on every request.
- The stable identifier matches: the page's `"currentOid":"303f2327a8e8411efc4457da03d2016ce42733cf"` is the commit `CLAIM.md` cites for the property file.
- Benchmarks tree: https://api.github.com/repos/VNN-COMP/vnncomp2026_benchmarks/git/trees/main?recursive=1, fetched 2026-10-24T18:23:59Z, HTTP 200, sha256 `b8454c9360f88fbb201a2a5afd1d69970025bc3869321f5fef37af655d8b8069`. It reports sha `303f2327a8e8411efc4457da03d2016ce42733cf`, not truncated, 49532 entries.
  - `benchmarks/challenging_certified_training_2026/2.0/vnnlib/cifar10_eps8_wide_cnn7/cifar10_eps8_wide_cnn7_idx7490_sample8.vnnlib.gz` is 33067 bytes, git blob `c872c54a504a1311934c84639d13832acd24f883`.
  - The claim's `inputs/vnnlib/cifar10_eps8_wide_cnn7_idx7490_sample8.vnnlib.gz` has `git hash-object` = `c872c54a504a1311934c84639d13832acd24f883` and sha256 `c64e879e9a88b80384dc67f3b84cd8f12a299c9488f136961cb8f226e9f01a59`, so the property file is byte-identical to the live 2.0 file.
  - The 1.0 file is a different blob (`17e5cbd696c512af9d927ee1c99f36782a57e559`, 40384 bytes).
  - Neither version has a counterexample or witness file anywhere in the category.

## 4. This repository (V3R1T4S)

- Pinned copy: `TROPHY_CASE.md` has sha256 `b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1`, at repo commit `d14b0098c7dc3c372fa861a00175d3775aa097e7`.
  - Its only VNN-COMP rows (51, 52 and the summary row) are traffic_signs_recognition_2023 instances idx_1703 and idx_178.
  - `known-knowns/vnncomp-2026-unsolved-instances/INDEX.csv` lists the same two. The dated sub-entry `2026-10-15-verexxi-0e0b0ccd` is traffic_signs model_48 idx_6371.
  - A grep of the whole pinned repo (excluding .git) for `idx7490|wide_cnn7|challenging_certified` hits only the target statement text, in `bank/targets.json` and `known-unknowns/ml-robustness/vnncomp-2026-unsolved-instance-counterexample.md`.
- Live trophy case: https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md, fetched 2026-10-24T18:22:56Z, HTTP 200, 31235 bytes, sha256 `b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1`, byte-identical to the pinned copy.
- Live tree: https://api.github.com/repos/elder-plinius/V3R1T4S/git/trees/main?recursive=1, fetched 2026-10-24T18:22:57Z, HTTP 200, sha256 `9b7ab185b4625cdc16024df70f3fcd214aa01360a68d3fb2c6f8bbd2ff939d52`. It reports sha `1ebdef41c30414cd2a036b00f5e81d0fc4c1dc25`, not truncated, 5439 entries. 0 paths match `7490`, `eps8_wide`, `cifar10_eps8`, `challenging_certified` or `wide_cnn7`.
- Pull requests:
  - `gh pr list -R elder-plinius/V3R1T4S --state all --search <q>` at 2026-10-24T18:22:07Z–18:22:12Z returned `[]` for `idx7490`, `wide_cnn7`, `challenging_certified` and `cifar10_eps8`.
  - Because search turned out to miss underscore names (it found nothing for `wide_cnn7` even though #566's title contains it), I also dumped every PR at 2026-10-24T18:22:24Z (624 PRs, numbers 1–647: 276 open, 198 closed, 150 merged; dump sha256 `5fa942bd640abc3dd7dd61ef004343c43b9c2ff37e7f0070abcb60557771bb03`) and grepped titles, bodies and branch names myself.
  - `eps8_wide` and `cifar10_eps8` have 0 hits.
  - `7490` has 4 hits, all digit coincidences inside decimals (#638 `0.0749007698`, #487 `0.6627989728337490…`, #245 `0.25408038179177490…`, #207 `0.116284441837827490…`).
  - The only PR in the same benchmark is #566 (open, created 2026-10-19), "certified counterexample for unsolved tinyimagenet_eps1_wide_cnn7_idx7687_sample8". That is a different network and a different property, so it is neither a prior result nor a tie for this pair. Its file list (`gh pr view 566 --json files`, 2026-10-24T18:22:41Z, all under `known-knowns/vnncomp-2026-unsolved-instances/2026-10-19-mizopl-57af300b/`) contains nothing for idx7490 or cifar10_eps8_wide_cnn7.
  - #146 (merged) is the traffic-sign case 6371.
- Issues: issues share GitHub's number space with PRs, which accounts for the 23 missing PR numbers. I dumped them with `gh issue list -R elder-plinius/V3R1T4S --state all` at 2026-10-24T18:31:18Z (23 issues, dump sha256 `7e9db7ff62794fe5faf21f5c3e330ec497203031678285e5ab7e098339b48efa`).
  - 0 hits for `7490`, `eps8_wide`, `cifar10_eps8`, `wide_cnn7` or `challenging_certified`.
  - The 3 VNN-COMP issues are #625 (ACAS-Xu witnesses), #624 (errata on trophy rows 51–52) and #623 (pinned-coordinate rows). None concerns this instance.

## 5. Benchmark source repository and literature (criterion (e))

**Benchmark source repository**

- Repo metadata: https://api.github.com/repos/kkaulen/vnncomp_challenging_certified_training, fetched 2026-10-24T18:23:05Z, HTTP 200, sha256 `8ca36ef14a10456753814257b0e458257d77804afa180ab30d55ccb310f252af`. Last push was 2026-05-11T12:45:45Z.
- Tree at 2026-10-24T18:23:11Z, HTTP 200, sha256 `9e3e8bc5086a5373cac16113fab8007163510c4b3c81fcc8b5734c16c64f414f`: commit `63508e7d11eb7c551f123a9137d5adaa8790e0b0`, 15 entries, no counterexample files, no path containing 7490.
- `verification_results/cifar10_eps8_wide_cnn7.json` (https://raw.githubusercontent.com/kkaulen/vnncomp_challenging_certified_training/63508e7d11eb7c551f123a9137d5adaa8790e0b0/verification_results/cifar10_eps8_wide_cnn7.json), fetched 2026-10-24T18:23:19Z, HTTP 200, 1022150 bytes, sha256 `ed78b19e771aa6c0c2202fe283ab750f9425501c18ff463893346954a97b25fe`, git blob `4f199667186aa704d29d853fc9dc28f0e707d623`.
  - It has 10000 entries: 6408 sat, 3460 unsat, 132 timeout, all by abCROWN. Per the README, `unsat` means robust.
  - **Entry `"7490"`: `{'result': 'timeout', 'method': 'abCROWN', 'running_time': 1007.5780041217804}`.** The benchmark authors' own 1000 s H100 run did not resolve it, and no verdict or counterexample was published.
- `metadata/sampled_instances.json` (same commit, 2026-10-24T18:23:20Z, HTTP 200, sha256 `167c3d02596709393eca150d92aa76ef73e07b68d40405fb5b005e6c6501407a`) is the seed-42 sample. Its 10 cifar10_eps8_wide_cnn7 entries do not include image index 7490; the competition's 2.0 set was sampled separately. It carries no verdict for 7490.
- README.md (same commit, 2026-10-24T18:23:21Z, HTTP 200, sha256 `d6b4a44719293e8fc57e0927865f43974199fd51ea51f5d378c4c374f49b4112`) contains no counterexamples.
- A second copy of the generator, `Lemutisme/vnncomp_CCT`, was found by code search.
  - Metadata at 2026-10-24T18:26:18Z, HTTP 200, sha256 `6763a88fcd097110f2c58883b37e012f0b16132e9d336e24ee04a3f44a9481c0`, not a fork, created and pushed 2026-06-30.
  - Tree at commit `80fe50b04bf13db3352617c6200a9af28bafc4f2`, HTTP 200, sha256 `58b6fd8d52828227fd451e676c1a28302cd2b82988f0ea46cb3eb29621aa56d9`, 11 entries. Its `cifar10_eps8_wide_cnn7.json` is the same blob `4f199667…`, so 7490 is `timeout` there too.
  - Its README (2026-10-24T18:26:32Z, HTTP 200, sha256 `922aaed18f524cf13a3f24fce8343879392723f7c42f39cdebf0deadb30c2eb5`) differs only in sample counts. No counterexamples.
- Issues and PRs of the competition and source repos (`gh issue list` / `gh pr list --state all`, 2026-10-24T18:26:43Z–18:26:47Z):
  - VNN-COMP/vnncomp2026_results: 1 issue (input-bound precision, 1.0 vs 2.0), 0 PRs.
  - VNN-COMP/vnncomp2026_benchmarks: 13 issues, 0 PRs.
  - kkaulen/vnncomp_challenging_certified_training: 0 issues, 0 PRs.
  - None mentions 7490, eps8_wide, wide_cnn7 or certified training.

**GitHub code search** (`gh search code`, 2026-10-24T18:25:28Z–18:26:04Z)

- `idx7490_sample8` and `cifar10_eps8_wide_cnn7_idx7490` hit only the two benchmark `instances.csv` files and the 11 `results.csv` files above.
- `cifar10_eps8_wide_cnn7` additionally hits only the idx637 and idx8397 sibling check.json files and the two generator repos.
- `idx7490` adds unrelated repos (openafs docs, tasepy).
- `eps8_wide_cnn7 counterexample` returns nothing.
- The first runs at 18:25:28Z–18:25:36Z were cut off by my own `head -c` display limit, not by a block. I re-ran them once at 18:25:49Z–18:25:54Z with compact `--jq` output.

**arXiv** (export API, one request per URL, `sortBy=submittedDate`, `max_results=50`)

- 18:24:24Z `all:"VNN-COMP 2026"`: HTTP 200, 0 entries (sha256 33b48e105a365163d62c82e1c1334c505ff39bb9cff260f4157742d588b83b66).
- 18:24:29Z `all:"VNN-COMP" AND submittedDate:[202410240000 TO 202610242359]`: HTTP 200, 12 entries (sha256 8bf8feabc813b3e639bede24993a82ac5a39f3166e616e6e114960d2f3d1efe4).
  - These include the VNN-COMP 2024 and 2025 reports (2412.19985, 2512.19007), which are earlier competitions, plus tool papers.
  - The only 2026 hits are 2606.09377, 2605.23203 and 2603.23878. Their abstracts concern other benchmarks: 2606.09377 uses VNN-COMP 2022 MNIST-FC and 2024 CIFAR-100. None mentions challenging_certified_training or CTRAIN models.
- 18:24:34Z `all:"challenging certified training"`: HTTP 200, 0 entries (sha256 721f1a6be4a47539ba7e3ec7f89135f08e590a66026759371afb7f832f5b6792).
- 18:24:39Z `all:CTRAIN AND all:verification` (last 24 months): HTTP 200, 0 entries (sha256 eadd8a74673473d099a866e3f71e7c17e6ca555e40f7ea3369c3a072e1a00a65).
- 18:24:44Z `all:"wide_cnn7"`: HTTP 200, 0 entries (sha256 9cfb8b0bf441893e3404d1fc259471823c72664e862a98872d92c2972f51021b).
- 18:24:48Z `abs:"neural network verification" AND abs:counterexample` (last 24 months): HTTP 200, 2 entries (sha256 511a813460a26830f52a0df9145e30d203250e83f89f1024869264b1dab62a12). Both are unrelated (2609.34628 CLAD, 2504.03272 KeYmaera X).
- 2601.13303 (seed variance of certified robustness, Le and Cao), found by web search: `id_list` fetch at 2026-10-24T18:27:16Z, HTTP 200, sha256 bbf0e9767803dae1003b5d9ec0bb69340aff2c25438126808d2e52471813f6c2. The abstract has nothing about this benchmark or instance.
- No VNN-COMP 2026 summary report exists on arXiv.

**Web**

- WebSearch, 2026-10-24, run after the arXiv queries (exact time not logged):
  - `"cifar10_eps8_wide_cnn7_idx7490_sample8"`: no relevant result.
  - `"cifar10_eps8_wide_cnn7" counterexample VNN-COMP 2026`: only V3R1T4S PR #566 (different instance) and the VNN-COMP 2022–2025 reports.
  - `VNN-COMP 2026 summary results challenging_certified_training …`: no 2026 report.
  - `"VNN-COMP 2026" results report counterexample` and `"challenging_certified_training_2026" OR "challenging certified training" … counterexample`: only #566, #146, earlier reports and unrelated papers.
- https://vnn-comp.github.io/ at 2026-10-24T18:27:20Z, HTTP 200, 70242 bytes, sha256 `8e85c596eac5562422354664e59cffa3265ddadf7cf5ec70daa11fa02fbb69bb`. It links only the 2026 results repo, the benchmarks repo, the rules and the SAIV talk page, with no report PDF.
- https://aiverification.org/2026/talks/vnncomp/ at 2026-10-24T18:27:30Z, HTTP 200, 9592 bytes, sha256 `b2f2a4f2ab5c3507b522d46ae45bce73dd4a9aa09db734c13c9c13c7c254bfb9`. No slides, report links or instance mentions.

## 6. Comparison with the best known

- The best known result for this exact pair is "unsolved":
  - All 8 table participants fail (timeout or `-`), and so do the 3 non-table tools with results (unknown or error).
  - There is no check.json, and `True Result: -`.
  - The benchmark authors' abCROWN run timed out at 1007.578 s.
- No published counterexample, sat verdict or unsat verdict exists for `onnx/cifar10_eps8_wide_cnn7.onnx` + `vnnlib/cifar10_eps8_wide_cnn7/cifar10_eps8_wide_cnn7_idx7490_sample8.vnnlib` (2.0) anywhere I could reach.
- A valid counterexample (`object/cifar10_eps8_wide_cnn7_idx7490_sample8.counterexample.txt`, sha256 `36afa0dd0c97274d86c6c31f0b42cfab276b522b393a8374a9bb2e18391696b4`) would therefore strictly beat everything known. It is not a replication, and it does not tie the only related submission (#566), which is a different instance.
- Whether the object is valid is outside my remit and is not judged here.

pass: true
