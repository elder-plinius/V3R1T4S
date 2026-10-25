# V3R1T4S panel: NOVELTY skeptic

context: subagent (Claude Code Agent tool, opus, fresh context, saw only claim/)

target id: vnncomp-2026-unsolved-instance-counterexample
instance: `challenging_certified_training_2026` (2.0) `onnx/cifar10_eps8_cnn7.onnx` + `vnnlib/cifar10_eps8_cnn7/cifar10_eps8_cnn7_idx4688_sample8.vnnlib`
claim files hashed by me (sha256sum, 2026-10-24T21:09:15Z), all equal to the values in `CLAIM.md`:
- `object/cifar10_eps8_cnn7_idx4688_sample8.counterexample.txt` e3c0ad30743d22fc7dd1050ab095a0b6c572a36de934bb8fe105009062f9cb75
- `object/cifar10_eps8_cnn7_idx4688_sample8_v2.counterexample` 7988a60d0148ba4a5110dc366b75c4d25f472d13a2052444780039f525889208
- `object/cifar10_eps8_cnn7_idx4688_sample8.counterexample.npy` e05e95b5399c3525024b9e65db5e5224d227cd95ebbe4285cd5ce2206775ce22

Scope: novelty only, meaning criteria (a) and (e) of `CLAIM.md`, plus this repository's own record. I did not re-run the
counterexample and make no statement on (b) or (c); that belongs to the other skeptics.

novelty: CONFIRMED (the live table still shows the instance as unsolved by every tool, and I found no published counterexample or verdict for this exact pair)

## 1. Deciding table (criterion a): one live fetch

- URL: https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_results/main/SCORING/results.txt
- time: request started 2026-10-24T19:31:45Z (server `date: Sat, 24 Oct 2026 19:31:45 GMT`), finished 2026-10-24T19:31:48Z
- HTTP status: 200; 7681226 bytes; etag "3aaa631e8ff8cd8b7906e9dd4ef03db1d7dd1094ebd8586ddaf40ac13d84cea6"
- sha256: ec1b6fcbdef79539ffee17adbda2e99add137ba963a5306b87904035289eb26f. This equals the hash in `CLAIM.md` for the claimant's
  three earlier fetches.
- The instance's row (line 12974, under `Category 2026_challenging_certified_training_2026:`, header line
  `8 participating tools: ['agate', 'alpha_beta_crown', 'n2v', 'neuralsat', 'nnv', 'pyrat', 'super_simple_vnn_comp', 'vibecheck']`):
  `Row: ['cifar10_eps8_cnn7-cifar10_eps8_cnn7_idx4688_sample8', '-', 'timeout', 'timeout', '-', 'timeout', 'timeout', '-', 'timeout']`
- My own parse (Python `ast.literal_eval` of the row, zipped with the tool list): 8 cells for 8 tools: agate `-`,
  alpha_beta_crown `timeout`, n2v `timeout`, neuralsat `-`, nnv `timeout`, pyrat `timeout`, super_simple_vnn_comp `-`,
  vibecheck `timeout`. No cell contains `(h)` or `(v)`. The next lines are `True Result: -` and a score of 0 for all 8 tools,
  with is_ver False and is_fals False. The CSV form of the same row at line 13578 is identical. The claim's
  `table/results_txt_excerpt.txt` shows the same row.
- Fetch-time gap: my session was cut by an API usage limit after these three fetches, and the rest of the checks ran from
  2026-10-24T21:02Z to 21:09Z. Following the kit (fetch once, no retries) and the coordinator, I did not re-fetch.
  Nothing points to a change in between: the tree fetch three seconds later shows main = eea564f5 (the claim records
  that commit as made on 2026-08-03), and the table bytes match the claimant's hash.

## 2. Results repo tree (criterion a, second half): one live fetch

- URL: https://api.github.com/repos/VNN-COMP/vnncomp2026_results/git/trees/main?recursive=1
- time: 2026-10-24T19:31:48Z to 19:31:54Z (server date Sat, 24 Oct 2026 19:31:49 GMT); HTTP 200; 10027325 bytes;
  sha256 8f7b2c70b39e468007149f341da977236ef0287d2f34700aa08456163d716960
- tree sha eea564f5d0a8751d8321a409214db14d03f452b8, `truncated` False, 27250 entries.
- Paths containing `idx4688`: 0. The tree has 116 counterexample files and 57 `.check.json` files in this category, all
  for other instances. The only ones for the `cifar10_eps8_cnn7` network belong to `idx8090_sample7` (alpha_beta_crown,
  super_simple_vnn_comp, vibecheck). No tool directory holds a counterexample or `.check.json` for this instance.
