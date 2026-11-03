# The object: super edge-magic labelings of every tree on 18, 19 and 20 vertices

The object is three certificate files, one per order n. Each is plain text, one line per unlabeled tree on n vertices:

    n;u-v,u-v,...;l0,l1,...,l(n-1)[;search statistics]

Vertices are 0..n-1, the second field lists the n-1 edges, and li is the label of vertex i. The labels are a
bijection onto {1..n} whose n-1 edge sums li+lj are consecutive integers (a super edge-magic labeling). Any fourth or
fifth field holds search statistics (nodes, attempts, or the word `caterpillar`) and is ignored by the checkers.

Each file is over 1 MB, so none is in this folder (kit/SUBMIT.md section 1). They are hosted as one archive:

| file | lines (trees) | bytes | sha256 |
|---|---|---|---|
| cert_n18.txt | 123867 | 17089949 | 309673ed41bc341d17833f4a07601fd44136da06ad45a24338d1d70b30a627f8 |
| cert_n19.txt | 317955 | 46813524 | 98dc47816ccf6ed93acf6021a5e9f76013f801db196862dad0cabafc268436c0 |
| cert_n20.txt | 823065 | 128710366 | 063a327ec5540e6a17a6d94e6ad4a3cfa3a8c85b928f9ebd13eb4ab20498bdb5 |

The same hashes are in `object/certificates.sha256` (sha256sum format), which `run_checks.sh` uses.

archive_name: sem-trees-18-20-certificates.tar.xz
archive_bytes: 29618152
archive_sha256: 390d1698ff6e9563ed2e41a645cff865a05ab6b5427ece910e5bdda6ed82cc8b
archive_url: https://zenodo.org/records/23918679/files/sem-trees-18-20-certificates.tar.xz?download=1
archive_doi: 10.5281/zenodo.23918679 (record https://zenodo.org/records/23918679)

The archive is published on Zenodo (DOI 10.5281/zenodo.23918679, CC BY 4.0). It is a tar file compressed with xz;
it unpacks to the three files above, with no folder.

`object/hardest_trees_n19_n20.txt` (in this folder) repeats, in the same format, the labelings of the five trees
the searches found hardest: the two at n=19 that needed long restarts and the three at n=20 that were finished by
the caterpillar construction. It is a spot check only, not the certificate.
