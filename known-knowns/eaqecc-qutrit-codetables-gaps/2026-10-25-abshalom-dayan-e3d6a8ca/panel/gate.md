# Honesty gate (main session), run folder 2026-10-25-0233

status: CONFIRMED_SOLUTION
confirmed_scope: The 42 x 70 GF(3) stabilizer matrix S in claim/object/eaqecc_35_7_16_14.json (sha256 e3d6a8ca...b73b4) has 42 independent rows and rank(S J S^T) = 28, so it defines a non-catalytic entanglement-assisted qutrit code with n = 35, c = 14, k = 7 whose minimum distance (minimum symplectic weight over span(S)^perp outside span(S) ∩ span(S)^perp) is exactly 16, which is strictly above d_lower = 15 and at most d_upper = 26 of the listed cell [[35,7,15-26;14]]_3 on https://eaqecc.codetables.de/qutrit.php as re-fetched 2026-10-25T03:52:24Z (HTTP 200, sha256 37bbf731...936c).

Claim: [[35,7,16;14]]_3 at the listed cell (n,k,c) = (35,7,14) of https://eaqecc.codetables.de/qutrit.php, object
claim/object/eaqecc_35_7_16_14.json (sha256 e3d6a8cad3db3a6ea28262ced2969b03a429b1ede488ae9cd59b69f5055b73b4), a
Construction X code over GF(9) from the Hermitian-curve AG codes C(D_28, 2Q + 8P_inf) [28,14,12] > C(D_28, Q + 8P_inf)
[28,10,16] (Q a place of degree 4) with a [7,4,4] tail and a column sign pattern: [35,14,16]_9 with Hermitian hull 7.

Claim folder unchanged since the panel started: every file's sha256 equals panel/claim.sha256 (16 of 16 files OK,
checked at the gate). Self-break (self_break/verdict.md, main session): SURVIVES.

Panel files read in full by the main session (each skeptic a fresh subagent, claude-opus-5-5, given only its own
copy of claim/, run one after another, never in parallel; NOVELTY started 03:37:22Z, CRITERION 03:51:48Z, REPRODUCE
04:17:45Z; verdict files written 03:51:14Z, 04:14:34Z, 04:57:55Z UTC by file time). A first REPRODUCE skeptic,
started 02:50:53Z in the run that the harness stopped at 03:34:13Z, left only an unfinished draft without a pass line
(panel/cutoff-0334/); it is not a verdict and was replaced by the fresh skeptic above.
- reproduce.md: own checker written from the definition before reading the author's code (mine/eacheck.py,
  mine/mine_bz9.c): s = 42, rank(S J S^T) = 28, c = 14, k = 7, dim N = 28, dim I = 14, N closed under w; a complete
  two-information-set enumeration of every codeword of weight <= 16 (7,304,564,710 + 1,006,817,254 codewords): none
  of weight <= 15, 7762 projective weight-16 words, none in I, so d = 16 exactly; 160 + 150 brute-force cases with 0
  failures; two full-size seeded negatives caught; byte-identical rerun; the author's steps 1, 2, 3, 5, 6 and step 4
  W = 16 part 0 reproduced exactly; its 7762 supports predict the step-4 per-part counts 2593, 2556, 2613. Steps 4
  W = 15 and W = 16 parts 1, 2 not run by it (covered by its complete enumeration; the evaluator ran all six parts).
  Disclosed: one of its brute-force tests peaked at 2.6 GB for about 134 s (over its 1 GB cap). pass: true.
- novelty.md: one honest GET at 2026-10-25T03:37:49Z, HTTP 200, sha256 37bbf731..., cell [[35,7,15-26;14]]_3;
  closure of all listed non-teleportation cells under the page's six rules gives 15, also with every open-PR code
  (9 PRs, none at n = 35), the known-knowns code, the workspace's unfiled codes and arXiv:2607.02170's qutrit codes
  added; teleportation seeding breaks 2658 d_upper values; TROPHY_CASE.md nothing; codetables.de [35,14]_9 16-19
  (Xing-Ling), no published hull-7 version found. Could not read: the arXiv API (HTTP 429, not retried) and the
  journal-only Cao-Li-Zhu paper. pass: true.
- criterion.md: every clause with its own code; own Brouwer-Zimmermann enumeration of 2,013,634,508 codewords,
  validated against brute force: d = 16; one GET at 03:52:24Z, byte-identical, cell listed; 15 < 16 <= 26; c >= 1;
  non-catalytic; page-rule closure 15; teleportation seeding invalid. Not a partial win: the full criterion.
  pass: true.

Live re-fetch at the gate: one plain curl GET, User-Agent "V3R1T4S-research-agent (honest single fetch)", no
retries, 2026-10-25T04:58:16Z to 2026-10-25T04:58:16Z (server date: Sun, 25 Oct 2026 04:58:16 GMT), HTTP 200,
628039 bytes, sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c (unchanged since the claim's
02:35:12Z fetch), footer "Last change: 10.07.2025". Saved in data/gate_fetch/. 16 > 15 and 16 <= 26.

Downgrade checks (none triggered): no hedging panelist (NOVELTY's "if the claimed d = 16 holds" leaves d to the
REPRODUCE skeptic, which confirmed it); no reproduction mismatch (methods A and B, bz64, goppa_x4.py, the
self-break, and complete enumerations by the REPRODUCE and CRITERION skeptics all give d = 16, with 7762 weight-16
supports in four independent counts); 16 strictly above the live d_lower 15; no stretched criterion or hidden
quantifier; scope no wider than reproduced; no sample presented as complete; no capped search used as an exclusion;
no probable prime; the table read only by honest single GETs. One object, one cell.

Caveats carried into the package and report, not downgrades:
- The classical [35,14,16]_9 parameters are codetables.de's (Xing and Ling 2000). Wording: "improves the table cell"
  with a hull-7 code, not "new technique".
- The same row lists [[35,7,16-26;15]]_3, so the gain is one entangled pair saved at d = 16. Optimality not claimed
  (d_upper 26).
- Literature: the arXiv API returned 429 to the NOVELTY skeptic; it searched by web search and single abstract pages
  instead. The search is not exhaustive for journal-only papers.
Not part of this claim: cells that follow by the table's rules (for example (36,7,14)).
