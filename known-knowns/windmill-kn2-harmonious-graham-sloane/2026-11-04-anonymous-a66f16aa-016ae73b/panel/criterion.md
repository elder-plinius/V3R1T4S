---
role: criterion skeptic
confirmed_scope: There is no injective labeling of the 19 vertices of two copies of K10 sharing exactly one vertex by residues modulo 90 for which the 90 within-clique edge sums are all distinct modulo 90.
---

The exact finite mathematical exclusion passes the selected partial-win p1 computational criterion. The original independent review reran both supplied programs over their full n=10 domains and audited the reductions and pruning from the definition. This verdict covers the mathematical and computational criterion. Novelty and literature priority were not checked in this review and require a separate assessment. The result does not establish the general windmill conjecture or decide another n.

### Literal criterion and independence

The selected partial win is “The same (a) or (b) decision for n = 10 (19 vertices, q = 90).” The negative branch requires an exhaustive search by two independent programs. No statistical null model is needed: this is a universal finite nonexistence statement, not an inference from sampling. The domain includes every injective assignment from all 19 vertices into the 90 residues, with both cliques' 90 edges considered together. Pairwise distinct edge sums necessarily fill the group. There are no additional edges between the two cliques' noncentral vertices.

The two programs meet the program-level independence requirement. [Method 1](../how-we-built-it/method1/ComplementSearch.cs) enumerates single cliques and matches complementary masks in a dictionary. [Method 2](../how-we-built-it/method2/DirectConstraintWide.cs) directly grows two cliques with candidate propagation and a parity constraint. They do not share search functions, stored enumerations, or each other's answers. Common use of center normalization, sorted labels, C#, UInt128, and the same runtime is disclosed. These are distinct implementations and distinct decision procedures; the review does not establish separate authorship or independent compiler implementations. The quoted criterion does not require those stronger conditions.

The following completeness arguments support the finite exclusion documented in [the proof](../object/PROOF.md).

### Symmetry and exhaustive domain

For an arbitrary solution with shared-vertex label c, replace every vertex label f(v) by f(v)-c modulo 90. Injectivity is preserved, the shared vertex becomes zero, and every edge sum translates by -2c. Translation of residues is bijective even though 2 is not a unit modulo 90; no inversion of 2 is needed. Therefore center-zero search loses no solution.

The other nine labels of each clique are distinct nonzero residues and can be sorted increasingly by permuting the clique's noncentral vertices. Their smallest label ranges from 1 to 81 inclusive, because nine values must fit in 1 through 89. Both independent reruns completed exactly those 81 roots. The programs do not fix that smallest value to 1, quotient by clique interchange, or use multiplication by units. No additional unit-orbit justification is needed.

### Method 1: enumeration and complementary masks

At depth d, `Labels[0..d-1]` is an increasing center-zero clique and `sumMask` contains exactly its distinct edge sums. Appending x tests x plus every existing label modulo 90 against both old and newly added sums. The upper loop bound `90-(10-d)` merely reserves enough larger labels to finish the clique. Every valid sorted clique is therefore reached once, and each leaf has 45 sum bits.

At a leaf, the program looks for `FullMask XOR sumMask`. Both masks lie wholly inside the 90-bit universe, so this is exactly the complementary 45-residue set. Storing only one label representative for each sum mask is safe: every noncentral label x is also the sum of its edge to the zero center. Thus two complementary masks cannot have any noncentral vertex label in common, regardless of which representative is stored. Together their cliques give exactly 19 distinct labels and 90 distinct edge sums. Conversely, any harmonious labeling yields two complementary masks, and whichever leaf is visited second finds the first mask. No additional pairing test or hidden disjointness restriction is missing.

### Method 2: direct search and pruning

The candidate invariant is: each candidate is greater than the last selected label and all its sums with the current clique's existing vertices avoid `used`. While constructing the second clique, `used` includes the completed first clique's edge sums. New sums from one candidate are mutually distinct because the existing clique labels are distinct modulo 90.

