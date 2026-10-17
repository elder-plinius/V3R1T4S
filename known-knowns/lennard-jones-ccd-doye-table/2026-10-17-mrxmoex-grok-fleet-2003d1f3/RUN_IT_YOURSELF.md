# Run it yourself
    sh verify-it-yourself/run_checks.sh                 # (A) CCD LJ tables + 6 CCD point files, then (B) CCD Morse table + points/63C; a few seconds
    sh verify-it-yourself/run_checks.sh --with-sources  # (A) also the Nankai 2004 archive (4.6 MB) and Barron 2005 PDF hash
Requires Python 3 (standard library only) and network access. No CCD data is bundled. Each source is downloaded at run time, and its sha256 and Last-Modified are printed and compared with SOURCES.csv. (A) is verify-it-yourself/repro_ccd_lj_errata.py and (B) is verify-it-yourself/repro_ccd_morse_63c.py; each can also be run on its own. Prints FAIL if any table entry no longer disagrees with its file, or if the 63C sign has been fixed (for example, after a CCD fix). Expected last line: PASS.
