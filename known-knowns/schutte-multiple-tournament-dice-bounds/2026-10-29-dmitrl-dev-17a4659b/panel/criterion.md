# CRITERION panel: schutte-multiple-tournament-dice-bounds, claim "f(2,5) = 14" (partial win p1)

context: subagent (fresh context, Claude Science delegation)
role: CRITERION (kit/RUN.md step 6)
date: 2026-10-29 (UTC)
inputs: the claim folder (27 files) and public sources only (arXiv abstract page and PDF, the V3R1T4S bank at
commit 8846324 and at HEAD, read-only; one web search). Nothing else from the claimant was seen.

## Verdict

- Full success criterion: **not met, and not claimed.** It asks for explicit adjacency matrices showing f(2,5) <= 13
  or f(3,6) <= 12. The claim argues the opposite direction for f(2,5): no S_5 pair of order 13 exists.
- Named partial win: **p1, f(2,5) branch: met at the criterion level.** Every element of the p1 sentence maps onto
  a part of the claim that this review checked (section 2). This role does not check the certificate run itself (a
  CaDiCaL LRAT proof accepted by cake_lpr). The proof is not in the folder, and that run belongs to the REPRODUCE
  panelist, so this pass does not cover it.
- Not subsumed: none of the public sources checked here settles f(2,5) (section 6).

## 1. Criterion text

README.md's "Success criterion" and "Partial wins" sections are verbatim copies of the bank entry
`known-unknowns/graphs-games-automata/schutte-multiple-tournament-dice-bounds.md` at the pinned commit
8846324a8fe813bf89a9ef2a60eb9b13d0ba79fd (fetched 2026-10-29T00:31:19Z, 5638 bytes, sha256
ecf021110c60705fb72e488ad5d14cc823eab4604193f6e9d01f0e489a12cd13; a string comparison of both sections found them
equal). The entry is byte-identical at bank HEAD c027ca3e0c8d1fc475d8e39cccd4b146fd50ffb8 (commit date
2026-10-27T16:42:35Z). p1 is the only enumerated partial win. For p1 the entry's "How a win is checked" asks for
three checks: (i) re-encode the CNF independently from Definition 2.2, or check the encoder line by line; (ii) check
every symmetry-breaking clause against its soundness argument; (iii) run the verified checker on the proof. This
review did (i) and (ii). (iii) is the REPRODUCE panelist's. The kit's dictionary rule for CRITERION applies to
language targets and does not apply here.

## 2. p1, element by element

| p1 element | what the claim offers | checked here |
|---|---|---|
| "An exact value ... (proving f(2,5) = 14)" | lower bound: the CNF is UNSAT at n = 13, extended to smaller orders by one added vertex (how-we-built-it/SOUNDNESS.md section 4); upper bound: object/upper_bound_m2k5n14.json | The extension lemma is valid (section 3 e). The upper-bound object is S_5: verify-it-yourself/check_schutte.py prints "m=2 k=5 n=14: 2002 k-subsets checked, 0 undominated -> PASS", and the reviewer's own check finds 0 undominated 5-sets. The object is exactly Proposition 2.3 applied to two Paley QR7 tournaments: T_0 is QR7 on {0..6} with {0..6} -> {7..13}; T_1 is QR7 on {7..13} with {7..13} -> {0..6}; the free edges are transitive. This is the Figure 7 value 14. |
| "an UNSAT certificate (DRAT or LRAT checked by a formally verified checker such as cake_lpr)" | an LRAT proof from CaDiCaL 3.0.1 (pinned commit), accepted by cake_lpr (pinned commit) with `s VERIFIED UNSAT`. The 372 MB proof is not stored, and the folder has no proof hash, solver log or checker log. | Not run here: by instruction, REPRODUCE runs the 13-vertex solve. The CNF the certificate must refer to is pinned: verify-it-yourself/spec_check.py regenerates it byte-identically ("42644 variables, 148931 clauses, sha256 247ca74489c8144e2eca1fa1b7bfdd6c2f7f826e7deac2c46e4b3748c7069626", "matches object/cnf_spec.json"). |
| "for a CNF encoding of 'two tournaments on 13 vertices with every 5-subset dominated'" | `encode_schutte.py 2 5 13 --sb global3` | The base clauses equal the reviewer's independent re-encoding (section 4). |
| "with symmetry breaking proved sound" | how-we-built-it/SOUNDNESS.md sections 2-3 | The proof was checked step by step. Every added clause family was identified and counted, then tested semantically and with mutation controls (section 5). |
| "the encoding's correctness argued in a short note that a skeptic checks against Definition 2.2" | how-we-built-it/SOUNDNESS.md section 1 | Checked against Definitions 2.1 and 2.2 of the paper (section 3). |

