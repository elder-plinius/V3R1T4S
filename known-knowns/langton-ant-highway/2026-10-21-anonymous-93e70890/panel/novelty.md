# Novelty verdict — langton-ant-highway, 6x6 exhaustive highway-capture claim (p1)

context: fresh-context subagent session (no prior conversation), sees only claim/

Files judged: CLAIM.md, NOVELTY_RECORD.md (also listed METHOD.md, REPRODUCE.md, code/, data/ — not re-run; novelty role only). Scratch copies of fetched pages: scratch_novelty/.

## Status source (single plain request, UA "V3R1T4S novelty reviewer", no retries)
- URL: https://arxiv.org/abs/2505.05426
- HTTP 200, 38,195 bytes, fetched 2026-10-21T01:08:18Z UTC (2026-10-20 21:08 EDT)
- sha256 9d5f01827af97b964dc29f3c2a2c156d203f7395cdfee8277895f022e1db3a76 (identical to data/status/arxiv_2505.05426_abs.html in the package)
- Title "[2505.05426] Sideways on the highways" (V. Lutfalla). Versions listed: only [v1], Thu, 8 May 2025 17:14:05 UTC (339 KB).
- Value: the paper concerns generalised ants; the classical highway conjecture is treated as open. It contains no box enumeration.

## Sources named in NOVELTY_RECORD.md (one request each)
- Zenodo 10.5281/zenodo.21716510 -> https://zenodo.org/records/21716510, HTTP 200, 2026-10-21T01:08:25Z UTC. Jillhewar, "Finite-Support Periodic Highways of Langton's Ant ...", v1.3, published July 31, 2026. Excludes finite-support periodic highways of nonzero drift with period <= 48 and transverse widths 2 and 4; states "The Langton's ant highway conjecture remains OPEN". No exhaustive box-capture enumeration. Matches the package description.
- arXiv 2606.26677, HTTP 200, 2026-10-21T01:08:27Z UTC. Etse, "How Long Can the Escaping Ant Be Confined?", v1 25 Jun 2026. Exhaustive (branching) computation of exact *escape times from k x n rectangles* for k,n <= 9 (corrects OEIS A282425). This is confinement/first-exit time, NOT highway capture on the infinite plane with certificates, so it is not a prior instance of p1. Matches the package description.

## V3R1T4S repo (one request each)
- TROPHY_CASE.md (raw, main branch), HTTP 200, 31,235 bytes, 2026-10-21T01:08:27Z UTC: no mention of Langton / highway / langton-ant-highway. No existing trophy for this target.
- Open pull requests (GitHub API, state=open, per_page=100), HTTP 200, 2026-10-21T01:08:27Z UTC: 100 PRs returned (created 2026-10-19T06:29Z .. 2026-10-20T23:51Z UTC); none mention Langton/highway in title or body. CAVEAT: exactly 100 were returned, so older open PRs beyond page 1 were not seen (one-request limit). A web search for V3R1T4S + langton-ant-highway found nothing either.

## Literature search (last 24 months + classic)
Searched for exhaustive small-box Langton ant enumerations (Gajardo/Lutfalla/Rao "Ants on the highway", Natural Computing 2025; Lutfalla 2505.05426; Gajardo/Moreira/Goles complexity; Bunimovich-Troubetzkoy, Cohen-Kong unboundedness; OEIS A261990/A282425; udec Gajardo page; langtonsant.es / MrCamoga; matpic essay). Closest recent results found:
- H. Ke, Zenodo 10.5281/zenodo.22086967 (Aug 2026): Lean-checked proof that every state with exactly ONE black cell (any position/pose) reaches the period-104 highway. Infinite family, but only 1-black-cell patterns; does not cover all 2^36 patterns of a 6x6 box. Not a tie.
- Zenodo 10.5281/zenodo.23402413 (Oct 15, 2026): half-plane <=3-black-cell exit bound and 4-cell highway extension result. Not a box enumeration.
- Gajardo-Lutfalla-Rao 2024/2025: random 11x11 samples of generalised ants; one-black-cell-in-radius-3 simulations. Not exhaustive.
No published or otherwise known exhaustive, certificate-backed verification that every pattern in a 6x6 (or 5x5, or even 4x4) box leads the classical ant to the highway was found. Largest previously verified box (published): none found; the only exhaustive box-type computation found (Etse, 9x9) is for escape time, a different property. The package's own 4x4/5x5 runs are internal validation, not prior art.

## Assessment
- The claim is a first instance of p1 as far as I can find; therefore it strictly beats everything known (no tie, no re-derivation).
- Scope caveats correctly stated by CLAIM.md: one fixed ant placement/heading relative to the box; NUMERICAL (not a proof); exhaustive coverage rests on lant4 summaries. These do not affect novelty.
- Residual gap: open PRs older than 2026-10-19T06:29Z UTC not inspected (one-request limit). Low risk, but the parent should be aware.

novelty: NEW (no prior 6x6-or-larger exhaustive certified highway-capture verification known)
pass: true
