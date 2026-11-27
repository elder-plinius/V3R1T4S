# How We Built the Certificate

Requirements: an ISO C99 compiler (`cc`) with 128-bit integer support (`__int128`) and Python 3.8+ standard library (`fractions`, zero third-party packages).

From the package root folder, regenerate `object/lcm_lower_bound_certificate.tsv` from scratch in approximately `6` seconds (`NUMERICAL`):

```sh
WORK=$(mktemp -d)
cc -O3 -std=c99 how-we-built-it/generate_raw_certificate.c -lm -o "$WORK/gen_raw"
"$WORK/gen_raw" "$WORK/raw_cert.tsv"
python3 how-we-built-it/enrich_exact_fractions.py "$WORK/raw_cert.tsv" "$WORK/rebuilt_cert.tsv"
cmp -s "$WORK/rebuilt_cert.tsv" object/lcm_lower_bound_certificate.tsv && echo "IDENTICAL"
rm -rf "$WORK"
```

Note that `generate_raw_certificate.c` uses floating-point search only to propose candidate integer cap numerators `m_i` (where `C_i = m_i / 32`). Every proposed row is then converted to an exact reduced rational fraction by `enrich_exact_fractions.py` and verified independently with zero floating-point operations by both `verify-it-yourself/verify_lcm_bound_c.c` and `verify-it-yourself/verify_lcm_bound_py.py`.
