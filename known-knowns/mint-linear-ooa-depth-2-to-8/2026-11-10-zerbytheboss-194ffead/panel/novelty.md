# Skeptic Panel — NOVELTY

context: fresh research subagent invoked with zero solver history (role: NOVELTY)
target_id: mint-linear-ooa-depth-2-to-8
claimed_object: object/ooa_b3_T2_m8_s8_k7.tsv (sha256 194ffead9a4b890088a7fd74dcaacdeb200e2b6f22f70081d38b141a6503e025)
claimed_cell: b = 3 (F_3), T = 2, m = 8, s = 8
claimed_value: linear OOA(3^8, 8, F_3, 2, 7) (strength k = 7, t = m - k = 1; dual [(8, 2), 8, 8]-NRT code over F_3 with d_RT = 8)

## 1. Live MinT Status and Saved Snapshot Verification

I verified both the saved raw MinT HTML snapshot and an independent single honest HTTP GET request (no browser-imitating headers, no retries) against the live MinT server (`KNOWN` / `PROVED-HERE`):

| Source | URL | UTC Fetch Time | HTTP | Bytes | SHA-256 | Extracted Entry |
|---|---|---|---|---|---|---|
| Live MinT cell query (independent panel fetch) | `http://mint.sbg.ac.at/query.php?i=x&b=3&s=8&m=8&p=smt&de=2` | `2026-11-10T18:41:31Z` | `200` | `8336` | `5aed6c5b2410094646d736a48515f8241cf76491caeafc8be5a0719482cb9dcf` | Constructive and linear: `OOA(3^8, 8, F_3, 2, 8-2)` (`t = 2`, `k = 6`); Lower bound on `t`: `OOA(3^8, 8, S_3, 2, 8-1)` (`t >= 1`, `k <= 7`); DB footer `2024-09-05` |
| Package snapshot (`the-record-we-beat/mint_b3_T2_m8_s8_snapshot.md`) | `http://mint.sbg.ac.at/query.php?i=x&b=3&s=8&m=8&p=smt&de=2` | `2026-11-10T18:30:43Z` | `200` | `8336` | `5aed6c5b2410094646d736a48515f8241cf76491caeafc8be5a0719482cb9dcf` | Byte-identical HTML (`8336` bytes) |
| Saved overview table (`mode=cd&opt=bd`) | `http://mint.sbg.ac.at/table.php?i=x&b=3&col=1&mode=cd&opt=bd&de=2&p=smt&minx=1&maxx=20&miny=0&maxy=15` | `2026-11-10T18:30:44Z` | `200` | `41568` | `f9ed86586695a5a120ca499a43d5bd53e99de174806290b493b3739c05473ef8` | Cell `(m = 8, s = 8)` anchor text `2-1` (constructive linear `t = 2`, linear lower bound `t = 1`) |
| Live MinT depth-3 cell (`de=3`, propagation check) | `http://mint.sbg.ac.at/query.php?i=x&b=3&s=8&m=8&p=smt&de=3` | `2026-11-10T18:44:40Z` | `200` | — | `eae41b741d117b288cdbdd25f34ffa5b0cae009d804f48b8dca13aff6d91c48f` | Constructive and linear `t = 2` (`k = 6`); Lower bound `t >= 2` (`M >= 59049 / 8 > 3^8`, LP bound `[id=225561]`) |
| Live MinT digital-net cell (`de=net`, propagation check) | `http://mint.sbg.ac.at/query.php?i=x&b=3&s=8&m=8&p=smt&de=net` | `2026-11-10T18:44:41Z` | `200` | — | `dcd352f81cab10b13d533c58c9963179e5ef2a3c3a000676c0030bc9b46c260b` | Constructive digital `(2, 8, 8)`-net; Lower bound `t >= 2` (no `(1, 8, 8)`-net in base 3, `[id=129151]`) |

