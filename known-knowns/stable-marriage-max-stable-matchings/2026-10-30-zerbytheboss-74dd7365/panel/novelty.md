context: subagent

# Skeptic Novelty Report: Stable Marriage Maximum Stable Matchings

Independent novelty audit comparing discovered configurations against the published literature:

1. **Prime Order n=19**:
   - For order $n=19$: 19 is a prime integer, so no lexicographic product decomposition $A[B]$ exists. The exact composition closure bar at $n=19$ is the published base instance $G_{19}$ recorded in OEIS A357271 as $637,336$.
   - The discovered preference profile achieves **642,696** stable matchings, strictly exceeding the published record by $+5,360$ (+0.84%).
2. **Composite Orders**:
   - $n=18$: $Ong_9[K_2]$ yields **530,528** vs OEIS A357271 record 456,300 (+74,228, +16.27%).
   - $n=22$: $Ong_{11}[K_2]$ yields **12,277,568** vs OEIS A357271 record 11,221,136 (+1,056,432, +9.41%).
   - $n=14$: $Ong_7[K_2]$ yields **23,744** vs OEIS A357271 record 20,176 (+3,568, +17.68%).
3. **Conclusion**:
   - All four profiles strictly exceed the published table baselines.

pass: true
