# Novelty skeptic: vnncomp-2026-unsolved-instance-counterexample

context: subagent (Claude Code Agent tool, opus, fresh context, saw only claim/)

Claim under review (from `CLAIM.md`): the input in `object/cifar10_eps8_cnn7_idx8072_sample9.counterexample.txt` is a
strict counterexample for VNN-COMP 2026 `challenging_certified_training_2026` (version 2.0)
`onnx/cifar10_eps8_cnn7.onnx` + `vnnlib/cifar10_eps8_cnn7/cifar10_eps8_cnn7_idx8072_sample9.vnnlib`.

Scope of this file: criteria (a) and (e) of the success criterion. (a): the instance is all-tool-unsolved in the LIVE
table, by my own parse, and no tool directory holds a `correct` counterexample. (e): nothing has been published
anywhere for this exact ONNX + vnnlib pair. Whether the witness actually satisfies the property (b, c) is for the other
skeptics; I did not re-run the network.

Session note: my session was cut once by an API usage limit and then resumed. The cut came before any web fetch, so
no fetch was interrupted and none was repeated. Every fetch below was one request.

## 1. Deciding table (live), fetched once

- URL: https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_results/main/SCORING/results.txt
- Fetch started 2026-10-24T21:01:24Z and ended 2026-10-24T21:01:28Z. Server `date: Sat, 24 Oct 2026 21:01:25 GMT`,
  `source-age: 0`.
- Result: HTTP 200, 7681226 bytes, sha256 `ec1b6fcbdef79539ffee17adbda2e99add137ba963a5306b87904035289eb26f`,
  etag `"3aaa631e8ff8cd8b7906e9dd4ef03db1d7dd1094ebd8586ddaf40ac13d84cea6"`. Size and hash are the same as in
  `CLAIM.md`, so the table has not changed since the claim was made.
- The instance appears in exactly one `Row:` line (line 12985), inside `Category 2026_challenging_certified_training_2026`,
  with 8 participating tools `['agate', 'alpha_beta_crown', 'n2v', 'neuralsat', 'nnv', 'pyrat', 'super_simple_vnn_comp', 'vibecheck']`:

      Row: ['cifar10_eps8_cnn7-cifar10_eps8_cnn7_idx8072_sample9', '-', 'timeout', 'timeout', '-', 'timeout', 'timeout', '-', 'timeout']

  The next line is `True Result: -`, and every tool scored 0 (`is_ver: False, is_fals: False`).
