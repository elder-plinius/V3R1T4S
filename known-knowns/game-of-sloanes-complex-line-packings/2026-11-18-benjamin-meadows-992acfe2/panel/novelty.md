# NOVELTY verdict: game-of-sloanes-complex-line-packings, cell (d, n) = (7, 19)

context: fresh reviewer (new context started for the NOVELTY role only; saw only CLAIM.md, object/ and public pages; no access to the search code or the claimant's checker)
verdict_utc: 2026-11-18T00:33:03Z

## Value computed here
- Method: own script, mpmath at 50 digits; layout = real parts of all 19 vectors vector by vector, then imaginary parts; each vector normalised; mu = max over all 171 pairs of |<phi_j,phi_k>|. Fingerprints (rotation, phase and permutation invariant): sorted list of all pairwise |overlaps| and the eigenvalues of the frame operator.
- Object 7x19_bmea.txt (sha256 992acfe275d9130797743c01024fb7741a1317458a47a32d45a6918de64e7a87; CLAIM.md states 992acfe275d9130797743c01024fb7741a1317458a47a32d45a6918de64e7a87, match): mu = 0.30883640020136799853 (claim states about 0.30883640020136). Shortest number in the file has 17 significant digits.
- Live table row (7, 19): Best Coherence 0.30884718, Lower Bound 0.30860670, Creator hlc, file CurrentBestPackings/7x19_hlc.txt, Notes "" (no provably-optimal mark). CLAIM.md read the table at 2026-11-18T00:23:25Z as 0.30884718 (hlc); same as live.
- Posted file https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/7x19_hlc.txt fetched 2026-11-18T00:29:32Z HTTP 200 sha256 da6c93125d8b856b694e6dc2a1090714a677d7244e628ea05057152aebcfe675: mu = 0.30884718254029793981 (table 0.30884718, difference 2.54e-9).
- Open PRs 11-19: no file for (7, 19) in any of them (file lists checked one by one).
- Open PR 20 (author TheBenMeadows) file 7x19_bmea.txt: https://github.com/gnikylime/GameofSloanes/raw/cd4bf5ea596b70c1eb9c65e4cad5903018f3e1ca/SubmittedPackings%2F7x19_bmea.txt fetched 2026-11-18T00:30:47Z HTTP 200 sha256 992acfe275d9130797743c01024fb7741a1317458a47a32d45a6918de64e7a87: mu = 0.30883640020136799853.
- README: https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/README.md fetched 2026-11-18T00:26:17Z HTTP 200 sha256 699dbe7157363e568d11e019a0ea98178ec9f52f8834e900587c162801b0502d
- Repository latest commit (gh api repos/gnikylime/GameofSloanes/commits/main, fetched 2026-11-18T00:32:11Z, HTTP 200): e43ad02ab783 dated 2026-04-28T17:04:24Z
- All pull requests to gnikylime/GameofSloanes (gh pr list --state all, fetched 2026-11-18T00:26:19Z, HTTP 200, sha256 7f0d4cd2172b6ffcff8eebcf4b467c2c6a84caf9182c5239a1541fa856f0d650): 20 total, open = 11-20; newest merge was PR 10 on 2026-04-21 and newest close was PR 5 (2025-08-21), so no pull request was merged or closed since 2026-04-28. Per-PR file lists via gh api repos/gnikylime/GameofSloanes/pulls/<N>/files --paginate fetched 2026-11-18T00:26:38Z, HTTP 200.
- V3R1T4S prior claims: gh pr list --repo elder-plinius/V3R1T4S --state all --limit 2000 fetched 2026-11-18T00:27:05Z HTTP 200 (1082 PRs, sha256 2ce4bc55580abd6a1ad6820e4676232d0e2ce592f0a8a67176b451cdd15aa9b9); gh search prs "game-of-sloanes" HTTP 200 (3 hits: #847 merged d=5 n=49, #856 open (5,47) (6,40) (6,41) (4,11), #1114 open d=3 n=34; sha256 6b0a9e8752ae70199cfa4620a86a45240fd1fa97dd97f340630c026ee26cced5); TROPHY_CASE.md on main fetched 2026-11-18T00:27:26Z HTTP 200 sha256 83af764f5a6551a5a27bbb135324931659bda04e60b66a2c0e711b991b356113 (no Game of Sloanes entry); known-knowns/game-of-sloanes-complex-line-packings/ on main fetched 2026-11-18T00:32:09Z HTTP 200 sha256 6be91bc32f8be4eed1857f13eed1c45597443e29b5e4c6e0b7d4de8162a4b8cf (one folder, 2026-10-30-zerbytheboss-421cee37, cell 5x49 only).
- Literature: http://export.arxiv.org/api/query?search_query=all:%22complex%20line%20packing%22%20OR%20all:%22Game%20of%20Sloanes%22%20OR%20all:%22Grassmannian%20frames%22&sortBy=submittedDate&sortOrder=descending&max_results=15 fetched 2026-11-18T00:27:33Z HTTP 200 sha256 4034bb4fe3803721e7b0ea13df25fe806f70ec7a69b74882c4d487986e3ffced; 15 results, newest 2510.08638 (unrelated); the only table-relevant entries are 1907.07848 (the Game of Sloanes paper itself, whose values the table already carries) and 2504.21084 (a genetic-algorithm frame search; its abstract states no per-cell coherence values). No result gives a value for any cell.

## Clauses checked
- Object below the live table value by at least 1e-8: PASS (0.30884718 - 0.30883640020136 = 1.0780e-5).
- Posted file reproduces the table value (layout check): PASS (recomputed 0.308847182540 vs 0.30884718).
- Object is not the posted file or a unitary/phase/permutation copy of it: PASS (coherence gap 1.078e-5; sorted-overlap fingerprints differ by up to 1.078e-05; frame-operator eigenvalues differ by up to 3.584e-02).
- Row not marked provably optimal: PASS.
- Object mu at or above the listed lower bound 0.30860670: PASS (margin 2.2970e-4).
- Object at least 1e-7 below every other open-PR packing for this cell: PASS (no open PR other than 20 has a file for this cell).
- PR 20 file is the same data as the object: PASS (byte-identical, same sha256 992acfe275d9130797743c01024fb7741a1317458a47a32d45a6918de64e7a87).
- No pull request to gnikylime/GameofSloanes merged or closed since 2026-04-28: PASS (newest merge 2026-04-21, before the latest main commit of 2026-04-28T17:04:24Z).
- No prior V3R1T4S claim covers (7, 19): PASS (the three Game of Sloanes claims cover (5,49), (5,47)/(6,40)/(6,41)/(4,11) and (3,34); a title scan of all 1082 PRs for sloane/packing/coherence/C^/mu= found no other; TROPHY_CASE.md has no Game of Sloanes entry; known-knowns folder on main holds only 5x49).
- No newer literature value for (7, 19) in the shared arXiv search: PASS (see source line above).

## Decision
The object reaches mu = 0.30883640020136, 1.078e-5 below the live table value 0.30884718 (hlc) and below every packing in the other open pull requests; it is a distinct packing from the posted file by coherence and frame spectrum, and open PR 20 holds the same packing. Both the object and the posted hlc file are equiangular (all 171 overlaps equal to within 1e-6), so the sorted-overlap fingerprint differs only by the coherence gap; the frame-operator eigenvalues differ by 0.036, so the object is a different equiangular arrangement with a smaller common angle, not a copy of the posted file. Residual risk not checked: unpublished or non-GitHub results (other forks, preprints outside the single arXiv query, private submissions to the maintainers), and pull requests opened after the fetch times above.

pass: true
