# Preregistration — Spreads of the Elliptic Quadric Q^-(7,3) & Ternary Kerdock Sets

- primary_target_id: elliptic-quadric-q7-3-spread
- secondary_target_id: kerdock-set-ternary-m6
- frozen_utc: 2026-11-18T04:03:04Z
- null_test: not needed because both targets are exact deterministic finite-geometry existence or nonexistence claims over GF(3), verified by deterministic algebraic checkers, complete conjugacy-class enumeration in the full collineation group, and exact cover / DRAT-LRAT proof certificates with zero statistical, heuristic, or probabilistic claims.

## 1. Verbatim Target Criteria (from bank/targets.json)

### Primary Target: `elliptic-quadric-q7-3-spread`
- **Full `success_criterion`:**
  > Either (a) existence: using the quadratic form Q(x) = x1x2 + x3x4 + x5x6 + x7^2 + x8^2 over GF(3), whose x7^2 + x8^2 part is anisotropic so the form is elliptic, give 82 planes as 3 x 8 basis matrices over GF(3). Each must have rank 3 and be totally singular, and together they must cover each of the 1066 singular points exactly once. Or (b) nonexistence: an exhaustive search for spreads of this quadric whose code the skeptic reruns to the same conclusion, with every symmetry-breaking step justified, or a checkable DRAT/LRAT certificate for a published CNF encoding. Either settles a problem open on 2026-10-30 (direction: settle).

- **Partial Win `p1`:**
  > A rerunnable computer proof that no spread of Q^-(7,3) admits an automorphism of order 2 (or of order 3), extending the restriction in Kiermaier-Schmidt-Wassermann that only the primes 2 and 3 can divide the order of an automorphism. The skeptic reruns the code.

### Secondary Target: `kerdock-set-ternary-m6`
- **Full `success_criterion`:**
  > Give 243 distinct 6 x 6 matrices over GF(3) that are skew-symmetric (A^T = -A, zero diagonal) and such that det(A_i - A_j) != 0 mod 3 for all 29403 pairs i < j. Alternatively, give an explicit spread of the hyperbolic quadric Q^+(11,3) (244 totally singular 6-spaces partitioning its singular points) in a stated form, from which the Kerdock set is derived and checked. Direction: settle an existence question open on 2026-10-30.

- **Partial Win `p1`:**
  > Removal of one order r in {2,3,4,5,6,8} from the Kiermaier-Schmidt-Wassermann list. This is a published, rerunnable exhaustive computer search proving that no 1-(6,6,1) design in Omega^+(12,3) has an automorphism group of order r, for example by showing that no such design is invariant under any subgroup of order r of the quadric's collineation group, taken up to conjugacy. Code and orbit data are released, and the verifier reruns the search, or an independent reimplementation, to the same conclusion.

*(Strict single-claim rule: at most one target and one object/cell will be packaged in `claim/`.)*

## 2. Live Status Scout (Frozen Before Attack)

- Primary status source: https://arxiv.org/abs/2403.11188 (Kiermaier, Schmidt, Wassermann, *"Designs in finite classical polar spaces"*, Designs, Codes and Cryptography 2025; arXiv:2403.11188v3, 1 Oct 2025)
  - Fetched UTC: 2026-11-18T03:58:25Z, HTTP status: 200
  - SHA-256 (`data/arxiv_2403.11188_abs.html`): `b54a2f4cdb2bf94340a65ae21570103810d15152ae5f8ad43a1874f54525a742`
  - Latest version on arXiv: `[v3] Wed, 1 Oct 2025 14:04:02 UTC`.
