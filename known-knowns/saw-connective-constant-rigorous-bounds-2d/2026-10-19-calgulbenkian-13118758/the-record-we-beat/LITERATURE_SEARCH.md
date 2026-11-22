# Literature search: rigorous upper bounds for mu(4.8^2), after Jensen 2004

Date: 2026-10-19 (UTC, 06:22 to 06:28). Agent: Claude (literature-search worker). Honest client rules followed: one plain GET per URL, user agent "V3R1T4S-research (honest client; curl)", no retries, no browser, no writes. Raw responses are in raw/ and every fetch is in FETCHLOG.txt.

Question: since 2004, has any rigorous upper bound below 1.82926 been published for the self-avoiding-walk connective constant of the 4.8^2 lattice? (Claim under test: mu(4.8^2) <= 1.8281442934.)

## Conclusion (plain)

I found no published rigorous upper bound below 1.82926 for the 4.8^2 lattice. Nothing in the searchable record contradicts 1.82926 as the best published bound, so Argon's 1.8281442934 would be new, as far as this search can show.

Limits on that statement:
- The only paper that could contain a better number is Alm 2005 (J. Phys. A 38 (2005), "Upper and lower bounds for the connective constants of self-avoiding walks on the Archimedean and Laves lattices"). It is the published form of the Alm "in preparation" result that Jensen cites as 1.82926. It is paywalled (OpenAlex: closed access). I read only its abstract, which gives no numbers. It is therefore possible, though not indicated, that the published version states a value different from the 1.82926 that Jensen quoted from a private communication.
- Parviainen's thesis (Uppsala Dissertations in Mathematics 34, 2004), which Jensen names as the source of 1.82926, has an open full text at DiVA, but the DiVA host timed out and I did not retry (rule). So I could not read the thesis itself. The 1.82926 attribution rests on Jensen's footnote.
- Semantic Scholar returned HTTP 429 on all four searches (not retried, unresolved). I substituted OpenAlex and arXiv for the citation and topic searches; they are not the same index.
- Not searched: Google Scholar, MathSciNet, zbMATH, Scopus/Web of Science, publisher full texts behind paywalls.

Number of candidates read: 13 (full text: 4; abstract only: 8; unreadable: 1). Details below.

## Evidence that 1.82926 is the figure on record

Jensen 2004 (arXiv cond-mat/0409381v2, J. Phys. A 37 (2004) 11521), Table 3, full text read:
"(4.8^2)  Lower Bound 1.804596   mu 1.80883001(6) [15]   Upper Bound 1.82926 [3]"
Reference [3]: "Alm S E 2004 in preparation. Courtesy of a private communication from R Parviainen and contained in his PhD Thesis Connective Properties of Archimedean and Laves Lattices Uppsala dissertations in mathematics 34 Uppsala University".
Jensen also says: "It is clear that sharper upper bounds can be obtained for square and triangular lattices by Alm's method if carried out to higher values of n and m."

## Candidates

