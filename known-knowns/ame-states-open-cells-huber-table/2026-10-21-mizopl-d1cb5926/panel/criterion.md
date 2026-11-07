---
panel_role: criterion
context: independent cold-check skeptic session (fresh process, bank criterion and cut-rank audit)
verdict: PASS
date: 2026-11-07
target_id: ame-states-open-cells-huber-table
run_id: 2026-10-21-mizopl-d1cb5926
---

# Criterion Skeptic Report — `PASS`

## 1. Alignment With `bank/known-knowns/ame-states-open-cells-huber-table/` and `kit/SUBMIT.md`

1. **In-range table coordinates ($D \in \{2..10\}$):**
   The Huber–Wyderka online table (`https://tp.nt.uni-siegen.de/ame/table.html`) tabulates $n$-partite local dimensions $D = 2..10$. Our claimed cell has $n = 17$ parties and local dimension $D = 8 \in \{2..10\}$, where cell $(n = 17, D = 8)$ is **Blank** (`<td></td>`). All out-of-range cells with $D \ge 11$ have been removed.
2. **One cell per package (`kit/SUBMIT.md` §1):**
   This package (`known-knowns/ame-states-open-cells-huber-table/2026-10-21-mizopl-d1cb5926/`) contains exactly one claimed cell (`AME(17, 8)`) and one certificate file (`object/ame_17_8_pure_circulant_certificate.json`, `4,176` bytes, `sha256: 0bc632480b2bfb3a90117f0676e8894dc5972ea32cb315cd47e1d04077f20a28`).
3. **Mathematical equivalence between Schlingemann–Werner $\mathbb{F}_8$ cut rank and $\operatorname{AME}(17, 8)$:**
   By Schlingemann & Werner (*Phys. Rev. A* 65, 012308, 2001) and Helwig *et al.* (*Phys. Rev. A* 86, 052335, 2012), a graph state $|\Gamma\rangle \in (\mathbb{C}^q)^{\otimes n}$ over a finite field $\mathbb{F}_q$ ($q = 8 = 2^3$) with symmetric hollow adjacency matrix $\Gamma \in \mathbb{F}_8^{17 \times 17}$ is an $\operatorname{AME}(17, 8)$ state (and a pure `[[17, 0, 9]]_8` quantum MDS stabilizer code achieving the quantum Singleton bound $d = \lfloor 17/2 \rfloor + 1 = 9$) if and only if for every subset $S \subset \{0, \dots, 16\}$ of size $|S| = \lfloor 17/2 \rfloor = 8$, the $8 \times 9$ off-diagonal submatrix $\Gamma_{S, S^c}$ has full rank $8$ over $\mathbb{F}_8$.
4. **Independent $51$-qubit binary trace-symplectic graph-state verification:**
   To avoid relying solely on $\mathbb{F}_8$ arithmetic, `verify-it-yourself/verify.py` also expands $\Gamma$ via the $\mathbb{F}_8 / \mathbb{F}_2$ trace map $\operatorname{Tr}(x) = x + x^2 + x^4$ in the self-dual normal trace-orthonormal basis $\{w^3, w^6, w^5\} = \{w+1, w^2+1, w^2+w+1\}$ into a $51 \times 51$ binary symmetric hollow graph-state adjacency matrix $B_{51} \in \mathbb{F}_2^{51 \times 51}$, and checks directly over $\mathbb{F}_2$ that for all $\binom{17}{8} = 24,310$ eight-qudit (`24`-qubit vs `27`-qubit) partitions, the $24 \times 27$ submatrix $(B_{51})_{Q(S), Q(S^c)}$ has full $\mathbb{F}_2$-rank `24`, certifying $S(\rho_S) = 24$ bits ($8$ octits of maximal entanglement) across every $8$-party cut.

pass: true
