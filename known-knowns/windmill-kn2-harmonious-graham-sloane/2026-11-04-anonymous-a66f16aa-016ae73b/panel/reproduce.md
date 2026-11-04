context: fresh subagent, fork_turns=none; publication edition of original independent review.
role: REPRODUCE
verdict: SURVIVES for the finite mathematical n=10 exclusion only
claim level: PROVED-HERE by complete exact finite enumeration

A harmonious labeling of a graph with q edges injects its vertices into Z_q and makes the unordered edge sums bijective. Two cliques K_n sharing exactly one vertex have 2n-1 vertices and q=n(n-1) edges.

K10^(2) therefore has one center c and two disjoint sets of nine other vertices. Its edges are precisely the pairs within either ten-vertex clique, giving 19 vertices and 90 edges. The confirmed computational statement is that no injective residue labeling modulo 90 makes those 90 edge sums distinct. This review makes no general-n or novelty claim.

This is an editorial publication edition of the original independent review. No new computation or review was performed for this edition. Paths below refer to artifacts in the public contribution.

Independent implementation and complete run

Before reading either author program or the author's reproduction instructions, I designed and wrote the independent checker from the definition above. I completed its n4, n8, and whole n10 runs before reading the supplied programs. The public checker is [independent.cs](../verify-it-yourself/independent.cs), with [run-independent.ps1](../verify-it-yourself/run-independent.ps1).

The checker uses sorted clique enumeration, UInt128 sum masks, forward candidate filtering, and a dictionary retaining all vertex sets for each completed sum mask. It rechecks every complete clique by explicit nested pair loops. If it finds a graph witness, it directly checks distinct vertices and all q edge sums.

| Case | Result | Complete clique leaves | Distinct masks | Complement pairs |
| --- | --- | ---: | ---: | ---: |
| n4 calibration | Valid witness | 33 before witness | 32 before witness | 1 |
| n8 calibration | COMPLETE, no pair | 449472 | 407352 | 0 |
| n10 central claim | COMPLETE, no pair | 1702800 | 1571472 | 0 |

The n4 witness is [0,1,9,11] and [0,2,3,4]. The independent checker verifies seven distinct vertices and all twelve edge sums. The n8 result is only a calibration. The n10 search visited 91726677 nodes and completed in 20.2463615 seconds, with a peak working set of 581566464 bytes. Its result says COMPLETE and found:false. It exhausted the whole normalized domain. See the public [independent result](../object/receipts/independent-result.json).

The runs had a 600-second time limit and a 1900 MiB process-memory check. Neither limit interrupted the completed n10 search. A rerun interrupted by either limit would be INCOMPLETE and would not establish exclusion. The wrapper requires PowerShell7 and its bundled .NET runtime with UInt128 support; it compiles the C# source in memory. Run it in a fresh PowerShell process from the contribution root:

```powershell
pwsh -NoProfile -File ./verify-it-yourself/run-independent.ps1 -Size 10 -Seconds 600
```

Completeness and arithmetic derivation

1. Replace every label f(v) with f(v)-f(c). This is a bijection of vertex residues. Every edge sum changes by the same constant -2f(c), also a bijection of residues. Thus c=0 loses no labeling, even though 2 is not a unit modulo 90. No division by 2 occurs.
2. The noncentral vertices within each clique may be sorted because they have identical graph roles. Every normalized ten-element clique label set then appears exactly once. The independent run starts with all nonzero residues as candidates. It uses no unit multiplication symmetry, parity filter, or histogram filter.
3. Adding label x to old vertices V creates the edge sums V+x modulo q. Translation is injective, so these new sums are mutually distinct. A candidate is rejected exactly when a new sum intersects an existing sum. This collision remains present in every extension, so forward filtering is sound. A branch with too few remaining candidates cannot reach n vertices.
4. Rotate(V,x)=((V<<x)&Full)|(V>>(q-x)) implements residue translation. For q=90 and 1<=x<=89, every shift is strictly below 128. The low part retains unwrapped residues and the right-shifted part supplies wrapped residues. Bits lost above position 127 in the left shift do not lose any residue: those wrapped residues are also supplied by the right-shift term. UInt128 stores all 90 residues exactly.
5. Each completed clique contributes exactly 45 distinct edge sums. Two cliques complete the graph exactly when their masks complement each other within Full and their vertex sets intersect only at zero. A dictionary lookup against earlier completed cliques examines every unordered pair when its second member is reached. The independent program retains every vertex set for a repeated sum mask and explicitly checks the intersection. No pair was found, so there is no labeling in the full normalized domain.

