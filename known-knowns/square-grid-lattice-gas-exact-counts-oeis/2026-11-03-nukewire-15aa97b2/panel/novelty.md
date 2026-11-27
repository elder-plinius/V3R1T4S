# NOVELTY skeptic verdict — A210662 row 28 (T(28,k), k=1..27)

Run: 2026-11-03-0830 · target: square-grid-lattice-gas-exact-counts-oeis (partial win p2)
Object: the 27 integers in claim/object/row28_final.json, claimed to be row 28 of OEIS A210662
(triangle of monomer-dimer tilings of n X k boards = matchings of P_n x P_k), extending the
published rows 1..27.

## 1. Status fetch (one honest attempt, succeeded)

- URL: https://oeis.org/A210662/b210662.txt
- Client: `curl -sS -A "V3R1T4S-panel/1.0"` (single attempt, no retries)
- Result line: `HTTP_CODE=200 SIZE=22774 TIME=0.106537s FETCHED_AT=https://oeis.org/A210662/b210662.txt`
- UTC time: 2026-11-03T08:38:42Z
- sha256: 05d85498be37eb57e7c52bb4119f70296891026c270432c8502ccf79dd9ddf7d
  (byte-identical to the claim's archived copy claim/data/b210662.txt)
- Terms: 378 lines, indices 1..378, i.e. triangle rows 1..27 (27*28/2 = 378). Row 28 would be
  indices 379..405: ABSENT, as claimed.
- Membership check (my own code on my fetched copy): none of the 27 claimed integers appears
  anywhere in the 378 published terms (`claimed values already present in published b-file: NONE`).

## 2. Repo sweep (V3R1T4S pinned read-only copy, commit f3b19b4, 2026-10-30)

- `grep -rn "A210662"` over TROPHY_CASE.md, README.md, READ_BEFORE_CITING.md, bank/, known-knowns/,
  known-unknowns/, news/: hits only the p2 criterion definition (bank/targets.json line 10984,
  quoted verbatim in CLAIM.md — verified word-for-word) and the known-unknowns problem page.
- TROPHY_CASE.md: zero occurrences of A210662, A028420, A054759, A089980, "monomer".
- known-knowns/ for this target: the merged 2026-10-17 result is A054759(15) (Eulerian
  orientations of the 15x15 torus — partial p1, a different sequence; no A210662 cells).
- news/, llms.txt: no mentions.

## 3. Pull-request sweep (gh, state all)

- `gh pr list --repo elder-plinius/V3R1T4S --state all --search "210662"` — 0 results: no open or
  closed PR mentions A210662 anywhere in title or body.
- `--search "monomer-dimer"` and `--search "A028420"` surface, among unrelated targets:
  - **PR #849** (DRAFT, ours): "square-grid-lattice-gas-exact-counts-oeis: A028420 a(28) =
    503599...75471 (222 digits, full criterion)" — the DIAGONAL cell T(28,28). Its body cites
    `a28_value.txt (sha256 883cfca9...)`; the claim's anchor file claim/data/a28_value.txt hashes
    to sha256 prefix 883cfca970395b0b — same object. The claim explicitly excludes k=28 and uses
    this only as CRT anchor/cross-check: complementary cell, not a tie.
  - PR #462 (OPEN, CONFIRMED_PARTIAL): A089980 antidiagonal d=79 — hard squares, the OTHER branch
    of p2; different table, no overlap with A210662 row 28.
  - PRs #832/#782/#366: A054759 independent-set counts; PRs #843/#537/#536: cubic dimer bounds;
    #818/#488/#487: entropy-constant digits. None touches A210662 cells.
- Conclusion: no PR, merged or open, publishes or claims any off-diagonal cell of row 28.

## 4. Neighbouring cells and the OEIS propagation channels

The A210662 entry itself (fetched once, internal format, HTTP 200, 2026-11-03T08:43:06Z,
URL https://oeis.org/search?q=id:A210662&fmt=text) documents the only public propagation rules:

- Symmetry T(n,k)=T(k,n): every published term has both indices <= 27, so restriction/relabel/
  symmetry of the published triangle stays inside rows 1..27 and cannot produce an index-28 cell.
- "Right hand diagonal is A028420" (k=n): published through n=27; a(28) is our own draft PR #849,
  unpublished and excluded from this claim.
- "Left hand diagonal is A000045" (k=1, Fibonacci) and "columns 1-7 match A000045(n+1), A030186,
  A033506(n-1), A033507(n-1), A033508(n-1), A033509(n-1), A033510(n-1)".
  - Column 1: T(28,1) = F(29) = 514229 is trivially known (Fibonacci). Disclosure: 1 of the 27
    cells is a published quantity via this documented propagation; it gives nothing further.
  - Columns 2..7: I fetched each sequence's b-file once (`https://oeis.org/A030186/b030186.txt`
    etc., UA V3R1T4S-panel/1.0, 2026-11-03T08:44:03Z): all six returned HTTP 404 (no b-file
    exists; a 143-line error page). I then fetched each entry once in internal text format
    (2026-11-03T08:44:16Z, HTTP 200) and counted the published DATA terms:
    A030186 (col 2): 28 terms, max n=27 (last 32655756991442); A033506 (col 3): max n=20;
    A033507 (col 4): max n=19; A033508 (col 5): max n=15; A033509 (col 6): max n=14;
    A033510 (col 7): max n=15. None reaches n=28, and none of the claimed T(28,2)..T(28,7)
    values appears in any of them. Columns 8..27 have no separate published sequences.
- There is no published row-to-row recurrence that turns row 27 into row 28 (each new width needs
  a fresh transfer computation); no local numerical polish of a 200+-digit published integer
  yields a neighbour cell.

## 5. Web sweep (last 24 months; exact integers and terms)

- Exact 214-digit T(28,27) = 5157066570165070567729489132695776810440342246744652257306934345615680
  488835864787743067750009969185890689005251257229646554654400380259718864552194014646931029
  555623884848420463651868096212298160284685217585130061 — quoted in full in the query;
  0 matches ("No direct matches found ... likely doesn't appear in any indexed public web page").
- Exact 80-digit T(28,14) = 7023074485444863025086472133714490577307305108832133853059242799565
  8767217862722056616543242680996392077612869 — 0 matches.
- "A210662 row 28" — 0 matches (no indexed OEIS-row-28 discussion).
- "514229" + "A210662"/"monomer-dimer" board 28 — no page connects F(29) to a 28-cell of A210662;
  the A210662 entry page itself is the only A210662 hit.
- monomer-dimer exact enumeration 2024-2026 sweep: closest items are method papers/computations
  (Kong 2024 arXiv:2405.09457 recurrence solution; Oh 2019 arXiv:1901.07847 state-matrix
  recursion; Grad/Klavzar et al. 2026 matching-vector transfer matrices; Sinclair's grids.pdf
  approximation algorithms; Klarner-Pollack domino tables). None publishes an m=28 row of the
  monomer-dimer rectangle table, and no code repository or release asset with these integers
  surfaced (total: 6 web searches, 3 exact-integer/term queries all returning zero relevant hits).

## 6. Trivial-edit test

Deletion, restriction, relabelling, symmetry of the published 378-term triangle: all stay inside
indices <= 27. The documented propagation rules (column sequences, Fibonacci diagonal) reach n=28
only for k=1. A local numerical polish of published neighbours cannot produce the 26 unpublished
integers (14..214 digits). The row as an object (m=28, all n=1..27 = the published range) is not
obtainable from any combination of trivial edits of published objects, and no seeding source for
these integers is published anywhere found. The one Fibonacci cell is disclosed above and does
not affect the row-level claim (bank p2: "extending the largest published m by one for all n up
to the published range" — largest published m is 27, confirmed by my own fetch).

## Verdict

The status fetch succeeded on the first honest attempt (HTTP 200, sha256 recorded, 378 terms,
row 28 absent). The published table, all documented column/diagonal channels, this repo
(trophy case, known-knowns, all PRs open and closed), and the indexed web/literature of the last
24 months contain none of the 26 non-trivial cells of row 28 and no object from which trivial
edits yield them. The diagonal T(28,28) belongs to our own draft PR #849 and is explicitly
excluded. The row strictly extends everything published; no tie found.

context: subagent
pass: true
