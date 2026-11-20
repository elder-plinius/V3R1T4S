# REPRODUCE skeptic verdict: no 5 x w Life orphan for w <= 8 (new size 5x8), target life-smaller-orphan (partial win p1)
context: fresh headless Grok Build CLI session (grok --prompt-file), started with no prior conversation in a copy of claim/

## what you read
CLAIM.md, REPRODUCE.md, METHOD.md, TARGET_CRITERION.md, NOVELTY_RECORD.md.
code/mcnf_route/mcnf.c (full), mcube.sh; code/tcnf_route/tcnf.c, tcnfc.c, subseq.c, brutepred.c, summary.sh (headers/logic).
data/mcnf_route/cubes/h5w7r8_12 and h5w8r8_12 result rows; data/tcnf_route/cubes/h5w7r8_12 and h5w8r8_12; subset_day3_seg2.txt, subset_day6_seg3.txt, cube_controls.txt, control_rules.txt, life.tsv, tcnf/mcnf NOTES.md.
Public LifeWiki Garden of Eden page snippet (read-only): Wade 2023 no height-4 orphans; Beer no 7x7 GoE; Eker 5x83 exists; smallest listed orphan 12x8; no statement that 5x8 is already empty.

## what you ran
Re-executed:
- `gcc -O2` rebuild of mcnf.c, tcnf.c, tcnfc.c, subseq.c, and an independent predcheck.c
- `./mcnf 5 7 3 8 12 4 23` (val 23, not 11 or 26) -> `p cnf 147715 14696677` (256MB); trailing units `16 0 / 17 0 / 18 0 / -19 0 / 20 0` = column-4 bits of 23
- `claim/tools/cadical-cli --lrat=true --binary=false` under `nice -n 19`, `ulimit -t 600`, `ulimit -v 4500000`, `timeout 400`
  key output: `s UNSATISFIABLE`; `c exit 20`; process time 163.28 s; max RSS 2728.70 MB
- `claim/tools/lrat-check work/c4v23.cnf work/c4v23.lrat`
  key output: `c parsed a formula with 147715 variables and 14696677 clauses`; `c VERIFIED`; verification time 4.35 s; proof size 122384 KB
  recorded row c4v23.res: result=20, proof_kb=122384, check=c_VERIFIED, check_ms=4378, clauses=14696677
  then deleted the CNF and proof
- independent column-DP predecessor checker: `./predcheck 3 3` -> `NO_ORPHAN_3x3 checked=512`; five random 5x5 targets (seeds 42, 99) all `HAS_PRED`
- `./subseq` on tcnf 3x4 c2v5: `SUBSET_OK matched=101171 units=3`; on tcnf 4x5 c3v9: `SUBSET_OK matched=1058483 units=4`
- polarity controls: mcnf B64/S1 h=2 w=2 -> cadical exit 10, `s SATISFIABLE` (matches control first-SAT width 2); mcnf Life 3x3 -> `s UNSATISFIABLE`, `c VERIFIED`, clauses=99352 matching life.tsv

Audited only (not re-solved): all 32 tcnf and 32 mcnf 5x7 and 5x8 `.res` files; tcnf/mcnf subset logs; coverage argument in METHOD.md / tcnfc.c comments; LifeWiki novelty snippet. Full 5x8 cubes were not re-run.

## findings
VERDICT: pass

The one fully re-executed 5x7 mcnf cube (col 4, val 23) is UNSAT with an LRAT proof that lrat-check accepts. Clause count, proof size, and `c VERIFIED` match `data/mcnf_route/cubes/h5w7r8_12/c4v23.res` exactly (solve time 163 s vs recorded 151 s, ordinary solver variance). Cube units land on mcnf X vars 16..20 as METHOD.md states.

Coverage (audited, sound): every 5-row target fixes column 4 to exactly one of 32 values. tcnf cubes = full formula minus some transfer clauses plus h units, a clause-subset of (full + units), so cube UNSAT implies full-and-cube UNSAT; subseq confirmed that shape on two small sizes, and their 5x8 subset log says SUBSET_OK for v0/v13/v31. mcnf cubes add five units and drop nothing (subset_day6_seg3: 16793856 + 5). Both 5x7 and 5x8 tables are 32/32 `result=20` + `check=c_VERIFIED` for each encoding.

Encoding polarity (re-executed on tiny instances): SAT iff some target is an orphan. Independent Life DP finds no 3x3 orphan and predecessors for random 5x5 targets, agreeing with the SAT side.

No soundness error found in the audited split or in mcnf/tcnf join/transfer polarity. 5x8 is the new size relative to Beer 2023 (no 7x7) and Wade 2023 (height <= 4). This is p1, not a smaller orphan than Eker 12x8. kissat was not run; CLAIM.md discloses that.

## caveats
Did not re-solve any 5x8 cube (each ~7–20 min). Did not run kissat or cake_lpr. subseq was not re-run on the 15M-clause 5x8 formulas. Independent checker was only 3x3 exhaustive plus five random 5x5s. Literature check is a LifeWiki snippet, not a full Beer 2023 paper read. Bundled `lrat-check` is the drat-trim-family checker named in METHOD.md; its source was not rebuilt.

scope: re-executed one rebuilt 5x7 mcnf cube (val=23) through CaDiCaL+LRAT+lrat-check, a small independent predecessor DP, subseq on two small tcnf cubes, and tiny SAT/UNSAT polarity controls; audited but did not re-solve the 5x8 cube tables or kissat.

pass: true
