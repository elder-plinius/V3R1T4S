# Re-fetch before packaging

Two live records were fetched again immediately before this package was built (plain GET with a User-Agent naming V3R1T4S, and one git clone). Both were unchanged since the panel's live comparison of 2026-10-20T03:16Z.

| Source | URL | UTC fetch time | HTTP / result | sha256 or head |
|---|---|---|---|---|
| 9a.md (primary table) | https://raw.githubusercontent.com/teorth/optimizationproblems/main/constants/9a.md | 2026-10-20T03:45:32Z | 200 | 92f6e1ee5d7219af29572c37dbb54192f3d12c2b1bc818aaf1c3e4ffe46d9899 |
| BPZ Lean repository (git clone) | https://github.com/spectra-research/shannon-capacity-lean | 2026-10-20T03:45:32Z | clone ok | head aa21eeb12b75b0413d3fa9fb4208b5d0bf2c4d65 (2026-08-10, "Update the bounds"); CertC23.lean sha256 843fffb9617918c93cea732ac708686b25a4cd7d469c4463af41e83e7cf0d016 |

The value this claim is compared against: Theta(C_23) >= 11.33455792275451814963309014607990805631803694025507 (CertC23.lean, degree 3040). The older BPZ version 1 value still printed in the 9a.md comment: 11.328224257774.
