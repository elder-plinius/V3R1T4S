context: subagent

# Novelty Panel Report — `non-attacking-queens-game-nimbers-a344227`

## 1. Scope of Novelty Audit

As the NOVELTY panelist, I inspected `claim/claim.md`, `claim/REPRODUCE.md`, `claim/result/toroidal_queens_and_margins.json`, and every primary-source status snapshot stored in `claim/data/` (`claim/data/A344227.json`, `claim/data/A344227.html`, `claim/data/queens-n18-paper.md`, `claim/data/conjecture-theory.md`, `claim/data/submission-package.md`, `claim/data/verification-RESULTS.md`, `claim/data/queens-nimbers-commits.json`, `claim/data/queens-nimbers-tree.json`, `claim/data/othello-winning-geometry-n20.md`, `claim/data/othello-cgt-laws-and-tricks.md`, `claim/data/othello-almost-mirror-method.md`, `claim/data/othello-refutation_geometry.py`, `claim/data/arxiv-queens-kayles.xml`, and the GitHub search snapshots) to determine whether any of the claimed results:
- $G(TQ_{11} \dots TQ_{16}) = (1, 0, 1, 1, 1, 0)$ for Node-Kayles on the $n \times n$ toroidal queens graph $TQ_n$, specifically $G(TQ_{12}) = 0$ ($20/100$ winning replies in $H_{12}$), $G(TQ_{14}) = 1$ ($0/144$ winning replies in $H_{14}$, refuting Toroidal Conjecture T1), and $G(TQ_{16}) = 0$ ($196/196$ winning replies in $H_{16}$),
- the exact planar central-strike refutation margins on $R_n = Q_n \setminus N[c^*]$ at $n = 14$ ($140/144$, with the $4$ non-refuting replies $(4,7), (7,4), (7,8), (8,7)$ in $0$-based coordinates) and at $n = 16$ ($146/196$, with $146$ refuting and $50$ non-refuting replies),

were already known in prior literature, present in the repository snapshots, or trivially derivable from a known theorem or simple construction.

---

## 2. Prior State in Status Snapshots (`claim/data/`)

### 2.1 OEIS A344227 (`claim/data/A344227.json`, `claim/data/A344227.html`, `claim/data/submission-package.md`)
- OEIS A344227 (revision 72, last modified August 23, 2026) catalogues planar Non-Attacking Queens Sprague-Grundy values $a(0) \dots a(17) = 0, 1, 1, 2, 1, 3, 1, 2, 3, 1, 0, 1, 0, 1, 0, 1, 0, 2$.
- Its comments note the elementary proof that on any vertex-transitive graph (such as the toroidal queens graph $TQ_n$), the Sprague-Grundy value must be either $0$ or $1$, because every opening move leaves an isomorphic residual graph $H_n = TQ_n \setminus N[(0,0)]$.
- However, OEIS A344227 lists **no values** of $G(TQ_n)$ for any $n$, does not have a cross-referenced OEIS entry for toroidal queens (`claim/data/submission-package.md` Section 9 explicitly notes that torus-queens nimbers are *"Not yet in OEIS"* and computed only to $n = 10$), and does not mention planar central-strike refutation margins $R_n$.

### 2.2 Toroidal Queens Nimbers and Conjecture T1 (`claim/data/queens-n18-paper.md`, `claim/data/othello-cgt-laws-and-tricks.md`)
- In `claim/data/queens-n18-paper.md` (Section 6.7, lines 898–913) and `claim/data/othello-cgt-laws-and-tricks.md` (Section 2.4, lines 185–200), Rudd computes $G(TQ_n)$ **only for $n = 1 \dots 10$**:
  $$G(TQ_1 \dots TQ_{10}) = (1, 1, 1, 0, 1, 0, 1, 0, 1, 0).$$
