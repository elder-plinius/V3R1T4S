# Run it yourself (from this folder, fresh shell)

Fast exact checks (Python 3.8+, standard library; under a second):

    sh verify-it-yourself/run_checks.sh          # last line: PASS

Full exhaustive certificate (Go >= 1.21, Python 3 with numpy; ~12 minutes on 6 cores, ~2 GB memory):

    PYTHON=python3 FULL=1 sh verify-it-yourself/run_checks.sh
    # last line: PASS (full: counts reproduced byte for byte, 7 of 7 links certified)

What FULL does, step by step (you can run these by hand from a copy of object/code):

    cd code/cert && go build -o cert.exe . && cd ../..       # any name works; chain.py calls code/cert/cert.exe
    ./code/cert/cert.exe 3 3 3 6 6 counts counts.txt          # all 2^27 states of the 3x3x3 block
    cmp counts.txt <package>/object/counts_b333_s6.txt        # must be identical (sorted, deterministic)
    python3 code/chain.py counts.txt chainB q1=501/1000 2317/5000 9/20 1781/4000
    python3 code/chain.py counts.txt chainA q1=1781/4000 1109/2500 443/1000 1107/2500 4427/10000

Each link prints "CERTIFICATE: PASS (p = ..., q = ...)" and its worst up-set margin; compare with
how-we-built-it/outputs/chainB_summary.txt and chainA_summary.txt (links 4-7 there). cert.exe arguments:
a b c workers minSize mode ...; the worker count changes speed (and the last bits of the float bounds in the laws
files), never the pass/fail result. If your Go is older than the go.mod line, see ERRATA.md.

How the object was built: object/PROOF.md is the argument; object/code is the certificate engine (cert/main.go:
exhaustive enumeration and outward-rounded interval laws; cert.py: exact rational trace laws, float enclosures and
the exact integer up-set check; upsets.py: the 7581 up-sets of {0,1}^5; chain.py: runs the links). The block rule
(largest component, face-weight tie-break, empty below 6 sites) was chosen with the float probes in how-we-built-it/.
