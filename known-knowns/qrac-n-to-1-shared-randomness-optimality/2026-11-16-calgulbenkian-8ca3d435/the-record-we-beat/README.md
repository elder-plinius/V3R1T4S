# Status Snapshot: qrac-n-to-1-shared-randomness-optimality

## Primary Status Source

- **Source**: Xinyu Tan and Syed A. Jafar, *Exact Optimality of `(n, n-1)` and `(n, n-2)` Quantum Random Access Codes*, `arXiv:2607.10414` (`v3`, revised `Fri, 23 Oct 2026 02:43:17 UTC`)
- **URL**: `https://arxiv.org/abs/2607.10414`
- **Fetched UTC**: `2026-11-15T14:07:10Z`
- **HTTP status**: `200`
- **Selected HTTP headers**:
  - `content-type: text/html; charset=utf-8`
  - `last-modified: Mon, 26 Oct 2026 00:25:35 GMT`
  - `date: Sun, 15 Nov 2026 14:07:10 GMT`
  - `content-length: 40825`
- **Page SHA-256**: `d142a0b561942b6b537a178198fff607e0fece61e29900487dbcb91102e9756f`
- **Full v3 HTML URL**: `https://arxiv.org/html/2607.10414v3` (`HTTP 200`, fetched `2026-11-15T14:08:04Z`, `sha256: 975fd184642ab7db6794bffb0644d22e830f61b69addc92ad87f0727032243a5`)
- **Extracted status cell**: For `(n, m) = (4, 1)` (4-to-1 binary QRAC over a single qubit, whose optimal average success probability equals the optimal worst-case success probability with shared randomness by Yao's minimax principle / `arXiv:0810.2937` Lemma 2), exact optimality remained **open** as of `23 Oct 2026`: Section 1.1 records that prior exact values were known only for `(n, m) in {(2,1), (3,1), (3,2), (4,2), (6,2)}` and proves `(n, n-1)` and `(n, n-2)`, leaving `(4, 1)` open between the Ambainis et al. lower bound `1/2 + (1 + sqrt(3)) / (8 * sqrt(2)) = 0.741481456572267...` and the analytical upper bound `1/2 + 1/(2*sqrt(4)) = 0.75`.

## Original Problem Source and Additional Literature Snapshots

| Source | URL | UTC fetch time | HTTP status | Page SHA-256 | Extracted cell / status |
|---|---|---|---|---|---|
| Ambainis, Leung, Mancinska, Ozols (`arXiv:0810.2937`) | `https://arxiv.org/abs/0810.2937` | `2026-11-15T14:07:10Z` | `200` | `b8615ffdf1dd4f9a425f1e2dfec3af45eff7ea5dc2876bc389ba1a175b4cccda` | Constructs `n = 4` protocol achieving `1/2 + (1 + sqrt(3)) / (8 * sqrt(2)) = 0.741481...` (Table 2); global optimality for `n >= 4` open |
| Mancinska and Storgaard (`arXiv:2106.00155`) | `https://arxiv.org/abs/2106.00155` | `2026-11-15T14:07:10Z` | `200` | `ab32f29af033427e16506f47910874bf35c13c297edfff90e959dac26f5a10ae` | Studies QRACs without shared randomness for `n >= 4`; `(4, 1)` with shared randomness remains open |
| Kondo et al. (`arXiv:2604.21274`) | `https://arxiv.org/abs/2604.21274` | `2026-11-15T14:09:22Z` | `200` | `c55459b01fc8634846d63bbfcc9c48192cf1b6b29f5d9daf42c12bddfaafda0c` | Studies high-dimensional `(n, n-1)` QRACs; does not treat `(4, 1)` qubit optimality |
| Akibue et al. (`arXiv:2606.12700`) | `https://arxiv.org/abs/2606.12700` | `2026-11-15T14:10:05Z` | `200` | `ac187ba333c15dbb17421e3450078f8f67cebd93afe03ae338841236d5967e23` | Studies `n -> infinity` asymptotic limits; does not prove finite `n = 4` optimality |