Exact entries verified against the raw HTML of `query.php?i=x&b=3&s=8&m=8&p=smt&de=2`:
- **Constructive and linear** (`KNOWN`): `OOA(3^8, 8, F_3, 2, 8-2) over F_3 — Constructive and linear` — `Linear OOA(3^8, 8, F_3, 2, 6) (dual of [(8, 2), 8, 7]-NRT-code), using extended algebraic-geometric NRT-code AG_e(2;F,9P) [id=880683] based on function field F/F_3 with g(F) = 2 and N(F) >= 8`.
- **Lower bound on `t`** (`KNOWN`): `OOA(3^8, 8, S_3, 2, 8-1) in Base 3 — Lower bound on t` — `There is no OOA(3^8, 8, S_3, 2, 8), because the generalized Rao or (dual) Hamming bound shows that M >= 7457 > 3^8 [id=73393]`.
- **Independent Rao sphere-volume derivation** (`PROVED-HERE`): In `(F_3^2)^8`, a single depth-2 block over `F_3` has Rosenbloom-Tsfasman weight enumerator `1 + 2x + 6x^2`. Expanding `(1 + 2x + 6x^2)^8 = 1 + 16x + 160x^2 + 1120x^3 + 6160x^4 + ...`, the radius-4 NRT ball has exact cardinality `1 + 16 + 160 + 1120 + 6160 = 7457 > 3^8 = 6561`, ruling out `k = 8` (`t = 0`) even for nonlinear arrays over `S_3`.

The claimed array achieves `k = 7` (`t = 1`), strictly exceeding MinT's constructive linear value `k = 6` (`t = 2`) by `+1` and meeting the Rao upper bound `k <= 7` (`t >= 1`).

## 2. Target Exclusions, Repository (`TROPHY_CASE.md`, `known-knowns/`), and Pull Requests

1. **Target exclusions** (`PROVED-HERE`): Target `mint-linear-ooa-depth-2-to-8` excludes `(b, T, m, s) in {(2, 2, 6, 6), (2, 2, 8, 7), (2, 2, 8, 8)}` (all binary `b = 2`), and excludes digital nets `k <= T` (`mint-digital-nets-lower-t`). The claimed cell `(3, 2, 8, 8)` has ternary prime base `b = 3 != 2`, depth `2 <= T = 2 <= 8`, and strength `k = 7 > T = 2`.
2. **Repository check** (`PROVED-HERE`): Checked all 53 rows of `TROPHY_CASE.md` and all 31 directories under `known-knowns/`. Zero entries cover `mint-linear-ooa-depth-2-to-8`, ordered orthogonal arrays, or NRT codes.
3. **Open and closed PRs / issues** (`PROVED-HERE`): Searched `elder-plinius/V3R1T4S` issues and pull requests (open and closed) for `mint-linear-ooa`, `mint`, `mint.sbg.ac.at`, `OOA`, `ordered orthogonal`, `NRT`, and `Rosenbloom`. Zero open or closed PRs or issues target `mint-linear-ooa-depth-2-to-8` (the only MinT target PRs are `#875` and `#1006`, both for `mint-digital-nets-lower-t` on a binary `(11, 24, 17)`-net over `F_2`; PRs `#158`, `#711`, `#792`, `#806`, and `#823` belong to `codetables-binary-linear` and `cap-set-dim7-dim8`).

## 3. Neighbouring Cells, Propagation Rules, and Structural Equivalence Audit

I checked every propagation rule and algebraic lift that could trivially produce `(b, T, m, s) = (3, 2, 8, 8)` with `k = 7` from neighbouring cells or related code families:

