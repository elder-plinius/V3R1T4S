# claim_v2: post-panel errata (wording only; no number, code path or certificate changes). claim/ stays as judged.
Panel: runs/2026-11-24-0729/panel/{reproduce,novelty,criterion}.md, all pass: true (files untouched).
(a) PROOF.md / PROOF_DELTA.md R2: relabelled from PROVED-HERE to KNOWN (standard rearrangement), crediting Tao 254A Notes 4 eq. (28)
    (lambda+_d = sum_{[d1,d2]=d} rho_d1 rho_d2) and Vaughan's Selberg notes; "applied numerically to Brun's constant here for the first
    time as far as the panel's search found" (NOVELTY section 3).
(b) PROOF_DELTA.md preamble: the other intervals' FORMULA is unchanged but their z_i were re-chosen (+7.6e-9 in total).
(c) PROOF.md / PROOF_DELTA.md R2: R_1 = E(x;1) - 1 because p = 2 is excluded (inherited from Dunn; harmless).
(d) REPRODUCE.md: the checker's sieve (wvcount) uses min(8, cpu count) threads; documented pinning with taskset (no env var exists).
(e) CLAIM.md: intended to supersede 2026-11-24-blocksavvy-e6b84d42 / PR #1232 (2.126988) for the same cell; five rho intervals sit at
    the 20000 cap.
(f) Margin note added (CLAIM.md, PROOF R4): the certified value is about 1.0e-7 below the claimed 2.1257395.
Certificate verify/cert_rho_p128.json unchanged: sha256 ece6008a7d8615fe294374f58927b8b45aedbf478c39e5a88f346a90d4f8261c.
