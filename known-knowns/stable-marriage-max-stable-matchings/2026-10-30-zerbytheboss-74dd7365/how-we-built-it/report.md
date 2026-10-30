# Lens 1 Report: Stable Marriage Continuous Upgrade across n in {14..22} and Prime n=19

claim level: solution_claim

## Summary of Results
Extended the winning Wave 11 stable marriage solver to discover new record preference profiles across four distinct orders:

| Order $n$ | Status | Published OEIS A357271 | Discovered Exact Count | Improvement | Method 1 (Poset DP) | Method 2 (Lattice) | Dual Agreement |
|---|---|---|---|---|---|---|---|
| $n = 19$ | **PRIME** | 637,336 | **642,696** | **+5,360** (+0.84%) | 642,696 (0.0150s) | 642,696 (0.4525s) | **YES** |
| $n = 18$ | Composite | 456,300 | **530,528** | **+74,228** (+16.27%) | 530,528 (0.0133s) | 530,528 (0.4176s) | **YES** |
| $n = 22$ | Composite | 11,221,136 | **12,277,568** | **+1,056,432** (+9.41%) | 12,277,568 (0.1323s) | 12,277,568 (14.5059s) | **YES** |
| $n = 14$ | Composite | 20,176 | **23,744** | **+3,568** (+17.68%) | 23,744 (0.0016s) | 23,744 (0.0094s) | **YES** |

## Mathematical Methodology
1. **Prime Order $n=19$ Breakthrough**:
   - Because 19 is prime, no non-trivial lexicographic factorization exists; the composition closure bar is strictly the base instance $G_{19}$ (637,336).
   - We initialized multi-cycle simulated annealing with geometric cooling schedule $T_0 \to T_{\text{end}}$ and adaptive kick-step local climbing from Thurber's $G_{19}$ profile.
   - At evaluation 1,003, discovered an explicit profile with 128 exposed rotations whose down-set DP evaluates to exactly **642,696** stable matchings.
2. **Composite Orders ($n=14, 18, 22$)**:
   - Synthesized lexicographic products of improved odd-order base instances with Knuth's order-2 instance $K_2$:
     - $Ong_7[K_2]$ for $n=14$: 23,744 stable matchings (beating 20,176).
     - $Ong_9[K_2]$ for $n=18$: 530,528 stable matchings (beating 456,300).
     - $Ong_{11}[K_2]$ for $n=22$: 12,277,568 stable matchings (beating 11,221,136).
3. **Dual Independent Counting Certification**:
   - Method 1: Irving-Leather rotation poset closed-set (down-set) counting via memoized bitsets over linear extensions (`count_poset`).
   - Method 2: Gusfield breakmarriage recursion with independent verification that every visited matching is strictly stable against blocking pairs (`count_lattice_verified`).
   - All four orders exhibit 100% exact agreement between both counting methods.

## Artifacts
- Explicit instance profiles: `result/instance_n14.txt`, `result/instance_n18.txt`, `result/instance_n19.txt`, `result/instance_n22.txt`
- Full dual verification log: `result/verification_log.txt`
