# How the object was built (the contributor's search code)

Everything in this folder is copied from the contributor's own snapshot (taken 2026-10-19), with absolute local paths replaced by {WORKDIR} and the C include lines written with quotes instead of angle brackets. No other change was made.

Construction field of the object, in the contributor's words: "GF(4) Hermitian self-orthogonal code via weight-4 unitary transvection climb".

- `qecc_toeplitz.c`: seeds the search with a bordered Toeplitz shortened double-circulant Hermitian self-orthogonal code over GF(4) of length 23 and dimension 7.
- `qecc_transvect.c`: climbs from that seed by weight-4 Hermitian transvections over GF(4) (and, in later stages, weight-2 and weight-3 binary symplectic transvections), computing the exact quantum distance by Gray-code enumeration and the quaternary MacWilliams identity at every step. The contributor's results file says the weight-4 centralizer count reached 0 at step 12,386.

Commands: both programs take no arguments (`int main(void)`). Compile with `cc -O3 -o NAME NAME.c` (an assumption; the snapshot does not record the flags). Running them reproduces the search only in distribution: the seeds and the random state are not recorded. The final object is checked by the standalone checker in `verify-it-yourself/`.

PREREG.md: there is none. The snapshot holds no pre-registration for this search.
