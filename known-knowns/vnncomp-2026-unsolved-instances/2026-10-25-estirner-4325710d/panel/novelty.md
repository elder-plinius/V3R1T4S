# Novelty skeptic verdict

target: vnncomp-2026-unsolved-instance-counterexample
instance: traffic_signs_recognition_2023 (2.0) `onnx/3_64_64_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_MP_2_BN_Dense_1024_BN_Dense_43_ep_30.onnx` + `vnnlib/model_64_idx_6371_eps_1.00000.vnnlib`
object: `object/3_64_64_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_MP_2_BN_Dense_1024_BN_Dense_43_ep_30_model_64_idx_6371_eps_1.00000.counterexample.txt` (sha256 4325710daebb1a883c943578d1000983a547dcda305001938005135ba95f3a9b)
context: subagent (Claude Code Agent tool, opus, fresh context, saw only claim/)
verdict written: 2026-10-25T18:25:37Z
injection_suspected: none

novelty: PASS (new: no VNN-COMP 2026 tool resolved this instance, and no counterexample for this exact ONNX + VNN-LIB pair was published or claimed before, as far as an honest single-fetch search can see)

## 1. Status source (fetched once)

- https://github.com/VNN-COMP/vnncomp2026_benchmarks: HTTP 200, request at 2026-10-25T18:17:19Z, 250890 bytes,
  sha256 e906f4898d96a8d4162bb3cbd361d9c2b66da03555308bc1ce9aa0143cb70668 (dynamic HTML, so the claim's page hash
  differs, as expected). The page's `currentOid` is 303f2327a8e8411efc4457da03d2016ce42733cf, the same benchmark
  commit the claim cites.
- https://api.github.com/repos/VNN-COMP/vnncomp2026_benchmarks/commits/main: HTTP 200, 2026-10-25T18:19:25Z, sha256
  c42d8a1e5aeee8ea294cdc118113ae712a164c8725595ca6fe60ecc4fe2f9457; main = 303f2327a8e8411efc4457da03d2016ce42733cf.
- Directory listings of `benchmarks/traffic_signs_recognition_2023/2.0/vnnlib` and `.../2.0/onnx` (contents API, ref
  main): HTTP 200 at 2026-10-25T18:19:25Z / 18:19:26Z, sha256 d3d2ad091847306b8827100c26cdc144a820d9cc96f393ddd37341bcfd549483 /
  bbe2e239f287315b5b84b3330539f1ae6bed04d23815ba981ac39af43e65e038. Live blob ids: vnnlib.gz 021afd014a64d3b59a7c62f28d56c05bad4ca099
  (89129 bytes), onnx.gz b3515c781e420e63a4c0d0e775b4d55a2f1fd6ee (429719 bytes). `git hash-object` of
  `inputs/vnnlib/model_64_idx_6371_eps_1.00000.vnnlib.gz` and `inputs/onnx/3_64_64_..._ep_30.onnx.gz` gives exactly these
  two ids, so the claim's files are the live benchmark files.

## 2. Deciding table: own parse of the live results.txt

- https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_results/main/SCORING/results.txt: HTTP 200, request started
  2026-10-25T18:17:20Z, finished by 18:17:24Z (server Date header: Sun, 25 Oct 2026 18:17:21 GMT), 7681226 bytes,
  sha256 ec1b6fcbdef79539ffee17adbda2e99add137ba963a5306b87904035289eb26f (same hash the claim records).
- Results repo main: https://api.github.com/repos/VNN-COMP/vnncomp2026_results/commits/main, HTTP 200,
  2026-10-25T18:17:52Z, sha256 115ae82ccc35fb391f0b220abf73c022ba596bd502465901e28d8e708396f517; main =
  eea564f5d0a8751d8321a409214db14d03f452b8 (committed 2026-08-03T14:03:54Z), same as in the claim.
- Own parse: I read every `Row: [...]` line (3618 in the file) with `ast.literal_eval`, tracked the enclosing
  `Category` header and its `participating tools` list, matched the instance name exactly, and scanned every cell for
  `(h)` or `(v)`. Result: 1 Row hit, exact name match, at line 102064 in category `2026_traffic_signs_recognition_2023`
  (tools alpha_beta_crown, pyrat, vibecheck):
  `Row: ['3_64_64_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_MP_2_BN_Dense_1024_BN_Dense_43_ep_30-model_64_idx_6371_eps_1.00000', 'timeout', 'timeout', 'timeout']`
  No cell has `(h)` or `(v)`. The summary line 102263 agrees (`timeout, timeout, timeout`). The instance is in the
  all-tool-unsolved set.
