# claim_v2 vs claim/ (the panelled version); applied after the panel at the gate, per panel notes. No numeric change to U'', U', R.
1. CLAIM.md status-source line: removed the impossible "re-fetched ~17:20Z" (CLAIM.md mtime was 17:07:16Z). Replaced with the real fetches:
   ours 16:18:57Z and 16:57:58Z (file mtimes of data/tao_81a.html, data/tao_81a_refetch.html; same sha256 f8344f6a...), and the novelty
   skeptic's 17:11:43Z (panel/novelty.md), HTTP 200, still 2.1594.
2. PROOF.md A: states the inherited omission in Dunn Thm 2.1 (twin pairs with p+2 <= z) and the correction pi_2(x) <= S + pi_2(z); bound
   2 sum z_i/m_i <= 1.03e-15 (verify/check.py), included in the total 2.15696693552995885 < 2.156967.
3. Dunn numbering: "Theorem 3.3" -> arXiv:2504.15658v2 Theorem 3.1 (published BAustMS numbering not checked). Citation: Bull. Aust. Math. Soc.
   113(2) (2026) 293-303, doi:10.1017/s0004972725100233, online 2025-07-04 (Crossref, data/crossref_dunn.json, fetched 2026-11-23T17:37:23Z).
4. CLAIM.md: margins and z-choice sensitivity; U' = 2.1569562895 noted alone; headline unchanged (2.156967).
5. PROOF.md E: sources of inherited inputs (pi_2(4e18) verified in BKO 2013; PT Lemma 6 verified; Klyve Thm 5.7 not verified).
6. Added out/a_bound_certificate.json (from code/replay.py --cert, same run settings as U'') and verify/ (standalone checker).
7. Post-gate, pre-submit (2026-11-24T01:54-01:56Z): Klyve thesis Theorem 5.7 checked against the primary source (thesis PDF, sha256
   5f3e0034..., receipt in the run's verify/klyve/RECEIPT.md); PROOF.md E and README "Not claimed" updated (verified; matches Dunn Thm 2.1;
   Klyve's (5.27) confirms the pi_2(z) correction). Tao 81a re-fetched (unchanged, 2.1594); README and the-record-we-beat updated.
   No numeric change; panel files unchanged. Charter quarry 6 already read "formally verified in Lean by L. Alpoge, Nov 2026; not yet
   refereed" in both charter.md and prompt/charter.md, so no charter edit was needed.
