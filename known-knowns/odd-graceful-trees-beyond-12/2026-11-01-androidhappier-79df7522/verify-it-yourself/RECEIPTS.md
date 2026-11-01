# Receipts: real output of verify-it-yourself/run_checks.sh

Machine: Linux x86-64, 8 cores, Python 3.13.5, gcc 14.2.0. Run on 2026-11-01.

## 1. This package as shipped (orders 2..20; large-files/ absent)

    == 1. sha256 of object/CERTIFICATES.txt
    got  79df75225a75f48b971b2e7ea2a91e325a129d836720df7542d056dfed2971af
    want 79df75225a75f48b971b2e7ea2a91e325a129d836720df7542d056dfed2971af
    manifest sha256: match
    == 2. reassemble the certificates and check each sha256 and size against object/CERTIFICATES.txt
    cert_2.txt.gz: sha256 match (1 part(s), 39 bytes)
    cert_3.txt.gz: sha256 match (1 part(s), 43 bytes)
    cert_4.txt.gz: sha256 match (1 part(s), 58 bytes)
    cert_5.txt.gz: sha256 match (1 part(s), 72 bytes)
    cert_6.txt.gz: sha256 match (1 part(s), 99 bytes)
    cert_7.txt.gz: sha256 match (1 part(s), 149 bytes)
    cert_8.txt.gz: sha256 match (1 part(s), 281 bytes)
    cert_9.txt.gz: sha256 match (1 part(s), 545 bytes)
    cert_10.txt.gz: sha256 match (1 part(s), 1287 bytes)
    cert_11.txt.gz: sha256 match (1 part(s), 2948 bytes)
    cert_12.txt.gz: sha256 match (1 part(s), 7313 bytes)
    cert_13.txt.gz: sha256 match (1 part(s), 18218 bytes)
    cert_14.txt.gz: sha256 match (1 part(s), 47267 bytes)
    cert_15.txt.gz: sha256 match (1 part(s), 124007 bytes)
    cert_16.txt.gz: sha256 match (1 part(s), 331263 bytes)
    cert_17.txt.gz: sha256 match (1 part(s), 892536 bytes)
    cert_18.txt.gz: sha256 match (3 part(s), 2410425 bytes)
    cert_19.txt.gz: sha256 match (7 part(s), 6550060 bytes)
    cert_20.txt.gz: sha256 match (18 part(s), 17860164 bytes)
    cert_21.txt.gz: not present (external file, order 21 not checked here)
    cert_22.txt.gz: not present (external file, order 22 not checked here)
    orders available: 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 
    == 3. Python checker (check_odd_graceful.py, standard library): every line of every available certificate
    order 2: 1 lines, 1 distinct odd-gracefully labelled trees, A000055(2) = 1 (Otter) PASS
    order 3: 1 lines, 1 distinct odd-gracefully labelled trees, A000055(3) = 1 (Otter) PASS
    order 4: 2 lines, 2 distinct odd-gracefully labelled trees, A000055(4) = 2 (Otter) PASS
    order 5: 3 lines, 3 distinct odd-gracefully labelled trees, A000055(5) = 3 (Otter) PASS
    order 6: 6 lines, 6 distinct odd-gracefully labelled trees, A000055(6) = 6 (Otter) PASS
    order 7: 11 lines, 11 distinct odd-gracefully labelled trees, A000055(7) = 11 (Otter) PASS
    order 8: 23 lines, 23 distinct odd-gracefully labelled trees, A000055(8) = 23 (Otter) PASS
    order 9: 47 lines, 47 distinct odd-gracefully labelled trees, A000055(9) = 47 (Otter) PASS
    order 10: 106 lines, 106 distinct odd-gracefully labelled trees, A000055(10) = 106 (Otter) PASS
    order 11: 235 lines, 235 distinct odd-gracefully labelled trees, A000055(11) = 235 (Otter) PASS
    order 12: 551 lines, 551 distinct odd-gracefully labelled trees, A000055(12) = 551 (Otter) PASS
    order 13: 1301 lines, 1301 distinct odd-gracefully labelled trees, A000055(13) = 1301 (Otter) PASS
    order 14: 3159 lines, 3159 distinct odd-gracefully labelled trees, A000055(14) = 3159 (Otter) PASS
    order 15: 7741 lines, 7741 distinct odd-gracefully labelled trees, A000055(15) = 7741 (Otter) PASS
    order 16: 19320 lines, 19320 distinct odd-gracefully labelled trees, A000055(16) = 19320 (Otter) PASS
    order 17: 48629 lines, 48629 distinct odd-gracefully labelled trees, A000055(17) = 48629 (Otter) PASS
    order 18: 123867 lines, 123867 distinct odd-gracefully labelled trees, A000055(18) = 123867 (Otter) PASS
    order 19: 317955 lines, 317955 distinct odd-gracefully labelled trees, A000055(19) = 317955 (Otter) PASS
    order 20: 823065 lines, 823065 distinct odd-gracefully labelled trees, A000055(20) = 823065 (Otter) PASS
    == 4. controls: damaged copies of the order-13 certificate must FAIL
    order 13: line 1: edge differences are not {1, 3, ..., 23} FAIL
    control 1: FAIL as expected
    order 13: lines 1300, distinct trees 1300, but A000055(13) = 1301 FAIL
    control 2: FAIL as expected
    order 13: line 1301: duplicate tree FAIL
    control 3: FAIL as expected
    == 5. second checker (ogcheck.c, C): regenerates all trees of order n by leaf addition and matches the certificate
    order 2: regenerated 1 trees
    order 2: certificate lines 1, valid labelings 1, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 2
    ogcheck order 2: regenerated 1 = A000055(2)
    order 3: regenerated 1 trees
    order 3: certificate lines 1, valid labelings 1, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 3
    ogcheck order 3: regenerated 1 = A000055(3)
    order 4: regenerated 2 trees
    order 4: certificate lines 2, valid labelings 2, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 4
    ogcheck order 4: regenerated 2 = A000055(4)
    order 5: regenerated 3 trees
    order 5: certificate lines 3, valid labelings 3, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 5
    ogcheck order 5: regenerated 3 = A000055(5)
    order 6: regenerated 6 trees
    order 6: certificate lines 6, valid labelings 6, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 6
    ogcheck order 6: regenerated 6 = A000055(6)
    order 7: regenerated 11 trees
    order 7: certificate lines 11, valid labelings 11, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 7
    ogcheck order 7: regenerated 11 = A000055(7)
    order 8: regenerated 23 trees
    order 8: certificate lines 23, valid labelings 23, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 8
    ogcheck order 8: regenerated 23 = A000055(8)
    order 9: regenerated 47 trees
    order 9: certificate lines 47, valid labelings 47, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 9
    ogcheck order 9: regenerated 47 = A000055(9)
    order 10: regenerated 106 trees
    order 10: certificate lines 106, valid labelings 106, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 10
    ogcheck order 10: regenerated 106 = A000055(10)
    order 11: regenerated 235 trees
    order 11: certificate lines 235, valid labelings 235, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 11
    ogcheck order 11: regenerated 235 = A000055(11)
    order 12: regenerated 551 trees
    order 12: certificate lines 551, valid labelings 551, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 12
    ogcheck order 12: regenerated 551 = A000055(12)
    order 13: regenerated 1301 trees
    order 13: certificate lines 1301, valid labelings 1301, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 13
    ogcheck order 13: regenerated 1301 = A000055(13)
    order 14: regenerated 3159 trees
    order 14: certificate lines 3159, valid labelings 3159, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 14
    ogcheck order 14: regenerated 3159 = A000055(14)
    order 15: regenerated 7741 trees
    order 15: certificate lines 7741, valid labelings 7741, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 15
    ogcheck order 15: regenerated 7741 = A000055(15)
    order 16: regenerated 19320 trees
    order 16: certificate lines 19320, valid labelings 19320, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 16
    ogcheck order 16: regenerated 19320 = A000055(16)
    order 17: regenerated 48629 trees
    order 17: certificate lines 48629, valid labelings 48629, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 17
    ogcheck order 17: regenerated 48629 = A000055(17)
    order 18: regenerated 123867 trees
    order 18: certificate lines 123867, valid labelings 123867, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 18
    ogcheck order 18: regenerated 123867 = A000055(18)
    order 19: regenerated 317955 trees
    order 19: certificate lines 317955, valid labelings 317955, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 19
    ogcheck order 19: regenerated 317955 = A000055(19)
    order 20: regenerated 823065 trees
    order 20: certificate lines 823065, valid labelings 823065, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 20
    ogcheck order 20: regenerated 823065 = A000055(20)
    ogcheck control (swapped labels): FAIL as expected
    == summary: orders checked: 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 
    PASS