- For context, the sibling rows for the same network and image are resolved: eps 3 (`4.1 (v)` alpha_beta_crown), eps 5
  (`3.3 (v)`), eps 10 (`2.5 (v)`, vibecheck `13.1 (v)`), eps 15 (`2.1 (v)`, vibecheck `12.6 (v)`). eps 1 is the only
  unresolved one for this pair.

## 3. Live results repository: check files and every tool's results.csv

- Tree https://api.github.com/repos/VNN-COMP/vnncomp2026_results/git/trees/eea564f5d0a8751d8321a409214db14d03f452b8?recursive=1:
  HTTP 200, 2026-10-25T18:18:01Z, sha256 8f7b2c70b39e468007149f341da977236ef0287d2f34700aa08456163d716960, truncated false,
  27250 entries. No path in any tool directory contains `model_64_idx_6371_eps_1.`, so there is no counterexample or
  `*.counterexample.check.json` for this instance. The 12 files for `model_64_idx_6371` are all for eps 3/5/10/15
  (alpha_beta_crown and vibecheck).
- Nine tool directories have a results.csv for this category. Each was fetched once from
  `https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_results/main/<tool>/2026_traffic_signs_recognition_2023/results.csv`
  (all HTTP 200, 2026-10-25T18:18:27Z to 18:18:30Z). The result recorded for this instance:
  - agate (2.0): unknown, sha256 12d99cd24ef856a52ca0559aa4dda9d020e090a807fb11f3c57048f8562445fe
  - alpha_beta_crown (1.0): timeout, sha256 5d81bbc9c686b6bca62a7cbd4198274bd7722c073d6d62153bc8d9d3468c2dca
  - n2v (2.0): timeout, sha256 5b558a7496afb90d593796ff76d8bcb4585c07a03f01564d8c3adc2e2dde4498
  - neuralsat (1.0): error_exit_code_1, sha256 16aa35410f433d974f6391c98df67dbac4bbb870c0a663a5df1e54c81c56f9b3
  - nnenum (1.0): error_exit_code_1, sha256 8a05a28d90d73ba2803d71a06a1c992b5c60df82a5385ef2328c54325388dbb0
  - nnv (1.0): timeout, sha256 ebe8da786037eff21d8b49726d64e67b6b0f80df57f80d96e2e600f345108c25
  - pyrat (1.0): run_instance_timeout, sha256 f40e0316c9ed4841194e74a905f4c4d403bf08b74360dc86b543b0375e5ca06f
  - super_simple_vnn_comp (1.0): no_result_in_file, sha256 134dfb5178b7d6754dd800abaece7033c3e88e241818a0521d71df94c1acf066
  - vibecheck (2.0): timeout, sha256 b8eee527133e3be95d4ae2ba97a639b5184b2fcbc451d87b689d8444e20f7ccc. Its line matches
    `table/vibecheck_results_csv_excerpt.txt`. The claim's hash 00a7f2bf... is for a different file (`vibecheck/results.csv`).
  No tool in either version directory reported sat or unsat, including the tools that were not scored in this category.
- Published counterexamples for the larger boxes. I fetched each once from the same results repo (all HTTP 200,
  2026-10-25T18:18:41Z to 18:18:47Z) and tested it against the eps-1 box of this vnnlib, comparing exact rationals:
  - alpha_beta_crown eps 3 (sha256 579185b97c07d7ce3dbcb64789800fe7097fba774fa71b6635325f026e3a08ca): 10582 coordinates outside the closed eps-1 box, max violation 2.0
  - alpha_beta_crown eps 5 (sha256 9dc4d7355b47231eb34aa8f11ec0131b65b7ea1429f5fc4d0cb92a861e32e561): 11118 outside, max 4.0
  - alpha_beta_crown eps 10 (sha256 a0c5ccf1cc496a5a321537ef2181697453321abc0b3d9b614cde2c1739e8372f): 11979 outside, max 9.0
  - alpha_beta_crown eps 15 (sha256 6791c4b182ce05f0f6b159b05675dd818947383ca560bb65e8255a79fb156f8a): 11774 outside, max 14.0
  - vibecheck eps 10 (sha256 c8a58dd31d6fd782eee791210bd60d2f31289079866ba66ee3e3d9d7792bba7d): 11911 outside, max 9.0
  - vibecheck eps 15 (sha256 02562a6309e0873b9920b35680b426c397cb5b10790ed7aa467d86da3360f5a9): 11998 outside, max 14.0
  None of these is incidentally a counterexample for the eps-1 pair. The same test on the claim's witness: 0 of 12288
  coordinates outside, 12288 of 12288 strictly inside.

