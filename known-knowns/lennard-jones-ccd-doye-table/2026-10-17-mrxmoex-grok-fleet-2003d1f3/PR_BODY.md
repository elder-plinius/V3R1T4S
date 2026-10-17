# Cambridge Cluster Database: Lennard-Jones table errata (N = 602 link; N = 486, 487, 813, 899 stale energies) and Morse table erratum (63C, ρ0 = 3 sign typo) (data-integrity errata)

One combined errata package for two Cambridge Cluster Database (CCD) tables: (A) the Lennard-Jones tables `LJ310-561.html` and `LJ562-1000.html`, and (B) the Morse table `Morse/tables.html`.

| | |
|---|---|
| **Claim** | **(A) Lennard-Jones.** (1) The N = 602 row links to `LJ562-1000/601.TXT`, a 601-atom file whose energy is the N = 601 value. The correct 602-atom file is already on the CCD server at `LJ562-1000/602.TXT` but is not linked. (2) For N = 486, 487, 813 and 899, the posted coordinate file sits *below* its own table row: the table value is higher than the energy of the file it links to. **(B) Morse.** The 63C cell at ρ0 = 3 reads **+495.356854[1]**. The posted 63C file, relaxed at ρ0 = 3, gives an index-1 stationary point at **−495.356853771**, which matches the cell's own [1] bracket. The magnitude is right and the sign is wrong. It is the only positive energy on the whole page. |
| **One-command repro** | `sh verify-it-yourself/run_checks.sh` runs (A) and then (B). Add `--with-sources` to also check the original LJ authors' 2004 archive and the Barron 2005 PDF. Python 3 standard library only. Everything is downloaded from the live sites at run time. Expected last line: `PASS`. |
| **Not claimed** | No new minimum and no record. **(A)** Every lower LJ energy here is already published: the four files are byte-identical to the original authors' 2004 archive, and Barron's 2005 tables list the lower values (sources below). So these are table-vs-file errata, not discoveries. For N = 813 a still lower value, −5712.251749, was published by Barron, so neither the CCD table nor the CCD file holds the best-known N = 813 structure. **(B)** 63C is a sign correction only. The value −495.356854 is the table's own number with its sign fixed. Novelty: the CCD has no public errata or history page, so we cannot show these errata are unreported (see Not claimed). We make no claim about any other row. |
| **Confidence** | High. Each check is deterministic. **(A)** Every file was downloaded 3 times and was byte-identical each time. The energies come from the posted coordinates exactly as given, and a tight L-BFGS polish moves them by < 4e-8. **(B)** The table page and the 63C file were each downloaded 3 times, byte-identical each time. Two independent codes (a numpy/scipy adjudication run and the stdlib-only repro here) both give −495.356853771 with Hessian index 1. The same file at its own header ρ0 = 6 reproduces the table's ρ0 = 6 cell (−285.141958), which shows the parser and the potential are right. |

## What

These are errata for two tables in the Cambridge Cluster Database (Wales group): the LJ tables N = 310–561 and N = 562–1000, and the Morse-cluster table (Doye and Wales). No CCD coordinate data is shipped here, only URLs, sha256 hashes, sizes and Last-Modified dates (`SOURCES.csv`). The energy numbers, atom counts and Hessian indices below are the finding.

## (A) Lennard-Jones tables: N = 602, 486, 487, 813, 899

Energy: E = Σ_{i<j} 4(r⁻¹² − r⁻⁶) with ε = σ = 1, as the CCD pages state.

### A.1 Per-N numbers

