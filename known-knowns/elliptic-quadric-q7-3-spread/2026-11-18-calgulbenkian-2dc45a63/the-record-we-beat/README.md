# The record we beat (metadata only)

No third-party page is copied here. Each row records one honest GET (`curl -sS -L -A "V3R1T4S-scout/1.0"`, no retries) during live scouting.

| Source | URL | UTC fetch time | HTTP status | sha256 of the fetched page | Extracted status / value |
|---|---|---|---|---|---|
| Kiermaier, Schmidt, Wassermann (`arXiv:2403.11188` abstract page, primary `status_source`) | https://arxiv.org/abs/2403.11188 | 2026-11-18T03:58:25Z | 200 | `b54a2f4cdb2bf94340a65ae21570103810d15152ae5f8ad43a1874f54525a742` | Latest version `[v3] Wed, 1 Oct 2025 14:04:02 UTC` (*"Designs in finite classical polar spaces"*, *Designs, Codes and Cryptography* 2025) |
| Kiermaier, Schmidt, Wassermann (`arXiv:2403.11188` e-print source archive) | https://arxiv.org/e-print/2403.11188 | 2026-11-18T03:58:26Z | 200 | `c23156d51a467cbfdca14cbdc6682998f834338abea26874368bcdea39a657fa` | Sec. 6 (`designspolarspaces.tex`, lines 1065-1068): spread existence in $\Omega^-(8,3) = Q^-(7,3)$ is open; prior computer search restricted prime-power divisors of an automorphism order to $\{2, 3\}$ (neither order $2$ nor order $3$ excluded) |
| Kiermaier & Wassermann companion Zenodo dataset (`13353388`) | https://zenodo.org/api/records/13353388 | 2026-11-18T03:59:56Z | 200 | `401d34012ffc21fe63fc8e98030701175d05e1f7e7c84f13c66fae720e8986b5` | Contains strength-$2$ designs only (`q3_Q-_r3_k3.txt` has $\lambda \in \{2, 5\}$); zero spreads ($\lambda = 1$) |
| OpenAlex work metadata (`arXiv:2403.11188`) | https://api.openalex.org/works/https://doi.org/10.48550/arXiv.2403.11188 | 2026-11-18T03:59:57Z | 200 | `af7f1146c6545bbdaf57c7129f981f00a74e3aa72a2d9b9e95cf9a48425c5cbd` | `cited_by_count: 5` |
| OpenAlex citing works (`cites:W4402584757`) | https://api.openalex.org/works?filter=cites:W4402584757 | 2026-11-18T04:00:14Z | 200 | `3df0834c61096a9c0e5476c1006972afa957b9c1810e11b7f82a7388fc1c3ebc` | None of the 5 citing papers (2024-2026) resolve spreads of $Q^-(7,3)$ or exclude automorphisms of order $3$ or $2$ |
| Kiermaier & Klawuhn (`arXiv:2608.14437` abstract) | https://arxiv.org/abs/2608.14437 | 2026-11-18T03:59:34Z | 200 | `d9b72c45bca493e4678a948ecca02aa2a956b67690d1f14ee6313404c3a0b208` | Intersection numbers in regular semilattices; does not address spreads of $Q^-(7,3)$ |
| V3R1T4S pull requests (`state=all`) | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100 | 2026-11-18T03:58:27Z | 200 | `eadd7bee03a4cf8b7f47215c3ba7229c4e99a060a368faecf6ad2a63a63da856` | Zero open or closed PRs on `elliptic-quadric-q7-3-spread` |

*(Note: one GET to `https://api.semanticscholar.org/graph/v1/paper/ARXIV:2403.11188?...` at `2026-11-18T03:58:26Z` returned HTTP `429`, sha256 `65ab993d12c5c2cc9b68e6da2bb79b326930283e520363ffcdc145f88cd5a148`, and was not retried per Rule 5.)*

Compared prior restriction: Kiermaier, Schmidt, and Wassermann (`arXiv:2403.11188v3`, Sec. 6) proved that only the primes $2$ and $3$ can divide the order of an automorphism of a spread of $\Omega^-(8,3) = Q^-(7,3)$. This package proves that **no spread of $Q^-(7,3)$ admits an automorphism of order $3$** (partial win `p1`), and furthermore excludes all odd primes $\{5, 7, 13, 41\}$ and all involutions in $\mathrm{PO}^-(8,3)$ from first principles, proving $\mathrm{Aut}(\mathcal{S}) \cap \mathrm{PO}^-(8,3) = \{1\}$ and $|\mathrm{Aut}(\mathcal{S})| \in \{1, 2\}$.
