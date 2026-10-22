# Table record (metadata and short excerpts only)

Each row is one honest GET (curl, user agent naming the research client, no retries) made by the contributor's team on
2026-10-18. No page is copied here, only the extracted cells named below. Fetch lines come from the contributor's FETCHLOG.

| Source | URL | UTC fetch time | HTTP | sha256 of the fetched bytes |
|---|---|---|---|---|
| A247413 (json) | https://oeis.org/search?q=id:A247413&fmt=json | 2026-10-18T20:46:01Z | 200 | 12c0e72579f0e422ddf1a43bfb25eda74756be01107b7bfcee3d8af08da40ef8 |
| A063443 b-file | https://oeis.org/A063443/b063443.txt | 2026-10-18T19:06:18Z | 200 | 60a6814583722264c81298bbe8c37e5b4367630cc57702da82bdb057db4d4d8f |
| Liang, arXiv 2505.12776 (pdf) | https://arxiv.org/pdf/2505.12776 | 2026-10-18T19:35:36Z | 200 | da54abc4a97c456c5b4d617043ed20d747c5260e22c6495d5bf87e44c3864ee8 |
| Liang, arXiv 2507.04007 (pdf) | https://arxiv.org/pdf/2507.04007 | 2026-10-18T20:46:16Z | 200 | 3a50788707bb819750a435169cf32a65f4b7f0b77f59568de01a342848d82f04 |

## A247413 DATA (18 terms)

Fetched 2026-10-18T20:46:01Z; the record shows revision 30, last edit 2026-05-30T16:40:43-04:00, keyword "nonn,cons,more,nice",
offset 1,2. Its DATA field, the only part excerpted here:

```
DATA_BEGIN
1,3,4,2,6,4,3,9,5,1,1,2,4,6,0,1,2,9
DATA_END
```

The first term is the integer part, so the 18 terms give 1.34264395112460129 (17 decimals). The success criterion counts the
terms of DATA (18), so the required number of decimals is at least 22.

## A063443 terms used by the checker

First terms of the b-file fetched 2026-10-18T19:06:18Z, n and A063443(n) (A063443(n) = number of independent sets of the king
graph on the (n-1) x (n-1) grid):

```
A063443_BEGIN
0 1
1 1
2 2
3 5
4 35
5 314
6 6427
7 202841
8 12727570
9 1355115601
10 269718819131
11 94707789944544
12 60711713670028729
A063443_END
```

## Kai Liang's stated bracket

arXiv 2505.12776v2 (23 Jun 2025), Independent Set Enumeration in King Graphs by Tensor Network Contractions, section 2
(Independent set enumeration), page 6, text extracted from the fetched pdf: "Here we calculate all the cases of m <= 34 and
n <= 100, and the more accurate estimation is:" followed by the displayed line

    1.34264395112460129 7851 (approximately less than) e^kappa < 1.34264395112460129 8092

(the lower sign is printed as an approximately-less-than symbol in the pdf; the space inside the digit string is in the
original and separates the digits after the 17th decimal).

arXiv 2507.04007v2 (8 Aug 2025), Independent Set Enumeration and Estimation of Related Constants of Grid Graphs and Their
Variants, the same king-graph bracket, stated in the summary of results on page 4 and as equation (38) on page 16 of the
fetched pdf:

    1.34264395112460129 7851 < e^(f_K) < 1.34264395112460129 8092

Page numbers are those printed in the page footers of the text extraction of the fetched pdfs.

## Other searches made by the contributor's team (all 2026-10-18)

- https://oeis.org/search?q=1,3,4,2,6,4,3,9,5,1,1,2,4,6,0,1,2,9,7,8,5&fmt=text, 20:46:01Z, HTTP 200, sha256
  f3ccbfe0c63618ee9b9ecf167105289e2cf30215c1e8c5e8e1c3ca70536176cc: the page reports "No results" for the first 21 terms
  (the 18 published terms followed by 7, 8, 5).
- https://export.arxiv.org/api/query?search_query=all:%22king%20graph%22%20AND%20all:%22independent%20set%22&max_results=30&sortBy=submittedDate,
  20:46:11Z, HTTP 200, sha256 a4ac23946c3da2a30e75ee1e345cc10101916dfbb5500ee1a5c4d9b2cbd27135 (the same query over http
  at 20:46:06Z answered 301 and was not retried).
- https://oeis.org/A247413/text at 19:06:18Z answered HTTP 404 and was not retried; the search form above was used instead.

## Compared cell

OEIS A247413 DATA: 18 terms, i.e. 17 decimals (the novelty skeptic's count, from its fetch 2026-10-19T01:44:50Z, HTTP 200, sha256 12c0e72579f0e422ddf1a43bfb25eda74756be01107b7bfcee3d8af08da40ef8, the same hash as the fetch above). Best published value found: Kai Liang's 21-decimal bracket. This package: 33 decimals.
