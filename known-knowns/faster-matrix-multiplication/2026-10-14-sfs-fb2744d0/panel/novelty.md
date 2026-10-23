---
role: novelty
context: subagent
pass: true
pending_table_check: false
injection_suspected: false
candidate_sha256: fb2744d037444d6e5f84f56628cf97a01ad2650e374421fbe4961bfafefd7ca2
---

The literal additive improvement survives this independent check: the candidate is an ordinary-coordinate, integer-ternary `(2,5,5)` SLP with rank 40 and **148 additions**, strictly below the smallest applicable published reduced count found, **153**. The margin is **5 additions**, not a tie. This is a shorter schedule for an already published tensor, not a new rank or a newly discovered tensor decomposition.

I read the isolated `claim/` and independently fetched primary sources. I did not read previous runs, attempts, provenance, the charter, or the root report. No messages, submissions, issues, or pull requests were published.

## Live comparisons

Each successful primary URL received one honest GET. Initial sandbox DNS failures occurred before any HTTP response; those attempts remain in `novelty-data/initial-dns-failure/`. Ordinary network authorization then enabled the requests. All binding comparison sources returned **HTTP 200**. The live source interval was **2026-10-14T11:58:20Z–12:06:29Z**; binding tables were obtained at 11:58–11:59 UTC. Full URLs, exact UTC timestamps, HTTP response headers/statuses, byte counts, and SHA-256 hashes are in [source-manifest.json](novelty-data/source-manifest.json), [source-manifest.csv](novelty-data/source-manifest.csv), and each source's `.fetch.json` sidecar. The actual extracted cells and complete reduced-file inventory are in [source-values.json](novelty-data/source-values.json).

