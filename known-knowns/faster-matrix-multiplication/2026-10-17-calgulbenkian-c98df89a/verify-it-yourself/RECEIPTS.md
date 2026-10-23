# Verification Receipts (`2026-10-17-calgulbenkian-c98df89a`)

Command run from package root (`2026-10-14T03:55:00Z`, macOS, Python 3.9.6):

```sh
sh verify-it-yourself/run_checks.sh
```

Output:
```text
== Checking object/2x4x7_m45_cr164_fv50_cn282_ZT_reduced.json
sha256 matches INDEX.csv (c98df89a60c52bfd65c3266489f3cbef4a28715305d200e2a3f01334d1076429)
PASS: 2x4x7_m45_cr164_fv50_cn282_ZT_reduced.json | format=2x4x7 m=45 cr=164 (U=27, V=64, W=73) fv=50 cn=282
cr 164 matches INDEX.csv
== Running negative control (mutated SLP coefficient must FAIL)
negative control rejected as expected
ALL CHECKS PASS
```

| File | Format | Rank `m` | Reduced Additions (`cr`) | Fresh Vars (`fv`) | Naive Additions (`cn`) | Brent Monomials Verified | SHA-256 Matches `INDEX.csv` | Verdict |
|---|---|---|---|---|---|---|---|---|
| `object/2x4x7_m45_cr164_fv50_cn282_ZT_reduced.json` | `(2, 4, 7)` | `45` | **`164`** | `50` | `282` | `3,136` | yes | `PASS` |
