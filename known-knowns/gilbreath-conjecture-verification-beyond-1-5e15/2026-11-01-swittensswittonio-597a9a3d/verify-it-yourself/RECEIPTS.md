# Receipts: real output of `sh verify-it-yourself/run_checks.sh` (run by the author, 2026-11-01)
```
step 1: hashes
files hashed 23 bad 0
step 2: consistency
ok:   46567 windows numbered consecutively from 0
ok:   window start values follow lo = 1500000000000001 + 2*2^30*w
ok:   cumulative primes 2859087706237 == RESULT total_primes
ok:   blocks 349009729 == RESULT blocks (carry rule reproduced)
ok:   depth histogram sums to the number of blocks
ok:   max depth 783 == max over windows 783 == RESULT 783
ok:   every depth < overlap 1536 (no flagged block)
ok:   RESULT: blocks whose owned row-1280 entries are not all in {0,2}: 0
ok:   95/95 recorded primecount checks equal the sieved cumulative counts
ok:   85208 sampled first primes at blocks 0, 4096, 8192, ... in increasing order
ok:   range reaches beyond 1.6e15
PASS
step 3: recompute sample blocks
block=0 first_prime=1500000000000013 first_is_prime=True depth_claimed=141 depth_recomputed=141 ok=True
block=20480017 first_prime=1505863000349507 first_is_prime=True depth_claimed=175 depth_recomputed=175 ok=True
block=39941245 first_prime=1511434955855921 first_is_prime=True depth_claimed=165 depth_recomputed=165 ok=True
block=58211795 first_prime=1516666535257303 first_is_prime=True depth_claimed=175 depth_recomputed=175 ok=True
block=124951218 first_prime=1535781052271849 first_is_prime=True depth_claimed=184 depth_recomputed=184 ok=True
block=158982926 first_prime=1545530539684819 first_is_prime=True depth_claimed=181 depth_recomputed=181 ok=True
block=168895663 first_prime=1548370693624259 first_is_prime=True depth_claimed=177 depth_recomputed=177 ok=True
block=192291085 first_prime=1555074435602483 first_is_prime=True depth_claimed=155 depth_recomputed=155 ok=True
block=206463935 first_prime=1559135939585891 first_is_prime=True depth_claimed=185 depth_recomputed=185 ok=True
block=215859283 first_prime=1561828517755841 first_is_prime=True depth_claimed=769 depth_recomputed=769 ok=True
block=261200146 first_prime=1574824481328151 first_is_prime=True depth_claimed=759 depth_recomputed=759 ok=True
block=269482130 first_prime=1577198664005623 first_is_prime=True depth_claimed=236 depth_recomputed=236 ok=True
block=344321659 first_prime=1598657386774249 first_is_prime=True depth_claimed=203 depth_recomputed=203 ok=True
block=344572324 first_prime=1598729274569041 first_is_prime=True depth_claimed=783 depth_recomputed=783 ok=True
block=349009728 first_prime=1600001870532427 first_is_prime=True depth_claimed=207 depth_recomputed=207 ok=True
blocks checked 15 mismatches 0
PASS
PASS
```
