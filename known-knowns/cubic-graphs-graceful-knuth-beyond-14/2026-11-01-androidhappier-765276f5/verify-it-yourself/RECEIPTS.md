# Receipts: real output of verify-it-yourself/run_checks.sh

Machine: Linux x86-64, 8 cores, 15 GB RAM, Python 3.13.5, gcc (Debian 14.2.0-19) 14.2.0. Run on 2026-11-01 (America/New_York).

## 1. This package as shipped (orders 4..20; large-files/ absent; NAUTY_BIN not set)

    == 1. sha256 of object/CERTIFICATES.txt
    got  765276f52743141c9fa508cbe9558c8cd2814e5a7e4711e8992fd5f57d985ffc
    want 765276f52743141c9fa508cbe9558c8cd2814e5a7e4711e8992fd5f57d985ffc
    manifest sha256: match
    == 2. reassemble the certificates; check sha256 and size of the .gz and of the uncompressed text
    cert_4.txt.gz: sha256 match (1 part(s); text 11 bytes, sha256 01e273e7e9554a3f...)
    cert_6.txt.gz: sha256 match (1 part(s); text 34 bytes, sha256 c53487802013683e...)
    cert_8.txt.gz: sha256 match (1 part(s); text 129 bytes, sha256 47c4eb488ec72714...)
    cert_10.txt.gz: sha256 match (1 part(s); text 651 bytes, sha256 79dcace00a1b5a6c...)
    cert_12.txt.gz: sha256 match (1 part(s); text 3632 bytes, sha256 7bac76ffc54d31ee...)
    cert_14.txt.gz: sha256 match (1 part(s); text 27182 bytes, sha256 3bf218dc93f7b2b1...)
    cert_16.txt.gz: sha256 match (1 part(s); text 255699 bytes, sha256 98e196335f901be5...)
    cert_18.txt.gz: sha256 match (1 part(s); text 3083661 bytes, sha256 b6404ba8cd5e93a5...)
    cert_20.txt.gz: sha256 match (13 part(s); text 44109825 bytes, sha256 6a0a93da4a1d3ca2...)
    cert_22.txt.gz: not present (external file, order 22 not checked here)
    orders available: 4 6 8 10 12 14 16 18 20 
    == 3. Python checker (check_graceful_cubic.py, standard library): every line, exact canonical forms, A002851
    order 4: 1 lines, 0 bad lines, 0 duplicates, 1 pairwise non-isomorphic gracefully labelled connected cubic graphs, A002851 = 1 PASS
    order 6: 2 lines, 0 bad lines, 0 duplicates, 2 pairwise non-isomorphic gracefully labelled connected cubic graphs, A002851 = 2 PASS
    order 8: 5 lines, 0 bad lines, 0 duplicates, 5 pairwise non-isomorphic gracefully labelled connected cubic graphs, A002851 = 5 PASS
    order 10: 19 lines, 0 bad lines, 0 duplicates, 19 pairwise non-isomorphic gracefully labelled connected cubic graphs, A002851 = 19 PASS
    order 12: 85 lines, 0 bad lines, 0 duplicates, 85 pairwise non-isomorphic gracefully labelled connected cubic graphs, A002851 = 85 PASS
    order 14: 509 lines, 0 bad lines, 0 duplicates, 509 pairwise non-isomorphic gracefully labelled connected cubic graphs, A002851 = 509 PASS
    order 16: 4060 lines, 0 bad lines, 0 duplicates, 4060 pairwise non-isomorphic gracefully labelled connected cubic graphs, A002851 = 4060 PASS
    order 18: 41301 lines, 0 bad lines, 0 duplicates, 41301 pairwise non-isomorphic gracefully labelled connected cubic graphs, A002851 = 41301 PASS
    order 20: 510489 lines, 0 bad lines, 0 duplicates, 510489 pairwise non-isomorphic gracefully labelled connected cubic graphs, A002851 = 510489 PASS
    == 4. controls: damaged copies of the order-10 certificate must FAIL
    order 10: line 1: edge differences are not exactly {1, ..., 15}
    order 10: 19 lines, 1 bad lines, 0 duplicates, 18 pairwise non-isomorphic gracefully labelled connected cubic graphs, A002851 = 19 FAIL
    control 1: FAIL as expected
    order 10: 18 lines, 0 bad lines, 0 duplicates, 18 pairwise non-isomorphic gracefully labelled connected cubic graphs, A002851 = 19 FAIL
    control 2: FAIL as expected
    order 10: line 19: graph isomorphic to line 1 (duplicate)
    order 10: 19 lines, 0 bad lines, 1 duplicates, 18 pairwise non-isomorphic gracefully labelled connected cubic graphs, A002851 = 19 FAIL
    control 3: FAIL as expected
    order 10: line 19: graph isomorphic to line 1 (duplicate)
    order 10: 19 lines, 0 bad lines, 1 duplicates, 18 pairwise non-isomorphic gracefully labelled connected cubic graphs, A002851 = 19 FAIL
    control 4: FAIL as expected
    == 5. optional second checker (checkK.c, C, per-line) and nauty coverage (NAUTY_BIN)
    CHECKK n=4 lines=1 bad=0
    CHECKK n=6 lines=2 bad=0
    CHECKK n=8 lines=5 bad=0
    CHECKK n=10 lines=19 bad=0
    CHECKK n=12 lines=85 bad=0
    CHECKK n=14 lines=509 bad=0
    CHECKK n=16 lines=4060 bad=0
    CHECKK n=18 lines=41301 bad=0
    CHECKK n=20 lines=510489 bad=0
    checkK control (swapped labels): FAIL as expected
    NAUTY_BIN not set: nauty coverage skipped (the Python checker's canonical forms decide completeness)
    == summary: orders checked: 4 6 8 10 12 14 16 18 20 
    PASS

Wall time: 0m14.313s.

## 2. The same package with large-files/cert_22.txt.gz added (orders 4..22)

    == 1. sha256 of object/CERTIFICATES.txt
    got  765276f52743141c9fa508cbe9558c8cd2814e5a7e4711e8992fd5f57d985ffc
    want 765276f52743141c9fa508cbe9558c8cd2814e5a7e4711e8992fd5f57d985ffc
    manifest sha256: match
    == 2. reassemble the certificates; check sha256 and size of the .gz and of the uncompressed text
    cert_4.txt.gz: sha256 match (1 part(s); text 11 bytes, sha256 01e273e7e9554a3f...)
    cert_6.txt.gz: sha256 match (1 part(s); text 34 bytes, sha256 c53487802013683e...)
    cert_8.txt.gz: sha256 match (1 part(s); text 129 bytes, sha256 47c4eb488ec72714...)
    cert_10.txt.gz: sha256 match (1 part(s); text 651 bytes, sha256 79dcace00a1b5a6c...)
    cert_12.txt.gz: sha256 match (1 part(s); text 3632 bytes, sha256 7bac76ffc54d31ee...)
    cert_14.txt.gz: sha256 match (1 part(s); text 27182 bytes, sha256 3bf218dc93f7b2b1...)
    cert_16.txt.gz: sha256 match (1 part(s); text 255699 bytes, sha256 98e196335f901be5...)
    cert_18.txt.gz: sha256 match (1 part(s); text 3083661 bytes, sha256 b6404ba8cd5e93a5...)
    cert_20.txt.gz: sha256 match (13 part(s); text 44109825 bytes, sha256 6a0a93da4a1d3ca2...)
    cert_22.txt.gz: sha256 match (large-files; text 726142050 bytes, sha256 dbbe54e5a91052a9...)
    orders available: 4 6 8 10 12 14 16 18 20 22 
    == 3. Python checker (check_graceful_cubic.py, standard library): every line, exact canonical forms, A002851
    order 4: 1 lines, 0 bad lines, 0 duplicates, 1 pairwise non-isomorphic gracefully labelled connected cubic graphs, A002851 = 1 PASS
    order 6: 2 lines, 0 bad lines, 0 duplicates, 2 pairwise non-isomorphic gracefully labelled connected cubic graphs, A002851 = 2 PASS
    order 8: 5 lines, 0 bad lines, 0 duplicates, 5 pairwise non-isomorphic gracefully labelled connected cubic graphs, A002851 = 5 PASS
    order 10: 19 lines, 0 bad lines, 0 duplicates, 19 pairwise non-isomorphic gracefully labelled connected cubic graphs, A002851 = 19 PASS
    order 12: 85 lines, 0 bad lines, 0 duplicates, 85 pairwise non-isomorphic gracefully labelled connected cubic graphs, A002851 = 85 PASS
    order 14: 509 lines, 0 bad lines, 0 duplicates, 509 pairwise non-isomorphic gracefully labelled connected cubic graphs, A002851 = 509 PASS
    order 16: 4060 lines, 0 bad lines, 0 duplicates, 4060 pairwise non-isomorphic gracefully labelled connected cubic graphs, A002851 = 4060 PASS
    order 18: 41301 lines, 0 bad lines, 0 duplicates, 41301 pairwise non-isomorphic gracefully labelled connected cubic graphs, A002851 = 41301 PASS
    order 20: 510489 lines, 0 bad lines, 0 duplicates, 510489 pairwise non-isomorphic gracefully labelled connected cubic graphs, A002851 = 510489 PASS
    order 22: 7319447 lines, 0 bad lines, 0 duplicates, 7319447 pairwise non-isomorphic gracefully labelled connected cubic graphs, A002851 = 7319447 PASS
    == 4. controls: damaged copies of the order-10 certificate must FAIL
    order 10: line 1: edge differences are not exactly {1, ..., 15}
    order 10: 19 lines, 1 bad lines, 0 duplicates, 18 pairwise non-isomorphic gracefully labelled connected cubic graphs, A002851 = 19 FAIL
    control 1: FAIL as expected
    order 10: 18 lines, 0 bad lines, 0 duplicates, 18 pairwise non-isomorphic gracefully labelled connected cubic graphs, A002851 = 19 FAIL
    control 2: FAIL as expected
    order 10: line 19: graph isomorphic to line 1 (duplicate)
    order 10: 19 lines, 0 bad lines, 1 duplicates, 18 pairwise non-isomorphic gracefully labelled connected cubic graphs, A002851 = 19 FAIL
    control 3: FAIL as expected
    order 10: line 19: graph isomorphic to line 1 (duplicate)
    order 10: 19 lines, 0 bad lines, 1 duplicates, 18 pairwise non-isomorphic gracefully labelled connected cubic graphs, A002851 = 19 FAIL
    control 4: FAIL as expected
    == 5. optional second checker (checkK.c, C, per-line) and nauty coverage (NAUTY_BIN)
    CHECKK n=4 lines=1 bad=0
    CHECKK n=6 lines=2 bad=0
    CHECKK n=8 lines=5 bad=0
    CHECKK n=10 lines=19 bad=0
    CHECKK n=12 lines=85 bad=0
    CHECKK n=14 lines=509 bad=0
    CHECKK n=16 lines=4060 bad=0
    CHECKK n=18 lines=41301 bad=0
    CHECKK n=20 lines=510489 bad=0
    CHECKK n=22 lines=7319447 bad=0
    checkK control (swapped labels): FAIL as expected
    NAUTY_BIN not set: nauty coverage skipped (the Python checker's canonical forms decide completeness)
    == summary: orders checked: 4 6 8 10 12 14 16 18 20 22 
    PASS

Wall time: 2m56.806s.

## 3. As shipped, with NAUTY_BIN set to nauty 2.8.8 geng and labelg and PAR=8 (orders 4..20, nauty coverage on)

Steps 1 to 4 print the same lines as run 1. Step 5 and the summary:

    == 5. optional second checker (checkK.c, C, per-line) and nauty coverage (NAUTY_BIN)
    CHECKK n=4 lines=1 bad=0
    CHECKK n=6 lines=2 bad=0
    CHECKK n=8 lines=5 bad=0
    CHECKK n=10 lines=19 bad=0
    CHECKK n=12 lines=85 bad=0
    CHECKK n=14 lines=509 bad=0
    CHECKK n=16 lines=4060 bad=0
    CHECKK n=18 lines=41301 bad=0
    CHECKK n=20 lines=510489 bad=0
    checkK control (swapped labels): FAIL as expected
    nauty coverage order 4: 1 geng graphs = certificate graphs, no duplicates
    nauty coverage order 6: 2 geng graphs = certificate graphs, no duplicates
    nauty coverage order 8: 5 geng graphs = certificate graphs, no duplicates
    nauty coverage order 10: 19 geng graphs = certificate graphs, no duplicates
    nauty coverage order 12: 85 geng graphs = certificate graphs, no duplicates
    nauty coverage order 14: 509 geng graphs = certificate graphs, no duplicates
    nauty coverage order 16: 4060 geng graphs = certificate graphs, no duplicates
    nauty coverage order 18: 41301 geng graphs = certificate graphs, no duplicates
    nauty coverage order 20: 510489 geng graphs = certificate graphs, no duplicates
    == summary: orders checked: 4 6 8 10 12 14 16 18 20 
    PASS

Wall time: 0m57.515s.
