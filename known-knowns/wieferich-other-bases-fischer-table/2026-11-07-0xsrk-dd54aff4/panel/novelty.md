role: NOVELTY
context: hermes delegation (delegate_task subagent, fresh context, saw only claim/)
novelty: NEW as of 2026-11-07T12:18:47Z. The pair (b, p) = (24766, 1000747824697) is absent from both live Fischer tables (re-fetched once, HTTP 200, byte-identical to the scout's copies), from his six other Fermat-quotient files, from OEIS (no match; a positive control returns hits), from the 24-month arXiv, web and GitHub searches, and from the V3R1T4S repository (TROPHY_CASE, known-knowns/, 924 PRs, issue search, no releases). It is not a trivial derivation: 24766 = 2*7*29*61 is squarefree, and 24766 is the only base in 2..65536 with a^(p-1) == 1 (mod p^2) at this p.
injection_suspected: none (no fetched source tried to give instructions)

## Status fetches (one request each, no retries, User-Agent "V3R1T4S-panel/1.0 (open-research notebook; one honest request)")

UTC times come from `date -u` just before each curl; hashes from `sha256sum`.

| URL | UTC | HTTP | sha256 |
|---|---|---|---|
| http://www.fermatquotient.com/FermatQuotienten/FermQ_Sorg.txt | 2026-11-07T12:18:47Z | 200 | 35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4 |
| http://www.fermatquotient.com/FermatQuotienten/FermQ_Sort.txt | 2026-11-07T12:18:48Z | 200 | bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b |
| http://www.fermatquotient.com/ | 2026-11-07T12:18:48Z | 200 | 42508627832b9d654ea777db3c10126d558bf7bf13c21c07c5b74452b8e84fd1 |
| http://www.fermatquotient.com/FermatQuotienten/News.txt | 2026-11-07T12:20:28Z | 200 | 1970fbe5188e93b0fa0381beac91b0654b18c9491043bbdb42e256bc7f6080e7 |
| http://www.fermatquotient.com/FermatQuotienten/ErstBasen.txt | 2026-11-07T12:20:31Z | 200 | e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820 |
| http://www.fermatquotient.com/FermatQuotienten/ErstPBasen.txt | 2026-11-07T12:20:33Z | 200 | 3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362 |
| http://www.fermatquotient.com/FermatQuotienten/SwitchFermQ.txt | 2026-11-07T12:20:36Z | 200 | 8190a7ca0bf2a31d9b03b77e97e5d09f45abc8b7df6f4321d706732b329f3faa |
| http://www.fermatquotient.com/FermatQuotienten/FermatQ3.txt | 2026-11-07T12:20:38Z | 200 | 022855e8d16257ca4931bd9f7f9133012f17bbf1bc528f9a6cd12995b02a0a41 |
| http://www.fermatquotient.com/FermatQuotienten/Statistik.txt | 2026-11-07T12:20:40Z | 200 | dde1fa8d6c6105a74895dfb64646b7b74cb327a15aa7c49695f1c58ebabd2b2b |
| https://oeis.org/search?q=1000747824697&fmt=data | 2026-11-07T12:22:21Z | 200 | d29b6a9bcb1b53a991e6b7446d2cee5f1e702d4e1399efa4bb24e77e09b4e97b |
| https://oeis.org/search?q=24766+wieferich&fmt=data | 2026-11-07T12:22:25Z | 200 | adaa5ead47d313713edd639b291f84805713983a66760ff978df6d1dbee6a3ff |
| https://oeis.org/search?q=188748146801&fmt=data (positive control) | 2026-11-07T12:26:36Z | 200 | f1fc0135a31b259409ed4b6ac332dc09a730e4d08eca9703df90b38fde05860d |

The FermQ_Sorg.txt and FermQ_Sort.txt hashes are identical to the scout's record in status_sources.md and to claim/inputs/. Server headers: FermQ_Sorg.txt `Last-Modified: Wed, 21 Oct 2026 05:59:16 GMT`, `Content-Length: 288459`. FermQ_Sort.txt `Last-Modified: Wed, 21 Oct 2026 05:59:05 GMT`, `Content-Length: 33141`. The six extra Fischer files were each fetched once because a "first base" or record list could hold the pair even when the two base tables do not.

### Quoted value and limit lines (latin-1 decoded)

- FermQ_Sorg.txt: "Die gefundenen Primzahlen (P) der Fermatquotienten von der Basis 2 bis 10125". "Die Basen sind gegenwaertig durchsucht bis 4.8E+12". The last base row is "10125,  2, 7, 17093, 123151337", and the file is signed "21.10.2026  Richard Fischer".
- FermQ_Sort.txt: "Die gefundenen Primzahlen der Fermatquotienten von der Basis 2 bis 1052". "Die Basen, die einen maximalen Primteiler bis 149 haben, sind durchsucht bis 2.00E+14". "Die restlichen Basen sind gegenwaertig durchsucht bis 7.4E+13". The only base above 1052 is "65537  P: 2^16, 3, 131, 151, 163 (>1.2E+14)".
- Value: neither file has a row for base 24766. Base rows end at 10125 in FermQ_Sorg.txt and at 1052, plus 65537, in FermQ_Sort.txt. The string 1000747824697 occurs in neither file. A search that also allows digit-group separators (space, apostrophe, dot, comma) finds neither the prime nor 24766. Among the 572 numbers of 13 or more digits in FermQ_Sorg.txt, the nearest to p are 1000436194319 and 1002205496401.
- Fischer's other files contain neither the prime nor "1000747": News.txt (records), ErstBasen.txt (extreme first bases; its all-bases-below-p survey stops at "Durchsucht bis zur Primzahl 1120000031"), ErstPBasen.txt, SwitchFermQ.txt, FermatQ3.txt and Statistik.txt. In ErstBasen.txt "24766" appears only inside the unrelated number 149247661, and nowhere as a standalone token.
- OEIS, q=1000747824697: "Sorry, but the terms do not match anything in the table." q=24766 wieferich: the same "Sorry, but the terms do not match anything in the table." Control q=188748146801: "Displaying 1-10 of 10 results found", including A123692, so the search engine was working.

## V3R1T4S repository (main HEAD 6bb0dcfd1623abe2f827b90059d01a007eb310f0, committed 2026-11-06T20:24:57Z)

| URL | UTC | HTTP | sha256 |
|---|---|---|---|
| https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-11-07T12:22:47Z | 200 | 83af764f5a6551a5a27bbb135324931659bda04e60b66a2c0e711b991b356113 |
| https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns?ref=main | 2026-11-07T12:22:49Z | 200 | 735c1b56905b74c72b61f70afb4da79fb2330a3b3c67b7c4c2e0757eaf0bb89d |
| https://api.github.com/repos/elder-plinius/V3R1T4S/git/trees/main?recursive=1 | 2026-11-07T12:22:51Z | 200 | ab3762505fcd8d9eb713be8a84b75e848b2889076ba305aee8f30cd5eae27880 |
| https://api.github.com/repos/elder-plinius/V3R1T4S/releases | 2026-11-07T12:22:55Z | 200 | 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945 |
| https://api.github.com/repos/elder-plinius/V3R1T4S/commits/main | 2026-11-07T12:22:57Z | 200 | d21eb7581dcb9878837866ddd6148c68617341fb56b9541fd6b94f5147d8b6e7 |
| https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/known-unknowns/number-hunts/wieferich-other-bases-fischer-table.md | 2026-11-07T12:24:27Z | 200 | 8395b2fe8a39df3816c850ea9279ab8931e3e3655b4b7ad69c7e437b8f520d52 |
| https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+wieferich&per_page=100 | 2026-11-07T12:26:40Z | 200 | c9938edecb99d754b2d039ac9eec320a94c769b6a6417921e2dcbef9e2fe01a0 |
| https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+1000747824697&per_page=100 | 2026-11-07T12:26:44Z | 200 | c9938edecb99d754b2d039ac9eec320a94c769b6a6417921e2dcbef9e2fe01a0 |

The PR list, `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=N`, was fetched one request per page, all HTTP 200:

| page | UTC | items | sha256 |
|---|---|---|---|
| 1 | 2026-11-07T12:22:53Z | 100 | 6c18040691d2c74cf4cd7de0e67d6e1c4bbafbd26f116c93a5cef612fe1ef791 |
| 2 | 2026-11-07T12:23:37Z | 100 | a0474d6b548c9e832543a0c64f238bc52bbf5f0fac904aca593fb16ed94b72fb |
| 3 | 2026-11-07T12:23:40Z | 100 | 8e2ea315cc60bd976dfe3730fb9b0158ed876a3ccb0d9554824f3cb7fe0a7fca |
| 4 | 2026-11-07T12:23:43Z | 100 | 67726b4679ce4c36c88c550cac4f49649449ffdb31756cf1f23d9d91cf063eb7 |
| 5 | 2026-11-07T12:23:47Z | 100 | 128673a6b098d20c2aaad401381f299dc7565a382e9467a800fdefc7c314aad6 |
| 6 | 2026-11-07T12:23:50Z | 100 | 3c0abdd65ca5205f3a8914b3bfd9c92b90fd854640c9d03cb2d354d84c381dd1 |
| 7 | 2026-11-07T12:23:53Z | 100 | 99df8b7901ad37cc6c7a24d06014e201056457285e67f8f4cfe9fc2372206333 |
| 8 | 2026-11-07T12:23:56Z | 100 | aa2611a913ac37d5d108254c9440813d36dc1684022d85d0219386a1d38afb04 |
| 9 | 2026-11-07T12:23:59Z | 100 | aaab4b5faafcebf34225e177590e51960ed3e3c5fabd3caa1cd6117d7662f4db |
| 10 | 2026-11-07T12:24:02Z | 24 | 733187f142694368657ec79306c16430254d0804521e2195b7aa9098a9cf6733 |

Findings:
- TROPHY_CASE.md has no occurrence of "ieferich", "Fermat", "Fischer", "24766" or the prime. Its families are degree-diameter graphs, constant-weight codes, matrix multiplication, the Lehmer bound, VNN-COMP, RobustBench and cipher commitments.
- known-knowns/ holds 29 directories, none of them Wieferich or Fermat-quotient related.
- The full tree has 7056 entries and is not truncated. The only paths matching wieferich|fermat|fischer|24766|the prime are the target cards known-unknowns/number-hunts/wieferich-other-bases-fischer-table.md and wieferich-base-2-beyond-2-64.md, plus two unrelated Fermat-number and Fermat-Catalan cards.
- The repository has 0 releases, so no release asset can be ahead of the tree.
- PRs: 924 objects (#1 to #972; 399 open, 348 closed unmerged, 177 merged). No title, body or head branch mentions Wieferich, Fermat quotient, 24766 or the prime. One false positive on "Fischer": #700, a rendezvous-search bank proposal citing a different author.
- The issue/PR search API returns total_count 0 for "wieferich" and total_count 0 for the prime.
- The target card on main carries the p1 text verbatim as in claim.md and reads "open as of 2026-10-30".

## Literature and code, last 24 months

- arXiv API, `http://export.arxiv.org/api/query?search_query=all:wieferich&sortBy=submittedDate&sortOrder=descending&max_results=60`, fetched 2026-11-07T12:25:47Z, HTTP 200, sha256 447c9e925929cffe0c5a19a6454fa98e06d3fdff7fc710cd11b665df5c996dc6. It reports 53 results, 18 of them published since 2024-11-01: 2610.28685, 2610.25248, 2610.17649, 2609.13904, 2609.03091, 2608.30389, 2609.00039, 2607.29329, 2607.15305, 2606.30232, 2605.20860, 2605.13460, 2602.17727, 2601.12753, 2512.08060, 2508.08472, 2503.19144 and 2412.11588. All are theoretical work (abc, monogenic polynomials, Drinfeld/Carlitz analogues, number fields, binomial congruences). None tabulates Wieferich pairs for bases above 10125, and none mentions this pair.
- Web search (one query each):
  - "1000747824697" returned 10 hits, all unrelated (parts inventories, finance pages), with no mathematical occurrence.
  - "24766" Wieferich prime base, "Fermat quotient" OR "Wieferich" "24766", Wieferich primes to bases above 10125 table search, Wieferich primes all bases up to 65536 Fermat quotient search, "Wieferich" "bases up to" 100000 OR 65536 OR "2^16", and Wieferich primes bases beyond 10125 new search extension Fischer 4.8E+12: no page mentions base 24766, and none gives a table for bases above 10125. The results were the Wikipedia Fermat-quotient table (small bases), lecture notes, MathWorld, Crandall-Dilcher-Pomerance and Dorais-Klyve (bases 2, 3, 5, 7).
  - arXiv 2025 Wieferich primes arbitrary bases computation new pairs: theoretical papers only.
  - github wieferich search bases fermat quotient GPU: https://github.com/OrygnsCode/wieferich-base-search searched 27 bases between 186 and 986 for p in (4.4e12, 1e14] and found no hits. Numerisect is a tool with no table. The WWocl and primepath searches are base 2 only.
  - mersenneforum Wieferich primes other bases search Fischer table new pairs: no thread covering bases above 10125.
  - Wieferich pairs dataset composite bases large p: Borwein-Mossinghoff, "Wieferich pairs and Barker sequences II". Its data covers prime pairs (q, p) with q < p, both == 1 mod 4. Composite bases such as 24766 are not covered, and none of its prime factors is a Wieferich base for this p (see below).
  - "fermatquotient.com" Wieferich new pair 2026: only Fischer's own index.
  - V3R1T4S wieferich-other-bases-fischer-table: repository pages and forks, no claim of this pair.
- Not run: GitHub code search (it needs a login). OEIS b-files are not indexed by OEIS search. However, base 24766 has no OEIS sequence, and the A039951(24766) entry would be 777979, not p (below).

## Derivation check (panel/work-novelty/derive_check.py and small_wief.py, Python stdlib, exact integers)

- p = 1000747824697 is prime by deterministic Miller-Rabin with bases 2..37, and pow(24766, p-1, p^2) = 1.
- 24766 = 2*7*29*61 is squarefree, so it is not a perfect power and the pair does not reduce to a smaller root base.
- Fermat quotients mod p: q_p(2) = 231556755366, q_p(7) = 206995164662, q_p(29) = 98138082196, q_p(61) = 464057822473. None is 0, and their sum is exactly p, so q_p(24766) == 0. The pair is "primitive": by additivity (q_p(ab) = q_p(a) + q_p(b)) it cannot follow from published pairs for its factors.
- Exhaustive scan of a = 2..65536 at this p: a^(p-1) == 1 (mod p^2) holds only for a = 24766.
  - No proper divisor of 24766 (2, 7, 14, 29, 58, 61, 122, 203, 406, 427, 854, 1769, 3538, 12383) and no other base up to 65536 shares p. So the pair is not a power, product or quotient of other pairs at the same p with bases up to 65536 (relabelling or propagation).
  - p appears for no base in Fischer's range. This agrees with p's absence from FermQ_Sorg.txt, which is searched to 4.8E+12 > p.
  - 24766 is the smallest base above 1 for this p.
- Base 24766's Wieferich primes below 3e7: only 777979. So p is not the base's first Wieferich prime, and "smallest Wieferich prime per base" lists such as A039951 would show 777979, not p.
- Nothing was seeded from a published object, and none of the trivial edits applies: deletion, restriction, propagation, relabelling, symmetry and polish have no meaning for a single (b, p) pair except through the power, product and quotient relations checked above.

## Verdict

As of the fetches above, the claimed pair beats everything known in its cell: the base 24766 row is empty everywhere checked, and the neighbouring cells (bases 10126..65536 and the published bases up to 10125 and 65537) have no pair at this p. It adds one new pair, so it is not a tie. Residual risk is limited to non-indexed private data and GitHub code search, which was not run.
pass: true