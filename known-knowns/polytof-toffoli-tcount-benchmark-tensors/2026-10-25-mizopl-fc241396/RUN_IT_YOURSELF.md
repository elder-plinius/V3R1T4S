# Run It Yourself (`2026-10-25-mizopl-fc241396`)

1. Ensure `python3` (`>= 3.9`) with `numpy` is available.
2. From the root of this package directory, execute:
   ```sh
   sh verify-it-yourself/run_checks.sh
   ```
3. The script runs `verify-it-yourself/verify.py` (which also invokes `verify-it-yourself/synthesize_and_verify_circuits.py`), performing in **`~4.5` seconds single-thread CPU time**:
   - **Dual Standalone + `polytof` Waring Verification (`8` `.npy` matrices in `object/waring/`):** verifies exact cubic monomial equality `reconstruct_waring_triples(A) == bco_triples`, full-signature zero-Clifford-overhead conditions (`odd_cols == 0` and `odd_pairs == 0`), and `polytof`'s `verify_waring` check for `0732-00139.npy` (`139`), `0732-00141.npy` (`141`), `0732-00143.npy` (`143`), `0733-00161.npy` (`161`), `0105-00039.npy` (`39`), `0108-00073.npy` (`73`), `0115-00051.npy` (`51`), and `0817-00059.npy` (`59`).
   - **Requirement (c) Explicit `{CNOT, T, S, Z, CZ}` Circuit Synthesis & Equivalence (`n <= 30`):** synthesizes explicit gate-level circuits for `0732` ($n=27$, `139` $T$-gates), `0733` ($n=30$, `161` $T$-gates), and `0105` ($n=21$, `39` $T$-gates) and verifies both exact symbolic $\mathbb{Z}_8[x_0, \dots, x_{n-1}]/(x_i^2 - x_i)$ path-sum equality and $2^{20} = 1,048,576$-state $\mathrm{GF}(2^k)$ multiplier oracle / exhaustive $2^{21} = 2,097,152$-state statevector equivalence (`0` mismatches).
   - **Partial Win `p2` Optimality Certificates (`7` benchmark rows):** verifies in `< 0.15 s` that no decomposition with `table_value - 1` terms exists for `0112`/`0812` (`Mod 5_4` `CP = 1, Waring = 7`), `0101`/`0801` (`Barenco Tof_3` `CP = 2`), `0120`/`0820` (`Tof_3` `CP = 2`), `0134` (`Relative Tof_3` `CP = 2`), and `0725` ($\mathrm{GF}(2^2)$ Mult `CP = 3`).
   - **Partial Win `p3` Audit & Law `M5` 400-Sample Null Control:** verifies the 88-tensor audit report, the 400-sample random sparse parity null control (`0 / 400` matches), and exact integrity of `object/CERTIFICATE.json`, printing `PASS` as its final line.
