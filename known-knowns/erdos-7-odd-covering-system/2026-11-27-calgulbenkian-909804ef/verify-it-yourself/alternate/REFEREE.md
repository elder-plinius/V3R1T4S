# Referee report on the lower bound for an odd covering

The statement concerns finite families of residue classes covering the integers, with distinct odd moduli greater than one. The verified lower bound on their least common multiple is \(X=6\,557\,114\,959\,770\,375\). A global cell has Haar mass \(1/135\).

**Verdict on the numerical theorems.** Theorem A and Theorem 1 follow from the stated covering argument and the exact finite inequalities. I checked all those inequalities and the complete normalized partitions in the issued tables. The proof of Theorem A is internal to the document. All 28 named mathematical results have individual verdicts below. The reviewed manuscript has SHA-256 `567447b65f00261676133bc02c7202455d3f983c49907b659433babc75e623fe`.

## Lemma-by-lemma verdicts

| Manuscript item | Verdict | Reason |
|---|---|---|
| Lemma 1.1 | Correct | The common finite period partitions the digit space into fibers. Each tested residue class is a union of those fibers, including for unrestricted cap coordinates. |
| Lemma 1.2 | Correct | Pulling back the covering classes under digit truncation and adjoining unused coordinates preserves all moduli and covers the larger space. The stated implication is the contrapositive. |
| Lemma 2.1 | Correct | Restrict digit alphabets coordinatewise. A class either disappears or retains its depth vector. The surviving distinct depth vectors give distinct nonunit moduli. |
| Corollary 2.2 | Correct | The \(i\)-th support prime is at least the \(i\)-th odd prime. The comparison uses the original exponents as caps. |
| Proposition 2.3 | Correct | The eight-prime unrestricted cap dominates all smaller supports after replacement. The first fourteen odd primes already have product greater than \(X\). |
| Proposition 2.4 | Correct | The multiplier enumeration and a second recursion produce the same five sets. Each of their 6,782 vectors is dominated by an actually verified cap at its own rank. |
| Lemma 3.1, completion | Correct | Increasing order fixes all proper divisors permanently. A displaced cylinder lies wholly in one already fixed cylinder, which gives the asserted inclusion even for countably many changes. |
| Lemma 3.2, capped kernel | Correct | The total kernel mass equals \(\min(C H(G),1)\). The stated zero-density convention covers \(H(G)=0\). |
| Lemma 3.3, ordered increments | Correct | On each point the active partial sum is bounded by the full partial sum. Convexity increases each forward difference, and monotonicity makes the integrated differences nonnegative. |
| Lemma 3.4, cylinder comparison | Correct | The empty label case gives \(\mu(X)f(b)\le Sf(b)\). For positive label count the ordered increments telescope, including ties and a finite final atom. |
| Lemma 3.5, weighted aggregation | Correct | Add the slack to one residue and apply Jensen to the distribution with masses \(c_i/C\). The text handles \(C=0\) and empty data. |
| Lemma 3.6, first-hit accounting | Correct | A cylinder gets zero measure when its last coordinate is processed. Subsequent kernels have mass at most one, the total losses telescope, and changing the initial measure by a nonnegative measure can only increase each loss. |
| Lemma 3.7, nested comparison | Correct | Conditioning on the prefix freezes the live-label background. The measurable comparison weights depend only on the anchor. Backward iteration therefore applies with the previous coordinates still free. |
| Proposition 4.1, scalar criterion | Correct | Conditioning the anchor on the complements of the disjoint pure powers gives the stated cylinder mass bounds. The product of the height counts includes the pure shape exactly once. Applying the hinge to this inventory and using the lower bound on the initial mass gives \(B\ge1\) for every cover. |
| Section 4.2, scalar evaluation | Correct | The identity follows by writing \(u_+=u+(-u)_+\). Strictly below the kink only finitely many positive products contribute a correction. |
| Section 5.2, completion table | Correct | The largest proper-divisor sum is \(86/105\) at 105. For the single extra modulus \(15q_2\) the sum is \(3/5+1/q_2\le38/55\). Only finitely many mixed moduli have been added. |
| Lemma 5.1, normal form | Correct | After fixing the first pure cylinders, the stabilizer permutes the unmarked ternary depth-two nodes in each first-digit branch and the unmarked quinary columns. Its orbits on the admissible \(45\)-classes have the four stated signature components. The subsequent residue lists allow every coincidence compatible with disjointness. |
| Section 5.4, budget vertices | Correct | The quinary vertex at \((T e_k,T)\) has coefficient \(\epsilon/T\). Splitting the mass on column \(k\) between this vertex and \((T e_k,0)\) recovers the actual overlap. A zero total budget is a singleton. |
| Lemma 5.2, anchor reserve | Correct | Intersecting the union of mixed classes with the pure survivors gives the baseline \(135(1-\rho_3-\rho_5)\). The finer \(75\)-credit uses only the part outside the \(15\)- and \(45\)-classes. In a \(B\)-cell its surviving mass is \((1-z)(1/5-\epsilon)\). The overlap \(\epsilon\) is measured relative to the whole column. |
| Section 5.6, geometric maximum properties | Correct | Moving two pieces of one coefficient back to a common residue is weighted aggregation. The positive part is 1-Lipschitz, and the positive-baseline case maximizes each linear section separately. |
| Lemma 5.3, anchor comparison | Correct | Inside a live cell the comparison measure factors. Applying the cylinder bound successively with the actual total mass in the column and row gives precisely the two zero-level weights. At \(e_3=3\) the row is a singleton. The same residue is used for every cell when aggregating a category. |
| Lemma 6.1, load | Correct | Subadditivity of Haar measure and \(C_q/n_q=1/\beta_q\) give the displayed loss bound. |
| Lemma 6.2, padding at 7 | Correct | Enlarge the labels already present to exactly \(s\) distinct digits outside the pure first digit. Higher pure powers may overlap those digits. Both the union upper bound and the surviving-mass upper bound still apply to the same kernel. |
| Proposition 6.3, stage 7 | Correct | A fixed pair of anchor exponents contributes total normalized weight at most one. Removing its exponent-one class subtracts precisely \(n_7/7\) for each of the four specified pairs. |
| Lemma 6.4, later stages | Correct | The terms with zero anchor depth have normalized total at most \(M-1\), since a pure class is excluded. Only \(15q_2\) is reserved at the second later prime. Its depth in the coordinate 7 is zero at every multiplier. Removing its exact weight from category 15 leaves a nonnegative coefficient. Other later stages retain all their free coefficients. |
| Theorem 7.1, comparison of reserve and losses | Correct | The ordered inequalities are \(R\le\nu_0(Y_0)\le\sum_i L_i^+\le\sum_i\mathrm{Fine}_i\). |
| Lemma 7.2, budget vertices | Correct | The fine loss is separately convex in the ternary and quinary budgets, the reserve separately affine. Applying concavity of their difference twice, with the actual discrete data fixed, gives a vertex with nonpositive surplus for any cover. The sums are finite by the first moments of the geometric laws. |
| Lemma 8.0, ordinary envelope | Correct | With \(0\le a_x\le1\), the mass plus linear load at height \((u,v)\) is at most \(8\lvert K\rvert(1+u)(1+v)\), which is integrable under the product level masses. The tail subtraction is therefore defined. For \(m\ge\tau\) the maximum is exactly affine. For smaller \(m\) the omitted linear load is an upper bound. |
| Lemma 8.1, row implies the covered vertices | Correct | Enlarging the core and its nonnegative weights upper-bounds every loss. Dropping reserve credits gives a lower bound. For the last phase the leaf designates the same residue \(\eta\) in both channels, including the fixed-channel contribution at multiplier one. The ordinary and coarse omitted-height estimates have the required upper sign. |
| Theorem 8.2, complete anchored certificate | Correct | A covering gives a nonpositive budget vertex with fixed discrete data by Lemma 7.2. Completeness and Lemma 8.1 give strict positivity at exactly that vertex with its actual \(\eta\). |
| Theorem A, eight-prime exclusion | Correct | The normalized cap has exactly the first eight odd primes, all unrestricted. The actual A8 inputs prove its exclusion by Theorem 8.2. Corollary 2.2 replaces any smaller support by the first primes, and Lemma 1.2 embeds that support into the eight unrestricted caps. This establishes the stated lower bound of nine on the number of distinct primes. |
| Theorem 1, lower bound on the period | Correct | For ranks nine through thirteen, replace the support primes without increasing the period and compare to an excluded cap at the same rank. At rank fourteen the squarefree kernel alone exceeds the target. At lower ranks Theorem A applies. The comparison is strict on input periods below the target, giving the claimed weak lower bound. |

