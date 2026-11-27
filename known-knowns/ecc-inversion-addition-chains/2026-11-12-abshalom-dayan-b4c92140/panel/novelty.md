# Novelty skeptic report: addition chain of length 281 for the secp256k1 scalar inversion exponent

context: subagent (fresh context, own copy of claim/)
date of review: 2026-11-12 (all times UTC)
claim reviewed: claim/CLAIM.md, object claim/object/chain.txt (sha256 b4c92140602faf399a6aad09073210f46b902351a6b7db3bfa1c848e06d4ce9b, matches CLAIM.md)

## Verdict in brief

- Status source read: yes (HTTP 200). Its value for this cell is still 290.
- Lowest public length found for this exact exponent (n - 2, n the secp256k1 group order): 282, Brian Smith 2026, published on Neill Clift's page. Nothing of length 281 or less, and no announcement of one, was found anywhere I looked.
- Our object replays as a valid chain of length 281 (251 doublings, 30 additions) ending at n - 2. 281 < 282: strictly better, not a tie.
- The claim names its seed (Smith's 282 chain, with URL). Our chain is not a trivial edit of it: 109 of our 282 values are absent from the published chain, and exhaustive, exact chain-level edits of the published chain (delete one element; delete two and insert one; delete three and insert two) do not reach 281.
- Remaining uncertainty is listed in the last section. None of it is a known value at or below 281.

novelty: CONFIRMED against everything public that I could read

## 1. Status and table fetches (one plain GET each, User-Agent v3r1t4s-run/1.0, no cookies, no retries)

| what | URL | UTC time | HTTP | sha256 | value for this cell |
|---|---|---|---|---|---|
| status source (Brian Smith's page) | https://briansmith.org/ecc-inversion-addition-chains-01 | 2026-11-12T18:52:32Z | 200 | 7b688992bf9bcea9a25f2e11369828037ad94d17315b08e2e749d2aabe1c9ca3 | "Total length: 290 = 253 doubles + 37 adds" (secp256k1 scalar inversion); last dated note on the page is September 3rd, 2017 |
| addchain results | https://raw.githubusercontent.com/mmcloughlin/addchain/master/doc/results.md | 2026-11-12T18:52:32Z | 200 | c805367ced12810d221ac3513ca3ccd0d329382dac2a8ec7b54f2f272e167357 | Length 293, Best Known 290, N-d = fffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd036413f |
| Clift, "Short Addition Chains for Cryptographic Exponents" | https://additionchains.com/LargeChains.html | 2026-11-12T18:52:32Z | 200 | 55d0846dd1d95abaa647e37cca1d5abc2dd9dd7bb1b5bb6a764b0fcc22cad345 | row "secp256k1 scalar inversion 282 ... 251 + 31 ... Brian Smith (2026)"; server Last-Modified Fri, 06 Nov 2026 16:52:16 GMT |
| the chain file that page links | https://additionchains.com/secp256k1-scalar-inverse-example.txt | 2026-11-12T18:52:33Z | 200 | ff57a8519d4fdc4ee5c154390d30ca83824c14cdfddb1907b9f736c30a050ccf | 283 lines of integers; replayed by me: valid chain, length 282, ends at n - 2; Last-Modified Mon, 02 Nov 2026 19:26:13 GMT |
| Clift's home page | https://additionchains.com/ | 2026-11-12T18:52:34Z | 200 | 01779f23339f8d0526d30ae70a2c391a6b2f8209d1719a9125b90c6356fd0c5d | no value for this cell; links to the page above; Last-Modified Thu, 29 Oct 2026 19:49:32 GMT |

The first four hashes equal the hashes in claim/table/RECORD.md and claim/table/FETCHES.txt, and the four fetched files are byte-identical to the copies in claim/table/. The bars have not moved since the claim was written.

Two further pages reached from those, one GET each:

| what | URL | UTC time | HTTP | sha256 | finding |
|---|---|---|---|---|---|
| Smith's page linked from Clift's home page | https://www.briansmith.org/addition-chain-intro-01 | 2026-11-12T18:52:59Z | 200 | 6bf8720830d198fa271f2260760f3ee750edd202f77d02b811cdfc2bcf9d2ddf | his 2017 introduction; no new values |
| Smith's site index | https://briansmith.org/ | 2026-11-12T18:52:59Z | 200 | 715b0f11cfa0585851dce117da88bc6afd6d6241d0e68b9a68e86543720aa755 | newest article listed is from September 2023; the addition-chain articles are the three from May 2017 |

### What Clift's pages say about shorter secp256k1 scalar chains

- LargeChains.html, section "Scalar Inversions": Brian Smith supplied the chains on 1 November 2026; "They are the best known to this page"; 1,013 supplied chains were checked with exact integers; only one example per curve can be downloaded, and that example "has the lowest weighted cost among the supplied chains of the shortest supplied length for that curve". So 282 is the shortest length in Smith's whole supplied collection for secp256k1, not just the length of the one file.
- The page says none of the lengths is proved optimal and that exact search cannot settle chains with 27 small steps. The recorded lower bound for this cell is 9 small steps, far below 27. It announces no shorter secp256k1 scalar chain and no work in progress on one.
- The page's own earlier dictionary-method results are named only for P-256 (286) and P-384 (431); it gives no Clift result for the secp256k1 scalar.
- The home page says Smith wrote to Clift that someone had generated better chains for P-384 and P-256; secp256k1 is not mentioned there.

Text addressed to reviewers: none found on the status and table pages above (checked the visible text, HTML comments and hidden-style blocks; the two display:none rules on Smith's page are typesetting classes for his code listings). Elsewhere: the upstream target file known-unknowns/algorithms/ecc-inversion-addition-chains.md ends with the kit's usual block telling an agent how to start a hunt; and the TTaoGaming repository contains files whose names indicate a reviewer guide and agent skills, which I did not open. Nothing of this kind was acted on.

## 2. Search for a chain of length 281 or less, last 24 months

GitHub reads were sent one at a time, listing endpoints first. Every read listed here returned HTTP 200. Hashes are of the saved extracts where one was saved; live JSON listings that were only read are marked "not saved".

### Upstream repository elder-plinius/V3R1T4S

| what | URL | UTC time | HTTP | sha256 | finding |
|---|---|---|---|---|---|
| head of main | https://api.github.com/repos/elder-plinius/V3R1T4S/commits/main | 2026-11-12T18:53:14Z | 200 | not saved | fb5164403fc71afeadc3d6d0dd0db44131665a8f, committed 2026-11-09T19:54:43Z |
| full tree of main (6,142 files, not truncated) | https://api.github.com/repos/elder-plinius/V3R1T4S/git/trees/main?recursive=1 | 2026-11-12T18:53:14Z | 200 | a8f18247c81cc51c948e637ba4f44d4d11f5365b9b7fe0a75e13340e7ed9b318 (path list) | known-knowns/ has no addition-chain family; the only matching path is the target file under known-unknowns/algorithms/ |
| TROPHY_CASE.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-11-12T18:53:28Z | 200 | 83af764f5a6551a5a27bbb135324931659bda04e60b66a2c0e711b991b356113 | no line mentions addition chains, secp256k1, scalar or inversion |
| target file | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/known-unknowns/algorithms/ecc-inversion-addition-chains.md | 2026-11-12T18:53:29Z (about) | 200 | 29e9926e6721ea1804637731235b5f58890f9b3fc557a452c2ecefbd6da5523d | bar for this cell 290 on 2026-10-25; the criterion text in claim/CLAIM.md is verbatim |
| all pull requests, open and closed (1,018; 11 pages) | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=1..11 | 2026-11-12T18:53:40Z to 18:54:05Z | 200 | 7f63b6f6f9174afa65954a83ce85a6a8962deffa5e4e00703cbcd447d0e56993 (extract) | titles, branch names and bodies searched |
| all issues and pull requests with full bodies (1,061; 11 pages) | https://api.github.com/repos/elder-plinius/V3R1T4S/issues?state=all&per_page=100&page=1..11 | 2026-11-12T18:54:53Z to 18:55:14Z | 200 | 5fe760270cf741a08998035949bbf7431c18d7fe913b17c50d32d981a61cc0bf (extract) | two items mention addition chains, secp256k1 or ecc-inversion: #664 and #833 |
| pull request #833 and its file list | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls/833 and .../pulls/833/files | 2026-11-12T18:54:18Z, 18:54:26Z | 200 | 6a844cf41c9bc1084adb1a12d90d148cd7757b7bec41b5c16932624684cdbfa2 (extract) | open, unmerged, no comments; head a60aac0cb414035342c4114d1c0ba0032dc9f2ab |
| its chains file | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/a60aac0cb414035342c4114d1c0ba0032dc9f2ab/known-knowns/ecc-inversion-addition-chains/2026-10-29-zerbytheboss-395a524b/object/certified_chains.json | 2026-11-12T18:54:36Z | 200 | bfe66828a6bf1fe559ec55dd0b8298a806f1ac0840347fc5e32deb8753789bd0 | entry "secp256k1 Scalar": total_length 293 (253 + 40), published_bar 290 |

- #664 (closed) is the pull request that proposed the target. #833 (open, by another contributor) claims Curve25519 scalar 282, P-384 scalar 432, M-383 395 and M-511 524. Its chains file carries a secp256k1 scalar chain of length 293, the addchain baseline. So the upstream repository holds no value below 290 for this cell, merged or unmerged.
- Small correction to claim/table/COMPARATORS.md: its row for the upstream repository says "no entry or value for this cell". The unmerged pull request #833 does contain a value for this cell (293). It is not a bar and changes nothing.

### Repositories of the people involved

| what | URL | UTC time | HTTP | sha256 | finding |
|---|---|---|---|---|---|
| TTaoGaming/addition-chain-search: repository, branches, releases, tags, pull requests, issues | https://api.github.com/repos/TTaoGaming/addition-chain-search and /branches, /releases, /tags, /pulls?state=all, /issues?state=all | 2026-11-12T18:55:21Z | 200 | not saved | last push 2026-10-26; 4 branches; no releases, no tags, so no release assets; 2 open pull requests (#1, #3), 1 further issue (#2) |
| trees of all 4 branch heads | https://api.github.com/repos/TTaoGaming/addition-chain-search/git/trees/{88948a79…, 0273e624…, 11c45534…, 82d3a920…}?recursive=1 | 2026-11-12T18:55:36Z to 18:55:42Z | 200 | ecc934238aaaca8de88364938b0e520dfea67fa8b8f3dc40d5f8857c23e42691, fb041a925c6a3ec416453ad4c0890cf9db9124313c2a0eeb7498e314d77e129c, ea61918d1e98c5ad2e46dac5a7268a93165c00cb2598fe016cdb37052022e78d, 29482d222060fa1fe09f6349ca7e16e72aef5eb60312793858638bfce1129b3f (path lists) | secp256k1 files: chains/targets/secp256k1/candidate.json, its manifest, review-candidates/certificates/secp256k1_288.json, and in the branch of pull request #3 one witness named secp256k1_288.json.gz |
| that branch's frontier summary | https://raw.githubusercontent.com/TTaoGaming/addition-chain-search/0273e62487dffa13e17a214966bd24f11e92b2a3/research/2026-10-26-brian/report-support/RETAINED_FRONTIER.json | 2026-11-12T18:56:04Z | 200 | 642f3f5a846f561069679ef32ade3b3340358adc8d12ee2b4b50aed952f9e043 | secp256k1: 4 files, "minimum_retained_operations": 288, split 253 + 35 |
| candidate.json for secp256k1 | https://raw.githubusercontent.com/TTaoGaming/addition-chain-search/0273e62487dffa13e17a214966bd24f11e92b2a3/chains/targets/secp256k1/candidate.json | 2026-11-12T19:10:08Z | 200 | 904518c4f165a168f0412164a23babe91b66d70820a0fad76686e5a84bf77e5a | 290 rows (a 290-step chain) |
| Brian Smith's repositories, by last push | https://api.github.com/users/briansmith/repos?per_page=100&sort=pushed | 2026-11-12T18:56:40Z | 200 | not saved | recent: ring (pushed 2026-11-07) and a fork of curve25519-dalek (created 2026-11-11); no repository with a chain collection |
| ring: commits since 2026-09-01, branches, issues and pull requests updated since 2026-08-01 | https://api.github.com/repos/briansmith/ring/commits, /branches, /issues | 2026-11-12T18:56:52Z | 200 | not saved | scalar-inversion clean-ups for P-256 and P-384 on 2026-11-06; ring has no secp256k1 |
| gists of Smith, Clift and TTaoGaming | https://api.github.com/users/{briansmith,NeillClift,TTaoGaming}/gists | 2026-11-12T18:57:03Z | 200 | not saved | nothing about addition chains |
| everything Smith, Clift and TTaoGaming opened recently on GitHub | https://api.github.com/search/issues with author:briansmith created:>2026-09-01; author:NeillClift created:>2025-11-01; author:TTaoGaming created:>2026-08-01 | 2026-11-12T19:10:32Z to 19:10:40Z | 200 | not saved | Smith: curve25519-dalek pull request #930 (2026-11-11, Curve25519 scalar chain 284 to 275) and four ring items; Clift: addchain issue #156 only; TTaoGaming: nothing on secp256k1 beyond the above |
| Clift's repositories | https://api.github.com/users/NeillClift/repos | 2026-11-12T18:56:40Z | 200 | not saved | no chain data for this exponent |

### addchain and libraries

| what | URL | UTC time | HTTP | sha256 | finding |
|---|---|---|---|---|---|
| addchain issues and pull requests updated since 2024-11-01, releases, last commits | https://api.github.com/repos/mmcloughlin/addchain/issues?state=all&since=2024-11-01T00:00:00Z, /releases, /commits | 2026-11-12T18:56:21Z | 200 | not saved | last commit 2024-06-30, last release v0.4.0 (2021); issue #156 (Clift, 2026-10-22) lists field-inversion lengths only (secp256k1 field 268); issue #154 is a tool failure report |
| RustCrypto k256 scalar arithmetic: history since 2024-11-01 and current file | https://api.github.com/repos/RustCrypto/elliptic-curves/commits?path=k256/src/arithmetic/scalar.rs and https://raw.githubusercontent.com/RustCrypto/elliptic-curves/master/k256/src/arithmetic/scalar.rs | 2026-11-12T18:57:16Z, 18:57:18Z | 200 | 53c9681a882a44492bbfecd449c03098e2feb150c9a889cdff94e64ed17b1937 (file) | since commit c971eaa95a (2026-01-05) inversion goes through a big-integer routine, so master has no fixed chain; released versions use Smith's 290 chain |

libsecp256k1 was not re-read today. According to Smith's page and claim/table/COMPARATORS.md its last addition chain for this exponent was the 290 one (253 + 37) before it switched to safegcd, which is not an addition chain.

### GitHub search

| query | URL | UTC time | HTTP | sha256 | finding |
|---|---|---|---|---|---|
| code, low limb of n - 2 | https://api.github.com/search/code?q=bfd25e8cd036413f | 2026-11-12T18:57:25Z | 200 | b8d521104a048da1d567d3460b5732ca911726df619894a21a60a0ff3d5a14b0 (first 100 hits) | 1,322 hits; I read the repository list of the first 100 and opened none beyond those already covered. This search cannot show a chain's length by itself |
| repositories, "addition chain" pushed after 2025-11-01 | https://api.github.com/search/repositories?q="addition chain" pushed:>2025-11-01 | 2026-11-12T18:57:45Z | 200 | fcc9e42cfb619ba97f946839d5fd36999d098a0810d88fdd59c3b6c37036be9c | 17 repositories |
| repositories, "addition chains" pushed after 2025-11-01 | same with "addition chains" | 2026-11-12T18:57:50Z | 200 | 534787bd535795885cd8a59971cc180e62b1202d64ed8895fe5517312d4190f7 | 16 repositories, the same set less one |
| issues and pull requests, "addition chain" secp256k1 scalar, updated after 2024-11-01 | https://api.github.com/search/issues | 2026-11-12T18:58:28Z | 200 | not saved | 217 hits, first 50 titles read |
| issues and pull requests, "addition chain" "scalar inversion", updated after 2024-11-01 | https://api.github.com/search/issues | 2026-11-12T18:58:33Z | 200 | not saved | 129 hits, first 50 titles read |

Of the repositories found, the ones that could bear on this cell were opened: SETPOINT1/short-addition-chains (tree and README at 2e12390b, 18:58:03Z and 18:58:21Z: general exponentiation benchmarks, no cryptographic exponents), SETPOINT1/superfast-addition-chains (licence and a one-line README only), Allanodora/ECC-inversion-benchmarking-harness (README at 2bd2030c, 18:58:20Z: secp256k1 field inversion only). The others are about optimal chains for small numbers, the Scholz-Brauer conjecture, tools, or other curves. The issue searches returned library performance work, a cryptanalysis challenge (one submission read, unrelated) and the items already listed; no title announces a secp256k1 scalar inversion chain.

### Literature and general web

Eight web searches on 2026-11-12, all between about 18:59Z and 19:09Z (a general search engine; individual times, HTTP status and hashes are not exposed by the search tool): secp256k1 scalar inversion chain lengths 280 to 282; Smith and Clift 2026; arXiv and IACR ePrint 2025 to 2026; the title and file name of Clift's page; Smith's 2026 chain lengths; forum and blog posts on n - 2 chains shorter than 290; TTaoGaming's secp256k1 lengths; machine-search results on scalar inversion chains.

- No paper, post or page gives a chain of length 281 or less for this exponent, or announces one.
- IACR ePrint 2026/2102 (https://eprint.iacr.org/2026/2102, abstract page read once through a page-reading tool at about 19:00Z; status and hash not exposed): a small-range discrete-logarithm solver; no addition chain for n - 2 in the abstract. The PDF was not read.
- Judged from the search result summaries and titles only, not opened: arXiv 2606.02235 and the "ECDSA.Fail" preprint (quantum circuits for point addition, not addition chains for inversion); arXiv 2609.28374 (distribution of minimal chain lengths, theoretical).
- The searches surfaced Smith's curve25519-dalek pull request #930 (Curve25519, 275) and his 2017 page; nothing for secp256k1 beyond 290 there. The search engine did not index Clift's LargeChains page, so the 282 is confirmed only by the direct fetch above.

### Neighbouring cells

The other scalar cells on Clift's page are different exponents (P-256 281, Curve25519 275, P-384 419, P-521 568); a chain for one is not a chain for another, and there is no relabelling or symmetry that maps one exponent to another. The equal number 281 for P-256 is a coincidence of a different cell, not a tie. The secp256k1 field cell (268 on Clift's page) is likewise a different exponent.

### Summary of public values for this exponent

| length | source |
|---|---|
| 293 | addchain results.md; the chains file of upstream pull request #833 |
| 290 | Smith's 2017 page (status source); TTaoGaming chains/targets/secp256k1/candidate.json; older libraries |
| 288 | TTaoGaming review-candidates/certificates/secp256k1_288.json (replayed from claim/table/tt_secp256k1_288.json: valid, 253 + 35) |
| 282 | Brian Smith 2026 on Clift's page (replayed: valid, 251 + 31); the shortest length in his supplied collection according to that page |
| 281 | this claim |

## 3. The seed question

Does the claim name its seed? Yes. claim/CLAIM.md, section "Composition and seed statement", says the chain is seeded from Brian Smith's 282 chain, gives the URL of the file, and says the search started from that chain's dictionary (its 27 values below 2^21). The claim line itself says the same. It also states that the chain is not a composition.

### How the two chains differ (my own replay of both files)

- Ours, claim/object/chain.txt: 281 steps, 251 doublings and 30 additions, strictly increasing, ends at n - 2.
- Published, claim/table/secp256k1-scalar-inverse-example.txt: 282 steps, 251 doublings and 31 additions, ends at n - 2. Every element of it has exactly one representation as a sum of two earlier elements.
- Values in common: 173. Only in ours: 109. Only in the published chain: 110.
- Small values (below 2^21, the "dictionary"): ours has 30, the published chain 27, 24 in common. Ours lacks 139552, 419427, 1398106 and adds 289, 70033, 559236, 699062, 1258297, 1817533. This is exactly what the claim states. The two sequences first differ at position 10 (ours 289, published 513).
- Top of the chain: identical. Both build 2^21 - 1, then runs of 42, 84 and 126 ones by the same three additions, and share every value from 22 up to 146 bits.
- Middle, between the last shared 146-bit value and the first shared 238-bit value: completely different. Ours adds, in order, 699062, 2^21 - 1, 289, 699062, 1817533, 69776, 1817533, 289, 2309, 1817533, 699061, 70033 (12 additions); the published chain adds 699061, 2^21 - 1, 1398106, 2^21 - 1, 2^21 - 1, 139809, 257, 257, 257, 699061, 419427, 2309, 699045, 1, 4361, 699045 (16 additions). No value in this stretch is shared (103 main-line values of ours against 107 of theirs).
- Tail: the last 21 elements (238 bits up to n - 2, with additions of 2309 and 2^21 - 1) are identical.
- Count: ours spends 3 more steps on the dictionary (29 against 26) and 4 fewer on the main line (252 against 256).

So ours keeps the published chain's top ladder, most of its dictionary and its last 21 elements, and replaces the whole middle of the main line together with part of the dictionary. That is not a deletion, a relabelling or a polish of one or two steps: 109 values change, and the two dictionaries are at least six single edits apart.

### What trivial edits of the published chain give

Chain-level edits, exhaustive and exact, computed by me on the published file:

- Delete one element: no element can be deleted (0 of 281 candidates leave a valid chain).
- Delete two elements and insert at most one new value (a one-step polish plus a deletion): 39,340 pairs, every admissible inserted value tried (3,733,313 candidates): no valid chain of length 281 or 280.
- Delete three elements and insert at most two new values (a two-step polish plus a deletion): all 3,658,620 triples, every admissible pair of inserted values: no valid chain of length 281, 280 or 279. Before this run the search routine was compared with brute force on 160 random small chains; it found exactly the same set of solvable deletions (several thousand).

Dictionary-level edits with the main line re-optimised after each edit (the claim's own baseline, claim/baseline/):

- I rebuilt claim/baseline/acw_big.c and reran claim/baseline/trivial_edits.py on claim/baseline/seed_dictionary.txt with the stated arguments (beam 2048). Output identical to claim/baseline/one_edit.txt apart from the file name in its first line: 663 dictionaries, histogram 282:11 283:183 284:150 285:3 308:1 309:37 310:229 311:49. Nothing below 282. (The first line of claim/baseline/one_edit.txt names smith2/init2.txt; the shipped file with the same content is claim/baseline/seed_dictionary.txt. Cosmetic.)
- Sanity of the evaluator: with the same beam it scores the seed dictionary 282, the published length, and our final dictionary 281. So it can see a 281 when one is there. With the narrower beam of the search (256) it scores the seed 284, as claim/rebuild/search.log shows.
- My extension: a second edit applied to each of the 10 one-edit neighbours that score 282. 6,946 further distinct dictionaries, histogram 282:26 283:3328 284:265 285:6 308:7 309:210 310:2349 311:755. Nothing below 282. Several of the 282s lie on the way to our dictionary (for example replacing 139552 by 70033 and then inserting 289, 699062 or 1817533), which shows the search crossed a plateau of equal-length dictionaries before reaching 281.

Is the claim's baseline an adequate measure of "what those edits alone give"? For the purpose of the rule, yes, with stated limits. It is a generous reading of a trivial edit: one change to the dictionary followed by a full re-optimisation of the main line, which already moves many chain elements. Together with the exact chain-level checks above it shows that deletion and one- or two-step polishing of the published chain stay at 282. What it does not cover:

- It scores with a beam search, a heuristic. A one-edit dictionary could in principle admit a 281 main line that the beam misses. The beam does recover 282 for the seed and 281 for ours, and the chain-level checks above are exact, but this is evidence, not proof.
- Only one edit deep in the claim; two edits only along the 282 plateau in my extension. The 183 neighbours at 283 were not expanded a second time.
- Inserted values are restricted to sums of two dictionary values below 2^22. Values built otherwise (for example from main-line elements) are not tried.
- The model is "dictionary, fixed top ladder, then a main line of doublings and additions of dictionary values". Chains outside this model are not in the baseline. The chain-level checks partly cover this, up to the edit sizes stated.
- The other chains of length 282 in Smith's supplied collection are not public, so only the one downloadable example could serve as the seed and as the comparison object.

Composition: the claim says the chain is not a composition, and I agree: its middle section and six of its dictionary values occur in no published chain I have. As for a composition of published chains forming a lower bar than 282: the TTaoGaming 288 chain shares 7 values with the 282 chain (1, 2, 2^126 - 1 and its next three doublings, n - 2) and 11 with ours. Below 2^126 - 1 the two published chains build runs of ones by different ladders (TTaoGaming through 2^6 - 1 and 2^14 - 1, Smith through 2^21 - 1), and the union does allow mixed ladders; but Smith's ladder already reaches 126 ones from 21 ones with three additions, the minimum for a factor of six, and any other ladder needs run values that Smith's dictionary does not contain. Above that point the main lines share nothing until n - 2. I see no splice that gives less than 282, but I did not prove it by exhaustive search (see section 4).

## 4. What I could not check

- Smith's full supplied collection (1,013 chains over five curves) is not public. Clift's page says the downloadable example has the shortest supplied length, so I rely on that sentence for "nothing shorter than 282 in the collection".
- Anything Smith, Clift or others found after 2 November 2026 and have not published. Private mail, mailing lists, chat servers and social media were not searched.
- GitHub code search: 1,322 files contain the low limb of n - 2. I read the repository names of the first 100 hits only and did not replay chains from them. Code search covers default branches only.
- The roughly 120 witness files in the branch of TTaoGaming pull request #3 were not downloaded or replayed; I relied on that branch's own frontier summary (minimum 288 for secp256k1) and on the file names, one of which is a secp256k1 file (length 288).
- libsecp256k1, BoringSSL, Go, fiat-crypto, NSS, mbedTLS, AWS-LC and other libraries were not re-read today. The claim's comparator table reports them at 290, 293 or without a fixed chain; I verified only k256 (no fixed chain on master) and the upstream and TTaoGaming values.
- Literature search was by a general web search engine, not by the arXiv or ePrint search forms; it did not index Clift's page, so it can miss recent pages of that kind.
- Optimality is not claimed and not checked. The lower bound recorded on Clift's page is far below 281.
- The search run of claim/rebuild/ (about an hour) was not repeated; I checked the object and the baseline, not how the object was found.
- Chain-level edits larger than "delete three, insert two" were not enumerated.
- Best composition of published chains: I tried to compute the shortest valid chain inside the union of the published 282, 288 and 290 chains exactly (branch and bound); it did not finish, so that point rests on the structural argument in section 3, not on an exhaustive computation.

## 5. Verdict

The status source was read and still shows 290. The best published length for this exponent is 282, re-fetched today with unchanged hashes, and the page that publishes it says it is the shortest of the supplied collection. No chain or announcement at 281 or below was found in the upstream repository (tree, trophy case, 1,018 pull requests, 43 issues), in the repositories and recent activity of Smith, Clift and TTaoGaming, in addchain's tracker, in GitHub searches or on the web. The object is a valid chain of length 281. It names its seed, differs from it in 109 values, and deletion or one- and two-step edits of the seed do not give 281 (exact at chain level; beam-scored at dictionary level). 281 strictly beats 282.

pass: true
