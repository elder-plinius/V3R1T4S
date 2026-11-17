# How the certificates were built (exact commands)

Run from the package folder in a fresh shell. Needs a C compiler with OpenMP (gcc), python3 and networkx
(requirements.txt pins networkx==3.7, the version used). The search is deterministic: tree number t of order n is
searched with seed t + 12345, whatever the thread count, so the output depends only on the order in which networkx
lists the trees.

    python3 -m pip install -r how-we-built-it/requirements.txt
    sh how-we-built-it/run_all.sh                      # writes rebuild/cert_N.txt, N = 2..22 (about 5 minutes on 8 cores)

Single order, by hand:

    cc -O3 -fopenmp -o oglabel how-we-built-it/oglabel.c
    python3 how-we-built-it/gen_trees.py 18 | ./oglabel 18 200 20000 > cert_18.txt

To compare with the shipped files, compare the uncompressed text (gzip headers carry no meaning):

    python3 -c "import gzip,sys;sys.stdout.buffer.write(gzip.decompress(b''.join(open(p,'rb').read() for p in sorted(sys.argv[1:]))))" object/certs/cert_18.txt.gz.part* | cmp - cert_18.txt && echo identical

Checked on the build machine on 2026-11-01: rebuilds of orders 13 and 18 were byte-identical to the uncompressed
certificates.

## Files
- gen_trees.py: lists every free tree on n vertices with networkx.nonisomorphic_trees (Wright, Richmond, Odlyzko and
  McKay's algorithm) and prints each as a BFS parent array.
- oglabel.c: searcher S1. Places the odd differences from the largest (2n-3) down to 1; each difference labels one new
  vertex next to the already-labelled subtree. Candidates are tried in random order with a node budget (20000) and
  up to 200 restarts. A tree that exhausts every restart would be printed with FAIL; none did (search_log.txt:
  fails=0 at every order, 161 s for the 5,623,756 trees of order 22).
- run_all.sh: the loop over orders 2..22.
- search_log.txt: the run's log (trees, fails and seconds per order).
- PREREG.md: the run's preregistration, copied unchanged (frozen 2026-11-01T02:28:42Z, before any search output). It
  states null_test: not needed (explicit labelings checked deterministically).
- The trees came from networkx, not nauty's gentreeg (not installed on the build machine). Completeness does not rest
  on the generator: both checkers in verify-it-yourself/ establish it independently.
