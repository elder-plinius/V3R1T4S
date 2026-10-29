PROVED-HERE: correctness of the direct exhaustive counter.

For each man i, variable X_i is his assigned woman. For distinct men i,j, assignments X_i=w and X_j=v are compatible exactly when w differs from v and neither cross pair (i,v) nor (j,w) blocks. The support masks are computed from the validated integer preference ranks, directly from these three conditions.

Initially each variable may use every woman. Arc consistency removes a value w from i only when some other variable j has no compatible value left in its current domain. Inductively every stable matching uses values still in the domains: a removed value could not be in such a matching because its value at j would be a support. Repeating removals preserves all stable matchings, and an empty domain proves this branch has none.

After reaching a fixed point, if any domain has multiple values, the recursion chooses one such variable and branches on each remaining value. Every valid completion lies in exactly one branch. The recursion either removes values or fixes a nonsingleton domain, so it terminates. When all domains are singletons, pairwise distinctness yields a bijection; every blocking pair is a cross pair between two couples and would violate compatibility. The implementation nevertheless independently tests the full blocking-pair definition at every leaf.

Thus accepted leaves are exactly the stable matchings, each once. Their checked unsigned-integer sum is exact; overflow fails. No search-space sample is used. The counter supports at most 31 men; this object has 13. Its output nodes and elapsed time are telemetry, not additional mathematical claims.

The auxiliary construction word can be replayed to recreate object.prefs exactly using rebuild.py. Its chronological preference construction is checked for repeated encounters. The stable count is established by direct enumeration of the resulting preference lists, so no general word/rotation bijection is required as a premise.

The construction file uses cycles of any arity. Each man in a cycle receives the previous token of the next man in that listed cycle. The rebuild checks every encounter; the count is independently proved by exhaustive enumeration of the final explicit preferences and does not assume a generalized cycle-poset theorem.
