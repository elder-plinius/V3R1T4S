# How We Built It (`post-tag-busy-beaver-bbpt`: Exact `BB_PT(8) = 19`)

## Pinned Requirements
- `python3 >= 3.8` (standard library only; zero external dependencies) for both certificate generation (`build_bbpt8_certificate.py`) and verification (`verify-it-yourself/verify_bbpt8.py`).

## Exact Commands to Rebuild and Verify
```sh
python3 how-we-built-it/build_bbpt8_certificate.py
sh verify-it-yourself/run_checks.sh
```
