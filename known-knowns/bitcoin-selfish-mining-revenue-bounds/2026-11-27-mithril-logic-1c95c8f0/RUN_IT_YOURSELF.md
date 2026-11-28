# Run it yourself

Fresh shell, from this package folder (python3 only):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected: a line `ok:` for every object file hash, `CERT_OK` (printed and corrected variants) for the T = 2000 headline certificate with max residual g = -29177/5497558138880, `CERT_OK` for the T = 250 certificate (g = -82708181/21990232555520), `CERT_FAIL` for each negative control, `POLICY_GAIN_POSITIVE` for the exact policy at the old point, and the final line `PASS`. The headline certificate is stored as 32 parts object/parts/upper_a45_T2000_rho67005787.txt.gz.part00 .. part31; the checker concatenates them in name order.

To check one file by hand: `cat object/parts/upper_a45_T2000_rho67005787.txt.gz.part* > joined.txt.gz; sha256sum joined.txt.gz` (expect 1c95c8f035bc8fb8f68e5a86fb8bf9fc3db6b6eed8383881ca63db959aec2f0f), then `python3 verify-it-yourself/check_cert.py joined.txt.gz both`.

Rebuild the object (numpy; about 20 s for the headline certificate): `cd how-we-built-it && nice python3 code/mkcert.py 9/20 2000 67005787/100000000 max c2.txt.gz 0.98`; the decompressed bytes (`zcat c2.txt.gz | sha256sum`) must equal 1d816e719eed5ac8cde09f0b5f1d32fde2807e09ae68e3156aab1851252c59f3 (the gzip bytes differ only by the time stamp in the gzip header).

Format: gzip text; line 1 a JSON header (alpha, rho, T, scale_log2 = 40); then T+1 lines, line a holding the integers H[a][0..T]; bias h(a,h,f) = H[a][h] / 2^40 for every fork label f. A skeptic should rebuild N_rho^T from the paper's Table 1, Sec. 4.2, and the corrected compensations derived in how-we-built-it/CLAIM.md, not from our checker.
