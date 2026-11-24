# Design of the certificate pipeline (excerpt of the workspace's certify/README.md: tools, job pipeline, cover, trusted items; status and validation-result paragraphs removed)

## Tools (built from source, inside the workspace; human permission D-022, recorded D-023)
| tool | source | commit | build |
|---|---|---|---|
| drat-trim (DRAT -> LRAT) | github.com/marijnheule/drat-trim, shallow clone in `logs/certify-tools/drat-trim` | `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` (2024-11-25) | `cc drat-trim.c -std=c99 -O2` (Apple clang 21, arm64) |
| cake_lpr (verified LRAT/LPR checker, CakeML) | github.com/tanyongkiam/cake_lpr, shallow clone in `logs/certify-tools/cake_lpr` | `a36874a8b750b43fe4b385b8ddbf5b033e46a3fa` (2026-07-22) | `cc -O2 basis_ffi.c cake_lpr_arm8.S -std=c99` (the repo's own `make cake_lpr_arm8` recipe; native arm64, no Rosetta) |
| CaDiCaL 1.9.5 | pysat 1.9.dev17 `cadical195` in `venv-schutte` (the venv runs 0745-1144 used) | - | already installed |

Source read before building (rule 11): drat-trim.c opens files only at paths given on its command line (`-L`, `-c`, `-l`, `-a`, `-r`)
and deletes the proof only with `-D` (not used); no network, no subprocess. cake_lpr: `basis_ffi.c` (C wrapper) has no network,
subprocess or exec; its file FFI opens paths chosen by the checker; the arm8 assembly calls out only through the FFI stubs
get_arg*, open_in, read, write, close, exit (no open_out), and its 408,808 code bytes contain no aligned `svc` instruction.
sha256: `cake_lpr_arm8.S` 95b64883...f00c and `cake_lpr.S` 2f3af32d...b72d4a match the repo's `cake_lpr.sha256`; `basis_ffi.c`
(8e30d84f...87cb) does not match the hash listed there (3fbd8f31...): the 2026-07-22 commit changed the wrapper (heap/stack flags)
without updating that file. The wrapper is outside the verified part in any case (it is the trusted C shim).
The CakeML proof of cake_lpr (HOL4 0ae70303..., CakeML fb377b4b..., per its README) covers the checker down to arm8 machine code
inside the CakeML compiler's correctness theorem; we did not rebuild it from HOL4.

## What one job does (`driver.py`, `solve.py`)
`solve.py` builds the job's CNF (leaf: the unchanged v2 encoder `encoder/cube.py`, `encoder/cube3.py`, byte-identical to
`runs/2026-10-27-1144/attempts/solver/code`, sha256 checked at every start; cover lemma: `certlib.cover_cnf`), writes `f.cnf`,
and solves with CaDiCaL 1.9.5 writing binary DRAT straight to `proof.drat` (pysat's trace file is given a name; nothing in memory).
Then `drat-trim f.cnf proof.drat -i -w -L proof.lrat`, then `cake_lpr f.cnf proof.lrat`. Verdict VERIFIED only if cake_lpr exits 0
and its whole stdout is the line `s VERIFIED UNSAT`, and `f.cnf` still has the sha256 recorded at solve time. One ledger row
(`ledger.tsv`: job, attempt, verdict, CNF sha256, vars, clauses, DRAT sha256 and bytes, LRAT bytes, solve/convert/check seconds,
peak RSS, note) is appended, and the proof, LRAT and CNF are deleted. Work files live in `logs/certify-work/` (git-ignored).

## What the certificate covers
Tree: exactly the cover of runs 0844/1144 as reconstructed from their ledgers (`certlib.tree`, same logic as run 1144's audit.py);
all leaves are re-solved as **v2** cubes (stronger than the v1 cubes some rows used; still a cover, PREREG.v2 of run 0844).
- (3,6,12): 126 level-1 leaves (d,a,b), 114 level-2 leaves (d,a,b,c), 2,569 level-3 leaves (d,a,b,c,(e,a',b')); 1 + 21 + 40 cover lemmas.
- (2,5,13): the 196 level-1 cubes of run 0844 (193 were solver-UNSAT there; 6_0_0, 6_1_0, 6_0_2 were closed only by counting and run
  last as tier `hard`, one attempt with a 2 h cap) and 1 cover lemma.
- Total 3,068 jobs (`jobs.tsv`).

**Leaf**: CNF = Definition 2.2 clauses + the cube's constraints, exactly as the encoder emits them (sha256 in the ledger).

**Cover lemma** (one per refined node: the root of each cell, every refined level-1 cube, every refined level-2 sub-cube).
Each child CNF is checked (Python asserts in `certlib.cover_cnf`, run for all 63 nodes in validation step 1) to be the parent CNF
followed by unit clauses L_j on arc variables and non-unit clauses R_j that are *exactly* the encoder's seqcounter at-most constraints
(regenerated with the same arguments and compared clause by clause). The lemma CNF is:
parent CNF without the Definition 2.2 clauses (for a root: nothing) + normal-form clauses NF + exact unary counters
(`certlib.counter`) + one clause per child, `(not L_j) or (some R_j row has count >= bound+1)`. UNSAT means: every assignment that
satisfies the parent's degree/row constraints and NF satisfies L_j and the meaning of R_j for some child j, so it extends to a model of
that child CNF. With all children UNSAT, the parent has no model satisfying NF.
- NF level 1 (root): (T_1, vertex 0) has the largest out-degree of all m*n rows; T_1 row of 0 is the prefix 1..d; T_2 row of 0 is a
  prefix inside A = {1..d} and inside B = {d+1..}; for m=3 (v2) the T_3 row of 0 is no larger than the T_2 row. The lemma itself
  derives d >= ceil((n-1)/2) and a+b <= d (no counting fact is assumed).
- NF level 2 (cube (d,a,b)): the T_3 row of 0 is a prefix inside each of the four blocks. Children: sum(c) <= a+b (v2).
- NF level 3 (sub-cube): in the largest cell C (first vertex s), s has the largest T_1 out-degree inside C, s's T_1 row inside C is a
  prefix, and its T_2 row is a prefix inside A' and inside B'. The lemma derives e >= floor(z/2).

## What stays trusted (not checked by cake_lpr)
1. The encoder's correctness w.r.t. Definition 2.2 (`encoder/cube.py` `build`, SOUNDNESS_NOTE.md of run 0844): satisfiable iff an
   S_k set exists. The CNF sha256 values tie each checked CNF to this encoder.
2. The normal forms are without loss of generality: the relabelling arguments of SOUNDNESS_NOTE.md (run 0844, level 1),
   PREREG.v2.md (run 0844, tournament order T_2/T_3), PREREG.md (run 0844, level 2) and SOUNDNESS_L3.md (run 1144, level 3), i.e.
   Definition 2.2 is invariant under vertex permutations and tournament permutations, and those permutations reach NF.
   `validate.py` step 3 tests level 1 on random tuples (not a proof).
3. The cover-lemma CNF expresses the statement above: `certlib.cover_cnf` (Python, about 150 lines), the exhaustive tests of
   `test_encodings.py` (the counters' honest assignment satisfies every clause and ge(k) is exact for up to 12 inputs; pysat's seqcounter
   at-most is satisfiable iff count <= bound for up to 12 inputs, every bound), and the structural asserts above.
4. The tree is complete: `certlib.tree` / `assemble.py` enumerate children with the same ranges as the original drivers and audit.py.
5. cake_lpr's C wrapper `basis_ffi.c`, the assembler/linker (Apple clang), the OS, and the driver's reading of cake_lpr's stdout.
Not trusted: CaDiCaL, pysat's solver, drat-trim (any error there makes cake_lpr reject, never accept).
