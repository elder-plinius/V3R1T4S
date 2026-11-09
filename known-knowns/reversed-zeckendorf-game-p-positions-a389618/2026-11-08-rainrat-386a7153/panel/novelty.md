# Novelty Skeptic Report — `reversed-zeckendorf-game-p-positions-a389618`

context: subagent

## 1. Primary Status & Table Fetch

Per the 7-day source-cache rule, the primary OEIS status pages (`A389618`, `A389617`, `A389619`, fetched once honestly via `curl` at `2026-11-08T01:14:31Z`, HTTP `200`) and sequence b-files (`b389618.txt`, `b389617.txt`, `b389619.txt`, fetched once honestly via `curl` at `2026-11-08T01:15:19Z`, HTTP `200`) recorded in `the-record-we-beat/snapshot.md` were verified:

- **`https://oeis.org/A389618`** (Numbers $n$ for which player 2 has a winning strategy in the Reversed Zeckendorf Game with $n$ pieces):
  - Snapshot recorded in `the-record-we-beat/snapshot.md` (`A389618.html`, fetched `2026-11-08T01:14:31Z`, HTTP `200`): SHA-256 `f939a8eadbae5e50daec69187e8a51314689260214ccdc6406c50f0e47398515`.
- **`https://oeis.org/A389618/b389618.txt`**:
  - Snapshot recorded in `the-record-we-beat/snapshot.md` (`b389618.txt`, fetched `2026-11-08T01:15:19Z`, HTTP `200`): SHA-256 `888ff71b7705af8e5894e47ca06460c2253b75a84670a7e789e352b3d46f0b85`
  - Quoted terminal entries: `45 120`, `46 121`, `47 124`, `48 128`, `49 129` (stops at $a(49) = 129$; 49 terms covering $2 \le n \le 129$).
- **`https://oeis.org/A389617/b389617.txt`** (Number of edges in the DAG of the Reversed Zeckendorf Game with $n$ pieces):
  - Snapshot recorded in `the-record-we-beat/snapshot.md` (`b389617.txt`, fetched `2026-11-08T01:15:19Z`, HTTP `200`; `A389617.html` fetched `2026-11-08T01:14:31Z`, HTTP `200`, SHA-256 `8b4cc38591080d2d251489f39a8225e14565162bfe1a39184981523d073da2ed`): SHA-256 `379cfc0a8465153f52bf3f677e48a91189008d8027bb1bd56e9168d1609e70f1`
  - Quoted terminal entries: `61 49794`, `62 53971`, `63 58458`, `64 63222`, `65 68351` (stops at $n = 65$ with $68,351$ edges on OEIS; Table A1 of `arXiv:2309.12748v2` tabulates up to $n = 129$ with $384,715$ vertices and $2,945,040$ edges).
- **`https://oeis.org/A389619/b389619.txt`** (Numbers $n$ for which player 1 has a winning strategy in the Reversed Zeckendorf Game with $n$ pieces):
  - Snapshot recorded in `the-record-we-beat/snapshot.md` (`b389619.txt`, fetched `2026-11-08T01:15:19Z`, HTTP `200`; `A389619.html` fetched `2026-11-08T01:14:31Z`, HTTP `200`, SHA-256 `8f354c8cf74f3dc5c349310b746e093c9514041ca1ca30a3f7cac4e02f6e6ed4`): SHA-256 `2500c5d5cab045f7d62f99977d2140dcd4525c8a9c5183c89b68efdc86a70868`
  - Quoted terminal entries: `76 122`, `77 123`, `78 125`, `79 126`, `80 127` (stops at $a(80) = 127$; 79 terms in $2 \le n \le 129$ plus $a(1) = 1$).

## 2. Literature, Repository, and PR/Issue Search

1. **Literature and Web (last 24 months)**:
   - Zoë X. Batterman, Aditya Jambhale, Steven J. Miller, Akash L. Narayanan, Kishan Sharma, Andrew K. Yang, and Chris Yao, *"The Reversed Zeckendorf Game"*, `arXiv:2309.12748v2` (and *The Fibonacci Quarterly* 63:2, 2025, pp. 215–239) is the sole primary paper studying this game. Its Table A1 (documented in `the-record-we-beat/snapshot.md`, ground-truth TSV SHA-256 `cea0c77942d3e7c3cc127fb8370da12d4075cc8a6b3dedc71a5ad297ee8361f6`) tabulates outcomes, DAG vertex counts, and DAG edge counts for $2 \le n \le 129$. Appendix B notes a 24-hour timing test at $n = 144$ without publishing its outcome, vertex count, or edge count.
   - OEIS sequences `A389617`, `A389618`, and `A389619` (added December 2025) contain no entries beyond $n = 65$ (`A389617`) and $n = 129$ (`A389618`, `A389619`).
   - Web and literature searches for `"Reversed Zeckendorf Game"`, `"A389618"`, `"A389617"`, `"A389619"`, and `"2309.12748"` confirm no subsequent paper, preprint, or code release has published outcomes or edge counts for $n \ge 130$.
