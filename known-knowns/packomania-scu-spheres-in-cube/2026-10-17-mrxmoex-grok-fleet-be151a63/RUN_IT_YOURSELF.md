# Run it yourself
    sh verify-it-yourself/run_checks.sh            # fast path, N=83 and N=507
    sh verify-it-yourself/run_checks.sh --rowcount # + the 285-file N-1 list (downloads ~182 MB)
Requires Python 3 (standard library only) and network access to https://packomania.com/. Nothing from Packomania is bundled. Each source is downloaded at run time, and its sha256 and Last-Modified are printed and compared with SOURCES.csv. If Packomania has updated a file, the script says so. It prints FAIL if the posted coordinates now certify the posted radius.
To re-derive the list offline from an archive you have extracted yourself: python3 how-we-built-it/sweep_rowcount.py <dir>
