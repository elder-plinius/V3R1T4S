# Table snapshot: Sicherman, Heptiamond Compatibility, cell M-X

Snapshot only (no third-party page is copied into this package). All fetches were single read-only GETs
with user agent "V3R1T4S-kit (whosedreams)".

## The table cell compared against
| field | value |
|---|---|
| URL | https://sicherman.net/7mond/7compat.html |
| fetched (UTC) | 2026-11-25T00:18:18Z |
| HTTP status | 200 |
| Content-Length | 36097 |
| Last-Modified | Wed, 27 Mar 2024 02:37:20 GMT |
| ETag | "8d01-6149b492fd9ea" |
| page sha256 | c602d9d24d51bf7e5b3d933b6f77e2092f62a95bb479e9d722683d9bcb02ffd0 |
| page footer | "Last revised 2012-01-04." |
| table | "Minimal Solutions", Summary table (unrestricted: holes allowed) |
| cell M-X (row M, column X) | `?` (red), no known compatibility figure |
| cell X-M (row X, column M) | `?` (red) |
| same pair, "Holeless Variants" Summary table | `?` in both M-X and X-M |
| any `×` (believed impossible) cell on the page | none (0 occurrences) |

Row M of the unrestricted table as read: A:6 B:2 C:6 D:6 E:6 F:6 G:2 H:2 I:9 J:? K:6 L:2 M:* N:2 P:? Q:2
R:12 S:18 T:6 U:? V:? X:? Y:6 Z:2. The page's sha256 is identical to the copy fetched for the contributor's
run kit on 2026-11-03T00:52:19Z, so the table has not changed between the run and this snapshot.

## Other pages read for the novelty check
| URL | fetched (UTC) | HTTP | sha256 | what it says about M-X |
|---|---|---|---|---|
| https://sicherman.net/pairwise.html | 2026-11-25T00:18:18Z | 200 | 9d88e03a6e0f514490051152a8cbd329b5907464794fb4813b683a3ce226b5ad | Lists "Heptiamond Compatibility" under the Polyiamonds heading (in scope for the bank criterion). No M-X result. |
| https://sicherman.net/7mond/labels.png | 2026-11-25T00:18:19Z | 200 | 3044870c00d4bee9bf8e55ae21713615c93f14211f7d29448d684210408a7ec8 | The page's piece-name image. M: a row of five triangles with two peaks on one side; X: a 3-armed pinwheel. Matches the pieces used here (see README). |
| https://erich-friedman.github.io/mathmagic/0904.html | 2026-11-25T00:18:20Z | 200 | c6d1e1ad373a6f5f023041413153463dfd0f32140fd2bce6f4d5ae3de3a872d0 | Math Magic, September 2004: polyiamonds only up to order 6 (no heptiamond pairs), as the 7compat page itself says. |
| https://sicherman.net/compatibility.html | 2026-11-25T00:18:25Z | 200 | dc169216523af629bd2a875169013ba89f672db33b8a682da7d6576c281a8462 | Index page; no M-X result. |
| https://sicherman.net/mincom/ | 2026-11-25T00:19:01Z | 200 | 3020fa35578ce6f49a0ae475cd267cf3f53885fff794d68e537840c278ea4bc3 | Minimal incompatibility for polyiamonds (smallest polyiamonds incompatible with each heptiamond; orders 4 to 6). No heptiamond-heptiamond impossibility for M-X. |
| https://sicherman.net/ncomresta/addendum.html | 2026-11-25T00:19:02Z | 200 | d4c43078f94b61a5cdd25a635f94e1b87baa1a48275248c9f0f98eddbbc31191 | Describes Giovanni Resta's Polypolyominoes as the main resource for polyomino (square-cell) compatibility; nothing on polyiamonds. |
| http://www.iread.it/Poly/ (Resta) | 2026-11-25T00:18:40Z | 500 | (empty) | Not reachable from the packaging machine; https://www.iread.it/Poly/index.html returned 404. Resta's site covers polyominoes, per the addendum above. |
| http://recmath.org/PolyCur/7mond/7compat.html (mirror) | 2026-11-25T00:18:55Z | 500 | (empty) | Not reachable over http or https from the packaging machine. A search-engine copy of the mirror read on 2026-11-25 showed the same M row with `?` at M-X. |
| https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+heptiamond | 2026-11-25T00:19:25Z | 200 | (API JSON) | 0 issues or pull requests mention heptiamond; 0 mention polyform-compatibility. |
| https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns | 2026-11-25T00:19:33Z | 200 | (API JSON) | No polyform-compatibility family folder; TROPHY_CASE.md on main has no polyform or heptiamond entry. |

## Re-fetch at claim time
| URL | fetched (UTC) | HTTP | sha256 | Last-Modified | M-X / X-M (unrestricted) | M-X / X-M (holeless) |
|---|---|---|---|---|---|---|
| https://sicherman.net/7mond/7compat.html | 2026-11-25T00:46:46Z | 200 | c602d9d24d51bf7e5b3d933b6f77e2092f62a95bb479e9d722683d9bcb02ffd0 | Wed, 27 Mar 2024 02:37:20 GMT | `?` / `?` | `?` / `?` |

Unchanged from the 2026-11-25T00:18:18Z snapshot. Re-fetch once more right before the pull request is opened.
