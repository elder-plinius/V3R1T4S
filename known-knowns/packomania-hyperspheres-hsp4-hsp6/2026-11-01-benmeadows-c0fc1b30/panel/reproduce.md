# REPRODUCE verdict: hsp4-N214

context: subagent (fresh context started by the packaging session's Agent tool; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-01T21:06Z

## Value computed here
- r* = 0.20388671005401594317 (binding term: half minimum pairwise distance; 1 - max|c_i| = 0.2038867100540159982519296)
- table (claim/hsp4_radius_live.txt row 214) = 0.203884464476
- r* - table = 2.24557801594317e-6
- Coordinate precision: 18-20 significant digits per number (scientific notation, 20-digit mantissas; fewer only where trailing zeros dropped).

## Clauses checked
- Parse: object sha256 c0fc1b30...dc67 matches CLAIM.md; 214 non-comment rows, 4 numbers each, no NaN/inf, no duplicate rows. PASS.
- Recompute r* in mpmath at 50 digits (work/rep.py): 0.2038867100540159431742318, no tolerance. PASS.
- Second independent computation: exact Fractions for squared distances/norms + 60-digit Decimal sqrt gives identical r* (difference 0.0 at 50 digits); exact rational check confirms 4(T+1e-10)^2 <= min squared distance and (1-T-1e-10)^2 >= max squared norm. PASS.
- Margin r* - table = 2.2456e-6 >= 1e-10. PASS.
- Note: no evidence/ folder (FETCHED.md) was supplied to this skeptic, so the table value was read from claim/hsp4_radius_live.txt (sha256 f3ddaa94...569f) as provided; the live-refetch provenance itself was not verifiable here. Comment lines in the object file state the same values; they were ignored and recomputed. No injection suspected.

## Decision
Independently recomputed r* agrees across two methods and exceeds the table value 0.203884464476 for N = 214 by 2.2456e-6, far above the 1e-10 threshold. The other clauses of the success criterion (non-isometry, polish comparison, queue/history checks) are outside the REPRODUCE role.

pass: true
