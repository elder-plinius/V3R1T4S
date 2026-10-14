# CRITERION verdict: hsp4, d = 4, N = 62

context: subagent (Claude Code Agent tool, fresh context; one context panelled 14 separate claims, each judged on its own files)

Files consulted, all relative to this claim folder: CLAIM.md, REPRODUCE.md, hsp4-62-candidate.txt, hsp4-62-posted.txt, hsp4_radius_as_fetched.txt. Nothing outside the claim folder was read. All numbers below come from my own checker (mpmath, mp.dps = 50, no tolerance anywhere, values parsed directly from the file strings), run with `python -I` on this claim's files only; the claimant's REPRODUCE.md script was not executed.

## Clause-by-clause

1. Object and container convention. hsp4-62-candidate.txt has one `#` comment line and exactly 62 coordinate lines of 4 tokens each (header says N=62; folder says N=62; consistent). Container is the unit ball centred at the origin: every centre has norm <= 1, and every centre has norm <= 1 - r*_cand (checked explicitly, True). Convention cross-check: recomputing r* from hsp4-62-posted.txt with the same formula reproduces the table value to 5.4628e-13, i.e. Packomania's hsp4 numbers are on exactly this convention. Verdict: met.

2. r* computed exactly as the clause says. r*_cand = min( min_(i<j) |c_i - c_j| / 2 , 1 - max_i |c_i| ) = 0.26883347811496426252 (15 significant digits: 0.268833478114964); binding term: wall. No tolerance, no rounding, mpmath 50 digits. Verdict: met.

3. Strictly greater than the 12-decimal table value by at least 1e-10. Table row in hsp4_radius_as_fetched.txt: `62 0.268830626376` (12 decimals; the posted file's first line carries the identical string). gain = r*_cand - table = 2.85173896426252e-6 (15 significant digits) = 28517.39 x 1e-10. Strict inequality: True. gain >= 1e-10 with no tolerance: True. Verdict: met.

4. Not isometric to the posted configuration. Sorted pairwise-distance multisets (1891 distances each): max |difference| = 0.0064937575; 1891 entries differ by more than 1e-8. The sorted multiset is isometry-invariant, so any difference above 1e-8 proves non-isometry. Verdict: met.

5. Table value "re-fetched live immediately before claiming". CLAIM.md asserts a fetch at 2026-10-14 15:29:10 UTC, HTTP 200, byte-identical to an earlier fetch. Not verifiable from files; this is the NOVELTY skeptic's job. If the live row for N = 62 has moved above 0.268833478114964 the margin clause fails. Not counted as failed here.

6. No newer History-of-updates entry for (4, 62) on the live hsp4.html. Not verifiable from files; depends on the live page. Not counted as failed here.

7. Queue rule and the 26-Sep-2026 "Moki & Julio *many* 4666 candidates" bundle. Not verifiable from files; the bundle is category-unspecified, so N = 62 must be re-checked against the live table once that bundle leaves the pending list. Not counted as failed here, but a pass on this file is conditional on it.

8. No submission is made. Nothing in the folder indicates one; nothing to check.

## Stretch hunt

- Rounding artefact: no. The comparison operands are the exact decimal strings in the files; the candidate's 17-significant-digit coordinates define r* deterministically.
- Wrong container radius: no (clause 1 cross-check, posted packing reproduces the table within 5.4628e-13).
- Mislabelled N: no (file name, header, row count and table row all say 62; the table has exactly one row for 62).
- More than one cell per claim: no, this claim is a single (d, N) = (4, 62) cell with one configuration file.
- Hidden quantifiers: "one N listed in the live radius.txt" and "d in {4,5,6}" are satisfied with d = 4, N = 62 present in the snapshot; nothing else in the clause is quantified over.
- Margin: gain = 2.85173896426252e-6 is 28517.39x the 1e-10 floor; nothing close to a rounding question.
- The sorted pairwise-distance multisets differ by up to 0.0064937575 (1891 of 1891 entries differ by more than 1e-8): a different arrangement, not a perturbation of the posted one.
- Null model: not needed and would be meaningless. The object is explicit, the checker is deterministic, and the criterion is a strict inequality on a computed number; there is no statistic to compare against chance.

## Raw checker output for this claim

```
candidate file: 1 comment line(s), 62 coordinate line(s), 0 line(s) with token count != 4; header: # N=62 r_float=0.26883347811496427 table=0.268830626376 gain=2.852e-06
  header N=62, folder N=62, rows=62 -> N consistent: True
posted file: first-line radius string '0.268830626376', 62 centres
table snapshot: 299 rows, rows for N=62: 1, row = 62 0.268830626376
  12-decimal table string: '0.268830626376' (12 decimals); posted first line equals table string: True
candidate: min pair half-distance = 0.26883347811524715031, 1 - max norm = 0.26883347811496426252, max norm = 0.73116652188503573748
  r*_cand = min(...) = 0.26883347811496426252   (15 sig: 0.268833478114964); binding term: wall
  container: all 62 norms <= 1 - r*_cand: True; all norms <= 1: True
posted:    min pair half-distance = 0.2688306263756899209, 1 - max norm = 0.26883062637545371686
  r*_posted recomputed = 0.26883062637545371686; |r*_posted - table| = 5.4628e-13 (convention sanity: True)
gain = r*_cand - table = 2.85173896426252e-6  (15 sig digits)
  strictly greater: True; gain >= 1e-10 (no tolerance): True; gain/1e-10 = 28517.39
  also vs posted packing recomputed r*: r*_cand - r*_posted = 2.8517395e-6
isometry: 1891 vs 1891 pairwise distances; max |sorted diff| = 0.0064937575; entries differing by > 1e-8: 1891; non-isometric: True
ALL FILE-LEVEL CLAUSES: True
```

confirmed_scope: For d = 4 and N = 62, the 62 centres in hsp4-62-candidate.txt lie in the unit ball centred at the origin and have feasible radius r* = 0.268833478114964 (mpmath 50 digits, no tolerance), which exceeds the 12-decimal table value 0.268830626376 in hsp4_radius_as_fetched.txt by 2.85173896426252e-6 (>= 1e-10) and is not isometric to hsp4-62-posted.txt (sorted distance multisets differ by up to 0.0064937575); the live re-fetch, History-of-updates and pending-queue clauses, including the unresolved category-unspecified Moki & Julio bundle, are not verifiable from these files and the pass is conditional on them.
pass: true
