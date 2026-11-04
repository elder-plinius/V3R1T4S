# hsp4 N = 152: 152 equal balls in the unit 4-ball

## What

152 centres in R^4 (object/hsp4-152.txt) whose feasible radius in the unit 4-ball, r* = 0.22097502706448416409, exceeds the Packomania hsp4 table value 0.220960306508 for N = 152 (radius.txt fetched 2026-11-01T14:32Z) by 1.472e-05 and the Moki & Julio MANIFEST.csv value 0.2209615356462587873029967 by 1.349e-05; the configuration is not isometric to the posted hsp4-152.txt, its r* exceeds every panel polish of that posted file by more than 1e-9, and it was found from non-posted starts.

Conditions recorded by the panel gate: queue caveat: the 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle on Packomania's pending list is category-unspecified and cannot be resolved; N = 152 must be re-checked against the live table once that bundle disappears from the pending list. No email submission was made.

## Check it yourself

From this folder, Python 3 standard library only (about 1 second on a laptop):

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. The checker reads the coordinates as exact decimals, computes squared distances and inner
products exactly with `fractions`, and takes square roots with `decimal` at 50 digits, with no tolerance.

## Compared to

- Table: Packomania, section "hyperspheres in a hypersphere", d = 4 (E. Specht), https://packomania.com/hsp4/hsp4.html
- Cell: N = 152, file https://packomania.com/hsp4/txt/radius.txt, row `152 0.220960306508` (12 decimals)
- Fetched: 2026-11-01T14:32Z (sha256 f3ddaa944aac014718bc9f5438700698abedac0189266198df8bb60772ac569f).
- Our value: r* = 0.22097502706448416408815908921357097646062824532483 (50 digits, from object/hsp4-152.txt), gain 0.00001472055648416408815908921357097646062824532483 over the posted 12-decimal value.
- Prior public claim: Moki & Julio collection, MANIFEST.csv row hsp4 N = 152, new_radius 0.2209615356462587873029967; our r* is higher.
- Posted packing hsp4-152.txt: not isometric to ours, and our r* exceeds the panel's own polishes of it by more than
  1e-9 (numbers in panel/novelty.md and panel/criterion.md).

## Not claimed

Not optimality, and nothing about any other N or about hsp5/hsp6. No email submission to Packomania was made.
Queue caveat (bank QUEUE RULE): the 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle on
https://packomania.com/pending-requests.html is category-unspecified and cannot be resolved; N = 152 must be re-checked
against the live table once that bundle disappears from the pending list. The table, history and queue pages were
read from copies fetched at 2026-11-01T14:32Z, not re-fetched by the machine that built this package.

## Credits

- Eckard Specht, Packomania (https://packomania.com/), author of the table and of row N = 152 and its posted packing.
- Moki & Julio, https://github.com/Hashirama1337s/moki-julio-circle-packing (MANIFEST.csv), prior public claims compared against.
- Bank target and criterion: V3R1T4S, `packomania-hyperspheres-hsp4-hsp6` (https://github.com/elder-plinius/V3R1T4S).
- Contributor: benmeadows.