| # | Paper | Read | What it says about 4.8^2 upper bounds |
|---|---|---|---|
| 1 | Jensen 2004, Improved lower bounds ... (arXiv cond-mat/0409381v2) | full text | Table 3 above: upper bound 1.82926 credited to Alm [3]. Abstract: "Upper bounds are obtained from recent exact enumeration data ... and compared to current best available upper bounds from other methods." |
| 2 | Alm 2005, J. Phys. A 38 (2005), DOI 10.1088/0305-4470/38/10/001 | abstract only (OpenAlex; paywalled) | "We give improved upper and lower bounds for the connective constants of self-avoiding walks on a class of lattices, including the Archimedean and Laves lattices. ... The upper bounds are obtained as the largest eigenvalue of a certain transfer matrix." No numbers in the abstract. This is the paper that could hold a different 4.8^2 value. Unresolved. |
| 3 | Parviainen, PhD thesis, Uppsala 2004, "Connective Properties of Archimedean and Laves Lattices" (OpenAlex lists it as "Connectivity Properties ...", W1921768404; DiVA urn:nbn:se:uu:diva-4251) | not read | Open full text at uu.diva-portal.org/smash/get/diva2:164546/FULLTEXT01.pdf: connection timed out (one GET, not retried); the urn.kb.se resolver returned 302 and I did not follow it. Unresolved. |
| 4 | Alm and Parviainen 2004, Bounds for the connective constant of the hexagonal lattice, J. Phys. A 37 (2004), DOI 10.1088/0305-4470/37/3/001 | title only (Crossref, no abstract) | Hexagonal lattice only (upper bound 1.868832 per Jensen). No 4.8^2 bound. |
| 5 | Grimmett and Li, Self-avoiding walks and connective constants (arXiv 1704.05884v2) | full text, searched for 4.8, octagon, 1.82, Archimedean | Example 5.2: "The best lower bound currently known appears to be mu > 1.804 ..., see [45]" (Jensen). Gives no upper bound for (4,8^2). |
| 6 | Bauerschmidt, Duminil-Copin, Goodman, Slade, Lectures on Self-Avoiding Walks (arXiv 1206.2092v1) | full text, searched | No occurrence of the 4.8^2 lattice or of any 1.82 bound. |
| 7 | Upper bounds for the connective constant of weighted self-avoiding walks (arXiv 2508.01993v3; J. Phys. A 2025, 10.1088/1751-8121/ae280e) | full text, searched | "Building on a work by Alm ... implement it in a publicly available software package." No 4.8^2 value, no octagon lattice mentioned. |
| 8 | New upper bound for the connective constant for square-lattice SAWs (arXiv 2211.16146v2) | abstract | "we obtain 2.662343 as an upper bound for the connective constant in the lattice Z^2." Square lattice only. |
| 9 | Existence and bounds of growth constants for restricted walks, surfaces ... (arXiv 2509.04568v1) | abstract | Bounds for self-osculating walks on square and triangular lattices only. |
| 10 | A numerical adaptation of SAW identities from the honeycomb to other 2D lattices (arXiv 1110.1141v2) | abstract | Numerical estimates for square and triangular lattices; no rigorous 4.8^2 bound. |
| 11 | Self-avoiding walks on cubic graphs and local transformations (arXiv 2601.12571v2) | abstract | Exact substitution identities for cubic graphs; no 4.8^2 bound stated in the abstract. The square-octagon lattice is cubic, so the full text is worth a look if exact values matter (not a rigorous numeric upper bound in the abstract). |
| 12 | Zenodo certificate archive, improved lower bound mu(Z^2) >= 2.6273856 (OpenAlex W7171182314, 2026) | abstract | Square-lattice lower bound; cites Jensen 2004. Not about 4.8^2. |
| 13 | Grimmett and Li, Locality of connective constants (arXiv 1412.0150v5) | abstract | Locality theorem; no bounds for 4.8^2. |

Also screened by title and abstract (no 4.8^2 or Archimedean upper bound found): the 5 Crossref result sets (about 330 unique records; keyword hits for Archimedean/octagon were physics papers on Ising, percolation, quantum models, none about SAW bounds), arXiv topic queries (66 SAW/connective-constant records; 1 Archimedean+self-avoiding record, a 1997 Kagome percolation paper; 5 "bathroom tile" records, all Ising), and the OpenAlex citing lists: 12 works citing Alm 2005, 22 and 23 citing the two OpenAlex records of Jensen 2004 (about 55 distinct titles). None of the citing titles is a 4.8^2 bound. Cited-by lists include Grimmett-Li (2014 regular graphs, 2014 strict inequalities, 2019 book chapter), Sinclair-Srivastava-Stefankovic (spatial mixing), and Alm 2006 "On measures of average degree for lattices" (Combin. Probab. Comput.; not read, abstract absent in OpenAlex). Alm 2006 deserves a check: a lattice-degree paper by the same author could restate bounds.

Titles listed under the Crossref hits that are relevant by topic but not about 4.8^2: Alm 2005 (above), Jensen 2004 lower bounds (above), Guttmann-Parviainen-Rechnitzer 2005 on the 3.12^2 lattice (10.1088/0305-4470/38/3/002; no abstract), Grimmett-Li regular graphs (10.1007/s00493-014-3044-0; no abstract).

## Queries and fetches

Crossref (cr1 to cr5) used filter=from-pub-date:2004-01-01, rows=100, select=DOI,title,issued,container-title,abstract. Queries: (1) connective constant 4.8^2 lattice; (2) self-avoiding walks square-octagon lattice upper bound; (3) bathroom tile lattice self-avoiding; (4) Archimedean lattices connective constant bounds; (5) rigorous bounds connective constant self-avoiding walk Archimedean. Crossref relevance ranking returns mostly noise on these (total hits are in the millions), so these searches mainly surfaced the Alm 2005 and Jensen 2004 records.

Semantic Scholar: the four requested queries all returned 429. The Semantic Scholar citations endpoint was not requested, since the API was already refusing; OpenAlex cited-by lists were used instead. Crossref "references" filter returned 400 (not supported without the right parameters, not retried). OpenAlex "cites:doi" returned 400 (not retried; used OpenAlex ids instead).

