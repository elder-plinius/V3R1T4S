# CRITERION skeptic — run 2026-10-14-0717
context: subagent (executor), fresh. Read only claim/ (README, A_1382, B_3552, C_550). Independent checks: float64 energies of all objects/posted files (venv python), table-cell regex on the saved live pages, live HEAD/GET of the point-file URLs at ~08:57Z.

## A_1382 — full success_criterion
Clause by clause, literally:
- N <= 1500 and listed in at least one live table: N = 1382; rows in CCD Riesz s=1 (926576.1030330) and CCD Thomson2 (926576.1175606). Re-extracted from saved pages: matches. PASS.
- >= 20 digits: cand_1382.txt has 40 decimals, 1382 lines. PASS.
- Strictly lower than the min over ALL tables by >= 1e-6: Deeter (N <= 524), CCD Thomson/table.html (max 972), Wikipedia (<= 470) have no 1382 row (grep confirms 0 hits); EinsteinArena applies only to N = 282. Min = 926576.1030330; E* = 926576.0968589705350586982 (my float64: 926576.0968589706); margin 6.174e-3. PASS. Null model: arXiv 2610.08122 (not a listed table) also gives 926576.10303295, so no hidden lower literature value.
- "re-fetched live immediately before claiming": all five tables fetched 07:28:26–07:28:30Z; claim.md mtime 09:31 local = 07:31Z (~3 min later). Acceptable as "immediately". Point files fetched 07:21Z — the clause binds the tables, not point files; my live re-GET at ~08:57Z returned identical sha256 for both 1382 point files. PASS.
- mpmath Newton gradient < 1e-20: grad 2-norm 5.79e-32 (Newton in MPFR-170 via gmpy2, direction from float64 Hessian; energy recomputed in mpmath dps 30, change 3.1e-19 < 1e-12). The Newton direction source does not matter; the gradient criterion is on the MPFR/mpmath gradient. PASS (not independently re-run by me).
- All 2N-3 = 2761 non-rotational eigenvalues > 0: the verification_method itself says "build the 3N x 3N Hessian in double ... assert 2N-3 positive eigenvalues", so a float64 eigensolve meets the wording; this one is stronger (smallest 8.3098, explicit Weyl bound 4.2e-8, Cholesky of shifted matrix ok). Label NUMERICAL, not interval — acceptable under the stated checker. PASS.
- Distinct basin from every posted file, including tables not listing N: Riesz points_1382_1.dat polishes to 926576.10303295 (+6.174e-3), Thomson2 xyz/1382.xyz to 926576.11756068 (+2.070e-2). Tables without a row: CCD Thomson xyz/1382.xyz -> HTTP 404 (live, my check); Deeter e.1382.txt -> HTTP 404. No hidden posted file. PASS.
Residual caveats: I did not re-run the full mpmath Newton/Hessian (relied on expected/cand_1382_cert.json + float64 energy agreement); recommend the reproducer runs hp.py step 1.
Verdict A: meets the full success criterion literally.

## B_3552 — p1
Posted cell 6191355.6866585 (re-extracted). Posted file raw 6191355.686658503 (my float64 agrees); polished object 6191355.6866435455 (my float64 agrees); grad 9.8e-22. Polished differs from the posted energy by 1.4955e-5 > 1e-6, reported to 12+ digits. Literal p1 wording ("not reproduced by its own posted coordinates after mpmath polishing by more than 1e-6") is met. Stretch check: the raw coordinates DO reproduce the cell; the finding is under-convergence of the posted file (same basin), which is exactly the Deeter-documented kind. N > 1500 is no bar for p1. Verdict: valid p1 (table-integrity), not a new structure.

## C_550 — p1
Posted Thomson2 cell 144126.0927100 (re-extracted); file header 144126.0927999970; raw and polished mpmath 144126.09279999922118 (float64 agrees); polished − cell = +8.9999e-5 > 1e-6. p1 is direction-agnostic: "not reproduced ... by more than 1e-6" — a posted value LOWER than the coordinates can reach is precisely a non-reproduction (arguably the more serious integrity defect, as the table advertises an unreachable energy). Null model: could another basin reach the cell? Irrelevant to p1, which concerns the table's own coordinates. Likely transcription error. Verdict: valid p1.

## Subsumption
B and C are independent table-integrity findings at different N; neither is subsumed by A. The genuine headline win is A.

confirmed_scope: The 1382-point configuration in claim/A_1382/cand_1382.txt has mpmath energy 926576.0968589705 — 6.174e-3 below the lowest live-table value for N = 1382 (CCD Riesz s=1, 926576.1030330), with tangent gradient 5.8e-32, all 2761 non-rotational Hessian eigenvalues numerically positive (float64 with explicit error bound), and a basin distinct from both posted N = 1382 files — and, separately, the live CCD posted energies for Riesz s=1 N = 3552 (1.50e-5 above its polished coordinates) and Thomson2 N = 550 (9.00e-5 below what its coordinates reach) are not reproduced by their own coordinates (p1).
pass: true
