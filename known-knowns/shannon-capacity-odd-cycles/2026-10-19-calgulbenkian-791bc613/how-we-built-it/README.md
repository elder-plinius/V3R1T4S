# How the object was built (contributor sources, sanitised)

Contents, copied from the contributor's snapshot: PREREG.md (the preregistration), RESULTS.md (the contributor's report for all six cycles, prose only), verify_shannon.py (the contributor's own verifier, kept for completeness; the package's checker is verify-it-yourself/shannon_check.py, written from the definitions). Absolute local paths were replaced by {WORKDIR}.

Commands as recorded: the snapshot documents one command, running verify_shannon.py with python3 from the results folder of the working directory ({WORKDIR}); it writes shannon_certificates.json, whose C23 entry is shipped as object/argon_shannon_certificates.json (the whole file, byte for byte). The search runs that produced the schedule are not recorded in the snapshot as commands or logs; only the resulting schedule is, and the snapshot does not contain the search code for it.

Known errors in RESULTS.md prose: titles and dates of the cited papers, the C7 codebook sizes, and some decimals past digit 41 are wrong there. The numbers in object/ and the checker output in verify-it-yourself/RECEIPTS.md are the ones to rely on. The C7 sections of RESULTS.md concern a different claim that is not part of this package.

Third-party code and data (the BPZ Lean repository, Tandon's repository, the arXiv sources) are named in README.md and not copied.