## 3. Definitions 2.1 and 2.2 of arXiv:2604.08790, and hidden quantifiers

Each source was fetched once. https://arxiv.org/pdf/2604.08790: 2026-10-28T23:37:18Z, HTTP 200, 393509 bytes,
sha256 6aca2fdf8285dabf47dbc7b83fd6232e31fe0e11bb02cb163f9dba05be97a8e8, the same file as in
the-record-we-beat/RECORD.md. https://arxiv.org/abs/2604.08790: 2026-10-29T00:36:14Z, HTTP 200, 39949 bytes, sha256
0b2c17af0cb7342b68eecf9951a3f011cbf28e31fdb41b3c086f9b58cfd9e3c0, the same bytes as the RECORD.md fetch; the
submission history lists v1 only (9 Apr 2026).

- Definition 2.1: a set tau = {T_1, ..., T_m} of labeled tournaments on one vertex set has S_k if for every k-set U
  there are some T_i and some vertex u with u -> U in T_i. Section 1 defines "dominates" as "directed towards every
  vertex in the set".
- Definition 2.2: f(m,k) is the minimum |V| such that an S_k set of m tournaments on V exists.
- Figure 7: the cell m = 2, k = 5 reads 14, unstarred.
- Section 4 says the work gives no non-trivial lower bound for f(m,k).

Quantifiers and definitions checked:

1. **One vertex and one tournament for all of U.** The encoding has one auxiliary per (t, v, U), which implies
   lit(t,v,u) for every u in U. This avoids the bank's trap ("the dominator must be the same vertex ... in one
   tournament").
2. **The dominator lies outside U.** Definition 2.1 only says u is in V(tau). But u -> U is impossible for u in U,
   because a tournament has no loops. So the encoder's "v not in U" is equivalent to the definition, not an extra
   restriction.
3. **"Set" of m tournaments versus ordered tuples.** The CNF ranges over ordered pairs and allows a repeated
   tournament. That is a superset of the sets of two tournaments, so UNSAT excludes every set. Both readings give
   the same f(m,k), because a repeated tournament can be replaced by an arbitrary other one (padding, as in
   Proposition 2.1).
4. **The vacuous case n <= k.** Read literally, Definition 2.1 holds vacuously when n < k. Proposition 2.2
   (f(m,k) >= k+1) and the bank's "n>=k+1" exclude this case. SOUNDNESS.md section 4 uses the same convention
   without saying so ("none on 6..12 vertices").
5. **"Minimum" in Definition 2.2 needs every order up to 13.** The extension in SOUNDNESS.md section 4 is correct:
   add a vertex w that loses to everyone in every tournament. A 5-set U that contains w is dominated by the
   dominator of (U - {w}) + {x}, where x is an old vertex outside U. That dominator is old, lies outside U and beats
   w. So UNSAT at 13 means no S_5 pair of order 6..13 exists, and orders up to 5 are excluded by point 4.
6. **Labelled tournaments.** The symmetry breaking only relabels vertices and reorders tournaments. Both operations
   preserve S_k and all out-degrees.

## 4. Base formula: line-by-line reading and independent re-encoding

- **Line-by-line reading** of verify-it-yourself/encode_schutte.py (identical to how-we-built-it/encode_schutte.py):
  - edge variable e(t,i,j), i < j, true iff i -> j in T_t;
  - for every 5-set U and every (t, v) with v not in U, one auxiliary d with 5 clauses (-d, lit(t,v,u));
  - one clause OR d per U.

  This matches Definitions 2.1 and 2.2.
- **Independent re-encoding.** The reviewer re-encoded the base formula from Definition 2.1 with separate code that
  shares only the documented edge-variable numbering. The CNF's 1287 all-positive clauses, with their 20592
  auxiliaries and 102960 defining clauses, equal the re-encoding exactly, as a multiset over 5-sets of
  candidate literal sets, up to renaming of the auxiliaries. No auxiliary occurs in any other clause, and the other
  44684 clauses contain no auxiliary.
