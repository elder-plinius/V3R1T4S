context: subagent (Claude Code Agent tool, fresh context)

# Novelty skeptic: card-guessing-yes-no-feedback-exact

Claim under review: exact reduced fractions for P+_{2,n} (yes/no feedback, two copies of each of n labels,
maximise the expected number of correct guesses) for n = 11..16, with n = 2..10 as calibration.
Inputs read from the claim folder: README.md, status/status_record.md, values.json. No other local file was read
(the only exception is the harness paging back one long output of my own command).

## Verdict

novelty: NEW. I found no published exact or numerical value of P+_{2,n} for any n >= 11, so none for n = 11..16.
The published frontier is the four-decimal table of Diaconis-Graham-Spiro (DGS, arXiv:2012.04019, Amer. Math.
Monthly 129 (2022)): Table 2 covers n = 2..5 and Table 3 covers n = 6..10. The only published exact value is
P+_{2,2} = 17/6 (Luo, arXiv:2609.25062, Prop. B.1). The newest paper on exactly this quantity (Luo, 14 Sep 2026)
calls the exact extrema at fixed multiplicity open: "Even for m = 2, the available bounds do not give an exact
answer." The claimed n = 11..16 values are therefore first values, not ties.

## 1. Status source (one honest fetch)

- URL: https://arxiv.org/search/?query=card+guessing+feedback&searchtype=all&abstracts=show&order=-announced_date_first&size=25
- Fetched 2026-10-15 13:52:33 UTC (finished 13:52:34 UTC) with one plain curl GET, User-Agent "V3R1T4S-novelty-skeptic/1.0".
  Result: HTTP 200, 98,792 bytes, saved as ../panel/novelty_status_fetch.html, sha256
  b457009a53b9c7f9ccf724ce8f7c247446977de8a5eb819340e5d339e80ed6fd. No retry was needed.
- This hash is byte-identical to the scout's hash in status/status_record.md (fetched 13:16:53 UTC). That fits
  with no arXiv announcement between the two fetches.
- The page shows "Showing 1-19 of 19 results":
  - Complete-feedback or no-feedback papers (mostly riffle or shelf shuffles):
    - 2610.17479 (Dey, Manthripragada, 12 Oct 2026, complete feedback)
    - 2609.25063 (Luo, complete feedback, shelf shuffles)
    - 2607.10418, 2602.12928, 2601.16607 (Kuba et al., shelf and riffle shuffles)
    - 2602.07920 (Tripathi, shelf position matrix)
    - 2308.15782, 2306.16079 (Kuba, Panholzer)
    - 2303.15601 (Ottolini, Tripathi)
    - 2211.09094 (Ottolini, Steinerberger)
    - 2209.04276, 2205.08793, 2107.11142 (Krityakierne, Thanatipanonda et al.)
    - 1908.07718 (Liu)
    - 1006.1321 (Pehlivan)
  - Yes/no-feedback papers:
    - 2609.25062 (Luo, partial feedback, v1 14 Sep 2026)
    - 2107.00850 (Alimohammadi, Diaconis, Roghani, Saberi; the greedy yes/no strategy via SIS)
    - 2012.04019 (DGS)
    - 2010.05059 (Diaconis, Graham, He, Spiro)
- Does any entry report an exact or numerical P+_{2,n} for n >= 11? No. It is not in any abstract, and not in the
  full TeX sources of the yes/no-feedback entries or of the two newest entries (all opened below).

## 2. What is published about P+_{2,n}

| n | published value | source |
|---|---|---|
| 2 | exact 17/6; also 2.8333 | Luo 2609.25062 Prop. B.1 (closed form for P+-_{m,2}); DGS Table 2 |
| 3-5 | 3.0111, 3.0452, 3.0467 (four decimals) | DGS Table 2 |
| 6-10 | 3.0376, 3.0323, 3.0260, 3.0219, 3.0186 (four decimals) | DGS Table 3 |
| >= 11 | none found | - |

Other related results, none of which is P+_{2,n} for n >= 11:
- **Diaconis-Graham 1981 (Gatto 1978).** Computed decks with composition vectors smaller than (5,5,5,5,5), so for
  m = 2 at most n = 5. Only the m = n values are printed: E(3,3,3) = 4.26, E(4,4,4,4) = 5.47, E(5,5,5,5,5) = 6.63.
