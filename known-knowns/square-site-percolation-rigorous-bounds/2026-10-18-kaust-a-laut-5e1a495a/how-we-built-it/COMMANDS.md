# How we built it

- code/window.py: the certificate (exact message cones and the domination check). `python window.py 3`
  bisects for the best bound at each depth; `python cert.py 4433/10000 3 out.json` writes the record.
- code/vdbe1996.py: the exact reproduction of the 1996 paper (`python vdbe1996.py`).
- code/validate.py: message passing against brute force on random explicit trees, and the root step
  (`python validate.py 4433/10000 300 2`).
- code/independent/indep.py: the second implementation (`python independent/indep.py margins 3 4433/10000`).
- outputs/: the outputs of these four as run for the claim (2026-10-18T18:44:22Z to 18:44:51Z).
- PREREG.md: the frozen rule (2026-10-18T18:43:48Z). No null test: it is a deterministic exact certificate.
- REPRODUCE.md: the commands the panel was given.
Only the Python standard library is needed.