## 4. Earlier VNN-COMP editions (2023-2025)

- Trees fetched once with `git/trees/main?recursive=1`, all HTTP 200, none truncated:
  - vnncomp2023_results at 3084a62ec39cb2cb419e33b23dacb44fdce1ca55: 2026-10-25T18:19:43Z, sha256 d89ebe910c94a33d35f2bcfc0653f6b9de39ab89d043cb0efef2eb54e39e5c18
  - vnncomp2024_results at 9a8fb29efa1e7c3400c766b1624cf22e1b9dc384: 18:19:46Z, sha256 64d855c2dc0ac0b743ed193a28b23de1c998e487ce8406c207f69143bc5a1303
  - vnncomp2025_results at ea89fbc2518b6729f17c96eeec22c56c88e496a9: 18:19:48Z, sha256 82ba4e0dc30a69666e16ba14cf2fcc1d3121469ed9fd53b3681345ee8e592a61
  No path in any of them contains `6371`.
- Their traffic-sign results.csv files: 2023 alpha_beta_crown, marabou, neuralsat, pyrat; 2024 alpha_beta_crown,
  neuralsat, pyrat; 2025 alpha_beta_crown, pyrat. All fetched once at 2026-10-25T18:20:01Z to 18:20:04Z, all HTTP 200.
  sha256s in the same order: 5525ae3e0e820eda11938b1d8d128695f210c5fa878b632fe86bdec230b52660, 74f40d68adc26b3ccce33bd7856ea4f99593b5169d46d92fb2a3f0b7d955c9d2,
  c68f42ce1110e54acb28b320c01474491f8f7330fc6307ad3bd9a563aba8780c, 02a0b58c9017cbe37aa139b74916dff950a682064fde88155a44b4e81830acb3,
  738dd2709a3dc3bd0cd926a42317953cdd7ed98ecee775d29481a57c9020b464, eafa845496de6a517efbbb8d53a11e611d1507b457bea98b25a1bfa362d77a51,
  c695c096455f4f12e2f92f7fc34f06c1d64344bcdfd0580faa29a59a7a657bc2, c8cb4614bf344b47fdfbe473b8fdedc4f7160a1395b00d1f8faa79e2513c7060,
  4322435c781be7e94c78cf0836e97b40d1547cf827261741e307e8041b550a91.
  Each has 0 lines with `idx_6371`. Those editions used images idx 11985, 7040 and 8258, so this pair was never posed
  before 2026.

## 5. The benchmark authors' repository

- https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_benchmarks/main/benchmarks/traffic_signs_recognition_2023/README.md:
  HTTP 200, 2026-10-25T18:21:59Z, sha256 9d6a6b5c7453821d51e6a14f170168eed1a17240b80a98bbd8b514375bd15688. It names the
  source repo https://github.com/apostovan21/vnncomp2023.git at commit 3587d3b11dc4ebffcf9784a93fb35a943eec5656 (directory
  listing via the contents API: HTTP 200, 18:21:53Z, sha256 46bd8b421efdbe9c6d726d023a2431acabe69406b5de6a92ad6d76437827164a).
- https://api.github.com/repos/apostovan21/vnncomp2023/commits?per_page=20: HTTP 200, 2026-10-25T18:22:07Z, sha256
  5ff16d16d3d55b583500c2a9c3d0af8440db98b2dd5265a154a171321b4bb4a5. The newest commit is 3587d3b1 (2023-07-03), so
  nothing was added after 2023.
- Tree at 3587d3b1 (recursive): HTTP 200, 2026-10-25T18:22:15Z, sha256 c858a3d20929ec662369eccb4cdea24ef9020c6c8e1e58fca553827f16e9b42f,
  not truncated, 12692 entries. The only `6371` path is the dataset image `GTSRB_dataset/Test/06371.png`. No path looks
  like a counterexample, adversarial example or result file.

## 6. Literature and web (last 24 months)

- Web searches (search tool, 2026-10-25), with no hit for this pair:
  - `"model_64_idx_6371" vnnlib counterexample`
  - `VNN-COMP 2026 traffic_signs_recognition_2023 counterexample unsolved instance 3_64_64 QConv Dense_1024`
  - `binarized neural network traffic sign GTSRB verification VNN-COMP counterexample 2025 2026 Postovan Erascu`
  - `"VNN-COMP 2026" summary and results` (no 2026 report found)
  - `"6371" GTSRB traffic sign binarized network robustness eps 1 counterexample`
  - `"traffic_signs_recognition_2023" counterexample github`