- **The claimant's audit agrees.** verify-it-yourself/cnf_audit.py prints "1287 domination clauses over 1287
  k-sets; 102960 defining clauses; 44684 added clauses" and "AUDIT OK".

## 5. Symmetry breaking: SOUNDNESS.md sections 2-3 against the encoder

**Clause families.** The expected counts were derived from SOUNDNESS.md section 2 and the encoder, then compared
with the CNF:

- edge-only clauses: (a) 11, (c) 5, (n) segment 10, (n) conditional "units" 4, (l) 64. Total 94; the CNF has 94.
- Sinz counters: (b) "at most D" for D = 5..11 over 2 tournaments x 13 vertices, 32578 clauses and 16016 registers;
  (n) "at most D'" for D' = 4..10 over T_1 x 12 vertices, 12012 clauses and 5880 registers. Total 44590 clauses; the
  CNF has 44590.
- variables: 156 + 20592 + 16016 + 5880 = 42644, as in the header.
- (s) is absent (m = 2), as expected.

**Proof check (SOUNDNESS.md section 3).**

1. A vertex of globally maximum out-degree becomes vertex 0 of T_0, with out-neighbours 1..D*. This gives (a), (c)
   and (b).
2. If D* < n-1: an in-neighbour w of vertex 0 gets label D*+1, and its out-neighbours come first inside {1..D*} and
   inside {D*+2..n-1}. This gives (l); the (n) block is void.
3. If D* = n-1: every 5-set {0} + W must be dominated in T_1 by a vertex of V' = {1..12}. So the maximum
   out-degree inside V' over t >= 1 is at least 4. A vertex attaining it becomes vertex 1 of T_1, which gives (n);
   (b) and (l) are void.

Each step keeps the conditions of the earlier steps, and the argument is correct. For n = 13 the premises D* >= 5
and D' >= 4 hold for every pair of tournaments: any tournament on 13 vertices has a vertex of out-degree at least
6, and the same holds inside the 12 vertices of V'. So every pair, S_5 or not, has a relabelling that satisfies the
added clauses.

Two wording slips in the note have no effect. The counters' register clauses carry no condition literal, and that
includes the units -s[0][j], which force bits down rather than up. They are satisfied by the exact counts.

**Reviewer tests.** These were written from SOUNDNESS.md, not from how-we-built-it/sb_audit.py. With all 156 edge
variables fixed, the added clauses become a Horn formula over the registers, decided by forward chaining.

- **Canonical pairs:** 4000 random pairs (seed 20261029), including pairs forced to have vertices of out-degree 12
  and 11, regular tournaments, and an out-degree-12 vertex in both tournaments. The reviewer's canonical relabelling
  satisfied the reviewer's predicate for (a), (c), (b), (n) and (l) in 4000/4000 cases, and the added clauses in
  4000/4000.
  - d (the out-degree of vertex 0 in T_0) took every value 6..12: {6: 500, 7: 5, 8: 197, 9: 478, 10: 268, 11: 545,
    12: 2007}.
  - d' (when d = 12) took {6: 504, 7: 83, 8: 263, 9: 157, 10: 32, 11: 968}.
- **Non-canonical inputs:** 8000 random relabellings and single-edge perturbations of canonical pairs. Clause
  satisfiability equalled the predicate in 8000/8000 cases. The clauses rejected 3994/4000 random relabellings, and
  1036/4000 perturbations violated the predicate. On these inputs the clauses say exactly what section 2 says.
- **Mutation controls** (each check must catch its own class of error):
  - Flipping one defining literal, or deleting one domination clause, makes the re-encoding comparison fail; the
    symmetry-breaking test is unaffected.
  - Removing the d = D condition from one (l) clause, making one (b) counter unconditional, or adding an unjustified
    edge unit makes the symmetry-breaking test fail (canonical pairs accepted 301/400, 322/400 and 197/400); the
    re-encoding comparison is unaffected.

The random test is a spot check that supports the proof check. It is not a substitute for it.

## 6. Null models and subsumption

- **Starred cells.** The same encoder with `--sb global3`, run with pysat's CaDiCaL 1.9.5 on the starred small
  cells of Figure 7, gives SAT at n = f(m,k) and UNSAT at n = f(m,k) - 1 for (m,k) = (2,2), (2,3), (3,3), (3,4),
  (2,4), (3,5), (4,5): 14 of 14 runs as expected. Every SAT model was re-checked as S_k by the reviewer's checker.
