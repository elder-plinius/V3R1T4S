# Current wrapper receipt (2026-10-15)

Real end-to-end run on Linux x86_64, Python 3.12.14, NumPy 2.3.5.
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1`; exit code **0**.
Release inputs and checker sources were fetched from upstream commit
`371938deefd77b9e6a95d2a0c3e2d3c6ead7eaac` and verified against its Git blob IDs.
These are actual scientific checker outputs, not synthetic fixture output.

All 30 original release codes and five Delsarte certificates ran. Contributed sibling packages are outside this wrapper’s scope.

Command (from this family directory, with the stated Python environment):

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 sh verify-it-yourself/run_checks.sh
```

Exact source and output SHA-256:

- `run_checks.sh`: `044bf318743ee59dd5c4d77a8da46a905304e34de7c76dd79cae86615d86b598`
- `known-knowns/check_harness_contract.py`: `f0f43ba4ab6970001f228affb5a95f9ec5d37b115f8487c7ce4cc11ce9e5a070`
- Raw combined stdout/stderr below: `2015d2ad3e893904ed80bb913b127503b0a1d4323ddb4ff2c29093642d7a437a`

## Complete current output

```text
HARNESS INVENTORY PASS codes=30 certificates=5
== codes/A25_6_11_8718.txt
sha256 verified by inventory preflight
file=A25_6_11_8718.txt sha256=fb5145c3b40d3ac0a67a539bce0fa075f6a2d98f9c635932bc7309ee78d1d7ae
F format: lines=8718 claimed_M=8718 bad_lines=0
W weight/distinct: bad_weight=0 distinct=8718
A all-pairs: words=8718 pairs=37997403 expected=37997403 min_distance=6 need>=6 histogram={6: 655839, 8: 2641714, 10: 7936494, 12: 11930619, 14: 9497165, 16: 4316579, 18: 915828, 20: 100181, 22: 2984}
B packing: t=9 subsets=479490 distinct=479490 collisions=0
VERDICT: VALID  A(25,6,11) >= 8718
== codes/A25_6_12_9895.txt
sha256 verified by inventory preflight
file=A25_6_12_9895.txt sha256=b2631ed9296e9a0622a535edaba582a715520fe06af36de4d51cd1cf18698519
F format: lines=9895 claimed_M=9895 bad_lines=0
W weight/distinct: bad_weight=0 distinct=9895
A all-pairs: words=9895 pairs=48950565 expected=48950565 min_distance=6 need>=6 histogram={6: 709526, 8: 3267105, 10: 9474200, 12: 15127248, 14: 12715381, 16: 5959697, 18: 1521614, 20: 162830, 22: 12916, 24: 48}
B packing: t=10 subsets=653070 distinct=653070 collisions=0
VERDICT: VALID  A(25,6,12) >= 9895
== codes/A26_6_11_12222.txt
sha256 verified by inventory preflight
file=A26_6_11_12222.txt sha256=0637a3a3ee1fa65d5230bacbf14fb7a88c56a047fc5a24db614ccd795e488961
F format: lines=12222 claimed_M=12222 bad_lines=0
W weight/distinct: bad_weight=0 distinct=12222
A all-pairs: words=12222 pairs=74682531 expected=74682531 min_distance=6 need>=6 histogram={6: 866973, 8: 4282053, 10: 13439615, 12: 22423911, 14: 20490869, 16: 10203332, 18: 2650288, 20: 315054, 22: 10436}
B packing: t=9 subsets=672210 distinct=672210 collisions=0
VERDICT: VALID  A(26,6,11) >= 12222
== codes/A26_6_13_16225.txt
sha256 verified by inventory preflight
file=A26_6_13_16225.txt sha256=be7b1c9464c67bc9cac8c175214c607291cb427e127534b30994b29eff4f274e
F format: lines=16225 claimed_M=16225 bad_lines=0
W weight/distinct: bad_weight=0 distinct=16225
A all-pairs: words=16225 pairs=131617200 expected=131617200 min_distance=6 need>=6 histogram={6: 1254872, 8: 6429365, 10: 20971400, 12: 37660170, 14: 37071277, 16: 20643831, 18: 6516225, 20: 997168, 22: 69717, 24: 2825, 26: 350}
B packing: t=11 subsets=1265550 distinct=1265550 collisions=0
VERDICT: VALID  A(26,6,13) >= 16225
== codes/A26_6_8_3603.txt
sha256 verified by inventory preflight
file=A26_6_8_3603.txt sha256=bd239ef369bb94ca6af15162cf2790b7848640adf01ffae05a4a099d7ae7b509
F format: lines=3603 claimed_M=3603 bad_lines=0
W weight/distinct: bad_weight=0 distinct=3603
A all-pairs: words=3603 pairs=6489003 expected=6489003 min_distance=6 need>=6 histogram={6: 270655, 8: 861684, 10: 2099301, 12: 2092703, 14: 1001502, 16: 163158}
B packing: t=6 subsets=100884 distinct=100884 collisions=0
VERDICT: VALID  A(26,6,8) >= 3603
== codes/A26_6_9_5986.txt
sha256 verified by inventory preflight
file=A26_6_9_5986.txt sha256=b09c1c5d9772aae336ca2ba29e4c3e25c6346299aabcd677008d08f0749308cf
F format: lines=5986 claimed_M=5986 bad_lines=0
W weight/distinct: bad_weight=0 distinct=5986
A all-pairs: words=5986 pairs=17913105 expected=17913105 min_distance=6 need>=6 histogram={6: 421262, 8: 1588691, 10: 4594425, 12: 5897900, 14: 4035336, 16: 1236594, 18: 138897}
B packing: t=7 subsets=215496 distinct=215496 collisions=0
VERDICT: VALID  A(26,6,9) >= 5986
== codes/A27_6_9_8325.txt
sha256 verified by inventory preflight
file=A27_6_9_8325.txt sha256=d6b278e96ded45c784f351c80dff216c65dba8173d63bb4d2e96b1602c33df3e
F format: lines=8325 claimed_M=8325 bad_lines=0
W weight/distinct: bad_weight=0 distinct=8325
A all-pairs: words=8325 pairs=34648650 expected=34648650 min_distance=6 need>=6 histogram={6: 617721, 8: 2707722, 10: 8094927, 12: 11450984, 14: 8537390, 16: 2868733, 18: 371173}
B packing: t=7 subsets=299700 distinct=299700 collisions=0
VERDICT: VALID  A(27,6,9) >= 8325
== codes/A27_8_10_1737.txt
sha256 verified by inventory preflight
file=A27_8_10_1737.txt sha256=5a9ef07f5d958179ac069f546c43914147ac041f0c10e80a2229ea3d1287a05f
F format: lines=1737 claimed_M=1737 bad_lines=0
W weight/distinct: bad_weight=0 distinct=1737
A all-pairs: words=1737 pairs=1507716 expected=1507716 min_distance=8 need>=8 histogram={8: 178748, 10: 120292, 12: 676151, 14: 243018, 16: 261100, 18: 24402, 20: 4005}
B packing: t=7 subsets=208440 distinct=208440 collisions=0
VERDICT: VALID  A(27,8,10) >= 1737
== codes/A27_8_11_2421.txt
sha256 verified by inventory preflight
file=A27_8_11_2421.txt sha256=79e63d441921eda3444f3a4fe0601672c97c8df1f9f2a974fa5909f762afaf3a
F format: lines=2421 claimed_M=2421 bad_lines=0
W weight/distinct: bad_weight=0 distinct=2421
A all-pairs: words=2421 pairs=2929410 expected=2929410 min_distance=8 need>=8 histogram={8: 207403, 10: 371016, 12: 841504, 14: 899424, 16: 438521, 18: 150919, 20: 20032, 22: 591}
B packing: t=8 subsets=399465 distinct=399465 collisions=0
VERDICT: VALID  A(27,8,11) >= 2421
== codes/A28_8_11_3785.txt
sha256 verified by inventory preflight
file=A28_8_11_3785.txt sha256=c3160db5f409d2700e974d77503ac3806ac535ef052fb94f8558c92829c9fb91
F format: lines=3785 claimed_M=3785 bad_lines=0
W weight/distinct: bad_weight=0 distinct=3785
A all-pairs: words=3785 pairs=7161220 expected=7161220 min_distance=8 need>=8 histogram={8: 401362, 10: 787247, 12: 1908995, 14: 2293423, 16: 1221554, 18: 472236, 20: 73886, 22: 2517}
B packing: t=8 subsets=624525 distinct=624525 collisions=0
VERDICT: VALID  A(28,8,11) >= 3785
== codes/A28_8_12_4962.txt
sha256 verified by inventory preflight
file=A28_8_12_4962.txt sha256=02553ea43f9584446414c23dc611e751cbfb6a8f037e0c115d30aae43e6c5341
F format: lines=4962 claimed_M=4962 bad_lines=0
W weight/distinct: bad_weight=0 distinct=4962
A all-pairs: words=4962 pairs=12308241 expected=12308241 min_distance=8 need>=8 histogram={8: 624834, 10: 664097, 12: 4375813, 14: 2002032, 16: 3813788, 18: 465890, 20: 358805, 22: 136, 24: 2846}
B packing: t=9 subsets=1091640 distinct=1091640 collisions=0
VERDICT: VALID  A(28,8,12) >= 4962
== codes/A28_8_14_6359.txt
sha256 verified by inventory preflight
file=A28_8_14_6359.txt sha256=a4a88d0575c275884d3d34a25156a980f418a5ffd56bf0e188ecbe4a758a7d22
F format: lines=6359 claimed_M=6359 bad_lines=0
W weight/distinct: bad_weight=0 distinct=6359
A all-pairs: words=6359 pairs=20215261 expected=20215261 min_distance=8 need>=8 histogram={8: 1044569, 10: 1360267, 12: 5085109, 14: 5497439, 16: 4280773, 18: 2258684, 20: 606619, 22: 66753, 24: 14218, 26: 438, 28: 392}
B packing: t=11 subsets=2314676 distinct=2314676 collisions=0
VERDICT: VALID  A(28,8,14) >= 6359
== codes/A28_8_9_1406.txt
sha256 verified by inventory preflight
file=A28_8_9_1406.txt sha256=4912b21d4eed029dc861a85506f7a4bc10189106ae95793eaada8c1654d316cb
F format: lines=1406 claimed_M=1406 bad_lines=0
W weight/distinct: bad_weight=0 distinct=1406
A all-pairs: words=1406 pairs=987715 expected=987715 min_distance=8 need>=8 histogram={8: 104739, 10: 184784, 12: 305762, 14: 297614, 16: 78029, 18: 16787}
B packing: t=6 subsets=118104 distinct=118104 collisions=0
VERDICT: VALID  A(28,8,9) >= 1406
== codes/A29_6_10_25974.txt
sha256 verified by inventory preflight
file=A29_6_10_25974.txt sha256=5551204c40538f6b11e53e60414e417d5ff7d8c8c59b40a8185ddd59a9de9cd3
F format: lines=25974 claimed_M=25974 bad_lines=0
W weight/distinct: bad_weight=0 distinct=25974
A all-pairs: words=25974 pairs=337311351 expected=337311351 min_distance=6 need>=6 histogram={6: 2309765, 8: 13397058, 10: 49341137, 12: 96401531, 14: 101369564, 16: 57438721, 18: 15496556, 20: 1557019}
B packing: t=8 subsets=1168830 distinct=1168830 collisions=0
VERDICT: VALID  A(29,6,10) >= 25974
== codes/A29_6_11_41219.txt
sha256 verified by inventory preflight
file=A29_6_11_41219.txt sha256=505ba4d63b0faab9bf8a4e470cebb3111f5622a40985d3324a34a0b994ebee25
F format: lines=41219 claimed_M=41219 bad_lines=0
W weight/distinct: bad_weight=0 distinct=41219
A all-pairs: words=41219 pairs=849482371 expected=849482371 min_distance=6 need>=6 histogram={6: 3824405, 8: 24226819, 10: 97491644, 12: 210565525, 14: 257804615, 16: 177316998, 18: 65651397, 20: 11819436, 22: 781532}
B packing: t=9 subsets=2267045 distinct=2267045 collisions=0
VERDICT: VALID  A(29,6,11) >= 41219
== codes/A29_6_12_61823.txt
sha256 verified by inventory preflight
file=A29_6_12_61823.txt sha256=d467400b0827c8db81a1c9348317ca1d645c049d6cb54fdf5b927964490e4d2f
F format: lines=61823 claimed_M=61823 bad_lines=0
W weight/distinct: bad_weight=0 distinct=61823
A all-pairs: words=61823 pairs=1911010753 expected=1911010753 min_distance=6 need>=6 histogram={6: 6372782, 8: 42387302, 10: 181030245, 12: 421055053, 14: 567053897, 16: 443236523, 18: 196901932, 20: 47279753, 22: 5464441, 24: 228825}
B packing: t=10 subsets=4080318 distinct=4080318 collisions=0
VERDICT: VALID  A(29,6,12) >= 61823
== codes/A30_8_8_1166.txt
sha256 verified by inventory preflight
file=A30_8_8_1166.txt sha256=b4d9fdacd8a4d441b3025389d37026d77627a2ff234d76496a14b94ee11ef742
F format: lines=1166 claimed_M=1166 bad_lines=0
W weight/distinct: bad_weight=0 distinct=1166
A all-pairs: words=1166 pairs=679195 expected=679195 min_distance=8 need>=8 histogram={8: 112430, 10: 98687, 12: 303302, 14: 124157, 16: 40619}
B packing: t=5 subsets=65296 distinct=65296 collisions=0
VERDICT: VALID  A(30,8,8) >= 1166
== codes/A33_8_8_1809.txt
sha256 verified by inventory preflight
file=A33_8_8_1809.txt sha256=0a8e9c53dc656f46c45a5e2a50149612644132789219501aa3a32592643ee139
F format: lines=1809 claimed_M=1809 bad_lines=0
W weight/distinct: bad_weight=0 distinct=1809
A all-pairs: words=1809 pairs=1635336 expected=1635336 min_distance=8 need>=8 histogram={8: 184651, 10: 236946, 12: 683106, 14: 395000, 16: 135633}
B packing: t=5 subsets=101304 distinct=101304 collisions=0
VERDICT: VALID  A(33,8,8) >= 1809
== codes/A34_8_7_602.txt
sha256 verified by inventory preflight
file=A34_8_7_602.txt sha256=1a1d0958047e78b8d29752ccb0210518b170663b6862f84d57669c7b0c02d81e
F format: lines=602 claimed_M=602 bad_lines=0
W weight/distinct: bad_weight=0 distinct=602
A all-pairs: words=602 pairs=180901 expected=180901 min_distance=8 need>=8 histogram={8: 32414, 10: 44914, 12: 75763, 14: 27810}
B packing: t=4 subsets=21070 distinct=21070 collisions=0
VERDICT: VALID  A(34,8,7) >= 602
== codes/A34_8_8_1965.txt
sha256 verified by inventory preflight
file=A34_8_8_1965.txt sha256=125083e27d7b04aee88f0c271af7a8946cba376bb87948705f89a2edc6f95eb4
F format: lines=1965 claimed_M=1965 bad_lines=0
W weight/distinct: bad_weight=0 distinct=1965
A all-pairs: words=1965 pairs=1929630 expected=1929630 min_distance=8 need>=8 histogram={8: 196259, 10: 283369, 12: 785434, 14: 494881, 16: 169687}
B packing: t=5 subsets=110040 distinct=110040 collisions=0
VERDICT: VALID  A(34,8,8) >= 1965
== codes/A35_6_6_2217.txt
sha256 verified by inventory preflight
file=A35_6_6_2217.txt sha256=3bc77f117eb9ead8b3d35b6e9a610b8fd2cc183e14d71c2f42a7abe244371459
F format: lines=2217 claimed_M=2217 bad_lines=0
W weight/distinct: bad_weight=0 distinct=2217
A all-pairs: words=2217 pairs=2456436 expected=2456436 min_distance=6 need>=6 histogram={6: 133289, 8: 523000, 10: 1086270, 12: 713877}
B packing: t=4 subsets=33255 distinct=33255 collisions=0
VERDICT: VALID  A(35,6,6) >= 2217
== codes/A45_8_7_1907.txt
sha256 verified by inventory preflight
file=A45_8_7_1907.txt sha256=3572d00c548890628259491cbcd330950c5ad79d2797b3b14a1bbe224750fd6e
F format: lines=1907 claimed_M=1907 bad_lines=0
W weight/distinct: bad_weight=0 distinct=1907
A all-pairs: words=1907 pairs=1817371 expected=1817371 min_distance=8 need>=8 histogram={8: 141694, 10: 383793, 12: 783205, 14: 508679}
B packing: t=4 subsets=66745 distinct=66745 collisions=0
VERDICT: VALID  A(45,8,7) >= 1907
== codes/A51_6_5_1785.txt
sha256 verified by inventory preflight
file=A51_6_5_1785.txt sha256=9871c29974fe58c7d181433671fa8d0cda3e3fc95b551549ddb7170167c67123
F format: lines=1785 claimed_M=1785 bad_lines=0
W weight/distinct: bad_weight=0 distinct=1785
A all-pairs: words=1785 pairs=1592220 expected=1592220 min_distance=6 need>=6 histogram={6: 116690, 8: 543103, 10: 932427}
B packing: t=3 subsets=17850 distinct=17850 collisions=0
VERDICT: VALID  A(51,6,5) >= 1785
== codes/A51_6_6_11184.txt
sha256 verified by inventory preflight
file=A51_6_6_11184.txt sha256=2e6f09bcacc16fa3f0a3bddb450567e52cd405afbb48dadb91f605c2a0701955
F format: lines=11184 claimed_M=11184 bad_lines=0
W weight/distinct: bad_weight=0 distinct=11184
A all-pairs: words=11184 pairs=62535336 expected=62535336 min_distance=6 need>=6 histogram={6: 1117327, 8: 7643168, 10: 25498222, 12: 28276619}
B packing: t=4 subsets=167760 distinct=167760 collisions=0
VERDICT: VALID  A(51,6,6) >= 11184
== codes/A52_8_7_3799.txt
sha256 verified by inventory preflight
file=A52_8_7_3799.txt sha256=d2b02baf300e96e2332afeaeab049f5d3231e891bd2de7a3598aa1eb67d2e12e
F format: lines=3799 claimed_M=3799 bad_lines=0
W weight/distinct: bad_weight=0 distinct=3799
A all-pairs: words=3799 pairs=7214301 expected=7214301 min_distance=8 need>=8 histogram={8: 389256, 10: 1287385, 12: 3113099, 14: 2424561}
B packing: t=4 subsets=132965 distinct=132965 collisions=0
VERDICT: VALID  A(52,8,7) >= 3799
== codes/A53_8_7_3987.txt
sha256 verified by inventory preflight
file=A53_8_7_3987.txt sha256=23f6622b2679419869372031dbeafba85d80c256dfb28434aed8ba01b4df6417
F format: lines=3987 claimed_M=3987 bad_lines=0
W weight/distinct: bad_weight=0 distinct=3987
A all-pairs: words=3987 pairs=7946091 expected=7946091 min_distance=8 need>=8 histogram={8: 404117, 10: 1395735, 12: 3419157, 14: 2727082}
B packing: t=4 subsets=139545 distinct=139545 collisions=0
VERDICT: VALID  A(53,8,7) >= 3987
== codes/A54_8_7_4193.txt
sha256 verified by inventory preflight
file=A54_8_7_4193.txt sha256=a5109255714dd876f6fc80f2b7323b5d63570e25a4e104e260b75309ea321118
F format: lines=4193 claimed_M=4193 bad_lines=0
W weight/distinct: bad_weight=0 distinct=4193
A all-pairs: words=4193 pairs=8788528 expected=8788528 min_distance=8 need>=8 histogram={8: 419440, 10: 1515691, 12: 3771865, 14: 3081532}
B packing: t=4 subsets=146755 distinct=146755 collisions=0
VERDICT: VALID  A(54,8,7) >= 4193
== codes/A55_8_7_4426.txt
sha256 verified by inventory preflight
file=A55_8_7_4426.txt sha256=90be7c1e30354c0f3460b78f295518af0db360b61b02732439c6f63716b26049
F format: lines=4426 claimed_M=4426 bad_lines=0
W weight/distinct: bad_weight=0 distinct=4426
A all-pairs: words=4426 pairs=9792525 expected=9792525 min_distance=8 need>=8 histogram={8: 437089, 10: 1652430, 12: 4187643, 14: 3515363}
B packing: t=4 subsets=154910 distinct=154910 collisions=0
VERDICT: VALID  A(55,8,7) >= 4426
== codes/A56_8_7_4685.txt
sha256 verified by inventory preflight
file=A56_8_7_4685.txt sha256=8c1381b23af4e23adba3332069530f1a929dfd59d454c9f8d5ddc8de087e2fb5
F format: lines=4685 claimed_M=4685 bad_lines=0
W weight/distinct: bad_weight=0 distinct=4685
A all-pairs: words=4685 pairs=10972270 expected=10972270 min_distance=8 need>=8 histogram={8: 437924, 10: 1816933, 12: 4660455, 14: 4056958}
B packing: t=4 subsets=163975 distinct=163975 collisions=0
VERDICT: VALID  A(56,8,7) >= 4685
== codes/A58_6_5_2684.txt
sha256 verified by inventory preflight
file=A58_6_5_2684.txt sha256=9bf9102dbf2921f83d5e0d8c64c0d6d300239e8d3fe7f9c5cc82f48221596d4e
F format: lines=2684 claimed_M=2684 bad_lines=0
W weight/distinct: bad_weight=0 distinct=2684
A all-pairs: words=2684 pairs=3600586 expected=3600586 min_distance=6 need>=6 histogram={6: 205581, 8: 1136555, 10: 2258450}
B packing: t=3 subsets=26840 distinct=26840 collisions=0
VERDICT: VALID  A(58,6,5) >= 2684
== Delsarte certificates
cert_A31_12_10.json  A(31,12,10) <= 197   dual bound = 8091/41 = 197.341463   worst dual row = 0   primal==dual: True   VALID
cert_A31_12_11.json  A(31,12,11) <= 380   dual bound = 145638/383 = 380.255875   worst dual row = 0   primal==dual: True   VALID
cert_A32_12_10.json  A(32,12,10) <= 245   dual bound = 26784/109 = 245.724771   worst dual row = 0   primal==dual: True   VALID
cert_A32_12_15.json  A(32,12,15) <= 2511   dual bound = 1102464/439 = 2511.307517   worst dual row = 0   primal==dual: True   VALID
cert_A32_12_16.json  A(32,12,16) <= 2652   dual bound = 801009/302 = 2652.347682   worst dual row = 0   primal==dual: True   VALID
ALL CERTIFICATES VALID
ALL CHECKS PASSED
```

