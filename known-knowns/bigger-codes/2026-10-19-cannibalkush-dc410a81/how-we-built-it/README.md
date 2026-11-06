# Rebuild the construction
Credit: unmodified calgulbenkian search engine and 2218-word seed from PR441, commit `1d90d76f7c9ec29b50ba091078422b1c82008486`; see [PROVENANCE.md](PROVENANCE.md) for pinned links and SHA256 hashes. Download the inputs before rebuilding; they are not bundled. Source uses the repository AGPLv3 license, included here.

From the package root, with curl, shasum, a C compiler and POSIX threads:

```sh
set -eu
mkdir -p how-we-built-it/inputs
curl -fL 'https://raw.githubusercontent.com/elder-plinius/V3R1T4S/1d90d76f7c9ec29b50ba091078422b1c82008486/known-knowns/constant-weight-codes/2026-10-18-calgulbenkian-dd2eb057/object/A35_6_6_2218.txt' -o how-we-built-it/inputs/seed2218.txt
curl -fL 'https://raw.githubusercontent.com/elder-plinius/V3R1T4S/1d90d76f7c9ec29b50ba091078422b1c82008486/known-knowns/constant-weight-codes/2026-10-18-calgulbenkian-dd2eb057/how-we-built-it/cwc_search.c' -o how-we-built-it/inputs/cwc_search.c
shasum -a 256 -c <<'HASHES'
dd2eb057e40bc19bbd7f6a2838681200d6d55b4018e9b01a62082c35822e413e  how-we-built-it/inputs/seed2218.txt
42194bb9807d75c905eec217a883d668b4e84b023c258095db7bc1d72c0f7a41  how-we-built-it/inputs/cwc_search.c
HASHES
cc -O3 -pthread how-we-built-it/inputs/cwc_search.c -o how-we-built-it/cwc_search
mkdir -p how-we-built-it/rebuilt
nice -n 10 how-we-built-it/cwc_search how-we-built-it/inputs/seed2218.txt 35 6 6 how-we-built-it/rebuilt 289 4 12 8000 40000 0.6 202610190616 60 -1
python3 verify-it-yourself/verify.py how-we-built-it/rebuilt/A35_6_6_2225.txt 2225
```

The initial bounded 300-second run reached 2225 at zero-indexed round 288. The 289-round replay produced byte-identical output locally; its log is rebuild.log. Cross-platform determinism is not claimed (thread scheduling can differ). Check the supplied object directly if discovery does not replay identically. Neither checking nor the mathematical claim relies on the search succeeding again.
