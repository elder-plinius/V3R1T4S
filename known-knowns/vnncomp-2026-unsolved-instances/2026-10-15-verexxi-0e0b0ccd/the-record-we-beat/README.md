# The record we compared against

- table: VNN-COMP 2026 scoring table, https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_results/main/SCORING/results.txt
- fetched (UTC): 2026-10-15T00:58:03Z, HTTP 200, sha256 ec1b6fcbdef79539ffee17adbda2e99add137ba963a5306b87904035289eb26f (one plain curl; identical bytes to the
  fetches at 2026-10-14T20:00:35Z and 2026-10-15T00:28:04Z)
- selected headers of a HEAD request at 2026-10-15T01:05:39Z (HTTP 200): etag "3aaa631e8ff8cd8b7906e9dd4ef03db1d7dd1094ebd8586ddaf40ac13d84cea6", content-length 7681226, cache-control max-age=300
- extracted cell (the instance's row; three participating tools alpha_beta_crown, pyrat, vibecheck):
  `Row: ['3_48_48_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_BN_Dense_256_BN_Dense_43_ep_30-model_48_idx_6371_eps_3.00000', 'timeout', 'timeout', 'timeout']`
- the table's per-row log for this row (index 21) shows no "Checking counterexamples" entry (no tool claimed a
  violation), and the three tools' results.csv rows for it read timeout / run_instance_timeout / timeout.
- larger-radius siblings of the same image are solved '(v)': model_48_idx_6371_eps_5.00000 '4.0 (v)' (alpha_beta_crown).
