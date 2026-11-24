# claim_v2: post-panel errata (claim/ is kept exactly as the panel judged it)
Panel (runs/2026-11-24-0527/panel/, all pass: true) asked for wording fixes that do not change the claim B < 2.126988.
Applied here only; the certificate verify/cert_selberg_p128.json is byte-identical to the panelled one
(sha256 e6b84d427b0fc63661a4011cd7bc2b4f1f35e60f75f3ac3411e8829b7d4ac92c).

(a) PROOF.md A cited verify/check.py (a file of the earlier submission). Now cites verify/check_selberg.py, which adds 2 z_i/m_i per term.
(b) PROOF.md A/E/F: Dunn Lemma 2.2 (r(z) above 1e7) and M(z) are marked as used only by the weights-off control; the claimed bound uses Lambda(z).
(c) verify/check_selberg.py takes the precision as a second argument; verify/run_checks.sh now runs 128 and 256 bits and prints PASS only
    if both pass. Both give B <= 2.1269871669853558245 (out/check_selberg_both.txt, out/check_selberg_p256.txt).
(d) Panel note: "the program value 2.1269872000642055706 does not include the pi_2(z) correction". Checked and found NOT to hold:
    code/selberg_bound.py line 133 adds 2 z/m_i to each term, and a test copy with that addend removed gives sum_upper
    0.28339365690049545989 vs 0.28339365690049896914, a difference of exactly 3.50925e-15 = the correction
    (out/pi2z_included_test.txt). The real defect is the certificate's inherited key name 'B_upper_without_pi2z' and its 'note'
    text, which are wrong for this certificate. They are documented in PROOF.md S4 instead of edited, so the panelled object keeps
    its hash; the checker ignores both fields. Either way the claimed value comes from the checker, which includes the correction.
(e) PROOF.md A: the pi_2(z) correction for this certificate is <= 3.5093e-15 (arb sup 3.509248783e-15, out/pi2z_correction.txt),
    not the 1.03e-15 of the earlier submission.
Also: REPRODUCE.md's last command now runs both precisions; no number in CLAIM.md changes.
(f) Checker hardening (no change to the bound): verify/check_selberg.py now also fails if a stated term exceeds the recomputed one by
    more than 1e-5 relative (observed max slack 5.0e-6, from the author's coarser V/W table lookups), so a corrupted certificate is
    rejected in both directions. The total still uses the recomputed sups.
