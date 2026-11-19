# The record we compared against: OEIS A005164

Status source (bank target tsasm-a005164-order-51-exact): https://oeis.org/A005164

## Extracted cell
| quantity | OEIS A005164 (DATA and b-file) | this package |
|---|---|---|
| last published index | n = 24 | n = 25 |
| a(24) (order 49) | 52893528399758443649956432899616 | reproduced exactly |
| a(25) (order 51) | absent | 30533896243799704017627552102998416 |

Quoted from the record (text format, revision #41, Sep 21 2022): the last %U line ends
"...,125253905685915522767942493032,52893528399758443649956432899616"; the b-file's last line is
"24 52893528399758443649956432899616"; the draft page says "(No pending changes for A005164.)".

## Fetches (one GET each, curl or plain client, User-Agent "V3R1T4S-research-agent", no retries, no cookies)
| when (UTC) | by | URL | HTTP | sha256 of the bytes fetched |
|---|---|---|---|---|
| 2026-11-01T02:07:52Z | run scout | https://oeis.org/search?q=id:A005164&fmt=text | 200 | 3f428b9e0a360ea8683f27a6430a66ada6c9d3d9081fbeaa3f388d3010ae3e37 |
| 2026-11-01T02:09:05Z | run scout | https://oeis.org/A005164/b005164.txt | 200 | b93ec1418f1bf5b84892248ff52f3d4dc121c82f2ad0ad7ec90173fa43abccbf |
| 2026-11-01T02:09:05Z | run scout | https://oeis.org/draft/A005164 | 200 | 41cc9f68148785d3c6f3e23d6d3c956ee5f21d453f27f57a7c98fcff08c637c5 |
| 2026-11-01T03:00:03Z | novelty skeptic | https://oeis.org/A005164, b-file, draft page | 200 each | b-file identical to the scout's (prefix b93ec1418f1bf5b8) |
| 2026-11-01T03:03:53Z | criterion skeptic | https://oeis.org/search?q=id:A005164&fmt=text | 200 | 3f428b9e0a360ea8683f27a6430a66ada6c9d3d9081fbeaa3f388d3010ae3e37 |
| 2026-11-01T03:08:49Z | reproduce skeptic | text record, b-file, draft page | 200 each | text record and b-file identical to the scout's |
| 2026-11-01T03:09:51Z | honesty gate | https://oeis.org/search?q=id:A005164&fmt=text | 200 | 3f428b9e0a360ea8683f27a6430a66ada6c9d3d9081fbeaa3f388d3010ae3e37 |

## Selected response headers (honesty-gate fetch, 2026-11-01T03:09:51Z)
```
HTTP/2 200
date: Sun, 01 Nov 2026 03:09:51 GMT
content-type: text/plain; charset=utf-8
content-length: 2212
cache-control: private, no-store
cf-cache-status: DYNAMIC
server: cloudflare
```

The pages themselves are not included (third-party content). Anyone can re-fetch the URLs above.
