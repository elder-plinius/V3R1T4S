# NOVELTY panel: OEIS A054961 a(16) >= 102 (claim_a054961_16_102)
context: independent fresh-context NOVELTY panelist (a knowledgeWork subagent with no prior conversation); did its own fetches and searches
reviewed: 2026-10-22T19:29:40Z
verdict: PASS. 102 strictly beats every value found (best known a(16) >= 91 in OEIS A054961 and in O'Dwyer's wolfy-out.txt; no larger n=16 value in literature from the last 24 months, in TROPHY_CASE.md, or in any open or past V3R1T4S PR). Margin +11. Not a tie.

## Object identity (read only)
- A054961_n16_m102.txt sha256 de9e6522f190dbddc1bf2db69e8e1dcf9cb8995e8adc7f5b9a61093b95ffe381 (matches CLAIM.md).
- Quick sanity read: 102 distinct lines, all length 16; 5151 of 5151 pairwise ORs distinct. (Validity is the other panelists' job; this is only so novelty is judged on a real 102.)

## Fetch records (one plain GET each, honest User-Agent naming V3R1T4S, no retries)
1. https://oeis.org/A054961?fmt=text
   - time (date -u just before the GET): 2026-10-22T19:27:54Z; HTTP 200; no challenge page (the server returned the normal HTML entry).
   - sha256 of the saved scratch copy: 9d570470cfa48f3e99ed1fdcf31e6a5f881a377a0271a946cbf2149f3b3ecb43
   - page footer: "Last modified October 22 15:23 EDT 2026."
   - DATA: 1, 2, 3, 4, 5, 6, 8, 10, 13, 17 (stops at a(9)).
   - quoted bound: "a(13) to a(27) are >= 55,63,72,91,112,145,182,230,281,359,447,566,685,891,1065. - Zhao Hui Du, Apr 19 2018" -> a(16) >= 91. (The older Mar 30 2018 comment gives 90.) The only later comment, Sarosh Adenwalla, May 25 2024, is the general bound 1.134^n <= a(n) <= ceiling(2^((n+1/2))), which is about 363 at n=16; no contradiction with 102. No a(16) value above 91 anywhere on the page.
2. https://raw.githubusercontent.com/Quuxplusone/wolves-and-sheep/master/wolfy-out.txt
   - time: 2026-10-22T19:27:56Z; HTTP 200
   - sha256: f445d27a7c366cc683b26434112bc1ced76f09695623b2c1f8ea8681f9b0e508 (the same as the claim's 2026-10-19 scout copy, so the file is unchanged)
   - D=2 rows near the cell: "N=91 D=2 T=16 guaranteed_best=0", then "N=113 D=2 T=17 guaranteed_best=0". No D=2 entry with N >= 92 at T=16. Full D=2 (N,T) list: 8/6, 10/7, 11/8, 12/8, 13/8, 17/9, 22/10, 31/11, 46/12, 55/13, 63/14, 72/15, 91/16, 113/17, 145/18, 182/19, 230/20, 281/21, 359/22, 449/23, 571/24, 696/25, 893/26, 1090/27.
3. Extra single GET (context only): https://emathgroup.github.io/blog/two-poisoned-wine/ at about 2026-10-22T19:28Z (the exact date -u line went to a truncated log), HTTP 200, sha256 1780819d0bf89662ccece37391a1e455adae22c9b8a74e88a7575e8100b2e0bc. The blog text lists small n only (n=6..14, e.g. "n=14,至少47坛" and "12人46瓶"). It gives no n=16 value above 91. The emath data file poisonall.txt (row 16: [91]) was not re-fetched. The claim's scout copy is 3 days old.

## Searches run (last 24 months emphasised) and findings
- Web: "2-separable binary matrix 16 rows maximum columns union-free family". Found O'Dwyer's blog (A361928 triangle, n <= 20 columns only), arXiv:1410.1826 (asymptotic) and an SDSU REU note (small cases). Nothing at n=16 above 91. One search-engine "synthesis" claimed an n=16 maximum of 63 by misreading the T(n,d) triangle. It is not a source and was ignored.
- Web: "A054961 OEIS bitwise OR distinct binary vectors a(16)". Found the OEIS entry, its history (latest revision #89, Nov 14 2024, the Adenwalla bound) and A286874 (2-disjunct, a different sequence). No new n=16 bound.
- Web: "arXiv 2025 2026 non-adaptive group testing two defectives ... small parameters". Found Goshkoder-Polyanskii-Vorobyev arXiv:2401.16540 (asymptotic rates), arXiv:2601.09362 (inclusive disjunct, asymptotic), arXiv:2608.11858 (Bshouty, randomized lower bounds) and Redundancy 2021 fast union-free decoding. None has a small-length table with m >= 102 at length 16.
- Web: "union-free / 2-separable code small length table ... 2024 2025 2026". Found Fernandez et al., "GPU generation of binary 2-separating codes", J. Supercomputing, Feb 2026 (read in full). It is about Sagalovich 2-separating codes, a different notion, and its lengths are large (up to 116). Its search algorithm is in github GTAC-ITEAM-UPV/separating-codes. The paper has no union-free (A054961-type) result at length 16.
- Web: "github 2-separable matrix search A054961 n=16 n=17". No relevant repository with n=16 data.
- Web: "two poisoned bottles 16 mice ... 91 OR 102" and the Chinese query "毒酒 两瓶 老鼠 16 只". Found MSE 639, MO 59939, MSE 102958, emath blog, reddit. None states a 16-test, 2-poison family above 91. One engine "synthesis" asserted "16 mice ... 102 bottles". No cited source contained it, and it echoes the query terms, so it is not evidence of prior art.
- Web: "cancellative family / union-free family maximum size n=16 explicit construction 2025". Found Fox et al., 2-cancellative hypergraphs (CPC), arXiv:1511.00170 (weak union-free, A u B != C, a different notion) and EJC v5 (asymptotic). Nothing at n=16 for this notion.
- Repository: TROPHY_CASE.md (local copy, last commit 2026-10-15; remote copy read through the GitHub API, sha256 b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1). Grep for A054961 / group-testing / separab / union / poison found no matches. No group-testing entry exists there.
- Repository PRs: `gh pr list -R elder-plinius/V3R1T4S --state open --limit 100` returned 100 rows (#516 to #620), none about A054961 or group-testing-separable-designs. A wider read-only scan (limit 400 open, 300 rows returned) also found none. A search over all states for A054961 or group-testing-separable-designs found only #314 (a(14) >= 65) and #315 (a(15) >= 79), both MERGED 2026-10-17 and both about other n. No PR at n=16 at any value.
- This workspace's own earlier 92 (run 2026-10-19-1345) is unpanelled, never submitted, and superseded by this claim. It does not block novelty.

## Residual risks
- Du-Hwang's book tables and unarchived emath forum pages (thread 1511 beyond the archived page 18) were not read. A private or unpublished n=16 value >= 102 cannot be excluded. The poisonall.txt [91] value comes from the claim's 3-day-old scout copy, not a new fetch.
- Web search indexes are incomplete, and some engine "synthesis" text was wrong in both directions. Only primary pages were relied on.
- The jump 91 -> 102 (+11) is large for a 2018-era search frontier. That is plausible here because the published families are weight-5/6 and the claim's family is almost all weight 4, but it raises the bar for the validity panelists. It does not affect novelty.
- The OEIS page changed today (footer 15:23 EDT) but still shows 91 for a(16). If someone edits it before submission, a re-read is needed.
- Reading B (the stricter "at most 2" definition, with singletons counted) fails for this family. Under the OEIS literal definition (reading A), the claim is novel. Novelty is judged only under reading A, the same convention as the published 91-families.
pass: true
