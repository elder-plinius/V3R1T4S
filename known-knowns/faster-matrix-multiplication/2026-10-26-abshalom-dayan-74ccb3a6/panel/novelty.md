# NOVELTY skeptic: <14,15,15> rank 1836 over Q

context: subagent (Claude Opus 5.5, fresh context, saw only claim/)

Verdict: the claim passes on novelty. The lowest rank public anywhere for (14,15,15) is 1842, the merged entry in this repository; the lowest in the four tables is 1848. 1836 beats both by 6 and 12. The only earlier public mention of rank 1836 for this format is open draft pull request #752, filed by the same contributor. That mention describes this same object: the library code is byte-identical and the parameters are identical. So it does not make the claim non-novel. It sets the credit date to 2026-10-25T11:18:58Z (see section 4).

## 1. The four criterion sources, fetched live once each

Each source got one plain GET with curl and the User-Agent "V3R1T4S-novelty-skeptic (curl)", with no cookies and no retries. Times are UTC from `date -u`. Values are copied from the command output.

| fetched (UTC) | HTTP | URL | sha256 of body | value for sorted (14,15,15) |
|---|---|---|---|---|
| 2026-10-26T22:13:04Z | 200 | https://fmm.univ-lille.fr/ (status_source) | 57e936b6aa0efe3a2e4020e14a84f5533983f66d5befd16fbb08bd448bd906a9 | catalogue row `⟨14×15×15:1848⟩`, rank 1848, credited "Perminov 2026 [GitHub repository]" (the only value; no row for 15×14×15 or 15×15×14). Last-Modified: Tue, 20 Oct 2026 08:14:45 GMT |
| 2026-10-26T22:13:05Z | 200 | https://fmm.univ-lille.fr/14x15x15.html | 72bedfe2f8cb81f8a2b7ca2daa73561f04f2de1961c52e15dad8bf7c2fe8d465 | "Description of fast matrix multiplication algorithm: ⟨14×15×15:1890⟩". Last-Modified: Wed, 10 Jun 2026 10:43:30 GMT; this page lags the index |
| 2026-10-26T22:13:05Z | 200 | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae | `{"format": [14, 15, 15], "rank": 1848, "exponent": 2.801382}`; createdAt 2026-10-19T20:46:33 |
| 2026-10-26T22:13:05Z | 200 | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/ranks.md | e71786dda6669d49fb1af448046cd294d7246977ba5372eeab5f536bf58dcbe4 | `` | `14x15x15` |    1894     | 1892 (1894)  | 1848 (1894)  | **2.801382482** | `` under Format / `ZT` rank / `Z` rank / `Q` rank: the minimum is 1848 |
| 2026-10-26T22:13:06Z | 200 | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | 2423783b98fe1d364d40244cb29eae5fb089d47914525b1d91cc832fdccad582 | newest section is 26/10/2026 (addition reductions only); the latest 14x15x15 rank entry is `14x15x15_m1848_Q.json` (section 26/09/2026). Nothing below 1848 |
| 2026-10-26T22:13:06Z | 200 | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 52db72a9cd408815d98ebcd851d55fb13b8d84eaa70b7ebd7c4de67cc29b9e61 | no 14x15x15, 15x14x15 or 15x15x14 line |
| 2026-10-26T22:13:06Z | 200 | https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/main?recursive=1 | f25a290fcb035c0a0b1df06f5baccbd99653698ed38b1abcc49807da335e8c37 | 39 paths, truncated False; no scheme for 14x15x15 or any permutation |

The minimum over the four named sources is **1848** (fmm_sota.json, the Lille index and Perminov Q). The per-format Lille page reads 1890, and MerlijnW70 has no entry. **1836 < 1848**, a margin of 12. The bodies are byte-identical (same sha256) to the scout's fetches in TABLE_RECORD.md, so nothing changed between 22:01Z and 22:13Z.

## 2. This repository

