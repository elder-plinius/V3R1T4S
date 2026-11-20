# Skeptic REPRODUCE: dom(Q_11) <= 19 (no partition of the 121 squares into 20 dominating classes)

context: subagent (Claude Code Agent tool, fresh context)

Everything I wrote and every output named below is in panel\reproduce-code\. I read only claim\ (CLAIM.md,
REPRODUCE.md, the data files, checker\src\drat-trim.c, checker\src\binmode.c, checker\PROVENANCE.md,
checker\selftest-bin-output.txt) and, only after my own formula and chain checks had run, the author programs
code\formula_audit.py, code\audit_chain.py, code\crosscheck_base.py and the first 120 lines of code\enc2.py (plus a
grep for file writes in code\ before running any author command). I read no other folder of the run and no other
panel file. Time window of my work: 2026-11-12 00:50Z to 03:10Z.

## Definition checked (quoted from claim\CLAIM.md, "as in the source")

> Q_n has the n^2 squares as vertices; two distinct squares are adjacent iff they share a row, a column or a
> diagonal. A set D of squares dominates if every square is in D or adjacent to a member of D.
> dom(Q_n), the domatic number, is the largest k such that the squares split into k disjoint dominating sets.
> If the squares split into more than 20 dominating sets they also split into exactly 20 (merge classes: a superset
> of a dominating set dominates). So "no partition into exactly 20 dominating classes" gives dom(Q_11) <= 19.

The merging step is correct. What has to hold, and what I checked separately:
(1) a domatic 20-partition of Q_11 would satisfy Fbase.cnf; (2) if every chain file is unsatisfiable, Fbase implies
the 60 lemma clauses; (3) every chain file is unsatisfiable (drat-trim); (4) Fbase-lemmas.cnf is unsatisfiable
(drat-trim). Then Fbase is unsatisfiable and no domatic 20-partition exists. Both encodings, independently.

## 1. The two long checks (final step), started first

Command (my wrapper run_one.py, below-normal priority, output in final\):
`checker\bin\drat-trim-bin.exe formulas\<enc>\Fbase-lemmas.cnf final\<enc>\proofB2.bin`

| | enc1 | enc2 |
|---|---|---|
| start / end (UTC, my clock) | 00:50:43 / 02:32:37 | 00:50:43 / 02:35:54 |
| wall time measured by my wrapper | 6,114.0 s | 6,310.5 s |
| verdict line | `s VERIFIED` (exit code 0) | `s VERIFIED` (exit code 0) |
| proof bytes read by drat-trim | 153,739,919 (= file size) | 156,821,960 (= file size) |
| clauses in core | 95,497 of 163,090 | 97,071 of 160,910 |
| lemmas in core | 3,700,652 of 6,826,858 (1,575,329 RAT) | 3,717,486 of 6,847,300 (1,575,266 RAT) |
| peak paged memory (last poll 02:29Z) | 521 MB | 519 MB |

- enc2: this is, as far as the folder shows, the first verdict on the final step of the second encoding.
- enc1: the core statistics are identical, digit for digit, to the author's log final\enc1\drat-trim-stageB2.log.
- drat-trim's own "c verification time" lines say 1,818.9 s and 2,015.4 s: exactly my measured times minus 2^32
  microseconds (4,295.0 s), the 32-bit wrap described in checker\PROVENANCE.md. Verdicts are unaffected.
- Process ids: final\pids.txt (enc2) and final\pids-by-hand.txt (both; the enc1 line was lost by a concurrent
  append, see "Deviations").

## 2. The formula: my own program from the definition (formula_check.py)

