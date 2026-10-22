# How the object was built (contributor sources, sanitised)

Contents, copied from the contributor's snapshot: PREREG.md (the preregistration), RESULTS.md (the contributor's report, prose only), verify_shannon.py (the contributor's own verifier, kept for completeness; the package's checkers are in verify-it-yourself/ and were written from the definitions). Absolute local paths were replaced by {WORKDIR}.

Commands as recorded: the snapshot documents one command, running verify_shannon.py with python3 from the results folder of the working directory ({WORKDIR}); it writes shannon_certificates.json, whose C7 entry (key new_record_best) is read from object/argon_shannon_certificates.json (the whole file, byte for byte). The search runs that produced the schedule are not recorded in the snapshot as commands or logs; only the resulting schedule is, and the snapshot does not contain the search code for it. The extra data files in object/ (base_g5.json, cert_input.json, bpz_lean_c7_schedule.json) were added by the panel, not by the contributor.

Known errors in RESULTS.md prose: titles and dates of the cited papers, the codebook sizes, and some decimals past digit 41. The numbers in object/ and the checker output in verify-it-yourself/RECEIPTS.md are the ones to rely on.

Third-party code and data (the BPZ Lean repository, Tandon's repository, the arXiv sources) are named in README.md and not copied.
