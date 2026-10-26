# Vault incident, 2026-10-23 ~21:40Z

The first run of `attempts/statistician/code/decompose.py` read `data/vault_drugs.txt` with
`str.split()`, i.e. on whitespace. Eight vault entries are drug **combinations** whose IDs
contain spaces, so they were split into fragments, matched nothing, and were **not excluded**.

- Affected: the 8 IDs in `data/vault_contaminated.txt`.
- Exposure: their responses entered one **descriptive** variance decomposition
  (`output/decompose.log`, run 1). No model was fitted, tuned or selected on them.
- The other 74 vault drugs were correctly excluded.
- Fix: all code reads the vault with `splitlines()`; an assertion now checks that exactly 82
  vault IDs are matched and removed.
- Disclosure commitment: the confirmatory vault diagnostic is reported **both** on all 82 vault
  drugs and on the 74 never-exposed ones.

The vault was not redrawn: redrawing after exposure would be a choice made with knowledge of the
data, which is worse than a disclosed, bounded exposure.
