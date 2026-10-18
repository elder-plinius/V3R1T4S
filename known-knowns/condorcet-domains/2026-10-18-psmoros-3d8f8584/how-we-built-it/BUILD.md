# How the object was built (search provenance)

- The n = 20 object comes from the lns-high (code/: lsx.c dlns / restrict / extend, multistart.py, dchain.py, vcycle.py) lens of the contributor's run folder 2026-10-17-2220. Every list
  is the full domain of its final never-condition assignment, enumerated in lexicographic order (`lsx enum` /
  `lsearch enum`), then compressed with `xz -9e` and split with `split -b 1000000` where larger than 1 MB.
- The search: the record paper's one-alternative inductive extension step (arXiv:2601.07336v1, Section 5.1) with
  exact branch and bound on the mixed triples, from the n = 8 maximum of arXiv:2303.15002; pair-LNS (all triples
  through a pair of alternatives re-optimised by exact branch and bound); restriction of polished larger domains by
  deleting one alternative, and extension by cloning one. Each step was time-limited, so a rerun may end elsewhere.
- code/ holds the n = 21 package's copy of the lns-high tools (see its BUILD notes in the header comments);
  build with `cc -O3 -o lsx code/lsx.c -lm`.
- PREREG.md is the frozen rule of the claiming run folder (frozen 2026-10-18T06:09:01Z); the object was
  re-verified, not searched, in that folder.
