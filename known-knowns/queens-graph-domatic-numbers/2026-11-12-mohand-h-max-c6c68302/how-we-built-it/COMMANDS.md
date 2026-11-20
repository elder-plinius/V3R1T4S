# Commands (Windows 11; six processes at a time for the chain, one thread for each final step)

Requirements: Python 3 with python-sat 1.9.dev22 (CaDiCaL 1.5.3 as "cadical153"), and drat-trim built from the
unmodified upstream source (checker/PROVENANCE.md gives the two compile commands, the one extra file binmode.c that
sets binary file mode on Windows, and the size limit of these builds).

    python run_pool.py 6 11 dom 20 7 CHAIN DT . pids.txt enc1:0-19,enc2:0-19 lists/e2-Q11-m5.txt lists/e2-Q11-m6-minimal.txt
    python stage_b2.py enc1 11 dom 20 7 FINAL-enc1 DT lists/e2-Q11-m5.txt lists/e2-Q11-m6-minimal.txt
    python stage_b2.py enc2 11 dom 20 7 FINAL-enc2 DT lists/e2-Q11-m5.txt lists/e2-Q11-m6-minimal.txt

The lists must be given in this order (two dominating 5-sets, then 432 minimal dominating 6-sets of Q_11): another
order renumbers variables. The lists only serve to state lemmas; that they are complete is proved by the solver
inside the chain, not assumed. lists/dom-Q11-19-partition.txt is our own 19-partition (cross-check on the
satisfiable side, crosscheck_base.py); the published 18-partition used for the same purpose is Figure 2(c) of the
Corrigendum and is not copied here.
What each program is: enc1.py, enc2.py the two encoders; stage_l12.py, stage_a4.py the class lemmas (34 refutations
per class); counting.py the derivation of the counting bound inside the final proof; stage_b2.py the final step;
audit_chain.py and second_audit.py two independent checks of how the chain composes; formula_audit.py what the base
formula consists of; write_fbase.py writes a base formula in a few seconds (the same file stage_b2.py writes before
its long step); regen_formulas.py rebuilds every chain formula without a solver; recheck_all.py runs the checker
again on every saved proof; faithful.py tests the formulas against the definition; test_counting.py, probe_core.py
and audit_negative.py are controls; no_comment_lines.py checks that no formula file has a comment line after its
header (drat-trim can misread such a file). prereg/ holds the three pre-registration files.
checker2/DratCheck.cs is the source of the second proof checker (C# 5; build: csc.exe /nologo /optimize+
/out:dratcheck.exe DratCheck.cs). In its third line, a comment, two local folder paths were shortened to the bare
file names; nothing else differs from the file that was compiled. The three text files next to it are the records of
its pass over the 2 x 680 saved proofs of the chain (flag --binary, its exact deletion mode, no cap). The four files
second-checker-final-*.txt are the records of its runs on the two proofs of the final step (2026-11-12, 03:13:58Z to
04:41Z, both deletion modes, --timeout 5200): all four end with `s TIMEOUT`, which is not a verdict. These runs
started after panel/gate.md was written; the gate file has a dated note about them.
checker/PROVENANCE.md is the provenance note of the checker as kept in the working folder, except its first line,
where a quotation of the human's chat messages was dropped. It names files that are not shipped (src/drat-trim.c,
to be fetched from upstream at the commit given in RUN_IT_YOURSELF.md; bin/, the self-test outputs, a Python virtual
environment); binmode.c is next to it here. REPRODUCE-from-the-saved-files.md is the instruction file the panel
used, unchanged: its commands use the layout of the authors' claim folder (code/, formulas/, chain/, checker/bin/,
partitions/, manifests/, final/), not the layout of this package, and its estimate "about 28 GB per encoding" for a
single proof file was computed for the first encoding (the second is larger).
