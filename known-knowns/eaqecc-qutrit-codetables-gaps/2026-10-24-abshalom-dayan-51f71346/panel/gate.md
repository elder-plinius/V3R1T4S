# Honesty gate (main session), run 2026-10-24-1500

status: CONFIRMED_SOLUTION
confirmed_scope: object/eaqecc_28_6_12_6.json (sha256 51f713462c7db831...) gives a 28 x 56 GF(3) matrix S (rows (x|z), form x.z' - z.x') for which my own code, working from S alone, finds s = rank(S) = 28, c = rank(S J S^T)/2 = 6, k = n - s + c = 6 and d = 12 exactly (no vector of span(S)^perp outside span(S) ∩ span(S)^perp is supported on any of the 21474180 sets of 11 positions, and a symplectic-weight-12 vector orthogonal to every row of S and outside span(S) exists on 0-based positions 15 to 26), so it is an [[28,6,12;6]]_3 EAQECC whose distance is strictly above d_lower = 11 and at most d_upper = 17 of the listed cell [[28,6,11-17;6]]_3, as read both in the author's table copy (fetched 2026-10-24 15:03:31 UTC per RECORD.md and its saved server Date header, footer "Last change: 10.07.2025", sha256 37bbf731030c113e...) and in my single live re-fetch at 2026-10-24 16:07:32 UTC (HTTP 200, 628039 bytes, byte-identical to that copy).

Claim: [[28,6,12;6]]_3 at the listed cell (n,k,c) = (28,6,6) of https://eaqecc.codetables.de/qutrit.php, object
claim/object/eaqecc_28_6_12_6.json (sha256 51f713462c7db831723702a4d0b0cc9a73faacd2552999a7007f75d393188573), the
natural extended one-point Hermitian code E_16 over GF(9) ([28,14,12]_9, Hermitian hull 8).

Claim folder unchanged since the panel started: every file's sha256 equals panel/claim.sha256 (14 files, checked at
the gate). Self-break (self_break/verdict.md, main session, in a copy of claim/): SURVIVES.

Panel files read in full by the main session (each skeptic a fresh subagent, claude-opus-5-5, given only its own
copy of claim/ made at 2026-10-24T15:16:56Z, run one after another, never in parallel; times are the verdict files'
write times):
- reproduce.md (written 15:33:08Z): own checker written and tested before reading the author's code; Brouwer-Zimmermann
  enumeration over two disjoint information sets (3 partitions) and a separate position-subset rank test; 161 + 30 +
  158 tests against brute force, seeded negatives on the claim's own S. Result s = 28, c = 6, k = 6, dim N = 28,
  dim I = 16, d = 12 (504 weight-12 vectors in I, 56448 outside; 1112832 of weight 13). Author's rebuild
  byte-identical and REPRODUCE steps 1-4 reproduced exactly, twice. pass: true.
- novelty.md (written 15:59:43Z): one honest GET at 2026-10-24T15:34:47Z, HTTP 200, sha256 37bbf731..., cell
  [[28,6,11-17;6]]_3; every single-rule source into (28,6,6) has d_lower <= 11 once teleportation cells are excluded
  as sources of increasing dimension (shown impossible: it would give [[28,14,21;14]] above the page's upper bound
  15); codetables.de [28,14]_9 12-13, [28,15]_9 11-12, [27,14]_9 11-12, [29,15]_9 11-13, [29,14]_9 12-14; the
  table's source arXiv:2207.05647 lists [[28,9,12;9]] (hull 5), arXiv:2105.02166 gives c >= 9 at d >= 12;
  TROPHY_CASE.md, known-knowns/ and the EAQECC/qutrit PRs give nothing. pass: true, with caveats (below).
- criterion.md (written 16:14:00Z): eleven clauses met when read literally (exact GF(3) matrix, s = 28 independent
  generators, c = 6 >= 1, k = 6, d = 12 by the criterion's definition, listed cell, re-fetched, 12 > 11, 12 <= 17);
  own GF(3) code shares nothing with the author's; own subset test (W = 11: 0 of 21474180) and own witnesses.
  One GET at 16:07:32Z, byte-identical. pass: true.

Live re-fetch at the gate: one plain curl GET, User-Agent "V3R1T4S-research-agent (honest single fetch)", no
retries, 2026-10-24T16:14:13Z to 2026-10-24T16:14:13Z (server date: Sat, 24 Oct 2026 16:14:13 GMT), HTTP 200, 628039 bytes,
sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c (unchanged since 15:03:31Z), cell verbatim
`[[28,6,11-17;6]]<sub>3</sub>` (title "increasing dimension of [[28,0,11;0]] from codetables.de"), footer
"Last change: 10.07.2025". Saved in data/gate_fetch/. 12 > 11 and 12 <= 17.

Downgrade checks (none triggered): no hedging panelist; no reproduction mismatch (five exact computations agree:
the author's GF(9) information-set test and GF(3) subset test, run 1033's bz9, REPRODUCE's Brouwer-Zimmermann and
subset test, CRITERION's own subset test with its own witnesses); 12 strictly above the live d_lower 11; no
stretched criterion or hidden quantifier found (symplectic weight, isotropic exclusion, c >= 1, listed cell, the
page's non-catalytic [[n,k,d;c]] convention checked); scope no wider than reproduced; no sample presented as
complete; no capped search used as an exclusion; no probable prime; the table read only by honest single GETs (no
browser User-Agent, cookies or retries). One object, one cell.

Caveats carried into the package and report, not downgrades:
- Teleportation neighbour: the page lists [[28,5,12-19;5]]_3 "using teleportation". Its increasing-dimension rule
  would give [[28,6,12;6]] if it applied to teleportation entries; the page does not apply it (the cell reads 11),
  and the source paper states that rule only for pure codes from the Hermitian construction. This object is a
  stabilizer EAQECC with c computed from S.
- Two qutrit stabilizer-code papers could not be read in full (IJTP 2026 paywalled; IEICE 2025 behind a bot check,
  not retried). They would matter only if they held a +1 record such as [[28,0,12]]_3 or [[29,1,12]]_3, which would
  make this a tie with a propagated code.
- Wording: "improves the table cell", not "new technique" (one-point Hermitian EA codes, Christensen, Munuera,
  Pereira, Ruano; the extension raising the hull, Luo, Ezerman, Grassl, Ling).
- Optimality not claimed (d_upper 17).
Not part of this claim: propagated cells (for example [[28,7,12;7]] and [[28,8,12;8]], which also beat listed cells)
and the run's other leads.
