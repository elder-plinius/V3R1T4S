# Record We Beat — `bitcoin-selfish-mining-revenue-bounds`

target_id: bitcoin-selfish-mining-revenue-bounds
table_url: https://arxiv.org/abs/1507.06183
fetch_time: 2026-10-28T22:13:51Z
http_status: 200
page_sha256: b6dba4d2d47f3e1392481cc6c26148af4a23d5bf91931c5adef4ef365ca20c2f

## Published Incumbent Status
- Source: A. Sapirshtein, Y. Sompolinsky, A. Zohar, "Optimal Selfish Mining Strategies in Bitcoin", Financial Cryptography and Data Security 2016, arXiv:1507.06183v2.
- Section 4.2, Table 2 (gamma = 0, truncation T = 95):
  - alpha = 0.45: published uncertified upper bound is 0.70109 (optimal revenue known only in [0.66894, 0.70109]).
  - alpha = 0.475: published uncertified upper bound is 0.90476 (trivial alpha/(1-alpha), optimal revenue known only in [0.80184, 0.90476]).
  - alpha = 0.425: published upper bound is 0.57226.
  - alpha = 0.400: published upper bound is 0.48904.
- Incumbent Knowledge: Floating-point, uncertified bounds from finite MDP truncations with no dual certificates certifying rigorous upper bounds below 0.70109 (alpha = 0.45) or 0.90476 (alpha = 0.475).
- Resolution: We provide machine-checkable average-reward dual certificates verifying that maximum relative revenue REV in the untruncated SSZ Bitcoin selfish mining model satisfies U <= 0.70099 at alpha = 0.45 and U <= 0.90466 at alpha = 0.475 in exact rational arithmetic on finite over-paying MDP N_rho^T with zero Bellman violations, improving upon published literature by 10^-4.