- **Alimohammadi-Diaconis-Roghani-Saberi (Ann. Appl. Probab. 2023).** The table "Greedy versus SIS estimator ...
  for m = 2" gives values of the greedy strategy, not the optimum:
  - n = 2..5: 2.8333, 3.0111, 3.0333, 3.0433;
  - n = 10: 2.9786; n = 20: 2.9585 (with confidence intervals).
  Greedy is already strictly below P+ at n = 4 (3.0333 against 3.0452), and the table has no entry for n = 11..16.
- **Bounds only.** 2.91 <= liminf P+_{2,n} <= limsup P+_{2,n} <= 2(e-1), from DGS Theorem 2 and Luo's universal
  upper bound.

## 3. Calibration check (not part of the novelty question)

- values.json n = 2..10 agree with DGS to four decimals.
  - n = 7 (3.0323693...) agrees only by truncation; rounding gives 3.0324, as README.md already notes.
  - n = 10 (3.0185985...) agrees by rounding.
- n = 2 equals Luo's exact 17/6. That is a tie with a published value, so it is calibration only.
- All 15 fractions are in lowest terms, and every decimal20 string is the truncated expansion of its fraction.

## 4. Sources opened (all times UTC, 2026-10-15)

Request method:
- curl, one plain GET per request, User-Agent "V3R1T4S-novelty-skeptic/1.0", no browser-like headers.
- arXiv requests at least 3 s apart (in practice 4 s or more).
- WebSearch is the Claude Code tool; its times are bracketed by the neighbouring timestamped requests.

arXiv
1. 13:52:33, the status source above.
2. 13:53:24, https://arxiv.org/abs/2609.25062 : HTTP 200. Only v1 exists (Mon 14 Sep 2026 16:57:19 UTC, 24 KB), 18 pages.
3. 13:53:42, 13:54:01, 13:54:18 and 14:06:18, https://arxiv.org/src/2609.25062 : HTTP 200, v1 tarball of 24,723 bytes.
   - There is no table or tabular environment.
   - The only explicit values are P-_{1,n}, P+_{1,n} = sum_{k<=n} 1/k!, the closed form for P+-_{m,2}, and
     (P-_{2,2}, P+_{2,2}) = (7/6, 17/6).
   - Appendix A gives the recursion only. "Further questions" calls the exact fixed-m extrema open.
   - All 12 bibliography entries were reviewed. Every relevant one is covered in this list.
4. 13:54:42, https://arxiv.org/abs/2012.04019 : HTTP 200. v1 is 7 Dec 2020, v2 is 18 Jul 2021, with the comment "to
   appear in the American Mathematical Monthly excluding Section 6".
5. 13:54:56, https://arxiv.org/src/2012.04019 : DGS v2 TeX, with four tables:
   - Table 1: m = n = 5, values 5 / 6.65 / 8.65.
   - Table 2: m = 2, n = 2..5, optimal, greedy and linear strategies.
   - Table 3: m = 2, n = 6..10, optimal, four decimals.
   - Table 4: simulated heuristics.
   Nothing for n >= 11.
6. 13:55:15, https://arxiv.org/src/2010.05059 : the DGHS TeX has no tables and no numerical value of P+.
7. 13:55:36, arXiv search "partial feedback guessing" (all fields): 6 results. They are 2609.25062, 2212.08113 (Nie),
   2010.05059 and 1908.07718, plus two unrelated papers (2608.22267, 2510.05174).
8. 13:55:44, arXiv search "\"yes/no feedback\"": 1 result, 2609.25062.
9. 13:55:50, arXiv title search "card guessing": 22 results. The ones not already in the status list are:
   - 2510.01844 (number-guessing card trick)
   - 2303.04609 (two card types only)
   - 2108.07355 (complete feedback)
   - 2107.03885 (limited memory)
   - a 2002 quant-ph quantum card game
   None is about P+_{2,n} for n >= 3.
10. 13:55:55, arXiv search "Diaconis Graham Spiro": 7 results (2609.25062, 2212.08113, 2110.10315, 2108.07355,
    2106.11866, 2012.04019, 2010.05059).
