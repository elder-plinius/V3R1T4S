context: subagent (fresh session)

# Novelty skeptic report: three-heap-wythoff-fraenkel-a1-11 (A_1 = 12)

## Verdict
The claim that both of Fraenkel's three-heap Wythoff conjectures hold for smallest heap $A_1 = 12$ (while also re-verifying $0 \le m \le 11$ and the $A_1 = 11$ prerequisite) is **novel** relative to all published literature, code, `TROPHY_CASE.md`, `known-knowns/`, and open/closed PRs and issues in `elder-plinius/V3R1T4S`. It strictly advances the frontier beyond Sun & Zeilberger ($A_1 \le 10$) and open PR #1117 ($A_1 = 11$), is not derivable by trivial edits from smaller $A_1$, and properly credits PR #1117.

## 1. Live primary status source (single honest fetch, no retries)
- **URL**: https://library.slmath.org/books/Book71/files/GONC6-04.pdf
- **UTC fetch time**: `2026-11-25T07:19:48Z`
- **HTTP status**: `200`
- **SHA-256**: `cc1b985ef7fa16d79877677a49b59eb65924a6d082341ae53348544c22cde1f1`
- **Problem A4(53) summary (pp. 61–62, Richard J. Nowakowski, *Unsolved Problems in Combinatorial Games*, *Games of No Chance 6*, MSRI Publ. 71, 2025)**:
  - Defines the $N$-heap Wythoff game ($N \ge 2$, sorted heaps $p_1 \le \dots \le p_N$; remove from a single heap or remove $(a_1, \dots, a_N)$ with $0 \le a_i \le p_i$, $\sum a_i > 0$, $a_1 \oplus \dots \oplus a_N = 0$).
  - States Fraenkel's **Conjecture 1** (for fixed $K = (A_1, \dots, A_{N-2})$, from some $m(K)$ on, $A_n^{N-1} = \operatorname{mex}(\{A_i^{N-1}, A_i^N : 0 \le i < n\} \cup T)$ and $A_n^N = A_n^{N-1} + n$) and **Conjecture 2** ($A_n^{N-1} = \lfloor n\phi \rfloor + \varepsilon_n + a$ with $\varepsilon_n \in \{-1, 0, 1\}$ for $n \ge M(K)$).
  - Summarizes Fraenkel & Krieger [49] (2004), who proved Conjecture 1 implies Conjecture 2 and established structural results for $N = 3$.
  - Reports the state of the art via Sun & Zeilberger [139] (*Ann. Comb.* 8 (2004), 225–238): *"the conjectures are true for the case $N = 3$, where the first heap has up to 10 tokens. For those 10 cases, the parameter values $m, M, a, T$ were listed in a table."* Also cites Sun [138] (*Discrete Math.* 300 (2005), 180–195) for similar results and a method to compute $a$.
  - Records **no proof** for $A_1 = 11$, $A_1 = 12$, any $A_1 > 10$, or general $A_1$.
- **Companion page check**: `https://sites.math.rutgers.edu/~zeilberg/mamarim/mamarimhtml/wythoff.html` still states: *"Here we prove Fraenkel's conjectures for three piles, with the smallest pile of size less than eleven."*

