# Dimension 25, 651 points

## What

The claim covers exactly the cell (25, 651), meaning 651 vectors in R^25 after unit normalization at 50-digit precision, with the requirement that the maximum pairwise cosine is strictly smaller than the live table cosine 0.245484258816 by at least 1e-10.

## Check it yourself

From this folder, run `sh verify-it-yourself/run_checks.sh`. The last line is `PASS`. A laptop finishes in well under a minute. The checker uses only the Python standard library.

## Compared to

The live table at https://spherical-codes.org/ and https://spherical-codes.org/plain, fetched 2026-10-23T08:26:36Z, HTTP 200. Cell (25, 651): table cosine 0.245484258816, this code's maximum inner product 0.24269125376256213554570755018269336149252422485568. The HTML reference is Azmi C. Özgen, 2026, with no proven-optimal mark and without the text needs more optimization. The extracted row is the-record-we-beat/table_rows.tsv. A later novelty fetch, Date Fri, 23 Oct 2026 08:30:14 GMT, still shows that same cell cosine, with no star and no needs-more-optimization text. The whole-page hashes differ because other rows moved. This cell did not.

## Not claimed

No other cell. In particular the 2026-10-22 lead file for this same N, the packaged cells (25, 653), (25, 73) and (25, 173), and every other polished dimension-25 file are not in this package. This is not partial win p2: the row is not labeled needs more optimization. Dimension 25 is outside 9..23, so the kissing-number handoff does not apply. Nothing here was uploaded.

## Credits

Henry Cohn maintains https://spherical-codes.org/ . The beaten row is attributed on that table to Azmi C. Özgen, 2026. The coordinate file was polished from the table's own posted points for this cell, starting from the 2026-10-22 polish of those points. Ilmari Vahteristo, arXiv:2610.19988 (2026), is the recent numerical paper checked for this cell; its feed does not list this cosine.
