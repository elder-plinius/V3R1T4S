# Correction (2026-11-02): upstream file hashes

During repackaging review, an adversarial check found that two upstream
`teorth/equational_theories` SHA-256 hashes recorded in the original
`2026-11-01` run artifacts do not match the real files:

| File (at commit `2f49bdaf3d38ffb722e54ac1288c8269dac61846`) | Wrong hash (inherited) | Correct hash (from `sha256sum` output) |
|---|---|---|
| `equational_theories/ManuallyProved/Equation677.lean` | `ad46b8e3015f43da7eb602924c27c6ab22f65f206f80b6ed802aa01122e963d4` | `dc1050b709dfe6c5ce33b9c2afa264dd70041308356df4045739061942ebbf3f` |
| `blueprint/src/chapter/677.tex` | `daeb5199018e0d8c0f063ac1b00bd989ba7321699a087df527c858380b61816c` | `e25f4c8e3ecfe454ad303782b68af69e41eb0572f780c5a7203cc8210b4b152e` |

The correct values were already on record in `runs/2026-11-01-1637/scout.md`
(lines 30–31) and were re-confirmed by direct `sha256sum` on both
`references/equational_theories/...` and `runs/2026-11-01-1637/data/...`
copies on 2026-11-02. The wrong strings entered via
`runs/2026-11-01-1637/claim/status_snapshot.md` and were copied by the
novelty panelist.

Fixed in this package: `README.md` and `the-record-we-beat/snapshot.md`
now carry the correct hashes. `panel/novelty.md` is left byte-identical
as sealed skeptic evidence from the 2026-11-01 gate; its two stale hash
strings are superseded by this note. No object bytes, theorem, model, or
panel verdict was affected: the novelty conclusion (both implications
still `"unknown"` on the live finite graph) was re-confirmed against a
fresh 2026-11-02 fetch of `finite_outcomes.json.gz` (see `snapshot.md`).