11. 13:56:04, arXiv abstract search "guessing feedback deck": 12 results, all already listed.
12. 13:56:11, a malformed arXiv author query ("Nie"): unrelated results, ignored.
13. 13:56:28, https://arxiv.org/src/2212.08113 (Nie, "The number of correct guesses with partial feedback"): no
    tables and no numerical values.
14. 13:56:34, https://arxiv.org/src/2110.10315 (Clifton-Deb-Huang-Spiro-Yoo): gives the limit of the
    increasing-subsequence statistic, L_2^1 = e(cos 1 + sin 1) - 1, which is a strategy lower bound. No P+_{2,n}.
15. 13:56:39, https://arxiv.org/src/2106.11866 (Spiro, "Online card games"): an adversarial complete-feedback game.
    No P+ values.
16. 13:56:43 and 13:57:18, https://arxiv.org/src/2107.00850 (ADRS): the m = 2 greedy table described in section 2.
    No optimal values and nothing for n = 11..16.
17. 14:06:40, arXiv title search "\"permutations with restricted positions\"": no results.
18. 14:08:48, https://arxiv.org/list/math.PR/recent?skip=0&show=2000 : 289 entries (8-15 Oct 2026). The only
    card-guessing title is 2610.17479.
19. 14:09:01, https://arxiv.org/list/math.CO/recent?skip=0&show=2000 : 389 entries, no card-guessing title.
20. 14:09:25, https://arxiv.org/src/2610.17479 (Dey-Manthripragada, 12 Oct 2026): partial feedback appears only in
    the introduction, which cites Luo 2026 as the latest such work and says "Our results concern only the complete
    feedback rule". No P+ values.
21. 14:12:25, https://arxiv.org/src/2609.25063 (Luo, complete feedback): no partial or yes/no feedback and no tables.

OEIS: 17 queries, 13:57:48-13:59:57, https://oeis.org/search?q=... (fmt=data, short or text)
22. "No match" for all of these:
    - numerators "17,271,1279,57583" and "271,1279,57583,1136743";
    - denominators "6,90,420,18900";
    - one digit string;
    - "card guessing feedback" and "\"card guessing\"".
    Control queries showing the search works:
    - "1,1,2,5,14,42,132,429" gives 23 hits.
    - "guessing" gives 199 hits; the first 10 are unrelated.
    Keyword queries, none relevant:
    - "guessing cards", 11 entries: A144188, A322755/A322756 (two-colour game), A371217, A000041, A000670,
      A318354, A372265, A372266, A143381, A214623. None is P+_{m,n}.
    - "guessing feedback": A286676, A010060.
    - "correct guesses": 40 hits; I inspected the first 30.
    - "card feedback": A348842.
    Conclusion: OEIS has no sequence of P+_{2,n} values.