2. **Repository & Pull Requests / Issues**:
   - Checked `TROPHY_CASE.md` and all subdirectories in `known-knowns/`: no prior entry or result exists for the Reversed Zeckendorf Game or `A389617`–`A389619`.
   - Checked all open and closed pull requests, issues, and releases in the `V3R1T4S` repository: the only match is closed PR `#851`, which proposed the target definition in `bank/targets.json` and solved only up to $n = 65$ during bank review. No solution PR or issue exists for $n \ge 130$.

## 3. Comparison with Published Data and Non-Triviality Analysis

- **Claimed Object**: `object/reversed_zeckendorf_n2_250.tsv` (SHA-256 `386a7153a5f084483101a9b9a1eab089f072a8106234535c4bf2b896beab82c1`, 250 lines covering $2 \le n \le 250$).
- **Reproduction & Strict Extension**:
  - For $2 \le n \le 129$, the table reproduces all 128 rows of Table A1 of `arXiv:2309.12748v2` (49 Player-2 wins matching `A389618`, 79 Player-1 wins matching `A389619`, and exact vertex and edge counts matching `A389617` and Table A1 through $n = 129$ with $384,715$ vertices and $2,945,040$ edges).
  - For $130 \le n \le 250$, it provides 121 new contiguous rows of exact 1st/2nd-player outcomes (30 new Player-2 wins for `A389618`: $n \in \{131, 136, 137, 142, 146, 152, 156, 157, 165, 166, 167, 173, 174, 175, 190, 197, 205, 206, 212, 220, 221, 225, 228, 231, 233, 234, 238, 240, 244, 245\}$; and 91 new Player-1 wins for `A389619`), exact DAG vertex counts (`A003107(n)` reaching $21,890,964$ at $n = 250$), and exact DAG edge counts (`A389617` reaching $209,975,689$ edges at $n = 250$). In total for `A389617`, 185 edge counts ($66 \le n \le 250$) extend the OEIS `b389617.txt` listing ($n \le 65$), while 121 ($130 \le n \le 250$) go beyond Table A1 of `arXiv:2309.12748v2` ($n \le 129$).
- **Why Trivial Edits Cannot Produce This Extension**:
  - **Distinction between DAG edge counts and normal-play outcomes**: For the DAG edge counts (`A389617`), this work proves a closed-form Fibonacci-partition convolution $A389617(n) = \sum_{i \ge 2}\bigl(A003107(n - F_i) + A003107(n - 2F_i)\bigr)$ by bijecting each Split move at bin $i \ge 2$ with partitions of $n - F_i$ and each Combine move producing $2F_i$ ($i \ge 2$) with partitions of $n - 2F_i$. By contrast, the 1st/2nd-player normal-play outcomes (`A389618` and `A389619`) have no known closed-form recurrence or trivial propagation rule across general $n$ and require full retrograde DAG evaluation.
  - **Non-monotonic outcome flips under $n \mapsto n + 1$**: Eliminating $h_1 = n - \sum_{i \ge 2} h_i F_i$ parameterizes states by higher-bin tuples $(h_2, h_3, \dots)$ with weighted sum $m = \sum_{i \ge 2} h_i F_i \le n$, making $V(G_n)$ an induced subgraph of $V(G_{n+1})$. However, incrementing $n \mapsto n + 1$ both introduces a new boundary layer of states ($m = n + 1$) and increases $h_1 = n - m$ by $1$ at every existing state, which enables new $F_1$-consuming Combine moves ($i = 2$: $F_1 + F_3 \mapsto 2F_2$, and $i = 3$: $F_1 + F_4 \mapsto 2F_3$, whenever $h_1 = n - m$ crosses from $0$ to $1$). Enabling outgoing transitions from previously constrained states flips their normal-play win/loss (N/P) labels non-monotonically and cascades upstream through the DAG. For example, the state with $h_3 = 1$ and all other higher counts zero ($m = 3$) has $h_1 = 0$ at $n = 3$—where its only legal move is the Split $F_3 \mapsto F_1 + F_2$ into a winning state, making it a P-position (Player 2 wins at $n = 3$)—whereas at $n = 4$ it has $h_1 = 1$, enabling the new Combine move $F_1 + F_3 \mapsto 2F_2$ into a P-position and flipping the very same higher-bin state $(h_3 = 1)$ to an N-position.
  - **Inapplicability of closed-form families to general $n \in [130, 250]$**: While Theorem 1.1 of Zoë X. Batterman et al. proves Player 1 wins for the sparse family $n = F_{i+1} + F_{i-2}$ (which covers only a single integer in $[130, 250]$, namely $n = F_{11} + F_8 = 144 + 34 = 178$), no closed-form recurrence, propagation rule, deletion, restriction, relabelling, or symmetry determines the normal-play outcomes for general $n \in [130, 250]$. Determining them requires full retrograde DAG evaluation across up to $2.189 \times 10^7$ states and $2.100 \times 10^8$ directed transitions per $n$.

The claimed table strictly beats the published frontier ($n = 129$ in `arXiv:2309.12748v2` and `A389618`/`A389619`, $n = 65$ in `A389617`) across the entire contiguous range $130 \le n \le 250$, fulfilling Branch B of the target.

pass: true
