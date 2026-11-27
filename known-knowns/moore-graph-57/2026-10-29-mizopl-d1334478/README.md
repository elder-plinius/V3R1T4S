# Independent Exact Computational Verification of `arXiv:2606.29183v2` on the Missing Moore Graph (`srg(3250, 57, 0, 1)`) (`moore-graph-57` — `p2`)

## What

Certified Partial Win p2 on moore-graph-57 (srg(3250, 57, 0, 1); indexed in object/certificate.json sha256 d13344783df1b7cf33f19e9b3408bad1bbe96939c5e087b02460113f03dc9c07 and verified on a 16 GB M1 laptop using the open-source we* engine at https://github.com/mizopl/we-star), verified in 100% exact integer, rational (fractions.Fraction), and finite-field (F_p Gaussian elimination) arithmetic with zero floating-point approximations: independent exact computational verification of arXiv:2606.29183v2 (Yawara Ishida, 8 July 2026), verifying the Bose-Mesner idempotents E_7 = (400I+50A-J)/750 (multiplicity 1729) and E_{-8} = (455I-65A+J)/975 (multiplicity 1520), the Brauer trace-rank identity on C_5, Petersen srg(10,3,0,1), and Hoffman-Singleton srg(50,7,0,1), Theorem 1.1 & Corollary 6.1 (Fix(t) = K_{1,55}, rank_{F_2}(975 E_{-8}[F] mod 2) = 54 => a_1(t) = -368 < 0, ruling out all involutory automorphisms), Theorem 1.2 for p in {7, 11, 13, 19}, and all 11 rows of Section 8 Table 1 across 5 open SRG families including Remark 8.5.

---

## Check It Yourself

Run the standalone zero-dependency checker from the package root (`< 0.1 seconds`, Python 3.8+ standard library only):
```bash
sh verify-it-yourself/run_checks.sh
```
This script executes `verify-it-yourself/verify.py`, which independently recomputes every rational Bose–Mesner idempotent, finite-field $\mathbb{F}_p$ matrix rank, Brauer trace–rank check on existing Moore graphs ($C_5$, Petersen, Hoffman–Singleton), Theorem 1.1, Theorem 1.2, and all 11 rows of Section 8 Table 1 from scratch in exact arithmetic, verifies digit-for-digit agreement with `object/certificate.json`, and prints `PASS`.

To run the standalone Lens 1 (`p2`) builder script directly:
```bash
python3 how-we-built-it/verify_lens1_p2.py
```

---

## Compared To

- **Primary Source Verified (`p2`):** Yawara Ishida, *"No involutions in the missing Moore graph"*, `arXiv:2606.29183v2` (`https://arxiv.org/html/2606.29183`, fetched `2026-10-26T03:31:00Z`, HTML `sha256: 943fd613a12c58ca20b8b9689e41ad63336dbbcd1ecf4bb2cacee443a87ab2cb`, PDF `sha256: a032dff9013b69e5610b445e8c352810932d17a62b5321fa710aad71c78707a7`).

| Theorem / Section in `arXiv:2606.29183v2` | Mathematical Statement Verified | Exact Computed Result | Status |
| :--- | :--- | :--- | :---: |
| **Section 5 (Eqs. 8–9)** | $p$-integrality & multiplicities of $E_7$ and $E_{-8}$ in $\mathrm{srg}(3250, 57, 0, 1)$ | $E_7 = \frac{400I+50A-J}{750}$ ($\mathrm{denom} = 2 \cdot 3 \cdot 5^3$, $m_7 = 1729$), $E_{-8} = \frac{455I-65A+J}{975}$ ($\mathrm{denom} = 3 \cdot 5^2 \cdot 13$, $m_{-8} = 1520$) | **PASS** |
| **Section 4 (Thm. 4.1)** | Existing Moore graphs $C_5$, Petersen $\mathrm{srg}(10,3,0,1)$, $\mathrm{HoSi}$ $\mathrm{srg}(50,7,0,1)$ | $\mathrm{tr}(T_g E_\theta) = \mathrm{rank}_{\mathbb{F}_p}(E_\theta[\mathrm{Fix}(g)] \bmod p)$ verified across all $5$ prime-order benchmark cases | **PASS** |
| **Theorem 1.1 & Cor. 6.1** | No involutions in $\mathrm{srg}(3250, 57, 0, 1)$ ($p = 2$, $\mathrm{Fix}(t) \cong K_{1,55}$) | $\mathrm{rank}_{\mathbb{F}_2}(975 E_{-8}[K_{1,55}] \bmod 2) = 54 \implies a_1(t) = -368 < 0$ (vs combinatorial $a_1(t) = 112, \chi_{-8}(t) = 22, \chi_7(t) = 33$) | **PASS** |
| **Theorem 1.2 ($p \in \{7,11,13,19\}$)** | Exact displacements $a_1(x)$ for odd primes | $p=7$: $(a_0, a_1) \in \{(2,49),(9,98),(16,147),(23,196),(30,245),(37,294)\}$ (excludes $\{44,51\}$); $p=11$: $a_1 = 55$; $p=13$: $a_1 = 65$; $p=19$: $a_1 = 57$ | **PASS** |
| **Section 8 (Table 1 & Rem. 8.5)** | $11$ branches across $5$ open SRG families | All $11$ rows of Table 1 and Remark 8.5 (correcting Makhnev–Nosov 2004 on $\mathrm{srg}(352,26,0,2)$) verified in exact $\mathbb{F}_p$ arithmetic | **PASS** |

---

## Not Claimed

- We do not claim a Full Win (`CONFIRMED_SOLUTION`) on `moore-graph-57` (constructing a $57$-regular Moore graph on $3250$ vertices or proving its non-existence in Lean/Isabelle).
- We do not claim Partial Win `p1` (exclusions of odd automorphism-group orders beyond `arXiv:2606.29183v2`).

---

## Credits

- **Primary Reference Verified (`p2`):** Yawara Ishida (*"No involutions in the missing Moore graph"*, `arXiv:2606.29183v2`, 8 July 2026).
- **Exact Computational Verification (`p2`):** `@mizopl` (`we*` = `@mizopl` + Gemini-CLSS autonomous research system, `https://github.com/mizopl/we-star`).
