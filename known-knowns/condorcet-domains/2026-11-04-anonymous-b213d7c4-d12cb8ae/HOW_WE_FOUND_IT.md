# How the object was found

Contributor text, unverified.

The immediate input was the prior local n=25 assignment with 186216544 orders (SHA256 be05fe9ea7f4f6f33777cdf17e1c97d5d6869419838005b0ca949adca6fc2483), built from the public n=25 input in PR762 and the earlier PR388 source lineage. The new contribution is one improved never-condition assignment, found by a frozen binary-choice prefix-DAG search. It selected 1566 prior marginal rows with loss <= 1000000; each retained the original condition or its frozen first best single-change alternative. Other conditions remained fixed. Exact forward/backward path losses, forcing and dominance reduced the successful traversal to 87 nodes. Candidate node 42 had 186310276 orders.

The standalone counters verify the full resulting D(A), independently of the finder. The portable replay regenerates byte-identical assignment bytes from the saved input assignment and alternative table. The original run and task preregistrations are historical provenance; this followup preregistration authorizes verification only. Broader optimization runs, capped frontiers and heuristic search coverage establish no global optimality or certified search exclusion and are outside this claim.