## 2. Repository, `TROPHY_CASE.md`, `known-knowns/`, PRs, issues, and releases
- `TROPHY_CASE.md`: lists 53 rows across 7 families (degree-diameter graphs, constant-weight codes, Lehmer's totient problem, matrix multiplication, cipher challenges, VNN-COMP 2026, RobustBench CIFAR-100). Zero entries mention Wythoff or Fraenkel.
- `known-knowns/`: contains 33 family folders; `grep` for `wythoff` / `fraenkel` found zero matches.
- Releases in `elder-plinius/V3R1T4S`: none (`gh release list` returned no releases).
- Issues in `elder-plinius/V3R1T4S`: zero issues matching `wythoff`, `fraenkel`, `three-heap`, or `a1`.
- Pull requests in `elder-plinius/V3R1T4S` (searched all PRs and inspected the 100 most recent PRs up to #1244):
  - Only **PR #1117** (state: `OPEN`, created `2026-11-17T05:36:16Z`, https://github.com/elder-plinius/V3R1T4S/pull/1117) targets `three-heap-wythoff-fraenkel-a1-11`.
  - PR #1117 proves **only $A_1 = 11$** (via Sun & Zeilberger Claims 3.4–3.5 with $n_2 = 1216, n_1 = 3249, \alpha = -61, N_1 = N_2 = 1214, N_3 = 1381$) and explicitly states under *Not claimed*: *"Fraenkel's 3-heap Wythoff conjectures for general `A_1 >= 12` (or `N >= 4` heaps) remain open."*
  - No open, closed, or merged PR claims $A_1 = 12$ or any $A_1 \ge 12$.

## 3. Literature and code search (last 24 months: 2024–2026)
- **arXiv API** (`all:wythoff AND all:fraenkel`, `all:"three-heap" AND all:wythoff`, `all:"N-heap" AND all:wythoff`, and recent 25 `all:wythoff` submissions):
  - `arXiv:2602.17735` (*The Golden Sieve*, Cloitre, Feb 2026): self-referential deletion sieves and Fraenkel complementary partitions; unrelated to 3-heap XOR Wythoff.
  - `arXiv:2512.11601` (*Variants of Wythoff game with terminal positions or blocking maneuvers*, Dec 2025): 2-pile Wythoff variants via Walnut automata; does not address 3-heap XOR Wythoff.
  - `arXiv:2412.08399` (*3 dimensional Wythoff Nim*, Akiyama, Dec 2024): defines a different 3-pile Wythoff Nim variant with degree-5 algebraic slopes, not Fraenkel's nim-sum-zero 3-heap game.
  - Other 2025–2026 Wythoff hits (`arXiv:2610.30427`, `arXiv:2605.01435`, `arXiv:2510.11767`) study 2-pile remoteness, terminal sets, or Hofstadter G-sequence variants.
- **OpenAlex citation graph**:
  - Sun & Zeilberger (2004) (`W2123291723`, 19 returned citations) has no citations after 2020; Sun (2005) (`W2030358070`, 7 citations) has no citations after 2017.
- **Crossref (2024–2026)** and **Web search**:
  - *International Journal of Game Theory* (2025, `10.1007/s00182-025-00953-3`, Mignoty, Renard, Rigo, Whiteland, *Automatic proofs in combinatorial game theory*) uses Walnut on 2-pile Wythoff/Fraenkel variants, not 3-heap XOR Wythoff.
  - *Discrete Mathematics* (2026, `10.1016/j.disc.2026.115183`) treats quadratic-irrational Beatty sequences.
  - *Games of No Chance 6* (2025) includes *Lexicographic Wythoff* and *m-modular Wythoff*, plus Nowakowski's Problem A4(53) confirming only $A_1 \le 10$.
- **Integers** (Volumes 24–26, 2024–2026): checked `vol24.html`–`vol26.html`; only *Wythoff's Game with a Pass* appears, unrelated to Fraenkel's 3-heap conjectures.
- **GitHub code & repos** (`gh search repos "wythoff fraenkel"`, `gh search code "three-heap-wythoff"`, `gh search code "wythoff_a1"`): no external implementations or proofs beyond `elder-plinius/V3R1T4S`'s own `known-unknowns/graphs-games-automata/three-heap-wythoff-fraenkel-a1-11.md` and `README.md`.

## 4. Distinctness from $A_1 \le 10$ and PR #1117 ($A_1 = 11$), and credit check
- **Non-triviality / strict advance**:
  - The bank criterion in `known-unknowns/graphs-games-automata/three-heap-wythoff-fraenkel-a1-11.md` states: *"CONFIRMED: both of Fraenkel's conjectures for N = 3 with smallest heap A1 = 11 (or any larger single value, once 11 is done)."*
  - $A_1 = 12$ is a genuinely distinct layer that cannot be derived from $A_1 \le 10$ or $A_1 = 11$ (PR #1117) by deletion, restriction, relabelling, symmetry, local polish, or a propagation rule. Under the nim-sum-zero move condition $d_1 \oplus d_2 \oplus d_3 = 0$, each layer $m$ has its own irregular early $P$-positions, shifted offset, missing-gap set, and modulo-$p(m)$ XOR ray witnesses:
    - $m = 11$ (PR #1117): $T^{11} = \{1, 7, 11, 13, 17, 21, 23\}$, $|S^{11}| = 40$ ($\max = 1252$), $\alpha^{11} = -61$, $(N_1, N_2, N_3) = (1214, 1214, 1381)$, $B_{N_3} = 1420$, $(n_2, n_1) = (1216, 3249)$.
    - $m = 12$ (`claim/wythoff_a1_12_certificate.json`): $T^{12} = \{0, 8, 9, 18, 22, 24\}$, $|S^{12}| = 43$ ($\max = 105$), $\alpha^{12} = -67$, $(N_1, N_2, N_3) = (64, 352, 988)$, $B_{N_3} = 1030$, $(n_2, n_1) = (601, 1762)$, with 43 newly constructed modulo-16 XOR ray-witness tables across $[2851, 2867]$.
  - Because $A_1 = 12$ relies on the verified invariants ($T^i, \alpha^i, N_3^i, B_{N_3^i}, B_{N_3^i+1}$) of all prior layers $0 \le i \le 11$, the claim independently recomputes and verifies $m = 0..11$ (matching PR #1117's $m = 11$ constants $T, S, \alpha, N_1, N_2, N_3, B_{N_3}, B_{N_3+1}, n_1$, while taking $n_2 = 1990$ instead of $1216$) and proves $m = 12$ both under the half-sum Claim 3.5 convention and via a self-contained Lemma 2.6 direct induction (`claim/PROOF.md`) that avoids the p. 235 midpoint typo.
- **Proper crediting of PR #1117**:
  - `claim/CLAIM.md` explicitly credits open PR #1117 twice (for the $A_1 = 11$ prerequisite that is independently verified here, and for the half-sum convention matching Table 1 and PR #1117), and `claim/pr-1117.json` records PR #1117's metadata (`number: 1117`, `state: OPEN`, URL `https://github.com/elder-plinius/V3R1T4S/pull/1117`).
  - Minor non-blocking note: when assembling the final submission package, including a dedicated `Credits` section listing Fraenkel, Fraenkel & Krieger, Sun & Zeilberger, Nowakowski, and PR #1117 (https://github.com/elder-plinius/V3R1T4S/pull/1117) together would make attribution even clearer.

## Limits
- Searches of arXiv, Crossref, OpenAlex, *Integers* (Vols. 24–26), GitHub, and web search found no published proof for $A_1 = 12$ or general $A_1 \ge 12$; as with any literature search, this establishes absence of evidence in indexed sources rather than an impossibility proof of an unindexed preprint.
- Novelty assessment only; independent computational re-verification of the $A_1 = 12$ certificate is the responsibility of the criterion/reproduce skeptics.

pass: true