1. **Block deletion (`s' = 9 -> s = 8` at `m = 8`)** (`KNOWN`): Requires `OOA(3^8, 9, F_3, 2, 7)` (`t' <= 1`). In MinT's `b = 3, T = 2` table, `(m = 8, s = 9)` has tight lower bound `t = 2` (`k <= 6`), so no such array exists.
2. **Dual NRT puncturing / OOA quotienting (`s' = 9, m' = 9, k' = 8` or `s' = 9, m' = 10, k' = 9`)** (`KNOWN`): Requires an ancestor at `s' = 9` with `t' = m' - k' <= 1`. In MinT, `(m = 9, s = 9)` has tight bound `t = 2`, and `(m = 10, s = 9)` has `3-2` (lower bound `t >= 2`), ruling out both ancestors.
3. **Row-count neighbours (`m = 7` and `m = 9` at `s = 8`)** (`PROVED-HERE`): At `(m = 7, s = 8)`, MinT has tight bound `t = 2` (`k = 5`). At `(m = 9, s = 8)`, MinT has `t = 2` (`k = 7`, dual `[(8, 2), 7, 8]`-NRT code of dimension `7`); moving from `m = 9` to `m = 8` requires enlarging a `7`-dimensional NRT code to an `8`-dimensional supercode while preserving `d_RT = 8`, which is the non-trivial direction (`(m = 8, s = 8, t = 1)` propagates upward to `(m = 9, s = 8, t = 2)`, not downward).
4. **Depth truncation from `T >= 3` or digital nets** (`KNOWN`): Live MinT queries for `de=3` and `de=net` at `(b = 3, m = 8, s = 8)` confirm that **no** `OOA(3^8, 8, S_3, T, 7)` exists for any `T >= 3` (even nonlinear), because the Martin-Stinson linear programming bound at `T = 3` proves `M >= 59049 / 8 = 7381.125 > 3^8 = 6561` (`[id=225561]`). Thus the claimed depth-2 array cannot arise by truncating any `(1, 8, 8)` digital net or higher-depth OOA.
5. **Classical Hamming-metric `[16, 8, d_H]_3` codes, self-dual NRT codes, and `GF(9)` GRS expansion** (`PROVED-HERE`):
   - By the ternary Griesmer bound, a linear `[n, 8, 8]_3` Hamming code requires `n >= 8 + 3 + 1 + 1 + 1 + 1 + 1 + 1 = 17 > 16` (the maximum Hamming distance of `[16, 8]_3` is `6`), so no Hamming code trivially induces `d_RT >= d_H = 8`.
   - Exhaustive enumeration of all `3^8 = 6561` codewords of the dual `[(8, 2), 8, 8]`-NRT code `H` in `object/ooa_b3_T2_m8_s8_k7.tsv` shows minimum Hamming weight `d_H = 5` (`6` codewords of Hamming weight `5`, `98` of weight `6`) and minimum NRT weight `d_RT = 8` (`366` codewords of NRT weight `8`), and confirms `H` is neither Euclidean self-dual nor NRT self-dual.
   - Exhaustive enumeration over all `4^7 = 16384` projective column-multiplier classes of `GF(9)` Generalized Reed-Solomon `[8, 4, 5]_9` codes expanded in an `F_3`-basis of `GF(9)` yields maximum NRT minimum distance `d_RT = 7` (`0` of `16384` achieve `d_RT >= 8`).

## 4. Coding-Theory and OOA Literature Audit (2008–2026)

I searched arXiv (`export.arxiv.org` API across `Rosenbloom-Tsfasman`, `ordered orthogonal array(s)`, `NRT metric`, `NRT codes`, `Hyperderivative Reed-Solomon`, and author queries) and journal indices covering 2008–2026, including the specific families named in the target traps:

