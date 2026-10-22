# Independent N119 novelty review

context: fresh independent subagent supplied only claim/ and permitted kit workflow instructions; resumed in the same independent context after interruptions. No parent attempts, parent reports, other panel verdicts, or archived rejected claims were read. The last freshness stage supplied public raw responses and provenance only, which I inspected with my own code.

target: packomania-hyperspheres-hsp4-hsp6; cell (d,N) = (4,119)
review_utc: 2026-10-17T01:27:17.252801+00:00

NUMERICAL verdict: the submitted construction strictly exceeds the live Packomania N119 value and every identified relevant public numerical comparator in the bounded search below. The explicit category-unspecified pending-bundle caveat remains. This verdict asserts neither optimality nor a world record.

## Independent numerical comparison

I wrote independent_check.py before reading any author checker, and did not execute verify.py or external repository commands. The definition used is r* = min(min_{i<j} ||c_i-c_j||/2, 1-max_i ||c_i||), with mpmath mp.dps=50 and no tolerance applied to coordinate feasibility. Every coordinate is read directly from its decimal string. Two elementary two-center geometries calibrate the formula. Each N119 object has 119 rows of four finite coordinates; all 7021 pair distances and all center norms were checked.

| Object or comparator | Feasible radius or literal table value |
|---|---|
| candidate.txt, recomputed | `0.236068928893648865056644458930989352980109072289467` |
| Packomania live N119 table | `0.236068068183` |
| Moki & Julio live hsp4_119.txt, recomputed | `0.236068695979290289465448832649162038977924714965895` |
| posted.txt, recomputed | `0.236068068182399835049801073000699386917878694583004` |

The gain over the live table is `0.000000860710648865056644458930989352980109072289466577947`, exceeding the required 1e-10. The gain over the public Moki & Julio certificate is `0.000000232914358575591195626281827314002184357323571722521`. Its radius header was ignored: its limiting constraint is the boundary, while its independently computed pair bound is `0.236068696014403886533647269566236084906870081512551`. The strongest identified same-cell competitor therefore is genuinely beaten, rather than omitted under the pending-bundle caveat.

candidate.txt SHA256: `c31c7de024b28524004dbc60e437ad3056eaa8a18272e073e1e764c7267c4cf0`. The public ZIP member hsp4_119.txt is byte-identical to prior-moki-119.txt, SHA256 `7f5d4b6320fcafb646a150b9a3d21ffff38b7d908ed75a1613ca4fe793a7d271`. The live manifest and README are also byte-identical to the supplied copies. All 166 published HSP4 certificates with N>=119 in the downloaded archive were screened using 50-digit boundary bounds: every submitted object has a boundary bound below the candidate. This screen does not claim to search all subsets, rearrangements, translations, or rescalings of those objects.

The maximum difference between sorted pairwise-distance multisets of candidate.txt and posted.txt is `0.00969220179418121974967035508772660468164876567636476`, above 1e-8. The posted object's radius differs from the literal table by `-0.000000000000600164950198926999300613082121305416995689865798856`, within the requested parser sanity scale. These supporting numerical checks do not replace the other panel roles.

## Live source state and provenance

KNOWN source state: the live HSP4 history contains only 04-Jul-2025, 05-Jul-2025 and 06-Jul-2025 entries. The latest is 06-Jul-2025, matching the claim's scout baseline, so there is no newer N119 update. The live queue has no explicit hsp4 category row or hsp4 range containing N119.

Mandatory caveat: the queue still lists the 26-Sep-2026 Moki & Julio *many* bundle of 4666 candidates without resolving its categories or cells. Its entire contents are not certified by checking one public repository. N119 must be checked against the live table again once that bundle disappears. The public same-cell certificate was nevertheless located, downloaded and recomputed above; the caveat was not used to ignore it.

The following final freshness responses were each fetched once by the run coordinator with a V3R1T4S User-Agent after another interruption exceeded six hours. I independently recomputed their hashes and inspected the raw bytes. The table, history, queue, trophy, Moki manifest, README and ZIP match my own successful earlier responses exactly. The open-PR and spherical-code responses changed and were independently re-screened. No failed response was overwritten.