## Direct scalar check

The scalar verifier constructs the entire finite distribution, including its upper tail. If \(\Pr(T\ge j)=(a/b)p^{-j}\) for \(1\le j\le e\), the integer weights of \(1+T\), on denominator \(bp^e\), are
\[
 bp^e-a p^{e-1},\quad a(p-1)p^{e-j-1}\ (1\le j<e),\quad a.
\]
They are nonnegative and sum to \(bp^e\). Multiplicative convolution gives every atom of \(M\). The script sums \((\rho M-\delta)_+\) directly, with no upper-tail identity or floating point. The head uses \(a/b=(1-\rho)^{-1}\). [Scalar verifier](verify_scalar.py)

Every one of the 738 witness bounds matched its stored rational exactly. The greatest was \(130157612206585412852431229/130269519960832360564391936<1\). I also evaluated \(B\) at the actual exponents of every one of the 1,754 candidates. A dominating witness supplied the parameters when available. The remaining cases used the nearest supplied parameter vector in the same rank. This gave 1,736 direct strict exclusions, including 1,467 at ten primes and 247 at eleven primes. The 18 remaining vectors have exactly the 13 maximal elements used for the anchored check. This calculation makes no assertion about optimal distortion parameters on those 18 vectors.

## The finite numerical reduction