- Primary e-print TeX archive: https://arxiv.org/e-print/2403.11188
  - Fetched UTC: 2026-11-18T03:58:26Z, HTTP status: 200
  - SHA-256 (`data/arxiv_2403.11188_src.tar.gz`): `c23156d51a467cbfdca14cbdc6682998f834338abea26874368bcdea39a657fa`
  - Status in Section 6 (lines 1065-1075 of `designspolarspaces.tex`):
    - For $\Omega^-(8,3) = Q^-(7,3)$: existence of a $1$-$(3,3,1)_{\Omega^-(3)}$ spread is OPEN; by computer search, only prime powers $2$ or $3$ may divide the order of an automorphism. Neither order $2$ nor order $3$ has been excluded.
    - For $\Omega^+(12,3) = Q^+(11,3)$: existence of a $1$-$(6,6,1)_{\Omega^+(3)}$ spread (ternary $6 \times 6$ Kerdock set) is OPEN; by computer search, its automorphism group has order in $\{1, 2, 3, 4, 5, 6, 8\}$.
- Companion Zenodo dataset: https://zenodo.org/api/records/13353388
  - Fetched UTC: 2026-11-18T03:59:56Z, HTTP status: 200
  - SHA-256 (`data/zenodo_13353388.json`): `401d34012ffc21fe63fc8e98030701175d05e1f7e7c84f13c66fae720e8986b5`
  - Contains strength-$2$ designs only (`q3_Q-_r3_k3.txt` has $\lambda \in \{2, 5\}$); zero spreads ($\lambda = 1$).
- OpenAlex work & citation graph:
  - https://api.openalex.org/works/https://doi.org/10.48550/arXiv.2403.11188 — Fetched UTC: 2026-11-18T03:59:57Z, HTTP status: 200, SHA-256 (`data/openalex_2403.11188.json`): `af7f1146c6545bbdaf57c7129f981f00a74e3aa72a2d9b9e95cf9a48425c5cbd` (`cited_by_count: 5`).
  - https://api.openalex.org/works?filter=cites:W4402584757 — Fetched UTC: 2026-11-18T04:00:14Z, HTTP status: 200, SHA-256 (`data/openalex_citing_ksw.json`): `3df0834c61096a9c0e5476c1006972afa957b9c1810e11b7f82a7388fc1c3ebc`. None of the 5 citing works (Weiß 2024/2025; *Regular sets of lines in rank 3 polar spaces* 2025; Kiermaier-Klawuhn `arXiv:2608.14437` 2026; `arXiv:2610.14509` 2026; *LDPC codes based on attenuated polar spaces* 2026) resolve spreads of $Q^-(7,3)$ or $\Omega^+(12,3)$ or narrow their automorphism orders.
  - Recent Kiermaier/Wassermann/Kerdock arXiv feed: https://export.arxiv.org/api/query?search_query=au:Kiermaier+OR+au:Wassermann+OR+ti:Kerdock&sortBy=submittedDate&sortOrder=descending&max_results=15 — Fetched UTC: 2026-11-18T03:59:15Z, HTTP status: 200, SHA-256 (`data/arxiv_kiermaier_wassermann_recent.xml`): `4dc8ec9cba5a18950a372776c104606fb420a68013a67fb819071a9dd2df2fba`; follow-up check https://arxiv.org/abs/2608.14437 — Fetched UTC: 2026-11-18T03:59:34Z, HTTP status: 200, SHA-256 (`data/arxiv_2608.14437_abs.html`): `d9b72c45bca493e4678a948ecca02aa2a956b67690d1f14ee6313404c3a0b208`.
  - Note: single GET to `api.semanticscholar.org` at 2026-11-18T03:58:26Z returned HTTP 429 (`data/s2_2403.11188_citations.json`, SHA-256 `65ab993d12c5c2cc9b68e6da2bb79b326930283e520363ffcdc145f88cd5a148`) and was not retried per Rule 5.
- Upstream V3R1T4S PRs & TROPHY_CASE.md:
  - https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100 — Fetched UTC: 2026-11-18T03:58:27Z, HTTP status: 200, SHA-256 (`data/v3r1t4s_pulls.json`): `eadd7bee03a4cf8b7f47215c3ba7229c4e99a060a368faecf6ad2a63a63da856`. Zero open or closed PRs and zero `TROPHY_CASE.md` entries match `elliptic-quadric-q7-3-spread` or `kerdock-set-ternary-m6`.