| fetched (UTC) | HTTP | URL | sha256 | finding |
|---|---|---|---|---|
| 2026-10-26T22:13:07Z | 200 | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1 | entry 44: "<14,15,15> rank 1842 over Q (supersedes our 1843 of 2026-10-10)" |
| 2026-10-26T22:14:12Z | 200 | https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/faster-matrix-multiplication/schemes | 7e5af9664db41286cde5d0d3b642bafb1a8f906db03697b4481c2625cb420513 | 14x15x15_r1842_Q.json, 14x15x15_r1843_Q.json (plus other formats) |
| 2026-10-26T22:14:18Z | 200 | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/known-knowns/faster-matrix-multiplication/INDEX.csv | 8e5b2a6c3c2b6a18dd3c2489f742b73890b9c81bb9d051f0628bab25101e83b7 | 14x15x15 rows: 1842 (record), 1843 (superseded) |
| 2026-10-26T22:14:23Z | 200 | https://api.github.com/repos/elder-plinius/V3R1T4S/git/trees/main?recursive=1 | 8fcb2e37ea36c064c605a0842a52b11cda1c67e6d05ecc39faec58a2d24a089f | 5630 paths, not truncated. The only paths naming the format are the two schemes above |
| 2026-10-26T22:14:36Z to 22:14:47Z | 40 × 200 | every FMM-family INDEX.csv on main (40 files) | n/a | contributed catalogue rows cover 13x15x15, 13x14x14, 15x15x16, 13x13x15, 14x16x16, 11x13x16, 13x13x14, 15x16x16 and 13x14x15; **none for 14x15x15** |
| 2026-10-26T22:16:32Z to 22:20:32Z | 840 × 200 | all text files (.md/.txt/.py/.json/.csv, under 200 kB, excluding object/ and schemes/) of the 39 merged contributed FMM folders | n/a | every 14x15x15 intermediate in the merged rebuild chains is rank 1843 or 1842 (REBUILD.md "Slice 1: 14x15x15, rank 1842"). None is below 1842 |

The merged repository minimum for (14,15,15) is **1842**. 1836 is 6 below it.

### Pull requests, all states

These counts come from the GitHub search API, one GET each, spaced to respect the rate limit. Every request returned 200 with `incomplete_results` false:

| fetched (UTC) | query term | sha256 | total_count | PR numbers |
|---|---|---|---|---|
| 2026-10-26T22:15:00Z | 14x15x15 | ccbb8c66cc8725a5bf9d9064e102599227f871811e314491d5fc92704aff9ca1 | 10 | 2, 130, 164, 166, 177, 197, 356, 402, 432, 615 |
| 2026-10-26T22:15:08Z | 15x15x14 | 840185ac69ff01c964c2bfead7f7b8a5a7764c3814155124f82ebe285189a90f | 0 | none |
| 2026-10-26T22:15:15Z | 15x14x15 | 840185ac69ff01c964c2bfead7f7b8a5a7764c3814155124f82ebe285189a90f | 0 | none |
| 2026-10-26T22:15:23Z | "14,15,15" | 39501d448712aab87aa20afd07f9d36eb239c295e48f10f5a5bb6b20afad8189 | 1 | 752 |
| 2026-10-26T22:15:31Z | "(14, 15, 15)" | a8ebf3772f3516f98610d9f34d151d0f39e24c4d37c077ad7fd918e3508919ef | 22 | tokenised matches (2, 130, 353, 379 to 392, 432, 710, 721, 726, 729, 752, 767) |
| 2026-10-26T22:15:39Z | 1836 | 39501d448712aab87aa20afd07f9d36eb239c295e48f10f5a5bb6b20afad8189 | 1 | 752 |
| 2026-10-26T22:15:46Z | fmm-catalogue-small-format-rank | 20475ecd0ff8c55e2c39a4d9f562dc7466253e4f7416f931f856bd0ea02815a7 | 47 | 2 to 7, 39 to 51, 130, 164, 166, 168, 172, 175, 177 to 179, 197, 399, 402, 432, 708, 714, 740 to 752 |
| 2026-10-26T22:15:54Z | "14 15 15" | 5ae175c1fbc0ec076d940a9ef9c97e965da82aabc8fdad424c9133064ce647bc | 24 | as for "(14, 15, 15)" plus 14, 15 |
| 2026-10-26T22:16:02Z | <14,15,15> | 39501d448712aab87aa20afd07f9d36eb239c295e48f10f5a5bb6b20afad8189 | 1 | 752 |

