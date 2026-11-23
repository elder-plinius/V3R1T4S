# The object: odd-graceful labelings of every tree on 10 to 23 vertices

The object is fourteen certificate files, one per order n. Each is plain text, one line per unlabeled tree on n vertices:

    n;u-v,u-v,...;l0,l1,...,l(n-1)[;search statistics]

Vertices are 0..n-1, the second field lists the n-1 edges, and li is the label of vertex i. The labels are an
injection into {0, 1, ..., 2q-1} (q = n-1) whose edge differences |li-lj| are exactly the odd numbers
{1, 3, ..., 2q-1}. That is an odd-graceful labeling (Gnanajothi 1991). Any fourth field holds search
statistics (a node or attempt counter) and is ignored by the checkers; it is not q and is not part of the
labeling.

Files of at most 1 MB (orders 10 through 15) are also copied into this folder. The larger files stay out of
git (kit/SUBMIT.md section 1). All fourteen files are hosted as one archive:

| file | lines (trees) | bytes | sha256 |
|---|---|---|---|
| cert_n10.txt | 106 | 7085 | b497ceb42712280ffc49c74b9f22447d5d84b70aef0d92e88812cf3fd68e4be2 |
| cert_n11.txt | 235 | 17723 | 12dd98a4d5408a8d4b68acc8d95edf6d60b452206d50d5cc1cff9173bef57867 |
| cert_n12.txt | 551 | 46090 | e2264df0545f16fcefdf3ca2e2c3f7435db2aa7daa4d6f9aa33db85933d3d505 |
| cert_n13.txt | 1301 | 119910 | b559c770f7f796749d050c7b134ae1e647d49fe1fbec41b1fa3ef188a84e1042 |
| cert_n14.txt | 3159 | 317942 | 842306d831786e624060e9b82da01bcc527513388ef8286b03fe8e971c223bfe |
| cert_n15.txt | 7741 | 846429 | 983c0b008e013b725d8689f94c7b80edd30956239a0a5b8b6d683710f1513d52 |
| cert_n16.txt | 19320 | 2283281 | 0e517e442cdb5562b3ab0521b2576dffa6c6dbfcfa251ae91423d6ae0f031755 |
| cert_n17.txt | 48629 | 6176493 | cf196cf24bca2168f3ef4d51ecb8ada6e5f1167297225abcb41035fac867c02f |
| cert_n18.txt | 123867 | 16849184 | 5d1ebc640d6264e337ce99c202be535f887d072017ff668119e66a16f0895781 |
| cert_n19.txt | 317955 | 46103423 | fe468e2ff8cc3f8d24e438f8b353a4e582c2bcf10ba747a202cff345db23f46c |
| cert_n20.txt | 823065 | 126707747 | 8383bf2e73a5a281adf95a0467e0130dc0a899b5d5bd7bbcd5a2f0b0263b5168 |
| cert_n21.txt | 2144505 | 349304494 | f32ed9fed86d6cdcc0c577cf15dccc7ef265e4b5a2550e0ff5cc6a8a9d5e1794 |
| cert_n22.txt | 5623756 | 966132895 | 995ed1508733f46aa28210b1b808e596eabd286c1984271aeae8dfec983060c5 |
| cert_n23.txt | 14828074 | 2679334720 | d25faee17d7c798dbe7f6d4acc882cb82f924a537de4c8620ed61264f79ecf0e |

The same hashes are in `object/certificates.sha256` (sha256sum format), which `run_checks.sh` uses. Line counts equal A000055(n).

The gzip of cert_n23.txt (not in the archive; the archive holds the plain text file) has
sha256 483c524995e2c184c1f5a7aeda65a69d44a97ac552c3c6177374bc4b13435520 and is 466729481 bytes.

archive_name: odd-graceful-trees-10-23-certificates.tar.xz
archive_bytes: 271015048
archive_sha256: f89ddd847de5ea066c05730800a17ac01f9ee694c346638d40d1b1b0dc526713
archive_url: https://zenodo.org/records/24322888/files/odd-graceful-trees-10-23-certificates.tar.xz?download=1
archive_doi: 10.5281/zenodo.24322888

The archive is published on Zenodo under CC BY 4.0 (https://doi.org/10.5281/zenodo.24322888). It is a tar file compressed with xz; it unpacks to
the fourteen files above, with no folder. `run_checks.sh` checks the bundled
orders 10..15 and the sample in this folder, and checks 16..23 when the files are placed in
`certificates/` or CERT_DIR, or by fetching archive_url.

`object/sample_labelings.txt` (in this folder) repeats, in the same format, ten lines taken from orders
10, 16, 20 and 23, as a spot check only, not a census.