---

## Historical receipts

The records below are preserved from earlier runs of the former wrapper. Their
wrapper messages do not describe the current run; use the complete current
output above for the current wrapper contract. Historical comparison dates and
optional-runtime coverage remain those stated in the original records.

# Check results (constant-weight codes)

`sh verify-it-yourself/run_checks.sh` was run on the shipped files from 2026-10-11T22:31:01Z to 2026-10-11T22:46:07Z on the build machine (macOS, python3 3.9,
numpy 2.0.2, one thread, machine load average about 160–250 from other jobs; `83.16s user 10.59s system 10% cpu 15:06.45 total`). Exit code 0, last line
`ALL CHECKS PASSED`. Host-specific fields (absolute paths) do not occur in this output. The complete raw output is
at the end of this file.

## 30 codes: all VALID

Tests: F (format and count), W (weights, distinctness), A (all M(M−1)/2 pairwise distances; the smallest must be
≥ d), B (no two words share t = w − d/2 + 1 common ones; a second route to the same property).

| file | claim | pairs tested | min distance | d | B-test collisions | sha256 vs index | verdict |
|---|---|---|---|---|---|---|---|
| `codes/A25_6_11_8718.txt` | A(25 6 11) >= 8718 | 37 997 403 | 6 | 6 | 0 | matches | VALID |
| `codes/A25_6_12_9895.txt` | A(25 6 12) >= 9895 | 48 950 565 | 6 | 6 | 0 | matches | VALID |
| `codes/A26_6_11_12222.txt` | A(26 6 11) >= 12222 | 74 682 531 | 6 | 6 | 0 | matches | VALID |
| `codes/A26_6_13_16225.txt` | A(26 6 13) >= 16225 | 131 617 200 | 6 | 6 | 0 | matches | VALID |
| `codes/A26_6_8_3603.txt` | A(26 6 8) >= 3603 | 6 489 003 | 6 | 6 | 0 | matches | VALID |
| `codes/A26_6_9_5986.txt` | A(26 6 9) >= 5986 | 17 913 105 | 6 | 6 | 0 | matches | VALID |
| `codes/A27_6_9_8325.txt` | A(27 6 9) >= 8325 | 34 648 650 | 6 | 6 | 0 | matches | VALID |
| `codes/A27_8_10_1737.txt` | A(27 8 10) >= 1737 | 1 507 716 | 8 | 8 | 0 | matches | VALID |
| `codes/A27_8_11_2421.txt` | A(27 8 11) >= 2421 | 2 929 410 | 8 | 8 | 0 | matches | VALID |
| `codes/A28_8_11_3785.txt` | A(28 8 11) >= 3785 | 7 161 220 | 8 | 8 | 0 | matches | VALID |
| `codes/A28_8_12_4962.txt` | A(28 8 12) >= 4962 | 12 308 241 | 8 | 8 | 0 | matches | VALID |
| `codes/A28_8_14_6359.txt` | A(28 8 14) >= 6359 | 20 215 261 | 8 | 8 | 0 | matches | VALID |
| `codes/A28_8_9_1406.txt` | A(28 8 9) >= 1406 | 987 715 | 8 | 8 | 0 | matches | VALID |
| `codes/A29_6_10_25974.txt` | A(29 6 10) >= 25974 | 337 311 351 | 6 | 6 | 0 | matches | VALID |
| `codes/A29_6_11_41219.txt` | A(29 6 11) >= 41219 | 849 482 371 | 6 | 6 | 0 | matches | VALID |
| `codes/A29_6_12_61823.txt` | A(29 6 12) >= 61823 | 1 911 010 753 | 6 | 6 | 0 | matches | VALID |
| `codes/A30_8_8_1166.txt` | A(30 8 8) >= 1166 | 679 195 | 8 | 8 | 0 | matches | VALID |
| `codes/A33_8_8_1809.txt` | A(33 8 8) >= 1809 | 1 635 336 | 8 | 8 | 0 | matches | VALID |
| `codes/A34_8_7_602.txt` | A(34 8 7) >= 602 | 180 901 | 8 | 8 | 0 | matches | VALID |
| `codes/A34_8_8_1965.txt` | A(34 8 8) >= 1965 | 1 929 630 | 8 | 8 | 0 | matches | VALID |
| `codes/A35_6_6_2217.txt` | A(35 6 6) >= 2217 | 2 456 436 | 6 | 6 | 0 | matches | VALID |
| `codes/A45_8_7_1907.txt` | A(45 8 7) >= 1907 | 1 817 371 | 8 | 8 | 0 | matches | VALID |
| `codes/A51_6_5_1785.txt` | A(51 6 5) >= 1785 | 1 592 220 | 6 | 6 | 0 | matches | VALID |
| `codes/A51_6_6_11184.txt` | A(51 6 6) >= 11184 | 62 535 336 | 6 | 6 | 0 | matches | VALID |
| `codes/A52_8_7_3799.txt` | A(52 8 7) >= 3799 | 7 214 301 | 8 | 8 | 0 | matches | VALID |
| `codes/A53_8_7_3987.txt` | A(53 8 7) >= 3987 | 7 946 091 | 8 | 8 | 0 | matches | VALID |
| `codes/A54_8_7_4193.txt` | A(54 8 7) >= 4193 | 8 788 528 | 8 | 8 | 0 | matches | VALID |
| `codes/A55_8_7_4426.txt` | A(55 8 7) >= 4426 | 9 792 525 | 8 | 8 | 0 | matches | VALID |
| `codes/A56_8_7_4685.txt` | A(56 8 7) >= 4685 | 10 972 270 | 8 | 8 | 0 | matches | VALID |
| `codes/A58_6_5_2684.txt` | A(58 6 5) >= 2684 | 3 600 586 | 6 | 6 | 0 | matches | VALID |

