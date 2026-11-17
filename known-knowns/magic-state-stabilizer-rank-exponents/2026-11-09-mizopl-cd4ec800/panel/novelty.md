# Skeptic 2 — Novelty & Literature Audit (`novelty.md`)

- `context`: `fresh independent skeptic review comparing package against stabrank edde871 and arXiv literature`
- `target_id`: `magic-state-stabilizer-rank-exponents`

## Audit Findings

1. **Comparison with `unitaryfoundation/stabrank` (`edde871`) and `kuyanov/stabzoo` (`b56ae82`)**:
   - While `stabrank/docs/ledger.json` lists lower bounds from `arXiv:2202.09202` and `arXiv:2605.28586`, neither repository provides a standalone, self-contained `<4s` lower-bound verifier or the **135-Tableau Pauli-Fiber & Bitwise-XOR Homomorphism (`Master Theorem 55`)** on $D_3$.
   - For $|CS\rangle^{\otimes 3}$, `stabrank` records $[6, 16]$ with no slice-rank structure theorem; **Master Theorem 52 (`Cert #3`)** proves that the even-parity slice $P_{000}|CS\rangle^{\otimes 3} = (2|0\rangle+(1+i)|1\rangle)^{\otimes 3}$ has exact stabilizer rank $4$ over $D_3$.
   - For qutrit $|H_3\rangle^{\otimes 4}$ and Norrell $|\mathbb{N}\rangle^{\otimes 6}$, **Master Theorem 42B (`Cert #4`)** establishes complete untwisted $\mathbb{Z}_4$-cycle closure at rank $\le 6$ across all `132` $g^2$-invariant flats (`192` fixed + `6,960` pair orbits), and our $\tau$-invariant real MILP (`Cert #5`) closes Russo–Labib's timed-out symmetric dictionary at $m=6$ ($r_{\text{sym}} = 16$).
   - **Master Theorem 54 (`W01..W07`)** proves that even-parity face-cat states $|\text{cat}_{2k}(F)\rangle$ contract $\sqrt{3}$ completely into $\mathbb{Z}[i]^{2^{2k}}$, yielding $\chi(|\text{cat}_6(F)\rangle) = 3 < 6 = \chi(|F\rangle^{\otimes 6})$ and $\chi(|\text{cat}_{10}(F)\rangle) \le 9 < 15$, alongside new non-product rank-6 $|F\rangle^{\otimes 6}$ (`W08..W09`) and 2-block rank-9 $|F\rangle^{\otimes 7}$ (`W10`) witnesses.

pass: true
