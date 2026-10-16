# The record we compared against (snapshot, not the page)

| source | URL | fetched (UTC) | HTTP | Last-Modified | sha256 |
|---|---|---|---|---|---|
| scu txt/radius.txt | https://packomania.com/scu/txt/radius.txt | 2026-10-15T18:38:02Z | 200 | Thu, 15 Oct 2026 12:05:12 GMT | 832c9563391ccaffd571066d407dcd92c95661e6802e1da291e4d9f2e2fd1ed8 |
| scu83.txt | https://packomania.com/scu/txt/scu{N}.txt | 2026-10-15T18:38:05Z | 200 | Tue, 28 Feb 2012 07:05:00 GMT | cc08dcaf1f88de0ff8107525047ffa110f0d39ef5aa06172c30b691809d41c62 |
| scu.html (History of updates) | https://packomania.com/scu/scu.html | 2026-10-15T18:38:04Z | 200 | Thu, 08 Oct 2026 07:42:29 GMT | 344927b84a7214c58f20f508646a93c6885e3c3e635abce1357413ffe4a35900 |
| author.txt | https://packomania.com/scu/txt/author.txt | 2026-10-15T18:38:03Z | 200 | Thu, 15 Oct 2026 12:05:12 GMT | fafdf2d15007d951b3f320dc5cf760b3efce98c9916ac630d437e97eb694ea75 |
| pending-requests.html | https://packomania.com/pending-requests.html | 2026-10-15T18:38:04Z | 200 | Thu, 08 Oct 2026 07:39:03 GMT | 0d6ebbbe8e95abe7e701e1c70fbc1c0ec5bb06d611822b0b135ce3b776972384 |

Extracted cell: radius.txt row `83  0.116285160418976515059766617287`; author.txt row `83 Francesco Bagattini, Fabio Schoen and Luca Tigli`.
- scu.html table row N = 83 shows 0.11628516041895784 (17 digits; differs from radius.txt by 1.9e-14, not material). Per-N page scu83.html footer 28-Feb-2012.
- History of updates (scu.html) newest entry 08-Oct-2026 (Lu Peng); no entry names N = 83 after the posted file's date.
- pending-requests.html (08-Oct-2026): no scu row; category-unspecified Moki & Julio bundle (26-Sep-2026) unresolved.
- scu83-posted.txt here is the single posted coordinate file for this N (as in the hsp4 packages), kept so the checker runs offline.
