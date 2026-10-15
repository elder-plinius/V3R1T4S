# Novelty skeptic verdict

Instance: 3_48_48_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_BN_Dense_256_BN_Dense_43_ep_30-model_48_idx_6371_eps_3.00000

## 1. Primary status source (fetched once by me, no retries)
- URL: https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_results/main/SCORING/results.txt
- Fetched: Thu Oct 15 00:58:51 UTC 2026 (date -u), HTTP status 200, 7681226 bytes. Byte-identical (cmp) to table_record/results.txt (operator fetch 2026-10-15T00:58:03Z, status 200), so the table did not change between the two fetches.
- Parsed myself (ast.literal_eval of every 'Row:' line). Exactly one Row matches the instance name (line 101928):
  `Row: ['3_48_48_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_BN_Dense_256_BN_Dense_43_ep_30-model_48_idx_6371_eps_3.00000', 'timeout', 'timeout', 'timeout']`
  followed by `True Result: -` and score 0 for alpha_beta_crown, pyrat, vibecheck.
  Tool cells containing '(h)' or '(v)': none (all three are 'timeout'). The neighbouring rows eps_1 (all timeout) and eps_5 ('4.0 (v)', timeout, timeout) are different instances.
- The same-idx rows for the 30 and 64 networks are different instances (30: '0.8 (v)'; 64: '4.1 (v)').
- Result: the instance is unsolved by every participating tool as of that fetch.

## 2. Published counterexample for this exact ONNX+vnnlib pair
- Web searches (3, standard and extended; exact instance name, 'idx_6371' + vnnlib + counterexample, VNN-COMP 2026 + traffic_signs_recognition_2023): no hit mentioning the instance, idx_6371, or a 2026 counterexample. Only the 2023 benchmark paper (arXiv 2310.03033), VNN-COMP 2023/2024/2025 summaries and the benchmark generator repo appeared.
- The 2023 benchmark instances.csv (https://raw.githubusercontent.com/ChristopherBrix/vnncomp2023_benchmarks/main/benchmarks/traffic_signs_recognition/instances.csv, fetched once 2026-10-15 01:03:05Z, HTTP 200) uses only idx 7040, 8258, 11985; idx_6371 is not in it, so no earlier VNN-COMP year can have a published solution for this pair. (A guessed 2026 instances.csv path returned 404, unused.)
- Limit: web search cannot rule out an unindexed publication; none was found.

## 3. This repo (V3R1T4S)
- TROPHY_CASE.md: https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md fetched once 2026-10-15 00:58:52Z, HTTP 200, 30486 bytes. grep for 6371, 3_48_48, model_48, traffic, vnn: the only VNN-COMP entries are rows 51-52, both network 3_30_30 (model_30_idx_1703 and idx_178, eps_1). This instance is not listed.
- Pull requests: GitHub web/API are 403 from this VM, so I re-ran the read-only git scan myself. `git ls-remote https://github.com/elder-plinius/V3R1T4S 'refs/pull/*'` at 2026-10-15 00:59:03Z: 172 refs = 144 PR heads + 28 merge refs (open PRs); main = 9b1d444eb864a1475e092047d49612a7410a7c5a. The ref list is identical (sorted diff empty) to novelty_record/v3r1t4s_pull_refs.txt. I shallow-fetched all 144 PR heads (`--depth 1 --filter=blob:limit=2m`, blobs over 2 MB were not fetched) and ran `git grep -I -l -E "6371_eps_3|model_48_idx|3_48_48_QConv|model_64_idx|3_64_64_QConv"` over every head: zero hits. Sanity check: the same tree search finds "3_30_30_QConv" in PR 1's TROPHY_CASE.md, INDEX.csv and README.md, and 'idx_6371' over all heads has no hits. So no open or closed PR mentions this instance.

## 4. Operator-reported evidence (novelty_record/README.md section A)
Treated as reported, unverified data. It says: 0 PRs and no relevant issues in the VNN-COMP results/benchmarks repos, last results commit 2026-08-03, row all-timeout, no published counterexample. Weight: low to moderate, corroborative only. My own independent checks (table parse, web search, V3R1T4S scan) carry the verdict; section A agrees with them (its row value matches my parse exactly) and I did not rely on it for any decision. I could not verify the VNN-COMP PR/issue lists myself (403), so that part rests on the operator's report plus the table's own state (no counterexample credited to any tool).

## 5. Literature, last 24 months
The 2024 and 2025 competition summaries and 2023 paper cover the benchmark family but none mention a 2026 instance; no paper or repo found reporting a counterexample for the 48x48 network at idx_6371. Nothing found that ties or beats the claim.

novelty: CONFIRMED NEW as of 2026-10-15 00:58-01:03Z. The live table shows 'timeout, timeout, timeout' for the instance (no '(h)'/'(v)'), no published counterexample for this exact pair was found, and the instance is absent from V3R1T4S TROPHY_CASE.md and all 144 PR heads. Residual caveats: web search is not exhaustive, VNN-COMP PR/issue lists were not independently verifiable (operator-reported only), PR blobs over 2 MB were not scanned. This verdict covers novelty only, not the validity of the witness.

context: subagent (same VM)
pass: true
