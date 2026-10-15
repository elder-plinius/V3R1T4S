# The record we compare against

| page | UTC fetch time | HTTP | sha256 of the page as fetched |
|---|---|---|---|
| https://www.erdosproblems.com/699 | 2026-10-14T19:21:03Z (run scout) | 200 | 2c52b8bbd3319ac657e323156ed028d42ce7b9460c4d1fe88190d52b87f8d63c |
| https://www.erdosproblems.com/699 | 2026-10-15T00:13:42Z (NOVELTY skeptic) | 200 | 1882f3c2bf2174e76619073f6d5261f3f1508e3fcf2574e3e65ef02a6ae93c80 |
| https://www.erdosproblems.com/forum/thread/699 | 2026-10-14T16:17:01Z (earlier scout) | 200 | 0c17761aa2fe6f16ac6acb4cf94d6675e68e0f22ada38ed6845ed4749bebd545 |
| https://www.erdosproblems.com/forum/thread/699 | 2026-10-15T00:13:42Z (NOVELTY skeptic) | 200 | f33bfbe5a9b63148fe2c32e6f1c46d8732be3066a152f223771ef8346bd6e83f |

Each was one plain request with User-Agent "V3R1T4S", no retries. Selected response headers were not recorded.

Extracted cell: the status page poses #699 as open (proved for j <= 3i/2 or n = 2j). The largest exhaustive
computation on the forum thread is Cong's comment of 06 Jan 2026: "I ran a Rust implementation to test the official
statement ... up to n = 10^7; no counterexamples found. Targeted extensions: all n = 2^k for k ≤ 27 (n ≈ 1.34×10^8)
and all n = 3^m + 1 for m ≤ 17 (n ≈ 1.29×10^8)."
Not reached: Cong's repository https://github.com/conglu1997/erdos_699_rust (HTTP 403 from the sandbox proxy).