- Three tools that are not scored for this category also have `results.csv` files there. I fetched each once at commit
  eea564f5 (2026-10-24T21:02:14Z, all HTTP 200):
  - act: sha256 1671c7d346c9bb5ce390260753f82c2ac3d95e50888501013dc3ba3e0756271c; row (2.0 paths) result `unknown`
  - cora: sha256 26fa7313dbac743f7ab80a0a2a51f81c71ce3130c38aee2f53cf8cfd2c1428ba; row (1.0 paths) result `unknown`
  - nnenum: sha256 b7ce4367305d5899e30a0e9f0a8ecb58dfc5bcbfa53126f4ba058e49953d6465; row (1.0 paths) result `error_exit_code_1`

  None of the three resolved the instance. cora and nnenum ran the 1.0 version directory; I am noting that, not judging it.

## 3. Status source: one live fetch

- URL: https://github.com/VNN-COMP/vnncomp2026_benchmarks
- time: 2026-10-24T19:31:54Z to 19:31:56Z; HTTP 200; 250885 bytes; sha256 566a49d52bca938a2b26a320e702b4c90da09a922aa9367c4766496969ed5d74
- The page shows `"currentOid":"303f2327a8e8411efc4457da03d2016ce42733cf"` on `main` and 107 commits. That is the
  benchmarks commit `CLAIM.md` names as the source of both instance files. The page says nothing about this instance and
  nothing addressed to AI agents.

## 4. This repository (V3R1T4S)

- Pinned copy at commit d14b0098c7dc3c372fa861a00175d3775aa097e7 (read only):
  - `TROPHY_CASE.md` (sha256 b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1): the only VNN-COMP entries
    are rows 51 and 52, both traffic_signs_recognition_2023 (model_30_idx_1703 and model_30_idx_178).
  - `known-knowns/vnncomp-2026-unsolved-instances/INDEX.csv`: the same two traffic_signs witnesses, nothing else.
  - A whole-repo grep (excluding .git) for `idx4688|eps8_cnn7|challenging_certified|certified_training` matches only
    `bank/targets.json` and `known-unknowns/ml-robustness/vnncomp-2026-unsolved-instance-counterexample.md`. Both list
    `challenging_certified_training_2026` only as part of the open, unsolved set; neither mentions idx4688. The bare
    `4688` hits are numbers inside unrelated graph and code data files.
- Live PRs and issues of elder-plinius/V3R1T4S, read-only `gh`, 2026-10-24T21:02:58Z to 21:03:52Z:
  - My first `gh pr list` stopped at its 500 limit (prs.json sha256 af548ef26ad825e845ec6394543c82cf55700789cdbc169872126a695ac53c33),
    so I listed everything again with a limit of 5000. That gave 687 PRs, numbers 1 to 710: 339 OPEN, 150 MERGED,
    198 CLOSED (prs_full.json sha256 abdf762137b8673530384916eded413acf425a5e791b2e1d570aa696f8385db5). Issues: 23
    (issues_full.json sha256 7e9db7ff62794fe5faf21f5c3e330ec497203031678285e5ab7e098339b48efa).
  - Title and body scan: no PR or issue mentions `idx4688` or `eps8_cnn7`. PR #566 (open) matches only on the category
    name. It covers a different instance, `tinyimagenet_eps1_wide_cnn7_idx7687_sample8`, and its body contains 0
    mentions of idx4688, 4688 or eps8_cnn7.
  - `gh search prs/issues` covers comments too. To check that it works on these names, I searched for `idx7687` and the
    full name `tinyimagenet_eps1_wide_cnn7_idx7687_sample8`; both find PR #566. Searches for `idx4688`,
    `cifar10_eps8_cnn7_idx4688_sample8`, `eps8_cnn7` and `4688` return [] for both PRs and issues.

## 5. Literature and code, last 24 months (criterion e)

