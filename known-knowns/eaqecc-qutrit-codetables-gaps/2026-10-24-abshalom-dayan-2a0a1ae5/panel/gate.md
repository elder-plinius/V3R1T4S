# Honesty gate (main session), run 2026-10-24-1640

status: CONFIRMED_SOLUTION
confirmed_scope: The 26 x 56 GF(3) matrix S in object/eaqecc_28_9_11_7.json defines a [[28,9,11;7]]_3 EAQECC: it has 26 independent rows, rank(S J S^T) = 14 (c = 7) and k = 9, and its distance is exactly 11 as the minimum symplectic weight on span(S)^perp outside span(S) ∩ span(S)^perp (exhaustive over all 10-position subsets plus an explicit weight-11 non-isotropic witness), which is strictly above the d_lower = 10 and within the d_upper = 14 of the listed cell [[28,9,10-14;7]]_3 on https://eaqecc.codetables.de/qutrit.php as fetched 2026-10-24T17:42:49Z (sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c).

Claim: [[28,9,11;7]]_3 at the listed cell (n,k,c) = (28,9,7) of https://eaqecc.codetables.de/qutrit.php, object
claim/object/eaqecc_28_9_11_7.json (sha256 2a0a1ae5e178dcc0264b6a9f40ee1935991f28e65199a0712aecffe879b6c7d0), the
natural extended one-point Hermitian code E_17 over GF(9) ([28,15,11]_9, Hermitian hull 6).

Claim folder unchanged since the panel started: every file's sha256 equals panel/claim.sha256 (14 files, checked at
the gate). Self-break (self_break/verdict.md, main session, in a copy of claim/): SURVIVES.

Panel files read in full by the main session (each skeptic a fresh subagent, claude-opus-5-5, given only its own
copy of claim/, run one after another, never in parallel; times are the verdict files' write times):
- reproduce.md (written 17:14:55Z): own exact checker written before reading the author's code; exhaustive GF(3)
  position-subset test (all 13,123,110 10-subsets, none holding a vector of span(S)^perp outside the isotropic part)
  and its own weight-11 witness outside span(S); 1,016 brute-force agreements (40 where excluding the isotropic part
  changes the answer) and three seeded negatives caught (d = 1, 7, 10). s = 26, c = 7, k = 9, d = 11. The author's
  rebuild hash and every value of REPRODUCE steps 1-4 reproduced exactly, twice. pass: true.
- novelty.md (written 17:32:11Z): one honest GET at 2026-10-24T17:16:20Z, HTTP 200, sha256 37bbf731...,
  cell [[28,9,10-14;7]]_3; its own fixed-point closure of all 3888 entries under the page's rules gives 10 at
  (28,9,7), also with every code of the open PRs (#363, #403-#405, #643, #645, #646) added; TROPHY_CASE.md and
  known-knowns/ give nothing; 13 arXiv queries and 4 web searches (closest arXiv:2607.02170, qutrit codes n <= 26);
  codetables.de [28,15]_9 11-12 (2003 AG code; the table already uses a hull-4 [28,15,11]_9 via [[28,11,11;9]]),
  [27,15]_9 10-11, [29,15]_9 11-13. pass: true.
- criterion.md (written 17:48:38Z): every clause checked with its own code (s = 26, rank(S J S^T) = 14, c = 7, k = 9;
  exhaustive W = 10 subset test, 0 of 13,123,110; W = 11 gives 5211, matching the author; own non-isotropic
  weight-11 witness; 2 x 40 brute-force agreements); one GET at 17:42:49Z, byte-identical, cell listed verbatim;
  10 < 11 <= 14; c >= 1; non-catalytic. pass: true.

Live re-fetch at the gate: one plain curl GET, User-Agent "V3R1T4S-research-agent (honest single fetch)", no
retries, 2026-10-24T17:49:29Z to 2026-10-24T17:49:30Z (server date: Sat, 24 Oct 2026 17:49:30 GMT), HTTP 200,
628039 bytes, sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c (unchanged since 16:42:29Z),
cell verbatim `[[28,9,10-14;7]]<sub>3</sub>` (title "increasing dimension of [[28,2,10;0]] from codetables.de").
Saved in data/gate_fetch/. 11 > 10 and 11 <= 14.

Downgrade checks (none triggered): no hedging panelist (the caveat sections change nothing: the author's fetch was
17 minutes before the claim files, and the panel's own fetches are byte-identical); no reproduction mismatch (the
author's GF(9) information-set test and GF(3) subset test, run 1033's bz9, the self-break's numpy checker and Goppa
argument, REPRODUCE's and CRITERION's own exhaustive subset tests and witnesses all give d = 11); 11 strictly above
the live d_lower 10; no stretched criterion or hidden quantifier; scope no wider than reproduced; no sample presented
as complete; no capped search used as an exclusion; no probable prime; the table read only by honest single GETs. One
object, one cell. NOVELTY's local notes (a Python TLS failure before any request was sent, and two curl "URL
rejected" errors before sending, each then sent once) are not retries after a server block.

Caveats carried into the package and report, not downgrades:
- Journal-only qutrit papers not read (Cao-Li-Zhu IEEE TIT 2025, Liu-Li-Shi AMC 2025, Li-Li-Guan-Song IJTP 2024;
  arXiv:2607.02170 compares with them and states no qutrit code beyond n = 26), and closed PRs not searched.
- Wording: "improves the table cell", not "new technique" (one-point Hermitian EA codes, Christensen, Munuera,
  Pereira, Ruano; the Hermitian construction, Luo, Ezerman, Grassl, Ling). The classical [28,15,11]_9 is codetables'.
- Optimality not claimed (d_upper 14).
Not part of this claim: propagated cells (for example [[29,9,11;7]], [[30,9,11;7]] by lengthening, and five more
listed cells the claim beats beyond everything known, out of six in run 1500's sweep) and the run's other leads
(the [[33,8,16;15]]_3 X code is claimed separately in runs/2026-10-24-1727).