## Comparison with the table (2026-10-10T19:23:48Z, `the-record-we-beat/parsed_cells_2026-10-10T19-23-48Z.tsv`)

All 30 codes strictly exceed the printed lower bound of their cell and none exceeds the printed or Johnson
upper bound (margins in `INDEX.csv`; ten are +1 to +3). A(32,8,8) = 1676 is a tie with the [YZW] entry and was never
claimed. The five Delsarte values remain strictly below the printed (Johnson) upper bounds 229, 415, 300, 2641, 2870.
An independent re-parse of the same table version earlier on 2026-10-10 (separate script, separate checker run) gave
the same verdict for each of these cells.

## 5 Delsarte certificates: all VALID

```
== Delsarte certificates
cert_A31_12_10.json  A(31,12,10) <= 197   dual bound = 8091/41 = 197.341463   worst dual row = 0   primal==dual: True   VALID
cert_A31_12_11.json  A(31,12,11) <= 380   dual bound = 145638/383 = 380.255875   worst dual row = 0   primal==dual: True   VALID
cert_A32_12_10.json  A(32,12,10) <= 245   dual bound = 26784/109 = 245.724771   worst dual row = 0   primal==dual: True   VALID
cert_A32_12_15.json  A(32,12,15) <= 2511   dual bound = 1102464/439 = 2511.307517   worst dual row = 0   primal==dual: True   VALID
cert_A32_12_16.json  A(32,12,16) <= 2652   dual bound = 801009/302 = 2652.347682   worst dual row = 0   primal==dual: True   VALID
ALL CERTIFICATES VALID
sha256 ok cert_A31_12_10.json
sha256 ok cert_A31_12_11.json
sha256 ok cert_A32_12_10.json
sha256 ok cert_A32_12_15.json
sha256 ok cert_A32_12_16.json
```
(`worst dual row = 0`: the binding dual constraints hold with equality; `primal==dual: True`: the stated value is the
exact LP optimum.)

