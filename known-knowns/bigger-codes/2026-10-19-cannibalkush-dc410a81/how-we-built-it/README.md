# Rebuild the construction
Credit: unmodified calgulbenkian search engine and 2218-word seed from PR441, commit1d90d76f7c9ec29b50ba091078422b1c82008486; see PROVENANCE.md. Source is distributed under the repository AGPLv3 license, included here.

From the package root, with a C compiler and POSIX threads:

```sh
cc -O3 -pthread how-we-built-it/cwc_search.c -o how-we-built-it/cwc_search
mkdir -p how-we-built-it/rebuilt
nice -n 10 how-we-built-it/cwc_search how-we-built-it/seed2218.txt 35 6 6 how-we-built-it/rebuilt 289 4 12 8000 40000 0.6 202610190616 60 -1
python3 verify-it-yourself/verify.py how-we-built-it/rebuilt/A35_6_6_2225.txt 2225
```

The initial bounded 300-second run reached 2225 at zero-indexed round 288. The 289-round replay produced byte-identical output locally; its log is rebuild.log. Cross-platform determinism is not claimed (thread scheduling can differ). Check the supplied object directly if discovery does not replay identically. Neither checking nor the mathematical claim relies on the search succeeding again.