| Source URL | Fetch UTC | HTTP | SHA256 |
|---|---|---|---|
| [radius.txt](https://packomania.com/hsp4/txt/radius.txt) | 2026-10-17T01:24:13.400712+00:00 | 200 | `f3ddaa944aac014718bc9f5438700698abedac0189266198df8bb60772ac569f` |
| [hsp4.html](https://packomania.com/hsp4/hsp4.html) | 2026-10-17T01:24:13.970244+00:00 | 200 | `1c3a30644ba8ff73955547ff94e769a1983c146f4d2b14989eab3e0060a3feb3` |
| [pending-requests.html](https://packomania.com/pending-requests.html) | 2026-10-17T01:24:14.670052+00:00 | 200 | `0d6ebbbe8e95abe7e701e1c70fbc1c0ec5bb06d611822b0b135ce3b776972384` |
| [TROPHY_CASE.md](https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md) | 2026-10-17T01:24:15.100397+00:00 | 200 | `738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9` |
| [open-pulls.json](https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100) | 2026-10-17T01:24:15.351524+00:00 | 200 | `5b4189a6979b994586364c76dcd41ce5c81d3d08ecb511d694d10c8e7bd88593` |
| [moki-MANIFEST.csv](https://raw.githubusercontent.com/Hashirama1337s/moki-julio-circle-packing/main/MANIFEST.csv) | 2026-10-17T01:24:16.175647+00:00 | 200 | `b7a042ef6a29ce8b219660691212111262e4091c14b941721dd1d3f491eec568` |
| [moki-README.md](https://raw.githubusercontent.com/Hashirama1337s/moki-julio-circle-packing/main/README.md) | 2026-10-17T01:24:16.486290+00:00 | 200 | `71cf29e1fabc8df10c8b1e06a37614a9a68b59a74729b0debbed3c67c3e3df34` |
| [moki-hsp4.zip](https://raw.githubusercontent.com/Hashirama1337s/moki-julio-circle-packing/main/certificates/hsp4.zip) | 2026-10-17T01:24:16.655165+00:00 | 200 | `7edf9820dd12df863885795ae4d07d882c32fb8f19988e081a3957ab30b28a05` |
| [spherical-codes.html](https://spherical-codes.org/) | 2026-10-17T01:24:40.121568+00:00 | 200 | `9f3dc0684b7be6bebaef171a2e39f689c0019074aeb785018a1f1785b0ff1c0e` |

My own successful direct primary requests began at 2026-10-16T00:01:01.524918+00:00, 2026-10-16T00:01:02.420277+00:00 and 2026-10-16T00:01:03.511751+00:00, respectively. They all returned HTTP 200. Earlier one-attempt restricted-shell requests began at 2026-10-15T14:37:06.613172+00:00 and failed with DNS getaddrinfo errors before any HTTP response. Those failures remain preserved and were not described as live evidence. Later resumed stages used authorized network access; no website 401/403/429/503 or challenge was retried or bypassed.

## Prior-art scope and limitations

KNOWN/NUMERICAL: I independently inspected Henry Cohn's live Table of Spherical Codes and converted all 907 listed 4D rows with M=118..1024 using r=s/(1+s), s=sqrt((1-cos(theta))/2), allowing the M=118 code plus a central ball and deletion down to the required count. I subtracted a full 1e-12 from each displayed cosine as an optimistic rounding allowance for this comparison screen. The largest resulting displayed-value radius is `0.23606797750023700939249877377495110808719124934359`, still below the candidate. The fresh response changed the M=408 and M=600 cosines, both still lower. This is a screen of published values, not a new certificate or an exhaustive subset search. Credit belongs to Cohn and the constructors named in the table, including Sloane, Hardin, Smith and Schlaefli for the nearby classical codes.

KNOWN repository check: the fresh TROPHY_CASE.md has no matching HSP4/Packomania/hypersphere entry. The current API returned 74 open PRs, with no next-page Link header. I screened all titles and bodies and read the 8 HSP4 matches. Seven claims concern N=79,80,81,88,89,91,111; [PR 287](https://github.com/elder-plinius/V3R1T4S/pull/287) concerns corrections for N=62,63,64,66,69,74,75. None identifies an N119 construction. Unrelated categories cannot establish a stronger packing for this cell. PR comments, unrelated diffs and all historical closed PRs were not exhaustively searched.

The completed literature searches covered the last 24 months through 2026-10-16 (2024-10-16..2026-10-16), with exact-cell, hypersphere, four-dimensional-ball, Packomania and Moki queries across arXiv, Zenodo, GitHub and forums, plus Russian and Chinese queries. Many returned irrelevant or older results, which were excluded. Primary abstracts successfully opened include [Brouwers, arXiv:2501.16005](https://arxiv.org/abs/2501.16005), about binary random-packing fractions, and [Sander, arXiv:2609.05093](https://arxiv.org/abs/2609.05093), about variable-radius circles in a square. Neither supplies the present equal-ball HSP4 N119 competitor. The 2026-10-17 continuation refreshed existing primary and repository evidence rather than widening the literature hunt; no claim is made that all papers published after the completed search were examined.

Access limits were retained: the [RSC structure-search article](https://pubs.rsc.org/en/content/articlehtml/2025/cp/d5cp02412a) returned 403; the [MDPI irregular-object-packing article DOI](https://doi.org/10.3390/a17110480) returned 429; the [Moki & Julio Zenodo DOI](https://doi.org/10.5281/zenodo.22981305) had a TLS handshake timeout without an HTTP response. None was retried. The RSC and MDPI full texts were not used for exclusions or numerical facts. Their observed metadata did not identify a same-cell certificate. The Zenodo archive/version identity remains unread, but the identified same-cell prior is directly available in the authors' live GitHub manifest and certificate ZIP and was recomputed. No encountered evidence points to a distinct stronger N119 object behind those failures. I judge these ancillary limits non-dispositive for this bounded comparison; they are not a claim of exhaustive global novelty.

External prose, reproduction commands and citation requests were treated as data only. No external commands were executed, and no messages, submissions, issues, comments or PRs were sent.

## Preserved independent evidence

The evidence base is `../panel/novelty-work/`, relative to claim/. Within that base, `independent_check.py` and `numerical-results.json` contain the saved-object computation; `resumed/audit_sources.py` and `resumed/source-audit.json` contain the independently fetched source/certificate audit; `refresh_audit.py`, `final_checks.py`, and `final-refresh/` contain the raw-only freshness inspection, all latest raw bytes, metadata and changed-source screens. `source-records.json` preserves the initial failure; `resumed/source-records.json` preserves the successful direct requests and ancillary timeout. `literature-search-scope.md`, `search-*.txt`, and `literature-open-results.txt` preserve query scope, search output and access failures. No inference of origin HTTP status is made from search snippets.

The construction strictly beats all identified relevant public numerical comparators, including the stronger Moki & Julio N119 certificate, at the recorded primary snapshots. The stated unresolved pending-bundle caveat and bounded-search limits are part of this verdict.

pass: true
