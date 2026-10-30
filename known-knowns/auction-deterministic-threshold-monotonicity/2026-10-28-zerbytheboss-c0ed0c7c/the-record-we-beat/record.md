# Record We Beat — `auction-deterministic-threshold-monotonicity`

target_id: auction-deterministic-threshold-monotonicity
table_url: https://arxiv.org/abs/2608.22371
fetch_time: 2026-10-28T22:17:25Z
http_status: 200
page_sha256: 2e5090ce7dc820acfcde224c0819b8299d2bc5c9da24733ed65d70c4b5d7a48e

## Published Incumbent Status
- Source: D. Thirumulanathan, "On Deterministic Optimal Mechanisms in a Two-Item Setting for Distributions with Nondecreasing Density", arXiv:2608.22371v1; Journal of Mathematical Economics, DOI 10.1016/j.jmateco.2026.103293.
- Section 3.1 Footnote: "Whether c*2 is an increasing function of c1 or not is still an open problem."
- Incumbent Knowledge: Only uniform distributions were known, where c2*(c) = 2*b2*b1^2/(b1-c)^2 strictly increases. Theorem 5 established asymptotic divergence c2*(c) -> infinity as c -> 1/g1(0), leaving monotonicity open.
- Resolution: We provide the first certified counterexample with an explicit admissible rational polynomial density pair (g1(x) = 7/57 + (350/57)x^6, g2(x) = 1 on [0, 1]) and rational shifts c_A = 11702081697/2754078775 < c_B = 939499441/214943135 where c2*(c_A) = 24.43151065 > 24.32958944 = c2*(c_B) strictly decreases by > 0.1019, refuting monotonicity.
