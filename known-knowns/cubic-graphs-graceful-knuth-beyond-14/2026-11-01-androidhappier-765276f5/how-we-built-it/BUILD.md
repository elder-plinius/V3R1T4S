# How the certificates were built (exact commands)

Run from the package folder in a fresh shell. Needs a C compiler and nauty 2.8.8 (geng; labelg for the optional
coverage script). Nothing else: the searcher is plain C with no dependencies.

## nauty 2.8.8

The run built geng and labelg from the nauty 2.8.8 source as shipped inside the PyPI sdist pynauty-2.8.8.1
(https://pypi.org/project/pynauty/2.8.8.1/, file pynauty-2.8.8.1.tar.gz, sha256
454d3b0e605d649d13478afb090daef4a152f15c4a337a391fe69fded7e683f2, folder src/nauty2_8_8). The official nauty
distribution (https://users.cecs.anu.edu.au/~bdm/nauty/) works the same. The source is not copied here.

    cd nauty2_8_8 && ./configure
    gcc -O3 -march=native -DMAXN=WORDSIZE -DWORDSIZE=32 -o geng geng.c gtools.c nauty.c nautil.c naugraph.c schreier.c naurng.c
    gcc -O3 -o labelg labelg.c gtools.c gtnauty.c naututil.c nautinv.c gutil2.c gutil1.c traces.c nauty.c nautil.c nausparse.c naugraph.c schreier.c naurng.c
    export NAUTY_BIN=$PWD

Check: `$NAUTY_BIN/geng -cu -d3 -D3 18` reports 41301 graphs.

## The search

    cc -O3 -march=native -o how-we-built-it/glab how-we-built-it/glab.c
    OUT=./rebuild sh how-we-built-it/run_all.sh        # writes rebuild/cert_N.txt, N = 4..22

run_all.sh runs `geng -cq -d3 -D3 n | glab -c` for n = 4..18. For n = 20 and 22, it runs 64 geng res/mod slices
(0/64 .. 63/64, 6 in parallel) and concatenates them in slice order. So the first column of each certificate is
geng's own output, in order. Single order, by hand:

    $NAUTY_BIN/geng -cq -d3 -D3 18 | how-we-built-it/glab -c > cert_18.txt

To compare with the shipped files, compare the uncompressed text:

    cat object/certs/cert_20.txt.gz.part* | gunzip | cmp - rebuild/cert_20.txt && echo identical

## Files
- glab.c: the searcher. It realises the differences q, q-1, ..., 1 in turn by edge-driven backtracking, with a
  randomised vertex order and restarts under growing node limits. With -c, a final complete (uncapped) search runs
  for any graph that exhausts its restarts. No graph needed it: search_log.txt shows fails=0 at every order. Order 22
  took 2,162,456,868 search nodes in total, at most 10,200 for one graph. glab -c prints FAIL only for 2K4 when fed
  disconnected graphs, as expected.
- run_all.sh: the production driver (orders 4..22).
- coverK.sh: the run's nauty coverage check, kept for reference. It needs checkK (verify-it-yourself/checkK.c) and
  the A002851 b-file (https://oeis.org/A002851/b002851.txt) in B002851. verify-it-yourself/run_checks.sh contains
  the same check inline.
- search_log.txt: per-order totals from the run's logs (graphs, fails, search nodes).
- PREREG.md: the run's preregistration, copied unchanged (frozen 2026-11-01T15:20:55Z, before any certificate was
  produced). It states null_test: not needed (explicit labelings checked deterministically).