| N | table row says | posted file (as linked) | file − table | published lower value | fix |
|---|---|---|---|---|---|
| 602 | −4134.979952 | `601.TXT`: **601 atoms**, E = −4127.726727 (= the N = 601 row) | +7.253225 (wrong file) | n/a | point the 602 row at `LJ562-1000/602.TXT` (602 atoms, E = −4134.979952, matches the table) |
| 486 | −3278.642178 | 486 atoms, E = −3278.672947 | −0.030769 | −3278.672947 (Barron 2005) | table → −3278.672947 |
| 487 | −3285.926242 | 487 atoms, E = −3285.966242 | −0.040000 | −3285.966242 (Barron 2005) | table → −3285.966242 (one digit: 2 → 6) |
| 813 | −5712.249964 | 813 atoms, E = −5712.250652 | −6.88e-4 | −5712.251749 (Barron 2005; lower than the file too) | table → at least −5712.250652; best known is Barron's −5712.251749 |
| 899 | −6371.011413 | 899 atoms, E = −6371.011483 | −6.96e-5 | −6371.011483 (Barron 2005) | table → −6371.011483 |

**N = 602.** The table link is `<a href="LJ562-1000/601.TXT">602</a>`, so N = 601 and N = 602 both open the same file (sha256 b0bb11e9…8dd9). The correct `LJ562-1000/602.TXT` (sha256 9c7b8021…8043, 24080 B) is on the CCD server. It is byte-identical to `./LJ562-1000/602.TXT` in the original authors' 2004 archive (Xiang, Cheng, Cai, Shao; Nankai `LJ562-1000.tar.gz`). It has 602 atoms and E = −4134.979952, which matches the table. Only the href needs to change.

**N = 487.** The difference is exactly 0.040000, which looks like a one-digit transcription error (−3285.9**2**6242 vs −3285.9**6**6242). Note that the authors' own 2004 table has the same values as the CCD for N = 486, 487, 813 and 899, so these stale numbers date back to the 2004 source table, not to the CCD copy.

**N = 813.** The CCD table lags *both* its own file (−5712.250652) *and* the best published value. Barron's 2005 tables and his novel-clusters page give −5712.2517 (table: −5712.251749) and list −5712.2506 as the "old" value from Xiang et al. The minimum correction is to state the file's own energy. Posting Barron's structure would make the row current. That choice belongs to the maintainer.

## (B) Morse table: 63C at ρ0 = 3

Energy: E = Σ_{i<j} e^{ρ0(1−r)} (e^{ρ0(1−r)} − 2), in units of the pair well depth, with unit equilibrium pair distance, as the CCD page states. The page explains that a number in square brackets after an energy is the Hessian index ("the number of negative eigenvalues of the Hessian") when the structure is a saddle point at that ρ0. The first line of each points file gives the ρ0 the coordinates belong to.

| item | value |
|---|---|
| table cell, row 63C, column ρ0 = 3 | **+495.356854[1]** (the only positive energy anywhere on the page) |
| other 63C cells (ρ0 = 6, 10, 14) | −285.141958, **−262.030007**, **−258.620607** |
| `points/63C` | 63 atoms; first line `6.0000000000` (ρ0 = 6) |
| file at its own ρ0 = 6 (calibration) | E = −285.141957629, max\|grad\| 2e-13: matches the ρ0 = 6 cell |
| file relaxed at ρ0 = 3 (L-BFGS, then Newton) | stationary point E = **−495.356853771**, max\|grad\| < 1e-13, **Hessian index 1** |
| table + file at ρ0 = 3 | +2.3e-7 (equal magnitude to table precision, opposite sign) |
| fix | 63C, ρ0 = 3 cell: `495.356854[1]` → `-495.356854[1]` |

