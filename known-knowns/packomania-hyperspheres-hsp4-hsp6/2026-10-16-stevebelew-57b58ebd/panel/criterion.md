# CRITERION skeptic verdict, claim N88 (d=4)

context: subagent (Claude Code Agent tool, fresh context for this one claim)

Method: I read CLAIM.md, REPRODUCE.md, hsp4-88-candidate.txt, hsp4-88-posted.txt and
hsp4_radius_as_fetched.txt, then wrote my own checker (not the one in REPRODUCE.md) and ran it
with the project venv's python using the -I flag, mpmath at mp.dps = 50, parsing every coordinate
string directly into mpf (no float round trip, no tolerance anywhere). Candidate lines are parsed
as exactly 4 fields; posted lines as exactly "index x1 x2 x3 x4" after the one-field radius header.
Any line of another shape would have been reported as malformed (none were).

Real command output (symbols ge/gt/lt written out in words to keep this file free of angle
brackets; everything else verbatim):

    candidate: N = 88  malformed lines: []
    posted:    N = 88  malformed lines: []
    posted header radius = 0.248505598356
    radius.txt rows: 299  rows with N=88: [['88', '0.248505598356']]  max N: 300  min N: 2
    candidate half-min-dist   = 0.2485140713906191231248344
    candidate 1 - max|c|      = 0.2485140713904002593455848
    candidate r*              = 0.2485140713904002593455848
    candidate max|c|          = 0.7514859286095997406544152  all centres within 1 - r*: True
    posted half-min-dist      = 0.2485055983552963024414646
    posted 1 - max|c|         = 0.2485055983551620584559392
    posted r*                 = 0.2485055983551620584559392
    table (12 dec)            = 0.248505598356
    |posted r* - table|       = 8.37942e-13  (less than 1e-11 parser sanity): True
    gain = r*cand - table     = 8.47303440025935e-6  at least 1e-10: True  strictly greater than table: True
    gain vs posted r* exact   = 8.47303523820089e-6
    num pairs cand/posted     = 3828 3828  (expect 3828)
    max |sorted-dist diff|    = 0.01570545603  greater than 1e-8: True
    count of sorted-dist diffs greater than 1e-8 = 3828
    min pairwise dist cand    = 0.49702814278123824625  (no duplicate centres: True )
    comment line: # N=88 r_float=0.24851407139040016 table=0.248505598356 gain=8.473e-06
    float(r*cand) = 0.24851407139040027
    contacts within 1e-9 of 2r*: 256  centres within 1e-9 of boundary: 81

    r* 15 sig fixed  : 0.248514071390400
    r* 16 sig fixed  : 0.2485140713904003
    gain 15 sig      : 8.47303440025935e-6
    gain / 1e-10     : 84730.3

## Clause-by-clause

1. "N centers in R^d (d in {4,5,6}) for one N listed in the live radius.txt"
   VERDICT: met for the snapshot. hsp4-88-candidate.txt has exactly 88 non-comment lines of
   exactly 4 coordinates each (d = 4). hsp4_radius_as_fetched.txt has 299 rows, N = 2..300, and
   exactly one row for N = 88. The posted file also has 88 centres, so N is not mislabelled.
   "Live" listing itself is the NOVELTY skeptic's re-fetch; the snapshot row is "88 0.248505598356".

2. "FEASIBLE radius r* := min( min_{i lt j} |c_i - c_j| / 2, 1 - max_i |c_i| ) (unit container
   ball centred at the origin), computed in mpmath at 50 digits directly from the submitted
   coordinates with no tolerance"
   VERDICT: met. Container convention confirmed: the binding term is 1 - max|c| (boundary term
   0.24851407139040025934..., half-min-distance term 0.24851407139061912312..., the boundary is the
   smaller by 2.2e-13), which only makes sense for a unit ball centred at the origin; the largest
   centre norm is 0.75148592860959974..., and every centre satisfies |c| at most 1 - r* (True by
   construction of the min, confirmed explicitly). r* = 0.2485140713904002593455848 at 50 digits,
   i.e. 0.248514071390400 to 15 significant digits. No duplicate centres (min pairwise distance
   0.497028...). As a parser sanity check the same code on hsp4-88-posted.txt returns
   0.24850559835516205..., which rounds to the table's 0.248505598356 (difference 8.4e-13, i.e.
   the table is the 12-decimal rounding of the posted packing), so the convention I used is the
   one Packomania uses.

