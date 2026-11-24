# Honesty gate (kit/RUN.md step 7): run 2026-11-24-0527, Brun's constant, bank partial win p1 (GRH)

gated: Tue Nov 24 06:14:14 UTC 2026 by the run's main session (executor follow-up), after reading all three panel files in full.
panel files read (sha256): reproduce.md 7702e4aeed3d86cb695b70b4c2787d136f468004d04a23214059953b5d299581, novelty.md 4873a258ea3ecf728c571281a09566af09a74a60337e7663782e5a57b94fb52a, criterion.md 02d2f5cc5d1740bb72c44d67717b5d458825b5842132cb2b703a315439dbeb50
panel: REPRODUCE pass: true, NOVELTY pass: true, CRITERION pass: true (with confirmed_scope); three fresh subagent contexts launched by the parent session, each given only kit/RULES.md, its PANEL_BRIEFS.md section and a copy of claim/; panel files kept exactly as written.
prereg: sha256sum -c PREREG.sha256: runs/2026-11-24-0527/PREREG.md OK (unchanged since 05:27Z). PREREG.md threshold (gain >= 1e-4 over 2.15696693552995885 from the stated method change, at 128 and 256 bits, weights-off control reproducing it) is met: 2.1269872 vs 2.1569669, control reproduced.

## Downgrade checks (kit/RUN.md step 7), each judged literally
- hedging panelist: none. All three verdicts are unconditional passes. NOVELTY records residual risk (Google Scholar 403 and Semantic Scholar 429, not retried; Halberstam-Richert, Opera de Cribro, Greaves, Montgomery-Vaughan not opened). It did read the status source, OpenAlex and Crossref (0 citations of Dunn) and arXiv; no source states a GRH bound below 2.1594. This is not a PENDING STATUS CHECK case (the status source was read). Listed for the human under Needs you.
- reproduction mismatch: none in the claim. REPRODUCE's own sieve, constants and arb evaluation at 256 and 128 bits give B <= 2.126987166958116 (< 2.126988), 2.7e-11 below the author checker's 2.1269871669853558245 (it used A = 0.01070009059 instead of 0.0107001). Its "defect 1" (program value lacks the pi_2(z) correction) was checked by this gate and does not hold: the program adds it (claim_v2/out/pi2z_included_test.txt, difference exactly 3.50925e-15); the stale certificate key name is documented in claim_v2/CHANGES.md (d). Its defect 2 (1.03e-15 vs 3.5092e-15) is fixed in claim_v2 (e).
- value not strictly better than the live table: no. p1 bar 2.1594 (Dunn); claim 2.126988. NOVELTY fetched https://teorth.github.io/optimizationproblems/constants/81a.html at 2026-11-24T06:01:30Z, HTTP 200, sha256 f8344f6ab5e7162878949de7b362dcbe4e5a54a48df35185e564e1901d4e0cc9 (best conditional 2.1594); under 6 hours old at gating, no re-fetch needed. Re-fetch again just before any submission.
- stretched criterion or hidden quantifier: none. Hypothesis GRH for Dirichlet L-functions (no stronger than Dunn's). Upper bound only; main (unconditional) win not claimed.
- scope wider than reproduced: no. confirmed_scope is the CRITERION sentence verbatim.
- sample presented as complete / capped search / probable prime: not applicable (all 9906 intervals evaluated in ball arithmetic).
- table value by evasion: none (plain fetches, UA names V3R1T4S; blocked Scholar/Semantic Scholar not retried).
- several objects bundled: no; one bound, one certificate (verify/cert_selberg_p128.json, sha256 e6b84d427b0fc63661a4011cd7bc2b4f1f35e60f75f3ac3411e8829b7d4ac92c).
- unresolved benchmark baseline: not applicable.
Post-panel errata (wording only, no number in CLAIM.md changes): claim_v2/ with CHANGES.md (a)-(e); checker now runs 128 and 256 bits, both PASS (claim_v2/out/check_selberg_both.txt).

status: CONFIRMED_PARTIAL
partial_win: p1 (GRH-conditional bound strictly below Dunn's 2.1594)
confirmed_scope: Assuming the Generalized Riemann Hypothesis for Dirichlet L-functions, the written proof in PROOF.md together with its arb-certified computation shows Brun's constant satisfies B < 2.126988 (sup 2.1269871669853558245), strictly below Dunn's conditional 2.1594, which meets partial win p1 and not the main (unconditional) win.
stands_only_if: python3 repo/kit/check_run.py prints CHECK_RUN: PASS for the run and for the package; otherwise the status is PROMISING.
