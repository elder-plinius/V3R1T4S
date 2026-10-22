# REPRODUCE skeptic verdict — N = 4141 claim (packomania-cci-equal-circles-in-circle)

Fresh context. Judged only from the claim package (CLAIM.md, REPRODUCE.md, table_record.md,
verify_standalone.py, candidate_N4141.txt, cci4141.txt, radius.txt). Author's code was run only
after my own checkers passed.

## Definition I worked from (quoted, CLAIM.md "Success criterion")

> r\* := min( min_{i<j} |c_i - c_j| / 2, 1 - max_i |c_i| ), computed in mpmath at 50 digits
> directly from the submitted coordinates (no tolerance)

## What I implemented and ran (my own code, scratch under %TEMP%, outside the workspace)

1. `my_check.py` — my own checker: full float64 pass over all 8,571,570 pairs (row loop),
   generous 1e-7-relative candidate windows, exact re-evaluation of every window member from
   the coordinate strings in mpmath at dps=60 and again at dps=80 (both >= 50 significant
   digits); table row parsed from radius.txt by me; sha256 checks; sorted-distance multiset
   comparison; float64-rounded cross-check.
2. `check2.py` — a second, fully independent stack with NO mpmath: coordinates as exact scaled
   Python integers (x 10^18 / x 10^30), exact integer minimisation of squared pair distance and
   maximisation of squared norm (norm over all 4141 points; no window), binding term decided by
   pure integer comparisons, final square roots via stdlib Decimal at precision 100; pair
   discovery cross-validated with scipy cKDTree (set of near-min pairs identical to my row-loop
   set, symmetric difference 0). The two stacks agree digit-for-digit through 80 digits, and
   dps=60 vs dps=80 agree through 50 digits — deterministic, no precision cliff.
3. Author's `verify_standalone.py` run last, read-only, from this claim folder.

## Results (all from my own checkers unless stated)

- **Object shape:** candidate_N4141.txt has exactly 4141 centres, one "x y" per line, 18
  decimals each, no duplicate lines. cci4141.txt has 4141 centres, indices 1..4141, 30 decimals.
- **My r\* (candidate, string-exact, 80 digits, both stacks):**
  0.0146094714488139345759856245307456297376838717217189187511112429664194638505099...
  Binding term: half-distance (single binding pair, indices 3692/3883 in my 0-based scan);
  r_half = 0.01460947144881393457598562453074562..., r_cont = 0.01460947144881400784693320774118...
  CLAIM.md's value 0.01460947144881393457598562453075 is exactly this rounded to 31 significant
  digits: **matches**.
- **Table value:** radius.txt row 4141 parsed by me: `4141 0.014601755763187308074373236782`
  (raw row compared as text). sha256 of radius.txt and cci4141.txt match table_record.md.
  Corroboration: one plain curl of the live table this run returns the identical row
  `4141 0.014601755763187308074373236782`, so the margin also holds against the live cell.
- **Margin:** r\* - table = 0.00000771568562662650161238774874563... >= 1e-11 (threshold met with
  ~5 orders of magnitude to spare); equals REPRODUCE.md's `margin = 0.0000077156856266265...`.
- **Integrity (posted cci4141.txt vs its own table row):** my r\*(posted) =
  0.0146017557631873080743732367811705723053622845895322575175372..., i.e. it reproduces its
  table row to -8.29e-31 (rounding at the printed 30th decimal). Integrity clean.
- **Non-isometry:** sorted float64 pairwise-distance multisets of candidate_N4141.txt vs
  cci4141.txt (8,571,570 entries each): max elementwise difference 1.912e-02 (rounding noise
  would be ~1e-16). The multisets genuinely differ, so the configurations are not isometric.
  Matches table_record.md's "max elementwise diff 1.9e-2".
- **Author's checker:** verify_standalone.py prints r\* = 0.0146094714488139345759856245307456
  297376838717217189187511112, margin = 0.000007715685626626501612387748745629737683871721718
  9187511112, PASS — identical to my values through every printed digit. **No disagreement** on
  r\*, the table value, the margin, or the pass/fail logic (its two-pass float-window design is
  sound: float64 absolute distance error ~3e-16 against a 1e-9 relative window).

## Errata found (auxiliary numbers in the package that do NOT reproduce; none load-bearing)

1. table_record.md (and REPRODUCE.md's reference to it) states the posted config's feasible
   radius as 0.01460175576318720678111670571864, "reproduces its table row to -1.01e-16".
   Both of my independent stacks get 0.01460175576318730807437323678117057... (diff -8.29e-31);
   the recorded value is wrong at the 16th digit. The conclusion ("table integrity clean") is
   correct and in fact stronger with the right number.
2. CLAIM.md's parenthetical float64 cross-check states "gives 0.014609471448813892..."; parsing
   the coordinates as float64 and re-evaluating exactly at 50 digits gives
   0.01460947144881393470509886112830919... in both my stacks. The printed digits are wrong,
   though the sentence's own description ("differs only at the 17th decimal") fits my value,
   not the printed one.

Neither erratum touches the success criterion: the criterion's quantities (N centres, feasible
r\* from the submitted strings, strict improvement over the table row by >= 1e-11, non-isometry)
all reproduce exactly.

## Caveat (required by the criterion, restated)

The 26-Sep-2026 'Moki & Julio \*many\*' 4666-candidate bundle on pending-requests.html is
category-unspecified and unresolved; N = 4141 must be re-checked against the live table once
that bundle disappears. Live-fetch aspects beyond the one table row above rest on
table_record.md's records, which my sha256 checks corroborate but do not re-verify (out of this
panel seat's scope).

context: zcode Agent-tool subagent, fresh context

pass: true
