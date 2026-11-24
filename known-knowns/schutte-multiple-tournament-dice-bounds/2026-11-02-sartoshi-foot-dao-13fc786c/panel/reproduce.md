Reviewer: REPRODUCE skeptic, addendum (Claude Opus 5.5, general-purpose subagent)
context: subagent (fresh context; read kit rule 3, RUN.md steps 6-7, claim/, B/reproduce.md and the re-run files only)

# Claim B: f(3,6) = 13. Audit of the full re-run of the (3,6,12) certificate

The earlier report (B/reproduce.md) found no mismatch but failed because only 17 of the 2,871 jobs were re-run. This
addendum audits the claimant session's later full re-run: `rerun_one.sh`, `rerun_cell.sh`, `rerun/m3k6n12/results.tsv`,
`rerun/m3k6n12.log` (paths relative to the thread folder; claim files are relative to `claim/`). Scratch work went in a
temporary folder under `panel/B/`, deleted at the end. All Python ran with `-I -B`, all jobs at `nice -n 19`.

## 1. The scripts, read line by line
`rerun_one.sh <job> <scratch>`: looks up the job's ledger row; makes a new `mktemp -d` folder and works inside it;
`solve.py` builds the job's CNF from the encoder and writes `f.cnf` and a new `proof.drat` there (CaDiCaL via pysat;
the proof file is opened fresh by `open(proof, 'w+b')`); drat-trim turns that proof into `proof.lrat` in the same folder;
cake_lpr checks `f.cnf` against that `proof.lrat`, and the script keeps only the **last stdout/stderr line**. Result is
PASS only if that line is exactly `s VERIFIED UNSAT` **and** the sha256 of the freshly written `f.cnf` equals ledger
column 5. The folder is deleted after each job. No step reads a proof, CNF or result from earlier runs; every file is
produced by this job in a new empty folder, so there are no stale or reused proofs, and the exit code is never used.
The DRAT-sha and LRAT-bytes columns are reported but do not gate PASS (that is fine, they are extra).
`rerun_cell.sh <cell>`: the job list is every `jobs.tsv` row starting with `m3k6n12/`; jobs already in results.tsv are
skipped (resume); 3 in parallel at nice 19; each job appends one short printf line (atomic append). The log shows one pass
with no resume: `start 2026-10-30T14:51:02Z todo 2871 of 2871` / `end 2026-10-30T23:17:06Z results 2871 pass 2871`.

The scripts ran from the workspace root, i.e. against the workspace's `certify/` and tools, not the `claim/` copy. I
checked: `certlib.py`, `solve.py`, `mkjobs.py`, `jobs.tsv`, `ledger.tsv`, `encoder/cube.py`, `cube3.py`, `checker.py` have the
same sha256 in both places, and their modification times (2026-10-27/28) are before the re-run started. `certlib`
checks the encoder hashes itself at start.