A Morse cluster energy is a sum of pair terms that are each ≥ −1 and are positive only for pairs compressed below the equilibrium distance. A positive total for a 63-atom stationary point would need a heavily compressed structure, and every other cell on the page is negative. The posted file gives the same magnitude with a negative sign, and it lands on a stationary point whose index is exactly the bracketed [1]. So this is a dropped minus sign, not a wrong structure. The Oxford mirror (`doye.chem.ox.ac.uk/jon/structures/Morse/tables.html`) shows the same `495.356854[1]` cell.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh                 # (A) CCD LJ tables + 6 CCD files (~0.2 MB), then (B) Morse table + 63C file (~0.2 MB); a few seconds
sh verify-it-yourself/run_checks.sh --with-sources  # (A) also the Nankai 2004 archive (4.6 MB) and Barron 2005 PDF (hash)
```

The script prints each file's sha256 and Last-Modified and flags any change since `SOURCES.csv`. **(A)** It parses the LJ table rows and their hrefs, counts atoms and computes the LJ energy of each posted file in pure Python. **(B)** It reads the Morse ρ0 column headers and the 63C row, and checks that the ρ0 = 3 cell is the only positive cell on the page. It checks the posted file against the ρ0 = 6 cell, relaxes it at ρ0 = 3 (L-BFGS, then Newton with the six rigid-body modes shifted out) and counts the negative Hessian eigenvalues from the inertia of an LDL^T factorisation. All of this runs in pure Python. The script prints `FAIL` if a check no longer holds, for example after the CCD fixes the rows. Our own output is in `how-we-built-it/repro_output_2026-10-17.txt`, and the LJ tight-polish numbers are in `how-we-built-it/tight_polish_2026-10-17.txt`.

## Sources (no CCD data is shipped)

Fetched 2026-10-17 (CEST). Full list with sizes: `SOURCES.csv`.

| URL | sha256 | Last-Modified |
|---|---|---|
| https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/LJ/LJ310-561.html | 3e8d5141e2e731600337cdab88a435b44467130a840190d6b7a1e615f41847f4 | Thu, 25 Jul 2024 14:44:28 GMT |
| https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/LJ/LJ562-1000.html | 5afa46bfc46fad0d78f24617dacb48864de565406a31f533c85d9ec70fb75967 | Thu, 25 Jul 2024 14:44:28 GMT |
| https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/LJ/LJ562-1000/601.TXT | b0bb11e9d42d83b6cdc5ec92e20b978227b8cf1c9f6f029b81c7481152f48dd9 | Thu, 25 Jul 2024 14:44:20 GMT |
| https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/LJ/LJ562-1000/602.TXT (not linked) | 9c7b80219a96e1552d2bf8521f2cdd98b1eb45939a5011dc1b74195bb9858043 | Thu, 25 Jul 2024 14:44:13 GMT |
| https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/LJ/LJ310-561/486.TXT | 9c5a587086f2e244f5cecda6b6714b1dea7cb8b1bd727e44016704e14d96b2dc | Thu, 25 Jul 2024 14:44:34 GMT |
| https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/LJ/LJ310-561/487.TXT | 15b077fb30922f31fdc1808c630766ed7af0e20f6bc2f40fc34d5d6de02f573c | Thu, 25 Jul 2024 14:44:33 GMT |
| https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/LJ/LJ562-1000/813.TXT | 51f22dc726c20976b326bb0904d69cf1548c31b4acd131732423086442b05119 | Thu, 25 Jul 2024 14:44:16 GMT |
| https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/LJ/LJ562-1000/899.TXT | 00b63b42e176f49aaffa4d055498d71ed798e04c2c76b23bcefd32b61f7d77d8 | Thu, 25 Jul 2024 14:44:17 GMT |
| https://chinfo.nankai.edu.cn/chmm/pubmats/LJ/LJ562-1000.tar.gz (member `./LJ562-1000/602.TXT` = sha256 9c7b8021…8043) | f8b6dabd5b57ca7476ca405cbd927072e739049904e630c28a2d70387d47b958 | Thu, 25 May 2023 09:22:15 GMT |
| https://chinfo.nankai.edu.cn/chmm/pubmats/LJ/LJ310-561.tar.gz | ca19988b0aef36c073ac3f1e3b19cd79cd7ff3579979ff5d9fd29a8a12fd0548 | Thu, 25 May 2023 09:22:15 GMT |
| https://academicos.azc.uam.mx/cbr/PDF/MSSEMSCO_CBR_tables.pdf (Barron 2005, Tables 18–27 "minimum" column) | 7316df2d8f584609e2cf3480db7ced69dfbb33354d8a5af6985684c5edc7adb8 | Mon, 09 May 2005 21:38:15 GMT |
| https://academicos.azc.uam.mx/cbr/LennardJones/nw537-548.htm (Barron: "813 IC −5712.2517 (old −5712.2506)") | b15a9cd470ffb0b6c178dad3a927c471159a7b703278ef2b992c75191b4cbb55 | Tue, 06 Jul 2010 00:13:16 GMT |
| https://www-wales.ch.cam.ac.uk/~jon/structures/Morse/tables.html (B) | fe78ecc8ffd9a85dba2968d34c3a2d726ffdd429cfe77d643ab00bfa838f475b | Mon, 26 Feb 2018 16:56:59 GMT |
| https://www-wales.ch.cam.ac.uk/~jon/structures/Morse/points/63C (B) | 30d9aaabfa6b985ac40d5e4227df9bdd276df748061c024411a2d41382d94a27 | Mon, 04 Nov 1996 16:55:27 GMT |
| https://doye.chem.ox.ac.uk/jon/structures/Morse/tables.html (B, mirror; same 63C cell) | 2e435e3efdb13b720b39b3b8b2b74352b3f3b8f1934b932c9fbb96a9380173d5 | Tue, 04 Mar 2025 09:59:41 GMT |

## Not claimed

- **No new minimum and no record.**
  - (A) Every lower LJ value in this package is already published:
    - N = 486, 487, 899: Barron's 2005 tables list exactly the file energies (−3278.672947, −3285.966242, −6371.011483).
    - N = 813: Barron publishes −5712.251749 (lower than the CCD file) and lists the file's −5712.2506 as the earlier value.
    - The four CCD files are byte-identical to the original authors' 2004 archive (Xiang, Cheng, Cai, Shao; J. Phys. Chem. A 108, 3586 (2004) and 108, 9516 (2004)).
  - (B) 63C is a sign correction to the table's own number. We do not claim a new or lower 63C energy.
- We do not claim that the structures are global minima. We claim only that each table entry disagrees with its own linked file (A) or with its own sign (B).
- We say nothing about why the entries differ beyond what is dated above.
- **Novelty is not established.** The CCD has no public errata, history or pending-corrections page. Not finding a public report does not prove these errata are unreported. We file them as data-integrity errata with that caveat, and their novelty is unconfirmed.
- No claim about any other CCD row. (A) A full scan of N = 2–150 and 310–1000 found no other LJ table-vs-file disagreement above convergence level (|Δ| ≲ 2e-5). (B) For the Morse table we claim only the 63C sign. A dropped minus sign elsewhere would show up as a positive cell, and 63C at ρ0 = 3 is the only positive cell on the page.
- Open question for the maintainers, not claimed: for eight Morse (label, ρ0) cells (31D ρ0 = 3, 47A ρ0 = 10, 66B ρ0 = 3, 70B ρ0 = 6, 75B ρ0 = 3, and 147A ρ0 = 6, 10, 14), we could not reproduce the table value from the posted file. In each case the file's structure does not survive as a minimum at that ρ0, so the value depends on how it was relaxed. We make no claim about these cells.

## Credits

- Finding and package: MrxMoex@Grok_Fleet.
- Structures and tables: the Cambridge Cluster Database (D. J. Wales, J. P. K. Doye and co-workers). LJ N = 310–1000 rows provided by X. Shao's group (Y. Xiang, H. Jiang, L. Cheng, W. Cai, X. Shao, J. Phys. Chem. A 108, 3586 (2004) and 108, 9516 (2004)). Morse table: J. P. K. Doye and D. J. Wales.
- Barron 2005 tables: C. Barrón-Romero, companion tables to "Minimum search space and efficient methods for structural cluster optimization", arXiv:math-ph/0504030.
- Related: the CCD Morse 32E file-swap erratum (#240).
- The CCD maintainers have not been contacted.