Because search tokenises, I also listed **all 755 pull requests** through `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=1..9`, fetched 2026-10-26T22:15:45Z to 22:15:54Z, all HTTP 200, PR numbers 1 to 784. I scanned every title and body with a regex for 14/15/15 in all three orders, with separators x, ×, *, comma or "by". I also scanned for 1836 and for any number from 1800 to 1849 near the format. What I found:
- #432 (open) and #356 (closed): (14,15,15) at ZT 1894 and 1895. These are another target and above 1842.
- #615 (open): quotes 14x15x15:1894 only.
- #2, #130, #164, #166, #177, #197: merged or closed chains through the merged rank-1842 scheme.
- #752 (open, draft): the only PR anywhere that names a (14,15,15) rank of 1836 or less. See section 4.

No pull request holds a (14,15,15) scheme, or states a rank, below 1836. No other PR states 1836.

## 3. Literature, last 24 months

- The arXiv API (`https://export.arxiv.org/api/query?...abs:"matrix multiplication" AND (rank OR scheme OR schemes)`, sorted by date, 100 results), fetched 2026-10-26T22:15:12Z, returned HTTP 200 (sha256 c80386d1ba5e3c6ae15e6b3234538f795e536c6681e5e2635f74df67fdf99f14). The first try at the http:// URL, at 22:15:07Z, returned HTTP 301 to https with an empty body; I did not retry it, and the https URL is a different URL. A second query (`abs:"flip graph" OR abs:"trilinear aggregation" OR ti:"fast matrix multiplication"`, 60 results), fetched 2026-10-26T22:15:32Z, returned HTTP 200 (sha256 b318e10d43507b6ed09d0a0c8452e8f455d142bbfe0a131be70fd4ea601b02e3). Relevant hits:
  - arXiv:2606.02480 (Perminov, June 2026, meta flip graph and serendipitous product). Its formats up to 16 feed docs/ranks.md, which reads Q 1848.
  - arXiv:2603.02398 (Perminov, March 2026).
  - arXiv:2511.20317 (ternary meta flip graphs), arXiv:2511.10786 (structured matrix multiplication), arXiv:2510.19787 (meta flip graph) and arXiv:2508.01748 (trilinear aggregation).
  - arXiv:2610.26563v2 (Solomonik and Bläser, updated 2026-10-22). This covers direct sums of square products only, with no (14,15,15) rank.
  - arXiv:2610.13971 (border-rank claim for powers of 2, not an explicit (14,15,15) scheme).
  - arXiv:2606.13408 (matmulcatalog).

  None states a (14,15,15) rank below 1848.
- The LITA repository tree (`https://api.github.com/repos/khoruzhii/lita/git/trees/HEAD?recursive=1`), fetched 2026-10-26T22:15:31Z, returned HTTP 200 (sha256 d923a68888fc427aa8e9d216c6e54d45eb078afb8718ea55ae4990f443b89339). It holds only square schemes, 13^3 to 32^3, and no 14x15x15. Its `schemes/15x15x15_r1977.npz` has blob sha1 65821484d954b4aade06cbda624932ba2a481f7b, equal to `git hash-object` of claim/rebuild/15x15x15_r1977.npz (sha256 94515288f3079546e2c9f552bd246742ac45b2bc62b5aa908a9f491c44102a33).
- matmulcatalog COVERAGE.md (`https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md`), fetched 2026-10-26T22:15:31Z, returned HTTP 200 (sha256 c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7). Its row reads `` `⟨14,15,15⟩` | **✓ 1895** Dronperminov-Z [Z→F₂] | **✓ 1890** Dronperminov-Q ``, so its best is 1890.
- A general web search for "14x15x15" matrix multiplication returned only a stale snapshot of the Lille page (1905) and unrelated papers.

## 4. PR #752 and the rank-1836 intermediate: non-novel, or only a credit date?

