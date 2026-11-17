# Novelty skeptic: anomaly-free-atlas-qmax (run 2026-11-03-0919)

Scope: I read only CLAIM.md, status.md, object/, source/atlas/ (and listed the claim folder's other file names), plus the
kit repository checkout's TROPHY_CASE.md and known-knowns/. Working files are in ../panel_work/novelty/ (paths below
are relative to claim/).

## 1. Status source, fetched once (no retries)

- URL: https://arxiv.org/abs/1812.04602 (the arXiv record named in status.md)
- Time (UTC, `date -u` before and after): 2026-11-04T09:21:08Z
- Client: curl, User-Agent "V3R1T4S-research-bot"
- HTTP status: 200 (final URL https://arxiv.org/abs/1812.04602, no redirect)
- Saved bytes: ../panel_work/novelty/fetch/arxiv_1812.04602_abs.html, 46974 bytes,
  sha256 3cce96fa1ab6826f9e8f0879fda2f474d2ca7d075e8466e8016be33863f23b93
  (byte-identical to the scout's 2026-11-03 fetch recorded in status.md and to source/atlas/arxiv_1812.04602_abs.html).
- Value read: title "An Anomaly-free Atlas: charting the space of flavour-dependent gauged U(1) extensions of the
  Standard Model"; DOI 10.1007/JHEP02(2019)082; submission history v1 (2018-12-11) ... v5 (Wed, 8 Jan 2020 19:00:19 UTC);
  no v6. The abstract page itself states no Q_max; the published range is stated in the v5 text
  (source/atlas/arXiv-1812.04602v5.txt, section 4.2): lists on Zenodo "for Qmax <= 10 in the SM and Qmax <= 10 in the
  SMnuR". So the published range is Q_max 1..10 for both contents.
- Release assets (the paper's data release, checked because a release can be ahead of the text): Zenodo API
  https://zenodo.org/api/records/3345889, 2026-11-04T09:21:29Z, HTTP 200 (../panel_work/novelty/lit/zenodo_3345889.json):
  version 1.1.0, the only/last version of concept record 1478084; files SMcharges0..SMcharges10 and
  SMnuRcharges0..SMnuRcharges10(.bz2) plus searchU1.cpp/runme.sh. Largest Q_max released: 10 (both contents).

## 2. Searches

arXiv API (export.arxiv.org/api/query, sorted by submission date, max 100 per query; log with UTC times and HTTP
codes in ../panel_work/novelty/lit/queries.log, all HTTP 200), 2026-11-04T09:21:46Z..09:27Z, 16 queries, e.g.:
abs:"anomaly-free" AND abs:"U(1)" AND abs:charges (175 hits; the 100 returned reach back to 2017-11, so the whole
24-month window is covered); "anomaly-free atlas"; "anomaly cancellation" AND "U(1)" AND "charge assignments";
"anomaly-free" AND "charge assignments" AND "right-handed neutrinos"; flavour-/flavor-dependent U(1) anomaly;
anomaly AND Diophantine; "gauge anomaly equations"; "anomaly-free" AND Qmax / "maximum charge"; anomaly U(1) with
machine/reinforcement learning; "anomaly-free" AND solutions AND integer; au:Rathsman AND anomaly.
45 distinct hits dated 2024-11-01 or later (../panel_work/novelty/lit/parsed_all.txt). Closest ones read:
- 2508.11583 (Gripaios, Nguyen, 2025): arithmetic-geometry parametrisation of solutions for one u(1) factor; no
  bounded-charge census or counts.
- 2610.26092 (Gripaios, 2026-10): degree-3 Prouhet-Tarry-Escott / millicharged fermions; different equations.
- 2606.07735 (Tsai, Lee, Takahashi, 2026): asymptotics of symmetric PTE solutions; different problem.
- 2603.27157 (2026): classifies a family of flavour-specific chiral U(1)_X assignments with benchmarks; no census.
- Others in window are phenomenology (Z', B-L, L_mu-L_tau, dark photons) with no counts.
Older neighbours (outside the window, for completeness): 1812.04602 itself (Q_max <= 10); 2107.07926 SUSY atlas
(MSSM + up to 3 singlets, a different field content, Q_max <= 10); 2006.03588 and 2111.04148 (general/rational
solutions, no bounded counts); 2206.09956 (Ising-machine search, not a complete census); 1902.08529 (Froggatt-Nielsen
models). None tabulates SM or SMnuR counts beyond Q_max = 10.
Limitation: the arXiv API searches title/abstract metadata, not full text.

Zenodo search API (../panel_work/novelty/lit/zenodo_search.txt, 2026-11-04T09:25:52Z..09:26:04Z): title:"anomaly-free"
gives 10 records; the only census datasets are 3345889 (this atlas, Q_max <= 10) and 5062067 (SUSY atlas). Free-text
queries sorted by date returned only unrelated records.

GitHub (authenticated REST search via gh api, 2026-11-04T09:24:28Z..09:25Z; ../panel_work/novelty/gh/code_search.txt):
repository search "anomaly-free U(1) charges", "anomaly free atlas", "searchU1" gave 0; "anomaly cancellation" gave 21
repositories, the only relevant one being jstoobysmith/Anomaly_Cancellation_in_Lean (Lean formalisation, last push
2024-04). Code search "SMnuRcharges" gave 0; "SMcharges" hits are Lean formalisations (physlib, aftd-platform) and
unrelated code; "anomaly free U(1) Qmax" and "anomaly free charges Qmax" hits are unrelated. No repository or
release publishing SM/SMnuR counts or lists past Q_max = 10 was found.

This repo (kit checkout, remote https://github.com/elder-plinius/V3R1T4S, HEAD cf68067):
- TROPHY_CASE.md (100 lines) and known-knowns/ (29 target folders): no match for anomaly-free, atlas,
  Allanach, Davighi, 1812.04602 or any anomaly-free U(1) census. No entry for this target or its neighbours.
- Pull requests: listing PRs by API (titles, open/closed state) was NOT possible. gh GraphQL, gh REST and the GitHub
  MCP tool all returned 403 / not configured for this session, and I did not attach the repo. What I could check:
  `git ls-remote` gave 908 refs/pull/N/head (N = 1..943, which covers open, closed and merged PRs) at
  2026-11-04T09:23:58Z. I fetched all 908 heads with commits and trees but no blobs into
  ../panel_work/novelty/gh/prmirror and searched every commit message and every file path in every PR head tree
  (24907 distinct paths). There was no match for anomal(y)-free census terms (anomal, atlas, allanach, U(1), qmax,
  charge assign); the only path hits were unrelated (hsp6_anomaly fixtures, lunar/proteinbench "atlas", etc.).
  Not checked: PR titles and bodies, PR comments, and file contents (blobs) of PRs.

## 3. Comparison

Cells claimed: SMnuR Q_max = 20 (6465226975); SM Q_max = 36, 37, 38 (32457211, 37347334, 42898799), in the atlas
convention (1 + nonzero gcd-1 solutions modulo family permutations within species and overall sign). The
convention's agreement with all 40 published values for Q_max 1..10 is recorded in source/atlas/table_comparison.txt.
- Best published value for these cells: none. The largest published Q_max is 10 for both contents (paper v5 text,
  arXiv record unchanged since v5, Zenodo release 1.1.0). Nothing published in the last 24 months, or earlier, that I
  could find reaches Q_max 11 for either content. That includes the 2026 Gripaios and PTE papers, which solve
  different equations or parametrise solutions without counting them.
- Neighbouring cells: SMnuR 11..19 and SM 11..35 are this workspace's own earlier rows (CLAIM.md Context). They are
  not independent prior art. I did not find them published in the kit repo (TROPHY_CASE, known-knowns, PR heads) or
  elsewhere. The new rows are beyond them in any case (20 > 19; 36..38 > 35).
- Trivial edits of published objects: restricting or deleting from the Q_max <= 10 lists gives only rows with
  Q_max <= 10. Relabelling, permutation and sign are quotiented out by the convention. Dropping nu (F_nu = 0) maps
  SMnuR rows to SM rows at the same Q_max <= 10. Integer rescaling of a Q_max-10 solution gives non-primitive
  assignments, which the gcd-1 convention excludes, and it could not give a complete list in any case. Sums of
  solutions are not solutions (the quadratic and cubic ACCs). The published rational parametrisations (method of
  chords, 2006.03588 and 2508.11583) generate solutions but do not certify a complete bounded census. So no
  combination of these edits produces an exact count, let alone a complete list, at Q_max 20 (SMnuR) or 36..38 (SM).
  CLAIM.md says the lists are regenerated by the claimant's own enumerators (source/csenum2.c, source/acclist.c), not
  seeded from a published list. (I did not audit correctness; that is the other skeptics' job.)
- Tie check: there is no published value at these cells to tie with, and every claimed row lies strictly past the
  largest published Q_max for its content.

Verdict: on novelty, each of the four rows extends the census strictly beyond everything published or released that I
could find (published maximum Q_max = 10 for both contents). Residual gap: PR titles, bodies and blob contents were
not readable through the API; PR head commit messages and file paths were checked.

context: subagent (fresh context, Claude Code Agent tool)
pass: true
