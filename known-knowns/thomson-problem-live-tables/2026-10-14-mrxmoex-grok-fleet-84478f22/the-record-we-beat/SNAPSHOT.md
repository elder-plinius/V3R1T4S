# The record we beat (snapshot, not the page)

Selected headers were not stored by our single honest fetch; recorded below: URL, UTC fetch time, HTTP status and the sha256 of the page bytes. The pages themselves are not included.

| source | URL | fetched (UTC) | HTTP | page sha256 | extracted cell, N = 1382 |
|---|---|---|---|---|---|
| CCD Riesz s=1 | https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/site/s_1/index.html | 2026-10-14T07:28:29Z | 200 | eeac3235eeba4835d635c6f07f8be6bb54466c2425bceba65ced315460fa649d | 926576.1030330 (lowest live value, compared against) |
| CCD Thomson2 | https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson2/table.html | 2026-10-14T07:28:28Z | 200 | caf24199154912eb24d59a6ed6695a7a814ef94081e010390ffa5bd5d53d3794 | 926576.1175606 |
| Deeter | https://deetour.net/oppp/thomson/ | 2026-10-14T07:28:26Z | 200 | cf138c88fc00c5e0f2ef4dcec5fac4b18b1b7dd16f3c415c5dc088fde34ee647 | no row (table ends at 524) |
| CCD Thomson | https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/table.html | 2026-10-14T07:28:26Z | 200 | 5466173175b10a81d19e20763dffa64589f3ce5b92b09e827de14eb1fbb583e2 | no row (table ends at 972) |
| Wikipedia | https://en.wikipedia.org/wiki/Thomson_problem | 2026-10-14T07:28:30Z | 200 | a279d4de9f41a56ffcb6966589156fa3692d409b3e0e674233ddd9444735ddd0 | no row (table ends at 470) |
| arXiv 2610.08122 (literature) | https://arxiv.org/html/2610.08122 | 2026-10-14T07:28:30Z | 200 | 24ff8b310f1a00c9d283f6fe2eb21426c3ef0bc6afbcd6af5f19201a38b1efbe | 926576.10303295 |

Posted point files polished for the distinct-basin test:

| file | URL | fetched (UTC) | HTTP | sha256 |
|---|---|---|---|---|
| points_1382_1.dat | https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/site/s_1/dat/points_1382_1.dat | 2026-10-14T07:21:25Z | 200 | dd3b546e7b4c35d6415d3a47d4d284968d0baa11e2ffd988547b7b7676aa71d9 |
| 1382.xyz | https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson2/xyz/1382.xyz | 2026-10-14T07:21:38Z | 200 | b94e354f956d7e095589dfd2c95a88eaf1189d08af55a2ce41347936cd99bf50 |

The novelty skeptic re-fetched every table independently at 2026-10-14T08:56Z and found the same N = 1382 cells (panel/novelty.md).
