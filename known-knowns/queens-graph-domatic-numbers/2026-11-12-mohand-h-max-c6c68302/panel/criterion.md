# CRITERION skeptic: claim "dom(Q_11) <= 19", filed as partial win p2

context: subagent (Claude Code Agent tool, fresh context)

Written 2026-11-12, report started 01:02:08Z (`date -u`). I read claim/CLAIM.md, claim/REPRODUCE.md, the three files
of claim/prereg/, claim/checker/PROVENANCE.md, claim/table/scout.md, the table PDF claim/table/lauri-corrigendum.pdf
(text extracted with pdftotext to the terminal), claim/code/formula_audit.py, crosscheck_base.py, check.py, enc1.py,
enc2.py and the header of audit_chain.py, and the kit files RUN.md, RULES.md, SUBMIT.md. I opened nothing else of the
workspace (in particular no other panel file). I did not re-run drat-trim; another skeptic does that.

## Light checks I ran (real output, abridged)

1. `code/formula_audit.py` on both encodings (run from claim/ with `python -I`):
   `FORMULA AUDIT enc1: PASS, the file is exactly these families and nothing else` (ALO 121, AMO 22990, OCC 10960,
   DOM 2420, SB 2299, CNT 63520, ZS 60720; 163030 clauses; missing 0, extra 0), and the same for enc2 (ALO 121,
   AMO 22990, DOM 2420, Q 7220, SB 2299, CNT 65080, ZS 60720; 160850 clauses). sha256 of the two Fbase.cnf equal the
   values in REPRODUCE.md (e08e926c... and 30a7518b...).
2. My own program, panel/criterion-code/semantic_check.py (imports no encoder and no author checker; queens
   adjacency written by me: same row, same column, or |dr| = |dc|):
   - both partitions in claim/partitions/ cover all 121 squares and every class dominates (19 classes, 18 classes);
     Lauri's 18-partition is moreover independent in every class;
   - the variable maps have no aliasing (28900 resp. 30460 named variables, all distinct, in range; no zero CNT entry
     where the count is reachable); the 64 lines of enc1 are exactly the rows, columns and diagonals;
   - for 12 different 20-partitions per encoding (6 near-domatic ones obtained by splitting a class of the 19-partition,
     6 random ones), relabelled by smallest square, with every auxiliary variable set to its intended meaning, every
     clause of Fbase.cnf holds except exactly one domination clause per (class, square) pair the class misses
     (e.g. 81/81/81 ... 466/466/466). So a domatic 20-partition would satisfy Fbase.cnf: the direction the claim needs;
   - Fbase-lemmas.cnf is Fbase.cnf followed by exactly the 60 lemma clauses a1, a2, a3 as stated in CLAIM.md.
   Last line: `SEMANTIC CHECK (criterion skeptic): PASS`.
3. REPRODUCE part A5 (`code/crosscheck_base.py`, with -B, output into panel/criterion-code/): for both encodings,
   K=19 with partitions/dom-Q11-19-partition.txt and K=18 with partitions/lauri-idom-Q11-18.txt: `SAT`, same
   partition, check.py `PASS`; last lines `CROSSCHECK BASE enc1: PASS`, `CROSSCHECK BASE enc2: PASS`.
4. REPRODUCE part A2 without --hash-proofs: `AUDIT enc1: PASS FOR THE LEMMA CHAIN ONLY (...)`, same for enc2.
5. My own third composition check, panel/criterion-code/composition_check.py (written without reading the body of
   audit_chain.py or second_audit.py): for each of the 40 classes, L1, L2, the 31 pieces and the glue file contain only
   clauses of Fbase, earlier lemmas / earlier Q_i, or unit clauses negating the file's own target; every Q_i contains
   all literals of a3; each file's sha256 equals the recorded cnf_sha256 next to a recorded "s VERIFIED", the proof has
   the recorded size. `COMPOSITION CHECK enc1 (criterion skeptic): PASS`, same for enc2.
6. sha256 of formulas/enc1/Fbase-lemmas.cnf (a69970d7...) and final/enc1/proofB2.bin (502f34a7...) equal the record
   final/enc1/stageB2.json; final/enc2/proofB2.bin is dde21857..., as stated in REPRODUCE.md; final/enc2/ has no verdict.
7. Largest proof file in chain/: 179,529,723 bytes (chain/enc2-c13-a4/piece-00.bin); 1,360 proof files, 79.49 GB.

## Point by point

