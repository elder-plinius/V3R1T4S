# Criterion skeptic: anomaly-free-atlas-qmax (charter quarry 5), claim of run 2026-11-11-0917

Scope of reading: the claim folder only (CLAIM.md, REPRODUCE.md, status.md, object/, checker/, source/ including
source/atlas/). Scratch work: panel_work/criterion/ (lister, both checkers and mitm compiled from the claim's
sources; small lists, corruption tests, mitm outputs). No background jobs were started. The Q_max 41/42 lists were
not regenerated here (another skeptic does that); only their first 200000 lines were.

Claim under test: SM fermion content only (no right-handed neutrinos), Q_max 41: 66526761; Q_max 42: 79174540,
counted in the atlas paper's convention (arXiv:1812.04602 v5, JHEP 02 (2019) 082, erratum JHEP 08 (2019) 064).

## 1. Counting convention versus the paper

What the paper says (source/atlas/arXiv-1812.04602v5.txt):
- Rescaling invariance (sec. 2, item 2): solutions related by F -> cF, c rational, are one equivalence class; with
  integers this means gcd 1 and the overall sign identified (c = -1; sec. 4.1 also says F_Q1 <= 0 is chosen
  because solutions with positive F_Q1 come from multiplying all charges by -1, "in the same equivalence class").
- Permutation invariance (item 3): families permuted independently within each species (S3 per species).
- Bound: "integers whose magnitudes are bounded by some user-defined Qmax", "charge magnitudes up to Qmax", i.e.
  max |F| <= Q_max over all charges.
- Tables 2 and 3 (and erratum Table 1) captions: "Each row contains the all-zero charge solution".
- SM content: right-handed-neutrino charges set to zero (equivalently absent); 15 charges.

The claim's convention (CLAIM.md): 1 + #(nonzero, gcd 1, max|F| <= Q_max integer solutions modulo S3 per species and
F -> -F). This is the paper's convention item for item; the ACCs written in CLAIM.md and in checklist.c (hypercharge
equation x6: F_Q + 8F_u + 2F_d + 3F_L + 6F_e) are the standard ones in the all-left-handed basis.

One textual hazard I checked: the paper's prose says gcd > 1 assignments are removed "by checking whether all
charges divide by the same prime number less than Qmax" (strictly less). Read literally, at prime Q_max this would
keep e.g. Q_max x (a Q_max = 1 solution). The published numbers refute that literal reading: at Q_max = 2 it would
give 22 + 7 = 29, the table says 22. The tables, not the prose, fix the convention, and they fix gcd 1.

Own verification of all 40 published values (not taken from table_comparison.txt):
- SM solutions, Q_max 1..10: acclist (count + 1) and mitm both give 8 22 82 251 626 1983 3902 7068 14354 23800 = Table 2.
- SMnuR solutions, Q_max 1..10: mitm gives 38 358 4116 24552 111152 435305 1358388 3612734 9587085 21546920 =
  Table 3 / erratum Table 1; acclist agrees for Q_max 1..5.
- "Symmetry" (CIS, every species of the form {-a,0,a}, zero included): counted from the acclist lists, SM 1..10 =
  8 14 32 56 114 144 252 336 492 582, SMnuR 1..6 = 16 48 154 338 796 1218; SMnuR 7..10 from mitm's sign-fixed
  primitive term + 1 = 2332 3514 5648 7540. All equal the tables. 40/40.
- Fully independent brute force (own Python, plain enumeration of sorted triples, all six ACCs, divide by gcd,
  min of F/-F as class key): SM Q_max 1, 2, 3 -> 8, 22, 82.
- Alternative conventions do not fit (acclist modes, SM): both signs kept, Q_max 2/3/5 -> 30/132/1138 (+zero);
  gcd > 1 kept -> 29/96/668; only "with the zero solution" (mode 3) gives 22/82/626. So none of the candidate
  hidden quantifiers (sign, gcd, zero, permutations, bound as max|F|) is ambiguous: each alternative is excluded by
  the published values.

Verdict on 1: the convention is exactly the paper's; no hidden quantifier is left open.

## 2. Certificate: complete and independently recountable?

What the claim provides: a deterministic lister (source/acclist.c) whose output is globally sorted and canonical,
so the byte stream is a function of the solution set alone; the sha256 of each uncompressed stream
(object/counts.txt, receipts/SM41.sha256, SM42.sha256); a streaming checker (checker/checklist.c) plus a Python twin;
an independent counter (source/mitm.c) that does not list. The lists are not stored (3.3-4 GB each) but regenerated;
that is acceptable for "regenerable, identified by sha256" since the order is canonical and the sha256 pins the bytes.

What checklist.c checks per line: exactly 15 (18) integers; all six ACCs in integer form; max|F| <= QMAX; nonzero;
canonical (each species sorted ascending, the lexicographically larger of F and -F); gcd 1; strictly increasing
lexicographic order. Distinct canonical primitive lines are distinct equivalence classes (a canonical form is unique
per S3^5 x sign orbit, and primitive integer solutions related by a rational rescaling differ only by sign), so
"valid lines" is a lower bound on the class count: the checker proves soundness and distinctness.