The contribution also provides a [proof write-up](../object/PROOF.md). The derivation above records the reasoning of this independent review.

Supplied-source and receipt audit

The original review checked all twelve entries of the frozen source manifest against their actual SHA256 hashes on first inspection and again at final verification. All matched. The four copied author source and wrapper files also matched. This statement records the original audit; this editorial edition does not claim to have rehashed the public export.

The audited author programs are [ComplementSearch.cs](../how-we-built-it/method1/ComplementSearch.cs) and [DirectConstraintWide.cs](../how-we-built-it/method2/DirectConstraintWide.cs).

The [method1 receipt](../object/receipts/complement-result.json) agrees exactly with the independent 1702800 cliques and 1571472 masks; its duplicate count is 131328. The first-label range is 1 through 81, all marked complete. This bound is exhaustive: nine sorted nonzero labels in 1..89 have minimum at most 81.

Method1 constructs every new edge sum and rejects only collisions. Its upper candidate bound reserves enough larger residues to finish the clique. Keeping one representative per sum mask does not compromise the negative conclusion. Complementary masks automatically imply disjoint noncentral labels: with center zero, a common label x would produce the common spoke sum x. Thus method1 does not need a separate test for cross-clique vertex injectivity.

In the original review, I inspected method2's complete progress receipt: 84 records, including each completed root 1..81 exactly once. Its finish record reported nodes_a=271924415, nodes_b=559147377, complete_a=1547248, found=false, timed_out=false, and elapsed_seconds=23.833506. Its [result](../object/receipts/constraint-result.json) states range_complete:true and full_domain:true. These were receipt checks; this reviewer did not rerun either author's entire n10 program.

Method2's candidate invariant is that every existing vertex plus the candidate yields a sum absent from used. After adding x, Extend excludes y when x+y belongs to usedNew, and excludes y when y plus any old vertex belongs to the newly added sums. Old candidates already excluded old sums. These are exactly the new collisions; strict Higher(x) only orders the clique. SearchB begins with center zero and candidates outside used, correctly enforcing its spokes. This also excludes all noncentral A labels because A's spokes lie in used.

The parity pruning is necessary: a clique with k odd labels has k(n-k) odd edge sums. A complete graph labeling uses all q residues once, including q/2 odd residues. Hence k(n-k)+l(n-l)=q/2. Since zero is even, each clique has at most n-1 odd labels, matching the array bounds. OddReachable bounds attainable odd counts using the odd and even candidates that remain. Rejecting a branch only when no allowed final pair lies in those bounds is sound. BackShift is the inverse cyclic shift on q bits; its mask restricts it to exactly the residue domain. No unit-orbit reduction is present.

Scope and reservations

The mathematical verdict rests on this reviewer's independently completed whole n10 enumeration, supported by an audit of the two author programs and their complete receipts. The reviewer did not read author attempt notes or other panel reviews. Agreement with receipt numbers alone would not have sufficed.

No correctness mismatch, incomplete n10 range, or nondeterministic decision was found. A concrete portability prerequisite remains for the author wrappers: their output directories must exist before execution. REALISTIC scenario: a file-only export omits empty directories, causing the wrappers to fail when writing results. Conditional probability if the directories are absent: effectively certain. Correction cost: create the two directories before execution, under one minute. They existed in the originally reviewed package. Documenting and satisfying this prerequisite is sufficient; it does not affect the completed exclusion.

Novelty and external publication status are outside this reproduction verdict. The mathematical opinion is unchanged by this editorial export.

pass:true
