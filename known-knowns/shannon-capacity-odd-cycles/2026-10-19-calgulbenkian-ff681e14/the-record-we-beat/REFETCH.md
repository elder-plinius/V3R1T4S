# Re-fetch before packaging

Two live records were fetched again immediately before this package was built (plain GET with a User-Agent naming V3R1T4S, and one git clone). Both were unchanged since the panel's live comparison of 2026-10-20T03:16Z.

| Source | URL | UTC fetch time | HTTP / result | sha256 or head |
|---|---|---|---|---|
| 9a.md (primary table) | https://raw.githubusercontent.com/teorth/optimizationproblems/main/constants/9a.md | 2026-10-20T03:45:32Z | 200 | 92f6e1ee5d7219af29572c37dbb54192f3d12c2b1bc818aaf1c3e4ffe46d9899 |
| BPZ Lean repository (git clone) | https://github.com/spectra-research/shannon-capacity-lean | 2026-10-20T03:45:32Z | clone ok | head aa21eeb12b75b0413d3fa9fb4208b5d0bf2c4d65 (2026-08-10, "Update the bounds"); CertC13.lean sha256 7fe600d088d61ca22d06159c9c3f9003b2119dbc152ff72e47fe0361decfa971 |

The value this claim is compared against: Theta(C_13) >= 6.30292672931010853494960279947052989703296258437934 (CertC13.lean, degree 522). The older BPZ version 1 value still printed in the 9a.md comment: 6.302455083464.