Facts read live:
- `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls/752` (2026-10-26T22:13:07Z, HTTP 200, sha256 ab0df03b1de26dcc08864403cc41399159032a64df692ffb39e06d0ca200e945): state open, draft true, created 2026-10-25T11:18:58Z, not merged. The title is the <14,14,15> rank-1709 claim. TABLE_RECORD.md says it is by the same contributor as this claim. The body says: "HOW_WE_FOUND_IT.md and how-we-built-it/COMMANDS.md name the chain's intermediate <14,15,15> scheme of rank 1836. It is not claimed here and was not verified by the panel or the review."
- The file list (`.../pulls/752/files?per_page=100`, 2026-10-26T22:13:44Z, HTTP 200, sha256 3cf0d39ce3c65feaf7fcffc4633b335bb25d2298aa049c6f667687082829d5e6) has 47 files. **Its object/ files are the 1709 scheme only; PR #752 does not contain the bytes of this 1836 object.**
- Its how-we-built-it/COMMANDS.md (fetched 2026-10-26T22:13:58Z, HTTP 200, sha256 d65ae95f0a1770b8c7d26ea10cc46d0446ac9171a5d46a8f8f5cb63536b2c58c) documents step 1 of its chain as `0/1,1,1,1,1,1,1,-5,1,1,1,1,1,1,1/-1,1,1,1,1,1,1,1,1,1,1,1,1,1,1/5001/6` with the printed lines "-> (14, 15, 15) rank 1865" and "flat absorption (seed 5001, restarts 6) removed 29 -> rank 1836". These are the slice, direction pair (e, f), seed and restarts given in claim/REPRODUCE.md.
- Code identity, by git blob sha1:
  - PR #752's code/convert.py, engine.py, export_txt.py and flat.py have the same blob ids as claim/rebuild/convert.py, engine.py, export_txt.py and flat.py: abcd74ad..., 2fe8a437..., c4210530..., 79c84745....
  - claim/rebuild/rebuild_slice.py differs from PR #752's rebuild_chain.py, but makes the same calls: `restrict(S, 0, e, f)`, then `flat_all(S1, rng=random.Random(seed), restarts=6)`. With default `mode="rflat"` and `start=0` (signature in claim/rebuild/flat.py), the call is equivalent. Only the JSON note string differs, and export_txt.py does not write it.
  - So running PR #752's public code with step 1 alone, then export_txt.py, rebuilds this object. I established this by reading the code and parameters. I did not run it, because python-flint is not in my sandbox.

Policy as quoted in my brief:
- Credit goes to the first public filing, dated by the PR's creation time.
- An earlier PR here with byte-identical bytes sets the date to that earlier filing.
- A value public before the filing date at equal or better rank means the claim is not a record.

**Decision: the earlier mention only sets the credit date. It does not make the claim non-novel.**

Reasons:
1. "A value that was already public is not new" is a prior-art rule: someone, somewhere, already had this rank. The only public appearance of 1836 for (14,15,15) is this same object. It comes from the same contributor, through byte-identical code, from the same public parent, with the same parameters. It is not an equal value obtained separately. A result cannot tie with itself.
2. The policy's own rule for a duplicate filing (byte-identical bytes in an earlier PR here) moves the date back. It does not disqualify the claim. PR #752 did not ship the bytes, but it shipped the value, the exact recipe and the code that regenerates them. That is the same object in another form, so the same rule should apply.
3. Applying it gives a credit date of **2026-10-25T11:18:58Z** (PR #752 creation). At that time:
   - the tables stood at 1848 (fmm_sota.json createdAt 2026-10-19; the Lille index Last-Modified 2026-10-20; the Perminov changelog has no 14x15x15 entry after 26/09/2026);
   - this repository stood at 1842;
   - no pull request named a lower value.

   So 1836 strictly beat everything public at its credit date, and it still does.

Caveat for the gate and maintainers: a strictly literal reading has the filing date as this new PR's creation. Under it, "the value 1836 was public before the filing date" (in #752's body), so the claim would not be a record. The byte-identical clause does not literally apply, because #752 shipped a recipe, not bytes, and it disclaimed the claim. I reject that reading for the reasons above, but the filing should disclose #752 openly. It should cite #752 as the first public mention and accept 2026-10-25T11:18:58Z as the credit date, not hide it.

## 5. Summary

| comparator | value for (14,15,15) | 1836 vs it |
|---|---|---|
| fmm_sota.json | 1848 | -12 |
| Lille index (status_source) | 1848 | -12 |
| Lille 14x15x15.html | 1890 | -54 |
| Perminov ranks.md min(ZT 1894, Z 1892, Q 1848) | 1848 | -12 |
| MerlijnW70/fmm-schemes | none | n/a |
| this repository, merged (TROPHY_CASE #44) | 1842 | -6 |
| this repository, any PR other than #752 | lowest stated 1842 | -6 |
| PR #752 (same object, same contributor; sets the credit date) | 1836 (not an independent value) | same result |
| literature, last 24 months (arXiv, LITA, matmulcatalog) | nothing below 1848 | -12 or better |

No source blocked a request. No text addressed to reviewers was found in the claim files, pull-request bodies or fetched pages. The fetch log and the saved bodies are in the novelty skeptic's working folder, fetch/.

pass: true
