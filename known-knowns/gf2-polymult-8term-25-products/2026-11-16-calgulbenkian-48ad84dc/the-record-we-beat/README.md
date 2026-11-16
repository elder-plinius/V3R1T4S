# The Record We Beat (`gf2-polymult-8term-25-products` `p2`, `GF(2^7)` mod `x^7 + x^4 + 1`)

- **NIST List of Circuits**: <https://csrc.nist.gov/Projects/circuit-complexity/list-of-circuits>
  - Fetched UTC: `2026-11-15T16:29:25Z` (HTTP `200`, `134,548` bytes, sha256 `3d621498fca085e96d5e973d8c17cd4291bc9750d7cfb0202631e96c62537283`)
  - Listed entry (`gf128-740-mult.slp`): `GF(2^7) mod x^7 + x^4 + 1` -> **`84` gates** (`40 AND + 44 XOR`, depth `5`)
- **Peralta Circuit Minimization Team (CMT)**: <https://www.cs.yale.edu/homes/peralta/CircuitStuff/CMT.html>
  - Fetched UTC: `2026-11-15T16:29:26Z` (HTTP `200`, `17,154` bytes, sha256 `8db7dd6385e40c8b809f375363d68f337f6da0084bd3e9b627a62beb5706f490`)
  - Listed entry (`slp_740.txt`, July 2010): **`84` gates**, depth `5`
- **Swapnil Jain (`gf2m-circuits`, Oct 2026)**: <https://github.com/Swapnil-jain/gf2m-circuits>
  - Checked UTC: `2026-11-15T16:29:26Z` (`main` head `9daf883e`, `multipliers/circuits/final_f7.slp`)
  - Best circuit for `GF(2^7) mod x^7 + x^4 + 1`: **`87` gates** (`32 AND + 55 XOR`, depth `11`; Sec. 5 & 7 note `84` remained unbeaten)
- **Our Circuit (`object/gf128_0x91_82gates.slp.txt`)**: **`82` gates** (`34 AND + 48 XOR`, depth `6`) — `-2` vs NIST/CMT, `-5` vs Jain (Oct 2026).