## 2. The same package with large-files/cert_21.txt.gz and large-files/cert_22.txt.gz added (orders 2..22)

    == 1. sha256 of object/CERTIFICATES.txt
    got  79df75225a75f48b971b2e7ea2a91e325a129d836720df7542d056dfed2971af
    want 79df75225a75f48b971b2e7ea2a91e325a129d836720df7542d056dfed2971af
    manifest sha256: match
    == 2. reassemble the certificates and check each sha256 and size against object/CERTIFICATES.txt
    cert_2.txt.gz: sha256 match (1 part(s), 39 bytes)
    cert_3.txt.gz: sha256 match (1 part(s), 43 bytes)
    cert_4.txt.gz: sha256 match (1 part(s), 58 bytes)
    cert_5.txt.gz: sha256 match (1 part(s), 72 bytes)
    cert_6.txt.gz: sha256 match (1 part(s), 99 bytes)
    cert_7.txt.gz: sha256 match (1 part(s), 149 bytes)
    cert_8.txt.gz: sha256 match (1 part(s), 281 bytes)
    cert_9.txt.gz: sha256 match (1 part(s), 545 bytes)
    cert_10.txt.gz: sha256 match (1 part(s), 1287 bytes)
    cert_11.txt.gz: sha256 match (1 part(s), 2948 bytes)
    cert_12.txt.gz: sha256 match (1 part(s), 7313 bytes)
    cert_13.txt.gz: sha256 match (1 part(s), 18218 bytes)
    cert_14.txt.gz: sha256 match (1 part(s), 47267 bytes)
    cert_15.txt.gz: sha256 match (1 part(s), 124007 bytes)
    cert_16.txt.gz: sha256 match (1 part(s), 331263 bytes)
    cert_17.txt.gz: sha256 match (1 part(s), 892536 bytes)
    cert_18.txt.gz: sha256 match (3 part(s), 2410425 bytes)
    cert_19.txt.gz: sha256 match (7 part(s), 6550060 bytes)
    cert_20.txt.gz: sha256 match (18 part(s), 17860164 bytes)
    cert_21.txt.gz: sha256 match (1 part(s), 48911418 bytes)
    cert_22.txt.gz: sha256 match (1 part(s), 134933581 bytes)
    orders available: 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 
    == 3. Python checker (check_odd_graceful.py, standard library): every line of every available certificate
    order 2: 1 lines, 1 distinct odd-gracefully labelled trees, A000055(2) = 1 (Otter) PASS
    order 3: 1 lines, 1 distinct odd-gracefully labelled trees, A000055(3) = 1 (Otter) PASS
    order 4: 2 lines, 2 distinct odd-gracefully labelled trees, A000055(4) = 2 (Otter) PASS
    order 5: 3 lines, 3 distinct odd-gracefully labelled trees, A000055(5) = 3 (Otter) PASS
    order 6: 6 lines, 6 distinct odd-gracefully labelled trees, A000055(6) = 6 (Otter) PASS
    order 7: 11 lines, 11 distinct odd-gracefully labelled trees, A000055(7) = 11 (Otter) PASS
    order 8: 23 lines, 23 distinct odd-gracefully labelled trees, A000055(8) = 23 (Otter) PASS
    order 9: 47 lines, 47 distinct odd-gracefully labelled trees, A000055(9) = 47 (Otter) PASS
    order 10: 106 lines, 106 distinct odd-gracefully labelled trees, A000055(10) = 106 (Otter) PASS
    order 11: 235 lines, 235 distinct odd-gracefully labelled trees, A000055(11) = 235 (Otter) PASS
    order 12: 551 lines, 551 distinct odd-gracefully labelled trees, A000055(12) = 551 (Otter) PASS
    order 13: 1301 lines, 1301 distinct odd-gracefully labelled trees, A000055(13) = 1301 (Otter) PASS
    order 14: 3159 lines, 3159 distinct odd-gracefully labelled trees, A000055(14) = 3159 (Otter) PASS
    order 15: 7741 lines, 7741 distinct odd-gracefully labelled trees, A000055(15) = 7741 (Otter) PASS
    order 16: 19320 lines, 19320 distinct odd-gracefully labelled trees, A000055(16) = 19320 (Otter) PASS
    order 17: 48629 lines, 48629 distinct odd-gracefully labelled trees, A000055(17) = 48629 (Otter) PASS
    order 18: 123867 lines, 123867 distinct odd-gracefully labelled trees, A000055(18) = 123867 (Otter) PASS
    order 19: 317955 lines, 317955 distinct odd-gracefully labelled trees, A000055(19) = 317955 (Otter) PASS
    order 20: 823065 lines, 823065 distinct odd-gracefully labelled trees, A000055(20) = 823065 (Otter) PASS
    order 21: 2144505 lines, 2144505 distinct odd-gracefully labelled trees, A000055(21) = 2144505 (Otter) PASS
    order 22: 5623756 lines, 5623756 distinct odd-gracefully labelled trees, A000055(22) = 5623756 (Otter) PASS
    == 4. controls: damaged copies of the order-13 certificate must FAIL
    order 13: line 1: edge differences are not {1, 3, ..., 23} FAIL
    control 1: FAIL as expected
    order 13: lines 1300, distinct trees 1300, but A000055(13) = 1301 FAIL
    control 2: FAIL as expected
    order 13: line 1301: duplicate tree FAIL
    control 3: FAIL as expected
    == 5. second checker (ogcheck.c, C): regenerates all trees of order n by leaf addition and matches the certificate
    order 2: regenerated 1 trees
    order 2: certificate lines 1, valid labelings 1, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 2
    ogcheck order 2: regenerated 1 = A000055(2)
    order 3: regenerated 1 trees
    order 3: certificate lines 1, valid labelings 1, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 3
    ogcheck order 3: regenerated 1 = A000055(3)
    order 4: regenerated 2 trees
    order 4: certificate lines 2, valid labelings 2, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 4
    ogcheck order 4: regenerated 2 = A000055(4)
    order 5: regenerated 3 trees
    order 5: certificate lines 3, valid labelings 3, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 5
    ogcheck order 5: regenerated 3 = A000055(5)
    order 6: regenerated 6 trees
    order 6: certificate lines 6, valid labelings 6, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 6
    ogcheck order 6: regenerated 6 = A000055(6)
    order 7: regenerated 11 trees
    order 7: certificate lines 11, valid labelings 11, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 7
    ogcheck order 7: regenerated 11 = A000055(7)
    order 8: regenerated 23 trees
    order 8: certificate lines 23, valid labelings 23, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 8
    ogcheck order 8: regenerated 23 = A000055(8)
    order 9: regenerated 47 trees
    order 9: certificate lines 47, valid labelings 47, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 9
    ogcheck order 9: regenerated 47 = A000055(9)
    order 10: regenerated 106 trees
    order 10: certificate lines 106, valid labelings 106, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 10
    ogcheck order 10: regenerated 106 = A000055(10)
    order 11: regenerated 235 trees
    order 11: certificate lines 235, valid labelings 235, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 11
    ogcheck order 11: regenerated 235 = A000055(11)
    order 12: regenerated 551 trees
    order 12: certificate lines 551, valid labelings 551, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 12
    ogcheck order 12: regenerated 551 = A000055(12)
    order 13: regenerated 1301 trees
    order 13: certificate lines 1301, valid labelings 1301, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 13
    ogcheck order 13: regenerated 1301 = A000055(13)
    order 14: regenerated 3159 trees
    order 14: certificate lines 3159, valid labelings 3159, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 14
    ogcheck order 14: regenerated 3159 = A000055(14)
    order 15: regenerated 7741 trees
    order 15: certificate lines 7741, valid labelings 7741, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 15
    ogcheck order 15: regenerated 7741 = A000055(15)
    order 16: regenerated 19320 trees
    order 16: certificate lines 19320, valid labelings 19320, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 16
    ogcheck order 16: regenerated 19320 = A000055(16)
    order 17: regenerated 48629 trees
    order 17: certificate lines 48629, valid labelings 48629, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 17
    ogcheck order 17: regenerated 48629 = A000055(17)
    order 18: regenerated 123867 trees
    order 18: certificate lines 123867, valid labelings 123867, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 18
    ogcheck order 18: regenerated 123867 = A000055(18)
    order 19: regenerated 317955 trees
    order 19: certificate lines 317955, valid labelings 317955, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 19
    ogcheck order 19: regenerated 317955 = A000055(19)
    order 20: regenerated 823065 trees
    order 20: certificate lines 823065, valid labelings 823065, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 20
    ogcheck order 20: regenerated 823065 = A000055(20)
    order 21: regenerated 2144505 trees
    order 21: certificate lines 2144505, valid labelings 2144505, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 21
    ogcheck order 21: regenerated 2144505 = A000055(21)
    order 22: regenerated 5623756 trees
    order 22: certificate lines 5623756, valid labelings 5623756, invalid 0, duplicate trees 0, missing trees 0, extra trees 0
    PASS order 22
    ogcheck order 22: regenerated 5623756 = A000055(22)
    ogcheck control (swapped labels): FAIL as expected
    == summary: orders checked: 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 
    PASS

Wall time of run 2: 4m59.281s.
