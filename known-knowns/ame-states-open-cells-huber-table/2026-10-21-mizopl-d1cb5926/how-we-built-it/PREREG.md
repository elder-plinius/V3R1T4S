# Pre-Registration — `AME(17, 8)` (`[[17, 0, 9]]_8`, Huber–Wyderka Table)

- **Target:** `known-knowns/ame-states-open-cells-huber-table`
- **Package ID:** `2026-10-21-mizopl-d1cb5926`
- **Claimed cell (single cell per `kit/SUBMIT.md` §1):** `AME(17, 8)` ($n = 17$ parties, local dimension $D = 8 = 2^3 \in \{2..10\}$, pure quantum MDS stabilizer code `[[17, 0, 9]]_8`).

## 1. Falsifiable Hypothesis & Pass/Fail Criterion

We test whether there exists a pure Schlingemann–Werner graph state $|\Gamma\rangle \in (\mathbb{C}^8)^{\otimes 17}$ over $\mathbb{F}_8 = \mathbb{F}_2[w]/(w^3 + w + 1)$ with symmetric hollow circulant adjacency matrix $\Gamma \in \mathbb{F}_8^{17 \times 17}$ such that:
1. For **every** 8-element subset $S \subset \{0, \dots, 16\}$ across all $\binom{17}{8} = 24,310$ eight-party cuts (with zero sampling and no symmetry omission in the final verifier), the $8 \times 9$ off-diagonal submatrix $\Gamma_{S, S^c}$ has full rank $\operatorname{rank}_{\mathbb{F}_8}(\Gamma_{S, S^c}) = 8$.
2. Equivalently, after expanding $\Gamma$ via the self-dual normal trace-orthonormal basis $\{w^3, w^6, w^5\} = \{w+1, w^2+1, w^2+w+1\}$ of $\mathbb{F}_8 / \mathbb{F}_2$ into a $51 \times 51$ binary symmetric hollow adjacency matrix $B_{51} \in \mathbb{F}_2^{51 \times 51}$, for all $\binom{17}{8} = 24,310$ eight-qudit (`24`-qubit vs `27`-qubit) cuts, the $24 \times 27$ submatrix $(B_{51})_{Q(S), Q(S^c)}$ has full rank $\operatorname{rank}_{\mathbb{F}_2}((B_{51})_{Q(S), Q(S^c)}) = 24$.

Any single cut $S$ with $\operatorname{rank}_{\mathbb{F}_8}(\Gamma_{S, S^c}) < 8$ (or $\operatorname{rank}_{\mathbb{F}_2}((B_{51})_{Q(S), Q(S^c)}) < 24$) falsifies the candidate immediately.

## 2. Pre-Registered Null & Mutant Controls

1. **Random symmetric 17-circulant null benchmark (`400` random draws over $\mathbb{F}_8^8$, `seed=42`):**
   Sample $400$ independent chord vectors $c \in \mathbb{F}_8^8$ uniformly at random and evaluate the exact number of full-rank cuts out of $24,310$.
2. **Single-entry & single-chord mutation controls:**
   Verify that zeroing a single symmetric edge ($\Gamma_{0,1} = \Gamma_{1,0} \leftarrow 0$) or zeroing a single chord ($a_1 \leftarrow 0$) causes `verify.py` to detect rank-deficient cuts (`184` and `918` bad cuts, respectively).
