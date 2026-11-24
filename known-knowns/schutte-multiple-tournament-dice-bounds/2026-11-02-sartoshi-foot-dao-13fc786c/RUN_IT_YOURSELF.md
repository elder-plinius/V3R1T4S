# Run it yourself

All commands run from this folder, in a fresh shell.

## The whole check

    sh verify-it-yourself/run_checks.sh

Last line `PASS`. Steps: 0. object files match SHA256SUMS; 1. object/witness_m3k6n13.json is three tournaments on 13
vertices with S_6 (verify-it-yourself/check_witness.py, written from Definition 2.1, standard library); 2. a temporary venv
with python-sat 1.9.dev17; 3. verify-it-yourself/check_cert.py: encoder files unchanged, job list = cover tree, 40 seeded
formulas rebuilt with matching sha256 and sizes; 4. drat-trim and cake_lpr built at pinned commits; 5. 6 jobs re-proved.
Set CHECK_PYTHON, DRAT_TRIM and CAKE_LPR to reuse tools you already have. FULL=1 rebuilds and re-proves all 2,871 jobs.

## One job by hand

    python -I how-we-built-it/certify/solve.py <job> <dir>     # writes <dir>/f.cnf and <dir>/proof.drat; prints result and cnf_sha256
    drat-trim <dir>/f.cnf <dir>/proof.drat -i -w -L <dir>/proof.lrat
    cake_lpr --CML_HEAP_SIZE=4500 --CML_STACK_SIZE=1000 <dir>/f.cnf <dir>/proof.lrat

Success is the exact output line `s VERIFIED UNSAT`: cake_lpr can exit 0 while rejecting a proof, so read the line, not
the exit code. Compare the formula's sha256 with column cnf_sha256 of the job's row in object/certificate_m3k6n12.tsv, and
the DRAT proof's sha256 with column drat_sha256. Job ids are column 1. Delete the proofs after each job (LRAT up to 2 GB).

## Rebuild the object

object/certificate_m3k6n12.tsv is the (3,6,12) part of the certification ledger (how-we-built-it/certify/driver.py ran
every job of `how-we-built-it/certify/mkjobs.py`'s list three at a time, 2026-10-28) plus the result of the second full
run (how-we-built-it/rerun/, 2026-10-30). object/witness_m3k6n13.json comes from the solver run that found it (SAT for the
13-vertex cube d11a7b0); any S_6 triple on 13 vertices will do, and Proposition 2.3 gives one too.

Pinned versions: python-sat 1.9.dev17 (CaDiCaL 1.9.5 as `cadical195`), drat-trim 2e3b2dc0ecf938addbd779d42877b6ed69d9a985,
cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (build `cc -O2 basis_ffi.c cake_lpr_arm8.S`, or cake_lpr.S on x86-64).
