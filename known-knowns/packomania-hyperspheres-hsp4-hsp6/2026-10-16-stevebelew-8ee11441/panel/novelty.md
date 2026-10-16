# Novelty verdict: hsp4, N = 94

context: subagent (Claude Code Agent tool, fresh context for this one claim)

Claim under review (CLAIM.md): 94 equal balls in the unit 4-ball with feasible radius r* = 0.245941019536845 (hsp4-94-candidate.txt), vs Packomania's posted hsp4 value 0.245932827006 for N = 94. Float re-computation from hsp4-94-candidate.txt in this review: r_feas = 0.24594101953684522, gain over the live table = 8.19e-06 (well above the 1e-10 criterion). The 50-digit certification is the numeric skeptic's job; this file judges only whether the result is new and strictly beats everything known.

## Fetches (each URL requested exactly once, plain curl, User-Agent "V3R1T4S skeptic", no retries)

1. https://packomania.com/hsp4/txt/radius.txt
   - time (date -u): 2026-10-16T17:55:11Z, HTTP 200, 5575 bytes
   - row 94 quoted verbatim: `94 0.245932827006`
   - byte-identical to the claim's snapshot hsp4_radius_as_fetched.txt (cmp: identical; md5 deb4cbcd0a0131989fbf6d1adf1e85f9 for both). The live value is still the snapshot value.

2. https://packomania.com/hsp4/hsp4.html
   - time: 2026-10-16T17:55:12Z, HTTP 200, 88618 bytes
   - quoted: `Last update: 06-Jul-2025`
   - History of updates contains only three entries: 04-Jul-2025 (first presentation N=2-100), 05-Jul-2025 (extension to N=200), 06-Jul-2025 (extension to N=300). No entry newer than 06-Jul-2025; no entry singles out N=94. The table row for N=94 on the page shows 0.245932827006, matching radius.txt.

3. https://packomania.com/pending-requests.html
   - time: 2026-10-16T17:55:13Z, HTTP 200, 4954 bytes; page dated 08-Oct-2026
   - Categories listed: csc, ccq, crt, csq, chx, cpt, crc, cxd, csqv, and one "*many*". No hsp4 (or hsp5/hsp6) entry exists, so no hsp4 range includes 94.
   - QUEUE CAVEAT (unresolvable): entry `26-Sep-2026 01:11  Moki & Julio  *many*  4666 candidates total` is category-unspecified. It cannot be ruled in or out as covering hsp4 N=94. Per the bank rule, N=94 must be re-checked against the live table once that bundle disappears from the pending list.

4. https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md
   - time: 2026-10-16T17:55:14Z, HTTP 200, 30936 bytes
   - grep for hsp4, hsp5, hsp6, hypersph, packomania, and standalone "94": zero hits. The file lists six result families plus two cipher commitments; none is a hypersphere packing.

5. https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100
   - time: 2026-10-16T17:55:15Z, HTTP 200, 53 open PRs
   - Scan of title + body + head branch for hsp4/hsp5/hsp6/hypersphere/packomania-hyperspheres/standalone 94: no open PR targets packomania-hyperspheres-hsp4-hsp6, and none claims N=94 in any 4-ball category. Packomania PRs present are for other targets (scu spheres-in-cube N=882-886, cci N=4141, two scu posted-coordinate complaints). PR 231 is spherical-codes-cohn-table (6,526), a different target; PR 224 mentions "94" only as an addition count in a matrix-multiplication program.

   Repo tree (https://api.github.com/repos/elder-plinius/V3R1T4S/git/trees/main?recursive=1, time 2026-10-16T17:55:16Z, HTTP 200, truncated=false): the merged family known-knowns/packomania-hyperspheres-hsp4-hsp6/ holds candidate objects for d=4, N = 30, 35, 42, 48, 54, 62, 63, 64, 66, 69, 74, 75. No hsp4-94 object exists anywhere in the tree. The only other hsp4 path is the bank entry under known-unknowns/packings-physics/.

## Literature search (web, 2024-2026)

Three searches: "packing 94 equal balls in a 4-dimensional ball best known radius 0.2459"; "hyperspheres packed in a 4-dimensional hypersphere improved packings Packomania hsp4 2025 2026"; "hsp4 packomania OR 4-ball packing 94 balls radius new record 2026". Results: only Packomania's own pages (last update 06-Jul-2025), a 2012 paper on packing congruent hyperspheres into a hypersphere (covers n = 2..24 only), general D4-lattice background, and unrelated hyperbolic-space packing results. No 2024-2026 source lists a packing of 94 equal balls in a 4-ball with radius at or above 0.245941019536845, and none lists any value above the posted 0.245932827006.

## Conclusion

- Live table value for N=94 is unchanged (0.245932827006); the candidate strictly beats it by 8.19e-06, far more than 1e-10.
- No History-of-updates entry on hsp4.html is newer than 06-Jul-2025, so none covers (4,94) after the scout's fetch.
- No hsp4 queue range on pending-requests.html includes 94 (there is no hsp4 queue entry at all), subject to the unresolvable "Moki & Julio *many* 4666 candidates" caveat above.
- Nothing in TROPHY_CASE.md, the merged hsp4-hsp6 family (N = 30..75 only), the 53 open PRs, or the literature matches or beats the candidate. The result is not a tie.

pass: true