- Based on $n = 1 \dots 10$, Rudd formulates **Conjecture T1**: *"For $n \ge 4$, $G(\text{torus}_n) = n \bmod 2$."*
- Neither `claim/data/queens-n18-paper.md`, nor `claim/data/othello-cgt-laws-and-tricks.md`, nor any commit or file in `claim/data/queens-nimbers-tree.json` or `claim/data/queens-nimbers-commits.json` contains $G(TQ_n)$ for any $n \ge 11$.
- Furthermore, Rudd repeatedly treats Conjecture T1 as likely true (e.g., `claim/data/queens-n18-paper.md` line 206: *"the torus game collapses to a parity law while all n-dependent difficulty concentrates at the border"*). Thus, the discovery that $G(TQ_{14}) = 1 \ne 14 \bmod 2$ refutes Conjecture T1 at an even $n$ and reverses the author's expectation in the prior literature.

### 2.3 Planar Central-Strike Refutation Margins $R_{14}$ and $R_{16}$ (`claim/data/queens-n18-paper.md`, `claim/data/othello-winning-geometry-n20.md`, `claim/data/othello-refutation_geometry.py`)
- In `claim/data/queens-n18-paper.md` (Section 6.6, lines 846–853; Section 9, lines 1182–1183) and `claim/data/othello-winning-geometry-n20.md` (Section 0, line 63; Section 1.6, lines 188–197; Section 3.4, lines 417–418), the central-strike refutation margin on $R_n = Q_n \setminus N[c^*]$ is computed **only for $n = 8$ ($0/36$), $n = 10$ ($8/64$), and $n = 12$ ($100/100$)** (along with $0/256$ at $n = 18$ where $R_{18}$ is a P-position).
- The script `claim/data/othello-refutation_geometry.py` (line 177) loops solely over `for n in [8, 10, 12]:`.
- The margins at $n = 14$ and $n = 16$ are explicitly registered as open questions in the paper (`claim/data/queens-n18-paper.md` line 850: *"the margins at n = 14 and 16 are the cheap missing data points"*; `claim/data/othello-winning-geometry-n20.md` line 194: *"Deferred (one cheap engine run each): the margins at n=14, 16"*).

### 2.4 Other Literature and Snapshots (`claim/data/arxiv-queens-kayles.xml`, `claim/data/conjecture-theory.md`, `claim/data/verification-RESULTS.md`)
- Jenrich (arXiv:1312.5135, 2013/2014) determined planar win/loss outcomes for $n \le 16$, without computing toroidal values $G(TQ_n)$ for $n \ge 11$ or the ply-2 refutation margins on $R_{14}$ and $R_{16}$.
- Noon & Van Brummelen (2006), Noon (2002), Fan (2021), and Dailly–Gledel–Heinrich (arXiv:1709.05219, in `claim/data/arxiv-queens-kayles.xml`) do not contain $G(TQ_{11} \dots TQ_{16})$ or the $R_{14}, R_{16}$ refutation margins.

---

## 3. Check for Triviality or Known Structural Theorems

Could $G(TQ_{12}) = 0$, $G(TQ_{14}) = 1$, $G(TQ_{16}) = 0$, or the margins $140/144$ on $R_{14}$ and $146/196$ on $R_{16}$ follow trivially from a known symmetry, pairing construction, or graph theorem?

