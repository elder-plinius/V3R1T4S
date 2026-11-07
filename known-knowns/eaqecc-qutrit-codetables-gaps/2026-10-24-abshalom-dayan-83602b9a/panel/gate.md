# Honesty gate (main session), run 2026-10-24-1033

status: CONFIRMED_SOLUTION
confirmed_scope: claim/object/eaqecc_28_5_15_11.json (sha256 83602b9ae21bd9ab3d1872f4bb244f452a689cb88254e0cc398a75df2e9fd434) holds a 34 x 56 GF(3) symplectic matrix S with n = 28, s = rank(S) = 34, c = rank(S J S^T)/2 = 11 >= 1 and k = n - s + c = 5 (recomputed by me), whose minimum symplectic weight over span(S)^perp minus span(S) ∩ span(S)^perp is at least 15 (I derived d >= 15 from the Hermitian one-point code structure, verified G9 against it, and tested the zero-count bound exhaustively for top pole order <= 10; d is exactly 15 per the author's checkers, which I read but did not rerun), which is strictly greater than d_lower = 13 and at most d_upper = 22 in the listed cell [[28,5,13-22;11]]_3 of claim/table/qutrit.php (sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c, server date 2026-10-24T10:36:29Z), with no neighbouring cell or legend rule on that saved page giving d_lower >= 15 for (28,5,11); a fresh live re-fetch at the moment of claiming is still owed by the claimer and was not done by me.

Claim: [[28,5,15;11]]_3 at the listed cell (n,k,c) = (28,5,11) of https://eaqecc.codetables.de/qutrit.php, object
claim/object/eaqecc_28_5_15_11.json (sha256 83602b9ae21bd9ab3d1872f4bb244f452a689cb88254e0cc398a75df2e9fd434).

Panel files read in full by the main session:
- reproduce.md (fresh subagent, claude-opus-5-5): own checker written from the definition and tested (39 brute-force
  cases, altered copies rejected); complete enumeration of all 3^22 vectors of span(S)^perp gives d = 15 (71280
  words outside the isotropic part, none lighter); author's rebuild byte-identical; author's checkers A and B rerun
  and agree. pass: true.
- novelty.md (fresh subagent, claude-opus-5-5): one honest GET at 2026-10-24T11:13:23Z, HTTP 200, same page sha256,
  cell 13-22; literature (table source arXiv:2207.05647, Christensen-Munuera-Pereira-Ruano arXiv:2105.02166,
  arXiv:2607.02170 and others), TROPHY_CASE.md and all open PRs: nothing reaches d >= 15 at (28,5,11). Published
  length-27 codes imply d = 14 there through the table's rules, so the margin over everything known is +1 (15 vs 14),
  over the table +2. pass: true.
- criterion.md (fresh subagent, claude-sonnet-5-5): condition by condition against the criterion verbatim; own
  recomputation of s = 34, c = 11, k = 5; cell listed (not implied), single cell, c >= 1, k >= 1, strict, d <= d_upper.
  It notes that the final live re-fetch was owed by the claimer. pass: true.

Live re-fetch at the gate (owed per criterion.md): one plain curl GET, User-Agent "V3R1T4S-research-agent (honest
single fetch)", no retries, 2026-10-24T11:35:08Z to 11:35:09Z (server date Sat, 24 Oct 2026 11:35:08 GMT), HTTP 200,
628039 bytes, sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c (unchanged), cell verbatim
`[[28,5,13-22;11]]<sub>3</sub>` (title "lengthening of [[27,5,13;11]] subcode of [[27,8,13;11]] from arXiv:2207.05647"),
footer "Last change: 10.07.2025". Saved in data/gate_fetch/.

Downgrade checks (none triggered): no hedging panelist (criterion.md states what d rests on; reproduce.md reran the
full enumeration); no reproduction mismatch; 15 strictly above the live d_lower 13 and above the literature-implied
14; the criterion is met literally, no hidden quantifier found; scope no wider than reproduced; no sample presented as
complete (3^22 enumerated in full); no capped search used as an exclusion; no probable prime; table read by honest
single GETs only (no browser UA, cookies or retries); one object, one cell.
Not part of this claim: the run's other candidates (dossier) and any propagated cells.