- My own parse (Python `ast.literal_eval` of the Row, cells zipped with the category's tool list) gives:
  agate `'-'`, alpha_beta_crown `'timeout'`, n2v `'timeout'`, neuralsat `'-'`, nnv `'timeout'`, pyrat `'timeout'`,
  super_simple_vnn_comp `'-'`, vibecheck `'timeout'`. Result: `any (h)/(v): False`.
- The only other occurrence of the instance in the file is the summary CSV line 13579, with the same cells. This
  matches `table/results_txt_excerpt.txt`.

**Criterion (a), table part: confirmed.** The instance is all-tool-unsolved in the live table.

## 2. Results repo tree (live), fetched once

- URL: https://api.github.com/repos/VNN-COMP/vnncomp2026_results/git/trees/main?recursive=1
- Fetched 2026-10-24T21:01:57Z to 21:02:03Z: HTTP 200, 10027325 bytes, sha256
  `8f7b2c70b39e468007149f341da977236ef0287d2f34700aa08456163d716960`.
- The tree is at commit `eea564f5d0a8751d8321a409214db14d03f452b8`, with `truncated: false` and 27250 entries.
  `last-modified: Mon, 03 Aug 2026 14:12:13 GMT`.
- Paths containing `idx8072` (any tool, any file): **0**. So no `*.counterexample*` file and no
  `*.counterexample.check.json` exists for this instance in any tool directory. The category's 120 counterexample and
  check files all belong to other instances.
- Eleven tool directories exist for this category: act, agate, alpha_beta_crown, cora, n2v, neuralsat, nnenum, nnv,
  pyrat, super_simple_vnn_comp and vibecheck. act, cora and nnenum are not among the 8 tools in the scored Row; each
  holds only `.gitkeep` and `results.csv`.
- I fetched each tool's `results.csv` once from `https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_results/main/<tool>/2026_challenging_certified_training_2026/results.csv`,
  between 2026-10-24T21:02:36Z and 21:02:40Z. All 11 returned HTTP 200. The row for this instance in each:

| tool | version dir | result | sha256 of results.csv |
|---|---|---|---|
| act | 2.0 | unknown | 1671c7d346c9bb5ce390260753f82c2ac3d95e50888501013dc3ba3e0756271c |
| agate | 2.0 | unknown | fd4cf8c4ce96ebbba664b53a9fbcae6b50a1610512164f1b96eb40c803b023cd |
| alpha_beta_crown | 1.0 | timeout | 40ffee2c369cbf3e6512e0fb1b87e39697843cab4668cf5b372394d68c01c380 |
| cora | 1.0 | unknown | 26fa7313dbac743f7ab80a0a2a51f81c71ce3130c38aee2f53cf8cfd2c1428ba |
| n2v | 2.0 | run_instance_timeout | fdc826598717edacef126af9b0e406b6dd2af0670e56d19b64948bd9ee4bd978 |
| neuralsat | 1.0 | unknown | 99d36c1240433682edd40519d4dd3d3673f4b114035d8456eb6168f6e59b9c6a |
| nnenum | 1.0 | error_exit_code_1 | b7ce4367305d5899e30a0e9f0a8ecb58dfc5bcbfa53126f4ba058e49953d6465 |
| nnv | 1.0 | timeout | a1099307bfec84750eafffd5b3d042fc7c44ac3cfc56891ce65fcc4c59afbfd2 |
| pyrat | 1.0 | timeout | 19af4185ca8cbfb1b7da09d806197f210400c2128d0de812e5eaf9023502b9a3 |
| super_simple_vnn_comp | 1.0 | no_result_in_file | b5893d59c115b6b43e81d7aa02b61972bc10524052010d6ccde5cd26d4187498 |
| vibecheck | 2.0 | timeout | ae0c8bf7053c4d7adf7da722d6d796178fe53e0c61427681935f540a2bfe2bd7 |

No tool, scored or unscored, reports `sat` or `unsat` for this instance in either version directory.

**Criterion (a), counterexample-file part: confirmed.**

## 3. Status source, fetched once

- URL: https://github.com/VNN-COMP/vnncomp2026_benchmarks
- Fetched 2026-10-24T21:02:54Z to 21:02:55Z: HTTP 200, 250891 bytes, sha256
  `caa8cabcb3259f4b5dd7f44700f85b06442babe2f73b265628584fad7d05c82e`. The HTML is dynamic, so its hash differs from the
  claimant's; that is expected.
- The page's `currentOid` is `303f2327a8e8411efc4457da03d2016ce42733cf`, so the benchmarks main HEAD is still the
  commit `CLAIM.md` pins. The README body is only the title. The page contains no `idx8072` and no
  `challenging_certified` text.
- Identity of the exact pair. `git hash-object` on `inputs/onnx/cifar10_eps8_cnn7.onnx.gz` gives
  `f084be840473d8ebc88ccaaba50bbf1c57001c05`, and on `inputs/vnnlib/cifar10_eps8_cnn7_idx8072_sample9.vnnlib.gz` gives
  `6b2f50fefbd4871361c7d17e80477ec0cd24879e`. I compared these with the live contents API at 2026-10-24T21:08:13Z to
  21:08:15Z (both requests HTTP 200):
  - `https://api.github.com/repos/VNN-COMP/vnncomp2026_benchmarks/contents/benchmarks/challenging_certified_training_2026/2.0/onnx?ref=main`
    lists `.../2.0/onnx/cifar10_eps8_cnn7.onnx.gz blob=f084be840473d8ebc88ccaaba50bbf1c57001c05 size=65214983`.
  - `.../2.0/vnnlib/cifar10_eps8_cnn7?ref=main` lists
    `.../cifar10_eps8_cnn7_idx8072_sample9.vnnlib.gz blob=6b2f50fefbd4871361c7d17e80477ec0cd24879e size=34824`.

  Both match. The sha256 values in `CLAIM.md` also match the claim files: onnx.gz
  `172f2bb1f3cfebb70875c361a56ca3217a19d1463d241020bbb93fc705c3dd6d`, vnnlib.gz
  `db437615a60f98e58989e7acfe165b3a6fc10d44ef5bc37ed4bdf3e568186fa5`, `object/...counterexample.txt`
  `38855485249d98be61182cb41f1c3d370a4e3208e0cf8efb2796feabc7f3cc29`, `object/..._v2.counterexample`
  `eaed7ec06e6c0430cb69508f60a86b7a38ddac2ddd15e0f142798cc389f5485a`, `object/...counterexample.npy`
  `923ce426ec4f25ef40500027d65de34a4f4c2c47799fb999143cbd411bcffe8d`.

## 4. This repository (V3R1T4S): trophy case, known-knowns, PRs and issues

- **Pinned copy** (commit `d14b0098c7dc3c372fa861a00175d3775aa097e7`, 2026-10-22T05:58:36-07:00, read only).
  - TROPHY_CASE.md: the only VNN-COMP rows are 51 and 52, both traffic_signs_recognition_2023 (`model_30_idx_1703`,
    `model_30_idx_178`).
  - known-knowns/vnncomp-2026-unsolved-instances/INDEX.csv lists the same two instances. Its one nested package,
    `2026-10-15-verexxi-0e0b0ccd`, is per PR #632 the 48x48 traffic-sign `model_48_idx_6371`.
  - A recursive grep of the whole pinned repo for `idx8072` returns nothing. The only `cnn7` / `certified_training`
    hit is `bank/targets.json`, which uses the category in the target description and gives no result.
- **Live main** (commit `1ebdef41c30414cd2a036b00f5e81d0fc4c1dc25`, committed 2026-10-24T16:13:09Z, read via `gh api` at
  2026-10-24T21:07:48Z).
  - The recursive tree (sha256 `e49a030f07630ba8def4ae850727750719a3401efe6da1940ad03fc80ee8874c`, not truncated,
    5439 entries) has the same known-knowns package list. It has 0 paths matching `idx8072` or `eps8_cnn7`.
  - The live TROPHY_CASE.md (read at 2026-10-24T21:07:58Z) has sha256
    `b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1`. That is identical to the pinned copy, and it
    has 0 matches for `idx8072|eps8_cnn7|certified_training`.
- **Live PRs and issues** (read-only `gh pr list` / `gh issue list`, `--state all`, 2026-10-24T21:03:30Z to 21:03:55Z).
  - Coverage: 687 PRs (#1 to #710; CLOSED=198, MERGED=150, OPEN=339; sha256
    `abdf762137b8673530384916eded413acf425a5e791b2e1d570aa696f8385db5`) and 23 issues (CLOSED=1, OPEN=22; sha256
    `7e9db7ff62794fe5faf21f5c3e330ec497203031678285e5ab7e098339b48efa`).
  - The first PR listing used `--limit 500` and returned exactly 500, so it was cut by my own limit. I re-listed with
    `--limit 5000`. That was pagination after a successful call, not a retry after a block.
  - No PR or issue title, body or branch name matches `idx8072` or `8072_sample9`.
  - **PR #566** ("submission(vnncomp-2026-unsolved-instance-counterexample): certified counterexample for unsolved
    tinyimagenet_eps1_wide_cnn7_idx7687_sample8", open, head `52bb8b2f7ba8d92f550618f0246fcd899daf4e21`) is the only
    `cnn7` hit. Its `how-we-built-it/polish_and_attack_cct.py` (line 121) lists
    `cifar10_eps8_cnn7_idx8072_sample9.vnnlib` as an attack target. However, none of the following contains a
    witness, margin or result for this instance: the PR's INDEX.csv, README.md, HOW_WE_FOUND_IT.md,
    how-we-built-it/README.md, panel/criterion.md, its 37-file list, or its 2 comments. It publishes a counterexample
    only for `tinyimagenet_eps1_wide_cnn7_idx7687_sample8`.
    This is a prior unsuccessful or unreported *attempt* on this instance, not a published counterexample, so it does
    not defeat novelty.
  - **PR #632** ("[bank] VNN-COMP: exclude archived counterexamples from new hunts") names the three archived results
    (`model_30_idx_1703`, `model_30_idx_178`, `model_48_idx_6371`). This instance is not among them.
  - PRs #631, #146 and #9: their file lists contain nothing for `idx8072` or `eps8_cnn7`.
  - Coverage limit: I inspected PR-branch file contents only for the five VNN-COMP-related PRs (#566, #631, #632,
    #146, #9). I screened the other 682 by title, body and branch-name text only.

## 5. Literature and web, last 24 months

- **Benchmark source repo: kkaulen/vnncomp_challenging_certified_training.**
  - Fetched at 2026-10-24T21:05:12Z: the page https://github.com/kkaulen/vnncomp_challenging_certified_training
    (HTTP 200, sha256 `d995a387220e59cf859c028e93201bfab66fc16e7bea9479f4df3012738c06d0`) and the API
    `https://api.github.com/repos/kkaulen/vnncomp_challenging_certified_training` (HTTP 200, sha256
    `8ca36ef14a10456753814257b0e458257d77804afa180ab30d55ccb310f252af`; pushed_at 2026-05-11T12:45:45Z).
  - Head is `63508e7d11eb7c551f123a9137d5adaa8790e0b0`. Its tree (fetched 2026-10-24T21:05:20Z, HTTP 200, sha256
    `9e3e8bc5086a5373cac16113fab8007163510c4b3c81fcc8b5734c16c64f414f`, not truncated) has 15 entries. None is a
    counterexample file.
  - `verification_results/cifar10_eps8_cnn7.json` at that commit (fetched 2026-10-24T21:05:34Z, HTTP 200, 1026015
    bytes, sha256 `cc59887d424fb623ce356beea655c01743b37eec606d6fcd4202b460807720e6`) has this entry for test image 8072:
    `{"result": "timeout", "method": "abCROWN", "running_time": 1004.6271016597748}`. That is the benchmark authors'
    own 1000 s abCROWN baseline, and it gives no verdict. Totals in that file: sat=6317, timeout=134, unsat=3549 over
    10000.
  - `metadata/sampled_instances.json` (HTTP 200, sha256
    `167c3d02596709393eca150d92aa76ef73e07b68d40405fb5b005e6c6501407a`; seed 42, "portable" mode) is a different
    sampling. Its `cifar10_eps8_cnn7` samples 7 to 9 are images 2527, 5631 and 1655, so it carries no data on the
    competition's idx8072 sample. The README (HTTP 200, sha256
    `d6b4a44719293e8fc57e0927865f43974199fd51ea51f5d378c4c374f49b4112`) puts samples 7 to 9 in the abCROWN "timeout"
    bin, which is consistent with the 8072 entry above.
- **GitHub code search** (`gh search code`, 2026-10-24T21:06:14Z to 21:06:17Z; GitHub indexes default branches).
  - `idx8072_sample9`: 13 hits. `cifar10_eps8_cnn7_idx8072`: the same 13 hits. They are the 1.0 and 2.0
    `instances.csv` in VNN-COMP/vnncomp2026_benchmarks, plus the 11 tool `results.csv` files above. None is a
    counterexample or a verdict.
  - `cifar10_eps8_cnn7 counterexample`: 0 hits.
  - `challenging_certified_training_2026`: 87 hits, all tool configs, readiness notes, results.csv files and the
    V3R1T4S target page. None of these names idx8072.
- **arXiv API** (export.arxiv.org, fetched 2026-10-24T21:06:26Z to 21:06:46Z, each HTTP 200).
  - `all:"VNN-COMP"` returned 24 results (sha256 `d814cfaa1e8e43479d4b133b1b3ad29cc40e840878543ea2495c2c59e1df0db5`).
    The newest are 2606.09377, 2605.23203, 2603.23878 and the VNN-COMP 2025 report 2512.19007. There is no VNN-COMP
    2026 report yet, and none of the 2026 abstracts mention this benchmark or counterexamples.
  - `all:"challenging certified training"`: 0. `all:CTRAIN AND all:verification`: 0. `all:"cifar10_eps8_cnn7"`: 0.
  - arXiv 2606.02134, "Rethinking Evaluation Paradigms in IBP-based Certified Training", published
    2026-06-01T12:00:15Z (fetched 2026-10-24T21:07:25Z, HTTP 200, sha256
    `e1b91eb7ca89d299d8589482694100fb06ddb3c1516732f95538a59259263743`). It is about Pareto fronts of aggregate
    accuracy, with no per-instance counterexamples.
- **Web search** (3 queries, including the exact string `"cifar10_eps8_cnn7_idx8072_sample9"`). There are no matches
  for the instance. The only hits in this category are PR #566 (a different instance) and the general VNN-COMP
  reports.
- **https://sites.google.com/view/vnn2026** (requested 2026-10-24T21:07:25Z with `curl -L`). It redirected to a Google
  sign-in page,
  `https://accounts.google.com/v3/signin/identifier?continue=https://sites.google.com/view/vnn2026&...`, with HTTP 200
  and sha256 `1abb6a5e82fca17bea92e690100510468a0567edf0cd7d28016c4f61e6602f65`. That is a login wall: the content
  could not be read, I did not retry and did not log in. This was not one of the required sources.

**Criterion (e): confirmed, as far as live search can.** I found no published counterexample, `sat` verdict or witness
for this exact ONNX + vnnlib pair, in either version directory. The only prior touch is the unreported attack attempt
in PR #566's script.

## 6. Injection check

injection_suspected: none. I scanned:
- the status page;
- the benchmark source README;
- all 687 PR and 23 issue titles and bodies (regex for agent-addressed text);
- PR #566's key files and its 2 comments;
- the arXiv abstracts.

The one keyword hit, on the status page, was the CSS class `scrollMarks` matching `llM`. No page or issue addresses AI
agents.

## Verdict

- (a) The live table, re-fetched at 2026-10-24T21:01:24Z (sha256 `ec1b6fcb…eb26f`, HTTP 200), shows the instance's Row
  with no `(h)` or `(v)` and `True Result: -`. No tool directory, of all 11, holds a counterexample or check.json for it.
- (e) No prior published counterexample exists for this exact pair.

The claim would be the first resolution of this instance.

pass: true
