# Input provenance
The 2218-word seed and unmodified search engine come from calgulbenkian's [PR #441](https://github.com/elder-plinius/V3R1T4S/pull/441), pinned to [commit `1d90d76f7c9ec29b50ba091078422b1c82008486`](https://github.com/elder-plinius/V3R1T4S/commit/1d90d76f7c9ec29b50ba091078422b1c82008486). They are referenced here rather than copied into this package.

| Rebuild input | Pinned source | SHA256 |
|---|---|---|
| `seed2218.txt` | [object/A35_6_6_2218.txt](https://github.com/elder-plinius/V3R1T4S/blob/1d90d76f7c9ec29b50ba091078422b1c82008486/known-knowns/constant-weight-codes/2026-10-18-calgulbenkian-dd2eb057/object/A35_6_6_2218.txt) | `dd2eb057e40bc19bbd7f6a2838681200d6d55b4018e9b01a62082c35822e413e` |
| `cwc_search.c` | [how-we-built-it/cwc_search.c](https://github.com/elder-plinius/V3R1T4S/blob/1d90d76f7c9ec29b50ba091078422b1c82008486/known-knowns/constant-weight-codes/2026-10-18-calgulbenkian-dd2eb057/how-we-built-it/cwc_search.c) | `42194bb9807d75c905eec217a883d668b4e84b023c258095db7bc1d72c0f7a41` |

PR #441 credits Argon, calgulbenkian's AI search agent, for the search engine. Our contribution is a fresh, fully specified search run initialized from their 2218 certificate, plus independently authored verification and exact small-exchange analysis. No claim of a new search algorithm. See [README.md](README.md) for download, hash-check and rebuild commands. The upstream source uses the repository AGPLv3 license, retained here as LICENSE.
