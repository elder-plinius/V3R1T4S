# Honesty gate (main session), run 2026-10-24-1953

status: CONFIRMED_SOLUTION
confirmed_scope: The 38 x 66 GF(3) stabilizer matrix S in object/eaqecc_33_7_15_12.json has 38 independent rows, c = rank(S J S^T)/2 = 12 and k = n - s + c = 7 at n = 33, and the minimum symplectic weight of span(S)^perp outside span(S) ∩ span(S)^perp is exactly 15, strictly above d_lower = 14 and at most d_upper = 23 of the cell [[33,7,14-23;12]]_3 listed on https://eaqecc.codetables.de/qutrit.php as fetched at 2026-10-24T21:29:07Z (HTTP 200, sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c).

Claim: [[33,7,15;12]]_3 at the listed cell (n,k,c) = (33,7,12) of https://eaqecc.codetables.de/qutrit.php, object
claim/object/eaqecc_33_7_15_12.json (sha256 5713c745e8e837dc41e1883a120488fb38dce3b4254292335ca98f99a1787256), a
Construction X code over GF(9) from the Hermitian-curve AG codes C(D_28, 4Q + 4P_inf) > C(D_28, 3Q + 4P_inf) (Q a
place of degree 3) with a [5,3,3] tail and a column sign pattern: [33,14,15]_9 with Hermitian hull 7.

Claim folder unchanged since the panel started: every file's sha256 equals panel/claim.sha256 (15 of 15 files OK,
checked at the gate). Self-break (self_break/verdict.md, main session, in a copy of claim/): SURVIVES.

Panel files read in full by the main session (each skeptic a fresh subagent, claude-opus-5-5, given only its own
copy of claim/, run one after another, never in parallel; times are the verdict files' write times, UTC):
- reproduce.md (written 21:11:52Z): own GF(3)-only Brouwer-Zimmermann checker (mine/bz3.c) written before reading
  the author's code: two disjoint full sets to level 7, 8054538032 words, bound 16, so d = 15 exactly over all of
  span(S)^perp, with 39784 weight-15 words on 9946 supports outside the isotropic part; 846 brute-force agreements
  (n = 3..7) and two seeded negatives caught; a shuffled-order run and a byte-identical rerun; the author's steps 1-5
  reproduced exactly (rebuild hash, infoset m = 19 all 0 and m = 18 5445/2942/1559, both witnesses, subset test
  W = 14 all 0 and W = 15 3362/3252/3332, bz64 d = 15); its 9946 supports equal both of the author's counts. pass: true.
- novelty.md (written 21:28:01Z): one honest GET at 2026-10-24T21:14:39Z, HTTP 200, sha256 37bbf731..., cell
  [[33,7,14-23;12]]_3; one-step rules and a full closure over 3888 parsed cells give 14 at (33,7,12), also with every
  code of the 9 open PRs (#363, #403-#405, #643, #645, #646, #651, #710) added (14, a tie via #645's lengthened
  [[29,7,14;11]]); TROPHY_CASE.md nothing; known-knowns one package at n = 14; codetables.de [33,14]_9 15-18 (Ding,
  Niederreiter, Xing Construction X; the qutrit table uses that code type only at hull 2, [[33,12,15;17]]); arXiv
  2024-10 to 2026-10 nothing at this cell (arXiv:2607.02170 read in full: qutrit lengths <= 25); a web search for
  "[[33,7,15;12]]" found nothing. pass: true.
- criterion.md (written 21:37:39Z): every clause with its own code (s = 38, rank(S J S^T) = 24, c = 12, k = 7; dim
  span(S)^perp = 28, dim I = 14 two ways; N closed under w; its own GF(9) and GF(3)-only Brouwer-Zimmermann programs,
  node counts equal to the closed-form totals, minimum 15 with bound 15; 40 weight-15 vectors rebuilt over GF(3), all
  outside span(S)); one GET at 21:29:07Z, byte-identical, cell listed; 14 < 15 <= 23; c >= 1; non-catalytic; table
  rules give at most 14 at (33,7,12). pass: true.

Live re-fetch at the gate: one plain curl GET, User-Agent "V3R1T4S-research-agent (honest single fetch)", no
retries, 2026-10-24T21:38:48Z to 2026-10-24T21:38:49Z (server date: Sat, 24 Oct 2026 21:38:49 GMT), HTTP 200,
628039 bytes, sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c (unchanged since the claim's
19:55:15Z fetch), footer "Last change: 10.07.2025", cell verbatim `[[33,7,14-23;12]]<sub>3</sub>` (title "lengthening
of [[27,7,14;12]] from arXiv:2207.05647"). Saved in data/gate_fetch/. 15 > 14 and 15 <= 23.

Downgrade checks (none triggered): no hedging panelist; no reproduction mismatch (the author's methods A and B, bz64
and the theorem-based goppa_x.py, the self-break's checker and Construction X bound, REPRODUCE's bz3.c and
CRITERION's bz.c and bz3.c all give d = 15, and three independent counts give 9946 weight-15 supports); 15 strictly
above the live d_lower 14; no stretched criterion or hidden quantifier; scope no wider than reproduced; no sample
presented as complete (every enumeration is exhaustive, with its count checked against the formula); no capped
search used as an exclusion; no probable prime; the table read only by honest single GETs. One object, one cell.
NOVELTY's 301 redirects on arXiv API http requests (each followed by one request to the https target, HTTP 200) are
not retries after a block.

Caveats carried into the package and report, not downgrades:
- The classical [33,14,15]_9 code type is codetables.de's (Ding, Niederreiter, Xing 2000; listed since 2003).
  Wording: "improves the table cell" with a hull-7 version of it, not "new technique".
- Literature: mostly abstracts read; four journal-only papers (IEEE TIT 2025, AMC 2025, IJTP 2024, QIP 2026) judged
  from abstracts and from the codes arXiv:2607.02170 cites from them; issues and branches not searched.
- NOVELTY's closure lets teleportation cells feed only lengthening and puncturing (a modelling choice it states);
  without quantum shortening the closure gives the same 14.
- Optimality not claimed (d_upper 23).
- Process: the REPRODUCE skeptic ran with a 1-process cap until the main session raised it to 2 at 20:58:34Z
  (panel/main_session_notes.txt); it stopped only its own driver shell. No verdict depends on it.
Not part of this claim: propagated cells ((34..36,7,12) by lengthening; (33,8,13), (33,9,14), (33,10,15), (33,11,16)
by increasing dimension), folder 2026-10-24-2001's claim [[33,9,14;12]]_3 (its own panel), and the optimizer lens's
new lead [[33,3,20;18]]_3 (a live lead for a later run).
