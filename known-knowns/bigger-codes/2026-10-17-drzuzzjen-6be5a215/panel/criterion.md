# Independent CRITERION review

reviewer: Independent Codex CRITERION skeptic

context: fresh subagent, CRITERION role, started with only the claim package and pinned procedural rules; no memory, sibling panel, old review or gate was used.

## Literal criterion

> Success means an explicit list of M distinct binary vectors of length n, each with Hamming weight exactly w, with all pairwise distances >= d (d even), where M is STRICTLY GREATER (direction: max) than the lower bound shown at verification time in the (n,d,w) cell of https://aeb.win.tue.nl/codes/Andw.html (also checking the mirror cell A(n,d,n-w)), and also strictly greater than any value for that cell in arXiv:2608.13906 (Echols, 124 improved cells), arXiv:2607.19550 (Lysenstoen) or any newer arXiv paper. M must not exceed the tabulated upper bound; exceeding it means a bug.

Target: `constant-weight-codes`. Object: `object/A26_6_9_5997.txt`.

classification: full success criterion met for this one lower-bound cell; no partial-win substitution.

## Mathematical quantifiers

PROVED-HERE: I wrote `../independent-criterion/check.py` directly from the definition, without the author's checker. Its saved output is `../independent-criterion/check-output.txt`. The object SHA-256 is `6be5a215f0b662497e21330c98db83b5128095af52e4a45a8484ba60ff524de8`. It has exactly 5997 distinct rows; every row consists of exactly 26 binary characters and has weight exactly 9. Every one of the 17979006 unordered pairs was checked by integer XOR and population count. Minimum distance is exactly 6, which is even. The distance histogram is:

```
6: 422994
8: 1593916
10: 4611184
12: 5920181
14: 4049592
16: 1241882
18: 139257
```

PROVED-HERE: Complementing within exactly 26 coordinates maps every word to weight 17, preserves distinctness, and preserves every XOR distance because `(x XOR mask) XOR (y XOR mask) = x XOR y`. Consequently the mirror statement follows for the identical cardinality. This is one cell up to complement symmetry, not two independent findings.

## Current table and mandatory sources

KNOWN: I parsed the raw `reference-data/brouwer.html`, not `brouwer-cell.json` or an author's audit verdict. Its SHA-256 independently recomputes to `117899cff5af3fd00af17389595c5756050edb94cba876570cf9b76e451107f8`, matching `reference-data/brouwer-receipt.json`. That receipt records one honest named-client request with HTTP 200 at `2026-10-17T14:00:04.470242+00:00`, and Last-Modified `Sat, 17 Oct 2026 06:18:21 GMT`. The d=6 table header places weight 9 in the column whose n=26 entry is `5986Pl-16122`. Thus 5997 is strictly above 5986 by 11 and below 16122 by 10125. The full table contains no separately printed n=26, weight-17 entry; complementation makes the weight-9 comparison the equivalent mirror comparison, rather than treating the missing mirror as a zero bound. This snapshot is contemporaneous with this review and within the pinned six-hour gate window.

KNOWN: I opened the actual cached primary HTML/text for William Echols, `primary-texts/mandatory-primary/2608.13906v1.*`, and Christian Lysenstøen, `primary-texts/mandatory-primary/2607.19550v1.*`. The HTML hashes recompute to `57b3e5fd6679385eb244a7a1171631204b0aa48cc61c68a37d6421ec2fe742a4` and `138e693dab62b9ce51829de318209faa0986ba167778ebbe5d2b9aa259cd190c`, matching their HTTP-200 receipts. Echols's Table 1 was read as paired parameter columns: its d=6 results concern weights 5, 6 and 8, and its n=26 weight-9 result has d=8 and size 890. It gives no same-cell or mirror lower bound reaching 5997. Lysenstøen's explicit improvements are on smaller-length cells, including (23,6,10), (24,6,10), (23,6,11), and (24,6,8); its discussions of saturation and insertion maximality are not claims that A(26,6,9) reaches 5997. Neither mandatory source subsumes this object.

## Newer papers and existing contributions

KNOWN: I screened the raw `reference-data/metadata-union.jsonl` records (378 records), including titles throughout the recent corpus and abstracts of plausible coding/construction leads. I independently read the supplied actual primary texts for the concrete leads, rather than adopting the supplied coverage or shortening conclusions. In particular:

