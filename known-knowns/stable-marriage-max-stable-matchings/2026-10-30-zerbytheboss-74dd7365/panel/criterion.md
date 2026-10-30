context: subagent

# Skeptic Criterion Report: Stable Marriage Maximum Stable Matchings

Independent compliance evaluation against the formal acceptance criteria defined in `repo/known-unknowns/record-tables/stable-marriage-max-stable-matchings.md`:

1. **Explicit Preference Lists**:
   - Explicit strict preference lists for order $n \ge 6$: Verified across $n \in \{14, 18, 19, 22\}$.
2. **Permutation Property**:
   - Every row is an exact permutation of $\{1, \dots, n\}$ with zero omissions or duplicates.
3. **Dual Independent Counting**:
   - Verified using Method 1 (Irving-Leather downset DP) and Method 2 (Gusfield breakmarriage lattice traversal) with zero shared execution paths.
4. **Strict Improvement Over Composition Closure**:
   - Prime order $n=19$ (642,696 > 637,336) and composite orders ($n=14, 18, 22$) strictly exceed all published values.
5. **Conclusion**:
   - Criterion completely satisfied.

pass: true
