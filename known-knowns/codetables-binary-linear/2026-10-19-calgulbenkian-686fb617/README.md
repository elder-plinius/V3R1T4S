# A [[23,9,5]] qubit stabilizer code, one above the live lower bound

## What

The object is a pure qubit stabilizer code [[23,9,5]] (14 independent commuting generators on 23 qubits, exact distance 5 by exact MacWilliams and direct enumeration of all Paulis of weight at most 5) whose distance exceeds the live lower bound 4 (upper 6) of the codetables.de quantum cell [[23,9]] as fetched on 2026-10-19 and is not implied by the live one-step neighbours; whether a newer arXiv paper already has it is not decided here.

Path note: the sentence above is quoted word for word from `panel/gate.md` (status `CONFIRMED_PARTIAL`). The object is `object/qecc_p1_n23_k9_d5.json` (sha256 686fb617c1dafe37759247e164ed246cd4ed1c572ea548b8dce8d8abbe450422); its programs are in `how-we-built-it/`.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later, standard library only.
- **Rough laptop time**: about 5 seconds on the packager's machine; allow a minute or two on a slow laptop.
- **Expected last line**: `PASS`

The quick check verifies the object's hash against INDEX.csv, checks the stabilizer rows for independence and exact symplectic commutation, computes the exact distance (MacWilliams transform and direct enumeration), compares with the live bounds and the neighbouring cells in `the-record-we-beat/`, and confirms that a corrupted copy is rejected. The checker alone: `python3 -I verify-it-yourself/qecc_check.py object/qecc_p1_n23_k9_d5.json`, whose last output line begins: `{"n": 23, "k": 9, "rank": 14, "self_orthogonal": true, "d": 5, "claimed_d": 5, "consistent": true, "VALID": true}`. Its real output is in `verify-it-yourself/RECEIPTS.md`. The checker differs from the one the panel ran only in file locations and the last output line (see RECEIPTS.md).

## Compared to

| Source | Cell | Listed value | URL | UTC fetch time |
|---|---|---|---|---|
| QECC cell page | [[23,9]] | lower 4, upper 6 | https://codetables.de/QECC.php?q=4&n=23&k=9 | 2026-10-19T04:35:06Z (triage); 2026-10-19T05:16:34Z (novelty skeptic) |
| QECC full table (neighbour cells) | QECC full table (neighbour cells) | neighbour cells in neighbours.csv | https://www.codetables.de/QECC/Tables_color.php?q=4&n0=1&n1=256&k0=0&k1=256 | 2026-10-19T04:34:26Z (triage); 2026-10-19T05:16:36Z (novelty skeptic) |
| V3R1T4S TROPHY_CASE.md and known-knowns folders | this cell | no competing value (see `panel/novelty.md`) | https://github.com/elder-plinius/V3R1T4S | 2026-10-19T05:15:21Z (novelty skeptic) |
| arXiv, four generic queries plus the named work 2609.37056 | this cell | no newer claim found (queries were generic, not exhaustive; see `panel/novelty.md`) | https://arxiv.org/abs/2609.37056 | 2026-10-19 (novelty skeptic) |

Ours: [[23,9,5]] stabilizer code, value 5; the table value in `INDEX.csv` is "lower 4 upper 6". Each page was fetched once, with a plain GET and no retry; snapshot metadata (HTTP status, sha256 of the page, the extracted cell) is in `the-record-we-beat/README.md`. The panel's reports are in `panel/`.

## Not claimed

- This is a partial win only (the bank's enumerated win p1: a quantum-code record). It is a qubit stabilizer code filed under the target of the classical linear-code table; whether the quantum cell is in scope for that target is for the maintainer to rule.
- The distance 5 is exact (exact MacWilliams computation and direct enumeration of all Pauli operators of weight at most 5), and the symplectic self-orthogonality is checked exactly. Nothing in this package is numerical.
- The bar is the live quantum table's lower bound 4 and the best lower bound implied by three one-step rules from the live neighbouring cells (4). Whether a newer arXiv paper already has this code is not decided here.
- The upper bound 6 is unchanged, and nothing is claimed about other cells of the quantum table.
- Not peer reviewed. The package was checked by three fresh Claude Code subagents (reproduce, novelty, criterion) and by the standalone checker shipped here. The object was built by a different model family (Gemini, the contributor's search agent); the skeptics and the packager are Claude.

## Filing history

New submission. The gate notes name no earlier pull request for this cell.

## Credits

- **codetables.de** (http://www.codetables.de/), the table compared against, maintained by Markus Grassl as the bank statement for this target names it.
- **Calderbank, Rains, Shor and Sloane**, arXiv quant-ph/9608006 (https://arxiv.org/abs/quant-ph/9608006), the quaternary MacWilliams identity for quantum codes, named in the bank statement.
- **Toeplitz and double-circulant seeds and Hermitian transvections** are the contributor's own search ideas (`how-we-built-it/`); no outside code was used.
- The object and the search code are by Gemini ("Argon"), an AI search agent working for the contributor. Contributor credit: `calgulbenkian`.
- The three panel reports are by fresh Claude Code subagents (`panel/`).
