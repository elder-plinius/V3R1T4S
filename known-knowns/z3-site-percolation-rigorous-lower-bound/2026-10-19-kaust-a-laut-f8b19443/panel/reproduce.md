# REPRODUCE skeptic report: p_c^site(Z^3) >= 263376/10^6

context: subagent (fresh, claim/ copy only)

Inputs: only my private copy claim/ (CLAIM.md, PROOF.md, REPRODUCE.md, code/, outputs/, result/, table/,
MANIFEST.sha256) and my own files in skeptic/. Nothing else on the machine was read. Paths below are relative to
claim/ or to skeptic/.

Claim-copy note: my copy of claim/ is the original version. I did not modify it, and it verifies against its own
MANIFEST.sha256. The coordinator reports that the master folder was corrected afterwards: the record is now 0.2522,
and only CLAIM.md, table/literature_record.md, result/bound.json and MANIFEST.sha256 changed. My evidence concerns
PROOF.md, code/ and outputs/. Their sha256 values in my copy follow, so they can be compared with the corrected
folder:
- PROOF.md 425cb1e7cb1f94e04c06bcddc32a0b55a19f9d9d13dbb0623b89c32878181879
- code/par/main.go 36db20e5af3c60c9281731242e3258a03bb9d24bfefc77d920b7f56a18064037
- code/par/go.mod 6dc33a47f1e3c8b1ac3ac2793702e47f898e52ac5f28a1c863678e44354dabc3
- code/verify_cert.py d0b8812332c81d204c286dd9adcea6e026f6c23b76eea9af9b7ff9396a6a5ab9
- code/kcheck.py 76e7a9c4bf3505ae95867964d99dc15777817f57be6f1fe2ac73dd7fa9f7d30a
- outputs/p16.txt fefaaeb76f5717232325d6cfa9abeca5a8a8485e997c21a293a77a824ce8c373
- outputs/p18.txt 0f418116ec365d290dd4384b8345ed6a625905dc38d2d273f609fabcf3df84f6
- outputs/p20.txt 04bce75fa19d4609b41f0ba82d0ef32d3c78259dde5f9fcd492917afdaccc989
- outputs/verify_N20.txt 43ffad624a83c1a51a9752355f38f07b27fe79d47db3a2b61f02ec502937afbb
- outputs/k20.txt bb0bb4e0a13f1d6f0e6f73879a817adc04b13a9b084329d0545c52f532c8a1fa
- outputs/k18.txt 6a9c954e05195899389b85c99bada4b7f662c423ba036cc100b7f7ccf6c0c651

## Order of work (blindness)
1. I read CLAIM.md and PROOF.md and re-derived the proof.
2. I wrote three enumerators of my own from the PROOF.md definitions.
3. I produced my own full tables for N = 1..18 before opening code/ or outputs/.
4. I looked at outputs/p20.txt only after my own exhaustive N = 20 run had finished.

## 1. Proof re-derivation
Definitions I implemented, quoted from PROOF.md:
- "S(gamma) = { w not in gamma : w ~ v_i and w ~ v_j for some i, j with j - i >= 3 } (shortcut sites)"
- "C(gamma) = { u_k : 1 <= k <= N - 1, v_{k+1} - v_k != v_k - v_{k-1} (a turn), and dirindex(u_k - v_{k+1}) <
  dirindex(v_k - v_{k+1}) }, where u_k = v_{k-1} + v_{k+1} - v_k (turn corners)"; F = S u C
- "E(gamma) = { y ~ v_N : y not in gamma, y adjacent to no v_i with i < N, y not in F(gamma) }"
- "K_N(p) = sum over N-step NAWs gamma from 0 of |E(gamma)| p^(N+1) (1-p)^|F(gamma)|", with c_f = the sum of |E|
  over NAWs with |F| = f.
- Directions e_0..e_5 = +x,-x,+y,-y,+z,-z. The parent of x is the element of P(x) with the smallest direction
  index seen from x.

I re-derived every step and found no gap:
- Parent rule and tree. For x != 0 in C(0), P(x) is nonempty. The parent is unique because x's neighbours lie in
  distinct directions. d drops by 1 along parent pointers, so the parents form a spanning tree of C(0) in which
  every vertex has at most 6 children.
- Lemma 0 (F and gamma are disjoint). At a turn, u_k is adjacent to both v_{k-1} and v_{k+1}. If u_k were some
  v_m, the NAW property would force m = k. But u_k - v_k is a sum of two orthogonal unit vectors, so u_k != v_k.
  S excludes gamma by definition.
