# Independent REPRODUCE review

context: fresh independent subagent; research inputs restricted to claim/; workflow instructions read from repo/AGENTS.md and kit rules.
verdict: SURVIVES — saved-object numerical reproduction.
review_completed_utc: 2026-10-16T00:02:45.635786+00:00

The checker in ../panel/reproduce-work/independent_check.py and its derivation in ../panel/reproduce-work/derivation.md were written and run before opening the author's verify.py. No attempts, parent reports, other reviewers, or prior rejected claims were read. All file references in this report are relative to claim/.

Quoted definition from target.json:

> the FEASIBLE radius r* := min( min_{i<j} |c_i - c_j| / 2, 1 - max_i |c_i| ) (unit container ball centred at the origin), computed in mpmath at 50 digits directly from the submitted coordinates with no tolerance

NUMERICAL: I used mpmath 1.4.1 with mp.dps=50, constructing each coordinate directly from its submitted decimal string. For each of candidate.txt, posted.txt and prior-moki-119.txt, the checker evaluates every one of the 7021 unordered pairs and all 119 center norms/walls. It checks 476 coordinate tokens per object. There is no sampling or feasibility tolerance.

| Object | Recomputed feasible radius at 50 digits | Limiting constraint |
|---|---|---|
| candidate.txt | 0.23606892889364886505664445893098935298010907228947 | pair 18, 78 |
| posted.txt | 0.236068068182399835049801073000699386917878694583 | wall 92 |
| prior-moki-119.txt | 0.23606869597929028946544883264916203897792471496589 | wall 91 |

Indices are one-based. The candidate's smallest wall clearance is 0.23606892889364893030105085677053991319349300944365 at center 42. Every pair and wall passes at the computed radius.

NUMERICAL: The saved hsp4_radius.txt value at N=119 is 0.236068068183. The candidate gain is 0.00000086071064886505664445893098935298010907228946624385, exceeding the required 1e-10. The posted-object radius minus the table is -0.00000000000060016495019892699930061308212130541699568986579886; its absolute magnitude is below the explicitly specified 1e-11 parser sanity threshold. That sanity threshold is not used to excuse candidate overlaps. The posted decimal header itself is slightly infeasible at the printed coordinates, as independently documented in the exact header checks.

NUMERICAL: The candidate minus the independently recomputed Moki & Julio radius is 0.00000023291435857559119562628182731400218435732357138843. The prior object's header matches its unique hsp4,N=119 row in moki-manifest.csv; its header radius was also exactly certified from its centers, with no reliance on the external project's checker or verdict.

NUMERICAL: All 7021 entries of the sorted pairwise-distance lists were compared. The maximum absolute difference is 0.0096922017941812197496703550877266046816487656763648 at rank 5461, strictly greater than 1e-8. The corresponding candidate and posted distances are 1.2681517578510427940713207460599877401831843360207 and 1.277843959645224013820991101147714344864833101697.

PROVED-HERE: Treating the submitted decimals as exact rationals, every squared pair separation is at least 4r^2 and every squared center norm is at most (1-r)^2 at the conservative radius r=0.236068928893648865. The minimum exact pair slack is 10697597398079151177/100000000000000000000000000000000000000; the minimum exact wall slack is 124713754313457562250827/1250000000000000000000000000000000000000. Both are positive. The exact feasible radius lies in [0.236068928893648865, 0.236068928893648866); the upper endpoint violates the active pair. This is a finite, exhaustive rational proof of a feasible construction, with no interval or floating-point decision.

PROVED-HERE: The full printed radius in CLAIM.md, 0.2360689288936488650566444589309893529801090722894663, is also exactly feasible. Its minimum squared pair slack is 15020497907737473959949367263229020652257966206116431/25000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 > 0. Its 50-digit mpmath value agrees with the independent calculation.

PROVED-HERE: The prior object's exact feasible radius lies in [0.236068695979290289, 0.236068695979290290). The candidate's certified lower bound exceeds that upper endpoint by 0.000000232914358575 and exceeds the exact saved table decimal by 0.000000860710648865. Thus both improvements also hold in exact rational inequalities.

PROVED-HERE: Exact Fraction-sorted squared-distance multisets differ. At the reported rank, writing A >= B for the squared distances and t=1e-8, I verified A-B-t^2 > 0 and (A-B-t^2)^2 > 4t^2 B. These are exact sufficient inequalities for sqrt(A)-sqrt(B) > t, so the non-isometry threshold is independently certified without relying solely on rounded square roots.

Verification controls: the exact tangent two-ball packing is accepted, an oversized radius is rejected, and an independent wall-violating example is rejected. 5 malformed parser controls are rejected. Each input has exactly 119 distinct finite four-dimensional centers; posted indices are sequential and unique. The table has 299 unique 12-decimal rows with the stated index coverage. Two complete executions produced identical results apart from timestamps. All 13 SHA256SUMS entries and all 6 saved-source object hashes match. Candidate SHA256: c31c7de024b28524004dbc60e437ad3056eaa8a18272e073e1e764c7267c4cf0.

After those independent checks were completed, I read and ran verify.py. Its saved-object check passed and agreed with the independent results. That corroborating output is in ../panel/reproduce-work/author-checker-output.txt; it is not the basis of this verdict.

Evidence and rerun: from claim/, run `python -X utf8 ../panel/reproduce-work/independent_check.py` with mpmath available. Complete captured results are ../panel/reproduce-work/independent-output.json and ../panel/reproduce-work/independent-output-repeat.json. The before-author-code and deterministic-repeat record is ../panel/reproduce-work/independence-and-repeat.json. Exhaustive pair/wall ledgers are ../panel/reproduce-work/candidate-constraints.csv, ../panel/reproduce-work/posted-constraints.csv and ../panel/reproduce-work/prior-constraints.csv. The entire sorted-distance comparison is ../panel/reproduce-work/sorted-distance-comparison.csv.

Scope and caveat: this pass establishes reproduction from the saved objects. Source-record hashes establish package consistency; they do not authenticate a current live table. The saved source fetches precede this resumed review by more than the gate's six-hour window, so the live-table/history/queue and literature verdicts require current independent checking. The saved pending-requests.html retains the category-unspecified 26-Sep-2026 Moki & Julio 4666-candidate bundle. Its contents remain unresolved by reproducing one same-cell certificate; N=119 must be rechecked against the live table when that bundle disappears. No optimality, exhaustive search, or broad novelty claim is established by this review.

Credit: Eckard Specht's Packomania table and posted coordinates, and Moki & Julio's public comparison certificate, are identified with source URLs and saved fetch metadata in source-records.json. External text was treated as data. No outward action was taken.

pass: true
