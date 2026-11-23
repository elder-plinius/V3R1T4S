context: Claude Code subagent, fresh context [Sonnet 5.5]

novelty: HOLDS (the target is still open and unclaimed as of 2026-11-17)

What I checked (all reads, no writes; every fetch is logged with UTC time, URL, status and sha256 in the fetches log in work-novelty, plus the gh calls):

1. Live status source. The claim names https://github.com/ImperialCollegeLondon/FLT/issues as the status source. I read the file at https://raw.githubusercontent.com/ImperialCollegeLondon/FLT/main/FLT/Patching/Utils/CompactHausdorffRings.lean at 2026-11-17T04:11:53Z (HTTP 200). `Group.subsingleton_of_pow_prime_eq_one` is still stated with `@[to_additive]` and ends in `:= by sorry` (lines 37-42). The statement matches the package's. FLT main (https://api.github.com/repos/ImperialCollegeLondon/FLT/commits/main, 2026-11-17T04:11:54Z, 200) is still a3210204ad88..., dated 2026-10-22, the same commit the claim pins. The file's last commit is a Mathlib bump from 2026-07-29, so nothing new touched it.

2. Open pull requests. I listed all 40 open PRs (2026-11-17T04:12:05Z, 200) and fetched the changed-file list of each via gh. None touches CompactHausdorffRings.lean or anything under Patching/Utils. The one closed PR the search finds for that file name (#898, a partial proof that compact Hausdorff rings are totally disconnected) is a different lemma and is not merged here. Searches for "subsingleton_of_pow_prime" in FLT issues and PRs return 0 hits; "subsingleton" returns only unrelated items (#1155 is the GL0 sorries PR, not this file).

3. Issues, claims, blueprint. Issue searches by title and body for compact, Hausdorff, subsingleton, divisible, totally disconnected, Pontryagin and rootable found no issue about this lemma and no assignee on any such issue (the only hit, #258 "A_Q / Q is compact", is unrelated). I could not view the org project board (needs sign-in) and did not fetch the blueprint page, so a claim recorded only there is unchecked. That is the one residual gap.

4. Duplicate-in-repo condition. The file's own downstream lemmas (`Group.totallyDisconnected_of_pow_prime_eq_one`, rootable, divisible) use this lemma; no other name in FLT proves it.

5. Mathlib. A gh code search of leanprover-community/mathlib4 for the lemma name and for exponent/connected/compact subsingleton phrasing found nothing. Mathlib has Topology/Algebra/PontryaginDual.lean, but only basic instances (locally compact, finiteness for discrete compact), not the duality theorem needed. A PR search on Pontryagin dual with connected compact returned nothing. I found no Mathlib one-liner that closes the sorry.

6. V3R1T4S. TROPHY_CASE.md has no mention of FLT, Imperial or this lemma. Code search for the lemma name and CompactHausdorff in elder-plinius/V3R1T4S finds only the bank entry the target's own page in the repository's known-unknowns folder (the target itself, which lists this lemma as p1 partial win, i.e. it is the open target, not a claim). Searches of V3R1T4S PRs for FLT returned no results. No known-knowns entry matches.

7. Other code. External hits only list the sorry (Graphenium gap list, SNAPKITTYWEST audit, competemath/emissary-archangel export, which contains the sorried statement). The unsubmitted fork futarchy-fi/FLT has no copy of this lemma name (code search empty); its open PRs are in the fork, not upstream, and are not bars.

Limits: gh code search is an index and can lag; GitHub search of FLT PRs for text is not file-level, which is why I checked file lists of all 40 open PRs directly. Literature search was limited to code/repo hits; I found no published formal proof of this exact lemma. The claim's own snapshot says fetched 2026-11-16T16:55:45Z; my fresh read about 11 hours later agrees.

All eligibility conditions I could check hold: Prop-valued theorem, still sorry, no open or merged PR touches it, no issue or assignee, not proved elsewhere in the repo, statement does not depend on a sorried definition (it is plain topological group hypotheses), Mathlib does not already supply it. Residual: project board and blueprint not viewed.

pass: true
