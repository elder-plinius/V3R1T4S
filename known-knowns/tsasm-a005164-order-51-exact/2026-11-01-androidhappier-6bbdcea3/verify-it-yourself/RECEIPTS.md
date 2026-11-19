# Receipts: real output of verify-it-yourself/run_checks.sh

Run from a clean copy of this folder on 2026-11-01 at about 03:14Z (Python 3.13.5, one core, 63 s wall clock).
The command was `sh verify-it-yourself/run_checks.sh`. Exit status 0.

```
== 1. sha256 of object/A005164_25.txt
got  6bbdcea3372a91c60f07506f99ec6b9660bc885517e741f43460352421d6b745
want 6bbdcea3372a91c60f07506f99ec6b9660bc885517e741f43460352421d6b745
sha256: match
== 2. brute force from the definition: fixtures, then a(0..8)
fixture pos (order-5 TSASM): True
fixture neg1 (identity 3, ASM not TSASM): True False
fixture neg2 (symmetric non-ASM): False
a(0) order 1: 1
a(1) order 3: 1
a(2) order 5: 1
a(3) order 7: 2
a(4) order 9: 4
a(5) order 11: 13
a(6) order 13: 46
a(7) order 15: 248
a(8) order 17: 1516
== 3. exact height-function DP, n = 0..25 (about 1-3 minutes)
0 1
1 1
2 1
3 2
4 4
5 13
6 46
7 248
8 1516
9 13654
10 142873
11 2156888
12 38456356
13 974936056
14 29540545024
15 1259111024288
16 64726478396896
17 4641989615977216
18 404396533544588344
19 48825344233129714772
20 7202552030561982627472
21 1464587581921220811285325
22 365627222082497915618219716
23 125253905685915522767942493032
24 52893528399758443649956432899616
25 30533896243799704017627552102998416
== 4. compare: DP vs brute force (n<=8), DP vs published a(0..24), DP a(25) vs the object
brute-force fixtures behave as expected: True
DP == brute force for n=0..8: True
DP == published a(0..24): True
object a(25) = 30533896243799704017627552102998416
DP     a(25) = 30533896243799704017627552102998416
object == DP a(25): True
PASS
```
