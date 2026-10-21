# NOVELTY panel report

context: subagent (fresh context; saw only the claim package and the kit docs; did not read the author's working notes)

claim checked: a rank-38 scheme for <3,4,4> with 124 reduced additions (ternary, over Z), against Perminov's 125.
Scope of search: <3,4,4> and every permutation (3x4x4, 4x3x4, 4x4x3), rank 38, any addition count <= 124, any source.

Fetches (one plain request each, User-Agent naming V3R1T4S, no retries, all HTTP 200; UTC fetch times 2026-10-16T17:45Z to 17:46Z):

1. Perminov FastMatrixMultiplication, repository tree (GitHub API, master, recursive, not truncated, 6637 paths).
   Files for this format, any permutation: schemes/results/addition_reduced_ZT/3x4x4_m38_cr125_cn224_ZT_reduced.json
   (header "complexity": {"naive": 224, "reduced": 125}) and 3x4x4_m38_cr133_cn194_ZT_reduced.json.
   No 4x3x4 or 4x4x3 file in any folder. Other 3x4x4 files are Z-ring starting points
   (known/alpha_tensor, serendipitous_base), not reduced programs. status.json lists complexity 401 and 531 for
   the Z variants. Latest commit seen: 2026-10-13T14:54:59Z. Minimum known: 125. 124 < 125.
2. fmm_sota.json (sedoglavic/fmm_digest, master): {"format": [3,4,4], "rank": 38}. Rank only, no operation count.
   Rank 38 equals the claim's rank, so no new rank is claimed (consistent with the package).
3. Lille page https://fmm.univ-lille.fr/3x4x4.html: <3x4x4:38>, taken from Smirnov 2013. It lists encodings
   and no addition count.
4. matmulcatalog generated/COVERAGE.md: <3,4,4> r=38, "+216" adds (naive nonzero-based count, a different
   measure). Its repository tree has 3x4x4, 4x3x4 and 4x4x3 r38 files; I fetched the four that carry
   a count. The derived 4x3x4 r38 file has additions 200 and the derived 4x4x3 r38 file has 204. The Lille-derived file is named
   a192 (192). The perminov_cr133_cn194 file is the naive 194 variant. All are far above 124.
   Not comparable to a reduced SLP, but none is at or below 124 on any measure.
5. V3R1T4S pull requests, open plus closed via the GitHub API (235 PRs scanned, 6 pages each state).
   Title and body search for 3x4x4, 4x4x3, 4x3x4, <3,4,4>: no PR claims this format. The only mention is
   #173 (<6,8,8> rank 266, merged), which cites 3x4x4:38 as a Kronecker factor in the Lille entry. Open PR #222 is
   <4,5,5>. Repository search "3x4x4" returns only #173. TROPHY_CASE.md has no <3,4,4> row.
6. Literature (web search, last 24 months): Perminov arXiv:2512.13365, 2512.21980, 2511.20317, 2603.02398,
   2606.02480; the 3x3 rank-23 addition papers (2607.28676, 2609.06588); matmulcatalog theory notes.
   None reports a reduced addition count for <3,4,4> or its permutations at rank 38, and 2606.02480 states that
   no systematic additive-complexity study across formats exists. IACR ePrint 2026/849 (Mårtensson and Stankovski
   Wagner) lists a 344-38 scheme whose PDF is behind a challenge page (and their repository includes a Moosbauer
   <3,4,4>:38 scheme); the comparison stands against Perminov, Lille and COVERAGE.md. Search results are not
   exhaustive; this is a best-effort search, not a proof of absence.

Verdict: no known <3,4,4> rank-38 scheme (any permutation) with 124 or fewer additions was found in any
source. The best live reduced value is 125 (Perminov), so 124 strictly beats it by 1. This is not a tie.

Caveats (do not widen the claim):
- The margin is 1 addition.
- The comparison is only against the "reduced additions" measure used in Perminov's ZT files. Counts after a
  basis change, or over other rings, are a different quantity.
- This skeptic did not re-verify the object itself; that is the REPRODUCE role.
- Upstream tables move; the 125 value is as of 2026-10-16T17:45Z. Re-fetch immediately before submitting.

novelty: PASS
pass: true
