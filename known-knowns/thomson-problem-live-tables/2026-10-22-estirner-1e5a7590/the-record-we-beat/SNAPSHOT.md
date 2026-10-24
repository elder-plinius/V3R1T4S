# The record we beat (snapshot, not the pages)

One plain GET per URL (curl, User-Agent "V3R1T4S-research-run (curl)", no retries). Response headers were not stored;
recorded below are the URL, the UTC time just before the request, the HTTP status, the sha256 of the bytes received and
the extracted N = 743 cell. The pages themselves are not included.

| URL | fetched (UTC) | HTTP | sha256 | N = 743 |
|---|---|---|---|---|
| https://deetour.net/oppp/thomson/ | 2026-10-22T01:59:59Z | 200 | cf138c88fc00c5e0f2ef4dcec5fac4b18b1b7dd16f3c415c5dc088fde34ee647 | no row for N = 743 (N = 4..524) |
| https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/table.html | 2026-10-22T02:00:01Z | 200 | 5466173175b10a81d19e20763dffa64589f3ce5b92b09e827de14eb1fbb583e2 | no row for N = 743 |
| https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson2/table.html | 2026-10-22T02:00:04Z | 200 | caf24199154912eb24d59a6ed6695a7a814ef94081e010390ffa5bd5d53d3794 | no row for N = 743 |
| https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/site/index.html | 2026-10-22T02:00:04Z | 200 | b28eed78a616e8e688e7c01bd84b7a51445e638ad2e485ab1ee893a0fe2aa008 | index (53 configurations, 512 to 9913) |
| https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/site/s_1/index.html | 2026-10-22T02:00:05Z | 200 | eeac3235eeba4835d635c6f07f8be6bb54466c2425bceba65ced315460fa649d | 264837.5858504 (the only live N = 743 cell; compared against) |
| https://en.wikipedia.org/wiki/Thomson_problem | 2026-10-22T02:00:05Z | 200 | 39da937f6961c1ac4f1016c3602d40d2934239b27bc355ab4563d0315e95fa57 | no row for N = 743 (N <= 470) |
| https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/site/s_1/dat/points_743_1.dat | 2026-10-22T02:00:07Z | 200 | 68ac9c8deba352959b12b63fa04ea87aef2cfbb502fe44123437f3e860b3df9a | posted N = 743 configuration (polished for the distinct-basin test) |
| https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/xyz/743.xyz | 2026-10-22T02:06:16Z | 404 | 9646e03ab81f0d2ab39b0fd3afe6fa08869f2af98c40b03621f32f454fb3843e | 404: no posted CCD Thomson file |
| https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson2/xyz/743.xyz | 2026-10-22T02:06:17Z | 404 | 9646e03ab81f0d2ab39b0fd3afe6fa08869f2af98c40b03621f32f454fb3843e | 404: no posted Thomson2 file |

Other known N = 743 values (all above the object's energy 264837.4538033452076921018):

| source | value | where |
|---|---|---|
| merged V3R1T4S claim #125 (2026-10-15) | 264837.5287041150044362828 | known-knowns/thomson-problem-live-tables/2026-10-14-mrxmoex-grok-fleet-9293bcd2 |
| Amore and Wales 2026, Table 3 ("this work") | 264837.58585036 | https://arxiv.org/abs/2610.08122 |
| Roshal, Myasnikova and Rochal 2015 | 264837.700971304 | https://arxiv.org/abs/1408.3473 (Phys. Lett. A 379, 372) |

The NOVELTY skeptic re-fetched the status source and the Riesz s=1 page independently (panel/novelty.md).
