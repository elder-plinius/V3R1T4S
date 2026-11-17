# Baseline Record & Upstream Provenance (`magic-state-stabilizer-rank-exponents`)

## 1. Upstream Sources, Fetch Timestamps & SHA-256 Checksums

- **Target Problem Card**: `magic-state-stabilizer-rank-exponents` (`★★☆☆☆` Physics)
- **Upstream Ledger Repository**: `https://github.com/unitaryfoundation/stabrank` (commit `edde871fda354479d56e49b93a2502989bd956a2`, fetched `2026-11-09T09:02:14Z`)
  - `docs/ledger.json` sha256: `4e097d4ea559e00ae6701287bdc1372ce8be923d901ffabf8bff785585b1c3ad` (`167,365` bytes)
- **Companion Search Repository**: `https://github.com/kuyanov/stabzoo` (commit `b56ae82076c52233d7705d4e9b1f80c23d1fc7c9`, fetched `2026-11-09T09:02:28Z`)
  - `stab_core.py` sha256: `d73d76940ef10379cbb07b23dac77aecb21a1cc736819e13e3229a98ceba026a` (`11,412` bytes)
  - `stab_search.py` sha256: `aa111d8bf776d1f1f974fae170bd98536da8579c1940c34a760c363b7b37c0bb` (`48,705` bytes)
- **Primary Literature**:
  - S. Bravyi et al., *Simulation of quantum circuits by low-rank stabilizer decompositions*, Quantum 3, 181 (2019), `https://arxiv.org/abs/1808.00128`
  - H. Qassim, J. J. Wallman, J. Emerson, *Clifford-enhanced stabilizer decompositions*, `https://arxiv.org/abs/2106.07740`
  - A. Kuyanov (`2603.22293`), V. Russo & F. Labib (`2605.28586`), and H. Bevins (`2610.17500`).

## 2. Prior State of the Art vs. Our Certified Results (`p2`, `p3` & Constructive Witnesses)

| Problem Stratum | Published / `stabrank` Status (`edde871`) | Our Certified Contribution |
|---|---|---|
| **`qubit_T` ($|F\rangle^{\otimes 5,6}$) & `qubit_H` ($|T\rangle^{\otimes 5,6}$) Lower Bounds (`p2`)** | `docs/ledger.json` cites `[19, 25]` (`arXiv:2202.09202`, `2605.28586`) without a standalone machine-verifiable certificate script in `stabrank` | First standalone `~8.5s` Galois-quotient + 135-tableau Pauli-fiber XOR slice certifier (`Certs #1 & #2`) proving $\chi(|F\rangle^{\otimes 5,6}) \ge 5$ and $\chi(|T\rangle^{\otimes 5,6}) \ge 5$ across all `2,372` / `2,406` $G_3$-orbits |
| **Non-Clifford $|CS\rangle^{\otimes 3}$ (`6` qubits) (`p2`)** | `stabrank` records $[6, 16]$ with no slice-rank structure theorem | **Even-Qubit Slice Theorem (`Cert #3`)**: proves the $P_{000}$ slice collapses to $(2|0\rangle+(1+i)|1\rangle)^{\otimes 3}$ with exact stabilizer rank $\chi(|\psi_0\rangle^{\otimes 3}) = 4$ over $D_3$ (`idx=[0,7,568,624]`) |
| **Qutrit ($d=3$) $|H_3\rangle^{\otimes 4}$ & Norrell $|\mathbb{N}\rangle^{\otimes 6}$ (`p3`)** | Russo–Labib (`2605.28586`) MILP timed out on $r \le 15$ for Norrell $m=6$; no cyclic $\mathbb{Z}_4$ obstruction theorem for $|H_3\rangle^{\otimes 4}$ at rank $\le 6$ | **Complete Untwisted $\mathbb{Z}_4$-Cycle Closure (`Cert #4`)** across all `132` $g^2$-invariant flats (`192` fixed + `6,960` pair orbits) proving $\chi_{\text{untwisted-}\mathbb{Z}_4}(|H_3\rangle^{\otimes 4}) \ge 7$, plus $\tau$-invariant real MILP proving $r_{\text{sym}}(|\mathbb{N}\rangle^{\otimes 6}) = 16$ (`7,300x` faster) and tetrahedral $A_4^\Delta$ MILP proving $R_5(|F\rangle^{\otimes 10}) = 15$ (`Cert #5`) |
| **Face-Cat States $|\text{cat}_{2k}(F)\rangle$ & Non-Product $|F\rangle^{\otimes 6,7}$ (`Bonus`)** | Not previously catalogued in `stabrank` / `stabzoo` | **Master Theorem 54 (`W01..W07`)**: $|\text{cat}_{2k}(F)\rangle \in \mathbb{Z}[i]^{2^{2k}}$ has $\chi(|\text{cat}_6(F)\rangle) = 3 < 6 = \chi(|F\rangle^{\otimes 6})$ and $\chi(|\text{cat}_{10}(F)\rangle) \le 9 < 15$, plus new non-product rank-6 $|F\rangle^{\otimes 6}$ (`W08..W09`) and rank-9 $|F\rangle^{\otimes 7}$ (`W10`) decompositions over $\mathbb{Z}[i, \sqrt{3}]$ |
