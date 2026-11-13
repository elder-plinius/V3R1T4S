# NOVELTY panel, round 3 — A210662 row 29, cells T(29,k) for k = 12..28

context: subagent

Panelist: fresh context (NOVELTY round 3). Saw only the claim folder
`claim (the panelist's claim folder)`. Claim under test: the 17
integers T(29,k), k = 12..28, of OEIS A210662 (monomer-dimer tilings of the
k X 29 grid), with k = 1..11 disclosed as published/mechanical and T(29,29)
explicitly NOT claimed. Every check below was one honest GET (or one gh call)
per source; no retries; nothing blocked.

Search integers used (from claim/row29.json):
- k=13: 3378922357612323289114824435533312531621430407758060865372531834132232659148852944418174223104301366489418
- k=28: 49177697804872297016727302711594119377773797320206651255894936912413256592078514557334089110305782773937427290128372702681357081476749909395993637862320007857944179229707528967905923212378186197399082422807195828650578570227530259

## 1. Live status source: the b-file

- URL: https://oeis.org/A210662/b210662.txt
- fetch_time_utc: 2026-11-08T21:10:19Z; http_status: 200; size_bytes: 22774
- sha256: 05d85498be37eb57e7c52bb4119f70296891026c270432c8502ccf79dd9ddf7d
- 378 data lines, flat triangle indices 1..378 = rows 1..27 of the table
  (1+2+...+27 = 378). max_index: 378.
- last term (index 378, i.e. T(27,27)):
  102463679128226917026803992291271780699070022553141981032613488312506661561549950007523199427527023711046393977692208269034259697189730276411550008064022485759903700230738620478821625628626370413757043480347
- Rows 28 and 29 ABSENT: the only lines matching "^28 " / "^29 " are flat
  indices 28 ("28 11945257052321") and 29 ("29 34") — interior terms of rows
  7-8 of the triangle, not table rows 28/29. grep of the full b-file for the
  claimed k=13 and k=28 integers: count 0 each.
- Conclusion: published table stops at row 27. Claim's "b-file rows 1..27" is
  accurate.

## 2. Entry page cross-references, enumerated myself

- URL: https://oeis.org/A210662 ; fetch_time_utc: 2026-11-08T21:10:20Z;
  http_status: 200; size_bytes: 26382.
- FORMULA (verbatim): "T(1,n) = A000045 (n+1), T(2,n) = A030186 (n), T(3,n) =
  A033506 (n), T(4,n) = A033507 (n), T(5,n) = A033508 (n), T(6,n) = A033509
  (n), T(7,n) = A033510 (n), T(8,n) = A033511 (n), T(9,n) = A033512 (n),
  T(10,n) = A033513 (n), T(11,n) = A033514 (n), T(n,n) = A028420 (n)."
  -> functional references cover columns 1..11 and the diagonal ONLY. Nothing
  for columns k >= 12. The entry has NO generating function or recurrence of
  its own (grep for "G.f"/"generating function" on the page: no hits).
