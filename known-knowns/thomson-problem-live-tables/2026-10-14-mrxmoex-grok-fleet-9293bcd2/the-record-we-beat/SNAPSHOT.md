# The record we beat (snapshot, not the page)

Selected headers were not stored by our single honest fetch; recorded below: URL, UTC fetch time, HTTP status and the sha256 of the page bytes. The pages themselves are not included.

| source | URL | fetched (UTC) | HTTP | page sha256 | extracted cell, N = 743 |
|---|---|---|---|---|---|
| CCD Riesz s=1 | https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/site/s_1/index.html | 2026-10-14T14:23:31Z | 200 | eeac3235eeba4835d635c6f07f8be6bb54466c2425bceba65ced315460fa649d | 264837.5858504 (lowest live value, compared against) |
| CCD Thomson2 | https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson2/table.html | 2026-10-14T14:23:29Z | 200 | caf24199154912eb24d59a6ed6695a7a814ef94081e010390ffa5bd5d53d3794 | no row for N = 743 |
| Deeter | https://deetour.net/oppp/thomson/ | 2026-10-14T14:23:27Z | 200 | cf138c88fc00c5e0f2ef4dcec5fac4b18b1b7dd16f3c415c5dc088fde34ee647 | no row for N = 743 |
| CCD Thomson | https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/table.html | 2026-10-14T14:23:28Z | 200 | 5466173175b10a81d19e20763dffa64589f3ce5b92b09e827de14eb1fbb583e2 | no row for N = 743 |
| Wikipedia | https://en.wikipedia.org/wiki/Thomson_problem | 2026-10-14T14:23:32Z | 200 | 45b2be68631dafbfe27b89e013ece2c3c31c06e70376d73d6cbab57258bc5185 | no row for N = 743 |
| arXiv 2610.08122 (literature) | https://arxiv.org/html/2610.08122 | 2026-10-14T14:23:32Z | 200 | 24ff8b310f1a00c9d283f6fe2eb21426c3ef0bc6afbcd6af5f19201a38b1efbe | no row for N = 743 |

Posted point file polished for the distinct-basin test:

| file | URL | fetched (UTC) | HTTP | sha256 |
|---|---|---|---|---|
| points_743_1.dat | https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/site/s_1/dat/points_743_1.dat | 2026-10-14T07:47:13Z | 200 | 68ac9c8deba352959b12b63fa04ea87aef2cfbb502fe44123437f3e860b3df9a |

Live CCD Thomson / Thomson2 / Deeter point URLs for N = 743 returned 404 at gate time (2026-10-14T14:36Z). The novelty skeptic re-fetched every table independently at 2026-10-14T14:28Z (panel/novelty.md).