## 3. Exact Mathematical Formulation & Acceptance Gate

1. **Canonical Form & Polar Space Construction:**
   Construct $Q^-(7,3)$ over $\mathbb{F}_3^8$ using the exact target form $Q(x) = x_1 x_2 + x_3 x_4 + x_5 x_6 + x_7^2 + x_8^2 \pmod 3$ with polar bilinear form $B(x,y) = Q(x+y) - Q(x) - Q(y) \pmod 3$. Verify deterministically that $Q^-(7,3)$ has exactly $1,066$ singular projective points and $22,960$ totally singular planes ($13$ points per plane; $82$ pairwise-disjoint planes per spread).
2. **Full Automorphism Group $\mathrm{Aut}(Q^-(7,3)) = P\Gamma O^-(8,3) = PGO^-(8,3)$:**
   An automorphism of a spread $S$ of $Q^-(7,3)$ is an incidence-preserving bijection of the polar space $Q^-(7,3)$ mapping $S$ to $S$. Because $Q^-(7,3)$ has rank $3 \ge 3$ and $\mathrm{Aut}(\mathbb{F}_3) = 1$, the Fundamental Theorem of Polar Geometry (Tits / Chow / Dieudonné) identifies $\mathrm{Aut}(Q^-(7,3))$ with the full projective similarity group $PGO^-(8,3) = GO^-(8,3)/\{\pm I\}$ (including similarities $Q(Ax) = 2 Q(x) \pmod 3$ as well as isometries $Q(Ax) = Q(x) \pmod 3$). Any symmetry-breaking or conjugacy classification MUST operate in the full group $\mathrm{Aut}(Q^-(7,3)) = PGO^-(8,3)$, and we will also verify independently by an elementary linear-algebraic proof in the standalone verifier that every automorphism of $Q^-(7,3)$ is induced by an element of $GO^-(8,3)$.
3. **100% Conjugacy-Class Completeness Proof (Algebraic + Exact Enumeration):**
   For prime order $p = 3$ (and/or $p = 2$), construct explicit matrix representatives $\{g_1, \dots, g_k\}$ in $PGO^-(8,3)$, verify pairwise non-conjugacy in $PGO^-(8,3)$, compute the exact centralizer order $|C_{PGO^-(8,3)}(g_i)|$ for each $g_i$ by exact stabilizer/linear-algebra enumeration, and prove that $\sum_{i=1}^k |PGO^-(8,3)| / |C_{PGO^-(8,3)}(g_i)|$ equals the exact total count of elements of order $p$ in $PGO^-(8,3)$ computed from first principles.
4. **Mandatory Positive Control on $Q^-(5,3)$:**
   Run the identical polar-space, conjugacy-class, and Kramer-Mesner exact-cover pipeline on $Q^-(5,3)$ ($Q(x) = x_1 x_2 + x_3 x_4 + x_5^2 + x_6^2$, $112$ singular points, $280$ totally singular lines, spread size $28$) and confirm it constructs valid spreads invariant under automorphisms of order $3$ and order $2$.
5. **Dual-Engine Zero-Shared-Code Exact Cover Verification & Negative Controls:**
   - **If SAT on $Q^-(7,3)$:** Output the $82$ basis matrices ($3 \times 8$ over $\mathbb{F}_3$) and verify all $1,066$ points are covered once (`Full Win`).
   - **If UNSAT across ALL conjugacy classes of order $3$ (and/or order $2$):** Prove UNSAT by two completely independent zero-shared-code engines (e.g., C99 Knuth Dancing Links DLX / symmetry-justified normalizer reduction AND an independent solver or checkable LRAT/DRAT/branching certificate), packaged so that `sh verify-it-yourself/run_checks.sh` reruns the entire verification from scratch in a clean environment using standard tools (`python3` stdlib / C99), ends with `PASS`, and prints `FAIL` (non-zero exit) on surgical negative controls (dropped conjugacy class, altered matrix entry, corrupted certificate).
