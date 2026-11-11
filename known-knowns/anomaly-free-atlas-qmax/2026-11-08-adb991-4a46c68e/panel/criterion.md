# Criterion skeptic: SM Q_max 39 and 40 (run 2026-11-08-0917)

Scope read: claim/ only (CLAIM.md, REPRODUCE.md, status.md, object/, checker/, source/ incl. source/atlas/).
Own work: panel_work/criterion/ (compiled acclist, checklist, mitm from the claim's sources; own brute-force
counter brute.py; corrupted-list tests). One background job (python brute.py 4, PID 5224) ran and finished on its own;
nothing else was started in the background. The Q_max 39/40 lists were not regenerated (another skeptic's task).

## 1. Counting convention vs the paper

Paper text (arXiv:1812.04602v5, source/atlas/): solutions are identified up to (a) rational rescaling, i.e. integer,
primitive representative, sign F -> -F included (sec. 2, item 2; sec. 4.1 "multiplying all U(1)F charges ... by the
same -1 factor ... same equivalence class"); (b) independent family permutations within each species (item 3,
S3^5 for SM); (c) bound = charge magnitudes |F_X| <= Q_max ("integers whose magnitudes are bounded by some
user-defined Qmax"; "charge magnitudes up to Qmax"), i.e. max |charge| <= Q_max; (d) the tables' captions: "Each row
contains the all-zero charge solution, as well as the solutions indicated in the rows above" (cumulative, zero counted).
In the SM case the nu charges are set to zero (15 charges). CLAIM.md's convention (1 + #nonzero primitive solutions
mod S3^5 x sign, max|F| <= Q_max) matches each of these.

One textual wrinkle checked: sec. 4.1 says non-primitive assignments are removed by testing primes "less than Qmax".
Read literally (strict), the doubled Q_max=1 solutions would survive at Q_max = 2 (giving 29, not 22). The published
22 (and every other value) fits gcd = 1 exactly, so the published numbers fix the convention as full gcd 1.

Hidden quantifiers are discriminated by the data: acclist's alternative modes at Q_max 2..5 give (lines, excl. zero)
sign-not-identified 29/131/445/1137, gcd not required 28/95/285/667, versus the main convention 21/81/250/625
(= published 22/82/251/626 minus the zero row). Only the claimed convention reproduces the table.

Own checks (all match the published values exactly):
- mitm SM Q_max 1..10: 8 22 82 251 626 1983 3902 7068 14354 23800 (Table 2).
- mitm SMnuR Q_max 1..10: 38 358 4116 24552 111152 435305 1358388 3612734 9587085 21546920 (Table 3 / erratum Table 1).
- acclist SM Q_max 1..10 lists, each PASS under checklist, line count + 1 = Table 2 "Solutions", and the number of
  totally CIS rows (every species {-a,0,a}) + 1 = Table 2 "Symmetry" (8 14 32 56 114 144 252 336 492 582).
- acclist SMnuR Q_max 1..5: Solutions and Symmetry (16 48 154 338 796) both match Table 3.
- The Q_max = 1 SM list equals the paper's Table 1 row for row (after reordering species Q nu e u L d -> Q u d L e).
- Own brute-force counter (Python, enumerates multiset 5-tuples and imposes all six ACCs literally, explicit
  canonical sign representative, gcd 1): Q_max 1..4 give 8/22/82/251 with CIS 8/14/32/56.
- I re-derived the ACC coefficients (Q: 6 states, u,d: 3, L: 2, e: 1; Y^2 F times 6 = Q + 8u + 2d + 3L + 6e) and the
  linear-sum reductions used by acclist and mitm (s_d = -2sQ - su, s_L = -3sQ, s_e = 2sQ - su, s_nu = 4sQ + su).
So the 40 published values in table_comparison.txt are reproduced, plus the 30 Symmetry values I could test, and the
convention is exactly the paper's.

## 2. Certificate shape (complete, independently recountable list)

Structure: a deterministic lister (acclist.c; single-threaded, total-order sort, fixed formatting) regenerates each
list, identified by the sha256 of its uncompressed stream (counts.txt); checklist.c checks every line; mitm.c counts
by a different method (multiset counting over a different meet-in-the-middle split, Moebius over gcd, Burnside for
the sign) without listing. Completeness follows from: every line is a valid canonical class (checker), lines are
strictly increasing hence pairwise distinct classes (canonical form is a unique orbit representative), and the number
of lines + 1 equals the independent total. I reproduced the stated SM 20 hash (f8e2ce35...e770) and its PASS, and
re-ran mitm: SM 39 = 51237625, SM 40 = 58626334 (73 s, 86 s), equal to counts.txt. Cross-check at Q_max 25:
acclist count-only 3920607 + 1 = mitm 3920608.

checklist.c, tested with deliberately corrupted SM Q_max 6 streams:
- duplicated line, swapped adjacent lines, first line re-appended at end: FAIL (not strictly increasing).
- species unsorted, raw negation, sorted negation (wrong sign representative): FAIL (not canonical).
- doubled (gcd 2) solution within the bound: FAIL (gcd not 1). Zero line: FAIL. ACC perturbed: FAIL.
  14 integers: FAIL (wrong length). Q_max 6 list checked at bound 5: FAIL (charge above QMAX).
- missing line: PASS with 1981 instead of 1982. The checker does not compare with an expected count (REPRODUCE.md
  says so); a missing solution or wrong count is caught only by comparing its "valid solutions" with counts.txt and
  the mitm count. That comparison is part of the protocol and was done (receipts: 51237624, 58626333 = count - 1).
- Tolerated without failing: blank lines (skipped), "+6" or "06" spellings (strtoll). These cannot change the set of
  classes counted; byte-level deviations are caught by the sha256, not by the checker. Minor.
The Python checker applies the same rules independently (used on 200000-line samples only, per receipts).

Verdict on shape: the list is not stored (2.5-2.9 GB) but is fully specified by a deterministic generator plus its
sha256, checked line by line, and recounted by an algorithmically independent counter; anyone can regenerate it in
about 15-18 min. I accept this as "the full solution list as the certificate". Caveat: lister, checker and counter come
from the same workspace; independence is methodological, and my own brute force only reaches Q_max 4.

## 3. "with and without three right-handed neutrinos"

Two readings: (B) every claim must contain both contents; (A) the parenthetical defines what the census covers (two
tables, SM and SMnuR), and the census is extended row by row, each (content, Q_max) row being an exact count with
its own certificate. I adopt (A). Reasons: the object being extended is "the exact census ... (with and without ...)",
i.e. the paper's two tables; the charter's shape speaks of "exact counts past the published range", which are
per-row records; the two contents have very different costs (the claim notes SMnuR 21 needs a multi-hour list), so
requiring both in one claim would make the criterion depend on bundling rather than on the correctness of new counts.
Under (A) SM-only rows satisfy the criterion; under (B) this claim alone would not (CLAIM.md says SMnuR rows 11..20
were confirmed in other runs; I did not verify those and do not rely on them). The confirmed scope below is therefore
stated as SM only.

## 4. Beyond the published range; overstatement

The paper says the atlas is "for Qmax <= 10 in the SM and Qmax <= 10 in the SMnuR" and the erratum adds only SMnuR
7..10; the arXiv record fetches show v5 is still current. Q_max 39 and 40 are far beyond 10. The claim says "SM alone
(no right-handed neutrinos)", gives the zero-assignment convention explicitly (count - 1 lines), marks itself
unpanelled, says the checker does not compare counts, and makes no SMnuR claim for these rows. "Independent count"
is fair as methodological independence. No overstatement found.

confirmed_scope: In the published atlas convention (family permutations within each species and overall sign identified, gcd 1, max |charge| <= Q_max, the all-zero assignment counted), the number of inequivalent anomaly-free integer U(1) charge assignments of the Standard Model fermions without right-handed neutrinos is 51237625 for Q_max = 39 and 58626334 for Q_max = 40, which goes past the published range (Q_max <= 10), with each row certified by a deterministic canonical list (count - 1 lines, sha256 in object/counts.txt) and an independent count; this skeptic reproduced the convention on all 40 published values and re-ran the independent counter at 39 and 40, but did not regenerate the lists.
context: subagent (fresh context, Claude Code Agent tool)
pass: true
