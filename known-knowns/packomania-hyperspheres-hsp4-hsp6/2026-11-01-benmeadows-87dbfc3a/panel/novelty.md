# NOVELTY verdict: hsp4-N136

context: subagent (fresh context started by the packaging session's Agent tool; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-01T21:10Z

## Value computed here
- Object: claim/hsp4-136.txt, sha256 87dbfc3abb5d7b1ebf915eb0dc8fc981c328ea801cd3e1f0ba587e29a225a963 (matches CLAIM.md); 136 centres x 4 coords, '#' comment line ignored.
- r* (mpmath, 50 digits, from the file's decimal strings) = 0.22622027641762341826997812036415868264356258381056
  (half min distance 0.226220277697839050279634..., 1 - max norm 0.226220276417623418269978...; the container is binding).
- Live table row (evidence/hsp4_radius_live.txt): `136 0.226201706521`. r* - table = 1.85698966e-5.
- Evidence provenance: the files in evidence/ are the repository owner's live re-fetch of 2026-11-01T14:32Z (FETCHED.md), and I treat them as this panel's live re-fetch. I recomputed sha256 for all 8 listed files and every value matches FETCHED.md. No other web access was made.

## Clauses checked
- **1 Value:** r* - table = 1.857e-5 >= 1e-10. **PASS.**
- **2 Parser sanity:** I recomputed the posted evidence/posted/hsp4-136.txt the same way (50 digits): 0.226201706520486810792601. It differs from the header (0.226201706521) and from the table row by 5.13e-13, which is within 1e-11, so clauses 3 and 4 apply. **PASS.**
- **3 Non-isometry:** the sorted multisets of all 9180 pairwise distances differ by at most 1.119e-2 (> 1e-8). For information, the sorted centre norms differ by at most 0.261. **PASS.**
- **4 Polish floor:** I wrote my own sequential-LP polish (work/polish.py; HiGHS). It linearizes near-active pair and wall constraints (margin m0 + 6*delta), maximizes t under a box trust region delta on every coordinate, and accepts a step only if the exactly recomputed radius increases; otherwise it shrinks delta. It stops when delta < 1e-13 or after 20 consecutive iterations with no gain > 1e-15. Every final radius was recomputed at 50 digits from the polished coordinates. Each run started from the posted coordinates (header 0.226201706521).
  - d0=1e-2, shrink 0.5, m0 0.02: 0.2262017065469594612, gain +2.596e-11, 46 iterations, stop: 20 iterations without gain.
  - d0=1e-3, shrink 0.5, m0 0.02: 0.2262017065472210236, gain +2.622e-11, 39 iterations, stop: 20 iterations without gain.
  - d0=1e-4, shrink 0.5, m0 0.02: 0.2262017065472755342, gain +2.628e-11, 39 iterations, stop: 20 iterations without gain.
  - d0=1e-2, shrink 0.5, m0 0.05, regrow x2: 0.2262017065470591239, gain +2.606e-11, 51 iterations, stop: 20 iterations without gain.
  - d0=1e-3, shrink 0.3, m0 0.05, regrow x2: 0.2262017065462777288, gain +2.528e-11, 34 iterations, stop: trust region < 1e-13.
  - d0=1e-4, shrink 0.7, m0 0.01, regrow x1.5: 0.2262017065473100758, gain +2.631e-11, 60 iterations, stop: 20 iterations without gain (the highest run).
  - d0=1e-2, shrink 0.8, m0 0.1, regrow x1.25: no step accepted, so it stays at the posted value; 20 iterations, stop: 20 iterations without gain (weak schedule, reported for completeness).
  - Highest polished radius: 0.22620170654731008. r* minus that = 1.857e-5 >= 1e-9. The posted basin tops out about 2.6e-11 above its header. **PASS.**
- **5 Not a relaxed copy:** The claim says it came from search lane hsp4-a, which never had the posted coordinates. Its starts were random configurations, lattice and shell seeds, and the lane's own neighbouring-N packings, and it names no posted packing as a start. I did not get the claimant's search code. My own evidence:
  - Contacts at tolerance 1e-7: the claim has 405 ball-ball + 120 wall = 525 contacts and 3 rattlers. The posted file has 407 + 119 = 526 contacts and 3 rattlers.
  - The degree histograms differ (claim [3,0,0,0,1,21,27,33,36,10,5]; posted [3,0,0,0,1,19,33,33,24,17,6]).
  - Shell profile: the claim has 13 inner centres and 123 outer. The posted file has 13 inner, 1 at norm 0.51 and 122 outer.
  - The distance-multiset difference is 1.1e-2.
  - An O(4)+permutation alignment (ICP with Hungarian matching, 400 random starts including reflections) found a best RMS displacement of 0.122 and a median of 0.074. Every centre moved by more than 1e-3 and 135 of 136 moved by more than 1e-2, so the claim is no small perturbation of the posted packing.
  - Every polish of the posted file stalls about 1.9e-5 below r*.
  - Nothing indicates that the claim derives from a posted packing. **PASS.**
- **6 History of updates:** evidence/hsp4.html shows "Last update: 06-Jul-2025". Its history has three entries: 04-Jul-2025 (N=2–100), 05-Jul-2025 (extension to N=200) and 06-Jul-2025 (extension to N=300), all by Specht. No entry is newer than the 06-Jul-2025 table snapshot, and none names N=136 after it. **PASS.**
- **7 Queue rule:** evidence/pending.html, dated 30-Oct-2026, lists only these categories: csc, ccq, crt, csq, chx, cpt, crc, cxd, cci and ssp. The only other entries are the Moki & Julio bundles of 24-Sep (crt, ccq, crc) and the 26-Sep '*many*' bundle. No range is listed for hsp4, so N=136 lies in no hsp4 range. The csc "136 candidates" entry is a count in another category. The HTML comment block concerns csqv only. **PASS.** Caveat (required): the 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle is category-unspecified and cannot be resolved. N=136 must be re-checked against the live hsp4 table once that bundle disappears from the pending list.
- **8 Moki & Julio MANIFEST:** the row `hsp4,136,0.226201706521,0.2262019190148776245179929,9.394000e-07,UNCLEAR (alignment),dp` gives published_radius 0.226201706521 and new_radius 0.22620191901487762. r* - new_radius = 1.8357e-5 >= 1e-10. That is the only hsp4 row for N=136. The other N=136 rows belong to other shelves (ccq, crc_*, cxd, hsp5, hsp6, scu), and no other row carries a radius near 0.2262. **PASS.**
- **9 Other prior work:**
  - Claims lists: hsp4 claims exist for N = 30, 35, 42, 48, 54, 62, 63, 64, 66, 67, 69, 74, 75, 79, 80, 81, 83, 88, 89, 91, 94, 104, 111, 119, 170 and 301 (open, merged or closed). None is for N=136, and the spherical-codes claims list has no hsp4 N=136 entry.
  - TROPHY_CASE.md has no hsp4 or 136 entry.
  - Bank-page construction, using spherical_plain_live.txt: (4,136) c=0.838381205119 gives s/(2+s) = 0.221347498140. (4,135) c=0.837973296726 with a centre ball gives min(1/3, ·) = 0.221564800326. Both are below r*, by 4.87e-3 and 4.66e-3.
  - **PASS.**

## Decision
All nine clauses pass on numbers computed here. The claim's r* = 0.226220276417623 beats the live table (0.226201706521) by 1.857e-5. It also beats the strongest prior work found, the Moki & Julio MANIFEST value 0.226201919015, by 1.836e-5, and the spherical-code constructions by about 4.7e-3. It is not isometric to the posted packing and is not a near-relabelling or small relaxation of it. My polishes of the posted file reach only +2.63e-11 over its header. The prior-work clauses are clean: there is no hsp4 history entry after 06-Jul-2025, no hsp4 range on the 30-Oct-2026 pending list, and no hsp4 N=136 claim or trophy. This holds subject to the required caveat: the category-unspecified 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle cannot be resolved, so N=136 must be re-checked against the live table once that bundle leaves the pending list. No injection was suspected in claim/ or evidence/.

pass: true
