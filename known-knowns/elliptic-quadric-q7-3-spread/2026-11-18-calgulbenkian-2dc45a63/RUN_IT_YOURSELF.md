# Run it yourself

## 1. Verify the shipped certificate and rerun the exhaustive proof from scratch

From a fresh shell in this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8+ (standard library only) and a C99 compiler (`cc`, `clang`, or `gcc`) with `-lpthread`.
- **Rough laptop time**: ~55 seconds.
- **Expected last line**: `PASS`

Real output from a clean run is saved in `verify-it-yourself/RECEIPTS.md`.

### What `sh verify-it-yourself/run_checks.sh` verifies (zero shared code with `how-we-built-it/`)

1. **Positive control on $Q^-(5,3)$**: constructs $Q^-(5,3)$ ($112$ singular points, $280$ totally singular lines) independently in both `check_certificate.py` and `verify_engine2_dlx.c`, verifies the $28$ basis matrices in `object/q7_3_ord3_certificate.json` partition all $112$ singular points without overlap and are preserved by an explicit order-$3$ isometry, and finds a $28$-line spread by independent backtracking.
2. **Full collineation group $\mathrm{Aut}(Q^-(7,3)) = \mathrm{PGO}^-(8,3)$**: verifies over all $\binom{1066}{2}$ point pairs that collinearity coincides with sharing a totally singular plane, and proves by direct graph-automorphism backtracking on the $1{,}066$-vertex collinearity graph $\Gamma$ that the pointwise stabilizer of a standard $6$-point hyperbolic frame has order $64$, establishing $|\mathrm{Aut}(Q^-(7,3))| = 1066 \cdot 729 \cdot 112 \cdot 81 \cdot 10 \cdot 9 \cdot 64 = 40{,}607{,}874{,}478{,}080 = |\mathrm{PGO}^-(8,3)|$.
3. **100% constructive order-$3$ conjugacy-class completeness**: verifies via RREF subspace enumeration and Cayley's bijection $S = G(A - I)(A + I)^{-1}$ that $\mathrm{PGO}^-(8,3)$ contains exactly $430{,}408{,}160$ elements of order $3$, verifies pairwise distinct fixed-point counts $(94, 121, 13, 4, 22)$ of the $5$ certified representatives, computes exact class sizes via deterministic $\mathrm{GO}^-(8,3)$-generator BFS (`59,696` and `537,264`) and exhaustive Jordan-chain centralizer enumeration (`42,981,120`, `193,415,040`, and `193,415,040`), and confirms their sum equals $430{,}408{,}160$.
4. **Exhaustive exact-cover nonexistence (`UNSAT`)**: verifies `C3_94`, `C3_121`, `C3_4`, `C3_22`, all $5$ $\mathrm{PO}^-(8,3)$ involution classes (`Inv_364`, `Inv_130`, `Inv_114`, `Inv_44`, `Inv_26`), and all $4$ odd-prime Sylow-$\{5, 7, 13, 41\}$ representatives are `UNSAT`, verifies that `C3_13` requires the fixed plane $\Pi_*$ (`Case B` impossible since all $36$ other fixed planes meet $\Pi_*$ in $4$-point lines), constructs the full normalizer $|N_{\mathrm{PGO}^-(8,3)}(\langle A \rangle)| = 1{,}889{,}568$, verifies transitivity of $N$ on all $6{,}561$ disjoint plane $3$-orbits, and proves all $4$ canonical stages (`143` Depth-$2$ tasks, `8,776,899` deterministic Row-DLX branching nodes) `UNSAT`.

## 2. Rebuild the certificate and run Engine 1 (64-bit SWAR solver)

See `how-we-built-it/BUILD_COMMANDS.md` and the complete mathematical proof in `how-we-built-it/PROOF.md`.
