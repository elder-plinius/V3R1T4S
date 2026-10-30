# Record We Beat — `levine-hat-two-player-value`

target_id: levine-hat-two-player-value
table_url: https://arxiv.org/abs/2508.01737
fetch_time: 2026-10-29T08:07:00Z
http_status: 200
page_sha256: 78a1f96a58a69dd70d64216fb609a7d70c1cb00dc0fa21e92de2eaacc712e6dd

## Published Incumbent Status
- Primary Reference: Bouquet, Chikhi, Charles, Zhou, Wang, "On Lionel Levine's Hat Puzzle", arXiv:2508.01737v2 [math.PR] (19 Apr 2026).
- Status Source: arXiv:2508.01737v2 retrieved 2026-10-29T08:07:00Z (HTTP 200).
- Published Record:
  - Exact optima proved previously only for h <= 3: V_{2,1} = 1/4, V_{2,2} = 5/16, V_{2,3} = 22/64 = 11/32 (Carter-Reyes & Tiefenbruck, OEIS A345255).
  - For h = 4, Buhler et al. (2021) exhaustively verified symmetric strategies only.
  - Bouquet et al. (arXiv:2508.01737v2, Table 1 & Section 3) reported a numerical lower bound V_{2,4} >= 89/256 = 0.34765625 via local hill climbing, calling 4 <= h <= 6 "likely sharp, unproven".
  - Provable upper bound in literature remains V_2 <= 81/224 ~ 0.361607 (Buhler et al., 2021).
- Resolution: This package delivers an exhaustive canonical search over all 178,973,355 restricted growth string states covering all 4^{16} = 4,294,967,296 strategy pairs, unconditionally certifying that max wins is strictly 89 out of 256. This proves the exact rational equality V_{2,4} = 89/256 = 0.34765625, settling Bouquet et al.'s conjecture.
