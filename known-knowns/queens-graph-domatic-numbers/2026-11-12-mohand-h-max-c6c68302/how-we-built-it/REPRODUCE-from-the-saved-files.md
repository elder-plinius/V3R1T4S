# Reproduce

Run every command from this folder (the one that holds CLAIM.md). Two tools are named below:
- PY: a Python 3. Parts A1 to A3 need only the standard library. The parts that solve or rebuild need the package
  python-sat (version used: 1.9.dev22, which contains the solver CaDiCaL 1.5.3 under the name cadical153).
- DT: checker/bin/drat-trim-bin.exe, drat-trim for 64-bit Windows built from the unmodified source in checker/src
  (how it was built, why there are two builds, and the size limit of these builds: checker/PROVENANCE.md). On another
  system, build drat-trim from checker/src/drat-trim.c; the proofs here are in drat-trim's binary format.
The programs write nothing outside the folders you give them. Encoders are found through PYTHONPATH=code.

## A. Check the claim from the saved files

A1. What the formula consists of (no encoder is imported; about 5 s each):
    PY -I code/formula_audit.py formulas/enc1/varmap.json formulas/enc1/Fbase.cnf
    PY -I code/formula_audit.py formulas/enc2/varmap.json formulas/enc2/Fbase.cnf
  Expected last line: FORMULA AUDIT enc1: PASS, the file is exactly these families and nothing else   (same for enc2)
  Expected sha256 of Fbase.cnf: enc1 e08e926ce30272fa64f0524d5d0325ae1c0d1f5390b6cd16bd54e6a6c87dda3f,
  enc2 30a7518ba31872fb8a1dbd962f4eaa855b19428fd9a0e87ee53e03d1876e37ce.

A2. How the chain composes (reads files only, no solver, no checker; under a minute without --hash-proofs, a few
    minutes with it because it then reads 36.5 and 43.0 GB of proofs):
    PY code/audit_chain.py formulas/enc1/Fbase.cnf formulas/enc1/Fbase-lemmas.cnf chain enc1 20 --hash-proofs
    PY code/audit_chain.py formulas/enc2/Fbase.cnf formulas/enc2/Fbase-lemmas.cnf chain enc2 20 --hash-proofs
  Expected last line: AUDIT enc1: PASS FOR THE LEMMA CHAIN ONLY (all 20 classes; the final step was not re-run here, ...)
  A second program for the same job, written by another context that had not seen the first:
    PY -I code/second-audit/second_audit.py --fbase formulas/enc1/Fbase.cnf --flem formulas/enc1/Fbase-lemmas.cnf --root chain --label enc1
    PY -I code/second-audit/second_audit.py --fbase formulas/enc2/Fbase.cnf --flem formulas/enc2/Fbase-lemmas.cnf --root chain --label enc2
  Expected last line: SECOND AUDIT enc1: PASS   (same for enc2)

A3. Every drat-trim check of the chain again, from the saved proofs (680 per encoding; the sum of the check times is
    about 2 to 3 hours of one core per encoding; the last argument is how many run at the same time):
    PY code/recheck_all.py chain enc1 20 checker/bin/drat-trim-bin.exe recheck-enc1.txt 6
    PY code/recheck_all.py chain enc2 20 checker/bin/drat-trim-bin.exe recheck-enc2.txt 6
  Expected last line: RECHECK enc1: 680 of 680 checks VERIFIED   (same for enc2)

A4. The final step, one drat-trim check per encoding (about 95 minutes each on the machine of this run while it was busy, 0.4 GB of memory, one thread; drat-trim prints nothing until the end):
    checker/bin/drat-trim-bin.exe formulas/enc1/Fbase-lemmas.cnf final/enc1/proofB2.bin
    checker/bin/drat-trim-bin.exe formulas/enc2/Fbase-lemmas.cnf final/enc2/proofB2.bin
  Expected: a line "s VERIFIED".
  sha256 of proofB2.bin: enc1 502f34a7892dd18460fbcef35873fdca8847897e5d5ce4139ab984316d5067de, enc2 dde2185725888dda48621abe850434c482621df2a0d17f531ebe1c12819b1679 (also in final/<enc>/stageB2.json).

A5. Satisfiable side (needs python-sat; a few seconds). The formulas for 19 and 18 classes, built by the same
    generators, must be satisfied by the two known partitions; the decoded grids are checked by code/check.py:
    PY code/crosscheck_base.py enc1 11 dom 7 out-crosscheck code/check.py lists/e2-Q11-m5.txt lists/e2-Q11-m6-minimal.txt 19 partitions/dom-Q11-19-partition.txt 18 partitions/lauri-idom-Q11-18.txt
    (and the same with enc2). Expected last line: CROSSCHECK BASE enc1: PASS

A6. Does the formula say what it should? Tests against a direct count on small boards and against the definition on
    the 11 x 11 board (needs python-sat; about 15 s per encoding):
    PY code/faithful.py enc1 lists/e2-Q11-m5.txt lists/e2-Q11-m6-minimal.txt partitions/dom-Q11-19-partition.txt out-faithful-enc1.txt base
    (and the same with enc2). Expected last line: FAITHFUL enc1 (base formula, counting block cut out): PASS
    It prints the sha256 of the 20-class formula it tested; it must equal the sha256 of formulas/enc1/Fbase.cnf.

