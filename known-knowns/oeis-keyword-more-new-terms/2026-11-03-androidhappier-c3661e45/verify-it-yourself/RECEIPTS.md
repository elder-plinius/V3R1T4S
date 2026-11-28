# Receipts: real output of verify-it-yourself/run_checks.sh

Run from a clean copy of the package folder on the build machine, 2026-11-03T22:03Z (Python 3, cc available), wall time under 1 s:

    == 1. sha256 of object/ROW6.txt and object/VALUE.txt
    got  c3661e45bbff1f5a2fb05098c2940739a0d096689e593c1095142858cb66f120
    want c3661e45bbff1f5a2fb05098c2940739a0d096689e593c1095142858cb66f120
    sha256: match
    == 2. independent count from the definition (n = 0..6)
    0 len=1 sum=1 head: 1
    1 len=1 sum=1 head: 1
    2 len=2 sum=3 head: 2,1
    3 len=5 sum=15 head: 6,3,3,2,1
    4 len=14 sum=105 head: 24,12,12,12,8,8,6,6,4,4,3,3
    5 len=42 sum=945 head: 120,60,60,60,60,40,40,40,30,30,30,30
    6 len=132 sum=10395 head: 720,360,360,360,360,360,240,240,240,240,180,180
    single-tree sanity star/path/two cherries = 720/1/80 ok
    indices 0..65 equal OEIS DATA (66 terms)
    row 6 (132 values, flattened indices 65..196) equals object/ROW6.txt
    index 66 = T(6,2) = 360 equals object/VALUE.txt
    == 3. negative control: labelings without the increasing condition
    control rows 0..5 first 15: [1, 1, 2, 2, 6, 6, 6, 6, 6, 24, 24, 24, 24, 24, 24]
    control: differs from DATA as expected
    == 4. Program B (C) row 6
    pB row 6 identical to object/ROW6.txt
    summary: A131449 index 66 = 360; row 6 head 720,360,360,360,360,360,240,240,...
    PASS
