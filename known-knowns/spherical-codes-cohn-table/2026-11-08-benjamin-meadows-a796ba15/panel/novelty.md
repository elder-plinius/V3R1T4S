# NOVELTY verdict: spherical-codes-cohn-table, cell 29-727

context: subagent (fresh context; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-08T02:36:30Z

## Value computed here
- Object object/29_727.txt, sha256 a796ba15c620c062792f104ee416a92acba3ab77cabe80ceedcf97f67e233ddc (matches CLAIM.md): 727 rows × 29 coordinates, at least 21 significant digits per coordinate.
- Max pairwise cosine after normalisation: float64 over all 263,901 pairs, then the top 200 pairs recomputed in mpmath at 50 digits. The max sits 5.9e-7 above the 200th pair, far beyond float64 error. c* = 0.2365029694576581825515, at 0-based pair (696, 721) (the file header says 697,722, which is the same pair counted from 1). Minimal angle 76.3197657509483°. 2,103 pairs lie within 1e-6 of c*.
- Live table cosine 0.240054045231. Margin c_table − c* = 3.55107577334e-3, well above the required 1e-10.
- https://spherical-codes.org/plain fetched 2026-11-08T02:34:26Z, HTTP 200, 373,199 bytes, sha256 9f26579e6f0842bb92f62f790943000afd787a1b2a0145476997b9620abbc493. Row `29,727,0.240054045231`.
- https://spherical-codes.org/ fetched 2026-11-08T02:34:28Z, HTTP 200, 4,564,675 bytes, sha256 0f9353613fea9193f1135cba56c09c0a3c9069d95b5578c5afb7466de31091ff. Row: `<a href="/data/29/727">727</a>` with no `&ast;`, cosine 0.240054045231, reference "Azmi C. Özgen, 2026." with no "needs more optimization".
- https://spherical-codes.org/data/29/727 fetched 2026-11-08T02:34:32Z, HTTP 200, 435,605 bytes, sha256 bc7648857920fcba1f07ec9a44fd4ac9b117b13083213122cc8abfe5917ed1db. It holds 727 × 29 coordinates at about 16 digits. Its max cosine is 0.2400540452303840, at pair (18, 22). That reproduces the table value to 6.2e-13, so the parser is sound.
- Fingerprint against the posted code: the sorted pairwise-cosine vectors differ by up to 0.386 (top cosines 0.236503 vs 0.240054). The frame-operator eigenvalues differ by up to 12.8. The object is not the posted code and not a rotation of it.
- Prior claims: `gh pr list -R elder-plinius/V3R1T4S --state all --search "spherical-codes"` was run at 2026-11-08T02:35:13Z and returned 27 PRs. Spherical-code claims in d=29 cover only (29,60), (29,72), (29,114) and (29,145). Searches for "29, 727", "29,727", "29-727", "29_727", "29 727", "N=727", "d=29" and "spherical 727" found no claim for (29, 727). Their only hits were the unrelated PR #727 (eaqecc) and the d=29 rows above.
- TROPHY_CASE.md on main, read through `gh api` (31,306 bytes, sha256 83af764f5a6551a5a27bbb135324931659bda04e60b66a2c0e711b991b356113): no mention of spherical codes, Cohn or 727.
- arXiv "spherical code", newest 15 by submission date (fetched 2026-11-08T02:34:34Z, HTTP 200, sha256 0ca177d4…8ace, 153 total hits): none of the entries mentions 727. The one directly relevant entry is arXiv:2610.19988 (I. Vahteristo, 2026-10-14, "New spherical codes by tuning an annealing solver"), which covers all N ≤ 1024 and 3 ≤ D ≤ 32, so (29, 727) is in its range. The live index already credits Vahteristo on 2,856 rows, which means that paper's results are in the table. The (29, 727) row is credited to Özgen 2026 instead, so the live value is at least as good as anything from that paper that was uploaded. The abs page (https://arxiv.org/abs/2610.19988, 200, sha256 3165b1db…fb89) links the code repository https://github.com/ilmari99/Spherical-code-solver. I did not download that repository.
- arXiv "Tammes", newest 15 (fetched 2026-11-08T02:34:36Z, HTTP 200, sha256 d65abefe…364d): every entry was an off-topic physics paper matched by "Tamm"/"Tamm-Dancoff". None gives a spherical code.
- Kissing-number clause: d = 29 is outside 9 ≤ d ≤ 23, so the clause does not apply.
- Side observation: c* = 0.23650 is below the live table values for N = 719…726 in d = 29 (0.23685 to 0.23986). This is consistent with a region of the table that is not yet well optimised. It does not bear on novelty.
- No steering text was found in claim/CLAIM.md.

## Clauses checked
- Live /plain row (29,727) exists and reads 0.240054045231: PASS
- c* is strictly below the table value by ≥ 1e-10 (margin 3.551e-3): PASS
- No `&ast;` proven-optimal mark on the index row: PASS
- No "needs more optimization" in the row: PASS
- Not superseded by a newer arXiv result. Newest-15 searches only; Vahteristo 2610.19988 is already in the table, and the row is credited to Özgen 2026: PASS
- Not a kissing-number configuration (d = 29): PASS
- No prior V3R1T4S PR or TROPHY_CASE entry for (29, 727): PASS
- Not a copy of the posted code (rotation-invariant fingerprints differ by 0.386): PASS

## Decision
The object beats the live table cosine for (29, 727) by 3.55e-3. The row carries no optimality mark and no unconverged flag, the object is not the posted code, and no prior V3R1T4S claim exists for this cell. The residual novelty risk is unpublished or un-uploaded work. Checking it was out of scope: the codes in Vahteristo's GitHub repository for arXiv:2610.19988, arXiv results beyond the newest 15 per query, and full-text mentions of N = 727. The table's Özgen 2026 credit for this row suggests the live value already absorbs the October 2026 annealing results.

pass: true
