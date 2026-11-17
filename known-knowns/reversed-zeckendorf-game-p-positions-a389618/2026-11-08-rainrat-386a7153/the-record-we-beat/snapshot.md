# The Record We Beat — Snapshot Metadata (`reversed-zeckendorf-game-p-positions-a389618`)

Per repository policy (`kit/POLICY.md`), raw third-party web pages are not redistributed in this package; below are the exact URLs, UTC request/response timestamps, HTTP status codes, selected response headers, SHA-256 hashes of the fetched response bodies, and the extracted published frontier values.

## 1. OEIS Primary Status and Sequence Files

| Source URL | Request Start UTC | HTTP Status & Selected Response Headers | SHA-256 of Fetched Body | Published Frontier |
|---|---|---|---|---|
| `https://oeis.org/A389618` | `2026-11-08T01:14:31Z` | `HTTP/2 200`, `date: Sun, 08 Nov 2026 01:14:31 GMT`, `content-type: text/html; charset=utf-8`, `last-modified: Sun, 14 Dec 2025 18:15:56 GMT`, `server: cloudflare` | `f939a8eadbae5e50daec69187e8a51314689260214ccdc6406c50f0e47398515` | Player-2 winning starting numbers ($P$-positions) for $n \le 129$ (`a(1)=3` through `a(49)=129`) |
| `https://oeis.org/A389618/b389618.txt` | `2026-11-08T01:15:19Z` | `HTTP/2 200` (plain-text b-file, 344 bytes) | `888ff71b7705af8e5894e47ca06460c2253b75a84670a7e789e352b3d46f0b85` | 49 terms: `1 3`, `2 5`, ..., `48 128`, `49 129` |
| `https://oeis.org/A389617` | `2026-11-08T01:14:31Z` | `HTTP/2 200`, `date: Sun, 08 Nov 2026 01:14:31 GMT`, `content-type: text/html; charset=utf-8`, `last-modified: Sun, 14 Dec 2025 05:50:31 GMT`, `server: cloudflare` | `8b4cc38591080d2d251489f39a8225e14565162bfe1a39184981523d073da2ed` | Number of directed edges in the Reversed Zeckendorf Game DAG for $2 \le n \le 65$ |
| `https://oeis.org/A389617/b389617.txt` | `2026-11-08T01:15:19Z` | `HTTP/2 200` (plain-text b-file, 538 bytes) | `379cfc0a8465153f52bf3f677e48a91189008d8027bb1bd56e9168d1609e70f1` | 64 terms: `2 1`, `3 2`, ..., `64 63222`, `65 68351` |
| `https://oeis.org/A389619` | `2026-11-08T01:14:31Z` | `HTTP/2 200`, `date: Sun, 08 Nov 2026 01:14:32 GMT`, `content-type: text/html; charset=utf-8`, `last-modified: Sun, 14 Dec 2025 18:19:00 GMT`, `server: cloudflare` | `8f354c8cf74f3dc5c349310b746e093c9514041ca1ca30a3f7cac4e02f6e6ed4` | Player-1 winning starting numbers ($N$-positions) for $n \le 127$ (plus $a(1)=1$ by OEIS convention) |
| `https://oeis.org/A389619/b389619.txt` | `2026-11-08T01:15:19Z` | `HTTP/2 200` (plain-text b-file, 535 bytes) | `2500c5d5cab045f7d62f99977d2140dcd4525c8a9c5183c89b68efdc86a70868` | 80 terms: `1 1`, `2 2`, `3 4`, ..., `79 126`, `80 127` (79 terms with $n \ge 2$) |

## 2. Primary Literature Source (`arXiv:2309.12748v2`)

- **Citation**: Zoë X. Batterman, Aditya Jambhale, Steven J. Miller, Akash L. Narayanan, Kishan Sharma, Andrew K. Yang, and Chris Yao (2025), *"The Reversed Zeckendorf Game"*, *The Fibonacci Quarterly* 63(2):215–239 (`https://www.tandfonline.com/doi/abs/10.1080/00150517.2024.2417193`); preprint `https://arxiv.org/abs/2309.12748` (`arXiv:2309.12748v2`).
- **Abstract page (`https://arxiv.org/abs/2309.12748`)**:
  - Request start UTC: `2026-11-08T01:14:31Z`
  - Selected response headers: `HTTP/2 200`, `date: Sun, 08 Nov 2026 01:14:32 GMT`, `last-modified: Mon, 24 Aug 2026 19:27:38 GMT`, `content-type: text/html; charset=utf-8`, `content-length: 40862`, `server: Google Frontend`
  - SHA-256: `7ff488d36fec55eb85b1e69ae38e2b2dd833e5f42b6cef226e0ea1e50c3dc4bb`
- **LaTeX source archive (`https://arxiv.org/e-print/2309.12748`)**:
  - Request start UTC: `2026-11-08T01:14:43Z`
  - Selected response headers: `HTTP/2 301` (`date: Sun, 08 Nov 2026 01:14:44 GMT`, `location: /src/2309.12748`) $\to$ `HTTP/2 200` (`date: Sun, 08 Nov 2026 01:14:45 GMT`, `last-modified: Sat, 17 Oct 2026 21:30:46 GMT`, `content-disposition: attachment; filename="arXiv-2309.12748v2.tar.gz"`, `etag: COLhq8mf4IEDEAM=`, `content-type: application/gzip`, `content-length: 37846`)
  - SHA-256: `72221859a338c3e5a996c7e04d57c0787b22adfa85f8bd6d4bf12ac412644208` (`draftPaperV2.tex`)
- **Published Frontier in Table A1 (`draftPaperV2.tex`, lines 610–897)**:
  - Tabulates `(n, Winner, Number of Edges, Number of Vertices)` for $2 \le n \le 129$ (`n = 129` at line 897: `Winner = 2` via `\cellcolor{gray!25}`, `Edges = 2,945,040`, `Vertices = 384,715`; extracted ground truth SHA-256 `cea0c77942d3e7c3cc127fb8370da12d4075cc8a6b3dedc71a5ad297ee8361f6`).
  - Appendix B notes that the authors' tree/DAG exploration code required ~24 hours at $n = 144$ without reporting the winner, edge count, or vertex count for any $n \ge 130$.
