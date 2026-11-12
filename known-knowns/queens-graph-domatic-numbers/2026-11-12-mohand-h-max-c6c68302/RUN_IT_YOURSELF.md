# Run it yourself

## The quick check (under a minute, no solver, no proof checker)

From this folder, in a fresh shell with Python 3 (standard library only):

    sh verify-it-yourself/run_checks.sh

Expected output ends with `PASS`. It checks the sha256 of object/certificate.txt (c6c683024171c1fc2a95a3f8699d1d353f358c603c555fcd743941f15b67e13d) and of the two manifests,
rebuilds the two base formulas and all 2 x 680 formulas of the chain from the generators in how-we-built-it/, and
compares every sha256 with the certificate and the manifests. It does not run any solver or proof checker, and the
hash written in run_checks.sh only guards the package against accidental change.

To see what a base formula consists of, clause family by clause family, without trusting the generator (a few
seconds each, standard library only), from the folder how-we-built-it/:

    python write_fbase.py enc1 11 dom 20 7 Fbase-enc1.cnf lists/e2-Q11-m5.txt lists/e2-Q11-m6-minimal.txt
    python dump_varmap.py enc1 11 dom 20 7 varmap-enc1.json lists/e2-Q11-m5.txt lists/e2-Q11-m6-minimal.txt
    python -I formula_audit.py varmap-enc1.json Fbase-enc1.cnf

The first command writes the base formula and prints its sha256 (compare with the line "enc1 Fbase.cnf" of
object/certificate.txt); the second only names the variables; the third imports no generator. Same with enc2.
Expected last line: FORMULA AUDIT enc1: PASS, the file is exactly these families and nothing else

## The full check (hours)

Needs Python 3 with the package python-sat (we used 1.9.dev22; solver name cadical153) and drat-trim built from its
unmodified source (https://github.com/marijnheule/drat-trim, commit 2e3b2dc0ecf938addbd779d42877b6ed69d9a985,
drat-trim.c sha256 d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee; on Windows see
how-we-built-it/checker/PROVENANCE.md, the proofs are in drat-trim's binary format). With DT the path of that
drat-trim, from the folder how-we-built-it/:

    python run_pool.py 6 11 dom 20 7 CHAIN DT . pids.txt enc1:0-19,enc2:0-19 lists/e2-Q11-m5.txt lists/e2-Q11-m6-minimal.txt
    python chain_summary.py CHAIN enc1 20 manifest-enc1.txt        (and enc2)
    python stage_b2.py enc1 11 dom 20 7 FINAL-enc1 DT lists/e2-Q11-m5.txt lists/e2-Q11-m6-minimal.txt      (and enc2)
    python audit_chain.py FINAL-enc1/Fbase.cnf FINAL-enc1/Fbase-lemmas.cnf CHAIN enc1 20 --hash-proofs   (and enc2)

CHAIN is a new empty folder for the proofs (about 80 GB). run_pool.py solves and checks the 2 x 680 refutations
(about 14 and 17 minutes of one core per class for the two encodings, six classes at a time here, 1.7 to 2.3 GB of
disk per class); stage_b2.py writes the base formula, derives
the counting bound, refutes and checks the final step (about 95 to 120 minutes each); audit_chain.py checks how the
chain composes. The formula files must have the sha256 listed in object/; on our machine the solver is deterministic
(one class was produced twice with byte-identical proofs), but proofs made by another build may differ and are still
proofs if drat-trim accepts them. The commands we used to re-check everything from saved files are in
how-we-built-it/REPRODUCE-from-the-saved-files.md.