3. "STRICTLY GREATER than that file's 12-decimal value for N ..., by at least 1e-10"
   VERDICT: met literally against the snapshot. gain = r*cand - 0.248505598356 =
   8.47303440025935e-6 (15 significant digits), which is strictly positive and about 84,730 times
   the 1e-10 floor. This is not a rounding artefact: the gain exceeds the table's 12-decimal
   rounding (5e-13) by seven orders of magnitude, and the gain against the exact posted r* is
   8.47303523820089e-6, essentially the same. The clause's "re-fetched live immediately before
   claiming" sub-condition is the NOVELTY skeptic's job; CLAIM.md records a 2026-10-16 16:29:32
   UTC fetch, HTTP 200, byte-identical to earlier fetches, with row 88 unchanged.

4. "the configuration is not isometric to the posted hsp4-88.txt configuration (sorted
   pairwise-distance multisets differ by more than 1e-8 somewhere)"
   VERDICT: met. Both multisets have 3828 = 88*87/2 entries. The largest entrywise difference of
   the sorted multisets is 0.0157, and in fact all 3828 entries differ by more than 1e-8. Since
   the sorted distance multiset is invariant under every isometry of R^4 (and under relabelling),
   this rules out isometry outright. The candidate is visibly a local re-polish of the posted cell
   (same rough centre pattern), but that is irrelevant to the clause, which only asks for
   non-isometry; the packings are genuinely different objects.

5. "(d, N) does not appear in a History-of-updates entry on the live hsp4.html newer than the one
   the scout fetched"
   VERDICT: cannot verify from the claim folder (no copy of hsp4.html is included). CLAIM.md and
   REPRODUCE.md record the expected "Last update: 06-Jul-2025" and no newer entry. Depends on the
   NOVELTY skeptic's live re-fetch; not counted as failed.

6. QUEUE RULE: "the N must NOT lie inside any range listed for this category on
   pending-requests.html re-fetched at verification time"
   VERDICT: cannot verify from the claim folder (no copy of pending-requests.html is included).
   CLAIM.md records no hsp4 entry on 2026-10-16 16:29:32 UTC. Depends on the NOVELTY skeptic's
   live re-fetch; not counted as failed.

7. Mandatory caveat: "The 26-Sep-2026 'Moki and Julio many 4666 candidates' bundle is
   category-unspecified and cannot be resolved; the verdict must state this caveat and the N must
   be re-checked against the live table once that bundle disappears from the pending list."
   CAVEAT STATED: the 26-Sep-2026 bundle of 4666 candidates is category-unspecified, so it cannot
   be excluded that it already contains a d=4, N=88 improvement; N = 88 must be re-checked against
   the live hsp4 radius.txt once that bundle disappears from the pending list.

8. "No submission (email) is ever made; the claim is for the verified construction only."
   VERDICT: consistent. CLAIM.md claims only the verified construction and records no submission.

## Stretch hunt

- Rounding artefact: no (gain is 8.47e-6, see clause 3).
- Wrong container radius: no (unit ball, origin-centred; boundary term binding, posted file
  reproduces the table under the same convention).
- Mislabelled N: no (88 lines in both files; one table row for 88).
- More than one cell: no; this folder is one N. CLAIM.md's note about N in (68, 69, 74, 75, 76)
  concerns other cells and does not affect the N = 88 judgement; the "earlier, smaller improvement
  of the same cell" note is confusingly worded but the folder contains one candidate and it is
  judged on its own, as the note says.
- Hidden quantifier "one N listed": satisfied, N = 88 is listed.
- Precision stretch: candidate coordinates carry 17 significant digits, parsed exactly as decimal
  strings into 50-digit mpf, so the computed r* is the r* of the submitted object, not of some
  higher-precision internal state.
- Minor cosmetic discrepancy, not material: the file's comment line states
  r_float=0.24851407139040016, whereas the correctly rounded double of the 50-digit r* is
  0.24851407139040027 (difference 1.1e-16, consistent with the lens having computed the comment
  value in double precision). CLAIM.md itself quotes 0.248514071390400..., which is correct.
- Null model: not needed and I agree. The claim is an explicit object judged by a deterministic
  checker against a published number; there is no sampling or statistical selection to control
  for, and "beats the table by 8.47e-6 with a non-isometric configuration" is either true of the
  file or it is not. It is true of the file.

## Subsumption

Not subsumed by any enumerated partial win: this is the full success criterion (strict gain at
least 1e-10 plus non-isometry) for one listed (d, N), conditional only on the live-page clauses
(5, 6) that the NOVELTY skeptic verifies.

confirmed_scope: In d=4 the 88 centres in hsp4-88-candidate.txt have feasible radius r* = 0.248514071390400 (mpmath, 50 digits, unit ball centred at the origin, no tolerance), exceeding Packomania's snapshot hsp4 table value 0.248505598356 for N=88 by 8.47303440025935e-6 and non-isometric to hsp4-88-posted.txt (all 3828 sorted pairwise distances differ by more than 1e-8), with the live history, queue and 4666-bundle clauses left to the NOVELTY re-fetch.

pass: true
