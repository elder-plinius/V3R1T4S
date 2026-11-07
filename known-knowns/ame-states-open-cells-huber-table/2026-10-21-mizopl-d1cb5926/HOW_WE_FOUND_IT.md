# How We Found `AME(17, 8)` (`[[17, 0, 9]]_8`) — *(contributor text, unverified)*

> **Note:** *This narrative is contributor text, unverified; all verified claims rest solely on `object/ame_17_8_pure_circulant_certificate.json` and `verify-it-yourself/verify.py`.*

## 1. Why Characteristic-$2$ Dimension $D = 8 = 2^3$ Required a New Construction

In the Huber–Wyderka online table of Absolutely Maximally Entangled states (`https://tp.nt.uni-siegen.de/ame/table.html`, local dimensions $D \in \{2..10\}$), column $D = 8$ lists `Yes` for $n = 2..14$ and `No` for $n \ge 18$ (`#8_18`), while rows $n = 15$, $n = 16$, and $n = 17$ are **Blank** (`<td></td>`).

For **odd** prime powers $q$ ($\operatorname{char}(\mathbb{F}_q) \ne 2$), Ball (*J. Phys. A* 53, 2020, `arXiv:1907.04391`) and `arXiv:2609.11796` (Sep 2026) construct $\operatorname{AME}(2q-1, q)$ and $\operatorname{AME}(2q, q)$ using quadratic-residue / extended Cauchy structures, which rely on $-1$ and $2$ being invertible or having quadratic character in odd characteristic. For $D = 8 = 2^3$, however, $\mathbb{F}_8 = \mathbb{F}_2[w]/(w^3 + w + 1)$ has characteristic $2$ ($1 + 1 = 0$, and the squaring map $x \mapsto x^2$ is a Frobenius automorphism rather than a two-to-one quadratic character). Consequently, neither Ball (2020) nor `arXiv:2609.11796` nor Bidav (`arXiv:2608.05781`, Aug 2026) covers $D = 8, n = 17$.

## 2. Dihedral $D_{17}$ Orbit Filtration over $\mathbb{F}_8$ Palindromic 17-Circulants

We formulated the search for `AME(17, 8)` as a pure Schlingemann–Werner graph state $|\Gamma\rangle \in (\mathbb{C}^8)^{\otimes 17}$ whose $17 \times 17$ symmetric hollow adjacency matrix $\Gamma \in \mathbb{F}_8^{17 \times 17}$ is circulant under $\mathbb{Z}_{17}$:
$$\Gamma_{i,j} = a_{\min((j-i)\bmod 17, \, (i-j)\bmod 17)} \quad (i \ne j), \qquad \Gamma_{i,i} = 0,$$
parameterized by the $8$ chord weights $a = (a_1, a_2, a_3, a_4, a_5, a_6, a_7, a_8) \in \mathbb{F}_8^8$.

1. **Diagonal $\mathbb{F}_8^\times$ Normalization & Frobenius Reduction:**
   Global multiplication by $\lambda \in \mathbb{F}_8^\times$ preserves the rank of every submatrix $\Gamma_{S, S^c}$, allowing $a_1 = 1$ without loss of generality and reducing the space from $8^8 = 16,777,216$ to $8^7 = 2,097,152$ normalized chord vectors (further quotiented by $3\times$ under the Frobenius automorphism $x \mapsto x^2$).
2. **Exact $750$-Orbit $D_{17}$ Sieve Followed by Full $24,310$-Cut Verification:**
   Because $\Gamma$ is invariant under cyclic shifts $i \mapsto i + s \pmod{17}$ and reflection $i \mapsto -i \pmod{17}$, the dihedral group $D_{17}$ of order $34$ partitions all $\binom{17}{8} = 24,310$ eight-party cuts into exactly $750$ orbits (whose orbit sizes sum to $24,310$). Ordering those $750$ orbit representatives by failure rate (starting with the contiguous cut $S = \{0, 1, 2, 3, 4, 5, 6, 7\}$) prunes almost all candidates within the first $12$ cuts.
3. **The Certificate (`object/ame_17_8_pure_circulant_certificate.json`):**
   This search isolated the palindromic chord vector:
   $$a = (1, 2, 5, 1, 5, 2, 2, 2) = (1, w, w^2+1, 1, w^2+1, w, w, w) \in \mathbb{F}_8^8,$$
   with first circulant row:
   $$\Gamma_{0, :} = [0, 1, 2, 5, 1, 5, 2, 2, 2, 2, 2, 2, 5, 1, 5, 2, 1].$$
   Direct verification across all $\binom{17}{8} = 24,310$ eight-party cuts over $\mathbb{F}_8$ (`0.40s`) and across all $24,310$ eight-qudit (`24`-qubit) cuts of the $51$-qubit binary trace-symplectic graph state $[I_{51} \mid B_{51}]$ over $\mathbb{F}_2$ (`0.66s`) confirms `24,310 / 24,310` full-rank cuts (`0` rank-deficient cuts).
