# The object: super edge-magic labelings of every tree on 18 to 25 vertices

Eight certificate files, one per order n. Plain text (n >= 21 xz-compressed), one line per unlabeled tree:

    n;u-v,u-v,...;l0,l1,...,l(n-1)[;search statistics]

Vertices are 0..n-1, the second field lists the n-1 edges, li is the label of vertex i. The labels are a bijection onto
{1..n} whose n-1 edge sums are consecutive integers (a super edge-magic labeling). Further fields are search statistics
and are ignored by the checkers.

| file | trees | bytes | sha256 |
|---|---|---|---|
| cert_n18.txt | 123867 | 17089949 | 309673ed41bc341d17833f4a07601fd44136da06ad45a24338d1d70b30a627f8 |
| cert_n19.txt | 317955 | 46813524 | 98dc47816ccf6ed93acf6021a5e9f76013f801db196862dad0cabafc268436c0 |
| cert_n20.txt | 823065 | 128710366 | 063a327ec5540e6a17a6d94e6ad4a3cfa3a8c85b928f9ebd13eb4ab20498bdb5 |
| cert_n21.txt.xz | 2144505 | 53099036 | 88af13db7d462dba3551df35eecaf294d12bb1838d7ebb2a9b6552496c1fb356 |
| cert_n22.txt.xz | 5623756 | 147195652 | 58933786e80b94272f3a5da81b88a3ed8dafcfe37f9e4f8045b1af2c247b2b8d |
| cert_n23.txt.xz | 14828074 | 406649516 | 0a5411a53397a65c07b3d8b68da202370228088395c7c9e51f3d7a737ab46ad5 |
| cert_n24.txt.xz | 39299897 | 1126133720 | 76627c15fef404c1836805cafe34b21385049f197856a67e8ee29d418d8866c7 |
| cert_n25.txt.xz | 104636890 | 3108424328 | a349985cc70fbdc72eaa634d689b708197aaa55768ac68a87b84403092361197 |

The same hashes are in `object/certificates.sha256`. Every file is over 1 MB, so none is in this folder
(kit/SUBMIT.md section 1). All are on Zenodo, CC BY 4.0, version v3 of the record that pull requests #917 and #945
used. Orders 18 to 20 come from the p1 archive (unchanged), 21 and 22 from the p2 package (#945), 23 to 25 are new.
The n = 23 to 25 files are the search output merged with the labelings of the trees the time-capped search left over
(see how-we-built-it/); every labeling in them was checked against the definition before it was written.
On Zenodo the n = 23 to 25 files are named cert_n23_merged.txt.xz, cert_n24_merged.txt.xz and cert_n25_merged.txt.xz
(same bytes and hashes as in the table); run_checks.sh saves them as cert_nN.txt.xz.

archive_name: sem-trees-18-20-certificates.tar.xz
archive_bytes: 29618152
archive_sha256: 390d1698ff6e9563ed2e41a645cff865a05ab6b5427ece910e5bdda6ed82cc8b
archive_url: https://zenodo.org/records/24116616/files/sem-trees-18-20-certificates.tar.xz?download=1
n21_url: https://zenodo.org/records/24116616/files/cert_n21.txt.xz?download=1
n22_url: https://zenodo.org/records/24116616/files/cert_n22.txt.xz?download=1
n23_url: https://zenodo.org/records/24116616/files/cert_n23_merged.txt.xz?download=1
n24_url: https://zenodo.org/records/24116616/files/cert_n24_merged.txt.xz?download=1
n25_url: https://zenodo.org/records/24116616/files/cert_n25_merged.txt.xz?download=1
record_doi: 10.5281/zenodo.24116616 (record https://zenodo.org/records/24116616; concept DOI of all versions: 10.5281/zenodo.23918678)