- **Forcing vertex 0 to beat everyone in T_0.**
  - (3,4,7) and (4,5,8) are SAT, so the nested block keeps genuine solutions.
  - (2,4,10) is UNSAT, as expected: it would need an S_3 tournament on 9 vertices, and f(3) = 19.
- **One vertex above the claimed bound.** (2,5,14) with global3 is SAT in 0.9 s, and the model is an S_5 pair
  (reviewer's checker). So the pipeline does not "prove" the false statement f(2,5) > 14.
- **Simple bounds stop short of 14.**
  - Counting (the sum of C(outdeg, 5) is at most 2 C(n,6)) gives n >= 8.
  - Deleting a vertex from an S_5 pair leaves an S_4 pair, which gives n >= f(2,4) + 1 = 11.
- **Published work does not settle f(2,5).**
  - The paper is at v1 only, the cell is unstarred, and Section 4 offers no non-trivial lower bound.
  - One web search (2026-10-29) found no later determination of f(2,5). The hits were the paper itself, a Lean
    formalisation of the classical single-tournament bounds, and bank pull request #694, which proposed this target.
  - Bank: no claim folder for this target exists at 8846324 or at HEAD c027ca3, and TROPHY_CASE.md at HEAD has no
    match for schutte, tournament or dice.
  - Not read: reference [8] (the author's 2024 dissertation). The 2026 paper cites it for the starred values and
    still leaves f(2,5) unstarred. The literature search proper is NOVELTY's.
- **Not a bundle.** The claim covers one cell with one CNF. The 14-vertex object is the published construction,
  and README.md reports it as such, naming Proposition 2.3 and its two order-7 Paley ingredients.

## 7. Weak points (not criterion failures)

- The folder contains neither the certificate, its hash, nor any solver or checker log. The certificate element of
  p1 therefore rests entirely on the panel's own run.
- The tests in how-we-built-it/ ship without outputs. This review did not run them and used its own checks instead.

## 8. Context disclosure and deviations

- **Recalled memory.** My context contained memory notes recalled automatically by the harness: the user's general
  working preferences, and project notes about earlier V3R1T4S runs and panels. None of them reported a
  verification result for this claim.
- **Previews from other sessions.** When I wrote a private scratch note, the harness showed truncated one-line
  previews of notes from other sessions. One of them was evidently written by another panel context ("REPRODUCE
  skeptic task: package unzipped to ..."). I did not open or use any of these notes, and no finding above depends on
  them. I saw nothing from the earlier, stalled CRITERION context.
- **Open findings from another session.** Before submitting, I queried the harness's list of open reviewer
  findings. It showed two findings from another session about an unrelated literature task. They are not about this
  claim, and I did not use them.
- **Not done here, by instruction:** the full CaDiCaL and cake_lpr run on the 13-vertex CNF. One sub-case of that
  CNF was run instead: with an extra unit clause forcing vertex 0 to beat everyone in T_0, pysat's CaDiCaL 1.9.5
  reports UNSAT in 0.0 s. That is expected, since the sub-case would need an S_4 tournament on 12 vertices, and
  f(4) >= 47 by the Szekeres-Szekeres bound.
- **Solver substitution:** the calibrations used pysat's CaDiCaL 1.9.5, not the CaDiCaL 3.0.1 pinned by the claim.
- path key: my_base_check.py, my_sb_test.py, my_cells.py and my_mutations.py are reviewer-written scripts outside the
  claim folder. "The regenerated CNF" is the file that verify-it-yourself/spec_check.py writes from
  object/cnf_spec.json.

confirmed_scope: Partial win p1 for f(2,5), not the full success criterion: the CNF regenerated by verify-it-yourself/encode_schutte.py 2 5 13 --sb global3 (sha256 247ca74489c8144e2eca1fa1b7bfdd6c2f7f826e7deac2c46e4b3748c7069626, 42644 variables, 148931 clauses) is satisfiable whenever two tournaments on 13 vertices have property S_5 of Definitions 2.1 and 2.2 of arXiv:2604.08790 (base clauses and every symmetry-breaking clause checked in this review), so cake_lpr's acceptance of an UNSAT proof for exactly this CNF, which this review did not run, together with the one-vertex extension and the published 14-vertex composition of two order-7 Paley tournaments, gives f(2,5) = 14.

pass: true