cake_lpr: I rebuilt it myself from the local clone (commit a36874a8, `git status` clean apart from the built binary;
`cake_lpr_arm8.S` sha256 95b64883...f00c matches the repo's `cake_lpr.sha256`) with
`cc -O2 basis_ffi.c cake_lpr_arm8.S -std=c99`. My binary is **byte-identical** to the one the re-run used
(sha256 dee0798c...6d2d), and prints `s VERIFIED UNSAT` on the repo's example.

## 2. Coverage
Script (own, using only certlib's child functions `l1_cubes`, `l2_children`, `l3_children`, which the earlier report
checked against its own enumeration): starting from COVER1, every level-1 cube must be in results.tsv as exactly one of
leaf or COVER2; every child of a COVER2 as exactly one of leaf or COVER3; every child of a COVER3 as a leaf.

    rows 2871, all with 7 columns; duplicates 0
    result column: PASS 2871; cake_lpr column: "s VERIFIED UNSAT" 2871; (cnf, drat, lrat) match columns: (1,1,1) 2871
    closure problems 0; needed set 2871; extra 0; missing 0
    by kind: COVER1 1, COVER2 21, COVER3 40, level-1 leaves 126, level-2 leaves 114, level-3 leaves 2569
    certlib.tree(claim/) set == results.tsv set: True; jobs.tsv m3k6n12 set == results.tsv set: True
    ledger: exactly one VERIFIED row per job: True

The counts agree with the earlier report's own tree enumeration (147 level-1 cubes = 126 + 21, 114 + 40, 2,569).
Timing check: summed wall in results.tsv 90,390 s (ledger total 96,504 CPU-s); over 3 parallel slots that is about
30,130 s, against 30,364 s between the logged start and end. No job with a ledger solve over 100 s finished in under 30%
of its ledger time. Largest wall 1,509 s (7_0_2_0-0-0-2; ledger largest solve 1,412 s).

## 3. Spot check of results.tsv honesty (seed 20261030)
Selection (`random.Random(20261030)`, pools sorted by job id, excluding the 17 jobs the earlier report ran): 7 from leaves
with ledger solve <= 100 s, 1 from cover lemmas, 2 from jobs with ledger solve > 100 s and ledger total <= 450 s (50
such jobs; the cap kept the budget). Each run end to end with my own script: `claim/venv-schutte/bin/python -I -B
claim/certify/solve.py <job> <dir>`, `drat-trim <dir>/f.cnf <dir>/proof.drat -i -w -L <dir>/proof.lrat`, then **my rebuilt**
`cake_lpr --CML_HEAP_SIZE=4500 --CML_STACK_SIZE=1000 <dir>/f.cnf <dir>/proof.lrat`, reading stdout; sha256 of f.cnf and
proof.drat and LRAT bytes computed by me and compared with the ledger (and so with results.tsv, whose rows for these jobs
all read PASS / s VERIFIED UNSAT / 1 / 1 / 1).

    job                                     ledger solve s  my result (cake stdout, one line)  cnf  drat  lrat  wall
    m3k6n12/9_1_1_0-0-0-1_L3_4_2_1          3.68            s VERIFIED UNSAT                    =    =     =      6
    m3k6n12/8_0_1_0-0-1-0_L3_6_5_0          0.74            s VERIFIED UNSAT                    =    =     =      1
    m3k6n12/9_1_1_0-0-1-0_L3_4_2_2          1.86            s VERIFIED UNSAT                    =    =     =      4
    m3k6n12/8_1_0_0-1-0-0_L3_3_1_0          34.6            s VERIFIED UNSAT                    =    =     =     65
    m3k6n12/8_1_2_0-0-0-1_L3_3_3_1          2.34            s VERIFIED UNSAT                    =    =     =      5
    m3k6n12/10_0_1_0-0-0-0_L3_6_4_3         0.33            s VERIFIED UNSAT                    =    =     =      1
    m3k6n12/9_0_2_0-0-0-0_L3_5_5_2          0.26            s VERIFIED UNSAT                    =    =     =      0
    m3k6n12/COVER3/8_1_1_0-0-1-0            0.0             s VERIFIED UNSAT                    =    =     =      2
    m3k6n12/7_0_1_0-0-0-1                   110.54          s VERIFIED UNSAT                    =    =     =    193
    m3k6n12/8_2_0                           245.1           s VERIFIED UNSAT                    =    =     =    298
    10/10 agree with results.tsv and the ledger (CNF sha256, DRAT sha256 and LRAT size identical: deterministic)

About 575 s wall, 2 at a time.

## 4. Negative controls
- Wrong proof (the LRAT of 9_0_2_0-0-0-0_L3_5_5_2 against the CNF of 10_0_1_0-0-0-0_L3_6_4_3): cake_lpr prints
  `c Checking failed at line: 1. Reason: clause index unavailable: 101847`, exit code 0.
- CNF with its last unit clause removed (header count fixed), right proof: `c Checking failed at line: 1. Reason: clause not
  empty or singleton after reduct`, exit 0. Its sha256 (d359e5c7...) also differs from the ledger.
- Truncated LRAT: `c empty clause not derived at end of proof`.
- `rerun_one.sh` itself, run unchanged against a copy of `certify/` whose ledger had the CNF hash of
  10_0_1_0-0-0-0_L3_6_4_3 altered in its first byte: `FAIL  s VERIFIED UNSAT  0 1 1 1` (rejected on the hash); an unaltered
  job in the same copy: `PASS ... 1 1 1 1`; a job id not in the ledger: `FAIL  no ledger row`.
So both the cake_lpr line and the CNF-hash comparison really gate PASS, and exit code 0 is not mistaken for acceptance.

## 5. What I did not check
- I re-ran 10 jobs myself (27 counting the earlier report). For the other jobs I rely on results.tsv as the re-run's own
  record, audited above (script logic, coverage, timing, seeded agreement). I cannot rule out that the file was edited
  afterwards, but nothing points to that: 27 of 27 independent re-runs agree with it, and its timing fits the log.
- Correctness of the CNFs' meaning (encoder vs Definition 2.2, cover lemmas, relabelling lemmas L1/L2/L3/v2): not re-done
  here; covered in B/reproduce.md sections 2-4.
- Trusted: the CakeML proof of cake_lpr, `basis_ffi.c`, the C compiler, the OS. drat-trim and CaDiCaL need no trust.
- The witness on 13 vertices: checked in B/reproduce.md section 2 (undominated 0).

## Verdict
The full re-run checked every one of the 2,871 jobs the certificate needs (exactly that set, no duplicates, all PASS). The
scripts PASS only on a fresh CNF whose hash matches the ledger and a fresh proof accepted by cake_lpr's stdout line. My
seeded re-run of 10 jobs (two over 100 s solve) agrees exactly, my rebuilt cake_lpr is byte-identical to the one used,
and the negative controls are rejected. Together with B/reproduce.md this reproduces the whole certificate with no mismatch.
pass: true
