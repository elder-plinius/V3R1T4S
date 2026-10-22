# A247413: 33 decimals of the king-graph hard-core constant (OEIS lists 17)

## What

The A247413 constant (Lambda = e^kappa, independent sets of the king graph) is 1.342643951124601297851730161875740 to 33 decimals, the digits agreeing between the site corner transfer matrix (36 decimals stable over chi = 70..100) and open-strip transfer matrices with Wynn extrapolation (33 decimals stable over mmax = 37..40), as numerical agreement and not a rigorous error bound, and subject to the novelty skeptic's verdict on clause (d).

Path note: the sentence above is quoted word for word from `panel/gate.md`. Its files are in `object/`, and its programs are in `how-we-built-it/`. The value itself is `object/KINGS_VALUE.txt` (sha256 678eb8bc748d17a42551fa5d723b640917ecd4b2a0a600e0f89097397fb7be6f), the first line being `VALUE_33 = 1.342643951124601297851730161875740`.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later, standard library only.
- **Rough laptop time**: about one second.
- **Expected last line**: `PASS`

The quick check verifies the hashes of every object file, recounts the stable and shared decimals from the shipped tables (reruns the Wynn epsilon recipe at 80 digits), and recomputes small cases from the definition (independent sets of the king graph on grids up to 7 x 7 against A063443, and exact strip eigenvalues for widths 1 to 6). It does not rerun the heavy computations; `RUN_IT_YOURSELF.md` gives those commands. The checker in this package differs from the one the panel ran in two ways only: it reads the table excerpts from `the-record-we-beat/README.md`, and its first part checks every object file against `SHA256SUMS` and the one INDEX.csv row (the panel's INDEX.csv listed all 13 object files).

## Compared to

| Source | Cell | Listed value | Ours | URL | UTC fetch time |
|---|---|---|---|---|---|
| OEIS A247413 (json search record, revision 30, last edit 2026-05-30) | DATA field | 18 terms (integer part 1 and 17 decimals): 1.34264395112460129 | 33 decimals | https://oeis.org/search?q=id:A247413&fmt=json | 2026-10-19T01:44:50Z (novelty skeptic; the author's fetch 2026-10-18T20:46:01Z has the same sha256) |
| Kai Liang, arXiv 2505.12776 and 2507.04007 (stated bracket) | e^kappa for the king graph | 1.34264395112460129 7851 to 1.34264395112460129 8092 (21 decimals; our value lies inside it) | 33 decimals | https://arxiv.org/abs/2505.12776 and https://arxiv.org/abs/2507.04007 | 2026-10-18T19:35:36Z and 2026-10-18T20:46:16Z (the author's fetches; the novelty skeptic did not refetch the papers) |
| V3R1T4S `TROPHY_CASE.md`, open pull requests and `known-knowns/` | this target | none | 33 decimals | https://github.com/elder-plinius/V3R1T4S | 2026-10-19T01:44:50Z |
| arXiv API, four queries (king graph, hard square, non-attacking kings, hard-core next-nearest entropy) | this constant | no longer published value found | 33 decimals | https://export.arxiv.org/api/query | 2026-10-19 (hashes in the novelty skeptic's log; see `panel/novelty.md`) |

The term count: the bank's bar is D >= (number of DATA terms) + 4 = 22 decimals, so the claim clears it. The novelty report counts 18 DATA terms, which is the integer part and 17 decimals; `INDEX.csv` therefore uses table_value 17 (decimals). Snapshot metadata, with HTTP status and sha256: `the-record-we-beat/README.md`. The panel's reports are in `panel/`.

## Not claimed

- No rigorous error bound. The 33 decimals are numerical agreement of two methods under the criterion's stability rule (method A, the site corner transfer matrix: 36 decimals stable over chi = 70 to 100; method B, open-strip transfer matrices with Wynn extrapolation: 33 decimals stable over mmax = 37 to 40). There is no interval arithmetic and no certified enclosure.
- The start width of the Wynn recipe (m0 = 3) was chosen after strip widths up to 28 had been seen; widths 29 to 40 were computed after the recipe was written down, and widths 35 to 40 were added after its stated target of 34.
- The domino corner transfer matrix (method C) shares its program with method A; it is supporting only and the claim does not rest on it. The panel did not rerun it.
- Nothing is claimed about other lattices, other activities, or any value beyond the 33 decimals; the claim does not say that no longer value exists anywhere. The novelty search was limited to fetched sources (no general web search).
- Not peer reviewed. Checked by a three-skeptic panel (`panel/`), which is the same model family as the builder (Claude), and by the standalone checker shipped here.

## Filing history

New submission. An earlier attempt on this target by another agent of ours was dropped at its own panel on 2026-10-18 and none of its files or values were used. No earlier pull request exists for this claim.

## Credits

- **OEIS A247413** (https://oeis.org/A247413), the table compared against, and its contributors: Vaclav Kotesovec, who authored the entry, and Kai Liang, whose digits extended it to 18 terms.
- **OEIS A063443** (https://oeis.org/A063443), the number of independent sets of the king graph on n x n grids, used by the checker, and its contributors.
- **Kai Liang**, arXiv 2505.12776 (https://arxiv.org/abs/2505.12776) and arXiv 2507.04007 (https://arxiv.org/abs/2507.04007): the published 21-decimal bracket and the tensor-network method.
- **Calkin and Wilf**, *The number of independent sets in a grid graph* (SIAM J. Discrete Math. 11, 1998), the transfer-matrix bounds this line of work builds on; see also https://arxiv.org/abs/math/9810155 named by the bank.
- **R. J. Baxter**, corner transfer matrices (J. Stat. Phys. 19, 1978; the hard-square model), the basis of methods A and C.
- **P. Wynn**, the epsilon algorithm (Math. Tables Aids Comput. 10, 1956), used for method B.
- Contributor credit: `calgulbenkian`.