1. **Odd vs. Even Toroidal Boards**:
   - On odd toroidal boards $TQ_n$ ($n$ odd), placing the first queen at $(0,0)$ removes its row, column, and both wrapped diagonals. Under the point reflection $\rho(r,c) = (-r \bmod n, -c \bmod n)$ fixing $(0,0)$, a vertex $(r,c) \ne (0,0)$ is self-mirroring (adjacent to $(-r,-c)$ in $TQ_n$) if and only if $2r \equiv 0$, $2c \equiv 0$, $2(r-c) \equiv 0$, or $2(r+c) \equiv 0 \pmod n$. Since $\gcd(2,n) = 1$ for odd $n$, those conditions reduce to $r \equiv 0$, $c \equiv 0$, $r \equiv c$, or $r \equiv -c \pmod n$—which are precisely the closed neighborhood $N[(0,0)]$ deleted by the first move. Therefore, for odd $n$, the residual $H_n = TQ_n \setminus N[(0,0)]$ has no self-mirroring vertices under $\rho$, so Player 1 has an immediate $\rho$-mirror pairing strategy on $H_n$, proving $G(H_n) = 0$ and $G(TQ_n) = 1$ for all odd $n$ (and $0$ winning replies for Player 2 in $H_n$).
   - Crucially, the claim does **not** rest on odd $n$: both the target `success_criterion` (clause 3) and `partial_wins` (`p1`) specifically require **even** toroidal boards ($n = 12, 14, 16$, testing the even half of Conjecture T1 and finding an even-$n$ counterexample).
   - For **even** $n$, $\gcd(2,n) = 2$, so the congruences $2r \equiv 0$, $2c \equiv 0$, $2(r-c) \equiv 0$, $2(r+c) \equiv 0 \pmod n$ have non-trivial solutions $r = n/2$, $c = n/2$, $r - c \equiv n/2$, and $r + c \equiv n/2 \pmod n$ that survive in $H_n = TQ_n \setminus N[(0,0)]$. As noted in `claim/data/othello-cgt-laws-and-tricks.md` (Section 7, line 386), *"all natural involutions on the even torus are fully self-mirroring (checked for translations, glides, point reflections)"*. No static involution or Closed-Pairing (Theorem S1) argument resolves even $TQ_n$. [Update 2026-11-23: a later run (`2026-11-22-2234`) sketched a pairing construction for toroidal $n$ divisible by four. It is a sketch with no novelty claim and does not cover $n \equiv 2 \bmod 4$, including the $n=14$ counterexample; this panel's conclusion concerns only the computed values $n=12,14,16$.]
2. **Non-triviality of $G(TQ_{12}) = 0$, $G(TQ_{14}) = 1$, $G(TQ_{16}) = 0$**:
   - The winning-reply fractions in $H_n$ for even $n = 4, 6, 8, 10, 12, 14, 16$ are $4/4, 16/16, 36/36, 8/64, 20/100, 0/144, 196/196$.
   - This irregular sequence ($100\%, 100\%, 100\%, 12.5\%, 20\%, 0\%, 100\%$) shows that the even toroidal outcomes are governed by deep game-tree interaction rather than any simple formula or local invariant. In particular, certifying $G(TQ_{14}) = 1$ requires refuting all $21$ $D_4((0,0))$ orbits of $H_{14}$ ($144$ live squares) via an adaptive ply-3 response table whose residuals each have $69$–$71$ live squares and require full game-tree search.
3. **Non-triviality of Planar Refutation Margins $140/144$ ($R_{14}$) and $146/196$ ($R_{16}$)**:
   - On planar boards $Q_{14}$ ($196$ squares, $R_{14}$ has $144$ live squares) and $Q_{16}$ ($256$ squares, $R_{16}$ has $196$ live squares), determining the exact count of legal replies in $R_n$ that leave a P-position requires solving all $72$ (at $n=14$) and $98$ (at $n=16$) $\sigma$-symmetry classes of ply-2 subgames on boards with up to $144$ and $196$ live squares. No known theorem predicts the $140/144$ and $146/196$ margins. [Correction 2026-11-23: this report originally said $78$ and $105$; direct enumeration of the $\sigma(r,c)=(c,r)$ fold used by the margin solver gives $(144+0)/2=72$ and $(196+0)/2=98$, because $c^*$ and its attacks leave no live main-diagonal square in either $R_n$.]

---

## 4. Conclusion

The claimed results—the exact toroidal Sprague-Grundy values $G(TQ_{12}) = 0$, $G(TQ_{14}) = 1$ (an explicit even-$n$ counterexample refuting Rudd's Toroidal Conjecture T1), and $G(TQ_{16}) = 0$, together with the exact planar central-strike refutation margins $140/144$ on $R_{14}$ and $146/196$ on $R_{16}$—are genuinely novel, are not present in any prior literature or status snapshot in `claim/data/`, and are not derivable by any trivial construction or known theorem. Both `partial_wins` (`p1`) and full `success_criterion` clause (3) of `non-attacking-queens-game-nimbers-a344227` are newly established.

pass: true
