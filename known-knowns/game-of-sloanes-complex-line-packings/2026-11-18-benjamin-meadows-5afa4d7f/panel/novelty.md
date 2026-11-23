# NOVELTY verdict: game-of-sloanes-complex-line-packings, cell (d, n) = (7, 25)

context: fresh reviewer (new context started for the NOVELTY role only; saw only CLAIM.md, object/ and public pages; no access to the search code or the claimant's checker)
verdict_utc: 2026-11-18T00:33:03Z

## Value computed here
- Method: own script, mpmath at 50 digits; layout = real parts of all 25 vectors vector by vector, then imaginary parts; each vector normalised; mu = max over all 300 pairs of |<phi_j,phi_k>|. Fingerprints (rotation, phase and permutation invariant): sorted list of all pairwise |overlaps| and the eigenvalues of the frame operator.
- Object 7x25_bmea.txt (sha256 5afa4d7ffef566ee89999ca24b1c10dcb1450cbc032c34c8b3b316e8255ddbf9; CLAIM.md states 5afa4d7ffef566ee89999ca24b1c10dcb1450cbc032c34c8b3b316e8255ddbf9, match): mu = 0.33206832825399350959 (claim states about 0.33206832825399). Shortest number in the file has 18 significant digits.
- Live table row (7, 25): Best Coherence 0.33247138, Lower Bound 0.32732684, Creator hlc, file CurrentBestPackings/7x25_hlc.txt, Notes "" (no provably-optimal mark). CLAIM.md read the table at 2026-11-18T00:23:25Z as 0.33247138 (hlc); same as live.
- Posted file https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/7x25_hlc.txt fetched 2026-11-18T00:29:34Z HTTP 200 sha256 528d3e625a61ef3baf800df782139f5347ec773c3aa079a8754aa4ee723aeca1: mu = 0.33247138110292098254 (table 0.33247138, difference 1.10e-9).
- Open PR 18 (author owhs) file 7x25_owhs.txt: https://github.com/gnikylime/GameofSloanes/raw/b0f64bccff9751542f9cb0803131542e37cb75e5/SubmittedPackings%2F7x25_owhs.txt fetched 2026-11-18T00:30:05Z HTTP 200 sha256 aa1cf06bcd5484f96ceba542a4c907b4ea727eea7cf3bf7c6f701c45cd344dff: mu = 0.33211991135920991668.
- Open PR 20 (author TheBenMeadows) file 7x25_bmea.txt: https://github.com/gnikylime/GameofSloanes/raw/cd4bf5ea596b70c1eb9c65e4cad5903018f3e1ca/SubmittedPackings%2F7x25_bmea.txt fetched 2026-11-18T00:30:52Z HTTP 200 sha256 5afa4d7ffef566ee89999ca24b1c10dcb1450cbc032c34c8b3b316e8255ddbf9: mu = 0.33206832825399350959.
- README: https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/README.md fetched 2026-11-18T00:26:17Z HTTP 200 sha256 699dbe7157363e568d11e019a0ea98178ec9f52f8834e900587c162801b0502d
- Repository latest commit (gh api repos/gnikylime/GameofSloanes/commits/main, fetched 2026-11-18T00:32:11Z, HTTP 200): e43ad02ab783 dated 2026-04-28T17:04:24Z
- All pull requests to gnikylime/GameofSloanes (gh pr list --state all, fetched 2026-11-18T00:26:19Z, HTTP 200, sha256 7f0d4cd2172b6ffcff8eebcf4b467c2c6a84caf9182c5239a1541fa856f0d650): 20 total, open = 11-20; newest merge was PR 10 on 2026-04-21 and newest close was PR 5 (2025-08-21), so no pull request was merged or closed since 2026-04-28. Per-PR file lists via gh api repos/gnikylime/GameofSloanes/pulls/<N>/files --paginate fetched 2026-11-18T00:26:38Z, HTTP 200.
- V3R1T4S prior claims: gh pr list --repo elder-plinius/V3R1T4S --state all --limit 2000 fetched 2026-11-18T00:27:05Z HTTP 200 (1082 PRs, sha256 2ce4bc55580abd6a1ad6820e4676232d0e2ce592f0a8a67176b451cdd15aa9b9); gh search prs "game-of-sloanes" HTTP 200 (3 hits: #847 merged d=5 n=49, #856 open (5,47) (6,40) (6,41) (4,11), #1114 open d=3 n=34; sha256 6b0a9e8752ae70199cfa4620a86a45240fd1fa97dd97f340630c026ee26cced5); TROPHY_CASE.md on main fetched 2026-11-18T00:27:26Z HTTP 200 sha256 83af764f5a6551a5a27bbb135324931659bda04e60b66a2c0e711b991b356113 (no Game of Sloanes entry); known-knowns/game-of-sloanes-complex-line-packings/ on main fetched 2026-11-18T00:32:09Z HTTP 200 sha256 6be91bc32f8be4eed1857f13eed1c45597443e29b5e4c6e0b7d4de8162a4b8cf (one folder, 2026-10-30-zerbytheboss-421cee37, cell 5x49 only).
- Literature: http://export.arxiv.org/api/query?search_query=all:%22complex%20line%20packing%22%20OR%20all:%22Game%20of%20Sloanes%22%20OR%20all:%22Grassmannian%20frames%22&sortBy=submittedDate&sortOrder=descending&max_results=15 fetched 2026-11-18T00:27:33Z HTTP 200 sha256 4034bb4fe3803721e7b0ea13df25fe806f70ec7a69b74882c4d487986e3ffced; 15 results, newest 2510.08638 (unrelated); the only table-relevant entries are 1907.07848 (the Game of Sloanes paper itself, whose values the table already carries) and 2504.21084 (a genetic-algorithm frame search; its abstract states no per-cell coherence values). No result gives a value for any cell.

## Clauses checked
- Object below the live table value by at least 1e-8: PASS (0.33247138 - 0.33206832825399 = 4.0305e-4).
- Posted file reproduces the table value (layout check): PASS (recomputed 0.332471381102 vs 0.33247138).
- Object is not the posted file or a unitary/phase/permutation copy of it: PASS (coherence gap 4.031e-4; sorted-overlap fingerprints differ by up to 2.181e-02; frame-operator eigenvalues differ by up to 9.210e-02).
- Row not marked provably optimal: PASS.
- Object mu at or above the listed lower bound 0.32732684: PASS (margin 4.7415e-3).
- Object at least 1e-7 below every other open-PR packing for this cell: PASS (lowest other: PR 18 7x25_owhs.txt mu 0.33211991135920, gap 5.1583e-5; PR 18 gap 5.1583e-5).
- Object is none of the other open-PR packings (fingerprints): PASS (PR 18: overlap-fingerprint diff 3.503e-02, eigenvalue diff 3.507e-02).
- PR 20 file is the same data as the object: PASS (byte-identical, same sha256 5afa4d7ffef566ee89999ca24b1c10dcb1450cbc032c34c8b3b316e8255ddbf9).
- No pull request to gnikylime/GameofSloanes merged or closed since 2026-04-28: PASS (newest merge 2026-04-21, before the latest main commit of 2026-04-28T17:04:24Z).
- No prior V3R1T4S claim covers (7, 25): PASS (the three Game of Sloanes claims cover (5,49), (5,47)/(6,40)/(6,41)/(4,11) and (3,34); a title scan of all 1082 PRs for sloane/packing/coherence/C^/mu= found no other; TROPHY_CASE.md has no Game of Sloanes entry; known-knowns folder on main holds only 5x49).
- No newer literature value for (7, 25) in the shared arXiv search: PASS (see source line above).

## Decision
The object reaches mu = 0.33206832825399, 4.031e-4 below the live table value 0.33247138 (hlc) and below every packing in the other open pull requests; it is a distinct packing from the posted file by coherence and frame spectrum, and open PR 20 holds the same packing. Residual risk not checked: unpublished or non-GitHub results (other forks, preprints outside the single arXiv query, private submissions to the maintainers), and pull requests opened after the fetch times above.

pass: true