## B. Controls that the checks can fail

    PY code/audit_negative.py formulas/enc1/Fbase.cnf formulas/enc1/Fbase-lemmas.cnf chain enc1 20 <a new folder>
  (seven kinds of tampering on copies of class 0, all must be rejected; last line AUDIT CONTROLS: PASS)
    PY code/test_counting.py enc1 checker/bin/drat-trim-bin.exe <a folder>
    PY code/probe_core.py enc1 6 8 6 checker/bin/drat-trim-bin.exe <a folder>
  (the derivation of the counting bound on small boards: accepted when right, rejected with a bound that is one too
  strong, on a satisfiable formula, and when cut in half)

## C. Rebuild everything from the generators (hours)

The lists are read in the order lists/e2-Q11-m5.txt, lists/e2-Q11-m6-minimal.txt; another order renumbers variables.
    PY code/dump_varmap.py enc1 11 dom 20 7 varmap.json lists/e2-Q11-m5.txt lists/e2-Q11-m6-minimal.txt
    PY code/stage_b2.py enc1 11 dom 20 7 <folder> checker/bin/drat-trim-bin.exe lists/e2-Q11-m5.txt lists/e2-Q11-m6-minimal.txt
  writes Fbase.cnf, Fbase-lemmas.cnf and proofB2.bin and checks the final step (about 95 minutes).
    PY code/run_pool.py 6 11 dom 20 7 <chain folder> checker/bin/drat-trim-bin.exe code <a file for process ids> enc1:0-19,enc2:0-19 lists/e2-Q11-m5.txt lists/e2-Q11-m6-minimal.txt
  rebuilds and checks the 2 x 680 proofs of the chain (about 14 minutes of one core per class for enc1 and 17 for enc2, 1.8 to 2.1 GB of disk per
  class). On the machine of this run the solver is deterministic: class 0 of enc1 was produced twice and gave
  byte-identical formulas and proofs. The formulas must have the sha256 listed in manifests/; proofs made by another
  build of the solver may differ and are still proofs if drat-trim accepts them.

## Departures from the pre-registration, stated as facts

- The pre-registration of the first run on this cell (2026-11-11T20:13:41Z) asked for "a CNF file and a proof file"
  on which drat-trim prints s VERIFIED. What exists is a chain of 681 checks per encoding. The pre-registration of
  the present run (2026-11-11T21:42:12Z, before any of its computations) announced a chain and left to the reader
  whether a chain is "a DRAT/LRAT proof checked by drat-trim" in the bank's sense.
- That second pre-registration described ONE drat-trim check for the third lemma of a class (all cases in one proof).
  It was replaced by 31 independent checks and a glue check, because the single proof (2.9 GB for one class) could
  not be loaded by the checker; this was written down at 22:02Z, before the 40 classes were computed.
- The object became Fbase (the formula without the encoder's counting clauses) instead of the encoder's full formula;
  written down at 22:56:28Z, before the first full-size verdict on the new final step was known.
- Classes 0 to 3 of enc1 were computed one after the other; from 23:06Z the remaining classes were computed six at a
  time by code/run_pool.py, with the same commands.

## Things a reader should know

- The Python process of stage_a4.py ended with the Windows code 0xC0000409 after printing its last line in 34 of
  its 43 runs (never stage_l12.py; first seen for classes 2 and 3 of enc1). The files it had written were complete
  each time. A class is counted as finished
  from its records (l12.json, state.json), never from an exit code, and A2 and A3 re-examine every file.
- An attempt to merge the chain into one proof file per encoding was abandoned: 80% of the lemmas are needed, so the
  file would be about 28 GB per encoding, which drat-trim cannot load on the machine of this run.

## The second encoding, and who wrote what

- enc1.py: written by the main session of the run (file time 2026-11-11T20:34:30Z,
  sha256 591e46907600b95d6a42ccc1fbe7d4e28e36aa273b99c2a073ff36d0e69ddae8).
- enc2.py: written by a subagent of that session (Claude Code Agent tool, a fresh context, model Sonnet 5.5), file
  time 2026-11-11T20:49:58Z, sha256 2ac9df43911f374bd8ee2c67b4c0e87f1f174135937b49f8fdf8636aab48d0b9; its own tests
  finished at 21:02:57Z. The file used here is byte-identical to that one: it was not edited after its tests or after
  any result. So encoding 1 existed when encoding 2 was written.
- What the subagent was given: a written brief asking for an encoder of the same problem with a fixed interface
  (the attributes X, S, ZS, clauses, nv and the methods class_vars, decode, partition_literals, write_dimacs) and the
  same list of additions (two-way size counters, indicators of listed sets, symmetry breaking on class labels, the
  implied counting constraint), to be written from the definition and not from encoding 1.
- What is NOT documented: the exact text of that brief. It exists only in the transcript of the main session, which
  lies outside the project folder; it was not consulted when this file was written, so it is not quoted here and has
  no recorded hash. The subagent could technically read the project folder, enc1.py included; that it did not is
  the author's statement and is not proved by a log. What a reader can check instead: the two files share no code
  (different variable order, domination stated on neighbourhoods against line indicators, a separate chain Q against
  the size counter for symmetry breaking, a totalizer against a sequential counter for the counting constraint).
- Everything after the encoders is shared and was written by the main session: the lists, the lemma statements, the
  stage programs, counting.py, audit_chain.py, faithful.py, formula_audit.py. Written by other fresh contexts:
  code/second-audit/ (the second composition check; its author had not seen audit_chain.py).