`BackShift(S,t)` gives exactly the labels y with y+t in S modulo 90. In `Extend`, the old candidate set already excludes collisions of y plus old clique vertices with old sums. The new masks exclude y+x in all updated sums and y plus every old vertex in newly added sums. These are exactly the additional forbidden collisions after adding x. Intersecting with `Higher(x)` implements sorting. Population-count pruning only rejects prefixes having too few available labels. The loop's early break is sound because every later candidate has still fewer larger choices.

At the start of the second clique, candidates are all nonzero residues outside the first clique's sum mask. This ensures the next center edge is unused and also excludes every noncentral vertex label of the first clique. Subsequent candidate sets only shrink. Global vertex injectivity is therefore enforced implicitly and correctly. A complete second clique must have `used == full`, which is checked explicitly.

If a center-zero K10 has k odd vertex labels, exactly k(10-k) of its edge sums are odd. A complete labeling must cover all 45 odd residues. The necessary equation is therefore k(10-k)+l(10-l)=45, with k,l in 0..9. Its ordered solutions are (3,4), (3,6), (4,3), (4,7), (6,3), (6,7), (7,4), and (7,6). `OddReachable` bounds possible final odd counts using the numbers of remaining odd and even candidates. Those bounds contain every feasible completion; ignoring further pairwise compatibility can only retain extra impossible prefixes. Rejecting a bound with no permitted pair is safe. The audit identified no unresolved pruning concern requiring an unpruned rerun.

### Wide arithmetic and execution evidence

All masks are UInt128, with bit positions 0..89; full-mask, shift, rotation, and population-count operations preserve that domain. `Higher` shifts by at most 90, never 128. `BackShift` handles shift zero separately, and its final 90-bit mask discards only irrelevant bits. `Pop` and `Low` explicitly handle both 64-bit halves; `Low` is called only on nonzero masks. Search counters, including the 5.8 billion candidate counter, are 64-bit integers.

The original review also checked the direct program's actual arithmetic helpers against simple residue-by-residue expected values: 8,460 rotation checks, 90 `Higher` checks, 94 population counts, and 93 lowest-bit checks, including bits 63, 64, and 89. All passed. These checks supplement the completeness arguments and full-domain executions.

Both full-domain reruns completed without timing out and with empty error output. Their exact root coverage and checked deterministic counters agreed with the supplied receipts. The conclusion rests on independent full executions and the source audit, not receipt agreement alone. Package evidence is provided in the [complement result](../object/receipts/complement-result.json), [constraint result](../object/receipts/constraint-result.json), and [independent result](../object/receipts/independent-result.json).

| Check | Complement search | Direct constraint search |
|---|---:|---:|
| Completed roots | All 1..81 | All 1..81 |
| Search nodes | 522,000,390 | A: 271,924,415; B: 559,147,377 |
| Complete first cliques | 1,702,800 | 1,547,248 after parity pruning |
| Distinct sum masks | 1,571,472 | Not used |
| Result | `exhaustive_no_pair` | `found:false`, `range_complete:true`, `full_domain:true`, `timed_out:false` |

Method 1 also recorded 5,828,815,644 candidate attempts and 131,328 duplicate masks. The code copies used for the original reruns matched the frozen source files byte for byte. The original manifest entries matched SHA-256 before and after execution. The reviewed main source hashes were:

| Source | SHA-256 |
|---|---|
| `ComplementSearch.cs` | `ffbfe989da1765355ad8bc7b6cb5870715fb401f5d63498c77dc9e01d7dc5ac9` |
| `DirectConstraintWide.cs` | `91a3c00e5d5f07b9c2e844a6da6d4e04bbe1eadec0f6d16df2d0065c24456e0c` |

No blocking mathematical or implementation finding was identified. The realistic scope risk is treating this finite decision as a general-conjecture proof or an independently established novelty claim: either assertion would be unsupported by this review. Correcting that overstatement requires only limiting the claim to the confirmed scope above. No speculative hardening or additional test infrastructure is proposed. The scientific verdict is unchanged in this publication edition.

pass:true