**Correct.** Suppose the actual support is \(q_1<\cdots<q_r\), with exponents \(e_i\). Write \(p_i\) for the \(i\)-th odd prime. Then \(p_i\le q_i\) gives \(\prod p_i^{e_i}\le L\). To enumerate all possibilities below \(X\), put \(K_r=\prod p_i\) and factor in turn every integer \(m\) between 1 and \(\lfloor(X-1)/K_r\rfloor\). Keep \(m\) precisely when its factors belong to these \(r\) primes and return \(e_i=1+v_{p_i}(m)\). Every vector occurs exactly once. A separate recursion that added factors in nondecreasing order returned exactly the same sets of vectors.

| \(r\) | \(K_r\) | Largest multiplier tested | Distinct vectors |
|---:|---:|---:|---:|
| 9 | 3,234,846,615 | 2,027,024 | 5,028 |
| 10 | 100,280,245,065 | 65,387 | 1,484 |
| 11 | 3,710,369,067,405 | 1,767 | 248 |
| 12 | 152,125,131,763,605 | 43 | 21 |
| 13 | 6,541,380,665,835,015 | 1 | 1 |
| 14 | 307,444,891,294,245,705 | 0 | 0 |

**Correct.** A cover with smaller coordinate exponents lifts to any coordinatewise larger caps by taking inverse images under digit truncations. The classes keep their distinct shapes. It suffices to exclude each of the dominating models, even when the product of that model's own prime powers exceeds \(X\).

**Correct.** The 23 nine-prime models cover all 5,028 vectors. I recomputed the reserve and seven-stage loss sum at all 736 basic vertices by two calculations. One splits the four deeper residue choices between the modulo-9 subtrees. The other aligns the deeper ternary choices in a full modulo-9 block in each first-digit branch and optimizes the quinary columns using convexity. The least reserve minus loss is \(7353010244456360618611/457648694712387914811075>0\). The latter calculation and its proof are included. [Nine-prime checker](verify_nine.py) · [Geometric argument](BASIC-CHECK.md)

**Correct.** Twelve of the finite ten- and eleven-prime anchored models close at all 32 basic vertices. In the remaining ten-prime model with caps \((4,3,2,2,1,1,1,1,1,1)\), 28 basic vertices and 280 mixed vertices close. I independently generated the hierarchy and all 692 pairs of exact reserves and loss sums, including the individual losses at each published minimum. The least surplus is \(31892572639/133917433650\) global cells.

## Which quantities the executable checks

The nine data files total 5,604,948 bytes. The largest has 939,982 bytes. The issued manifest has SHA-256 `909804ef2bf322270ec686552d0952780851e07d3c8471cbfac58507b3c715d6`. All files were read as plain text and their exact byte lengths and digests were recomputed.

| Data | Required assertion | Independent result |
|---|---|---|
| `thmA_8p.part01.tsv` through `part06.tsv` | The eight caps are unrestricted on the first eight odd primes. Every normalized branch closes and every recomputed \(R>S\). | 28,057 exact rows. The least \(R-S\) is between 0.00200370 and 0.00200371 global cells. |
| `nine_finite.tsv` | Each of the 23 models closes all 32 basic vertices. Each length-nine exponent vector of period below \(X\) is dominated by a verified model. | 736 exact rows and all 5,028 vectors dominated. |
| `scalar_lemma_u.tsv` | For each cap on the specified prime list, the computed \(B\) equals its record and \(B<1\). | 738 equalities and strict inequalities. |
| `global_anchored.tsv` | An anchored model closes at every vertex for each residual cap on its own prime list. | 692 exact rows, 13 maximal residual caps, 18 residual vectors covered. |

