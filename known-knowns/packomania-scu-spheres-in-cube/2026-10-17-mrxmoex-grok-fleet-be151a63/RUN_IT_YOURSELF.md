# Run it yourself
    sh verify-it-yourself/run_checks.sh            # fast path, N=83 and N=507
    sh verify-it-yourself/run_checks.sh --rowcount # + the 285-file N-1 list (downloads ~182 MB)
Requires Python 3 (standard library only) and network access to https://packomania.com/. Nothing from Packomania is bundled. Each source is downloaded at run time, and its sha256 and Last-Modified are printed and compared with SOURCES.csv. If Packomania has updated a file, the script says so. If scu83.txt / scu507.txt differ from SOURCES.csv, the cell is reported as "replaced upstream" (Packomania replaced both on 17 Oct 2026, so the original files cannot be re-checked live) and the last line is `REPLACED UPSTREAM`. If the archive differs, the 285-file list is reported as a dated snapshot.
To re-derive the list offline from an archive you have extracted yourself: python3 how-we-built-it/sweep_rowcount.py <dir>