Corruption tests on the SM Q_max 6 list (1982 lines, PASS on both checkers):
- caught (FAIL, both checkers): duplicated line, swapped adjacent lines, one charge altered (ACC), line negated
  (non-canonical), permutation inside a species (non-canonical), zero line inserted, gcd-2 multiple inserted in
  sorted position, a valid Q_max 7 solution inserted in sorted position (bound), short line, wrong QMAX (smaller),
  wrong NU.
- NOT caught (PASS): a deleted line (1981, PASS); a truncated stream (1000, PASS); an inserted blank line; doubled
  spaces. CRLF line ends: C checker FAILs, Python checker PASSes (format leniency, no effect on counts). A
  non-integer token makes the Python checker raise (non-zero exit, no PASS), which is safe.
- Hence completeness is NOT certified by the checker; it rests on (a) comparing the checker's "valid solutions" with
  count - 1 by hand (REPRODUCE.md says so explicitly), (b) the independent mitm count, and (c) the sha256 (which
  also catches the whitespace variants). Also a list for a smaller bound would pass "checklist 42" (lines need only
  max|F| <= 42); again only the count and the sha256 catch that. The certificate logic is sound as a whole:
  checker (every line valid, distinct) + an independent count equal to the line count = complete list.

My recomputations:
- mitm SM 41: RESULT inequivalent = 66526761 (P = 133019307, sign-fixed primitive = 34213; 80 s).
- mitm SM 42: RESULT inequivalent = 79174540 (P = 158313119, sign-fixed primitive = 35959; 106 s).
  Both equal the claim and receipts/mitm.txt.
- Lister on the certified row SM 20: sha256 f8e2ce35...e770, as REPRODUCE.md states; checker 1071440 = mitm 1071441 - 1.
- First 200000 lines of fresh SM 41 / SM 42 streams: sha256 ed8eacf1... / c9d64209..., identical to the
  pysample receipts; both PASS the C checker.
- mitm vs acclist agree at every Q_max I ran (SM 1..10, 20; SMnuR 1..5).
Independence of mitm from acclist: same author pool and the same linear-ACC elimination, but a different split
(Q,L,nu | u,d,e versus Q,u,d | L,e,nu), gcd by Moebius inversion instead of a per-line gcd, and the sign quotient by
Burnside instead of a canonical-representative choice. That is methodologically independent enough for the shape;
the 40 published values (computed by the paper's own program) anchor both.

Verdict on 2: the shape "complete, independently recountable list" is met, with the stated caveat that the list's
completeness is established by count agreement (checker line count = mitm count - 1), not by the checker alone.
Whether the full 41/42 streams hash to the claimed sha256 and pass the checker is the other skeptic's
regeneration; the receipts (checker PASS 66526760 and 79174539, pipeline exit 0) are consistent with the counts.

## 3. "with and without three right-handed neutrinos": single-content rows

Two readings: (a) the census is a two-table object and a claim extends it row by row, any new exact row of either
table being an extension; (b) every claim must extend both contents.

I adopt reading (a). Reasons: the criterion's object is "the exact census" and the parenthetical names its scope
(the two tables the paper tabulates); the shape asks for "exact counts past the published range", each row being
its own exact count with its own list. The paper itself treats the contents as separate tables with separate
published ranges ("Qmax <= 10 in the SM and Qmax <= 10 in the SMnuR"), and its erratum extended the census for
SMnuR alone (Q_max 7..10) with no SM rows, so a single-content extension is the authors' own practice for this very
census. Under reading (b) this claim alone would not satisfy the criterion; CLAIM.md reports SMnuR rows 11..20 as
confirmed in earlier runs, which I did not inspect (outside my read scope) and do not rely on. The confirmed scope
below is therefore stated as SM-only and must not be cited as an SMnuR result.

## 4. Beyond the published range; overstatement

- Largest published Q_max is 10 for both contents (paper sec. 4.2; erratum Table 1 stops at 10; status.md records
  the arXiv abstract page still at v5 on 2026-11-11). 41 and 42 are far beyond it. The criterion only requires going
  beyond the atlas's own range; I make no literature-wide novelty judgement, and the claim's sentence "No count for
  these rows existed before this run" reads as workspace provenance (rows computed after the run's PREREG), not as
  a literature claim.
- Wording: "complete canonical solution list (count - 1 lines; the zero assignment is counted but not listed)" is
  accurate and discloses the zero-solution convention. "Certified ... by an independent count (mitm.c)" is
  accurate. The claim states SM only and explicitly excludes SMnuR 21. I find no overstatement. Minor reproduce
  nits (not affecting the verdict): checklist.c does not compare against an expected count (disclosed); the
  `tee >(sha256sum > file)` process substitution can in principle finish after the next `cat`.

confirmed_scope: In the convention of the anomaly-free atlas (arXiv:1812.04602 and its erratum; all 40 published values reproduced), the number of inequivalent anomaly-free integer U(1) charge assignments of the Standard Model fermions without right-handed neutrinos is 66526761 for Q_max = 41 and 79174540 for Q_max = 42 (zero assignment included), each recounted here by the independent meet-in-the-middle counter and certified by a regenerable canonical list of count - 1 lines identified by sha256, subject to the separate regeneration check of those lists.
context: subagent (fresh context, Claude Code Agent tool)
pass: true