## Negative controls (earlier run, same checkers)

Codes: a duplicated word, a word at distance 2, a word of weight w+1, a short line and a wrong count in the file name
were each reported INVALID (exit code 1) on modified copies of `A34_8_7_602.txt`. Certificates: changing the stated
floor `U` from 197 to 196, or `y_1` from 61/123 to 60/123, in a copy of `cert_A31_12_10.json` is reported.

## Earlier independent checks (for the record)

Before release each code had passed the author's checker and two checkers written independently by separate
reviewers, and a further independent code checker and exact certificate checker were rerun on everything in a final
pre-release check. None of
those checkers is shipped; `verify-it-yourself/` contains the two written for the release.

## Raw output of `sh verify-it-yourself/run_checks.sh`

```
2026-10-11T22:31:01Z
== codes/A25_6_11_8718.txt
sha256 matches INDEX.csv
file=A25_6_11_8718.txt sha256=fb5145c3b40d3ac0a67a539bce0fa075f6a2d98f9c635932bc7309ee78d1d7ae
F format: lines=8718 claimed_M=8718 bad_lines=0
W weight/distinct: bad_weight=0 distinct=8718
A all-pairs: words=8718 pairs=37997403 expected=37997403 min_distance=6 need>=6 histogram={6: 655839, 8: 2641714, 10: 7936494, 12: 11930619, 14: 9497165, 16: 4316579, 18: 915828, 20: 100181, 22: 2984}
B packing: t=9 subsets=479490 distinct=479490 collisions=0
VERDICT: VALID  A(25,6,11) >= 8718
== codes/A25_6_12_9895.txt
sha256 matches INDEX.csv
file=A25_6_12_9895.txt sha256=b2631ed9296e9a0622a535edaba582a715520fe06af36de4d51cd1cf18698519
F format: lines=9895 claimed_M=9895 bad_lines=0
W weight/distinct: bad_weight=0 distinct=9895
A all-pairs: words=9895 pairs=48950565 expected=48950565 min_distance=6 need>=6 histogram={6: 709526, 8: 3267105, 10: 9474200, 12: 15127248, 14: 12715381, 16: 5959697, 18: 1521614, 20: 162830, 22: 12916, 24: 48}
B packing: t=10 subsets=653070 distinct=653070 collisions=0
VERDICT: VALID  A(25,6,12) >= 9895
== codes/A26_6_11_12222.txt
sha256 matches INDEX.csv
file=A26_6_11_12222.txt sha256=0637a3a3ee1fa65d5230bacbf14fb7a88c56a047fc5a24db614ccd795e488961
F format: lines=12222 claimed_M=12222 bad_lines=0
W weight/distinct: bad_weight=0 distinct=12222
A all-pairs: words=12222 pairs=74682531 expected=74682531 min_distance=6 need>=6 histogram={6: 866973, 8: 4282053, 10: 13439615, 12: 22423911, 14: 20490869, 16: 10203332, 18: 2650288, 20: 315054, 22: 10436}
B packing: t=9 subsets=672210 distinct=672210 collisions=0
VERDICT: VALID  A(26,6,11) >= 12222
== codes/A26_6_13_16225.txt
sha256 matches INDEX.csv
file=A26_6_13_16225.txt sha256=be7b1c9464c67bc9cac8c175214c607291cb427e127534b30994b29eff4f274e
F format: lines=16225 claimed_M=16225 bad_lines=0
W weight/distinct: bad_weight=0 distinct=16225
A all-pairs: words=16225 pairs=131617200 expected=131617200 min_distance=6 need>=6 histogram={6: 1254872, 8: 6429365, 10: 20971400, 12: 37660170, 14: 37071277, 16: 20643831, 18: 6516225, 20: 997168, 22: 69717, 24: 2825, 26: 350}
B packing: t=11 subsets=1265550 distinct=1265550 collisions=0
VERDICT: VALID  A(26,6,13) >= 16225
== codes/A26_6_8_3603.txt
sha256 matches INDEX.csv
file=A26_6_8_3603.txt sha256=bd239ef369bb94ca6af15162cf2790b7848640adf01ffae05a4a099d7ae7b509
F format: lines=3603 claimed_M=3603 bad_lines=0
W weight/distinct: bad_weight=0 distinct=3603
A all-pairs: words=3603 pairs=6489003 expected=6489003 min_distance=6 need>=6 histogram={6: 270655, 8: 861684, 10: 2099301, 12: 2092703, 14: 1001502, 16: 163158}
B packing: t=6 subsets=100884 distinct=100884 collisions=0
VERDICT: VALID  A(26,6,8) >= 3603
== codes/A26_6_9_5986.txt
sha256 matches INDEX.csv
file=A26_6_9_5986.txt sha256=b09c1c5d9772aae336ca2ba29e4c3e25c6346299aabcd677008d08f0749308cf
F format: lines=5986 claimed_M=5986 bad_lines=0
W weight/distinct: bad_weight=0 distinct=5986
A all-pairs: words=5986 pairs=17913105 expected=17913105 min_distance=6 need>=6 histogram={6: 421262, 8: 1588691, 10: 4594425, 12: 5897900, 14: 4035336, 16: 1236594, 18: 138897}
B packing: t=7 subsets=215496 distinct=215496 collisions=0
VERDICT: VALID  A(26,6,9) >= 5986
== codes/A27_6_9_8325.txt
sha256 matches INDEX.csv
file=A27_6_9_8325.txt sha256=d6b278e96ded45c784f351c80dff216c65dba8173d63bb4d2e96b1602c33df3e
F format: lines=8325 claimed_M=8325 bad_lines=0
W weight/distinct: bad_weight=0 distinct=8325
A all-pairs: words=8325 pairs=34648650 expected=34648650 min_distance=6 need>=6 histogram={6: 617721, 8: 2707722, 10: 8094927, 12: 11450984, 14: 8537390, 16: 2868733, 18: 371173}
B packing: t=7 subsets=299700 distinct=299700 collisions=0
VERDICT: VALID  A(27,6,9) >= 8325
== codes/A27_8_10_1737.txt
sha256 matches INDEX.csv
file=A27_8_10_1737.txt sha256=5a9ef07f5d958179ac069f546c43914147ac041f0c10e80a2229ea3d1287a05f
F format: lines=1737 claimed_M=1737 bad_lines=0
W weight/distinct: bad_weight=0 distinct=1737
A all-pairs: words=1737 pairs=1507716 expected=1507716 min_distance=8 need>=8 histogram={8: 178748, 10: 120292, 12: 676151, 14: 243018, 16: 261100, 18: 24402, 20: 4005}
B packing: t=7 subsets=208440 distinct=208440 collisions=0
VERDICT: VALID  A(27,8,10) >= 1737
== codes/A27_8_11_2421.txt
sha256 matches INDEX.csv
file=A27_8_11_2421.txt sha256=79e63d441921eda3444f3a4fe0601672c97c8df1f9f2a974fa5909f762afaf3a
F format: lines=2421 claimed_M=2421 bad_lines=0
W weight/distinct: bad_weight=0 distinct=2421
A all-pairs: words=2421 pairs=2929410 expected=2929410 min_distance=8 need>=8 histogram={8: 207403, 10: 371016, 12: 841504, 14: 899424, 16: 438521, 18: 150919, 20: 20032, 22: 591}
B packing: t=8 subsets=399465 distinct=399465 collisions=0
VERDICT: VALID  A(27,8,11) >= 2421
== codes/A28_8_11_3785.txt
sha256 matches INDEX.csv
file=A28_8_11_3785.txt sha256=c3160db5f409d2700e974d77503ac3806ac535ef052fb94f8558c92829c9fb91
F format: lines=3785 claimed_M=3785 bad_lines=0
W weight/distinct: bad_weight=0 distinct=3785
A all-pairs: words=3785 pairs=7161220 expected=7161220 min_distance=8 need>=8 histogram={8: 401362, 10: 787247, 12: 1908995, 14: 2293423, 16: 1221554, 18: 472236, 20: 73886, 22: 2517}
B packing: t=8 subsets=624525 distinct=624525 collisions=0
VERDICT: VALID  A(28,8,11) >= 3785
== codes/A28_8_12_4962.txt
sha256 matches INDEX.csv
file=A28_8_12_4962.txt sha256=02553ea43f9584446414c23dc611e751cbfb6a8f037e0c115d30aae43e6c5341
F format: lines=4962 claimed_M=4962 bad_lines=0
W weight/distinct: bad_weight=0 distinct=4962
A all-pairs: words=4962 pairs=12308241 expected=12308241 min_distance=8 need>=8 histogram={8: 624834, 10: 664097, 12: 4375813, 14: 2002032, 16: 3813788, 18: 465890, 20: 358805, 22: 136, 24: 2846}
B packing: t=9 subsets=1091640 distinct=1091640 collisions=0
VERDICT: VALID  A(28,8,12) >= 4962
== codes/A28_8_14_6359.txt
sha256 matches INDEX.csv
file=A28_8_14_6359.txt sha256=a4a88d0575c275884d3d34a25156a980f418a5ffd56bf0e188ecbe4a758a7d22
F format: lines=6359 claimed_M=6359 bad_lines=0
W weight/distinct: bad_weight=0 distinct=6359
A all-pairs: words=6359 pairs=20215261 expected=20215261 min_distance=8 need>=8 histogram={8: 1044569, 10: 1360267, 12: 5085109, 14: 5497439, 16: 4280773, 18: 2258684, 20: 606619, 22: 66753, 24: 14218, 26: 438, 28: 392}
B packing: t=11 subsets=2314676 distinct=2314676 collisions=0
VERDICT: VALID  A(28,8,14) >= 6359
== codes/A28_8_9_1406.txt
sha256 matches INDEX.csv
file=A28_8_9_1406.txt sha256=4912b21d4eed029dc861a85506f7a4bc10189106ae95793eaada8c1654d316cb
F format: lines=1406 claimed_M=1406 bad_lines=0
W weight/distinct: bad_weight=0 distinct=1406
A all-pairs: words=1406 pairs=987715 expected=987715 min_distance=8 need>=8 histogram={8: 104739, 10: 184784, 12: 305762, 14: 297614, 16: 78029, 18: 16787}
B packing: t=6 subsets=118104 distinct=118104 collisions=0
VERDICT: VALID  A(28,8,9) >= 1406
== codes/A29_6_10_25974.txt
sha256 matches INDEX.csv
file=A29_6_10_25974.txt sha256=5551204c40538f6b11e53e60414e417d5ff7d8c8c59b40a8185ddd59a9de9cd3
F format: lines=25974 claimed_M=25974 bad_lines=0
W weight/distinct: bad_weight=0 distinct=25974
A all-pairs: words=25974 pairs=337311351 expected=337311351 min_distance=6 need>=6 histogram={6: 2309765, 8: 13397058, 10: 49341137, 12: 96401531, 14: 101369564, 16: 57438721, 18: 15496556, 20: 1557019}
B packing: t=8 subsets=1168830 distinct=1168830 collisions=0
VERDICT: VALID  A(29,6,10) >= 25974
== codes/A29_6_11_41219.txt
sha256 matches INDEX.csv
file=A29_6_11_41219.txt sha256=505ba4d63b0faab9bf8a4e470cebb3111f5622a40985d3324a34a0b994ebee25
F format: lines=41219 claimed_M=41219 bad_lines=0
W weight/distinct: bad_weight=0 distinct=41219
A all-pairs: words=41219 pairs=849482371 expected=849482371 min_distance=6 need>=6 histogram={6: 3824405, 8: 24226819, 10: 97491644, 12: 210565525, 14: 257804615, 16: 177316998, 18: 65651397, 20: 11819436, 22: 781532}
B packing: t=9 subsets=2267045 distinct=2267045 collisions=0
VERDICT: VALID  A(29,6,11) >= 41219
== codes/A29_6_12_61823.txt
sha256 matches INDEX.csv
file=A29_6_12_61823.txt sha256=d467400b0827c8db81a1c9348317ca1d645c049d6cb54fdf5b927964490e4d2f
F format: lines=61823 claimed_M=61823 bad_lines=0
W weight/distinct: bad_weight=0 distinct=61823
A all-pairs: words=61823 pairs=1911010753 expected=1911010753 min_distance=6 need>=6 histogram={6: 6372782, 8: 42387302, 10: 181030245, 12: 421055053, 14: 567053897, 16: 443236523, 18: 196901932, 20: 47279753, 22: 5464441, 24: 228825}
B packing: t=10 subsets=4080318 distinct=4080318 collisions=0
VERDICT: VALID  A(29,6,12) >= 61823
== codes/A30_8_8_1166.txt
sha256 matches INDEX.csv
file=A30_8_8_1166.txt sha256=b4d9fdacd8a4d441b3025389d37026d77627a2ff234d76496a14b94ee11ef742
F format: lines=1166 claimed_M=1166 bad_lines=0
W weight/distinct: bad_weight=0 distinct=1166
A all-pairs: words=1166 pairs=679195 expected=679195 min_distance=8 need>=8 histogram={8: 112430, 10: 98687, 12: 303302, 14: 124157, 16: 40619}
B packing: t=5 subsets=65296 distinct=65296 collisions=0
VERDICT: VALID  A(30,8,8) >= 1166
== codes/A33_8_8_1809.txt
sha256 matches INDEX.csv
file=A33_8_8_1809.txt sha256=0a8e9c53dc656f46c45a5e2a50149612644132789219501aa3a32592643ee139
F format: lines=1809 claimed_M=1809 bad_lines=0
W weight/distinct: bad_weight=0 distinct=1809
A all-pairs: words=1809 pairs=1635336 expected=1635336 min_distance=8 need>=8 histogram={8: 184651, 10: 236946, 12: 683106, 14: 395000, 16: 135633}
B packing: t=5 subsets=101304 distinct=101304 collisions=0
VERDICT: VALID  A(33,8,8) >= 1809
== codes/A34_8_7_602.txt
sha256 matches INDEX.csv
file=A34_8_7_602.txt sha256=1a1d0958047e78b8d29752ccb0210518b170663b6862f84d57669c7b0c02d81e
F format: lines=602 claimed_M=602 bad_lines=0
W weight/distinct: bad_weight=0 distinct=602
A all-pairs: words=602 pairs=180901 expected=180901 min_distance=8 need>=8 histogram={8: 32414, 10: 44914, 12: 75763, 14: 27810}
B packing: t=4 subsets=21070 distinct=21070 collisions=0
VERDICT: VALID  A(34,8,7) >= 602
== codes/A34_8_8_1965.txt
sha256 matches INDEX.csv
file=A34_8_8_1965.txt sha256=125083e27d7b04aee88f0c271af7a8946cba376bb87948705f89a2edc6f95eb4
F format: lines=1965 claimed_M=1965 bad_lines=0
W weight/distinct: bad_weight=0 distinct=1965
A all-pairs: words=1965 pairs=1929630 expected=1929630 min_distance=8 need>=8 histogram={8: 196259, 10: 283369, 12: 785434, 14: 494881, 16: 169687}
B packing: t=5 subsets=110040 distinct=110040 collisions=0
VERDICT: VALID  A(34,8,8) >= 1965
== codes/A35_6_6_2217.txt
sha256 matches INDEX.csv
file=A35_6_6_2217.txt sha256=3bc77f117eb9ead8b3d35b6e9a610b8fd2cc183e14d71c2f42a7abe244371459
F format: lines=2217 claimed_M=2217 bad_lines=0
W weight/distinct: bad_weight=0 distinct=2217
A all-pairs: words=2217 pairs=2456436 expected=2456436 min_distance=6 need>=6 histogram={6: 133289, 8: 523000, 10: 1086270, 12: 713877}
B packing: t=4 subsets=33255 distinct=33255 collisions=0
VERDICT: VALID  A(35,6,6) >= 2217
== codes/A45_8_7_1907.txt
sha256 matches INDEX.csv
file=A45_8_7_1907.txt sha256=3572d00c548890628259491cbcd330950c5ad79d2797b3b14a1bbe224750fd6e
F format: lines=1907 claimed_M=1907 bad_lines=0
W weight/distinct: bad_weight=0 distinct=1907
A all-pairs: words=1907 pairs=1817371 expected=1817371 min_distance=8 need>=8 histogram={8: 141694, 10: 383793, 12: 783205, 14: 508679}
B packing: t=4 subsets=66745 distinct=66745 collisions=0
VERDICT: VALID  A(45,8,7) >= 1907
== codes/A51_6_5_1785.txt
sha256 matches INDEX.csv
file=A51_6_5_1785.txt sha256=9871c29974fe58c7d181433671fa8d0cda3e3fc95b551549ddb7170167c67123
F format: lines=1785 claimed_M=1785 bad_lines=0
W weight/distinct: bad_weight=0 distinct=1785
A all-pairs: words=1785 pairs=1592220 expected=1592220 min_distance=6 need>=6 histogram={6: 116690, 8: 543103, 10: 932427}
B packing: t=3 subsets=17850 distinct=17850 collisions=0
VERDICT: VALID  A(51,6,5) >= 1785
== codes/A51_6_6_11184.txt
sha256 matches INDEX.csv
file=A51_6_6_11184.txt sha256=2e6f09bcacc16fa3f0a3bddb450567e52cd405afbb48dadb91f605c2a0701955
F format: lines=11184 claimed_M=11184 bad_lines=0
W weight/distinct: bad_weight=0 distinct=11184
A all-pairs: words=11184 pairs=62535336 expected=62535336 min_distance=6 need>=6 histogram={6: 1117327, 8: 7643168, 10: 25498222, 12: 28276619}
B packing: t=4 subsets=167760 distinct=167760 collisions=0
VERDICT: VALID  A(51,6,6) >= 11184
== codes/A52_8_7_3799.txt
sha256 matches INDEX.csv
file=A52_8_7_3799.txt sha256=d2b02baf300e96e2332afeaeab049f5d3231e891bd2de7a3598aa1eb67d2e12e
F format: lines=3799 claimed_M=3799 bad_lines=0
W weight/distinct: bad_weight=0 distinct=3799
A all-pairs: words=3799 pairs=7214301 expected=7214301 min_distance=8 need>=8 histogram={8: 389256, 10: 1287385, 12: 3113099, 14: 2424561}
B packing: t=4 subsets=132965 distinct=132965 collisions=0
VERDICT: VALID  A(52,8,7) >= 3799
== codes/A53_8_7_3987.txt
sha256 matches INDEX.csv
file=A53_8_7_3987.txt sha256=23f6622b2679419869372031dbeafba85d80c256dfb28434aed8ba01b4df6417
F format: lines=3987 claimed_M=3987 bad_lines=0
W weight/distinct: bad_weight=0 distinct=3987
A all-pairs: words=3987 pairs=7946091 expected=7946091 min_distance=8 need>=8 histogram={8: 404117, 10: 1395735, 12: 3419157, 14: 2727082}
B packing: t=4 subsets=139545 distinct=139545 collisions=0
VERDICT: VALID  A(53,8,7) >= 3987
== codes/A54_8_7_4193.txt
sha256 matches INDEX.csv
file=A54_8_7_4193.txt sha256=a5109255714dd876f6fc80f2b7323b5d63570e25a4e104e260b75309ea321118
F format: lines=4193 claimed_M=4193 bad_lines=0
W weight/distinct: bad_weight=0 distinct=4193
A all-pairs: words=4193 pairs=8788528 expected=8788528 min_distance=8 need>=8 histogram={8: 419440, 10: 1515691, 12: 3771865, 14: 3081532}
B packing: t=4 subsets=146755 distinct=146755 collisions=0
VERDICT: VALID  A(54,8,7) >= 4193
== codes/A55_8_7_4426.txt
sha256 matches INDEX.csv
file=A55_8_7_4426.txt sha256=90be7c1e30354c0f3460b78f295518af0db360b61b02732439c6f63716b26049
F format: lines=4426 claimed_M=4426 bad_lines=0
W weight/distinct: bad_weight=0 distinct=4426
A all-pairs: words=4426 pairs=9792525 expected=9792525 min_distance=8 need>=8 histogram={8: 437089, 10: 1652430, 12: 4187643, 14: 3515363}
B packing: t=4 subsets=154910 distinct=154910 collisions=0
VERDICT: VALID  A(55,8,7) >= 4426
== codes/A56_8_7_4685.txt
sha256 matches INDEX.csv
file=A56_8_7_4685.txt sha256=8c1381b23af4e23adba3332069530f1a929dfd59d454c9f8d5ddc8de087e2fb5
F format: lines=4685 claimed_M=4685 bad_lines=0
W weight/distinct: bad_weight=0 distinct=4685
A all-pairs: words=4685 pairs=10972270 expected=10972270 min_distance=8 need>=8 histogram={8: 437924, 10: 1816933, 12: 4660455, 14: 4056958}
B packing: t=4 subsets=163975 distinct=163975 collisions=0
VERDICT: VALID  A(56,8,7) >= 4685
== codes/A58_6_5_2684.txt
sha256 matches INDEX.csv
file=A58_6_5_2684.txt sha256=9bf9102dbf2921f83d5e0d8c64c0d6d300239e8d3fe7f9c5cc82f48221596d4e
F format: lines=2684 claimed_M=2684 bad_lines=0
W weight/distinct: bad_weight=0 distinct=2684
A all-pairs: words=2684 pairs=3600586 expected=3600586 min_distance=6 need>=6 histogram={6: 205581, 8: 1136555, 10: 2258450}
B packing: t=3 subsets=26840 distinct=26840 collisions=0
VERDICT: VALID  A(58,6,5) >= 2684
== Delsarte certificates
cert_A31_12_10.json  A(31,12,10) <= 197   dual bound = 8091/41 = 197.341463   worst dual row = 0   primal==dual: True   VALID
cert_A31_12_11.json  A(31,12,11) <= 380   dual bound = 145638/383 = 380.255875   worst dual row = 0   primal==dual: True   VALID
cert_A32_12_10.json  A(32,12,10) <= 245   dual bound = 26784/109 = 245.724771   worst dual row = 0   primal==dual: True   VALID
cert_A32_12_15.json  A(32,12,15) <= 2511   dual bound = 1102464/439 = 2511.307517   worst dual row = 0   primal==dual: True   VALID
cert_A32_12_16.json  A(32,12,16) <= 2652   dual bound = 801009/302 = 2652.347682   worst dual row = 0   primal==dual: True   VALID
ALL CERTIFICATES VALID
sha256 ok cert_A31_12_10.json
sha256 ok cert_A31_12_11.json
sha256 ok cert_A32_12_10.json
sha256 ok cert_A32_12_15.json
sha256 ok cert_A32_12_16.json
ALL CHECKS PASSED
sh verify-it-yourself/run_checks.sh  83.16s user 10.59s system 10% cpu 15:06.45 total
2026-10-11T22:46:07Z
```
