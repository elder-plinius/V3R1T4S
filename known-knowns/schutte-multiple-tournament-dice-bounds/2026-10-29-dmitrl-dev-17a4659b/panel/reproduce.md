# REPRODUCE panel: schutte-multiple-tournament-dice-bounds, claim 2026-10-28-1153 (partial win p1)

context: subagent (fresh context, Claude Science delegation)

- role: REPRODUCE (bank kit RUN.md step 6)
- claim: no S_5 set of two tournaments on 13 vertices exists (CNF + LRAT certificate checked by cake_lpr), hence
  f(2,5) >= 14; with the published 14-vertex composition, f(2,5) = 14 (partial win p1)
- reviewer machine: macOS arm64 laptop, 8 GB RAM, 6 cores; Python 3.11.17; Apple clang 21.0.0; 2026-10-28 (UTC)
- verdict: every property and the claimed value reproduced. I found no mismatch, no missing object and no
  non-determinism. pass: true (last line)

## 0. Outside context and sources

My context contained memory notes that were recalled automatically from the requesting user's earlier sessions:
working conventions, machine limits, and earlier V3R1T4S panels on other claims. None of them concerned this claim,
and I did not use them as evidence. Apart from the claim folder I used only public sources:
arXiv:2604.08790 (abs page and PDF), the CaDiCaL and cake_lpr GitHub repositories at the pinned commits (read-only
clones), and one web search for later results on f(2,5). I saw nothing from the claimant beyond the folder.

## 1. Instructions checked against (verbatim)

- RUN.md step 6: "Before reading the author's code, write your own checker from the definition (quote it). Verify
  every property and the claimed value from the saved files; re-derive every proof step. For an exhaustive search, a
  sample is a spot check and cannot pass. Fail on any mismatch, missing object or non-determinism."