- Lemma 1.
  - (a) d(v_k) = k, by induction along the path.
  - (b) A chord v_i ~ v_j with j >= i+2 would give d(v_j) <= i+1, a contradiction.
  - (c) An open shortcut site would give d(v_j) <= i+2 < j. An open corner u would have d(u) = k, so u would be in
    P(v_{k+1}); its smaller direction index would make it the parent instead of v_k, contradicting the tree path.
- Lemma 2. T is infinite and locally finite, so by Konig's lemma it has an infinite ray. Take y = v_{N+1}. It is in
  E(gamma): the NAW property gives the adjacency conditions, and y is open while F is closed. The tail of the ray
  is an open self-avoiding path that avoids gamma u F.
- Lemma 3 and Corollary.
  - A_gamma depends only on gamma u F, which consists of N+1+|F| distinct sites (Lemma 0).
  - B_{gamma,y} depends only on sites outside gamma u F, and it lies inside {|C(y)| = infinity}.
  - Independence, the union bound and translation invariance give theta <= K_N theta. So K_N(p) < 1 implies
    theta(p) = 0, and then p_c >= p.
- Lemma 4 (sign flips).
  - At a turn, the corner test compares the axis of the incoming step with the axis of the outgoing step, which
    differ. So the test depends only on axes, and flips preserve axes.
  - The stabiliser of a walk is the set of flips of unused axes. So its orbit has 2^|A| elements, exactly one of
    which is canonical.
- Additional facts I proved and used in my fast enumerator; all are confirmed by agreement with the naive checker:
  - (i) Every F site is adjacent to some v_i with i < N, so the condition "y not in F" in E is redundant. Hence
    |E| equals the number of one-step NAW extensions, and sum_f c_f(N) = a_{N+1}.
  - (ii) Two distinct corners that are not in S never coincide, so |F| = |S| + (number of corners not in S).
  - (iii) For an axis permutation pi, |F_r(pi g)| = |F_{r o pi}(g)|, and |E| does not depend on the axis order.

## 2. My implementations (in skeptic/, written before reading code/ or outputs/)
- naive/main.go (Go, literal from the definitions).
  - Enumerates every NAW from 0, with all 6 first steps and no symmetry reduction.
  - At each leaf it computes S, C, F and E from the complete path, using dirindex on vectors.
  - It asserts Lemma 0 and, for N <= 10, the full NAW property.
  - A second mode enumerates all 6^N walks and filters them by the NAW definition.
- naive_py.py (Python): brute force over all 6^N walks, with literal definitions.
- fast/main.go (Go). Its structure is deliberately different from the author's sign-flip reduction.
  - It reduces by the full 48-element group of signed axis permutations. In the canonical form, axes are labelled
    in order of first use and the first step on each axis is positive.
  - At each leaf it evaluates all 6 axis orderings. It does this through counters n_ab of non-S corners, indexed by
    (in-axis, out-axis), and weights the result by w = 1, 4, 8 for |A| = 1, 2, 3.
  - Run-time asserts: no corner lies on the path; no two non-S corners coincide; the state is restored after every
    subtree.
  - It has a -nosym mode: all walks, standard order only, weight 1.
- kexact.py. Computes K_N(p) exactly with Python integers over the common denominator den^(N+1+fmax), and asserts
  equality with a separate Fraction evaluation.
- compare.py. Compares my table format with the author's TOTAL/EXT format entry by entry: N, the walk total, and
  every f, including zeros.

## 3. Comparisons
Every comparison matched exactly.

Agreement among my own implementations:
- naive_py and naive Go agree for N = 1..7. The text files differ only in line endings: Python writes CRLF on
  Windows.
- In naive Go, the NAW generator and the 6^N filter agree for N = 1..8.
- naive Go and fast (48-fold) agree for N = 1..13, all full tables. The naive N = 12 run took 66 min and the
  N = 13 run took 136 min; both ran in full.
- fast -nosym and fast 48-fold agree for N = 1..14.
- Hand check at N = 2: c_0 = 78 and c_1 = 48. Derivation: 6 straight walks each have |E| = 5; 24 turning walks
  each have |E| = 4, and half of them have a flagged corner. Both programs agree.
- Chain check on my own runs: sum_f c_f(N) equals my walk total a_{N+1} for N = 1..17. I did not compute a_19 or
  a_21 independently. For N = 18 and 20 I checked only that sum_f c_f equals the summed |E|.

