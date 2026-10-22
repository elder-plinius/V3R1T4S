# Carried entry r0202-broker/PRIMARY (PREREG rule 8)

Frozen in run 2026-10-18-0202 at 2026-10-18T03:14:07Z (its freeze record: ../../FROZEN.md, the ROLE=PRIMARY record of lens broker). It was developed there on validation data cut from training-0.50 only and was never scored on test there at 0.50.
Byte-copied into this run by the main session; code tree hash re-verified against that record:
code_tree_sha256=e0e12da3febeabfd8eb1818560c8655ead2d2179ea78481e83bd6126d3620eec
results_tree_sha256 (run 0202 record) = 9680435ec5ccc879b9d38a5fc8832dcf888b62ff1465a4fc4e9dab67fa34e209
The val/0.50 result files here are byte copies of the frozen ones (sha256 listed in the record). The test/0.50 result files were produced in this run by the main session with tools/q15h.py run --mode test --props 0.50 (log run_test_0.50.txt) and checked with the test-mode audit (audit_test_0.50.txt); they are not in the 0202 record, so their sha256 are listed here:
49199b962360449425fd2839bc12c267bdf55d99443e4040af054a9d41d15f8d  test/0.50/bantubvd/result-0.50.tsv
42e2fc74b7c60ed9bc3269c0a6bfdf0873d10fd67b7f37c7cdeb1a33e5a34181  test/0.50/beidazihui/result-0.50.tsv
e9efa86d9a9e5db9919a67b3a7da6ca12d3ebe68098cb2d1dbdca1602a868f87  test/0.50/birchallchapacuran/result-0.50.tsv
7c15eb63a7a113ba5c2b09b166e21b806622ddac074a60095137157d04e33544  test/0.50/bodtkhobwa/result-0.50.tsv
8ea90ff81861ac57f7eb245420c0471b86e6cb95f5a5821115424e247c838af2  test/0.50/bremerberta/result-0.50.tsv
57698791aa4081c0887930e9b977312b000c6a552d8529cfd812fdcfa31b829f  test/0.50/deepadungpalaung/result-0.50.tsv
8c043ea1cf909e261a35c85289fb8dbddd43b9f2edeeb1fa0ca09a8fe5229341  test/0.50/hillburmish/result-0.50.tsv
eb14c7f33674cfe0e02412106f65064d0a6aad110983ac8357b4d49a139ea70c  test/0.50/kesslersignificance/result-0.50.tsv
578e0ea7c2f1daeedb93185c18b5894445248b7a1711a3f012f04e947242eae1  test/0.50/luangthongkumkaren/result-0.50.tsv
d833de839b1f12904172740f0ecea2e7e836850a0d0f0f754fb4cf12e4e227c8  test/0.50/wangbai/result-0.50.tsv

See also rules/carry_setup.out and rules/carry_entries.json (paths scrubbed to WORKDIR).
