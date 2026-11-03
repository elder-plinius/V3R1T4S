# The record we beat (table snapshot; the page itself is not copied)
- table: OEIS A357271 instance file "Improved lower bounds for n=7, 9, 11, 13, 15" (Ong, Ang, Ho, Eilers, Marks, Buzi, 2025)
- URL: https://oeis.org/A357271/a357271_1.txt
- fetched (UTC): 2026-11-03T15:55:29Z, HTTP status 200, one plain request by the run's scout; headers not captured
- sha256 of the fetched file: 95735e185c5435e7cbe4c6753fe4e4ee120321457279f1f3283523654db5cd47
- extracted cell: "lb(9)=365 (previously 330)" (the order-9 example in that file has 365 stable matchings; re-counted here at 365)
- re-fetched independently by the panel's NOVELTY skeptic at 2026-11-03T17:35:48Z: HTTP 200, same sha256 95735e185c5435e7cbe4c6753fe4e4ee120321457279f1f3283523654db5cd47 (see panel/novelty.md)
- the entry itself: https://oeis.org/A357271 fetched 2026-11-03T15:55:29Z, HTTP 200, sha256 480198b2e16d793eccb540193ea392ed269fdc54dad65240908afb1a332f46b6 (HTML), data line a(9) = 330; internal text format https://oeis.org/search?q=id:A357271&fmt=text fetched by the panel at 2026-11-03T17:35:48Z, HTTP 200, sha256 fd27d7c9ede8781f1fac606a633c62938a7bda778fc04f8557f26278a7c95143
- other values at n = 9 checked: A069156 330 (https://oeis.org/search?q=id:A069156&fmt=text, 2026-11-03T15:59:20Z, HTTP 200, sha256 a0b564cfb51317f995f0719e2cbd6feb54bc76e38239c7b2d1427240220f8a61); A371810 288 (https://oeis.org/A371810, 2026-11-03T15:56:17Z, HTTP 200, sha256 14311061020c6c93b323dc81999f9d3dd1f8cf5ba43f17c5107429218fd551c5)
- composition closure: the best composition of published instances found by the panel was 378 (Z2^3 Latin order-8 block-summed with one pair, frozen blocks, hill-climbed cross placements); the claim's own probe found 366. These values come from search and are lower bounds, not a proven closure maximum.