V3R1T4S repository (https://github.com/elder-plinius/V3R1T4S)
23. 14:00:11, https://api.github.com/repos/elder-plinius/V3R1T4S : default branch main, last push 2026-10-14T05:12:50Z.
24. 14:00:18, https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md : HTTP 200, 30,264 bytes,
    sha256 067922c90c3ba409bde64b775a42e8caef685d25d1934a25a855768ca19ce249.
    - It lists six result families (degree-diameter graphs, constant-weight codes, matrix multiplication, Lehmer,
      VNN-COMP, RobustBench) plus two cipher commitments.
    - No match for card, guess, feedback, Diaconis, Spiro or Luo.
25. 14:00:30 and 14:00:44, https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 :
    59 open PRs, numbered #1 to #177 (newest created 13:58:12Z).
    - Targets: FMM rank and additive complexity, QOBLIB portfolio, stable marriage, risk-or-safety, robust forecast
      aggregation, codetables, Hadamard, Erdos 699, VNN-COMP, degree-diameter, Packomania, Thomson, constant-weight
      codes, and tooling fixes.
    - None is for card-guessing-yes-no-feedback-exact. No title, body or branch mentions card, guess, yes/no,
      feedback, Luo, Diaconis or Spiro.
26. 14:01:06, https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=closed&per_page=100 : the 100 most recent
    closed PRs. The only keyword hit (#29) is an Erdos 757 Sidon-set claim. Nothing on this target.
27. 14:01:21, https://api.github.com/repos/elder-plinius/V3R1T4S/git/trees/main?recursive=1 : 609 paths, none
    containing card, guess or feedback.
28. 14:01:29 and 14:01:44, https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/bank/targets.json :
    135 targets, no card-guessing target (every "card" hit is "cardinality" or "discard"). The target is not in the
    public bank.

Other sources
29. WebSearch, 5 queries between 14:01:45 and 14:02:40:
    - card guessing "yes/no feedback" optimal ... two copies exact values;
    - "card guessing" "partial feedback" 2025 OR 2026 ... m=2;
    - mathoverflow OR math.stackexchange ... two copies;
    - ... dynamic programming exact rational "n = 11" OR "n=12" OR "n = 16";
    - Congyi Luo ... follow-up OR citing.
    The results were the arXiv papers above, 2507.10294 (shelf-shuffling machines, not yes/no feedback),
    ResearchGate copies of DGS and DGHS, Zenodo 22762230, NSF PAR 10339301, a UCSD seminar page and Spiro's talk PDF.
    None gives P+_{2,n} for n >= 11.
30. 14:02:41, https://zenodo.org/api/records/22762230 : Luo's preprint, deposited 2026-09-15. It holds one PDF
    (177,690 bytes) and no supplementary data.
31. 14:03:02, that PDF, via https://zenodo.org/api/records/22762230/files/.../content : the same text as arXiv v1. No
    tables; the only values are 17/6 and the 2.91 bound.
32. 14:03:32, https://discretemath.wp.txstate.edu/files/2023/04/Spiro_Feb_18_2022.pdf : a seminar announcement only
    (Spiro, "Card Guessing with Partial Feedback", 18 Feb 2022). No numbers.
33. 14:03:49, https://par.nsf.gov/servlets/purl/10339301 : the accepted CPC version of DGHS. No tables and no
    numerical P+ values.
34. 14:04:23-14:04:40, https://api.openalex.org/works?search=... (4 title searches): HTTP 429 every time, no data.
    See section 5.
35. 14:05:00, https://api.semanticscholar.org/graph/v1/paper/arXiv:2012.04019/citations : HTTP 429. Stopped, not retried.
36. 14:05:20, https://api.zbmath.org/v1/document/_search?search_string=card%20guessing%20feedback : 23 documents
    (1981-2026).
    - All are either already covered here, or about riffle and shelf shuffles, no feedback, complete feedback, or
      Mastermind.
    - None gives P+_{2,n} for n >= 11.
    - It confirms the journal versions: DGS in AMM 2022 (doi 10.1080/00029890.2022.2069986), DGHS in CPC 2022
      (doi 10.1017/S0963548321000134), ADRS in AAP 2023.
37. WebSearch, 3 queries between 14:05:21 and 14:06:17:
    - "persistence conjecture" card guessing;
    - deck "1,1,2,2,...,n,n" yes/no feedback table;
    - Sam Spiro homepage data code.
    No new source, and nothing for n >= 11.
38. WebSearch, 1 query between 14:06:41 and 14:07:47: Diaconis-Graham-Holmes 2001. It located the PDF in item 39.
39. 14:07:48, https://mathweb.ucsd.edu/~ronspubs/01_07_permutations.pdf (Diaconis, Graham, Holmes 2001): yes/no
    feedback appears only for the ESP deck (6.63). No m = 2 table.
40. 14:08:05-14:08:25, https://api.github.com/search/repositories?q=... with three queries:
    - "card guessing feedback": 9 hits, all toy games;
    - "card guessing partial feedback": 0 hits;
    - "diaconis graham guessing": 0 hits.
41. WebSearch, 2 queries between 14:09:26 and 14:09:58:
    - "3.0154" OR "3.01542" OR "3.0137" OR "3.0076" with card guessing;
    - "Table 3" Diaconis Graham Spiro extended computation 2025 2026.
    Nothing found.
42. 14:09:59, https://gwern.net/doc/reinforcement-learning/exploration/1981-diaconis.pdf (Diaconis-Graham 1981 scan):
    - Gatto's computation covers composition vectors smaller than (5,5,5,5,5). The printed values are those of
      section 2.
    - The paper says "We do not know if the greedy strategy is optimal for decks of 2n cards with composition vector
      (2, 2, ..., 2)".
    - Nothing for m = 2, n >= 11.
43. 14:13:26, https://api.opencitations.net/index/v2/citations/doi:10.1080/00029890.2022.2069986 (works citing DGS):
    5 citing works. They are AIMS Math. 2025 (10.3934/math.20251075), Ottolini-Steinerberger (AAM 2023),
    Clifton et al. (EJC 2023), He-Ottolini (AAP 2023) and Ottolini-Tripathi (JAP).
44. 14:13:33, https://api.opencitations.net/index/v2/citations/doi:10.1017/S0963548321000134 (works citing DGHS):
    8 records. They are Tripathi arXiv:2602.07920, AIMS Math. 2025, Kuba-Panholzer (JSPI 2024), ADRS (AAP 2023),
    Spiro (EJP 2022), He-Ottolini, Ottolini-Tripathi, and one self-record.
45. 14:13:52-14:14:04, https://api.crossref.org/works/ for three DOIs:
    - 10.3934/math.20251075: Krityakierne-Thanatipanonda, "A generating function framework for the no-feedback card
      guessing game after riffle shuffles" (no feedback).
    - 10.1214/22-ejp768: Spiro, "Online card games" (complete feedback).
    - 10.1214/23-aap1946: He-Ottolini (complete feedback).
    None computes P+_{2,n}.
46. WebSearch, 1 query between 14:14:05 and 14:16:17: Sam Spiro's dissertation. The thesis was not found. Two new
    URLs came back:
    - 14:16:18, https://purl.stanford.edu/kr135hw1604 : the connection timed out after 60 s and was not retried.
      Judging by its title in the search results, it is a repository copy of DGS, which item 5 already read.
    - 14:17:22, https://lmns.fudan.edu.cn/_upload/article/files/c9/22/b24a21b44ef6be83bf811b717089/67ac182e-4271-4681-8252-c74633a114c1.pdf :
      the host does not resolve in DNS, from curl or from WebFetch (about 14:17:40). Content unknown; the search
      summary suggests a talk listing.

## 5. Deviations and limitations

Deviations from the request rules:
- **13:53:42, stray file.** A malformed command wrote the response headers of one arXiv source request to a
  temporary file outside the panel folder and discarded the body. I deleted the file at once and confirmed it was
  gone, then re-requested the source at 13:54:01. The first response was HTTP 200, so this was not a retry after a
  block.
- **14:00:30, parser crash.** My JSON parser crashed on the open-PR list, which had come back HTTP 200. I sent the
  same request again at 14:00:44.
- **14:04:23-14:04:40, OpenAlex.** OpenAlex returned HTTP 429 to the first query, but my loop still sent three more,
  different queries, all of which also got 429. That breaks the no-requests-after-a-block rule for this host. I made
  no further OpenAlex requests. The single Semantic Scholar request (14:05:00) also got 429 and was not retried.

Coverage gaps:
- **Citation graphs are only partly covered.** OpenAlex and Semantic Scholar were unavailable, and OpenCitations
  only covers references deposited with Crossref. Google Scholar was not used, because the sources had to be
  Google-free.
- **Some texts are paywalled or unreachable:**
  - the AMM 2022 version of DGS (arXiv v2 is the accepted text, excluding its Section 6);
  - Chung-Diaconis-Graham-Mallows 1981 (Adv. Appl. Math.);
  - Gatto's 1978 thesis (Diaconis-Graham 1981 says it covers compositions below (5,5,5,5,5));
  - the two unreachable URLs in item 46.
- **Unannounced arXiv submissions and unpublished work cannot be checked.**

None of these gaps contradicts the finding. The newest work on exactly this quantity (Luo, Sep 2026) calls the
exact fixed-m extrema open. The newest card-guessing paper (Dey-Manthripragada, 12 Oct 2026) cites Luo as the latest
partial-feedback work.

## Conclusion

novelty: NEW. I found no exact or numerical value of P+_{2,n} for any n = 11..16, and none for any n >= 11. The
sources searched were:
- arXiv (search, recent listings, and the full sources of every yes/no-feedback paper);
- OEIS, zbMATH Open, OpenCitations and Crossref;
- Zenodo, NSF PAR and author or talk pages;
- GitHub;
- the V3R1T4S TROPHY_CASE.md, its open and recent closed PRs, and the public bank.

The claimed values for n = 11..16 are first values, not ties. The n = 2..10 values are calibration only: they match
the DGS four-decimal tables and Luo's exact 17/6.

pass: true
