# Results: Hadamard Maximal Determinant Records (`hadamard-maxdet-records`)

## 1. Summary of New All-Time Full-Win Records ($n = 105, 109, 117$)

We constructed and dual-verified (exact fraction-free Bareiss + multi-prime CRT) three explicit $n \times n$ $\{-1, +1\}$ matrices for $n \in \{105, 109, 117\}$ that **strictly exceed all standing records** across Orrick's MaxDet archive (`indiana.edu/~maxdet`), Rokicki's `newrec.html`, `Math-AI-Caltech/hadamard-maxdet`, `calgulbenkian`'s unmerged fork branches (`#66`, `#67`), and merged V3R1T4S PR `#155`:

| Order $n$ | Previous Literature Record $D_{\text{rec}}$ (Rokicki) | `calgulbenkian` / PR `#155` | **New Record $D_{\text{norm}} = \|\det X\|/2^{n-1}$ (This Work)** | Gain vs Literature | Gain vs `cg` / `#155` | Barba Ratio $R$ | Artifact File |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **$105$** | $\approx 263.955 \cdot 26^{51}$ (`3847437472...625`) | $276 \cdot 26^{51}$ (`#66`, unmerged) | **$\mathbf{277 \cdot 26^{51}}$** (`403757419044975201959422423846994970270257858463738130848861743562151165952`) | **`1.049419x`** | **`+1 \cdot 26^{51}`** (`1.003623x`) | `0.736942` | `results/M105_403757419044975201959422423846994970270257858463738130848861743562151165952.txt` |
| **$109$** | $\approx 257.808 \cdot 27^{53}$ (`1877483841...352`) | $291 \cdot 27^{53}$ (PR `#155`, merged) | **$\mathbf{297 \cdot 27^{53}}$** (`2162897555231082049798834993796033279114137960386362436200469570917630303164899`) | **`1.152019x`** | **`+6 \cdot 27^{53}`** (`1.020619x`) | `0.746729` | `results/M109_2162897555231082049798834993796033279114137960386362436200469570917630303164899.txt` |
| **$117$** | $\approx 318.084 \cdot 29^{57}$ (`7231499425...615`) | $324 \cdot 29^{57}$ (`#67`, unmerged) | **$\mathbf{325 \cdot 29^{57}}$** (`73887205478246242985652874268409752933911041846892660492861670872395821475850942725425`) | **`1.021741x`** | **`+1 \cdot 29^{57}`** (`1.003086x`) | `0.734188` | `results/M117_73887205478246242985652874268409752933911041846892660492861670872395821475850942725425.txt` |

### Construction Details
- **$n = 105$ (`277 * 26^51`)**: Constructed via 1/2/3-flip steepest ascent + Basin Hopping (`tools/fast_maxdet_search.c`) on the Paley Class I Hadamard matrix $H_{104}$ ($p = 103 \equiv 3 \pmod 4$) and also independently realized on the Kronecker–Williamson Hadamard matrix $H_2 \otimes H_{52}$, reaching Hadamard excess $\Sigma(H_{104}) = 1004$ and normalized determinant factor $26 + 1004/4 = \mathbf{277}$ (just 1 step below the Cauchy–Schwarz ceiling $\lfloor 26(1+\sqrt{104})\rfloor = 278$).
- **$n = 109$ (`297 * 27^53`)**: Constructed via the Orrick–Solomon 3-normalized construction (`tools/os_3norm_search.c`, `arXiv:math/0311292`) on the Paley Class I Hadamard matrix $H_{108}$ ($p = 107 \equiv 3 \pmod 4$) at triple $r = (0, 1, 2)$, $s = (1, 1, 1)$, achieving residual excess $E_{3..107} = 972$ and normalized determinant factor $2(27) + 972/4 = \mathbf{297}$, exceeding the Cauchy–Schwarz ceiling ($294$) of standard single-row Hadamard bordering and beating merged PR `#155` ($291 \cdot 27^{53}$) by $+6 \cdot 27^{53}$. (We also found `295 * 27^53` on Williamson $m=27$ and `293 * 27^53` on Paley Class II $q=53$.)
- **$n = 117$ (`325 * 29^57`)**: Constructed via the Orrick–Solomon 3-normalized construction (`tools/os_3norm_search.c`) on a symmetric-circulant Williamson Hadamard matrix $H_{116}$ ($m = 29$, block sums $9^2+5^2+3^2+1^2 = 116$) at triple $r = (0, 97, 100)$, $s = (1, -1, -1)$, achieving residual excess $E_{3..115} = 1068$ and normalized determinant factor $2(29) + 1068/4 = \mathbf{325}$.

---

## 2. Partial Win (`p2`) Frozen Gram Certificates ($n = 49, 81$)

We verified and proved global optimality in the 1- and 2-border congruent families for the two odd-square Frozen Gram Target (`p2`) certificates:

| Order $n$ | Previous Record $D_{\text{rec}}$ | **$\sqrt{\det G}/2^{n-1}$ (`p2`)** | Gain vs Record | Realized Rows $M_0$ | Rational Congruence $Q Q^T = G$ & $P(n I_n)P^T = G$ | Artifact File |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **$49 = 7^2$** | $96 \cdot 12^{23}$ (`635974777627126753067532288`) | **$\mathbf{116 \cdot 12^{23}}$** (`768469522966111493289934848`) | **`1.208333x`** | $48 \ge 47$ rows (`[1_48, H_48]`) | $Q_{\text{den}} = 6$, $P_{\text{den}} = 42$ ($P = Q/7$) | `results/G49_p2.json` |
| **$81 = 9^2$** | $196 \cdot 20^{39}$ (`107752139522048000...000`) | **$\mathbf{252 \cdot 20^{39}}$** (`138538465099776000...000`) | **`1.285714x`** | $80 \ge 79$ rows (`[1_80, H_80]`) | $Q_{\text{den}} = 10$, $P_{\text{den}} = 90$ ($P = Q/9$) | `results/G81_p2.json` |

---

## 3. Audit of `calgulbenkian` Branches & SHA-256 Receipts

All 5 branches in `cg_repo.git` pass exact Bareiss + CRT verification against `data/maxdet_table.json` and `Math-AI-Caltech/hadamard-maxdet` (which only covers $n \in \{51, 103, 107, 111, 115, 119\}$). For all three Full-Win orders ($n=105, 109, 117$), our new matrices strictly supersede `calgulbenkian`'s matrices.

### SHA-256 Checksums of Canonical Artifacts in `results/`
```text
dd1e1520b87d97fe404bf0857235652e04d819a08484c85fd3e024fb1346d28b  results/M105_403757419044975201959422423846994970270257858463738130848861743562151165952.txt
fe44093142381fa403c5bc471d6639775c6a3d4f5150f3ee70519e646ed1425e  results/M109_2162897555231082049798834993796033279114137960386362436200469570917630303164899.txt
fb62d553933dd6bdc7f5539d03b59092c1e624f47a382e4363b30499eb051bf5  results/M117_73887205478246242985652874268409752933911041846892660492861670872395821475850942725425.txt
cd7ea151cb23cea573fc617f983c2ce21a340dda94ec30baf82c4180c170e347  results/G49_p2.json
03b380a2074785deac39cb19b68c0853cd52ea469f7b848600cc756df42c8992  results/G81_p2.json
```
