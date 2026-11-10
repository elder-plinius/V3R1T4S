# Novelty skeptic: p_c^site(Z^2) >= 0.5567

context: subagent (Claude Code Agent tool, fresh context, given only claim/)

Claim under review (CLAIM.md): p_c^site(Z^2) >= 0.5567. The best published rigorous lower bound it claims to improve
is 0.556, from van den Berg and Ermakov, Random Structures Algorithms 8 (1996) 199-212. The exact optimum of that
paper's method is stated as 0.5560829132 (code/vdbe1996.py).

Scope: novelty and record status only. I did not judge whether the proof or certificate is correct; the other panel
members cover that.

## Verdict

**novelty: CONFIRMED, as far as an honest search can tell.** No rigorous lower bound on p_c^site(Z^2) above 0.556
turned up anywhere: not in the literature from 1996 to 2026, not in the last 24 months, not in Russian or Chinese
sources, not in theses, not in this repo's TROPHY_CASE.md, and not in its 148 open PRs.

- 0.5567 is strictly above 0.556 by 0.0007, so this is not a tie.
- It is also above 0.5560829, the exact optimum of the 1996 method.
- I found no prior use of the claim's idea: exact message passing over the growth-process exploration tree, or a
  conditioning window larger than the 1996 one.

## Fetches (each URL requested once, with a plain request and an honest User-Agent)

All requests used curl with `-A "V3R1T4S-research-agent/1.0 (novelty check)"`. The time is UTC from `date -u`.
Where a URL answered with a plain 301/302 redirect (no login, cookie or authorization), I requested the target URL
once and list it as its own fetch.

