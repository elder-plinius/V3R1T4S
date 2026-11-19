# Honesty gate (main session), run folder 2026-10-24-2311 [not included]

[Note added when packaging: notes in square brackets were added then; nothing else in this file was changed. It was
written in the contributor's workspace, where claim/ is this package's root, so claim/object/eaqecc_28_7_13_9.json is
object/eaqecc_28_7_13_9.json here (same sha256) and CLAIM.md is README.md. Paths and run or folder ids marked [not included] name files and folders of
that workspace that are not included in this package.]

status: CONFIRMED_SOLUTION
confirmed_scope: The 30 x 56 GF(3) stabilizer matrix S in claim/object/eaqecc_28_7_13_9.json (sha256 64c0cbddea11688f7cc06644d8751c2f62328aae74f7f149b89164a73dea0c78) has s = 30 independent rows, rank(S J S^T) = 18 (c = 9) and k = 7, and the minimum symplectic weight of span(S)^perp outside span(S) ∩ span(S)^perp is exactly 13, which is strictly above d_lower = 12 and within d_upper = 18 of the cell [[28,7,12-18;9]]_3 on https://eaqecc.codetables.de/qutrit.php as fetched at 2026-10-25T00:41:55Z (HTTP 200, sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c).

Claim: [[28,7,13;9]]_3 at the listed cell (n,k,c) = (28,7,9) of https://eaqecc.codetables.de/qutrit.php, object
claim/object/eaqecc_28_7_13_9.json (sha256 64c0cbddea11688f7cc06644d8751c2f62328aae74f7f149b89164a73dea0c78), the
natural extended one-point Hermitian code E_15 over GF(9) ([28,13,13]_9, Hermitian hull 6, no column scaled), run
1033's panel-ready candidate 4 [run 1033 not included], rebuilt byte for byte from PREREG.md's parameters
[how-we-built-it/PREREG.md here].

Claim folder unchanged since the panel started: every file's sha256 equals panel/claim.sha256 [not included] (17 of 17 files OK,
checked at the gate). Self-break (self_break/verdict.md [not included], main session, in a copy of claim/): SURVIVES.

Panel files read in full by the main session (each skeptic a fresh subagent, claude-opus-5-5, given only its own
copy of claim/, run one after another, never in parallel; started 00:12:11Z, 00:24:22Z, 00:41:08Z; verdict files
written 00:23:41Z, 00:40:32Z, 00:49:19Z UTC by file time):
- reproduce.md: own checker from S alone (mine/ea_prep.py, mine/ea_subset.c [both not included], written before reading the author's
  code): s = 30, rank(S J S^T) = 18, c = 9, k = 7, dim N = 26, dim I = 12; exhaustive position-subset test, pruned and
  unpruned: W = 12 none of 30421755, W = 13 9036 of 37442160 (identical lists, same hash on rerun); 55 weight-13
  witnesses outside span(S); 135 brute-force cases with 0 failures; a planted weight-12 vector caught; the author's
  steps 1-6 reproduced exactly (rebuild hash, method A m = 16 all 0 and m = 15 5376/2541/1119, both witnesses, method B
  W = 12 all 0 and W = 13 2989/3104/2943, bz64 d = 13, onepoint_check RESULT True); method A's 9036 deficient
  15-subsets are exactly the complements of its 9036 bad 13-subsets; step-6 proof re-derived. pass: true.
- novelty.md: one honest GET at 2026-10-25T00:25:05Z, HTTP 200, sha256 37bbf731..., byte-identical to the claim's
  copy, cell [[28,7,12-18;9]]_3; own closure of all 3888 cells under the page's rules gives 12, also with all 47 codes
  of the repo's PR bodies, the workspace's unfiled codes, the whole length-27 one-point family of arXiv:2105.02166 (its
  hulls recomputed; the relevant members' EA distances pinned by explicit words) and arXiv:2607.02170's qutrit codes;
  teleportation seeding breaks 2700 d_upper values; TROPHY_CASE.md nothing; known-knowns one entry at n = 14; 9 open
  PRs (matching CLAIM.md); codetables.de [28,13]_9 13-14 (Hermitian AG, 2003). pass: true.
- criterion.md: every clause with its own code (mine/params.py; mine/dfs9.c [both not included], an exhaustive dependency search over the
  GF(9) parity-check matrix it derived: 76717268 nodes = the number of column subsets of size <= 12, all independent;
  9036 dependent 13-sets = 72288 weight-13 vectors, every one tested against S: orthogonal, outside span(S)); controls
  (40 random codes vs brute force; a planted 12-dependency found); the author's tools agree; one GET at
  2026-10-25T00:41:55Z, byte-identical, cell listed; 12 < 13 <= 18; c >= 1; non-catalytic; one-step sources give 12.
  pass: true.

Live re-fetch at the gate: one plain curl GET, User-Agent "V3R1T4S-research-agent (honest single fetch)", no
retries, 2026-10-25T00:49:54Z to 2026-10-25T00:49:54Z (server date: Sun, 25 Oct 2026 00:49:54 GMT), HTTP 200,
628039 bytes, sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c (byte-identical to the claim's
22:58:17Z copy), footer "Last change: 10.07.2025", cell verbatim `[[28,7,12-18;9]]<sub>3</sub>` (title "subcode of
[[28,9,12;9]] from arXiv:2207.05647"). Saved in data/gate_fetch/ [not included]. 13 > 12 and 13 <= 18.

Downgrade checks (none triggered): no hedging panelist; no reproduction mismatch (the author's methods A and B, bz64
and onepoint_check.py, the self-break's fresh numpy checker, run 1033's full 3^26 enumeration [run 1033 not included] (72288 weight-13 words), the REPRODUCE
skeptic's own subset test and the CRITERION skeptic's own GF(9) search all give d = 13, with 9036 weight-13 supports
in five independent counts); 13 strictly above the live d_lower 12; no stretched criterion or hidden quantifier;
scope no wider than reproduced; no sample presented as complete; no capped search used as an exclusion; no probable
prime; the table read only by honest single GETs. One object, one cell. Not subsumed by this workspace's other
codes: the already-settled lens's closure (attempts/already-settled/out/settled.txt [not included]) includes every package, every
lead and folder 2256's claim [folder 2256 not included], and gives 12 at (28,7,9).

Caveats carried into the package and report, not downgrades:
- The classical [28,13,13]_9 code is codetables.de's (an AG code on the Hermitian curve, listed since 2003); the
  table uses it at Hermitian hull 3 ([[28,10,13;12]]_3). What is new is the qutrit EA code from its hull of dimension 6.
  Wording: "improves the table cell", not "new technique".
- The same row lists [[28,7,13-19;11]]_3, so the gain is two entangled pairs saved at d = 13. Optimality not claimed
  (d_upper 18).
- Literature: the NOVELTY skeptic could not read arXiv:2207.05647 as HTML (HTTP 404, no other route tried; its codes
  are on the table) and judged journal-only papers (Cao-Li-Zhu IEEE TIT 2025, Li-Li-Guan-Song IJTP 2024, Li-Zhu DM
  2024, Liu-Li-Shi AMC 2025) from the codes arXiv:2607.02170 cites from them.
Not part of this claim: cells that follow by the table's rules (for example (29,7,9) and (30,7,9) by lengthening).
