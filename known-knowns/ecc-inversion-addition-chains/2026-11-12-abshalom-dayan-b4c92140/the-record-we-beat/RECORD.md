# The records compared against (snapshots, not the pages)

One GET each per day, User-Agent v3r1t4s-run/1.0, no retries. Every URL was fetched on 2026-11-10 and again on 2026-11-12 with identical bytes.

## Brian Smith's page (the target's status source)
- URL: https://briansmith.org/ecc-inversion-addition-chains-01
- fetched (UTC): 2026-11-10T20:09:02Z and 2026-11-12T18:19:13Z
- HTTP status: 200
- sha256 of the page: 7b688992bf9bcea9a25f2e11369828037ad94d17315b08e2e749d2aabe1c9ca3
- extracted cell: "secp256k1 scalar inversion", 290 = 253 squarings + 37 multiplications. The page says it was last updated on 3 Sep 2017.

## addchain doc/results.md
- URL: https://raw.githubusercontent.com/mmcloughlin/addchain/master/doc/results.md
- fetched (UTC): 2026-11-10T20:09:02Z and 2026-11-12T18:20:02Z
- HTTP status: 200
- sha256 of the file: c805367ced12810d221ac3513ca3ccd0d329382dac2a8ec7b54f2f272e167357
- extracted cell: section "secp256k1 (Bitcoin) Scalar Inversion", Length 293, Best Known 290. The N-2 hexadecimal printed in that section is the exponent of this package.

## Shortest chain found published elsewhere (the bar): Brian Smith, 2026, on Neill Clift's page
- URL of the chain file: https://additionchains.com/secp256k1-scalar-inverse-example.txt
- listed on: https://additionchains.com/LargeChains.html, section "Scalar Inversions" (sha256 of the page: 55d0846dd1d95abaa647e37cca1d5abc2dd9dd7bb1b5bb6a764b0fcc22cad345)
- fetched (UTC): 2026-11-10T20:32:35Z and 2026-11-12T18:19:13Z
- HTTP status: 200; Last-Modified of the chain file: Mon, 02 Nov 2026 19:26:13 GMT
- sha256 of the chain file: ff57a8519d4fdc4ee5c154390d30ca83824c14cdfddb1907b9f736c30a050ccf
- extracted cell: "secp256k1 scalar inversion", length 282 = 251 doublings + 31 additions, credited "Brian Smith (2026)". The page says each downloadable example "has the lowest weighted cost among the supplied chains of the shortest supplied length for that curve". Replayed with verify-it-yourself/check_values.py: 283 values, every one after the first a sum of two earlier ones, the last is n-2.
- The page gives no reuse license for the file, so it is not copied here.

## TTaoGaming/addition-chain-search
- URL: https://raw.githubusercontent.com/TTaoGaming/addition-chain-search/main/review-candidates/certificates/secp256k1_288.json
- fetched (UTC): 2026-11-10T20:09:03Z and 2026-11-12T18:20:02Z
- HTTP status: 200
- sha256 of the file: 4f8fc44ad666a60717c4f9f0add36f7cc0156c3794dc76af66119054cef0f8f8
- extracted cell: a chain for the same exponent of length 288 = 253 doublings + 35 additions.

Lowest: 282. This package's chain has length 281.
