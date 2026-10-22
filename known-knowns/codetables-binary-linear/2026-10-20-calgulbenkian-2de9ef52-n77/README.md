# Qubit stabilizer code [[77,59]] of distance 5, above the codetables.de lower bound 4

## What

The stabilizer code [[77,59]] in the supplied object file has exact minimum distance 5 (commuting, rank 18, pure distance >= 5 by distinct syndromes of all weight <= 2 errors, weight-5 logical outside the stabilizer), which exceeds the lower bound 4 shown in the codetables.de QECC cell for [[77,59]] on 2026-10-20T02:59Z, within upper bound 6; no claim about the literature or about any other cell.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

- Requirements: python3 3.8 or later, standard library only.
- Rough laptop time: a few seconds.
- Expected last line: `ALL CHECKS PASS` (the checker's own line is `RESULT PASS [[77,59,5]] live [4,6]`).

## Submission id and the shared object file

The object file object/new_stabilizer_codes_d5.json (sha256 2de9ef5264ea4bbbe334bf590f12f5ce89cb8f8ce30a464b4112e55f66a2927f) is one file shipped unchanged in ten packages (cells [[39,23]], [[75,57]], [[77,59]], [[79,61]], [[81,63]], [[83,65]], [[85,67]], [[87,69]], [[89,71]], [[91,73]]); this package claims only the entry n = 77, k = 59. The usual submission id ends in the first 8 hex digits of the object's sha256 (2de9ef52), which would be identical for all ten packages. So each id here is 2026-10-20-calgulbenkian-2de9ef52-n77, the usual id with the code length appended. (The earlier distance-4 packages sharing one six-code file used a different device: the first 8 hex digits of the sha256 of the text OBJECTSHA:n:k. We follow the instruction for this batch instead.)

## Compared to

| Source | Cell | Lower bound | Upper bound | Ours | URL | UTC fetch time |
|---|---|---|---|---|---|---|
| codetables.de QECC table (Markus Grassl) | [[77,59]] | 4 | 6 | **5** | https://codetables.de/QECC.php?q=4&n=77&k=59 | 2026-10-20T02:59:13Z |
| same page, first fetch | [[77,59]] | 4 | 6 | **5** | https://codetables.de/QECC.php?q=4&n=77&k=59 | 2026-10-20T02:44:47Z |

The qubit table is addressed with the form parameter q=4. The page says "Last change: 10.06.2024". Snapshot metadata, HTTP status and page sha256: the-record-we-beat/README.md. The panel's novelty report is panel/novelty.md; it found no competing value in the repository's merged or open pull requests and no qubit distance-5 code at these parameters in six arXiv HTML searches, and found that the standard propagation rules of the table and Rains shortening of the table's stored codes do not give this value from other cells.

## Not claimed

- This covers only this cell under the partial win p1 of the target codetables-binary-linear (a quantum code above the live codetables.de quantum lower bound). It is not a claim under the target's main success criterion, which concerns linear codes over GF(q), and it says nothing about the other nine cells of the same object file.
- The distance is exactly 5, but the live upper bound is 6, so the cell does not close. The proof is pure distance at least 5 (all errors of weight at most 2 have distinct syndromes) plus a weight-5 logical operator outside the stabilizer, which excludes 6.
- It says nothing about novelty against the literature beyond what the panel searched. The arXiv export API was rate-limited (HTTP 429) throughout the novelty check, so the panel used the arXiv HTML search with six queries, which is less complete. A construction outside arXiv, or one the table has not recorded, cannot be excluded, and work after the table's last change (10.06.2024) could already contain a code with these parameters. The live table is the status source.
- The ten cells come from one family construction in one object file, by one search agent. Each was judged separately, and none follows from another cell or from a table code by the standard propagation rules or by shortening (the panel tested Rains shortening only on the table's stored stabilizer matrices; codes the table does not store were not tested). A reader who counts constructions rather than cells should count one family.
- Longer chains of propagation rules (Construction X, subcodes) were not excluded exhaustively by the panel; none is visible in the table.
- Exactness rests on the panel's programs and this package's checker, which enumerates by exact integer bit arithmetic (no sampling), with a second independent enumeration of the syndromes.
- The construction code is not in this package (how-we-built-it/README.md).
- Not peer reviewed. It was checked by a three-skeptic panel (panel/; the skeptics are Claude Code subagents of a different model family from the object's builder) and by the standalone checker shipped here.

## Filing history

New filing. It is not a refile of an earlier pull request.

## Credits

- Markus Grassl and codetables.de (https://codetables.de/): the quantum code table this claim is compared against and whose stored codes the panel used for the propagation checks. The fetched table page states that it is maintained by Markus Grassl.
- The object's builder: the contributor's AI search agent (Gemini, called Argon), working for the contributor calgulbenkian.
- Contributor credit: calgulbenkian.
- No construction paper is credited: none was fetched and seen attributed to this construction, and the object file names none.
