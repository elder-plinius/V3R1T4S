# The record we compared against: Gallian, A Dynamic Survey of Graph Labeling (DS6), Table 2 and Section 2.4

Status source (bank target windmill-kn2-harmonious-graham-sloane): https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS6
PDF linked from it: https://www.combinatorics.org/ojs/index.php/eljc/article/download/DS6/pdf/

## Extracted cell
| quantity | DS6 value (28th edition, "DS6: Oct 30, 2025") | this package |
|---|---|---|
| is the windmill K_8^(2) harmonious? | open: the K_n^(2) conjecture is listed as "H?"; only n odd, n = 4 and n = 6 are settled | not harmonious (exhaustive search) |

Table 2 (harmonious labelings), row "windmills K_n^(m) (n > 3) (see §2.4)", as extracted from the PDF:
"H if n = 4 [1376]" / "m = 2, H? iff n = 4 [1249]" / "not H if m = 2, n odd or 6 [1249]" / "not H for some cases m = 3 [2153]".

Section 2.4 (p. 25): "Graham and Sloane [1249] conjectured that K_n^(2) is harmonious if and only if n = 4. They
verified this conjecture for the cases that n is odd or n = 6. Liu [2153] has shown that K_n^(2) is not harmonious if
n = 2^a p_1^a_1 ... p_s^a_s where a, a_1, ..., a_s are positive integers and p_1, ..., p_s are distinct odd primes and
there is a j for which p_j ≡ 3 (mod 4) and a_j is odd." For n = 8 = 2^3 there is no odd prime factor, so Liu's
condition does not apply. Levine (1983) requires n to be a sum of two squares, and 8 = 2^2 + 2^2.

Graham and Sloane (1980), Theorem 20 (p. 398): "K_n^(2) is harmonious if n = 4 but is not harmonious if n is odd or
n = 6." ... "The computer eliminated n = 6."

## Fetches (one GET each, plain curl, User-Agent "V3R1T4S-research-agent (honest client)", no cookies, no retries)
| when (UTC) | by | URL | HTTP | bytes | sha256 of the bytes received |
|---|---|---|---|---|---|
| 2026-11-01T23:43:30Z | run scout | DS6 article page | 200 | | b36c78828cb24f424aa7a2c476f723f4294df6ba8254abdb6a35a54308fc1a00 |
| 2026-11-01T23:43:31Z | run scout | DS6 PDF | 200 | | b1b5d8ba828b3fcd7eb4d73402b63252bd06b59bdcfb4f32f558f8af5898842e |
| 2026-11-01T23:44:38Z | run scout | https://fanchung.ucsd.edu/ron/papers/80_07_harmonious.pdf | 200 | | 109e4ea21bb10a1a1b89c12e8b0df46ac2c496846c3ed0ae64edb3385263afe6 |
| 2026-11-02T00:22:54Z | novelty skeptic (panel) | DS6 article page | 200 | 18415 | 68a1f0a879c8b46b7ac04137674be7a412cd6dc441a83a280a00037ec84c8703 |
| 2026-11-02T00:22:55Z | novelty skeptic (panel) | DS6 PDF | 200 | 3945134 | b1b5d8ba828b3fcd7eb4d73402b63252bd06b59bdcfb4f32f558f8af5898842e |
| 2026-11-02T00:22:59Z | novelty skeptic (panel) | Graham-Sloane 1980 PDF | 200 | 1155753 | 109e4ea21bb10a1a1b89c12e8b0df46ac2c496846c3ed0ae64edb3385263afe6 |
| 2026-11-02T00:26:45Z | packaging re-check | DS6 article page | 200 | 18415 | 68013a414aef2c0f34005d987864b2cbd91248f9652224f2fe9f5509bb42d7b1 |
| 2026-11-02T00:26:46Z | packaging re-check | DS6 PDF | 200 | 3945134 | b1b5d8ba828b3fcd7eb4d73402b63252bd06b59bdcfb4f32f558f8af5898842e |

The article-page copies differ by fetch (dynamic OJS page). All of them read "DS6: Oct 30, 2025". The PDF hash is
the same at all three fetches, so the survey did not change between the scout, the panel and packaging.

Selected response headers of the packaging-time fetches:

    HTTP/1.1 200 OK
    Date: Mon, 02 Nov 2026 00:26:46 GMT
    Server: Apache
    Cache-Control: no-store
    Content-Type: text/html; charset=utf-8

    HTTP/1.1 200 OK
    Date: Mon, 02 Nov 2026 00:26:47 GMT
    Server: Apache
    Content-Length: 3945134
    Cache-Control: private
    Content-Type: application/pdf

The pages and PDFs are not included (third-party content). Anyone can re-fetch the URLs above.