1. **Algebraic-geometric and Hyperderivative Reed-Solomon NRT codes** (`KNOWN` / `PROVED-HERE`; Rosenbloom and Tsfasman, *Probl. Inf. Transm.* 33, 1997; Skriganov, *St. Petersburg Math. J.* 13, 2002; Niederreiter and Xing extended Goppa NRT codes; recent HRS NRT preprints `arXiv:2512.22948`, `arXiv:2601.03982`, `arXiv:2604.17864`, `arXiv:2607.19905`, `arXiv:2610.16643`):
   - Extended AG NRT codes `AG_e(T; F, rP)` on a curve `F / F_3` of genus `g` achieve `t <= g` using up to `s <= N_1(F)` rational places of degree `1`.
   - Over `F_3`, genus `g = 0` (`P^1(F_3)`, including Rosenbloom-Tsfasman Reed-Solomon and HRS codes) has `N_3(0) = 4` rational places (`t = 0` only for `s <= 4`).
   - By the Hasse-Weil bound, any genus `g = 1` curve over `F_3` has at most `N_3(1) <= 3 + 1 + floor(2 * sqrt(3)) = 7` rational places (`t = 1` only for `s <= 7`, matching MinT's `t = 1` entries at `m = 8, s = 5, 6, 7`). Reaching `s = 8` blocks via standard function-field NRT evaluation over `F_3` either increases the genus to `g = 2` (`N_3(2) = 8`, giving MinT's `t = 2` record `AG_e(2; F, 9P)`) or uses places of degree `>= 2` (each adding `deg(Q) - 1 >= 1` to `t`, again leaving `t >= 2`).
2. **LFSR-based OOA constructions** (`KNOWN`; Castoldi, Moura, Panario, and Stevens, *"Ordered Orthogonal Array Construction Using LFSR Sequences"*, *IEEE Trans. Inf. Theory* 63(2), 1336–1347, 2017 / `arXiv:2208.00333`, 2022, cited with a paraphrased title in `README.md`; Panario, Saaltink, Stevens, and Wevrick, `arXiv:1805.10350`; Castoldi, Monte Carmelo, Moura, Panario, and Stevens, *J. Combin. Designs* 31, 304–329, 2023 / `arXiv:2208.01410`, `arXiv:2208.01412`):
   - Both `arXiv:2208.00333` (primitive LFSRs) and `arXiv:1805.10350` (permissible non-primitive / reducible LFSRs) construct index-1 arrays `OOA(q^k, s, F_q, k, k)` (`m = k`, i.e., `t = 0` MDS NRT duals) from degree-`k` polynomials over `F_q` with `s <= q + 1` blocks (`(q + 1)k` columns). Over `F_3` (`q = 3`), they yield `t = 0` with at most `s <= 4` blocks—never `s = 8` blocks and never `t = 1` arrays such as `OOA(3^8, 8, F_3, 2, 7)` (where `t = 0` is impossible by `7457 > 6561`). The 2023 companion papers (`arXiv:2208.01410`, `arXiv:2208.01412`) construct ordered covering arrays for RT covering-radius upper bounds rather than OOAs.
3. **RT-metric matrix code bounds and constructions** (`KNOWN`; Wang, Li, and Heng, *"New Bounds of Linear Matrix Codes for the Rosenbloom-Tsfasman Metric and Optimal Constructions"*, *IEEE Trans. Inf. Theory* 71(9), 6844–6856, Sept. 2025; plus `arXiv:2302.02037`, `arXiv:2302.11738`, `arXiv:2401.10470`, `arXiv:2501.11978`, `arXiv:2607.18908`):
   - Wang, Li, and Heng establish Singleton-type and Plotkin-type upper bounds for `[h x n, K, d_RT]` linear matrix codes under the RT metric and construct low-rate trace / defining-set matrix codes and RT-MDS codes (`t = 0`). Neither Wang, Li, and Heng (2025) nor any other surveyed paper constructs or tabulates an `[(8, 2), 8, 8]`-NRT code over `F_3` or a linear `OOA(3^8, 8, F_3, 2, 7)`.

## Verdict

The explicit linear array `OOA(3^8, 8, F_3, 2, 7)` in `object/ooa_b3_T2_m8_s8_k7.tsv` (`k = 7`, `t = 1`) strictly beats live MinT's constructive linear record `k = 6` (`t = 2`) for `(b, T, m, s) = (3, 2, 8, 8)`, meets the generalized Rao bound `k <= 7`, cannot be derived by propagation or trivial edits from neighbouring cells or higher-depth nets, and does not appear in `TROPHY_CASE.md`, `known-knowns/`, repository pull requests, or the coding-theory and OOA literature.

pass: true
