# Rhombicosidodecahedron certificate: independent C# re-verification of all 192,696 records

## What

A C#/BigInteger exact-Q(sqrt5) program, written from Hervay's paper and data files, accepts all 192,696 records (Domain 12,650, Global 157,458, Local 21,792, Exotic 796) of the sha256-pinned `search.cert`, proves exactly that the record paths are prefix-free and tile the root box (Kraft sum 1), re-checks all 11,231 cells of the 38 zoom-cover files (including that the 48 handed-over cells satisfy the hand-over lemma's hypothesis), and refuses 711 falsity-certified corrupted records, while the paper's hand-proved lemmas (symmetry reduction to D, tube/point/hand-over coverage as mathematics, Bernstein lemma, component soundness) and the claim that the zoom families cover the covered sets are not re-proved, and I personally reproduced Domain, Global, Local, Exotic, covers and cube but not the full 711-control run.

Plainly: Hervay's computer-assisted proof that the rhombicosidodecahedron (RID) is not Rupert (https://github.com/bence-hervay/nopert-rid, commit 802a3ded09535c4a99cef1371ce0d0277c433fa8) ships a certificate of 192,696 records. This package contains a from-scratch verifier in C# (own exact Q(sqrt5) arithmetic on BigInteger, no floating point in any acceptance decision) that was written from the paper's mathematics and the certificate/cover data files, not from the author's Rust or Python code, and that accepts every record (Domain 12,650, Global 157,458, Local 21,792, Exotic 796), checks the tiling of the root box exactly, re-checks the 11,231 zoom-cover cells, and refuses 711 deliberately corrupted records. It is bank partial win p3 of `rupert-open-classical-solids`. It settles none of the nine undecided solids.

## Check it yourself

Needs Python 3.9+, the .NET SDK (8 or newer), a POSIX shell (Git Bash on Windows works) and network access to github.com (the pinned public inputs, about 31 MB, are downloaded and checked by sha256; they are not copied into this package):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS` (just before it the log shows `OVERALL: ALL CHECKS PASSED` and `CONTROLS total: 711 certified-false corrupted claims, 711 refused, 0 accepted`). Rough laptop time: 5 to 8 minutes (about 3 minutes of verification on 4 threads, plus download and build). Any changed byte in `object/` gives `FAIL`. Real output is in `verify-it-yourself/RECEIPTS.md`; `RUN_IT_YOURSELF.md` has the individual commands.

## Compared to

| target | cell | table value | status page | fetched (UTC) | this package |
|---|---|---|---|---|---|
| rupert-open-classical-solids | p3: independent re-verification of Hervay's RID certificate (192,696 records) in a language other than Rust or Python | no table cell; the status page does not mention the RID certificate. Prior art found by the novelty skeptic: github.com/davidryan59/rid-nopert-audit (re-runs Hervay's own Rust/Python tools; its independent checker is Python and covers only the 38 cover files) and github.com/oscardssmith/Nopert.jl (Julia + Lean, its own different 91,845-leaf certificate) | https://en.wikipedia.org/wiki/Prince_Rupert%27s_cube (HTTP 200, sha256 df13564bc42baaf790b88dcef12d1038603ecc2bc6f9c89ca79c10803e67b475) | 2026-10-31T11:33:37Z | all 192,696 records accepted, 0 rejected |

The novelty skeptic re-read the page at 2026-10-31T12:25:36Z (same bytes). Snapshot data is under `the-record-we-beat/`.

## Not claimed

- The hand-proved mathematics of the paper is not re-proved: the symmetry reduction to the domain D, the centering, zoom, tube/point/hand-over coverage lemmas as mathematics, the Bernstein lemma and the soundness of each component; only the finite exact facts they rest on were recomputed. The claim that the zoom families cover the covered sets is likewise not re-proved.
- The header `policy` hash of the certificate is not interpreted.
- Labelling conventions (vertex numbering, fold-index order, witness field roles, tree encoding) were recovered from the paper and the certificate data; each accepted record proves its own statement for the named edge, vertex, inequality or cover whatever the labelling.
- Nothing about the nine undecided solids (snub cube, snub dodecahedron, deltoidal and pentagonal hexecontahedra, J72-J75, J77). The rhombicosidodecahedron is not one of them.
- The .NET runtime, the compiler, BigInteger and the download of the pinned inputs are trusted. Not machine-checked in a proof assistant.
- The independence of the author from Hervay is by procedure (the author never opened Hervay's `proof/src` or `audit/`), not by proof; the author did read the paper and the certificate data.

## Credits

- Bence Hervay, "Non-Rupertness of the Rhombicosidodecahedron" (Zenodo, 10.5281/zenodo.23013945; https://zenodo.org/records/23013945) and the certificate and Rust/Python tools at https://github.com/bence-hervay/nopert-rid.
- Jakob Steininger and Sergey Yurkevich, "A convex polyhedron without Rupert's property", https://arxiv.org/abs/2508.18475: the method this certificate extends.
- David Ryan (davidryan59), https://github.com/davidryan59/rid-nopert-audit, and Oscar Smith (oscardssmith), https://github.com/oscardssmith/Nopert.jl: earlier audit and an independent proof, compared against.
- Scriba (1968); Jerrard, Wetzel and Yuan (2017); Chai, Yuan and Zamfirescu (2018); Hoffmann (2019); Lavau (2019); Fredriksson, https://arxiv.org/abs/2210.00601; Gosain and Grimmer, https://arxiv.org/abs/2509.08190: the Rupert problem background.