- `primary-texts/mandatory-primary/2603.00174v1.*` (Christopher D. Rosin) concerns 24 improved cells; its n=26 rows have distance 8 and do not give this d=6 cell.
- `primary-texts/corpus-review/2609.35051v1.*` (Yang and coauthors) supplies kissing constructions and d=8 weight-8 improvements, not a competing 5997-word (26,6,9) code.
- `primary-texts/literature/2610.10973v1.*` is an asymptotic invariant-packing theorem with fixed parameters as the length tends to infinity; it does not certify a numerical bound at length 26. Likewise `primary-texts/page2/2411.16028v1.*` and `primary-texts/page2/2401.00733v2.*` are asymptotic results, not finite-size certificates for this cell.
- `primary-texts/literature/2610.15340v1.*`, `primary-texts/literature/2608.14437v1.*`, and `primary-texts/literature/2606.03299v1.*` concern triple orbits/design distributions, diameter-perfect structures, and signed weight-4 Johnson graphs respectively; their parameters/results do not supply this binary weight-9 bound.
- `primary-texts/corpus-review/2610.11609v1.*` gives general binary codes of only 84, 196 and 65 words, at other length/distance choices. `primary-texts/corpus-review/2610.04617v1.*`, `primary-texts/literature/2610.08480v1.*`, and `primary-texts/literature/2609.33753v1.*` concern linear graph/matroid or odd-prime-field codes and scheduling constraints, not a competing value in this cell.
- `primary-texts/corpus-review/2606.24573v1.*` concerns a classical self-dual [26,13,6] binary linear code, all of whose words have even weight, not the claimed odd-weight slice. `primary-texts/corpus-review/2609.25086v1.*` concerns a rank-26 lattice and a geometric design, not a binary length-26 weight-9 code.
- The actual `primary-texts/page2-addendum/2503.11934v1.*`, `2407.11554v2.*`, and `2407.04193v2.*` concern nonbinary weight-4 codes, conflict-avoiding codes, and quaternary additive codes. Their alphabets, weights and objectives do not supply the needed value.
- I also examined the supplied older construction/propagation papers in `primary-texts/corpus-review/1004.1503v3.*`, `1008.1610v1.*`, `1505.06524v4.*`, and `1707.02315v1.*`, and the remaining `primary-texts/page2/` primary texts. Their general constructions, asymptotic statements, upper bounds, special distances or other parameter families supply no same-cell value reaching 5997.

KNOWN: The raw upstream `reference-data/upstream-index.csv`, `upstream-family-README.md`, and `upstream-TROPHY-cwc-excerpt.md` identify 5986 as the existing explicit (26,6,9) result, consistent with the current table. I screened the raw upstream PR listing and relevant file data for this cell and its mirror; no competing 5997-or-larger same-cell contribution was found. The GitHub lexical search results alone were not treated as proof of absence.

PROVED-HERE: To test obvious neighbor subsumption, I wrote `../independent-criterion/shorten.py` and `extra-slices.py` independently. They count every coordinate set and fixed-bit pattern that removes the necessary number of ones/zeros to yield length 26 and weight 9 from the supplied raw neighboring objects. The maximum target-preserving slices are:

| Raw object in `reference-data/published-code-inputs/` | Maximum |
|---|---:|
| `A27_6_9_8325.txt` | 5555 |
| `brouwer-A28_6_9_11388.txt` | 5162 |
| `pr28-code.txt` (27,6,10), size 13026 | 4827 |
| `A-29-6-9-14313.txt` | 4517 |
| `A-29-6-10-25896.txt` | 4290 |
| `A29_6_10_25974.txt` | 4476 |
| `A29_6_11_41219.txt` | 3760 |
| `A29_6_12_61823.txt` | 3756 |

The raw inputs, not the author's `shortening-audit*.json`, were used. Each maximum is below 5997. These are exhaustive slice comparisons of these particular published inputs, not a new constructive search or an assertion that all possible transformations have been exhausted. No essential source comparison is being delegated as a condition of this pass.

## Scope, method, access, credit and disclosure

The explicit-object claim needs no statistical null model: deterministic checks decide all mathematical properties. The source comparison supports the stated improvement at the recorded verification snapshot; it does not establish optimality, global search exhaustion, new algorithmic methodology, public priority, or external table acceptance. No enumerated partial win appears in `target.json`, and merely reproducing a known object would not qualify as a fallback partial win.

`METHOD_AND_CREDITS.md` identifies random removal/regrowth and the existing V3R1T4S engine, and credits Jean Francois Gutierrez / DrZuzzjen, Jordan Boisclair for the seed, A. E. Brouwer for the archive/table, and the original engine/contributors with AGPL-3.0 licensing preserved. This review adds source attribution to Echols, Lysenstøen, Rosin and the compared publications; it claims no new method or ownership of their work. The approved public attribution is not treated as scientific evidence. The target is explicitly open disclosure; this panel performs no publication or contact. No private person, credential, personal filesystem path or session identifier is included in this report.

Access authority does not prove novelty: the claim's supplied authorization overrides the historical local perpetual manual-only rule, while the HTTP receipts and actual source bytes establish what was read. I made no extra remote request, retried no block, and used no bypass. Prior incidents are not erased by this assessment.

confirmed_scope: The frozen 5997-word object proves A(26,6,9) >= 5997, equivalently A(26,6,17) >= 5997, exceeding the 5986 lower bound in the 17 October 2026 Brouwer snapshot by 11 without exceeding its 16122 upper bound or being subsumed by the mandatory papers and examined newer sources and contributions.

pass: true