My fast tables against the author's saved outputs/:
- N = 16, 18 and 20 all match. At N = 20: walk total 3516072837894, all 24 entries c_0..c_23 identical, and
  sum_f c_f = 14334995983614.
- My N = 20 run was exhaustive: 73255728350 canonical leaves under the 48-fold reduction, 38m56s, file fast/f20.txt.

The author's program, which I built from code/par (go1.26.4, binary in author_runs/):
- I ran it for N = 3..16, 18 and 20. Its tables match my fast tables at every one of these N, and my naive tables
  for N = 3..13.

Determinism and byte-for-byte reproduction:
- My reruns of the author's program at N = 16, 18 and 20 are byte-identical to outputs/p16.txt, outputs/p18.txt
  and outputs/p20.txt. For p20.txt the sha256 is 04bce75f...c989 in both. The N = 20 rerun took 8806 s on 6 cores,
  part of the time on a shared machine.
- I reran my own fast enumerator with the final binary and a different split depth:
  - N = 1..18: identical to the first runs.
  - N = 20 (split depth 8 instead of 9): byte-identical to my first N = 20 run. The leaf count was the same, and
    fast/f20.txt and fast/rerun/f20.txt share sha256 aa9634a8...084a.

The author's scripts, rerun on outputs/:
- code/verify_cert.py reproduces outputs/verify_N20.txt byte for byte.
- code/kcheck.py reproduces outputs/k20.txt (N = 20) and outputs/k18.txt (N = 18) byte for byte.

MANIFEST.sha256 (my copy):
- All 16 listed files are OK, and claim/ contains no unlisted files.
- I rechecked it at the end: still OK, so claim/ was not modified.

## 4. Review of the author's code (after my own numbers existed)
code/par/main.go implements the definitions faithfully. I found no defect.
- The shortcut test (adj > 0 and minIdx <= k-3) is the same first-neighbour-index rule I derived.
- The corner test (dp^1) < (di^1) is exactly dirindex(u - v_{k+1}) < dirindex(v_k - v_{k+1}).
- F is kept as a set, so nothing is counted twice, and flags are undone in LIFO order.
- E is counted at the leaf as sites with adj == 1 that are not in F.
- Each canonical sign-flip representative gets weight 2^|axes|.
- Each canonical 3-step prefix occurs exactly once among the 216 jobs.
- The 49^3 box holds walks up to N = 22.
- The results are integer sums, which do not depend on order.

## 5. Exact certificate
My own code, kexact.py, run on my N = 20 table, on the author's rerun file and on outputs/p20.txt:
- K_20(263376/10^6) < 1: TRUE, with K = 0.999971526024. Over the common denominator 10^264, 1 - K reduces to
  7432054542...677622981 / 2610121787...000000, about 2.8474e-5 > 0.
- K_20(263377/10^6) = 1.000041779030 > 1. This is consistent with the claim but not needed for validity.
- K_20(5/19) = 0.984758991853 < 1, K_20(1/5) = 0.005547, and f_max = 23. All three are as stated in PROOF.md
  section 4 and result/bound.json.
- The margin of 2.8e-5 is small. It is enough because the arithmetic is exact and two independent programs
  produced exactly the same integer counts.

## Discrepancies
None in the mathematics, the tables, the certificate, the determinism checks or the manifest.

The only differences seen were CRLF vs LF line endings in text-diff comparisons that involved Python output. Raw
byte comparison settled them: the author's saved check outputs are themselves CRLF, and they are byte-identical to
my reruns.

## Not checked (outside this role)
- Whether 0.263376 is strictly above every published rigorous lower bound, that is, the record. Neither the
  original 0.21103 nor the corrected 0.2522 was checked by me.
- The corrected CLAIM.md, table/literature_record.md and result/bound.json in the master folder. I did not read
  them.

confirmed_scope: I re-derived the PROOF.md argument step by step and found it correct. Two independent exhaustive
computations agree: my own enumerator, written from the definitions with a different symmetry reduction and run in
full at N = 20 twice, and the author's program, rerun at N = 20. Both reproduce the N = 20 table in outputs/p20.txt
exactly: all c_f and the walk total a_20 = 3516072837894. My enumerator also agrees with a literal no-symmetry
checker for every N <= 13. My own exact rational arithmetic gives K_20(263376/10^6) < 1, which implies
p_c^site(Z^3) >= 263376/10^6 = 0.263376. This says nothing about whether the bound beats the published record.

pass: true
