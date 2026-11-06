# Honesty gate (main session), run 2026-10-24-1727

status: CONFIRMED_SOLUTION
confirmed_scope: The 40 x 66 GF(3) matrix S in claim/object/eaqecc_33_8_16_15.json (sha256 763a503e8ca0560a07e6c650f172b8de932bfd91474eafc5302c6a00013ab459) has rank 40 and rank(S J S^T) = 30, so it defines a non-catalytic EAQECC with (n,k,c) = (33,8,15) whose exact minimum distance (minimum symplectic weight of span(S)^perp outside span(S) ∩ span(S)^perp) is 16, strictly above the d_lower = 15 and within the d_upper = 23 of the listed cell [[33,8,15-23;15]]_3 on https://eaqecc.codetables.de/qutrit.php as fetched at 2026-10-24T19:06:27Z (HTTP 200, sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c).

Claim: [[33,8,16;15]]_3 at the listed cell (n,k,c) = (33,8,15) of https://eaqecc.codetables.de/qutrit.php, object
claim/object/eaqecc_33_8_16_15.json (sha256 763a503e8ca0560a07e6c650f172b8de932bfd91474eafc5302c6a00013ab459), a
Construction X code over GF(9) from the Hermitian-curve AG codes C(D_28, 4Q + 3P_inf) > C(D_28, 3Q + 3P_inf) (Q a
place of degree 3) with a [5,3,3] tail and a column sign pattern: [33,13,16]_9 with Hermitian hull 5.

Claim folder unchanged since the panel started: every file's sha256 equals panel/claim.sha256 (15 files, checked at
the gate). Self-break (self_break/verdict.md, main session, in a copy of claim/): SURVIVES.

Panel files read in full by the main session (each skeptic a fresh subagent, claude-opus-5-5, given only its own
copy of claim/, run one after another, never in parallel; times are the verdict files' write times, UTC):
- reproduce.md (written 18:52:45Z): own exact GF(3) checker written before reading the author's code (two disjoint
  information position sets, all 4,093,804,520 low-weight messages, early-stop bound 2 x 8 = 16), d(span(S)^perp) =
  16 and its own weight-16 witness outside span(S); 169 brute-force agreements and seeded negatives caught (d = 1, 15,
  11); a second run with other sets and a byte-identical rerun; REPRODUCE steps 1-5 reproduced exactly (rebuild hash,
  infoset m = 18 / 17 counts, both witnesses, subset test W = 15 all 0 and W = 16 2775/2832/2815, bz64 d = 16); its
  own count of distinct weight-16 supports, 8422, matches. pass: true.
- novelty.md (written 19:04:26Z): one honest GET at 2026-10-24T18:53:56Z, HTTP 200, sha256 37bbf731..., cell
  [[33,8,15-23;15]]_3; one-step rules and a full closure over 3764 non-teleportation cells give 15 at (33,8,15),
  also with every code of the 8 open PRs (#363, #403-#405, #643, #645, #646, #651), known-knowns and arXiv:2607.02170's
  14 qutrit codes added; TROPHY_CASE.md nothing; codetables.de [33,13]_9 16-18 (Ding-Niederreiter-Xing Construction X,
  since 2003; the table uses it only at hull 2, [[33,11,16;18]]), [33,14]_9 15-18; literature 2024-10 to 2026-10
  nothing at this cell; a web search for "[[33,8,16;15]]" found nothing. pass: true.
- criterion.md (written 19:22:45Z): every clause with its own code (s = 40, rank(S J S^T) = 30, c = 15, k = 8; dim
  span(S)^perp = 26, dim I = 10 two ways; closure under w; its own exhaustive GF(9) enumeration on two disjoint
  information sets, minimum 16; three weight-16 witnesses outside span(S)); the author's methods A, B (all three
  W = 15 parts, 0) and bz64 rerun and agreeing; one GET at 19:06:27Z, byte-identical, cell listed explicitly by
  row/column; 15 < 16 <= 23; c >= 1; non-catalytic; no table rule gives 16 at (33,8,15). pass: true.

Live re-fetch at the gate: one plain curl GET, User-Agent "V3R1T4S-research-agent (honest single fetch)", no
retries, 2026-10-24T19:23:20Z to 2026-10-24T19:23:21Z (server date: Sat, 24 Oct 2026 19:23:20 GMT), HTTP 200,
628039 bytes, sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c (unchanged since 17:27:46Z),
cell verbatim `[[33,8,15-23;15]]<sub>3</sub>` (title "lengthening of [[27,8,15;15]] quantum shortening of
[[28,7,16;15]] increasing dimension of [[28,5,16;13]] from arXiv:2207.05647"). Saved in data/gate_fetch/. 16 > 15 and
16 <= 23.

Downgrade checks (none triggered): no hedging panelist (the caveats change nothing: the author's fetch was 1h39m
before CRITERION's, and all four fetches are byte-identical); no reproduction mismatch (the author's methods A and B
and bz64, the self-break's numpy checker and Construction X argument, REPRODUCE's and CRITERION's own exhaustive
checkers all give d = 16, and three independent counts give 8422 weight-16 supports); 16 strictly above the live
d_lower 15; no stretched criterion or hidden quantifier; scope no wider than reproduced; no sample presented as
complete (every enumeration is exhaustive, with its count checked against the formula); no capped search used as an
exclusion; no probable prime; the table read only by honest single GETs. One object, one cell. NOVELTY's 301 redirect
on an arXiv API http request (one request to the https target, HTTP 200) is not a retry after a block.

Caveats carried into the package and report, not downgrades:
- The classical [33,13,16]_9 code is codetables.de's (Ding, Niederreiter, Xing 2000; listed since 2003). Wording:
  "improves the table cell" with a hull-5 version of it, not "new technique".
- Literature: mostly abstracts read; journal-only papers and closed PRs not searched.
- Optimality not claimed (d_upper 23).
- REPRODUCE.md says "Step 5 takes about a minute" in its header and "a few seconds" in step 5 (bz64 takes about 6 s);
  a wording slip found by REPRODUCE, no value affected. Left as is: the claim folder stays as the panel saw it.
- Process: the REPRODUCE skeptic's optional cross-check (mine/count16.py) exceeded its 1.5 GB memory cap (several GB
  by its estimate, not measured, about 3 minutes); disclosed in its verdict and in the run report. The verdict does
  not depend on it.
Not part of this claim: propagated cells ((34..36,8,15) by lengthening) and the run's two new leads from the
optimizer lens ([[33,7,15;12]]_3 and [[33,9,14;12]]_3, live leads for the next run).
