# Novelty review: A389690(23) = 3570

context: subagent (fresh context, Claude Science delegation)

Path key (added by the claimant on 2026-10-28 at the maintainer's request, PR #781 review): this review was run on the panel zip, whose layout differs from this package. Its code/A/ and code/B/ are how-we-built-it/A/ and how-we-built-it/B/ here (byte-identical). These panel inputs are not shipped: CLAIM.md and REPRODUCE.md (the claim summary and its commands; see README.md, RUN_IT_YOURSELF.md and how-we-built-it/BUILD.md), histogram_sg_23_A.txt, histogram_sg_23_B.txt and maximising_set.txt (objects/; object/A389690_23.txt holds the same maximising set and, as lines 10-682, the same 673 histogram lines, sha256 760aabce6a540d00660f1e4ab4a243b83a5d6e3640773d6497d67ea630bc00ac), the check helpers verify_oeis.py and sg_ref.py (code/check/), and a389690_2.txt (inputs/), the OEIS program https://oeis.org/A389690/a389690_2.txt (sha256 9fe51a4caa7f2d3f381c44fcb39b43c270c7bab12204e9cbf7e6e2c59999b61f). File references in the text were changed only to name these package paths, URLs or bare file names; no finding, number or verdict changed. Verbatim logs keep the zip's paths.

- role: NOVELTY skeptic (kit/RUN.md step 6)
- claim (CLAIM.md): A389690(23) = 3570, the longest eventual Sprague-Grundy period over all 2^22 sets S with max S = 23, attained only by S = {2, 3, 5, 7, 9, 10, 13, 14, 16, 18, 20, 21, 22, 23}
- target: subtraction-game-max-period-terms (bank/targets.json at main 8846324a8fe813bf89a9ef2a60eb9b13d0ba79fd)
- review window: 2026-10-26 07:15 to 07:30 UTC
- inputs: only the package (the panel zip) plus the network. The sha256 values of maximising_set.txt, histogram_sg_23_A.txt and histogram_sg_23_B.txt match the values listed in CLAIM.md.

**novelty: PENDING STATUS CHECK.** The primary status page could not be read. The kit says a block means fail, so this review cannot pass.

## 1. Primary status source (one plain request per page, no retries)

Client: Python 3.11 `urllib.request.urlopen` with its default User-Agent (`Python-urllib/3.11`). I sent one request per URL and did not retry.

| URL | time (UTC) | HTTP | body | sha256 of body |
|---|---|---|---|---|
| https://oeis.org/A389690 | 2026-10-26T07:15:44Z | 403 | `error code: 1010` (17 bytes) | 2938e9f1284180959e33ab1718d0793a72ff6e4cdb8108c34dcd14e69446de5c |
| https://oeis.org/A389690/b389690.txt | 2026-10-26T07:15:48Z | 403 | `error code: 1010` (17 bytes) | same |
| https://oeis.org/history?seq=A389690 | 2026-10-26T07:15:52Z | 403 | `error code: 1010` (17 bytes) | same |

- Value read: **none**. The body `error code: 1010` matches the CDN response (Cloudflare error 1010) that refuses a request because of its client signature. The sandbox proxy let the connection through, so the remote side blocked the request; the sandbox did not.
- Under the kit rule I did not send the request again with curl or any other client. I also did not use mirrors, caches or search-engine snippets as a stand-in. Criterion (3) of the target ("the term is not yet in the OEIS entry, its b-file or its history at verification time") is therefore **not verified by this review**.
- The OEIS search pages could not be checked for the same reason. I made no further requests to oeis.org, so I did not check for another entry (for example a duplicate) that might already carry a term for n = 23.

The following is context only. None of it replaces a status read at verification time:

- CLAIM.md records the claimant's own fetch at 2026-10-26T07:08:28Z (HTTP 200). It lists n = 1..22 ending 1178, 1180, 4464, keyword nonn,more, latest revision #36 of Oct 26 2025.
- bank/targets.json at 8846324 has `status_checked: 2026-10-25` and lists A389690 n = 1..22.
- The maintainer's comment on PR #699 (2026-10-25T19:31:25Z, read through the GitHub API at 2026-10-26T07:29:18Z) says: "OEIS A389689 (n = 1..23) and A389690 (n = 1..22) show exactly the terms you list".
- The plain-language explainer linked from PR #699 notes that its preparers also received HTTP 403 from the OEIS pages.

## 2. Repository: TROPHY_CASE.md and pull requests (GitHub REST API, unauthenticated)

- main = 8846324a8fe813bf89a9ef2a60eb9b13d0ba79fd (commit date 2026-10-25T19:26:25Z), the same commit the claim cites.
- TROPHY_CASE.md at that commit (blob 571f24117c6b128ffe751a39f22fcab68c498e66, fetched 2026-10-26T07:16:56Z, 100 lines). Case-insensitive search for A389690, A389689, subtraction, Sprague, Grundy, 3570, 4464 and OEIS: **0 hits**. The file covers six other result families and two cipher commitments, none about subtraction games or OEIS terms.
- Open PRs: all **329** listed (4 pages, 2026-10-26T07:17:16Z to 07:17:21Z). I scanned titles and bodies for a389690, a389689, subtraction, sprague, grundy, 3570, max-period, subtraction-game and oeis. **No open PR claims A389690(23) or touches this target.** The keyword hits were unrelated. "oeis" matched claims on other targets. "subtraction" matched #465, a matrix-multiplication PR that counts additions and subtractions. "3570" matched #200, a card-guessing PR, as a digit string inside a fraction.
- Closed PRs: the 100 most recently updated (updated 2026-10-24T16:10:54Z to 2026-10-26T02:10:19Z). The only related one is **#699**, the bank proposal for this target, opened 2026-10-24, closed unmerged 2026-10-25T19:31:26Z. It claims no value and names n = 23 as the next unknown A389690 term.
- GitHub issue/PR search, which covers all states and searches titles, bodies and comments (2026-10-26T07:17:45Z to 07:18:10Z):
  - `repo:elder-plinius/V3R1T4S A389690`: 1 result (#699).
  - `repo:elder-plinius/V3R1T4S subtraction game`: 1 result (#699).
  - `A389690` across all of GitHub: 2 results, #699 and one unrelated dependency-bump PR in another repository.
  - `A389689` across all of GitHub: 1 result (#699).
- Not done: GitHub code search, which needs authentication. I did not use a token.

## 3. Literature, last 24 months (2024-10-26 to 2026-10-26)

- **arXiv API** (2026-10-26T07:18:53Z to 07:19:18Z). I ran six queries sorted by submission date: `all:"subtraction game"`, `all:"subtraction games"`, `abs:"subtraction" AND abs:"Grundy"`, `abs:"nim-sequence" AND abs:"period"`, `abs:"Sprague-Grundy" AND abs:"periodic"` and `abs:"subtraction set"`. They returned 15 distinct papers published since 2024-10-26:
  - 2610.25829, 2610.06925, 2609.30302, 2609.05358, 2609.00871
  - 2608.17654, 2607.27989, 2606.29015, 2605.14321, 2604.16759
  - 2603.10414, 2601.18715, 2512.24221, 2510.24280, 2507.20087

  No abstract reports the maximum period over all move sets with a given max S.
- **Full-text keyword search** (PDFs from arxiv.org, 2026-10-26T07:19:48Z to 07:21:07Z, text extracted with pypdf). I searched the text of the eight most relevant papers by pattern and read the passages that matched. I did not read the papers in full. The eight papers:
  - 2601.18715 (additive sink subtraction; listed in the target's primary_sources)
  - 2603.10414 (additive subtraction games)
  - 2609.05358 (purely periodic three-move games)
  - 2608.17654 (infinite subtraction sets)
  - 2610.25829 (two-move games with a pass)
  - 2605.14321 (subtraction Nim with a pass)
  - 2405.20054 (survey; published in Games of No Chance 6, 2025, doi:10.1017/9781009565486.003)
  - 2307.12458 (published in TCS, Nov 2024, doi:10.1016/j.tcs.2024.114775)

  Pattern searches for `A3896xx`, `OEIS`, `3570`, `4464`, `longest/maximum/largest period`, `all subsets`, `exhaustive` and `Yao` found **no report of the maximum Sprague-Grundy period for max S = 23, and no occurrence of 3570**. The matches were unrelated: one "exhaustive" about a partition in 2609.05358, and one "longest periods" about 3-move sets in 2405.20054.
- **CrossRef** (2026-10-26T07:28:03Z to 07:28:12Z). Three queries ("subtraction games period", "subtraction game Sprague-Grundy periodicity", "nim-sequence period subtraction set"), filtered to from-pub-date 2024-10-26, top 60 by relevance each. Related in-window items:
  - SSRN 10.2139/ssrn.7434544, pure periodicity for three-move games {2, 5, c}, 2026
  - LNCS 10.1007/978-3-032-17801-5_28, Sprague-Grundy values of games with a pass, 2026
  - IJGT 10.1007/s00182-026-00991-5, m-pile divisor Nim, 2026
  - the two published versions above

  None reports the quantity of A389690 for any n.
- **Web search** (queries on A389690, the longest eventual period over all move sets, the OEIS entry's author, and the leading terms of the sequence). The only hit naming the sequence was PR #699. No other source gives a value for n = 23.
- Not done: OpenAlex, because no API key was available in this session.

## 4. Older prior art that could not be cleared: Flammenkamp (1997)

The two in-window papers above describe A. Flammenkamp's thesis *Lange Perioden in Subtraktions-Spielen* (Bielefeld, 1997). 2307.12458 says: "He completes a table with record holders for any finite ruleset with max S ⩽ 30". The GONC6 survey (2405.20054) places that work in a search for "long outcome periods via extensive computations".

- If the table lists outcome (win/lose) periods, it bears on A389689 for n ≤ 30, not on A389690.
- If it also lists nim-value periods, A389690(23) may have been known since 1997.

Neither paper reproduces the table.

My attempts to read the source:

1. wwwhomes.uni-bielefeld.de was blocked by the sandbox at first. Access was then granted.
2. The CGI home page returned a "CGIWrap Error: Script Execution Failed" page at 2026-10-26T07:26:03Z.
3. The static /achim/ page (dated 2025-09-21) only points to that CGI page.
4. Four guessed static paths (subtract.html, subtraction.html, sub_games.html, diss.html) returned 404.
5. A third-party blog that links the thesis was blocked by the sandbox allowlist. I did not request access, since it was only a way to find the link.

The table was not read, so this point stays open. A future novelty check should clear it, together with the status read.

## 5. Verdict

- The primary status page, its b-file and its history all returned HTTP 403 (error 1010) to one plain request each. No value was read, so "not yet in the OEIS entry, its b-file or its history at verification time" is unconfirmed: **novelty: PENDING STATUS CHECK**.
- Within what could be checked, nothing known equals or beats the claim:
  - TROPHY_CASE.md and the 329 open pull requests contain nothing that reports or claims A389690(23).
  - The recent closed pull requests and GitHub-wide issue/PR search contain nothing either.
  - The literature of the last 24 months I could reach does not report the value.
- These negative findings are not enough to pass. A pass needs a successful status read at verification time, and the Flammenkamp (1997) record table (max S ≤ 30) is still unread.

pass: false
