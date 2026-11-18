# NOVELTY verdict: game-of-sloanes-complex-line-packings, cell (d, n) = (3, 38)

context: fresh reviewer (new context started for the NOVELTY role only; saw only CLAIM.md, object/ and public pages; no access to the search code or the claimant's checker)
verdict_utc: 2026-11-18T00:33:03Z

## Value computed here
- Method: own script, mpmath at 50 digits; layout = real parts of all 38 vectors vector by vector, then imaginary parts; each vector normalised; mu = max over all 703 pairs of |<phi_j,phi_k>|. Fingerprints (rotation, phase and permutation invariant): sorted list of all pairwise |overlaps| and the eigenvalues of the frame operator.
- Object 3x38_bmea.txt (sha256 a92052bf04a83b879bb98e662333aa98651f5a87c1b154b63d7241d107625f8f; CLAIM.md states a92052bf04a83b879bb98e662333aa98651f5a87c1b154b63d7241d107625f8f, match): mu = 0.77188415329493526906 (claim states about 0.77188415329493). Shortest number in the file has 18 significant digits.
- Live table row (3, 38): Best Coherence 0.77189089, Lower Bound 0.67612340, Creator bmem, file CurrentBestPackings/3x38_bmem.txt, Notes "" (no provably-optimal mark). CLAIM.md read the table at 2026-11-18T00:23:25Z as 0.77189089 (bmem); same as live.
- Posted file https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/3x38_bmem.txt fetched 2026-11-18T00:29:17Z HTTP 200 sha256 c0ce6c4ab12d9d4fe8c9f1781d1fc7a5bac6107ec64c5ceb36cf61891fe14686: mu = 0.77189089270668656349 (table 0.77189089, difference 2.71e-9).
- Open PR 14 (author dustinmixon) file 3x38_sol.txt: https://github.com/gnikylime/GameofSloanes/raw/04831504e5e74f42ca6742315a2eb2366503a10a/SubmittedPackings%2F3x38_sol.txt fetched 2026-11-18T00:29:41Z HTTP 200 sha256 7aa9d1a7dec4c4c91f3397422f01561ed783a5592cfb5fe0a1a58072bf004bee: mu = 0.77188789852848351835.
- Open PR 18 (author owhs) file 3x38_owhs.txt: https://github.com/gnikylime/GameofSloanes/raw/b0f64bccff9751542f9cb0803131542e37cb75e5/SubmittedPackings%2F3x38_owhs.txt fetched 2026-11-18T00:29:54Z HTTP 200 sha256 98639b66cfad9ed59ada984c9f36e083675e7dcfbbea1e7c245598cc66682722: mu = 0.7718851788436402057.
- Open PR 20 (author TheBenMeadows) file 3x38_bmea.txt: https://github.com/gnikylime/GameofSloanes/raw/cd4bf5ea596b70c1eb9c65e4cad5903018f3e1ca/SubmittedPackings%2F3x38_bmea.txt fetched 2026-11-18T00:30:20Z HTTP 200 sha256 a92052bf04a83b879bb98e662333aa98651f5a87c1b154b63d7241d107625f8f: mu = 0.77188415329493526906.
- README: https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/README.md fetched 2026-11-18T00:26:17Z HTTP 200 sha256 699dbe7157363e568d11e019a0ea98178ec9f52f8834e900587c162801b0502d
- Repository latest commit (gh api repos/gnikylime/GameofSloanes/commits/main, fetched 2026-11-18T00:32:11Z, HTTP 200): e43ad02ab783 dated 2026-04-28T17:04:24Z
- All pull requests to gnikylime/GameofSloanes (gh pr list --state all, fetched 2026-11-18T00:26:19Z, HTTP 200, sha256 7f0d4cd2172b6ffcff8eebcf4b467c2c6a84caf9182c5239a1541fa856f0d650): 20 total, open = 11-20; newest merge was PR 10 on 2026-04-21 and newest close was PR 5 (2025-08-21), so no pull request was merged or closed since 2026-04-28. Per-PR file lists via gh api repos/gnikylime/GameofSloanes/pulls/<N>/files --paginate fetched 2026-11-18T00:26:38Z, HTTP 200.
- V3R1T4S prior claims: gh pr list --repo elder-plinius/V3R1T4S --state all --limit 2000 fetched 2026-11-18T00:27:05Z HTTP 200 (1082 PRs, sha256 2ce4bc55580abd6a1ad6820e4676232d0e2ce592f0a8a67176b451cdd15aa9b9); gh search prs "game-of-sloanes" HTTP 200 (3 hits: #847 merged d=5 n=49, #856 open (5,47) (6,40) (6,41) (4,11), #1114 open d=3 n=34; sha256 6b0a9e8752ae70199cfa4620a86a45240fd1fa97dd97f340630c026ee26cced5); TROPHY_CASE.md on main fetched 2026-11-18T00:27:26Z HTTP 200 sha256 83af764f5a6551a5a27bbb135324931659bda04e60b66a2c0e711b991b356113 (no Game of Sloanes entry); known-knowns/game-of-sloanes-complex-line-packings/ on main fetched 2026-11-18T00:32:09Z HTTP 200 sha256 6be91bc32f8be4eed1857f13eed1c45597443e29b5e4c6e0b7d4de8162a4b8cf (one folder, 2026-10-30-zerbytheboss-421cee37, cell 5x49 only).
- Literature: http://export.arxiv.org/api/query?search_query=all:%22complex%20line%20packing%22%20OR%20all:%22Game%20of%20Sloanes%22%20OR%20all:%22Grassmannian%20frames%22&sortBy=submittedDate&sortOrder=descending&max_results=15 fetched 2026-11-18T00:27:33Z HTTP 200 sha256 4034bb4fe3803721e7b0ea13df25fe806f70ec7a69b74882c4d487986e3ffced; 15 results, newest 2510.08638 (unrelated); the only table-relevant entries are 1907.07848 (the Game of Sloanes paper itself, whose values the table already carries) and 2504.21084 (a genetic-algorithm frame search; its abstract states no per-cell coherence values). No result gives a value for any cell.

## Clauses checked
- Object below the live table value by at least 1e-8: PASS (0.77189089 - 0.77188415329493 = 6.7367e-6).
- Posted file reproduces the table value (layout check): PASS (recomputed 0.771890892706 vs 0.77189089).
- Object is not the posted file or a unitary/phase/permutation copy of it: PASS (coherence gap 6.739e-6; sorted-overlap fingerprints differ by up to 4.365e-02; frame-operator eigenvalues differ by up to 7.511e-02).
- Row not marked provably optimal: PASS.
- Object mu at or above the listed lower bound 0.67612340: PASS (margin 9.5761e-2).
- Object at least 1e-7 below every other open-PR packing for this cell: PASS (lowest other: PR 18 3x38_owhs.txt mu 0.77188517884364, gap 1.0255e-6; PR 14 gap 3.7452e-6; PR 18 gap 1.0255e-6).
- Object is none of the other open-PR packings (fingerprints): PASS (PR 14: overlap-fingerprint diff 6.131e-02, eigenvalue diff 9.183e-02; PR 18: overlap-fingerprint diff 5.445e-02, eigenvalue diff 7.905e-02).
- PR 20 file is the same data as the object: PASS (byte-identical, same sha256 a92052bf04a83b879bb98e662333aa98651f5a87c1b154b63d7241d107625f8f).
- No pull request to gnikylime/GameofSloanes merged or closed since 2026-04-28: PASS (newest merge 2026-04-21, before the latest main commit of 2026-04-28T17:04:24Z).
- No prior V3R1T4S claim covers (3, 38): PASS (the three Game of Sloanes claims cover (5,49), (5,47)/(6,40)/(6,41)/(4,11) and (3,34); a title scan of all 1082 PRs for sloane/packing/coherence/C^/mu= found no other; TROPHY_CASE.md has no Game of Sloanes entry; known-knowns folder on main holds only 5x49).
- No newer literature value for (3, 38) in the shared arXiv search: PASS (see source line above).

## Decision
The object reaches mu = 0.77188415329493, 6.737e-6 below the live table value 0.77189089 (bmem) and below every packing in the other open pull requests; it is a distinct packing from the posted file by coherence and frame spectrum, and open PR 20 holds the same packing. Residual risk not checked: unpublished or non-GitHub results (other forks, preprints outside the single arXiv query, private submissions to the maintainers), and pull requests opened after the fetch times above.

pass: true
