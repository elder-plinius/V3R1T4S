# The object: super edge-magic labelings of every tree on 18 to 22 vertices

Five certificate files, one per order n. Each is plain text (n = 21, 22 xz-compressed), one line per unlabeled tree:

    n;u-v,u-v,...;l0,l1,...,l(n-1)[;search statistics]

Vertices are 0..n-1, the second field lists the n-1 edges, and li is the label of vertex i. The labels are a bijection
onto {1..n} whose n-1 edge sums li+lj are consecutive integers (a super edge-magic labeling). Further fields are search
statistics and are ignored by the checkers.

| file | lines (trees) | bytes | sha256 |
|---|---|---|---|
| cert_n18.txt | 123867 | 17089949 | 309673ed41bc341d17833f4a07601fd44136da06ad45a24338d1d70b30a627f8 |
| cert_n19.txt | 317955 | 46813524 | 98dc47816ccf6ed93acf6021a5e9f76013f801db196862dad0cabafc268436c0 |
| cert_n20.txt | 823065 | 128710366 | 063a327ec5540e6a17a6d94e6ad4a3cfa3a8c85b928f9ebd13eb4ab20498bdb5 |
| cert_n21.txt.xz | 2144505 | 53099036 | 88af13db7d462dba3551df35eecaf294d12bb1838d7ebb2a9b6552496c1fb356 |
| cert_n22.txt.xz | 5623756 | 147195652 | 58933786e80b94272f3a5da81b88a3ed8dafcfe37f9e4f8045b1af2c247b2b8d |

The same hashes are in `object/certificates.sha256`. Every file is over 1 MB, so none is in this folder
(kit/SUBMIT.md section 1). They are on Zenodo (CC BY 4.0), version v2 of the record, DOI 10.5281/zenodo.23935954, which also holds the orders 18 to 20 archive. Orders 18 to 20 are the archive of the p1 package
(pull request #917), unchanged; orders 21 and 22 are added in a new version of the same Zenodo record.

archive_name: sem-trees-18-20-certificates.tar.xz
archive_bytes: 29618152
archive_sha256: 390d1698ff6e9563ed2e41a645cff865a05ab6b5427ece910e5bdda6ed82cc8b
archive_url: https://zenodo.org/records/23918679/files/sem-trees-18-20-certificates.tar.xz?download=1
n21_url: https://zenodo.org/records/23935954/files/cert_n21.txt.xz?download=1
n22_url: https://zenodo.org/records/23935954/files/cert_n22.txt.xz?download=1
record_doi: 10.5281/zenodo.23935954 (record https://zenodo.org/records/23935954; concept DOI of all versions: 10.5281/zenodo.23918678)
