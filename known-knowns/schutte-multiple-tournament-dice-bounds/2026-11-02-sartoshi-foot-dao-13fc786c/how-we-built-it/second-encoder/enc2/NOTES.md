# enc2 notes

Source: Joel Jeffries, "Schütte's property for sets of tournaments and an application to
dice games", arXiv:2604.08790v1 (PDF fetched from https://arxiv.org/pdf/2604.08790v1, 4 pages
of text extracted with pdftotext). Nothing else was consulted.

## Definitions, word for word (as extracted from the PDF)

Notation sentence just before Definition 2.1:

> If a vertex v dominates a set of vertices U , we say v → U .

**Definition 2.1** (Schütte's property for sets of tournaments). Let τ = {T1 , . . . , Tm } be a
set of m labeled tournaments each on the same vertex set V (τ ). The set τ has Schütte's
property Sk if for every set of k vertices U ⊂ V (τ ), there is a tournament Ti ∈ τ and a vertex
u ∈ V (τ ) such that u → U in Ti .

**Definition 2.2.** For m, k ∈ N, define f (m, k) to be the minimum size of a vertex set V such
that there is an Sk set of m tournaments on V .

"Dominates" is defined in the Introduction: "In a directed graph, a vertex v dominates a set
of vertices if v is directed towards every vertex in the set."

## My reading (direction)

"u → U in T_i" means: in tournament T_i, the arc between u and w points from u to w for every
w in U, i.e. u beats every member of U. The dominator is the winner, the set is beaten.
Since a tournament has no loops, u cannot beat itself, so u is necessarily outside U.
One tournament must do the whole job for a given U: it is not enough for u to beat some of
U in T_1 and the rest in T_2 (the definition says "a tournament Ti ... and a vertex u ... such
that u → U in Ti"). Different k-sets may use different tournaments and different dominators.
In the encoder a true arc variable means "i beats j", i.e. arc i -> j, so u → U in T_t is the
conjunction of arc(m,n,t,u,w) over w in U.

f(m,k) is the least n for which base_cnf(m,k,n) is satisfiable (with the caveat on tiny n
below).

## How each constraint is encoded

**Arc variables.** var(t,i,j) = t*C(n,2) + idx(i,j) + 1 for i<j, idx lexicographic,
idx(i,j) = i(n-1) - i(i-1)/2 + (j-i-1). arc(m,n,t,i,j) returns that variable for i<j and its
negation for i>j, so every tournament is automatically complete and antisymmetric; no further
clauses are needed to make each T_t a tournament.

**Property S_k (base_cnf).** For each k-subset U of {0..n-1}, for each tournament t and each
vertex u not in U, a fresh auxiliary y(U,t,u) with clauses (¬y ∨ arc(t,u,w)) for each w in U
(y implies u beats all of U in T_t). Then one clause OR of all y(U,t,u) for that U. Only the
implication y -> conjunction is encoded; the reverse is unnecessary for satisfiability. If no
candidate exists (n = k) the OR is empty, giving an empty clause (UNSAT), which is correct.
Vertices u in U are skipped because u cannot beat itself.

**(i) out-degree ≤ d** in every tournament: for every (t,v), a hand-written Sinz sequential
counter at_most(lits, d) over the n-1 literals arc(t,v,w). Counter vars s[i][j] mean "at least
j+1 of the first i+1 literals are true" (only the upward implication is enforced) and the
overflow clause forbids the (d+1)-th. K=0 becomes all-negative units, K ≥ len gives no clauses.
The counter was checked exhaustively for all lengths ≤ 6 and all K in the self-test.

**(ii) T_1 row of vertex 0:** unit clauses arc(0,0,w) for w=1..d and ¬arc(0,0,w) for
w=d+1..n-1.

**(iii) T_2 row of vertex 0:** unit clauses arc(1,0,w) for w in {1..a} ∪ {d+1..d+b},
negated for every other w ≥ 1 (only added when m ≥ 2).

**(iv) T_3 (only if m ≥ 3):** at_most over arc(2,0,w), w=1..n-1, with bound a+b, same
sequential counter.

**decode / has_Sk.** decode reads arc variables from the model into 0/1 matrices.
has_Sk loops over all k-subsets U and looks for a matrix A and vertex u with A[u][w]=1 for
all w in U (A[u][u]=0 rules out u in U); it also asserts each matrix is a tournament. It does
not use the CNF.

**Self-test.** Besides the requested base cases: an exhaustive check of at_most, an arc
numbering check, flip tests (take a SAT model, swap 1-3 random arcs, fix all arcs of the
flipped tournaments as unit clauses, compare SAT/UNSAT with has_Sk), and a few cube_cnf
cases whose models are checked against (i)-(iv) and S_k from the matrices. The (2,3,n) sweep
starts at n=4 and stops when ~60 s of solve time is used (the last case is interrupted and
reported TIMEOUT). (2,4,9) and (2,4,10) each have a 1200 s cap.

## Ambiguities / things noticed in the paper

1. **Tiny vertex sets (n < k).** Read literally, if |V| < k there are no k-sets, so any set
   of tournaments is vacuously S_k and Definition 2.2 would give f(m,k) = 0 (or 1, or
   whatever the smallest allowed vertex set is). That contradicts f(1,1)=3 and f(1,2)=7 used in
   the paper. The paper settles it in the proof of Proposition 2.2: "if τ is a set of
   tournaments such that |V(τ)| ≤ k, then τ is not Sk ... if such a set even possible", giving
   f(m,k) ≥ k+1. base_cnf follows the paper's statement: for n ≤ k it returns a single empty
   clause (UNSAT). The self-test prints (2,3,2) and (2,3,3) as UNSAT for this reason. All
   other self-test cases have n > k and are unaffected.
2. **"U ⊂ V(τ)"**: proper vs not-necessarily-proper subset is irrelevant except at n = k,
   where both readings give no valid dominator anyway.
3. **"set of m labeled tournaments"**: it is not said whether the m tournaments must be
   distinct. The encoder allows repeats. This does not change satisfiability whenever
   2^C(n,2) ≥ m: if a solution repeats a tournament, the repeated copy can be replaced by
   any unused tournament without losing S_k (property only needs "at least one"). Proposition
   2.1's proof also adds "arbitrary tournaments", consistent with this.
4. **Proposition 2.1, second bullet** reads "for all |V(τ)| − 1 ≤ k′ ≤ k"; from its proof
   it must mean 1 ≤ k′ ≤ k (looks like a typo). Not used by the encoder.
5. Definition 2.2 says "minimum size of a vertex set V"; I take that as n = |V|, with no
   requirement that the vertices be labelled 0..n-1 in any particular way. The cube constraints
   (ii)-(iv) are the caller's symmetry-breaking assumptions, not part of the paper's
   definitions; I implemented them as specified and did not check whether they are WLOG.

## Self-test results (selftest.out, CaDiCaL 1.9.5 via python-sat 1.9.dev17, ser5)

Least n found: (m=1,k=1) 3; (1,2) 7 (both match the classical values); (2,2) 4 (3 UNSAT,
4 SAT; the paper's Figure 5 caption says f(2,2)=4); (2,3) 6 (4,5 UNSAT, 6..30 SAT);
(2,4,9) UNSAT in 58 s, (2,4,10) SAT. Every SAT model passes has_Sk, every flip test agrees,
and the cube models satisfy (i)-(iv). Overall PASS.