For Theorem A there are 16 basic rows, 4 basic rows with the modulus-75 reserve credit, 604 mixed, 25,840 coarse, 1,003 spatial, 506 with a fixed ternary-budget row, and 84 with a modulus-165 projection. The last 84 are arranged as seven projections at each of twelve remaining vertices. For a fixed one of those residues, only the stage at eleven is changed. On each explicit height and multiplier below \(\tau_{11}\), keep the normalized \(n_{11}/11\) offset on that residue and remove the same weight from the free modulus-15 coefficient. The same residue applies in both channels. The envelope releases the offset for larger multipliers and omitted levels. The loss from stage seven is padded and all stages beyond eleven use their first-hit bounds. These formulas reproduce every row. A single fixed row establishes positivity at its projection. Its six siblings are essential to the coverage test. The least surplus over the full table occurs in a mixed row with key \((2,4,1,7,1,1,1,1,-1)\).

The principal checker binds a scalar model's rank both to the number of primes and to the cap-vector length. Domination is tested only at the matching dimension. At seven, a coarse omitted-height bound charges just the residual linear load, so it needs \(\tau_7-1-n_7/7\ge0\). The principal verifier tests this condition on all anchored headers. The proof requires it only when a coarse row occurs. Its padded rows require the weaker threshold of one. For scalar rows the format check \(\delta_i\ge\rho_i\) is stronger than Proposition 4.1 requires and holds on the supplied data. No sign or unit conversion is used to compare a printed decimal. Both operands of each strict comparison are rational numbers.

The full alternate program uses a separate implementation of the reserve, losses, geometric maximization and leaf traversal. Its geometric kernel checks that the fixed offset within each residue modulo 45 is constant on the positive-weight cells and that the same ternary child maximizes the weight in every column of that band. It then computes an exact maximum by splitting the four deeper residues over the bands. For both the principal and alternate geometric implementations, I also compared the values with direct maximization over 61,710 residue assignments in 18 small tests, including complete anchor cores with selected coefficients zero. [Full alternate verifier](check_alternate.py) · [Derivation and build instructions](ALTERNATE.md)

The issued 83,167-byte principal verifier (SHA-256 `139cfb5dcb10e70d1f53936a8f2b0c0267c423ac7ede5181e034797d9cced859`) printed `PASS` in 425.55 seconds using one process and its default package directory. The full alternate verifier on the issued manifest printed `PASS` in 14.48 seconds. Recomputing the scalar part alone with `python3 verify_scalar.py certs` took 1.00 second. The basic-only Python verifier accepts both the issued nine-prime table and the companion JSON. The issued model with \(e_3=12\) integrates height \(u=9\) explicitly. The companion uses the ordinary upper bound on that one finite endpoint. The other models agree, and the two files have the same least surplus. [Independent nine-prime check](verify_nine.py)

## Scope of the theorem

I compared the 23 printed F9 caps and 13 printed G caps individually with the corresponding table headers. The longer ternary cutoff belongs to F9_15. G08 is the model that uses mixed rows. The scalar counts by rank are 603, 120, 14 and one. Every stated orientation margin agrees at the published precision.

**Correct.** The enumeration requires exclusion of all 5,028 nine-prime vectors of product below \(X\). Some larger products are excluded as well. For example, \((1,1,1,1,1,1,1,1,6)\) has product \(66{,}350{,}420{,}912{,}410{,}635>X\) and is dominated by F9_01 and F9_02. At the boundary, \((5,3,2,2,2,1,1,1,1)\) has product exactly \(X\) and is undominated. The manuscript correctly states that unrestricted nine-prime support and the existence question remain open. Formal verification of this lemma chain also remains open.


I checked the optional attribution to the author preprint against its title page, Theorem 1.1, Corollary 1.3 and equation (1.3). They give the nine-prime statement, the older bound \(9{,}704{,}539{,}845\), and the same six thresholds for the unrestricted eight-prime model. The package supplies the premises of Theorem A through its own eight-prime certificate. [Author preprint](https://doi.org/10.5281/zenodo.22759614)

The two additional preprints cited as background report the stated results. Mian and Siddique give the lower bound \(L>10{,}000\). Dai, Li, Li and Yi give \(45\mid L\) and a least modulus at most nine. Neither enters the proof reviewed above. [Mian and Siddique](https://arxiv.org/abs/2607.25628) · [Dai, Li, Li and Yi](https://arxiv.org/abs/2611.15110)
