# The record we compared against

- table: VNN-COMP 2026 scoring table, https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_results/main/SCORING/results.txt
- fetched (UTC): 2026-10-25T15:07:01Z and 18:11:59Z by the claimant (one plain curl each), HTTP 200, 7681226 bytes,
  sha256 ec1b6fcbdef79539ffee17adbda2e99add137ba963a5306b87904035289eb26f both times (also the skeptics' fetches,
  panel/); results repo main = eea564f5d0a8751d8321a409214db14d03f452b8 (committed 2026-08-03T14:03:54Z).
- extracted cell (line 102064; category 2026_traffic_signs_recognition_2023, tools in order alpha_beta_crown, pyrat,
  vibecheck):
  `Row: ['3_64_64_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_MP_2_BN_Dense_1024_BN_Dense_43_ep_30-model_64_idx_6371_eps_1.00000', 'timeout', 'timeout', 'timeout']`
- the results tree at eea564f5 (not truncated) has no file for this instance in any tool directory; vibecheck's
  results.csv names the 2.0 files for this instance and records timeout.
