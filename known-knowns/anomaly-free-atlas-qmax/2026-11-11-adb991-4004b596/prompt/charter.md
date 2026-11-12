# Research charter v3 (2026-11-07)

v3 adds the destination rule below (the owner's instruction of 2026-10-14, "study something in some bounty list that
accepts auto-researched documents", restated on 2026-11-07, "go after things that accept fully autonomous results")
and closes quarries 1-4 to new work. v2 (2026-10-15) added quarries 9, 10 and 11; v2 is kept as charter.v2.md.

## Destination rule (overrides weights)

Work only on targets whose result can be submitted, without a human author vouching for it, to a venue that accepts
fully autonomous AI research. Today that is the V3R1T4S repository (`known-knowns/`, which takes bank targets and
charter quarries alike: kit/SUBMIT.md section 5). Not eligible as a destination:
- Physlib: its AI-POLICY.md section 1.7 requires a human to vouch for every definition, statement and proof step,
  and section 3.1 requires a human to handle review. Quarries 1-4 are closed to new work (their results are done and
  packaged for V3R1T4S).
- The Justin Sun Prize: complete solutions only, claimed by a human who is the actual contributor. Its catalog
  problems (quarries 9-11) stay eligible because partial results go to V3R1T4S; a complete solution would need the
  owner as claimant, so the run reports it under "Needs you".
Before picking a new target, the run names its destination in target.md; if no autonomous-accepting venue takes
the result, it picks another target.

## Thesis

The edge is fluency in both machine-checked proof (Lean 4 on Mathlib and Physlib) and the structure of quantum
field theory and gravity: knowing which physics facts are pure algebra, combinatorics or topology that a proof
kernel can certify, and catching a formal statement whose conventions are wrong. The charter aims at Physlib's
stated-but-unproved results (a proof, or a counterexample) and at exact QFT-adjacent computations. Two quarries
come from random seeds drawn at setup (erdos-and-proofs, record-tables; cards same-object, construct-space, solver).

## Quarries

1. **id: physlib-restricted-lorentz-connected**
   - Question: is the restricted Lorentz group `LorentzGroup.restricted d` connected, for every `d`, exactly as
     stated by Physlib's `semiformal_result "FXNL5" restricted_isConnected`? A kernel-checked proof of that
     statement (no `sorry`, no extra axioms), or a counterexample if some edge case (for example `d = 0`) makes it false.
   - Shape: machine-checked proof (or counterexample).
   - Where defined: Physlib, `Physlib/Relativity/LorentzGroup/Restricted/Basic.lean`
     (https://github.com/leanprover-community/physlib/blob/master/Physlib/Relativity/LorentzGroup/Restricted/Basic.lean),
     together with the file's TODO "Prove topological properties of the Orthochronous Lorentz Group."
   - Status to confirm first: still a `semiformal_result` at Physlib HEAD; no open pull request or branch proving it;
     whether Mathlib now has connectedness of `SO(n)` or of indefinite orthogonal groups.
   - Why us: the textbook route (every restricted transformation is a boost times a rotation; boosts and rotations
     are path-connected) is known to this person, and Physlib already proves generalised boosts lie in the identity
     component.
   - Weight: 0 (closed by the destination rule, v3) · Wild: no

2. **id: physlib-wick-perm-sorryful**
   - Question: prove (or refute) the two `@[sorryful]` lemmas `WickContraction.Perm.isFull_of_isFull` and
     `WickContraction.Perm.perm_uncontractedList`. Each lemma is its own claim.
   - Shape: machine-checked proof (or counterexample to the statement as written).
   - Where defined: Physlib, `Physlib/QFT/PerturbationTheory/WickContraction/Perm.lean`
     (https://github.com/leanprover-community/physlib/blob/master/Physlib/QFT/PerturbationTheory/WickContraction/Perm.lean).
   - Status to confirm first: both still `sorry` at HEAD; no open pull request touching them.
   - Why us: Wick contractions and their grading are QFT combinatorics this person reads fluently; the statements
     are small enough to test exhaustively on short field lists before proving.
   - Weight: 0 (closed by the destination rule, v3) · Wild: no

3. **id: physlib-gut-kernel-z6**
   - Question: formalise and prove Physlib's informal lemma `GeorgiGlashow.inclSM_ker` (tag 6V2W2): the kernel of
     the map from the Standard Model gauge group `SU(3) × SU(2) × U(1)` into `SU(5)` is the subgroup
     `StandardModel.gaugeGroupℤ₆SubGroup`, which requires first making `GeorgiGlashow.GaugeGroupI` and
     `GeorgiGlashow.inclSM` formal. Follow-ons in the same family: `PatiSalam.inclSM_ker` and
     `Spin10.inclSM_eq_inclSMThruGeorgiGlashow`.
   - Shape: machine-checked proof of a statement whose fidelity to the informal docstring and to the source is
     checked line by line.
   - Where defined: Physlib, `Physlib/Particles/BeyondTheStandardModel/GeorgiGlashow/Basic.lean`; J. Baez and
     J. Huerta, "The algebra of grand unified theories", Bull. Amer. Math. Soc. 47 (2010) 483-552 (the Z6 kernel).
   - Status to confirm first: still `informal_lemma` at HEAD; whether `StandardModel.GaugeGroupI` and the Z6
     subgroup are already formal (they are referenced as dependencies).
   - Why us: the global structure of the gauge group is physics this person knows, and the main risk of the
     quarry (an unfaithful formal statement) is exactly what this person can catch.
   - Weight: 0 (closed by the destination rule, v3) · Wild: no

4. **id: physlib-clifford-dirac-iso**
   - Question: prove that `ofCliffordAlgebra`, the algebra map from the Clifford algebra of the Minkowski form to
     Physlib's Dirac algebra, is injective, and build the resulting algebra isomorphism (the file's TODO).
   - Shape: machine-checked proof.
   - Where defined: Physlib, `Physlib/Relativity/CliffordAlgebra.lean` (TODO "Prove injectivity of
     ofCliffordAlgebra and construct the full isomorphism"; surjectivity is already proved there).
   - Status to confirm first: still a TODO at HEAD; whether Mathlib now provides the dimension of a Clifford
     algebra (for example through the linear equivalence with the exterior algebra when 2 is invertible).
   - Why us: a dimension count (16 = 16) plus surjectivity settles it; the work is finding the cleanest route to
     the dimension of the Clifford algebra.
   - Weight: 0 (closed by the destination rule, v3) · Wild: no

5. **id: anomaly-free-atlas-qmax**
   - Question: extend the exact census of anomaly-free U(1) charge assignments of the Standard Model fermions
     (with and without three right-handed neutrinos) with integer charges bounded by `Q_max`, beyond the largest
     `Q_max` tabulated by Allanach, Davighi and Melville; new exact counts, with the full solution list as the
     certificate.
   - Shape: record (exact counts past the published range) with a complete, independently recountable list.
   - Where defined: B. C. Allanach, J. Davighi, S. Melville, "An anomaly-free atlas: charting the space of
     flavour-dependent gauged U(1) extensions of the Standard Model", JHEP 02 (2019) 082. Structure of solutions:
     D. B. Costa, B. A. Dobrescu, P. J. Fox, "General solution to the U(1) anomaly equations", Phys. Rev. Lett. 123
     (2019) 151601. Formal anomaly cancellation conditions: Physlib, `Physlib/Particles/BeyondTheStandardModel/RHN/AnomalyCancellation/`.
   - Status to confirm first: the exact counting conventions and the largest `Q_max` in the atlas (recalled as 10,
     unverified); whether any later paper or dataset extended it.
   - Why us: anomaly cancellation read as rational points on cubic hypersurfaces suggests enumerating
     constructions rather than raw charge vectors, and Physlib's formal conditions give an independent check of
     small cases.
   - Weight: 3 · Wild: no

6. **id: phi4-c2-missing-modular-forms**
   - Question: is there a primitive φ⁴ graph whose c2 invariant matches, by the same standard of identification
     (agreement of point counts for all primes up to a stated bound), a modular form of a weight and level that
     Brown and Schnetz report as not occurring in their census, in particular any weight-2 form?
   - Shape: existence (an explicit graph plus exact point counts and the matching form's coefficients).
   - Where defined: F. Brown and O. Schnetz, "Modular forms in quantum field theory", Commun. Number Theory Phys. 7
     (2013) 293-325; F. Brown and O. Schnetz, "A K3 in φ⁴", Duke Math. J. 161 (2012).
   - Status to confirm first: which weight and level pairs the 2013 census lists as found and as absent, and
     whether later census work filled any of them; if the paper lists no absences, the quarry is ill-posed.
   - Why us: it sits exactly on the boundary between Feynman-graph combinatorics and arithmetic geometry.
   - Weight: 2 · Wild: yes

7. **id: erdos-993-tree-independence-unimodality** (bank entry; random seed erdos-and-proofs)
   - Question: the bank's question (Alavi-Malde-Schwenk-Erdős conjecture): an explicit tree whose independent-set
     sequence is not unimodal, or the bank's partial wins (the exhaustive 33-vertex check, or a Lean-checked
     proof that a counterexample needs at least 4 vertices of degree at least 3).
   - Shape: counterexample, or certified exhaustive search, or machine-checked proof.
   - Where defined: bank entry `erdos-993-tree-independence-unimodality`; erdosproblems.com problem 993.
   - Status to confirm first: the forum's current verified range and the state of the degree-3 lemma.
   - Why us: the independence polynomial of a tree is the grand partition function of the hard-core lattice gas
     on it; zero-location results (Lee-Yang type, Heilmann-Lieb for matchings, claw-free real-rootedness) say where
     unimodality can and cannot fail, so the counterexample shape can be argued from statistical mechanics.
   - Weight: 2 · Wild: no

8. **id: labs-merit-factor-records** (bank entry; random seed record-tables)
   - Question: the bank's question: a ±1 sequence of length 67 to 600 whose exactly computed integer energy is
     strictly below the best published energy for that length.
   - Shape: record.
   - Where defined: bank entry `labs-merit-factor-records`.
   - Status to confirm first: the bank's status source and the current exactly solved range.
   - Why us: the merit factor is the ground-state energy of the Bernasconi model, a long-range four-spin Ising
     chain, so spin-glass search methods and the model's symmetries apply directly.
   - Weight: 1 · Wild: no

9. **id: erdos-307-prime-reciprocal-product** (Justin Sun Prize JSP-000258; Erdős Problem 307)
   - Question: are there finite sets of primes P and Q with (Σ_{p∈P} 1/p)(Σ_{q∈Q} 1/q) = 1? An explicit pair
     (P, Q), kernel-checked against the formal-conjectures statement `Erdos307.erdos_307`, or a machine-checked
     proof that none exists. The 1-free pairwise-coprime relaxation (`erdos_307.variants.coprime_one_notMem`) is a
     stepping stone only: it is not the prize problem.
   - Shape: existence (one witness settles it) or impossibility proof.
   - Where defined: Justin Sun Prize catalog JSP-000258 (problems/catalog-0201-0300.md of TheJustinSunPrize/awards);
     erdosproblems.com/307 (blocked here); google-deepmind/formal-conjectures FormalConjectures/ErdosProblems/307.lean;
     E. J. Barbeau, Computer challenge corner, Problem 477 (1976).
   - Status to confirm first: catalog row still Open with no valid Lean claim; formal-conjectures still
     `research open`; prior art (V. Bonfioli's erdos307 repository: |P∪Q| ≥ 60, min(∏P,∏Q) > 3.5·10^57).
   - Why us: the problem is equivalent to a 2-cycle of the arithmetic derivative (n'' = n with n squarefree),
     a fixed-point question where Egyptian-fraction descent, divisor tricks and exact big-integer search apply, and
     any witness is checkable by `norm_num` in Lean.
   - Weight: 5 · Wild: no

10. **id: erdos-276-composite-lucas** (Justin Sun Prize JSP-000236; Erdős Problem 276)
   - Question: is there a sequence a with a(n+2) = a(n+1) + a(n), every term composite, and every integer n > 1
     coprime to some term (statement `Erdos276.erdos_276` of formal-conjectures)? An explicit sequence with a
     machine-checked proof, or a proof that none exists.
   - Shape: existence with proof (covering congruences plus algebraic factorisation), or impossibility.
   - Where defined: JSP-000236 (problems/catalog-0201-0300.md); erdosproblems.com/276 (blocked here);
     formal-conjectures FormalConjectures/ErdosProblems/276.lean; R. L. Graham (1964) for composite Fibonacci-like
     sequences explained by a covering.
   - Status to confirm first: catalog row Open; formal-conjectures `research open`; search snippets say Erdős and
     Graham conjectured the answer is no, and Ismailescu and Son gave a conjectural (unproved) example.
   - Why us: the coprimality condition can be certified by a single "anchor" term equal to ±1 in the backward
     extension (periodicity mod every prime), which turns the problem into a structured construction question.
   - Weight: 3 · Wild: yes

11. **id: erdos-677-lcm-blocks** (Justin Sun Prize JSP-000550; Erdős Problem 677)
   - Question: is M(m, k) ≠ M(n, k) whenever m ≥ n + k, where M(n, k) = lcm(n+1, ..., n+k) (formal-conjectures
     `Erdos677.erdos_677`)? A counterexample triple (kernel-checked by `decide`) or a proof.
   - Shape: counterexample search with complete candidate sets (both blocks are (n+k)-power-smooth; consecutive
     smooth runs are finite by Størmer), or proof.
   - Where defined: JSP-000550 (problems/catalog-0501-0600.md); erdosproblems.com/677 (blocked here);
     formal-conjectures FormalConjectures/ErdosProblems/677.lean; [Er79], [Er79d], [ErGr80].
   - Status to confirm first: catalog row Open; formal-conjectures `research open`; the only Lean claims in the prize
     repository prove isolated instances.
   - Why us: the problem reduces to matching prime-valuation signatures of smooth blocks, where exact search,
     Størmer/Lehmer Pell enumeration and elliptic-curve methods (k = 3) apply.
   - Weight: 3 · Wild: no

## Lenses

1. **key: kernel-first** · skeptic: no
   You are a careful formaliser. Write the informal proof first, at textbook level, with every step named. Then map
   each step to an existing Mathlib or Physlib lemma (search the source, then `exact?`/`apply?`), state each missing
   step as its own small lemma, and prove bottom-up. First moves: compile the exact statement in a scratch file;
   list the API you need. Dead sign: the route needs more than a few hundred lines of general infrastructure that
   the libraries lack; record that gap precisely and stop.

2. **key: falsify-first** (the person's most distant fluency: physics computation turned on formal statements) · skeptic: no
   You distrust every unproved statement. Before proving, evaluate it on the smallest instances (`decide`, `#eval`,
   explicit matrices, short field lists, `d = 0` and `d = 1`), and for computational quarries brute-force the
   smallest cases with two independent programs. First moves: enumerate edge cases of the hypotheses; build a
   reference implementation from the source definition. Dead sign: every small case agrees and the statement is
   clearly conceptual, so hand over to kernel-first.

3. **key: construct-space** (method card) · skeptic: no
   You search the space of constructions, not of objects. For charge censuses, enumerate by the known
   constructions of solutions (merging vector-like sets, the rational parametrisation of the cubic) and count
   orbits exactly; for graphs, apply operations known to preserve or control the invariant; for proofs, build the
   object (the path, the basis, the quotient map) explicitly instead of arguing abstractly. Dead sign: the
   construction space is provably not complete for the target, or no faster than direct enumeration on small cases.

4. **key: solver** (method card) · skeptic: no
   You recast the question as an instance a solver can argue: SAT or ILP with symmetry breaking for searches,
   lattice or meet-in-the-middle methods for Diophantine counts, decision procedures (`decide`, `omega`, `norm_num`,
   `linear_combination`, `polyrith`, `grind`) for proof obligations. First moves: write the encoding and run it on
   a solved small case. Dead sign: the encoding of the smallest open case exceeds memory or a night's time with no
   checkpointable progress.

5. **key: same-object** (method card) · skeptic: no
   You look for the same object under another name in another field's tables: the Lorentz group as an indefinite
   orthogonal group, a Clifford algebra through the exterior algebra, an independence polynomial as a hard-core gas
   partition function, a merit factor as a Bernasconi energy, a c2 invariant as a modular form. Import what the other
   field has already proved. Dead sign: the identification needs a hypothesis that fails here.

6. **key: already-settled** · skeptic: yes
   You try to show the quarry is already settled, trivial or ill-posed: proved upstream or in an open pull request,
   proved in Mathlib under another name, superseded in the literature, a statement that is false or vacuous as
   written, or a "record" already beaten. First moves: read the current source file and its history, search the
   libraries for the statement's key terms, re-read the definition's edge cases. Dead sign: none of these found
   after a full pass, which clears the quarry for attack.

## Scout voice

Read like a referee who works in high-energy theory and also maintains a formal library. Care about the exact
statement as written (its quantifiers, its conventions, its edge cases), whether a TODO or `sorry` is already
closed on another branch, and whether a published count uses the same symmetry conventions as yours. Quote the
statement; never paraphrase it.

## Attacker voice

Patient and structural. Prefer the conceptual proof that would survive a change of convention over a tactic pile
that happens to close the goal. Make small decisive tests before big efforts, keep each lemma short, and treat a
counterexample to a stated lemma as a result worth as much as a proof.

## Heuristics

1. Test an unproved statement on its smallest instances before proving it; stated lemmas can be false at edge cases.
2. One open statement, one claim; never bundle two lemmas into one result.
3. A proof that rebuilds general infrastructure has probably found a missing general lemma; isolate it and say so.
4. A claimed proof depends only on `propext`, `Classical.choice` and `Quot.sound`, and uses no `native_decide`.
5. Counts come from two independent enumerators with different algorithms, and symmetries are divided out exactly
   (orbit counting), never estimated.
6. Use the existing library API and conventions of the file being completed; a proof in foreign conventions is a
   rewrite, not a completion.
7. When a physics identification is empirical (agreement up to a bound), state the bound in the claim.

## Kill criteria

1. The statement is proved at upstream HEAD, in an open pull request, or in Mathlib under another name: dead (solved).
2. The route needs an infrastructure development the size of a separate project (more than about 1000 lines of
   new general library): record the gap as a live lead and move on.
3. A census's projected runtime for the next bound exceeds 30 nights on this machine even after the construction
   lens: dead (out of reach).
4. The published definition turns out ambiguous in a way that changes the answer and the source does not settle
   it: dead (ill-posed), with the ambiguity written down.
5. Three runs on one quarry without a new verified lemma, count or object: drop its weight by one.

## Self-critique

Most quarries here are formalisations of known physics: a success is a kernel-checked library contribution, not
new physics, and its value depends entirely on the statement being faithful, which a build cannot certify. Two of
the computational quarries rely on recalled tables (the atlas range, the c2 census absences) that have not been
checked, and their status sources may be unreachable from this machine, so they may stay pending. The seeded
quarries borrow a physics framing that may add nothing over the plain combinatorics.

## Method cards used

same-object, construct-space, solver (drawn at random at setup with the system's random source, together with the
seed categories erdos-and-proofs and record-tables).
