context: Claude Code subagent, fresh context [Sonnet 5.5]

Novelty review, claim leancamcombi-bkr-reimer-inequality (read the claim record). All checks used read-only `gh api` GET / search calls, one per page, no retries, no failures. Every fetch (UTC time, endpoint, exit code, sha256 of body) is in a working file (not shipped) (about 40 lines). The log records exit code 0, not an HTTP status line. All times below are from that log on 2026-11-15 (UTC).

Primary status source (fetched once)
- https://github.com/YaelDillies/LeanCamCombi/issues/34 (API: repos/YaelDillies/LeanCamCombi/issues/34): state "open", title "Van den Berg-Kesten-Reimer inequality", last updated 2025-01-24, 0 comments, no closed_at. Timeline holds only project-board events (no cross-referencing PR). The repository now lives at YaelDillies/cam-combi (the old name redirects). Last push 2026-11-12.
- Master head, repos/YaelDillies/LeanCamCombi/commits/master: 0a42535119073f677dd60a28acbbdcda11b87f60, committed 2026-11-11T13:51:59Z. This is exactly the commit the claim names.
- Live file CamCombi/PlainCombi/VanDenBergKesten.lean (blob sha 8a8eb49e...) line 105 reads: `lemma card_certificator_le : 2 ^ Fintype.card α * #(𝒜 □ ℬ) ≤ #𝒜 * #ℬ := sorry`. It is the only sorry in the file. So the lemma is still unproved on master at fetch time. Only one commit ever touched the file (09d15d0b, a library rename, 2026-07-14).

Pull requests in the repository (34 PRs listed, state=all; PRs 3 to 56)
- No PR title mentions certificator, Reimer, BKR, van den Berg or Kesten. Issue/PR searches in the repository for "certificator", "Reimer" and "Kesten" return only issue #34 itself (certificator: 0 hits).
- The three open PRs (#50 IntersectingFamilies, #46 ApproximateSubgroup, #21 Symmetric Chain Decomposition) have changed-file lists that do not include VanDenBergKesten.lean. No PR, open or merged, touches that file or proves the lemma.
- 3 releases exist; I did not find any release asset claiming the proof (the release list was only counted, not each asset inspected). The master tree is current to two days ago.

Mathlib (leanprover-community/mathlib4)
- Code search for "Reimer", "certificator", "BKR": 0 hits. "vanDenBerg" hits are unrelated files (references.bib, convex cone, triangulated generators). Issue/PR search for Reimer, certificator, "van den Berg Kesten", "BKR inequality": 0 hits. Nothing in Mathlib proves or states the BKR/Reimer inequality. (Search-index caveat: GitHub code search is incomplete; this is a negative from the index, not a proof of absence.)

Other formalisations found
- facebookresearch/atlas-lean (Meta): MathlibExt/Probability/CorrelationInequalities/Reimer.lean says plainly that it "does not prove it"; it states ReimerWprobCore as a Prop, proves reductions, the n = 0 case and the decreasing-events (BK) case. WantedExt/Probability/ReimerInequalityWanted.lean lists `reimer_inequality` and `reimer_wprob_core` as `theorem_wanted`. So that development leaves the general inequality unproved. I did not read ReimerDoubled/Compression/FamilyEvents/SpecialCases files in full; their names suggest partial cases, and a grep for "sorry" in the three files I fetched found none (they use the Prop-hypothesis style instead).
- Mirror/ingest copies of VanDenBergKesten.lean (competemath/emissary-archangel exports, uw-math-ai/TheoremSearch, weiyangzen/awesome_theorems) are copies of the sorry statement, not proofs.
- I found no public Lean, Isabelle or Coq proof of the general Reimer inequality through GitHub search. I did not search outside GitHub (no arXiv or Archive of Formal Proofs query was run), so this is a GitHub-only result. A proof in another system would not block this target anyway.

V3R1T4S repository (elder-plinius/V3R1T4S)
- the target's own page in the repository's known-unknowns folder is the bank entry (open as of 2026-10-30), not a claim. known-knowns (32 entries listed) has nothing on this lemma. TROPHY_CASE.md has no mention of certificator, Reimer, BKR, Kesten or camcombi. PR search (all states) for Reimer, bkr, card_certificator_le, leancamcombi returns 0; "van den Berg" returns only three percolation PRs (#458, #481, #778), unrelated. I listed the first 200 PRs (newest first, numbers about 882 to 1096 plus closed ones); older PRs were covered by the keyword searches only. No existing claim on this lemma.

Limits
- This review checked novelty only. It did not compile or check the claimed proof.
- Master is a moving target; the verdict holds as of the fetch times in a working file (not shipped) (master 0a425351 at 2026-11-11 commit time, fetched 2026-11-15).

novelty: PASS. The lemma is still `sorry` on live master, issue #34 is open with no linked PR, no PR in that repository touches the file or proves it, Mathlib has nothing, and V3R1T4S holds no prior claim.

pass: true