| # | UTC time | URL | HTTP | bytes | sha256 of saved body | value read |
|---|---|---|---|---|---|---|
| 1 | 2026-10-18T18:50:24Z | https://en.wikipedia.org/w/index.php?title=Percolation_threshold&action=raw | 200 | 267722 | 588b98d38a819a6712a7b3b497a8df7e5a955285ba0b7bc3bace199f2c742ba3 | Square site: estimates only (0.59274605079210(2) Jacobsen 2015, etc.). No rigorous bounds; no mention of van den Berg, Ermakov or Menshikov. Byte-identical to the fetch recorded in table/literature_record.md (same sha256 and size). |
| 2 | 2026-10-18T18:50:25Z | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 200 | 31235 | b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1 | No entry contains "percol"; no square-site bound. |
| 3 | 2026-10-18T18:50:37Z | `gh pr list -R elder-plinius/V3R1T4S --state open --limit 200` (gh API, JSON) | ok (exit 0) | 44077 | 1699cd45b312df59fba81b0358ccaad3fc3fcba637ddd2b0bc8f2ff3f3db6fda | 148 open PRs. Percolation-related: #391 (2-uniform lattice #23 site p_c = 0.57176454(10), a numerical estimate) and #239 (2-uniform row #22 bond p_c, numerical). Neither concerns Z^2 or a rigorous bound. No square-site bound claim. |
| 4 | 2026-10-18T18:51:11Z | https://ir.cwi.nl/pub/25488/Thesis_AErmakov.pdf | 200 (application/pdf) | 24782731 | 596ec4145af87f72daa7ec1229c509a673b995e7985962381cb6626e8c376e5f | Ermakov's thesis, "Percolation and Coalescing Particle Systems". Chapter 2, Theorem 2.1: "larger than 0.556". The thesis gives no bound above 0.556. Remark (ii) says that checking the 1248 inequalities in the same window would not improve 0.556. |
| 5 | 2026-10-18T18:51:45Z | https://api.openalex.org/works/doi:10.1002/(SICI)1098-2418(199605)8:3%3C199::AID-RSA4%3E3.0.CO;2-T | 200 | (json) | 29ce0de49b7a6a20caeeb17759de75ef69c2b494b9e5f67e3d9d9c6e5a335366 | Work W2115080498, "A new lower bound for the critical probability of site percolation on the square lattice", 1996, cited_by_count 51. |
| 6 | 2026-10-18T18:51:51Z | https://api.openalex.org/works?filter=cites:W2115080498&per-page=100&sort=publication_year:desc&select=id,title,publication_year,doi,primary_location | 200 | (json) | fbaddab8b083d26590f3e7e2ee8216f569cf34d10af532fc2568a8a84336a92f | All 51 citing works listed (2025 back to 1997). None claims a new lower bound for p_c^site(Z^2). The 2020-2025 citers are listed in the next section. |
| 7 | 2026-10-18T18:52:09Z | https://www.mathnet.ru/eng/into1305 | 302 to the archive URL | 0 | (empty) | Plain redirect. |
| 8 | 2026-10-18T18:52:18Z | https://www.mathnet.ru/php/archive.phtml?wshow=paper&jrnid=into&paperid=1305&option_lang=eng | 200 | 25383 | cdc242eeb5f39970a5d63dbe387e5cdc5c3d70418abd78125023bdc7dc005257 | This is the 2024 companion paper: Virchenko and Cherkashin, "Hierarchical models in discrete percolation theory and Markov branching processes", Itogi Nauki i Tekhniki 235 (2024) 15-33. The abstract gives no numeric bound. |
| 9 | 2026-10-18T18:52:29Z | https://www.mathnet.ru/eng/into/v242/p22 | **503** | 189 | (not used) | Blocked. I stopped and did not retry this URL. |
| 10 | 2026-10-18T18:52:52Z | https://ogarev-online.ru/2782-4438/article/download/312569/286922 | 302 to journals.rcsi.science | 0 | (empty) | Plain host redirect from the publisher's journal platform. |
| 11 | 2026-10-18T18:52:57Z | https://journals.rcsi.science/2782-4438/article/download/312569/286922 | 200 (application/pdf, 19 pp.) | 2007085 | 9a29dca3e6357aaabe404144d507dfffcc5de7695edc8e9aa697363f3122d87c | Full Russian text of Virchenko and Cherkashin, "Approximations of the percolation probability on a periodic graph Z^2", Itogi Nauki i Tekhniki 242 (2025) 22-40, DOI 10.36535/2782-4438-2025-242-22-40. Threshold lower bounds: c* = 0.25 (order 0), c* ≈ 0.34 (order 1, "с недостатком"), c* ≈ 0.38 (order 2). |
| 12 | 2026-10-18T18:53:12Z | http://export.arxiv.org/api/query?search_query=abs:%22site%20percolation%22%20AND%20abs:%22square%20lattice%22%20AND%20abs:bound&sortBy=submittedDate&sortOrder=descending&max_results=100 | 301 to https | 0 | (empty) | Plain scheme redirect. |
| 13 | 2026-10-18T18:53:18Z | https://export.arxiv.org/api/query?search_query=abs:%22site%20percolation%22%20AND%20abs:%22square%20lattice%22%20AND%20abs:bound&sortBy=submittedDate&sortOrder=descending&max_results=100 | 200 | (xml) | 91c8ca7f67752a46bf0febddb3d177e7de9d6112797d5aaf7ddb2c395b69549b | 4 hits (1507.01371, 1506.06125, 1103.0901, 0711.3563). None is a bound on p_c^site(Z^2). |
| 14 | 2026-10-18T18:53:27Z | https://export.arxiv.org/api/query?search_query=abs:percolation%20AND%20abs:rigorous%20AND%20abs:%22square%20lattice%22&sortBy=submittedDate&sortOrder=descending&max_results=100 | 200 | (xml) | 1d4cb7b7e9e93eedd758063f5894f5b7014a79be50a11fc2fee23c7a529869da | 7 hits (2026 back to 2010). None is a rigorous bound on p_c^site(Z^2). |
| 15 | 2026-10-18T18:53:28Z | https://export.arxiv.org/api/query?id_list=2405.07345,2503.16703,1312.0961,1210.4150 | 200 | (xml) | 63b61535631561c378dfd0ffaecc50e45e528932c67df50679b6e10911308715 | Abstracts of the four arXiv papers cited in table/literature_record.md (see the checks below). |
| 16 | 2026-10-18T18:53:48Z | https://www.math.fau.edu/combinatorics/abstracts/oberly55.pdf | 200 | (pdf) | 29e069a561615cc5c74091caa00587c3fb6003e0ca5e96470c5f92597efb8f5a | Oberly and Wierman, "Further Improvements to the Upper Bound...": upper-bound work only, with no number in the abstract. |
| 17 | 2026-10-18T18:54:23Z | https://ir.cwi.nl/pub/4915 | 200 | 19553 | 2e6cc6bacf9ebfcb42e2b5c120acb70fd4c9cc9acfb4bf68e08b139ddfc3828b | Primary abstract of the 1995 CWI report behind the 1996 paper: "the best lower bound so far, 0.541 [Menshikov and Pelikh (1989)] ... we get a significant improvement, namely 0.556." |