Two fetches timed out (curl exit 28, no HTTP status, logged in FETCHLOG.txt with status 000): citeseerx (Alm 2005 copy) and the DiVA result list. The thesis PDF fetch also timed out (logged as curl error). One 302 (urn resolver), and arxiv http:// calls returned 301 (re-fetched once each over https, which is a different URL).

Full fetch table (results = records returned in the response body; sha256 shortened here, full hashes in FETCHLOG.txt):

| UTC time | HTTP | sha256 | file | results | URL |
|---|---|---|---|---|---|
| 2026-10-19T06:22:26Z | 200 | 521f47f1507ea4c2... | cr1.json | 100 | https://api.crossref.org/works?filter=from-pub-date:2004-01-01&rows=100&select=DOI,title,issued,container-title,abstract&query=connective+constant+4.8%5E2+lattice |
| 2026-10-19T06:22:29Z | 200 | a2ba14c362961049... | cr2.json | 100 | https://api.crossref.org/works?filter=from-pub-date:2004-01-01&rows=100&select=DOI,title,issued,container-title,abstract&query=self-avoiding+walks+square-octagon+lattice+upper+bound |
| 2026-10-19T06:22:31Z | 200 | 59832d8faba84b1d... | cr3.json | 100 | https://api.crossref.org/works?filter=from-pub-date:2004-01-01&rows=100&select=DOI,title,issued,container-title,abstract&query=bathroom+tile+lattice+self-avoiding |
| 2026-10-19T06:22:33Z | 200 | 71ba506705921540... | cr4.json | 100 | https://api.crossref.org/works?filter=from-pub-date:2004-01-01&rows=100&select=DOI,title,issued,container-title,abstract&query=Archimedean+lattices+connective+constant+bounds |
| 2026-10-19T06:22:36Z | 200 | 7aad501ce825042c... | cr5.json | 100 | https://api.crossref.org/works?filter=from-pub-date:2004-01-01&rows=100&select=DOI,title,issued,container-title,abstract&query=rigorous+bounds+connective+constant+self-avoiding+walk+Archimedean |
| 2026-10-19T06:22:39Z | 429 | 65ab993d12c5c2cc... | ss1.json | - | https://api.semanticscholar.org/graph/v1/paper/search?fields=title,year,venue,abstract,externalIds&limit=100&query=connective+constant+4.8%5E2+lattice |
| 2026-10-19T06:22:39Z | 429 | 65ab993d12c5c2cc... | ss2.json | - | https://api.semanticscholar.org/graph/v1/paper/search?fields=title,year,venue,abstract,externalIds&limit=100&query=self-avoiding+walks+square-octagon+lattice+upper+bound |
| 2026-10-19T06:22:39Z | 429 | 65ab993d12c5c2cc... | ss3.json | - | https://api.semanticscholar.org/graph/v1/paper/search?fields=title,year,venue,abstract,externalIds&limit=100&query=bathroom+tile+lattice+self-avoiding |
| 2026-10-19T06:22:40Z | 429 | 65ab993d12c5c2cc... | ss4.json | - | https://api.semanticscholar.org/graph/v1/paper/search?fields=title,year,venue,abstract,externalIds&limit=100&query=Archimedean+lattices+connective+constant+bounds |
| 2026-10-19T06:23:05Z | 200 | 8d9005405dd7df68... | crdoi_alm2005.json | 0 | https://api.crossref.org/works/10.1088/0305-4470/38/10/001 |
| 2026-10-19T06:23:06Z | 200 | 27a79185e834019a... | crdoi_jensen2004.json | 0 | https://api.crossref.org/works/10.1088/0305-4470/37/48/001 |
| 2026-10-19T06:23:06Z | 200 | b39f08c144b67a79... | crdoi_almparv.json | 0 | https://api.crossref.org/works/10.1088/0305-4470/37/3/001 |
| 2026-10-19T06:23:07Z | 400 | 92c28a10ece8e16d... | crcites_alm2005.json | - | https://api.crossref.org/works?filter=references:10.1088/0305-4470/38/10/001&rows=100&select=DOI,title,issued,author |
| 2026-10-19T06:23:07Z | 301 | e3b0c44298fc1c14... | arx1.xml | - | http://export.arxiv.org/api/query?search_query=all:%22connective+constant%22+AND+all:Archimedean&max_results=100 |
| 2026-10-19T06:23:08Z | 301 | e3b0c44298fc1c14... | arx2.xml | - | http://export.arxiv.org/api/query?search_query=all:%22self-avoiding%22+AND+all:octagon&max_results=100 |
| 2026-10-19T06:23:08Z | 200 | 9b3072ce53441369... | oa_jensen.json | 25 | https://api.openalex.org/works?search=Improved+lower+bounds+on+the+connective+constants+for+two-dimensional+self-avoiding+walks&select=id,title,cited_by_api_url,doi,publication_year |
| 2026-10-19T06:23:14Z | 200 | d4ac7acd3ffd04f8... | arx1.xml | 0 | https://export.arxiv.org/api/query?search_query=all:%22connective+constant%22+AND+all:Archimedean&max_results=100 |
| 2026-10-19T06:23:14Z | 200 | 92bd0758dcc27fa6... | arx2.xml | 1 | https://export.arxiv.org/api/query?search_query=all:%22self-avoiding%22+AND+all:octagon&max_results=100 |
| 2026-10-19T06:23:15Z | 200 | 6169fb949144c2f2... | oa_alm2005.json | 0 | https://api.openalex.org/works/doi:10.1088/0305-4470/38/10/001 |
| 2026-10-19T06:23:25Z | 200 | 00e436c1b3afebf2... | oa_cites_alm2005.json | 12 | https://api.openalex.org/works?filter=cites:W2040632682&per-page=100&select=id,title,publication_year,doi,abstract_inverted_index |
| 2026-10-19T06:23:26Z | 200 | 4c9b9f923c57f935... | oa_cites_jensen_a.json | 22 | https://api.openalex.org/works?filter=cites:W2024602257&per-page=100&select=id,title,publication_year,doi,abstract_inverted_index |
| 2026-10-19T06:23:26Z | 200 | 89a333202ed4767f... | oa_cites_jensen_b.json | 23 | https://api.openalex.org/works?filter=cites:W3105783798&per-page=100&select=id,title,publication_year,doi,abstract_inverted_index |
| 2026-10-19T06:23:27Z | 400 | 42bee26ffa332ba4... | oa_cites_almparv.json | - | https://api.openalex.org/works?filter=cites:doi:10.1088/0305-4470/37/3/001&per-page=100&select=id,title,publication_year,doi,abstract_inverted_index |
| 2026-10-19T06:25:44Z | 200 | 5a77756254f479eb... | cr_parv.json | 50 | https://api.crossref.org/works?query.author=Parviainen+self-avoiding+walk&filter=from-pub-date:2003-01-01&rows=50&select=DOI,title,issued,container-title,author |
| 2026-10-19T06:25:46Z | 200 | c13a6cb5f46519cc... | arx3.xml | 66 | https://export.arxiv.org/api/query?search_query=all:%22connective+constant%22+AND+all:%22self-avoiding%22&max_results=100&sortBy=submittedDate |
| 2026-10-19T06:25:47Z | 200 | 735bd0dca189e729... | arx4.xml | 1 | https://export.arxiv.org/api/query?search_query=all:%22Archimedean%22+AND+all:%22self-avoiding%22&max_results=100 |
| 2026-10-19T06:25:47Z | 200 | 008a0bdbb363165d... | arx5.xml | 5 | https://export.arxiv.org/api/query?search_query=all:%22bathroom+tile%22&max_results=100 |
| 2026-10-19T06:25:48Z | 200 | 01a248fcd9f6a16e... | oa_cert.json | 0 | https://api.openalex.org/works/W7171182314 |
| 2026-10-19T06:25:59Z | 200 | f25e7dc5d6310c8e... | jensen_cm0409381.pdf | - | https://arxiv.org/pdf/cond-mat/0409381v2 |
| 2026-10-19T06:26:00Z | 200 | 38bf4354ac1d72b8... | weighted_2508.01993.pdf | - | https://arxiv.org/pdf/2508.01993v3 |
| 2026-10-19T06:26:14Z | 200 | 425de947892450ad... | survey_1704.05884.pdf | - | https://arxiv.org/pdf/1704.05884v2 |
| 2026-10-19T06:26:15Z | 200 | 48c4c9d89ff352a2... | lectures_1206.2092.pdf | - | https://arxiv.org/pdf/1206.2092v1 |
| 2026-10-19T06:26:27Z | 200 | 7d1aa403ea9f54e9... | oa_thesis.json | 10 | https://api.openalex.org/works?search=Connective+properties+of+Archimedean+and+Laves+lattices&select=id,title,publication_year,doi,locations,open_access,authorships&per-page=10 |
| 2026-10-19T06:27:47Z | 302 | e3b0c44298fc1c14... | urn_thesis.html | - | http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-4251 |