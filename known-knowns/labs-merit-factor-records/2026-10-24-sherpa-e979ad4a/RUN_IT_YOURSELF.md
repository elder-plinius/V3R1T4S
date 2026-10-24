# Run it yourself

From this folder, in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output (see `verify-it-yourself/RECEIPTS.md`): `L = 401  E = 10776  F = 7.461071`, five "below" lines,
`a corrupted copy is rejected`, then a last line `PASS`.

To re-read the comparison values, fetch each source once from its URL in `the-record-we-beat/RECORD.md`, check its
sha256, and run the readers in `how-we-built-it/code/` on it (`parse_dimitrov.py`, `parse_hex_table.py`, `read_erk2025_fig2.py`,
`parse_erk2025.py`; numpy and pypdf). To search for sequences of this quality on an NVIDIA GPU, run
`how-we-built-it/code/run_pass3b.sh` with the pinned requirements.