Written before reading any author program. It names every variable from formulas\<enc>\varmap.json (X, CNT, OCC,
Q, ZS), computes the queens graph itself (square v = row v div 11, column v mod 11; closed neighbourhood N[t]),
encodes the intended meaning of every auxiliary variable with its OWN two-way clauses (its own sequential counter
Y(i+1,m) <-> Y(i,m) or (Y(i,m-1) and X(i)), own OR/AND definitions), and puts every clause of Fbase.cnf in exactly
one kind, each of which is true in the "canonical model" of a domatic 20-partition (classes renamed by increasing
smallest square, each auxiliary variable set to the value of its name):
ALO / AMO (pattern), DOMX (positive X clause of one class containing some N[t]), DEF (one class, implied by the
definitions alone: SAT call "definitions and negated clause" is UNSAT), DOM (implied by definitions plus "class c
meets N[t]"), SB (`-X(v,b) or R`, R on class a < b, implied by definitions plus "class a has a square of index < v"),
SB1 (one class c, implied by definitions plus "class c has no square of index < c", true after the renaming).
Strict DIMACS parsing (p-line first, integers only, header counts exact).

| kind | enc1 | enc2 |
|---|---|---|
| ALO | 121 | 121 |
| AMO | 22,990 | 22,990 |
| DEF, counter (CNT only / CNT with X) | 30,480 + 33,040 = 63,520 | 31,320 + 33,760 = 65,080 |
| DEF, line indicators OCC | 10,960 | - |
| DEF, prefix chain Q (Q only / Q with X) | - | 2,420 + 4,800 = 7,220 |
| DEF, set indicators ZS | 60,720 | 60,720 |
| domination | 2,420 DOM through OCC | 2,420 DOMX, each exactly N[t] |
| symmetry breaking | 2,280 SB (b = a+1) + 19 SB1 | 2,299 SB (b = a+1) |
| UNACCOUNTED | 0 | 0 |
| total = header count | 163,030 | 160,850 |

- Variables used: enc1 28,900, enc2 30,460; every used variable is named in varmap.json, every named one is used
  (so none of the encoders' counting-block variables occurs). No empty clause, no tautology, no repeated literal,
  no duplicate clause, no CR. sha256 of Fbase.cnf: enc1 e08e926c...dda3f, enc2 30a7518b...e37ce (= REPRODUCE A1).
- The 2,420 enc1 DOM clauses are each EQUIVALENT under the OCC definitions to "class c meets N[t]"; the 2,420
  (class, t) pairs are all distinct. varmap lines = exactly the 64 rows, columns and diagonals of my geometry.
- The 19 SB1 clauses are the unit clauses -X(0,c), c = 1..19 (units-check.txt). The 140 unit clauses of enc2 are
  all DEF (none on X).
- Same classification with a second solver (minisat22 instead of glucose4: formula_check_m22.py, identical counts;
  enc1 457 s / 342 s, enc2 2.6 s / 2.3 s for the SAT part).
- SAT-free cross-test inside the same program: 40 random 20-partitions per encoding, renamed by smallest square,
  canonical values computed by direct counting, all 163,030 / 160,850 clauses evaluated: 16,861 false clauses in
  each encoding, all of them domination clauses of a class that misses that N[t]; 0 other false clauses; 0
  domination clauses true while their class misses N[t].
- Clauses that are not bare constraints, and why each is harmless: the OCC, CNT, Q and ZS definitions (true in the
  canonical model for every partition: shown by the DEF check); enc1's domination stated on OCC (equivalent to the
  bare domination clause given the OCC definitions); the symmetry breaking SB and the 19 units -X(0,c) (true after
  renaming the classes by increasing smallest square, possible because every dominating class is non-empty). The
  implied counting constraint is absent. Conclusion: a domatic 20-partition would satisfy Fbase, in both encodings.
- Outputs: formula-check-enc1.txt, formula-check-enc2.txt, formula-check-m22-enc1.txt, formula-check-m22-enc2.txt.

## 3. The chain: my own composition check (chain_check.py, then chain_check2.py)

From the files alone: Fbase-lemmas.cnf must be Fbase.cnf (same clauses, same order) followed by extra clauses LEM.
Per class, files in the order L1, L2, piece-00..30, glue; each clause of a file must be (a) a clause of Fbase, or
(b) subsumed by a target proven by an EARLIER file of the same class, or (c) a unit clause; the file's target is the
disjunction of the negated units (c). If the file is unsatisfiable, Fbase implies its target. Every LEM clause must
be subsumed by a proven target. The intended statements (a1, a2, a3, Q_ii with d_0..d_30 = my own N[0]) are
recomputed from varmap.json for comparison.

| | enc1 | enc2 |
|---|---|---|
| files parsed strictly | 680 | 680 |
| Fbase-lemmas = Fbase + 60 clauses = {a1,a2,a3} of classes 0..19, in that order | yes | yes |
| clause occurrences justified by an earlier target | 11,220 | 11,220 |
| targets exactly as described in CLAIM.md | 110 | 680 |
| targets one literal STRONGER than described | 570 | 0 |
| glue target = a3(c), all classes | 20 / 20 | 20 / 20 |
| lemma clauses established | 60 / 60 | 60 / 60 |
| problems | 0 | 0 |

The 570 (enc1, classes 1..19, pieces 01..30): the unit `-X(0,c)` that negates the literal X(d_0,c) of Q_ii is also a
clause of Fbase (the SB1 unit), so read from the files the piece proves Q_ii without X(0,c), which subsumes Q_ii.
Harmless; the first version chain_check.py flagged these 570 as "differs", chain_check2.py accepts a target that
lacks only literals negated by Fbase units. Outputs: chain-check-enc1.txt (first version), chain-check2-enc1.txt,
chain-check2-enc2.txt. Conclusion: if all 1,360 files are unsatisfiable, Fbase implies the 60 lemma clauses.

## 4. Every proof of the chain: my own loop (1,360 of 1,360)

recheck_chain.py / recheck_chain2.py / recheck_chain3.py (same pairs, see "Deviations"), below-normal priority,
3 to 5 at a time beside the two long checks (4 during the first 3 minutes), one result file per pair in
chainrc\res\, pids in chainrc\pids-run1.txt, -run2.txt, -run3.txt. Verdict = the list of lines starting with "s "
must be exactly ["s VERIFIED"].

| | enc1 | enc2 |
|---|---|---|
| pairs (L1, L2, piece-00..30, glue x 20 classes) | 680 | 680 |
| exactly one s-line "s VERIFIED", exit code 0 | 680 | 680 |
| sum of my measured wall times | 9,615 s (2.67 h) | 11,290 s (3.14 h) |
| longest single check | 39.8 s | 55.1 s |

- All 1,360: drat-trim reports reading the whole proof (bytes read = file size); no "trivial UNSAT"; the only warning
  kind is "backward mode ignores deletion of (pseudo) unit clause" (320,414 lines in all), which makes drat-trim
  check the proof without those deletions, still a valid refutation. The 40 glue checks end "UNSAT via unit
  propagation on the input instance", as described.
- Repeatability: 164 pairs run a second time (chainrc\res-again\, pids-again1.txt) and 10 small pairs run separately
  (detres\): 174 of 174 identical (verdict, exit code, number of warnings, all non-timing output lines including
  the core statistics; determinism2.txt). The enc1 final step also reproduced the author's core statistics exactly.
- 32-bit limit of these builds (checker\PROVENANCE.md, clause positions < 2^29 integers): from drat-trim.c
  (EXTRA = 4 integers per clause, at least 2 bytes per binary clause), the clause database is at most the formula
  plus 2 x the proof size in integers: largest chain proof 179.5 MB, so at most about 361 M < 536.9 M; the final
  checks stayed near 520 MB of memory. The limit is not reached by any of the 1,362 checks.
- Final tally: final-tally.txt.

## 5. Identity of the files, and other checks

- sha256 of all 1,360 chain formulas = the value in l12.json / state.json = manifests\chain-manifest-<enc>.txt
  (chain_check2.py); sha256 of all 1,360 chain proofs = records = manifest, sizes = manifest (hash_proofs.py, 58 s,
  proof-hashes.txt); all records and manifest lines carry "s VERIFIED".
- final\enc1\proofB2.bin 502f34a7...067de, final\enc2\proofB2.bin dde21857...1b1679 (= REPRODUCE A4, enc1 also
  = final\enc1\stageB2.json); formulas\enc1\Fbase-lemmas.cnf a69970d7...e4e5 (= stageB2.json);
  formulas\enc2\Fbase-lemmas.cnf d805e114...1cda (no author record exists for it).
- The 60 lemma clauses checked by the final step are exactly the 60 clauses the chain establishes (section 3).
- Lexical check of all 1,364 formulas given to drat-trim (token_check.py): p-line first, then only decimal integers
  without leading zero, single spaces/newlines: 0 bad. This matters, see "Doubts" (comment-line pitfall).
- varmap "sets" = lists\e2-Q11-m5.txt + lists\e2-Q11-m6-minimal.txt in this order, 434 sets, both encodings
  (lists-check.txt).
- Satisfiable side, my own checker (check_partition.py): partitions\dom-Q11-19-partition.txt is a partition into 19
  dominating classes (sizes 6 x14, 7 x3, 8 x2), partitions\lauri-idom-Q11-18.txt into 18 (partition-check.txt).
  (The lower bound is not part of the claim.)

## 6. Negative controls (neg_controls.py, neg\report.txt; all on copies inside my folder)

- Chain composition (encoding 2, class 0, chain_check3.py = chain_check2.py limited to one class): untampered copy
  passes; rejected as required: extra non-unit clause in piece-05; extra unit in glue; lemma a3 replaced by a
  stronger clause in Fbase-lemmas; header count off by one; later case Q_11 used in piece-10; comment line after the
  p-line.
- Formula (encoding 2, formula_check.py): rejected as required: extra clause on two squares of one class; one SB
  clause shifted to Q(c,v-1); extra unit "class 0 has at least 6 squares"; clause on an unnamed variable; one
  domination clause with N[60] minus square 60. (The harness mislabelled the unnamed-variable case as passing: the
  check printed UNACCOUNTED(unnamed var) and then stopped with a KeyError without its success line; re-judged
  with the right criterion by neg_f4_recheck.py: rejected, neg-f4-recheck.txt.)
- drat-trim (encoding 2, class 0): proof of piece-30 cut in half; L1 without its negated-target unit (satisfiable);
  glue without case Q_15; piece-00 with the proof of piece-01; L1 with an empty proof: all five "s NOT VERIFIED".
- 17 of 17 controls behave as required.

## 7. Author commands (run after my own checks) and comparison

A1 formula_audit.py: PASS, PASS. A2 audit_chain.py (without --hash-proofs, I hashed everything myself): PASS FOR THE
LEMMA CHAIN ONLY, both. code\second-audit\second_audit.py: PASS, PASS. A5 crosscheck_base.py (output into my folder,
run with -B so nothing was written in claim\): 19- and 18-class formulas SAT with the partitions fixed, decoded
grids pass check.py, PASS for both encodings (author-cmds\). Not run: A3 (my own loop replaces it), A6, part B,
part C. formula_audit.py rebuilds the expected clauses family by family and compares multisets (a syntactic check,
stronger than mine on form, weaker on meaning); its counts agree with mine. audit_chain.py defines each piece target
from the trailing run of units, like mine; it agrees.

## Mismatches and doubts

- No mismatch between the files and CLAIM.md / REPRODUCE.md was found. The 570 "stronger" piece targets of enc1
  are a reading difference (the file does contain all units negating Q_ii, one of which is also an Fbase clause).
- Comment-line pitfall (not exploited here): with a binary proof, drat-trim does not skip a comment line placed after
  the p-line of the formula; it reads it as empty clauses. My test (comment_pitfall.py, comment-pitfall.txt): a
  satisfiable 2-clause formula with such a line and the proof "add empty clause" gives "c trivial UNSAT" and
  "s VERIFIED" with claim\checker\bin\drat-trim-bin.exe. The author's parsers (formula_audit.py, audit_chain.py)
  skip lines starting with "c", so they would not see this. None of the 1,364 formulas here has such a line
  (lexical check), and no check printed "trivial UNSAT".
- One checker implementation only, compiled by the author (see "Could not check").
- Whether a chain of 681 checks per encoding is "a DRAT/LRAT proof checked by drat-trim" in the bank's sense is not
  judged here (CLAIM.md leaves it to the reader).

## Deviations in my own procedure

- formula_check.py was rewritten once with the Write tool before its first run (the only file of mine I overwrote);
  every later change went to a new file (chain_check2/3.py, formula_check_m22.py, recheck_chain2/3.py, ...).
- final\pids.txt lost the enc1 line (two processes appended at once); both pids are in final\pids-by-hand.txt.
- I stopped my own chain loop twice (version 1 after 3 minutes to lower concurrency to respect the 6-process limit;
  version 2 after 33 minutes to keep fuller output). The manager was killed before its checker children, so no record
  was written for a killed check; those pairs were re-run by the next version. 164 records of versions 1 and 2 kept a
  truncated output (verdict computed from the full output); these 164 pairs were run a second time with full output.
- Pids of the short sequential runs (negative controls, determinism run, pitfall test, analysis scripts) were not
  written to files; all ended. Idle wrapper/manager Python processes were not counted in the 6-process limit.
- An author's drat-trim process on encoding 2 (another folder, not mine) was running at 00:51Z and had ended by
  01:27Z; I did not touch it and did not read its output. At 03:07Z none of my processes remained.

## What I could not check

- That checker\bin\drat-trim-bin.exe was built from checker\src (no compiler used); that checker\src\drat-trim.c is the
  upstream file (its sha256 equals the one in PROVENANCE.md; no network). The binary behaved correctly on my 5
  negative drat-trim controls and repeated runs are identical, which is evidence, not proof.
- The SAT solvers of python-sat used by my formula check (two solvers agree; the SAT-free evaluation agrees).
- Pre-registration, timeline and the independence of enc2.py from enc1.py (outside the files' content).
- REPRODUCE A6, part B, part C (rebuild from the generators).

pass: true
