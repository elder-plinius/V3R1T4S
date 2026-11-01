# Run it yourself

Quick check (about 3 to 15 minutes; Python with mpmath, .NET SDK, POSIX shell, network):

```sh
sh verify-it-yourself/run_checks.sh
```

Individual steps, in a scratch folder `W` (the script does exactly steps 1-6; sources in `object/LebVerifyI`, tools in `object/tools`):

```sh
# 1  inputs (pinned commit da956b117a5f876fc3c530db3e00673e6cb18865 of github.com/Ujjwal238/universal-cover-problem; sha256 checked)
python verify-it-yourself/fetch_inputs.py W/work           # cert_B_08344.bin sha256 33973342ab754dd5261b682d657e0b46b55f3377173a9238a2fa3948fefdb91f, certB_test.bin
# 2  build
cd W && cp -r <package>/object/LebVerifyI <package>/object/tools . && (cd LebVerifyI && dotnet build -c Release -o ../dbin)
# 3  interval type containment test
dotnet dbin/LebVerify.dll ivtest 20000 outputs/ivtest_records.txt 7 && python tools/ivtest_check.py outputs/ivtest_records.txt     # expect: violations: 0
# 4  negative controls (valid author control + 14 tampered copies)
python tools/make_tampers.py work/certB_test.bin
for f in work/certB_test.bin work/tamper/*.bin; do dotnet dbin/LebVerify.dll verify $f --threads 1 --claim none; done   # valid: RESULT VERIFIED; all others refused / VERIFICATION FAILED
# 5  1% deterministic slice of the real certificate
dotnet dbin/LebVerify.dll verify work/cert_B_08344.bin --threads 6 --claim 8344/10000 --sample 0.01 --sseed 3             # expect: leaves 2,897,141, failing leaves 0, RESULT: SLICE OK
# 6  (optional) regenerate the interval constants: must reproduce object/LebVerifyI/IvConsts.cs byte for byte
mkdir -p LebVerifyI && python tools/gen_ivconsts.py        # writes LebVerifyI/IvConsts.cs in the current folder; compare with cmp
# 7  FULL replay (about 2.5 h wall on 5-6 threads at low priority, 1.1 GB RAM, checkpointed: rerun the same command to resume)
dotnet dbin/LebVerify.dll verify work/cert_B_08344.bin --threads 5 --claim 8344/10000 --ckpt work/full_ckpt.tsv --leaflog work/full_leaflog.txt --leafmod 200 > outputs/full_run.log
tail -3 outputs/full_run.log     # expect: RESULT VERIFIED  (interval mode)  a >= 0.8344 nodes 486,799,600 leaves 245,496,952 failing 0
```

Recorded outputs of the original full run: `object/records/full_run.log`, `object/records/full_summarize.txt`, `object/records/full_ckpt.tsv.gz` (3,596 job rows; a re-run must reproduce them byte for byte). Agreement with an earlier binary64 verifier on a 10% job sample: `object/records/cmp_new_vs_old.txt`. Operation-by-operation audit of the arithmetic: `object/INTERVAL_AUDIT.md`. Lemma layer: `object/LEMMAS.md` and `object/lemma_checks/`.
