context: subagent (executor)
# Novelty skeptic — Claim B, N = 3552 (p1 table integrity, CCD Riesz s=1)

## Live fetch (single, honest, no retries)
- URL: https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/site/s_1/index.html
- time: 2026-10-14T14:53:45Z (start) – 14:53:46Z, HTTP 200
- sha256: eeac3235eeba4835d635c6f07f8be6bb54466c2425bceba65ced315460fa649d (identical to scout fetch at 07:28:29Z — table unchanged)
- value, N = 3552 row: 6191355.6866585 (point file dat/points_3552_1.dat)

## Comparison
- claimed polished energy (mpmath dps 30): 6191355.686643545416998382
- live posted cell − claimed: 1.4955e-5 (> 1e-6 threshold; strict, not a tie)
- posted file raw energy per claim: 6191355.686658502748579249 (matches cell to 1e-9; discrepancy is under-convergence of posted coordinates)

## Known-results search
- Literature (last 24 months): arXiv 2610.08122 lists 6191355.686658503 for N = 3552 — same as posted cell, does not reach the polished value. Thomson2 cell 6191357.2579633 is higher. No other source found reporting a lower N = 3552 Riesz s=1 energy.
- repo elder-plinius/V3R1T4S TROPHY_CASE.md (fetched 14:53Z, HTTP 200): no mention of 3552.
- Open PRs: Thomson claims exist for N = 743, 745, 777, 1382 only; none for N = 3552.

## Verdict
Novel as a p1 table-integrity finding: the polished energy strictly beats everything known for N = 3552 by 1.4955e-5. Scope caveat: same basin as posted configuration (integrity finding, not new structure); energy recomputation is the reproducibility skeptic's job, not verified here.

pass: true