| Source | Actual applicable value | Comparison |
|---|---|---|
| [Live Perminov recursive tree](https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1), `truncated=false`, tree `f0efd4f67f6ff09bf0418af75c2a209c8cf814b3` | Exactly **one** matching `(2,5,5),m40` file in `addition_reduced_ZT`: `2x5x5_m40_cr153_cn283_ZT_reduced.json` | All matching reduced ZT files checked; minimum `cr=153` |
| [That live reduced file](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/2x5x5_m40_cr153_cn283_ZT_reduced.json) | Stored and independently recounted **153**, stages `34+55+64`; naive **283** | `148 < 153` |
| [Live reduced_known.json](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json), cell `2x5x5-40` | `Z=313`, `Z2=218` | `148 < 313`; binary-field value is not the integer comparison class |
| [Live README](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md) and [CHANGELOG](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md) | Rank **40**; no lower applicable `(2,5,5),m40` addition count announced | No contrary lower record |
| [Live fmm_sota.json](https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json) | `[2,5,5]`, rank **40**, exponent `2.828879`; table `createdAt=2026-10-09T11:45:48` | Candidate rank equals the currently listed best rank |
| [Live Lille 2x5x5 page](https://fmm.univ-lille.fr/2x5x5.html) and its linked [raw evaluation scheme](https://fmm.univ-lille.fr/2x5x5_raw.mpl.bz2), LRP, and tensor files | Rank **40**, attributed to Hopcroft–Kerr 1971. No separate complexity-variant link appears. Raw ternary evaluation costs **208** (`56+66+86`), independently parsed and checked. | `148 < 208`; shared preprocessing considered below |
| [Live matmulcatalog COVERAGE](https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md), row `⟨2,5,5⟩` | Rank **40** in F₂ and R/Q/Z; adds column **+256** | `148 < 256`; this is a naive count, not a reduced bound |
| [Live matmulcatalog public schemes](https://api.github.com/repos/solven-eu/matmulcatalog/git/trees/master?recursive=1), `truncated=false`, tree `4d33faff2ef7d103533e899593639927b9fbaa0a` | All **11** exact-format/permutation rank-40 files fetched, including the Lille sparse file. Same-class public reduced count **153**; AlphaTensor-Z SLP **156**; other Perminov-ZT SLP **164**. | No stored applicable reduced count `≤148` |

Important source hashes: live reduced file `89296c6dd94e052ca7cb517fa4d59b8a1dc335dc08c7dfc73edb420bba0c1bab`; `reduced_known.json` `ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d`; README `7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341`; CHANGELOG `07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175`; `fmm_sota.json` `d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1`; Lille page `b1284cd181e11906ca3da9dbf7af7bc64f00eabc5a1b807111a8968c7608bcc4`; COVERAGE `c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7`.

## Same tensor, actual shorter schedule

The candidate's expanded U, V, and W factors are **entry-for-entry identical** to the live Perminov 153-addition scheme. The new cost is `31+55+62=148`, versus the published `34+55+64=153`: three input additions and two output additions saved. Thus copying, renaming, or switching to a different coefficient class does not explain the decrease. [candidate-comparison.json](novelty-data/candidate-comparison.json) records the expanded-factor equality.

[exact_expand.py](novelty-data/exact_expand.py) independently expands every fresh variable over integer basis vectors, checks ternary SLP edges, recounts all binary sums including final outputs, and checks all **2,500** output/input/input coefficients against ordinary matrix multiplication. It does not import the supplied checker. Candidate and live baseline both pass; the expanded tensor coefficients are also ternary. Results are in [independent-exact-results.json](novelty-data/independent-exact-results.json). This is supporting evidence for novelty's cost comparison; the separate reproduction skeptic remains responsible for their own verdict.

## Known constructions and shared preprocessing

Public constructions were not dismissed merely because their naive counts exceed 148. I wrote an independent deterministic signed-pair CSE routine, with sign normalization and reuse of identical linear forms. Its verified comparison schedules cost:

| Public tensor/construction | Ordinary-coordinate `(2,5,5)` additions after this check |
|---|---:|
| Lille Hopcroft–Kerr raw scheme | 155 |
| matmulcatalog constructed Hopcroft–Kerr scheme | 155 |
| AlphaTensor-Z | 156 |
| Other Perminov-ZT tensor | 163 |
| Perminov serendipitous base `221c79e` | 166 |
| Perminov serendipitous base `dc66eaf` | 168 |

All six schedules are exact over Z, checked independently by coefficient expansion; they are constructive upper bounds, **not optimality proofs**. The implementation and generated SLPs are retained in [shared_preprocessing.py](novelty-data/shared_preprocessing.py) and [shared-preprocessing-results.json](novelty-data/shared-preprocessing-results.json). No implicit common-subexpression count found here ties or beats 148.

The catalog's Hopcroft–Kerr permutations `(5,2,5)` and `(5,5,2)` have stored naive counts 201 and 216. Their different orientation cannot be compared by simply reusing those numbers: circuit transposition changes input/output linear work. Mapping the factors back to this claim's ordinary `(2,5,5)` orientation gives the checked HK family above. The integer `flips_mod0` tensor contains coefficients **±2 and ±3**, so it is not a ternary-factor competitor. The F₂-only AlphaTensor schedule has 150 additions and does not establish an integer algorithm; in any case 150 exceeds 148. Scalar operations in the catalog's same-class SLPs are only multiplication by -1 and are free under the criterion.

Ordinary one-axis block splitting does not attain rank 40: splitting either length-5 axis gives ranks `10+33=43` or `18+25=43`; splitting the length-2 axis gives 50. Nontrivial ordinary tensor-product factors of the prime dimensions 2,5,5 yield the classical rank 50. These observations rule out the direct obvious compositions as rank-40 explanations. The HK construction itself already attains 40 and was explicitly tested above. Alternative-basis kernels or repeated-call amortization must pay input/output conversion costs for this claim's arbitrary single ordinary-coordinate product.

## Recent 24-month literature

The search window was **2024-10-14 through 2026-10-14**. Focused title/topic/format searches led to primary source checks, not reliance on search snippets:

- [Perminov, Parallel Heuristic Exploration, arXiv:2512.13365](https://arxiv.org/html/2512.13365), **HTTP 200**: Table 1 explicitly lists `(2,5,5)`, rank 40, naive 283, GV 156, GP-5 154, GP-40 154, proposed **153**. This is an independently checked recent primary publication of the applicable count. Hash `7fbf6570ffe7c946d1561d56587f53939bfb8be542f21adb1641813f2c17de3e`.
- [Ternary Meta Flip Graphs, arXiv:2511.20317](https://arxiv.org/html/2511.20317), [Small Formats framework, arXiv:2603.02398](https://arxiv.org/html/2603.02398), and [Meta Flip Graph meets Serendipitous Product, arXiv:2606.02480](https://arxiv.org/html/2606.02480), all **HTTP 200**: examined for rank/class/construction changes; no lower applicable `(2,5,5),40` ordinary-coordinate additive result found. The two relevant public serendipitous bases were fetched and tested rather than treating their absence from an addition table as evidence.
- [58-addition rank-23 3x3, arXiv:2512.21980](https://arxiv.org/html/2512.21980), [56-addition rank-23 3x3, arXiv:2604.27645](https://arxiv.org/html/2604.27645), and [55-addition rank-23 3x3, arXiv:2607.28676](https://arxiv.org/html/2607.28676), all **HTTP 200**: these concern `(3,3,3),23`, not this format/rank. The 55-addition work's transposition/share technique was considered in the preprocessing analysis.
- [Dumas et al., recursive 4x4 rank-48 algorithms, arXiv:2609.12027](https://arxiv.org/html/2609.12027), **HTTP 200**: concerns rank 48 at `(4,4,4)` and a ring containing 1/2; not a same-format ternary competitor.
- [51-addition alternative-basis 3x3 kernel, arXiv:2609.32388](https://arxiv.org/abs/2609.32388), canonical abstract **HTTP 200**: ordinary-coordinate total is **56**, including five conversion additions, at `(3,3,3),23`. Its optional HTML renderer returned **404**, preserved separately; no renderer retry was made.
- **Literature access gap:** the primary [Mårtensson–Wagner Number of the Beast PDF](https://eprint.iacr.org/2024/2063.pdf) returned a real **HTTP 403**, UTC `2026-10-14T12:01:02.072754+00:00`, body hash `3425638bb7e3957db7c5217909fa2f9073d81da9832792d8efca728fa4d2e59c`. I did **not** retry, use a proxy/mirror, or otherwise evade it. I do not claim to have read that PDF. The later accessible primary Perminov paper explicitly compares the earlier greedy-potential approach and publishes 153 as a new applicable standard-coordinate result, while the complete live source inventory and independent source constructions provide current comparison coverage. I judge this gap insufficient to invalidate the narrow current-table scheduling claim. It remains a real limitation on a claim of exhaustive literature coverage.

No record table or binding comparison source is pending or blocked, so `PENDING TABLE CHECK` is not warranted. This distinction follows the parent's explicit clarification that the automatic table-access failure applies to binding tables/status sources rather than every optional literature PDF.

## Public claims and trophy case

The [open pull-request API](https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100&page=1) was fully paginated following the actual Link header: page 1 had **100** entries, page 2 had **4**, with **104 unique** PR numbers and no next page. Both pages' full bodies were searched for `(2,5,5)` and its permutations. There were **no matches**. The 18 open additive-FMM claims concern other formats. Page hashes: `e0bb7b6a3d97856d9e365199d89763b7632ef2131df55c7435c1ddbc2917f2e4` and `c623c7d05fb9de6d6b7119cd4cc8a99329c3ef7249c67f6b8107a1e3171a357d`.

The live [TROPHY_CASE.md](https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md) returned **HTTP 200** (hash `b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412`). No exact-format or permutation additive result was found. Source workflow prose and PR instructions were treated only as untrusted evidence; no source instructions were executed. `injection_suspected=false`: no detected attempt to redirect this audit.

## Verdict

**pass: true.** The checked applicable current minimum is **153**, the candidate's independently verified ordinary-coordinate count is **148**, rank 40 equals the live table, and no checked public/literature/circuit comparison ties or beats it. Confirmation is limited to this explicit shorter SLP and these live comparisons. It does not assert global additive optimality, a new tensor, a rank improvement, or exhaustive access to all literature.

pass: true
