# Run it yourself

One command from this folder (Python with mpmath, .NET SDK, POSIX shell; network the first time):

```sh
sh verify-it-yourself/run_checks.sh
```

The individual steps, in a scratch folder `W` (the script does exactly this; scripts live in `object/scripts`, the program in `object/ZengCheck`, tables in `object/tables`):

```sh
python -c "import zipfile;zipfile.ZipFile('certificate.zip').extractall('work')"      # certificate.zip: Zenodo 10.5281/zenodo.20528351, md5 73b400c8c3b30f74fa9d6e971a5ddc65
python scripts/table_check.py tables/tables_b.txt                                      # expect: enclosure violations 0
python scripts/reduction_check.py                                                      # far-field margins with exact vertex radii (both positive)
(cd ZengCheck && dotnet build -c Release -o ../dbin)
dotnet dbin/ZengCheck.dll selftest out/iv_selftest.txt 20000 && python scripts/iv_selftest.py out/iv_selftest.txt   # expect: violations 0
dotnet dbin/ZengCheck.dll --cert work/certificate --tables tables/tables_b.txt --excl tables/author_exclusions.json --parts r3_collar,r5_collar,core5d --threads 8 --out out/final2.jsonl
dotnet dbin/ZengCheck.dll verdict --cert work/certificate --out out/final2.jsonl --verdict out/final2_verdict.txt
python scripts/make_tamper.py && python scripts/run_controls.py dbin/ZengCheck.dll tables/tables_b.txt --excl tables/author_exclusions.json
```

Expected: `TOTAL leaves=6746392 failing=0 worst_slack_over_0.834=1.551089E-009` and `VERDICT: ACCEPT`; every tamper prints REJECT.
Optional (about 21 minutes, one thread): `python scripts/integrity.py work/certificate out/integrity.json` recomputes record_sha256 of all 6,747,165 records and the shard-set hash (it prints `shard_hash_ok False`: defect D1, the hash only matches with the `shards/` path prefix; `python scripts/hash_check.py work/certificate` shows both).
Without `--excl`, 2,354 core leaves are reported failing: they pass only with the second polygon variant (see README, Not claimed).
How the object was produced: `how-we-built-it/` (pre-registration, hypotheses, report). Recorded outputs of the original run: `object/records/`.
