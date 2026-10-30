# Record We Beat — `bilateral-trade-best-offer-vs-second-best`

target_id: bilateral-trade-best-offer-vs-second-best
table_url: https://export.arxiv.org/api/query?search_query=abs:%22bilateral%20trade%22&sortBy=submittedDate&sortOrder=descending&max_results=50
fetch_time: 2026-10-28T22:15:43Z
http_status: 200
page_sha256: eec60e09ebe2aba12bedebe131ee8f9a925ce540c6156ab7e256490eada7047f

## Published Incumbent Status
- Literature Benchmark: M. Babaioff, S. Dobzinski, and N. Kupfer, "The Best-of-Both-Worlds in Bilateral Trade", arXiv:2111.07790 Section 3; FOCS 2021.
- Stated Record / Open Problem: BDK gave a 2x2 instance demonstrating a limiting ratio of 3/4 between best-of (max(SO, BO)) and second-best (SB), but that ratio crucially relied on adversarial tie-breaking (under favourable ties, the ratio is 1).
- Prior Universal Bounds: Brustle, Cai, Wu, and Zhao (2017) proved a universal lower bound of 1/2. Whether there exists any bilateral trade instance where max(SO, BO) / SB < 3/4 under GFT-favourable tie-breaking was an open question.
- Resolution: We construct an explicit finite-support bilateral trade instance (|S|=4, |B|=4) with rational probabilities and posted price mechanism M=8 certifying max(GFT_SO, GFT_BO) / GFT_M = 19080/26767 approx 0.712818 strictly below 3/4 under GFT-favourable tie-breaking with strictly unique optimal offers for every seller and buyer type.
