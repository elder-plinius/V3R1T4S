# Novelty verdict: CW(208,81)

context: hermes delegation

Claim under review: claim/CLAIM.md. Nonexistence of CW(208,81), repository key CW(208,9). Not an existence claim.

## Live table

Fetched once, User-Agent V3R1T4S, no retry.

- URL: https://raw.githubusercontent.com/dmgordo/circulant-weighing-matrices/main/cwm.json
- HTTP status: 200
- UTC time (`date -u`): Fri Nov 13 07:36:30 AM UTC 2026
- sha256: d86aab619852a6e77a1aa3304dcb7e18f6f192b25caa80cdb470dc081815602d
- Key CW(208,9), the repository name for CW(208,81): status string "Open", comment "" (empty).

Parsed object: {"status":"Open","comment":""}. Status was readable. Not a blocked fetch.

## Literature

Tan, arXiv:2608.18468v2, Theorem 1.1, as read from the PDF: none of CW(105,36), CW(140,36), CW(116,49), CW(120,49), CW(192,49), CW(140,64), CW(180,64), CW(196,64) exists. Eight other orders. The PDF text has no occurrence of 208 and no weight-81 case. This cell is not among them.

Arasu-Gordon-Zhang, arXiv:1908.08447v3 (Cryptogr. Commun. 13 (2021), 775-789): weight-81 nonexistence is for orders 110, 130, 143, 154, 132, and computer elimination of 104 and 160. Table 10 is remaining open cases with n at most 200. The PDF text has no occurrence of 208. Their beyond-the-table remarks do not name this cell as settled.

Arasu-Bayes-Nabavi, Transactions on Combinatorics 4 (2015), 43-52: nonexistence of CW(88,81) and CW(99,81). The theorem-4.3 table names CW(207,81), not CW(208,81). The PDF text has no occurrence of 208.

arXiv and open-web searches for CW(208,81), CW(208,9), and circulant weighing matrix order 208 weight 81 returned no paper that proves existence or nonexistence of this exact cell. Neighboring orders (104, 156, 160, 184, 195, 198, 207) are different cells. A tie is not a record; no such paper was found.

The only divisor of 208 that is at least 81, other than 208 itself, is 104. Live key CW(104,9) is status "No", so a multiple of a smaller weight-81 matrix does not already give this cell. That nonexistence does not by itself settle order 208.

## Decision

Live file still says Open for CW(208,9). No paper found that already proves existence or nonexistence of CW(208,81).

novelty: open and unsettled
pass: true