- Benchmark source https://github.com/kkaulen/vnncomp_challenging_certified_training (page 2026-10-24T21:04:19Z, HTTP 200,
  sha256 5827bacf93ebc77324b58883a1145c67f030d5c8a839176b9b4e6e2a52c619d3; API metadata HTTP 200, last pushed 2026-05-11T12:45:45Z;
  tree at 63508e7d11eb7c551f123a9137d5adaa8790e0b0, HTTP 200, not truncated):
  - `verification_results/cifar10_eps8_cnn7.json` (fetched 2026-10-24T21:04:33Z, HTTP 200, 1026015 bytes, sha256
    cc59887d424fb623ce356beea655c01743b37eec606d6fcd4202b460807720e6, git blob 6864713f9d7a5339d17bbc12b35b52f9e91791b4):
    key `4688` = `{'result': 'timeout', 'method': 'abCROWN', 'running_time': 1002.7726767063141}`. The file has 10000
    entries: 6317 sat, 3549 unsat, 134 timeout. The benchmark author publishes no verdict for this image, only a
    timeout at the 1000 s cutoff.
  - `metadata/sampled_instances.json` (HTTP 200, sha256 167c3d02596709393eca150d92aa76ef73e07b68d40405fb5b005e6c6501407a)
    does not contain 4688. It records a different seed's sample, which is not a problem. README (HTTP 200, sha256
    d6b4a44719293e8fc57e0927865f43974199fd51ea51f5d378c4c374f49b4112) gives aggregate timeout statistics only.
  - Second copy of the source, https://api.github.com/repos/Lemutisme/vnncomp_CCT (HTTP 200, not a GitHub fork, pushed
    2026-06-30T23:18:47Z): its `verification_results/cifar10_eps8_cnn7.json` has the same git blob 6864713f, so it carries
    the same `timeout` verdict.
- Issues and PRs of VNN-COMP/vnncomp2026_results, VNN-COMP/vnncomp2026_benchmarks and the kkaulen source repo
  (`gh`, 2026-10-24T21:07:50Z to 21:07:55Z): 0 PRs and 14 issues (1, 13 and 0); none mentions this instance, this
  network or the category.
- GitHub code search (`gh search code`, 2026-10-24T21:05:18Z to 21:05:25Z) for `cifar10_eps8_cnn7_idx4688_sample8`,
  `cifar10_eps8_cnn7_idx4688` and `idx4688_sample8`: 13 hits each, all in the competition repos. They are the two
  `instances.csv` files (1.0 and 2.0) in VNN-COMP/vnncomp2026_benchmarks and the 11 tools' `results.csv` in
  VNN-COMP/vnncomp2026_results. None is a counterexample. A search for `cifar10_eps8_cnn7` (21 hits) adds only the
  idx8090_sample7 check files and the two source repos' README, generator and metadata. The source repos'
  verification_results JSON files are about 1 MB, which may be too large for code search to index. I checked them
  directly instead (above).
- arXiv API: the `http://export.arxiv.org` requests (2026-10-24T21:05:56Z to 21:06:09Z) returned HTTP 301 with empty
  bodies (sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855). That is a redirect, not a block,
  so I sent one request to each `https://export.arxiv.org` URL instead (2026-10-24T21:06:22Z to 21:07:05Z, all HTTP 200).
  No URL was requested twice. Results: `all:"VNN-COMP 2026"` 0, `all:"challenging certified training"` 0,
  `all:"vnncomp_challenging_certified_training"` 0, `VNN-COMP AND CTRAIN` 0, `abs:"MTL-IBP"` 0, `abs:"adversarial attack"
  AND abs:"VNN-COMP"` 0. `abs:"VNN-COMP" AND abs:counterexample` 1 (2310.03033, 2023, traffic signs, out of window).
  `abs:"Verification of Neural Networks Competition"` 10; the newest competition report is 2512.19007 (VNN-COMP 2025,
  2025-12-22). There is no VNN-COMP 2026 report on arXiv.
- Web search (WebSearch, 5 queries: `"cifar10_eps8_cnn7" counterexample`, `"idx4688" cifar10 verification`,
  `"challenging_certified_training_2026"`, `VNN-COMP 2026 challenging_certified_training results counterexample unsolved`,
  and the VNN-COMP 2026 report): nothing relevant. The latest summary found is the 2025 one (https://arxiv.org/abs/2512.19007v1).

## Verdict

On criterion (a), my own parse of the live `SCORING/results.txt` (sha256 ec1b6fcb…eb26f, HTTP 200, 2026-10-24T19:31:45Z)
shows the row with no `(h)` or `(v)`, and the live tree (eea564f5, not truncated) holds no counterexample or
`.check.json` for this instance. On criterion (e), the source repo, its copy, the competition repos, this repo's
TROPHY_CASE, known-knowns, PRs and issues, GitHub code search, arXiv and the web show no published counterexample or
SAT verdict for this exact ONNX + vnnlib pair. The only published per-instance verdict is the benchmark author's
abCROWN `timeout` (1002.77 s). Every tool that ran it, scored or not, gave timeout, unknown, error or `-`. A valid
counterexample would therefore be a first resolution of the instance, not a tie or a replication. This passes on
novelty only; whether the witness itself is valid is for the other skeptics.

pass: true
