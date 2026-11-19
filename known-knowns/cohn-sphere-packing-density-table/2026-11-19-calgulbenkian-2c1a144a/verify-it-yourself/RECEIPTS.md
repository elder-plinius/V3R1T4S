=== [1/4] Compiling strict ISO C99 zero-float verifier ===
=== [2/4] Running strict ISO C99 exact rational verifier ===
[C99 CALIBRATION] MOG Golay G_24 (4096 words) and unimodular Leech lattice basis (det(Lambda_24)=1) verified.
[C99 CALIBRATION] E_8 verified: det=1, min_sq=2, kissing=240, center_density=1/16.
[C99 PROVED] P19_II_vtx: det(G)=300, leech_sat=1, sym_trans_stab_size=1, norm4(L)=6858, min_sq=52/15, tau_sorted=(4022,4022,4072,4072,4072,4072), min=4022, max=4072, avg=12166/3, tight_pairs=8/15, triangles=2, connected=1, bilateral_contact_rank_trans=95/95, bilateral_contact_nullity_trans=0, bilateral_contact_rank_full=285/285, bilateral_contact_nullity_full=0
[C99 PROVED] P19_ChenHuLiWangWu2025_ref: det(G)=300, leech_sat=1, sym_trans_stab_size=1, norm4(L)=6942, min_sq=52/15, tau_sorted=(4110,4110,4110,4110,4110,4110), min=4110, max=4110, avg=4110/1, tight_pairs=6/15, triangles=2, connected=0, bilateral_contact_rank_trans=76/95, bilateral_contact_nullity_trans=19, bilateral_contact_rank_full=266/285, bilateral_contact_nullity_full=19
[C99 PROVED] Exact center density squared = 1461920290375446110677 / 184736485004425048828125 == (3^(-9) * 5^(-21/2) * 13^(19/2))^2 (MATCHES COHN LIVE RECORD).
[C99 PROVED] Strict Non-Isometry & Kissing-Stratum Vertex Isolation certified: leech_sat=1; sym_trans_stab_size=1; norm4(L_new)=6858 != norm4(L_ref)=6942; max(tau_new)=4072 strictly_below min(tau_ref)=4110; bilateral_contact_rank_trans=95/95 (nullity=0); bilateral_contact_rank_full=285/285 (nullity=0).
[C99 NEGATIVE CONTROL] Perturbed packing rejected as expected: pair (1,2) has 553 vectors strictly below 52/15 (min_sq = 48172/14415)
C99_VERIFIER: PASS
=== [3/4] Running independent Python stdlib fractions.Fraction verifier ===
[PY CALIBRATION] E_8 verified: det=1, min_sq=2, kissing=240, center_density=1/16.
[PY PROVED] P19_II_vtx: det(G)=300, leech_sat=1, sym_trans_stab_size=1, norm4(L)=6858, min_sq=52/15, tau_sorted=(4022, 4022, 4072, 4072, 4072, 4072), min=4022, max=4072, avg=12166/3, tight_pairs=8/15, triangles=2, connected=True, bilateral_contact_rank_trans=95/95, bilateral_contact_nullity_trans=0, bilateral_contact_rank_full=285/285, bilateral_contact_nullity_full=0
[PY PROVED] P19_ChenHuLiWangWu2025_ref: det(G)=300, leech_sat=1, sym_trans_stab_size=1, norm4(L)=6942, min_sq=52/15, tau_sorted=(4110, 4110, 4110, 4110, 4110, 4110), min=4110, max=4110, avg=4110, tight_pairs=6/15, triangles=2, connected=False, bilateral_contact_rank_trans=76/95, bilateral_contact_nullity_trans=19, bilateral_contact_rank_full=266/285, bilateral_contact_nullity_full=19
[PY PROVED] Exact center density squared = 1461920290375446110677 / 184736485004425048828125 == (3^(-9) * 5^(-21/2) * 13^(19/2))^2 (MATCHES COHN LIVE RECORD).
[PY PROVED] Strict Non-Isometry & Kissing-Stratum Vertex Isolation certified: leech_sat=1; sym_trans_stab_size=1; norm4(L_new)=6858 != norm4(L_ref)=6942; max(tau_new)=4072 strictly_below min(tau_ref)=4110; bilateral_contact_rank_trans=95/95 (nullity=0); bilateral_contact_rank_full=285/285 (nullity=0).
PY_VERIFIER: PASS
=== [4/4] Running negative-control corruption rejection checks ===
[NEGATIVE CONTROLS] Both C99 and Python verifiers exited non-zero on corrupted input.
PASS
