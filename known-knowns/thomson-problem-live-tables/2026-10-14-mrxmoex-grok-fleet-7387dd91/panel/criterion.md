# CRITERION skeptic — run 2026-10-14-0717 (claims D–I)
context: subagent (executor), fresh. Read only claim/ D_534 E_548 F_777 G_542 H_743 I_745 (claim.md, criterion.txt, scout_table.md, REPRODUCE.md, expected/, cand_*.txt, data/). Independent checks: float64 Coulomb energies of all six objects and posted Riesz files; regex of Riesz cells on saved ccd_riesz_s1.html; absence of N-rows in saved Deeter/Thomson/Thomson2/wiki pages; live HEAD/GET of Deeter e.<N>.txt, CCD Thomson xyz/<N>.xyz, Thomson2 xyz/<N>.xyz; float64 energy of any xyz that returned 200. Did not re-run full mpmath Newton/Hessian (relied on expected/cand_*_cert.json + float64 energy agreement).

Hessian style NUMERICAL (float64 eigvalsh + explicit Weyl bound, Cholesky half-shift) matches the verification_method’s own “Hessian in double” wording — not a fail by itself. Riesz-only rows: Deeter max 524; min over tables that list N is the Riesz cell when no other table has a row — that is allowed for full success. p3’s “beating only that table” is the weaker-cert fallback, not a bar on full cert for Riesz-only N≤1500.

## D_534 — not full; p3 only
- N≤1500, listed in ≥1 live table: N=534 in CCD Riesz s=1 (cell 135762.9050570). Other saved tables: no energy row. PASS for listing.
- ≥20 digits: cand_534.txt 534 lines × 40 decimals. PASS.
- E* vs table-min ≥1e-6: E*=135762.8145401324761574878; margin vs Riesz cell 9.051687e-2. PASS (table cells only).
- grad<1e-20, 2N−3=1065 eigs>0: grad2 6.12e-31, certified_min 3.55433, nneg=0 (expected/cand_534_cert.json). PASS on paper.
- Distinct basin from every posted table point file: claim polished only Riesz (+9.05e-2). Live GET CCD Thomson xyz/534.xyz → HTTP 200. Float64 energy of that file 135762.8145409166; gap to E* = 7.84e-7 < 1e-6. Same (or energy-indistinguishable) basin as a posted CCD Thomson configuration the claim never polished. Deeter/Thomson2 xyz → 404. FAIL distinct-basin for full success.
- Null: arXiv 2610.08122 lists ~135762.91066 for N=534 (above E*); not a criterion table. Wikipedia “534” hit is a combinatorial cell under N=181, not an energy row.
Verdict D: full success_criterion NOT met (hidden CCD xyz basin). Valid p3: mpmath improvement of the Riesz s=1 cell only, with cert stronger than p3’s grad/Lanczos bar.

## E_548 — not full; p3 only
Same pattern as D. E*=143066.8793744849140468194; Riesz cell 143067.0064628; margin 1.270883e-1; grad2 6.44e-23; dim_nonrot 1093; certified_min 0.422791; Riesz polish gap +1.270883e-1. Live CCD Thomson xyz/548.xyz → 200; float64 E=143066.8793746029; gap to E* = 1.18e-7 < 1e-6. FAIL distinct-basin for full. Verdict E: p3 only (Riesz-table improvement).

## F_777 — full success_criterion
- N=777≤1500; Riesz cell 289900.8082430; no Deeter/Thomson/Thomson2/wiki energy row. PASS.
- cand_777.txt 777×40 decimals. PASS.
- E*=289900.778533909713618485; margin vs Riesz 2.970909e-2 ≥1e-6. PASS.
- grad2 1.93e-27 <1e-20; dim_nonrot 1551=2·777−3; certified_min 3.32126; nneg=0. PASS (NUMERICAL Hessian allowed).
- Distinct basin: Riesz points_777_1.dat polished → 289900.8082429848528735925 (+2.970908e-2). Live HEAD: Deeter e.777.txt, CCD Thomson xyz/777.xyz, Thomson2 xyz/777.xyz all 404 — no other posted point file for N. PASS.
- Null: arXiv best ~289900.80824 (=Riesz), above E*.
Verdict F: meets the full success criterion literally.

## G_542 — not full; p3 only
E*=139913.0793830909490116457 beats Riesz cell 139913.1454539 by 6.607081e-2; grad2 1.87e-25; dim_nonrot 1081; certified_min 2.17976; Riesz polish +6.607085e-2. But live CCD Thomson xyz/542.xyz → 200 with float64 E=139913.0167982610, which is 6.26e-2 *below* E*. Posted CCD configuration is a lower basin; polishing it cannot yield E_polished−E*≥1e-6. FAIL full (distinct-basin; also shows the Riesz-only “win” is not best among CCD-hosted files). Verdict G: p3 only (beats Riesz cell; loses to unlisted CCD xyz).

## H_743 — full success_criterion
E*=264837.5287041150044362828; Riesz 264837.5858504; margin 5.714628e-2; grad2 1.57e-24; dim_nonrot 1483; certified_min 3.63360; Riesz polish +5.714625e-2. No other table row. Live HEAD Deeter/Thomson/Thomson2 point URLs → 404. PASS all full clauses. Verdict H: full success_criterion met.

## I_745 — full success_criterion
E*=266280.2015165256924341327; Riesz 266280.2589229; margin 5.740637e-2; grad2 1.53e-22; dim_nonrot 1487; certified_min 3.27909; Riesz polish +5.740639e-2. No other table row; Deeter/Thomson/Thomson2 point URLs 404. PASS all full clauses. Verdict I: full success_criterion met.

## Subsumption / stretch notes
- D and E are not new basins vs CCD Thomson’s own xyz/<N>.xyz; counting them as full would stretch “every posted table configuration.” They remain non-subsumed p3 vs the Riesz HTML cell.
- G is strictly dominated by CCD xyz/542.xyz; full is false; p3 vs Riesz stands.
- F, H, I are genuine full wins: only Riesz lists N, min=that cell, full local-min cert, and no other posted point file exists (404). Not reduced to p3 merely for being Riesz-only.
- Residual: full Newton/Hessian not re-executed here; recommend reproduce role runs `verify/hp.py` steps for F/H/I.

confirmed_scope: For N=777, 743, and 745, the claimed unit-sphere configurations have mpmath energies 289900.7785339097, 264837.5287041150, and 266280.2015165257 — each ≥2.97e-2 below the sole live-table value (CCD Riesz s=1), with tangent gradient <1e-20, all 2N−3 non-rotational Hessian eigenvalues numerically positive (float64 + Weyl bound), and a basin distinct from the only posted point file (Riesz) — and, separately, N=534, 548, and 542 improve that same Riesz table by ≥6.6e-2 under the same cert (p3) but fail full success because live CCD Thomson xyz/534.xyz and xyz/548.xyz match E* within <1e-6 and xyz/542.xyz lies 6.26e-2 below the claim.
pass: true