(a) "a CNF encoding ... that a solver reports UNSAT, with a DRAT/LRAT proof checked by drat-trim or cake_lpr".
Literal reading of that clause of the full criterion: NOT met. No solver run ever reported Fbase itself UNSAT, and
there is no single DRAT proof of Fbase; there are 681 refutations per encoding of 681 different formulas, each with
its own drat-trim check, plus a composition step that is not a DRAT step (it is a clause-inclusion argument checked by
Python programs). The first pre-registration (claim/prereg/PREREG-run-2026-11-11-2012.md, 20:13:41Z) required
"a CNF file and a proof file" and said the status is otherwise at most PROMISING; the continuation pre-registration
(PREREG-run-2026-11-11-2141.md, 21:42:12Z, before the chain was computed) kept the requirements "unchanged" but
announced the chain and handed exactly this question to this skeptic. So the chain is not an after-the-fact change of
rule, but the author's own frozen rule is met only if this skeptic accepts the chain. (The 22:02Z note on splitting the
third lemma into 31 pieces plus glue is not in claim/prereg/, so I could not see it; it does not affect soundness,
since the composition is checked on the files.)
The claim, however, is p2, and the kit asks me to judge "one named enumerated partial win" by its words: "A
DRAT-certified upper bound improvement ...". On that wording I judge it MET ONLY WITH DISCLOSURE: every inference that
needs search is a refutation whose DRAT proof drat-trim checked (assumed confirmed); the only non-DRAT step is the
elementary rule "if every clause of G follows from Fbase and G with the negation of C is refuted, then Fbase implies
C", applied 680 times, and the inclusions it needs are checked by the author's two programs and by my third one
(check 5); this is the usual form of large SAT certificates (cube-and-conquer style composition). The confirmed scope
must say that the certificate is a chain of separately checked proofs, not one proof. Consequence: the result does not
meet the full success criterion's evidence clause literally (one more reason it is correctly filed as p2 and not as
the full criterion, which its "narrowing" wording would otherwise cover).

(b) "a CNF encoding of 'a partition into k classes exists'". MET, with disclosure. A CNF encoding in the ordinary
sense is a CNF that is satisfiable exactly when the statement holds; auxiliary variables with two-way definitions and
satisfiability-preserving symmetry breaking are standard parts of such encodings. Fbase contains exactly the families
listed (check 1), the definitions are total functional definitions of distinct fresh variables (check 2), and the
symmetry breaking holds for every partition relabelled by smallest square (classes of a domatic partition are never
empty); check 2 tests this directly on the file. The two premises (definitions, symmetry breaking) are not derived in
the proofs and must be named in the scope. The implied counting constraint is NOT a premise: it is absent from Fbase
(check 1) and derived inside the checked final proof, which makes the object stronger than the one first
pre-registered. The ZS sets and the lemma lists only name variables (premises that constrain nothing) or state lemmas
(derived), so their completeness is not assumed. "Exactly 20 classes" suffices: more than 20 dominating classes can be
merged into 20.

(c) "the encoding cross-checked by finding the known (k-1)-partitions as SAT". MET, with disclosure. With k = 20,
k-1 = 19, and no 19-partition is published (the table's lower bound is 18), so a published one cannot exist; the
19-partition used is the authors' own (draft pull request, unpublished). It is an explicit object and my own checker
accepts it (check 2); both generators at K=19 accept it as SAT (check 3). The 18-partition is the published one: its
grid equals Figure 2(c) "idom(Q11) = 18" of claim/table/lauri-corrigendum.pdf with the rows in reverse order (a
reflection of the board); both generators at K=18 accept it. The cross-check tests the generators at K=19 and 18, not
the K=20 file itself; that is inherent in the criterion, and check 2 covers the K=20 file against the definition. The
19-partition, if valid, would also give dom(Q_11) >= 19; that is not part of this claim and must not enter its scope.

(d) "with two independently written encodings agreeing". MET ONLY WITH DISCLOSURE. Facts from REPRODUCE.md: enc2.py
was written by a separate fresh context from a brief whose text is not recorded; that it did not read enc1.py is
the author's statement, not shown by a log; the brief prescribed the same design (same kinds of auxiliary variables,
same lists, same lemma statements) and everything after the encoders is shared. What I could check by reading the two
files: the code is genuinely different (variable allocation, domination on closed neighbourhoods against four line
indicators, symmetry breaking through a separate Q chain against the size counter, totalizer against Sinz counter,
different interfaces); the two-way size counter follows the same standard clause pattern in both, which the brief
prescribed; the docstring of enc2.py shows its author knew the downstream per-class renaming design. Independence of
writing is therefore plausible but only asserted. The risk the second encoding guards against (an encoder bug that
over-constrains the formula) is in any case covered by checks that do not depend on either encoder (formula_audit.py
and my semantic_check.py). "Agreeing" requires enc2's final step to be verified: pending at folder build time, so this
point is conditional. The scope should say "written in separate contexts", not "independently written" unqualified.