- https://arxiv.org/pdf/2512.19007 (VNN-COMP 2025 report): HTTP 200, 2026-10-25T18:23:41Z, sha256
  1805e75508c02ece68b767e9c0d10c4ecc83c21963c99f00f202d72dcd2f3074. No `6371` or `model_64_idx` in its text.
- https://ceur-ws.org/Vol-4263/short3.pdf (Schneider et al., TSR robustness verification with alpha,beta-CROWN):
  HTTP 200, 2026-10-25T18:22:57Z, sha256 bfe2db7ead8fdf6ac8346eb5c48539376573bcb11cd792b48d61b794c3a78ec4. It uses the
  authors' own models and gives no instance-level counterexample for this benchmark.
- GitHub-wide `gh search code` (2026-10-25T18:23:11Z to 18:23:13Z) for `model_64_idx_6371_eps_1.00000`, `model_64_idx_6371`
  and `idx_6371_eps_1`. The only hits are the benchmarks repo instances.csv files, the results repo results.csv and
  check files (none for eps 1 of model_64), and one diagnostic log in the V3R1T4S repo (see section 7).
  `gh search issues --include-prs "model_64_idx_6371"` (18:23:14Z) returned 0 results.

## 7. This repo (pinned copy at commit 1ebdef41) and its pull requests

- TROPHY_CASE.md has no entry for this exact instance.
- known-knowns/vnncomp-2026-unsolved-instances/: neither INDEX.csv nor the nested package index
  (`2026-10-15-verexxi-0e0b0ccd/INDEX.csv`) lists this instance. The nested package is for a different instance
  (48x48 network, model_48_idx_6371_eps_3.00000), and its README states under "Not claimed": "Anything about the other
  six unresolved 48x48 and 64x64 instances". The one mention of `model_64_idx_6371_eps_1.00000` in the repo is a
  diagnostic log line in that package
  (`how-we-built-it/attempts/exact-solver/code/validate_model.out`: "tgt 17 maxdiff 0.0 centre gap -276 cls 9 ..."),
  which gives instance statistics and no witness. It is not a prior claim.
- Pull requests (`gh pr list -R elder-plinius/V3R1T4S --state all`, read-only):
  - The full listing at 2026-10-25T18:21:14Z returned 734 PRs (sha256 2fb65a332936244af65b13fa92931916709d2c52b5a3f24b52460258dd7eff9f).
    I scanned all titles, bodies and branch names for `model_64`, `3_64_64`, `64x64`, `idx_6371`, `6371` and `Dense_1024`.
  - Searches at 18:20:42Z to 18:21:04Z: model_64_idx_6371, idx_6371, vnncomp, 3_64_64, traffic_signs, 6371, traffic,
    64x64, traffic-sign, unsolved-instance-counterexample, counterexample, model_64, eps 1.
  - Only two PRs touch this benchmark, and neither is about this instance: #146 (merged, model_48_idx_6371_eps_3) and
    #632 (open bank PR that lists the three already-archived traffic-sign instances, none of them 64x64).
  - File lists of all 10 VNN-COMP-related PRs (18:21:33Z) contain no `model_64` or `3_64_64` path.
  - Issues searched for "6371" and "traffic" (18:21:43Z): none for this instance.

## Conclusion

The criterion's novelty parts hold:
- (a) Own parse of the live table (sha256 ec1b6fcbdef79539ffee17adbda2e99add137ba963a5306b87904035289eb26f): this
  instance's row is timeout/timeout/timeout with no `(h)` or `(v)`, and there is no check file for it in any tool
  directory.
- (e) I found no previously published or claimed counterexample for this exact ONNX + VNN-LIB pair in the 2026
  results repo, the 2023-2025 editions, the benchmark authors' repo, recent literature, GitHub code search, or this
  repo's TROPHY_CASE.md, known-knowns and PRs. None of the published larger-eps counterexamples lies in the eps-1 box.

Settling an instance that no tool resolved, with no earlier witness, strictly beats everything known; it is not a tie.
This verdict covers novelty only. Soundness of the witness (validator replay, second runtime) is for the other
skeptics. The one quick check I ran, that all 12288 coordinates lie strictly inside the box, passed.

pass: true
