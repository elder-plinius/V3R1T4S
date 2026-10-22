# Qubit stabilizer code [[43,32]] of distance 4, above the codetables.de lower bound 3

## What

The object file's entry n=43, k=32 is a qubit stabilizer code [[43,32,4]] (11 independent commuting generators, no logical of weight 3 or less, a weight-4 logical), exactly checked here, and 4 is strictly above the live codetables.de QECC lower bound 3 for [[43,32]] (fetched 2026-10-19) and equals its upper bound; this covers only this cell under p1 and says nothing about novelty against the literature or about the other five cells.

The object file object/new_optimal_stabilizer_codes_r11_d4.json (sha256 3e9858a143b751d715399b3dc8248129a522c4d2628dfb3bc074f09c0930b9c0) is one file shared by six packages (cells [[37,26]], [[39,28]], [[43,32]], [[45,34]], [[47,36]], [[49,38]]); this package claims only the entry n = 43, k = 32. Because the six packages share one object file, the submission id of each uses the first 8 hex digits of the sha256 of the text "OBJECTSHA:n:k", where OBJECTSHA is the object file's full sha256 above, and n and k are this cell's values joined by colons: for this package, the text is "3e9858a143b751d715399b3dc8248129a522c4d2628dfb3bc074f09c0930b9c0:43:32", which gives 90731079.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

- Requirements: python3 3.8 or later, standard library only.
- Rough laptop time: a few seconds.
- Expected last line: `ALL CHECKS PASS` (the checker's own line is `RESULT PASS [[43,32,4]] live [3,4]`).

## Compared to

| Source | Cell | Lower bound | Upper bound | Ours | URL | UTC fetch time |
|---|---|---|---|---|---|---|
| codetables.de QECC table (Markus Grassl) | [[43,32]] | 3 | 4 | **4** | https://codetables.de/QECC.php?q=4&n=43&k=32 | 2026-10-19T06:43:23Z |
| same page, first fetch | [[43,32]] | 3 | 4 | **4** | https://codetables.de/QECC.php?q=4&n=43&k=32 | 2026-10-19T06:10:54Z |

The page says "last modified: 2006-04-03" for the cell text. The qubit table is addressed with the form parameter q=4. Snapshot metadata, HTTP status and page sha256: the-record-we-beat/README.md. The panel's novelty report is panel/novelty.md; it found no competing value in the repository's merged, open or closed pull requests and no earlier posted distance-4 code for these parameters in six arXiv queries, and found that the standard propagation rules (add a qubit, drop a logical qubit, puncture, Rains shortening from the stored [[44,33]] code) do not give this value from other table cells.

## Not claimed

- This covers only this cell under the partial win p1 of the target codetables-binary-linear (a quantum code above the live codetables.de quantum lower bound). It is not a claim under the target's main success criterion, which concerns linear codes over GF(q), and it says nothing about the other five cells of the same object file.
- It says nothing about novelty against the literature beyond what the panel searched: the panel's search was weak (arXiv, a few queries, no access to Grassl's private tables or Magma), and an unposted or unindexed earlier code with these parameters cannot be excluded. The live table is the status source.
- The distance is exactly 4, which equals the cell's upper bound, so the cell closes. The six cells come from one construction (an extension of a [[64,53,4]] code with 11 parity checks); each was judged separately and none follows from another or from a neighbouring live cell, but a reader who counts constructions rather than cells should count one family.
- The object file credits its base code [[64,53,4]] to "Dastbasteh et al."; the novelty skeptic believes it is the Bierbrauer-Edel quantum twisted code and could not confirm the attribution. No credit is given here for the base code beyond codetables.de.
- The construction code is not in this package (how-we-built-it/README.md).
- Not peer reviewed. It was checked by a three-skeptic panel (panel/; the skeptics are Claude Code subagents of a different model family from the object's builder) and by the standalone checker shipped here.

## Filing history

New filing. It is not a refile of an earlier pull request.

## Credits

- Markus Grassl and codetables.de (https://codetables.de/): the quantum code table this claim is compared against, and the stored [[64,53,4]]-derived codes at neighbouring lengths.
- The base code [[64,53,4]]: attribution unconfirmed (see Not claimed); no author is credited.
- The object's builder: the contributor's AI search agent (Gemini, called Argon), working for the contributor calgulbenkian.
- Contributor credit: calgulbenkian.
