# Run it yourself

Fresh shell, from this package folder. Requirements: python3 (standard library only). Optional: a C compiler `cc`;
nauty 2.8.8 geng and labelg (set NAUTY_BIN to their folder).

## 1. Verify the certificates

    sh verify-it-yourself/run_checks.sh

What it does, in order:
1. Checks that the sha256 of object/CERTIFICATES.txt is
   765276f52743141c9fa508cbe9558c8cd2814e5a7e4711e8992fd5f57d985ffc.
2. Reassembles each certificate (object/certs/cert_N.txt.gz, or its .partNN pieces in order). It checks the sha256
   and size of the gzip file and of the uncompressed text against object/CERTIFICATES.txt. Orders 4..20 must be
   present. Order 22 is checked if large-files/cert_22.txt.gz or large-files/cert_22.txt exists. Otherwise the
   script says "not present" and leaves it out of the summary.
3. Runs verify-it-yourself/check_graceful_cubic.py on every available order. This checker was written from the
   definition, uses the Python standard library only and does not use nauty. For each line it checks:
   - strict graph6 (vertex count, length, byte range, zero padding);
   - n vertices, every degree 3, connected;
   - exactly n labels, distinct integers in [0, 3n/2];
   - the 3n/2 edge differences are exactly {1, ..., 3n/2}.

   It then computes an exact canonical form of each graph. The seed colours are the distance profile of each vertex;
   colour refinement and individualisation explore the whole search tree, and the least relabelled edge list is
   kept. It requires the number of lines = the number of distinct forms = A002851. Expected, e.g.:
   `order 20: 510489 lines, 0 bad lines, 0 duplicates, 510489 pairwise non-isomorphic gracefully labelled connected cubic graphs, A002851 = 510489 PASS`
4. Runs controls on the order-10 certificate, all of which must FAIL:
   - two labels swapped in one line;
   - one graph removed;
   - one graph removed and another repeated;
   - one graph removed and another added again as a randomly relabelled isomorphic copy, with its labeling carried
     along so the line is still valid. This one tests the isomorphism detection.
5. If `cc` exists, compiles verify-it-yourself/checkK.c, a second per-line checker in C, and runs it on every
   available order. The swapped-label control must FAIL there too. If NAUTY_BIN is set, it also builds labelg
   canonical forms of the certificate graphs and of a fresh `geng -cq -d3 -D3 n` run (16 res/mod slices, PAR
   workers, default 4), and requires the two sorted lists to be identical with no duplicates.

The last line is `PASS` (exit code 0) or `FAIL` (exit code 1). The line before it lists the orders checked.

By hand:

    python3 verify-it-yourself/check_graceful_cubic.py 18 object/certs/cert_18.txt.gz

## 2. Order 22

Its certificate is too large for this package. It is pinned in object/CERTIFICATES.txt (both forms work):

    6439fa6bb934916ff471f66a582728eff46b6e5cd7282f6835a468a4e5d835d1  196915682 bytes  cert_22.txt.gz
    dbbe54e5a91052a9ac25375d57f5fea19e7b3e5b4d4a41eea1a4cec9772eb39d  726142050 bytes  cert_22.txt (uncompressed)

Put either file in a folder large-files/ next to object/ and rerun step 1. It then checks orders 4..22. The order-22
step takes about 3 minutes on 8 cores and about 2 GB of memory. Public archive location: see the pull request
description (to be added by the submitter). You can also rebuild the file with how-we-built-it/ (section 3). The
search is deterministic for a given geng output, so it reproduces the same lines.

The gzip files were made with `gzip -9 -n` (GNU gzip). If another gzip gives a different .gz sha256, compare the
uncompressed sha256 instead; that is the value the panel checked.

## 3. Rebuild the certificates

See how-we-built-it/BUILD.md. Briefly (needs gcc and nauty 2.8.8 geng):

    cc -O3 -o how-we-built-it/glab how-we-built-it/glab.c
    NAUTY_BIN=/path/to/nauty OUT=./rebuild sh how-we-built-it/run_all.sh     # orders 4..22; order 22 takes hours

## 4. Check the integrity of the package

    sha256sum -c SHA256SUMS
