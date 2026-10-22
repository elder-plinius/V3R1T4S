# Honesty gate (cage-upper-bounds)

status: CONFIRMED_PARTIAL
confirmed_scope: Under the forward-arc cycle convention that the source paper's table uses, the object is a connected [2,8;6]-mixed graph on 234 vertices (every vertex 8 edges, 2 in-arcs, 2 out-arcs, girth exactly 6), which is a partial win p2 against the listed upper bound 252 for [2,8;6] in arXiv 2506.20003 Table 1, and not a cage record.

## Gate notes
- Object: object/mixed_z2_r8_g6_N234.json, sha256 64e5ed7fd2e7c94e5ac9c7273d7e2abaefaa4d63d4c7816e1ec26a1058b599d4.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the package folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- Refile of the contributor's PR #103, closed unmerged on 2026-10-14 in the bulk close of about thirty early PRs during a handoff, not for a defect.
- Girth 6 holds under the forward-arc cycle convention (direction-blind girth is 4). The panel found the source table itself uses that convention: several of its listed values are impossible under the direction-blind reading (for example 196 is below the Moore bound 222 for an 11-regular girth-6 graph).
