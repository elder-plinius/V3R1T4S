# Run it yourself

Fresh shell, from this package folder. Requirements: python3 (standard library only); optionally a C compiler `cc`.

## 1. Verify the certificates

    sh verify-it-yourself/run_checks.sh

What it does, in order:
1. Checks that the sha256 of object/CERTIFICATES.txt is
   79df75225a75f48b971b2e7ea2a91e325a129d836720df7542d056dfed2971af.
2. Reassembles each certificate (object/certs/cert_N.txt.gz, or its .partNN pieces in order) and checks its sha256
   and size against object/CERTIFICATES.txt. Orders 2..20 must be present. Orders 21 and 22 are checked if
   large-files/cert_21.txt.gz and large-files/cert_22.txt.gz exist; otherwise the script says "not present" and
   leaves them out of the summary.
3. Runs verify-it-yourself/check_odd_graceful.py on every available order. The checker was written from the
   definition and uses the Python standard library only. For each line it checks: the parent array is a tree on n
   vertices; the labels are distinct in [0, 2n-3]; and the n-1 edge differences are exactly {1, 3, ..., 2n-3}. It
   also checks that the tree is not a duplicate (centre-rooted AHU canonical form). It then requires the number of
   lines = the number of distinct trees = A000055(n), computed from Otter's formula. Expected, e.g.:
   `order 20: 823065 lines, 823065 distinct odd-gracefully labelled trees, A000055(20) = 823065 (Otter) PASS`
4. Controls, all of which must FAIL: the order-13 certificate with two labels swapped in one line; with one tree
   removed; with one tree removed and another duplicated.
5. If `cc` exists, it compiles verify-it-yourself/ogcheck.c. This second checker, in C, regenerates every tree of
   order n by adding a leaf to every tree of order n-1, deduplicates by canonical code, and matches the certificate
   against that set (no missing, duplicate or extra tree). It runs the checker on every available order and requires
   the regenerated count to equal A000055(n). Expected, e.g.: `PASS order 20` and
   `ogcheck order 20: regenerated 823065 = A000055(20)`. The swapped-label control must FAIL here too.

The last line is `PASS` (exit code 0) or `FAIL` (exit code 1). The line before it lists the orders checked.

By hand:

    python3 verify-it-yourself/check_odd_graceful.py 17 object/certs/cert_17.txt.gz
    cc -O2 -o ogcheck verify-it-yourself/ogcheck.c && gunzip -c object/certs/cert_17.txt.gz | ./ogcheck 17 -

## 2. Orders 21 and 22

Their certificates are too large for this package. They are pinned in object/CERTIFICATES.txt:

    10b82e2c5e10113c38bb493ef254c29bf22ee93e046f0dcf0055c23f6f0ddf29  48911418 bytes  cert_21.txt.gz
    011e5e85c3ea6bddf2ded0621907680e365ad6278ac8876dde86c0884ff03070  134933581 bytes  cert_22.txt.gz

Put both files in a folder large-files/ next to object/ and rerun step 1. It then checks orders 2..22 (about 5
minutes and about 1 GB of memory or more). You can also rebuild them with the search in how-we-built-it/ (section 3), which
reproduces the same lines. Public archive location: see the pull request description (to be added by the
submitter).

## 3. Rebuild the certificates

See how-we-built-it/BUILD.md. Briefly (needs networkx 3.7 and gcc with OpenMP):

    sh how-we-built-it/run_all.sh        # rebuild/cert_N.txt for N = 2..22, about 5 minutes on 8 cores

## 4. Check the integrity of the package

    sha256sum -c SHA256SUMS