(e) "one of the open pairs" and "upper bound improvement". MET. dom(Q_11) in {18,19,20} is the first of the six
intervals named in the criterion, and the table PDF in claim/table/ lists dom(Q11) as 18-20 (row "dom(Qn) ... 18-20
20-21"). "Pairs" can only mean (parameter, n) cells: read as "two-value intervals", an upper-bound improvement would
settle the value, which is the full success, and would exclude three-value cells for no reason. 19 < 20 improves the
table's upper bound. Non-subsumed with respect to the source: the corrigendum's own count (two dominating 5-sets, so
21 parts need 2x5 + 19x6 = 124 > 121 squares) gives 20 and does not give 19 by the same count (the two 5-sets share
square 60, and 5 + 19x6 = 119 <= 121). The criterion also requires the interval to be still open "in any later erratum
or paper found by a search and in the live OEIS entries (A292192 and related), all re-fetched immediately before
claiming": the claim folder holds only the 21:42:14Z fetch of the corrigendum, no OEIS fetch and no literature search
(table/scout.md). That is the NOVELTY skeptic's part; my pass is conditional on it.

(f) Other points.
- Definition of "dominating": closed neighbourhoods in the queens graph (same row, column or any diagonal, any
  distance), the same in formula_audit.py, both encoders, check.py and my own code; no stretch. The domatic number is
  over partitions of all squares; the merge argument for more than 20 classes is sound.
- Checker: one implementation (drat-trim, upstream source byte-identical by its recorded sha256, Windows build with a
  32-bit `long`; reliable below about 2^29 integers of clause database). The largest proof is 180 MB (check 7) and the
  final proofs 154 MB and 157 MB, far below; the wrong "verification time" line is explained in PROVENANCE.md and does
  not touch the verdict. No LRAT / cake_lpr cross-check; the criterion allows drat-trim alone.
- Proofs cannot be shipped (79.49 GB in chain/ plus the final proofs): a stranger must regenerate them (hours; the
  solver is reported deterministic on the author's machine, another build may produce other proofs, which remain
  checkable). This limits outside verification; it is not a criterion failure, but the package must say so.
- Wording of CLAIM.md: "681 solver refutations" is loose: the 20 glue steps per encoding are unit propagation and the
  final proof is a counting.py derivation (749,958 new variables introduced by definition, RAT steps) followed by the
  solver's refutation; all are drat-trim checked, so the scope says "refutations", not "solver refutations".
- Null models: drat-trim self-tests reject a cut proof and a proof against a satisfiable formula
  (checker/selftest-output.txt, selftest-bin-output.txt); REPRODUCE part B lists further controls (not run by me);
  the satisfiable side shows the generators are not over-constrained at K=19 and 18, and my check 2 shows the K=20 file
  is not over-constrained relative to the definition. I see no null-model gap.
- No hidden quantifier found beyond "for each of the two encodings" (enc2's final step pending) and "re-fetched
  immediately before claiming" (NOVELTY). The claim is the upper bound only; nothing wider is claimed.

## Verdict

Full success criterion: not met to the letter (no single proof, no single solver report on the encoding).
Partial win p2: met, with the disclosures written into the sentence below, conditionally.

confirmed_scope: dom(Q_11) <= 19, one below the upper bound 20 of Table 1 of Lauri's Corrigendum (upper bound only), certified for each of two CNF encodings written in separate contexts (formulas/enc1/Fbase.cnf and formulas/enc2/Fbase.cnf, which besides the partition and domination clauses contain, as premises not derived in any proof, two-way definitions of auxiliary variables and symmetry breaking on class labels) not by one proof but by a chain of 681 refutations per encoding, each with its own DRAT proof checked by drat-trim (a Windows build of the unmodified upstream source) and composed by a clause-inclusion argument checked by scripts, the generators of both encodings accepting the authors' own unpublished 19-partition and Lauri's published 18-partition as satisfiable cases.

This pass is conditional on:
1. every drat-trim verdict the claim relies on being confirmed: the 1,360 chain checks (680 per encoding) and the
   final step of enc1, as recorded; and the final step of enc2 (formulas/enc2/Fbase-lemmas.cnf with
   final/enc2/proofB2.bin), which had no verdict when the folder was built, printing "s VERIFIED". If any of them
   fails, or the enc2 final step does not finish, this pass does not hold;
2. the NOVELTY skeptic's live re-fetch showing dom(Q_11) still open at 18-20 (table, later errata or papers, OEIS
   A292192 and related entries), as the criterion requires.
I assumed, as instructed, that the files are what CLAIM.md says; my own checks above found nothing contradicting it.

pass: true
