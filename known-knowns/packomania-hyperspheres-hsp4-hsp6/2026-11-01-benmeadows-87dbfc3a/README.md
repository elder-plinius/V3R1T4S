# hsp4 N = 136: 136 equal balls in the unit 4-ball

## What

136 centres in R^4 (object/hsp4-136.txt) whose feasible radius in the unit 4-ball, r* = 0.22622027641762341827, exceeds the Packomania hsp4 table value 0.226201706521 for N = 136 (radius.txt fetched 2026-11-01T14:32Z) by 1.857e-05 and the Moki & Julio MANIFEST.csv value 0.2262019190148776245179929 by 1.836e-05; the configuration is not isometric to the posted hsp4-136.txt, its r* exceeds every panel polish of that posted file by more than 1e-9, and it was found from non-posted starts.

Conditions recorded by the panel gate: queue caveat: the 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle on Packomania's pending list is category-unspecified and cannot be resolved; N = 136 must be re-checked against the live table once that bundle disappears from the pending list. No email submission was made.

## Check it yourself

From this folder, Python 3 standard library only (about 1 second on a laptop):

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. The checker reads the coordinates as exact decimals, computes squared distances and inner
products exactly with `fractions`, and takes square roots with `decimal` at 50 digits, with no tolerance.

## Compared to

- Table: Packomania, section "hyperspheres in a hypersphere", d = 4 (E. Specht), https://packomania.com/hsp4/hsp4.html
- Cell: N = 136, file https://packomania.com/hsp4/txt/radius.txt, row `136 0.226201706521` (12 decimals)
- Fetched: 2026-11-01T14:32Z (sha256 f3ddaa944aac014718bc9f5438700698abedac0189266198df8bb60772ac569f).
- Our value: r* = 0.22622027641762341826997812036415868264356258381056 (50 digits, from object/hsp4-136.txt), gain 0.00001856989662341826997812036415868264356258381056 over the posted 12-decimal value.
- Prior public claim: Moki & Julio collection, MANIFEST.csv row hsp4 N = 136, new_radius 0.2262019190148776245179929; our r* is higher.
- Posted packing hsp4-136.txt: not isometric to ours, and our r* exceeds the panel's own polishes of it by more than
  1e-9 (numbers in panel/novelty.md and panel/criterion.md).

## Not claimed

Not optimality, and nothing about any other N or about hsp5/hsp6. No email submission to Packomania was made.
Queue caveat (bank QUEUE RULE): the 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle on
https://packomania.com/pending-requests.html is category-unspecified and cannot be resolved; N = 136 must be re-checked
against the live table once that bundle disappears from the pending list. The table, history and queue pages were
read from copies fetched at 2026-11-01T14:32Z, not re-fetched by the machine that built this package.

## Credits

- Eckard Specht, Packomania (https://packomania.com/), author of the table and of row N = 136 and its posted packing.
- Moki & Julio, https://github.com/Hashirama1337s/moki-julio-circle-packing (MANIFEST.csv), prior public claims compared against.
- Bank target and criterion: V3R1T4S, `packomania-hyperspheres-hsp4-hsp6` (https://github.com/elder-plinius/V3R1T4S).
- Contributor: benmeadows.