- CROSSREFS (verbatim): "Sequence in context: A336854 A209666 A089124 *
  A229610 A117809 A052091 / Adjacent sequences: A210659 A210660 A210661 *
  A210663 A210664 A210665" — these are OEIS mechanical neighbors. Verified by
  their tooltip titles on the same page: A336854 = A336841(n)/2; A209666 =
  monomials in complete homogeneous symmetric polynomials; A089124 = largest
  prime factor of n^2+3; A229610 = prime array; A117809 = floor of algebraic
  powers; A052091 = palindromic prime pyramid; A210659-665 = expression
  depth / de Bruijn graph / triangulations / semiprime sequences. None is a
  monomer-dimer object. (A336841 occurs once, only inside A336854's tooltip.)
- EXTENSIONS: "Typo in term 27 corrected ... Dec 03 2012 / Reviewed by Ralf
  Stephan, May 22 2014" — no row/table extension ever recorded.
- PROG: a SageMath TilingSolver snippet (Ralf Stephan, 2014) — a brute-force
  algorithm, not published values and not a closed form; see section 7.

## 3. Every OEIS sequence referencing A210662 (full text search, paginated)

- URL: https://oeis.org/search?q=%22A210662%22&fmt=text (+ &start=10, + &start=20)
  ; 2026-11-08T21:12:26Z / 21:16:58Z / 21:17:11Z; all http_status 200.
- Complete result set (16 sequences; page 3 clamps to page 2 = end):
  A210662 (the table); A030186 (col 2); A033506..A033514 (cols 3..11 — nine
  sequences, all present); A028420 (diagonal); and four same-graph-different-
  object arrays: A242856 (2-matchings of n X n), A242861 (k dominoes on n X n),
  A286912 (EDGE COVERS of P_m X P_n), A288026 (MAXIMAL matchings of P_m X P_n).
- The only same-shaped candidate, A286912 (fetch: search?q=id:A286912,
  2026-11-08T21:13:11Z, 200), is a different quantity and tiny extent: DATA
  begins 0,1,1,1,7,1,2,43,43,2,... (T(1,1)=0 where A210662 has 1; T(2,3)=43
  where A210662 T(3,2)=22; T(1,n)=Fibonacci), antidiagonals only up to m+n ~ 9.
  A288026 (maximal matchings) likewise counts a different thing. Neither can
  publish T(29,12..28); neither reaches m or n = 29.
- -> No sequence anywhere in OEIS references A210662 as a column k >= 12.

## 4. Column-family existence: widths 12..28

Phrase searches "matchings in graph P_w" (OEIS text format, one GET each,
all http_status 200, all 219-byte empty "No results." responses):
- w=12: 2026-11-08T21:13:45Z — No results
- w=13: 2026-11-08T21:14:12Z — No results
- w=14: 2026-11-08T21:16:30Z — No results
- w=20: 2026-11-08T21:16:30Z — No results
- w=24: 2026-11-08T21:16:31Z — No results
- w=28: 2026-11-08T21:14:13Z — No results
Family enumeration ("matchings in graph P_", 21:14:00Z) returns exactly the
published widths: A033506..A033514 = P_3..P_11 (plus PERFECT-matchings series
A028468-474, a different object — A028474 "perfect matchings in graph P_{12}
X P_{n}" is domino-only tilings, not monomer-dimer). "monomer dimer tilings
tabl" search (21:13:45Z + page 2 21:16:59Z): only A210662 and A028420 are
monomer-dimer rectangular/square tables; the rest are tatami/partition/dimer-
constant objects. -> No monomer-dimer column sequence exists for any width in
12..28, spot-checked at 12,13,14,20,24,28 and consistent with the FORMULA
line's silence beyond column 11.

## 5. OEIS exact-integer search — with an honest method caveat

- q=<k=13 integer> (2026-11-08T21:11:23Z, 200): "No results."
- q=<k=28 integer> (2026-11-08T21:11:23Z, 200): "No results."
- CONTROL A (published T(27,27), 177 digits, b-file-only term; 21:11:49Z,
  200): "No results." TOO. -> The OEIS search index does not cover large
  b-file-only terms, so "No results" for our 95-169-digit cells is a WEAK
  negative on its own.
- CONTROL B (11945257052321 = T(7,7), DATA-line-sized; 21:12:26Z, 200): found
  %I A210662, %I A028420, %I A033510 — the method works when a term is in the
  index.
- Compensation: the structural checks in sections 2-4 (no column sequence for
  any width >= 12 exists at all; the table's own b-file stops at row 27) make
  an invisible-in-index publication of these cells impossible within OEIS.

## 6. GitHub code search (authenticated, gh api search/code)

- CONTROL (50-digit pi prefix 31415926535897932384626433832795028841971693993751;
  2026-11-08T21:14:28Z): {"total_count":9008, items incl. parrot/parrot,
  mpusz/mp-units, gambit/gambit} — method proven on long digit strings.
- k=13 integer (21:14:38Z): {"items":[],"total_count":0}
- k=28 integer (21:14:39Z): {"items":[],"total_count":0}
- -> Neither integer appears in any indexed GitHub repo.

## 7. arXiv

- https://export.arxiv.org/api/query?search_query=all:%22A210662%22
  (21:15:05Z, 200): totalResults 0 — no paper mentions A210662.
- search_query=all:"monomer-dimer" AND all:"generating function"
  (21:15:05Z, 200): totalResults 4 — "Rotating-Memory Fibonacci Numbers and
  Periodic Tilings"; "A Generalized Grassmann-Pfaffian Framework...";
  "Automatic Counting of Tilings of Skinny Plane Regions" (Zeilberger-style:
  proves GFs for skinny regions, publishes no width-12..28 table values);
  "A Reciprocity Theorem for Monomer-Dimer Coverings" (dimer reciprocity
  theory). Abstracts read from the fetched XML; none publishes T(29,k) or any
  k X 29 monomer-dimer integers, nor a GF/recurrence for widths >= 12.
- Disclosed GF check: the only published width GFs are k=5,6 in A033508/
  A033509 (Perepechko 2013) — consistent with the claim's own disclosure; no
  GF exists for widths 7..28 anywhere I could find (OEIS family absent,
  arXiv absent).

## 8. V3R1T4S repo record

- TROPHY_CASE.md: no mention of A210662 (grep hit only inside
  known-knowns/square-grid-lattice-gas-exact-counts-oeis/2026-10-17-mizopl-fd616054/
  PREREG.md, which merely defines the p2 criterion).
- known-knowns/square-grid-lattice-gas-exact-counts-oeis/ contains ONLY the
  2026-10-17-mizopl-fd616054 directory (A089980 antidiagonal d=79,
  CONFIRMED_PARTIAL via PR #462). No row-28 or row-29 material confirmed.
- gh pr list --state all --search "A210662" --repo elder-plinius/V3R1T4S
  (21:15:38Z): #960 "[claim] ... A210662 row 28 (T(28,k), k = 1..27)" DRAFT
  (Nukewire, same author as this claim); #832, #951 (A054759); #462 (A089980,
  CONFIRMED_PARTIAL). Nothing else.
- gh pr list --state all --search "A028420" (21:15:55Z) + gh pr view 849:
  #849 "[claim] ... A028420 a(28) = 503599...75471 (222 digits, full
  criterion)" DRAFT/OPEN (Nukewire).
- VERIFIED, not trusted: gh pr diff 960 (21:15:57Z, 689,755 bytes; 328 large
  integers) contains NONE of the 17 claimed row-29 integers; gh pr diff 849
  (21:16:04Z, 95,657 bytes) contains NONE. Row 28 in PR #960 ends at
  T(28,28)... k=1..27 per its title; row 29 is beyond it.

## 9. Trivial-edit test

Published objects: b-file rows 1..27; GFs for widths 5 and 6 only; a SageMath
brute-force PROG. T(29,k) for k=12..28 cannot be obtained by editing any of
these — no published GF, recurrence, or column sequence exists for widths
>= 12, so each cell requires fresh computation (which the claim reports as
two independent runs). This matches the bank's partial-win p2 definition
verbatim ("a new row of an associated rectangular table (A210662 ...) extending
the largest published m by one"). Not a tie: no competing value exists
anywhere; there is nothing to tie with.

## Verdict

All 17 cells T(29,12..28) are strictly absent from: the live b-file (row 27
max), the entry page and its complete cross-reference set (columns 1-11 +
diagonal only; all other A-numbers are mechanical neighbors, verified by
title), every OEIS sequence referencing A210662 (16, all classified), the
monomer-dimer column family (no width 12..28 sequence exists; spot-checked
12/13/14/20/24/28), OEIS exact-integer search (with the index blind spot
documented and compensated), GitHub code search (0 hits, control 9008 hits),
arXiv (0 mentions of A210662; no table-extension paper), and this repo's
record (PR #960 = row 28 and PR #849 = diagonal a(28) verified to contain no
row-29 integer). The one weak instrument (OEIS integer search) is covered by
stronger structural evidence that the sequences which would have to hold
these cells do not exist.

pass: true