- Bank verification method: "Check each matrix has diagonal zero, entries in {0,1}, and A[i,j]+A[j,i]=1 for i!=j.
  For every k-subset U, check that some single tournament and vertex v outside U have A[v,u]=1 for every u in U. At
  most C(13,5)=1287 subsets are needed for the proposed witnesses. Regenerate the best composition bar from published
  ingredients using Proposition 2.3 and compare exact integer orders. For a submitted composition, also check its
  ingredients and assembly rule; direct checking of the final matrices remains required. A positive SAT search is
  certified by the matrices independently of the solver. For p1, re-encode the CNF independently from Definition 2.2
  (or check the claimant's encoder line by line against it), check every symmetry-breaking clause against its
  soundness argument, and run the verified checker on the proof."

## 2. Definitions (arXiv:2604.08790 v1, read by me)

I fetched the PDF myself: HTTP 200, 393509 bytes, sha256 6aca2fdf8285dabf47dbc7b83fd6232e31fe0e11bb02cb163f9dba05be97a8e8.
The abs page: HTTP 200, 39949 bytes, sha256 0b2c17af0cb7342b68eecf9951a3f011cbf28e31fdb41b3c086f9b58cfd9e3c0, with
only v1 (9 Apr 2026) in the submission history. All three values equal the-record-we-beat/RECORD.md.

- Section 1: "a vertex v dominates a set of vertices if v is directed towards every vertex in the set."
- Definition 2.1: "Let τ = {T_1, ..., T_m} be a set of m labeled tournaments each on the same vertex set V(τ). The set
  τ has Schütte's property S_k if for every set of k vertices U ⊂ V(τ), there is a tournament T_i ∈ τ and a vertex
  u ∈ V(τ) such that u → U in T_i."
- Definition 2.2: "For m, k ∈ N, define f(m, k) to be the minimum size of a vertex set V such that there is an S_k
  set of m tournaments on V."
- Proposition 2.3: "If there exists an S_k1 m1-set of order n1 and an S_k2 m2-set of order n2, then there exists an
  S_(k1+k2+1) (m1 + m2)-set of order n1 + n2." In the construction, T'(1,i) restricted to V1 is T(1,i) and V1 → V2;
  T'(2,j) restricted to V2 is T(2,j) and V2 → V1; the other edges are arbitrary.
- Convention used for orders ≤ k. Proof of Proposition 2.2: "if τ is a set of tournaments such that |V(τ)| ≤ k,
  then τ is not S_k". The bank uses n ≥ k+1 as well.
- Figure 7, row k = 5, columns m = 1..5: `331 14 9* 8* 7*`. The m = 2 cell is 14 and carries no star.

## 3. Own checker, written before reading any claimant code (Appendix A)

### 3.1 The 14-vertex object (object/upper_bound_m2k5n14.json)
My checker tests every entry in {0,1}, zero diagonal and A[i][j]+A[j][i] = 1 for i ≠ j. It then tests every
k-subset U exhaustively for some tournament t and some vertex v ∉ U with A_t[v][u] = 1 for all u ∈ U. Output:

```
m=2 k=5 n=14, 2 tournaments in file
tournament 0: valid tournament matrix
tournament 1: valid tournament matrix
tournaments pairwise distinct: True
2002 k-subsets checked exhaustively, 0 undominated []
RESULT: PASS
```

Negative controls for the checker: deleting any one of the 14 vertices leaves 84 undominated 5-subsets (all 14
deletions), and flipping arc (0,1) of T_0 leaves 56.

### 3.2 Composition bar and the object's ingredients (Proposition 2.3)
- Ingredient: the Paley tournament P7 (residues {1,2,4} mod 7). It is S_2 (21 of 21 2-sets dominated) and not S_3
  (28 of 35 3-sets undominated). f(2) = 7 is starred in Figure 7.
- I composed two copies of P7 by Proposition 2.3 and filled the arbitrary edges transitively (i → j for i < j). The
  result is S_5 on 14 vertices (2002 subsets, 0 undominated) and equals the submitted object matrix for matrix.
- Assembly rule checked on the object: T_0[{0..6}] = P7 and {0..6} → {7..13} in T_0; T_1[{7..13}] = P7 and
  {7..13} → {0..6} in T_1. Both restrictions are S_2.
- Bar for f(2,5): the minimum of f(k1) + f(k2) over k1 + k2 = 4, with published f(0..4) = 1, 3, 7, 19, ≤67. The
  candidates are {68, 22, 14, 22, 68}, so the bar is 14, which equals the bank's stated bar. (The f(3,6) bar from
  f(1,k1) + f(2,k2), k1 + k2 = 5, comes out at 13, also the bank's value.)
- The submitted 14-vertex object is itself this composition. It is used only for the upper bound; the claim does not
  attempt the main win (an order below 14) and claims p1 (exact value).

### 3.3 Lower-bound step (re-derived)
Suppose an S_5 2-set of order n with 6 ≤ n ≤ 12 existed. Add a vertex w that loses to every vertex in both
tournaments. A 5-set without w keeps its dominator. For a 5-set U containing w, extend U − {w} by an old vertex
outside it; this is possible because n − 4 ≥ 2. The resulting 5-set of old vertices has a dominator v, which is old
and lies outside that set, so v ∉ U, v beats U − {w}, and v beats w. Repeating this gives an S_5 2-set of order 13.
Orders ≤ 5 are excluded by the paper's convention (Section 2). So UNSAT at order 13 gives f(2,5) ≥ 14, and with
3.1 f(2,5) = 14. The argument matches how-we-built-it/SOUNDNESS.md section 4.

## 4. Independent re-encoding and comparison with the shipped CNF

### 4.1 My encodings (Appendix A; written before reading verify-it-yourself/encode_schutte.py)
- Base encoding from Definition 2.1:
  - edge variables x(t,a,b) for a < b, t = 0,1, true iff a → b. Every assignment is a pair of tournaments.
  - d(t,v,U) for each 5-set U and each v ∉ U, with the clauses (¬d ∨ arc(t,v,u)) for u ∈ U.
  - one coverage clause OR d(t,v,U) per U.
  - Size: 20748 variables (156 edge variables) and 104247 clauses.
  - Soundness of UNSAT: from any S_5 pair, setting d := [v → U in T_t] satisfies every clause.
- Symmetry-breaking clauses implemented from the text of how-we-built-it/SOUNDNESS.md section 2:
  - Sinz counters with fresh registers s[i][j], i = 1..N−1, j = 1..D. Only the overflow clauses carry the extra
    literals.
  - Total: 42644 variables and 148931 clauses. Groups: (a) 11, (c) 5, (b) 32578, (n) 12026, (l) 64, (s) 0. These
    44684 added clauses equal the "44684 added clauses" that verify-it-yourself/cnf_audit.py reports.
  - sha256 of my file: 007dca92f7a796529aeb0522ac7bc35831390c483e16752b5e19cc3b7618fac1.

### 4.2 The shipped CNF
- `python3 verify-it-yourself/encode_schutte.py 2 5 13 --sb global3` gives header `p cnf 42644 148931` and sha256
  247ca74489c8144e2eca1fa1b7bfdd6c2f7f826e7deac2c46e4b3748c7069626. This equals object/cnf_spec.json.
- The output is the same under PYTHONHASHSEED = 0, 1 and 12345.
- The sha256 of object/cnf_spec.json is 17a4659b7971dd161f3d572e2871ef5f5eec1d0e7cdd4bf6f4a8a87e79b7c3e6, which
  equals INDEX.csv.
- how-we-built-it/encode_schutte.py is byte-identical to verify-it-yourself/encode_schutte.py.

### 4.3 Comparison (my CNF vs the shipped CNF)
- Numbering-independent check. I ran exact colour refinement (1-WL) on the clause/variable incidence graphs of both
  CNFs together. Edge variables 1..156 were fixed and every auxiliary variable started with the same colour.
  - It stabilised after 21 iterations with 42644 singleton classes in each CNF.
  - Under the induced bijection the clause multisets are identical, with 0 duplicate clauses.
  - Controls: flipping the sign of one literal in a symmetry-breaking clause (clause index 148928) or in a base
    clause (index 102) is detected. My base CNF without symmetry breaking is reported as different.
- Direct check. The two numberings turned out to be the same. All 148931 clauses agree position by position as
  literal sets. Only 14 clauses differ as text: the nested (n) clauses, where I put the guard literal ¬lit(0,0,12)
  first and the shipped encoder puts it last (clause index 136841: shipped `-92 91 -12`, mine `-12 -92 91`).

### 4.4 Claimant encoder read line by line (after 4.1–4.3)
- In verify-it-yourself/encode_schutte.py, `build(..., "global3")` calls "global2", which calls "global". The base
  encoding is exactly Definition 2.1 (one-directional d variables).
- "global" adds:
  - (a) for u = 1..n−2;
  - (c) units for u = 1..k;
  - (b) `at_most` for D = k..n−2 over all (t,v), with cond = [¬lit(0,0,D), lit(0,0,D+1)].
- "global2" adds, for m ≥ 2 and n−1 ≥ k, with guard ¬lit(0,0,n−1):
  - the order clauses for vertex 1 of T_1 (u = 2..n−2);
  - units for u = 2..k;
  - counters for D' = k−1..n−3, t ≥ 1 and v ∈ {1..n−1}, with the extra literals [¬lit(1,1,D'+1), lit(1,1,D'+2)].
- "global3" adds (l) for D = k..n−2, w = D+1, u ∈ 1..D−1 and u ∈ D+2..n−2, each with cond. It adds (s) only for
  m ≥ 3.
- `at_most` is a standard Sinz counter with fresh registers. The cases K ≥ n and K = 0 never occur here
  (4 ≤ K ≤ 11 < N).
- This matches SOUNDNESS.md and my implementation. The other variants (dom0, maxdeg, gsort) are not used by the
  certificate.

## 5. Every symmetry-breaking clause checked against its soundness argument (re-derived)

Notation: d = out-degree of vertex 0 in T_0; lit(t,v,u) = "v beats u in T_t"; cond(D) = [¬lit(0,0,D), lit(0,0,D+1)].

- Lemma S (counters).
  - Statement: for any edge assignment, setting every register s[i][j] := [at least j of the first i inputs are
    true] satisfies all register clauses. The overflow clause for input i then fails only if input i is true, at
    least D earlier inputs are true and every extra literal is false. So with all extras false, the counter means
    "at most D".
  - Check of the clause forms: (¬x1 ∨ s11) holds. (¬s1j) for j ≥ 2 holds because one input cannot reach count 2.
    (¬xi ∨ si1), (¬s(i−1)1 ∨ si1), (¬xi ∨ ¬s(i−1)(j−1) ∨ sij) and (¬s(i−1)j ∨ sij) hold because the counts are
    exact and monotone.
  - Registers are fresh per counter: 20748 + 26·11·56 + 12·10·49 = 42644. Here 26 (t,v) pairs × 11 × (5+…+11), and
    12 vertices × 10 × (4+…+10).
- Lemma C. Under (a), lit(0,0,u) holds iff u ≤ d. So cond(D) is all-false iff D = d.
- Step 1 (any S_5 pair). Choose (t*, v*) with the maximum out-degree D* over both tournaments.
  - Some vertex dominates some 5-set, so D* ≥ 5.
  - Relabel: t* becomes T_0, v* becomes vertex 0, its out-neighbours become 1..D*, its in-neighbours become
    D*+1..12.
  - (a) and (c) hold. For D = d = D*, (b) holds because D* is the maximum. For D ≠ d, cond(D) satisfies (b) by
    Lemma C. Register clauses are satisfied by Lemma S.
- Step 2 (D* < 12).
  - The in-neighbour w gets label D*+1. Inside {1..D*} and inside {D*+2..12}, the out-neighbours of w come first.
  - These permutations fix vertex 0, the set {1..D*} and w. So (a) and (b) are unchanged. (c) is unchanged because
    {1..5} ⊆ {1..D*}.
  - (l) for D = d holds by the chosen order. (l) for D ≠ d is satisfied by cond.
  - Every (n) clause carries ¬lit(0,0,12), which is true.
- Step 3 (D* = 12, vertex 0 beats everyone in T_0).
  - Each 5-set {0} ∪ W with W ⊆ {1..12}, |W| = 4, needs a dominator v that beats 0. That happens only in T_1, and
    then v ∈ {1..12} − W and v → W. So the maximum out-degree D' inside V' = {1..12} in T_1 is ≥ 4.
  - Relabel V' so that the maximiser is vertex 1 and its out-neighbours inside V' are 2..D'+1. Vertex 0 is fixed and
    still beats everyone in T_0.
  - (a) and (c) hold. All (b) and (l) clauses are satisfied by lit(0,0,D+1), which is true.
  - The (n) order clauses and units hold (D' ≥ 4). The (n) counters for D' hold by maximality, the other (n)
    counters by their extra literals, and the (n) registers by Lemma S.
- d(t,v,U) := [v → U in T_t] satisfies the base clauses for the relabelled pair. So for every S_5 pair the shipped
  CNF has a model, and UNSAT therefore proves that no S_5 pair exists on 13 vertices.

| group | clauses | active when | justified by |
|---|---|---|---|
| (a) ¬lit(0,0,u+1) ∨ lit(0,0,u), u = 1..11 | 11 | always | Step 1 labelling |
| (c) lit(0,0,u), u = 1..5 | 5 | always | D* ≥ k |
| (b) at-most-D counters, D = 5..11, all (t,v) | 32578 | d = D (overflow only) | Step 1, Lemmas S and C |
| (n) 10 order clauses, 4 units, counters D' = 4..10 on V', t = 1 | 12026 | d = 12 (and d' = D' for overflow) | Step 3, Lemma S |
| (l) w = D+1 initial segments, D = 5..11 | 64 | d = D | Step 2 |
| (s) | 0 | m ≥ 3 only | not generated (m = 2) |

Constructive test of this argument on my own generator (Appendix A): relabel by Steps 1–3, assign edges, d variables
and all registers explicitly, then evaluate every clause.
- On the 14-vertex object, with the full n = 14 CNF (base plus symmetry breaking, 246299 clauses): 5 random starting
  relabellings, all of the Step 2 kind, gave 0 violated clauses each. Without the canonical relabelling the controls
  violate 116, 67, 53, 12 and 16 clauses.
- On 200 random pairs of tournaments on 13 vertices (100 of the Step 2 kind, 100 with a forced all-beating vertex
  of the Step 3 kind), all symmetry-breaking and defining clauses were satisfied in all 200. Random relabellings
  violate some symmetry-breaking clause in 200 of 200.
- These are tests. The proof is the derivation above.

## 6. Solver and formally verified checker

- Builds from fresh clones:
  - CaDiCaL https://github.com/arminbiere/cadical at c60730422e758ef1cebe7aeddf2dda31c996bf04 (VERSION 3.0.1),
    built with `./configure && make`.
  - cake_lpr https://github.com/tanyongkiam/cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa, built with
    `cc -O2 -o cake_lpr basis_ffi.c cake_lpr_arm8.S`.
  - These are the same commands as verify-it-yourself/run_checks.sh. The working-tree files equal the commit's blobs
    (checked with `git hash-object`).
- cake_lpr controls: it accepts its bundled example.cnf/example.lpr (`s VERIFIED UNSAT`). It rejects the same proof
  with the hints of the first addition step removed (`c Checking failed at line: 0. Reason: clause index has no
  reduction sequence but is not satisfied by witness: 22`).
- All cake_lpr runs used `--CML_HEAP_SIZE=1500 --CML_STACK_SIZE=512`. Every proof file was deleted after its check.

| run | input | CaDiCaL | proof | cake_lpr | resources |
|---|---|---|---|---|---|
| A | verify-it-yourself/run_checks.sh, with CADICAL and CAKE_LPR set to the builds above | `s UNSATISFIABLE` | in the script's temporary folder, removed by its trap | `s VERIFIED UNSAT`, last line `PASS` | 161.9 s for the whole script; min free+inactive 1.21 GiB; peak child RSS 1281 MiB |
| B | my own CNF (4.1, sha256 007dca92…) | `s UNSATISFIABLE`, exit 20, 139.69 s, 115.45 MB | 468667706 bytes, sha256 aa3f14d5661ffd7dbbc73a3d3aece723b5404b272c45c246222907fb1306c2d5 | `s VERIFIED UNSAT` | 192.4 s including both checks; min free+inactive 1.11 GiB; peak RSS 1375 MiB |
| B' | shipped CNF (sha256 247ca744…) with the proof from run B | — | same as B | `s VERIFIED UNSAT` | (in B) |
| C | shipped CNF, solver only | `s UNSATISFIABLE`, exit 20, 143.60 s | 371954317 bytes (claim: 372 MB), sha256 d87598122cfb5f17397537deb15b893d7aaae49598a81ce41a1c92191d0de99a | not repeated (run A checked this CNF) | 148.7 s |

Run A log (verbatim, complete):

```
== 1. regenerate the CNF named by object/cnf_spec.json (shipped encoder) and compare sha256 and header
regenerated CNF: 42644 variables, 148931 clauses, sha256 247ca74489c8144e2eca1fa1b7bfdd6c2f7f826e7deac2c46e4b3748c7069626
matches object/cnf_spec.json
== 2. upper bound: object/upper_bound_m2k5n14.json is an S_5 set of two tournaments on 14 vertices
m=2 k=5 n=14: 2002 k-subsets checked, 0 undominated -> PASS
== 3. the base clauses of the CNF are exactly Definition 2.2 for (m,k,n) = (2,5,13) (cnf_audit.py)
f.cnf: 148931 clauses; 1287 domination clauses over 1287 k-sets; 102960 defining clauses; 44684 added clauses
AUDIT OK
== 4. solver and verified checker
CaDiCaL 3.0.1
== 5. CaDiCaL with a text LRAT proof, then cake_lpr on the formula and the proof
s UNSATISFIABLE
s VERIFIED UNSAT
no S_5 set of two tournaments on 13 vertices (so none on fewer, by adding a vertex that loses to all): f(2,5) >= 14;
with the 14-vertex object of step 2: f(2,5) = 14
PASS
```

path key: `f.cnf` in the log is the CNF that run_checks.sh regenerates inside its own temporary folder, which the
script deletes on exit.

All outputs that RUN_IT_YOURSELF.md (= REPRODUCE.md) promises appeared exactly. The README's sizes also match: the
CNF is 2116234 bytes ("2.1 MB") and the proof for the shipped CNF is 371954317 bytes ("372 MB"). The script's own
time note ("161 s without the builds") is consistent with the 161.9 s measured here.

## 7. Remarks (none blocks the pass)

1. verify-it-yourself/cnf_audit.py audits only the base clauses. run_checks.sh does not check the 44684 added clauses
   mechanically: they are argued in how-we-built-it/SOUNDNESS.md, and how-we-built-it/sb_audit.py tests them at
   random (it needs python-sat). Sections 4–5 close this gap independently: I re-implemented the clauses from the
   note, matched them exactly and re-derived their soundness. A future version could ship a deterministic check of
   the added clauses in verify-it-yourself/.
2. Read literally, Definition 2.1 is vacuous for orders below k. The lower-bound step relies on the paper's
   convention |V| ≤ k ⇒ not S_k (proof of Proposition 2.2), which the bank also uses (n ≥ k+1). Under that convention
   the step is correct.
3. At the pinned commit, upstream cake_lpr's file cake_lpr.sha256 still lists an older basis_ffi.c hash
   (8e30d84f…; the checked-out file is 3fbd8f31…). The two .S files match the listed hashes. This file belongs to the
   cake_lpr repository and is not the claimant's. Anyone comparing it will see the mismatch.
4. Novelty is outside this role. One web search found no publication after arXiv:2604.08790 v1 that settles f(2,5);
   treat this as provisional.

## 8. Deviations

- I ran verify-it-yourself/run_checks.sh with CADICAL and CAKE_LPR pointing to my own builds of the same pinned
  commits, so the script did not build the tools a second time. The build commands are the same as in the script.
- I set TMPDIR to an absolute folder for run A, because the sandbox's TMPDIR was a relative path.
- I did not run the claimant's development scripts in how-we-built-it/ (calibrate.py, cubes.py, test_global2.py,
  test_global3.py, test_alt.py, encode_alt.py, sb_audit.py, make_tests.py, solve_lrat_zstd.sh, check_lrat_zstd.sh).
  They are not part of the certificate, and some need python-sat or kissat. My own constructive test (section 5)
  replaces sb_audit.py.
- No proof file is stored. All were deleted after checking, as instructed.
- Outside context: automatically recalled memory notes (section 0), not used as evidence. I also made one web search.

## Appendix A: reviewer's own code (core functions, verbatim; file I/O omitted)

### Checker (Definition 2.1), `my_check.py`

```python
def check_tournament(M, n):
    errs = []
    if len(M) != n: errs.append("row count %d != n=%d" % (len(M), n))
    for i, row in enumerate(M):
        if len(row) != n: errs.append("row %d length %d" % (i, len(row)))
        for j, c in enumerate(row):
            if c not in "01": errs.append("entry (%d,%d)=%r not in {0,1}" % (i, j, c))
    if errs: return errs
    A = [[int(c) for c in row] for row in M]
    for i in range(n):
        if A[i][i] != 0: errs.append("diagonal (%d,%d) != 0" % (i, i))
        for j in range(n):
            if i != j and A[i][j] + A[j][i] != 1: errs.append("A[%d,%d]+A[%d,%d] != 1" % (i, j, j, i))
    return errs

def is_Sk(As, n, k):
    """returns (number of k-subsets, list of undominated k-subsets) -- exhaustive."""
    und = []
    cnt = 0
    for U in itertools.combinations(range(n), k):
        cnt += 1
        ok = False
        for A in As:
            for v in range(n):
                if v in U: continue
                if all(A[v][u] == 1 for u in U):
                    ok = True; break
            if ok: break
        if not ok: und.append(U)
    return cnt, und
```

### Base encoder (Definition 2.1), `my_encode.py`

```python
def encode(m, k, n):
    var = {}
    def x(t, a, b):
        return var.setdefault(('x', t, a, b), len(var) + 1)
    for t in range(m):
        for a in range(n):
            for b in range(a + 1, n):
                x(t, a, b)
    def arc(t, v, u):  # literal for v->u
        return x(t, v, u) if v < u else -x(t, u, v)
    clauses = []
    for U in itertools.combinations(range(n), k):
        cover = []
        for t in range(m):
            for v in range(n):
                if v in U: continue
                d = var.setdefault(('d', t, v, U), len(var) + 1)
                cover.append(d)
                for u in U:
                    clauses.append([-d, arc(t, v, u)])
        clauses.append(cover)
    return var, clauses
```

### Symmetry-breaking clauses from how-we-built-it/SOUNDNESS.md section 2, `my_sb.py`

```python
def build(m, k, n, with_sb=True, sem=None):
    var, clauses = encode(m, k, n)
    if sem is not None: sem['var'] = var
    nv = [len(var)]
    def x(t, a, b): return var[('x', t, a, b)]
    def lit(t, v, u): return x(t, v, u) if v < u else -x(t, u, v)
    def new():
        nv[0] += 1; return nv[0]
    def counter(xs, D, extra, tag):
        N = len(xs)
        s = [[None] * (D + 1) for _ in range(N)]
        for i in range(1, N):
            for j in range(1, D + 1):
                s[i][j] = new()
                if sem is not None: sem[s[i][j]] = (tuple(xs), i, j)  # s[i][j] := [#true among xs[:i] >= j]
        out = []
        out.append([-xs[0], s[1][1]])
        for j in range(2, D + 1): out.append([-s[1][j]])
        for i in range(2, N):
            out.append([-xs[i - 1], s[i][1]])
            out.append([-s[i - 1][1], s[i][1]])
            for j in range(2, D + 1):
                out.append([-xs[i - 1], -s[i - 1][j - 1], s[i][j]])
                out.append([-s[i - 1][j], s[i][j]])
            out.append([-xs[i - 1], -s[i - 1][D]] + extra)
        out.append([-xs[N - 1], -s[N - 1][D]] + extra)
        return out
    if not with_sb:
        return nv[0], clauses
    sb = {'a': [], 'c': [], 'b': [], 'l': [], 'n': []}
    # (a) out-neighbourhood of 0 in T_0 is {1..d}
    for u in range(1, n - 1): sb['a'].append([-lit(0, 0, u + 1), lit(0, 0, u)])
    # (c) d >= k
    for u in range(1, k + 1): sb['c'].append([lit(0, 0, u)])
    # (b) for D=k..n-2: if d == D then every out-degree <= D
    for D in range(k, n - 1):
        extra = [-lit(0, 0, D), lit(0, 0, D + 1)]
        for t in range(m):
            for v in range(n):
                xs = [lit(t, v, u) for u in range(n) if u != v]
                sb['b'] += counter(xs, D, extra, ('b', D, t, v))
    # (n) only when d = n-1, on V' = {1..n-1}, tournaments t >= 1
    g = [-lit(0, 0, n - 1)]
    for u in range(2, n - 1): sb['n'].append(g + [-lit(1, 1, u + 1), lit(1, 1, u)])
    for u in range(2, k + 1): sb['n'].append(g + [lit(1, 1, u)])
    for Dp in range(k - 1, n - 2):
        extra = g + [-lit(1, 1, Dp + 1), lit(1, 1, Dp + 2)]
        for t in range(1, m):
            for v in range(1, n):
                xs = [lit(t, v, u) for u in range(1, n) if u != v]
                sb['n'] += counter(xs, Dp, extra, ('n', Dp, t, v))
    # (l) only when d = D < n-1, w = D+1
    for D in range(k, n - 1):
        extra = [-lit(0, 0, D), lit(0, 0, D + 1)]
        w = D + 1
        for u in list(range(1, D)) + list(range(D + 2, n - 1)):
            sb['l'].append([-lit(0, w, u + 1), lit(0, w, u)] + extra)
    return nv[0], clauses, sb
```

### Relabelling of SOUNDNESS.md section 3 and explicit assignment, `sb_soundness_test.py`

```python
def relabel(T, newlist, order):
    n = len(newlist)
    return [[[T[o][newlist[a]][newlist[b]] if a != b else 0 for b in range(n)] for a in range(n)] for o in order]

def canonical(T, m, n, rng):
    deg = [(sum(T[t][v]), t, v) for t in range(m) for v in range(n)]
    Dstar = max(x[0] for x in deg)
    ts, vs = rng.choice([(t, v) for d, t, v in deg if d == Dstar])
    order = [ts] + [t for t in range(m) if t != ts]
    A = T[ts]
    O = [u for u in range(n) if u != vs and A[vs][u]]; I = [u for u in range(n) if u != vs and not A[vs][u]]
    rng.shuffle(O); rng.shuffle(I)
    if Dstar < n - 1:                                   # step 2
        w = rng.choice(I); rest = [u for u in I if u != w]
        O = [u for u in O if A[w][u]] + [u for u in O if not A[w][u]]
        rest = [u for u in rest if A[w][u]] + [u for u in rest if not A[w][u]]
        return relabel(T, [vs] + O + [w] + rest, order), 2
    T2 = relabel(T, [vs] + O, order)                   # step 3 (D* = n-1)
    sc = [(sum(T2[t][v][u] for u in range(1, n) if u != v), t, v) for t in range(1, m) for v in range(1, n)]
    Dp = max(x[0] for x in sc)
    tp, vp = rng.choice([(t, v) for d, t, v in sc if d == Dp])
    order2 = [0, tp] + [t for t in range(1, m) if t != tp]
    Op = [u for u in range(1, n) if u != vp and T2[tp][vp][u]]; Ip = [u for u in range(1, n) if u != vp and not T2[tp][vp][u]]
    rng.shuffle(Op); rng.shuffle(Ip)
    return relabel(T2, [0, vp] + Op + Ip, order2), 3

def assignment(T, m, k, n, sem):
    var = sem['var']; val = {}
    for key, x in var.items():
        if key[0] == 'x': _, t, a, b = key; val[x] = bool(T[t][a][b])
        else: _, t, v, U = key; val[x] = all(T[t][v][u] for u in U)
    ev = lambda l: val[l] if l > 0 else not val[-l]
    for s, info in sem.items():
        if s == 'var': continue
        xs, i, j = info
        val[s] = sum(1 for l in xs[:i] if ev(l)) >= j
    return ev
```

### Numbering-independent CNF comparison (exact colour refinement), `cnf_iso.py`

```python
def refine(cnfs, F):
    # nodes per cnf: vars 1..V, clauses
    occ = []
    for hdr, cls in cnfs:
        V = hdr[0]
        o = [[] for _ in range(V + 1)]
        for ci, c in enumerate(cls):
            for l in c: o[abs(l)].append((ci, 1 if l > 0 else -1))
        occ.append(o)
    vcol = [[('E', v) if v <= F else ('A',) for v in range(hdr[0] + 1)] for hdr, _ in cnfs]
    ccol = [[('C', len(c)) for c in cls] for _, cls in cnfs]
    def relabel(cols_lists):
        table = {}
        out = []
        for cols in cols_lists:
            out.append([table.setdefault(c, len(table)) for c in cols])
        return out, len(table)
    vcol, nv = relabel(vcol); ccol, nc = relabel(ccol)
    it = 0
    while True:
        it += 1
        newc = [[(ccol[g][ci], tuple(sorted((1 if l > 0 else -1, vcol[g][abs(l)]) for l in c)))
                 for ci, c in enumerate(cnfs[g][1])] for g in range(len(cnfs))]
        ccol2, nc2 = relabel(newc)
        newv = [[(vcol[g][v], tuple(sorted((s, ccol2[g][ci]) for ci, s in occ[g][v])))
                 for v in range(len(vcol[g]))] for g in range(len(cnfs))]
        vcol2, nv2 = relabel(newv)
        stable = (nv2 == nv and nc2 == nc)
        vcol, ccol, nv, nc = vcol2, ccol2, nv2, nc2
        if stable or it > 200: break
    return vcol, ccol, it
```

pass: true