Two more pages were blocked:
- A WebFetch of https://designday.jhu.edu/wp-content/uploads/formidable/18/Oberly-Sam_Poster_percolation_threshold-4.pdf returned **403**. I did not retry it.
- A WebFetch of the Ermakov thesis exceeded the tool's size limit, so I downloaded it once with curl instead (fetch 4).

Both status sources required by the instruction were read: the literature (fetches 1, 4-6, 8, 11, 13-17) and the
repo (fetches 2-3). So this is not a PENDING STATUS CHECK.

## Web search queries (all run on 2026-10-18)

1. `rigorous lower bound site percolation threshold square lattice improved 0.556` (extended)
2. `van den Berg Ermakov 0.556 site percolation square lattice lower bound improvement arXiv`
3. `нижняя оценка порога перколяции узельной квадратной решетки`
4. `"site percolation" "square lattice" "lower bound" critical probability 2024 OR 2025 OR 2026 new rigorous` (extended)
5. `Wierman lower bound site percolation threshold square lattice substitution method`
6. `computer-assisted proof lower bound percolation threshold square lattice site 0.556 improvement message passing exploration tree`
7. `Вирченко Черкашин перколяция квадратная решетка 2025 Итоги науки и техники оценка порога`
8. `Меньшиков Пелих оценка критической вероятности перколяции узлов квадратной решетки 0.541`
9. `Virchenko Cherkashin 2025 site percolation lower bound threshold Z^2 hierarchical graphs branching "2782-4438-2025-242"`
10. `Oberly Wierman "A New Upper Bound for the Site Percolation Threshold of the Square Lattice" 0.666894`
11. `"truncated square lattice" site percolation threshold rigorous bound arXiv 2024`
12. `Menshikov Pelikh "percolation with several defect types" estimate critical probability square lattice`
13. `"p_c" site square lattice "0.556" "best known" lower bound 2023 OR 2024 OR 2025 OR 2026` (extended)
14. `growth process stochastic domination coupling lower bound site percolation critical probability larger window improved van den Berg Ermakov method`
15. `Oberly dissertation Johns Hopkins site percolation threshold bounds square lattice substitution method thesis`
16. `正方晶格 座逾渗 阈值 严格 下界 0.556`
17. `Riordan Walters rigorous confidence intervals critical probabilities square lattice site 0.5925 0.5930 not rigorous lower bound`
18. `arXiv 2025 2026 rigorous bounds critical probability site percolation Archimedean lattices lower bound computer-assisted`

The structured searches were the arXiv API (fetches 13-15) and the OpenAlex citation index of the 1996 paper
(fetches 5-6).

## Strongest competing results found

These are the rigorous lower bounds on p_c^site(Z^2), in historical order:

| Bound | Source |
|---|---|
| 1/2 | Harris 1960 with Hammersley 1961 |
| > 1/2 strictly | Higuchi 1982 |
| 0.503478 | Tóth 1985 |
| 0.522105 | Zuev 1988 |
| 0.5416 | Menshikov and Pelikh 1989, Mat. Zametki 46(4) 38-47 |
| **0.556** | **van den Berg and Ermakov 1996 (best before this claim)** |

The Tóth, Zuev and Menshikov-Pelikh values are as listed in the Ermakov thesis and the CWI abstract.

The 0.556 bound is still cited as the best lower bound in later work:
- Ball, arXiv:1312.0961, which gives "p_c >= 0.556 due to van den Berg and Ermakov";
- arXiv:1210.4150;
- a 2025 paper found through search results, which says "p_c^site > 0.556".

