# How the object was found

Source: the contributor's search snapshot for the DNA-code targets (the folder dna_codes in Argon's 2026-10-19 snapshot, read-only). This folder holds the code and the notes, sanitised: every absolute local path was replaced by {WORKDIR}.

Files here:
- PREREG.md: the pre-registration written before the runs (copied as written, apart from path sanitising; it contains a stray unfinished sentence in section 3, Attack A, step 2, which we left in).
- RESULTS.md: the contributor's result summary for the whole batch of cells; this package is the single cell A_4^GC,RC(n,d,w) (n=10 d=6 w=5) (n=10, d=6, w=5).
- dna_search.c: the C search program (modes lns, walksat, exact and orbit; options -n, -d, -w, --rc, -t, --threads, --target, --step, --flip, --rcgen, --mode, -o, --seed, as read from its main function).
- algebraic_dna.py, delsarte_dna.py, generate_bound_certificates.py, test_ag24_rc.py, test_col_perm_rc.py: the algebraic constructions and bound tools used for other cells of the batch.
- verify_dna_codes.py and bounds_audit.py: the contributor's own verifier and a table audit. bounds_audit.py reads a saved copy of the King page, which is a third-party page and is not shipped here.

Exact commands: the snapshot does not record the command lines that produced this object. The snapshot has no command log. RESULTS.md names the method for this cell in its tables (see the row for n=10, d=6) and the options above are the only documented interface. The compiled binary in the snapshot was not copied; build it yourself, for example with a C compiler and the pthread option (this build line is our suggestion, not a recorded command).

Not shipped: the saved King page, the arXiv sources and the survey archive (third-party material; they are named and linked in ../README.md).
