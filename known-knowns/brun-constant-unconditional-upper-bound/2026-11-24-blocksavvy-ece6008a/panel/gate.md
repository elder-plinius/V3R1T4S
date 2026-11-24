# Honesty gate (kit/RUN.md step 7): run 2026-11-24-0729, Brun's constant, bank partial win p1 (GRH)

gated: Tue Nov 24 08:46:31 UTC 2026 by the run's executor, after reading all three panel files in full (not edited).
panel files read (sha256): reproduce.md 4519f4aa7837e828139628721b98fea2210484209050c574c4d6f57f8a867e53, novelty.md f7c00289a3b2ee82ee6f0c7de306a9fbd8574aaad9fdc7070f008f68689bd3f5, criterion.md 22abf9dc407db718c20c23819ed3338e0743ee310b3397b7be2a5d179530cd3c
panel: REPRODUCE pass: true, NOVELTY pass: true, CRITERION pass: true (with confirmed_scope); three fresh subagent contexts launched by the parent session, each given only kit/RULES.md, its PANEL_BRIEFS.md section and a copy of claim/; panel files kept exactly as written.
prereg: sha256sum -c PREREG.sha256: PREREG.md OK. Threshold (gain >= 1e-4 over 2.1269872000642055706 at 128 and 256 bits, checker passing) met: 2.1257394310 (gain 0.0012478), checker 2.1257393973 at both precisions; control K1 reproduced 2.1269872000642055706.

## Downgrade checks (kit/RUN.md step 7), each judged literally
- hedging panelist: none; all three verdicts are unconditional passes. NOVELTY records residual risk: Halberstam-Richert, Opera de Cribro, Greaves, Montgomery-Vaughan and explicit Brun-Titchmarsh papers not opened (paywalled). It found the per-modulus combination itself KNOWN (Tao 254A Notes 4 eq. (28)), a credit gap fixed in claim_v2 (a), not a novelty failure of the bound.
- reproduction mismatch: none. REPRODUCE wrote its own weights, accumulator and evaluation; 22/22 rho levels' stated fractions equal (S + 2N sum|L| + N^2)/2^80 exactly; run_checks.sh PASS at 128 and 256; tamper tests and two own corruptions rejected. It did not re-verify the inherited e6b84d42 base (gated CONFIRMED in runs/2026-11-24-0527); confirmed_scope is explicitly contingent on it.
- value not strictly better than the live table: no. p1 bar 2.1594 (Dunn); claim 2.1257395. NOVELTY fetched https://teorth.github.io/optimizationproblems/constants/81a.html at 2026-11-24T08:20:13Z, HTTP 200, sha256 f8344f6ab5e7162878949de7b362dcbe4e5a54a48df35185e564e1901d4e0cc9 (best conditional 2.1594); under 1 hour old at gating. Re-fetch before any submission.
- stretched criterion or hidden quantifier: none; GRH for Dirichlet L-functions, upper bound only, main win not claimed. R_1 = E(x;1) - 1 detail inherited and harmless (claim_v2 (c)).
- scope wider than reproduced: no; confirmed_scope below is the CRITERION sentence verbatim.
- sample presented as complete / capped search: no; all 9906 intervals evaluated; the z <= 20000 cap is a stated scope limit of the method, not a sampled search.
- table value by evasion: none.
- several objects bundled: no; one bound, one certificate (verify/cert_rho_p128.json, sha256 ece6008a7d8615fe294374f58927b8b45aedbf478c39e5a88f346a90d4f8261c).
- same-cell overlap: this claim supersedes the contributor's own unmerged 2.126988 (e6b84d42 / PR #1232) for the same cell (claim_v2 (e)); not prior art for p1 (CRITERION).
Post-panel errata (wording only): claim_v2/ with CHANGES.md (a)-(f); margin about 1.0e-7 below 2.1257395.

status: CONFIRMED_PARTIAL
partial_win: p1 (GRH-conditional bound strictly below Dunn's 2.1594)
confirmed_scope: Assuming GRH for Dirichlet L-functions, the package's proof (Dunn's Theorem 3.1 framework with the inherited e6b84d42 changes, plus the per-modulus combination of the Selberg remainder in the 22 intervals with z_i <= 20000) and its arb/exact-integer certificate give B <= 2.1257393973... < 2.1257395, strictly below Dunn's 2.1594, which is partial win p1 and not the unconditional main win, contingent on the inherited e6b84d42 base being correct.
stands_only_if: python3 repo/kit/check_run.py prints CHECK_RUN: PASS for the run and for the package; otherwise the status is PROMISING.
