context: Claude Code subagent, fresh context [Sonnet 5.5]

novelty: PASS on the evidence below.

Sources relied on (all in a working copy (not shipped); one request each, no retries, no blocks):
- 2026-11-16T03:0x UTC, GET https://api.github.com/repos/google-deepmind/formal-conjectures/contents/FormalConjectures/WrittenOnTheWallII/GraphConjecture25.lean (HTTP 200, saved as work-novelty/f25.lean). Live main head at the time was f50ff7be (2026-11-15T22:20Z). The theorem conjecture25 is tagged `@[category research solved, AMS 5]`, is stated as the negation of the universal claim, and its body is `sorry`. No `formal_proof` attribute anywhere in the file. Docstring says status F, disproved, same counterexample as Conjecture 24.
- Same time, GET .../commits?path=...GraphConjecture25.lean: the only commit touching the file is 4eee17ca (2026-10-23, PR #3796, "Add eight WOWII graph conjectures (batch 2)"). No later change, so no proof or link was ever merged.

FC pull request search (gh pr list, state all, a working file (not shipped), a working file (not shipped), a working file (not shipped)):
- Searched "GraphConjecture25", "Conjecture25", "conjecture 25", "WOWII 25", "WrittenOnTheWallII", plus "GraphConjecture24", "conjecture 24", "distEven", "dist_even", "WOWII", "Graffiti". That gave 210 distinct candidate PRs (open, merged, closed). For each I listed the changed files and kept any touching GraphConjecture25 (or 24).
- Result: only PR #3796 (merged 2026-10-23) touches GraphConjecture25.lean (it created it with the sorry). The other two raw matches (#7366, #7367) are GraphConjecture252 and 253, a prefix false match. No open or closed PR proves conjecture 25, adds a formal_proof for it, or touches GraphConjecture24.
- The "conjecture 25" search returned only unrelated hits (e.g. #25 README typo). Titles of the open WOWII PRs (#6956, #4161, #7248, #7665, #7792, etc.) concern other numbers.
- Limits: GitHub search is title/body text; a PR that bundles many files and never mentions 25 would be caught only if it was among the 210 candidates. Release assets: FC has no release stream relevant here, not checked beyond main.

V3R1T4S repository (elder-plinius/V3R1T4S, read-only gh/curl at the same time):
- TROPHY_CASE.md (HTTP 200): no mention of GraphConjecture25, WrittenOnTheWallII or fc-graffiti.
- Full tree listing (7564 paths): nothing named for GraphConjecture, WrittenOnTheWall or a fc-graffiti trophy or claim. Only the target's own page in the repository's known-unknowns folder (the bank target itself), which lists 25 as unclaimed at 2026-10-28.
- PR search (all states) for GraphConjecture25, conjecture25, WrittenOnTheWallII, formal-conjectures, Graffiti, WOWII: nothing about this theorem (two unrelated hits #841, #492).

Literature: the claim is a formal disproof of a conjecture the WOWII page already marks false (status F), so the mathematical fact is not new; the criterion asks only that the FC theorem be unproved and unclaimed, which holds. Residual note: the claim package must restate the statement verbatim; I did not compile or diff the package (out of scope for novelty).

pass: true
