# Honesty gate (main session), run 2026-10-24-2001

status: CONFIRMED_SOLUTION
confirmed_scope: The 36 x 66 GF(3) stabilizer matrix S in claim/object/eaqecc_33_9_14_12.json (sha256 059282c383e7d059867ecd1a1ec51d54197af25b2c6a320dd26b150ac1a99391) defines a non-catalytic qutrit EAQECC with s = 36, c = 12, k = 9 and exact minimum distance d = 14 (minimum symplectic weight on span(S)^perp outside span(S) ∩ span(S)^perp), which is strictly greater than d_lower = 13 and at most d_upper = 21 for the listed cell [[33,9,13-21;12]]_3 of https://eaqecc.codetables.de/qutrit.php as fetched at 2026-10-24T22:29:54Z (HTTP 200, sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c).

Claim: [[33,9,14;12]]_3 at the listed cell (n,k,c) = (33,9,12) of https://eaqecc.codetables.de/qutrit.php, object
claim/object/eaqecc_33_9_14_12.json (sha256 059282c383e7d059867ecd1a1ec51d54197af25b2c6a320dd26b150ac1a99391), a
Construction X code over GF(9) from the Hermitian-curve AG codes C(D_28, 3Q + 8P_inf) > C(D_28, 2Q + 8P_inf) (Q a
place of degree 3) with a [5,3,3] tail and a column sign pattern: [33,15,14]_9 with Hermitian hull 6.

Claim folder unchanged since the panel started: every file's sha256 equals panel/claim.sha256 (15 of 15 files OK,
checked at the gate). Self-break (self_break/verdict.md, main session, in a copy of claim/): SURVIVES.

Panel files read in full by the main session (each skeptic a fresh subagent, claude-opus-5-5, given only its own
copy of claim/, run one after another, never in parallel, and never alongside folder 2026-10-24-1953's skeptics;
times are the verdict files' write times, UTC):
- reproduce.md (written 22:06:57Z): own exhaustive GF(3) position-subset checker (mine/subsets.c, pruned subtrees
  credited by binomial counts, total checked against C(n,w)) written before reading the author's code: w = 13 covers
  573166440 of 573166440 subsets with 0 vectors outside the isotropic part, w = 14 finds 10404 subsets, a weight-14
  witness outside span(S): d = 14; 120 brute-force cases (n = 3..9) and 40 mid-size numpy cases (n = 10..16, 28 of
  them with lighter isotropic vectors) with 0 mismatches; two seeded negatives caught; a permuted run and
  byte-identical reruns; the author's steps 1-5 reproduced exactly (rebuild hash, infoset m = 20 all 0 and m = 19
  5931/3016/1457, both witnesses, subset test W = 13 all 0 and W = 14 3469/3448/3487, bz64 d = 14). pass: true.
- novelty.md (written 22:26:55Z): one honest GET at 2026-10-24T22:08:42Z, HTTP 200, sha256 37bbf731..., cell
  [[33,9,13-21;12]]_3; closure of all 3888 entries under the six rules (side conditions dropped, so an over-estimate)
  gives 13, also with codetables.de's qutrit stabilizer codes for n = 33..46, arXiv:2607.02170's qutrit codes and all
  69 parameter sets of the 9 open target PRs (#363, #403-#405, #643, #645, #646, #651, #710) added; TROPHY_CASE.md
  nothing; known-knowns one package at n = 14; codetables.de [33,15]_9 14-17 (Ding-Niederreiter-Xing, 2003-10-23;
  the qutrit table's diagonal for it starts at hull 2, [[33,13,14;16]]); literature 2024-10 to 2026-10 nothing at
  this cell. pass: true.
- criterion.md (written 22:40:47Z): every clause with its own code (s = 36, rank(S J S^T) = 24, c = 12, k = 9; dim
  N = 30, dim I = 12; N invariant under w; its own Brouwer-Zimmermann over GF(9), lower 14 = upper 14; an exact count
  of all words of weight <= 14, 0 below 14 and 10404 weight-14 words on 10404 supports; all 3^12 vectors of I
  enumerated, minimum weight 18, so every weight-14 vector is outside I; witnesses checked against S); one GET at
  22:29:54Z, byte-identical, cell listed; 13 < 14 <= 21; c >= 1; non-catalytic; the one-step rules give 13. pass: true.
  Its confirmed_scope first carried a garbled object hash; the skeptic corrected the sentence itself before handing
  back (file time 22:40:47Z); the hash above is the object's real sha256.

Live re-fetch at the gate: one plain curl GET, User-Agent "V3R1T4S-research-agent (honest single fetch)", no
retries, 2026-10-24T22:41:24Z to 2026-10-24T22:41:25Z (server date: Sat, 24 Oct 2026 22:41:24 GMT), HTTP 200,
628039 bytes, sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c (unchanged since the claim's
19:55:15Z fetch), footer "Last change: 10.07.2025", cell verbatim `[[33,9,13-21;12]]<sub>3</sub>` (title "lengthening
of [[27,9,13;12]] increasing dimension of [[27,8,13;11]] from arXiv:2207.05647"). Saved in data/gate_fetch/. 14 > 13
and 14 <= 21.

Downgrade checks (none triggered): no hedging panelist; no reproduction mismatch (the author's methods A and B, bz64
and the theorem-based goppa_x.py, the self-break's checker and Construction X bound, REPRODUCE's subsets.c and
CRITERION's bz9.c and count14.c all give d = 14, and four independent counts give 10404 weight-14 supports); 14
strictly above the live d_lower 13; no stretched criterion or hidden quantifier; scope no wider than reproduced; no
sample presented as complete (every enumeration is exhaustive, with its count checked); no capped search used as an
exclusion; no probable prime; the table read only by honest single GETs. One object, one cell. Not subsumed by this
weekend's other confirmed code either: the already-settled lens's closure (attempts/already-settled/out/settled.txt)
included [[33,7,15;12]]_3 and still gives 13 at (33,9,12).

Caveats carried into the package and report, not downgrades:
- The classical [33,15,14]_9 code is codetables.de's (Ding, Niederreiter, Xing 2000; listed since 2003). Wording:
  "improves the table cell" with a hull-6 version of it, not "new technique".
- The object's construction string says the gluing matrix fills "rows 11..13 of the tail"; the rows are 12..14
  (erratum stated in claim/CLAIM.md; G9, D9 and S, which every skeptic checked, are unaffected).
- Literature: mostly abstracts read; three paywalled journal papers judged from the codes arXiv:2607.02170 cites
  from them; CRITERION checked subsumption only against the live table (NOVELTY covered the rest).
- Optimality not claimed (d_upper 21). The same row lists [[33,9,14-21;13]]_3, so the gain is one entangled pair
  saved at d = 14.
Not part of this claim: cells that follow by the table's rules, folder 2026-10-24-1953's claim [[33,7,15;12]]_3
(its own panel and package), and that folder's new lead [[33,3,20;18]]_3.
