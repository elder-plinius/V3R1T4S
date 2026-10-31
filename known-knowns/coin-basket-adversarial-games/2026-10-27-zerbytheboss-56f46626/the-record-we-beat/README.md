# The Record We Beat — `coin-basket-adversarial-games`

## Status Sources
1. **OEIS A392305**:
   - URL: `https://oeis.org/A392305`
   - Entry Name: "Fill your basket: fair compensation paid to presenter under optimal play"
   - Author: Ruediger Jehn
   - Fetched: 2026-10-28T00:31:14Z (HTTP 200, SHA-256 `ca6b94758a63e1b792855461b24cbc261a930f23b039cdcc1a1b8c3eb5d781ee`)
   - Previous record: Published through $n = 16$ only ($1, 1, 1, 2, 3, 3, 3, 3, 3, 4, 4, 5, 5, 5, 6, 6$). All values for $n \ge 17$ were completely open.

2. **OEIS A391538**:
   - URL: `https://oeis.org/A391538`
   - Entry Name: "Game of Chests: sum the player can guarantee taking the largest of 3 baskets"
   - Author: Ruediger Jehn
   - Fetched: 2026-10-28T00:31:14Z (HTTP 200, SHA-256 `9d84f8723dd470e74956d48af05dbfec0a8d25470bb3eb6a919da8cedb94a7cf`)
   - Previous record: Published through $n = 14$ ($1, 2, 3, 5, 8, 11, 14, 17, 21, 25, 29, 34, 39, 44$). The conjectured formula $a(n) = \lfloor n(n-1)/6 \rfloor + n$ for $n > 4$ was unproved and unverified for $n \ge 15$.

## New Frontier Established
- $A392305$: New terms $a(17) = 7, a(18) = 7, a(19) = 8, a(20) = 8$ computed and verified with two-sided decision-bracket certificates, reproducing $n=1..16$.
- $A391538$: New terms $a(15..21) = 50, 56, 62, 69, 76, 83, 91$ evaluated and proven to match the conjectured formula, reproducing $n=1..14$.