Other results that do not compete:
- **Virchenko and Cherkashin 2025:** lower bounds 0.25, ≈0.34 and ≈0.38. These are far below 0.556.
- **Riordan and Walters 2007 (arXiv math/0702232):** 99.9999% confidence intervals, and Balister, Bollobás and
  Walters [0.5919, 0.5935] at 99.99%. These are statistical statements, not rigorous bounds, so they do not count.
- **arXiv:2503.16703 (2025):** Monte Carlo thresholds for extended neighbourhoods. This is a different problem and
  not rigorous.
- **Upper bounds:** Wierman 1995 gives 0.679492, and Wierman and Oberly 2024 give 0.666894 according to search-result
  abstracts. A JHU poster mentions 0.662869, but that page returned 403, so I could not verify it. None of these
  bears on the lower-bound record.
- **The 51 works citing the 1996 paper (OpenAlex):** none gives a new lower bound for p_c^site(Z^2). The 2020-2025
  citers are:
  - 1-independent percolation on Z^n, EJP 2025;
  - 1-independent percolation on Z^2 x K_n, RSA 2022;
  - the Wierman and Oberly upper-bound chapters of 2022 and 2024;
  - a cubic-lattice bond upper bound, JAP 2021;
  - fractal percolation, AAP 2020;
  - 1-independent random graphs, RSA 2020;
  - bootstrap percolation, AAP 2020;
  - uniqueness criteria, JMP 2021.

## Is the idea new?

I found no paper that runs exact message passing over the growth-process exploration tree, or that enlarges the
conditioning window of the van den Berg-Ermakov or Menshikov-Pelikh comparison.

The Ermakov thesis explains where the 1996 gain came from (Remark (iii)): it conditions on the joint law of all
children of a parent, where Menshikov and Pelikh used one child at a time. Remark (ii) says that the full set of 1248
inequalities in the same window cannot beat 0.556. Both remarks fit the claim's premise that only a larger window can
go further.

Some recent work uses related tools for other problems:
- Virchenko and Cherkashin (2024, 2025) use branching processes on hierarchical graphs and get weaker bounds.
- arXiv:2405.07345 uses stochastic domination for positively associated 1-independent models.

Neither is the claim's method.

## Checks of table/literature_record.md

- 0.556, its citation and the abstract's wording: **confirmed** (fetch 17; Ermakov thesis, Chapter 2).
- The Wikipedia fetch: **confirmed byte for byte.** It has the same sha256 588b98d3... and the same size, 267722
  bytes. It lists estimates only, with no rigorous bounds.
- "arXiv:1312.0961 and arXiv:1210.4150 cite 0.556 as the best known": **confirmed** for 1312.0961 from search-result
  text. 1210.4150 is consistent: the search results show it citing the bound.
- Virchenko and Cherkashin 2025 gives only 0.25 / ~0.34 / ~0.38: **confirmed from the full text** (fetch 11; DOI and
  pages 22-40 match). I read it from the publisher platform journals.rcsi.science, because the mathnet.ru URL I tried
  for this paper returned 503 and was not retried. So I could not confirm the record's remark "full text read from
  mathnet.ru", but the content is confirmed.
- **Error:** the record describes arXiv:2405.07345 (2024) as "a bound for the truncated square lattice". That is
  wrong. Its abstract (fetch 15) shows it is Köhler-Schindler and Sulser, "Critical probabilities for positively
  associated, finite-range dependent percolation models". It is about 1-independent and positively associated models.
  It is still not a competing bound, so the verdict stands, but the record should fix the citation.
- arXiv:2503.16703 is about complex neighbourhoods and is not rigorous: **confirmed.**
- The 2024 Wierman and Oberly upper bound of 0.666894: consistent with a search-result abstract ("reduced from
  0.679492 to 0.666894"). I did not verify it from a primary page. It is context only.
- Riordan and Walters do not count: **agreed.**

## Caveats

- Web search cannot prove a negative. In particular:
  - Russian literature from 1989-2000 not indexed online (Menshikov's school) could not be fully read.
  - The Menshikov-Pelikh paper itself was not read. It is cited at 0.5416 by both van den Berg and Ermakov and the
    thesis.
- I made no judgement on whether the 0.5567 proof or certificate is valid. Novelty passes only if the result holds.

pass: true
